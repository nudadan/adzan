import os
import json
from datetime import datetime, date
from typing import Dict

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - simple dependency check
    raise SystemExit(
        "Module 'requests' not installed. Install with 'pip install requests'."
    )

try:
    from crontab import CronTab
except ModuleNotFoundError:  # pragma: no cover - simple dependency check
    raise SystemExit(
        "Module 'python-crontab' not installed. Install with 'pip install python-crontab'."
    )

# Configuration
CITY = "Bandung"
COUNTRY = "Indonesia"
METHOD = 2  # method id for Aladhan (can be adjusted)
CRON_COMMENT = "adzan_schedule"
OUTPUT_FILE = "jadwal_sholat.json"

# Determine base directory for mp3 files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADZAN_SUBUH = os.path.join(BASE_DIR, "adzan_subuh.mp3")
ADZAN_UMUM = os.path.join(BASE_DIR, "adzan_umum.mp3")

API_URL = "https://api.aladhan.com/v1/timingsByCity"


def fetch_prayer_times() -> Dict[str, str]:
    """Fetch prayer times for today from Aladhan API."""
    params = {"city": CITY, "country": COUNTRY, "method": METHOD}
    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    timings = data["data"]["timings"]
    return {
        "Subuh": timings["Fajr"],
        "Dzuhur": timings["Dhuhr"],
        "Ashar": timings["Asr"],
        "Maghrib": timings["Maghrib"],
        "Isya": timings["Isha"],
    }


def save_schedule(schedule: Dict[str, str]):
    """Save prayer times to local JSON file."""
    payload = {"date": date.today().isoformat(), "schedule": schedule}
    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f, indent=2)


def update_cron(schedule: Dict[str, str]):
    """Update crontab entries for adzan playback."""
    cron = CronTab(user=True)
    cron.remove_all(comment=CRON_COMMENT)

    for name, time_str in schedule.items():
        hour, minute = [int(x) for x in time_str.split(":" )[:2]]
        mp3 = ADZAN_SUBUH if name.lower() == "subuh" else ADZAN_UMUM
        command = f'mpg123 "{mp3}"'
        job = cron.new(command=command, comment=CRON_COMMENT)
        job.minute.on(minute)
        job.hour.on(hour)

    cron.write()


def main():
    schedule = fetch_prayer_times()
    save_schedule(schedule)
    update_cron(schedule)
    print("Jadwal adzan berhasil diperbarui")


if __name__ == "__main__":
    main()
