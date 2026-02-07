# Traffic Monitoring Bot Walkthrough

This document outlines how to set up, run, and verify the Traffic Monitoring Bot.

## 1. Project Setup

The project uses a modular structure with a virtual environment.

### Files Created

- `main.py`: Core logic for fetching traffic data and sending alerts.
- `requirements.txt`: Python dependencies (`requests`, `python-dotenv`).
- `.env`: (Ignored by git) Stores API keys.
- `.github/workflows/traffic.yml`: GitHub Actions workflow for scheduled runs.
- `run.sh`: Helper script to run the bot with the virtual environment.

## 2. Configuration

The bot requires the following environment variables in `.env`:

- `TOMTOM_API_KEY`: From TomTom Developer Dashboard.
- `TELEGRAM_TOKEN`: From BotFather.
- `MY_CHAT_ID`: Your personal Telegram Chat ID.

## 3. Running Locally

To run the bot locally, use the helper script:

```bash
./run.sh
```

This script automatically activates the virtual environment (`.venv`) and runs `main.py`.

## 4. Verification Results

We verified the following:

- **API Connection**: The bot successfully connects to TomTom API with a 10-second timeout for reliability.
- **Route Naming**: The bot extracts street names from TomTom's guidance instructions to provide meaningful route descriptions (e.g., "Primary Route via El Nasr Street, El Wahat Road").
- **Delay Calculation**: The bot calculates delay using `trafficDelayInSeconds` from the API.
- **Alert Logic**:
  - If `trafficDelayInSeconds > 300` (5 minutes), an alert is sent.
  - If available, it suggests an alternative route with descriptive street names.
  - Recommendations include time savings when alternative routes are faster.
- **Telegram Notification**: Successfully tested with real traffic data.

## 5. Deployment

The bot is configured to run automatically on GitHub Actions:

- **Schedule**: Sunday to Thursday at 12:25 UTC.
- **Secrets**: Make sure to add `TOMTOM_API_KEY`, `TELEGRAM_TOKEN`, and `MY_CHAT_ID` to GitHub Repository Secrets.
