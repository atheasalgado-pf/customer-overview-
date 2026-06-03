# Project: Customer Insights

## Overview
This project integrates Salesforce data with Google Workspace (Gmail, Calendar, Sheets).

## Connections
- **Salesforce**: Connected as `athea@pathfactory.com` (Org ID: `00Di0000000ZnAgEAK`). 
    - Verified access to `Event` and `Task` objects.
- **Google Workspace**: ❌ Authentication Failed.
    - Error: `invalid_grant: reauth related error (invalid_rapt)`.
    - Action Required: Run `gws auth login` in your terminal to refresh credentials.

## Knowledge Base
- Use `sf` for Salesforce operations.
- Use `gws` for Google Workspace operations.

### Salesforce Queries
- Events: `sf data query --query "SELECT Id, Subject, StartDateTime FROM Event LIMIT 5"`
- Tasks: `sf data query --query "SELECT Id, Subject, Status FROM Task LIMIT 5"`

### GWS Commands
- Drive: `gws drive files list --params '{"pageSize": 10}'`
- Gmail: `gws gmail users messages list --params '{"userId": "me"}'`
- Calendar: `gws calendar events list --params '{"calendarId": "primary"}'`
