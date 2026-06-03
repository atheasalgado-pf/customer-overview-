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

# 2. Get Overview Data
with open('overview_data.json', 'r') as f:
    overview_rows = json.load(f)['values']

headers = overview_rows[0]
if "SF Pulse Alignment" not in headers:
    headers.append("SF Pulse Alignment")

updated_overview = [headers]
customer_mapping = {
    "Nvidia Corporation": "Nvidia", "Palo Alto Networks": "Palo Alto Networks",
    "Micron Technology, Inc.": "Micron", "Sysdig": "Sysdig",
    "Cornerstone On Demand": "Cornerstone", "Exabeam": "Exabeam",
    "Modern Health": "Modern Health", "Kinaxis": "Kinaxis",
    "Cotiviti": "Cotiviti", "Endeavor Business Media (EBM)": "Endeavor Business Media",
    "NinjaOne": "NinjaOne", "Planet": "Planet",
    "KPMG LLP (Canada)": "KPMG", "Semtech": "Semtech",
    "Thales": "Thales", "TransUnion": "TransUnion",
    "PWC": "PWC", "Amplitude": "Amplitude", "Appgate": "Appgate",
    "Egencia": "Egencia"
}

# Flip mapping for easier lookup
sheet_to_sf = {v: k for k, v in customer_mapping.items()}

for row in overview_rows[1:]:
    if not row or not row[0]: continue
    cust_name = row[0].strip()
    tech_pulse = row[2].strip() if len(row) > 2 else "Unknown"
    
    # Match to SF Pulse
    sf_key = next((v for k, v in sf_pulses.items() if cust_name.lower() in k.lower() or k.lower() in cust_name.lower()), None)
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

    # Update row for overview
    if len(row) < 10:
        row.extend([""] * (10 - len(row)))
    row[9] = alignment # Col J
    updated_overview.append(row)
    
    # 3. Update individual tab
    sheet_name = cust_name # Sheet names match column A in overview usually
    # (Checking mapping just in case)
    mapped_sheet = next((v for k, v in customer_mapping.items() if cust_name.lower() in k.lower()), cust_name)
    
    print(f"Updating alignment for {mapped_sheet}...")
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{mapped_sheet}'!I2:I3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [["SF Pulse Alignment"], [alignment]]})
    ], env=env, capture_output=True)

# 4. Write back to Overview tab
subprocess.run([
    gws_path, "sheets", "spreadsheets", "values", "update",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"}),
    "--json", json.dumps({"values": updated_overview})
], env=env, capture_output=True)

