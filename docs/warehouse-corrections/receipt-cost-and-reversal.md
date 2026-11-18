# Undo a receipt after part of its stock has been used

A receiving clerk can discover that a delivery was booked against the wrong supplier order after the warehouse has already issued some of the goods. Correcting this involves a supplier document, the original warehouse and lot allocations, physical quantities, and the product's current moving-average unit cost. The receipt may own the original stock entry at validation or at closure, depending on the entity's [posting policy](../policies/stock-posting-decisions.md).

## Which action owns the opposite quantity

| Action on a receipt sourced from a purchase order | State written | Stock consequence |
| --- | --- | --- |
| Reopen a closed receipt | Validated and unbilled. The conditional update requires the row still to be closed. | In closure-posting mode, issue the original received quantity from each applicable warehouse/lot allocation. In validation-posting mode, the stock was already owned by validation and reopening alone leaves it in place. |
| Return a validated or closed receipt to draft | Draft. The persisted state must still equal the state observed by the caller. | Validation-posting mode reverses the receipt. Closure-posting mode reverses it only when the previous state was closed. Reopening and then returning the same receipt to draft therefore has one stock reversal under an unchanged policy. |
| Delete a receipt | Remove receipt allocations and their additional fields, relationships and receipt header. | Reverse quantities where the current state and posting policy indicate stock was posted. The issued movement is recorded with zero price and without an origin pointing to the deleted document. |

The reopen and draft paths use a join from each receipt allocation to its originating purchase order line. Each row identifies quantity, warehouse, lot and stored acquisition cost. A zero quantity is skipped. A negative allocation participates when the negative-receipt policy permits it. Issue negates the signed allocation, so reversing a negative receipt adds physical stock. The reopen implementation obtains the product from the receipt allocation. The draft and delete queries obtain it from the originating order line. An allocation without a matching purchase line does not enter these joins. The receipt's document number alone is insufficient to reconstruct the stock effect.

Reopening emits the receipt-reopened event. When the origin is a supplier order, the operation sets that order back to partially received. A movement, event or source-status failure rolls back the transaction. The reopen routine restores the pre-operation state and billed flag on the loaded object on failure. On returning to draft, the source-order adjustment has a narrower branch. For a partially received order it inspects the linked receipts and can return the order to ordered if no linked receipt has a positive state. A document header's status and the physically available stock answer different questions.

Source locations are `htdocs/reception/class/reception.class.php:695–759,1445–1518,2077–2211,2282–2417,2426–2568` and `htdocs/product/stock/class/mouvementstock.class.php:877–907`. The interactive grants for receiving, validating, reopening and deleting are mapped in `htdocs/reception/card.php:175–196,261–277,578–618,743–759`.

## How the cost changes

For an ordinary stock-managed product in a single entity, the movements from a positive receipt use the acquisition cost carried on each allocation. Cost is averaged across the product's included warehouse stock. The writer collects the existing product quantity and average. For an eligible incoming-type movement with a positive price:

1. Treat a negative starting quantity as zero for weighting.
2. If the old average is positive and the weight denominator is nonzero, use `(max(old quantity, 0) × old average + incoming quantity × unit price) / (max(old quantity, 0) + incoming quantity)`. Apply the unit-price precision at each movement.
3. When the old average is unset or nonpositive, or the denominator is zero, use the incoming unit price.

A zero price usually preserves the previous average. A separate setting permits weighted zero-price entries for movements whose origin type is supplier order or supplier invoice. The receipt-document origin has a different type. Ordinary outgoing-type movements preserve the current average even if they carry a stored price. Thus reopening a receipt can issue the exact original quantity at the exact original location and still leave the product with the average established *after* that receipt. A later reclose weights the acquisition cost again against the quantity and average then on hand.

The recorded movement price, the product's average and the value produced by a dated inquiry are distinct. A dated quantity report can apply the current price basis to a reconstructed historical quantity. For a historical reconciliation identify the calculation basis and the time at which each price was read. [Stock at a date and value](../specification/operations/stock-at-date-and-value.md)

Source locations are `htdocs/product/stock/class/mouvementstock.class.php:276–282,342–350,530–565,588–615,653–671` and `htdocs/product/class/product.class.php:6484–6542`.

## Worked receipt with two lots

One warehouse begins with eight units of lot A and two of lot B. The product average is 10. A single supplier receipt adds five units of each lot at 16. Assume stock posts when the receipt closes, no intervening changes in policy, and negative stock is disallowed.

| Event | A | B | Total | Product average | On-hand at current average |
| --- | ---: | ---: | ---: | ---: | ---: |
| Opening | 8 | 2 | 10 | 10 | 100 |
| Closed receipt, A and B each gain five | 13 | 7 | 20 | 13 | 260 |
| Issue four units of B | 13 | 3 | 16 | 13 | 208 |
| Attempt to reopen the receipt | 13 | 3 | 16 | 13 | 208 |
| Four units of B are physically returned at zero entry price | 13 | 7 | 20 | 13 | 260 |
| Reopen the receipt successfully | 8 | 2 | 10 | 13 | 130 |
| Close the corrected receipt again with unchanged lines and prices | 13 | 7 | 20 | 14.50 | 290 |

The unsuccessful reopen needs five units in B and finds three. A's surplus does not cover B. Even if A's compensation ran first, the enclosing transaction rolls it back and leaves the receipt closed. Once the four units of B return, reopening succeeds. The ten units remaining then have the original physical distribution and a current value of 130. A close against the restored quantity weights ten units at 13 with ten at 16. The scenario uses rates with exact intermediate values at ordinary unit-price precision.

If the business intends to correct only a mistaken supplier receipt, a movement-list reversal and a receipt reopen are independent operations. Posting both can remove the same quantity twice. Where the document has to return to a prior state, reconciliation must follow the operation that also owns that state. [Movement-list compensation](movement-journal-and-counts.md)

The [lot-level projection](../../schemas/supply/lot-receipt-reversal.schema.json) and [worked correction](../../examples/supply/lot-receipt-reversal.json) retain the average alongside the lot positions at each step, including the failed reopen.
