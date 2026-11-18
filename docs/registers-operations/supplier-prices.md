# Supplier products and prices

The register starts with `product` in the permitted product entities. It left joins `product_fournisseur_price` by product ID and permitted supplier-price entities, then left joins the supplier `societe` by the offer's `fk_soc` and allowed party entities. Without an offer filter, even an item with no supplier price can contribute a row. Each price break for the same product and supplier can create another row. The selected `price`, `quantity` and `unitprice` belong to the offer. The displayed product row ID is shared by all its offers. There is no aggregate or minimum-price selection in this query.

| Input | Predicate |
| --- | --- |
| `sref`, `snom` | Keyword match on the item's own `ref` and `label`. |
| `srefsupplier` | Keyword match on `product_fournisseur_price.ref_fourn`. An unpriced item has no matching offer reference. |
| `fourn_id` | A positive ID selects the offer's `fk_soc`. External users have their own party ID substituted. Although parsed as an integer-list form value, the native predicate uses scalar integer equality. |
| `catid` | Adds the product-category relationship then requires the selected category ID on it. The applied category is a scalar integer. |
| `type` | A truthy supplied value is cast to integer and compared with `fk_product_type`. The service value 1 applies a filter. A submitted literal 0 for goods is false in this decision and adds no goods-only restriction. |

Access requires product read **or** service read. The selection has no general purchase-enabled, sale-enabled, active-supplier, effective-date, currency, quantity-threshold or lowest-cost predicate. The default sort is the product's own reference. A report that needs only immediately purchasable offers must establish those conditions separately.

If item A has offers at quantities one and ten with supplier S, and item B has no offers, the ordinary list returns three rows for two items. Selecting S returns the two rows for A. Selecting type 1 further requires that A be a service. This register cannot answer which of the two offers should price an order for four units without a quantity-selection rule.
