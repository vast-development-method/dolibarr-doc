# From a bill of materials to stock movements

A bill of materials (BOM) describes the quantities for one reference batch. A manufacturing order (MO) records the quantities intended for a particular run. Each posting records what actually happened. To answer “how many are still needed?”, compare the signed actuals with their own planned line. Product identity alone cannot distinguish two lines for the same component.

Bills of materials (650), manufacturing (660) and workstations (690) are available as standard modules. Enabling manufacturing requires BOM, which requires products. Workstations depend on manufacturing. The stock and batch settings determine which physical movements can be recorded.

## Records and ownership

| Record | Business identity and relationships | Lifecycle or ownership |
| --- | --- | --- |
| BOM | Entity, reference, label, product, reference batch quantity, manufacturing/disassembly type, ordered component or service lines | Draft (0), enabled (1), disabled (9). Adding component lines requires draft. The MO form's recipe selector offers enabled BOMs. |
| BOM line | Product/service, quantity, unit, efficiency, fixed-quantity flag, stock-change flag, optional child BOM and default workstation | Belongs to one BOM. Position orders rows. Fixed and stock-change flags express different decisions. |
| Manufacturing order | Main product, requested quantity, optional BOM, output warehouse, third party, project, planned dates | Creating with a BOM adopts its type and builds the planned lines in the creation transaction. Replacing provisional reference on validation records the validating user and date. |
| Production line | MO, product, quantity, role, optional warehouse, unit, lot, originating BOM line, originating planned row and stock movement | Planned roles are `toconsume` and `toproduce`. Actual roles are `consumed` and `produced`. An actual can link both to its plan and to one stock movement. One plan can have many actuals. |
| Workstation | Reference, operator and machine hourly estimates, associated user groups and resources | A service line can use the station estimates for BOM costing. This associates resources with a station, without asserting any capacity reservation during MO validation. |

## Plan quantities and cost a batch

For a variable component, planned quantity = component quantity × requested MO quantity ÷ BOM batch quantity ÷ efficiency. An empty efficiency falls back to 1 during expansion. A fixed component uses its BOM line quantity once, independent of the requested quantity and efficiency. Component plans with a nonpositive quantity after normalization are rejected. A child BOM is recursively expanded unless the order selects that line to stay unexpanded. Each child applies its own reference batch quantity. Consumption component rows start without a warehouse. Output component rows take the production warehouse. A disassembly BOM reverses the ordinary roles so the main product is consumed and its component products are produced.

For material cost, use the component's cost price when it is defined, otherwise its weighted-average price. If that result is zero, try the minimum supplier price and its applicable discount, otherwise use zero. A material contributes unit cost × recipe quantity ÷ efficiency. A component backed by a child BOM uses the child's calculated unit cost. A service with a workstation contributes duration in hours × (estimated operator rate + estimated machine rate). Without a workstation, a service with a usable default duration contributes (line hours ÷ service hours per unit) × service unit cost. The fallback uses quantity × service unit cost. The calculator rounds the summed batch cost with total-price precision, then the unit cost for a positive batch with unit-price precision. A cost-calculation extension hook may supply a different result.

**Worked batch.** A BOM makes 4 units from 6 kg of material at 75% efficiency. At 10 per kg the reference batch costs 80 in material. Add a fixed, single-use insert costing 3 (efficiency 1) and 30 minutes at a workstation costing 24 per hour. The estimated batch cost is 95 and the unit cost is 23.75. An order for 12 units plans 24 kg, one insert and 90 minutes of variable service. Multiplying 95 by three would charge three inserts. The BOM's per-unit estimate and a run's actual usage therefore answer different questions. On posting a positive stock receipt the transaction uses the production unit price supplied for that receipt.

## Post, close and correct

| Operation | Preconditions | Durable outcome and observable failure |
| --- | --- | --- |
| Create order | Manufacturing write permission on the API. When kits are enabled and their use in BOM/MO is disabled, the main product must pass the kit check. | Returns the order ID. Header and initial planned lines commit together. A failure creating a planned line rolls the order back. |
| Validate | Manufacturing write and access to the target order on the validation API. | Allocates a definitive reference if required and raises `MRP_MO_VALIDATE`. The API returns the refreshed object. A repeat validation of an already validated order returns 304. No consumption or receipt is posted by validation. |
| Post a partial run | A validated (1) or in-progress (2) order, manufacturing write access, selected planned lines. Provide a stock location for physical movement. | A positive consumption issues stock, a positive output receives stock. The actual row links to the selected planned row. Stock-disabled lines can record work without a movement. |
| Auto-close | Sum signed actuals per planned line and role. Every input and every output must meet or exceed its respective target. | Full coverage gives produced (3). A shortfall on even one line, or disabling auto-close, gives in-progress (2). |
| Reset, cancel or reopen | Draft reset is refused once consumed/produced rows exist. Cancellation accepts validated or in-progress. Reopening accepts produced or canceled (9). | Cancel may preserve actuals or explicitly reverse stock and remove actual rows. A reversal failure rolls back the cancel. Reopening returns to validated, and does not itself replay production. |

**Integration contract.** The normalized [posting schema](../../schemas/operations/production.schema.json) models the operation “apply signed actuals to existing planned lines”. The partial production endpoint is `POST /mos/{id}/produceandconsume` under the API base. Map `movementLabel` and `movementCode` to `inventorylabel` and `inventorycode`, and partition the rows into `arraytoconsume` and `arraytoproduce`. Here `objectid` is the **planned line ID**. The separate `produceandconsumeall` endpoint has an explicit-array branch that interprets `objectid` as a **product ID**. Use the correct operation-specific mapping. The partial endpoint returns the MO ID, reports 403 for insufficient rights, 404 for a missing order and 405 for an ineligible state. Missing movement labels/codes and unsupported tracked products produce 500 in this release. Tracked runs can instead be entered on the production screen with a warehouse and lot/serial value. The normalized contract encodes warehouse presence for physical postings and excludes zero-quantity postings. A consumer must resolve each plan's MO, role and stock policy from stored data before applying the command.

**Retry behavior.** Posting adds actual rows. The movement code is a descriptive grouping value. The partial endpoint has no request-key lookup in its posting loop. After an ambiguous response, compare linked actuals and stock movements with the intended posting before resubmitting. The operator screen explicitly rolls back its transaction when a row fails.

## Acceptance cases

| Given | When | Expected observation |
| --- | --- | --- |
| An order needs 24 kg in and 12 finished units out | Post 24 kg and 8 units with auto-close | There are two linked actuals. Raw stock falls by 24, finished stock rises by 8. The MO stays in progress. An additional 4 units can close it if every other planned line is satisfied. |
| Two planned lines use the same product in quantities 2 and 4 | Post 6 against the first line alone | The second line still has an unmet quantity of 4. |
| A physical component is lot-managed | Post with the partial REST operation | The operation reports the unsupported tracked product. Through the production screen, a required but missing lot produces an error and rolls the transaction back. |
| A disassembly order consumes one assembled unit and yields two component units | Post both as positive quantities | Stock of the assembled product falls by one and component stock rises by two. |
| A non-stock-changing line is posted | Inspect the actual and the stock ledger | The actual references the plan. Its stock-movement link is empty. |
| A partial run already recorded physical outputs | Attempt a draft reset, then cancel with reversal on an eligible order | Reset fails. With sufficient stock to reverse the outputs, the cancellation restores the related quantities and removes those actual rows. |

[Accepted normalized posting](../../examples/operations/production--partial.json)

Follow a [production plan through stock posting and costing](../production-control/README.md) to reconcile material issues, receipts, lots and the unit value used on each movement.
