import json
import os
import sys
from datetime import datetime, timedelta

def get_gmail_data(filename):
    """Parses NDJSON from Gmail data."""
    interactions = []
    if not os.path.exists(filename):
        return interactions
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        interactions.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Warning: Error reading {filename}: {e}")
    return interactions

def get_calendar_data(filename):
    """Parses JSON from Calendar data."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f).get('items', [])
    except Exception as e:
        print(f"Warning: Error reading {filename}: {e}")
        return []

def main():
    gmail_file = os.environ.get('GMAIL_DATA', 'interactions_full.json')
    cal_file = os.environ.get('CALENDAR_DATA', 'calendar_interactions.json')
    customers_file = os.environ.get('CUSTOMERS_FILE', 'customers.json')

    gmail = get_gmail_data(gmail_file)
    cal = get_calendar_data(cal_file)

    if not os.path.exists(customers_file):
        print(f"Error: {customers_file} not found. Please run sync_sfdc_accounts.py first.")
        sys.exit(1)

    with open(customers_file, 'r') as f:
        customers = json.load(f)

    today = datetime.now()
    two_weeks_ago = today - timedelta(days=14)
    
    results = {}
    for c in customers:
        summary = []
        dates = []
        
            # Gmail search
            for msg in gmail:
                snippet = msg.get('snippet', '').lower()
                subject = ""
                msg_date = None
                from_contact = "Unknown"
                
                for h in msg.get('payload', {}).get('headers', []):
                    if h['name'] == 'Subject': subject = h['value'].lower()
                    if h['name'] == 'From': from_contact = h['value']
                    if h['name'] == 'Date':
                        try:
                            # Simple date parsing, might need adjustment for complex headers
                            date_str = " ".join(h['value'].split()[:4])
                            msg_date = datetime.strptime(date_str, "%a, %d %b %Y")
                        except:
                            pass
                
                if c.lower() in snippet or c.lower() in subject:
                    summary.append(f"Email: {msg.get('snippet')[:120]}...")
                    if msg_date:
                        dates.append((msg_date, from_contact))
            
            # Calendar search
            for event in cal:
                title = event.get('summary', '').lower()
                desc = event.get('description', '').lower()
                if c.lower() in title or (desc and c.lower() in desc):
                    start_raw = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
                    if start_raw:
                        start_date_str = start_raw[:10]
                        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                        
                        # Get attendees as contacts
                        attendees = [a.get('email', 'Attendee') for a in event.get('attendees', []) if not a.get('self')]
                        contact = attendees[0] if attendees else "Meeting Invite"
                        
                        summary.append(f"Meeting: {event.get('summary')} ({start_date_str})")
                        dates.append((start_date, contact))

            if summary:
                unique_summary = list(dict.fromkeys(summary))
                # Sort dates to find the absolute latest contact
                dates.sort(key=lambda x: x[0], reverse=True)
                latest_date_obj, latest_contact = dates[0]
                
                results[c] = {
                    "narrative": "\n".join(unique_summary[:5]),
                    "latest_date": latest_date_obj.strftime("%Y-%m-%d"),
                    "primary_contact": latest_contact
                }

    output_file = 'processed_summary.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"Processed interactions for {len(results)} active customers. Saved to {output_file}")

if __name__ == "__main__":
    main()
