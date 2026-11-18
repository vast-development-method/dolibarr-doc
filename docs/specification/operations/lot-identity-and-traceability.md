# Lot identity, expiry and traceability

A receiver can put the same production lot in several warehouses. The expiry date belongs to the manufacturer's lot. The quantity available for dispatch belongs to a particular warehouse and lot. The movement journal records how that quantity got there. These distinctions also apply to individually numbered equipment, with an additional limit on the quantity held under one serial number.

## Records and keys

| Record | Identity | Contents and use |
| --- | --- | --- |
| Product tracking policy | Product | Selects ordinary, lot-tracked or serial-tracked stock. The product specifies whether sell-by, eat-by or both dates are mandatory. |
| Lot master | Product and lot/serial text, with a separate row ID | Holds the entity, manufacturing and expiry information, quality-control metadata and audit fields. The unique key uses product and batch. Different products can carry the same printed identifier. |
| Warehouse stock | Product and warehouse | Carries the aggregate physical quantity. |
| Lot balance | Warehouse stock row and lot/serial text | Carries the quantity of this product and lot in this warehouse. A single lot master can correspond to several balances. |
| Stock movement | Movement ID | Signed quantity, movement type, product, lot, warehouse, author, date, price, origin and operation reference. |
| Shipment or receipt allocation | Source line, warehouse, quantity and batch on its allocation row | Establishes which commercial document supplied or received a specific quantity. The lot master contains neither the sales order nor its customer. |

Sources include `htdocs/install/mysql/tables/llx_product_lot.key.sql`, `llx_product_batch.key.sql`, `llx_product_stock.key.sql`, `llx_stock_mouvement.sql` in the same directory. Movement creation is in `htdocs/product/stock/class/mouvementstock.class.php`, lines 305–375 and 505–550.

## Admission of new stock

An incoming movement for a tracked product supplies the product, destination warehouse, quantity and lot text. A missing identifier fails before the stock movement completes. The lot master trims the identifier when creating it and refuses an empty value. The master uses the product's date policy and the installation's enabled date fields. If a product requires both dates and sell-by is disabled globally, the remaining eat-by field is still required. Turning off both fields bypasses this date requirement.

| State of each date on the master | Value supplied on receipt | Result |
| --- | --- | --- |
| No lot exists | Date supplied or left empty | Create the lot with the incoming values, subject to the active mandatory-date policy. |
| Date already known | Same calendar date or omitted | Accept the movement and retain the established date. The comparison handles the stored timestamp and its day-level form. |
| Date already known | A different date | Reject the movement. A receiver cannot silently redefine the expiry for stock held elsewhere. |
| Date unset | Value supplied | Update the master with the newly learned date. |
| Date unset | Value omitted | Leave the master date unset, subject to the applicable validation path. |

For a negative movement, the stock writer discards the dates supplied by the calling document before resolving the master. A shipment entered before a correction to the lot's eat-by date can therefore go out against the corrected master. The outgoing operation cannot reintroduce its stale date. The common movement writer enforces the lot identity and date-consistency rules. Its date comparison does not itself constitute a general prohibition on moving expired stock.

Sources include `htdocs/product/stock/class/productlot.class.php`, lines 255–365 and 375–455. `htdocs/product/stock/class/mouvementstock.class.php`, lines 349–461.

## Quantity and serial identity

The movement changes the warehouse aggregate and the matching lot balance. A lot balance that reaches exactly zero is removed. A zero aggregate may be removed when it has no lot-balance children. This matters when one lot is positive and another negative: a warehouse aggregate of zero can still describe a meaningful split. The master remains available for traceability.

When negative transfers are disallowed, an issue for a tracked product looks for the requested identifier in that warehouse. Sufficient combined quantity of other lots cannot substitute for the requested one. The issue path compares batch keys as strings, preserving the distinction between printed identifiers such as `0123` and `123`. The stocktake closing path has a separate case-insensitive lookup for a typed lot number.

On an incoming movement for an individually numbered product, the writer sums quantities for the product and serial across its warehouse lot balances. A resulting total above one makes the movement fail and roll back. Counting the number of matching balance rows would produce a different outcome. The inter-warehouse transfer card also rejects repeating the same serial for a product on two transfer lines, and rejects a serial-line quantity greater than one.

**Example.** Warehouse A has four units of product P under lot R7 and warehouse B has six. Receiving another four in B changes B/R7 to ten and the combined quantity to fourteen. Shipping all four from A removes that warehouse's R7 balance. The remaining master still identifies the same lot, and B/R7 stays at ten. For a serial-tracked product already held as one unit in B, a second receipt of that serial into A fails the total-of-one guard.

Sources include `htdocs/product/stock/class/mouvementstock.class.php`, lines 467–508, 639–715, 948–1011 and 1321–1345. `htdocs/product/inventory/inventory.php`, lines 209–228. `htdocs/product/stock/stocktransfer/stocktransfer_card.php`, lines 170–230.

## Editing, retention and tracing

The lot card requires an internal user, enabled lot tracking and product read access. Product creation/modification permission governs changes to dates and metadata. Product deletion permission governs the delete action. An edit to an individual expiry field evaluates that field's mandatory setting and emits a lot-modification event on success. The card can expose manufacturing and scrapping dates, end-of-life date, inspection frequency and lifetime under the relevant options. A stored inspection interval is descriptive data. The stock movement described above uses the product, serial, warehouse and quantity rules.

Deletion examines both current warehouse lot rows and historic stock movements using product and batch. A lot that has left the warehouse can still be protected by its movement history. A permitted deletion invokes the delete event, removes its additional fields and deletes the master in a database transaction.

The lot statistics expose distinct counterparties and documents, allocation row counts or quantities depending on the report. Shipment, supplier-order and receipt summaries have different joins. Manufacturing separates planned consumption, actual consumption, planned output and actual output. In the receipt and manufacturing summaries the batch-text predicate is accompanied by document entity and access restrictions, but those two queries do not also require a matching product ID. If two products both use `JUL-1`, their numbers can combine on these views. For a product-specific trace, retain each allocation's product ID and document state alongside its lot text. A commercial allocation total and a posted movement total can diverge, especially when draft documents exist.

Sources include `htdocs/product/stock/productlot_card.php`, lines 115–142, 160–272 and 405–447. `htdocs/product/stock/class/productlot.class.php`, lines 706–790 and 864–1142.
