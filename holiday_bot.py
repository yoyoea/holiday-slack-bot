import os
import requests
from datetime import date, datetime

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
CALENDARIFIC_API_KEY = os.environ["CALENDARIFIC_API_KEY"]

COUNTRIES = ["CA", "US", "NL", "IN", "CN", "SE"]
TARGET_OFFSETS = {
    1: "in 1 day",
    3: "in 3 days",
    7: "in 7 days",
}

def get_holidays(country_code, year):
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": CALENDARIFIC_API_KEY,
        "country": country_code,
        "year": year,
        "type": "national",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data["response"]["holidays"]

def send_to_slack(message):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=20,
    )
    response.raise_for_status()

def build_matches():
    today = date.today()
    years_to_check = {today.year, today.year + 1}
    matches = []

    for country in COUNTRIES:
        for year in years_to_check:
            holidays = get_holidays(country, year)

            for holiday in holidays:
                holiday_date = datetime.fromisoformat(holiday["date"]["iso"]).date()
                days_until = (holiday_date - today).days

                if days_until in TARGET_OFFSETS:
                    holiday_name = holiday["name"]
                    timing = TARGET_OFFSETS[days_until]
                    matches.append(
                        f"• {country} — {holiday_name} ({timing}) on {holiday_date.isoformat()}"
                    )

    return matches

def main():
    matches = build_matches()
    print("Matches found:", matches, flush=True)

    if matches:
        message = "🌏 Upcoming Bank Holiday Reminder\n\n" + "\n".join(matches)
        send_to_slack(message)
    else:
        print("No matching holidays found.", flush=True)

if __name__ == "__main__":
    main()
