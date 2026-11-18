# Employee leave statement and corrections

Use the pair `holiday_users.fk_user` and `fk_type` to identify a balance. The unique key permits one `nb_holiday` for that pair. The corresponding request stores `fk_user`, `fk_type`, `date_debut`, `date_fin`, `halfday`, `statut` and the expected `fk_validator`. Each history row has a separate `rowid`. Its `fk_user_update` is the employee affected and `fk_user_action` is the actor, including the account running the accrual job. Read `prev_solde` and `new_solde` numerically when reconciling because both history columns are character fields. The stored movement equals new minus previous, in days.

`holiday_logs.type_action` holds the reason text. Some paths include the commercial request reference in that text. The log has no dedicated request-ID or accrual-month column. Two applications for the same number of days must be distinguished by their record identity and decision history.

## One employee, two absences and one adjustment

Assume an existing annual leave balance of 6.25 days, a monthly credit of 1.50, immediate deductions, an active employee and no schedule extension. Saturday and Sunday are closed. On request A, Monday is a public holiday for the employee and company. Request B is for a different open Wednesday afternoon only.

| Operation | Request state or event | Change | Resulting annual balance |
| --- | --- | ---: | ---: |
| Scheduled job processes one completed month | Monthly credit for this employee and type. A second run while the cursor is in the current month has no month to process. | +1.50 | 7.75 |
| Employee submits A, Friday afternoon through Tuesday morning | `statut` becomes 2. Submission records `fk_user_valid` and `date_valid` and emits `HOLIDAY_VALIDATE`. | 0.00 | 7.75 |
| Designated reviewer approves A on the individual card | Friday afternoon is 0.50, then the weekend and public holiday contribute zero, and Tuesday morning is 0.50. The approved request records `fk_user_approve`, `date_approval` and state 3. | −1.00 | 6.75 |
| Reviewer attempts the same approval again after its commit | The approval entry checks that the persisted state is awaiting approval. The service returns a state error on a sequential repeat. | 0.00 | 6.75 |
| Reviewer approves submitted request B | A single open day marked afternoon only consumes 0.50. | −0.50 | 6.25 |
| Authorized operator cancels the approved A | Record `fk_user_cancel`, `date_cancel` and state 4. The immediate policy restores A's recalculated working days. B remains approved. | +1.00 | 7.25 |
| Entitlement administrator sets a corrected absolute balance of 7.50 and records a reason | The previous and replacement balances are normalized to five decimals. History records 7.25 → 7.50. | +0.25 | 7.50 |
| Same target of 7.50 submitted again | Equality at the stored comparison precision produces no additional log entry. | 0.00 | 7.50 |

The check is 6.25 + 1.50 − 1.00 − 0.50 + 1.00 + 0.25 = **7.50**. A presubmission or approval rule that blocks a negative balance compares requested days with the **current** balance. Deferred mode can admit several individually affordable approvals before they are charged. That check by itself reserves no entitlement for a different approved request. The monthly worker subtracts the approved days and has no separate zero floor on its resulting counter.

## Working time, request state and the counter

| Stored half-day | First date | Last date | Quantity on a single open date with inclusive counting |
| ---: | --- | --- | ---: |
| 0 | Morning | Afternoon | 1.0 |
| −1 | Afternoon | Afternoon | 0.5 |
| 1 | Morning | Morning | 0.5 |
| 2 | Afternoon | Morning | 0.0 under the calculator. This describes a useful boundary pair on different days. |

For a range covering multiple dates, begin with the inclusive civil-day count less closed dates. Deduct half for an afternoon start on an open starting date and half for a morning end on an open ending date. A date that is both a weekend and a public holiday is closed once. The active holiday calendar includes common and applicable country records in the leave entity scope. An undated recurring month/day applies each year, while a specified year limits the fixed date. Calendar rules can also produce movable holidays. Standard weekly closure is configurable for Monday, Friday, Saturday and Sunday.

Employment `weeklyhours` is not an input to that base day count or to the monthly accrual rate. A positive employee ID permits a working-calendar extension to replace the computed day quantity. The individual approval card passes employee ID and country for consumption. The approval admission check passes employee ID with company country as the fallback. The immediate service consumption call passes employee country without the employee ID. Matching request dates can therefore yield different day quantities when an employee schedule or another country calendar matters. The optional calendar conversion to hours multiplies the day quantity by 24 and returns an integer. The leave account paths above request **days**. A half-day on this ledger is not automatically four hours of work or pay.

## Read the events in order

On the ordinary card path, the decision writer first updates the request and emits `HOLIDAY_APPROVE`. Under immediate deduction the caller then writes balance history and the new counter before completing the surrounding transaction. An approval observer can therefore see an approved request before the corresponding balance debit. In deferred mode no debit accompanies the approval.

The card cancellation first updates the request and emits the ordinary `HOLIDAY_MODIFY`. When canceling a previously approved request, it then emits `HOLIDAY_CANCEL` before recalculating the restoration, writing history and storing the balance. Canceling a pending request produces no restoration. A second sequential cancellation cannot credit a state-4 request again. The individual card's return-to-draft action puts a canceled request back into state 1. The separate service reopen operation sends an eligible canceled request through submission into state 2. Neither action recreates an approval debit.

The restoration uses the working calendar and deduction policy in force at cancellation. It reads no immutable consumption quantity from the original log. In the example, if Monday ceases to be a public holiday before cancellation and the policy still deducts immediately, A is recalculated as two days. The cancellation would credit 2.00 against the original 1.00 debit. An explicit corrective balance entry can explain the resulting difference without losing the decision record.
