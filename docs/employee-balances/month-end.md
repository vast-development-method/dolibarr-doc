# Month-end entitlement and the HR report

The scheduled accrual definition is enabled by default, has a daily interval and is available when leave management is enabled. Each invocation compares months. It can do no work on most days and catch up several completed months on a later day. The separate task that sends the previous month's HR information is disabled by default. Sending an HR report makes no balance entry.

## Who is credited

| Input | Selection or calculation |
| --- | --- |
| Checkpoint | The cursor is the value named `lastUpdate` in `holiday_config`. A missing or initially empty cursor is initialized to the current time. While its calendar month is earlier than the current month, process that cursor month and then advance to the first day of the next month. A future cursor yields no catch-up. |
| Counter and employment | Select existing `holiday_users` records joined to active user accounts. The worker's counter query does not select employees by hire date, prorate a month by employment dates, or filter the user by the employee flag. A newly active employee with no counter for the type is absent. The job wrapper does not create missing employee/type pairs. |
| Type and credit | Select `c_holiday_types` with `active = 1`, `affect = 1`, company or common country eligibility and the applicable entity scope including shared types. Look up `newbymonth` by that type ID. A zero or missing rate skips the entire counter for that month, including deferred consumption. A nonzero rate adds the configured amount once. |
| Deferred charges | After the credit, find approved requests for the employee and type whose inclusive dates overlap the processed month. Clip each start and end to that month, compute the days with its stored half-day flag, employee country and ID, and subtract each positive result. A request wholly in the current unclosed month waits. Immediate mode omits this step. |
| Historical settings | Catch-up uses the active users, dictionary and approved request records available when the job runs. It does not reconstruct an earlier rate, employment status or past calendar from effective-date history. An already processed month is not revisited simply because an old request is approved later. |

For example, a counter starts at 4.00, two completed months await processing and the current credit rate is 1.75. With no qualifying absences, it becomes 5.75 then 7.50. A later sequential rerun in the same month leaves 7.50. If the employee previously earned 1.25 in the first month but the rate has since changed to 1.75, the worker still uses 1.75 for both iterations. A retroactive correction needs its own identified adjustment.

The entitlement-maintenance action reads an absolute amount and calls the individual balance writer only after a **changed** balance has been logged. A missing counter reads as zero for that comparison. Entering zero for a missing pair can therefore leave it missing, whereas entering a positive opening balance creates the pair. An existing row with a stored zero participates in a future eligible accrual. A missing row and an existing zero have the same arithmetic value on a statement but different automatic accrual behavior.

## Why a cross-month half-day can disagree with the report

Assume two consecutive months within one year. The first ends on Wednesday and the next starts on Thursday. An approved request starts on Monday afternoon and finishes Friday morning. Tuesday is a public holiday, and all other days in the interval are open. Its stored `halfday` value is 2.

| Interval | Actual open portions of the request | HR report's clipped half-day flag and total | Deferred worker's flag and debit |
| --- | --- | --- | --- |
| Monday to Wednesday | Monday afternoon 0.5, Tuesday closed, Wednesday 1 | Ends at an artificial month boundary, so use −1. Total **1.5**. | Reuses 2, which halves Wednesday as well. Debit **1.0**. |
| Thursday to Friday | Thursday 1, Friday morning 0.5 | Starts at an artificial month boundary, so use 1. Total **1.5**. | Reuses 2, which halves Thursday as well. Debit **1.0**. |
| Whole absence | **3.0 days** | **3.0 days across the two reporting periods** | **2.0 days across the two counter updates** |

The monthly HR display and previous-month HR message adjust the half-day flag when clipping a request boundary. The deferred counter clips dates but passes the original flag through each calculation. With an initial balance of 8.00 and monthly credit of 1.50, the first worker iteration gives 8.50 and the second 9.00. A calculation based on the HR report's three days instead yields 8.00 after both credits. The one-day difference follows from those boundary rules. No extra leave request or payment explains it.

## Cancellation at the last processed date

In deferred mode the cancellation operation derives a cutoff at the last day of the month preceding the cursor. If the request **starts before** and **ends after** that date, the operation clips its end to the cutoff. If the request starts **after** the cutoff, it restores zero. With a start exactly equal to the cutoff, neither of those conditions applies and the original end is used.

Consider a full-day request beginning on the last Wednesday of a processed month and ending on Friday in the next month. All three dates are open. After processing the Wednesday month only, the worker has charged one day. At that point cancellation of the approved request recalculates Wednesday through Friday and credits three days. The request becomes canceled and is ineligible for the subsequent deferred debit. Relative to the one day charged, the employee has received two extra days. This case is observable even with no half-day flags or calendar changes.

## Transaction and audit boundaries

The scheduled wrapper opens an outer transaction. Month iterations and balance-history writes open nested transaction scopes. The transaction manager commits physically at the outer boundary, so a checked failure in a later month can roll back earlier month changes in the same invocation. The worker tests counter-write and cursor-write return values. Its two calls that add history for accrual and consumption do **not** test the returned result. A history-write error alone therefore does not provide the same explicit stop condition as a counter-write error. Reconcile the stored balance and cursor as well as individual log rows.

The cursor lookup and update address the name `lastUpdate`. The configuration table declares a unique pair of entity and name. The balance records use employee/type and have no entity column. A context with shared users or multiple configurations needs to account for these actual keys when reconciling runs. The operation reads current values and writes replacement balances. It does not include a per-employee, per-type, per-month accrual identity or an atomic reservation of a cursor month. Sequential replay after success and independently overlapping worker invocations have different guarantees.

After a late approval, a changed holiday calendar or a cutoff discrepancy, reconcile the affected employee/type's opening balance, monthly credits, original consumption and restoration before entering an absolute correction. The operator's reason and old/new balances preserve how the corrected closing balance was reached.
