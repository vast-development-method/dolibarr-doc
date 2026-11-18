# Contracts and service activation

Validation belongs to the contract header. Activation and termination belong to an identified service line with its own effective dates. Closing the contract is another transition.

## `get` — Read a contract

**Arguments** `id` (integer), `properties = ''` (text), `withLines = true` (boolean).

**Access** The decision uses right `contrat.lire`, contract record scope.

The properties selector projects the returned fields. The method loads related business records.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `thirdparty_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean), `withLines = true` (boolean).

**Access** The decision uses right `contrat.lire`.

The lookup uses the visible entity scope for `contrat`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a contract

**Arguments** `request_data = null` (collection).

The request-field validator requires `socid`, `date_contrat`.

**Access** The decision uses right `contrat.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, requested entity differs from the acting entity.
- `404` — party missing.
- `500` — business operation failed.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer), `sortfield = "d.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `contrat.lire`, contract record scope.

The lookup uses the visible entity scope for `contrat`. The properties selector projects the returned fields.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `503` — query or persistence failure.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `price_base_type`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `remise_percent`, `date_start`, `date_end`, `subprice_excl_tax`, `info_bits`, `fk_fournprice`, `pa_ht`, `array_options`, `fk_unit`, `rang`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method adds a line.

**Result** The inserted line identifier, or false on an unsuccessful insertion.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `desc`, `price_base_type`, `subprice`, `qty`, `remise_percent`, `date_start`, `date_end`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `date_start_real`, `date_end_real`, `info_bits`, `fk_fourn_price`, `pa_ht`, `array_options`, `fk_unit`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method amends a line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this contract.
- `404` — contract missing, contract line missing.
- `500` — business operation failed.

## `activateLine` — Activate line

Route `PUT {id}/lines/{lineid}/activate`.

**Arguments** `id` (integer), `lineid` (integer), `datestart` (text), `dateend = null` (text), `comment = null` (text).

**Access** The decision uses right `contrat.activer`, contract record scope.

The method activates a service line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

## `unactivateLine` — Unactivate line

Route `PUT {id}/lines/{lineid}/unactivate`.

**Arguments** `id` (integer), `lineid` (integer), `datestart` (text), `comment = null` (text).

**Access** The decision uses right `contrat.desactiver`, contract record scope.

The method closes a service line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `contrat.creer`, contract record scope, right `contrat.lire`.

The method removes a line.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this contract.
- `404` — contract missing, contract line missing.
- `405` — operation unavailable.

## `put` — Update a contract

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `contrat.creer`, party record scope, contract record scope, right `contrat.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing, body includes a forbidden identifier, changing entity of a contract using the APIs is not possible.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing, party missing.
- `500` — business operation failed.

## `delete` — Delete a contract

**Arguments** `id` (integer).

**Access** The decision uses right `contrat.supprimer`, contract record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — removal failed.

## `validate` — Validate a contract

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `contrat.creer`, contract record scope.

The method validates the record.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — business operation failed.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `contrat.creer`, contract record scope.

The method closes the contract lines.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already close).
- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — business operation failed.
