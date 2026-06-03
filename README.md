# Strategic Customer Intelligence Dashboard

This repository contains the automation scripts and instructions for maintaining the Strategic Customer Framework Google Sheet.

## 🚀 Overview
The system synthesizes Salesforce data (Solutions Architect assignments), product usage metrics, and Google Workspace interactions (Gmail/Calendar) into a unified strategic dashboard.

## 🛠 Features
- **SFDC Sync**: Automatically pulls accounts assigned to the current Solutions Architect.
- **Usage Indicators**: Calculates "Yield" and "Adoption" metrics from product data.
- **Interaction Summary**: Scans Gmail and Calendar to provide a narrative of recent customer touchpoints.
- **Strategic Recommendations**: Maps data to the Q2 Use Case Matrix to suggest automated "Goal -> Action" plans.

## 📋 Setup
1. **Clone the Repo**:
   ```bash
   git clone <your-repo-url>
   cd customer-overview
   ```
2. **Install Dependencies**:
   - Install the [Salesforce CLI](https://developer.salesforce.com/tools/sfdxcli).
   - Install the [Google Workspace CLI (gws)](https://github.com/google/gemini-cli).
   - Ensure Python 3 is installed.
3. **Authentication**:
   - `sf auth login`
   - `gws auth login`

## 🤖 Running with Gemini
Once setup, you can simply ask Gemini:
> "Refresh my Strategic Dashboard from Salesforce."

Gemini will read the `GEMINI.md` file in this repo and execute the full sync and update workflow.

## 📁 File Structure
- `sync_sfdc_accounts.py`: Pulls your assigned accounts from Salesforce.
- `extract_indicators.py`: Processes product usage data (`det_data.json`).
- `process_all_interactions.py`: Summarizes Gmail and Calendar events.
- `update_broad_strategy_v3.py`: Pushes updates and recommendations to Google Sheets.
