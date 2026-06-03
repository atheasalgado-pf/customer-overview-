---
name: strategic-customer-sync
description: Synchronizes customer data from Salesforce, analyzes usage and interactions, and updates the Strategic Customer Framework dashboard. Use when a Solutions Architect needs to refresh their account recommendations and health narratives based on SFDC, Gmail, and product data.
---

# Strategic Customer Sync

This skill automates the workflow for Solutions Architects to maintain their Strategic Customer Overview dashboards.

## Workflow

1. **Sync Salesforce Accounts**: Detects the current user and pulls all assigned accounts where they are the Solutions Architect.
2. **Analyze Interaction Activity**: Scans Gmail and Calendar to generate narratives of recent customer touchpoints.
3. **Extract Usage Indicators**: Calculates key health metrics (Yield, Adoption) from product data.
4. **Generate Strategic Recommendations**: Maps metrics to the [Use Case Matrix](references/use-case-matrix.md) and pushes updates to Google Sheets.

## Prerequisite Data
This skill requires the following files to be present in the workspace:
- `det_data.json`: Monthly product usage export.
- `interactions_full.json`: Recent Gmail/Calendar interaction dump.

## Commands & Scripts

### 1. Sync from SFDC
Run the sync script to generate `customers.json`.
```bash
python3 scripts/sync_sfdc_accounts.py
```

### 2. Process Interactions
Generate health narratives based on the synced customer list.
```bash
python3 scripts/process_all_interactions.py
```

### 3. Extract Metrics
Calculate indicators from `det_data.json`.
```bash
python3 scripts/extract_indicators.py
```

### 4. Update Spreadsheet
Push all data to the target spreadsheet.
```bash
python3 scripts/update_broad_strategy_v3.py
```

## Strategy Reference
For details on how "Goals" and "Actions" are derived from data, see [references/use-case-matrix.md](references/use-case-matrix.md).
