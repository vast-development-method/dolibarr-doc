# Supplier orders

Validation, approval, placement with a supplier and receipt are separate phases of procurement. The order, its individual lines and its role-based contacts are independently addressable.

The implementation locations below refer to `htdocs/fourn/class/api_supplier_orders.class.php`.

## `get` — Read a supplier order

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.commande.lire`, supplier record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.

Source lines `65–82`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `product_ids = ''` (text), `status = ''` (text), `sqlfilters = ''` (text), `sqlfilterlines = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `fournisseur.commande.lire`.

The lookup uses the visible entity scope for `supplier_order`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression, invalid request data.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `106–236`.

## `post` — Create a supplier order

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`.

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `248–286` with `_validate 872–885`.

## `put` — Update a supplier order

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`, supplier record scope, right `fournisseur.commande.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.
- `500` — business operation failed.

Source lines `298–337` with `get 65–82`.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `fk_prod_fourn_price`, `ref_fourn`, `remise_percent`, `price_base_type`, `pu_ttc`, `product_type`, `info_bits`, `notrigger`, `date_start`, `date_end`, `array_options`, `fk_unit`, `multicurrency_subprice`, `origin`, `origin_id`, `rang`, `special_code`.

**Access** The decision uses right `fournisseur.commande.creer`, supplier record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.

Source lines `351–404`.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `source` (text), `type = ''` (text).

**Access** The decision uses right `fournisseur.commande.lire`, supplier record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.

Source lines `420–447`.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}/{source}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source` (text).

**Access** The decision uses right `fournisseur.commande.creer`, supplier record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — contact already added.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.
- `500` — business operation failed.

Source lines `465–496`.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}/{source}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source` (text).

**Access** The decision uses right `fournisseur.commande.creer`, supplier record scope.

The method loads contacts by role and removes a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing, linked contact missing.
- `500` — removal failed.

Source lines `516–557`.

## `delete` — Delete a supplier order

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.commande.supprimer`, supplier record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier order missing.
- `500` — removal failed.

Source lines `567–591`.

## `validate` — Validate a supplier order

Route `POST {id}/validate`.

**Arguments** `id` (integer), `idwarehouse = 0` (integer), `notrigger = 0` (integer).

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`, supplier record scope.

The method validates the record.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `615–643`.

## `approve` — Approve

Route `POST {id}/approve`.

**Arguments** `id` (integer), `idwarehouse = 0` (integer), `secondlevel = 0` (integer).

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`, supplier record scope.

The method approves the record. The caller can supply a warehouse and a second-level flag. These values are forwarded to the purchase-order approval operation.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already approved).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `666–694`.

## `makeOrder` — Make order

Route `POST {id}/makeorder`.

**Arguments** `id` (integer), `date` (integer), `method` (integer), `comment = ''` (text).

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`, supplier record scope.

The method records placement with the supplier.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already sent).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `720–748`.

## `receiveOrder` — Receive order

Route `POST {id}/receive`.

**Arguments** `id` (integer), `closeopenorder` (integer), `comment` (text), `lines` (collection).

**Access** The decision uses one of `fournisseur.commande.creer` or `supplier_order.creer`, supplier record scope.

The method records the stock receipt. The service dispatches each specified product line to its warehouse, with quantity and tracking data from the row. After the rows are processed it recalculates the order’s dispatch state and passes the close-if-complete choice. A partial receipt and a completed order are separate results.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already dispatched).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `787–838`.
