# From batch estimate to inventory value

A recipe estimates a reference batch. The workshop estimates one output unit of a particular planned order. The stock writer receives the unit price of each physical receipt. These values can legitimately diverge even when all quantities reconcile.

## Which price enters each calculation?

| Calculation | Unit-cost selection and quantity | Precision and destination |
| --- | --- | --- |
| Purchased physical component in the recipe | A stored `product.cost_price` takes precedence even when zero. A null stored cost takes `product.pmp`. If that result is zero, locate a minimum eligible supplier price without a requested line quantity. Use its discounted unit price when there is a percentage discount. With no eligible price use zero. Multiply by recipe line quantity and divide by line efficiency. | Sum the components and services. Round the recipe total at monetary-total precision, divide by the positive reference batch quantity, then round per unit. |
| Manufactured component in the recipe | Recalculate its selected child recipe. Use the child's unit cost times parent line quantity divided by parent line efficiency. An unavailable child stops this calculation. | The child's calculated and rounded unit estimate feeds the parent. Its catalogue average can differ. |
| Service in the recipe | Convert the line unit into hours. A selected enabled workstation contributes line hours times the sum of operator and machine hourly estimates. Otherwise use the fraction of the product's standard service duration times its selected unit cost, or the literal quantity times unit cost when a usable duration is unavailable. | The timed service branch does not divide by line efficiency. It estimates labour and equipment used for this reference batch. |
| Workshop estimate from the order | Read the saved `toconsume` lines, including free entries. For ordinary material use the first nonzero of stored item cost and item average. If both are zero, request a supplier price for the **planned line quantity** and use its unit price. With usable time units apply the station or service-duration rule to the planned quantity. Otherwise use planned quantity times selected cost. | Divide each contribution by the positive header quantity, round at unit-price precision and add. The display can show a lower-precision amount per input. Prior posted quantities do not replace the planned amounts in this calculation. |
| Unit price proposed for a workshop output | For manufacturing, take the first nonzero value from the recalculated order estimate, recipe unit estimate, output item's stored cost and output item's average. For dismantling, this automatic proposal starts empty. | Output price entry is shown on the production screen for a user with recipe read access. Each eligible output split can carry a supplied price. An empty submitted price is read as zero. |
| Planned bulk service posting | For a positive output reaching physical stock, sum each planned input's literal quantity times its selected item cost, average or quantity-eligible supplier price, divided by header quantity (divisor one if nonpositive). | Each contribution and the final sum use unit-price precision. This path has no workstation-hours calculation or recipe-estimate fallback. The same computed unit price can reach several positive output lines. |
| Partial service posting | A positive supplied `pricetoproduce` applies to a positive output. An omitted or nonpositive price contributes zero. | A consumption, returned consumption or negative output uses zero as its supplied unit price on this service path. |

Here `pmp` is the current weighted-average acquisition cost. A zero explicit cost with a nonzero average is particularly important. The recipe checks whether cost is null before it considers the average, while the order estimate looks for a nonzero cost. An item with a stored cost of zero, average of 6 and a selected supplier unit offer of 8 with a 25 percent discount produces a recipe cost of 6 and an order cost of 6 **for different reasons**. Change the average alone to 7. The recipe remains 6 and the workshop now uses 7.

## A fixed setup and a timed operation

One reference batch yields four panels. There is no tax, freight, waste posting or overhead beyond the listed inputs. Quantities and rates use one currency. The station combines an operator estimate of 40 per hour and machine estimate of 20 per hour. Its service item's catalogue cost and average are zero, with no supplier offer.

| Input | Recipe specification | Reference batch cost | Executable plan for 12 panels | Workshop cost for the order |
| --- | --- | ---: | --- | ---: |
| Sheet blanks at 4 | Eight blanks, efficiency 0.8, variable | 8 × 4 ÷ 0.8 = 40 | 8 × (12 ÷ 4) ÷ 0.8 = 30 blanks | 120 |
| Setup liners at 3 | Two liners, efficiency 0.5, frozen | 2 × 3 ÷ 0.5 = 12 | Two liners once for this occurrence | 6 |
| Station operation | 30 minutes, variable, efficiency one | 0.5 × 60 = 30 | 90 minutes | 90 |
| **Total** | **Four reference units** | **82** | **Twelve ordered units** | **216** |

The recipe shows **20.50 per unit**. Its material costing applies the liner efficiency. Plan expansion deliberately takes the literal quantity for a frozen line. The workshop's estimate therefore gives **18 per unit**. On the planned bulk posting path the service has no item price and the station rate is unused, so the default receipt price for this case is **(120 + 6 + 0) ÷ 12 = 10.50**. These are comparable only with their quantities, operation and selected price sources attached.

## Valuing two receipts and a later correction

Start with three finished panels at average cost 12. Post the first five panels at 18 in the workshop. The receipt brings the finished balance to eight with average `(3 × 12 + 5 × 18) ÷ 8 = 15.75`. For the remaining seven use an agreed output price of 21. The second receipt gives fifteen panels at `(8 × 15.75 + 7 × 21) ÷ 15 = 18.20`. The two production receipt movements carry unit prices 18 and 21. The other three units were held before this job. The order contributed twelve units with receipt value 237, and the resulting total inventory value is 273.

Reverse just the seven-unit output while stock is still available. The compensating issue takes seven out and leaves eight at the current average of 18.20. Their current carrying value is 145.60. Immediately before the seven-unit receipt the same eight units had value 126.00. The remaining 19.60 difference follows from moving averages and the zero-price compensation. Removing seven units at the current average differs from undoing a historical price computation. The actuals register can now show five produced while the stock journal retains three movements for this job's outputs.

The stock writer ordinarily preserves `pmp` for issues and for a zero-price manufacturing receipt. For a positively priced incoming movement it uses the prior product-wide quantity and average, with negative prior quantity limited to zero in the weighting. When no positive prior average exists, it adopts the receipt price. Thus a first zero-priced output can increase quantity without supplying a cost. The stock movement alone creates no balanced general-ledger entry in these manufacturing posting steps. For the posting link and row-level quantities see [production posting modes](posting-modes.md).
