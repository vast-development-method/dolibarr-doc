# Employee reimbursement and salary payment registers

A person can receive a salary and reimbursement for travel on the same day. Each payment belongs to a different obligation. The amount on a payment row answers how much was paid in the selected period. Outstanding liability requires the obligation amount and all payments applied to it, including payments outside that period.

## Expense reimbursements

Start at `payment_expensereport.rowid`. Follow `fk_expensereport → expensereport.rowid` and `expensereport.fk_user_author → user.rowid` for the beneficiary. `fk_typepayment → c_paiement.id` supplies the method. `fk_bank → bank.rowid → bank.fk_account → bank_account.rowid` supplies the cash account. Payment reference on the register is the payment row ID. `num_payment` is the separate cheque or transfer reference.

The read grant `expensereport.lire` admits the operator. The query restricts the parent claim to the expense-report entity population. Ordinarily it also restricts `fk_user_author` to the actor and their subordinates. Either read-all grant (`readall` or `lire_tous`) or advanced all-employee writing when enabled removes this employee filter. Being the designated reviewer alone does not broaden this payment list. A missing bank or method mapping leaves payment history visible when no filter requires that mapping. A missing parent has no eligible entity and cannot appear.

| Operator filter | Compared value |
| --- | --- |
| Payment reference | Search the payment's `rowid`. |
| Payment period | Inclusive lower and upper bounds on `datep`, from the start to the end of the selected days. |
| Employee | Search beneficiary login, last name or first name. |
| Payment type | Exact **method code** in `c_paiement.code`. |
| Cheque or transfer | Search `num_payment`. |
| Bank account | Positive `bank.fk_account`, reached through the bank movement. |
| Amount | Numeric search on `payment_expensereport.amount`. |
| Search across fields | Payment row ID, beneficiary login, cheque/transfer reference and payment amount. |

Rows group by individual payment identity and displayed attributes. One claim with two payments has two rows even if they share a bank account and payment method. Default ordering is descending payment date. The displayed amount and total accumulator use each returned payment's own amount. Neither approval date nor claim gross supplies the payment amount. The register does not impose a closed-claim predicate.

## Salary disbursements

A salary obligation `salary.rowid` can own several `payment_salary` rows through `fk_salary`. The register requires a matching parent salary and a matching `user` on **the salary's** `fk_user`. Payment type and bank are optional joins through the same method and bank tables as the reimbursement register. Entity selection uses `payment_salary.entity`. The operator passes salary-area access before row-level employee restrictions apply.

| Salary grant combination | Employee predicate on payment rows |
| --- | --- |
| Neither `readchild` nor `readall` | `payment_salary.fk_user` must equal the actor and belong to their hierarchy (the hierarchy includes the actor). |
| `readchild` only | `payment_salary.fk_user` must belong to the hierarchy. |
| `readall` only | `payment_salary.fk_user` must equal the actor. |
| Both | No additional employee predicate. The entity and mandatory joins still apply. |

The recipient name and email search uses the parent salary employee, while the employee restriction uses `payment_salary.fk_user`. This difference is material for real records. The salary payment creation operation writes `fk_salary` and `fk_user_author` but omits the optional payment `fk_user`. In a newly created row retaining the default null, the parent identifies the beneficiary normally but neither the equality nor membership predicate can match the payment's employee. Such a payment may appear in a fully authorised register or in its salary's own settlement total while being absent from a restricted register. A salary obligation and its actual payment therefore remain necessary for reconciliation.

| Operator filter | Compared value |
| --- | --- |
| Salary reference and payment reference | Separate exact integer comparisons with `salary.rowid` and `payment_salary.rowid`. |
| Employee and label | Search the parent employee's login, first name, last name or email, and the parent salary label. |
| Payment date and salary period | The two inclusive ranges operate on `payment_salary.datep` and `salary.dateep`, respectively. The latter is the salary period's end. |
| Amount and transfer reference | Numeric comparison with `payment_salary.amount`, text search on `num_payment`. |
| Payment method | Exact `payment_salary.fk_typepayment` ID. |
| Bank account and bank movement | Independent comparisons with `bank.fk_account` and `payment_salary.fk_bank`. The bank value date comes from `bank.datev`. |

For a salary obligation of 1,000, payments of 600 in period A and 400 in B have distinct payment IDs. After both are recorded, the parent's paid sum is 1,000. A filter for payment period B returns 400 if the rows satisfy the visibility rules. A simultaneous salary period-end filter can remove that 400 when the salary period ended in A. The payment amount is independent of the employee's current salary rate and any historical rate stored on the payment.

On the salary payment form, the suggested amount is parent salary amount less recorded payments. The form requires a method, payment date, a positive first entered amount and, if banking is enabled, a bank account. The payment writer rounds each allocation and the aggregate to monetary precision, rejects a zero total, and stores each nonzero salary allocation on its own row. When closure is requested it tests the salary's remaining balance after insertion and marks it paid on exactly zero. The form wraps creation and the bank operation in one outer transaction. A reported bank failure rolls it back. A new payment is a new accounting event. Reopening a salary or changing its displayed status does not constitute evidence that a previous bank transfer was repaid.
