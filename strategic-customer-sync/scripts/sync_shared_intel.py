import json
import os
import subprocess
from datetime import datetime

def load_shared_intel(gws_path, shared_folder_id, env):
    """
    Downloads and merges all JSON files from the shared intelligence folder.
    This creates a local 'brain' of team-contributed strategies.
    """
    print(f"Syncing shared intelligence from folder: {shared_folder_id}...")
    
    # 1. List files in the shared folder
    try:
        res = subprocess.check_output([
            gws_path, "drive", "files", "list", 
            "--params", json.dumps({"q": f"'{shared_folder_id}' in parents and mimeType = 'application/json'", "fields": "files(id, name)"})
        ], env=env).decode()
        files = json.loads(res).get("files", [])
    except Exception as e:
        print(f"Warning: Could not list shared folder: {e}")
        return {}

    combined_intel = {
        "technical_pulse_rules": [],
        "strategic_recommendations": []
    }

    # 2. Download and merge each file
    for f in files:
        try:
            print(f"  Downloading {f['name']}...")
            content = subprocess.check_output([
                gws_path, "drive", "files", "get", 
                "--params", json.dumps({"fileId": f['id'], "alt": "media"})
            ], env=env).decode()
            
            data = json.loads(content)
            # Merge logic
            if "technical_pulse_rules" in data:
                combined_intel["technical_pulse_rules"].extend(data["technical_pulse_rules"])
            if "strategic_recommendations" in data:
                combined_intel["strategic_recommendations"].extend(data["strategic_recommendations"])
                
        except Exception as e:
            print(f"  Error processing {f['name']}: {e}")

    return combined_intel

def save_local_intel(intel):
    with open('shared_intel_cache.json', 'w') as f:
        json.dump(intel, f, indent=4)
    print("Shared intelligence cached locally.")

if __name__ == "__main__":
    # Configuration
    CONFIG_PATH = os.environ.get("SYNC_CONFIG_PATH", "strategic-customer-sync/scripts/config.json")
    if not os.path.exists(CONFIG_PATH):
        CONFIG_PATH = "scripts/config.json"
        
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except:
        print(f"Error: Config not found at {CONFIG_PATH}")
        sys.exit(1)

    shared_folder_id = config.get("shared_folder_id")
    if not shared_folder_id:
        print("No shared intelligence folder configured. Skipping.")
        sys.exit(0)

    gws_path = os.environ.get("GWS_PATH", "gws")
    env = os.environ.copy()
    env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

    intel = load_shared_intel(gws_path, shared_folder_id, env)
    save_local_intel(intel)
