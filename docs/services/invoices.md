# Customer invoices and settlement

Invoice retrieval calculates the remaining balance after payments, credit notes and deposits. The service separately exposes conversion from orders or contracts, fixed discounts, credit-note application, single-invoice receipts, distributed receipts and recurring templates.

## `get` — Read a customer invoice

**Arguments** `id` (integer), `contact_list = 1` (integer), `properties = ''` (text), `withLines = true` (boolean).

**Access** The decision uses right `facture.lire`, invoice record scope.

The properties selector projects the returned fields. The returned balance deducts allocated receipts, applied credit notes and applied deposits from the invoice total. The detail reader loads linked credit-note identifiers and an online payment address.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no invoice can be found with no criteria.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref` (text), `contact_list = 1` (integer).

**Access** The decision uses right `facture.lire`, invoice record scope.

**Result** A record with internal service properties removed.

- `400` — no invoice can be found with no criteria.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `getByRefExt` — Read by external reference

Route `GET ref_ext/{ref_ext}`.

**Arguments** `ref_ext` (text), `contact_list = 1` (integer).

**Access** The decision uses right `facture.lire`, invoice record scope.

**Result** A record with internal service properties removed.

- `400` — no invoice can be found with no criteria.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `status = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer), `withLines = true` (boolean).

**Access** The decision uses right `facture.lire`.

The lookup uses the visible entity scope for `invoice`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method reads allocated payments, reads applied credits, reads applied deposits, loads related credit notes, loads contacts by role, and loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a customer invoice

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`.

Named body fields used by the handler include `date_lim_reglement`.

**Access** The decision uses right `facture.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, requested entity differs from the acting entity.
- `404` — party missing.
- `500` — business operation failed.

## `createInvoiceFromOrder` — Create invoice from order

Route `POST /createfromorder/{orderid}`.

**Arguments** `orderid` (integer).

**Access** The decision uses right `commande.lire`, right `facture.creer`, order record scope.

The method creates the document from the order and loads related business records. The source order must have progressed beyond draft and must still be unbilled. A previously billed order and a draft order are both ineligible for this conversion.

**Result** A record with internal service properties removed.

- `400` — order id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — order missing.
- `405` — order is not eligible for invoicing: its status does not allow creating an invoice, operation unavailable.

## `createInvoiceFromContract` — Create invoice from contract

Route `POST /createfromcontract/{contractid}`.

**Arguments** `contractid` (integer).

**Access** The decision uses right `contrat.lire`, right `facture.creer`, contract record scope.

The method creates an invoice from contract lines and loads related business records.

**Result** A record with internal service properties removed.

- `400` — contract id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `405` — operation unavailable.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.lire`, invoice record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `label`, `subprice`, `qty`, `remise_percent`, `date_start`, `date_end`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `price_base_type`, `info_bits`, `product_type`, `fk_parent_line`, `fk_fournprice`, `pa_ht`, `special_code`, `array_options`, `situation_percent`, `fk_unit`, `multicurrency_subprice`, `ref_ext`, `rang`.

**Access** The decision uses right `facture.creer`, invoice record scope.

The method amends a line.

**Result** A record with internal service properties removed.

- `304` — unchanged state.
- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this invoice.
- `404` — invoice missing, invoice line missing.

## `postContact` — Attach a contact role

Route `POST {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text), `source = 'external'` (text), `notrigger = 0` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method attaches a participant role.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — source required, unknown contact source and role combination, type required, duplicate record or association, invalid request data, access refused, dB_ERROR_RECORD_ALREADY_EXISTS.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.
- `503` — query or persistence failure.

## `getContacts` — List attached contacts

Route `GET {id}/contacts`.

**Arguments** `id` (integer), `type = ''` (text).

**Access** The decision uses right `facture.lire`, invoice record scope.

The method loads contacts by role.

**Result** A collection of attached contacts and their roles.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `deleteContact` — Remove a contact role

Route `DELETE {id}/contact/{contactid}/{type}`.

**Arguments** `id` (integer), `contactid` (integer), `type` (text).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method loads contacts by role and removes a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — removal failed.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope, right `facture.lire`.

The method removes a line. Only an invoice in draft state accepts line deletion through this method.

**Result** The selected record with its response fields projected or cleaned.

- `400` — line id required, no invoice can be found with no criteria.
- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — invoice missing.
- `405` — operation unavailable.

## `put` — Update a customer invoice

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `facture.creer`, invoice record scope, right `facture.lire`.

The optional caller marker is placed in event context for synchronization. The method calculates the payment due date and records a bank-account association.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no invoice missing, invalid request data, no invoice can be found with no criteria.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `delete` — Delete a customer invoice

**Arguments** `id` (integer).

**Access** The decision uses right `facture.supprimer`, invoice record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no invoice missing.
- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — invoice missing.
- `500` — removal failed.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `label`, `product_type`, `fk_parent_line`, `subprice`, `remise_percent`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_fournprice`, `pa_ht`, `qty`, `fk_product`, `date_start`, `date_end`, `fk_code_ventilation`, `info_bits`, `fk_remise_except`, `price_base_type`, `rang`, `special_code`, `origin`, `origin_id`, `array_options`, `situation_percent`, `fk_prev_id`, `fk_unit`, `ref_ext`.

**Access** The decision uses right `facture.creer`, invoice record scope.

The method adds a line.

**Result** The identifier returned by the line insertion.

- `400` — line creation failed.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `addContact` — Add contact

Route `POST {id}/contacts`.

**Arguments** `id` (integer), `fk_socpeople` (integer), `type_contact` (text), `source` (text), `notrigger = 0` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method attaches a participant role.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `settodraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id` (integer), `idwarehouse = -1` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method restores draft state.

**Result** A record with internal service properties removed.

- `304` — no transition applied.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `validate` — Validate a customer invoice

Route `POST {id}/validate`.

**Arguments** `id` (integer), `force_number = ''` (text), `idwarehouse = 0` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `settopaid` — Mark paid

Route `POST {id}/settopaid`.

**Arguments** `id` (integer), `close_code = ''` (text), `close_note = ''` (text).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method records paid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `settounpaid` — Return to unpaid

Route `POST {id}/settounpaid`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method restores unpaid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed.

## `getDiscount` — Read discount

Route `GET {id}/discount`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.lire`, invoice record scope.

**Result** The selected record with its response fields projected or cleaned.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing, discount missing.
- `500` — business operation failed.

## `markAsCreditAvailable` — Mark as credit available

Route `POST {id}/markAsCreditAvailable`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The lookup uses the visible entity scope for `invoice`. The method records paid status. The method opens a database transaction and provides commit and rollback paths. This operation turns the source credit-note balance into usable credit. Applying the available credit to a destination invoice is a separate operation with its own invoice and discount identifiers.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `500` — business operation failed, could not set paid.

## `useDiscount` — Use discount

Route `POST {id}/usediscount/{discountid}`.

**Arguments** `id` (integer), `discountid` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method records a discount.

**Result** The result of applying the fixed discount to the invoice.

- `400` — invoice id required, discount id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `405` — operation unavailable.

## `useCreditNote` — Use credit note

Route `POST {id}/usecreditnote/{discountid}`.

**Arguments** `id` (integer), `discountid` (integer).

**Access** The decision uses right `facture.creer`, invoice record scope.

The method links the credit to the invoice.

**Result** The integer result of associating the available credit with the invoice.

- `400` — invoice id required, credit id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — credit missing.
- `405` — operation unavailable.

## `getPayments` — Read payments

Route `GET {id}/payments`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.lire`, invoice record scope.

The method reads linked payment allocations.

**Result** Payment records or allocations associated with the selected parent.

- `400` — invoice id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.
- `405` — operation unavailable.

## `addPayment` — Add payment

Route `POST {id}/payments`.

**Arguments** `id` (integer), `datepaye` (text), `paymentid` (integer), `closepaidinvoices` (text), `accountid` (integer), `num_payment = ''` (text), `comment = ''` (text), `chqemetteur = ''` (text), `chqbank = ''` (text).

**Access** The decision uses right `facture.paiement`, invoice record scope.

The method reads allocated payments, reads applied credits, reads applied deposits, and posts and links the bank entry. The method opens a database transaction and provides commit and rollback paths. The amount is the outstanding balance after receipt, credit and deposit allocations. A credit note uses a negative amount. Closing covered invoices is controlled by the close-paid option. With banking active this path also posts the payment to the selected account and requires an issuer for a cheque.

**Result** The record identifier.

- `400` — invoice id required, account id required, payment id or payment code required, invalid request data, emetteur required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice missing.

## `addPaymentDistributed` — Add payment distributed

Route `POST /paymentsdistributed`.

**Arguments** `arrayofamounts` (collection), `datepaye` (text), `paymentid` (integer), `closepaidinvoices` (text), `accountid` (integer), `num_payment = ''` (text), `comment = ''` (text), `chqemetteur = ''` (text), `chqbank = ''` (text), `ref_ext = ''` (text), `accepthigherpayment = false` (boolean).

**Access** The decision uses right `facture.paiement`, invoice record scope.

The method reads allocated payments, reads applied credits, reads applied deposits, and posts and links the bank entry. The method opens a database transaction and provides commit and rollback paths. Each keyed invoice may use an explicit amount or the remaining balance after receipts, credit notes and deposits. Choose either entity or document currency for a given allocation. The service compares absolute values to detect overpayment unless explicitly permitted. Credit-note shares are forced negative. For invoices with balances of 60 and 40, assigning 50 and “remain” creates one receipt allocated 50 and 40, leaving 10 on the first invoice.

**Result** The record identifier.

- `400` — invoice id required, account id required, payment id or payment code required, invalid request data, amount exceeds the open balance, emetteur required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — invoice id missing.

## `putPayment` — Put payment

Route `PUT payments/{id}`.

**Arguments** `id` (integer), `num_payment = ''` (text).

**Access** The decision uses right `facture.paiement`, invoice record scope.

The method changes the payment number.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — payment id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — payment missing.
- `500` — business operation failed.

## `getTemplateInvoice` — Read template invoice

Route `GET templates/{id}`.

**Arguments** `id` (integer), `contact_list = 1` (integer).

**Access** The decision uses right `facture.lire`, facturerec record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — template invoice missing.

## `indexTemplateInvoices` — Index template invoices

Route `GET templates`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `status = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `loadlinkedobjects = 0` (integer), `withLines = true` (boolean).

**Access** The decision uses right `facture.lire`.

The lookup uses the visible entity scope for `invoice`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method loads related business records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.
