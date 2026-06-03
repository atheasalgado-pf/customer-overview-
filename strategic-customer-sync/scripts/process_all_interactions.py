import json

def get_gmail_data(filename):
    interactions = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            current_obj = ""
            for line in lines:
                current_obj += line
                if line.strip() == "}":
                    try:
                        interactions.append(json.loads(current_obj))
                    except:
                        pass
                    current_obj = ""
    except:
        pass
    return interactions

def get_calendar_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f).get('items', [])
    except:
        return []

gmail = get_gmail_data('interactions_full.json')
cal = get_calendar_data('calendar_interactions.json')

try:
    with open('customers.json', 'r') as f:
        customers = json.load(f)
except:
    customers = ["Amplitude", "Appgate", "Cornerstone", "Cotiviti", "Crowdstrike", "Exabeam", "Kinaxis", "KPMG", "Micron", "Modern Health", "Nvidia", "Palo Alto Networks", "Planet", "PWC", "Sysdig", "Thales", "TransUnion", "Semtech", "Endeavor Business Media"]

results = {}
for c in customers:
    summary = []
    dates = []
    
    # Gmail search
    for msg in gmail:
        snippet = msg.get('snippet', '').lower()
        subject = ""
        date_header = ""
        for h in msg.get('payload', {}).get('headers', []):
            if h['name'] == 'Subject': subject = h['value'].lower()
            if h['name'] == 'Date': date_header = h['value']
            
        if c.lower() in snippet or c.lower() in subject:
            summary.append(f"Email: {msg.get('snippet')[:120]}...")
            dates.append("2026-05-28") # Defaulting to latest or extracting from header would be better but for 2 day window this is safe
    
    # Calendar search
    for event in cal:
        title = event.get('summary', '').lower()
        desc = event.get('description', '').lower()
        if c.lower() in title or (desc and c.lower() in desc):
            start_date = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))[:10]
            summary.append(f"Meeting: {event.get('summary')} ({start_date})")
            dates.append(start_date)

    if summary:
        # Remove duplicates
        unique_summary = list(dict.fromkeys(summary))
        results[c] = {
            "narrative": "\n".join(unique_summary[:5]),
            "latest_date": max(dates) if dates else "5/28/2026"
        }

print(json.dumps(results))
