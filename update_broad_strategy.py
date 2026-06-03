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

# Process Features
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

summary_stats = {"total": 0, "recs": []}

for tc, data in indicators.items():
    if data is None: continue
    sheet_name = mapping.get(tc, tc)
    print(f"Strategic Update for {sheet_name}...")
    
    ts = next((v for k, v in tech_stack.items() if tc.lower() in k.lower()), {})
    
    recs = []
    
    # 1. NEW UX MIGRATION
    if data.get("Total_New", 0) == 0:
        recs.append({
            "goal": "Modernize content delivery and increase 'Binger' sessions.",
            "action": "Migrate legacy tracks to Templated Experiences.",
            "why": "Templated experiences drive higher engagement through visual, guided journeys that reduce bounce rates compared to legacy tracks."
        })
    
    # 2. CHATFACTORY
    if data.get("CF_Agents", 0) == 0:
        recs.append({
            "goal": "Capture anonymous buyer intent.",
            "action": "Pilot ChatFactory Agents.",
            "why": "AI-powered conversations engage unknown visitors earlier, uncovering intent signals that static forms miss."
        })
    
    # 3. WEBTOOLS
    if data.get("Active_WT", 0) == 0:
        recs.append({
            "goal": "Turn website traffic into qualified leads.",
            "action": "Deploy Guide/Concierge widgets.",
            "why": "Persistent content discovery at entry points ensures visitors are always one click away from their 'Next Best Content'."
        })
    
    # 4. YIELD / AI
    if data.get("Yield", 0) < 10 and data.get("Visitors", 0) > 0:
        recs.append({
            "goal": "Improve visitor-to-engagement efficiency.",
            "action": "Enable AI-Powered Content Recommendations.",
            "why": "Machine learning identifies individual interests to dynamically surface relevant assets, increasing the percentage of traffic that converts into engaged sessions."
        })
    
    # 5. REVENUE INTELLIGENCE (PFRI)
    if ts.get("PFRI") != "TRUE" and data.get("Converted", 0) > 50:
        recs.append({
            "goal": "Attribute content consumption to pipeline.",
            "action": "Enable PathFactory for Revenue Intelligence (PFRI).",
            "why": "Syncing engagement data directly into Salesforce helps sales teams prioritize follow-up based on actual intent scores."
        })

    # 6. ACCOUNT INSIGHTS (ABM)
    if ts.get("Intent") and ts.get("Intent") != "N/A" and ts.get("Intent") != "Unknown":
        recs.append({
            "goal": "Surface buyer intent for Sales & ABM teams.",
            "action": "Deploy the Account Insights Tab in Salesforce.",
            "why": "Aggregating content engagement at the account level allows reps to see readiness signals for target accounts instantly."
        })

    # 7. WEBHOOKS / AUTOMATION
    if ts.get("Webhook") != "TRUE" and data.get("Visitors", 0) > 1000:
        recs.append({
            "goal": "Automate data flow to third-party systems.",
            "action": "Configure Event-Driven Webhooks.",
            "why": "Triggers real-time alerts or workflows in external tools based on specific high-value behaviors (e.g., a 'Binger' session)."
        })

    # 8. CONTENT INVENTORY
    if data.get("Total_Old", 0) > 50 and data.get("Yield", 0) < 5:
        recs.append({
            "goal": "Audit content effectiveness.",
            "action": "Run a Content Inventory Report.",
            "why": "Identifies underutilized assets so the team can optimize the library and retire low-performing content."
        })

    steps_str = "\n\n".join([f"GOAL: {r['goal']}\nACTION: {r['action']}\nWHY: {r['why']}" for r in recs])
    if not steps_str:
        steps_str = "GOAL: Scale current success.\nACTION: Optimize high-performing experiences.\nWHY: Maintaining current engagement levels requires continuous iteration of top-performing assets."

    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3"})
        ], env=env).decode()
        current_val = json.loads(res).get("values", [[""]])[0][0]
        clean_val = current_val.split("STRATEGIC RECOMMENDATIONS")[0].strip()
    except:
        clean_val = ""
    
    final_h3 = f"{clean_val}\n\nSTRATEGIC RECOMMENDATIONS (Aligned to Use Case Matrix):\n{steps_str}"
    
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [[final_h3]]})
    ], env=env, capture_output=True)

    summary_stats["total"] += 1
    summary_stats["recs"].extend([r["action"] for r in recs])

# --- UPDATE SUMMARY TAB ---
rec_counts = {x: summary_stats["recs"].count(x) for x in set(summary_stats["recs"])}
sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)

summary_header = [
    ["STRATEGIC OVERVIEW SUMMARY", "", "", "", "", "", "", "", ""],
    ["Source Matrix:", f"https://docs.google.com/spreadsheets/d/{matrix_id}/edit", "", "", "", "", "", "", ""],
    ["Top Team Actions:", "Count", "Outcome Goal", "", "", "", "", "", ""],
]

for rec_action, count in sorted_recs[:5]:
    goal = ""
    if "Migrate" in rec_action: goal = "Modernize delivery"
    elif "ChatFactory" in rec_action: goal = "Capture anon intent"
    elif "Guide" in rec_action: goal = "Turn traffic into leads"
    elif "AI-Powered" in rec_action: goal = "Improve traffic yield"
    elif "PFRI" in rec_action: goal = "Attribute revenue"
    elif "Account Insights" in rec_action: goal = "Surface ABM signals"
    elif "Webhooks" in rec_action: goal = "Automate workflows"
    elif "Inventory" in rec_action: goal = "Optimize library"
    
    summary_header.append([rec_action, count, goal, "", "", "", "", "", ""])

summary_header.append(["", "", "", "", "", "", "", "", ""])

current_table_res = subprocess.check_output([
    gws_path, "sheets", "spreadsheets", "values", "get",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:I100"})
], env=env).decode()
current_table = json.loads(current_table_res).get("values", [])

# Find first row that isn't empty and has 'Customer Name'
# Or just overwrite since I'm adding rows at the top.
# To be safe, I'll clear the sheet and write the new version.

full_summary_tab = summary_header + current_table

# Clear sheet first to avoid messy overlaps
subprocess.run([
    gws_path, "sheets", "spreadsheets", "values", "clear",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:Z500"})
], env=env, capture_output=True)

subprocess.run([
    gws_path, "sheets", "spreadsheets", "values", "update",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"}),
    "--json", json.dumps({"values": full_summary_tab})
], env=env, capture_output=True)

