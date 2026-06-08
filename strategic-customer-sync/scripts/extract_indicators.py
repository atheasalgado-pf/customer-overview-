import json
import os
import sys

def get_data(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f).get('values', [])
    except:
        return []

def clean_val(v):
    if v is None: return 0
    if isinstance(v, (int, float)): return float(v)
    try:
        return float(str(v).replace(',', '').replace('%', '').strip())
    except:
        return 0

def main():
    det_data_file = os.environ.get('DET_DATA_FILE', 'det_data.json')
    customers_file = os.environ.get('CUSTOMERS_FILE', 'customers.json')

    det_data = get_data(det_data_file)
    if not det_data:
        print(f"Error: {det_data_file} not found or empty.")
        sys.exit(1)

    if not os.path.exists(customers_file):
        print(f"Error: {customers_file} not found. Run sync_sfdc_accounts.py first.")
        sys.exit(1)

    with open(customers_file, 'r') as f:
        target_customers = json.load(f)

    # Headers are in row 4 (index 3), data usually starts around row 7 (index 6)
    results = {}
    for row in det_data:
        if len(row) > 110:
            name = str(row[0]).strip()
            try:
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
                    "New_UX_Adopt": row[109] if len(row) > 109 else "Unknown",
                    "Converted": clean_val(row[81])
                }
                data["Engaged_Total"] = data["Engaged_New"] + data["Engaged_Old"]
                data["Yield"] = (data["Engaged_Total"] / data["Visitors"] * 100) if data["Visitors"] > 0 else 0
                results[name] = data
            except (ValueError, IndexError):
                continue

    final_data = {}
    for tc in target_customers:
        # Match using case-insensitive partial match
        match = next((v for k, v in results.items() if tc.lower() in k.lower() or k.lower() in tc.lower()), None)
        final_data[tc] = match

    output_file = 'indicators_data.json'
    with open(output_file, 'w') as f:
        json.dump(final_data, f, indent=4)
    
    print(f"Extracted indicators for {len(final_data)} customers. Saved to {output_file}")

if __name__ == "__main__":
    main()
