# Supplier quotations

Purchase-side quotes have their own record lifecycle. Their read and write rights and resource scope are evaluated on the supplier quotation.

The implementation locations below refer to `htdocs/supplier_proposal/class/api_supplier_proposals.class.php`.

## `delete` — Delete a supplier quotation

**Arguments** `id` (integer).

**Access** The decision uses right `supplier_proposal.supprimer`, supplier quotation record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier proposal missing.
- `500` — removal failed.

Source lines `64–88`.

## `get` — Read a supplier quotation

**Arguments** `id` (integer).

**Access** The decision uses right `supplier_proposal.lire`, supplier quotation record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier proposal missing.

Source lines `100–117`.

## `post` — Create a supplier quotation

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`.

**Access** The decision uses right `supplier_proposal.creer`.

The optional caller marker is placed in event context for synchronization. The method loads additional fields.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `127–166` with `_validate 333–346`.

## `put` — Update a supplier quotation

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `supplier_proposal.creer`, supplier quotation record scope, right `supplier_proposal.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier proposal missing.
- `500` — business operation failed.

Source lines `177–214` with `get 100–117`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `supplier_proposal.lire`.

The lookup uses the visible entity scope for `propal`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `233–323`.
