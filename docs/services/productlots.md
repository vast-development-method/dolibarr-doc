# Product lots

A lot identifies a batch of a particular product and carries the lot's own descriptive data. Lot master data and warehouse stock movements have separate operations.

## `get` — Read a product lot

**Arguments** `id` (integer).

**Access** The decision uses right `product.lire`, product record scope.

The method loads additional fields and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product lots missing.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "pl.batch"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `user_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `produit.lire`.

The lookup uses the visible entity scope for `productlot`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a product lot

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_product`, `batch`.

**Access** The decision uses right `produit.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a product lot

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `produit.creer`, product record scope, right `product.lire`.

The optional caller marker is placed in event context for synchronization. The method loads additional fields.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — productlot missing, product lots missing.

## `delete` — Delete a product lot

**Arguments** `id` (integer).

**Access** The decision uses right `produit.supprimer`, product record scope.

The method loads additional fields.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — product lot missing.
- `500` — removal failed.
