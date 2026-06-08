# 🧠 Strategic Customer Sync: Technical Guide

This skill is a modular "Signals Engine" that transforms Salesforce data, product usage metrics, and Google Workspace interactions into rolling strategic dashboards.

## 📁 File Roles & Logic (How it Works)

### 1. The Core Workflow
- **`daily_sync.py [days]`**: The conductor. It accepts an optional "lookback" argument (default 1 day). It coordinates the fetching of fresh data and triggers the intelligence pipeline.
- **`setup_environment.py`**: The onboarding wizard. It verifies your CLI authentications and creates your personal `config.json`.
- **`schedule_me.py`**: The auto-scheduler. It sets a 2:00 AM "alarm" in your system (crontab) to run the sync while you sleep, protecting your daytime API quota.

### 2. Data Extractors
- **`sync_sfdc_accounts.py`**: Automatically identifies your assigned accounts. It only re-queries Salesforce once every 7 days (Smart Sync) to minimize API usage.
- **`process_all_interactions.py`**: The narrative detector. It extracts recent email and meeting snippets. 
    - **Primary Contact Extraction**: It scans headers to identify the *exact person* you last spoke with at the customer, which is then pushed to row 5 of your dashboard.
- **`extract_indicators.py`**: The metrics engine.
    - **Engagement Velocity**: It compares current usage against the previous sync. If engagement (Yield) drops by **>20%**, it triggers a `⚠️ Declining` warning.

### 3. Intelligence Layers
- **`process_jira_tickets.py`**: Uses regex to extract ticket IDs and statuses (e.g., *Blocked*) directly from your inbox.
- **`analyze_sentiment.py`**: Classifies the tone of interactions as *Positive*, *Neutral*, or *Concerned*.
- **`sync_shared_intel.py`**: Downloads the team's "Collective Brain" from the Solutions Team shared folder.

### 4. The Executioner
- **`update_broad_strategy.py`**: The final script that writes to Google Sheets.
    - **Technical Pulse (C3)**: Automatically downgrades accounts to "Needs Review" if sentiment is poor, engagement is declining, or Jira blockers exist.
    - **Smart Projects (Row 5)**: Automatically detects and lists active technical projects (e.g., *PostMessage*, *API Migration*) based on keyword detection.

## 🌐 Shared Intelligence (Collaborative Rules)

Any JSON file placed in the **Solutions Team Shared Folder** (`170rqQMfovdREHydGYnj6ZTwNtQhgbdQW`) is automatically merged into everyone's sync.

- **Shared Pulse Rules**: Define new "Red Flags" for the whole team.
- **Shared Recommendations**: Share a technical solution once, and everyone's AI will suggest it when a similar customer pattern is detected.

## 🛡️ Quota Optimization
This system is strictly incremental. It fetches dozens of recent items instead of thousands, and gates heavy "Product Data" refreshes to a monthly cadence.

---

## 🚀 Setup & Usage Guide

To use this skill across the team, follow these steps:

### 1. Prerequisites
- **Python 3.8+**
- **Salesforce CLI (`sf`)**: Authenticated to your org (`sf org login web`).
- **Google Workspace CLI (`gws`)**: Authenticated (`gws auth login`).

### 2. Environment Setup
Clone the repository and run the setup script:
```bash
# Install Python dependencies
pip install -r strategic-customer-sync/requirements.txt

# Run the setup wizard
python3 strategic-customer-sync/scripts/setup_environment.py
```

### 3. Workflow
To sync your dashboard manually:
```bash
python3 strategic-customer-sync/scripts/daily_sync.py [optional_days_lookback]
```

To schedule the sync for 2:00 AM (Recommended):
```bash
python3 strategic-customer-sync/scripts/schedule_me.py
```
