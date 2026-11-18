# Website publishing and customer access

The ERP has two distinct publication models. The website module publishes authored pages and translations. The web portal supplies controllers that read selected ERP records for a signed-in customer or member. Enabling a public website does not grant access to an invoice.

## Site and page publication

| Command | Caller and input | Result or guard |
| --- | --- | --- |
| Add a page | Website editor supplies site, page type, alias, language, title, content and optionally a parent-language page. | The editor creates a draft. The create operation removes invalid characters from the alias, collapses repeated hyphens and removes a leading hyphen. Regional language tags resolve to their primary language. The unique key is site plus page alias, including for translations. |
| Toggle the site | A user with website write permission takes the site online or offline. | Change the site status and invoke the website modification event. The editing UI keeps an offline site's individual page switches inactive. |
| Publish a page | On an online site, a website writer can toggle the page's online status. | The editor distinguishes the status of the site from that of the particular page. Taking a whole site offline uses the site status. The source has separate rights for content reads, ordinary authoring, privileged code authoring, deletion and export. |
| Resolve a translation | Select the original page and the primary target language. | The lookup can resolve a translated page by original-page ID and language. Locale metadata, alternative aliases and page content remain fields of the page. |

**Acceptance.** Create the alias `board--news` with language `en_GB`. The stored alias is `board-news` and language is `en`. Another page in the same site using the normalized alias fails the uniqueness check. The same alias can be used in another site. A writer with ordinary content-authoring rights alone has no privileged code-authoring grant.

## Portal account and invoice list

The third-party account stores its organisation, login, enabled status, entity and portal identifier. The login resolver requires one matching active account within the accessible party entities and verifies its password. The portal administration permission `webportal.write` is separately assigned to staff who manage accounts. The portal context can also authenticate members. Each controller registers its own requirements.

**List customer invoices.** The caller has a logged-in third-party session. Enable customer invoicing and the `WEBPORTAL_INVOICE_LIST_ACCESS` setting. The controller derives the party ID from the session context. Its query requires that party on the invoice and excludes draft status 0. Other controllers cover proposals, orders, interventions, tickets, documents and membership with their own rules. An invoice list entry conveys no independent authority to render an arbitrary stored file.

**Acceptance.** Give customer A one draft and one validated invoice and customer B one validated invoice. A's portal list contains exactly A's validated invoice. Turn off the invoice-list setting and the controller denies the list. Deactivate A's portal account and a new login cannot succeed. A separate logged-in back-office user with permission to manage portal accounts is not a substitute for A's customer context.
