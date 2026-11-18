# Classification and category membership

The category record and its links to classified objects have separate lifecycles. Membership can be changed by object identifier or reference. Asking for the types or objects of a category is a read operation.

The implementation locations below refer to `htdocs/categories/class/api_categories.class.php`.

## `get` — Read a category

**Arguments** `id` (integer), `include_childs = false` (boolean).

**Access** The decision uses right `categorie.lire`, category record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `81–108`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `type = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `categorie.lire`.

The lookup uses the visible entity scope for `category`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `128–185`.

## `getTypes` — Read types

Route `GET /types`.

**Access** The decision uses right `categorie.lire`.

**Result** A collection of matching entries.

- `403` — access refused.

Source lines `197–205`.

## `post` — Create a category

**Arguments** `request_data = null` (collection).

The request-field validator requires `label`, `type`.

**Access** The decision uses right `categorie.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `215–237` with `_validate 864–877`.

## `put` — Update a category

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `categorie.creer`, category record scope, right `categorie.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `250–290` with `get 81–108`.

## `delete` — Delete a category

**Arguments** `id` (integer).

**Access** The decision uses right `categorie.supprimer`, category record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — removal failed.

Source lines `301–325`.

## `getListForObject` — Read list for object

Route `GET /object/{type}/{id}`.

**Arguments** `id` (integer), `type` (text), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses one of `produit.lire` or `service.lire`, right `contact.lire`, right `societe.lire`, right `fournisseur.lire`, right `adherent.lire`, right `projet.lire`, right `knowledgemanagement.knowledgerecord.read`, right `agenda.allactions.read`, right `ficheinter.lire`, right `ticket.read`, right `user.lire`, right `stock.lire`.

The method reads classification links.

**Result** A collection of matching records.

- `403` — access or input restriction, access refused.
- `600` — domain operation rejected.

Source lines `346–397`.

## `linkObjectById` — Link object by id

Route `POST {id}/objects/{type}/{object_id}`.

**Arguments** `id` (integer), `type` (text), `object_id` (integer).

**Access** The decision uses right `categorie.lire`, category record scope, one of `produit.creer` or `service.creer`, right `societe.creer`, right `societe.contact.creer`, right `adherent.creer`, right `agenda.allactions.read`, right `projet.creer`.

The method adds a category link.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — invalid request data, this type is not recognized yet.
- `403` — access or input restriction, missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `413–501` with `_checkAccessToLinkedObject 973–994`.

## `linkObjectByRef` — Link object by ref

Route `POST {id}/objects/{type}/ref/{object_ref}`.

**Arguments** `id` (integer), `type` (text), `object_ref` (text).

**Access** The decision uses right `categorie.lire`, category record scope, one of `produit.creer` or `service.creer`, right `societe.creer`, right `societe.contact.creer`, right `adherent.creer`, right `agenda.allactions.read`.

The method adds a category link. The requested object type must match the category type. An existing category link is handled separately from other insertion errors.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — invalid request data, this type is not recognized yet.
- `403` — access or input restriction, missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `517–600` with `_checkAccessToLinkedObject 973–994`.

## `unlinkObjectById` — Unlink object by id

Route `DELETE {id}/objects/{type}/{object_id}`.

**Arguments** `id` (integer), `type` (text), `object_id` (integer).

**Access** The decision uses right `categorie.lire`, category record scope, one of `produit.creer` or `service.creer`, right `societe.creer`, right `societe.contact.creer`, right `adherent.creer`, right `agenda.allactions.read`.

The method removes a category link.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — this type is not recognized yet.
- `403` — access or input restriction, missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `616–686` with `_checkAccessToLinkedObject 973–994`.

## `unlinkObjectByRef` — Unlink object by ref

Route `DELETE {id}/objects/{type}/ref/{object_ref}`.

**Arguments** `id` (integer), `type` (text), `object_ref` (text).

**Access** The decision uses right `categorie.lire`, category record scope, one of `produit.creer` or `service.creer`, right `societe.creer`, right `societe.contact.creer`, right `adherent.creer`, right `agenda.allactions.read`.

The method removes a category link.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — this type is not recognized yet.
- `403` — access or input restriction, missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — business operation failed.

Source lines `702–772` with `_checkAccessToLinkedObject 973–994`.

## `getObjects` — Read objects

Route `GET {id}/objects`.

**Arguments** `id` (integer), `type` (text), `onlyids = 0` (integer).

**Access** The decision uses right `categorie.lire`, category record scope.

**Result** Objects classified under the selected category and object type.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — category missing.
- `500` — the "type" parameter required.
- `503` — record lookup or write failed.

Source lines `890–960`.
