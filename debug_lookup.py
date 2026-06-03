import json

with open('master_data.json', 'r') as f:
    master_rows = json.load(f)['values']

sf_pulses = {}
for row in master_rows[4:]:
    if len(row) > 14:
        name = row[4].strip()
        pulse = row[14].strip()
        sf_pulses[name] = pulse

with open('overview_data.json', 'r') as f:
    overview_rows = json.load(f)['values']

for row in overview_rows[1:]:
    if not row or not row[0]: continue
    cust_name = row[0].strip()
    
    # Debug lookup
    match_found = False
    for sf_name in sf_pulses:
        if cust_name.lower() in sf_name.lower() or sf_name.lower() in cust_name.lower():
            print(f"MATCH: '{cust_name}' matches '{sf_name}' (Pulse: {sf_pulses[sf_name]})")
            match_found = True
            break
    if not match_found:
        print(f"MISS: '{cust_name}' not found in master list.")

