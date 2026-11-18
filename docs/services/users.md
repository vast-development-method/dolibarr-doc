# Users, groups and subscriptions

A login identity, group membership and notification subscription have separate lifecycles. User lookups can resolve login, email or record identifier. Group membership and notification operations require their own identifiers.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `user_ids = '0'` (text), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `user.user.lire`, administrator status.

The lookup uses the visible entity scope for `user`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `get` — Read a user

**Arguments** `id` (integer), `includepermissions = 0` (integer).

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

Identifier zero selects a specimen.

**Result** A record with internal service properties removed.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

## `getByLogin` — Read by login

Route `GET login/{login}`.

**Arguments** `login` (text), `includepermissions = 0` (integer).

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

## `getByEmail` — Read by email address

Route `GET email/{email}`.

**Arguments** `email` (text), `includepermissions = 0` (integer).

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

## `getInfo` — Read info

Route `GET /info`.

**Arguments** `includepermissions = 0` (integer).

**Access** The decision uses one of `user.self.creer` or `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing, user group missing.

## `post` — Create a user

**Arguments** `request_data = null` (collection).

Named body fields used by the handler include `login`.

**Access** The decision uses right `user.user.creer`, administrator status, right `user.user.password`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `403` — access refused.
- `405` — field unavailable for this write.
- `500` — required request field absent, business operation failed.

## `put` — Update a user

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses conditional rights `user.user.creer`, `user.user.write`, `user.self.creer`, `user.self.write`, administrator status, user record scope, right `user.user.password`, right `user.self.password`, right `user.user.lire`.

The optional caller marker is placed in event context for synchronization. The method changes the record state.

**Result** A record with internal service properties removed.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — account missing, user missing.
- `405` — field unavailable for this write.
- `500` — business operation failed.

## `setPassword` — Set password

Route `GET {id}/setPassword`.

**Arguments** `id` (integer), `send_password = false` (boolean).

**Access** The decision uses right `user.user.password`, right `user.self.password`, user record scope.

The method sets credentials.

**Result** An integer success indicator of 1.

- `403` — credential changes disabled by configuration, missing operation rights, record outside the caller’s scope.
- `404` — no matching rows.
- `500` — business operation failed.

## `getGroups` — Read groups

Route `GET {id}/groups`.

**Arguments** `id` (integer).

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A collection of matching entries.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

## `setGroup` — Set group

Route `GET {id}/setGroup/{group}`.

**Arguments** `id` (integer), `group` (integer), `entity = 1` (integer).

**Access** The decision uses right `user.user.creer`, administrator status, user record scope.

The method adds the user to a group.

**Result** An integer success indicator of 1.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.
- `500` — business operation failed.

## `postGroups` — Post groups

Route `POST /groups`.

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `user.group_advance.write`, administrator status.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier.
- `403` — access refused.
- `500` — business operation failed.

## `putGroups` — Put groups

Route `PUT /groups/{group}`.

**Arguments** `group` (integer), `request_data = null` (collection).

**Access** The decision uses right `user.group_advance.write`, administrator status, user record scope, conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — body includes a forbidden identifier, no usergroup missing.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — usergroup missing.
- `500` — business operation failed.

## `removeUserFromGroup` — Remove user from group

Route `POST {id}/remove-group/{group}`.

**Arguments** `id` (integer), `group` (integer).

**Access** The decision uses administrator status.

The method removes the user from a group.

**Result** Acknowledgement under `success` with `message`.

- `403` — access refused.
- `404` — user missing.
- `500` — business operation failed.

## `listGroups` — List groups

Route `GET /groups`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `group_ids = '0'` (text), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception.

The lookup uses the visible entity scope for `user`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `infoGroups` — Info groups

Route `GET /groups/{group}`.

**Arguments** `group` (integer), `load_members = 0` (integer), `includepermissions = 0` (integer).

**Access** The decision uses conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception, user record scope.

**Result** A record with internal service properties removed.

- `400` — no usergroup missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — usergroup missing.

## `delete` — Delete a user

**Arguments** `id` (integer).

**Access** The decision uses right `user.user.supprimer`, administrator status, user record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.
- `500` — business operation failed.

## `deleteGroups` — Delete groups

Route `DELETE /groups/{group}`.

**Arguments** `group` (integer).

**Access** The decision uses right `user.group_advance.delete`, administrator status, user record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — usergroup missing.
- `500` — business operation failed.

## `getUserNotification` — Read user notification

Route `GET {id}/notifications`.

**Arguments** `id` (integer).

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** Notification subscriptions.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — notification missing, no matching rows.

## `createUserNotification` — Create user notification

Route `POST {id}/notifications`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused, duplicate record or association.
- `404` — requested data unavailable.
- `500` — error creating User Notification, request_data missing event, business operation failed.

## `createUserNotificationByCode` — Create user notification by code

Route `POST {id}/notificationsbycode/{code}`.

**Arguments** `id` (integer), `code` (text), `request_data = null` (collection).

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused, duplicate record or association.
- `404` — requested data unavailable, action trigger code missing.
- `500` — business operation failed.

## `deleteUserNotification` — Delete user notification

Route `DELETE {id}/notifications/{notification_id}`.

**Arguments** `id` (integer), `notification_id` (integer).

**Access** The decision uses right `user.user.creer`.

**Result** The notification-removal result.

- `403` — access refused.

## `updateUserNotification` — Update user notification

Route `PUT {id}/notifications/{notification_id}`.

**Arguments** `id` (integer), `notification_id` (integer), `request_data = null` (collection).

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — requested data unavailable.
- `500` — business operation failed.
