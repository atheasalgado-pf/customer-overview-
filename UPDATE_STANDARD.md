# Strategic Customer Overview: Update Standard (Source of Truth)

This document defines the rules and parameters for automated updates to the Strategic Customer Overview spreadsheet.

## 1. Automation Logic (Freshness)
- **Edit Trigger**: Any update made by the agent to a customer tab triggers a local Apps Script that refreshes the **Last Updated Date (C1)**.
- **Status Indicator**: Cell **B3** automatically calculates status based on C1:
  `=IF(TODAY()-C1>14, "UPDATE REQUIRED", "UP TO DATE")`
- **Agent Action**: The agent MUST NOT manually edit C1 or B3.

## 2. Granular Field Map (Individual Customer Tabs)

| Col | Field Name | My Role | Logic / Standard |
| :--- | :--- | :--- | :--- |
| **A** | **Customer Name** | **Read-Only** | Used for account matching. |
| **B** | **Update Status?** | **Read-Only** | Formula-driven: `TODAY()-C1>14`. |
| **C** | **Technical Pulse** | **Update** | **Healthy** (Progress) / **Needs Review** (Blockers OR Yield < 5%) / **Stale** (>30d). |
| **D** | **Pulse Reasoning** | **Overwrite** | Rolling 90-day summary (Incl. Gong, SFDC, [JIRA]). Crawl last 14 days and merge. |
| **E** | **Last Communication** | **Overwrite** | Latest interaction date (MM/DD/YYYY). |
| **F** | **Active Project(s)** | **Overwrite** | Identify specific technical hurdles (e.g., "PostMessage script"). |
| **G** | **Jira Tickets + Status** | **Overwrite** | List **existing** tickets + status from [JIRA] emails. No new IDs. |
| **H** | **Suggested Next Steps** | **Overwrite** | Specific technical action items. |
| **I** | **SF Pulse Alignment** | **Update** | Flag "MISMATCH" if Salesforce Pulse != Column C. |
| **J-W**| **Usage Metrics** | **Monthly Sync**| **Manual Trigger Required.** Overwrite only once per month. |

## 3. Data Sources & Extraction
- **Gmail/Calendar**: Filter for customer name.
- **Gong Summaries**: Search the inbox for "Gong" and filter for specific customer references.
- **Jira Notifications**: Search the inbox for "[JIRA]" or "jira@" to extract ticket IDs and statuses.
- **Salesforce**: Events and Tasks from the last 90 days.
- **Product Data**: `det_data.json` for usage metrics.

## 4. Required Output Schemas

### TAB 1: OVERVIEW (Summary Tab)
- The **Customer Health Status** sheet acts as a **strict rollup** of the individual customer deep-dive tabs.
- **Agent Role**: After updating individual customer tabs, the agent will refresh the corresponding row in the Summary Tab by reading the values directly from the customer tab.
- **Fields Synced**: Technical Pulse (B), Pulse Reasoning (C), Last Communication (D), Active Project(s) (E), Jira Tickets (F), Suggested Next Steps (G).

### TAB 2: CUSTOMER DEEP-DIVE (Individual Tabs)
*Columns A-W follow the Granular Field Map. Additionally, the project section must follow:*

| Field | Logic |
| :--- | :--- |
| **Project Name** | Identified from emails/SFDC/[JIRA]. |
| **Primary Contact** | Main stakeholder from latest threads. |
| **Technical Status** | To Do / In Progress / Closed. |
| **Latest Activity** | One-sentence technical summary. |
| **Next Steps** | Technical action item. |

## 5. Optimization & Quota Strategy

### Rolling Narrative Summary
- **Avoid Full Crawls**: Crawl ONLY the last 14 days of activity and merge with existing D3 content.
- **Cache Management**: Existing content in D3 serves as the "historical cache."

### Monthly Usage Sync
- **Gated Update**: Usage metrics (Col J-W) are updated **strictly once per month** when requested.
- **Pulse Integration**: Agent READS existing metrics (even if not updating) to assess **Technical Pulse** (e.g., Yield < 5%).

## 6. Constraint Checklist
- [ ] Only return results for the specific customer requested.
- [ ] No invented Jira IDs.
- [ ] 90-day rolling activity window for Overview.
- [ ] Include Gong call summaries and [JIRA] notifications from inbox.
- [ ] No new columns or rows added; no changes to formatting (colors, fonts).
- [ ] Overview (Summary) tab is a strict rollup and only updated after tab edits.
