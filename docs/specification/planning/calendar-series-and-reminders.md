# Recurring appointments and reminders

A weekly site visit should stay at 09:00 in the organizer's calendar when the clocks change. A reminder belongs to a particular visit and recipient. The calendar writes individual appointment records when creating a series, so each visit has its own start, finish, record ID and reminder dates.

## Series creation

The event card accepts a single event or a weekly, monthly or yearly recurrence. Recurring entries can be disabled for an installation. For the series, the form derives the weekday, day of month, or month and day from the first event's start. It stores the frequency and date component, a shared recurrence identifier and the final recurrence date. A timed appointment requires both a start and a finish. The create action requires an owner or assigned user. Agenda creation grants distinguish acting on one's own records from creating or managing events for others.

| Frequency | Derivation of subsequent starts |
| --- | --- |
| Weekly | Establish the start of the following week's matching weekday, then step forward seven calendar days. The weekday value on this entry path uses Sunday as zero. The weekly generation branch tests for a nonempty weekday, so Sunday is an exception and causes creation to fail. |
| Monthly | Use the first event's day of month and step forward by one calendar month. The form derives that day from the submitted start. |
| Yearly | Use the first event's month and day and step forward by one calendar year. |

The create action writes the initial event, then creates each additional occurrence while its start is on or before the inclusive end-of-day limit. Each additional occurrence inherits the event details and receives its own dates. The operation attaches the selected categories to each created occurrence. A regular appointment that ends after the recurrence limit can still qualify when its start is within the limit. The final date controls generation of starts.

Calendar arithmetic takes place in the user's named time zone when available. A missing or invalid user zone falls back to the server zone. Full-day events configured for storage in GMT use GMT for generation. Start and finish are advanced in the same zone. If an original meeting had positive duration and the new end would fall on or before the start after a daylight-saving adjustment, the operation restores the original elapsed duration for that occurrence.

For example, a Wednesday appointment from 09:00 to 09:45 repeated weekly in a zone whose clocks change on Sunday appears at 09:00 on both Wednesdays. The elapsed time between the two start instants can differ from 168 hours. An appointment in a skipped local clock hour requires the end-date adjustment if the normalized start would otherwise overtake its end. A consumer reconstructing a calendar from the stored occurrences can use their recorded starts and ends directly.

## Recipients, equipment and failure behavior

A reminder stores the event ID, recipient user, delivery type, offset amount and unit, reminder timestamp and processing status. The event form computes its timestamp by subtracting the offset from the start. Email reminders can carry a template ID. On a recurring visit, enabling reminders creates a separate pending reminder for each assigned internal user on each generated event. Three visits with two assigned staff produce six pending reminder records. A pending record establishes the reminder schedule. Delivery status progresses separately.

The creation of the series is wrapped in a database transaction. A failed occurrence or failed reminder insertion causes rollback. The resource-link section explicitly assigns the selected busy resources to the initially created event, using the configured overlap rule. The later-occurrence loop creates the event records, categories and reminders without replaying that resource-link section. A recurrence identifier on a calendar event therefore cannot establish that its room or equipment was reserved for every occurrence. Resource associations are checked per event. On subsequent date edits the event card can compare its linked busy resources against other reservations.

The individual resource allocation's start/end comparison is documented in [Project task schedules, assignments and shared resources](../operations/task-hierarchy-and-resource-booking.md).
