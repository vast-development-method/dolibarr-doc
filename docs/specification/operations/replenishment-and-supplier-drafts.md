# From a stock shortage to a supplier draft

A buyer sees a product below its target, chooses how many units to buy and selects a supplier price. Three quantities matter at different stages. Physical stock measures units held. Open purchases measure units already ordered. The suggested quantity is editable and becomes a commercial commitment only as the resulting purchase order moves through approval and ordering.

## How a shortage is measured

The planner loads open and internal warehouse stock. Stock-reading permission and access to the product or service area allow the user to consult it. Creating supplier orders additionally requires supplier-order creation permission. Settings that postpone stock movement until shipment, receipt or related events can make the projected quantity differ from the physical balance. Manufacturing can also make them diverge. When they can differ, the planner defaults to projected stock unless configured to prefer physical stock. The operator can explicitly select a mode.

| Operand | Physical mode | Projected mode |
| --- | --- | --- |
| Target | Greater of desired stock and low-stock alert threshold | Same |
| Available basis | Physical balance | Projected balance supplied by stock planning |
| Outstanding purchases | Ordered quantity on validated, accepted, sent and partially received supplier orders, less reception quantities on partially received orders. Selecting draft inclusion adds draft orders to the order total. | The projected quantity already accounts for its configured commitments. |
| Suggested order | `max(target − physical − outstanding purchases, 0)` | `max(target − projected, 0)` |
| Low-stock warning | Current physical balance below a nonzero alert | Current projected balance below a nonzero alert |

The receipt subtraction in physical mode filters on the **supplier order's status**. It sums receipt allocation quantities for the product across applicable orders. The supplier visibility rules of the statistics query can restrict the figures seen by an internal user with a limited supplier portfolio.

Warehouse limits can replace both the target and balance in the suggestion. A missing warehouse limit contributes zero to the corresponding target field. The physical formula still subtracts the product-level outstanding purchases. An inbound order for 20 units can therefore reduce a warehouse's suggestion even when the selected warehouse has no receipt allocated to it. Per-warehouse projected stock has a separate setting. A warehouse target paired with a projected balance requires that setting for a warehouse projection to be loaded by this page.

For example, a product has desired stock 60, alert 35, physical stock 18 and 22 outstanding. The warning appears and the editable suggestion is 20. If another 15 units on draft orders are included, the suggestion falls to 5. In projected mode a projected balance of 29 produces a suggestion of 31. Subtracting the same purchase commitments again would understate demand. When a buyer enters 24 instead of 20, the purchase operation uses 24.

## Selecting and pricing lines

The buyer selects individual rows. A selected row needs a supplier price selector value. The operation resolves the selected price record to its supplier and product, then searches for a price valid for the submitted quantity. The selected price record qualifies if its minimum quantity is at most the positive order quantity. When a selected offer is too large, a fallback search can find an eligible tier for the same product and supplier. If the initially selected price record cannot be resolved, the lookup falls back without those identifiers. When the buyer filtered by supplier, a mismatch with the resolved supplier excludes the line.

A valid nonzero quantity produces a line with the supplier reference, product, unit, goods or service type, supplier unit price, VAT rate and line discount. The base price is tax-exclusive. A supplier offer of 150 for ten units yields 15 per unit. When supplier-specific product descriptions are enabled and populated, that text appears on the order. Otherwise the product description is used. A foreign-currency offer also supplies a foreign unit price when multiple currencies are enabled. A blank or zero offer discount takes the supplier's default purchase discount. Local taxes are resolved against the ordering company, the supplier and the VAT rate.

A shortage of three units can be smaller than the smallest supplier tier of five. The buyer may choose a valid order quantity or a different offer. An unresolved minimum produces a warning for that selection. Other valid selections remain eligible for ordering in the same submission. The suggested quantity field does not round a shortage up to the supplier's minimum.

## Draft consolidation and resubmission

The operation groups accepted lines by supplier. For each supplier it searches the accessible order entities for a draft whose source is replenishment. The most recently created eligible draft receives the new lines. Manually created drafts have a different source and remain separate. Where no eligible draft exists, a new replenishment draft takes the supplier's currency and default payment terms and method. This operation appends commercial lines. Repeating the same submission can append the same demand a second time.

With three selected products, two from supplier S and one from supplier T, an existing replenishment draft for S receives two lines. T gets a separate replenishment draft even when T already has a manually prepared order. If the selected price for one of S's products has an unmet minimum, the remaining valid S and T lines can still be committed.

The operation wraps the suppliers in a database transaction. A recorded failure to create an order or append a line group rolls the submission back. In the existing-draft branch, the result variable is overwritten on each append and inspected after the loop. A later successful append can hide an earlier failed append in that group. The selected-line warning and the order-creation result therefore convey different information. The persisted order lines identify precisely which products and quantities the buyer obtained.
