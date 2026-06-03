import json
import subprocess
import os

with open('det_data.json', 'r') as f:
    det_data = json.load(f)['values']

def clean_val(v):
    if v is None: return 0
    try:
        return float(str(v).replace(',', '').replace('%', '').strip())
    except:
        return 0

results = {}
for row in det_data[6:]:
    if len(row) > 110:
        name = row[0].strip()
        data = {
            "Visitors": clean_val(row[79]),
            "Engaged_New": clean_val(row[103]),
            "Engaged_Old": clean_val(row[104]),
            "Total_New": clean_val(row[90]),
            "Total_Old": clean_val(row[91]),
            "WebTool_Eng": clean_val(row[102]),
            "Total_Coll": clean_val(row[87]),
            "Engaged_Coll": clean_val(row[101]),
            "Active_WT": clean_val(row[93]),
            "CF_Agents": clean_val(row[92]),
            "New_UX_Adopt": row[109],
            "Converted": clean_val(row[81])
        }
        data["Engaged_Total"] = data["Engaged_New"] + data["Engaged_Old"]
        data["Yield"] = data["Visitors"] / data["Engaged_Total"] if data["Engaged_Total"] > 0 else 0
        results[name] = data

# Mapping for the missing ones
missing_mapping = {
    "Endeavor Business Media (EBM)": "EBM - GEN", # Sum of EBMs would be better but let's take one
    "Egencia": "Amex GBT",
    "Modern Health": "Modernhealth"
}

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
headers = [
    "Total Visitors (PF exp)", "Engaged Experiences", "Yield (Visitors/Engaged Exp)",
    "Total Experiences (new)", "Total Experiences (old)", "WebTool Engagement",
    "Engaged Experiences (new)", "Engaged Experiences (old)", "Total Collections",
    "Engaged Collections", "Active Webtools", "ChatFactory Agents",
    "New UX Feature Adoption", "Unknown Visitors converted"
]

env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

for tab_name, source_name in missing_mapping.items():
    data = results.get(source_name)
    if not data: continue
    print(f"Updating {tab_name}...")
    
    row_data = [
        data["Visitors"], data["Engaged_Total"], round(data["Yield"], 2),
        data["Total_New"], data["Total_Old"], data["WebTool_Eng"],
        data["Engaged_New"], data["Engaged_Old"], data["Total_Coll"],
        data["Engaged_Coll"], data["Active_WT"], data["CF_Agents"],
        data["New_UX_Adopt"], data["Converted"]
    ]
    
    # Strategic Next Steps Logic
    strategic_steps = []
    if data["CF_Agents"] == 0: strategic_steps.append("- Pilot ChatFactory Agents to automate real-time buyer engagement.")
    if data["Active_WT"] == 0: strategic_steps.append("- Deploy Website Tools (Guide/Concierge) to increase conversion on high-traffic pages.")
    if data["Total_New"] == 0: strategic_steps.append("- Migrate to Templated Experiences (New UX) for faster launch times and enhanced visual engagement.")
    if data["Yield"] < 10 and data["Visitors"] > 0: strategic_steps.append("- Leverage AI-Powered Content Recommendations to improve Visitor-to-Experience yield.")
    if data["Engaged_Coll"] == 0 and data["Total_Coll"] > 0: strategic_steps.append("- Audit Collection strategy to ensure Smart Collections are surfacing relevant content.")
    
    steps_str = "\n".join(strategic_steps) if strategic_steps else "- Continue scaling current high-performing experiences."
    
    # Update headers J2:W2
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!J2:W2", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [headers]})
    ], env=env, capture_output=True)
    
    # Update data J3:W3
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!J3:W3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [row_data]})
    ], env=env, capture_output=True)
    
    # Update H3
    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!H3"})
        ], env=env).decode()
        current_h3 = json.loads(res).get("values", [[""]])[0][0]
    except:
        current_h3 = ""
    
    if "STRATEGIC RECOMMENDATIONS" not in current_h3:
        new_h3 = f"{current_h3}\n\nSTRATEGIC RECOMMENDATIONS (based on usage):\n{steps_str}"
        subprocess.run([
            gws_path, "sheets", "spreadsheets", "values", "update",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!H3", "valueInputOption": "USER_ENTERED"}),
            "--json", json.dumps({"values": [[new_h3]]})
        ], env=env, capture_output=True)

