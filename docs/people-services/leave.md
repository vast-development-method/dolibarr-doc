# Leave requests and employee balances

A leave request reserves dates for review. Submission and approval are separate decisions. Approval consumes entitlement immediately in the default configuration. An optional month-end process defers the consumption. These are units of employee time. The transactions described here do not create payroll expense, a liability, or a cash payment. [Module guide](https://wiki.dolibarr.org/index.php/Module_Holiday) · [Bundled descriptor and rights](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/modules/modHoliday.class.php#L64-L87) · [Approval transaction](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L638-L745)

## Records and identity

| Record | Identity and relationships | Information that must survive a change of state |
|---|---|---|
| Request | One employee, one leave type, one expected reviewer, entity and reference | Inclusive civil start and end dates, first and last half-day, description, submission, approval, refusal and cancellation actors and times, refusal explanation |
| Leave type | Dictionary identifier and code | Active flag, whether its counter participates in accrual, monthly credit quantity, negative-balance policy |
| Balance | One employee and leave type pair | Current number of days, separately from any request |
| Balance log | Acting user, affected employee and type | Timestamp, reason and resulting balance. The consumption and reversal labels include the request reference |
| Monthly checkpoint | Configuration entry named `lastUpdate` | Last month processed, used for catch-up |

[Request definition](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_holiday.sql) · [Type](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_c_holiday_types.sql) · [Balance key](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_holiday_users.key.sql) · [Log](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_holiday_logs.sql) · [Monthly processing](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/holiday.class.php#L1718-L1869)

## Request lifecycle

| Operation | Required context | Observable outcome |
|---|---|---|
| Create draft (1) | Actor may write for the target employee. Dates must cover at least half a working day, avoid conflicting leave and identify a permitted reviewer | Draft carries type, dates, owner and expected reviewer. Overlap detection considers drafts, pending and approved requests, skipping canceled and refused records |
| Submit (1 → 2) | Authorized writer for this employee. Recheck the balance if the type blocks a negative result | Assign final reference if provisional and record submitter/time. State 2 means awaiting approval |
| Approve (2 → 3) | Actor has approval rights and is the designated reviewer or also has `writeall`; check the stored record and entitlement again | Record actual approver and time. In immediate mode, save debit and resulting-balance log in the same transaction as the decision. An email delivery warning on the card does not roll back this transaction |
| Refuse (2 → 5) | Same review gate; card requires refusal details | Store decision, actor, date and explanation. No approval debit occurs |
| Cancel (2 or 3 → 4) | Card checks the request's scope and the actor's editing/review authority; past approved leave has an additional approver/administrator check | Stamp cancellation. Previously approved immediate leave is credited back. For deferred leave, the card uses the processed-month cutoff to restrict the credit. Canceling a pending request creates no balance credit |
| Return to draft (4 → 1) | Authorized writer for the owner | The canceled request can be edited and submitted again |

The set of employees a writer can act for normally includes the writer and their subordinates. Reading everybody's requests, writing for everybody, approval and maintaining entitlements each have a distinct grant. The expected reviewer and the person who actually approves are separate identities. [Access checks](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L88-L125) · [Creation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L184-L302) · [Overlap](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/holiday.class.php#L1250-L1338) · [Submission, approval and reversal](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L482-L954)

## Calculating days

For a multi-day request, take the inclusive civil date count, subtract configured nonworking days including public holidays, subtract 0.5 for an afternoon start on a working day, and subtract 0.5 for a morning finish on a different working day. On a single working day the supported whole-day, morning-only and afternoon-only choices yield 1, 0.5 and 0.5. The card supplies GMT-normalized boundaries, the employee country and employee ID. The calculator falls back to the company country when the caller omits a country; an employee-aware hook may adjust the result. Keep these inputs when reproducing a balance difference. [Calendar calculation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/date.lib.php#L1357-L1442) · [Half-day encoding](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L184-L202)

For example, assume Friday and Monday are working days, Saturday and Sunday are closed, and there is no public holiday or employee override. Friday afternoon through Monday morning consumes **1.0 day**. With a balance of 4.5, submission leaves 4.5 available. Immediate approval reduces the balance to 3.5 and cancellation restores it to 4.5. If Monday is a holiday, only Friday afternoon counts and the debit is 0.5. If the balance changes to 0.5 after submission and the type blocks negatives, approval of the original 1.0-day request fails. [Guard at both transitions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/holiday.class.php#L777-L801) · [Approval guard](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/holiday.class.php#L910-L930)

The monthly worker initializes an empty checkpoint in the current month. For each outstanding month it processes active-user counters for active, balance-affecting types with a nonzero monthly credit. It adds that credit, then, when deferred consumption is enabled, deducts qualifying approved leave clipped to the processed month. A type with a zero monthly credit skips this loop's debit step as well. Advancing the checkpoint and updating that month's counters take place inside its transaction. [Counter and checkpoint algorithm](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/holiday.class.php#L1728-L1868)

## Command contract and acceptance

`POST holidays/{id}/approve` has no client-supplied debit amount. It loads the request, checks access, state and reviewer, performs the mutation and returns the cleaned request. Missing record yields 404, wrong state 400 and missing authority 403. A model-level approval failure maps to 500. The card's immediate-debit calculation passes the employee ID to the calendar routine; the REST immediate-debit call supplies the employee's country only. Both negative-balance guards pass the employee ID and default the country. A site using employee-specific calendar extensions should test card and REST outcomes separately. [REST approval](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/class/api_holidays.class.php#L480-L541) · [Card approval](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/holiday/card.php#L638-L687)

| Acceptance case | Expected result |
|---|---|
| A draft already spans Tuesday; create another full-day request for the same employee on Tuesday | Creation fails even before the first draft is submitted |
| An approver without global write rights acts on another reviewer's pending request | REST returns 403; request and balance retain the prior values |
| Repeat approval after a successful response | REST returns 400 for the stored state; the debit appears once |
| Approve in deferred mode; cancel a future request entirely beyond the last processed month | Approval retains the counter; cancellation adds zero days |
| Fail a balance update while approving in immediate mode | Request decision and balance-log write roll back together |

The [leave request schema](../../schemas/people-services/leave.schema.json) describes snapshots for this workflow. Period ordering, overlap, permissions and balance arithmetic require a calendar and stored records.
