# Payment terms, collection requests and settlement discounts

## Derive the invoice due date

A term has a dictionary identifier and code, a calculation type, a day count and an offset. The calculation starts from the invoice date. An explicit term takes precedence, followed by the term code on the invoice and finally its term identifier. With none of these the invoice date is the due date. A code lookup uses the applicable dictionary entities. A successful lookup with no matching row leaves the day counts and calculation type at zero. A failed dictionary query returns an error.

| Calculation | Order of operations | Worked result |
| --- | --- | --- |
| Elapsed calendar days | Add the day count, then the offset in days. Use the server's calendar for day arithmetic across daylight-saving changes. | 20 January 2026 plus 30 days gives 19 February. A further five days gives 24 February. |
| Days, then month end | Add the day count, move to the last day of that resulting month, then apply the day offset. December rolls through January of the following year. | 20 January 2026 plus 30 days reaches February. The month end is 28 February. With a five-day offset, payment falls due on 5 March. |
| Specified day of month | Add the day count, compare the resulting calendar date with the specified day in that month, and use that day if the date is on or before it. Otherwise use the corresponding date in the next month. This type requires a nonzero target day. | With no delay and target day 15, an invoice dated 15 January is due 15 January. An invoice dated 16 January is due 15 February. |

The dictionary's display text can express a commercial agreement the calculation does not execute. The delivered “50% on order, 50% on delivery” entry uses the same one-day term formula as “due upon receipt”, “due on order” and “due on delivery”. The due-date calculation produces one date. It does not generate two collection instructions or listen for the delivery event. Installations can change their terms, so the values attached to the selected code govern the result.

Related records include [Payment terms](../../records/dictionaries.md#record-c_payment_term).

## Reserve an amount for bank collection or transfer

A customer direct-debit request references a customer invoice. A supplier transfer request references a supplier invoice. The document must be beyond draft and its paid flag must be clear. The service reads the counterparty bank coordinates from the selected or default bank record. It writes the invoice link, amount, request time, requester, copied bank coordinates, source type and entity, and the bank record identifier when available. After inserting a request it attempts to set the invoice's payment method to direct debit or transfer if that payment method exists. Creating a request leaves payment and bank movement registration for the subsequent processing steps.

Two active configurations define a duplicate request differently.

| Behavior | Reservation rule | Amount if omitted |
| --- | --- | --- |
| One request | Count bank-type requests for that invoice. By default only unprocessed requests count. An explicit all-requests option counts processed requests as well. A nonzero count blocks creation. | Gross invoice less payments, applied credit notes and applied deposits, rounded to amount precision. An explicit nonzero amount bypasses this default calculation. |
| Multiple partial requests | Add unprocessed bank requests plus the amounts of receipt lines linked to the invoice whose processing status is empty or zero. Subtract both from the remaining invoice balance. A further request needs positive room and must fit in it. | Both an omitted amount and an explicit zero request the entire positive amount still available. With no positive room the service declines the request. |

An invoice for 1,200 has payments of 200, applied credit of 50 and an applied deposit of 150. Its outstanding amount is 800. A pending request of 100 and a further 250 already in an uncredited receipt leave 450 available under partial-request mode. A new request for 450 uses the full remainder. Passing zero also requests 450 in this case. A request for 451 returns the over-amount outcome without writing a request. The calculation reads receipt-line amounts through their invoice links. A receipt line covering several invoices needs attention when comparing this calculation with per-invoice payment allocation.

A caller can distinguish a successful insert, a duplicate or unavailable-amount outcome, an invalid document state and a data access or amount error. A successful return confirms the request insert. The return from the separate change of payment method does not determine this result.

## Post the balance forgone on a discount closure

A settlement discount with tax has a specific closure reason. The journal selects validated-or-later standard, replacement, credit and progress invoices with that reason. It includes deposit invoices unless the installation treats deposits solely as payments. Selection can be restricted by closing-date interval and the accounting binding start date. The transferred-state filter looks for a bookkeeping row with the same invoice family, document identifier and journal code. The journal uses the closing date, falling back to the invoice date when no closing date is supplied to the builder.

The gross discount is the positive part of gross invoice amount minus recorded payments, applied credit notes and applied deposits. The monetary components and result are rounded at total precision. A zero or negative result contributes no journal lines. The service groups nonzero gross line amounts by tax rate to three decimal places. Each group receives a proportional share of the gross discount using its share of gross line value. Every group except the last receives its rounded share. The last takes the exact remainder. If the total available line weight is nonpositive, the whole discount goes into a group at zero tax.

For a positive tax rate, net discount equals rounded gross share divided by one plus the tax fraction, rounded to monetary precision. Tax equals the difference between gross and net. A zero-rate group carries its entire gross amount to net. The current account mapping uses a single configured tax account on each side, even when the amount is split by rate.

| Invoice side | Debit | Credit |
| --- | --- | --- |
| Customer | Discounts granted for the net share. The configured purchase-side tax account receives the tax correction when positive. | Customer control account for the gross share, with the customer subsidiary when present. |
| Supplier | Supplier control account for the gross share, with the supplier subsidiary when present. | Discounts received for the net share. The configured sales-side tax account receives the positive tax correction. |

For a 230 invoice, let gross lines be 120 at 20% tax and 110 at 10%. If the recorded settlement totals 207, the gross discount is 23. The 20% group takes 12, comprising 10 net and 2 tax. The 10% group takes 11, comprising 10 net and 1 tax. The customer journal therefore debits expense by 20 and tax by 3 and credits receivables by 23. On an equivalent supplier invoice the journal debits payables by 23 and credits income by 20 and tax by 3. Both transactions are balanced without creating a cash movement.

A party's own general account overrides the configured customer or supplier control account. Each proposed row carries a source family, document identifier, reference, transaction date, party code, ledger and journal. A proposed account must be found for its row to be emitted into bookkeeping. The journal writer compares total debits and credits of each source document at monetary precision before commit. A document with an unbalanced result rolls back independently of successful documents in the same transfer.
