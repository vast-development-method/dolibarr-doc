# Counting stock and moving it between warehouses

A stocktake has one observed quantity per product, location and lot. An internal transfer records a deliberate departure and a later arrival. Each changes stock, but only the transfer has a period in which the goods are in transit.

## Opening a stocktake

A count can cover one product, one warehouse, selected product categories or a broader scope. Starting a draft count deletes any earlier detail for that count and builds fresh lines from existing warehouse stock. The selection respects product and warehouse entity access. If the operator explicitly includes sub-warehouses and the installation enables that option, the selection extends to the warehouse's descendants. Category selection requires membership in at least one selected category. Service items qualify when service stock is enabled. With component associations enabled, products that are parents of assemblies are excluded from this initial snapshot.

For a warehouse row with a batch split, prefill the quantity from that split. For a row with no split, prefill the warehouse balance. If an existing batch row belongs to a product currently configured as untracked, start fails and the transaction restores the previous state. Newly discovered physical goods with no previous warehouse stock row cannot appear through prefill. The interface also supports adding a count line.

| State | Effect |
| --- | --- |
| Draft, 0 | Defines count scope. Starting generates the snapshot and changes status to in progress. |
| In progress, 1 | The operator enters observations and can choose to post or cancel. |
| Recorded, 2 | Ordinary completion has processed the observations for posting. Each nonzero adjustment refers to its movement. |
| Cancelled, 9 | Count is closed by cancellation without running its posting loop. |

Returning to draft via the domain operation deletes the existing count detail as it resets the status. A count-line key combines inventory ID, warehouse, product and batch. The line holds the comparison quantity, the observed quantity, optional valuation inputs and the resulting movement ID. The normal grant for saving observations and recording changes is stock-movement creation. Under advanced permissions the inventory-write grant supplies the count actions.

Sources include `htdocs/product/inventory/class/inventory.class.php`, lines 55–59, 247–445 and 764–795. `htdocs/product/inventory/inventory.php`, lines 130–138 and 410–476. `htdocs/install/mysql/tables/llx_inventorydet-stock.sql` and `htdocs/install/mysql/tables/llx_inventorydet-stock.key.sql`.

## From observation to correction

The save action processes the visible page of count rows. A value of zero is an observation. Clearing a previously entered field sets the observation to null. An omitted field is left alone. A negative observed physical quantity is rejected. A permitted save updates the count's modifying user.

At posting, load the current warehouse balance of each product. For a tracked product use the matching lot's current balance, taking zero if no matching split is present. Rows with a null observation are skipped. The signed adjustment is **observed quantity minus current quantity**, rounded to stock precision. A positive amount creates an incoming correction and a negative amount creates an outgoing correction. A zero difference produces no movement. Each nonzero movement carries the inventory origin and an operation code derived from the count reference. Its ID is stored back on the count line. When the current comparison quantity differs from the snapshot, the line's comparison quantity is refreshed on that movement-writing branch.

**Example.** The snapshot contains 14 units, an unrelated receipt adds 4 before posting, and the operator records 16. The posting correction is −2 against the live 18. Subtracting the snapshot from the observation would incorrectly add 2. An explicit zero for another line whose live balance is 3 posts −3. Leaving a third line blank creates no movement.

If real average-cost management is enabled and a nonzero observed unit cost is supplied, the action uses it for the correction and updates the product's average cost. A counted line can update cost even when its quantity difference is zero. A zero-valued cost doesn't enter this override branch. The product-level cost is shared by the count lines for that product. The posting loop runs in line-ID order, so different nonzero costs for the same product on multiple counted lines can successively replace it. Where sharing and per-entity average-cost options both apply, the entity-level value is updated as well.

The posting handler wraps the movement loop in one transaction and rolls back on reported movement or count-line write errors. Its call to mark the count recorded does not inspect the returned status before committing. When recovering from an interruption or a failed closing notification, read the stored count state, line movement IDs and current balances together.

Sources include `htdocs/product/inventory/inventory.php`, lines 163–307 and 311–385. `htdocs/product/inventory/class/inventory.class.php`, lines 408–425.

## Transfer lines and two-stage custody

The transfer card requires transfer write permission for draft line operations and for posting the departure and arrival. A draft line specifies a positive quantity, a product, a source warehouse and a destination warehouse. A tracked product requires lot text. An untracked product rejects supplied lot text. Repeating the same product, source, destination and lot adds to the matching line on ordinary add. A serial already present for the same product cannot be added a second time, even with a different warehouse pair. The draft line captures product average cost. The transfer's displayed value sums line quantity multiplied by captured cost.

| Starting state | Action | Movement | Resulting state and recorded time |
| --- | --- | --- | --- |
| Draft, 0 | Validate | No departure or arrival in this action | Validated, 1. A provisional reference becomes the final reference. |
| Validated, 1 | Confirm departure | Issue each line at its source | In transit, 2. Set actual departure time. |
| In transit, 2 | Undo departure | Receive each line back at its source | Validated, 1. Clear actual departure time. |
| In transit, 2 | Confirm arrival | Receive each line at its destination | Closed, 3. Set actual arrival time and invoke the close event. |
| Closed, 3 | Undo arrival | Issue each line from its destination | In transit, 2. Clear actual arrival time. |

The in-transit status explains the temporary reduction in total warehouse on-hand. If X sends five of its eight units to Y, dispatch leaves X with three and Y at its opening balance. Receiving the goods adds five to Y. Undoing arrival first takes the five out of Y. Undoing departure after that restores X to eight. These are new warehouse movements. If Y has already used the goods, the outgoing stock rules can prevent the arrival reversal.

For each confirmation, the card groups the selected leg's line movements into one database transaction. It commits the stock changes before setting the header's new status and actual timestamp. At arrival the closing event also follows the movement commit. A reported header or event failure therefore does not establish that the balances were rolled back. Before repeating a leg, identify its source/destination movements, lot splits and operation code. Repeating a leg while its header is stale can apply the quantity twice.

Sources include `htdocs/product/stock/stocktransfer/stocktransfer_card.php`, lines 103–106, 170–316 and 317–426. `htdocs/product/stock/stocktransfer/class/stocktransfer.class.php`, lines 110–113, 441–455 and 595–652. `htdocs/product/stock/stocktransfer/class/stocktransferline.class.php`, lines 434–507.
