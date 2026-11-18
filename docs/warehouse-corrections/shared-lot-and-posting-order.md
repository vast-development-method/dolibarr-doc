# Shared availability, competing allocations and posting order

An order for eight units can pass a commercial availability decision, yet only six units from its requested lot may be available when the warehouse posts the dispatch. Four decisions occur at different times. They use different quantities, and each produces different evidence.

| Decision | Quantity consulted | Result preserved |
| --- | --- | --- |
| Suggest a batch split on the new shipment form | Remaining requirement and the lot quantity at this warehouse, reduced by earlier suggestions on this form for the same product, warehouse and lot | Editable proposed quantities. A setup option can leave quantity inputs empty. |
| Admit a batch shipment line | When shipment sufficiency is enabled, each selected stock-split record is fetched and its balance is compared to the proposed quantity | Shipment line, its source-line relation and batch details. This operation leaves the warehouse balances available to other documents. |
| Validate or close under the applicable stock-posting policy | Current warehouse and lot balances when the actual movement is created. With negative stock forbidden, an ordinary positive balance must cover the issue from this lot | Signed movement, revised warehouse balance, revised lot position, product summary and movement event within the owning transaction. |
| Classify the source sales order | Closed shipment quantities grouped by the originating order line in the completion comparison | Commercial status, independent of how many units are still on hand in the warehouse. |

## More than one demand for a lot

On a shipment form the suggestion accumulator is keyed by product, lot text and warehouse. If there are seven units of the same item/lot/location, then an earlier order line suggesting four leaves at most three to suggest on a later line. The formula is the smaller of the line's remaining demand and the lot balance less prior suggestions, floored at zero. An already-entered quantity can override the suggested value on redisplay. The same printed lot in a different warehouse has a separate accumulator. The suggestion is calculated as the form is built.

Submission reads the selected lot-position IDs and quantities, accumulates the split total for the originating line, and retains its identity. A serial-tracked product admits at most one unit of a given selected serial-position ID within that shipment submission. For a lot-tracked product the batch-line admission guard compares each selected batch row with its proposed amount when shipment sufficiency is enabled. Two documents can both pass separate line-admission decisions before either posts stock.

With negative transfers prohibited, the movement path checks the lot in the **specified warehouse**. It compares the batch identifier as a string. Stock for batch `0012` and stock for `12` are distinct in this comparison. For an ordinary positive available balance below the requested amount, the move fails. For the ordinary movement guard the product stock loader asks for nonzero batch positions. A matching position with an exact zero balance is absent from this collection even if a storage row exists. A missing lot is refused. Normal stock writes remove a lot position once it reaches zero. The lot master can still exist for historic traceability after its available position disappears.

**Worked sequential allocation.** Warehouse East has lot Q with seven units. Two draft shipments each request five from Q. With enough-stock admission enabled, each can individually pass while there are seven. Under posting at validation and with negative transfers disallowed, the first dispatch issues five. When the second is validated against the remaining two, the issue fails and the dispatch transaction rolls back. Its draft allocations can be revised to two units or reassigned to another available lot. Lot Q is then fully consumed only if that revised dispatch successfully posts. An order quantity of ten, two draft allocations of five, and seven physical units stand for three different business facts.

## Persisted state and concurrent actions

When repeated operations target one document, inspect the header's state test before inferring whether it can post twice. A guarded state transition and a shared-stock write are separate units of consistency.

| Operation | State or record decision at write time | Consequence for a retried request |
| --- | --- | --- |
| Close shipment | Update only a positive state other than closed. Zero rows changed returns without further stock work. | A close repeated after successful closure does not write another issue through this branch. |
| Reopen closed shipment | Require closed in the persisted header update. A freshly loaded validated shipment returns without work. | An already-open result and a stale-state error can both leave stock unchanged. |
| Close supplier receipt | Requires the loaded state eligible for closing and a persisted validated row. The operation inspects the affected-row count. | A competing completed transition prevents a second close receipt from this branch. |
| Reopen or unvalidate supplier receipt | Reopen requires a persisted closed state. Unvalidation requires the state observed by its caller. | A state mismatch prevents stock compensation and reports the mismatch. |
| Validate a shipment | Checks that the loaded shipment is draft. The persisted update is by ID alone. | The source does not establish the same concurrent-once guarantee as the closure path. |
| Post movements against a product | The writer reads balances for sufficiency and valuation, then writes the derived warehouse total and product average. The warehouse pair is unique. The ordinary update uses the pair as its predicate and an already calculated total as its new value. The lot updater likewise edits or creates the position after reading it. | The transaction groups a movement's writes. The observed application-level queries do not establish a universal serialization or retry guarantee for independent transactions sharing a product, warehouse or lot. |

The final product-stock summary is recomputed from warehouse rows. That last step cannot by itself prove that every earlier increment was represented in those rows. Product-wide average cost also uses an earlier quantity and average, even for receipts into different warehouses. The database engine, transaction isolation and any external serialization determine what competing transactions observe. This chapter traces the writer and state guards; it makes no claim that a particular engine reproduced any one concurrent outcome.

For a rebuild, the observable sequential accounting contract gives a useful reference for concurrent writers. Begin with 12 units of the same lot at unit cost 15. A receipt of four at 19 followed by one of four at 21 gives 20 units, acquisition value 340 and a final average of 17. At sufficient unit precision the opposite receipt order has the same final value. Both committed quantities should appear in the movement history and the final warehouse/lot balance, or a refused operation must be available for a separately identified retry. If only one receipt commits, the receiving document, movement journal and warehouse balance should all identify which one. This is a reconstruction criterion. The source does not provide a caller-supplied idempotency key for the common movement writer.

[Reversing posted dispatches](dispatch-and-order-corrections.md) · [Undoing receipts at current cost](receipt-cost-and-reversal.md) · [Lot identity and availability](../specification/operations/lot-identity-and-traceability.md)
