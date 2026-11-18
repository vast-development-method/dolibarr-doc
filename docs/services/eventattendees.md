# Event registrations

Registrations can be looked up, amended or removed by local identifier or reference. A registration is an attendee's link to an event or booth. The associated invoice and payment are separate financial records. Its shared authorization helper considers the event module, the applicable project right, access to all projects and access to the particular project.

## `deleteById` — Remove by identifier

Route `DELETE {id}`.

**Arguments** `id` (integer).

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no eventattendee missing.
- `403` — access or input restriction.
- `404` — event attendee missing.
- `500` — removal failed, project id missing, query or persistence failure.

## `deleteByRef` — Remove by reference

Route `DELETE ref/{ref}`.

**Arguments** `ref` (text).

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access or input restriction.
- `404` — event attendee with ref missing.
- `500` — removal failed, project id missing, query or persistence failure.

## `getById` — Read by identifier

Route `GET {id}`.

**Arguments** `id` (integer).

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — project id missing, query or persistence failure.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text).

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — project id missing, query or persistence failure.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer).

The properties selector projects the returned fields. The method loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access or input restriction.
- `500` — project id missing, query or persistence failure.
- `503` — query or persistence failure.

## `post` — Create an event registration

Route `POST /`.

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_project`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access or input restriction.
- `500` — business operation failed, project id missing, query or persistence failure.

## `putById` — Amend by identifier

Route `PUT {id}`.

**Arguments** `id` (integer), `request_data = null` (collection).

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — business operation failed, project id missing, query or persistence failure.

## `putByRef` — Amend by reference

Route `PUT ref/{ref}`.

**Arguments** `ref` (text), `request_data = null` (collection).

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — business operation failed, project id missing, query or persistence failure.
