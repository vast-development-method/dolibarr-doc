# Email campaigns and targets

A campaign has a header and target rows. A target can be amended, deleted or reset independently of the campaign. The service also exposes duplication and transitions between draft and validated status.

The implementation locations below refer to `htdocs/comm/mailing/class/api_mailings.class.php`.

## `get` — Read a campaign

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.read`, mailing record scope, project record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.

Source lines `85–88` with `_fetch 100–122`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `fk_projects = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer).

**Access** The decision uses right `mailing.read`, project record scope.

The lookup uses the visible entity scope for `mailing`. The properties selector projects the returned fields. The method loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `503` — query or persistence failure.

Source lines `147–231`.

## `indexTargets` — Index targets

Route `GET {id}/targets`.

**Arguments** `id` (integer), `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `mailing.read`, project record scope.

The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `503` — query or persistence failure.

Source lines `258–339`.

## `clone` — Clone

**Arguments** `id` (integer), `cloneContent = 1` (integer), `cloneRecipients = 1` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `mailing.write`, project record scope, right `mailing.read`, mailing record scope.

The method duplicates the source record.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing to clone missing, mass mailing missing.
- `500` — business operation failed.

Source lines `356–380` with `get 85–88`, `_fetch 100–122`.

## `post` — Create a campaign

**Arguments** `request_data = null` (collection).

The request-field validator requires `title`, `sujet`, `body`.

**Access** The decision uses right `mailing.write`, project record scope.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

Source lines `395–423` with `_validate 976–989`.

## `put` — Update a campaign

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `mailing.write`, project record scope, mailing record scope, right `mailing.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — business operation failed.

Source lines `440–482` with `get 85–88`, `_fetch 100–122`.

## `delete` — Delete a campaign

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.delete`, project record scope, mailing record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — removal failed.

Source lines `498–526`.

## `updateTarget` — Update target

Route `PUT {id}/updateTarget/{targetid}`.

**Arguments** `id` (integer), `targetid` (integer), `request_data = null` (collection).

**Access** The decision uses right `mailing.write`, project record scope, mailing record scope, right `mailing.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — invalid request data, removal failed.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing, mass mailing target missing, target belongs to another campaign.
- `500` — business operation failed.

Source lines `546–592` with `getTarget 677–680`, `_fetchTarget 694–721`.

## `postTarget` — Post target

Route `POST {id}/createTarget`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `mailing.write`, project record scope.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — business operation failed.

Source lines `612–660` with `_validateTarget 999–1012`.

## `getTarget` — Read target

Route `GET {id}/getTarget/{targetid}`.

**Arguments** `id` (integer), `targetid` (integer).

**Access** The decision uses right `mailing.read`, project record scope, mailing record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing, mass mailing target missing, target belongs to another campaign.

Source lines `677–680` with `_fetchTarget 694–721`.

## `deleteTarget` — Delete target

Route `DELETE {id}/deleteTarget/{targetid}`.

**Arguments** `id` (integer), `targetid` (integer).

**Access** The decision uses right `mailing.delete`, project record scope, mailing record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing, mass mailing target missing, target belongs to another campaign.
- `500` — removal failed.

Source lines `740–774`.

## `deleteTargets` — Delete targets

Route `DELETE {id}/deleteTargets`.

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.delete`, project record scope, mailing record scope.

The method counts campaign targets and removes campaign targets.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — removal failed.

Source lines `792–821`.

## `resetTargetsStatus` — Reset targets status

Route `PUT {id}/resetTargetsStatus`.

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.write`, project record scope, mailing record scope.

The method counts campaign targets and resets campaign target statuses.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — business operation failed.

Source lines `839–868`.

## `settodraft` — Return to draft

Route `PUT {id}/settodraft`.

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.write`, project record scope, mailing record scope.

The method restores draft state and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already draft).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — business operation failed.

Source lines `885–914`.

## `validate` — Validate a campaign

Route `PUT {id}/validate`.

**Arguments** `id` (integer).

**Access** The decision uses right `mailing.write`, project record scope, mailing record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mass mailing missing.
- `500` — business operation failed.

Source lines `937–966`.
