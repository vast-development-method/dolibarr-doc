# Stock movements

Each movement changes or records quantity for a product and warehouse. The request can identify a batch. The movement record is separate from the current stock balance and from the product master.

The implementation locations below refer to `htdocs/product/stock/class/api_stockmovements.class.php`.

## `get` — Read a stock movement

Route `GET {id}`.

**Arguments** `id`.

**Access** The decision uses right `stock.mouvement.lire`, stockmovement record scope.

**Result** A record with internal service properties removed.

- `400` — no stock movement missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — stock movement missing.

Source lines `77–95`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `stock.lire`.

The lookup uses the visible entity scope for `stock`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `115–186`.

## `post` — Create a stock movement

**Arguments** `product_id`, `warehouse_id`, `qty`, `type = 2`, `batch = ''`, `movementcode = ''`, `label = ''`, `price = ''`, `datem = ''`, `sellBy = ''`, `eatBy = ''`, `origin_type = ''`, `origin_id = 0`.

**Access** The decision uses right `stock.creer`.

The method attaches a source record and posts the stock movement. Quantity zero is rejected. A supplied source type and source identifier can associate the movement with its origin. Warehouse, product, movement type, date, price and optional batch information are passed together to the business operation. The returned identifier addresses the movement in the stock journal.

**Result** The record identifier.

- `403` — access refused.
- `503` — zero movement quantity, record lookup or write failed.

Source lines `217–250`.
