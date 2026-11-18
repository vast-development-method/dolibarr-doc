# Speaker proposals, exhibition booths and conference votes

An event project can collect ideas before its program is confirmed. The speaker or exhibitor supplies a program suggestion. A visitor voting for that idea changes its popularity count. A visitor registering to attend creates an attendee record. These commands have different identities, price bases and state transitions.

## What the project advertises

| Project setting | Public event landing page |
| --- | --- |
| Conference mode 0 | No conference submission or voting button. |
| Conference mode 1 | Visitors can suggest a conference. |
| Conference mode 2 | Visitors can suggest conferences and view and vote on candidates. |
| Conference mode 3 | Visitors can view and vote on candidates. |
| Booth suggestions enabled | Visitors can suggest a booth independently of the conference mode. |

The landing page displays event dates and routes each choice to the corresponding project-scoped form. If none of its three actions is available, it displays an explanation. These are presentation options for contributor activity. Attendance uses a separate whole-event or session invitation, with its own registration conditions.

Project routing and choice visibility appear in `htdocs/public/project/index.php:190–207,260–282,301–325`. For attendee admission, fees, capacity and ticket use see [Event capacity, registration and attendance](../specification/planning/event-capacity-registration-and-payments.md).

## From proposal to program item

Both submissions require a family name, a valid email, organization name, program title and description. A speaker submission also requires the given name. A booth submission requires the country when its price is nonzero. Visitors select a format from the agenda types for the relevant event family. The conference form offers conference formats. The booth form uses booth formats. The records produced by a successful submission are shared across party, contact and event management.

1. Find the business party by organization name or create a prospect with the supplied address, country, region and email. A newly created prospect can receive an automatically generated customer code.
2. Look for a contact by email. If one is needed, create it active, attach it to the resolved party and populate its name and postal details from the form.
3. Apply the configured conference-contributor or booth-contributor customer category. The flow also sets the supplier role on the party and applies supplier numbering where automatic numbering is available. Failure to resolve the selected category is a submission error.
4. Create a calendar program record referencing the project, party, selected format, title and description. The conference also copies the contact's given and family names onto the program record. Assign the contact to the program item in the **speaker** role for a conference or the **responsible person** role for a booth.
5. Determine the program state and any fee document using the contribution type below. Successfully reusing an existing party and contact still produces a new program item on each successful suggestion. Separate presentations by the same speaker remain separate candidates.

The contributor record is distinct from an attendee and from a project-wide contact assignment. For example, a speaker proposing two sessions can have one party and one contact, two program records and two speaker assignments. An attendee count before and after those submissions is unchanged.

The conference form and party population appear in `htdocs/public/project/suggestconference.php:79–90,113–125,221–330,336–399,429–445,653–662`. The booth equivalents appear in `htdocs/public/project/suggestbooth.php:111–122,218–329,335–395,425–441,708–717`.

## Billing an exhibitor

| Contribution | State and document effects on the successful public path |
| --- | --- |
| Conference | Changes the program record to suggested after attaching the speaker. Sends the conference request notice to the resolved business party email using the configured request template, then returns to the acknowledgment page. |
| Booth with zero price | Changes the record to suggested after attaching the responsible contact. Commits and attempts the separately configured booth request email, then returns to acknowledgment. |
| Booth with a nonzero price | Creates an unpaid standard draft customer invoice for the party and event project. Takes payment terms from the contact or falls back to default terms. Links the invoice to the program record. Adds one booth-service line with the project's booth price as its **tax-exclusive** unit price and the applicable customer/service VAT rate. The program remains at the creation default of draft. |

The fee-bearing booth form sends the visitor to the same acknowledgment page as the free submission. Its normal path ends without a checkout redirect, invoice validation or receipt. The invoice is committed before the link and fee line are written. An invoice header left after a later line failure can therefore be real even though the visitor did not see success. The acknowledgment is a project-level message and supplies no evidence of a collected amount. A notification delivery failure is logged independently of the user's successful submission.

For example, a booth price of 120 and an applicable 20% rate produce a draft with net 120, tax 24 and gross 144. The ordinary whole-event **attendee** registration path interprets a registration price of 120 as tax-inclusive. At the same rate its fee line has net 100 and tax 20. Reusing the same amount parser across these two public forms would change one of the invoices.

Booth billing and confirmation appear in `htdocs/public/project/suggestbooth.php:437–506,518–559`, the conference notification in `htdocs/public/project/suggestconference.php:441–505`, and the acknowledgment in `htdocs/public/eventorganization/subscriptionok.php:181–197`. The program status dictionary appears in `htdocs/eventorganization/class/conferenceorbooth.class.php:55–63,110–122`, with the persisted initial default in `htdocs/install/mysql/tables/llx_actioncomm.sql:74–80`.

## Voting and program confirmation

The voting list selects calendar records for the current project and allowed agenda entities, with conference-family formats and program state below confirmed. In the defined status set, this includes drafts (0) and suggestions (1). Confirmed, unqualified, done and cancelled items drop out. The list resolves the party name where a party is associated and presents a vote action per candidate. The standard voting table has no corresponding booth ballot.

A successful vote increases that program record's counter by one and records the candidate in the visitor's session. A repeated vote for the same candidate in that session returns an already-voted message. The visitor can support another listed conference independently. This is a per-candidate session tally. The operation creates no attendee, customer, invoice, named electorate entry or allocation of seats. Failed updates return a voting error. The form returns to the project voting page after processing.

Consider two suggested sessions with counts of 4 and 7. The visitor votes for each, then repeats the first. The resulting counts are 5 and 8. If an organizer confirms the first session, it leaves this candidate list with its previously recorded count. Crossing a vote threshold does not confirm a session. Confirmation is an organizer operation on the program record.

Candidate selection, voting and repeat behavior appear in `htdocs/public/project/viewandvote.php:103–138,141–162,186–225`. Program confirmation is in `htdocs/eventorganization/class/conferenceorbooth.class.php:433–486`.
