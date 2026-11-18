# Salary liabilities and payments

Salary records and their payments can be read independently. Financial posting applies to a selected salary, while the service also offers a list of payments spanning salaries.

The implementation locations below refer to `htdocs/salaries/class/api_salaries.class.php`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text).

**Access** The decision uses one of `salaries.read` or `salaries.readchild` or `salaries.readall`.

The lookup uses the visible entity scope for `user`. The method resolves descendant records.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `78–136`.

## `get` — Read a salary record

**Arguments** `id` (integer).

**Access** The decision uses one of `salaries.read` or `salaries.readchild` or `salaries.readall`.

The method resolves descendant records.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — salary missing.

Source lines `146–174`.

## `post` — Create a salary record

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_user`, `label`, `amount`.

**Access** The decision uses right `salaries.write`.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `184–201` with `_validate 510–523`.

## `put` — Update a salary record

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `salaries.write`, one of `salaries.read` or `salaries.readchild` or `salaries.readall`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — salary missing.
- `500` — business operation failed.

Source lines `212–236` with `get 146–174`.

## `getAllPayments` — Read all payments

Route `GET /payments`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer).

**Access** The decision uses one of `salaries.read` or `salaries.readchild` or `salaries.readall`.

The lookup uses the visible entity scope for `salary`. The method resolves descendant records.

**Result** A collection of matching records.

- `403` — access refused.
- `503` — query or persistence failure.

Source lines `283–333`.

## `getPayments` — Read payments

Route `GET /payments/{pid}`.

**Arguments** `pid` (integer).

**Access** The decision uses right `salaries.readall`.

**Result** Payment records or allocations associated with the selected parent.

- `403` — access refused.
- `404` — paymentsalary missing.

Source lines `345–362`.

## `addPayment` — Add payment

Route `POST {id}/payments`.

**Arguments** `id` (integer), `request_data = null` (collection).

The request-field validator requires `paiementtype`, `datepaye`, `chid`, `amounts`.

Named body fields used by the handler include `accountid`.

**Access** The decision uses right `salaries.write`.

The method posts and links the bank entry. The method opens a database transaction and provides commit and rollback paths. When an amounts map is supplied its keys must belong to the salary named by the request. A caller cannot use one salary's payment command to distribute funds across other salaries.

**Result** The record identifier.

- `400` — amounts must be keyed by the salary id, invalid request data, required request field absent.
- `403` — access refused.
- `404` — salary missing.

Source lines `377–429` with `_validatepayments 533–550`.

## `updatePayment` — Update payment

Route `PUT {id}/payments`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `salaries.write`, one of `salaries.read` or `salaries.readchild` or `salaries.readall`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — payment salary missing, salary missing.
- `500` — business operation failed.

Source lines `444–468` with `get 146–174`.
