# Vacancies and applications

A job position and a candidature are different resource types with their own rows. The API has distinct reads, lists, creates, updates and deletions for each.

The implementation locations below refer to `htdocs/recruitment/class/api_recruitments.class.php`.

## `getJobPosition` — Read job position

Route `GET jobposition/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `recruitment.recruitmentjobposition.read`, recruitment record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — jobposition missing.

Source lines `78–94`.

## `getCandidature` — Read candidature

Route `GET candidature/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `recruitment.recruitmentjobposition.read`, recruitment record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — candidature missing.

Source lines `109–125`.

## `indexJobPosition` — Index job position

Route `GET /jobposition/`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `recruitment.recruitmentjobposition.read`.

The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `147–243`.

## `indexCandidature` — Index candidature

Route `GET /candidature/`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `recruitment.recruitmentjobposition.read`.

The application list applies the entity scope of the model and the supplied search criteria. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `265–360`.

## `postJobPosition` — Post job position

Route `POST jobposition/`.

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `recruitment.recruitmentjobposition.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `374–400` with `_validate 699–715`.

## `postCandidature` — Post candidature

Route `POST candidature/`.

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `recruitment.recruitmentjobposition.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `414–442` with `_validate 699–715`.

## `putJobPosition` — Put job position

Route `PUT jobposition/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `recruitment.recruitmentjobposition.write`, recruitment record scope, right `recruitment.recruitmentjobposition.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — jobposition missing.
- `500` — business operation failed.

Source lines `457–493` with `getJobPosition 78–94`.

## `putCandidature` — Put candidature

Route `PUT candidature/{id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `recruitment.recruitmentjobposition.write`, recruitment record scope, right `recruitment.recruitmentjobposition.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — candidature missing.
- `500` — business operation failed.

Source lines `508–544` with `getCandidature 109–125`.

## `deleteJobPosition` — Delete job position

Route `DELETE jobposition/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `recruitment.recruitmentjobposition.delete`, recruitment record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — jobposition missing.
- `500` — removal failed.

Source lines `559–583`.

## `deleteCandidature` — Delete candidature

Route `DELETE candidature/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `recruitment.recruitmentjobposition.delete`, recruitment record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — candidature missing.
- `500` — removal failed.

Source lines `597–621`.
