# Ticket routing, conversations and resolution

A ticket records a request, the party concerned, a stable tracking identifier, operational state, first-read time, assignee and progress. Contacts, dated conversation entries and linked interventions are separate records. A ticket can continue to belong to the same customer and engineer after its resolution state changes.

## Work queue and assignment

| Code | Staff meaning | Effect on dispatch |
| --- | --- | --- |
| 0 | Unread | An incoming request can enter the queue without a technician. |
| 1 | Read | Staff have acknowledged the request. Returning a ticket to the queue by removing its assignee also sets this state. |
| 2 | Assigned | A technician has been designated. This alone says nothing about time worked. |
| 3 | In progress | Work has started. |
| 5 | More information needed | The next expected contribution is from the requester. |
| 7 | Waiting | Work is on hold. This state distinguishes a general hold from a request for further information. |
| 8 | Closed, solved | Store closure time and 100% progress on the explicit close operation. |
| 9 | Closed, unresolved | The abandon operation also sets closure time and 100% progress. The state code preserves the distinction from a solution. |

Ordinary ticket write permission allows work management when advanced permissions are disabled. Under advanced permissions, moving a case through the queue, assigning it, resolving it and reopening it on the staff card use the specific manage authority. Read, write and delete are individually represented. The existing staff conversation action accepts a follow-up from a user permitted to read the ticket. Changing the subject or its linked contract uses write authority.

The staff create action can immediately acknowledge the case when configured and when the creator has management authority. A separate creator-assignment setting can fill a missing assignee or always assign the creator. Setting an explicit assignee writes their user ID and changes state to assigned, or to read when the automatic-read-on-assignment policy is enabled. Clearing the assignee sets the user field to empty and the state to read. Assignment publishes an assignment event. The staff action then removes superseded internal support-technician contact links and adds the new technician in that role. A contact synchronization error can therefore occur after the routing assignment has succeeded. Reading the assignee and reading the contacts answer two different questions.

The explicit mark-read action writes the read state and the current timestamp. The general state-change action preserves an existing first-read timestamp when setting a nonzero state and supplies one if absent. Changing to unread through that action clears the timestamp. Assigning someone changes the routing state directly and does not itself write the read timestamp. Reports on acknowledgment time should use the dated field.

## Internal notes and customer-visible replies

A conversation entry belongs to the ticket through an activity record. The classification distinguishes an ordinary message, a private message and whether dispatch by email was requested. It retains a label, the message body, time, actor, assigned internal participant, applicable external participants, attachments and parent ticket. Public submissions may also carry a sender email to identify an author without an application user. A supplied summary can replace the subject suffix while retaining a bracketed reference.

Visibility follows the activity classification. While both public and private text are held in the activity’s note field, the public reader excludes activities with the private-message classification, including emailed private entries. The thread reader orders activities by descending event time. The first request and its subject are also available on the ticket itself. Redrafting the first request is a separate staff write action.

| Where the contribution originated | Delivery behavior |
| --- | --- |
| Staff, email delivery disabled | Record the conversation entry. Its chosen visibility still governs which readers can see it. |
| Staff, private, email delivery enabled | Staff recipients may receive a notification. Skip the external delivery branch entirely. |
| Staff, customer-visible, email delivery enabled | Notify eligible internal parties. Build external delivery from linked contacts and configured addressing, including reply-to, originating mailbox or the linked party’s address as applicable. After a successful external send, record last-message-sent information and delivery metadata. |
| Public participant | Create a customer-visible entry. If staff notification is enabled, consider the assigned user, then other internal contacts with addresses. Avoid sending the assigned user’s address twice through those two paths. Use the default notification mailbox if individual addressing yields no one. An option can also include the support mailbox. |

A stored entry and an email delivery are distinguishable outcomes. The record is created before distribution resolves all recipients. A message shown in the staff history with no external recipient is insufficient evidence that the customer received an email. For example, staff can record a private incident diagnosis, email it internally and then publish a separate repair appointment to the customer. Only the appointment appears in the public conversation.

## Public access and resolution

The public ticket view requires a tracking identifier and a valid email address, supplied or recovered for the current session. Once the ticket is found, accepted participants include the originator, an associated external contact, the ticket party’s main address, the creating user and the assigned user. Matching the public participant allows the public conversation flow. It does not grant staff management authority. The public screen offers replies and closure while the request is open. It calls the same resolved-close operation for a public closure, and calls the message service with customer-visible scope for a public reply.

For staff resolution, solved and abandoned use a common close operation with different outcome values. A repeated close on an already solved or abandoned case returns a no-change result. With the intervention module and the linked-intervention closure policy active, closure loads the linked field interventions, validates drafts and attempts to close interventions below closed status, then publishes the ticket-close event. The workflow acts on linked interventions for either resolution outcome. It does not create a customer invoice or a new work order.

Reopening through the management card is available for either terminal state. It restores assigned when an assignee exists and unread when none exists. The reopen handler requests this status change without recalculating a percentage or explicitly clearing the historical closure timestamp. Interpreting a ticket as currently closed must therefore use its current state. For example, an abandoned case with an owner returns to the assigned queue when reopened, even if a prior closure recorded 100% progress.
