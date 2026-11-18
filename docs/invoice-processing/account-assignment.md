# Assigning sales accounts and posting the invoice

The unassigned sales queue asks an accountant to choose the general ledger account for each eligible invoice detail. A single invoice with five unassigned lines can appear five times. Assigning the last account can make the invoice eligible for journal transfer. Assignment alone creates no debit or credit.

## Which line appears?

The operator must be internal, have accounting enabled and hold accounting binding-write permission. Join the line to its invoice and that invoice to the billed party. The item is an optional join, so a free-text service can still appear. The query uses the invoice entity scope for accounting without cross-entity invoice sharing.

| Condition or filter | Meaning |
| --- | --- |
| Header status and kind | Require `facture.fk_statut > 0` and a standard, replacement, credit or progress invoice. Include deposits when deposits are treated as invoices. The status predicate alone can also admit an abandoned header. |
| Detail status | Require `facturedet.fk_code_ventilation <= 0` and `product_type <= 2`. There is no nonzero amount requirement in this queue. Type-9 structural rows are outside it. |
| Customer and invoice | `search_societe` matches the party name. `search_invoice` matches the invoice reference. `search_lineid` supports numeric line-ID searches. |
| Product and description | `search_ref` and `search_label` target the current catalogue reference and label. `search_desc` targets the transaction's stored line description. A free-text line can match the latter while having no catalogue reference. |
| Amount, rate and account | `search_amount` compares stored line net. `search_vat` compares the normalized numeric line VAT rate. `search_account` searches the joined domestic product sales account number. The displayed recommendation can come from a different account. |
| Dates | Boundaries use invoice date `datef`. Start and end can be applied separately and are inclusive from the beginning to the end of the chosen server days. Without a start the configuration can supply the accounting binding start. |
| Country and tax identity | `search_tvaintra` matches the customer's VAT number. `search_country` accepts a country or a group such as all foreign countries, regional members, foreign regional members, or nonmembers. Country membership and the seller's country supply the group boundaries. |

Cumulative progress changes the displayed net but not the amount filter's column. For an underlying line of 1,000 net, suppose the preceding certificate reached 20% and the current line stores 60% and a cumulative net of 600. The displayed increment is 600 × (60 − 20) / 60 = 400. Searching the raw line net for 600 can find the row displaying 400. A current percentage of zero yields a zero ratio. In incremental progress mode the selected line amount is already the instalment.

## Suggested account and operator decision

The item can carry separate domestic, regional and export sales accounts. Shared products or parties can carry entity-specific accounting values. Account-number lookups for the joined product and party suggestions require the active chart, active account and current accounting entity. The suggested value to store is `accounting_account.rowid`, not the account number printed on the screen.

| Decision in order | Result |
| --- | --- |
| Generic starting point | Choose the configured product-sold or service-sold domestic, intra-regional or export account according to detail type and transaction context. An unknown buyer country is treated as domestic. For two regional members in different countries, nonzero line VAT or a missing buyer VAT number favors the domestic generic code. |
| Specific product mapping | Domestic or unknown buyer country uses `accountancy_code_sell`. For two regional members with different countries, nonzero VAT or a missing buyer VAT number also chooses the domestic field. Otherwise the regional field `accountancy_code_sell_intra` is chosen if present. The remaining foreign branch tries `accountancy_code_sell_export`, including a qualifying regional sale with no item-specific regional code. |
| Customer preference | If party-specific product accounts are enabled and supplied, the billed party's sales mapping replaces the current suggestion. This is the account for what was sold, separate from the customer receivable control account. |
| Deposit override | If a customer deposit account is configured, a deposit invoice, a line whose description equals `(DEPOSIT)`, or a credit note sourced on a deposit invoice selects the dedicated account. |
| Generic fallback | If there is no resolved suggestion and no specific product code but a generic code exists, resolve its account unless generic autofill is disabled. A specific product code that fails to resolve can therefore leave the operator without a valid suggestion. |

A confirmed selection writes the chosen positive account ID to that detail's `fk_code_ventilation`. The pending queue processes selected lines individually and reports successes and failures. Leaving the second line's account blank can preserve the first assignment while returning a failure for the second. The assigned-lines screen also supports a single transaction to change a selection to a different account or set it to zero. Zero makes an otherwise eligible line pending again. Reassigning that field does not amend a posted bookkeeping row.

## From eligible lines to a balanced journal

1. Find positively assigned product and service rows (types 0 and 1) on eligible nondraft invoices. The journal applies its configured start date, and if both operator date limits are set it applies them to the invoice date. A cash-sales separation option can exclude point-of-sale origin documents. Where the journal handles deposit consumption separately, it excludes the lines consuming an identified originating deposit and derives the corresponding reversal separately.
2. For candidate invoice IDs, count remaining ordinary details with `product_type <= 2`, nonpositive assignment and nonzero `total_ttc`. Any such row blocks the **whole invoice**. If all eligible lines are unassigned there may be no candidate invoice in the first query at all. A zero-gross unassigned detail can remain in the queue without blocking the other assigned details.
3. Group net by assigned account, VAT by its mapped account and receivables by customer. Cumulative progress applies its stage ratio. Where configured, split retention from receivables and add the mapped invoice stamp once. Normal positive revenue and output VAT are credits, the gross receivable is a debit. Default credit-note amounts reverse those signs. A replaced original with no previous accounting transfer is skipped.
4. Open a posting transaction per invoice. Write entries with `doc_type = customer_invoice`, `fk_doc` equal to the invoice ID, `doc_date` equal to the invoice date and `doc_ref` equal to its commercial reference. Aggregated rows use `fk_docdet = 0` because several details may contribute to one ledger account. Receivable rows carry the customer subledger. A failed line or unequal debit and credit sums at money precision rolls back this invoice. Earlier successful invoices in the batch stay posted.
5. The pending/already-posted filter checks for a bookkeeping row with the invoice document type and document ID. It does not require a match on every invoice detail. A separate write-time duplicate comparison also considers account number, operation label, entity and a supplied subledger, with an optional detail comparison. As labels can change and the precheck and insert are separate operations, this does not establish concurrency-safe exactly-once posting.

### Reconcile the source, assignment, journal and settlement

Assume one currency, no retention or local taxes, and a domestic customer. Goods are three units at 50, discounted 10%, with VAT 15%. This gives 135.00 net, 20.25 VAT and 155.25 gross. A second line is a zero-rated service of 40.00. A third service carries zero net and gross.

| Observation | Expected result |
| --- | --- |
| Only goods assigned | Goods leave the pending queue. The unassigned 40.00 service blocks posting of the full 195.25 invoice. |
| Goods and 40.00 service assigned | The zero-value third line can still appear in the pending queue. It does not block the eligible invoice. |
| Transfer to separate income accounts | Debit customer receivable 195.25. Credit goods revenue 135.00, service revenue 40.00 and output VAT 20.25. Total credits equal total debits. |
| Allocate cash of 75.00 later | The invoice-read balance is 120.25, assuming no applied credit or deposit. The sales entry still totals 195.25. The cash allocation and bank posting have their own identities and dates. |
| Change a source assignment after transfer | The assigned-line value may change. The existing ledger carries its original account and the invoice is already in the transferred population. Reconcile and correct the ledger through the authorized accounting workflow. |

See [source journal postings](../specification/accounting/source-journal-postings.md) for additional source families and [bank and customer payments](../finance/collections.md) for the subsequent cash flow.
