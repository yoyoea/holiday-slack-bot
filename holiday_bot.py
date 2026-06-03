import os
import requests
from datetime import date, timedelta

print("Script started", flush=True)

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
COUNTRIES = ["SG", "US", "JP", "GB"]

def send_to_slack(message):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=20,
    )
    print("Slack status:", response.status_code, flush=True)
    print("Slack response:", response.text, flush=True)
    response.raise_for_status()

def get_holidays(country_code, year):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()

today = date.today()
three_days_later = today + timedelta(days=3)

matches = []

for country in COUNTRIES:
    holidays = get_holidays(country, today.year)

    for holiday in holidays:
        holiday_date = holiday["date"]

        if holiday_date == today.isoformat():
            matches.append(f"• {country} — {holiday['name']} TODAY")

        if holiday_date == three_days_later.isoformat():
            matches.append(f"• {country} — {holiday['name']} in 3 days")

print("Matches found:", matches, flush=True)

send_to_slack("✅ Slack bot test successful")
print("Message sent", flush=True)
