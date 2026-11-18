# Production control

Follow a manufacturing order from its recipe to the physical and financial evidence left by the workshop. The component list, saved work order, posted actuals and warehouse journal each answer a different question.

| Decision | Where to look |
| --- | --- |
| Which recipe and revision of the component list were used for this job? What survives a recipe edit, a quantity change or a child order? | [Recipe selection and plan changes](recipe-and-plan.md) |
| Which unit price will the recipe, workshop screen or posting service use? What happens to the finished item's average cost? | [From batch estimate to inventory value](production-cost.md) |
| Which rows does a partial post, a bulk post or a correction write? What can safely be inferred after a retry? | [Posting modes and completion](posting-modes.md) |
| Which input lots and output serials were recorded together? Can an inquiry establish a component's presence in a particular serial? | [Tracing a job across stock and lots](lot-reconciliation.md) |

The [production dictionary](../records/production.md) and [warehouse dictionary](../records/warehouse.md) give the stored field types and nullability. The [manufacturing correction guide](../warehouse-corrections/manufacturing-actuals.md) follows a full cancellation after some output has shipped. The [worked purchasing and production journey](../journeys/building-against-a-shortage.md) follows a material shortage back to purchasing.
