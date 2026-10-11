import os
import requests
from datetime import datetime, timezone

WEBHOOK_URL = os.getenv("CONTEST_WEBHOOK_URL")
ROLE_ID = "1555946767084949594"  # DSA Learner Role ID

# API endpoints for CP platforms
PLATFORMS = {
    "Codeforces": "https://kontests.net/api/v1/code_forces",
    "LeetCode": "https://kontests.net/api/v1/leet_code",
    "AtCoder": "https://kontests.net/api/v1/at_coder",
}

# Branding colors for Discord embeds
COLORS = {
    "Codeforces": 0x318CE7,  # Blue
    "LeetCode": 0xF59E0B,    # Amber/Yellow
    "AtCoder": 0x000000,     # Black
}

def fetch_contests():
    upcoming = []
    for platform, url in PLATFORMS.items():
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for contest in data:
                    if contest.get("status") == "BEFORE":
                        upcoming.append({
                            "platform": platform,
                            "name": contest.get("name"),
                            "url": contest.get("url"),
                            "start_time": contest.get("start_time"),
                            "duration": float(contest.get("duration", 0)),
                        })
        except Exception as e:
            print(f"Error fetching {platform}: {e}")
    return upcoming

def parse_iso_time(time_str):
    dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    return int(dt.timestamp())

def send_discord_alert(contests):
    if not WEBHOOK_URL:
        print("No Webhook URL found.")
        return

    if not contests:
        print("No upcoming contests found in the window.")
        return

    embeds = []
    for c in contests[:10]:
        start_unix = parse_iso_time(c["start_time"])
        duration_hrs = round(c["duration"] / 3600, 1)

        embeds.append({
            "title": f"🏆 {c['platform']}: {c['name']}",
            "url": c["url"],
            "color": COLORS.get(c["platform"], 0x7289DA),
            "fields": [
                {"name": "⏰ Start Time", "value": f"<t:{start_unix}:F> (<t:{start_unix}:R>)", "inline": True},
                {"name": "⏱️ Duration", "value": f"{duration_hrs} hours", "inline": True},
            ],
            "footer": {"text": "Tech Archive Discussions • Contest Alert"},
        })

    payload = {
        "content": f"🚨 **Upcoming Competitive Programming & LeetCode Contests!** <@&{ROLE_ID}>",
        "embeds": embeds,
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Notification sent with status code: {response.status_code}")

if __name__ == "__main__":
    contests = fetch_contests()
    send_discord_alert(contests)import os
import requests
from datetime import datetime, timezone

WEBHOOK_URL = os.getenv("CONTEST_WEBHOOK_URL")
ROLE_ID = "1555946767084949594"  # DSA Learner Role ID

# API endpoints for CP platforms
PLATFORMS = {
    "Codeforces": "https://kontests.net/api/v1/code_forces",
    "LeetCode": "https://kontests.net/api/v1/leet_code",
    "AtCoder": "https://kontests.net/api/v1/at_coder",
}

# Branding colors for Discord embeds
COLORS = {
    "Codeforces": 0x318CE7,  # Blue
    "LeetCode": 0xF59E0B,    # Amber/Yellow
    "AtCoder": 0x000000,     # Black
}

def fetch_contests():
    upcoming = []
    for platform, url in PLATFORMS.items():
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                for contest in data:
                    if contest.get("status") == "BEFORE":
                        upcoming.append({
                            "platform": platform,
                            "name": contest.get("name"),
                            "url": contest.get("url"),
                            "start_time": contest.get("start_time"),
                            "duration": float(contest.get("duration", 0)),
                        })
        except Exception as e:
            print(f"Error fetching {platform}: {e}")
    return upcoming

def parse_iso_time(time_str):
    dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    return int(dt.timestamp())

def send_discord_alert(contests):
    if not WEBHOOK_URL:
        print("No Webhook URL found.")
        return

    if not contests:
        print("No upcoming contests found in the window.")
        return

    embeds = []
    for c in contests[:10]:
        start_unix = parse_iso_time(c["start_time"])
        duration_hrs = round(c["duration"] / 3600, 1)

        embeds.append({
            "title": f"🏆 {c['platform']}: {c['name']}",
            "url": c["url"],
            "color": COLORS.get(c["platform"], 0x7289DA),
            "fields": [
                {"name": "⏰ Start Time", "value": f"<t:{start_unix}:F> (<t:{start_unix}:R>)", "inline": True},
                {"name": "⏱️ Duration", "value": f"{duration_hrs} hours", "inline": True},
            ],
            "footer": {"text": "Tech Archive Discussions • Contest Alert"},
        })

    payload = {
        "content": f"🚨 **Upcoming Competitive Programming & LeetCode Contests!** <@&{ROLE_ID}>",
        "embeds": embeds,
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Notification sent with status code: {response.status_code}")

if __name__ == "__main__":
    contests = fetch_contests()
    send_discord_alert(contests)
