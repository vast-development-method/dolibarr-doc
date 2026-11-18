# Portal identity and document delivery

A customer buying through two separate companies can have records under both. The portal resolves one account, one acting party and one entity scope before exposing those records. An employee with internal access to the same files follows a different access path.

## From credential to customer context

| Configured sign-in | Which record qualifies | Identity carried forward |
| --- | --- | --- |
| Party account | Login matches an active account of the reserved portal site within the visible party entities. Exactly one matching row and a matching password hash are required. | Account identifier and the account's linked party. A member can subsequently be looked up by that party. Where partnerships are active, the portal looks up the partnership for the member and party together. |
| Member account | Login matches one member in validated status within the visible member entities, and the password verifies. | Member identifier and that member's linked party for the acting user. Member-specific access can refer to the resolved member. |

The session stores the relevant account identifier. On a request the portal fetches that record again and loads the configured technical user. It assigns the acting user's party identifier from the member or party account. A missing technical user or missing party association prevents normal context initialization. In party-account mode the portal also fetches the party record and uses its preferred language when applicable. A matching login on two eligible records fails the uniqueness condition even if one password would verify.

See `htdocs/webportal/class/context.class.php:716–812` and `htdocs/public/webportal/webportal.main.inc.php:241–370`.

## Commercial and service lists

Each list has its own portal switch and requires the corresponding business area. The built-in list controllers add a party condition before applying the visitor's filters.

| List | Admitted population for the resolved party | Observable consequence |
| --- | --- | --- |
| Proposals | Party owns the proposal and its status differs from draft (0). | A salesperson saving a new draft does not expose it. |
| Customer orders | Same party and status differs from draft (0). | An older, closed order remains eligible for the list. |
| Customer invoices | Same party and status differs from draft (0). | An unpaid validated invoice can appear alongside a settled invoice. |
| Support tickets | Same party and status differs from deleted (9). | A newly received, unread ticket at status 0 remains eligible. |
| Field interventions | Same party and status differs from draft (0). | Filtering for validated and unsigned matches validated interventions with a null or zero signature flag. Other signature filters select their corresponding signature flag on a validated intervention. |

The member and partnership profile cards have independent visibility settings and require an actual member or partnership in the visitor context. Both *visible* and *edit* grant reading. Only *edit* grants the form's update capability. The form is bound to the resolved member or partnership identifier. Its delete-record, edit-note and unlink permissions are all disabled.

See `htdocs/webportal/controllers/propallist.controller.class.php:41–85`, `orderlist.controller.class.php:41–82`, `invoicelist.controller.class.php:40–81`, `ticketlist.controller.class.php:45–81`, `ficheinterlist.controller.class.php:40–103`, `membercard.controller.class.php:40–83` and `partnershipcard.controller.class.php:40–82` in the same directory.

## Three document populations

| What the visitor opens | How the population is selected | Detail that matters to delivery |
| --- | --- | --- |
| Party's own documents | The party-document switch grants listing. The portal uses the party's entity output directory and its numeric party identifier as the directory name. | Lists direct files in descending date order. It does not walk child folders for this view. |
| Shared document area | A separate shared-document switch exposes the configured shared document root. | Each page lists the current folder's direct files and subfolders in name order. A subfolder link carries the relative directory. The download link identifies a shared document under that root. |
| A generated commercial or service PDF | The domain list switch, authenticated party identifier, requested party identifier, content type, active module and entity output configuration must all qualify in the default handler. | For supported domains the document index must identify the source object. The handler checks the indexed object's relationship to the acting party before delivering the file. |

For the generated PDF route the supported sources are customer invoices, orders, proposals, tickets and field interventions. The lookup combines the stored filename with its directory. Two parties may both have a file called “summary.pdf”. The filename alone establishes neither which object produced it nor who can receive it. If the file exists on disk but its index entry has no source object or the object belongs to another party, the built-in path denies delivery. Integrations can supply a separate download decision through the documented extension point.

See `htdocs/webportal/controllers/documentlist.controller.class.php:44–110`, `htdocs/webportal/controllers/shareddocuments.controller.class.php:34–150` and `htdocs/webportal/controllers/document.controller.class.php:175–235`.

## Example — renewal and invoice

A portal account for company 42 resolves to member 17. The member-card setting permits editing and the invoice list is enabled. The member may update permitted fields of profile 17 and see validated invoices addressed to company 42. A draft renewal invoice stays out of that list. A member-card edit leaves both invoice ownership and invoice publication status intact. Once staff validate the renewal invoice, its row can appear. Downloading its generated PDF still depends on the indexed file identifying the invoice owned by company 42.
