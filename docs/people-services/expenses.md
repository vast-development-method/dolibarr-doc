# Expense claims, reimbursement and journal entries

An employee submits a claim for a period. An approver authorizes reimbursement, a payer records the transfer to the employee, and an accountant binds expense lines to accounts and posts the report. The employee appears as a user and accounting subledger party. Expense reports have their own payment records. [Module guide](https://wiki.dolibarr.org/index.php/Module_Expense_Reports) · [Module descriptor and permissions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/modules/modExpenseReport.class.php#L109-L169)

## Data and approval

| Record | Fields and relationships |
|---|---|
| Report | Entity, employee, period start/end, reference, expected reviewer, actual decision actors/dates, status, paid flag, aggregate net, VAT, local taxes, gross |
| Expense line | Parent report, date, expense type, quantity, gross unit value, VAT rate/source, net/VAT/gross and local taxes, optional mileage category, project, document file and accounting binding |
| Payment | One report per payment, date, amount, payment method, optional reference/note, creator and linked bank transaction. A report can have several payments |
| Accounting entry | Source type `expense_report`, source document/detail identifiers, posting date, entity, journal, account and optional employee subledger |

[Header](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_expensereport.sql) · [Lines](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_expensereport_det.sql) · [Payments](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_payment_expensereport.sql) · [Posting detail](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/accountancy/journal/expensereportsjournal.php#L307-L336)

The back-office card distinguishes draft (0), pending approval (2), canceled (4), approved (5), closed/paid (6) and refused (99). Submit assigns a final reference and stamps validation. Approve records the acting user and date. Refusal records the reason and clears the approval actor. Draft and refused reports accept line changes; a corrected refusal can return directly to pending. The card also allows refusal of an approved report. Capture each transition explicitly when integrating. [State gates](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/card.php#L233-L258) · [Submission and review mutations](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/expensereport.class.php#L1359-L1610)

Reading covers the actor's hierarchy, global readers, and the designated reviewer with approval rights. When advanced permissions are enabled, global writers can also read. Approval on a readable report requires the approval right. The card allows an authorized reader with this grant to approve even if another user was nominated. The card checks the pending state before approval; the REST approval method delegates directly to the domain method, whose protection checks whether it is already approved. A rebuilding client following the card lifecycle must enforce pending-to-approved itself. Payment and accounting posting have separate grants. The project and supporting-file fields on the card can be made mandatory through configuration. [Card access and settings](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/card.php#L126-L166) · [Card approval](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/card.php#L669-L678) · [REST approval](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/api_expensereports.class.php#L737-L763) · [Domain approval](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/expensereport.class.php#L1523-L1566)

## Allowable amount

Expense entry accepts a tax-inclusive unit price. The standard line routine computes all tax bases, applies a mileage offset when applicable, evaluates expense rules, inserts the line and recalculates the report total. A rule can cap one expense or aggregate by day, month or year for the employee and expense type. An advisory rule records a warning; a restrictive rule deducts the excess from the current line's gross and recalculates its components. Subsequent rules see the effect of earlier caps. [Line and rule calculation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/expensereport.class.php#L1975-L2153)

For example, enter two meals at 57.50 each with 15% VAT and no local tax. Gross is 115.00, net is 100.00 and VAT is 15.00. With a restrictive per-expense gross limit of 92.00, excess is 23.00. The allowable line becomes 92.00 gross, 80.00 net and 12.00 VAT. With an advisory rule alone, the warning accompanies the 115.00 gross line. Compute the reimbursable balance from the stored gross after rule processing.

## Reimbursement contract

`POST expensereports/{id}/payments` accepts payment type (`fk_typepayment`), payment date (`datep`), amounts (`amounts`, keyed by employee in the normal card flow), and a positive account ID (`accountid`) when banking is enabled. The caller needs the payment right and resource access. For an approved report compute **remaining = roundToMoney(report gross − sum of recorded payments)**. Reject payment above remaining. A zero payment is rejected by the payment model. A positive reimbursement creates a negative bank movement, links it to the payment and employee, recalculates remaining and marks paid when fully settled. The REST write returns the payment ID. A bank-link failure rolls the payment back. A separate classify-paid action exists, so a paid status by itself cannot establish a bank transfer. [API fields](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/api_expensereports.class.php#L42-L70) · [Payment transaction and errors](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/api_expensereports.class.php#L1010-L1091) · [Bank links](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/paymentexpensereport.class.php#L546-L628) · [Manual classification](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expensereport/class/expensereport.class.php#L823-L859)

## Posting contract

The expense journal selects the current accounting entity's bound expense lines with a report status numerically greater than zero, optionally filtered by report period start, binding cutoff and whether a journal entry already exists. That predicate also includes states other than approved. A rebuild requiring approval first must implement that as an explicit policy. Posting requires the accounting binding-write grant. A selected report with an unbound nonzero line is held back; a report with no bound lines is absent from the candidate set. By default the document date is period start; configuration can use its end. [Eligibility and entity scope](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/accountancy/journal/expensereportsjournal.php#L87-L165) · [Amounts, date and binding check](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/accountancy/journal/expensereportsjournal.php#L187-L303)

| Positive claim of 92.00 | Debit | Credit |
|---|---:|---:|
| Bound expense account | 80.00 | |
| Purchase VAT account | 12.00 | |
| Employee clearing account with employee subledger | | 92.00 |

If tax dispatch is disabled, debit the bound expense account for 92.00. The employee credit is still 92.00. The journal groups amounts by report and account, checks the debit/credit totals at monetary precision and commits or rolls back **per report**. Journalization and the bank payment are independent transactions. [Posting implementation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/accountancy/journal/expensereportsjournal.php#L276-L509)

## Acceptance

| Given and action | Expected outcome |
|---|---|
| Approved 92.00 claim; record 40.00, then 52.00 | First payment leaves 52.00 outstanding; second closes the report. With banking enabled the two linked bank movements are −40.00 and −52.00 |
| Remaining 52.00; submit 52.01 | REST returns 400 before inserting a payment |
| Report is pending; payer attempts to reimburse it | REST returns 400. Approval and payment remain separate |
| One of two nonzero lines is unbound; attempt journalization | No partial postings for this report |
| Tax dispatch is disabled | Expense debit equals gross with no separate VAT debit for the example |

The [reimbursement schema](../../schemas/people-services/reimbursement.schema.json) models a positive reimbursement command in business terms. The component executing it must look up the report, outstanding amount, bank setting and access rights.
