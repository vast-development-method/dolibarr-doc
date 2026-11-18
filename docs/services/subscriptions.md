# Membership subscriptions

A subscription is one period and charge for one member. Use the subscription identifier to amend an existing period. The separate member service also exposes creation against a specific member.

The implementation locations below refer to `htdocs/adherents/class/api_subscriptions.class.php`.

## `get` — Read a membership subscription

**Arguments** `id`.

**Access** The decision uses right `adherent.cotisation.lire`, member record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.

Source lines `67–86`.

## `index` — List records

**Arguments** `sortfield = "dateadh"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `adherent.cotisation.lire`.

The lookup uses the visible entity scope for `adherent`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `403` — access refused.
- `503` — invalid filter expression, query or persistence failure.

Source lines `108–179`.

## `post` — Create a membership subscription

**Arguments** `request_data = null`.

The request-field validator requires `fk_adherent`, `dateh`, `datef`, `amount`.

**Access** The decision uses right `adherent.cotisation.creer`, member record scope.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope.
- `500` — business operation failed.

Source lines `192–219` with `_validate 330–340`.

## `put` — Update a membership subscription

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `adherent.creer`, member record scope, right `adherent.cotisation.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.
- `500` — business operation failed.

Source lines `234–275` with `get 67–86`.

## `delete` — Delete a membership subscription

**Arguments** `id`.

**Access** The decision uses right `adherent.cotisation.creer`, member record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — subscription missing.
- `409` — removal failed.
- `500` — removal failed.

Source lines `290–320`.
