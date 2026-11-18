# Bank statements, cheque deposits and returned receipts

A bank account can have a running balance, a balance for a named statement and a batch of cheques awaiting deposit at the same time. Each view reads the same signed bank transactions with a different selection rule. A deposit slip groups existing receipts. Matching a bank statement records the operator's reconciliation decision. Returning a cheque creates a compensating receipt and cash movement.

## Bank transactions and statements

| Value on a bank transaction | Use |
| --- | --- |
| Account and signed amount | Receipts increase the account balance. Payments reduce it. Totals are expressed in the bank account's currency. |
| Operation date and value date | The operation date is the default cutoff date for a dated balance. A caller may select the value date for a value-dated balance. |
| Statement reference | Identifies the set of transactions displayed for this account and statement. It can be assigned before reconciliation. |
| Reconciliation flag and operator | The flag records confirmation. Confirmation records the acting operator. Saving a statement reference with the flag cleared does not replace the previous operator. |
| Payment type, cheque number and deposit slip identifier | Identify how the payment was made and whether the bank transaction belongs to a remittance. These are independent of its statement reference. |

A balance inquiry sums signed amounts for the account. In dated mode the calculation includes transactions through the supplied cutoff, or through the current date if the caller omits the cutoff. The unconstrained balance includes future-dated transactions. Reconciliation status does not participate in either sum. The named-statement opening balance sums amounts on this account with a nonempty reference sorting before the selected reference. Closing equals that opening plus all amounts bearing the selected reference. Statement detail orders movements by value date and then creation timestamp. The statement position depends on how references sort. Consistent references such as `2026-01` through `2026-12` preserve month order.

A May statement opens at 5,000, contains two receipts of 450 and 150 and a payment of 80. Its closing balance is 5,520. A fourth receipt of 200 already entered on the account with no statement assignment takes the overall balance to 5,720, assuming no other transactions. The 200 appears in the named closing balance once assigned to that statement, even if the operator has only saved the statement reference.

Release references include `htdocs/compta/bank/class/account.class.php:1376–1401` and `htdocs/compta/bank/releve.php:177–194,393–418,485–513,700–731`.

## Assign, confirm and rename a statement

The bank reconciliation permission authorizes the operator to save a reference on selected lines or to confirm them reconciled. Both operations require a nonempty statement reference and selected transaction identifiers. A configured statement naming expression applies to each update. For each line the service writes the submitted reference and flag, then optionally associates a transaction category. A duplicate category link does not undo a successful reconciliation. The list processes one line at a time and stops on a failed update. Previous successful lines retain their changes. Reopening the list reveals which lines still need attention.

A statement rename requires the reconciliation permission, a current reference and a new reference. The form checks whether the proposed new reference is already in use on a bank account in the current entity. If available, it changes every matching old reference on the selected account. The scope of collision detection is consequently broader than the scope of the rename. Reassigning or renaming a statement changes the statement totals for which those transactions are counted.

Release references include `htdocs/compta/bank/bankentries_list.php:252–297`, `htdocs/compta/bank/class/account.class.php:2610–2667` and `htdocs/compta/bank/releve.php:200–231`.

## Assemble a deposit slip

1. Choose the receiving bank account, payment type and at least one transaction. The default payment type is cheque. The cheque-management permission controls creation, line removal, validation, deletion and rejection from the deposit screen.
2. Create the header in the operating entity with author, creation and deposit dates, receiving account, type, provisional reference, draft status, zero count and zero amount.
3. Collect candidate transactions with this account and payment type, a strictly positive amount and no existing deposit. Intersect those candidates with the submitted transaction identifiers. The interactive screen requests all candidates. A service caller may limit the candidate set before the intersection.
4. Store the deposit identifier on each selected eligible bank line. Read all amounts linked to this deposit again to calculate the total and number of items. An ineligible submitted identifier contributes nothing. The service can consequently produce an empty draft if the candidate intersection is empty.
5. A successful validation replaces the provisional reference with the next deposit reference and changes the current entity's draft to validated. A second attempt to validate the same record fails the draft-state condition. The installation can request validation immediately on creation. The card can render the resulting slip for the bank.

For cheques of 65 and 135, the submitted form need not supply a total. The stored amounts yield two items and a deposit of 200. Removing the 65 line clears its deposit identifier only when it belongs to this deposit. Recalculation yields one item and 135. Deleting a deposit removes the entity's header and releases its transactions for selection again. Neither action reverses the underlying bank receipt. The remove operation reports success unconditionally to its caller, so reloading the membership and total is the observable confirmation when a write fails.

Release references include `htdocs/compta/paiement/cheque/card.php:94–100,153–252` and `htdocs/compta/paiement/cheque/class/remisecheque.class.php:179–315,326–421,687–754`.

## Return a cheque allocated to several invoices

The operator identifies the original bank transaction and enters the rejection date. The service finds the customer payment linked to the original bank line, reads its invoice allocations and attempts to reopen each linked invoice. It creates a new cheque payment with the rejection date, the original payment number and the negative of each original allocation. It posts the new negative payment to the original bank account and marks the original payment rejected. Failure to create the negative payment, register the bank movement or mark the original rejected rolls back the transaction. The individual invoice reopen return values are not checked inside this routine.

Suppose a single receipt for 300 had settled invoice A for 100 and invoice B for 200. Its return creates allocations of −100 to A and −200 to B and a bank movement of −300. With no other settlement, A and B again have outstanding amounts of 100 and 200. The new payment carries a separate identifier even though the payment number matches. A previously reconciled original bank entry remains on its original statement. The compensating movement can be reconciled against the bank's later return. The deposit slip's original positive receipt still records what was submitted to the bank.

Release references include `htdocs/compta/paiement/cheque/card.php:235–250` and `htdocs/compta/paiement/cheque/class/remisecheque.class.php:766–842`.
