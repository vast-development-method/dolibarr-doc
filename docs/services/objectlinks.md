# Business record links

A link identifies both source and target by type and identifier. Link retrieval and deletion support either a stored link identifier or the full tuple of endpoints. Removing the association does not remove its endpoint records.

The implementation locations below refer to `htdocs/api/class/api_objectlinks.class.php`.

## `getById` — Read by identifier

Route `GET {id}`.

**Arguments** `id`.

**Result** A record with internal service properties removed.

- `403` — access refused, access or input restriction.
- `404` — object link missing.

Source lines `81–84` with `_fetch 431–466`.

## `create` — Create

Route `POST /`.

**Arguments** `request_data = null`.

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — duplicate record or association.
- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `500` — business operation failed.

Source lines `136–194` with `_validate 577–587`, `_setObjectLinkField 95–112`.

## `deleteById` — Remove by identifier

Route `DELETE {id}`.

**Arguments** `id`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — removal failed.

Source lines `210–255`.

## `getByValues` — Read by values

Route `GET /`.

**Arguments** `fk_source`, `sourcetype`, `fk_target`, `targettype`, `relationtype = null`.

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** A record with internal service properties removed.

- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — business operation failed.

Source lines `275–329` with `_validate 577–587`, `_setObjectLinkField 95–112`.

## `deleteByValues` — Delete by values

Route `DELETE /`.

**Arguments** `fk_source`, `sourcetype`, `fk_target`, `targettype`, `relationtype = null`, `notrigger = 0`.

The request-field validator requires `fk_source`, `sourcetype`, `fk_target`, `targettype`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — required request field absent.
- `403` — access refused, access or input restriction.
- `404` — object link missing.
- `500` — business operation failed, removal failed.

Source lines `351–416` with `_validate 577–587`, `_setObjectLinkField 95–112`.
