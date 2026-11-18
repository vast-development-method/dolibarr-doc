# Contracts and service activation

Validation belongs to the contract header. Activation and termination belong to an identified service line with its own effective dates. Closing the contract is another transition.

The implementation locations below refer to `htdocs/contrat/class/api_contracts.class.php`.

## `get` — Read a contract

**Arguments** `id`, `properties = ''`, `withLines = true`.

**Access** The decision uses right `contrat.lire`, contract record scope.

The properties selector projects the returned fields. The method loads related business records.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

Source lines `71–95`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `thirdparty_ids = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`, `withLines = true`.

**Access** The decision uses right `contrat.lire`.

The lookup uses the visible entity scope for `contrat`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `119–215`.

## `post` — Create a contract

**Arguments** `request_data = null`.

The request-field validator requires `socid`, `date_contrat`.

**Access** The decision uses right `contrat.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — body includes a forbidden identifier, required request field absent.
- `403` — access refused, requested entity differs from the acting entity.
- `404` — party missing.
- `500` — business operation failed.

Source lines `230–286` with `_validate 1009–1022`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id`, `sortfield = "d.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `contrat.lire`, contract record scope.

The lookup uses the visible entity scope for `contrat`. The properties selector projects the returned fields.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `503` — query or persistence failure.

Source lines `308–385`.

## `postLine` — Add a line

Route `POST {id}/lines`.

**Arguments** `id`, `request_data = null`.

Named body fields used by the handler include `desc`, `price_base_type`, `subprice`, `qty`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `fk_product`, `remise_percent`, `date_start`, `date_end`, `subprice_excl_tax`, `info_bits`, `fk_fournprice`, `pa_ht`, `array_options`, `fk_unit`, `rang`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method adds a line.

**Result** The inserted line identifier, or false on an unsuccessful insertion.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

Source lines `399–444`.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`, `request_data = null`.

Named body fields used by the handler include `desc`, `price_base_type`, `subprice`, `qty`, `remise_percent`, `date_start`, `date_end`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `date_start_real`, `date_end_real`, `info_bits`, `fk_fourn_price`, `pa_ht`, `array_options`, `fk_unit`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method amends a line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this contract.
- `404` — contract missing, contract line missing.
- `500` — business operation failed.

Source lines `459–600`.

## `activateLine` — Activate line

Route `PUT {id}/lines/{lineid}/activate`.

**Arguments** `id`, `lineid`, `datestart`, `dateend = null`, `comment = null`.

**Access** The decision uses right `contrat.activer`, contract record scope.

The method activates a service line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

Source lines `618–642`.

## `unactivateLine` — Unactivate line

Route `PUT {id}/lines/{lineid}/unactivate`.

**Arguments** `id`, `lineid`, `datestart`, `comment = null`.

**Access** The decision uses right `contrat.desactiver`, contract record scope.

The method closes a service line.

**Result** The updated record on success. An unsuccessful business operation can return false.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.

Source lines `659–683`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`.

**Access** The decision uses right `contrat.creer`, contract record scope, right `contrat.lire`.

The method removes a line.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope, line does not belong to this contract.
- `404` — contract missing, contract line missing.
- `405` — operation unavailable.

Source lines `699–728` with `get 71–95`.

## `put` — Update a contract

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `contrat.creer`, party record scope, contract record scope, right `contrat.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** The selected record with its response fields projected or cleaned.

- `400` — no contract missing, body includes a forbidden identifier, changing entity of a contract using the APIs is not possible.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing, party missing.
- `500` — business operation failed.

Source lines `744–819` with `get 71–95`.

## `delete` — Delete a contract

**Arguments** `id`.

**Access** The decision uses right `contrat.supprimer`, contract record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — removal failed.

Source lines `835–862`.

## `validate` — Validate a contract

Route `POST {id}/validate`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method validates the record.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already validated).
- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — business operation failed.

Source lines `888–919`.

## `close` — Close the record

Route `POST {id}/close`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `contrat.creer`, contract record scope.

The method closes the contract lines.

**Result** Acknowledgement under `success` with `code`, `message`.

- `304` — no transition applied (possibly already close).
- `400` — no contract missing.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — contract missing.
- `500` — business operation failed.

Source lines `945–976`.
