# Field interventions

A work report combines a customer, intervention lines and people with assigned contact roles. Draft, validation and closure concern the report header, while line methods address work details individually.

## `get` — Read a field intervention

**Arguments** `id` (integer), `ref = ''` (text), `ref_ext = ''` (text), `contact_list = 1` (integer).

**Access** The decision uses right `ficheinter.lire`, fichinter record scope.

The method loads contacts by role and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `contact_type = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer).

**Access** The decision uses right `ficheinter.lire`.

The lookup uses the visible entity scope for `intervention`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads contacts by role and loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a field intervention

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`, `fk_project`, `description`.

**Access** The decision uses right `ficheinter.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a field intervention

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `ficheinter.creer`, fichinter record scope, right `ficheinter.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — fichinter missing, intervention missing.
- `500` — business operation failed.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

The request-field validator requires `description`, `date`, `duration`.

**Access** The decision uses right `ficheinter.creer`, fichinter record scope.

The optional caller marker is placed in event context for synchronization. The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — invalid request data, required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.

## `delete` — Delete a field intervention

**Arguments** `id` (integer).

**Access** The decision uses right `ficheinter.supprimer`, fichinter record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.
- `500` — removal failed.

## `validate` — Validate a field intervention

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `ficheinter.creer`, fichinter record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.
- `500` — business operation failed.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `ficheinter.creer`, fichinter record scope.

The method closes the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.
- `500` — business operation failed.

## `deleteLine` — Remove a line

Route `DELETE /{id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `ficheinter.creer`, intervention record scope.

The method removes a line. Only a draft field intervention accepts this line removal.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, access or input restriction, record outside the caller’s scope, line does not belong to this intervention.
- `404` — intervention missing, intervention line missing.
- `405` — operation unavailable.

## `settodraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id` (integer).

**Access** The decision uses right `ficheinter.creer`, intervention record scope.

The method restores draft state and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already set).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — intervention missing.
- `500` — business operation failed.

## `addContact` — Add contact

Route `POST {id}/contacts`.

**Arguments** `id` (integer), `fk_socpeople` (integer), `type_contact` (text), `source` (text), `notrigger = 0` (integer).

**Access** The decision uses right `ficheinter.creer`, intervention record scope.

The method attaches a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — interventional missing.
- `500` — business operation failed.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text), `source = ''` (text).

**Access** The decision uses right `ficheinter.lire`, intervention record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — interventional missing.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `ficheinter.creer`, intervention record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — interventional missing.
- `500` — removal failed.

## `putLine` — Amend a line

Route `PUT /{id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data` (collection).

Named body fields used by the handler include `desc`, `description`, `date`, `duration`, `rang`.

**Access** The decision uses intervention record scope.

Only a draft field intervention accepts this line change.

**Result** A record with internal service properties removed.

- `403` — access or input restriction, record outside the caller’s scope, line does not belong to this intervention.
- `404` — intervention missing, intervention line missing.
- `500` — business operation failed.
