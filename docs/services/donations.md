# Donations

Creation, editing and validation of a gift are distinct operations. A donor's gift record has its own identifier independently of bank transactions created when money is received.

The implementation locations below refer to `htdocs/don/class/api_donations.class.php`.

## `get` — Read a donation

**Arguments** `id`.

**Access** The decision uses right `don.lire`, donation record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.

Source lines `65–84`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `thirdparty_ids = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `don.lire`.

The lookup uses the visible entity scope for `don`. A caller linked to a party receives that party restriction. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `105–191`.

## `post` — Create a donation

**Arguments** `request_data = null`.

The request-field validator requires `amount`.

**Access** The decision uses right `don.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `201–232` with `_validate 411–424`.

## `put` — Update a donation

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `don.creer`, donation record scope, right `don.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.
- `500` — business operation failed.

Source lines `243–282` with `get 65–84`.

## `delete` — Delete a donation

**Arguments** `id`.

**Access** The decision uses right `don.supprimer`, donation record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing.
- `500` — removal failed.

Source lines `292–317`.

## `validate` — Validate a donation

Route `POST {id}/validate`.

**Arguments** `id`, `idwarehouse = 0`, `notrigger = 0`.

**Access** The decision uses right `don.creer`, donation record scope.

The method validates the donation and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — donation missing, order missing.
- `500` — business operation failed.

Source lines `341–377`.
