# Building four control units after a count finds a shortage

A customer project needs four control units for a site installation. The workshop will build them. Each unit consumes three identical fittings. Purchasing owns the supplier order, receiving owns the warehouse allocations, the storekeeper owns the count and the production team posts the job's actuals. They reconcile the same twelve fittings at different moments.

## Opening position

The single workshop warehouse holds eight untracked fittings at a product average cost of 2.50, with a carrying value of 20. It has no finished control units. There are no outstanding supplier orders. Finished units and fittings are stock-managed, negative stock is disallowed and purchase receipts move stock on validation. For clarity, the figures use one currency with no tax, freight, labor or overhead. Output receipts use the specified unit prices below. The fitting's desired physical stock is twelve and the lower alert threshold does not change that target.

The planner creates a job linked to the customer project and validates it. Its recipe base is one output, with three unfrozen fittings at efficiency one. The job consequently has a planned input of twelve and a planned output of four. Its planned quantities move no physical stock. If the operator attempts the full issue now, twelve exceeds the eight available, so the movement fails. The posting transaction leaves both the warehouse and the manufacturing actuals at their opening values.

## Purchasing, receiving and counting

| Event | Raw stock after event | What the next team can use |
| --- | ---: | --- |
| Buyer reviews physical replenishment | 8 | Target 12 less physical 8 less open purchases 0 gives a suggestion of 4. The buyer selects an eligible supplier offer at 4 per fitting. A draft purchase for 16 exists. |
| Supplier order approved and sent | 8 | The supplier order now identifies four ordered units. The receiving quantity is still zero. A rerun in physical mode accounts for the four outstanding, giving a suggestion of zero. |
| Receiver validates four fittings into the workshop at 4 each | 12 | Four received are linked to the supplier order line. Opening value 20 plus receipt value 16 yields an average cost of `36 ÷ 12 = 3` per fitting. |
| Storekeeper starts a stocktake and counts eleven | 12 until posting | The count contains a comparison quantity of twelve and an observation of eleven. The observation by itself leaves production availability at twelve. |
| Storekeeper posts the count with no cost override | 11 | Live stock is twelve, so the count posts an issue of one. The correction references the count. The supplier still delivered four and the manufacturing job still requires twelve. |

No one changes the supplier receipt to three or reports a twelfth fitting as consumed. A valid purchase receipt and a subsequently discovered loss are different events. The inventory correction makes that distinction observable. Purchasing and receiving can trace the 16 of supplies, while the storekeeper can explain the loss of one unit valued at 3.

The supplier draft flow is described in [Replenishment and supplier drafts](../specification/operations/replenishment-and-supplier-drafts.md). Receipt allocation and comparison rules are in [Partial supplier receipts](../specification/operations/receipts-allocations-and-order-completion.md). The count's live comparison rule is in [Counting and transferring stock](../specification/operations/stocktake-and-transfer.md).

## Finishing the job in two postings

1. Production issues nine fittings and records three finished units at a supplied output price of 9 per unit. Raw stock falls from eleven to two. Finished stock becomes three with value 27. With automatic completion requested, the job stays in progress. Its remaining planned quantities are three fittings to consume and one unit to produce. The **physical shortage for this job is one**, since two fittings remain on hand.
2. The warehouse planner still has a general stock target of twelve. With physical stock two and no open purchases, its displayed suggestion is ten. The buyer orders four at 4.50, the eligible supplier minimum for this second purchase. The buyer's override covers this job and leaves spare material. The job's shortage, the company stock suggestion and the submitted purchase quantity are three different numbers.
3. Receiving validates four at 4.50. The two carried fittings were worth 6. The receipt adds 18. Six fittings now have a product average of `24 ÷ 6 = 4`. The order and receipt provide an explanation for the higher replacement cost of the last production batch.
4. Production issues the remaining three planned fittings and records its last finished unit at a supplied output price of 12. Raw stock ends at three fittings valued at 12. Finished stock ends at four units with value `27 + 12 = 39` and average `39 ÷ 4 = 9.75`. Each plan line's linked actuals have reached its quantity. With automatic completion selected the job becomes produced.

The output prices here deliberately match the input value used in each run. The production posting receives its output unit price as an input. A different supplied price would change finished inventory value without altering the twelve fittings issued. The product cost calculation is in [Stock at a date and value](../specification/operations/stock-at-date-and-value.md). Planned and actual lines and their links are in [Nested production orders](../specification/operations/nested-production-orders.md).

## Closing evidence

| Consumer | Reconciled result |
| --- | --- |
| Supplier-order and receipt history | Two orders of four, eight received in total, purchase value 34. Supplier invoice and payment remain separate records if subsequently entered. |
| Storekeeper | `Opening 8 + receipts 8 − count loss 1 − production issues 12 = 3` fittings. Only the count explains the one-unit loss. |
| Production supervisor | Twelve fittings issued over two postings and four completed units received. The four-unit job has two output actuals, quantities three and one. The count's loss creates no manufacturing actual. |
| Project manager | The linked manufacturing order identifies the customer job. Its header does not post 39 of expense or revenue to the project overview. Purchases, invoices, measured labor and eligible stock movements enter project reporting through their own associations and contribution rules. |
| Inventory valuation | `Opening 20 + purchases 34 − count loss 3 = ending raw stock 12 + ending finished stock 39`. Finished units have not yet been shipped, invoiced or collected. |

After an interrupted response to a posting, the supervisor can use the linked actuals, warehouse movements and on-hand stock above to determine which batch committed. Repeating a production posting creates another actual and can change inventory a second time. The same twelve-unit requirement should never be used as evidence that twelve have already moved.
