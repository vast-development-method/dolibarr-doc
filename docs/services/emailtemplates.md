# Email templates

A template can be addressed by its identifier or label. Creation, updates and deletion work on the template definition. Message dispatch is a separate operation.

The implementation locations below refer to `htdocs/api/class/api_emailtemplates.class.php`.

## `deleteById` — Remove by identifier

Route `DELETE {id}`.

**Arguments** `id`.

**Access** The decision uses administrator status.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — removal failed, access refused, access or input restriction.
- `404` — email template missing.
- `500` — removal failed.

Source lines `93–119` with `_checkAccessRights 674–698`.

## `deleteByLabel` — Delete by label

Route `DELETE label/{label}`.

**Arguments** `label`.

**Access** The decision uses administrator status.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — removal failed, access refused, access or input restriction.
- `404` — email template with label missing.
- `500` — removal failed.

Source lines `135–161` with `_checkAccessRights 674–698`.

## `getById` — Read by identifier

Route `GET {id}`.

**Arguments** `id`.

**Result** A record with internal service properties removed.

- `400` — unknown error in your request, invalid request data.
- `403` — access or input restriction.
- `404` — email template missing, email template with label missing.

Source lines `178–181` with `_fetch 515–543`, `_checkAccessRights 674–698`.

## `getByLabel` — Read by label

Route `GET label/{label}`.

**Arguments** `label`.

**Result** A record with internal service properties removed.

- `400` — unknown error in your request, invalid request data.
- `403` — access or input restriction.
- `404` — email template missing, email template with label missing.

Source lines `198–201` with `_fetch 515–543`, `_checkAccessRights 674–698`.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "e.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `fk_user = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access or input restriction.
- `503` — query or persistence failure.

Source lines `225–304` with `_checkAccessRights 674–698`.

## `post` — Create an email template

Route `POST /`.

**Arguments** `request_data = null`.

The request-field validator requires `label`, `topic`, `type_template`.

Named body fields used by the handler include `fk_user`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, invalid request data, required request field absent.
- `403` — access or input restriction.
- `500` — business operation failed.

Source lines `324–365` with `_checkAccessRights 674–698`, `_validate 653–663`.

## `putById` — Amend by identifier

Route `PUT {id}`.

**Arguments** `id`, `request_data = null`.

**Access** The decision uses administrator status.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — body includes a forbidden identifier, invalid request data, access refused, unknown error in your request.
- `403` — access or input restriction, access refused.
- `404` — email template missing, email template with label missing.
- `500` — business operation failed.

Source lines `387–430` with `_checkAccessRights 674–698`, `_fetch 515–543`.

## `putbyLabel` — Putby label

Route `PUT label/{label}`.

**Arguments** `label`, `request_data = null`.

**Access** The decision uses administrator status.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — body includes a forbidden identifier, invalid request data, access refused, unknown error in your request.
- `403` — access or input restriction, access refused.
- `404` — email template missing, email template with label missing.
- `500` — business operation failed.

Source lines `451–498` with `_checkAccessRights 674–698`, `_fetch 515–543`.
