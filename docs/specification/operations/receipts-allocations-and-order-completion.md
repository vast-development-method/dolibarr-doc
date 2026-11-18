# Partial receipts, warehouse allocation and order completion

A supplier can send one order in several deliveries. One delivery can put goods from the same order line into two warehouses, or introduce several lots with different expiry dates. A receipt is the delivery document. Its allocations identify exactly how much of which order line reached each destination. The supplier order, receipt and warehouse each track a different result.

## Receiving a split delivery

For an order-backed allocation, the receiving operation resolves the actual order line and its product. It records the destination warehouse, quantity, product, source order and line, receipt, operator, lot, sell-by and eat-by dates, unit cost and comment. The allocation inherits additional fields from the order line. Additional fields entered for the receipt allocation override inherited keys when that feature is active. The allocation is marked validated for the dispatch-line status rule. Its parent receipt can still be a draft.

A product with stock management enabled requires a receiving warehouse unless the installation specifically permits warehouse-free receipt lines. A tracked product requires a batch or serial. Supplying a batch for an untracked product is rejected when batch handling is enabled. The product's active mandatory date fields also apply. A failing order-line lookup or a missing required field prevents that allocation from being added.

An order for 12 cartridges on line 41 arrives in two lots. Record seven from lot L1 in warehouse A and two from lot L2 in warehouse B, both against line 41. The undelivered three remain on the same commercial order line. A later receipt with three from lot L3 points back to line 41. For a trace inquiry, all three allocation rows matter. For comparison against the order quantity their combined quantity is twelve.

Related records include [Supplier receipt allocation](../../records/commercial.md#record-receptiondet_batch).

## Validation and the supplier order

Validation applies to a draft receipt. The ordinary permission is receipt creation. With advanced permissions the distinct receipt-validation grant applies. The operation assigns a definitive reference when it still has its provisional one, updates the receipt, optionally posts incoming stock and evaluates the originating order. It emits the receipt-validated event as part of the database transaction. A failed stock movement, source-order update or event causes the receipt validation to fail.

To determine the order's receiving status, collect allocations for the source order, excluding allocation rows belonging to **draft receipts**. When dispatch-line approval is enabled, only approved allocations qualify. Sum the eligible quantities by product. Separately sum the ordered quantities by product for goods and eligible stockable services. Service inclusion requires service stock support. Special line types above the service type are excluded. Exact equality of quantities and product keys makes the order completely received. An ordinary mismatch leaves the order partially received.

An optional over-receipt policy also permits completion for reported differing products whose received quantity meets or exceeds the ordered amount. The extra branch iterates differences found on the received side. It does not repeat the missing-order-product test used for exact equality. An order for X and Y, with X received exactly and no allocation at all for Y, can therefore be classified as completely received by that branch. The order's individual allocations and outstanding lines retain the information needed to identify Y.

Validation groups by product. If two order lines both carry the same product, receiving a combined quantity equal to their combined ordered quantity satisfies the product comparison, even if the references on the allocations distribute the quantities unevenly. Closing a receipt uses a separate order-line comparison. For line 41 ordered at five and line 42 ordered at seven, twelve booked against line 41 can satisfy the product comparison but leaves line 42 short in the closed-receipt comparison.

## Posting, closing and reversing

| Operation | Receipt state and stock effect |
| --- | --- |
| Validate in receipt-validation stock mode | Move to validated. Each applicable allocation posts its signed received quantity, stored unit cost and destination. Tracked rows also pass their lot and dates to stock. |
| Close in receipt-closure stock mode | Require validated state both on the loaded object and on the persisted record. Change to closed and post the corresponding receipts. Repeating the close on an already closed object does no work. A stale validated object fails the conditional write before stock changes. |
| Reopen a closed receipt | Change closed to validated and clear the billed flag. When stock was posted on close, issue the corresponding quantities back out of the same warehouses and batches. For a supplier-order source the operation sets the order back to partially received. |
| Return to draft | Require a current validated or closed state and condition the write on the previously observed state. Reverse quantities previously posted on validation, or posted on close when the previous state was closed. |

The stock-posting loops skip zero quantities. Negative receipt quantities participate only where the negative-receipts option allows them. A batch supplied on the document can fail later at stock posting, for example because a previously registered lot has a different established expiry. The posting date and the date on the goods record are separate from the supplier's commercial order date.

When closing a receipt from a supplier order, the closure operation loads quantities from **closed** receipts by source line ID. A stocked order line meets this comparison when its closed quantity is at least its ordered quantity. Once all relevant lines meet the comparison, the operation requests full delivery classification for the supplier order. Receipt closure itself remains available when the other deliveries are still pending. Thus the receiving team can close the nine-unit first delivery in the example and later close the separate three-unit delivery.

One other list used by replenishment compares goods ordered and dispatched by product and treats a product as pending while ordered quantity exceeds dispatched quantity. It excludes service lines when stock support for services is disabled. It reads dispatch rows for the order directly. Its boolean answer and the receipt's validated or closed state are distinct facts.

## Outbound carrier information and physical allocations

An outgoing shipment carries its carrier method, tracking number, actual weight, weight unit, depth, width, height and shared length unit on the shipment header. The create operation removes whitespace from the sanitized tracking number. Fetching the shipment reads that identifier and resolves its carrier tracking link. An order-line shipment allocation answers how many units of that order line left a warehouse, and its batch splits identify the goods. Neither a carrier tracking number nor a lot identifier identifies an individual carton within the shipment.

The physical schema also defines parcel rows with a shipment ID, description of contents, value, package type, dimensions, weight, handling information and rank. The ordinary shipment create/fetch path above writes and reads the measurements and tracking at header level. That path establishes no carton-level mapping from each parcel to its individual dispatch allocations. In a delivery of two cartons from different lots, the shipment and allocation records support a lot trace across the delivery. A carton-content manifest requires an explicit association beyond those records.

The [receipt reconciliation schema](../../../schemas/supply/receipt-completion.schema.json) and [two-line allocation example](../../../examples/supply/receipt-completion.json) show both completion decisions on the same goods. Origin line identity survives the grouping by product. The example compares the two decisions against one set of facts, independently of which transition last set the order's status.
