import json

with open('column_widths.json') as f:
    data = json.load(f)

with open('sheet_ids.json') as f:
    sheet_ids = json.load(f)

amplitude = next(s for s in data['sheets'] if s['properties']['title'] == 'Amplitude')
source_widths = [c.get('pixelSize', 100) for c in amplitude['data'][0].get('columnMetadata', [])]

requests = []
exclude_sheets = ["Amplitude", "Customer Health Status"]

for title, target_id in sheet_ids.items():
    if title in exclude_sheets:
        continue
    
    for i, width in enumerate(source_widths):
        if width:
            requests.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": target_id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1
                    },
                    "properties": {
                        "pixelSize": width
                    },
                    "fields": "pixelSize"
                }
            })

print(json.dumps({"requests": requests}))
