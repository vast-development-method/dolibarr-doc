# Home work queues

A queue reports one count per qualifying business object or line. Its domain provider determines the unit counted, eligibility, warning delay, monetary value when supported and destination list. The homepage checks the enabled domain, section visibility and applicable grant before invoking the provider. A successful response enters the workboard. An error return is omitted. A successful empty response can have zero counts. Extensions can contribute additional rows and groups.

## Commercial and service queues

| Queue | Who can receive it | Membership and warning basis |
| --- | --- | --- |
| Open and signed sales proposals | Proposal reader | Open means validated. Signed means signed status. Both count headers and sum header value before tax. Only the open row checks expiry against the warning interval. The signed queue tests the proposal state directly. |
| Open and signed supplier quotes | Supplier-proposal reader | Status 1 and 2 feed separate rows. Only the open row compares the quote’s recorded closing date with the closure warning boundary. The query uses the closing date field, including on an open quote. The provider counts documents and leaves the monetary total at its default. |
| Sales orders to ship | Customer-order reader | Validated and shipment-in-progress headers. The warning uses the later of order date and delivery date, strictly earlier than now minus the configured customer-order delay. |
| Sales orders to bill | Customer-order reader with billing-after-validation enabled | Validated, shipping-in-progress and closed orders with billed flag zero. Counts and header totals before tax are returned. This mode has no late increment. |
| Delivered sales orders to bill | Customer-order reader | Closed order with billed flag zero. This population overlaps the optional broader billing queue. The test uses the order header state and billing flag. |
| Supplier orders to process | Supplier-order reader | Validated or approved header in the current entity, with an order date older than the supplier warning boundary to qualify as late. |
| Supplier orders awaiting receipt | Supplier-order reader | Sent or partially received header. A missing delivery date still qualifies for the count. A defined delivery date earlier than the supplier warning boundary makes it late. Both supplier order queues sum net header amounts. |
| Customer and supplier invoices unpaid | Respective invoice reader | Validated and unpaid headers. Each contributes its net face value, including partly paid headers. The customer provider loads due date and state for its delay test. The supplier provider also evaluates delay using its invoice due date. |
| Contract services to activate and running | Contract reader | Count lines on validated contracts. Initial lines use planned opening date for late activation. Open lines use validity end for expiry. Missing comparison dates do not increment the late count. |
| Tickets open | Ticket reader | Excludes closed-solved and cancelled tickets. The provider returns an open count with zero late count. Ticket severity and age do not create a late home-workboard item here. |

Commercial providers commonly restrict an external viewer to their party and restrict internal sales staff to assigned parties. The exact entity set and date source are provider-specific. For example, the supplier-order workboard queries the current entity, while the supplier-order shortlist uses the supplier-order sharing selector.

Sources include `htdocs/index.php:246–316`, `htdocs/comm/propal/class/propal.class.php:3560–3657`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:2340–2409`, `htdocs/commande/class/commande.class.php:3686–3780, 4329–4340`, `htdocs/fourn/class/fournisseur.commande.class.php:3504–3570, 3724–3746`, `htdocs/compta/facture/class/facture.class.php:5501–5556`, `htdocs/fourn/class/fournisseur.facture.class.php:2805–2858`, `htdocs/contrat/class/contrat.class.php:2310–2402` and `htdocs/ticket/class/ticket.class.php:3393–3452`.

## Internal operations, staff and treasury

| Queue | Admission and measurement |
| --- | --- |
| Agenda actions | Requires own-agenda read. Counts progress at least zero and under 100. A restricted viewer can qualify as author, owner or an assigned user resource. Party-assignment scope also applies when required. Planned start supplies the warning date. |
| Projects | Project read. Count open project headers in project scope. A restricted project reader uses the allowed project list. A defined project end strictly before the warning boundary makes the open project late. |
| Tasks | Project read and tasks enabled. Count tasks with null or incomplete progress on open authorized projects. The late test uses incomplete progress, a positive end date and the project-task warning delay. |
| Bank lines to reconcile | Internal bank reader. Include unmatched lines of open, reconcilable, non-cash accounts. Value date and the bank reconciliation interval determine lateness. Page dispatch first checks whether there is an account to reconcile. |
| Cheques awaiting deposit | Internal bank reader with cheque deposits enabled. Count positive cheque bank lines without a deposit slip. Value date and the cheque warning interval determine lateness. |
| Direct debits and credit transfers | Internal bank reader with the corresponding payment feature enabled. Each row counts payment batches of its instrument type below debited or credited status. The age comparison uses the recorded transmission date. |
| Members awaiting validation or subscription | Internal membership reader. One row counts draft members. The other counts validated members whose type requires subscriptions and whose end date is missing or past. The member delay routine evaluates the subset considered late. |
| Expense claims | Approval permission selects validated claims to approve. Permission to mark paid selects approved claims to pay. Without full visibility the author or designated validator must be in the viewer's user hierarchy. Both warning clocks use the validation date, with separate approval and payment delays. External-user requests return no workboard response. |
| Leave approval | Approval permission, internal viewer. Pending validated requests use status 2. Restricted readers receive their applicable hierarchy or approver scope. Lateness compares leave start with the approval warning boundary. |
| Production orders | The homepage dispatches when production and its section are enabled. The provider excludes external viewers. Validated or in-progress orders count. A planned end earlier than the production warning boundary makes an order late. |

Sources include `htdocs/index.php:224–244, 319–380`, `htdocs/comm/action/class/actioncomm.class.php:1505–1586`, `htdocs/projet/class/project.class.php:2285–2354`, `htdocs/projet/class/task.class.php:2659–2727`, `htdocs/compta/bank/class/account.class.php:1410–1456`, `htdocs/compta/paiement/cheque/class/remisecheque.class.php:516–560`, `htdocs/compta/prelevement/class/bonprelevement.class.php:3062–3128`, `htdocs/adherents/class/adherent.class.php:2852–2924`, `htdocs/expensereport/class/expensereport.class.php:2608–2671`, `htdocs/holiday/class/holiday.class.php:2595–2641` and `htdocs/mrp/class/mo.class.php:2171–2215`.

## Calculating the headline

The workboard groups rows into agenda, projects, sales offers, orders, invoices, supplier quotes, purchase orders, supplier bills, contracts, tickets, bank, members, expense reports, leave and manufacturing. A work queue can have a full-list destination and a separate list filtered to late items. Hiding the global workboard or disabling an individual domain block changes which rows are evaluated. Widget shortlist limits have no bearing on this calculation.

For the headline, include a row only when its total and late counts are numeric and its late count is greater than zero. Sum its late count into the numerator and its full count into the denominator. Display the percentage rounded to two decimal places, or zero for an empty denominator. The visual indicator can use absolute late count or the percentage. Default band upper bounds are 0, 10, 20 and 30, with a fifth band above 30. Count mode and percentage mode have separate configurable bounds.

**Acceptance example.** Sales orders report 10 to ship, 3 late. Invoices report 4 unpaid, 1 late. Tickets report 100 open, 0 late. The headline reports 4 late and a percentage of 28.57%, calculated as 4 ÷ 14. The 100 tickets still appear in their own queue. If the same order qualifies for shipping and billing, reading either queue still returns the qualifying order. Summing across queues cannot produce a distinct-document count.

The normalized [workboard row schema](../../schemas/reporting/workboard-row.schema.json) and [invoice example](../../examples/reporting/workboard-row.json) describe an individual response. Use the per-domain count unit and monetary basis when interpreting it. No currency or exchange rate is supplied by the native response. Sources include `htdocs/core/class/workboardresponse.class.php:26–92` and `htdocs/index.php:395–539, 925–965`.
