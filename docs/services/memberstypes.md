# Membership types

Membership types are reference records. Changing the type definition and recording a particular member’s subscription are separate operations.

The implementation locations below refer to `htdocs/adherents/class/api_memberstypes.class.php`.

## `get` — Read a membership type

**Arguments** `id` (integer).

**Access** The decision uses right `adherent.lire`, member record scope.

**Result** A record with internal service properties removed.

- `401` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing.

Source lines `58–75`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `adherent.lire`.

The lookup uses the visible entity scope for `member_type`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `401` — access refused.
- `503` — invalid filter expression, query or persistence failure.

Source lines `94–143`.

## `post` — Create a membership type

**Arguments** `request_data = null` (collection).

The request-field validator requires `label`.

**Access** The decision uses right `adherent.configurer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `401` — access refused.
- `500` — business operation failed.

Source lines `153–175` with `_validate 277–287`.

## `put` — Update a membership type

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `adherent.configurer`, member record scope, right `adherent.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `401` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing.
- `500` — business operation failed.

Source lines `186–229` with `get 58–75`.

## `delete` — Delete a membership type

**Arguments** `id` (integer).

**Access** The decision uses right `adherent.configurer`, member record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `401` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing.
- `409` — removal failed.
- `500` — removal failed.

Source lines `239–267`.
