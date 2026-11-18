# Stock balances, valuation, counts and transfers

The warehouse balance answers “how many are here?” The movement records explain when, why and by whom it changed. The product's weighted average unit cost values incoming stock across warehouses. A purchase order, an invoice and a stock movement can therefore carry different quantities or costs at a particular moment. [Stock module guide](../reference/locators/supply.md#ref-12c0ebbd93ce) · [Movement implementation](../reference/locators/supply.md#ref-4cbd3be8da64)

| Grain | Stable identity | Stored facts |
| --- | --- | --- |
| Warehouse balance | Product × warehouse | On-hand quantity. The product-level cached stock is recalculated from warehouse balances. |
| Lot master | Product × batch identifier | Lot-wide sell-by and eat-by dates. The same lot can be held in several warehouses. |
| Lot balance | Warehouse balance × batch identifier | Quantity in this warehouse for this lot. |
| Stock movement | Movement ID | Product, warehouse, signed quantity, date, type, unit price, actor, optional lot, label, inventory code and originating document. |
| Count detail | Inventory, product, warehouse, optional batch | Starting stock, observed quantity, optional valuation, ID of resulting correction movement. |

[Warehouse balance key](../reference/locators/supply.md#ref-24bb0b7813e3) · [Lot master key](../reference/locators/supply.md#ref-6384e485e80f) · [Lot balance key](../reference/locators/supply.md#ref-1ebdca973b1b) · [Movement record](../reference/locators/supply.md#ref-e1b7f4e6000d) · [Count detail](../reference/locators/supply.md#ref-fdb0c9b9903c)

## Post one movement

A stock-managed product and a warehouse identify the balance. Input types 0 and 3 increase stock. Output types 1 and 2 are used with negative quantities. The REST creation route normalises a positive quantity submitted with type 1 or 2 to incoming type 0 or 3 respectively. It requires stock-create permission, rejects zero and returns the movement ID on success. A service call supplying a quantity of zero or failing to create a movement gets HTTP 503 at this route. [Stock movement API](../reference/locators/supply.md#ref-2576bb1d5605)

The movement transaction creates the ledger record, updates the warehouse balance and lot detail, and recalculates product-level quantity and cost. With batch tracking active, an incoming tracked item needs a batch. For an existing lot, an omitted date can use its established value and conflicting supplied dates fail. An outgoing quantity uses the lot's current dates. With negative transfers disallowed, the routine checks available stock for the warehouse or tracked lot. A downstream error can roll back the database changes. [Batch and quantity checks](../reference/locators/supply.md#ref-3cc8aa58cbe5) · [Write sequence](../reference/locators/supply.md#ref-1e0e65445cd0)

### Weighted average cost

For a priced receipt let **Q** be the previous physical quantity across visible warehouses, **C** the previous average unit cost, **q** the receipt quantity and **c** the incoming unit price. Use Q₀ = max(Q, 0). For positive C and a nonzero denominator, the new average is **(Q₀ × C + q × c) / (Q₀ + q)**, rounded at unit-price precision. Otherwise the incoming price becomes the average. An outbound movement preserves the average. A zero-priced input normally preserves it too. The zero-price override applies specifically to supplier order and supplier invoice origins. The standalone reception document has its own origin type. [Quantity scope](../reference/locators/supply.md#ref-17906fc487ce) · [Average-cost calculation](../reference/locators/supply.md#ref-85f39ac671cd)

| Given | When | Expected |
| --- | --- | --- |
| 8 units in warehouse A and 2 in B, current average 10 | Receive 5 at 16 into B | B has 7, the product has 15, average cost is 12, inventory value at average cost is 180. |
| 15 at average 12 | Issue 4 from B | B has 3, product has 11, average remains 12 and value is 132. |
| Product stock is −2 with recorded average 9 | Receive 5 at 11 | Net quantity becomes 3. The average uses zero prior units and becomes 11. |
| Lot L7 in two warehouses has one recorded expiry date | Submit an inbound lot with a different expiry date | The movement fails and neither warehouse gains stock. |

## Projected stock and replenishment

With receipt-based and shipment-based posting, the projection starts from physical stock. Add remaining purchase demand on the supplier (eligible order quantities minus already received quantities), subtract remaining customer demand (eligible sales quantities minus shipped quantities), and add active manufacturing quantities to produce less quantities to consume. Default supplier order statuses for the order term are sent and partially received. Shipment and reception cut-offs depend on the selected posting event. Invoice- and order-based posting have separate branches. The projection measures future availability and creates no warehouse entries. [Virtual-stock calculation and filters](../reference/locators/supply.md#ref-f85fddda7c3a)

For example, 11 physically held, 20 on eligible purchase orders with 5 received, 8 on eligible sales orders with 2 shipped, and 3 to make with 1 to consume give **11 + 15 − 6 + 2 = 22**. The replenishment screen computes a target from the larger of desired and alert stock. In physical mode it suggests max(target − physical − already ordered, 0). In virtual mode it suggests max(target − virtual, 0). A purchaser can edit the suggested quantity and select a supplier offer. [Replenishment quantities](../reference/locators/supply.md#ref-58a3f6a8dc24) · [Order selection](../reference/locators/supply.md#ref-6ae2f28bb3b5)

## Stocktaking and inter-warehouse transfer

Validating a draft inventory creates count lines from existing stock according to the product, warehouse, category and optional child-warehouse selection. The initial quantity is the lot quantity for a batch line. Recording the count reads physical stock again. A null observed quantity is skipped and zero means the counter saw none. The correction equals observed quantity minus the current warehouse/lot quantity at recording. If a count starts at 10, an issue leaves 8 and the observer enters 7, the movement is **−1**. Matching quantities create no correction. In normal permission mode the inventory page uses stock-movement-create for posting corrections. In advanced mode it uses inventory write. A nonempty actual unit cost can also replace the product average when actual-cost management is enabled. [Count generation](../reference/locators/supply.md#ref-f0ecee895945) · [Post a count](../reference/locators/supply.md#ref-9c78d5026431)

The transfer document has draft, validated, transferred and closed stages. Dispatch takes stock from the source. Receipt adds it to the destination. With 10 in A and 2 in B, dispatching 3 shows A = 7 and B = 2 until the destination confirms. Once confirmed B = 5. Each action groups its line movements in a transaction and commits them before updating the transfer header status and its date. If posting stops between those writes, the warehouse balances and the displayed transfer state can disagree. Reconcile the movements already posted against the transfer lines before retrying. The document provides reversal actions for the applicable state. [Transfer states](../reference/locators/supply.md#ref-1382036963f6) · [Transfer operations](../reference/locators/supply.md#ref-e3c62bac4fc1)
