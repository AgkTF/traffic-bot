# Project Mission: Modular Traffic Monitor

**Objective:** Create a Python-based automation to monitor travel times between two points using real-time traffic data, notifying me via Telegram if delays occur.

## Core Requirements

1. **Language:** Python 3.10+
2. **APIs:** - TomTom Routing API (Traffic data)
   - Telegram Bot API (Notifications)
3. **Modular Logic**
   - The script should use a single **Start Point** and a single **End Point**.
   - It should query the TomTom API for the **Two Best Alternative Routes** between these points.
   - Route A = The "Primary" (shortest/fastest usually).
   - Route B = The "Alternative" (the next best option).
   - **Trigger:** If Route A has a delay > 5 minutes AND Route B is currently faster, suggest Route B.
4. **Notification Trigger:**
   - If the delay on the primary route > 5 minutes, send a Telegram alert.
   - The alert must state the current travel time for both routes and suggest the faster one.
5. **Security:** - Use `os.getenv` for all credentials (`TOMTOM_API_KEY`, `TELEGRAM_TOKEN`, `MY_CHAT_ID`).
6. **Infrastructure:** - Minimal `requirements.txt` (e.g., `requests`).
   - GitHub Actions workflow (`.github/workflows/traffic.yml`).

## Scheduling (Egypt Work Week)

- **Schedule:** Sunday to Thursday.
- **Timing:** 02:25 PM Cairo Time (12:25 UTC).
- **Cron Expression:** `25 12 * * 0-4`
  _(Note: 0 is Sunday, 4 is Thursday in GitHub cron syntax)._

## Definition of Done

- `main.py` is modular and allows switching points by simply changing variables.
- GitHub Action runs on the Sun-Thu schedule.
- A README provides instructions on how to set secrets in GitHub.
