import json
import subprocess
import os

def get_current_user_name():
    try:
        res = subprocess.check_output(["sf", "data", "query", "--query", "SELECT Name FROM User WHERE Username = (SELECT Username FROM User WHERE Id = (SELECT Id FROM User LIMIT 1))", "--json"]).decode()
        # This is a hacky way to get current user if sf org display fails or is complex
        # Better: use sf org display
        res = subprocess.check_output(["sf", "org", "display", "--json"]).decode()
        username = json.loads(res).get("result", {}).get("username")
        
        user_res = subprocess.check_output(["sf", "data", "query", "--query", f"SELECT Name FROM User WHERE Username = '{username}'", "--json"]).decode()
        return json.loads(user_res).get("result", {}).get("records", [{}])[0].get("Name")
    except:
        return None

def sync_accounts(user_name):
    if not user_name:
        print("Error: Could not determine Salesforce user name.")
        return
    
    print(f"Syncing accounts for Solutions Architect: {user_name}...")
    query = f"SELECT Name FROM Account WHERE Solutions_Architect_Full_Name__c = '{user_name}'"
    
    try:
        res = subprocess.check_output(["sf", "data", "query", "--query", query, "--json"]).decode()
        records = json.loads(res).get("result", {}).get("records", [])
        customers = [r["Name"] for r in records]
        
        with open('customers.json', 'w') as f:
            json.dump(customers, f)
        
        print(f"Successfully synced {len(customers)} accounts to customers.json")
        return customers
    except Exception as e:
        print(f"Error syncing from SFDC: {e}")
        return []

if __name__ == "__main__":
    name = get_current_user_name()
    sync_accounts(name)
