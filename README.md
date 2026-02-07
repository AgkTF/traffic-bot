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
- `START_COORD`: Latitude and longitude of the starting point (e.g., `"34.05,-118.24"`).
- `DESTINATION_COORD`: Latitude and longitude of the destination (e.g., `"34.00,-118.30"`).

## 3. Running Locally

To run the bot locally, use the helper script:

```bash
./run.sh
```

This script automatically activates the virtual environment (`.venv`) and runs `main.py`.

## 4. Features & Verification

We have implemented and verified the following:

- **Enhanced Messaging**:
  - **Always-Send Logic**: The bot sends a message for every run—`✅ Traffic is clear!` for normal conditions and `⚠️ Traffic Alert!` when delays exceed 5 minutes.
  - **Rich Formatting**: Uses custom names (e.g., "Daily Commute") and emojis (🚗, 📍, 🛣️, 📏, ⏱️, 🚦) for a quick overview.
  - **Google Maps Integration**: Every message includes a 🗺️ **[Open in Google Maps]** link for immediate navigation.
- **Intelligent Routing**:
  - **Route Naming**: Extracts street names from TomTom guidance (e.g., "via Ring Road") to identify routes accurately.
  - **Distance & Time**: Shows distance in kilometers and total travel time.
  - **Alternative Routes**: Automatically checks for faster alternatives during delays and provides recommendations.
- **Reliability**:
  - **Security**: Sensitive coordinates and API keys are stored in environment variables and excluded from Git history.
  - **Performance**: 10-second request timeout to prevent hanging.

## 5. Deployment

The bot is configured to run automatically on GitHub Actions:

- **Schedule**: Sunday to Thursday at 12:25 UTC.
- **Secrets**: Add `TOMTOM_API_KEY`, `TELEGRAM_TOKEN`, `MY_CHAT_ID`, `START_COORD`, and `DESTINATION_COORD` to your GitHub Repository Secrets.
