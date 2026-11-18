# Commercial statistics and turnover

A sales or purchasing figure is reproducible when its date, population and unit of measure are known. A single transaction may contribute to the quotation statistics in April, order statistics in May, invoiced turnover in June and collections in July. The following definitions distinguish those populations down to the source document and line.

## Monthly activity and average document value

| Series | Month and row counted | Amount and population |
| --- | --- | --- |
| Customer offers | One customer offer, assigned to its proposal date | Sum the header net amounts. The basic population includes drafts dated in the period. Status, customer, author and party classifications can narrow it. |
| Supplier requests for quotation | One supplier request, assigned to its validation date | Sum the header net amounts. A draft without a validation date cannot enter a bounded month even when a status filter includes drafts. A sent request without a priced line can still contribute a count. |
| Customer and supplier orders | One order on its order date | Sum header net amounts. The general population by itself imposes no approved-only or delivered-only condition. Apply the chosen status when comparing confirmed commitments. The customer and supplier modes use their respective party categories. |
| Customer and supplier invoices | One invoice on its invoice date | Sum header net amounts. The statistics population admits nonnegative states, including draft. Customer mode excludes an abandoned original marked as replaced. Standard, replacement, credit and progress invoice types are included. Deposit invoices enter unless that side's deposits are treated solely as payments. |

The monthly mean is the arithmetic average of the selected header net amounts. Two invoices for 20 and 180 therefore produce a count of two, total 200 and mean 100 even if one invoice has twenty items and the other has one. Measures retain the signs of the stored amounts. A credit document can reduce monetary total while adding one to the count.

The commercial statistics screens require the selected domain's read entitlement. An external party context restricts the customer selection. An internal actor lacking unrestricted customer visibility is restricted in the header series to their assigned parties through the sales-representative relationship. An author filter refers to the person who created the document. It is independent of the representative assigned to the customer. Party classification and document classification also differ. On the quotation screen the number series is computed before the selected **document** category is added, while later monetary series can include that category filter. Matching caption and month do not guarantee matching populations in this case.

Product frequency on the customer document statistics groups referenced catalogue lines by product reference. Its measure is occurrence count, ordered from highest count downward, with the remainder accumulated into “Other” beyond the chosen limit. An order with two lines of one item adds two occurrences. One line for 500 units adds one. Free-text lines lack the required product join and disappear from this view while still contributing to header totals. Use the product turnover detail for billed quantities and values.

## Customer turnover, supplier turnover and collections

| Question | Grain, period basis and measure | Detail |
| --- | --- | --- |
| How much did we invoice each customer? | Group customer invoice headers in validated or closed status by party identity. Use invoice date within the selected dates. Sum signed net and gross amounts. Include ordinary, replacement, credit and progress documents, plus deposits when recognized as invoices. | The party links to its customer record. An amount can open the invoice list for that customer. |
| What amount did we collect from each customer? | Group the payment-to-invoice allocations by the invoice's customer. Select by payment date. Sum allocated amounts including tax. A 100 receipt divided between invoices in amounts of 60 and 40 contributes each allocation once. | Open the payment list for the party. The report also has a separate residual category for bank-linked receipts without an invoice allocation. |
| How much did suppliers invoice us? | The supplier-by-party accrual report sums supplier invoice headers in validated or closed status within invoice dates. Its type filter includes only standard invoices and credit notes. | Open the corresponding supplier invoice list. This specific report can differ from the more inclusive supplier invoice statistics even for the same dates. |
| What did we pay a supplier? | Select supplier payments by payment date and sum the amounts allocated to supplier invoices, grouped by the invoice's supplier. | Open the supplier payment list. The payment measure is gross and a partially settled invoice contributes only the allocated portion. |

For example, a customer invoice dated June 28 at net 200 and gross 240 receives 100 on July 3 and 140 on August 2. June accrual turnover is 200 net and 240 gross. Customer collection is 100 in July and 140 in August. Changing the period without switching to payment-date mode yields a different answer. Drill-downs that carry a party or product identifier may need the report's period and status filters reapplied on the destination list.

## Billed products, tax rates and geography

The customer product/service turnover view starts with invoice lines whose type is goods or services, and headers in validated or closed state. It applies the invoice date range and the configured deposit treatment. Each product group reports signed net and gross line totals. It counts units by adding the line quantity for ordinary invoices and subtracting it for credit notes. These are extended amounts after the line's pricing calculations. An item sold twice on one invoice can contribute two different prices. The selected product or service type and category filters narrow the line population. A left join to the catalogue allows lines without a product record to form an unassigned group when the filters permit them. The amount for a named catalogue item opens invoices containing that item.

The country-and-tax-rate report groups invoice lines by the party's country, line product type and line VAT rate. Each month column sums the **net tax base** for invoices dated in that month. The annual amount sums the same net lines. A net 100 line at 20% adds 100 to the rate bucket, even though its VAT component is 20. A change to the customer's current master country can change the report's geographic grouping, since the report joins the party at reporting time. A missing country has no country lookup value.

The customer query applies issued/closed state and invoice-type exclusions. In the supplier branch the corresponding state and type text is appended to a different query variable from the one executed. The executed supplier breakdown keeps the date and entity restrictions, and can include supplier drafts or other types excluded on the customer side. This affects reconciliation between that supplier breakdown and supplier-by-party accrual turnover.
