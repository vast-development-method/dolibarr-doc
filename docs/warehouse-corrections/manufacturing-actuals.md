# Correct a production actual after manufacturing has begun

A production plan says what the workshop intends to consume and produce. Each posting split is an actual, associated with its plan line, and may have a stock movement. For stock-managed goods the original movement identifies the product, warehouse, lot and signed quantity that changed. Correcting one actual and canceling the entire job select different populations.

## Single movement and plan-line paths

The production page's delete action carries the production line and, for an actual with a stock movement, the movement identifier. The common action passes these to the manufacturing order's delete-line operation. The production page distinguishes delete authority from ordinary editing, with an additional draft-only grant for a writer. In the class operation, the requested line must belong to the specified order and the order state must permit deletion. An existing produced child prevents deletion of its parent planned output.

| Input to the correction | Source of quantity and destination | Evidence after success |
| --- | --- | --- |
| An actual with its linked movement identifier | Resolve a manufacturing line for that movement on the same order. Load the original movement. Negate its **signed movement quantity**. A positive correction receives the goods, and a negative correction issues the absolute amount. Use the movement's product, warehouse and lot. | New stock row with the manufacturing origin, current time and zero unit price. The matching manufacturing actual row is deleted. The original stock movement remains in the journal. |
| A planned input with linked consumed children, movement identifier omitted | The method walks the linked consumption details. Positive recorded consumption restores that quantity at its recorded warehouse/lot. Negative consumption issues the absolute quantity. | The method deletes the processed consumption details and requests removal of the parent. Its implementation requests the parent deletion from within the child loop. Several linked children should therefore not be assumed equivalent to a series of independently confirmed single-actual corrections. |
| A line with no linked consumed or produced children and no movement argument | The generic line-delete branch receives only the line identifier. | Removal of the line alone supplies no evidence of a compensating stock movement. A movement-bearing actual is identified by both its line and linked movement on the production page. |

In the movement-identifier branch, compensation errors are copied to the order. A failed compensation leaves the branch without a positive deletion result and its transaction is rolled back. When a posting is disputed, distinguish the surviving actual row, the signed warehouse journal and the result reported by the operation. The movement plus its compensation can net to zero while the manufacturing register shows only surviving actuals.

## Canceling versus reopening the job

The order card accepts a separate choice to compensate actual consumption and production during cancellation or deletion. Cancellation with compensation runs both populations, requests deletion of the actual rows and then requests the canceled state. Without compensation, the header action itself does not unwind warehouse movements. Order deletion with compensation invokes the movement pass first, then delegates removal of the order and its related records. The stock-cancel routine exits before processing either population when the stock module is disabled.

For a full compensation, positive recorded consumption is an incoming movement. Positive finished output is an outgoing movement. Negative stored actuals reverse these directions. Each split supplies its own product, warehouse, lot and quantity. The method processes all eligible consumed splits first and then all produced splits. A finished lot that can no longer supply the return quantity can fail the entire compensation transaction, including earlier restored materials and any associated actual-row deletions. The resulting reported failure does not mean that the first input lot was independently restored.

The two ordinary ways of reopening manufacturing also differ. On the production page a produced order can return to **in progress**, allowing additional work against existing actuals. The general order reopen method accepts produced or canceled and moves the order to **validated/to produce**. Neither reopening method creates a warehouse movement or recreates an actual row removed by an earlier cancellation. On a job already canceled with full compensation, reopening the header alone does not manufacture stock a second time.

## Worked correction and material reconciliation

A job consumes three components from lot C1 and two from C2, then produces two finished units in lot F. Initially C1 held five, C2 held four and F held zero. The material balances after posting are two and two, with two finished units on hand. One finished unit is then shipped to a customer.

| Decision | C1 | C2 | F | Consequence |
| --- | ---: | ---: | ---: | --- |
| After the customer's shipment | 2 | 2 | 1 | The production register still shows two completed units. |
| Attempt a full manufacturing cancellation with compensation and negative stock prohibited | 2 | 2 | 1 | Removing the two-unit finished output requires two in F. The failed compensation restores neither component split permanently. |
| The customer actually returns the shipped F unit to its original warehouse/lot | 2 | 2 | 2 | A separate customer return or other authorised stock entry explains the additional physical unit. |
| A permitted full cancellation with compensation succeeds | 5 | 4 | 0 | The original material and finished quantities have been physically reversed. Production actuals are deleted on the cancellation path. |
| General reopen of that canceled order | 5 | 4 | 0 | The job is again validated/to produce. A new production posting is necessary to create physical output. |

Assume the job is in a state eligible for cancellation, such as in-progress after a production-page reopen, and has no other outputs. The first restoration attempt can fail even if another warehouse holds ample F or a different lot of the same finished item. A compensation writes current-time, zero-price movements, so restoration of original quantities does not rewind an earlier receipt's effect on the product average. [Current cost on a reversal](receipt-cost-and-reversal.md) · [Nested production and split actuals](../specification/operations/nested-production-orders.md)
