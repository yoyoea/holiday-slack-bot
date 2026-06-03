import os
import requests
from datetime import date, timedelta

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

COUNTRIES = ["CA", "US", "NL", "GB", "CN", "SE" ]

def get_holidays(country_code, year):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    response = requests.get(url)
    return response.json()

def send_to_slack(message):
    requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message}
    )

today = date.today()
seven_days_later = today + timedelta(days=7)

matches = []

for country in COUNTRIES:
    holidays = get_holidays(country, today.year)

    for holiday in holidays:
        holiday_date = holiday["date"]

        if holiday_date == today.isoformat():
            matches.append(
                f"• {country} — {holiday['name']} TODAY"
            )

        if holiday_date == seven_days_later.isoformat():
            matches.append(
                f"• {country} — {holiday['name']} in 7 days"
            )

if matches:
    message = "🌏 Upcoming Bank Holiday Reminder\n\n"
    message += "\n".join(matches)

    send_to_slack(message)
