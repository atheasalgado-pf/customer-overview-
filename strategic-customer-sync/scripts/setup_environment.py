import subprocess
import os
import sys
import json

def check_command(cmd):
    try:
        subprocess.check_output([cmd, "--version"], stderr=subprocess.STDOUT)
        return True
    except:
        return False

def setup():
    print("--- Strategic Customer Sync: Environment Setup ---")
    
    # 1. Check Dependencies
    deps = {"gws": "Google Workspace CLI", "sf": "Salesforce CLI", "python3": "Python 3"}
    missing = []
    for cmd, name in deps.items():
        if check_command(cmd):
            print(f"[OK] {name} found.")
        else:
            print(f"[MISSING] {name} not found in PATH.")
            missing.append(name)
    
    if missing:
        print("\nPlease install the missing dependencies before proceeding.")
        sys.exit(1)

    # 2. Setup Config
    config_template = "strategic-customer-sync/scripts/config.json.template"
    config_file = "strategic-customer-sync/scripts/config.json"
    
    if not os.path.exists(config_file):
        print(f"\nCreating {config_file} from template...")
        try:
            with open(config_template, 'r') as f:
                config = json.load(f)
            
            # Ask for Spreadsheet ID
            ss_id = input("Enter your Strategic Customer Spreadsheet ID: ").strip()
            if ss_id:
                config["spreadsheet_id"] = ss_id
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"[OK] Config created.")
        except Exception as e:
            print(f"[ERROR] Could not create config: {e}")
    else:
        print(f"\n[OK] {config_file} already exists.")

    # 3. Check Authentication
    print("\nChecking authentications...")
    # sf
    try:
        res = subprocess.check_output(["sf", "org", "display", "--json"], stderr=subprocess.DEVNULL)
        print("[OK] Salesforce CLI authenticated.")
    except:
        print("[WARNING] Salesforce CLI not authenticated. Run 'sf org login web'.")

    # gws
    try:
        # Just try to list drive files with limit 1
        subprocess.check_output(["gws", "drive", "files", "list", "--params", '{"pageSize": 1}'], stderr=subprocess.DEVNULL)
        print("[OK] Google Workspace CLI (gws) authenticated.")
    except:
        print("[WARNING] gws not authenticated. Run 'gws auth login'.")

    print("\nSetup complete. You can now use the skill.")

if __name__ == "__main__":
    setup()
