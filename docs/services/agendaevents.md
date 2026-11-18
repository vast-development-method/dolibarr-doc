# Calendar activities

An activity belongs to the agenda and can carry assigned users, dates and a related business record. An external identifier carried by an activity is distinct from its local record identifier.

The implementation locations below refer to `htdocs/comm/action/class/api_agendaevents.class.php`.

## `get` — Read a calendar activity

**Arguments** `id` (integer).

**Access** The decision uses right `agenda.myactions.read`, right `agenda.allactions.read`, agenda record scope.

The method loads additional fields and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — agenda events missing.

Source lines `73–99`.

## `index` — List records

**Arguments** `sortfield = "t.id"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `user_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `agenda.myactions.read`.

The lookup uses the visible entity scope for `agenda`. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method resolves descendant records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `123–227`.

## `post` — Create a calendar activity

**Arguments** `request_data = null` (collection).

The request-field validator requires `userownerid`, `type_code`.

**Access** The decision uses right `agenda.myactions.create`, right `agenda.allactions.create`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `241–275` with `_validate 406–419`.

## `put` — Update a calendar activity

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `userownerid`.

**Access** The decision uses right `agenda.myactions.create`, right `agenda.allactions.create`, actioncomm record scope, right `agenda.allactions.read`, right `agenda.myactions.read`, agenda record scope.

The optional caller marker is placed in event context for synchronization. The method loads additional fields and reads assigned users.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — actioncomm missing, agenda events missing.
- `500` — business operation failed.

Source lines `291–345` with `get 73–99`.

## `delete` — Delete a calendar activity

**Arguments** `id` (integer).

**Access** The decision uses right `agenda.myactions.delete`, right `agenda.allactions.delete`, actioncomm record scope.

The method loads additional fields and reads assigned users.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — agenda event missing.
- `500` — removal failed.

Source lines `360–397`.
