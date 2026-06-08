# Strategic Customer Intelligence Dashboard

This repository contains the automation scripts and instructions for maintaining the Strategic Customer Framework Google Sheet. It is optimized for team-wide use via the **Strategic Customer Sync** skill.

## 🚀 Overview
The system transforms Salesforce data, product usage metrics, and Google Workspace interactions into a unified strategic dashboard. It uses a **modular intelligence pipeline** to automatically assess account health and recommend next steps.

## 🧠 Advanced Features
- **Daily One-Click Sync**: Automates data fetching, analysis, and spreadsheet updates.
- **Engagement Velocity**: Detects and warns about declining usage trends.
- **Dynamic Contact Extraction**: Identifies the primary stakeholder for technical projects directly from interactions.
- **Shared Team Intelligence**: Syncs collaborative rules and recommendations from a shared Google Drive folder.
- **Auto-Scheduling**: Runs automatically at 2:00 AM to protect your daily API quota.

## 🚀 Team Setup
To set up your environment, follow these steps:

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/atheasalgado-pf/customer-overview-.git
   cd customer-overview
   ```
2. **Install Python Dependencies**:
   ```bash
   pip install -r strategic-customer-sync/requirements.txt
   ```
3. **Run the Setup Wizard**:
   ```bash
   python3 strategic-customer-sync/scripts/setup_environment.py
   ```
   *This will check for Salesforce (`sf`) and Google Workspace (`gws`) CLIs and help you configure your Spreadsheet ID and the team's Shared Intelligence folder.*

4. **Schedule the Daily Sync**:
   ```bash
   python3 strategic-customer-sync/scripts/schedule_me.py
   ```

## 🔄 Standard Workflow
To refresh your dashboard manually with a specific lookback window (e.g., last 3 days):
```bash
python3 strategic-customer-sync/scripts/daily_sync.py 3
```

## 📁 Key Documentation
- **[SKILL.md](./strategic-customer-sync/SKILL.md)**: Detailed technical guide on file roles and intelligence logic.
- **[UPDATE_STANDARD.md](./UPDATE_STANDARD.md)**: The "Source of Truth" for dashboard field mapping and logic standards.

## 🤖 Running with Gemini
Once setup, you can simply ask Gemini:
> "Run the Strategic Customer Sync for my accounts."

Gemini will utilize the `strategic-customer-sync` skill to execute the full pipeline.
