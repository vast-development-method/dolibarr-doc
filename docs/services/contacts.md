# Party contacts

A person can be resolved by identifier or email, linked to categories and used as the origin for a user account. The contact and the resulting user have separate identifiers.

## `get` — Read a contact

**Arguments** `id` (integer), `includecount = 0` (integer), `includeroles = 0` (integer).

**Access** The decision uses right `societe.contact.lire`, contact record scope.

The method reads the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.

## `getByEmail` — Read by email address

Route `GET email/{email}`.

**Arguments** `email` (text), `includecount = 0` (integer), `includeroles = 0` (integer).

**Access** The decision uses right `societe.contact.lire`, contact record scope.

The method reads the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `category = 0` (integer), `sqlfilters = ''` (text), `includecount = 0` (integer), `includeroles = 0` (integer), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `societe.contact.lire`.

The lookup uses the visible entity scope for `contact`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method reads the email opt-out flag.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a contact

**Arguments** `request_data = null` (collection).

The request-field validator requires `lastname`.

Named body fields used by the handler include `country_id`, `country_code`.

**Access** The decision uses right `societe.contact.creer`, party record scope.

The optional caller marker is placed in event context for synchronization. The method loads additional fields and changes the email opt-out flag.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — country code missing, party missing.
- `500` — business operation failed.

## `put` — Update a contact

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.contact.creer`, contact record scope, party record scope, right `societe.contact.lire`.

The optional caller marker is placed in event context for synchronization. The method changes the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, party missing.
- `500` — business operation failed.

## `delete` — Delete a contact

**Arguments** `id` (integer).

**Access** The decision uses right `societe.contact.supprimer`, contact record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.
- `500` — removal failed.

## `createUser` — Create user

Route `POST {id}/createUser`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `login`, `password`.

**Access** The decision uses right `societe.contact.lire`, right `user.user.creer`, contact record scope.

The method creates a user from the contact and sets credentials.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.
- `500` — business operation failed.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`, contact record scope.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — missing operation rights, record outside the caller’s scope.
- `503` — query or persistence failure.

## `addCategory` — Add category

Route `PUT {id}/categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.contact.creer`, contact record scope, category record scope.

The method adds a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, category missing.

## `deleteCategory` — Delete category

Route `DELETE {id}/categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.contact.creer`, contact record scope, category record scope.

The method removes a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, category missing.
