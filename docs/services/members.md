# Members

The member record, its linked party and its subscriptions have separate identifiers. Lookup by external account first resolves the site and account key to exactly one party and then resolves its member. Date-series operations return membership statistics independently of individual records.

The implementation locations below refer to `htdocs/adherents/class/api_members.class.php`.

## `get` — Read a member

**Arguments** `id`.

**Access** The decision uses right `adherent.lire`, member record scope.

Identifier zero selects a specimen.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.

Source lines `74–95`.

## `getByThirdparty` — Read by party

Route `GET thirdparty/{thirdparty}`.

**Arguments** `thirdparty`.

**Access** The decision uses right `adherent.lire`, member record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.

Source lines `111–128`.

## `getByThirdpartyAccounts` — Read by party accounts

Route `GET thirdparty/accounts/{site}/{key_account}`.

**Arguments** `site`, `key_account`.

**Access** The decision uses right `societe.lire`, member record scope.

The lookup uses the visible entity scope for `adherent`. The site and external key must resolve to exactly one party-account row in membership entity scope. The service then resolves the party and its linked member. Several matches for that account key produce the same not-found response as an absent account.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, member missing, account key absent or ambiguous.

Source lines `142–177`.

## `getByThirdpartyEmail` — Read by party email

Route `GET thirdparty/email/{email}`.

**Arguments** `email`.

**Access** The decision uses right `adherent.lire`, member record scope.

The service resolves the party email first and then loads the membership attached to the resulting party identifier. An existing party without an associated member yields a missing-member response.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, member missing.

Source lines `193–216`.

## `getByThirdpartyBarcode` — Read by party barcode

Route `GET thirdparty/barcode/{barcode}`.

**Arguments** `barcode`.

**Access** The decision uses right `adherent.lire`, member record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, member missing.

Source lines `232–255`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `typeid = ''`, `category = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `adherent.lire`.

The lookup uses the visible entity scope for `adherent`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `281–360`.

## `post` — Create a member

**Arguments** `request_data = null`.

**Access** The decision uses right `adherent.creer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `405` — field unavailable for this write.
- `500` — business operation failed.

Source lines `373–403` with `_validate 544–562`.

## `put` — Update a member

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `adherent.creer`, member record scope, right `adherent.lire`.

The optional caller marker is placed in event context for synchronization. The method ends membership, validates the record, and excludes the member.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.
- `405` — field unavailable for this write.
- `500` — business operation failed.

Source lines `418–492` with `get 74–95`.

## `delete` — Delete a member

**Arguments** `id`.

**Access** The decision uses right `adherent.supprimer`, member record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.
- `500` — removal failed.

Source lines `506–533`.

## `getSubscriptions` — Read subscriptions

Route `GET {id}/subscriptions`.

**Arguments** `id`.

**Access** The decision uses right `adherent.cotisation.lire`, member record scope.

**Result** A collection of matching entries.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.

Source lines `669–690`.

## `createSubscription` — Create subscription

Route `POST {id}/subscriptions`.

**Arguments** `id`, `start_date`, `end_date`, `amount`, `label = ''`.

**Access** The decision uses right `adherent.cotisation.creer`, member record scope.

The method creates a coverage period.

**Result** The record identifier.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.
- `422` — business rule or input rejected.
- `500` — business operation failed.

Source lines `709–737`.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id`, `sortfield = "s.rowid"`, `sortorder = 'ASC'`, `limit = 0`, `page = 0`.

**Access** The decision uses right `categorie.lire`, member record scope.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member missing.
- `503` — query or persistence failure.

Source lines `756–781`.

## `getType` — Read type

Route `GET /types/{id}`.

**Arguments** `id`.

**Access** The decision uses right `adherent.lire`, member record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing.

Source lines `799–816`.

## `indexType` — Index type

Route `GET /types/`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `adherent.lire`.

The lookup uses the visible entity scope for `member_type`. The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `403` — access refused.
- `503` — invalid filter expression, query or persistence failure.

Source lines `840–909`.

## `postType` — Post type

Route `POST /types/`.

**Arguments** `request_data = null`.

**Access** The decision uses right `adherent.configurer`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `924–946` with `_validateType 1143–1156`.

## `putType` — Put type

Route `PUT /types/{id}`.

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `adherent.configurer`, member record scope, right `adherent.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing, member missing.
- `500` — business operation failed.

Source lines `963–1006` with `get 74–95`.

## `deleteType` — Delete type

Route `DELETE /types/{id}`.

**Arguments** `id`.

**Access** The decision uses right `adherent.configurer`, member record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — member type missing.
- `500` — removal failed.

Source lines `1022–1048`.

## `getNbByMonth` — Read nb by month

Route `GET stats/nbbymonth`.

**Arguments** `year`, `format = 0`.

**Access** The decision uses right `adherent.lire`.

**Result** A collection of matching entries.

- `403` — access refused.

Source lines `1064–1071`.

## `getNbByYear` — Read nb by year

Route `GET stats/nbbyyear`.

**Access** The decision uses right `adherent.lire`.

**Result** A collection of matching entries.

- `403` — access refused.

Source lines `1083–1090`.

## `getAmountByMonth` — Read amount by month

Route `GET stats/amountbymonth`.

**Arguments** `year`, `format = 0`.

**Access** The decision uses right `adherent.lire`.

**Result** A collection of matching entries.

- `403` — access refused.

Source lines `1104–1111`.

## `getLastModifiedMembers` — Read last modified members

Route `GET stats/lastmodifiedmembers`.

**Arguments** `max`.

**Access** The decision uses right `adherent.lire`.

**Result** A collection of matching entries.

- `403` — access refused.

Source lines `1126–1133`.
