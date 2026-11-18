# Reconcile tax activity, declarations and payments by period

A controller reviewing March needs three figures. The trading records establish the tax recognized from business activity. A declaration records the amount attributed to the authority. A remittance records money paid against that declaration. Each can legitimately place the same transaction in a different month. The VAT summary even uses different date boundaries for two panels on the same screen.

## Periods and populations

| View | Period selection and grouping | What the amount represents |
| --- | --- | --- |
| VAT summary by month | Starts at the month containing the requested start date and visits calendar months through the month containing the requested end date. Each call reads the whole month. | Recognized sales VAT less recognized purchase VAT. Purchases can include reimbursed employee expenses. Draft invoices, unrelated bank payments and tax-authority remittances supply no trading tax here. |
| VAT detail by rate | Uses the selected start day at midnight and end day at 23:59:59, using server time for explicit bounds. Groups the selected details by rate and, when present, source code. | Recognized line net and VAT by sales or purchase side. Expanding a selected rate or showing all detail exposes the contributing documents and payment shares. The summary is computed even when a group is collapsed. |
| VAT detail by counterparty | Uses inclusive start and end dates. Groups customer and supplier rows under individual parties. An eligible expense reimbursement retains an expense author and reference in its supporting data. | Recognized base and tax for each displayed side. A turnover minimum changes the contributing party population. It is possible for one side of a party to pass the minimum and the other to fall below it. |
| VAT declared and paid panel | Filters declarations by their **value date** between the selected days. Groups both declaration amounts and linked payment amounts by that declaration's value-date month in the active entity. | “Claimed” is the sum of declaration amounts. “Paid” is the sum of signed payments joined to those declarations. A subsequent payment changes the earlier month's paid total when the report is rerun. |
| Local component declared and paid panel | Filters by current entity and selected component. The claimed side groups by the local tax record's value date. The paid side filters and groups by that record's payment date. | The value declaration and the cash date can show in different months. Each side uses the local tax record's amount. There is a separate data model for VAT declaration payments. |

The default period is prepared before each VAT enquiry. A pair of explicit bounds takes precedence. A month and year select that calendar month. The numbered quarter shortcuts use calendar quarters. When neither is supplied, the configured return frequency can choose a preceding complete month, a quarter computed from the fiscal start and current month, or an annual window. The annual branch has a six-month threshold for its chosen start year. These controls select report dates and do not create a declaration.

## A cutoff through the middle of a month

Assume invoice-based goods on both sides and a requested window of 10 to 20 March. A customer is invoiced for 100 net plus 20 VAT on 5 March. A second is invoiced for 50 net plus 10 VAT on 12 March. A supplier invoice dated 18 March carries 25 net plus 5 VAT. All documents are validated in the same visible entity. With no other entries:

| Output | Sales VAT | Purchase VAT | Difference |
| --- | ---: | ---: | ---: |
| March row on monthly activity summary | 30 | 5 | 25 |
| Rate detail for 10–20 March | 10 | 5 | 5 |
| Rate detail reached by the March month link | 30 | 5 | 25 |

Now enter a declaration of 25 with value date 15 March and record its only payment of 25 on 2 April. Before the payment exists, the March declaration contributes 25 and has no paid amount. After the payment exists, a rerun of the March panel shows claimed 25 and paid 25 for March. Selecting April alone excludes this declaration and its payment from that panel, even though the bank records cash leaving in April. For a local-tax record with the same two dates, the claimed 25 appears in March and the payment 25 appears in April. An auditor reconstructing cash therefore needs the payment dates and the linked bank operation, as well as the declaration periods.

## Reconstruct a counterparty cutoff

The detailed party reader collects original full line amounts once for each successive source line. It retains a line/payment detail for each eligible allocation. The VAT counterparty report applies its minimum against that party's **original net** accumulated for the side, before multiplying detail amounts by a payment share. A zero minimum admits all groups. A positive minimum admits amounts strictly greater than the threshold. A negative input meets neither condition in the comparison. The net and VAT total at the bottom are accumulated from admitted rows.

For example, an outstanding service invoice for 200 net plus 40 VAT receives one payment of 60 in the period. Under payment-based service recognition with ordinary proportional presentation, its allocation fraction is 60/240. A party minimum of 150 admits the group, even though its displayed recognized net is only 50 and its VAT is 10. A minimum of exactly 200 excludes it. By contrast the rate detail's expand control decides which details to print under a rate. A collapsed rate still contributes to the rate report's total.

The common reader classifies an ordinary goods line as type zero with both service dates empty. A service line or a line with a service start or end uses the service rule. For an expense, the purchase reader selects a paid expense report in the current entity and its reimbursement payments in the requested period. The expense author's identity and expense reference explain the record. Bank reconciliation status has no role in selecting the expense reimbursement. The expense-by-party query selects the author but omits the company key used by the collection routine to form its groups. Its stored author detail alone cannot establish separate, correctly named party subtotals for multiple employees.

There is a further difference when sales and purchase timing differ. The monthly VAT summary selects purchase rows through the purchase settings but reads the **sales** settings when deciding whether to prorate those rows. The exact-date rate-detail calculation uses the purchase settings at both stages. For example, set sales goods to invoice, purchase goods to payment and ordinary proportional presentation. A supplier goods invoice of 100 plus 20 tax is paid in two instalments of 60 in different months. Each payment selects one purchase row in its month. The monthly summary can display 20 purchase VAT in each month. The corresponding detailed period displays 10 per month. These four amounts come from the same two allocations. The monthly display does not alter the invoice, the payments or the ledger.

## Evidence and authority

The VAT menu exposes month, party and quarter enquiries under the tax-charge read permission. A separate creation grant controls adding a declaration through the menu. The report handlers enter the tax charges area. Source documents use their applicable invoice entity scope, whereas the declaration/payment panel explicitly filters to the current entity. An installation with shared invoice visibility can consequently recognize commercial amounts from a wider set than the declaration panel.

See [tax recognition and remittance](../specification/accounting/tax-recognition-and-remittance.md) for the invoice, payment and reimbursement calculations.
