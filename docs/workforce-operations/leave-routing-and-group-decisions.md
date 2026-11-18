# Leave routing, group requests and approval batches

A leave request identifies the employee, the expected approver, the person who submitted it and the person who approved it. A supervisor preparing a request for a subordinate can occupy just the submission role. Reassignment changes where the pending decision is routed. It preserves the employee whose entitlement is at stake. The [entitlement ledger](../specification/people-and-services/leave-entitlement-ledger.md) explains accrual and consumption.

## Find a request and choose a reviewer

The employee hierarchy used by the card and list is the acting user plus their descendants. Individual request access starts with the employee stored on the request. Read-all gives broad visibility. Ordinary read admits an employee in the actor's hierarchy. A designated approver with the approval grant can also read the card, unless the subordinate-only option suppresses this alternative. On the list, the ordinary population is restricted to employees in the hierarchy. Specifying an approver filter narrows that population. An approver can consequently receive a link to a legitimately assigned request that is absent from their ordinary employee list.

The new-request reviewer picker starts with the beneficiary's individually configured leave approver, falling back to their supervisor. Preparing the request on behalf of someone else switches this lookup to that beneficiary. An entity-level default takes precedence. A positive selection already made on the form takes precedence again. The options come from users with the leave-approval grant directly or through a group, filtered through the user selector. The single-request creation action requires a positive reviewer found among the registered approvers. Ordinary write is limited to the employee hierarchy. Write-all permits another employee to be selected. An approver who can open the existing card can use its reviewer-change action to update the expected reviewer. This updates the request without approving it.

Sources are `htdocs/holiday/card.php:89–140,182–222,275–304,322–341,1251–1279`, `htdocs/holiday/list.php:331–369`, `htdocs/holiday/class/holiday.class.php:2192–2224` and `htdocs/user/class/user.class.php:4149–4189`.

## Three ways of approving

| Question | Individual request card | Leave list bulk approval | Leave service approval |
| --- | --- | --- | --- |
| Who may decide? | Approval grant and either the designated reviewer or leave write-all, subject to card access. | Approval grant and the actual designated reviewer on each selected request. | Approval grant and resource access, then the designated reviewer or leave write-all. |
| Which state qualifies? | Submitted and awaiting approval. | Same. Other states produce a warning and are skipped. A row awaiting someone else's approval generates a message and is skipped. | Same. An ineligible state is reported as a bad request. |
| Which audit fields change? | Sets approval date and actual approver. Preserves the submission fields fetched with the request. | Sets both submission and approval dates to the current time and both actors to the approver. | Sets approval date and actual approver, retaining the loaded submission fields. |
| What changes the balance? | Immediate mode counts working days and posts the new balance with its reference. The calendar calculation receives employee country and employee ID. | Immediate mode uses the employee country but omits employee ID. The balance log uses a general leave description. | Immediate mode uses employee country without employee ID and logs the request reference. |
| When does an email go out? | The card tries to notify the employee inside its outer transaction. It supports blind copy. A missing address or mail failure does not reject the approval. | The list tries to notify each approved employee before the final commit. Its explicit send has no blind copy. A delivery error is a warning. | The service calls the approval operation and its event with explicit balance handling. The direct employee email produced by the card and list is outside this service path. |

All three defer the immediate balance write when month-end deduction is selected. The optional employee-specific working-time adjustment receives control only when the calendar call includes a positive employee ID. The standard calendar can therefore agree across entry points even where a site-specific employee schedule would give a different result. The balance admission inside the underlying approval operation and the subsequent deduction are separate calls.

In bulk approval, a missing selected record breaks the batch. A business approval error, balance-log error or detected balance-write failure sets the batch error. The outer transaction rolls back earlier database changes when there is a hard error. Already sent messages can survive rollback. A mixed selection containing only ineligible or differently assigned extra rows can still commit the eligible approvals. The selected row count, number actually approved and number of emails delivered need separate interpretation.

Suppose a supervisor submits two requests for a technician on Monday. The designated reviewer approves the first on Tuesday through its card and the second on Wednesday from the list. In both cases the technician owns the leave. The first request retains the supervisor as submitter and the reviewer as approver. The second records the reviewer in both fields and replaces the submission timestamp. A payroll report built from the submission field alone would attribute the requests to different people even though both originated with the supervisor.

Sources are `htdocs/holiday/card.php:637–747`, `htdocs/core/actions_massactions.inc.php:1783–1911`, `htdocs/holiday/class/api_holidays.class.php:480–542`, `htdocs/holiday/class/holiday.class.php:910–1034` and `htdocs/core/lib/date.lib.php:1357–1439`.

## Company-wide group absence

The collective form requires the authority to write leave for everyone. The operator supplies a leave type, period, start/end half days, reviewer and one or more employees or groups. The common period must contain at least half a business day under the company's calendar. Group membership and individually selected employees are combined by user ID. An employee selected individually and through two groups yields one request.

The action first checks existing overlaps for every selected employee. An overlap identified during this stage stops the whole insert phase. Once admitted, the action creates a separate request for each employee in an outer transaction. There is no single request with multiple beneficiaries. A failed creation or a reported validation error causes rollback of the batch. Each resulting request has its own reference, owner, future approval and cancellation history.

The optional automatic submission first validates each request under the selected reviewer's identity. The request becomes submitted and awaits approval. If the optional mail choice is also enabled, the mail helper fetches the submitted request and calls validation again with the operating user before contacting the designated reviewer. That repeat validation can write a later submission actor and trigger another validation event. An employee balance is charged through approval or month-end processing. Collective submission alone establishes no approval debit. The mail helper provides a message and severity to the form, so a mail warning and a successfully committed request can coexist.

For a three-person maintenance team with members A, B and C, selecting the team and A explicitly yields three prospective requests. If B has a conflicting absence, none are created by this action. If the conflict is resolved and the operation runs successfully with automatic submission only, three independent requests await the common reviewer. Approving A later changes A's request and A's balance according to the deduction policy.

Sources are `htdocs/holiday/card_group.php:128–138,174–197,221–365,696–737,812–834` and `htdocs/holiday/class/holiday.class.php:776–897`.

## Expected reviewer and mail recipient

Submission on the individual card directs mail to the expected reviewer's current email address. The sender can use the leave-specific address with the company sender as fallback. The submission notice can include a short-notice warning by leave type and an insufficient-balance warning for a counter-bearing type. These warnings are composed after successful submission. The employee's leave record therefore carries the decision even when the reviewer's mailbox is empty. Approval mail instead targets the employee. On the card the text naming who validated the leave is assembled from the expected reviewer field. If someone with write-all and approval actually approved, the actor stored in the approval field can differ from the name printed in that email. The approval ledger should take its actor from the record.

Sources are `htdocs/holiday/card.php:482–610,637–746`.
