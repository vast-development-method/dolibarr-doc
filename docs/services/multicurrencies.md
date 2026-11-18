# Currencies and exchange rates

The currency record can be resolved by identifier or code. Exchange rates have their own date-sensitive history. A rate update and an edit of the currency definition have distinct effects.

The implementation locations below refer to `htdocs/multicurrency/class/api_multicurrencies.class.php`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses right `multicurrency.currency.read`.

The lookup uses the visible entity scope for `multicurrency`. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `60–110`.

## `get` — Read a currency

**Arguments** `id`.

**Access** The decision uses right `multicurrency.currency.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.

Source lines `122–134`.

## `getByCode` — Read by code

Route `GET /bycode/{code}`.

**Arguments** `code`.

**Access** The decision uses right `multicurrency.currency.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.

Source lines `147–159`.

## `getRates` — Read rates

Route `GET {id}/rates`.

**Arguments** `id`.

**Access** The decision uses right `multicurrency.currency.read`.

The method loads rate history.

**Result** Rate history for the selected currency.

- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.

Source lines `172–193`.

## `post` — Create a currency

**Arguments** `request_data = null`.

Named body fields used by the handler include `code`, `name`, `rate`.

**Access** The decision uses right `multicurrency.currency.write`.

The optional caller marker is placed in event context for synchronization. The method adds an exchange-rate row.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `205–247`.

## `put` — Update a currency

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `multicurrency.currency.write`, right `multicurrency.currency.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.

Source lines `260–289` with `get 122–134`.

## `delete` — Delete a currency

**Arguments** `id`.

**Access** The decision uses right `multicurrency.currency.delete`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — currency missing.
- `500` — removal failed.

Source lines `301–322`.

## `updateRate` — Update rate

Route `PUT {id}/rates`.

**Arguments** `id`, `request_data = null`.

Named body fields used by the handler include `rate`.

**Access** The decision uses right `multicurrency.currency.write`.

The method adds an exchange-rate row.

**Result** A record with internal service properties removed.

- `400` — required request field absent.
- `403` — access refused.
- `404` — currency missing.
- `500` — business operation failed.

Source lines `337–359`.
