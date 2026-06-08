import json
import re
import os

def parse_jira_emails(gmail_data):
    jira_results = {}
    
    # Common Jira email patterns
    # Example: [JIRA] (PROD-1234) Created: ...
    # Example: [JIRA] (PROD-1234) Status: In Progress
    ticket_pattern = re.compile(r'\[JIRA\]\s*\((?P<id>[A-Z]+-\d+)\)')
    status_pattern = re.compile(r'Status:\s*(?P<status>[A-Za-z\s]+)')

    for msg in gmail_data:
        snippet = msg.get('snippet', '')
        subject = ""
        for h in msg.get('payload', {}).get('headers', []):
            if h['name'] == 'Subject': subject = h['value']
        
        full_text = f"{subject} {snippet}"
        
        if "[JIRA]" in full_text:
            ticket_match = ticket_pattern.search(full_text)
            if ticket_match:
                ticket_id = ticket_match.group('id')
                status_match = status_pattern.search(full_text)
                status = status_match.group('status').strip() if status_match else "Updated"
                
                # Link this ticket to a customer by searching the text for customer names
                # This requires the customers.json list
                jira_results[ticket_id] = {
                    "id": ticket_id,
                    "status": status,
                    "raw": full_text[:200]
                }
    
    return jira_results

def associate_tickets_with_customers(jira_tickets, customers):
    customer_jira = {c: [] for c in customers}
    
    for ticket_id, info in jira_tickets.items():
        text = info['raw'].lower()
        for c in customers:
            if c.lower() in text:
                customer_jira[c].append(f"{ticket_id} ({info['status']})")
    
    return customer_jira

def main():
    try:
        with open('interactions_full.json', 'r') as f:
            gmail_data = [json.loads(line) for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading Gmail data: {e}")
        return

    try:
        with open('customers.json', 'r') as f:
            customers = json.load(f)
    except:
        print("Error: customers.json not found.")
        return

    jira_tickets = parse_jira_emails(gmail_data)
    customer_mapping = associate_tickets_with_customers(jira_tickets, customers)
    
    with open('jira_data.json', 'w') as f:
        json.dump(customer_mapping, f, indent=4)
    
    print(f"Extracted {len(jira_tickets)} Jira ticket updates for {len(customer_mapping)} customers.")

if __name__ == "__main__":
    main()
