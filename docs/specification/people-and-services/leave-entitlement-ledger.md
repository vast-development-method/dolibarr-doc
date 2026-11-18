# Leave entitlements across reporting months

An employee has a balance for each leave type that participates in entitlement accounting. A leave request names the employee, type, first and last dates, boundary half-days and approver. The request can be approved before its days are charged. The setting for deduction timing determines which of those events changes the available balance.

## Balances and correction entries

| Record | Key or owner | Meaning |
| --- | --- | --- |
| Leave type | Dictionary ID | Activation, effect on entitlement, monthly credit and rules for insufficient balance. |
| Balance | Employee and leave type | Current number of days. An employee can have, for example, separate annual and training balances. |
| Balance history | Employee, type, change timestamp and acting user | Previous balance, new balance and reason. The change in days is the difference between the two stored balances. |
| Leave accounting cursor | Configuration name `lastUpdate` | Month reached by the accrual process. The next run processes the months between this value and the current month. |

An entitlement administrator enters an **absolute balance** for a selected employee and active balance-affecting type. Blank input leaves a value untouched. An explicit zero clears the balance. The operation reads the old value, normalizes the old and new values to five decimals and writes a history row only for a change. It can attach an operator's explanation. It updates the balance after recording that history in the same outer transaction. Entering 4.5 for a previous 3.0 creates a change of +1.5. Entering 4.5 a second time creates no additional movement. The individual writer can create the employee/type row when required.

Implementation evidence appears in `htdocs/holiday/define_holiday.php:150–208`, `htdocs/holiday/class/holiday.class.php:1860–1910,2289–2350`.

## Monthly accrual and consumption

The first run with an empty cursor stores the current timestamp as its starting point. Subsequent runs advance a month at a time. A run in July with a cursor in April can process April, May and June in sequence. Each iteration selects existing balances joined to active users, fetches active leave types that affect entitlement and looks up that type's monthly credit. A zero credit skips that balance for the iteration. In the deferred-deduction route this also skips the consumption loop for that balance.

For each eligible balance, the process first adds the monthly credit. Under immediate deduction, this finishes the month's processing for that balance. Under month-end deduction, it also loads approved requests for that employee and type whose dates intersect the month. It clips each request to the month and deducts the calculated open days. The calculation receives the stored half-day setting, employee and country. A zero or negative duration produces no debit. The cursor advances to the first of the next month after the updates. An unchanged cursor month yields no additional monthly credit.

For example, an employee starts a completed month with 7.00 days and accrues 1.75. One approved three-day absence falls entirely in the month. With month-end deduction, the credit brings the balance to 8.75 and the debit brings it to 5.75. With immediate deduction, approval has already reduced the opening 7.00 to 4.00, and accrual subsequently brings it to 5.75. A manager reading the balance between the two events sees different values under the two policies.

Implementation evidence appears in `htdocs/holiday/class/holiday.class.php:282–299,1718–1861,2117–2180`.

## Which days count

A date range includes its final day for leave consumption. The normal calculation subtracts configured nonworking weekdays and public holidays. The default weekly pattern excludes Saturday and Sunday. Configuration can change Monday, Friday, Saturday and Sunday. Public holidays may apply across countries or to the selected country and can carry a particular year or recur. The calculation falls back to the organisation's country when no country is supplied. Working-day extensions may supply an employee-specific result.

A start in the afternoon removes half a day only if the starting date is open. An end in the morning removes half a day only if the ending date is open. For a single open date, a morning-only or afternoon-only request consumes 0.5. For a multi-day request spanning a weekend with Friday afternoon start and Monday morning end, the default weekly pattern yields 1.0 day. If Monday is a public holiday, the same range yields 0.5 day. Approval's insufficient-balance check uses the date-only UTC endpoints where available to avoid daylight-saving transitions distorting a whole-day calculation.

The overlap check is separate from the day count. It ignores cancelled and refused records, considers full containment as well as intersecting endpoints, and treats complementary half-days at an otherwise shared boundary separately. A draft can therefore affect whether another request for the same time can be entered even though the draft has yet to debit entitlement.

Implementation evidence appears in `htdocs/core/lib/date.lib.php:787–1040,1357–1440`, `htdocs/holiday/class/holiday.class.php:910–937,1260–1344`.

## Approval, cancellation and restoration

The approval balance guard calculates the prospective balance before changing the request. When the guard is active, a result below zero refuses approval. A result exactly zero meets this particular constraint. The web action handles the immediate counter movement separately from the approval state change. The stored charge and the guard can receive different calendar context because the guard passes an empty country, which resolves to the organisation, while the consumption action supplies the employee's country. For organisations with staff in several countries, these calendars can yield different counts on the same dates.

Cancellation accepts requests pending approval or already approved under the card's owner, delegated write or approver rules. An already-ended approved request also requires the appropriate approval authority. Pending cancellation changes request state without returning days. For a previously approved request, the action records the cancelling actor and timestamp and calculates restoration according to the deduction policy. Under month-end deduction, a request wholly after the last processed month usually has zero debit to restore. For a request crossing that month-end, the handler clips the end date to the processed cutoff using its strict date comparisons. Reopening a cancelled request returns it to draft and does not itself reapprove it.

For instance, let the cursor be 1 June, so May is the last processed month. An approved absence from 28 May through 3 June has been charged only for the open May portion under deferred deduction. Cancelling it restores that May portion. Adding the unused June portion as a credit would overstate the employee's entitlement. At the exact cutoff the implementation uses strict before/after comparisons, so reproducing a boundary-day result requires the actual start and end dates.

Implementation evidence appears in `htdocs/holiday/card.php:637–682,841–950`, `htdocs/holiday/class/holiday.class.php:910–1040`.
