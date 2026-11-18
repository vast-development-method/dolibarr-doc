# Support tickets and correspondence

A support case can be addressed by local identifier, business reference or tracking identifier. Adding a message records correspondence on a case. Editing the ticket header and assigning a contact role use separate operations.

The implementation locations below refer to `htdocs/ticket/class/api_tickets.class.php`.

## `get` — Read a ticket

**Arguments** `id` (integer), `contact_list = 1` (integer).

**Access** The decision uses right `ticket.read`, ticket record scope.

The detail reader includes message subject, text, creation and occurrence dates, author and privacy marker. External and internal contact-role identifiers are returned in separate fields when contact expansion is enabled.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.

Source lines `78–81` with `getCommon 133–211`.

## `getByTrackId` — Read by tracking identifier

Route `GET track_id/{track_id}`.

**Arguments** `track_id` (text), `contact_list = 1` (integer).

**Access** The decision uses right `ticket.read`, ticket record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.

Source lines `98–101` with `getCommon 133–211`.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text), `contact_list = 1` (integer).

**Access** The decision uses right `ticket.read`, ticket record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.

Source lines `118–121` with `getCommon 133–211`.

## `index` — List records

**Arguments** `socid = 0` (integer), `sortfield = "t.rowid"` (text), `sortorder = "ASC"` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `loadcontacts = 0` (integer), `pagination_data = false` (boolean).

**Access** The decision uses right `ticket.read`.

The lookup uses the visible entity scope for `ticket`. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads contacts by role.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `232–341`.

## `post` — Create a ticket

**Arguments** `request_data = null` (collection).

The request-field validator requires `subject`, `message`.

Named body fields used by the handler include `socid`.

**Access** The decision uses right `ticket.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `404` — party missing.
- `500` — business operation failed.

Source lines `351–395` with `_validate 637–650`.

## `postNewMessage` — Post new message

**Arguments** `request_data = null` (collection).

The request-field validator requires `track_id`, `message`.

Named body fields used by the handler include `return_action_id`, `attachments`.

**Access** The decision uses right `ticket.write`, ticket record scope.

The optional caller marker is placed in event context for synchronization. The method appends case correspondence. The ordinary response is the ticket identifier. When the extended response is requested, the result contains the ticket identifier and the agenda activity identifier for this particular message.

**Result** Ticket identifier, or a pair of ticket and activity identifiers when requested.

- `400` — failed to decode attachment, required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.
- `500` — business operation failed, file write failed, file move failed.

Source lines `407–529` with `_validateMessage 660–673`.

## `put` — Update a ticket

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `socid`.

**Access** The decision uses right `ticket.write`, ticket record scope, right `ticket.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing, party missing.
- `500` — business operation failed.

Source lines `540–593` with `get 78–81`, `getCommon 133–211`.

## `delete` — Delete a ticket

**Arguments** `id` (integer).

**Access** The decision uses right `ticket.delete`, ticket record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.
- `500` — removal failed.

Source lines `603–627`.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source = "external"` (text), `notrigger = 0` (integer).

**Access** The decision uses right `ticket.write`, ticket record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — source required, type required, contact type missing, duplicate record or association, invalid request data, access refused, dB_ERROR_RECORD_ALREADY_EXISTS, unknown error occurred.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — external contact missing, internal contact missing, ticket missing.

Source lines `788–877`.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source = "external"` (text).

**Access** The decision uses right `ticket.write`, ticket record scope.

The method loads contacts by role and removes a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — source required, type required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — ticket missing.
- `500` — removal failed.

Source lines `898–940`.
