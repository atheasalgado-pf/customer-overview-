import json
import subprocess
import os

# Load Data
with open('indicators_data.json', 'r') as f:
    indicators = json.load(f)

try:
    with open('features_full.json', 'r') as f:
        features_raw = json.load(f).get('values', [])
except:
    features_raw = []

tech_stack = {}
for row in features_raw:
    if len(row) > 1:
        name = row[1].strip()
        tech_stack[name] = {
            "MAP": row[3] if len(row) > 3 else "Unknown",
            "Webhook": row[8] if len(row) > 8 else "Unknown",
            "Intent": row[10] if len(row) > 10 else "Unknown",
            "PFRI": row[20] if len(row) > 20 else "Unknown",
            "SFDC_Sync": row[22] if len(row) > 22 else "Unknown"
        }

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
matrix_id = "18soPmgZ41c0-d92OnDFliNtyko6-DLRdagNcT-x6b_A"
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
    "PWC": "PWC", "Amplitude": "Amplitude", "Appgate": "Appgate",
    "Egencia": "Egencia"
}

summary_stats = {
    "health": {"Healthy": 0, "Risk": 0, "Needs Review": 0, "Stale": 0},
    "alignment": {"Aligned": 0, "MISMATCH": 0},
    "recs": [],
    "total_accounts": 0,
    "engagement_delta": 0
}

# --- UPDATE INDIVIDUAL TABS AND COLLECT SUMMARY DATA ---
try:
    with open('customers.json', 'r') as f:
        target_customers = json.load(f)
except:
    target_customers = list(indicators.keys())

for tc, data in indicators.items():
    if data is None: continue
    if tc not in target_customers: continue
    sheet_name = mapping.get(tc, tc)
    ts = next((v for k, v in tech_stack.items() if tc.lower() in k.lower()), {})
    
    recs = []
    if data.get("Total_New", 0) == 0:
        recs.append({"goal": "Modernize delivery", "action": "Migrate to Templated Experiences", "why": "Drives higher binger sessions."})
    if data.get("CF_Agents", 0) == 0:
        recs.append({"goal": "Capture anon intent", "action": "Pilot ChatFactory Agents", "why": "Uncovers intent missed by forms."})
    if data.get("Active_WT", 0) == 0:
        recs.append({"goal": "Turn traffic into leads", "action": "Deploy Guide/Concierge", "why": "Persistent content discovery."})
    if data.get("Yield", 0) < 10 and data.get("Visitors", 0) > 0:
        recs.append({"goal": "Improve yield", "action": "Enable AI Recommendations", "why": "Increases traffic conversion."})
    if ts.get("PFRI") != "TRUE" and data.get("Converted", 0) > 50:
        recs.append({"goal": "Attribute revenue", "action": "Enable PFRI", "why": "Syncs intent directly to SFDC."})
    if ts.get("Intent") and ts.get("Intent") != "N/A" and ts.get("Intent") != "Unknown":
        recs.append({"goal": "Surface ABM signals", "action": "Deploy Account Insights Tab", "why": "Visualizes intent in Salesforce."})
    if ts.get("Webhook") != "TRUE" and data.get("Visitors", 0) > 1000:
        recs.append({"goal": "Automate workflows", "action": "Configure Webhooks", "why": "Real-time behavioral alerts."})
    if data.get("Total_Old", 0) > 50 and data.get("Yield", 0) < 5:
        recs.append({"goal": "Optimize library", "action": "Run Content Inventory Audit", "why": "Identifies low-performing assets."})

    steps_str = "\n\n".join([f"GOAL: {r['goal']}\nACTION: {r['action']}\nWHY: {r['why']}" for r in recs])
    if not steps_str: steps_str = "GOAL: Scale current success.\nACTION: Optimize high-performing experiences."

    # Update individual H3
    try:
        res = subprocess.check_output([gws_path, "sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3"})], env=env).decode()
        current_h3 = json.loads(res).get("values", [[""]])[0][0].split("STRATEGIC RECOMMENDATIONS")[0].strip()
    except: current_h3 = ""
    final_h3 = f"{current_h3}\n\nSTRATEGIC RECOMMENDATIONS (Aligned to Use Case Matrix):\n{steps_str}"
    subprocess.run([gws_path, "sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3", "valueInputOption": "USER_ENTERED"}), "--json", json.dumps({"values": [[final_h3]]})], env=env, capture_output=True)

    # Collect stats for Dashboard
    try:
        pulse_res = subprocess.check_output([gws_path, "sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C3"})], env=env).decode()
        pulse = json.loads(pulse_res).get("values", [["Unknown"]])[0][0]
        summary_stats["health"][pulse] = summary_stats["health"].get(pulse, 0) + 1
    except: pass
    
    try:
        align_res = subprocess.check_output([gws_path, "sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!I3"})], env=env).decode()
        align = json.loads(align_res).get("values", [["Unknown"]])[0][0]
        if "MISMATCH" in align: summary_stats["alignment"]["MISMATCH"] += 1
        elif "Aligned" in align: summary_stats["alignment"]["Aligned"] += 1
    except: pass

    summary_stats["total_accounts"] += 1
    summary_stats["recs"].extend(recs)

# --- BUILD DETAILED OVERVIEW DASHBOARD ---
dashboard = [
    ["STRATEGIC CUSTOMER SUCCESS COMMAND CENTER", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["SECTION 1: PORTFOLIO HEALTH SNAPSHOT", "", "SECTION 2: SF PULSE ALIGNMENT (The Perception Gap)", "", "", "SECTION 3: TEAM-WIDE STRATEGIC GOALS", "", "", ""],
    ["Status", "Count", "Status", "Count", "", "Goal Outcome", "Recommended Action", "Team Count", "Strategic Priority"],
]

# Column 1 & 2: Health
health_rows = [["Healthy", summary_stats["health"]["Healthy"]], ["Risk", summary_stats["health"]["Risk"]], ["Needs Review", summary_stats["health"]["Needs Review"]], ["Stale", summary_stats["health"]["Stale"]]]
# Column 3 & 4: Alignment
align_rows = [["Aligned", summary_stats["alignment"]["Aligned"]], ["MISMATCH", summary_stats["alignment"]["MISMATCH"]]]

# Column 6, 7, 8: Top Recs
rec_counts = {}
for r in summary_stats["recs"]:
    key = (r["goal"], r["action"])
    rec_counts[key] = rec_counts.get(key, 0) + 1
sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)

for i in range(max(len(health_rows), len(sorted_recs), len(align_rows))):
    row = [""] * 9
    if i < len(health_rows):
        row[0], row[1] = health_rows[i]
    if i < len(align_rows):
        row[2], row[3] = align_rows[i]
    if i < len(sorted_recs):
        (goal, action), count = sorted_recs[i]
        row[5], row[6], row[7] = goal, action, count
        row[8] = "High" if count > 10 else "Medium"
    dashboard.append(row)

dashboard.extend([
    ["", "", "", "", "", "", "", "", ""],
    ["SECTION 4: STRATEGIC SOURCE & GOVERNANCE", "", "", "", "", "", "", "", ""],
    ["Source Matrix:", f"https://docs.google.com/spreadsheets/d/{matrix_id}/edit", "Q2 25: Use Case + Features Matrix", "", "", "", "", "", ""],
    ["Data Governance:", "Updated daily via Gemini (Soft Signals) and monthly via Customer Master (Hard Data).", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["--- INDIVIDUAL ACCOUNT ROLLUP ---", "", "", "", "", "", "", "", ""],
])

# Append the original main table
current_table_res = subprocess.check_output([gws_path, "sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:I100"})], env=env).decode()
current_table = json.loads(current_table_res).get("values", [])
# Find headers and skip previous rollup
start_idx = 0
for i, r in enumerate(current_table):
    if len(r) > 0 and r[0] == "Customer Name":
        start_idx = i
        break
main_table = current_table[start_idx:] if start_idx > 0 else current_table

full_sheet = dashboard + main_table

# Update the Summary Sheet
subprocess.run([gws_path, "sheets", "spreadsheets", "values", "clear", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:Z500"})], env=env, capture_output=True)
subprocess.run([gws_path, "sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"}), "--json", json.dumps({"values": full_sheet})], env=env, capture_output=True)

