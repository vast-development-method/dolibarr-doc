# Knowledge articles

A knowledge record has a lifecycle and can belong to categories. The article's content and publication state are distinct from the category classification returned for that record.

## `get` — Read a knowledge article

Route `GET knowledgerecords/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.read`, knowledgerecord record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — knowledge article missing.

## `getCategories` — Read categories

Route `GET /knowledgerecords/{id}/categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — access refused.
- `503` — query or persistence failure.

## `index` — List records

Route `GET /knowledgerecords/`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.read`.

The article list applies its entity scope, optional category and supplied search criteria. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a knowledge article

Route `POST knowledgerecords/`.

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a knowledge article

Route `PUT knowledgerecords/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.write`, knowledgerecord record scope, right `knowledgemanagement.knowledgerecord.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — knowledge article missing.
- `500` — business operation failed.

## `delete` — Delete a knowledge article

Route `DELETE knowledgerecords/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.delete`, knowledgerecord record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — knowledge article missing.
- `500` — removal failed.

## `validate` — Validate a knowledge article

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.write`.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — access refused.
- `404` — knowledge article missing.
- `500` — business operation failed.

## `cancel` — Cancel

Route `POST {id}/cancel`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `knowledgemanagement.knowledgerecord.write`.

The method cancels the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — access refused.
- `404` — knowledge article missing.
- `500` — business operation failed.
