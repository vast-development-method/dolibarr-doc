# Assigning supplier lines to purchase accounts

A supplier invoice line carries an account **identifier**. Assigning it tells the purchase journal where to take that line's cost. Posting the invoice later writes monetary entries to the general ledger. A purchasing clerk might know that a bill is correct while an accountant still needs to decide whether the freight line belongs in transport or in the cost of the purchased goods. The invoice can carry one decision while the other remains pending.

## The accountant's pending list

The assignment screens require enabled accounting, an internal user and accounting binding-write permission. The list needs a selected chart of accounts. Its unit is one supplier invoice detail line joined to an invoice and supplier. An optional catalogue item supplies product-specific account codes. A free-text line can still enter the queue.

| Condition | Effect on the pending list |
| --- | --- |
| Parent state and entity | Invoice status must be positive. Draft invoices are outside the list. The accounting query requests the invoice entity with sharing disabled. Settlement status alone does not remove an unassigned line. |
| Line type and binding | Line type must be at most 2 and the stored account ID zero or negative. Presentation types above 2 do not enter. Zero-value ordinary lines can appear. |
| Invoice type | Includes standard, replacement, credit note and progress invoices. Includes deposits when supplier deposits are treated as invoices. Enabling deposits-as-payments drops deposit invoice headers from this list. |
| Dates | The configured binding start date supplies the initial lower date filter when no starting date was entered. The user can filter by invoice date. The journal has its own period and independently enforces the configured starting date. |
| Other selections | Search on line ID, supplier, invoice or supplier reference, item reference, label, description, amount, VAT rate, country and intra-community VAT number. Country presets include outside the company's country and inside or outside the configured European area. |

The display resolves domestic, intra-community and export purchase numbers from the product, plus the supplier's purchase-account number. Each of these joins requires an active account in the selected chart version and the current entity. When product or party accounts are maintained per entity, the list reads the current entity's records for that source. The separate supplier general and subsidiary accounts belong to the payable side and play a different role when the journal writes.

## Choosing the account

The suggestion service receives the purchasing company as buyer and the supplier as seller. It uses their country codes, European-area membership, the **buyer's** intra-community VAT number and the line's recorded VAT rate. Its area categories describe account routing in this implementation. For a product line it considers configured default product purchase accounts. For a service line it considers the corresponding service accounts. A type-2 line passes the queue's type test but does not acquire a generic product/service default from these two branches.

| First matching geography | Generic purchase account | Item-specific purchase account |
| --- | --- | --- |
| Same country, or buyer country missing | Domestic | Domestic |
| Different countries, both in the European area, nonzero line VAT | Domestic | Domestic, marked as intra-community with VAT |
| Different European-area countries, zero VAT, buyer VAT number missing | Domestic | Domestic, marked for review because the number is missing |
| Different European-area countries, zero VAT, buyer VAT number present | Intra-community | Intra-community when the item has this code. If its intra-community code is empty, the item-specific branch tries its export code. |
| Other cross-border purchase | Export | Export |

With the supplier-specific product account option enabled, a populated supplier purchase account supersedes the item suggestion. A configured supplier deposit account takes precedence for a deposit invoice, a detail whose description is exactly `(DEPOSIT)`, or a credit note whose source invoice was a deposit. Finally, if there is no suggested account ID, no item-specific account code and a generic code exists, the service resolves the generic code against the chart unless generic autofill is disabled. A nonempty item account number that fails to resolve can therefore leave the selector empty even when a generic code exists. The screen shows the candidate numbers and allows an accountant to choose a different ledger account. Binding-calculation extensions can supply a replacement suggestion.

## Saving or revising the assignment

| Entry point | What changes |
| --- | --- |
| Pending list, preselect account | Confirms one account to populate the selectors for the selected lines. This step prepares the form. |
| Pending list, bind | Reads a separate chosen account ID for every checked line. A nonpositive selection produces a line-level error. A positive selection is written to that detail row. There is no transaction around the entire selection. One row can be saved while the next is reported unresolved. |
| Bound-lines list | Joins assigned details to their account. A batch reassignment issues a single update in a transaction. A positive account replaces the old one. Zero unbinds the selected lines. |
| Detail card | The accounting operator can set the account on one line. A negative selection is converted to zero. This updates the source detail. An existing journal movement retains its recorded account. |
| Automatic historical binding | Runs a separate cleanup to clear IDs outside the current entity’s selected chart. It then scans up to 10,000 unbound ordinary rows, subject to the configured start date and optional month/year. It writes only still-unbound rows with a positive suggestion and a nonempty decision other than the missing-VAT-number warning. Unresolved suggestions remain pending and yield a warning. A write failure rolls back the automatic binding transaction. The earlier cleanup has its own commit. |

The automatic scan uses positive-state invoices and line type at most 2. Its query does not apply the manual list's invoice-type/deposit predicate. Assigning an account in that scan does not override the journal's independent invoice-type eligibility. Cleanup checks chart membership and entity, while the item suggestion joins also check active status. A disabled account still belonging to the chart need not be cleared by cleanup.

## From bound lines to a ledger movement

1. The operator chooses the purchase journal, invoice-date period and ledger-status filter. The default filter is “not yet in the general ledger”. Its initial query admits positive-state in-scope supplier invoices of the eligible types with at least one positively bound line. Invoice date is compared to both ends of the selected period and to the configured accounting start date. Eligibility is independent of payment date. A configured maximum, normally 10,000 source rows, can require a narrower selection before writing.
2. The journal checks **all** ordinary detail lines on each candidate invoice. If any type-at-most-2 line has nonzero gross and a nonpositive binding, the whole invoice is marked incomplete. An invoice with no bound line never entered the candidate set. A partly bound invoice can enter and then fail this second check. An unbound zero-gross line by itself does not block the transfer. A replaced invoice with no previous ledger transfer is skipped.
3. For an ordinary positive purchase, the supplier control is credited with the gross amount. The supplier's own general account takes priority over the configured supplier control. Its subsidiary code identifies the supplier and falls back to the configured supplier account when absent. In separate-tax mode the journal debits expense accounts by net amount and posts VAT and local taxes to their corresponding accounts. A tax-dictionary purchase mapping overrides the applicable tax fallback. In tax-inclusive expense mode, it debits gross to the expense account. A signed negative expense or tax amount produces a credit on that side. A negative supplier gross produces a debit to the supplier. The writer follows the signed amounts, including on credit notes.
4. Amounts are grouped by invoice and ledger account. Multiple source lines bound to one account can produce a single cost entry. The booked rows carry source type `supplier_invoice`, the invoice ID, invoice reference, invoice date, due date, journal and entity. Their source-detail ID is zero because one row can represent several details. Additional configured modes handle reverse-charge tax, noncollectible-tax counterparts and allocation of a supplier subsidiary to deposit entries. [Source journal postings](../specification/accounting/source-journal-postings.md) describes those branches.
5. Each candidate invoice opens its own transaction. Missing accounts, blocked accounting dates, duplicate-entry detection or unequal debit and credit totals at monetary precision can prevent commit. Earlier successful invoices retain their entries. On each failed invoice the writer checks the cumulative error count and stops the batch once it reaches ten.

## Two lines and a retry

Assume separate recoverable VAT, one currency, an open period and no special tax treatment. Invoice P-104 contains a material line for 100 net plus 20 VAT and a freight line for 50 net plus 10 VAT. Materials is already bound to purchases. Freight carries zero as its account ID. The accountant's pending list shows freight. The purchase journal can find P-104 through materials but refuses to write any part of the invoice because freight's gross amount is 60.

The accountant binds freight to transport and runs the period again. The ledger receives four entries for the invoice.

| Ledger account | Debit | Credit |
| --- | ---: | ---: |
| Materials purchases | 100 | 0 |
| Transport expense | 50 | 0 |
| Recoverable VAT | 30 | 0 |
| Supplier control with the supplier's subsidiary code | 0 | 180 |

A credit note reversing those signed amounts yields debit 180 to supplier control and credits of 100, 50 and 30 to the other accounts. If freight were bound to the same cost account as materials, the expense rows would combine into one for 150.

On the next ordinary run the source type and invoice ID already exist in bookkeeping, so P-104 disappears from the default transfer population. The “already in ledger” view uses the inverse existence test. A source-level binding correction after posting cannot by itself write a second corrective movement. The low-level insert also tests current entity, source type, document ID, account number, operation label and, when populated, subsidiary account. The source detail participates only under a separate setting. Designated profit/loss accounts are exempt from that low-level duplicate test. A detected duplicate marks the invoice as already journalized and rolls back that attempt. The page’s document-level existence test is broader than row matching and does not establish that an externally imported or manually altered movement is complete.
