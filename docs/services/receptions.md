# Inbound receipts

A receipt identifies incoming supplier-order lines. The service exposes receipt creation, individual line removal, validation and closure. The upstream purchase order remains separately addressable.

## `get` — Read a goods receipt

**Arguments** `id` (integer).

**Access** The decision uses right `reception.lire`, reception record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `reception.lire`.

The lookup uses the visible entity scope for `reception`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a goods receipt

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`, `origin_id`, `origin_type`.

Named body fields used by the handler include `lines`.

**Access** The decision uses right `reception.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `reception.creer`, reception record scope.

The method removes a line.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this reception.
- `404` — reception missing, reception line missing.
- `405` — operation unavailable.

## `put` — Update a goods receipt

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `reception.creer`, reception record scope, right `reception.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.

## `delete` — Delete a goods receipt

**Arguments** `id` (integer).

**Access** The decision uses right `reception.supprimer`, reception record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — removal failed.

## `validate` — Validate a goods receipt

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `reception.creer`, reception record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `reception.creer`, reception record scope.

The method closes the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.
