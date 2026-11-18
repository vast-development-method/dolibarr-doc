# Employee expenses from approval to the general ledger

An approved expense claim establishes what the employee may recover. Account assignment determines where each cost will be recognised. Journal transfer recognises the expense and the employee liability. A later reimbursement pays down that liability. The four operations have different owners, dates and records.

| Decision | Business record | Where to follow it |
| --- | --- | --- |
| Who incurred the expense, who reviewed it and how much was approved? | `expensereport`, `expensereport_det`, employee and reviewer identities | [Claim approval and reimbursement](../workforce-operations/expense-review-and-reimbursement.md) and [people record dictionary](../records/people.md#record-expensereport) |
| Which lines still need an account? | `expensereport_det.fk_code_ventilation`, fee type and active chart | [Account assignment](account-assignment.md) |
| Which reporting period, expense accounts, taxes and employee balance receive the entry? | `accounting_bookkeeping` grouped by claim and account | [Transfer rules and replay](journal-transfer.md) |
| What should a reviewer see after partial preparation, transfer and a partial reimbursement? | Two claim lines, one ledger movement and two independent cash events | [Worked reconciliation](worked-reconciliation.md) |
| Which payments appear under employee, bank, period and permission filters? | `payment_expensereport` or `payment_salary` linked to its own parent | [Employee payment registers](employee-payment-registers.md) |

## Identities carried through the process

| Role or key | Stored value | Use |
| --- | --- | --- |
| Employer | `expensereport.entity` | Accounting preparation uses the claim's owning entity. |
| Beneficiary | `expensereport.fk_user_author → user.rowid` | The employee for whom the costs were incurred. Their current account code and name are read for the transfer. |
| Expected reviewer | `expensereport.fk_user_validator` | Routes the initial request and contributes to card visibility. |
| Submitted by | `expensereport.fk_user_valid`, `date_valid` | Validation changes draft `0` into submitted `2` and assigns the final reference to a provisional claim. |
| Approved by | `expensereport.fk_user_approve`, `date_approve` | The approval command requires the approve grant and a visible submitted claim. It writes approved state `5` and the acting user's identity. |
| Expense and receipt | `expensereport_det.rowid`, `fk_expensereport`, `fk_ecm_files`, `date` | Each line belongs to one claim. The receipt link and expense date identify the underlying expenditure. |
| Booked by | `accounting_bookkeeping.fk_user_author` | The accounting operator who transferred the claim. |
| Paid by | `payment_expensereport.fk_user_creat` | The actor recording each reimbursement. The beneficiary is resolved through its parent claim. |

Refusal records `fk_user_refuse`, `date_refuse` and `detail_refuse`, clears the approving user and changes the status to `99`. Cancellation records `fk_user_cancel` and `date_cancel` and sets status `4`. The ordinary preparation queues use the document's current status. They do not create or reverse an existing ledger movement when approval changes. For a filed movement, the accountant must separately reconcile the source decision, payment trail and recorded entries.
