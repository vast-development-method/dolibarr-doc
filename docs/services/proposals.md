# Customer proposals

A proposal has separate line, contact and lifecycle operations. Sending a batch of lines, moving a proposal back to draft, closing it and classifying it as invoiced each use distinct methods.

## `get` — Read a proposal

**Arguments** `id` (integer), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text), `contact_list = 1` (integer).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A record with internal service properties removed.

- `400` — no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer).

**Access** The decision uses right `propal.lire`.

The lookup uses the visible entity scope for `propal`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads contacts by role and loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

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

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `propal.lire`, proposal record scope.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.

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

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `remise_percent`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `price_base_type`, `info_bits`, `special_code`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `product_type`, `date_start`, `date_end`, `array_options`, `fk_unit`, `multicurrency_subprice`, `rang`.

**Access** The decision uses right `propal.creer`, proposal record scope.

The method amends a line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this proposal.
- `404` — proposal missing, proposal line missing.

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

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `propal.lire`, proposal record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.

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

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing.
- `500` — removal failed.

## `put` — Update a proposal

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `propal.creer`, proposal record scope, right `propal.lire`.

The optional caller marker is placed in event context for synchronization. The method sets the due date.

**Result** A record with internal service properties removed.

- `400` — no proposal missing, no ID or Ref provided.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — proposal missing, commercial proposal missing.
- `500` — business operation failed.

## `delete` — Delete a proposal

**Arguments** `id` (integer).

**Access** The decision uses right `propal.supprimer`, proposal record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no proposal missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing.
- `500` — removal failed.

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

## `setinvoiced` — Classify as invoiced

Route `POST {id}/setinvoiced`.

**Arguments** `id` (integer).

**Access** The decision uses right `propal.creer`, proposal record scope.

The method classifies the source as billed and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — commercial proposal missing, proposal missing.
- `500` — business operation failed.
