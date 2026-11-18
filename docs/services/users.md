# Users, groups and subscriptions

A login identity, group membership and notification subscription have separate lifecycles. User lookups can resolve login, email or record identifier. Group membership and notification operations require their own identifiers.

The implementation locations below refer to `htdocs/user/class/api_users.class.php`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `user_ids = '0'`, `category = 0`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses right `user.user.lire`, administrator status.

The lookup uses the visible entity scope for `user`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `86–167`.

## `get` — Read a user

**Arguments** `id`, `includepermissions = 0`.

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

Identifier zero selects a specimen.

**Result** A record with internal service properties removed.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

Source lines `184–212`.

## `getByLogin` — Read by login

Route `GET login/{login}`.

**Arguments** `login`, `includepermissions = 0`.

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

Source lines `231–255`.

## `getByEmail` — Read by email address

Route `GET email/{email}`.

**Arguments** `email`, `includepermissions = 0`.

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

Source lines `274–298`.

## `getInfo` — Read info

Route `GET /info`.

**Arguments** `includepermissions = 0`.

**Access** The decision uses one of `user.self.creer` or `user.user.lire`, administrator status, user record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing, user group missing.

Source lines `315–345`.

## `post` — Create a user

**Arguments** `request_data = null`.

Named body fields used by the handler include `login`.

**Access** The decision uses right `user.user.creer`, administrator status, right `user.user.password`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `403` — access refused.
- `405` — field unavailable for this write.
- `500` — required request field absent, business operation failed.

Source lines `359–420`.

## `put` — Update a user

**Arguments** `id`, `request_data = null`.

**Access** The decision uses conditional rights `user.user.creer`, `user.user.write`, `user.self.creer`, `user.self.write`, administrator status, user record scope, right `user.user.password`, right `user.self.password`, right `user.user.lire`.

The optional caller marker is placed in event context for synchronization. The method changes the record state.

**Result** A record with internal service properties removed.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — account missing, user missing.
- `405` — field unavailable for this write.
- `500` — business operation failed.

Source lines `438–539` with `get 184–212`.

## `setPassword` — Set password

Route `GET {id}/setPassword`.

**Arguments** `id`, `send_password = false`.

**Access** The decision uses right `user.user.password`, right `user.self.password`, user record scope.

The method sets credentials.

**Result** An integer success indicator of 1.

- `403` — credential changes disabled by configuration, missing operation rights, record outside the caller’s scope.
- `404` — no matching rows.
- `500` — business operation failed.

Source lines `556–597`.

## `getGroups` — Read groups

Route `GET {id}/groups`.

**Arguments** `id`.

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** A collection of matching entries.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.

Source lines `615–641`.

## `setGroup` — Set group

Route `GET {id}/setGroup/{group}`.

**Arguments** `id`, `group`, `entity = 1`.

**Access** The decision uses right `user.user.creer`, administrator status, user record scope.

The method adds the user to a group.

**Result** An integer success indicator of 1.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.
- `500` — business operation failed.

Source lines `660–691`.

## `postGroups` — Post groups

Route `POST /groups`.

**Arguments** `request_data = null`.

**Access** The decision uses right `user.group_advance.write`, administrator status.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier.
- `403` — access refused.
- `500` — business operation failed.

Source lines `706–730`.

## `putGroups` — Put groups

Route `PUT /groups/{group}`.

**Arguments** `group`, `request_data = null`.

**Access** The decision uses right `user.group_advance.write`, administrator status, user record scope, conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — body includes a forbidden identifier, no usergroup missing.
- `403` — missing operation rights, record outside the caller’s scope, changing entity of a user using the APIs is not possible.
- `404` — usergroup missing.
- `500` — business operation failed.

Source lines `749–791` with `infoGroups 940–973`.

## `removeUserFromGroup` — Remove user from group

Route `POST {id}/remove-group/{group}`.

**Arguments** `id`, `group`.

**Access** The decision uses administrator status.

The method removes the user from a group.

**Result** Acknowledgement under `success` with `message`.

- `403` — access refused.
- `404` — user missing.
- `500` — business operation failed.

Source lines `808–838`.

## `listGroups` — List groups

Route `GET /groups`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `group_ids = '0'`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception.

The lookup uses the visible entity scope for `user`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `864–920`.

## `infoGroups` — Info groups

Route `GET /groups/{group}`.

**Arguments** `group`, `load_members = 0`, `includepermissions = 0`.

**Access** The decision uses conditional rights `user.user.lire`, `user.group_advance.read`, administrator status or configured login exception, user record scope.

**Result** A record with internal service properties removed.

- `400` — no usergroup missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — usergroup missing.

Source lines `940–973`.

## `delete` — Delete a user

**Arguments** `id`.

**Access** The decision uses right `user.user.supprimer`, administrator status, user record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — user missing.
- `500` — business operation failed.

Source lines `988–1021`.

## `deleteGroups` — Delete groups

Route `DELETE /groups/{group}`.

**Arguments** `group`.

**Access** The decision uses right `user.group_advance.delete`, administrator status, user record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — usergroup missing.
- `500` — business operation failed.

Source lines `1038–1065`.

## `getUserNotification` — Read user notification

Route `GET {id}/notifications`.

**Arguments** `id`.

**Access** The decision uses right `user.user.lire`, administrator status, user record scope.

**Result** Notification subscriptions.

- `400` — no user missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — notification missing, no matching rows.

Source lines `1084–1142`.

## `createUserNotification` — Create user notification

Route `POST {id}/notifications`.

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused, duplicate record or association.
- `404` — requested data unavailable.
- `500` — error creating User Notification, request_data missing event, business operation failed.

Source lines `1160–1201`.

## `createUserNotificationByCode` — Create user notification by code

Route `POST {id}/notificationsbycode/{code}`.

**Arguments** `id`, `code`, `request_data = null`.

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused, duplicate record or association.
- `404` — requested data unavailable, action trigger code missing.
- `500` — business operation failed.

Source lines `1221–1273`.

## `deleteUserNotification` — Delete user notification

Route `DELETE {id}/notifications/{notification_id}`.

**Arguments** `id`, `notification_id`.

**Access** The decision uses right `user.user.creer`.

**Result** The notification-removal result.

- `403` — access refused.

Source lines `1289–1306`.

## `updateUserNotification` — Update user notification

Route `PUT {id}/notifications/{notification_id}`.

**Arguments** `id`, `notification_id`, `request_data = null`.

**Access** The decision uses right `user.user.creer`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — requested data unavailable.
- `500` — business operation failed.

Source lines `1325–1351`.
