import os
import argparse
import requests
from datetime import datetime, timezone, timedelta

WEBHOOK_URL = os.getenv("CONTEST_WEBHOOK_URL")
ROLE_ID = os.getenv("ROLE_ID")

PLATFORMS = {
    "Codeforces": "https://kontests.net/api/v1/code_forces",
    "LeetCode": "https://kontests.net/api/v1/leet_code",
    "AtCoder": "https://kontests.net/api/v1/at_coder",
}

COLORS = {
    "Codeforces": 0x318CE7,  # Blue
    "LeetCode": 0xF59E0B,    # Amber
    "AtCoder": 0x10B981,     # Green
}

def parse_iso_time(time_str):
    return datetime.fromisoformat(time_str.replace("Z", "+00:00"))

def fetch_contests(mode="daily"):
    now = datetime.now(timezone.utc)
    # 36-hour lookahead for daily briefing; 7-day lookahead for weekly digest
    time_window = timedelta(hours=36) if mode == "daily" else timedelta(days=7)

    upcoming = []
    for platform, url in PLATFORMS.items():
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for contest in data:
                    start_dt = parse_iso_time(contest.get("start_time"))
                    if now <= start_dt <= (now + time_window):
                        upcoming.append({
                            "platform": platform,
                            "name": contest.get("name"),
                            "url": contest.get("url"),
                            "start_dt": start_dt,
                            "duration": float(contest.get("duration", 0)),
                        })
        except Exception as e:
            print(f"Error fetching {platform}: {e}")

    # Sort chronologically by start time
    upcoming.sort(key=lambda x: x["start_dt"])
    return upcoming

def send_discord_alert(contests, mode="daily"):
    if not WEBHOOK_URL:
        print("Error: CONTEST_WEBHOOK_URL secret is missing.")
        return

    if not contests:
        print(f"No upcoming contests found for {mode} mode.")
        return

    embeds = []
    for c in contests[:10]:  # Cap at 10 embeds per message to honor Discord limits
        start_unix = int(c["start_dt"].timestamp())
        duration_hrs = round(c["duration"] / 3600, 1)

        embeds.append({
            "title": f"🏆 {c['platform']}: {c['name']}",
            "url": c["url"],
            "color": COLORS.get(c["platform"], 0x7289DA),
            "fields": [
                {"name": "⏰ Start Time", "value": f"<t:{start_unix}:F> (<t:{start_unix}:R>)", "inline": True},
                {"name": "⏱️ Duration", "value": f"{duration_hrs} hours", "inline": True},
            ],
            "footer": {"text": "Tech Archive Discussions • Contest Radar"},
        })

    header_text = (
        "🌅 **Daily Contest Briefing (Next 24–36 Hours)**"
        if mode == "daily"
        else "📅 **Weekly Contest Digest (Next 7 Days)**"
    )

    role_mention = f"<@&{ROLE_ID}>" if ROLE_ID else ""

    payload = {
        "content": f"{header_text} {role_mention}".strip(),
        "embeds": embeds,
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Notification sent ({mode}) with status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily")
    args = parser.parse_args()

    contests = fetch_contests(mode=args.mode)
    send_discord_alert(contests, mode=args.mode)
