import json
import subprocess
import os

with open('final_processed_summary.json', 'r') as f:
    summaries = json.load(f)

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

mapping = {
    "Nvidia": "Nvidia Corporation", 
    "Palo Alto Networks": "Palo Alto Networks",
    "Micron": "Micron Technology, Inc.", 
    "Sysdig": "Sysdig",
    "Cornerstone": "Cornerstone On Demand", 
    "Exabeam": "Exabeam",
    "Modern Health": "Modern Health", 
    "Kinaxis": "Kinaxis",
    "Cotiviti": "Cotiviti", 
    "Endeavor Business Media": "Endeavor Business Media (EBM)",
    "NinjaOne": "NinjaOne", 
    "Planet": "Planet",
    "KPMG": "KPMG LLP (Canada)", 
    "Semtech": "Semtech",
    "Thales": "Thales", 
    "TransUnion": "TransUnion",
    "PWC": "PWC", 
    "Amplitude": "Amplitude", 
    "Appgate": "Appgate",
    "Appgate CyberSecurity Inc": "Appgate",
    "Scaled Agile": "ScaledAgile",
    "Thales Group": "Thales",
    "Cornerstone OnDemand Inc": "Cornerstone On Demand",
    "Micron Technology, Inc.": "Micron Technology, Inc.",
    "KPMG LLP (Canada)": "KPMG LLP (Canada)",
    "Nvidia Corporation": "Nvidia Corporation"
}

for tc, data in summaries.items():
    sheet_name = mapping.get(tc, tc)
    print(f"Updating {sheet_name} with interactions from June 1-5...")
    
    new_interactions = data["narrative"]
    latest_comm = data["latest_date"]
    
    # 1. Read current Pulse Reasoning (D3) to preserve engagement flags
    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!D3"})
        ], env=env).decode()
        current_reasoning = json.loads(res).get("values", [[""]])[0][0]
    except:
        current_reasoning = ""

    # Check if these interactions are already in the reasoning to avoid duplication
    if "Meeting:" not in current_reasoning and "Email:" not in current_reasoning and "Task:" not in current_reasoning:
        updated_reasoning = f"{new_interactions}\n\n{current_reasoning}".strip()
    else:
        # Just update with fresh data at the top if it's new
        updated_reasoning = f"LATEST ACTIVITY (June 1-5):\n{new_interactions}\n\n{current_reasoning}".strip()

    # 2. Perform Batch Update for C1, B3, D3, E3
    # C1: Last Updated Date
    # B3: Update Status?
    # D3: Pulse Reasoning
    # E3: Last Communication
    
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C1", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["6/5/2026"]]})
    ], env=env, capture_output=True)

    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!B3:E3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["UP TO DATE", "Healthy" if "Risk" not in current_reasoning else "Risk", updated_reasoning, latest_comm]]})
    ], env=env, capture_output=True)

print("Batch update complete.")
