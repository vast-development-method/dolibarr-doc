# Document models and recipient copies

The same order can produce a commercial confirmation, a pro forma or an editable document. The source record owns the ordered quantity, price and state. The model determines what the recipient can see, which addresses and external files to include, and which currency figures to print.

## Model register

The [model register](model-register.csv) identifies all **67** PDF and generic office writer files in the bundled core and recruitment module document directories of release 24.0.3. They span **35 record and report families**. There are 45 files named as PDF writers and 22 as office writers. Those counts include the dispositions below. Each row supplies a business purpose and an exact release-relative path. A writer's presence on disk, the company's configured default, and the saved choice on a particular record are separate facts.

| Disposition in the register | Files | What the reader can infer |
| --- | ---: | --- |
| Bundled | 54 | Supplied writer in a business module. Generating an output can still require module activation, company configuration, source records and, for office models, an actual template file. |
| Earlier layout identified by the release | 5 | Azur for offers, Einstein for orders, Rouget for shipments, Muscadet for purchase orders and Aurore for supplier requests have newer counterparts. Some remain selected by an existing record, an initialization setting or an unconfigured fallback. |
| Special-purpose output | 4 | Monthly event report, cheque deposit slip and two label-sheet writers. A label writer receives a collection of records and a sheet definition. It handles many stickers per page. The event writer produces a report for a month. |
| Delivery acknowledgment feature | 2 | Storm and Typhon belong to delivery receipts. A shipment can produce its own shipping note even when the additional delivery-receipt feature is disabled. |
| Conditional progress layout | 1 | Octopus declares itself unavailable by default and changes its release status when progress invoicing is configured in mode 2. |
| Development | 1 | The Ban banking writer identifies itself as unfinished. The SEPA mandate PDF has a separate implementation. |

The discovery boundary is the document subdirectory and the `pdf_` or `doc_generic_` filename convention. The two barcode symbology drivers in a document directory feed other outputs. The two generic module-builder writers belong to the development scaffold. The separate payment-report classes `htdocs/core/modules/rapport/pdf_paiement.class.php` and `htdocs/core/modules/rapport/pdf_paiement_fourn.class.php` produce customer and supplier payment reports outside this selectable-writer inventory. HTML print pages, third-party model packages, and website templates have their own entry points.

## Which model does the user get?

| Business document | Configuration and fallback |
| --- | --- |
| Customer proposal | The module sets Cyan. Explicit model wins. When absent, the proposal's saved model wins over the company setting, whose default is Cyan. |
| Customer order | The module initializes Eratosthene. The business method considers a saved model and then the company setting. With neither available it falls back to Einstein. Proforma inherits the Eratosthene order layout and supplies the pro forma heading. |
| Supplier quotation request | The module initializes Aurore even though the release describes Zenith as the current implementation. A saved or configured model can select Zenith. When the requested, saved and configured names are all empty, the operation returns success without writing a document. |
| Purchase order | The combined supplier module and the separate purchase-order descriptor initialize Cornas. The purchase-order method accepts an empty final selection and in that case finishes without creating a file. |
| Customer shipment | The installed setting specifies Espadon. A saved model wins over the company setting. If both are empty, the shipment method falls back to Rouget. Merou supplies an A5 alternative. |
| Customer invoice | A saved choice and invoice-type-specific company settings can distinguish credit notes, deposits and stage bills. Sponge supplies the general invoice form. The progressive-mode setting controls whether Octopus is available as a specialized layout. |

Conceptually an issued invoice, the copy given to its customer, and a later reprint are three different observations. Model availability can change when settings change. A later reprint can also use different translated labels or pictures even if the invoice's ledger effect has already been recognized.

See `htdocs/core/modules/modCommande.class.php:80–90`, `htdocs/core/modules/modPropale.class.php:80–90`, `htdocs/core/modules/modExpedition.class.php:85–124`, `htdocs/core/modules/modSupplierProposal.class.php:80–90`, `htdocs/core/modules/modFournisseur.class.php:90–101` and `htdocs/core/modules/modSupplierOrder.class.php:83–95`. Resolution uses `htdocs/comm/propal/class/propal.class.php:4091–4104`, `htdocs/commande/class/commande.class.php:4267–4288`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:2836–2860`, `htdocs/fourn/class/fournisseur.commande.class.php:3609–3632`, `htdocs/expedition/class/expedition.class.php:3333–3352` and `htdocs/compta/facture/class/facture.class.php:5814–5835`. Model maturity details appear in `htdocs/core/modules/facture/doc/pdf_octopus.modules.php:166–189`, `htdocs/core/modules/bank/doc/pdf_ban.modules.php`, and the release descriptions in `htdocs/langs/en_US/orders.lang:164–167`, `htdocs/langs/en_US/propal.lang:103–104`, `htdocs/langs/en_US/supplier_proposal.lang:44–45` and `htdocs/langs/en_US/admin.lang:2048–2049`.

## Read by task

- [Commercial documents and language selection](commercial-copies.md)
- [Shipping, transfer and progress certificate layouts](physical-and-stage-documents.md)
- [Editable templates, party contacts and installed fields](office-templates.md)
- [Generation, indexing and mail delivery](../specification/output/document-models-and-delivery.md)
