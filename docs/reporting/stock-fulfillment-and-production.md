# Inventory, fulfillment and production reporting

## Warehouse value and stock at a date

The warehouse list gives one row per warehouse. It aggregates physical quantities across that warehouse's product-stock records. Estimated acquisition value is the sum of physical quantity multiplied by the product's weighted-average unit cost. Where shared products have per-entity costs, the warehouse list uses the relevant entity's cost when present and the common product cost as fallback. Selling value uses current catalogue unit price times physical quantity. It therefore cannot predict receipts for the stock under individually negotiated customer prices.

The dedicated warehouse valuation page uses the weighted-average cost recorded on the **warehouse's product-stock record** for estimated value. Its selling value still uses catalogue price. A warehouse holding ten units at local weighted cost 8, a common product cost of 9 and catalogue selling price of 15 can report acquisition value of 80 on the dedicated valuation and 90 on the ordinary warehouse list with global pricing. Its selling value is 150 in both places. A user reconciling current value needs to know which cost basis was used.

The past-date report starts with current physical stock, grouped by product and warehouse within the chosen scope. For each product it subtracts the signed stock movements dated at or after the chosen day's 23:59:59 cutoff. Receipts are positive and issues negative. With current stock of ten and later receipts of four and issues of one, the historical quantity shown is seven. A movement recorded exactly at 23:59:59 is included among the movements reversed. Filtering warehouses limits both current quantity and the movements being reversed. Transfers between two selected warehouses offset across the combined result, while a single warehouse retains its side of the transfer.

Historical estimated value multiplies the reconstructed quantity by the product's current weighted-average unit cost. The selling value uses the current product selling price. These are reconstructed quantities valued at current master values. They cannot recover a historical unit valuation that has since changed. Supplier-price visibility controls viewing estimated acquisition value. The report requires product or service read access and stock access. A product's movement count links to the stock movement list for investigation.

Future stock uses a different calculation. It requests the product's theoretical quantity for open internal warehouses at the cutoff, and separately displays an unrestricted-horizon theoretical quantity. The future view operates across warehouses. A purchaser investigating a predicted shortage therefore needs the open supply and demand documents, while a discrepancy in a past physical balance leads to movement history.

## Shipment and receipt volumes

The shipment and receipt monthly series count **validated document headers** by validation date. The positive-status filter includes subsequent positive states. A shipment of thirty units in three lots counts once. Two receipts against one purchase order count twice. The filters include party and creation user when specified. The shipment measure uses the active entity, whereas the receipt measure uses the receipt entity scope. Sales representative visibility can further restrict parties.

The amount field in these statistics definitions is document weight. The calculation uses the raw header weight and does not normalize the weight-unit field. Summing headers stored using different units will therefore give a physically ambiguous number. The monthly volume count remains meaningful across such documents. For an item quantity use the individual shipment or receipt lines with their units. For inspection-adjusted receipt completion use the approved split quantities for the purchase order.

## Planned and actual manufacturing quantities

The product manufacturing history selects production rows for **one catalogue product** and groups them by manufacturing order, including the order reference, validation date and state. Four quantities are computed independently by summing the stock quantity on each matching role.

| Column | Rows contributing to the sum |
| --- | --- |
| To consume | Planned input records for the selected product. |
| Already consumed | Actual consumption records for that product. |
| To produce | Planned output records for that product. |
| Already produced | Actual output records for that product. |

A component planned at twelve and consumed in postings of five and four shows twelve planned and nine consumed. A further production record for seven finished units belongs to the finished product's own view. Combining the component and finished goods as a single measure would mix different units and purposes. The product history restricts orders by allowed manufacturing entities. Year and month filters apply to **order validation date**, so later production postings can appear under an earlier month's order. The query carries the order status without imposing a completed-order-only condition. The row links to the order's production record for the underlying postings.

The lot manufacturing view sums only actual consumed and produced quantities by order. It selects by the batch text in the production row and uses the same order validation date for month and year. The query has no product-identity predicate beside the batch text. Reuse of a lot designation across different products can thus bring multiple products into the same lot-history result. Inspect the order's production lines for the actual product and warehouse before attributing that result to one item.
