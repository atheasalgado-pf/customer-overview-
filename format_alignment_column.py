import json
import subprocess
import os

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

# 1. Get the sheetId for 'Customer Health Status'
res = subprocess.check_output([
    gws_path, "sheets", "spreadsheets", "get",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "fields": "sheets(properties(sheetId,title))"})
], env=env).decode()
sheets = json.loads(res).get("sheets", [])
sheet_id = next(s["properties"]["sheetId"] for s in sheets if s["properties"]["title"] == "Customer Health Status")

# 2. Define the formatting requests
# Column J (index 9)
requests = [
    # Format Header (J1)
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 9,
                "endColumnIndex": 10
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.8156863, "green": 0.8784314, "blue": 0.8901961},
                    "textFormat": {
                        "bold": True,
                        "fontSize": 11,
                        "fontFamily": "Google Sans Text",
                        "foregroundColor": {"red": 0.12156863, "green": 0.12156863, "blue": 0.12156863}
                    },
                    "borders": {
                        "bottom": {"style": "SOLID", "width": 1},
                        "left": {"style": "SOLID", "width": 1},
                        "right": {"style": "SOLID", "width": 1},
                        "top": {"style": "SOLID", "width": 1}
                    },
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,borders,verticalAlignment,wrapStrategy)"
        }
    },
    # Format Data Rows (J2:J100)
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 1,
                "endRowIndex": 100,
                "startColumnIndex": 9,
                "endColumnIndex": 10
            },
            "cell": {
                "userEnteredFormat": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP"
                }
            },
            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
        }
    }
]

# 3. Execute the batch update
subprocess.run([
    gws_path, "sheets", "spreadsheets", "batchUpdate",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id}),
    "--json", json.dumps({"requests": requests})
], env=env)

print("Formatting update complete.")
