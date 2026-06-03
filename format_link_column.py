import json
import subprocess
import os

spreadsheet_id = "1S5TaZ1mxLPh_TbpEluLJd_AV2GBaWE8GEF9-Y5_prfw"
gws_path = "/opt/homebrew/bin/gws"
env = os.environ.copy()
env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"

# 1. Get sheetId
res = subprocess.check_output([
    gws_path, "sheets", "spreadsheets", "get",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id, "fields": "sheets(properties(sheetId,title))"})
], env=env).decode()
sheets = json.loads(res).get("sheets", [])
sheet_id = next(s["properties"]["sheetId"] for s in sheets if s["properties"]["title"] == "Customer Health Status")

# 2. Format Column I (Link) and J (Alignment)
requests = [
    # Header I1
    {
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 8, "endColumnIndex": 9},
            "cell": {"userEnteredFormat": {
                "backgroundColor": {"red": 0.8156863, "green": 0.8784314, "blue": 0.8901961},
                "textFormat": {"bold": True, "fontSize": 11, "fontFamily": "Google Sans Text"}
            }},
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }
    },
    # Data Rows I2:I100
    {
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 8, "endColumnIndex": 9},
            "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
        }
    }
]

subprocess.run([
    gws_path, "sheets", "spreadsheets", "batchUpdate",
    "--params", json.dumps({"spreadsheetId": spreadsheet_id}),
    "--json", json.dumps({"requests": requests})
], env=env)
