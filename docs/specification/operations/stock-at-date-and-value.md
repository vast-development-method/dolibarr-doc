# Stock at a date, projected stock and value

A request for last month's stock can mean quantity physically held, the value assigned to it at the time, or today's estimate of what that quantity would be worth. The date report reconstructs the quantity and then applies current price information. Its future-date mode instead calculates a projection of the product's open demand and supply.

## Physical quantity at a past cutoff

The report starts with current warehouse balances within the selected scope. It sums the signed movements for the same product and warehouse scope beginning at the selected date's end-of-day cutoff, then subtracts that net from current stock. Inputs after the cutoff are subtracted. Outputs after the cutoff have negative signs, so subtracting them adds their quantity back. The query uses an inclusive lower bound at 23:59:59. A movement timestamped at that exact second belongs to the set subtracted.

For example, warehouse A now holds 31 units. Since the cutoff it received 14 and issued nine, a net gain of five. Its reconstructed quantity is `31 − (14 − 9) = 26`. If four of those nine units were internal transfers to B, a consolidated report that includes both warehouses cancels those four out across the paired movement rows. Moving stock into or out of the selected set changes the reconstructed quantity for that set. The displayed movement count is the count of journal rows considered, regardless of whether their signed quantities cancel out.

The date is required for the report calculation. Past mode rejects a future date, and future mode rejects a past date. The report can restrict product, warehouse, product text and, when extra warehouse statuses are enabled, warehouse status. The product and warehouse joins apply entity scope. Physical services participate when service-stock support is enabled. The report reads the product and stock areas, with a separate supplier-price disclosure rule for estimated buying value under advanced permissions.

The backward calculation depends on the **current balance** and subsequent journal records. A separate movement-history operation computes a strict sum of the product's journal rows before a timestamp. It has no warehouse argument. Those methods can disagree in the presence of opening balances absent from the journal, different warehouse filters, or a boundary movement at the exact cutoff. The date report's quantity has the warehouse filters and temporal boundary described above.

## Valuing the quantity

The buying-value column multiplies the reconstructed quantity by the **current product weighted average cost**. When a single product selling price applies, the selling-value column uses today's product selling price. Customer-specific or multiple selling-price modes show a variable price in this view. The report does not replay historic prices, foreign exchange or cost layers to value the past quantity.

At month end there were 26 units. A later receipt changed average cost from 10 to 12.50. A report run now estimates that earlier quantity at 325. Valuing the same units at the earlier cost would give 260. The difference is attributable to the price date, independent of the 26-unit reconstruction. A new selling price likewise changes the estimate without creating an inventory movement.

For an incoming stock movement at a qualifying price, the product average uses physical stock across warehouses. With `q` as the nonnegative existing stock, `a` its previous average, `n` the receipt quantity and `p` its price, the ordinary new average is `(q × a + n × p) ÷ (q + n)`. A negative existing stock level contributes zero historical units. If the prior average is unset or nonpositive, or the denominator is zero, the incoming price is used instead. An ordinary zero-price receipt leaves the old average in place. The configured exception for zero-priced supplier-order or supplier-invoice origins can include those free units in the average. An outgoing movement leaves the average unchanged.

For 20 units at 8 followed by 10 at 14, the new average is 10. A subsequent issue of 12 leaves 18 units at that average. Because the receipt uses the existing **product** balance, splitting the original 20 between two warehouses does not change this calculation. Independent cost adjustments made during a count can also affect the product price subsequently used by the date report.

## Projecting supply and demand

Future mode displays current stock, projected stock at the requested date and the projection with no date limit. The projection begins with physical stock and open manufacturing's planned outstanding output minus planned outstanding consumption. Then it applies the commercial commitments appropriate to the installation's stock-posting points. In shipment-based stock mode, for example, a confirmed customer order reduces the projection by what remains after eligible shipments. In receipt-based stock mode, an eligible supplier order adds its order quantity less goods already received.

The requested horizon does not apply identically to all sources. Supplier-order statistics compare promised delivery against the cutoff. Receipt statistics can filter on allocation creation time. Open production uses its validation date for this horizon. The product-wide customer-order and shipping statistics called by the product projection do not receive a cutoff argument on this path. The values are therefore planning indicators with source-specific time semantics. The report requests the whole product projection for open and internal warehouses even when the current-balance column is limited to a selected warehouse set.

Suppose physical stock is 40, there are six outstanding manufacturing outputs, three outstanding production inputs, twelve customer units still unshipped and twenty eligible purchase units still unreceived. With stock moving on shipment and receipt, projected stock is `40 + 6 − 3 − 12 + 20 = 51`. A later customer order or supplier promise can change the result before any warehouse balance changes. Calculating buying demand from that already projected 51 must avoid deducting those commitments a second time.
