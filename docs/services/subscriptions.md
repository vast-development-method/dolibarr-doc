# Membership subscriptions

A subscription is one period and charge for one member. Use the subscription identifier to amend an existing period. The separate member service also exposes creation against a specific member.

## `get` — Read a membership subscription

**Arguments** `id` (integer).

**Access** The decision uses right `adherent.cotisation.lire`, member record scope.

The single-record read resolves access through the member and loads typed object links. The record reader maps stored `dateadh` to `dateh`, `subscription` to `amount`, and `note` to the public note. The displayed reference is the subscription row ID.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.

## `index` — List records

**Arguments** `sortfield = "dateadh"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `adherent.cotisation.lire`.

The query selects period IDs by joining `subscription.fk_adherent` to `adherent.rowid` and filtering the member entity. It applies the requested criteria before counting and sorting. Each returned ID is loaded and projected using the properties selector. The [staff register](../specification/people-and-services/member-subscription-register.md) uses a different default sort and can display a linked bank account.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `403` — access refused.
- `503` — invalid filter expression, query or persistence failure.

## `post` — Create a membership subscription

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_adherent`, `dateh`, `datef`, `amount`.

**Access** The decision uses right `adherent.cotisation.creer`, member record scope.

The service accepts an optional `caller` marker. At event time the subscription writer replaces its context with the member record, so an event consumer cannot rely on that marker being retained.

The creation date written to storage is the time of insertion. The writer uses the supplied type or the member’s type, stores `dateh` in `dateadh`, and rejects an end date at or before the start. The database enforces the combination of member and period start. Creation refreshes the member’s greatest end date, writes supplied typed object links, then emits `MEMBER_SUBSCRIPTION_CREATE` before commit. This operation by itself creates a period. Billing and bank collection are separate [financial actions](../specification/people-and-services/member-renewals-and-collections.md).

**Result** The record identifier. A second submission with the same member and start conflicts with the stored key. It does not return the original ID as an idempotent acknowledgement.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

## `put` — Update a membership subscription

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `adherent.creer`, member record scope, right `adherent.cotisation.lire`.

The service accepts an optional `caller` marker. At event time the subscription writer replaces its context with the member record, so an event consumer cannot rely on that marker being retained.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.
- `500` — business operation failed.

A successful update commits before the operation performs the ordinary read for its response. A failed read at this stage can follow a durable change. Omitted ordinary fields retain the loaded values. The update checks that the amount is numeric, writes the member, type, public note, stored dates, amount and optional bank reference, refreshes the linked member’s end date and emits `MEMBER_SUBSCRIPTION_MODIFY`. The writer contains no corresponding create-time date-order check, invoice repricing or new bank posting. Query the subscription and associated financial records before retrying an interrupted amendment.

## `delete` — Delete a membership subscription

**Arguments** `id` (integer).

**Access** The decision uses right `adherent.cotisation.creer`, member record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.
- `409` — removal failed.
- `500` — removal failed.
