# Bills of materials

A bill defines the components needed to make an output. The header, its individual component rows and the validation transition have separate operations. Producing finished units belongs to the production-order service.

The implementation locations below refer to `htdocs/bom/class/api_boms.class.php`.

## `get` — Read a bill of materials

Route `GET {id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `bom.read`, bill of materials record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.

Source lines `72–88`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `bom.read`.

The bill list applies the entity scope of the model and the supplied search criteria. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `110–183`.

## `post` — Create a bill of materials

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `bom.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `196–220` with `_validate 662–678`.

## `put` — Update a bill of materials

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `bom.write`, bill of materials record scope, right `bom.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.
- `500` — business operation failed.

Source lines `237–278` with `get 72–88`.

## `validate` — Validate a bill of materials

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `bom.write`.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — access refused.
- `404` — bom missing.
- `500` — business operation failed.

Source lines `294–314`.

## `delete` — Delete a bill of materials

**Arguments** `id` (integer).

**Access** The decision uses right `bom.delete`, bill of materials record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.
- `500` — removal failed.

Source lines `328–352`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer).

**Access** The decision uses right `bom.read`, bom bom record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.

Source lines `368–388`.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `fk_product`, `qty`, `qty_frozen`, `disable_stock_change`, `efficiency`, `position`, `fk_bom_child`, `import_key`, `fk_unit`, `array_options`, `fk_default_workstation`.

**Access** The decision uses right `bom.write`, bom bom record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.
- `500` — business operation failed.

Source lines `406–442`.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `qty`, `qty_frozen`, `disable_stock_change`, `efficiency`, `position`, `import_key`, `fk_unit`, `array_options`, `fk_default_workstation`.

**Access** The decision uses right `bom.write`, bom bom record scope.

The method amends a line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this BOM.
- `404` — bom missing, bom line missing.

Source lines `460–506`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `bom.write`, bom bom record scope.

The method removes a line.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — bom missing.
- `500` — removal failed, business operation failed.

Source lines `525–563`.
