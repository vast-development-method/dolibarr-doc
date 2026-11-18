# Contracted services, help desk and interventions

A contract line states what a customer is entitled to receive. A ticket records a request for help; an intervention records work performed for a third party. These records can share customer, contract and project context while maintaining independent lifecycles. An invoice is another commercial document with its own creation and validation.

## Contract and service activation

| Record | Business data | Derived information |
|---|---|---|
| Contract | Third party, reference, contract date, project, document status and signature state | Counts of waiting, current, expired-open and closed lines. Earliest planned expiration among open lines is also stored for lookups |
| Service line | Parent contract, optional catalog item, description, quantity, unit price, discount, tax rates and calculated amounts. Separate planned/actual start and end dates, who opened/closed the service and the operational comment | Whether a still-open line has expired as of a given instant |
| Ticket | Tracking identifier and reference, optional third party and project, assignee, classification, severity, status, progress, last-message and closing times | Help-desk workload and history |
| Intervention | Third party, optional contract and project, reference, status, signature; ordered work lines with date, description and duration | Total seconds and earliest/latest eligible work-line dates |

Validate the draft contract to assign its permanent reference and record header status 1. Unless configured otherwise, validation calls the customer-role update for a third party whose supplier flag is zero. Validation alone leaves service lines waiting. A user can have the right to draft a contract without permission to activate its services. Activation and deactivation have separate grants.

| Line operation | Eligible stored state | Changes |
|---|---|---|
| Activate or reactivate | Waiting (0) or closed (5) | Open (4); write actual start and opener, clear actual closure, record comment, optionally replace planned end. A keep-existing instruction preserves planned end |
| Close | A line still waiting or open | Closed (5); record actual closing date, closer and comment. Refresh earliest planned end over the remaining open lines |
| Evaluate expiration | Open | If planned end is present and strictly earlier than the comparison instant, count as expired. Equality and an absent planned end count as current. Expiration does not change the stored line status |
| Activate all / close all | Iterate the contract's lines, skipping lines already in the desired state | Process within one outer transaction. Closing all sets each line's end to the current time, and can validate a draft header. Consumers should read line states to determine service closure |

For single-line activation the REST adapter uses `PUT contracts/{id}/lines/{lineid}/activate` with an actual-start timestamp, optional planned end and comment. Its paired `unactivate` endpoint calls the input timestamp `datestart` on the wire and uses it as the **actual end**. Both require access to the parent and the corresponding operational right. Success returns the refreshed contract; missing parent yields 404 and insufficient rights yields 403. A trigger failure can roll back the line update. A caller repeating an activation should examine the stored line and history; the update predicate restricts eligible rows, while the implementation checks query success before invoking the trigger.

## Ticket and intervention handoffs

1. **Triage.** Back-office and public intake produce tickets. The desk distinguishes unread (0), read (1), assigned (2), in progress (3), awaiting requester information (5), optional on hold (7), solved (8) and abandoned (9). Assignment normally writes the user and status 2. Auto-read-on-assignment writes status 1 instead. Removing an assignee also returns to read. Managing a ticket uses the write right in standard mode and the dedicated manage permission in advanced mode.
2. **Correspond.** Messages become dated agenda records linked to the ticket. Preserve public replies and internal notes as separate message types. In the ordinary default reply flow a public-facing internal answer on an early-state ticket advances it to in progress. The module also supports a configured status on answer and a separate public-area branch. A reply should therefore carry both origin and visibility.
3. **Record work.** Enter dated, described work lines. The ordinary card requires a nonempty duration unless duration capture is disabled. Quantities of time are stored in seconds. The header sums durations and takes minimum/maximum work dates excluding structural lines (type 9). If there are no qualifying lines, total duration is zero and these dates are empty. The ordinary detail-based card offers validation after a line exists; details-disabled mode can validate a header alone.
4. **Complete.** Closing a ticket stores solved or abandoned, progress 100 and a closing timestamp. With the intervention module active and `WORKFLOW_TICKET_CLOSE_INTERVENTION` enabled, the operation loads linked interventions, validates drafts and sets unfinished records to done. Already terminal tickets return without another close. Reopening on the card selects assigned when there is an assignee, otherwise unread. Reopening does not reopen completed service reports in that action.
5. **Bill.** From a validated intervention the card can start an invoice for the third party with the intervention as origin. The invoice module and invoice-create right are required. Closing a ticket or summing work durations does not price the work, generate a receivable, or settle a customer invoice. Pricing and posting belong to the invoice transaction.

## Acceptance

| Scenario | Expected observation |
|---|---|
| Validate a contract containing two waiting lines, then activate just the first | Contract is validated with one waiting and one open service |
| At noon, inspect two open services ending at noon and at 11:59 | The first counts as current, the second as expired; both retain status 4 |
| Reactivate a closed service with a new actual start | It becomes open, with new opener and start and a cleared actual closing date |
| Two work lines last 45 and 30 minutes plus a heading | Header duration is 4,500 seconds. Earliest/latest work dates are taken only from the work lines |
| Close a ticket with linked draft work while the workflow is enabled, then repeat closure | On success, work is validated and done; repeated closure returns a no-change result. Neither operation creates an invoice |
| Reopen a solved ticket with an assignee | Ticket returns to assigned. The intervention retains its own lifecycle |

The [service action schema](../../schemas/people-services/service-action.schema.json) gives portable command shapes for line activation, line closure and ticket closure. The service resolves the authenticated actor, resource access, parent-child identity and stored status before applying the operation.
