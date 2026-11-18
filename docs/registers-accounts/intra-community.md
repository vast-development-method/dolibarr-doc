# Intra-community reporting register

This development-stage feature stores reports prepared for cross-border goods or services. Its activation declares dependencies on invoicing, tax management and categories, loads the report table and registers separate read, write and delete grants. The register checks that reporting is enabled and applies the product-area access check for type 0, service-area check for type 1, or combined area check otherwise. The write grant controls the new-report action. The product/service access choice and the declaration family are separate inputs.

## Which saved reports appear

One row is one stored `intracommreport` header. The register reads its report reference, declaration family, period text, processing mode, stored XML, exchange direction, creation time and last modification time. Its base query reads the report table directly. Optional field values and installed list extensions can add joins. The stock query contains no invoice, product or declaration-line join. An accessible-entity filter applies by default and a current-entity option narrows it to the active company.

| Input | Effect on membership |
| --- | --- |
| Global or direct reference search | Global search matches keywords in `ref`. The direct reference criterion also matches that field. Neither searches inside the XML by default. |
| Header ID | `rowid` supports numeric comparisons. |
| Period, mode and content | `periods`, `mode` and `content_xml` have individual text predicates when supplied. Period selection matches stored text, independently of the invoice date window used by XML preparation. |
| Declaration family and exchange direction | The declared options are `deb` or `des` and `in` or `out`. The list forwards these text options to its integer-list comparison, which strips nonnumeric characters and produces a test against 0. String-to-number handling then depends on the database. Selecting DES does not reliably isolate service declarations. |
| Creation and modification | Each of `datec` and `tms` accepts inclusive lower and upper bounds. A day selection starts at midnight or ends at the final second of the chosen day. |
| Product/service context | Changes the access check without adding an invoice-line type predicate to the saved-report query. |

The full count, when enabled, counts the joined result rows before pagination. Ordering defaults to ascending header ID. None of the standard report fields is a financial measure. Suppose the current entity stores two headers with references `GOODS-A` and `SERVICES-B`. Another entity also stores `GOODS-A`. With current-entity scope and a global keyword of `GOODS`, exactly the first local header is selected, assuming ordinary joins. Its count is one whether the saved XML contains one item or fifty.

## Preparing an XML file

The preparation routines select invoices by the requested calendar month, current entity, positive invoice status, counterparty country and line type. Goods dispatched and service declarations select customer invoices. Goods received select supplier invoices. Product and counterparty masters are required. The selection includes a foreign country or a missing country. The goods writer records a missing country as an error. The initial country predicate does not itself verify community membership.

The goods writer can emit a product's customs code, quantity, destination, rounded mass and invoice amount for a qualifying line. The service writer emits a sequence, rounded value and partner VAT identifier. Both ordinary item writers receive the **header's untaxed total** from the line selection. Two ordinary qualifying goods lines on a single invoice totalling 150 therefore supply 150 to each item's amount field. Summing those items yields 300 even if the individual line values were 100 and 50. The saved report count, invoice count and sum of XML item values answer different questions.

The file writer stores the generated XML temporarily and returns it as a download. A saved reference, a stored XML payload and a download provide local evidence of preparation. Authority submission, acceptance, rejection and an external receipt require separate evidence. [Field definitions](../relational-model/README.md) · [Regional reporting](../regional-reporting/README.md)
