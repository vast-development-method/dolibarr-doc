# Features outside the stable module filter

Four experimental, four development and three deprecated definitions complete the [95-module inventory](modules.json). Their setup labels describe different levels of implementation. Appointment booking writes contacts and appointments. Collaborative editing registers a menu but provides no editor. The following sections identify the operation an administrator or operator can actually perform.

For an inactive module, the administration catalogue requires `MAIN_FEATURES_LEVEL` of at least 1 for experimental features, at least 2 for development features and below zero for deprecated features. An enabled module can pass this maturity check after the level changes. The stable-only filter still excludes all eleven. An administrator activates modules, and feature-specific grants, dependencies and hidden switches apply separately. [Configuration and visibility](README.md)

## Experimental features

### Appointment booking · `BookCal`

Staff maintain calendars and their availability periods with separate read, write and delete rights for each record family. A period in `bookcal_availabilities` points to `bookcal_calendar` through `fk_bookcal_calendar` and supplies its date limits, daily hours, duration and status. Both record families have configurable-field tables. The public slot query selects enabled periods (status 1) for the chosen calendar and day. It marks matching appointment start times occupied using agenda records with code `AC_RDV`, status zero and the same calendar ID.

A public booking requires given name, family name and email. It reuses a contact with that combination or creates one, then creates an agenda appointment linked to the contact and calendar. The end is the requested start plus the submitted duration in minutes. The contact and appointment writes share a transaction. The public submission tests for a non-draft calendar. A slot shown as free remains a suggestion until submission. The booking write does not repeat the slot calculation or reserve a unique calendar/start pair. The stored appointment and its participants are the evidence of a booking. [Agenda and event records](../engagement/agenda-and-events.md)

### Formula pricing · `DynamicPrices`

The product price editor can associate an item with `c_price_expression` through `fk_price_expression`. A supplier price uses `fk_supplier_price_expression`. Choosing a fixed price clears the product’s expression association. The editor uses product or service modification rights. An administrator manages global price variables and their updaters. Activation loads the expression, global-variable and updater tables.

The sale calculation supplies the minimum available supplier unit price with and without discount, or zero for each if no offer is found. It also exposes product cost, weighted average cost, minimum price, dimensions, rates, custom fields and configured global values. Pending variable updaters run when the parser evaluates an expression. Each advances its next run by its interval in minutes and records its result, then the parser reads the global values. An unresolved variable, invalid expression or negative result produces an error. On a successful sale calculation the result is floored at the product minimum. A formula result of 8 with a minimum of 10 gives a selling price of 10. The supplier calculation instead supplies the supplier quantity and VAT rate, and returns the evaluated result directly. [Catalogue prices and supplier offers](../supply/catalogue.md)

### Notes on record cards · `QuickMemo`

The module registers note controls on supported record screens. A nonzero `MODULE_QUICKMEMO_DISABLED` hides its definition from setup. Creating a note requires memo write permission. `quickmemo_memo` stores the text, owner, target record type and ID, display context, colour, sharing and privacy settings. A note can be archived or used to define a reusable template. Custom values use the memo’s configurable-field table. The interface requires memo read permission and tests ownership for private notes.

A reader can move or resize an accessible note. The active user's position, dimensions and stacking order are written to `quickmemo_memo_user` using the memo and user IDs. Moving a shared note on one person's display leaves the other person's layout intact. Editing or archiving the shared note changes the memo itself. The note deletion action checks write permission. Template deletion has a separate delete-permission check. [Definitions of the memo tables](../relational-model/README.md)

### Event subscriptions · `Zapier`

Activation requests the REST API. The connector declares separate read, write and delete permissions for subscriptions. Creation takes a destination URL and records the authenticated user in `zapier_hook.fk_user`. The stored subscription includes its module and action. For a handled event, the subscriber lowercases the first two parts of the event code, matches them against the stored pair and sends the cleaned object as JSON to each matching URL.

The send branches cover creation and modification of users, third parties, contacts and members, plus creation of appointments, customer orders and tickets. That gives eleven dispatching events. A subscription record alone does not establish that a named event will dispatch. The subscriber returns zero after sending and does not persist a transport acknowledgement. The general webhook module has its own target matching and per-target history. [Subscriber effects](../event-effects/README.md)

## Development features

### Shared document workspace · `Collab`

Activation registers a collaboration menu and temporary directory. A nonzero `MODULE_COLLAB_DISABLED` hides the definition. The landing screen requires administrator access. It reads action selections and renders a form with an empty toolbar. It has no implemented create, edit, save or share action and declares no active collaboration grants. Enabling it therefore creates no shared document, editing session or permission to co-edit. Ordinary file storage, indexing, classification and access use the [document workspace](../data-exchange/documents-and-classification.md).

### Direct-mail document generation · `DocumentGeneration`

Activation creates a temporary directory and registers document read and delete grants. The definition provides no associated setup page, generation menu, model, batch writer or recipient queue. There is no standalone direct-mail run to reconcile. Invoice and shipment output instead comes from the document's own layout, generation action and file storage. Mailing campaigns have their own messages and target rows. [Document generation and indexing](../document-lifecycle/README.md) · [Campaign targets and sending](../specification/channels/campaign-target-delivery-and-suppression.md)

### Label layouts · `Label`

Activation provisions temporary storage and declares sticker read, create/modify and delete rights. Enabling labels, barcodes or membership makes the card-format dictionary available. A `c_format_cards` record describes the paper, orientation, measurement unit, margins, row and column counts, spacing, dimensions and text size. It defines how labels fit on a sheet. Barcode and member workflows can use those formats independently of this module. The definition has no standalone queue of printed stickers. Selecting a layout or printing a sheet does not allocate a new barcode, serial or stock unit. [Barcode identities and printable labels](../specification/equipment/barcode-identities-and-label-sheets.md)

### Goods and services declarations · `Intracommreport`

Activation requests invoicing, tax management and categories, loads `intracommreport` and declares read, write and delete rights. Each row identifies a saved declaration by reference, family, period, direction and processing mode and can hold XML. Preparation selects qualifying invoice lines for a month. Outbound goods and services draw on customer invoices, inbound goods on supplier invoices. The normal item writers receive each invoice's header net total. Two eligible lines on a 150 invoice can therefore contribute two XML items of 150. A downloaded file or saved report records local preparation. A filing acknowledgement belongs to the receiving authority. [Selection, amounts and XML output](../registers-accounts/intra-community.md)

## Deprecated interfaces

### Remote file browser · `FTP`

The client opens a numbered, configured remote server using its host, port, account and connection mode. The default port is 21 when omitted. The connection helper selects ordinary FTP, FTP over TLS or SFTP according to configuration and the available runtime extensions. Read access covers browsing and downloading. Write actions include upload, remote directory creation, and deleting selected files or a directory. A transfer result belongs to that remote session. A remote file can exist without an entry in the ERP's local document index, and a local indexed document can exist without a remote copy. [Document workspace and indexed files](../data-exchange/documents-and-classification.md)

### Membership list and publishing accounts · `MailmanSpip`

Activation requests the membership module. List subscriptions and publishing accounts have separate enablement and connection settings. Member validation can subscribe the email address. Termination or deletion removes it. A change of email or membership type can invoke removal and then addition. Category link and unlink events can also change subscriptions where the record supports them. A configured list can apply to all members, a member type or a category. The publishing connector can create an author row in the external database and remove it by login. These are external writes. Check the external subscription or author account independently of the local membership status, particularly after a partially successful change. [Membership and subscriptions](../engagement/membership-and-donations.md) · [Subscriber order and results](../event-effects/README.md)

### SOAP business services · `WebServices`

This module publishes 41 registered operations across twelve WSDL service families. Enabling it exposes the SOAP interface separately from the REST API. The shared authentication routine checks the configured service key, a supplied numeric entity when present, the user account and its credentials. Business operations apply their own access checks. An order inquiry by ID or reference reads the order and returns a structured response.

| Service family | Registered operations |
| --- | --- |
| Agenda | List event types, read, create and update an event. |
| Categories | Read a category. |
| Contacts | Read, create, list by third party and update. |
| Customer invoices | Read, list by third party, create, create from an order and update. |
| Customer orders | Read, list by third party, create, update and validate. |
| General | Read service or application version information and retrieve a document. |
| Payments | Create a payment. |
| Products and services | Read, create, update, delete, list and list by category. |
| Projects | Create and read. |
| Supplier invoices | Read and list by third party. |
| Third parties | Read, create, update, list and delete. |
| Users and groups | Read a user, list groups, create a user from a third party and set a user password. |

The [REST service contracts](../services/README.md) describe the separately implemented resource routes, inputs and returns. A SOAP method and a REST operation with similar business purposes can require different credentials, arguments and response handling.
