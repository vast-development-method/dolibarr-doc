# Bank accounts and transactions

The account, bank entries and links from an entry to another business object are distinct records. A transfer posts a debit and a credit and links the two bank entries inside one database transaction.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `banque.lire`.

The lookup uses the visible entity scope for `bank_account`. The properties selector projects the returned fields. The method evaluates the outstanding balance.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `get` — Read a bank account

**Arguments** `id` (integer).

**Access** The decision uses right `banque.lire`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account missing.

## `post` — Create a bank account

**Arguments** `request_data = null` (collection).

The request-field validator requires `ref`, `label`, `type`, `currency_code`, `country_id`.

**Access** The decision uses right `banque.configurer`.

The optional caller marker is placed in event context for synchronization. The service supplies the current time as the opening-balance date before applying the request fields.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `transfer` — Transfer

Route `POST /transfer`.

**Arguments** `bankaccount_from_id = 0` (integer), `bankaccount_to_id = 0` (integer), `date = null` (text), `description = ""` (text), `amount = 0.0` (number), `amount_to = 0.0` (number), `cheque_number = ""` (text).

**Access** The decision uses right `banque.configurer`.

The method adds a line and links a bank entry to its counterpart. The method opens a database transaction and provides commit and rollback paths. A transfer between accounts in the same currency uses the source amount on both sides. For different currencies the caller supplies the destination amount. The source entry receives the negative source amount and the destination receives the positive destination amount. Both generated line identifiers are returned so a statement reconciliation can match each side independently.

**Result** Acknowledgement under `success` with `code`, `message`, `bank_id_from`, `bank_id_to`.

- `403` — access refused.
- `404` — source account missing, destination account missing.
- `422` — destination amount missing for cross-currency transfer, negative destination amount, source and destination coincide.
- `500` — business operation failed.

## `put` — Update a bank account

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `banque.configurer`, right `banque.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account missing.
- `500` — business operation failed.

## `delete` — Delete a bank account

**Arguments** `id` (integer).

**Access** The decision uses right `banque.configurer`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — account missing.
- `500` — removal failed.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `banque.lire`.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — access refused.
- `404` — account missing.
- `503` — query or persistence failure.

## `addLine` — Add line

Route `POST {id}/lines`.

**Arguments** `id` (integer), `date` (text), `type` (text), `label` (text), `amount` (number), `category = 0` (integer), `cheque_number = ''` (text), `cheque_writer = ''` (text), `cheque_bank = ''` (text), `accountancycode = ''` (text), `datev = null` (text), `num_releve = ''` (text).

**Access** The decision uses right `banque.modifier`.

The method adds a line.

**Result** The record identifier.

- `403` — access refused.
- `404` — account missing.
- `503` — record lookup or write failed.

## `addLink` — Add link

Route `POST {id}/lines/{line_id}/links`.

**Arguments** `id` (integer), `line_id` (integer), `url_id` (integer), `url` (text), `label` (text), `type` (text).

**Access** The decision uses right `banque.modifier`.

The method links a bank entry to its counterpart.

**Result** The record identifier.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `503` — record lookup or write failed.

## `getLinks` — Read links

Route `GET {id}/lines/{line_id}/links`.

**Arguments** `id` (integer), `line_id` (integer).

**Access** The decision uses right `banque.lire`.

**Result** A collection of matching entries.

- `403` — access refused.
- `404` — account missing.

## `getDetailAccountLine` — Read detail account line

Route `GET /lines/{line_id}`.

**Arguments** `line_id` (integer).

**Access** The decision uses right `banque.lire`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account line missing.

## `updateLine` — Update line

Route `PUT {id}/lines/{line_id}`.

**Arguments** `id` (integer), `line_id` (integer), `label` (text).

**Access** The decision uses right `banque.modifier`.

The method updates the label.

**Result** The record identifier.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `503` — record lookup or write failed.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{line_id}`.

**Arguments** `id` (integer), `line_id` (integer).

**Access** The decision uses right `banque.modifier`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `500` — removal failed.

## `getBalance` — Read balance

Route `GET {id}/balance`.

**Arguments** `id` (integer).

**Access** The decision uses right `banque.lire`.

The method evaluates the outstanding balance.

**Result** A numeric value.

- `403` — access refused.
- `404` — account missing.
