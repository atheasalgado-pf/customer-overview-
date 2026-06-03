import json

def get_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)['values']

data = get_data('master_data.json')
customers = ["Amplitude", "Appgate", "Cornerstone", "Cotiviti", "Crowdstrike", "Exabeam", "Kinaxis", "KPMG", "Micron", "Modern Health", "Nvidia", "Palo Alto Networks", "Planet", "PWC", "Sysdig", "Thales", "TransUnion", "Semtech", "Endeavor Business Media"]

# Header is row 4
pulses = {}
for row in data[4:]:
    if len(row) > 14:
        name = row[4]
        pulse = row[14]
        pulses[name] = pulse

for c in customers:
    match = next((v for k, v in pulses.items() if c.lower() in k.lower()), "Not Found")
    print(f"{c}: {match}")
