# From invoices and bank movements to double-entry journals

Sales and bank journals have different source records. Sales records the claim on the customer, earned revenue and VAT. Bank records cash received and clears the customer account. Either event can exist while its source remains in the journal's pending-transfer view. [Double-entry accounting guide][wiki] · [Sales selection][sales] · [Bank transfer][bank]

## Posting model

| Concept | Mapping and invariant |
| --- | --- |
| Journal | Journal code and label classify a posting. The sales journal reads invoice lines, their account bindings and the third party. The bank journal reads the bank movement and links describing its counterparty or purpose. |
| Movement | Rows sharing the accounting transaction number form one movement. While building a source transfer, reuse its transaction identity across rows. Record issuing entity, document type, source ID/reference, source date and author. A group of invoice lines posted to one account can yield a ledger line with source-detail ID zero. |
| Ledger row | General account, optional auxiliary account/customer code, operation label, debit and credit. Money on a debit or credit side is positive in ordinary postings. The posting writer compares total debit and credit rounded to amount precision before committing the movement. |
| Distinct evidence | The ledger records a validation timestamp, export timestamp and optional lettering code/date. Bank reconciliation records a statement and actor on the bank line. Checking the bank statement, matching customer ledger items and validating a ledger movement answer different questions. |

[Ledger columns][ledger] · [Line creation and grouping][writer] · [Bank statement matching][recon]

## Sales transfer

1. Require the double-entry account binding/write permission (`accounting.bind.write`). Select eligible non-draft sales invoices under the journal's entity/date filters. Standard, replacement, credit and progress documents are eligible kinds. Deposits join the selection under the ordinary invoiced-deposit configuration. An unposted original marked replaced is skipped.
2. Resolve the customer general account and auxiliary identifier. Read the bound account for each eligible product/service line and tax accounts for its tax components. The journal checks for unbound non-zero lines, which block the whole invoice.
3. For an ordinary positive sale, debit customer receivables by gross. Credit the applicable revenue and tax accounts. Negative amounts reverse the sides. Special branches handle deposits, collected local taxes and retained warranty. The account identifiers come from the entity's accounting setup.
4. Start and end a database transaction **per invoice**. A writer error or unbalanced movement rolls back that invoice. Previously committed invoices in the same transfer remain posted. The “not yet” view queries source type and source ID in bookkeeping, enabling a fresh selection after interruption. The row writer also checks a narrower combination involving account, label and entity. Treat this as a secondary check since labels are editable.

[Selection and account bindings][sales] · [Per-invoice validation and posting][transfer] · [Final balance check][balanced] · [Row-level duplicate check][writer]

## Bank transfer

For a positive customer receipt, debit the bank account and credit the customer general account with the associated auxiliary account where available. The posting source is the **bank row ID**, even when its commercial origin is a receipt split over several invoices. The bank journal uses other counter-account rules for supplier, payroll, internal transfer and other sources. The transfer requires binding/write permission and checks balance inside a transaction for each source bank row. [Bank-side and counterparty lines][bank] · [Bank balance check][bankbalance]

## Period controls

The ledger writer checks source date against the entity's fiscal-period configuration. In `blockedonclosed` mode the inclusive date range of a closed period prevents posting. In the alternate mode the date must fall in an active period, including its start and, when supplied, its end. An undefined ledger account also prevents creation. The closing workflow has its own fiscal-year write permission. It can validate movements for a date interval and separately close the period. When generating closing entries the closure screen requires configured groups for balance-sheet and income-statement accounts. [Period guard][period] · [Fiscal closing workflow][closure]

## Worked acceptance cases

| Case | Source and action | Ledger result |
| --- | --- | --- |
| FIN-GL-01 | Transfer a validated 62.10 invoice, 54.00 taxable revenue and 8.10 output VAT, fully bound, active period. | Receivables debit 62.10, revenue credit 54.00, VAT credit 8.10. One sales movement with the invoice ID, debit and credit each 62.10. |
| FIN-GL-02 | Same customer, ordinary bank receipt 40.00 allocated to that invoice. Transfer the bank row. | A second movement debits bank 40.00 and credits receivables 40.00. Customer balance from these two movements is a debit 22.10. Revenue remains 54.00. |
| FIN-GL-03 | Invoice X ready. Invoice Y contains a bound line and an unbound non-zero product line. Transfer them together. | X posts. Y remains pending with a binding error. Resolve Y's binding, select pending again and post Y. X is absent from the new pending selection. |
| FIN-GL-04 | A source is dated on the last day of a closed period with blocking on closed periods. | Inclusive date check rejects the ledger write. Its invoice or bank source still exists. |
| FIN-GL-05 | Prepare one movement with debit 62.10 and credits 54.00 and 8.09. | The 0.01 difference fails the per-movement balance check. No partial ledger rows for that source survive. |

[Movement schema](../../schemas/finance/journal-movement.schema.json) · [Sales movement example](../../examples/finance/journal-movement--sale.json). The normalized schema distinguishes posting sides and requires origin and journal identity. Equality of aggregate debits and credits is a transaction rule in addition to shape validation.

[wiki]: ../reference/locators/finance.md#ref-5415216013fc
[sales]: ../reference/locators/finance.md#ref-cf68d6d152e6
[ledger]: ../reference/locators/finance.md#ref-2a2765d49eab
[writer]: ../reference/locators/finance.md#ref-ffd2d5b0807e
[transfer]: ../reference/locators/finance.md#ref-9a92cf6767e5
[balanced]: ../reference/locators/finance.md#ref-529d6057b4a4
[bank]: ../reference/locators/finance.md#ref-61ee8fc8362a
[bankbalance]: ../reference/locators/finance.md#ref-9743ea6ecf05
[recon]: ../reference/locators/finance.md#ref-f7b005fa5282
[period]: ../reference/locators/finance.md#ref-982ac9257b71
[closure]: ../reference/locators/finance.md#ref-f52c8dc69a64
