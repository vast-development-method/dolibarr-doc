# Customer orders and fulfillment

An order can be created from a proposal. Its lines, role-based contacts, billing classification and shipments remain independently addressable. Creating a shipment starts from the order and a selected warehouse.

The implementation locations below refer to `htdocs/commande/class/api_orders.class.php`.

## `get` — Read a customer order

**Arguments** `id`, `contact_list = -1`.

**Access** The decision uses right `commande.lire`, order record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `71–74` with `_fetch 127–163`.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref`, `contact_list = -1`.

**Access** The decision uses right `commande.lire`, order record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `90–93` with `_fetch 127–163`.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext`, `contact_list = -1`.

**Access** The decision uses right `commande.lire`, order record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `109–112` with `_fetch 127–163`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `thirdparty_ids = ''`, `sqlfilters = ''`, `sqlfilterlines = ''`, `properties = ''`, `pagination_data = false`, `loadlinkedobjects = 0`.

**Access** The decision uses right `commande.lire`.

The lookup uses the visible entity scope for `commande`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads contacts by role and loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression, invalid request data.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `189–311`.

## `post` — Create a customer order

**Arguments** `request_data = null`.

The request-field validator requires `socid`, `date`.

**Access** The decision uses right `commande.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, requested entity differs from the acting entity.
- `404` — party missing.
- `500` — business operation failed.

Source lines `327–376` with `_validate 1382–1395`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id`.

**Access** The decision uses right `commande.lire`, order record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `390–410`.

## `getLine` — Read line

Route `GET {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`, `properties = ''`.

**Access** The decision uses right `commande.lire`, order record scope.

The properties selector projects the returned fields.

**Result** The selected record with its response fields projected or cleaned.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing, line missing.

Source lines `424–446`.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id`, `request_data = null`.

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `remise_percent`, `info_bits`, `fk_remise_except`, `price_base_type`, `date_start`, `date_end`, `product_type`, `rang`, `special_code`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `array_options`, `fk_unit`, `origin`, `origin_id`, `multicurrency_subprice`, `ref_ext`.

**Access** The decision uses right `commande.creer`, order record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `461–516`.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`, `request_data = null`.

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `remise_percent`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `price_base_type`, `info_bits`, `date_start`, `date_end`, `product_type`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `special_code`, `array_options`, `fk_unit`, `multicurrency_subprice`, `ref_ext`, `rang`.

**Access** The decision uses right `commande.creer`, order record scope.

The method amends a line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this order.
- `404` — order missing, order line missing.

Source lines `531–595`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`.

**Access** The decision uses right `commande.creer`, order record scope, right `commande.lire`.

The method removes a line.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `405` — operation unavailable.

Source lines `610–631` with `get 71–74`, `_fetch 127–163`.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id`, `type = ''`.

**Access** The decision uses right `commande.lire`, order record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `647–668`.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}`.

**Arguments** `id`, `contactid`, `type`, `source = "external"`, `notrigger = 0`.

**Access** The decision uses right `commande.creer`, order record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — source required, unknown contact source and role combination, type required, duplicate record or association, invalid request data, access refused, dB_ERROR_RECORD_ALREADY_EXISTS.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `503` — query or persistence failure.

Source lines `690–792`.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id`, `contactid`, `type`.

**Access** The decision uses right `commande.creer`, order record scope.

The method loads contacts by role and removes a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — removal failed.

Source lines `812–846`.

## `put` — Update a customer order

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `commande.creer`, order record scope, right `commande.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `400` — no order missing, invalid request data, no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `858–905` with `get 71–74`, `_fetch 127–163`.

## `delete` — Delete a customer order

**Arguments** `id`.

**Access** The decision uses right `commande.supprimer`, order record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no order missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — removal failed.

Source lines `916–943`.

## `validate` — Validate a customer order

Route `POST {id}/validate`.

**Arguments** `id`, `idwarehouse = 0`, `notrigger = 0`.

**Access** The decision uses right `commande.creer`, order record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `967–999`.

## `reopen` — Reopen the record

Route `POST {id}/reopen`.

**Arguments** `id`.

**Access** The decision uses right `commande.creer`, order record scope.

The method reopens the record.

**Result** The integer outcome from reopening the order.

- `304` — unchanged state.
- `400` — order id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `405` — operation unavailable.

Source lines `1019–1044`.

## `setinvoiced` — Classify as invoiced

Route `POST {id}/setinvoiced`.

**Arguments** `id`.

**Access** The decision uses right `commande.creer`, order record scope.

The method classifies the source as billed and loads related business records.

**Result** A record with internal service properties removed.

- `400` — order id required, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.

Source lines `1060–1085`.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `commande.creer`, order record scope.

The method closes the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `1097–1132`.

## `settodraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id`, `idwarehouse = -1`.

**Access** The decision uses right `commande.creer`, order record scope.

The method restores draft state and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `500` — business operation failed.

Source lines `1144–1179`.

## `createOrderFromProposal` — Create order from proposal

Route `POST /createfromproposal/{proposalid}`.

**Arguments** `proposalid`.

**Access** The decision uses right `propal.lire`, right `commande.creer`, proposal record scope.

The method creates the order from the proposal and loads related business records. The source identifier refers to a customer proposal. The service builds the new order from that proposal and returns the new order record.

**Result** A record with internal service properties removed.

- `400` — proposal id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.
- `405` — operation unavailable.

Source lines `1196–1227`.

## `getOrderShipments` — Read order shipments

Route `GET {id}/shipment`.

**Arguments** `id`.

**Access** The decision uses right `expedition.lire`, order record scope.

**Result** Shipment records associated with the order.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — shipments missing.
- `500` — query or persistence failure.

Source lines `1245–1290`.

## `createOrderShipment` — Create order shipment

Route `POST {id}/shipment/{warehouse_id}`.

**Arguments** `id`, `warehouse_id`.

**Access** The decision uses right `expedition.creer`, order record scope.

The new shipment retains the order as origin and uses its party. Each order row supplies the source-line identifier and ordered quantity, with the chosen warehouse assigned to its shipment line. Lines are supplied at creation so the shipment can expand kits. The returned number identifies the shipment.

**Result** The record identifier.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — warehouse missing, order missing.
- `500` — business operation failed.

Source lines `1307–1348`.
