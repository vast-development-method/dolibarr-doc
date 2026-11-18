# Document models and recipient copies

The same order can produce a commercial confirmation, a pro forma or an editable document. The source record owns the ordered quantity, price and state. The model determines what the recipient can see, which addresses and external files to include, and which currency figures to print.

## Model register

The [model register](model-register.csv) lists **67 document writers** across **35 record and report families**. Of these, 45 produce PDF output and 22 provide editable office output. Each entry identifies its output family, model key, availability and purpose. An operator can generate a particular model only under the applicable configuration and record conditions.

| Disposition in the register | Files | What the reader can infer |
| --- | ---: | --- |
| Bundled | 54 | Supplied writer in a business module. Generating an output can still require module activation, company configuration, source records and, for office models, an actual template file. |
| Earlier layout | 5 | Azur for offers, Einstein for orders, Rouget for shipments, Muscadet for purchase orders and Aurore for supplier requests have newer counterparts. Some remain selected by an existing record, an initialization setting or an unconfigured fallback. |
| Special-purpose output | 4 | Monthly event report, cheque deposit slip and two label-sheet writers. A label writer receives a collection of records and a sheet definition. It handles many stickers per page. The event writer produces a report for a month. |
| Delivery acknowledgment feature | 2 | Storm and Typhon belong to delivery receipts. A shipment can produce its own shipping note even when the additional delivery-receipt feature is disabled. |
| Conditional progress layout | 1 | Octopus declares itself unavailable by default and changes its availability when progress invoicing is configured in mode 2. |
| Development | 1 | The Ban banking writer identifies itself as unfinished. The SEPA mandate PDF has a separate implementation. |

The register covers selectable business-document writers. Barcode encoders, scaffolding for custom modules, stand-alone payment reports, HTML print pages and website templates have separate roles.

## Which model does the user get?

| Business document | Configuration and fallback |
| --- | --- |
| Customer proposal | The module sets Cyan. Explicit model wins. When absent, the proposal's saved model wins over the company setting, whose default is Cyan. |
| Customer order | The module initializes Eratosthene. The business method considers a saved model and then the company setting. With neither available it falls back to Einstein. Proforma inherits the Eratosthene order layout and supplies the pro forma heading. |
| Supplier quotation request | The module initializes Aurore while Zenith is the current layout. A saved or configured model can select Zenith. When the requested, saved and configured names are all empty, the operation returns success without writing a document. |
| Purchase order | The combined supplier module and the separate purchase-order descriptor initialize Cornas. The purchase-order method accepts an empty final selection and in that case finishes without creating a file. |
| Customer shipment | The installed setting specifies Espadon. A saved model wins over the company setting. If both are empty, the shipment method falls back to Rouget. Merou supplies an A5 alternative. |
| Customer invoice | A saved choice and invoice-type-specific company settings can distinguish credit notes, deposits and stage bills. Sponge supplies the general invoice form. The progressive-mode setting controls whether Octopus is available as a specialized layout. |

Conceptually an issued invoice, the copy given to its customer, and a later reprint are three different observations. Model availability can change when settings change. A later reprint can also use different translated labels or pictures even if the invoice's ledger effect has already been recognized.

## Read by task

- [Commercial documents and language selection](commercial-copies.md)
- [Shipping, transfer and progress certificate layouts](physical-and-stage-documents.md)
- [Editable templates, party contacts and installed fields](office-templates.md)
- [Project reporting and manufacturing work sheets](project-and-manufacturing-sheets.md)
- [Generation, indexing and mail delivery](../specification/output/document-models-and-delivery.md)
