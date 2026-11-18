# Customer prices, quantity breaks and price floors

A price enquiry resolves a product, a selling party, a buying party and optionally a selected quantity-price record. It returns a unit quotation and a floor, each in net and gross terms, the entry basis and applicable tax information. The document editor applies the line discount and extends the price by quantity. A dated negotiated price, a buyer's price level and a quantity break are distinct records.

## Resolving the selling price

The standard resolver begins with the catalogue's net price, gross price, minimums and entry basis. An empty basis means net. It obtains default VAT treatment from seller, buyer and product, and clears the recoverable-only indicator when there is no rate. A price extension can supply the result before the standard selection proceeds. The resolver chooses one configured branch in the following order.

| Pricing arrangement | Selection and fallback |
| --- | --- |
| Individual agreement plus price levels | Search this buyer's prices for this product, latest starting date first. Take the first record whose start is on or before today's comparison date and whose end is empty or on or after it. If none qualifies, use the buyer's assigned level when present. Without either, keep the catalogue values. |
| Price levels | With an assigned buyer level, use its net, gross, corresponding minima and basis. Missing entries for that assigned level default to zero and net basis. An unassigned level leaves the catalogue starting values available to the subsequent applicable branch. |
| Individual agreement only | Use the same buyer, product and date selection. A qualifying row supplies prices, minima, basis, VAT, optional VAT code and recoverable-only treatment. If the search yields no current agreement, keep the standard product price. |
| Quantity pricing | Look up the supplied **row identifier** in the product's ordinary quantity-price list. A match changes the net or gross unit amount according to the matched row's own basis. No match leaves the original values. |
| Quantity pricing within levels | Start with the buyer's level values when assigned. Search the selected quantity row only within that level. No selection uses the level price. A row belonging to another level cannot override it. |

For both quantity arrangements the lookup compares the argument with a break's identifier. Sending the number of units as that argument can select an unrelated record with the same identifier. The resolver writes the matched amount on one basis and leaves the other unit amount and minimums as initially selected. A consumer calculating the extended price needs the intended entry basis and tax treatment. The resolver also derives the two local-tax descriptors from the resulting VAT rate.

For example, a catalogue item sells for 100 and the customer's wholesale level is 90. In combined individual and level mode a dated agreement at 75 through June 30 supplies the price on June 30. On July 1 the price is 90 if no successor agreement has started. In the separate quantity-with-level arrangement, a wholesale break of 82 changes the net unit price only when the caller supplies its identifier. The sale-price query itself returns no agreement-discount percentage. The offer clone's optional repricing procedure reads the selected agreement's discount separately.

Source locations include `htdocs/product/class/product.class.php:getSellPrice`, `htdocs/product/class/productcustomerprice.class.php:fetchAll` and `htdocs/comm/propal/class/propal.class.php:createFromClone`.

## Entering an individual agreement

An agreement identifies a product and buyer, and can carry that buyer's own product reference. The record includes a start, optional end, basis, net and gross selling and minimum prices, tax treatment, discount, label and author. On creation an absent start defaults to the current timestamp. A missing or non-numeric discount becomes zero. Gross entry derives net by dividing by one plus the VAT fraction. Net entry derives gross by multiplying by that factor. The unit-price rounding convention applies to the derived values. Period matching in the resolver compares against a day boundary. Supplying an explicit start day avoids ambiguity when a record was created with an intraday start.

Period validation for a product and customer excludes the row being edited. Equality between a new endpoint and an existing endpoint counts as a conflict, as does either new endpoint falling inside an existing closed interval. For example, adding July 20–August 15 over an existing July 1–31 agreement is rejected. A proposed June 1–August 31 interval encloses that entire July interval, but neither of its endpoints falls inside July. The implemented comparison can admit this overlap. Its containment comparison also uses the stored end directly, whereas the resolver treats an empty end as open-ended. When multiple agreements qualify the default search order favors the latest start.

Where customer-company price propagation is enabled and a forced update is requested, the operation visits each immediate child in the permitted entity scope. If a child already has records for the product it selects the first by descending start date and updates its prices, basis, tax rate, recoverability, label, discount and dates. It does not match that child row by the parent's effective period. For a missing child price it creates a row with the child as buyer and copies the customer product reference. Child creation and updates receive the propagation choice. A failed child write propagates an error to its caller.

Source locations include `htdocs/product/class/productcustomerprice.class.php:verifyDates`, `htdocs/product/class/productcustomerprice.class.php:create` and `htdocs/product/class/productcustomerprice.class.php:setPriceOnAffiliateThirdparty`.

## Setting levels and deriving minimums

The price-maintenance entry point distinguishes product and service edit rights from deletion rights. A product price update rejects a nonzero minimum greater than the selling price on the supplied basis. It derives the counterpart basis using VAT and unit-price precision. Updating an individual higher level does not replace the product's ordinary selling amount. Shared tax attributes can still change. The persisted level and history let a later enquiry use the latest applicable price, while issued document lines retain their own amounts.

Automatic generation runs in level order. Level one starts at the entered base. For a later level with a nonzero variation rule, multiply the referenced level price by one plus the percentage variation. A nonzero minimum variation derives the floor by multiplying that level price by one minus the minimum percentage. Without a minimum variation, the initialized floor is the original base price. For a base of 100, a level priced 20% above level one and a 10% floor reduction yields a level price of 120 and minimum of 108. Without the minimum variation its generated floor starts at 100. Rules depending on other levels need those referenced values to have been generated already.

Source locations include `htdocs/product/price.php:737–917`, `htdocs/product/class/product.class.php:updatePrice` and `htdocs/product/class/product.class.php:generateMultiprices`.
