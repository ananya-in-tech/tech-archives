#!/usr/bin/env python3
"""Fetch upcoming Codeforces, LeetCode and AtCoder contests and post them to Discord.

Data is pulled directly from each platform (no third-party aggregators):
  - Codeforces: official REST API
  - LeetCode:   official GraphQL endpoint (topTwoContests)
  - AtCoder:    contest list page, upcoming table

Environment variables:
  CONTEST_WEBHOOK_URL  Discord webhook URL (required unless --dry-run)
  DSA_ROLE_ID          Discord role ID to ping (optional; no ping if unset)

Usage:
  python scripts/contest_notifier.py --mode daily
  python scripts/contest_notifier.py --mode weekly
  python scripts/contest_notifier.py --mode weekly --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

HTTP_TIMEOUT = 20
USER_AGENT = "Mozilla/5.0 (compatible; ContestNotifier/1.0; +https://github.com)"
JST = timezone(timedelta(hours=9))

MODE_WINDOWS = {
    "daily": timedelta(hours=36),
    "weekly": timedelta(days=7),
}

MODE_HEADERS = {
    "daily": "Daily Contest Briefing",
    "weekly": "Weekly Contest Digest",
}

PLATFORM_COLORS = {
    "Codeforces": 0x318CE7,
    "LeetCode": 0xF59E0B,
    "AtCoder": 0x10B981,
}

MAX_EMBEDS_PER_MESSAGE = 10
EMBED_FOOTER = "Tech Archive Discussions \u2022 Contest Radar"


@dataclass
class Contest:
    platform: str
    name: str
    url: str
    start: datetime
    duration: timedelta


def _session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def fetch_codeforces(session):
    resp = session.get(
        "https://codeforces.com/api/contest.list",
        params={"gym": "false"},
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "OK":
        raise RuntimeError(f"Codeforces API returned status {data.get('status')}: {data.get('comment')}")

    contests = []
    for item in data.get("result", []):
        if item.get("phase") != "BEFORE" or "startTimeSeconds" not in item:
            continue
        contests.append(
            Contest(
                platform="Codeforces",
                name=item["name"],
                url=f"https://codeforces.com/contests/{item['id']}",
                start=datetime.fromtimestamp(item["startTimeSeconds"], tz=timezone.utc),
                duration=timedelta(seconds=item.get("durationSeconds", 0)),
            )
        )
    return contests


def fetch_leetcode(session):
    query = """
    query topTwoContests {
      topTwoContests {
        title
        titleSlug
        startTime
        duration
      }
    }
    """
    resp = session.post(
        "https://leetcode.com/graphql",
        json={"query": query, "operationName": "topTwoContests", "variables": {}},
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/contest/",
        },
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("errors"):
        raise RuntimeError(f"LeetCode GraphQL errors: {payload['errors']}")

    contests = []
    for item in (payload.get("data") or {}).get("topTwoContests") or []:
        contests.append(
            Contest(
                platform="LeetCode",
                name=item["title"],
                url=f"https://leetcode.com/contest/{item['titleSlug']}",
                start=datetime.fromtimestamp(int(item["startTime"]), tz=timezone.utc),
                duration=timedelta(seconds=int(item.get("duration") or 0)),
            )
        )
    return contests


ATCODER_ISO_PATTERN = re.compile(r"iso=(\d{8}T\d{4})")


def _parse_atcoder_duration(text):
    # Durations are shown as HH:MM, where HH can exceed 24 for long contests.
    match = re.match(r"^\s*(\d+):(\d{2})\s*$", text)
    if not match:
        return timedelta(0)
    return timedelta(hours=int(match.group(1)), minutes=int(match.group(2)))


def fetch_atcoder(session):
    resp = session.get(
        "https://atcoder.jp/contests/",
        params={"lang": "en"},
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    table = soup.select_one("#contest-table-upcoming")
    if table is None:
        return []

    contests = []
    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        time_link = cells[0].find("a", href=ATCODER_ISO_PATTERN)
        if time_link is None:
            continue
        iso_value = ATCODER_ISO_PATTERN.search(time_link["href"]).group(1)
        start_jst = datetime.strptime(iso_value, "%Y%m%dT%H%M").replace(tzinfo=JST)

        contest_link = cells[1].find("a", href=re.compile(r"^/contests/"))
        if contest_link is None:
            continue

        contests.append(
            Contest(
                platform="AtCoder",
                name=contest_link.get_text(strip=True),
                url="https://atcoder.jp" + contest_link["href"],
                start=start_jst.astimezone(timezone.utc),
                duration=_parse_atcoder_duration(cells[2].get_text()),
            )
        )
    return contests


FETCHERS = {
    "Codeforces": fetch_codeforces,
    "LeetCode": fetch_leetcode,
    "AtCoder": fetch_atcoder,
}


def collect_contests(mode):
    now = datetime.now(timezone.utc)
    window_end = now + MODE_WINDOWS[mode]
    session = _session()

    collected = []
    failures = []
    for platform, fetcher in FETCHERS.items():
        try:
            results = fetcher(session)
        except Exception as exc:  # One platform failing must not block the others.
            print(f"[warn] {platform} fetch failed: {exc}", file=sys.stderr)
            failures.append(platform)
            continue
        in_window = [c for c in results if now <= c.start <= window_end]
        print(f"[info] {platform}: {len(results)} upcoming, {len(in_window)} within {mode} window")
        collected.extend(in_window)

    collected.sort(key=lambda c: c.start)
    return collected, failures


def _format_hours(duration):
    hours = round(duration.total_seconds() / 3600, 2)
    return f"{hours:g} hours" if hours != 1 else "1 hour"


def build_embed(contest):
    unix_ts = int(contest.start.timestamp())
    return {
        "title": contest.name,
        "url": contest.url,
        "color": PLATFORM_COLORS[contest.platform],
        "author": {"name": contest.platform},
        "fields": [
            {
                "name": "\U0001F552 Start Time",
                "value": f"<t:{unix_ts}:F> (<t:{unix_ts}:R>)",
                "inline": False,
            },
            {
                "name": "\u23F3 Duration",
                "value": _format_hours(contest.duration),
                "inline": True,
            },
        ],
        "footer": {"text": EMBED_FOOTER},
    }


def build_payloads(contests, mode, role_id):
    header = MODE_HEADERS[mode]
    embeds = [build_embed(c) for c in contests]
    chunks = [embeds[i:i + MAX_EMBEDS_PER_MESSAGE] for i in range(0, len(embeds), MAX_EMBEDS_PER_MESSAGE)]

    payloads = []
    for index, chunk in enumerate(chunks):
        if index == 0:
            mention = f"<@&{role_id}> " if role_id else ""
            content = f"{mention}\U0001F3C6 **{header}** | {len(contests)} upcoming contest(s)"
            allowed_mentions = {"parse": [], "roles": [role_id] if role_id else []}
        else:
            content = f"**{header}** (continued)"
            allowed_mentions = {"parse": []}
        payloads.append({"content": content, "embeds": chunk, "allowed_mentions": allowed_mentions})
    return payloads


def post_to_discord(webhook_url, payload, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        resp = requests.post(webhook_url, json=payload, timeout=HTTP_TIMEOUT)
        if resp.status_code == 429:
            retry_after = float(resp.json().get("retry_after", 1))
            print(f"[warn] Discord rate limited, retrying in {retry_after}s")
            time.sleep(retry_after)
            continue
        if resp.status_code >= 400:
            raise RuntimeError(f"Discord webhook returned {resp.status_code}: {resp.text[:300]}")
        return
    raise RuntimeError("Discord webhook still rate limited after retries")


def parse_args():
    parser = argparse.ArgumentParser(description="Send upcoming contest alerts to Discord.")
    parser.add_argument("--mode", choices=sorted(MODE_WINDOWS), default="daily")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the Discord payloads instead of sending them.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    webhook_url = os.environ.get("CONTEST_WEBHOOK_URL", "").strip()
    role_id = os.environ.get("DSA_ROLE_ID", "").strip()

    if not webhook_url and not args.dry_run:
        print("[error] CONTEST_WEBHOOK_URL is not set.", file=sys.stderr)
        return 1
    if role_id and not role_id.isdigit():
        print("[error] DSA_ROLE_ID must be a numeric Discord role ID.", file=sys.stderr)
        return 1

    contests, failures = collect_contests(args.mode)
    if len(failures) == len(FETCHERS):
        print("[error] All platform fetches failed.", file=sys.stderr)
        return 1
    if not contests:
        print(f"[info] No contests within the {args.mode} window. Nothing to send.")
        return 0

    payloads = build_payloads(contests, args.mode, role_id)
    for payload in payloads:
        if args.dry_run:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            post_to_discord(webhook_url, payload)
    print(f"[info] Prepared {len(contests)} contest(s) in {len(payloads)} message(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
