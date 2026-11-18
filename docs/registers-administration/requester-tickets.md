# Requester's public ticket register

The support module and its public interface must both be enabled. A requester presents a tracking reference and a valid email address associated with that ticket. Recognized associations at this step include a linked external contact, the linked company's address, the creating user's address or the originating email. The verified address determines the resulting register.

| Decision | Visible result |
| --- | --- |
| Ticket population | Within the ticket entity scope, show tickets linked to that address through an active external ticket-contact role, the linked company's email or the ticket's own originating email. Association as the internal creator alone is sufficient for the initial address check but does not independently select every ticket the user created. |
| Relationships | A ticket's type, category, severity, company, creator and assignee supply display values. Contact-role assignments join to external contacts. The projection selects distinct ticket records, so multiple qualifying links to the same address need not create duplicate rows. |
| Subject and classification | Subject uses a contains search. Ticket type, category and severity use exact stored codes. The public category picker offers publicly designated categories. |
| People and status | A positive assignee selection is an exact match. A positive creator selection uses the register's text containment comparison on the stored creator ID. A single status selects the numeric code. The nonclosed selection admits precisely codes 0, 1, 3, 4, 5 and 6. |
| Dates and progress | Default ordering is by creation time descending. Creation, first-read and closure are separate dates. The standard public filter set does not apply an interval to them. The progress column is available when public progress display is enabled. |

Suppose a verified customer's address is the originating email on ticket A and an active external contact on ticket B. Ticket A also carries the same company email. The register can show A and B once each. A ticket C linked only to a different address remains outside the register even if it shares A's type and subject. Selecting one severity then narrows the already eligible tickets.
