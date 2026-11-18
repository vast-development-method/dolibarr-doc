# Currencies and exchange rates

The currency record can be resolved by identifier or code. Exchange rates have their own date-sensitive history. A rate update and an edit of the currency definition have distinct effects.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `multicurrency.currency.read`.

The lookup uses the visible entity scope for `multicurrency`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `get` — Read a currency

**Arguments** `id` (integer).

**Access** The decision uses right `multicurrency.currency.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.

## `getByCode` — Read by code

Route `GET /bycode/{code}`.

**Arguments** `code` (text).

**Access** The decision uses right `multicurrency.currency.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.

## `getRates` — Read rates

Route `GET {id}/rates`.

**Arguments** `id` (integer).

**Access** The decision uses right `multicurrency.currency.read`.

The method loads rate history.

**Result** Rate history for the selected currency.

- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.

## `post` — Create a currency

**Arguments** `request_data = null` (collection).

Named body fields used by the handler include `code`, `name`, `rate`.

**Access** The decision uses right `multicurrency.currency.write`.

The optional caller marker is placed in event context for synchronization. The method adds an exchange-rate row.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a currency

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `multicurrency.currency.write`, right `multicurrency.currency.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.

## `delete` — Delete a currency

**Arguments** `id` (integer).

**Access** The decision uses right `multicurrency.currency.delete`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — currency missing.
- `500` — removal failed.

## `updateRate` — Update rate

Route `PUT {id}/rates`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `rate`.

**Access** The decision uses right `multicurrency.currency.write`.

The method adds an exchange-rate row.

**Result** A record with internal service properties removed.

- `400` — required request field absent.
- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.
