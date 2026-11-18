# Outbound event targets

The target definition describes an outbound integration. Its operations edit the target or list available triggers. Delivering an event to a configured target occurs in the event dispatch path.

## `get` — Read an event target

**Arguments** `id` (integer).

**Access** The decision uses right `webhook.webhook_target.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — target missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `webhook.webhook_target.read`.

The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `404` — no matching rows.
- `503` — query or persistence failure.

## `post` — Create an event target

**Arguments** `request_data = null` (collection).

The request-field validator requires `url`, `trigger_codes`.

**Access** The decision uses right `webhook.webhook_target.write`.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update an event target

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `webhook.webhook_target.write`, right `webhook.webhook_target.read`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — target missing.
- `500` — business operation failed.

## `delete` — Delete an event target

**Arguments** `id` (integer).

**Access** The decision uses right `webhook.webhook_target.delete`.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — target missing.
- `500` — removal failed.

## `listOfTriggers` — List of triggers

Route `GET triggers`.

**Access** The decision uses right `webhook.webhook_target.read`.

**Result** A collection of matching records.

- `403` — access refused.
- `500` — event list unavailable.
