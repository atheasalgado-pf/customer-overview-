import subprocess
import os
import sys
from datetime import datetime, timedelta
import json

def get_yesterday_range():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    # Gmail format: YYYY/MM/DD
    gmail_after = yesterday.strftime("%Y/%m/%d")
    # Calendar format: RFC3339
    cal_min = yesterday.strftime("%Y-%m-%dT00:00:00Z")
    return gmail_after, cal_min

def run_command(cmd, shell=False):
    print(f"Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        subprocess.run(cmd, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def main():
    print("--- Strategic Customer Sync: Daily Incremental Update ---")
    
    gmail_after, cal_min = get_yesterday_range()
    
    # 1. Fetch Fresh Data (Incremental)
    # We use a 2-day window for Gmail to ensure we don't miss late-night threads
    lookback_date = (datetime.now() - timedelta(days=2)).strftime("%Y/%m/%d")
    
    print(f"Step 1: Fetching Gmail and Calendar activity since {lookback_date}...")
    
    gmail_cmd = [
        "gws", "gmail", "users", "messages", "list", 
        "--params", json.dumps({"q": f"after:{lookback_date}", "userId": "me"}), 
        "--page-all"
    ]
    
    # Note: Using redirection in shell for gws output
    with open("interactions_full.json", "w") as f:
        subprocess.run(gmail_cmd, stdout=f, check=True)

    cal_cmd = [
        "gws", "calendar", "events", "list", 
        "--params", json.dumps({"calendarId": "primary", "timeMin": cal_min})
    ]
    with open("calendar_interactions.json", "w") as f:
        subprocess.run(cal_cmd, stdout=f, check=True)

    # 2. Run Processing Scripts
    print("\nStep 2: Processing intelligence...")
    if not run_command(["python3", "strategic-customer-sync/scripts/process_all_interactions.py"]):
        sys.exit(1)
    
    if not run_command(["python3", "strategic-customer-sync/scripts/process_jira_tickets.py"]):
        print("Warning: Jira ticket processing failed.")
    
    if not run_command(["python3", "strategic-customer-sync/scripts/analyze_sentiment.py"]):
        print("Warning: Sentiment analysis failed.")
    
    if not run_command(["python3", "strategic-customer-sync/scripts/extract_indicators.py"]):
        sys.exit(1)

    # 3. Update Spreadsheet
    print("\nStep 3: Synchronizing to Google Sheets...")
    if not run_command(["python3", "strategic-customer-sync/scripts/update_broad_strategy.py"]):
        sys.exit(1)

    print("\n[SUCCESS] Daily sync complete. Dashboard is up to date.")

if __name__ == "__main__":
    main()
