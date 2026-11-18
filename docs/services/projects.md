# Projects and project participation

Project lookup supports local, internal, external and message references. Time summaries, roles and assignment links refer to the project or its tasks. Linking a participant and updating a project header are different writes.

## `get` — Read a project

**Arguments** `id` (integer).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project with supplied id missing.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project with supplied ref missing.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project with supplied ref_ext missing.

## `getByMsgId` — Read by msg id

Route `GET email_msgid/{email_msgid}`.

**Arguments** `email_msgid` (text).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project with supplied email_msgid missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `projet.lire`.

The lookup uses the visible entity scope for `project`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a project

**Arguments** `request_data = null` (collection).

The request-field validator requires `ref`, `title`.

**Access** The decision uses right `projet.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `addContact` — Add contact

This operation shares its route with `addToContact`. The final route table dispatches requests to the latter handler. [Route selection](route-selection.md)

Route `POST {id}/contacts`.

**Arguments** `id` (integer), `fk_socpeople` (integer), `type_contact` (text), `source` (text), `notrigger = 0` (integer).

**Access** The decision uses right `projet.creer`, intervention record scope.

The method attaches a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — business operation failed.

## `deleteContact` — Remove a contact role

This operation shares its route with `deleteToContact`. The final route table dispatches requests to the latter handler. [Route selection](route-selection.md)

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `projet.creer`, project record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — removal failed.

## `getLines` — Read document lines

Route `GET {id}/tasks`.

**Arguments** `id` (integer), `includetimespent = 0` (integer).

**Access** The decision uses right `projet.lire`, project record scope.

The method totals recorded time and reads task time entries.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.

## `getRoles` — Read roles

Route `GET {id}/roles`.

**Arguments** `id` (integer), `userid = 0` (integer).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads role assignments.

**Result** Available contact-role assignments.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.

## `put` — Update a project

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `projet.creer`, project record scope, right `projet.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing, project with supplied id missing.
- `500` — business operation failed.

## `delete` — Delete a project

**Arguments** `id` (integer).

**Access** The decision uses right `projet.supprimer`, project record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — removal failed.

## `validate` — Validate a project

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `projet.creer`, project record scope.

The method validates the record.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — business operation failed.

## `listTimespent` — List timespent

Route `GET /alltimespent`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `projet.lire`.

The lookup uses the visible entity scope for `project`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `projet.lire`, project record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.

## `addToContact` — Add to contact

Route `POST {id}/contacts`.

**Arguments** `id` (integer), `fk_socpeople` (integer), `type_contact` (text), `source` (text), `notrigger = 0` (integer), `affect_to_tasks = null` (integer list).

**Access** The decision uses right `projet.creer`, project record scope.

The method attaches a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — business operation failed.

## `deleteToContact` — Delete to contact

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `projet.creer`, project record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
- `500` — removal failed.

## `getTimespent` — Read timespent

Route `GET {id}/timespent`.

**Arguments** `id` (integer).

**Access** The decision uses right `projet.lire`, project record scope.

The method totals recorded time.

**Result** A collection of matching entries.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — project missing.
