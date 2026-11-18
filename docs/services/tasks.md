# Project tasks and time entries

Time entries belong to tasks and have their own identifiers. Editing a task, assigning contacts and amending a single recorded labor interval are separate operations.

The implementation locations below refer to `htdocs/projet/class/api_tasks.class.php`.

## `get` — Read a task

**Arguments** `id` (integer), `includetimespent = 0` (integer).

**Access** The decision uses right `projet.lire`, task record scope.

The method totals recorded time and reads task time entries.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.

Source lines `76–99`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `projet.lire`.

The lookup uses the visible entity scope for `project`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `121–215`.

## `post` — Create a task

**Arguments** `request_data = null` (collection).

The request-field validator requires `ref`, `label`, `fk_project`.

**Access** The decision uses right `projet.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `227–300` with `_validate 1021–1034`.

## `getTimespent` — Read timespent

Route `GET {id}/timespent`.

**Arguments** `id` (integer).

**Access** The decision uses right `projet.lire`, tasks record scope.

The method reads task time entries.

**Result** A collection of matching entries.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.

Source lines `312–335`.

## `getRoles` — Read roles

Route `GET {id}/roles`.

**Arguments** `id` (integer), `userid = 0` (integer).

**Access** The decision uses right `projet.lire`, tasks record scope.

The method loads role assignments.

**Result** Available contact-role assignments.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.

Source lines `350–379`.

## `put` — Update a task

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `projet.creer`, task record scope, right `projet.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.
- `500` — business operation failed.

Source lines `527–565` with `get 76–99`.

## `delete` — Delete a task

**Arguments** `id` (integer).

**Access** The decision uses right `projet.supprimer`, task record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.
- `500` — removal failed.

Source lines `579–603`.

## `getTimeSpentByID` — Read time spent by id

Route `GET {id}/getTimeSpent/{timespent_id}`.

**Arguments** `id` (integer), `timespent_id` (integer).

**Access** The decision uses right `projet.lire`, task record scope, time record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing, timespent missing.

Source lines `619–644`.

## `addTimeSpent` — Add time spent

Route `POST {id}/addtimespent`.

**Arguments** `id` (integer), `date` (date/time), `duration` (integer), `product_id = null` (integer), `user_id = 0` (integer), `note = ''` (text), `progress = -1` (integer).

**Access** The decision uses right `projet.creer`, project record scope.

The method records time.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.
- `500` — business operation failed.

Source lines `669–715`.

## `putTimeSpent` — Put time spent

Route `PUT {id}/timespent/{timespent_id}`.

**Arguments** `id` (integer), `timespent_id` (integer), `date` (date/time), `duration` (integer), `product_id = null` (integer), `user_id = 0` (integer), `note = ''` (text).

**Access** The decision uses right `projet.creer`, task record scope.

The method amends recorded time.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied.
- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

Source lines `739–773`.

## `deleteTimeSpent` — Delete time spent

Route `DELETE {id}/timespent/{timespent_id}`.

**Arguments** `id` (integer), `timespent_id` (integer).

**Access** The decision uses right `projet.supprimer`, task record scope.

The method removes recorded time.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `500` — removal failed.

Source lines `789–810`.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `projet.lire`, task record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.

Source lines `1051–1072`.

## `addContact` — Add contact

Route `POST {id}/contacts`.

**Arguments** `id` (integer), `fk_socpeople` (integer), `type_contact` (text), `source` (text), `notrigger = 0` (integer).

**Access** The decision uses right `projet.creer`, task record scope.

The method attaches a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.
- `500` — business operation failed.

Source lines `1094–1120`.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contacts/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `projet.creer`, task record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — task missing.
- `500` — removal failed.

Source lines `1139–1169`.
