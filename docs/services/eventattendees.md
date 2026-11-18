# Event registrations

Registrations can be looked up, amended or removed by local identifier or reference. A registration is an attendee's link to an event or booth. The associated invoice and payment are separate financial records. Its shared authorization helper considers the event module, the applicable project right, access to all projects and access to the particular project.

The implementation locations below refer to `htdocs/eventorganization/class/api_eventattendees.class.php`.

## `deleteById` — Remove by identifier

Route `DELETE {id}`.

**Arguments** `id`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no eventattendee missing.
- `403` — access or input restriction.
- `404` — event attendee missing.
- `500` — removal failed, project id missing, query or persistence failure.

Source lines `86–111` with `_checkAccessRights 632–686`.

## `deleteByRef` — Remove by reference

Route `DELETE ref/{ref}`.

**Arguments** `ref`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access or input restriction.
- `404` — event attendee with ref missing.
- `500` — removal failed, project id missing, query or persistence failure.

Source lines `127–149` with `_checkAccessRights 632–686`.

## `getById` — Read by identifier

Route `GET {id}`.

**Arguments** `id`.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — project id missing, query or persistence failure.

Source lines `166–169` with `_fetch 484–516`, `_checkAccessRights 632–686`.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref`.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — project id missing, query or persistence failure.

Source lines `186–189` with `_fetch 484–516`, `_checkAccessRights 632–686`.

## `index` — List records

Route `GET /`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`, `loadlinkedobjects = 0`.

The properties selector projects the returned fields. The method loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access or input restriction.
- `500` — project id missing, query or persistence failure.
- `503` — query or persistence failure.

Source lines `213–314` with `_checkAccessRights 632–686`.

## `post` — Create an event registration

Route `POST /`.

**Arguments** `request_data = null`.

The request-field validator requires `fk_project`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access or input restriction.
- `500` — business operation failed, project id missing, query or persistence failure.

Source lines `334–359` with `_checkAccessRights 632–686`, `_validate 609–619`.

## `putById` — Amend by identifier

Route `PUT {id}`.

**Arguments** `id`, `request_data = null`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — business operation failed, project id missing, query or persistence failure.

Source lines `380–413` with `_checkAccessRights 632–686`, `_fetch 484–516`.

## `putByRef` — Amend by reference

Route `PUT ref/{ref}`.

**Arguments** `ref`, `request_data = null`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no eventattendee missing, no eventattendee can be found with no criteria.
- `403` — access or input restriction.
- `404` — event attendee missing, event attendee with ref missing.
- `500` — business operation failed, project id missing, query or persistence failure.

Source lines `434–468` with `_checkAccessRights 632–686`, `_fetch 484–516`.
