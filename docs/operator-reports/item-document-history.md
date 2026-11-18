# One item's commercial history

Start with the catalogue record and open the history for a particular document family. Each table answers which lines actually reference that catalogue ID. A line entered only as free text is absent even if its description matches the item name. Two lines for the same product on one document can give two rows with the same public document reference. Their line IDs preserve that distinction.

## Population and date by tab

| Tab | Source row and date selector | Quantity and net value |
| --- | --- | --- |
| Customer offers | One proposal detail joined to its party and proposal. Month and year independently filter proposal date. The base selection has no accepted-only condition. | Stored proposed quantity and line net, including each separate occurrence on a proposal. |
| Customer orders | One customer order line. Optional month/year use order date. A supplied status list filters the order state, including a selection of several states. Promised delivery is separately available. | Stored ordered quantity and line net. A later shipment or invoice does not rewrite the historical measure. |
| Customer invoices | One customer invoice line. Optional independent start and end boundaries use invoice date, beginning and end of day at server time. The base item query has no validated-only or standard-type filter. Header extra fields and extension selections can contribute additional criteria. | Stored line net. The presentation negates the line quantity for a credit note before calculating the page total. It uses the stored line amount as signed and does not apply a second monetary sign change. |
| Recurring customer invoice models | A recurring template line, joined to its own header and party. The selected month/year refer to the template creation date. Suspended status can appear on the result. | Quantity and line net from the template. The detail query supplies type zero on every row, so its credit-note sign branch is never selected. Quantities appear as stored. One template does not show how many times generation succeeded. |
| Outbound shipments | One shipment detail whose origin type identifies a customer order, joined to its original order line. Month/year use shipment creation date. Expected delivery date and shipment status can be shown. | Shipped quantity times source order unit net price times one minus the percentage discount. The display normalises the derived net per row. Other invoice or catalogue price changes are outside this calculation. |
| Supplier quote requests | One supplier request detail. The result displays validation date. Its selectors for month/year refer to a different field as described below. | Requested quantity and stored line net, irrespective of whether the request was converted to an order. |
| Supplier orders | One purchase order line. Optional month/year use order date and an optional status set narrows the result. Delivery date and stored line unit price are separate fields. | Ordered quantity and line net. |
| Supplier invoices | One vendor invoice detail. Optional month/year use invoice date. The selection also reads header amounts but the amount added to the item footer is the line net. | Quantity and net exactly as stored on each selected supplier line. The customer-credit display adjustment is absent on this screen. |
| Incoming receipts | One receipt allocation with supplier-order origin, joined to its receipt and source purchase order line. The product ID is read on the allocation. Month/year use receipt creation date. | Allocated quantity times the discounted purchase unit price on the linked order line. The amount is normalised per allocation before summing the displayed page. |

A shipment detail is a physical allocation associated with an order line. The outgoing history does not join the deeper per-lot split table. Splitting one shipment detail among two lots need not produce two item-history rows. In the incoming history the query starts at the receipt allocation/batch relation and selects its individual row ID. A receipt split there can yield two rows for one supplier document. Neither history subtracts a cancelled document merely because a stock journal later contains a compensating movement. A document-history view, the warehouse journal and the financial ledger each retain different evidence.

**Supplier-request date exception.** The supplier tab's base selection reads and sorts by validation date. Its month and year filters refer to the proposal-date column on the supplier request header. The shipped installation table defines creation, validation, closure and delivery dates but does not declare that proposal-date column. Against that schema, applying either of those two filters makes the query refer to an unavailable column. The unfiltered list and a date-filtered list therefore differ in more than the chosen range. The month and year filters on the ordinary customer proposal tab use a defined column.

## Visibility and what the total counts

Opening the product area uses the product/service access rule, then each detail table tests the document-family read capability. The supplier-request tab specifically tests the proposal read capability. Customer and supplier order/invoice tables restrict an external account to its linked party. Their item queries add the current user's party-representative assignment when unrestricted customer visibility is absent. The shipment and receipt queries apply the internal representative restriction when the actor lacks unrestricted visibility and no linked-party scope was already supplied. The entity scope follows the header family, so shared products and shared invoices can have different eligible populations.

The tables with the line footer sum quantities and net values while rendering the rows on the current page. The extra row fetched to detect another page is excluded. Totalling a page of 25 items on a search matching 32 items consequently leaves seven matching lines outside that footer. On the sales invoice tab the row carries a payment/state display for its invoice as well. That display does not allocate the invoice's payment to this particular product line.

## Reconciling an order, shipment and credit

Suppose a customer orders ten units at 24.00 with a 10% line discount on 30 April. A shipment created on 2 May allocates six units. A May invoice bills five at the same terms, and a May credit note has a stored positive quantity of one and net of −21.60. There are no other matching documents, amounts are in company currency and all rows fit on one page.

| Selection | Quantity | Net |
| --- | ---: | ---: |
| April order history | 10 | 216.00 |
| May shipment history | 6 | 129.60 |
| May invoice history, both lines | 4 | 86.40 |

The net of 86.40 comprises five units billed for 108.00 and one credited for 21.60. The May dispatch still records six units. An actual goods return requires its own inventory evidence. The four-unit difference between order and shipment is a fulfilment question, while the difference between shipment and invoice history also depends on credits and billing timing.

Evidence is in `htdocs/product/stats/propal.php:143–199,247–299`, `htdocs/product/stats/commande.php:79–94,157–209,271–320`, `htdocs/product/stats/facture.php:107–126,302–381,482–559`, `htdocs/product/stats/facturerec.php:167–204,271–309`, `htdocs/product/stats/expedition.php:151–190,243–292`, `htdocs/product/stats/supplier_proposal.php:150–180,247–287`, `htdocs/install/mysql/tables/llx_supplier_proposal.sql:21–58`, `htdocs/product/stats/commande_fournisseur.php:80–94,157–205,272–321`, `htdocs/product/stats/facture_fournisseur.php:152–194,253–298` and `htdocs/product/stats/reception.php:150–189,246–291`. [Commercial statistics and turnover](../reporting/commercial-statistics-and-turnover.md)
