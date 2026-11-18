# Inbound receipts

A receipt identifies incoming supplier-order lines. The service exposes receipt creation, individual line removal, validation and closure. The upstream purchase order remains separately addressable.

The implementation locations below refer to `htdocs/reception/class/api_receptions.class.php`.

## `get` — Read a goods receipt

**Arguments** `id`.

**Access** The decision uses right `reception.lire`, reception record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.

Source lines `67–84`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `thirdparty_ids = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `reception.lire`.

The lookup uses the visible entity scope for `reception`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `107–201`.

## `post` — Create a goods receipt

**Arguments** `request_data = null`.

The request-field validator requires `socid`, `origin_id`, `origin_type`.

Named body fields used by the handler include `lines`.

**Access** The decision uses right `reception.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `211–259` with `_validate 785–798`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`.

**Access** The decision uses right `reception.creer`, reception record scope.

The method removes a line.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this reception.
- `404` — reception missing, reception line missing.
- `405` — operation unavailable.

Source lines `444–478`.

## `put` — Update a goods receipt

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `reception.creer`, reception record scope, right `reception.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.

Source lines `489–528` with `get 67–84`.

## `delete` — Delete a goods receipt

**Arguments** `id`.

**Access** The decision uses right `reception.supprimer`, reception record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — removal failed.

Source lines `538–562`.

## `validate` — Validate a goods receipt

Route `POST {id}/validate`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `reception.creer`, reception record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.

Source lines `583–610`.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `reception.creer`, reception record scope.

The method closes the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — reception missing.
- `500` — business operation failed.

Source lines `705–734`.
