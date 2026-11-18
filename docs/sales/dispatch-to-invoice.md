# Partial dispatch, delivery and billing

For an order of ten identical units, a warehouse may send four today and six next week. Warehouse allocation, physical stock movement, delivery completion, billing classification and cash receipt occur at different times. Tracking the ordered line ID and the document links makes each quantity and amount reconcilable.

## Fulfilment records

A shipment has a party, entity, reference, validation date and actor, intended delivery date, actual shipping date, shipping method, tracking information, status and an independent billed flag. Its allocations carry the shipment ID, source object type and line ID, quantity, warehouse, optional product and unit. Kit component rows can have a parent. Lot allocations attach to individual shipment detail IDs with quantity, batch identifier and dates. Multiple dispatches of the same SKU can belong to different order lines and separate shipments.

| Event | Guard or calculation | Changes |
| --- | --- | --- |
| Prepare allocation | For stockable items the standard add-line path checks the warehouse unless the exemption applies. Optional sufficient-stock checking tests available physical quantity. Lot-managed goods use the batch path. | Capture warehouse and quantities. A draft can already count against the optional order-quantity ceiling. |
| Validate shipment | Draft with a party. The REST method requires shipment create and resource access. With advanced permissions the domain also tests the shipping validation right. | Assign reference, validator and date, move the origin order to shipment in process and fire `SHIPPING_VALIDATE`. With stock-on-shipment enabled, issue quantities per warehouse and lot in the validation transaction. |
| Close shipment | The domain attempts validation if still draft. Closing updates a positive, nonclosed status. A second close does no work in the domain. | Set actual dispatch date if absent. Stock-on-close issues stock at this stage. The origin order can close when the eligible order line quantities match cumulative dispatch. |
| Mark billed | A separate shipment billing action can run from an invoice workflow. | Set the billing flag. Delivery status and payment records have their own lifecycles. |

### Three different quantity tests

1. **Allocation ceiling.** When `STOCK_EXPEDITION_NO_MORE_THAN_ORDER` is enabled, the comparison is requested quantity ≤ ordered quantity − quantity on other shipment rows for the same origin line whose shipment status is ≥ 0. Draft reservations count. Editing excludes the current row. For an update with multiple lots, the proposed quantity is their sum. The guard skips title/separator lines.
2. **Built-in completion on closing.** The close operation asks for cumulative shipments at the closed threshold. The underlying query uses status **≥ 2**. For each physical order line, and for services when stock supports them, it compares the summed quantity by order line ID with the ordered quantity for equality. A missing shipment contributes zero. The shipment class also defines an in-progress status with numeric code 3, so the threshold is significant. If every eligible line matches, shipment closure calls order closure. This core path does not inspect the order-close return value, so read back the stored order status after closing the shipment. A successfully closed shipment can coexist with an order that still requires attention.
3. **Workflow completion.** Optional `WORKFLOW_ORDER_CLASSIFY_SHIPPED_SHIPPING` or `WORKFLOW_ORDER_CLASSIFY_SHIPPED_SHIPPING_CLOSED` evaluates the corresponding event. This handler sums positive-status linked shipments **by product**, skips ineligible service and title lines on the expected side, and closes the order when expected product totals match. Two separately priced lines for the same SKU illustrate why this roll-up differs from the built-in per-line comparison.

## Billing sources and classifications

| Path | Quantity and amount basis | References and conditions |
| --- | --- | --- |
| Order → invoice | The order-conversion method copies ordered quantities and commercial terms into a new invoice. It preserves tax inputs, currency values and line organisation. | Keeps source order as linked document. With workflow and automatic invoice creation enabled, `ORDER_CLOSE` calls this routine. That may be triggered by completion of shipping. |
| Shipment → invoice via invoice card | For ordinary selected shipment lines the quantity is the shipped quantity. Price, discounts and source VAT inputs come from the source commercial line. When all order products are loaded, a zero-quantity shipment line is skipped. | Invoice records the shipment as origin. For an ordinary single-order shipment, the card also links the invoice back to the originating order. Run both partials from shipment sources if each invoice should reflect its own dispatch. |
| Validated invoice → billed shipment | With `WORKFLOW_SHIPPING_CLASSIFY_BILLED_INVOICE`, sum net amounts of linked validated or closed shipments. Compare with the invoice net at total precision. | On a match the workflow calls the shipment billing operation for the linked shipments. |
| Multiple invoices → billed order | `WORKFLOW_SUM_INVOICES_AMOUNT_CLASSIFY_BILLED_ORDER` requires exactly one linked source order on the triggering invoice. All its linked invoices must be validated/closed, allowing the currently validating one. | When their summed net equals order net at configured total precision, classify the order as billed. Another option compares **one invoice** to the sum of eligible linked orders. Only the latter comparison uses the optional unequal-amount override. |

## Service boundaries

`POST /orders/{id}/shipment/{warehouse_id}` requires shipment-create and access to the order, and rejects a nonpositive warehouse ID. The service populates **the original ordered quantities**, sends the rows to the shipment creation routine for kit expansion, and returns the shipment ID. This operation has no partial-quantity input or request idempotency key. To create a partial dispatch, submit explicit allocation quantities through the shipment creation service or card. `GET /orders/{id}/shipment` requires shipment-read and order access, groups linked shipment IDs through the order-line join and returns 404 for no matches.

The [dispatch allocation schema](../../schemas/sales/dispatch-allocation.schema.json) represents **positive, order-backed physical allocations**. It suits an outbound warehouse integration. The business layer must resolve the order line and warehouse, total any lots and apply the correct status-dependent limits. The schema covers this named operation, while the source also supports free shipment lines and other shipment contexts.

## Acceptance scenario

Assume ten units on one line at 50 each, discount 10%, VAT 15%, stock starting at 20, stock issue on shipment validation and no local taxes. Enable the order-line quantity ceiling and the cumulative invoice workflow. Disable automatic invoice generation at order closure for this scenario.

| Step | Action | Expected observation |
| --- | --- | --- |
| 1 | Prepare a draft for 4 units. Attempt a second draft for 7. | The second allocation exceeds the 6 remaining and is refused. Physical stock remains 20. |
| 2 | Validate the first shipment, then close it. | Stock is 16. The order is in fulfilment. Closing 4 alone cannot satisfy a line for 10. |
| 3 | Invoice the selected shipment line in full. | Invoice for 4 gives 180 net, 27 VAT, 207 gross. After validation 180 is below the required order net 450. |
| 4 | Prepare, validate and close another shipment of 6. | Stock becomes 10. Cumulative closed quantities equal 10 and the origin order can close. |
| 5 | Generate and validate the second shipment invoice. | The second invoice gives 270 net, 40.50 VAT, 310.50 gross. The sum of validated nets is 450, so the order qualifies as billed. Neither invoice requires a payment record for this classification. |
| 6 | Close an already closed shipment through the same domain operation. | The already-closed guard returns no work. No further stock issue is made. |
