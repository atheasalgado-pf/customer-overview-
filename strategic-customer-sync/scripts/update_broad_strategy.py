import json
import subprocess
import os
import sys
from datetime import datetime

# Configuration
CONFIG_PATH = os.environ.get("SYNC_CONFIG_PATH", "scripts/config.json")
if not os.path.exists(CONFIG_PATH):
    # Fallback to local scripts folder if running from root
    CONFIG_PATH = "strategic-customer-sync/scripts/config.json"
    if not os.path.exists(CONFIG_PATH):
        CONFIG_PATH = "strategic-customer-sync/scripts/config.json.template"

try:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error loading config from {CONFIG_PATH}: {e}")
    sys.exit(1)

spreadsheet_id = os.environ.get("STRATEGIC_SHEET_ID", config.get("spreadsheet_id"))
matrix_id = config.get("matrix_id", "18soPmgZ41c0-d92OnDFliNtyko6-DLRdagNcT-x6b_A")
gws_path = os.environ.get("GWS_PATH", "gws") # Assume in PATH
mapping = config.get("customer_mapping", {})

env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

def run_gws_command(args, json_input=None):
    cmd = [gws_path] + args
    try:
        if json_input:
            res = subprocess.check_output(cmd + ["--json", json.dumps(json_input)], env=env).decode()
        else:
            res = subprocess.check_output(cmd, env=env).decode()
        return json.loads(res) if res.strip() else {}
    except subprocess.CalledProcessError as e:
        print(f"GWS Command Failed: {' '.join(cmd)}")
        print(f"Error: {e.output.decode() if e.output else e}")
        return None
    except json.JSONDecodeError:
        return {}

# Load Data
try:
    with open('indicators_data.json', 'r') as f:
        indicators = json.load(f)
except FileNotFoundError:
    print("Error: indicators_data.json not found. Run extract_indicators.py first.")
    sys.exit(1)

try:
    with open('processed_summary.json', 'r') as f:
        narratives = json.load(f)
except:
    narratives = {}

try:
    with open('jira_data.json', 'r') as f:
        jira_data = json.load(f)
except:
    jira_data = {}

try:
    with open('sentiment_data.json', 'r') as f:
        sentiment_data = json.load(f)
except:
    sentiment_data = {}

# NEW: Shared Intelligence
try:
    with open('shared_intel_cache.json', 'r') as f:
        shared_intel = json.load(f)
except:
    shared_intel = {"technical_pulse_rules": [], "strategic_recommendations": []}

# Tech Stack Fetch (from a specific features sheet if available)
tech_stack = {}
features_raw = run_gws_command(["sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": matrix_id, "range": "Features!A1:Z500"})])
if features_raw and 'values' in features_raw:
    for row in features_raw['values']:
        if len(row) > 1:
            name = row[1].strip()
            tech_stack[name] = {
                "MAP": row[3] if len(row) > 3 else "Unknown",
                "Webhook": row[8] if len(row) > 8 else "Unknown",
                "Intent": row[10] if len(row) > 10 else "Unknown",
                "PFRI": row[20] if len(row) > 20 else "Unknown",
                "SFDC_Sync": row[22] if len(row) > 22 else "Unknown"
            }

summary_stats = {
    "health": {"Healthy": 0, "Risk": 0, "Needs Review": 0, "Stale": 0},
    "alignment": {"Aligned": 0, "MISMATCH": 0},
    "recs": [],
    "total_accounts": 0
}

today_str = datetime.now().strftime("%m/%d/%Y")

# --- UPDATE INDIVIDUAL TABS ---
try:
    with open('customers.json', 'r') as f:
        target_customers = json.load(f)
except:
    target_customers = list(indicators.keys())

for tc in target_customers:
    data = indicators.get(tc)
    if data is None: continue
    
    sheet_name = mapping.get(tc, tc)
    ts = next((v for k, v in tech_stack.items() if tc.lower() in k.lower()), {})
    narrative = narratives.get(tc, {}).get("narrative", "No recent activity recorded.")
    latest_comm = narratives.get(tc, {}).get("latest_date", today_str)
    primary_contact = narratives.get(tc, {}).get("primary_contact", "Team Lead")
    
    # NEW: Jira and Sentiment
    jira_tickets_list = jira_data.get(tc, []),
    jira_tickets = ", ".join(jira_tickets_list[0]) if isinstance(jira_tickets_list[0], list) else ""
    sentiment = sentiment_data.get(tc, "Neutral")

    # Strategic Pulse Logic Enhancement
    current_pulse = "Healthy"
    trend = data.get("Trend", "Stable")
    
    if data.get("Yield", 0) < 5: current_pulse = "Needs Review"
    if trend == "Declining": current_pulse = "Needs Review"
    if sentiment == "Concerned": current_pulse = "Needs Review"
    if any("Blocked" in t or "High" in t for t in jira_tickets_list[0] if isinstance(jira_tickets_list[0], list)): current_pulse = "Needs Review"
    
    # NEW: Apply Shared Pulse Rules
    for rule in shared_intel.get("technical_pulse_rules", []):
        condition = rule.get("condition", "").lower()
        if condition in narrative.lower() or condition in jira_tickets.lower():
            current_pulse = rule.get("pulse", current_pulse)

    # NEW: Project Detection Logic
    project_keywords = ["PostMessage", "Webhook", "API Migration", "PFRI", "ChatFactory", "Guide", "Concierge", "Account Insights", "Templated Experiences"]
    detected_projects = [p for p in project_keywords if p.lower() in narrative.lower() or p.lower() in jira_tickets.lower()]
    project_str = ", ".join(detected_projects) if detected_projects else "General Optimization"

    # Strategic Recommendations Logic
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
    if ts.get("Intent") and ts.get("Intent") not in ["N/A", "Unknown"]:
        recs.append({"goal": "Surface ABM signals", "action": "Deploy Account Insights Tab", "why": "Visualizes intent in Salesforce."})
    
    # NEW: Append Shared Recommendations
    for shared_rec in shared_intel.get("strategic_recommendations", []):
        trigger = shared_rec.get("trigger", "").lower()
        if trigger in narrative.lower() or trigger in jira_tickets.lower():
            recs.append(shared_rec)

    steps_str = "\n\n".join([f"GOAL: {r['goal']}\nACTION: {r['action']}\nWHY: {r['why']}" for r in recs])
    if not steps_str: steps_str = "GOAL: Scale current success.\nACTION: Optimize high-performing experiences."

    print(f"Updating tab for {tc} ({sheet_name})...")
    
    # Update Basic Info (C1, B3, C3, D3:E3, F3, G3, H3)
    # C1: Last Updated Date
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C1", "valueInputOption": "USER_ENTERED"})], {"values": [[today_str]]})
    
    # B3: Status
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!B3", "valueInputOption": "USER_ENTERED"})], {"values": [["UP TO DATE"]]})
    
    # C3: Technical Pulse (Overwriting based on new logic)
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C3", "valueInputOption": "USER_ENTERED"})], {"values": [[current_pulse]]})

    # D3:E3: Narrative and Last Communication
    final_narrative = f"[Sentiment: {sentiment}] "
    if trend == "Declining":
        final_narrative += "⚠️ WARNING: Declining Engagement detected. "
    final_narrative += narrative
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!D3:E3", "valueInputOption": "USER_ENTERED"})], {"values": [[final_narrative, latest_comm]]})
    
    # F3: Active Project(s)
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!F3", "valueInputOption": "USER_ENTERED"})], {"values": [[project_str]]})

    # G3: Jira Tickets
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!G3", "valueInputOption": "USER_ENTERED"})], {"values": [[jira_tickets]]})

    # H3: Recommendations
    final_h3 = f"STRATEGIC RECOMMENDATIONS (Aligned to Use Case Matrix):\n{steps_str}"
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3", "valueInputOption": "USER_ENTERED"})], {"values": [[final_h3]]})

    # NEW: Update Project Tracking (Row 5+)
    # B5: Project Name, C5: Primary Contact, D5: Technical Status, E5: Latest Activity
    project_row = [project_str, primary_contact, "In Progress", narrative[:100] + "..."]
    run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!B5:E5", "valueInputOption": "USER_ENTERED"})], {"values": [project_row]})

    # Collect stats for Dashboard
    pulse_val = run_gws_command(["sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!C3"})])
    if pulse_val and 'values' in pulse_val:
        pulse = pulse_val['values'][0][0]
        summary_stats["health"][pulse] = summary_stats["health"].get(pulse, 0) + 1
    
    align_val = run_gws_command(["sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!I3"})])
    if align_val and 'values' in align_val:
        align = align_val['values'][0][0]
        if "MISMATCH" in align: summary_stats["alignment"]["MISMATCH"] += 1
        elif "Aligned" in align: summary_stats["alignment"]["Aligned"] += 1

    summary_stats["total_accounts"] += 1
    summary_stats["recs"].extend(recs)

# --- REBUILD DASHBOARD ---
print("Rebuilding Summary Dashboard...")
dashboard = [
    ["STRATEGIC CUSTOMER SUCCESS COMMAND CENTER", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["SECTION 1: PORTFOLIO HEALTH SNAPSHOT", "", "SECTION 2: SF PULSE ALIGNMENT", "", "", "SECTION 3: TEAM-WIDE STRATEGIC GOALS", "", "", ""],
    ["Status", "Count", "Status", "Count", "", "Goal Outcome", "Recommended Action", "Team Count", "Strategic Priority"],
]

health_rows = [[k, v] for k, v in summary_stats["health"].items()]
align_rows = [[k, v] for k, v in summary_stats["alignment"].items()]

rec_counts = {}
for r in summary_stats["recs"]:
    key = (r["goal"], r["action"])
    rec_counts[key] = rec_counts.get(key, 0) + 1
sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)

for i in range(max(len(health_rows), len(sorted_recs), len(align_rows))):
    row = [""] * 9
    if i < len(health_rows): row[0], row[1] = health_rows[i]
    if i < len(align_rows): row[2], row[3] = align_rows[i]
    if i < len(sorted_recs):
        (goal, action), count = sorted_recs[i]
        row[5], row[6], row[7] = goal, action, count
        row[8] = "High" if count > 5 else "Medium"
    dashboard.append(row)

# Append Individual Account Rollup (Current Table)
current_table_res = run_gws_command(["sheets", "spreadsheets", "values", "get", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:I200"})])
current_table = current_table_res.get("values", [])
start_idx = 0
for i, r in enumerate(current_table):
    if len(r) > 0 and r[0] == "Customer Name":
        start_idx = i
        break
main_table = current_table[start_idx:] if start_idx > 0 else current_table

full_sheet = dashboard + [[""]*9, ["--- INDIVIDUAL ACCOUNT ROLLUP ---", "", "", "", "", "", "", "", ""]] + main_table

# Update the Summary Sheet
run_gws_command(["sheets", "spreadsheets", "values", "clear", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1:Z500"})])
run_gws_command(["sheets", "spreadsheets", "values", "update", "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": "'Customer Health Status'!A1", "valueInputOption": "USER_ENTERED"})], {"values": full_sheet})

print("Dashboard Update Complete.")
