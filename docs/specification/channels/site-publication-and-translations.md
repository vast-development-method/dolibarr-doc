# Site publication, translation and revisions

A site holds the main language, additional languages, current home page, entity and online state. A page holds its own identity, alias, language, optional translation parent, content, publication state and editorial metadata. The public entry page and the generated representation of each page are stored separately from these records.

## Addresses and language identity

Site creation reduces a regional language such as `en_US` or `en-US` to `en`. It applies the same rule to each additional language and drops empty list entries. A main language is required. A page's language undergoes the same normalization at creation.

Page creation allows letters, digits, dashes and underscores in the primary alias. It removes other characters, collapses repeated dashes and removes a leading dash. The pair of site identifier and resulting primary alias must be unique. Two language variants on the same site consequently need separate primary aliases. Two sites can reuse one alias. Alternate aliases are a separate list kept with the page.

The page record can hold a container type, title, description, keywords, representative image, search-engine directives, framing permission, page header, body and an optional business-object type and identifier. It records its creator and creation time, a modifying user, modification time and an optional public author alias. Public credit and internal authorship serve different purposes.

Related records include [Site page](../../records/content.md#record-website_page).

## Copy and translation

| Operation | Initial new record | Resulting relationship |
| --- | --- | --- |
| Copy a page | New identity, new alias (or one derived from the supplied title), fresh creation time, cleared alternate aliases and author alias, description initialized from title, offline state. | Ordinary copies have no translation parent and can have a different destination site. Editing the new page changes its own content. |
| Translate into a secondary language | The same copy operation sets the requested language and starts the translation offline. | New page points at the source page by identifier. Site consistency is a condition of translation. |
| Create the site's main-language page from an existing translation | New main-language page starts offline with no translation parent. | After the new row exists, the operation updates the original page so it points to the new main-language page. |

A translation carries its own text, alias, publication state and editor. Editing the main page does not update its translations in this operation. The fetch contract supports both site/alias lookup and lookup by translation parent and language. A rebuild needs to preserve the numeric links when URLs or titles change.

## Making an edit visible

1. The editor selects a site and page. A saved body edit requires site editing permission. Changing embedded server-side content is subject to an additional authoring permission. The page creation interface also disallows server-side content in a page header.
2. The edit replaces the current body on the selected row. Head sections are stripped from that body at this stage. Metadata such as the page header has its own storage. The editor receives an error when the database update fails.
3. After the content update commits, the publisher writes the master file, alias routing and rendered page content. A storage failure here can leave the editor's saved body ahead of the public representation. Repair the failed publication from the saved record, preserving its page identity and translation links.
4. Selecting a home page is a separate operation. It commits the site's home-page identifier, then generates the index pointing to the chosen page. If index generation fails, the stored home-page choice already reflects the edit.

The site's online/offline transition requires editing permission. The editor suppresses the individual page switch on an offline site and for setup containers. On an online site it enables the switch for an existing ordinary container when the user has site-write permission. A page copy therefore provides an offline working record with its own address. Saving an edit directly on the published record uses the existing address and can regenerate its public content immediately.

The page table declares a history-retention field defaulting to five. The body-save operation described above overwrites the current record and regenerates output. The field alone does not establish a snapshot-restore interface, a scheduled release or an approval workflow.

## Example — moving the home page to a new language

A site uses English as its main language. An editor translates its French welcome page into English. The resulting English page becomes a translation root, and the original French page points to it. The copy initially remains offline. Placing the English page online and choosing it as the home page are distinct actions. A failed index write after the home-page choice requires regenerating the entry page. Creating a second English copy would allocate a different identifier and would leave the stored home-page choice pointing at the first copy.
