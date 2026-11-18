# Purchase receipt splits, inspection and completion

A delivery of one ordered item may arrive in several warehouses or lots. The purchase order tracks the commitment, a dispatch split records a particular quantity received against it, an optional inspection decision determines whether that split counts toward completion, and a stock movement changes warehouse inventory. These records answer different questions even when one user action writes several of them.

## Recording physical arrival

The direct dispatch operation accepts a sent, partially received or completely received purchase order. A positive warehouse identifier and a nonzero quantity are mandatory. The inputs include the catalogue item, ordered line, received quantity, warehouse, unit valuation, comment, lot, expiration and sell-by dates and optional linked receipt. It records the operator and creation time. One delivery split belongs to one warehouse. Receiving six units at the depot and four at a branch creates two rows.

The default split status is approved. When inspection is enabled, the split starts pending. On successful insertion the operation emits a supplier-line dispatch notification. With inventory enabled and stock posting configured at purchase dispatch, it then creates a warehouse receipt for the catalogue product. If supplier returns by negative quantity are enabled, a negative split posts an outward movement with the absolute quantity. The supplied unit price is expected to reflect the applicable discount and valuation settings. A failed stock movement or dispatch notification rolls back the recording transaction.

The physical posting can run while a split is pending inspection. The inspection decision and the inventory entry therefore need separate timestamps in a receiving history. Repeating the same dispatch request can append a second split and another stock movement, including against an order already classified as completely received. In the event of an ambiguous response, the originating order line, warehouse, lot, receipt identity and quantity allow the receiving operator to distinguish an existing arrival from a new delivery.

## Inspection and warehouse corrections

Under ordinary permissions the right to receive purchase orders also allows inspection in direct-dispatch mode. Advanced permissions can reserve inspection for the purchase-order controller. With the dedicated reception module enabled the form uses its creation and advanced validation permissions. When acting on an existing split the form first verifies that the split belongs to the purchase order being displayed.

| Action | Split and order | Warehouse effect |
| --- | --- | --- |
| Approve | Set split status to 1 and recalculate the order. An approved split counts when inspection is required. | The inspection handler does not issue an inventory movement. The original inbound posting follows the configured stock milestone. |
| Deny | Set status to 2 and recalculate. The split retains its quantity, inspector's decision and order association. | A denial alone does not return physical inventory to the supplier. |
| Return to pending | Set status to 0 and recalculate. It ceases to contribute to the inspected-quantity aggregate. | The original inbound movement remains independently traceable. |
| Correct warehouse or quantity | Update the existing split with the new warehouse and quantity. | When stock posts on dispatch, remove the old quantity from the original warehouse and receive the corrected quantity in the new warehouse in one transaction. Stock movement uses current lot dates when available. |
| Delete a recorded split | Remove the selected split under the receiving permission. | Where dispatch posted stock, the direct form also posts an outward movement to reverse the received quantity. |

An edit from four in warehouse A to three in warehouse B can therefore produce movements of minus four at A and plus three at B. In the correction path failure of the second movement rolls back the change and the first movement. Changing an inspection decision follows a different procedure and does not execute that pair of stock corrections.

## Deriving the purchase-order status

The recomputation builds two maps keyed by product. The received map sums dispatch quantities, limited to approved splits when inspection is enabled. The requested map sums quantities across the order lines for each catalogue product. It skips free-text lines. It includes a service only when service stock is supported and the service line is stockable. This comparison discards lot, warehouse and individual order-line identity. Two lines for the same item, ordered at different prices, can jointly be satisfied by the correct number of units of that item.

With exact matching, the key sets must agree both ways, and all corresponding quantities must match. If the caller requests closure, a complete match sets the order to completely received. The same match leaves the order partially received when the caller elects to keep it open. Any ordinary mismatch produces partial receipt. When the filtered dispatch query returns no rows, the recomputation returns success without assigning a replacement state. Undoing the only split approval can therefore leave the previous header classification until another operation changes it.

The optional overdelivery rule works differently. If exact matching fails, it compares entries in the **received** map that differ from the requested values. It permits completion when all those received differences meet or exceed the matching request and closure was requested. Missing requested keys are not carried into that second comparison. Consider an order for five A and three B. A single approved split of five A fails the exact-match rule because B is missing. With overdelivery enabled the received-side differences can be empty, and the implementation can classify this order as complete. A header showing complete in that configuration cannot establish receipt of every product.

For reconciliation by individual purchase-order line, the order also exposes a different receipt query that sums split quantities against originating line identifiers, with an optional receipt-status filter. That projection preserves the distinction between two ordered lines for the same product that the product-level completion decision combines.
