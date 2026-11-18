# Event capacity, registration and attendance

An organized event is a use of a project. The project defines event dates, location, registration price, booth price, eligibility for conference and booth suggestions, and an optional maximum attendance. A particular conference or booth is a separate program record linked to the project. A person's registration, ticket usage and payment belong to the attendee record.

## What is being counted

| Record or count | Scope | Interpretation |
| --- | --- | --- |
| Project event | Whole organized event | Holds the event dates, even if project work starts earlier. The optional overall maximum belongs here. |
| Conference or booth | A program item in the project | Carries its own calendar times, format, description and status. The defined states are draft, suggested, confirmed, unqualified, done and cancelled. |
| Attendee registration | Person, project and registration context | Carries identity and address/contact information for registration, subscription date, state, amount and associated invoice where applicable. |
| General-event admission count | Registrations for the project whose states are draft or validated | Used when presenting availability for the overall event. It excludes used and cancelled attendee records. |
| Financial denominator | Validated attendee records for the project | The financial overview shows profit per validated attendee when at least two qualify. This can differ from both registrations made and people who have entered. |

If the maximum is 50 and the project has 47 validated registrations, three draft registrations and four used tickets, the public general-event form's count is 50. The form can show that the limit has been reached and suppress entry. The financial denominator for that same population is 47. A ticket moved from validated to used increases recorded attendance while lowering both of those state-filtered counts. The two views answer different questions and are poor substitutes for a running door count.

The standard public subscription page supplies the overall maximum on the whole-event path. A conference or booth has its own program record but this path does not load a session-specific seating maximum for it. A maximum displayed by the public whole-event form is an availability indication. The registration model has no distinct seat-hold record with an expiry or reserved seat number. A sold ticket and a dated busy reservation on a room's calendar are independent records.

Event and program fields are in `htdocs/projet/class/project.class.php` and `htdocs/eventorganization/class/conferenceorbooth.class.php`. The public count and form are in `htdocs/public/eventorganization/attendee_new.php`. The financial denominator is in `htdocs/projet/element.php`.

## Registration and repeat submissions

The public page uses a registration context for either an organized project or one conference/booth. The add action checks for a confirmed program item or a validated project in its loaded context. The public form collects name and email. Fee-based registration also requires a company name. For general registration the duplicate lookup uses project and email. For an individual session it uses program record and email. Accordingly, one attendee may have distinct registration contexts for two sessions.

A matching unpaid registration can be updated with current details and additional fields. A paid registration with a subscription date and nonzero amount is recognized on return and the page avoids processing it again as a new enrollment. Financial liability is attached to the existing attendee/invoice link. The visitor's email address alone does not identify an invoice across unrelated events.

When the price is zero, the registration path can complete without creating a customer. It marks the registration validated and commits before sending its confirmation email. A mail delivery problem therefore does not mean that the registration failed to persist. When the project charges a fee, the flow resolves or creates the customer as needed and prepares a standard customer invoice. The draft can take the project's identifier and the applicable payment terms. The attendee stores the invoice identifier. On resubmission the existing invoice can be reused.

If no invoice lines already exist, the fee generates a single service line at quantity one based on the tax-inclusive registration price. Configuration can supply the service product. A paid registration for 120 at 20% VAT can therefore give a 100 tax-exclusive line and 20 of tax. The standard paid path prepares the payment step for the registration. An attendee record with an invoice ID indicates the billing link, while its amount, subscription date and status identify the recorded registration and payment state.

The public free and paid flows and their duplicate lookup are in `htdocs/public/eventorganization/attendee_new.php`. Registration lifecycle and labels are in `htdocs/eventorganization/class/conferenceorboothattendee.class.php`. Back-office record permissions and actions are in `htdocs/eventorganization/conferenceorboothattendee_card.php`.
