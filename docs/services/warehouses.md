# Warehouses and balances

A warehouse can be created or amended independently of its stock. Listing its products reports the inventory stored there. Moving quantity uses the stock-movement service.

The implementation locations below refer to `htdocs/product/stock/class/api_warehouses.class.php`.

## `get` — Read a warehouse

Route `GET {id}`.

**Arguments** `id`.

**Access** The decision uses right `stock.lire`, stock record scope.

**Result** A record with internal service properties removed.

- `400` — no warehouse missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — warehouse missing.

Source lines `74–92`.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `category = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `stock.lire`.

The lookup uses the visible entity scope for `stock`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `120–196`.

## `post` — Create a warehouse

Route `POST /`.

**Arguments** `request_data = null`.

The request-field validator requires `label`.

**Access** The decision uses right `stock.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, changing entity of a user using the APIs is not possible.
- `500` — business operation failed.

Source lines `216–245` with `_validate 554–567`.

## `put` — Update a warehouse

Route `PUT {id}`.

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `stock.creer`, stock record scope, right `stock.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no warehouse missing, body includes a forbidden identifier, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — warehouse missing.
- `500` — business operation failed.

Source lines `266–316` with `get 74–92`.

## `delete` — Delete a warehouse

Route `DELETE {id}`.

**Arguments** `id`.

**Access** The decision uses right `stock.supprimer`, stock record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no warehouse missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — warehouse missing.
- `500` — removal failed.

Source lines `336–363`.

## `listProducts` — List products

Route `GET /{id}/products`.

**Arguments** `id = 0`, `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `includestockdata = 0`, `includesubproducts = false`, `includeparentid = false`, `includetrans = false`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `stock.lire`.

The lookup uses the visible entity scope for `stock`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — no warehouse missing.
- `403` — access refused.
- `404` — warehouse missing.
- `500` — query or persistence failure.

Source lines `396–462`.
