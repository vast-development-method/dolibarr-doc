# Leave requests and employee balances

A leave request reserves dates for review. Submission and approval are separate decisions. Approval consumes entitlement immediately in the default configuration. An optional month-end process defers the consumption. These are units of employee time. The transactions described here do not create payroll expense, a liability, or a cash payment. [Module guide](../reference/locators/people-services.md#ref-8a7c906e598a) · [Bundled descriptor and rights](../reference/locators/people-services.md#ref-08fde68765d1) · [Approval transaction](../reference/locators/people-services.md#ref-5d15123cbd03)

## Records and identity

| Record | Identity and relationships | Information that must survive a change of state |
|---|---|---|
| Request | One employee, one leave type, one expected reviewer, entity and reference | Inclusive civil start and end dates, first and last half-day, description, submission, approval, refusal and cancellation actors and times, refusal explanation |
| Leave type | Dictionary identifier and code | Active flag, whether its counter participates in accrual, monthly credit quantity, negative-balance policy |
| Balance | One employee and leave type pair | Current number of days, separately from any request |
| Balance log | Acting user, affected employee and type | Timestamp, reason and resulting balance. The consumption and reversal labels include the request reference |
| Monthly checkpoint | Configuration entry named `lastUpdate` | Last month processed, used for catch-up |

[Request definition](../reference/locators/people-services.md#ref-47cba3db1ad6) · [Type](../reference/locators/people-services.md#ref-0c946121aa90) · [Balance key](../reference/locators/people-services.md#ref-d77d73556060) · [Log](../reference/locators/people-services.md#ref-b94e2d9b4480) · [Monthly processing](../reference/locators/people-services.md#ref-0ff3ddaa9395)

## Request lifecycle

| Operation | Required context | Observable outcome |
|---|---|---|
| Create draft (1) | Actor may write for the target employee. Dates must cover at least half a working day, avoid conflicting leave and identify a permitted reviewer | Draft carries type, dates, owner and expected reviewer. Overlap detection considers drafts, pending and approved requests, skipping canceled and refused records |
| Submit (1 → 2) | Authorized writer for this employee. Recheck the balance if the type blocks a negative result | Assign final reference if provisional and record submitter/time. State 2 means awaiting approval |
| Approve (2 → 3) | Actor has approval rights and is the designated reviewer or also has `writeall`; check the stored record and entitlement again | Record actual approver and time. In immediate mode, save debit and resulting-balance log in the same transaction as the decision. An email delivery warning on the card does not roll back this transaction |
| Refuse (2 → 5) | Same review gate; card requires refusal details | Store decision, actor, date and explanation. No approval debit occurs |
| Cancel (2 or 3 → 4) | Card checks the request's scope and the actor's editing/review authority; past approved leave has an additional approver/administrator check | Stamp cancellation. Previously approved immediate leave is credited back. For deferred leave, the card uses the processed-month cutoff to restrict the credit. Canceling a pending request creates no balance credit |
| Return to draft (4 → 1) | Authorized writer for the owner | The canceled request can be edited and submitted again |

The set of employees a writer can act for normally includes the writer and their subordinates. Reading everybody's requests, writing for everybody, approval and maintaining entitlements each have a distinct grant. The expected reviewer and the person who actually approves are separate identities. [Access checks](../reference/locators/people-services.md#ref-d602340f48db) · [Creation](../reference/locators/people-services.md#ref-2c4ff95441fc) · [Overlap](../reference/locators/people-services.md#ref-955ae99e0871) · [Submission, approval and reversal](../reference/locators/people-services.md#ref-c29d54685678)

## Calculating days

For a multi-day request, take the inclusive civil date count, subtract configured nonworking days including public holidays, subtract 0.5 for an afternoon start on a working day, and subtract 0.5 for a morning finish on a different working day. On a single working day the supported whole-day, morning-only and afternoon-only choices yield 1, 0.5 and 0.5. The card supplies GMT-normalized boundaries, the employee country and employee ID. The calculator falls back to the company country when the caller omits a country; an employee-aware hook may adjust the result. Keep these inputs when reproducing a balance difference. [Calendar calculation](../reference/locators/people-services.md#ref-9553628eb583) · [Half-day encoding](../reference/locators/people-services.md#ref-5d1714be6ef7)

For example, assume Friday and Monday are working days, Saturday and Sunday are closed, and there is no public holiday or employee override. Friday afternoon through Monday morning consumes **1.0 day**. With a balance of 4.5, submission leaves 4.5 available. Immediate approval reduces the balance to 3.5 and cancellation restores it to 4.5. If Monday is a holiday, only Friday afternoon counts and the debit is 0.5. If the balance changes to 0.5 after submission and the type blocks negatives, approval of the original 1.0-day request fails. [Guard at both transitions](../reference/locators/people-services.md#ref-05181f7340af) · [Approval guard](../reference/locators/people-services.md#ref-6f174b3ffc49)

The monthly worker initializes an empty checkpoint in the current month. For each outstanding month it processes active-user counters for active, balance-affecting types with a nonzero monthly credit. It adds that credit, then, when deferred consumption is enabled, deducts qualifying approved leave clipped to the processed month. A type with a zero monthly credit skips this loop's debit step as well. Advancing the checkpoint and updating that month's counters take place inside its transaction. [Counter and checkpoint algorithm](../reference/locators/people-services.md#ref-d849ca9b7f29)

## Command contract and acceptance

`POST holidays/{id}/approve` has no client-supplied debit amount. It loads the request, checks access, state and reviewer, performs the mutation and returns the cleaned request. Missing record yields 404, wrong state 400 and missing authority 403. A model-level approval failure maps to 500. The card's immediate-debit calculation passes the employee ID to the calendar routine; the REST immediate-debit call supplies the employee's country only. Both negative-balance guards pass the employee ID and default the country. A site using employee-specific calendar extensions should test card and REST outcomes separately. [REST approval](../reference/locators/people-services.md#ref-7ca6c882bab9) · [Card approval](../reference/locators/people-services.md#ref-bea1dc4e2eb1)

| Acceptance case | Expected result |
|---|---|
| A draft already spans Tuesday; create another full-day request for the same employee on Tuesday | Creation fails even before the first draft is submitted |
| An approver without global write rights acts on another reviewer's pending request | REST returns 403; request and balance retain the prior values |
| Repeat approval after a successful response | REST returns 400 for the stored state; the debit appears once |
| Approve in deferred mode; cancel a future request entirely beyond the last processed month | Approval retains the counter; cancellation adds zero days |
| Fail a balance update while approving in immediate mode | Request decision and balance-log write roll back together |

The [leave request schema](../../schemas/people-services/leave.schema.json) describes snapshots for this workflow. Period ordering, overlap, permissions and balance arithmetic require a calendar and stored records.
