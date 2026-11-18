# Choose when a trade changes physical stock

A sale can have an order date, multiple dispatch dates, an invoice date and a date when the final delivery is closed. Each date can fall in a different reporting month. The stock policy selects the business event that writes the movement for ordinary trading documents. It is set separately for sales and purchases, for the current entity. The point-of-sale workflow has its own settings.

## Sales and purchasing

| Side | Selected event | Quantity and operational consequence |
| --- | --- | --- |
| Sales | Confirm customer order | The order transition issues stock for applicable product lines at the selected warehouse. Stock can leave the balance before a carrier receives the goods. Returning the order to draft has a compensating path. |
| Sales | Validate shipment | The dispatch allocations carry the goods, lots and warehouses used to issue stock. Two shipments against an order can generate two independently dated issues. |
| Sales | Close shipment | A validated dispatch can exist with its goods still counted at the warehouse. Closing it posts the issue. Reopening has a corresponding stock path. |
| Sales | Validate customer invoice | A qualifying document with a positive selected warehouse uses product-bearing lines. A customer credit uses the receipt direction. A deposit invoice skips this stock action. The warehouse on the validation operation matters. |
| Purchases | Approve supplier order | A move into the accepted state receives the applicable product lines. When a second approval is required, an intermediate approval that leaves the order in the validated state does not run this stock branch. The acquisition unit price includes the line discount unless the moving-average policy excludes it. |
| Purchases | Allocate goods on supplier order | The dispatch operation uses the allocated quantity and a positive destination warehouse. This route can receive the order in instalments. |
| Purchases | Validate receipt | A receipt document posts the incoming movement at validation. Further receipts can allocate the balance of the order. |
| Purchases | Close receipt | A validated receipt exists before its stock posting. Closing and reopening each have an inventory effect. Receipt completion and the purchase order's aggregate delivery status have their own rules. |
| Purchases | Validate supplier invoice | Stock posting takes its quantities from the supplier invoice. Its issue date, product lines and warehouse choice can differ from those on the delivery paperwork. |

On the setup screen, enabling one sales event clears the other three sales selections for the entity. Enabling one purchase event clears the other four purchase selections. Clearing an option removes that setting. Changing the selection updates policy for the entity. The setup action contains no replay of historical documents or migration of in-flight allocations. For a transition that reverses stock, trace which policy it reads at the time of reversal. Historical inventory is established by recorded movements.

## Availability at data entry

Stock sufficiency is a separate decision for customer order lines, invoices and shipments. An order can require sufficient stock when its line is entered and still use shipment closure as the later posting event. Passing the entry decision does not create a movement or reserve a quantity. Two open documents can compete for the same balance.

For an ordinary stock-managed product, an order line reads real product stock. For a shipment with a specified warehouse, the line examines that warehouse's quantity. When product composition is enabled and a product has children, availability uses the component-derived quantities. The ordinary shipment path selects the specified warehouse when present. The order path takes the least of the returned warehouse quantities and falls back to zero when no value was obtained. Batch allocations add a second level of identity below the product and warehouse. A separate negative-transfer setting controls whether the transfer policy permits a negative balance.

The setup screen disables invoice and order posting choices on both sides when lot/serial handling is enabled. A separately configured restriction can have the same effect when component products are enabled. This is a restriction on choices presented by setup. The invoice implementation also contains specialised batch handling, including a lot-selection rule. Treat the route and the selected policy as part of any scenario that depends on an automatic lot choice.

## A delivery across month end

An order for 12 units is confirmed on 29 April. Five are dispatched and validated on 30 April, closed on 2 May. The other seven are validated and closed on 4 May. Assume a single warehouse, sufficient opening stock, ordinary stock-managed goods and no adjustments. With order posting, the order reduces April stock by 12. With shipment-validation posting, the April reduction is five. With shipment-closure posting, April has no reduction from either dispatch and May records the two issues. The ordered quantity is 12 in all three cases. A warehouse cutoff report and the sales order register answer different questions.

For the purchase side, suppose the supplier order has ten units at 20 each with a 10% line discount. If final approval owns the stock increase, the receipt call gets ten units at 18 each under discount-inclusive valuation, or at 20 when the discount is excluded from moving-average cost. If receipt closure owns the increase, approval alone leaves physical stock unchanged. Reconcile cost and quantity through the actual movements before attributing a supplier invoice difference to the warehouse.

[Stock allocation and completion](../specification/operations/receipts-allocations-and-order-completion.md) · [Stock at a date](../specification/operations/stock-at-date-and-value.md) · [Kits and components](../specification/operations/kit-composition-and-stock.md)
