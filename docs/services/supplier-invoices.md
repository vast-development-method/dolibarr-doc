# Supplier invoices and disbursements

Supplier billing and payment use the purchase-side authorization scope. The service exposes payable invoice lines, supplier payments, draft restoration and paid or unpaid classifications.

For nested line request bodies, pricing and transaction outcomes, see [supplier invoice line inputs and pricing](supplier-invoice-line-inputs.md).

## `get` — Read a supplier invoice

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.facture.lire`, supplier record scope.

The method loads related credit notes and loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `status = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `fournisseur.facture.lire`.

The lookup uses the visible entity scope for `supplier_invoice`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a supplier invoice

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`.

**Access** The decision uses right `fournisseur.facture.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a supplier invoice

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope, right `fournisseur.facture.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.

## `delete` — Delete a supplier invoice

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.facture.supprimer`, supplier record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — supplier invoice missing.
- `500` — removal failed.

## `validate` — Validate a supplier invoice

Route `POST {id}/validate`.

**Arguments** `id` (integer), `idwarehouse = 0` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method validates the record.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `settodraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id` (integer), `idwarehouse = -1` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method restores draft state.

**Result** A record with internal service properties removed.

- `304` — no transition applied.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `getPayments` — Read payments

Route `GET {id}/payments`.

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.facture.lire`, supplier record scope.

The method reads linked payment allocations.

**Result** Payment records or allocations associated with the selected parent.

- `400` — invoice id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `405` — operation unavailable.

## `addPayment` — Add payment

Route `POST {id}/payments`.

**Arguments** `id` (integer), `datepaye` (integer), `payment_mode_id` (integer), `closepaidinvoices` (text), `accountid` (integer), `num_payment = ''` (text), `comment = ''` (text), `chqemetteur = ''` (text), `chqbank = ''` (text), `amount = null` (number).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method reads allocated payments, reads applied deposits, and posts and links the bank entry. The method opens a database transaction and provides commit and rollback paths.

**Result** The record identifier.

- `400` — invoice id required, bank account id required, payment mode id required, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `settopaid` — Mark paid

Route `POST {id}/settopaid`.

**Arguments** `id` (integer), `close_code = ''` (text), `close_note = ''` (text).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method records paid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already paid).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.
- `500` — business operation failed.

## `settounpaid` — Return to unpaid

Route `POST {id}/settounpaid`.

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method restores unpaid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.
- `500` — business operation failed.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer).

**Access** The decision uses right `fournisseur.facture.lire`, supplier record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `description`, `ref_supplier`, `pu_ht`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `qty`, `fk_product`, `remise_percent`, `date_start`, `date_end`, `fk_code_ventilation`, `info_bits`, `price_base_type`, `product_type`, `rang`, `array_options`, `fk_unit`, `origin_id`, `multicurrency_subprice`, `special_code`.

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — line creation failed.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — supplier invoice missing.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `description`, `ref_supplier`, `pu_ht`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `qty`, `fk_product`, `price_base_type`, `info_bits`, `product_type`, `remise_percent`, `date_start`, `date_end`, `array_options`, `fk_unit`, `multicurrency_subprice`, `rang`.

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method amends a line.

**Result** A record with internal service properties removed.

- `304` — line amendment or subsequent header repricing returned a nonpositive result.
- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this supplier invoice.
- `404` — supplier invoice missing, supplier invoice line missing.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `fournisseur.facture.creer`, supplier record scope.

The method removes a line.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — line id required.
- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this supplier invoice.
- `404` — supplier invoice missing, supplier invoice line missing.
- `405` — operation unavailable.
