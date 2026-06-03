# Use Case Matrix & Strategic Logic

This reference documents the logic used to generate strategic recommendations for customers.

## Logic Mapping

| Metric | Condition | Goal | Action | Why |
| :--- | :--- | :--- | :--- | :--- |
| **UX Adoption** | `Total_New == 0` | Modernize delivery | Migrate to Templated Experiences | Drives higher binger sessions. |
| **Conversion** | `Yield < 10` | Improve yield | Enable AI Recommendations | Increases traffic conversion. |
| **Intent** | `CF_Agents == 0` | Capture anon intent | Pilot ChatFactory Agents | Uncovers intent missed by forms. |
| **Product Discovery**| `Active_WT == 0` | Turn traffic into leads | Deploy Guide/Concierge | Persistent content discovery. |
| **Revenue Sync** | `Converted > 50` | Attribute revenue | Enable PFRI | Syncs intent directly to SFDC. |
| **ABM Signals** | `Intent != N/A` | Surface ABM signals | Deploy Account Insights Tab | Visualizes intent in Salesforce. |
| **Automation** | `Visitors > 1000`| Automate workflows | Configure Webhooks | Real-time behavioral alerts. |
| **Optimization** | `Total_Old > 50` | Optimize library | Run Content Inventory Audit | Identifies low-performing assets. |

## Thresholds
- **High Traffic**: >1000 visitors/month.
- **Low Yield**: <10% conversion from visitor to engaged session.
- **Stale Account**: No strategic update in >7 days.
