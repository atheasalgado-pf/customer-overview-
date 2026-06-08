import subprocess
import os
import sys
from datetime import datetime, timedelta
import json

def get_date_range(days):
    today = datetime.now()
    lookback = today - timedelta(days=days)
    # Gmail format: YYYY/MM/DD
    gmail_after = lookback.strftime("%Y/%m/%d")
    # Calendar format: RFC3339
    cal_min = lookback.strftime("%Y-%m-%dT00:00:00Z")
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
    # 0. Handle Arguments
    lookback_days = 1
    if len(sys.argv) > 1:
        try:
            lookback_days = int(sys.argv[1])
        except ValueError:
            print(f"Warning: Invalid days '{sys.argv[1]}'. Defaulting to 1 day.")

    print(f"--- Strategic Customer Sync: {lookback_days}-Day Incremental Update ---")
    
    gmail_after, cal_min = get_date_range(lookback_days)
    
    # 1. Fetch Fresh Data (Incremental)
    # Use an extra day for Gmail safety to capture overnight threads
    gmail_buffer_date = (datetime.now() - timedelta(days=lookback_days + 1)).strftime("%Y/%m/%d")
    
    print(f"Step 1: Fetching Gmail and Calendar activity since {lookback_days} days ago...")
    
    gmail_cmd = [
        "gws", "gmail", "users", "messages", "list", 
        "--params", json.dumps({"q": f"after:{gmail_buffer_date}", "userId": "me"}), 
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

    # NEW: Sync Shared Intelligence
    print("\nStep 1b: Syncing Shared Intelligence from team folder...")
    run_command(["python3", "strategic-customer-sync/scripts/sync_shared_intel.py"])

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
