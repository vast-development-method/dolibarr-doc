# Business record links

A link identifies both source and target by type and identifier. Link retrieval and deletion support either a stored link identifier or the full tuple of endpoints. Removing the association does not remove its endpoint records.

## `getById` — Read by identifier

Route `GET {id}`.

**Arguments** `id` (integer).

**Result** A record with internal service properties removed.

- `403` — access refused, access or input restriction.
- `404` — object link missing.

## `create` — Create

Route `POST /`.

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — duplicate record or association.
- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `500` — business operation failed.

## `deleteById` — Remove by identifier

Route `DELETE {id}`.

**Arguments** `id` (integer).

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — removal failed.

## `getByValues` — Read by values

Route `GET /`.

**Arguments** `fk_source` (integer), `sourcetype` (text), `fk_target` (integer), `targettype` (text), `relationtype = null` (text).

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** A record with internal service properties removed.

- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — business operation failed.

## `deleteByValues` — Delete by values

Route `DELETE /`.

**Arguments** `fk_source` (integer), `sourcetype` (text), `fk_target` (integer), `targettype` (text), `relationtype = null` (text), `notrigger = 0` (integer).

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — business operation failed, removal failed.
