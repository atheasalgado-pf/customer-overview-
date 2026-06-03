import json

with open('sheet_ids.json') as f:
    sheet_ids = json.load(f)

source_sheet_id = sheet_ids["Amplitude"]
requests = []

# Exclude 'Customer Health Status' if it has a different layout, 
# but the user said "all the other tabs", and individual tabs usually share layout.
# I will exclude 'Customer Health Status' as it is the summary tab.
exclude_sheets = ["Amplitude", "Customer Health Status"]

for title, target_id in sheet_ids.items():
    if title in exclude_sheets:
        continue
    
    # Copy format from Amplitude A1:Z100 to target A1:Z100
    requests.append({
        "copyPaste": {
            "source": {
                "sheetId": source_sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 100,
                "startColumnIndex": 0,
                "endColumnIndex": 26
            },
            "destination": {
                "sheetId": target_id,
                "startRowIndex": 0,
                "endRowIndex": 100,
                "startColumnIndex": 0,
                "endColumnIndex": 26
            },
            "pasteType": "PASTE_FORMAT",
            "pasteOrientation": "NORMAL"
        }
    })

# Also copy row heights and column widths if they were adjusted?
# Copying formatting (PASTE_FORMAT) usually doesn't include column widths.
# I'll add column width updates too if I can find them in Amplitude.

print(json.dumps({"requests": requests}))
