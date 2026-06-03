import json
import subprocess
import os

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

# 1. Get Master SF Pulses
with open('master_data.json', 'r') as f:
    master_rows = json.load(f)['values']
sf_pulses = {}
for row in master_rows[4:]:
    if len(row) > 14:
        name = row[4].strip()
        pulse = row[14].strip()
        sf_pulses[name] = pulse

# 2. Get Sheet Titles
with open('sheet_titles.json', 'r') as f:
    sheets = json.load(f).get('sheets', [])
sheet_titles = [s['properties']['title'] for s in sheets]

# 3. Get Overview Data
with open('full_overview.json', 'r') as f:
    overview_rows = json.load(f)['values']

# Correct Headers
headers = ["Customer Name", "Update Status?", "Technical Pulse", "Pulse Reasoning", "Last Communication", "Active Project(s)", "Jira Tickets + Status", "Suggested Next Steps", "Link", "SF Pulse Alignment"]

updated_overview = [headers]

for row in overview_rows[1:]:
    if not row or not row[0]: continue
    cust_name = row[0].strip()
    tech_pulse = row[2].strip() if len(row) > 2 else "Unknown"
    
    # Match to SF Pulse
    sf_key = next((k for k in sf_pulses if cust_name.lower() in k.lower() or k.lower() in cust_name.lower()), None)
    sf_pulse = sf_pulses.get(sf_key, "Unknown")
    
    alignment = "Aligned"
    if tech_pulse == "Risk" and sf_pulse in ["Ideal", "Managed"]:
        alignment = f"MISMATCH: Tech Risk vs SF {sf_pulse}"
    elif tech_pulse == "Healthy" and sf_pulse == "Escalation":
        alignment = f"MISMATCH: Tech Healthy vs SF Escalation"
    elif tech_pulse == "Needs Review" and sf_pulse == "Ideal":
        alignment = f"MISMATCH: Tech Needs Review vs SF Ideal"
    else:
        alignment = f"Aligned (SF: {sf_pulse})"

    # Find the correct sheet name for the link
    # (Usually it's the customer name, but some are mapped)
    link_name = next((s for s in sheet_titles if cust_name.lower() in s.lower() or s.lower() in cust_name.lower()), cust_name)
    
    # Rebuild the row correctly
    # Name, Status, Tech, Reasoning, Comm, Projects, Jira, NextSteps, Link, Alignment
    new_row = [
        row[0], 
        row[1] if len(row) > 1 else "",
        row[2] if len(row) > 2 else "",
        row[3] if len(row) > 3 else "",
        row[4] if len(row) > 4 else "",
        row[5] if len(row) > 5 else "",
        row[6] if len(row) > 6 else "",
        row[7] if len(row) > 7 else "",
        link_name,
        alignment
    ]
    updated_overview.append(new_row)
    
    # 4. Update individual tab
    print(f"Updating alignment for sheet: {link_name}...")
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{link_name}'!I2:I3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["SF Pulse Alignment"], [alignment]]})
    ], env=env, capture_output=True)

# 5. Write back to Overview tab
subprocess.run([
    gws_path, "sheets", "spreadsheets", "values", "update",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"}),
    "--json", json.dumps({"values": updated_overview})
], env=env, capture_output=True)

