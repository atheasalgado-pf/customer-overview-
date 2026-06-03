import json

def get_gmail_data(filename):
    interactions = []
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
    return interactions

def get_calendar_data(filename):
    with open(filename, 'r') as f:
        return json.load(f).get('items', [])

gmail = get_gmail_data('interactions_full.json')
cal = get_calendar_data('calendar_interactions.json')

customers = ["Amplitude", "Appgate", "Cornerstone", "Cotiviti", "Crowdstrike", "Exabeam", "Kinaxis", "KPMG", "Micron", "Modern Health", "Nvidia", "Palo Alto Networks", "Planet", "PWC", "Sysdig", "Thales", "TransUnion", "Semtech", "Endeavor Business Media"]

results = {}
for c in customers:
    summary = []
    # Gmail search
    for msg in gmail:
        snippet = msg.get('snippet', '').lower()
        subject = ""
        for h in msg.get('payload', {}).get('headers', []):
            if h['name'] == 'Subject':
                subject = h['value'].lower()
        if c.lower() in snippet or c.lower() in subject:
            summary.append(f"Email: {msg.get('snippet')[:100]}...")
    
    # Calendar search
    for event in cal:
        title = event.get('summary', '').lower()
        desc = event.get('description', '').lower()
        if c.lower() in title or c.lower() in desc:
            summary.append(f"Meeting: {event.get('summary')} ({event.get('start', {}).get('dateTime', '')[:10]})")

    if summary:
        results[c] = "\n".join(summary[:5])

print(json.dumps(results))
