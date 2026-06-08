---
name: strategic-customer-sync
description: Synchronizes customer data from Salesforce, analyzes usage and interactions, and updates the Strategic Customer Framework dashboard with rolling intelligence.
---

# Strategic Customer Sync

This skill automates the maintenance of Strategic Customer Overview dashboards. It pulls account assignments from Salesforce, crawls recent interactions (Gmail/Calendar), extracts usage metrics, and rolls everything up into a centralized dashboard.

## 🚀 Replicability & Setup

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

# Run the setup wizard to check dependencies and configure Spreadsheet IDs
python3 strategic-customer-sync/scripts/setup_environment.py
```

### 3. Configuration
All IDs and customer name mappings are stored in `strategic-customer-sync/scripts/config.json`. If a customer name in Salesforce doesn't match the Tab name in Google Sheets, add it to the `customer_mapping` section.

## 🔄 Standard Workflow

### Option A: The "One-Click" Daily Sync (Recommended)
This command automates the entire pipeline for "Yesterday's" activity. It's the most quota-efficient way to stay up to date.
```bash
python3 strategic-customer-sync/scripts/daily_sync.py
```

### Option B: Granular Manual Steps
Run these in order if you need to perform a deep-crawl or troubleshooting:
...
## 🛡️ Quota Optimization & Efficiency

This skill is designed to minimize API consumption and respect Google Workspace quotas:

- **Incremental Fetching**: The `daily_sync.py` script uses narrow `after:` filters for Gmail and `timeMin` for Calendar. Instead of crawling thousands of emails, it only fetches the dozens from the last 24-48 hours.
- **Rollup Logic**: The script only updates the individual customer tabs that have *new* activity. The "Command Center" dashboard is rebuilt only once at the end of the process.
- **Gated Usage Sync**: Product usage metrics (`det_data.json`) are massive. The skill is configured to only update these **Monthly** unless a manual refresh is triggered, saving significant Sheets API write quota.
- **Selective Crawling**: It only searches for accounts assigned to you in Salesforce, ignoring the rest of the company's data.

## 📋 Enforced Output Schema
- **Technical Pulse (C3)**: Healthy / Needs Review / Stale.
- **Pulse Reasoning (D3)**: 1 Strategic sentence + Max 3 bullets of recent activity.
- **Jira Tickets (G3)**: Only references existing tickets + status from [JIRA] emails.

## Reference
See [UPDATE_STANDARD.md](../UPDATE_STANDARD.md) for logic definitions and field maps.
