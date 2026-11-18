# Shipping, transfer and progress certificate layouts

## Dispatching a partial order

Espadon, the installed shipment default, joins three sources on one page. The shipment identifies the dispatch and its physical measurements. The originating order identifies the commercial reference, customer reference and order date. The shipment lines carry the ordered quantity, actual quantity sent and allocation details. A customer's address on the order and its designated delivery contact are independent data.

When the source object has been loaded and has a positive ID, the role-based contact lookup reads the **origin** contacts. Otherwise it uses the shipment. It selects the first external contact in the shipping role. If a valid order exists without a shipping contact, the helper returns the contacts found on that order, even when the shipment itself has a contact. It does not make a second search on the shipment in that case. An origin that cannot supply a shipping contact yields the normal party-address path. The internal follow-up representative uses the same origin-selection rule with an internal role.

| Output | How the current shipment writer obtains it |
| --- | --- |
| Ordered and shipped quantities | Uses separate prepared fields. Independent visibility settings can remove either column. For inventory goods, shipped quantity drives the physical line calculation. |
| Ordered unit | Visible when product units are enabled. It is the line's unit. A quantity expressed in cartons still needs a separate catalog weight expressed for that line's unit. |
| Item image | The shipment illustration option and at least one available picture enable the column. Without an illustration for a specific row that row has no product image. |
| Weight and volume | For ordinary goods with a unit measure, multiplies by shipped units. Uses separate weight and volume rounding settings with a five-place fallback. The volume option can suppress line and summary volume. |
| Actual package measures | Starts with calculated quantity and measure totals. A nonzero measured weight replaces calculated weight in the summary. Three nonzero dimensions produce measured volume; the summary can then display that instead of the item-volume total. |
| Value | The optional price setting exposes both unit price and line net amount. These use the prepared line fields. The summary prints the shipment's own net total. |
| Additional line data | Enabled custom line columns get the value from the line itself. Title or subtotal rows are excluded from the ordinary merchandise quantity, price and dimensional branches. |

Suppose the order is for eight pieces, each 1.25 kg. The first shipment sends three. The line displays 8 ordered, 3 shipped and 3.75 kg. If the entered packed weight is 4.20 kg, the measured summary displays 4.20 kg. Posting another sale or changing the inventory quantity to account for the 0.45 kg difference would be incorrect. Hiding the ordered column changes neither the shipped quantity nor how many remain against the order. A dispatch split over warehouses can have different line and header value behaviour, described in [Shipment and reception notes](../specification/output/shipment-and-reception-notes.md).

## Internal transfer and declared value

The ordinary transfer sheet prints the transferred quantity and the individual source and destination warehouse for each line. Their references and recorded places are resolved through the line's warehouse identifiers and can be cached across lines. A shipment to a customer has a recipient. An internal transfer has two participating stock locations. Two lines on one transfer can therefore have different source or destination warehouses.

The transfer pro forma reads the weighted-average price carried on each transfer line. The default unit-price cell takes that line value. Its net line amount multiplies it by the line quantity. The document total independently calls the transfer valuation operation, which sums the stored line average prices times their quantities, fetching the lines if necessary. The term “pro forma” on this model identifies a goods valuation. An order pro forma instead renders the customer order's commercial amounts.

Suppose goods move from the main warehouse to the branch. Two units of item A carry an average price of 30. Four units of B carry 7.50. The pro forma contains row values of 60 and 30, total 90. Later catalog list prices of 45 and 10 would give a retail value of 130, which is outside the transfer's stated calculation. Printing the 90 does not book a 90 receivable. Warehouse balances and actual posted movement values remain available from the stock transaction.

## Reading a progressive certificate

The Octopus model becomes eligible in progressive billing mode 2. The intended subject is a situation invoice and its associated credits. The writer's initial guard is narrower than that description. It warns and returns success for a missing record, or for a non-situation, non-credit document with a nonempty cycle reference. This condition alone does not reject an ordinary invoice with no cycle reference. A selected model, a successful return and a suitably typed certificate should therefore be treated as separate observations.

In the default column definition, current progress percentage and current amount have their own places. A dated previous situation enables a contract-amount column and, for the situation layout, the previous percentage and previous amount. The previous-period header includes certificate number and date. The current header uses the current certificate's number and date. The default unit column stays disabled even if product units are enabled.

For each continuation line, the lookup requires a cycle and a counter greater than one. It compares the current previous-line identifier with each row ID on the selected previous situation. For a match it calculates the **full contract net** from prior quantity, unit price, discount and tax inputs without reducing for progress. It also returns the prior line's actual progress percentage and its stored net amount. The current-column amount reads the current line's stored net separately. Labels or product codes cannot disambiguate continuation where the same product occurs on several lines. If the predecessor cannot be found the helper returns no matched amounts. A new line on a later stage is handled separately in the cycle aggregates for additional work.

For example the contract specifies ten units at 100, no discount. The previous row records progress at 30% and stored net 300. The next linked row has stored net 200. On that next certificate the full-work field is 1,000, the previous-progress amount is 300, and the current-progress amount is 200. Adding all three would count the same contract work repeatedly. A separate additional-work line with no previous-line ID has no matched previous percentage. Replacing the job's line relationships with a product-level running balance would give the two rows the wrong history.

A more subtle case occurs in foreign currency. Three adjacent detail columns use the recomputed ordinary full-contract amount, the previous ordinary net and the current ordinary net; those specific expressions do not use the corresponding foreign-currency fields. Other parts of the document, including line VAT handling, do have a multicurrency branch. A downstream extractor should identify each column's actual calculation when turning a foreign-currency certificate back into structured values. [Invoice print calculations and settlement evidence](../specification/output/invoice-print-calculations.md)
