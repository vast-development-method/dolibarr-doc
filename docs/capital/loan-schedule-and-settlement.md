# Reconciling a monthly loan schedule to cash

A due date identifies an obligation. A repayment records the date and amount actually paid. The loan screen can show a paid term due in January alongside a bank payment made in February. The relationship is carried by identifiers. Matching on date, amount or sequence number would lose this settlement.

## From an agreement to the first schedule

The agreement supplies original principal, annual rate as a percentage, number of terms, start date and total insurance. Term 1 falls on the start date. For term `k`, the screen adds `k − 1` calendar months to the original start date. The agreement end date does not determine the interval or override the final term. A nonexistent day spills into the following month. For a 31 January 2026 start, adding one month gives 3 March and adding two months gives 31 March. The second of those dates is still anchored to 31 January.

Let `C` be the balance before a term, `i` the annual percentage divided by 1,200 and `n` the number of terms left including this one. The schedule uses the following amounts.

| Field on the schedule | Value used |
| --- | --- |
| Monthly **Amount** | Principal plus interest. Calculate `C × i / (1 − (1 + i)^(−n))` for a nonzero rate, or `C / n` at zero rate. Round to the configured total-amount precision. |
| Interest | Round `C × i` separately to total-amount precision. There is no count of elapsed days between payments. |
| Principal component | Rounded monthly amount less rounded interest. The next term starts with the rounded difference between the opening principal and this component. The annuity is calculated again for the shorter remaining term. |
| Insurance | Round the agreement's total insurance divided by the original term count. Allocate the difference between total insurance and the sum of these rounded shares to the first term. |
| Planned bank outflow | Monthly amount **plus** the term's insurance. Adding interest again would count it twice. |

Creating the plan stores one row per term with loan ID, expected date, principal, interest and insurance. The database requires unique expected dates within a loan. The term number shown in the interface is its position in the returned rows. The schedule reader filters by loan ID without an explicit sort. The payment action takes the first returned row with an empty bank link. For reconstruction, retain the expected date and schedule-row ID when identifying the term.

The creation response has a display discrepancy. After a term is inserted with separate components, the in-memory object holds their combined total in its principal field. The same request renders that object as though it held plain principal. Reloading the schedule reads the separately stored principal and restores the persisted amount and running balance. On the first example row below the immediate response can show 353.36 as the monthly amount, from 343.36 plus 10.00. A fresh read shows 340.02.

## Changing a term or settling it on another date

| Event | Changed values | Values carried forward |
| --- | --- | --- |
| Edit a future monthly amount in the schedule | Use the preceding term's closing principal as the opening balance. Honour the entered monthly amount on the edited term. Recalculate its interest and closing balance, then the annuity for each later term. | Earlier terms, due dates and insurance allocations retain their places. Saving sends principal as displayed amount less interest. |
| Enter a zero monthly amount in that editor | The recalculator sets this term's interest to zero and carries its entire opening principal to the following term. For example, with 600 principal, two terms left and a 12% annual rate, a zero second-to-last amount gives a final monthly amount of 606, including interest of 6. | The helper still returns the original number of terms. A zero final monthly entry can leave a residual principal in the preview. Creating a term with zero combined principal, interest and insurance is rejected. |
| Pay a term as planned | Store actual principal, interest and insurance with the entered payment date. Set the schedule row's bank movement ID and repayment ID. | No later terms are recalculated when all three components equal those on the selected term. An earlier or later payment date alone leaves the plan intact. |
| Pay different principal or insurance | Record the actual components. The schedule's saved interest is authoritative for the payment. Use actual principal plus that interest as the current monthly amount. Start recalculation from the actual remaining principal supplied by the payment form. Update principal and interest on the current and later schedule rows. | The payment action leaves scheduled insurance and expected dates as stored. The original agreement insurance also stays the same. Changing just insurance still selects the recalculation path. |
| Pay an agreement without a schedule | The operator supplies principal, insurance, interest and actual date. The repayment and its bank movement can be recorded directly. | No term is inferred from the date. Once this type of loan has started or been marked paid, the schedule screen disables creation of an initial schedule. |

The edit and payment recalculator rounds interest and remaining principal to **two decimal places, half up**. It also rounds freshly calculated later monthly amounts to two places. The initial schedule instead follows the installation's total-amount precision. A three-decimal configuration can consequently give different principal and interest splits after an edit. Both forms operate in monthly periods irrespective of the number of days by which a payment was early or late.

The payment form offers the open term's expected date as the initial actual-payment date. Without a term, its date can default to today when date autofill is active. On submission it constructs the payment timestamp at noon on the chosen day. Its summary cell labelled “Date due” displays the loan start date even for a later instalment. Use the schedule row for the individual due date, and use the payment record for the actual date.

## Worked three-term settlement

A loan starts on 31 January 2026 with principal 1,000.00, annual rate 12%, three monthly terms and total insurance 10.00. Amounts use two decimal places.

| Term and due date | Opening principal | Principal | Interest | Insurance | Monthly amount | Closing principal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 · 31 Jan | 1,000.00 | 330.02 | 10.00 | 3.34 | 340.02 | 669.98 |
| 2 · 3 Mar | 669.98 | 333.32 | 6.70 | 3.33 | 340.02 | 336.66 |
| 3 · 31 Mar | 336.66 | 336.66 | 3.37 | 3.33 | 340.03 | 0.00 |

The first repayment arrives on **4 February**. The operator records **400.00 principal and 5.00 insurance**. The payment uses the scheduled 10.00 interest, and the bank outflow is 415.00. The loan's actual principal remaining is now 600.00. The recalculation preserves the first due date and spreads that 600.00 across the two remaining due dates.

| Term due | Revised scheduled principal | Revised scheduled interest | Scheduled insurance | Actual payment date | Actual insurance | Actual bank change | Actual outstanding after payment |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 31 Jan | 400.00 | 10.00 | 3.34 | 4 Feb | 5.00 | −415.00 | 600.00 |
| 3 Mar | 298.51 | 6.00 | 3.33 | 2 Mar | 3.33 | −307.84 | 301.49 |
| 31 Mar | 301.49 | 3.01 | 3.33 | 1 Apr | 3.33 | −307.83 | 0.00 |
| **Total** | **1,000.00** | **19.01** | **10.00** | | **11.66** | **−1,030.67** | |

The 1.66 difference between planned and paid insurance does not change the principal balance. A February cash report captures only 415.00. Through 31 March the actual register contains two repayments totaling 722.84 cash and 698.51 principal. The March schedule contains both remaining due dates, yet 301.49 of principal is still outstanding at that month end. The agreement's current payment list has no as-of filter. To reconstruct the March balance after 1 April, sum actual principal with payment dates through 31 March.

The calculated terms, month-end dates, repricing after the first payment and reloaded repayment components above were reproduced with the stable calculation and record methods. Bank changes are the negatives of the saved three-component totals.

## How to join plan, repayment and ledger

| Result | Join and measurement |
| --- | --- |
| Scheduled position | Select terms by loan ID. Starting with original principal, subtract each stored scheduled principal. The screen calculates displayed insurance shares from the current agreement total and number of terms. This schedule balance includes future terms. |
| Actual outstanding | Select repayments by loan ID and sum the stored principal only. Subtract from original principal. The payment form and the agreement card both use this measure. It includes repayments without a matching bank row. |
| Actual payment history | On the agreement card, join the repayment to the loan and restrict to permitted loan entities. Left-join its payment method and its bank movement, then resolve the bank account from the movement. Sort descending by the repayment date. Each row displays actual principal, interest, insurance and their sum. |
| Banked term | A nonzero bank movement ID marks the plan row paid. The repayment ID supplies the detail link. Join the movement using its row ID. An account ID alone cannot identify the payment. |
| Accounting counterpart | For a loan-payment bank link, the bank journal reads the repayment whose bank movement ID matches, joins its parent loan for account codes, and accumulates the three actual components by account code. Shared codes combine their amounts. For the first repayment the bank credits 415.00. Distinct counterpart accounts debit 400.00, 10.00 and 5.00. |
| Closed agreement | A first repayment normally changes unpaid to started. Closing is an explicit operation. The card tests the outstanding principal rounded to a **whole currency unit** when offering its buttons. For example, at 0.49 outstanding the amount display can still show 0.49 and the card offers classification as paid. At 0.50 it offers payment. |

**Banking disabled.** On the standard path with no selected bank account, recording a payment can start the loan and reduce its outstanding principal while leaving the term's bank marker zero. The schedule row can hold a valid repayment ID but still appear unpaid and be selected again for the next entry. For example, recording 100 principal on a 300 agreement gives a principal balance of 200 and state started, even though the schedule can offer that same term again. A check of the repayment register resolves that discrepancy.

**Removing a repayment.** On a successful deletion the card clears the schedule's bank marker by matching the old bank movement, removes the bank line and repayment, then recalculates the principal paid. It resets the agreement to unpaid if the remaining principal payments sum to zero. It does not reverse the earlier schedule recalculation or clear the schedule's old repayment ID in the marker update. The paid link is hidden once the bank marker is zero. Deleting a reconciled movement is refused. The ordinary bank rule also refuses deletion of a bank movement already posted to the ledger. A bank-line refusal causes the payment deletion transaction to roll back. The repayment card makes deletion unavailable for an agreement already classified paid.

[Loan agreement and repayment contract](loans.md) · [Bank accounts and obligations](../treasury/bank-and-obligations.md)
