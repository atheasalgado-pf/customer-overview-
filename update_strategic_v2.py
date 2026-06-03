import json
import subprocess
import os

with open('indicators_data.json', 'r') as f:
    indicators = json.load(f)

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
    "PWC": "PWC", "Amplitude": "Amplitude", "Appgate": "Appgate",
    "Egencia": "Egencia"
}

for tc, data in indicators.items():
    if data is None: continue
    sheet_name = mapping.get(tc, tc)
    print(f"Strategic Update for {sheet_name}...")
    
    strategic_steps = []
    
    # 1. NEW UX MIGRATION
    if data["Total_New"] == 0:
        strategic_steps.append("GOAL: Modernize content delivery and increase 'Binger' sessions. ACTION: Migrate legacy tracks to Templated Experiences. WHY: Templated experiences drive higher engagement by providing a visual, guided journey that encourages deeper content consumption compared to legacy tracks.")
    
    # 2. CHATFACTORY
    if data["CF_Agents"] == 0:
        strategic_steps.append("GOAL: Capture anonymous buyer intent. ACTION: Pilot ChatFactory Agents. WHY: AI-powered conversations engage unknown visitors earlier in the journey, uncovering content relevance and intent that is missed by static forms.")
    
    # 3. WEBTOOLS
    if data["Active_WT"] == 0:
        strategic_steps.append("GOAL: Turn website traffic into qualified leads. ACTION: Deploy Guide/Concierge widgets. WHY: These widgets provide persistent content discovery at every entry point, ensuring visitors are always one click away from their 'Next Best Content'.")
    
    # 4. YIELD / AI
    if data["Yield"] < 10 and data["Visitors"] > 0:
        strategic_steps.append("GOAL: Improve visitor-to-engagement efficiency. ACTION: Enable AI-Powered Content Recommendations. WHY: Leveraging machine learning to suggest relevant assets reduces friction and ensures a higher percentage of visitors convert into engaged sessions.")
    
    # 5. COLLECTION AUDIT
    if data["Engaged_Coll"] == 0 and data["Total_Coll"] > 0:
        strategic_steps.append("GOAL: Optimize automated content assembly. ACTION: Audit Smart Collection filters. WHY: Ensuring metadata is correctly mapped will allow Smart Collections to surface more relevant content, reducing manual work for the marketing team.")

    # 6. PFRI / REVENUE INTEL
    # If they have high conversion but no PFRI mentioned? (I don't have a direct PFRI field but I can guess based on active projects)
    
    steps_str = "\n\n".join(strategic_steps) if strategic_steps else "GOAL: Scale current success. ACTION: Optimize high-performing experiences. WHY: Maintaining current engagement levels requires continuous iteration of top-performing assets."
    
    # Get current H3 to maintain recent activity notes
    try:
        res = subprocess.check_output([
            gws_path, "sheets", "spreadsheets", "values", "get",
            "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3"})
        ], env=env).decode()
        current_val = json.loads(res).get("values", [[""]])[0][0]
        # Remove old strategic recs if they exist
        clean_val = current_val.split("STRATEGIC RECOMMENDATIONS")[0].strip()
    except:
        clean_val = ""
    
    final_h3 = f"{clean_val}\n\nSTRATEGIC RECOMMENDATIONS (Aligned to Use Case Matrix):\n{steps_str}"
    
    subprocess.run([
        gws_path, "sheets", "spreadsheets", "values", "update",
        "--params", json.dumps({"spreadsheetId": spreadsheet_id, "range": f"'{sheet_name}'!H3", "valueInputOption": "USER_ENTERED"}),
        "--json", json.dumps({"values": [[final_h3]]})
    ], env=env, capture_output=True)

