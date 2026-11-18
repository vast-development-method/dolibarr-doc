# Planning and posting a nested production order

An assembly can be consumed as a finished component from stock or built from its ingredients within the same job. The choice changes which warehouse balances move. A bill of materials identifies the selected child recipe on a specific component line. A separate manufacturing order records whether that subassembly has an independent production job.

## From a recipe to executable lines

| Decision | Effect on planned production |
| --- | --- |
| Manufacturing recipe | The header product is a planned output. Recipe components are planned inputs. |
| Disassembly recipe | The header product is a planned input. Recipe components are planned outputs. |
| No recipe | The order type determines the direction of its header product. Additional planned lines can be entered directly. |
| Component without a linked recipe | Generate one planned line referencing the original recipe line and component. |
| Component with a linked recipe and no separate job | Expand the linked recipe in place. The parent posts its leaf components in the inherited input or output role. |
| Component selected for a child order | Keep the subassembly as a planned line on the parent. Create a child order using that product, its selected recipe and the planned quantity. |

For each recipe level, divide the incoming requested quantity by the recipe's base output quantity. For an ordinary line, multiply that ratio by the component quantity and divide by line efficiency. Empty efficiency uses one. A frozen line takes its literal quantity. Pass the resulting component requirement to the child recipe when expanding it. Write leaf quantities at the configured calculation precision. A nonpositive leaf requirement fails plan creation. The plan copies the leaf's position, unit when present, frozen flag, stock-change setting and default workstation. Planned outputs use the manufacturing order's warehouse. Planned inputs leave the issuing warehouse for execution.

The embedded recipe is the one identified on the line. The existence of another recipe for the same product does not make it an interchangeable substitute at posting time. On the create-with-children action, the parent is written first. Each requested child line is matched by parent order ID, origin kind and exact recipe-line ID. A match creates the child with a link back to that specific planned line and an order-to-order link. An unmatched selection is skipped. The card processes the children individually after creating the parent. A request for several related orders therefore has different persistence behavior from inserting all lines of one plan.

Consider a finished unit requiring two motor modules. The motor recipe yields four modules from twelve bearings. A job for eight finished units needs sixteen modules. Inline expansion yields a parent plan with 48 bearings. Selecting a child order instead yields a parent plan consuming sixteen modules, and a child order for sixteen modules consuming 48 bearings. Posting both parent plans for the same job would count the bearings twice. With a bearing-line efficiency of 0.8, the ordinary planned requirement becomes 60. With a frozen bearing line of twelve, the requirement stays twelve for this expanded recipe occurrence.

## Reading the materials requirement alongside the shop order

The recipe needs view starts with a multiplier of one for the displayed recipe. Its flat view combines leaf quantities under each product. For a linked child recipe, it multiplies by the parent line quantity and divides by the child's base quantity before descending. Its tree view retains the intermediate recipe, parent ID, level and position as well as the product totals at each level. Physical and projected stock appear beside the displayed requirements. Reading this view creates neither an allocation nor a procurement order.

The report and manufacturing order answer different quantity questions. The report applies the ordinary recipe multipliers. Its accumulator does not apply line efficiency or frozen-quantity logic. It adds numbers as entered and retains a leaf unit identifier, with no conversion step in the summation. For example, if the same ingredient occurs twice as 500 grams and once as 1 kilogram across two branches, summing the literals is insufficient to express the material requirement in kilograms. The executable plan is an additional calculation for the selected order size. This matters when comparing a single-recipe report against actual consumption or promising inventory to a customer.

## Plan changes, partial postings and cancellation

Regenerating the plan requires a draft order with no consumed or produced lines. Rebuilding the plan deletes its existing lines before creating the replacement plan within a database transaction. For an ordinary draft quantity edit with a known nonzero old quantity, the update scales each existing unfrozen planned input and output by `new order quantity / old order quantity`. Frozen lines keep their recorded quantity. This proportional edit uses the saved plan quantities, including prior edits. It does not re-read the latest recipe quantities through this path.

Production entry requires manufacturing write permission and an order in validated or in-progress state. Each warehouse or lot split produces a separate actual line. The actual records its order, parent planned line, product, quantity, warehouse, lot, operator and stock movement ID when a movement occurred. A material issue reduces warehouse stock. Finished stock enters the receiving warehouse at the unit value entered on that output split. A posting with no associated warehouse movement can have a null movement link. Services entered as free planned lines use the service's default workstation and disable stock change. A service with a duration unit can seed the planned quantity and time unit from the service record.

For a plan requiring 48 bearings, posting 20 from lot X and 16 from lot Y leaves twelve units against the same planned input. The ledger identifies the lots and warehouse involved in each posting. Closing the work as fully processed depends on the sum of actual quantities against each relevant stockable planned input and output. Posting all required components while producing only seven of eight finished units still leaves a planned output outstanding. The completion comparison accepts an actual total greater than its planned total.

The cancellation command can include reversal of actual inputs and outputs. It uses the actual product, warehouse, lot and quantity of each split. A positive consumption becomes a receipt, a positive output becomes an issue, and negative recorded quantities reverse the opposite way. The resulting movements reference the manufacturing order, are dated at cancellation time and carry zero as the supplied movement price. The order can reverse consumed lines, produced lines or both through the underlying operation. A movement error rolls back that reversal operation, including any associated actual-line deletions requested by its caller. If stock is disabled, the reversal routine returns without creating movements. Simply opening a completed order for further work changes its status to in progress and leaves the earlier actuals available.

Related records include [Planned or actual production position](../../records/production.md#record-mrp_production).
