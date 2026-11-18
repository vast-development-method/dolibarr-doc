# Party contacts

A person can be resolved by identifier or email, linked to categories and used as the origin for a user account. The contact and the resulting user have separate identifiers.

The implementation locations below refer to `htdocs/societe/class/api_contacts.class.php`.

## `get` — Read a contact

**Arguments** `id`, `includecount = 0`, `includeroles = 0`.

**Access** The decision uses right `societe.contact.lire`, contact record scope.

The method reads the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.

Source lines `79–112`.

## `getByEmail` — Read by email address

Route `GET email/{email}`.

**Arguments** `email`, `includecount = 0`, `includeroles = 0`.

**Access** The decision uses right `societe.contact.lire`, contact record scope.

The method reads the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.

Source lines `129–162`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `thirdparty_ids = ''`, `category = 0`, `sqlfilters = ''`, `includecount = 0`, `includeroles = 0`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `societe.contact.lire`.

The lookup uses the visible entity scope for `contact`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method reads the email opt-out flag.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `186–327`.

## `post` — Create a contact

**Arguments** `request_data = null`.

The request-field validator requires `lastname`.

Named body fields used by the handler include `country_id`, `country_code`.

**Access** The decision uses right `societe.contact.creer`, party record scope.

The optional caller marker is placed in event context for synchronization. The method loads additional fields and changes the email opt-out flag.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — country code missing, party missing.
- `500` — business operation failed.

Source lines `341–394` with `_validate 718–729`.

## `put` — Update a contact

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `societe.contact.creer`, contact record scope, party record scope, right `societe.contact.lire`.

The optional caller marker is placed in event context for synchronization. The method changes the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, party missing.
- `500` — business operation failed.

Source lines `411–465` with `get 79–112`.

## `delete` — Delete a contact

**Arguments** `id`.

**Access** The decision uses right `societe.contact.supprimer`, contact record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.
- `500` — removal failed.

Source lines `477–502`.

## `createUser` — Create user

Route `POST {id}/createUser`.

**Arguments** `id`, `request_data = null`.

Named body fields used by the handler include `login`, `password`.

**Access** The decision uses right `societe.contact.lire`, right `user.user.creer`, contact record scope.

The method creates a user from the contact and sets credentials.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing.
- `500` — business operation failed.

Source lines `518–560`.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id`, `sortfield = "s.rowid"`, `sortorder = 'ASC'`, `limit = 0`, `page = 0`.

**Access** The decision uses right `categorie.lire`, contact record scope.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — missing operation rights, record outside the caller’s scope.
- `503` — query or persistence failure.

Source lines `577–596`.

## `addCategory` — Add category

Route `PUT {id}/categories/{category_id}`.

**Arguments** `id`, `category_id`.

**Access** The decision uses right `societe.contact.creer`, contact record scope, category record scope.

The method adds a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, category missing.

Source lines `613–639`.

## `deleteCategory` — Delete category

Route `DELETE {id}/categories/{category_id}`.

**Arguments** `id`, `category_id`.

**Access** The decision uses right `societe.contact.creer`, contact record scope, category record scope.

The method removes a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contact missing, category missing.

Source lines `655–681`.
