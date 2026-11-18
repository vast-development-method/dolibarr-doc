# Cheque deposits, direct debit and credit transfer lines

## Cheque deposits

A row represents the deposit slip `bordereau_cheque`. Its `fk_bank_account` must resolve to `bank_account.rowid` and its `entity` must equal the current entity. Bank-area access is required. The separate cheque grant controls creation. The standard search accepts the slip's `ref`, destination bank-account ID, stored `amount` and inclusive range on `date_bordereau`. Status, deposit type and count may be displayed or sorted. Selecting the status column does not restrict the query by status.

The register reads `nbcheque` and `amount` saved on the slip. The slip recalculation reads all bank movements with `bank.fk_bordereau = slip.rowid`, counts them and sums their signed `amount`, then updates both header fields in a transaction. Slip reference, movement ID and cheque or transfer number belong to separate records. A search by slip date does not compare cheque receipt dates or the bank's value dates.

Three cheque movements of 80, 120 and 50 linked to one deposit produce one row, count 3 and amount 250. The operational receipts already account for the three instruments. Adding the slip total to those receipts would count the same deposit twice. A fourth cheque of 30 assigned to another slip makes a second row rather than changing the first slip to 280.

## Bank instruction lines

The register joins instructions to the obligations they address. Direct debit mode requires access to collection batches. Credit transfer mode requires the bank-transfer area. An invoice can have more than one instruction line, such as two instalments or a new attempt. Use the batch reference and instruction line ID to distinguish them.

| Mode | Necessary relationship chain | Entity and party |
| --- | --- | --- |
| Direct debit | `prelevement_lignes.fk_prelevement_bons → prelevement_bons.rowid`. Link `prelevement.fk_prelevement_lignes` to the line, then `fk_facture → facture.rowid`. | The invoice must be in the invoice entity population. Use its `fk_soc → societe.rowid` and customer code. |
| Credit transfer for a purchase | Same batch, line and instruction link. Resolve `fk_facture_fourn → facture_fourn.rowid`. | The supplier invoice is checked against the invoice entity population in this query. Use the linked supplier's name and supplier code. |
| Credit transfer for salary | The transfer view unions a second selection with `fk_salary → salary.rowid` and `salary.fk_user → user.rowid`. | Uses the salary row's entity against the invoice entity population. Employee names populate the party column. The projection supplies the employee reference in the customer-code position and null in the supplier-code position. |

All joins to the obligation and party are required. In the transfer union, identical whole projected rows collapse. The register displays the batch reference, the line's own status `prelevement_lignes.statut`, line ID, linked obligation, party, **batch creation date** `prelevement_bons.datec` and **instruction amount** `prelevement_lignes.amount`. The invoice gross or salary amount is also selected, but does not supply the displayed instruction amount. A batch creation date by itself establishes neither a cleared payment date nor a failed collection date.

Text search on the batch reference and exact search on line ID are independent. Party name and customer or supplier code search the corresponding party row. Salary-name search compares employee first and last names. The credit-transfer code predicate on salary rows tests the null supplier-code slot, so an ordinary nonempty supplier-code search excludes the salary branch. A fixed third-party context adds an invoice-party condition. In the salary branch the same condition refers to a party alias absent from that branch, so a party-scoped transfer query can fail. An empty result and a query error are different outcomes.

For a customer invoice of 300 covered by two direct debit lines of 100 and 200 in separate batches, the register can show both lines and a total instructed value of 300 across those distinct line IDs. If the first 100 is rejected and a new line for 100 is issued, the historical instruction amounts sum to 400. Reconciliation must inspect their status and the resulting payment/bank records to establish the amount actually settled.
