import json
import subprocess
import os

with open('indicators_data.json', 'r') as f:
    indicators = json.load(f)

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
headers = [
    "Total Visitors (PF exp)", "Engaged Experiences", "Yield (Visitors/Engaged Exp)",
    "Total Experiences (new)", "Total Experiences (old)", "WebTool Engagement",
    "Engaged Experiences (new)", "Engaged Experiences (old)", "Total Collections",
    "Engaged Collections", "Active Webtools", "ChatFactory Agents",
    "New UX Feature Adoption", "Unknown Visitors converted"
]

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
    "Appgate": "Appgate"
}

env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

for tc, data in indicators.items():
    if data is None: continue
    sheet_name = mapping.get(tc, tc)
    print(f"Updating {sheet_name}...")
    
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
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!J2:W2", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [headers]})
    ], env=env, capture_output=True)
    
    # Update data J3:W3
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!J3:W3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [row_data]})
    ], env=env, capture_output=True)
    
    # Update H3
    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3"})
        ], env=env).decode()
        current_h3 = json.loads(res).get("values", [[""]])[0][0]
    except:
        current_h3 = ""
    
    if "STRATEGIC RECOMMENDATIONS" not in current_h3:
        new_h3 = f"{current_h3}\n\nSTRATEGIC RECOMMENDATIONS (based on usage):\n{steps_str}"
        subprocess.run([
            gws_path, "sheets", "spreadsheets", "values", "update",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3", "valueInputOption": "USER_ENTERED"}),
            "--json", json.dumps({"values": [[new_h3]]})
        ], env=env, capture_output=True)

