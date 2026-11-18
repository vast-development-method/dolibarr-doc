# Warehouses and balances

A warehouse can be created or amended independently of its stock. Listing its products reports the inventory stored there. Moving quantity uses the stock-movement service.

## `get` — Read a warehouse

Route `GET {id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `stock.lire`, stock record scope.

**Result** A record with internal service properties removed.

- `400` — no warehouse missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — warehouse missing.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `stock.lire`.

The lookup uses the visible entity scope for `stock`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a warehouse

Route `POST /`.

**Arguments** `request_data = null` (collection).

The request-field validator requires `label`.

**Access** The decision uses right `stock.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, changing entity of a user using the APIs is not possible.
- `500` — business operation failed.

## `put` — Update a warehouse

Route `PUT {id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `stock.creer`, stock record scope, right `stock.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no warehouse missing, body includes a forbidden identifier, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — warehouse missing.
- `500` — business operation failed.

## `delete` — Delete a warehouse

Route `DELETE {id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `stock.supprimer`, stock record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no warehouse missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — warehouse missing.
- `500` — removal failed.

## `listProducts` — List products

Route `GET /{id}/products`.

**Arguments** `id = 0` (integer), `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `includestockdata = 0` (integer), `includesubproducts = false` (boolean), `includeparentid = false` (boolean), `includetrans = false` (boolean), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `stock.lire`.

The lookup uses the visible entity scope for `stock`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — no warehouse missing.
- `403` — access refused.
- `404` — warehouse missing.
- `500` — query or persistence failure.
