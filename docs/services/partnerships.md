# Partnership records

The service operates on the business relationship held by the partnership record. List and detail access are evaluated on that resource. The related party has a separate service and lifecycle.

## `get` — Read a partnership

Route `GET partnerships/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `partnership.read`, partnership record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — partnership missing.

## `index` — List records

Route `GET /partnerships/`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `partnership.read`.

In party-managed mode, the list applies the caller’s linked party or the sales representative restriction for a user limited to assigned customers. In member-managed mode this party predicate is inactive. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a partnership

Route `POST partnerships/`.

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `partnership.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a partnership

Route `PUT partnerships/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `partnership.write`, partnership record scope, right `partnership.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — partnership missing.
- `500` — business operation failed.

## `delete` — Delete a partnership

Route `DELETE partnerships/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `partnership.delete`, partnership record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — partnership missing.
- `500` — removal failed.
