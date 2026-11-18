# Stable module coverage

The configuration catalogue contains **95 module declarations**. The module administration screen's stable filter admits **84**. Four declare experimental status, four development status and three deprecated status. These counts describe the available declarations before applying visibility and dependency rules. An individual installation can expose a different set because of its supplier configuration, organisation, enabled modules and instance settings.

[Machine-readable module inventory](modules.json) provides the descriptor key, numeric module ID, functional area, setup family, maturity and eligibility for every module. Optional fields describe activation dependencies, conflicts and conditional visibility. The activation setting combines `MAIN_MODULE_` with the uppercase module key. For example, `Facture` uses `MAIN_MODULE_FACTURE`. Permission namespaces and public API resource names can differ. The inventory records scope eligibility. Chapter coverage is tracked separately in the [blueprint index](../../README.md).

For progress on individual records, services, lists and reports, see the [coverage checkpoint](checkpoint.md) and [operator-list inventory](operator-list-inventory.md).

## Modules by business area

| Area | Stable | Other descriptor classifications |
| --- | --- | --- |
| Platform and access | BlockedLog, Cron, DataPolicy, DebugBar, ModuleBuilder, Syslog, User | — |
| Documents, reference data and productivity | Barcode, Bookmark, Categorie, ECM, Export, ExternalRss, Fckeditor, Import, Subtotals | Collab (development), DocumentGeneration (development), Label (development), QuickMemo (experimental) |
| Partners, selling and margin | Commande, Expedition, Margin, Partnership, Propale, Societe | — |
| Catalogue and warehouse | Product, ProductBatch, Service, Stock, StockTransfer, Variants | DynamicPrices (experimental) |
| Purchasing and receipt | Fournisseur, Incoterm, Reception, SupplierInvoice, SupplierOrder, SupplierProposal | — |
| Billing, payments and checkout | Banque, Facture, MultiCurrency, PaymentByBankTransfer, Paypal, Prelevement, ReceiptPrinter, Stripe, TakePos | — |
| Accounting, assets and other financial records | Accounting, Asset, Comptabilite, Don, Loan, Salaries, Tax | Intracommreport (development) |
| Manufacturing | Bom, Mrp, Workstation | — |
| Projects, agenda and events | Agenda, EventOrganization, Projet, Resource | BookCal (experimental) |
| People and association membership | Adherent, ExpenseReport, HRM, Holiday, Recruitment | — |
| Contracts, field service and support | Contrat, Ficheinter, KnowledgeManagement, Ticket | — |
| Communication, websites and portals | EmailCollector, Mailing, Notification, OpenSurvey, SocialNetworks, WebPortal, Website | — |
| Automation, identity and external interfaces | Ai, Api, ClickToDial, Dav, GeoIPMaxmind, Gravatar, Ldap, Oauth, Printing, Webhook, Workflow | FTP (deprecated), MailmanSpip (deprecated), WebServices (deprecated), Zapier (experimental) |

## How to interpret the inventory

* **Eligibility.** The stable filter includes modules marked as stable and modules with an accepted numeric version marker, including the audit log. The other eleven descriptors appear in the inventory solely to record their exclusion. Stability is checked again for individual features. A stable module can contain flags, unfinished screens and optional integrations with different support levels. Built-in shipment PDFs, for example, are a separate question from the maturity of the standalone DocumentGeneration descriptor.
* **Visibility.** The setup catalogue includes readable, available module definitions and skips repeated definition names. For inactive modules the feature level must be at least 2 for development, at least 1 for experimental, or negative for deprecated. Previously enabled modules pass this particular feature-level test. A truthy descriptor `hidden` property still removes the module from the list. A nonzero `MODULE_CRON_DISABLED`, for example, hides the scheduled-jobs descriptor.
* **Purchasing.** With the supplier split option off, the combined Fournisseur descriptor supplies the purchasing module and configuration exposes both order and invoice capabilities. With `MAIN_USE_NEW_SUPPLIERMOD` enabled, the combined descriptor class is absent and the separate SupplierOrder and SupplierInvoice descriptors become visible. Count the business flows once. Dependencies can branch on the option, including those for supplier quotations, batch tracking and bank transfers. Reception's descriptor still names Fournisseur directly, so exercising receipts with the split option warrants its own integration test.
* **Activation.** The setup action requires an administrator. Activation checks minimum runtime and application versions and any JavaScript requirement, skips an already enabled module by default, then initialises the requested module. It recursively activates the declared dependencies and disables declared conflicts. A country-specific dependency is skipped only when a country is present and fails the prefix comparison. This explains the inventory's `country_FR_or_unset` entry for TakePos. Errors from a dependent module are accumulated after the parent initialisation; reconcile the resulting state before retrying.
* **Deactivation.** Setup requires confirmation. A successful ordinary removal follows the descriptor's explicit `requiredby` list, which is maintained separately from the forward dependencies in the inventory. Conflict removal suppresses that recursive cascade. The two accounting modes declare a mutual conflict. Users and groups is permanently enabled in the normal setup interface. For BlockedLog, the protected status depends jointly on prior activation, prior use and the configured country list.

## Scope of the inventory

The catalogue counts one row per bundled module definition. Document layouts, numbering rules, grouped financial exports and optional integrations have their own registers because a single enabled module may provide several of each. An externally installed module can add further records or operations.

## Acceptance cases for configuration

| Setup | Operator action | Observable outcome |
| --- | --- | --- |
| Ordinary level, clean installation, supplier split off | Browse the stable catalogue | The combined supplier module can appear. The two split descriptors are hidden. Inactive experimental, development and deprecated descriptors are absent. |
| Products, orders and shipments disabled | Enable shipments with dependency resolution under valid setup conditions | Shipment activation requests customer orders, which request third parties. Products is outside this descriptor dependency chain. |
| Simplified accounting enabled, prerequisites available | Activate double-entry accounting | The activation path requests invoices, bank and tax, then disables the conflicting simplified mode. |
| Experimental module already enabled, feature level returned to zero | Browse all maturity levels, then filter explicitly to stable | The feature-level gate alone retains the enabled module. The explicit stable filter excludes it. |
| An existing module dependency fails after parent initialisation | Inspect the activation result and entity settings | The result reports dependency errors. Check the parent and each prerequisite independently before retrying. |
