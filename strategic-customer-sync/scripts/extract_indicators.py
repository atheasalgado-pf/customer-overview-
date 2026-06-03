import json

def get_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)['values']

def clean_val(v):
    if v is None: return 0
    try:
        return float(v.replace(',', '').replace('%', '').strip())
    except:
        return 0

det_data = get_data('det_data.json')
# Headers are in row 4 (index 3)
# Cols:
# CB: Total Visitors (PF) - index 79
# CZ: Content Experience (new) Engaged - index 103
# DA: Content Experience (old) Engaged - index 104
# CM: Content Experience Total - new (Adoption) - index 90
# CN: Content Experience Total - old (Adoption) - index 91
# CY: WebTool Engagement - index 102
# CJ: Collection Total (adoption) - index 87
# CX: Collectioms Engaged - index 101
# CP: Active Webtools - index 93
# CO: ChatFactory Agent Total (Adoption) - index 92
# DF: New UX Feature Adoption - index 109
# CD: Visitor Converted (PF) - index 81

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

target_customers = ["Amplitude", "Appgate", "Cornerstone", "Cotiviti", "Crowdstrike", "Egencia", "Endeavor Business Media", "Exabeam", "Franklin Covey", "Gainsight", "Heinz Marketing", "Informa", "Jumio", "Kinaxis", "KPMG", "Micron", "Modern Health", "Monotype", "NinjaOne", "NowSecure", "Nvidia", "Palo Alto Networks", "PEAC Solutions", "Planet", "PWC", "ScaledAgile", "Seclore", "Semtech", "Sysdig", "Textio", "Thales", "TransUnion"]

final_data = {}
for tc in target_customers:
    # Match
    match = next((v for k, v in results.items() if tc.lower() in k.lower()), None)
    final_data[tc] = match

print(json.dumps(final_data))
