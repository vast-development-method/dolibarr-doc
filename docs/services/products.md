# Product catalog, prices and variants

Catalog records, variant axes, values, combinations, supplier-price rows and customer-price views are distinct resources within this service. A product identifier is different from a variant combination identifier or an attribute-value identifier.

## `get` — Read a product

**Arguments** `id` (integer), `includestockdata = 0` (integer), `includesubproducts = false` (boolean), `includeparentid = false` (boolean), `includetrans = false` (boolean).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A record with internal service properties removed.

- `400` — no product missing, bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text), `includestockdata = 0` (integer), `includesubproducts = false` (boolean), `includeparentid = false` (boolean), `includetrans = false` (boolean).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text), `includestockdata = 0` (integer), `includesubproducts = false` (boolean), `includeparentid = false` (boolean), `includetrans = false` (boolean).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getByBarcode` — Read by barcode

Route `GET barcode/{barcode}`.

**Arguments** `barcode` (text), `includestockdata = 0` (integer), `includesubproducts = false` (boolean), `includeparentid = false` (boolean), `includetrans = false` (boolean).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `index` — List records

**Arguments** `sortfield = "t.ref"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `mode = 0` (integer), `category = 0` (integer), `sqlfilters = ''` (text), `ids_only = false` (boolean), `variant_filter = 0` (integer), `pagination_data = false` (boolean), `includestockdata = 0` (integer), `properties = ''` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`. The properties selector projects the returned fields. The method reads warehouse balances.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a product

**Arguments** `request_data = null` (collection).

The request-field validator requires `ref`, `label`.

**Access** The decision uses right `produit.creer`.

The optional caller marker is placed in event context for synchronization. The method updates selling prices.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a product

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `produit.creer`, product record scope, right `produit.lire`.

The optional caller marker is placed in event context for synchronization. The method updates selling prices.

**Result** A record with internal service properties removed.

- `400` — no product missing, physical stock must change through a movement, bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.
- `500` — business operation failed.

## `delete` — Delete a product

**Arguments** `id` (integer).

**Access** The decision uses right `produit.supprimer`, product record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no product missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.
- `409` — removal failed.
- `500` — removal failed.

## `getSubproducts` — Read subproducts

Route `GET {id}/subproducts`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`, product record scope.

Each component result includes its identifier, quantity, product type, label, stock increment/decrement indicator, reference, association identifier and ordering rank.

**Result** An array of component rows with product and association identifiers, quantity and rank.

- `403` — missing operation rights, record outside the caller’s scope.

## `addSubproducts` — Add subproducts

Route `POST {id}/subproducts/add`.

**Arguments** `id` (integer), `subproduct_id` (integer), `qty` (number), `incdec = 1` (integer).

**Access** The decision uses right `produit.creer`, product record scope.

The method adds a component product.

**Result** The integer outcome of adding the component association.

- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

## `delSubproducts` — Del subproducts

Route `DELETE {id}/subproducts/remove/{subproduct_id}`.

**Arguments** `id` (integer), `subproduct_id` (integer).

**Access** The decision uses right `produit.creer`, product record scope.

The method removes a component product.

**Result** The integer outcome of removing the component association.

- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — access refused.
- `503` — query or persistence failure.

## `getCustomerPricesPerSegment` — Read customer prices per segment

Route `GET {id}/selling_multiprices/per_segment`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`.

The response separates prices and minimum prices before and including tax, tax rates and price-base types by customer pricing segment.

**Result** A record with `multiprices`, `multiprices_inc_tax`, `multiprices_min`, `multiprices_min_inc_tax`, `multiprices_vat`, `multiprices_base_type`.

- `400` — invalid request data.
- `403` — access refused.
- `404` — product missing.
- `503` — query or persistence failure.

## `getCustomerPricesPerCustomer` — Read customer prices per customer

Route `GET {id}/selling_multiprices/per_customer`.

**Arguments** `id` (integer), `thirdparty_id = ''` (text).

**Access** The decision uses right `produit.lire`.

Prices negotiated specifically with customers are returned as separate customer-price records for the selected product.

**Result** Customer-specific price rows.

- `400` — invalid request data.
- `403` — access refused.
- `404` — product missing, prices missing.

## `getCustomerPricesPerQuantity` — Read customer prices per quantity

Route `GET {id}/selling_multiprices/per_quantity`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`.

The response distinguishes quantity-price settings from the detailed list of quantity tiers.

**Result** A record with `prices_by_qty`, `prices_by_qty_list`.

- `400` — invalid request data.
- `403` — access refused.
- `404` — product missing.
- `503` — query or persistence failure.

## `addPurchasePrice` — Add purchase price

Route `POST {id}/purchase_prices`.

**Arguments** `id` (integer), `qty` (number), `buyprice` (number), `price_base_type` (text), `fourn_id` (integer), `availability` (integer), `ref_fourn` (text), `tva_tx` (number), `charges = 0` (number), `remise_percent = 0` (number), `remise = 0` (number), `newnpr = 0` (integer), `delivery_time_days = 0` (integer), `supplier_reputation = ''` (text), `localtaxes_array = []` (collection), `newdefaultvatcode = ''` (text), `multicurrency_buyprice = 0` (number), `multicurrency_price_base_type = 'HT'` (text), `multicurrency_tx = 1` (number), `multicurrency_code = ''` (text), `desc_fourn = ''` (text), `barcode = ''` (text), `fk_barcode_type = null` (integer).

**Access** The decision uses right `produit.creer`, product record scope.

The method associates a supplier and updates supplier pricing.

**Result** The supplier-price row identifier.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing, supplier missing.
- `500` — query or persistence failure.

## `deletePurchasePrice` — Delete purchase price

Route `DELETE {id}/purchase_prices/{priceid}`.

**Arguments** `id` (integer), `priceid` (integer).

**Access** The decision uses right `produit.supprimer`, product record scope.

The method removes the supplier price.

**Result** The integer result of removing the supplier price.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getSupplierProducts` — Read supplier products

Route `GET purchase_prices`.

**Arguments** `sortfield = "t.ref"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `mode = 0` (integer), `category = 0` (integer), `supplier = 0` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused, access or input restriction.
- `503` — query or persistence failure.

## `getPurchasePrices` — Read purchase prices

Route `GET {id}/purchase_prices`.

**Arguments** `id` (integer), `ref = ''` (text), `ref_ext = ''` (text), `barcode = ''` (text).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getPurchasePriceLogs` — Read purchase price logs

Route `GET {id}/purchase_prices/logs`.

**Arguments** `id` (integer), `ref = ''` (text), `ref_ext = ''` (text), `barcode = ''` (text).

**Access** The decision uses right `produit.lire`, product record scope.

**Result** A collection of matching entries.

- `400` — bad value for parameter id, ref, ref_ext or barcode.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `getAttributes` — Read attributes

Route `GET attributes`.

**Arguments** `sortfield = "t.ref"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`. The properties selector projects the returned fields.

**Result** A collection of attribute records, projected to the requested fields.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getAttributeById` — Read attribute by id

Route `GET attributes/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — product attribute missing.

## `getAttributesByRef` — Read attributes by ref

Route `GET attributes/ref/{ref}`.

**Arguments** `ref` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A single attribute record.

- `403` — access refused.
- `404` — requested data unavailable.

## `getAttributesByRefExt` — Read attributes by ref ext

Route `GET attributes/ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A single attribute record.

- `403` — access refused.
- `404` — requested data unavailable.

## `addAttributes` — Add attributes

Route `POST attributes`.

**Arguments** `ref` (text), `label` (text), `ref_ext = ''` (text).

**Access** The decision uses right `produit.creer`.

**Result** The created attribute identifier.

- `403` — access refused.
- `500` — business operation failed.

## `putAttributes` — Put attributes

Route `PUT attributes/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `produit.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — attribute missing.
- `500` — business operation failed.

## `deleteAttributes` — Delete attributes

Route `DELETE attributes/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.supprimer`.

**Result** The attribute-removal result.

- `403` — access refused.
- `500` — removal failed.

## `getAttributeValueById` — Read attribute value by id

Route `GET attributes/values/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A single attribute-value record.

- `403` — access refused, access or input restriction.
- `404` — attribute value missing.

## `getAttributeValueByRef` — Read attribute value by ref

Route `GET attributes/{id}/values/ref/{ref}`.

**Arguments** `id` (integer), `ref` (text).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `product`.

**Result** A single attribute-value record.

- `403` — access refused, access or input restriction.
- `404` — attribute value missing.

## `deleteAttributeValueByRef` — Delete attribute value by ref

Route `DELETE attributes/{id}/values/ref/{ref}`.

**Arguments** `id` (integer), `ref` (text).

**Access** The decision uses right `produit.supprimer`.

The lookup uses the visible entity scope for `product`.

**Result** An integer success indicator of 1.

- `403` — access refused, access or input restriction.
- `404` — attribute value missing.
- `500` — removal failed.

## `getAttributeValues` — Read attribute values

Route `GET attributes/{id}/values`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.lire`.

**Result** A collection of values for the selected attribute.

- `403` — access refused.
- `404` — attribute values missing.

## `getAttributeValuesByRef` — Read attribute values by ref

Route `GET attributes/ref/{ref}/values`.

**Arguments** `ref` (text).

**Access** The decision uses right `produit.lire`.

**Result** A collection of values for the selected attribute.

- `403` — access refused.

## `addAttributeValue` — Add attribute value

Route `POST attributes/{id}/values`.

**Arguments** `id` (integer), `ref` (text), `value` (text).

**Access** The decision uses right `produit.creer`.

**Result** The record identifier.

- `403` — access refused, access or input restriction.
- `500` — business operation failed.

## `putAttributeValue` — Put attribute value

Route `PUT attributes/values/{id}`.

**Arguments** `id` (integer), `request_data` (collection).

**Access** The decision uses right `produit.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — attribute value missing, attribute missing.
- `500` — business operation failed.

## `deleteAttributeValueById` — Delete attribute value by id

Route `DELETE attributes/values/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.supprimer`.

**Result** An integer success indicator of 1.

- `403` — access refused.
- `500` — removal failed.

## `getVariants` — Read variants

Route `GET {id}/variants`.

**Arguments** `id` (integer), `includestock = 0` (integer).

**Access** The decision uses right `produit.lire`.

The method reads warehouse balances. The service loads combinations for the parent product, associates each with its attribute/value pairs and resolves the associated child product. Combination identity and child-product identity are distinct.

**Result** Combinations for the parent product with attribute-value pairs.

- `403` — access refused.

## `getVariantsByProdRef` — Read variants by prod ref

Route `GET ref/{ref}/variants`.

**Arguments** `ref` (text).

**Access** The decision uses right `produit.lire`.

**Result** Combinations for the selected parent product.

- `403` — access refused.
- `404` — product missing.

## `addVariant` — Add variant

Route `POST {id}/variants`.

**Arguments** `id` (integer), `weight_impact` (number), `price_impact` (number), `price_impact_is_percent` (boolean), `features` (collection), `reference = ''` (text), `ref_ext = ''` (text).

**Access** The decision uses right `produit.creer`.

The method creates a product variant. Each selected attribute value is normalized to an identifier. The combination creation operation receives price and weight impacts, the price-impact mode and optional product references along with the selected features.

**Result** The integer result of combination creation.

- `400` — product id required, features required, invalid attribute ID, invalid attribute value ID.
- `403` — access refused.
- `404` — product missing.
- `500` — business operation failed.

## `addVariantByProductRef` — Add variant by product ref

Route `POST ref/{ref}/variants`.

**Arguments** `ref` (text), `weight_impact` (number), `price_impact` (number), `price_impact_is_percent` (boolean), `features` (collection).

**Access** The decision uses right `produit.creer`.

The method creates a product variant.

**Result** The record identifier.

- `403` — access refused, access or input restriction.
- `404` — requested data unavailable, product missing.
- `500` — business operation failed.

## `putVariant` — Put variant

Route `PUT variants/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `produit.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** An integer success indicator of 1.

- `403` — access refused.
- `404` — variant missing.
- `500` — business operation failed.

## `deleteVariant` — Delete variant

Route `DELETE variants/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `produit.supprimer`.

**Result** The integer result of removing the combination.

- `403` — access refused.
- `404` — variant missing.
- `500` — removal failed.

## `getStock` — Read stock

Route `GET {id}/stock`.

**Arguments** `id` (integer), `selected_warehouse_id = null` (integer).

**Access** The decision uses both `produit.lire` and `stock.lire`, product record scope.

The method reads warehouse balances. The result includes physical and theoretical stock and a warehouse-balance field. Supplying a warehouse limits the warehouse detail.

**Result** A stock record containing physical, theoretical and warehouse quantities.

- `403` — missing operation rights, record outside the caller’s scope.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `produit.lire`, product record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source = "external"` (text), `notrigger = 0` (integer).

**Access** The decision uses right `produit.creer`, product record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — contact already added.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.
- `500` — business operation failed.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `produit.creer`, product record scope.

The method loads contacts by role and removes a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product missing.
- `500` — removal failed.
