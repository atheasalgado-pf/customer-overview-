import json
import subprocess
import os

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

# 1. Read the current sheet
res = subprocess.check_output([
    gws_path, "sheets", "spreadsheets", "values", "get",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:I200"})
], env=env).decode()
rows = json.loads(res).get("values", [])

# 2. Find the original header "Customer Name"
start_idx = -1
for i, row in enumerate(rows):
    if len(row) > 0 and row[0] == "Customer Name":
        start_idx = i
        break

if start_idx != -1:
    original_table = rows[start_idx:]
    print(f"Found original table at row {start_idx + 1}. Restoring...")
    
    # 3. Clear the sheet
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "clear",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:Z500"})
    ], env=env)
    
    # 4. Write back starting at A1
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": original_table})
    ], env=env)
    print("Restoration complete.")
else:
    print("Could not find original table headers. No changes made.")

