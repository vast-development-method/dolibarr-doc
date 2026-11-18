# Bank accounts and transactions

The account, bank entries and links from an entry to another business object are distinct records. A transfer posts a debit and a credit and links the two bank entries inside one database transaction.

The implementation locations below refer to `htdocs/compta/bank/class/api_bankaccounts.class.php`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `category = 0`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses right `banque.lire`.

The lookup uses the visible entity scope for `bank_account`. The properties selector projects the returned fields. The method evaluates the outstanding balance.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `71–126`.

## `get` — Read a bank account

**Arguments** `id`.

**Access** The decision uses right `banque.lire`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account missing.

Source lines `136–149`.

## `post` — Create a bank account

**Arguments** `request_data = null`.

The request-field validator requires `ref`, `label`, `type`, `currency_code`, `country_id`.

**Access** The decision uses right `banque.configurer`.

The optional caller marker is placed in event context for synchronization. The service supplies the current time as the opening-balance date before applying the request fields.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `159–184` with `_validate 413–426`.

## `transfer` — Transfer

Route `POST /transfer`.

**Arguments** `bankaccount_from_id = 0`, `bankaccount_to_id = 0`, `date = null`, `description = ""`, `amount = 0.0`, `amount_to = 0.0`, `cheque_number = ""`.

**Access** The decision uses right `banque.configurer`.

The method adds a line and links a bank entry to its counterpart. The method opens a database transaction and provides commit and rollback paths. A transfer between accounts in the same currency uses the source amount on both sides. For different currencies the caller supplies the destination amount. The source entry receives the negative source amount and the destination receives the positive destination amount. Both generated line identifiers are returned so a statement reconciliation can match each side independently.

**Result** Acknowledgement under `success` with `code`, `message`, `bank_id_from`, `bank_id_to`.

- `403` — access refused.
- `404` — source account missing, destination account missing.
- `422` — destination amount missing for cross-currency transfer, negative destination amount, source and destination coincide.
- `500` — business operation failed.

Source lines `210–325`.

## `put` — Update a bank account

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `banque.configurer`, right `banque.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account missing.
- `500` — business operation failed.

Source lines `336–372` with `get 136–149`.

## `delete` — Delete a bank account

**Arguments** `id`.

**Access** The decision uses right `banque.configurer`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — account missing.
- `500` — removal failed.

Source lines `382–403`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id`, `sqlfilters = ''`.

**Access** The decision uses right `banque.lire`.

**Result** A collection of line records for the selected parent.

- `400` — invalid filter expression.
- `403` — access refused.
- `404` — account missing.
- `503` — query or persistence failure.

Source lines `461–506`.

## `addLine` — Add line

Route `POST {id}/lines`.

**Arguments** `id`, `date`, `type`, `label`, `amount`, `category = 0`, `cheque_number = ''`, `cheque_writer = ''`, `cheque_bank = ''`, `accountancycode = ''`, `datev = null`, `num_releve = ''`.

**Access** The decision uses right `banque.modifier`.

The method adds a line.

**Result** The record identifier.

- `403` — access refused.
- `404` — account missing.
- `503` — record lookup or write failed.

Source lines `527–565`.

## `addLink` — Add link

Route `POST {id}/lines/{line_id}/links`.

**Arguments** `id`, `line_id`, `url_id`, `url`, `label`, `type`.

**Access** The decision uses right `banque.modifier`.

The method links a bank entry to its counterpart.

**Result** The record identifier.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `503` — record lookup or write failed.

Source lines `580–611`.

## `getLinks` — Read links

Route `GET {id}/lines/{line_id}/links`.

**Arguments** `id`, `line_id`.

**Access** The decision uses right `banque.lire`.

**Result** A collection of matching entries.

- `403` — access refused.
- `404` — account missing.

Source lines `626–644`.

## `getDetailAccountLine` — Read detail account line

Route `GET /lines/{line_id}`.

**Arguments** `line_id`.

**Access** The decision uses right `banque.lire`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — account line missing.

Source lines `655–668`.

## `updateLine` — Update line

Route `PUT {id}/lines/{line_id}`.

**Arguments** `id`, `line_id`, `label`.

**Access** The decision uses right `banque.modifier`.

The method updates the label.

**Result** The record identifier.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `503` — record lookup or write failed.

Source lines `680–709`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{line_id}`.

**Arguments** `id`, `line_id`.

**Access** The decision uses right `banque.modifier`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — line does not belong to this account.
- `403` — access refused.
- `404` — account missing, account line missing.
- `500` — removal failed.

Source lines `722–754`.

## `getBalance` — Read balance

Route `GET {id}/balance`.

**Arguments** `id`.

**Access** The decision uses right `banque.lire`.

The method evaluates the outstanding balance.

**Result** A numeric value.

- `403` — access refused.
- `404` — account missing.

Source lines `765–781`.
