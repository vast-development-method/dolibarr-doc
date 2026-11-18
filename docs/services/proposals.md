# Customer proposals

A proposal has separate line, contact and lifecycle operations. Sending a batch of lines, moving a proposal back to draft, closing it and classifying it as invoiced each use distinct methods.

The implementation locations below refer to `htdocs/comm/propal/class/api_proposals.class.php`.

## `get` — Read a proposal

**Arguments** `id` (integer), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `76–79` with `_fetch 134–166`.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `96–99` with `_fetch 134–166`.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `116–119` with `_fetch 134–166`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer).

**Access** The decision uses right `propal.lire`.

The lookup uses the visible entity scope for `propal`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads contacts by role and loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `190–297`.

## `post` — Create a proposal

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`.

**Access** The decision uses right `propal.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, requested entity differs from the acting entity.
- `404` — party missing.
- `500` — business operation failed.

Source lines `311–359` with `_validate 1221–1234`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `377–407`.

## `postLine` — Add a line

Route `POST {id}/line`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `remise_percent`, `price_base_type`, `info_bits`, `product_type`, `rang`, `special_code`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `date_start`, `date_end`, `array_options`, `fk_unit`, `origin`, `origin_id`, `multicurrency_subprice`, `fk_remise_except`.

**Access** The decision uses right `propal.creer`, proposal record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `425–479`.

## `postLines` — Add document lines

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `remise_percent`, `info_bits`, `product_type`, `rang`, `special_code`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `label`, `date_start`, `date_end`, `array_options`, `fk_unit`, `origin`, `origin_id`, `multicurrency_subprice`, `fk_remise_except`.

**Access** The decision uses right `propal.creer`, proposal record scope.

The method adds a line. The method opens a database transaction and provides commit and rollback paths. The service accepts one line record or a sequence. Inserts run in one database transaction. Failure on a line rolls back the set, including earlier successful inserts. Success returns the result of the last inserted line.

**Result** The result from the last inserted proposal line.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

Source lines `495–564`.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `remise_percent`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `price_base_type`, `info_bits`, `special_code`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `product_type`, `date_start`, `date_end`, `array_options`, `fk_unit`, `multicurrency_subprice`, `rang`.

**Access** The decision uses right `propal.creer`, proposal record scope.

The method amends a line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this proposal.
- `404` — proposal missing, proposal line missing.

Source lines `582–649`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope, right `propal.lire`.

The method removes a line.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing, commercial proposal missing.
- `405` — operation unavailable.

Source lines `665–686` with `get 76–79`, `_fetch 134–166`.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `propal.lire`, proposal record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.

Source lines `700–721`.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source = 'external'` (text), `notrigger = 0` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — source required, unknown contact source and role combination, type required, duplicate record or association, invalid request data, access refused, dB_ERROR_RECORD_ALREADY_EXISTS.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.
- `500` — business operation failed.
- `503` — query or persistence failure.

Source lines `744–850`.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.
- `500` — removal failed.

Source lines `868–896`.

## `put` — Update a proposal

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `propal.creer`, proposal record scope, right `propal.lire`.

The optional caller marker is placed in event context for synchronization. The method sets the due date.

**Result** A record with internal service properties removed.

- `400` — no proposal missing, no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing, commercial proposal missing.
- `500` — business operation failed.

Source lines `911–961` with `get 76–79`, `_fetch 134–166`.

## `delete` — Delete a proposal

**Arguments** `id` (integer).

**Access** The decision uses right `propal.supprimer`, proposal record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no proposal missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.
- `500` — removal failed.

Source lines `975–1003`.

## `settodraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method restores draft state and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already draft).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.
- `500` — business operation failed.

Source lines `1017–1052`.

## `validate` — Validate a proposal

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method validates the record and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.
- `500` — business operation failed.

Source lines `1076–1111`.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id` (integer), `status` (integer), `note_private = ''` (text), `notrigger = 0` (integer), `note_public = ''` (text).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method closes the proposal and loads related business records.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already closed).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing, proposal missing.
- `500` — business operation failed.

Source lines `1129–1164`.

## `setinvoiced` — Classify as invoiced

Route `POST {id}/setinvoiced`.

**Arguments** `id` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method classifies the source as billed and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing, proposal missing.
- `500` — business operation failed.

Source lines `1178–1210`.
