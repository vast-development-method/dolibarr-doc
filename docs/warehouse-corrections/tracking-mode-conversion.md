# Change tracking mode for an item already in stock

A catalogue change from untracked goods to lot-tracked goods changes how the next pick is identified. Existing stock must be reconciled to the new identity at each warehouse. A switch between lot and serial tracking has different effects again. The sale price, moving-average price, old commercial line numbers and actual manufacturer serials are separate facts.

## Preserve the prior settings

The product card captures the previous product before applying the edit. For an edit that omits the tracking-mode input entirely, the card retains the previous mode. It likewise retains omitted expiry requirements and numbering-mask values. This allows a form changing another part of the product to preserve its tracking configuration. When batch handling and stock are enabled, choosing tracking on a product edited as non-stock-managed causes the edit form to turn stock management on and display a warning. Initial creation contains its own admission rule for that combination.

The product update determines the direction of conversion from the previous and proposed **has-tracking** values. Its fallback clones the current product where a usable prior product object is unavailable. A caller that supplies only the final mode and fails to supply the effective previous value cannot expect the same transition detection as the edit card. Moving from one tracked mode to another is different from crossing the tracked/untracked boundary.

## Introduce tracking

The update loads warehouse positions and their active lot details. For each warehouse with a stock row:

1. Sum quantities on existing individual lot positions, excluding any existing default/unidentified lot rows encountered. The configured default comes from `STOCK_DEFAULT_BATCH`, with `000000` as the fallback. The cleanup recognises the historic unidentified label as well as the current default.
2. Compare this sum with the physical warehouse balance. When they differ, create a default lot position for the signed difference. A warehouse in balance needs no residual position.
3. For a newly created residual position, look up the product/default lot master. If it is absent, create a master with the product, entity, creating user and default identifier. A failure creating the position or master is an error in the product update.

The conversion establishes identities for existing warehouse quantities. Its allocation path writes lot positions and, where needed, the master directly. It does not create a supplier receipt or purchase, and this allocation itself records no acquisition price. The default label on 40 previously untracked units records an unassigned traceability balance. It cannot identify the 40 manufacturer's serial numbers. Per-lot labeling and the individual-serial stock admission rule are distinct from assigning a default residual position.

Suppose East holds 12 units and its existing named lots account for four under N1 and three under N2. West holds five units with no named splits. Enabling lot tracking creates default balances of five in East and five in West, using the same product-level default lot master. East now reconciles as `4 + 3 + 5 = 12`. West reconciles as `5 = 5`. If the named positions instead total 14 against East's warehouse balance of 12, the arithmetic residual is −2 in this branch. The conversion does not silently reduce one of the named lots to make it balance.

## Remove tracking or change to serial tracking

When switching from a tracked to an untracked product, the update reads its lot positions together with their warehouses. For each positive split it removes that quantity from the named lot and adds the same quantity to untracked stock at the same warehouse. For a negative split it performs the opposite pair. The first operation explicitly directs the writer to update the batch position even though the product now has its untracked mode. Both calls carry the same generated operation code, zero price and the warehouse from the selected position. The effects pass through the stock movement writer with its normal stock and component policies. The lot master and earlier journal rows are independently retained records.

For an ordinary stock-managed item with lot A=4 and B=3, removing tracking makes two separate pairs of entries. Their signed sum is zero. After success the warehouse still holds seven and the lot positions have been cleared. Counting only positive journal entries for the conversion would falsely report a new seven-unit receipt. A product-level query against old movements can continue to identify A and B after there are no current positions to pick from.

Changing a tracked product from lot to serial mode crosses neither boundary above. On the product card the new mode elicits a warning that units can already share a batch. The conversion branch does not split an existing five-unit lot into five new serial identifiers. Subsequent positive serial movements run the ordinary product/serial quantity rule. A blueprint needs to keep the operator's change in policy separate from any individually substantiated reassignment of historical identifiers.

[Lot identity and expiry](../specification/operations/lot-identity-and-traceability.md) · [Warehouse record dictionary](../records/warehouse.md)
