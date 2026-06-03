import json
import subprocess
import os

# Re-use the data from results (I'll re-extract from the json file I have)
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

missing_mapping = {
    "Endeavor Business Media (EBM)": "EBM - GEN",
    "Egencia": "Amex GBT",
    "Modern Health": "Modernhealth"
}

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

for tab_name, source_name in missing_mapping.items():
    data = results.get(source_name)
    if not data: continue
    print(f"Strategic Update for {tab_name}...")
    
    strategic_steps = []
    if data["Total_New"] == 0:
        strategic_steps.append("GOAL: Modernize content delivery and increase 'Binger' sessions. ACTION: Migrate legacy tracks to Templated Experiences. WHY: Templated experiences drive higher engagement by providing a visual, guided journey that encourages deeper content consumption compared to legacy tracks.")
    if data["CF_Agents"] == 0:
        strategic_steps.append("GOAL: Capture anonymous buyer intent. ACTION: Pilot ChatFactory Agents. WHY: AI-powered conversations engage unknown visitors earlier in the journey, uncovering content relevance and intent that is missed by static forms.")
    if data["Active_WT"] == 0:
        strategic_steps.append("GOAL: Turn website traffic into qualified leads. ACTION: Deploy Guide/Concierge widgets. WHY: These widgets provide persistent content discovery at every entry point, ensuring visitors are always one click away from their 'Next Best Content'.")
    if data["Yield"] < 10 and data["Visitors"] > 0:
        strategic_steps.append("GOAL: Improve visitor-to-engagement efficiency. ACTION: Enable AI-Powered Content Recommendations. WHY: Leveraging machine learning to suggest relevant assets reduces friction and ensures a higher percentage of visitors convert into engaged sessions.")
    if data["Engaged_Coll"] == 0 and data["Total_Coll"] > 0:
        strategic_steps.append("GOAL: Optimize automated content assembly. ACTION: Audit Smart Collection filters. WHY: Ensuring metadata is correctly mapped will allow Smart Collections to surface more relevant content, reducing manual work for the marketing team.")

    steps_str = "\n\n".join(strategic_steps) if strategic_steps else "GOAL: Scale current success. ACTION: Optimize high-performing experiences. WHY: Maintaining current engagement levels requires continuous iteration of top-performing assets."
    
    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!H3"})
        ], env=env).decode()
        current_val = json.loads(res).get("values", [[""]])[0][0]
        clean_val = current_val.split("STRATEGIC RECOMMENDATIONS")[0].strip()
    except:
        clean_val = ""
    
    final_h3 = f"{clean_val}\n\nSTRATEGIC RECOMMENDATIONS (Aligned to Use Case Matrix):\n{steps_str}"
    
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{tab_name}'!H3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [[final_h3]]})
    ], env=env, capture_output=True)

