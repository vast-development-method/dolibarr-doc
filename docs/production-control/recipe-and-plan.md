# Recipe selection and plan changes

A planner chooses a recipe for the order and can choose a different treatment for each subassembly. Someone investigating an old job must therefore recover the saved order lines before consulting the item's current default recipe.

## Four distinct references

| Field or pair | Meaning | How the value is used |
| --- | --- | --- |
| `product.fk_default_bom` | Catalogue preference for an item | Can be changed on the product. It identifies one recipe among those that can produce the same item. |
| `mrp_mo.fk_bom` | Recipe selected for this order | Creation uses this recipe's `bomtype` as the order's `mrptype`. Type 0 makes the header item an output. Type 1 makes it an input for dismantling. |
| `bom_bomline.fk_bom_child` | Specific recipe selected for one component occurrence | The selected child supplies its own reference batch quantity and lines when the planner expands that component. Choosing a separately manufactured child leaves that component on the parent plan. |
| `mrp_production.origin_type`, `origin_id` | Origin of a generated or manually added plan line | An expanded leaf carries `bomline` and the source leaf's row ID. A manually added line carries `free`. The header-product line is created directly from the order. |

A recipe line belongs to its recipe through `fk_bom`. Its product and child recipe are separate references. When the operator chooses a child recipe on the entry form, the form derives the component product from that child's header. It rejects the parent recipe's own product as a component. For a nested recipe it follows incoming child-recipe references upwards and rejects a selected child already present among the current recipe's ancestors. Adding a plain component selects its product directly. Omitting the unit takes the component's unit. A service can take the selected workstation or, when none was selected, its product's default workstation.

New lines with an unspecified position are appended after the current maximum. Insertion at an existing rank increments the positions at or after that rank. Moving an existing line shifts the intervening positions. Editing a line updates its quantity, efficiency, frozen and stock-change flags. A supplied nonempty unit replaces the prior unit. Submitted additional-field values replace the corresponding keys. The line editor preserves the associated product and child recipe. A replacement component therefore needs its own decision about lineage.

The recipe card allows writers to validate a draft once it contains a line. Validation assigns the final reference when provisional, stores the validating user and time and sets status 1. The card offers manufacturing-order creation against an enabled recipe to a manufacturing writer. Disabling that recipe sets status 9. Reopening restores enabled status. Returning an enabled recipe to draft allows another edit. Existing saved order positions retain their values. A recipe row ID and an enabled state do not constitute a permanent version history of its quantities or costs.

## Nested quantities and ancestry

For each recipe occurrence combine order demand with that recipe's base quantity. A variable component with line quantity `q`, local demand `d`, recipe base `b` and line efficiency `e` requires `q × d ÷ b ÷ e`. An empty line efficiency gives divisor one during plan expansion. A frozen line takes its literal `q`. The recipe header's own efficiency is not another divisor in this expansion. A leaf is rounded at quantity precision before insertion and must be positive. When a component is expanded inline, its computed requirement becomes the incoming demand at the child's recipe. The outer role is retained for the leaves.

A base recipe for two panel sets calls for three frame modules. A frame recipe yields two frames from eight rails. An order for four sets needs six frames. The inline plan has a 24-rail input. If the same frame recipe is referenced by two different parent branches, two leaf occurrences can carry the same `origin_id` and product. Each saved plan line has a separate `rowid`; that ID determines which balance a subsequent actual satisfies. The leaf does not store the entire path of intermediate recipe occurrences.

If the job instead requests an independent frame order, the parent has a six-frame input and the child a 24-rail input and six-frame output. The child header's `fk_parent_line` refers to the parent planned frame line. To retrieve its parent order, read that line's `fk_mo`. To retrieve children, select order headers with `fk_parent_line` among the parent's plan-line IDs. The order-to-order document link is an additional navigation path. Completing the child's six-frame receipt gives the parent material it may issue. Posting the parent consumption still requires its own warehouse transaction.

## Draft quantity edits and saved history

Consider a draft order with header quantity four. Its saved main output was independently edited down to three, a free variable material line holds ten, and a frozen setup line holds two. The operator changes the header quantity to eight on the production tab.

1. The order update scales each unfrozen saved planned quantity by `8 ÷ 4`. The material becomes 20, setup stays two and the temporarily scaled main output is six.
2. The production tab reloads the lines. For every unfrozen `toproduce` line of the header product it aligns the saved quantity with the new header quantity. The main line becomes eight. A different product or frozen line keeps its result from the first step.
3. In a dismantling order the main item's role is `toconsume`, so this extra output alignment does not apply. A free additional output for the same header product that satisfies the exact predicate is also subject to alignment.

This correction belongs to that tab's draft quantity command. Proportional rescaling in the underlying order update uses the saved line quantities and the old nonzero header quantity. Regeneration instead rebuilds the entire plan and discards existing free plan positions. It requires a draft with no consumed or produced rows. A change to the catalogue default, a recipe edit and a draft regeneration can consequently yield three different histories for the same product. For an issued order, use the saved plan, actual and stock movement identities to explain the transaction.
