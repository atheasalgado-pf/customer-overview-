import json
import subprocess
import os
import sys

def get_current_user_name():
    """Fetches the current user's full name from Salesforce CLI."""
    try:
        # First, try to get the default username
        res = subprocess.check_output(["sf", "org", "display", "--json"], stderr=subprocess.DEVNULL).decode()
        username = json.loads(res).get("result", {}).get("username")
        
        if not username:
            return None

        # Then, query for the Full Name
        user_res = subprocess.check_output(["sf", "data", "query", "--query", f"SELECT Name FROM User WHERE Username = '{username}'", "--json"], stderr=subprocess.DEVNULL).decode()
        return json.loads(user_res).get("result", {}).get("records", [{}])[0].get("Name")
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return None

def sync_accounts(user_name):
    """Syncs accounts assigned to the specified Solutions Architect."""
    if not user_name:
        print("Error: Could not determine Salesforce user name. Make sure 'sf' is authenticated.")
        sys.exit(1)
    
    print(f"Syncing accounts for Solutions Architect: {user_name}...")
    
    # Field name could vary by org, consider making this configurable
    sa_field = os.environ.get("SF_SA_FIELD", "Solutions_Architect_Full_Name__c")
    query = f"SELECT Name FROM Account WHERE {sa_field} = '{user_name}'"
    
    try:
        res = subprocess.check_output(["sf", "data", "query", "--query", query, "--json"]).decode()
        records = json.loads(res).get("result", {}).get("records", [])
        customers = [r["Name"] for r in records]
        
        output_file = 'customers.json'
        with open(output_file, 'w') as f:
            json.dump(customers, f, indent=4)
        
        print(f"Successfully synced {len(customers)} accounts to {output_file}")
        return customers
    except subprocess.CalledProcessError as e:
        print(f"Error querying Salesforce: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Allow overriding user name via env var or arg
    name = os.environ.get("SA_FULL_NAME") or (sys.argv[1] if len(sys.argv) > 1 else get_current_user_name())
    sync_accounts(name)
