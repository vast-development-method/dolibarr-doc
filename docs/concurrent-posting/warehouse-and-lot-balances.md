# Warehouse balances, lots and average cost during simultaneous posting

A stock movement records a signed quantity in `stock_mouvement.value`. The current warehouse balance is `product_stock.reel`, keyed uniquely by product and warehouse. A tracked lot also has one `product_batch.qty` per warehouse-balance row and lot code. The product's cached `stock` and average unit cost `pmp` each have a separate calculation.

## Read and write order

1. The movement obtains the product's existing unit cost. It opens or joins a transaction and loads the quantities of the warehouses in scope. For a tracked item it checks the product/lot master and its dates. A new lot master uses a unique product/lot key. For a withdrawal with `STOCK_DISALLOW_NEGATIVE_TRANSFER` enabled, the quantity test uses the previously loaded warehouse or lot balance.
2. It inserts the signed movement and reads the current warehouse-balance row. An existing row receives the absolute sum of its read quantity and the requested change. If no row was found, the operation inserts the balance for that product and warehouse.
3. For tracked stock it finds the lot detail by warehouse-balance ID and lot number, or fetches the supplied detail ID. It adds the change to the value read. A zero result deletes the detail. A new detail uses a unique warehouse-balance/lot key. The normal warehouse cleanup can subsequently remove a zero warehouse row with no lot children.
4. It writes the product cost calculated from its saved inputs and refreshes cached product stock from the sum of the warehouse rows. A priced receipt with positive opening cost uses `(opening quantity × opening unit cost + received quantity × receipt unit cost) / closing quantity`. A withdrawal retains the loaded cost. For a serialised receipt, a final sum across warehouse details must not exceed one. Movement, warehouse, lot and product updates belong to the outer transaction.

The transaction boundary for a direct movement begins after the initial product lookup. A document operation may already own an outer transaction. A database write lock can order changes to a row while leaving the two callers' earlier read values unchanged.

## Two receipts into existing stock

Opening stock is ten at unit cost 2. A receives three at 5. B receives four at 8. The correct closing quantity after both receipts is 17 and its value basis is `20 + 15 + 32 = 67`, giving average cost 3.94118. Two PHP processes called the public receipt method with separate database connections. Each reached its warehouse quantity read before A committed. B then resumed using its earlier read. The fixture retained zero-balance rows and used no extension subscribers.

| Executed case | Committed movement rows | Warehouse quantity / cached product quantity | Average unit cost |
| --- | --- | --- | ---: |
| Repeatable read, conflict check off | +3 and +4 | 14 / 14 | 3.71429 |
| Read committed | +3 and +4 | 14 / 14 | 3.71429 |
| Repeatable read, conflict check on | +3. B receives a changed-row conflict and rolls back. | 13 / 13 | 2.69231 |
| B starts a fresh transaction after that rollback | +3 and +4 | 17 / 17 | 3.94118 |

With conflict checking enabled, B's movement object had already received a new movement ID when the warehouse update failed. The receipt returned `-6`. A separate connection found only A's movement. A movement ID in memory therefore does not prove a commit. In both runs that left quantity 14, both receipt calls returned positive IDs and both movement rows were visible afterward.
| Serializable conflict followed by a fresh retry of the rejected request | Both movements, once each | 17 / 17 | 3.94118 |

In the first two cases B writes `10 + 4`; both movements survive. Its cost is `(20 + 32) / 14`. Recalculating the product cache from the warehouse rows simply copies the already incorrect balance. Reconcile **opening quantity plus signed movement sum** against both warehouse and item totals.

Two warehouses can isolate the warehouse quantities while sharing the product cost. With ten units at each warehouse and a product-wide opening cost of 2, the same receipts lead to warehouse balances of 13 and 14. Under read committed or repeatable read with conflict checking off, the product quantity reached 27, but B's saved cost was 3.00000 from `(40 + 32) / 24`. The value basis for both receipts is 87, so the reconciled cost is 3.22222. With conflict checking on under repeatable read, B rolled back and a fresh run produced 3.22222.

There is a further timing distinction even with conflict checking on. In a direct movement, B can load unit cost 2 before A commits and open its own transaction afterward. B then reads quantity 13 in the new transaction and writes the stale-cost calculation `(13 × 2 + 4 × 8) / 17 = 3.41176`. Both movements and all 17 units survived in this case. A check of quantity alone cannot detect this valuation difference.

## First warehouse row, lot detail and lot master

A shared product/warehouse balance, a product/lot master and a warehouse-specific lot balance are three different unique keys. The point at which the conflict occurs determines which attempt must reread its inputs.

| Starting state and overlapping requests | Observed result |
| --- | --- |
| First balance for a warehouse, +3 and +4 | A registered +3. B's stale insert or write failed under all three read modes. Its provisional movement rolled back. Retrying from a fresh transaction produced one balance of 7, two movements and average cost 6.71429. |
| Product/lot master already exists; selected warehouse contains 10 units, with no detail for the selected lot, then +3 and +4 to that lot | Repeatable read rolled B back on a duplicate detail or changed row. Fresh execution reached warehouse 17, lot 7. Under read committed B saw the detail created by A and advanced it to 7, while its warehouse assignment still wrote 14. The opening ten units were outside the selected lot in this fixture. |
| Product/lot master absent; both requests select the same new lot | One master insert succeeded. The competing insert failed its unique key, before the second movement was posted. A fresh request found the existing master, checked any supplied dates and posted the second receipt. |

## Negative-stock and serial controls

Two dispatches of seven units each began from ten units in one warehouse, all in one lot. In both transactions the negative-stock guard initially saw sufficient stock.

| Isolation | Durable inventory after the competing operations |
| --- | --- |
| Repeatable read, conflict check on | One withdrawal of 7 committed. B rolled back on a changed row. The new attempt saw 3 available and failed the quantity check. |
| Repeatable read, conflict check off | Both movements of −7 committed. Warehouse and lot each showed 3. The signed movement history implied −4. |
| Read committed | Both movements of −7 committed. The warehouse showed 3. B's later lot lookup saw A's 3, so the detail became −4. |

For a serialised item, the master identifies the serial across warehouses, while each warehouse has its own quantity row. With an existing serial master, two receipts of one unit each into different empty warehouse rows gave another distinction. Under read committed B saw the two units at its final serial check and rolled back. Under repeatable read with conflict checking on, B's product update failed; on retry the serial check rejected the second unit. With conflict checking off under repeatable read, each transaction saw only its own new serial detail and both committed. The durable result was two units of the same serial in two warehouses. An inquiry must aggregate that serial's quantities across all warehouses.

## Retry and reconciliation

After a confirmed rollback, a fresh request can reread cost, availability, the warehouse key and the lot key. After an unknown commit outcome, inspect movements by product, warehouse, originating document or line, quantity, lot, and the actual business event before reissuing it. The movement origin and inventory code are trace identifiers. A sequential test submitted the same +3 twice, including the same origin, after each prior transaction committed. Both movements survived and an opening 10 became 16. Some document entry points provide a separate state guard. Check that specific document and its posted movements before repeating a movement.

[Posting and correction modes](../production-control/posting-modes.md) · [Lot and serial reconciliation](../production-control/lot-reconciliation.md) · [Execution conditions](README.md)
