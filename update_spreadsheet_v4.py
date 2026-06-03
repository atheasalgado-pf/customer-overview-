import json
import subprocess
import os

with open('processed_summary.json', 'r') as f:
    summaries = json.load(f)

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

mapping = {
    "Nvidia": "Nvidia Corporation", "Palo Alto Networks": "Palo Alto Networks",
    "Micron": "Micron Technology, Inc.", "Sysdig": "Sysdig",
    "Cornerstone": "Cornerstone On Demand", "Exabeam": "Exabeam",
    "Modern Health": "Modern Health", "Kinaxis": "Kinaxis",
    "Cotiviti": "Cotiviti", "Endeavor Business Media": "Endeavor Business Media (EBM)",
    "NinjaOne": "NinjaOne", "Planet": "Planet",
    "KPMG": "KPMG LLP (Canada)", "Semtech": "Semtech",
    "Thales": "Thales", "TransUnion": "TransUnion",
    "PWC": "PWC", "Amplitude": "Amplitude", "Appgate": "Appgate"
}

for tc, summary in summaries.items():
    sheet_name = mapping.get(tc, tc)
    print(f"Updating {sheet_name}...")
    
    # Update Last Updated Date (C1)
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C1", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["5/28/2026"]]})
    ], env=env, capture_output=True)

    # Update Last Communication (E3) and Pulse Reasoning (D3)
    # Note: I'll prepend the new summary to Pulse Reasoning if possible, or just overwrite for freshness
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!D3:E3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [[summary, "5/28/2026"]]})
    ], env=env, capture_output=True)

    # Update Status flag (B3)
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!B3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["UP TO DATE"]]})
    ], env=env, capture_output=True)

