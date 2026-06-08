import json

def process_interactions():
    try:
        with open('sf_events.json', 'r') as f:
            events_raw = json.load(f).get('result', {}).get('records', [])
    except:
        events_raw = []
        
    try:
        with open('sf_tasks.json', 'r') as f:
            tasks_raw = json.load(f).get('result', {}).get('records', [])
    except:
        tasks_raw = []

    results = {}
    
    # Process Events
    for e in events_raw:
        acc_name = e.get('Account', {}).get('Name')
        if not acc_name: continue
        
        subject = e.get('Subject', 'No Subject')
        date = e.get('StartDateTime', '')[:10]
        
        if acc_name not in results:
            results[acc_name] = []
        
        results[acc_name].append(f"Meeting: {subject} ({date})")

    # Process Tasks
    for t in tasks_raw:
        acc_name = t.get('Account', {}).get('Name')
        if not acc_name: continue
        
        subject = t.get('Subject', 'No Subject')
        date = t.get('CreatedDate', '')[:10]
        
        if acc_name not in results:
            results[acc_name] = []
        
        results[acc_name].append(f"Task: {subject} ({date})")

    # Format narratives
    final_results = {}
    for acc, comms in results.items():
        # Unique and sorted by date (reverse)
        unique_comms = sorted(list(set(comms)), reverse=True)
        final_results[acc] = "\n".join(unique_comms[:5])

    with open('processed_interactions.json', 'w') as f:
        json.dump(final_results, f)
    
    print(f"Processed interactions for {len(final_results)} accounts.")

if __name__ == "__main__":
    process_interactions()
