# Outbound shipments

Creation and validation operate on the shipment header with source-document lines. Removing one line, deleting the shipment and closing it are separate operations.

## `get` — Read a shipment

**Arguments** `id` (integer).

**Access** The decision uses right `expedition.lire`, expedition record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `expedition.lire`.

The lookup uses the visible entity scope for `expedition`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a shipment

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`, `origin_id`, `origin_type`.

Named body fields used by the handler include `lines`.

**Access** The decision uses right `expedition.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `expedition.creer`, expedition record scope.

The method removes a line.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.
- `405` — operation unavailable.

## `put` — Update a shipment

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `expedition.creer`, expedition record scope, right `expedition.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.
- `500` — business operation failed.

## `delete` — Delete a shipment

**Arguments** `id` (integer).

**Access** The decision uses right `expedition.supprimer`, expedition record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.
- `500` — removal failed.

## `validate` — Validate a shipment

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `expedition.creer`, expedition record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.
- `500` — business operation failed.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `expedition.creer`, expedition record scope.

The method closes the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipment missing.
- `500` — business operation failed.
