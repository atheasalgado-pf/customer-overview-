# Strategic Customer Intelligence Dashboard

This repository contains the automation scripts and instructions for maintaining the Strategic Customer Framework Google Sheet. It is optimized for team-wide use via the **Strategic Customer Sync** skill.

## 🚀 Overview
The system synthesizes Salesforce data (Solutions Architect assignments), product usage metrics, and Google Workspace interactions (Gmail/Calendar) into a unified strategic dashboard.

## 🛠 Features
- **Daily One-Click Sync**: Automates the entire data pipeline with a single command.
- **Advanced Intelligence**: Includes Interaction Sentiment Analysis and Jira Ticket parsing.
- **SFDC Sync**: Automatically pulls accounts assigned to the current Solutions Architect.
- **Quota Efficiency**: Uses incremental fetching to minimize API consumption.

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
   *This will check for Salesforce (`sf`) and Google Workspace (`gws`) CLIs and help you configure your Spreadsheet IDs.*

## 🔄 Standard Workflow
To refresh your dashboard with the latest activity:
```bash
python3 strategic-customer-sync/scripts/daily_sync.py
```

## 📁 Key Files
- `strategic-customer-sync/SKILL.md`: Detailed documentation of the skill logic.
- `strategic-customer-sync/scripts/setup_environment.py`: Automated setup and config tool.
- `strategic-customer-sync/scripts/daily_sync.py`: Main execution script for incremental updates.
- `UPDATE_STANDARD.md`: The "Source of Truth" for dashboard logic and field mapping.

## 🤖 Running with Gemini
Once setup, you can simply ask Gemini:
> "Run the Strategic Customer Sync for my accounts."

Gemini will utilize the `strategic-customer-sync` skill to execute the full workflow.
