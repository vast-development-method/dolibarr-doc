# Reading sales figures by person

A sales representative can find an invoice in their customer portfolio while all the invoiced turnover appears under the billing clerk's name. The customer, commercial document and payment each have their own relationship to a person. Choose the report using the relationship that answers the question.

| Operator question | Selection | What appears |
| --- | --- | --- |
| Which parties are assigned to one or more representatives? | The third-party list tests the current party-to-user assignments. Multiple positive IDs match any selected representative. “No sales representative” alone selects parties with zero assignments. Selecting it alongside representatives also includes the unassigned parties. | One row per matching party within the list's entity and role filters. When a user lacks unrestricted customer visibility and has no linked-party scope, the list forces their own representative assignment. |
| Which proposals, orders or customer invoices belong to a representative's customers? | Each document list tests the party on its header against current assignments. A positive representative ID selects parties assigned to that user. The unassigned option selects parties with no assignments. | Each qualifying document appears as a whole. Two separate representatives' filtered lists can both contain the same invoice and its entire amount. Removing an account assignment can remove older invoices from that representative's search. |
| On which documents did a user serve as an internal contact? | The user filter looks up an internal contact type for that particular document family and a link between the document and the selected user. | An invoice contact does not thereby match the contact filter on the associated order. Combining contact and representative filters requires both relationships. The same person need not hold both roles. |
| Who issued the sales that are reported as turnover? | The financial report groups by the user recorded as the customer invoice's author, in both invoiced and collected modes. | A separate line per matching author shows invoiced totals or allocated receipts for invoices they created. Recording a receipt under another operator leaves this attribution with the invoice author. |
| What share of sales and gross margin is attributed to an agent? | The margin report uses current party assignments or a designated invoice contact role, and the party's representative count. | See the invoice-line cost, percentage and equal-sharing rules in [Gross margin by customer and sales representative](../reporting/sales-profitability-and-attribution.md). |

The third-party multiselect offers active users and an unassigned choice. Its existence test can still encounter an assignment to a user who is no longer active. A party with that assignment alone does not qualify as unassigned. Searching a document by invoice author uses a separate author field. This is also the field used when the invoiced-turnover amount links to the invoice list. That link carries the author ID alone, so a drill-down covering other dates or states can show a different total.

## Turnover by invoice author

| Rule | Invoice basis | Receipts basis |
| --- | --- | --- |
| Reporting event | Invoice date | Customer payment date |
| Input measure | Sum signed net and gross invoice header amounts in the reporting currency. | Sum gross amounts of individual payment-to-invoice allocations. A payment shared between two authors contributes each allocation to its invoice's author. |
| Invoice population | Validated or closed standard, replacement, credit and progress invoices. Include deposits unless the setting treats deposits solely as payments. | Require a dated payment allocated to an invoice. The allocation query supplies no matching invoice-state or invoice-type restriction. |
| Party and entity | Scope to the visible invoice entities and, where selected, the invoice party. A party-linked account forces its own party ID. | Same scope on the invoice for author-attributed allocations. |
| Percentage | Author's gross divided by report gross, multiplied by 100 and rounded to two places. | Same ratio, with collected gross in the denominator. A nonpositive grand total leaves percentages blank on either basis. |

The report checks the enabled accounting module's financial-report access. The bookkeeping mode names select the corresponding invoice or receipt calculation from business documents. This report does not read ledger postings. Explicit start and end dates bracket the period inclusively at the server's day boundaries. In the absence of a complete date pair, an explicit month selects that calendar month, a quarter selects its calendar quarter and the annual default begins in the configured fiscal starting month. With no selected year, a fiscal start later in the calendar than the current month places the period start in the preceding year.

In receipts mode a separate “payments not linked to user” row can contribute to the gross total. It covers bank-linked customer payments with no invoice allocation. This calculation uses the bank account's entity and the payment dates, with no invoice party to filter. It sums distinct **amounts** within this single group. Two qualifying unallocated receipts for 30 therefore contribute 30 to that row. Allocated receipts in the ordinary author groups use their individual allocation amounts.

## Worked portfolio and collection

Consider one customer assigned to Ana and Jules. Lin creates a validated invoice dated 30 April for 100 net and 115 gross. Only Jules is assigned an internal invoice contact role. Another user records 46 against this invoice on 2 May.

| Selection | Expected result |
| --- | --- |
| Invoice list filtered to Ana, then separately to Jules as party representative | Each list finds the same invoice for 115 gross. Adding both list totals would count it twice. |
| Invoice list filtered to Ana as representative and Jules as internal contact | One invoice. The reverse combination yields no match because Ana has no internal contact role there. |
| April invoiced turnover by author | Lin receives 100 net and 115 gross. |
| May collected turnover by author | Lin receives 46 gross. The operator who recorded the receipt receives no share from that action. |
| Margin by representative under the ordinary party rule | With an eligible cost of 60, each representative receives 50 of net sales, 30 of cost and 20 of margin. |

Source locations include `htdocs/societe/list.php:108–116,637–666,1352–1361`, `htdocs/comm/propal/list.php:796–820`, `htdocs/commande/list.php:1203–1221`, `htdocs/compta/facture/list.php:860–878,1058–1077`, `htdocs/compta/stats/cabyuser.php:45–138,192–197,267–355,467–525` and `htdocs/compta/facture/class/facture.class.php:400–453`.
