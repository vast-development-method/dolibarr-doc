# Catalogue activity by month

The catalogue statistics screen builds a monthly series for each enabled document family. It can show the number of units, the number of documents or the net value of the qualifying catalogue lines. One of those measures can grow while another stays constant. An order with two lines of the same item for 3 and 8 units contributes 11 units, one order, and the sum of both net line amounts. The document count uses distinct header IDs within a month. Adding the counts from separate item reports can double-count a document containing both items.

## Months and source populations

| Series | Month | Input rows |
| --- | --- | --- |
| Customer offers | Proposal date | Offer lines linked to the offer. No accepted-only condition. |
| Supplier quote requests | Validation date | Supplier request lines. Requests without a validation date have no calendar month. |
| Sales orders | Order date | Customer order detail. Quantities are quantities ordered, including orders still awaiting fulfilment. |
| Purchase orders | Order date | Supplier order detail. Receiving some of the order leaves the ordered quantity intact. |
| Customer invoices | Invoice date | Customer invoice detail. All header states and types can qualify. The unit measure directly sums stored quantities, including those on credit notes. |
| Supplier invoices | Invoice date | Supplier invoice detail. The same straight sum applies to the stored vendor quantities. |
| Contracts | Contract date | Contract detail. It groups by the date of the contract even when service activation or termination is later. |
| Manufacturing | Order validation date | Manufacturing order headers in a positive state. Units sum the planned header quantity for the named output item. Document mode counts these orders. The screen omits monetary mode for this series. |

The year selector normally yields a January–December sequence, with zero for empty months. Each commercial series can narrow to one party in the document header's entity scope. An account linked to a party uses that party. The series applies the user's representative assignment where unrestricted customer visibility is absent. The current catalogue product/service type narrows the selection when requested. The category selector uses the item IDs assigned to the category, and the unassigned choice tests for no category memberships. With no specific item selected these queries still require a positive catalogue-item ID, which excludes free-text lines.

## Credit notes and dispatch

Suppose May contains a customer invoice for five units at 20 net each and a credit note for one unit stored with a positive quantity and line net of −20. The customer pays neither document during May. There is a shipment created in May for four units at the same price. The sale and credit are both validated.

| May output | Units or count | Net value |
| --- | ---: | ---: |
| Customer invoice chart, units | 6 | — |
| Customer invoice chart, document count | 2 | — |
| Customer invoice chart, amount | — | 80 |
| Item's customer invoice line history | 4 signed units | 80 |
| Item's outbound shipment history | 4 shipped units | 80 |

The equality of the two fours in this example follows from the chosen data. A fifth unit on the dispatch changes only the shipment history. A later payment changes collections and leaves all five rows above unchanged. A dated draft for two additional catalogue units at net 40 changes the monthly invoice chart to eight units, three documents and 120 net. A financial turnover report limited to validated or closed invoices still reports 80 net. [Item document history](item-document-history.md) · [Turnover and collections](../reporting/commercial-statistics-and-turnover.md)

## The references table above the item history

The item history has a separate all-date summary with columns for distinct parties, referring documents and total quantity. The customer order, invoice and shipment summaries count distinct headers and distinct customers, then sum their matching line quantities. On the customer invoice summary a credit note **does** reverse quantity. The summary in the example above shows one customer if both documents belong to the same party, two invoice references and four units. It remains an all-date total when an operator changes the dates on the item detail below.

Two further rules affect reconciliation.

- For incoming receipts the summary follows each receipt allocation to its source purchase order. Its distinct document count is the number of **purchase orders** represented. Ten units received in two receipt documents on one purchase order can produce one referring document, ten units and two receipt lines in the detailed history.
- When configured to include parents for stock-affecting kit/component relationships, the customer order, invoice and shipment summaries add their parent items' results. Parent quantity is multiplied by the child's quantity per parent, while party and document counts are added from the parent subtotals. A document listing both the component and its parent can enter those counts twice. The item line drill-down still selects lines directly referencing the component.

Evidence is in `htdocs/product/stats/index.php:50–85,319–365,393–505,542–568`, `htdocs/product/class/product.class.php:3790–3843,4004–4062,4089–4123,4341–4393,4592–4659,4673–5090` and `htdocs/core/lib/product.lib.php:527–548,585–669,703–741`.
