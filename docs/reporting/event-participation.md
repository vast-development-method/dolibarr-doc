# Event registration, capacity and participant economics

Event activity is attached to a project. An individual activity such as a conference or booth can also carry attendee registrations. A registration record has its own reference, project, attendee email, registration date, status and optional invoice, paid amount and party. Two registrations with the same email remain separate rows. Counting records, counting unique people, available capacity and attendance therefore require explicit populations.

## Operational measures

| Question | Implemented population |
| --- | --- |
| How many registration records are associated with this event? | The event project tab counts attendee rows matching the project. Its count has no status condition, so drafts, registered, showed-up and cancelled records can all appear. |
| How many records are associated with one session or booth? | The activity tab counts registrations by the activity identity. It does not require a specific registration status. Its count and the project-wide tab count can be cached for 120 seconds. |
| Which participants are registered or checked in? | The participant list filters by project or selected activity and can filter the registration status. Draft is 0, registered is 1, showed up is 5 and cancelled is 9. An attended registration carries its own status and will not appear in a filter restricted to registered. |
| Does the public registration page show capacity remaining? | For an event project it counts registrations in draft or registered status and compares the result with the project's maximum. A nonzero maximum is reached at equality. Used and cancelled tickets are outside this count. |
| What did registrants pay? | The list's paid amount is the amount recorded on the registration. Its optional invoice link identifies the associated accounting document. Counting registration rows or summing this field alone does not recover invoice payment allocations. |

For five registrations consisting of one draft, two registered, one showed-up and one cancelled, the event tab can show five. The public capacity counter sees three against the configured limit. A list filtered to showed-up shows one. A change from registered to showed-up increases attendance but reduces the population used by the public capacity counter. Because it includes drafts, that counter also depends on participants who have yet to complete registration.

Registration date orders business activity differently from the date of the event or its session. The list's registration filter uses the registration field, while a project or activity restriction chooses which event the record belongs to. Operators can open an attendee record by registration reference and, when supplied, follow its invoice and party links. Access to the internal participant list uses the project area and its permissions.

## Profit per validated attendee

For a project organizing an event the linked-elements financial view calculates profit per attendee only when at least two registrations currently have **validated/registered** status for that project. It divides the project's signed net balance by that count and does the same with the gross balance. The numerator comes from the project income and cost families configured for the balance. It is independent of the participant list's recorded paid-amount column. The denominator excludes drafts, cancellations and registrations already changed to showed-up status.

With a project net balance of 900 and three registered tickets, the view reports 300 net profit per validated attendee. If one ticket changes to showed-up and the balance stays 900, the remaining two registered tickets yield 450. With only one registered ticket remaining the row is suppressed. This measure cannot be interpreted as cost per person who attended. For attendance by project or session, the showed-up status itself supplies the relevant population. For a distinct visitor count across sessions, the record-by-record tab totals do not establish that registrations represent different people.
