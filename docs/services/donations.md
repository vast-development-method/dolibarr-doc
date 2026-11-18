# Donations

Creation, editing and validation of a gift are distinct operations. A donor's gift record has its own identifier independently of bank transactions created when money is received.

## `get` — Read a donation

**Arguments** `id` (integer).

**Access** The decision uses right `don.lire`, donation record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `don.lire`.

The lookup uses the visible entity scope for `don`. A caller linked to a party receives that party restriction. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a donation

**Arguments** `request_data = null` (collection).

The request-field validator requires `amount`.

**Access** The decision uses right `don.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a donation

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `don.creer`, donation record scope, right `don.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.
- `500` — business operation failed.

## `delete` — Delete a donation

**Arguments** `id` (integer).

**Access** The decision uses right `don.supprimer`, donation record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.
- `500` — removal failed.

## `validate` — Validate a donation

Route `POST {id}/validate`.

**Arguments** `id` (integer), `idwarehouse = 0` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `don.creer`, donation record scope.

The method validates the donation and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing, order missing.
- `500` — business operation failed.
