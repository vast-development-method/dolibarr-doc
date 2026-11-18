# Employee salary obligations and cash settlement

A salary obligation records an amount owed to one employee for a pay period. The operator supplies the amount. The salary record can also retain a separate salary value, a project, a preferred payment method and a bank account. The amount due, the sum of cash payments, and the document's paid classification answer three different questions.

## Who can enter and see the obligation

The web card checks the salary module and record scope. Reading all salaries allows access across employees. An ordinary salary-read grant restricts access to employees in the user's applicable hierarchy. Creating or editing a salary uses salary-write permission. The web action enables deletion with the explicit delete permission or, for an unpaid obligation, with write permission. Employee identity matters even when several obligations use the same project or bank account.

On ordinary entry the card requires the employee, a nonzero amount and both pay-period dates. The record writer also requires a label. With immediate payment selected, the form requires a payment method and, when bank accounting is active, an account to debit. It opens an outer transaction, creates the obligation and its extra attributes, then attempts the requested payment and banking steps. A reported failure of those steps rolls the combined operation back. Creating only the obligation leaves later cash disbursement to a separate operation.

## Settlement document and posting

| Fact | Storage and meaning |
| --- | --- |
| Face amount | The salary's amount for the period, interpreted in the entity's monetary context. |
| Salary payment | A row linked to one salary, with amount, method, date of payment, entry date, reference, note, author and optional bank-row ID. A salary can have several payment rows. |
| Outstanding | Salary amount less the sum of the amounts on its payment rows. Monetary precision is applied when testing whether the remaining amount is zero. |
| Paid classification | A separate flag. The operator can set it or reopen the record. The later classification operation has no independent payment or bank effect. |
| Cash movement | Under banking, the account receives a movement equal to the negative of the salary payment. The payment carries the bank-row ID. Navigation links associate the movement with the payment and the employee. |

The ordinary salary-payment page requires the write grant, payment date, payment method and positive first entered payment amount. In the presence of the bank module it also requires an account. The underlying payment operation rounds each submitted allocation at amount precision and requires a nonzero total. Negative values are meaningful on adjustment/rejection paths. Each nonzero allocation produces its own salary-payment row. Internally the operation returns the last inserted payment ID. This differs from supplier or customer settlements with a separate many-invoice allocation table.

With automatic closure requested, each salary's payment total is reread and the paid flag is set when the rounded remaining amount equals zero. The lower-level writer does not propagate a failed paid-flag update into its payment error count. An integration reporting payment and classification together should read back both results. A payment-create event can reject the operation. Banking then uses the payment date, method, signed amount, reference and optional value date to create the cash movement. The card treats a failed bank operation as an error in the outer transaction.

## Period and statement examples

An employee is owed 3,500.00 for a completed month. The first transfer is 1,000.00. The outstanding amount becomes 2,500.00 and the bank movement is −1,000.00. A second transfer for 2,500.00 gives a second cash movement and zero outstanding. If automatic closure is selected and classification succeeds, the salary becomes paid. Reopening this record changes the flag. It leaves the two payment rows and their movements intact, so the outstanding calculation remains zero until a transaction changes it.

Deleting a salary payment with a linked bank row first delegates deletion to the bank-line operation. On an error it preserves the payment. After a successful bank deletion it deletes the payment row within the same transaction. The payment delete method does not itself recompute the parent paid flag. If the second payment in the example is removed through an allowed correction, the surviving payment total is 1,000.00 and outstanding is again 2,500.00. Review the salary classification as its own fact.

A bank-order request is an instruction to pay. For the salary route it records the salary ID, requested amount, bank coordinates, request date, actor and entity. Duplicate detection normally checks unprocessed bank requests for that salary. A stricter caller can check processed requests too. Zero-amount requests are refused. A successful request attempts to assign the corresponding transfer method to the obligation. Creating the request alone produces no salary-payment row and does not reduce outstanding.
