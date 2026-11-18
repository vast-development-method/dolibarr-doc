# Business partners and related accounts

The service manages customer and supplier identity, representatives, categories, price levels, account notifications, banking instructions, payment mandates and external site accounts. Several child operations require both the party identifier and the child identifier.

## `get` — Read a business partner

**Arguments** `id` (integer).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getByEmail` — Read by email address

Route `GET email/{email}`.

**Arguments** `email` (text).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getByBarcode` — Read by barcode

Route `GET barcode/{barcode}`.

**Arguments** `barcode` (text).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `mode = 0` (integer), `category = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `societe.lire`.

The lookup uses the visible entity scope for `societe`. A caller linked to a party receives that party restriction. The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields. The method reads the email opt-out flag.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `404` — no matching rows.
- `503` — query or persistence failure.

## `post` — Create a business partner

**Arguments** `request_data = null` (collection).

The request-field validator requires `name`.

Named body fields used by the handler include `country_id`, `country_code`.

**Access** The decision uses right `societe.creer`.

The optional caller marker is placed in event context for synchronization. The method loads additional fields and changes the email opt-out flag.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `404` — country code missing.
- `500` — business operation failed.

## `put` — Update a business partner

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope, right `societe.lire`.

The optional caller marker is placed in event context for synchronization. The method changes the email opt-out flag.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.
- `500` — business operation failed.

## `merge` — Merge

Route `PUT {id}/merge/{idtodelete}`.

**Arguments** `id` (integer), `idtodelete` (integer).

**Access** The decision uses right `societe.creer`, party record scope, right `societe.lire`.

The method merges party records.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.
- `500` — party merge failed.

## `delete` — Delete a business partner

**Arguments** `id` (integer).

**Access** The decision uses right `societe.supprimer`, party record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.
- `409` — removal failed.
- `500` — removal failed.

## `setThirdpartyPriceLevel` — Set party price level

Route `PUT {id}/setpricelevel/{priceLevel}`.

**Arguments** `id` (integer), `priceLevel` (integer).

**Access** The decision uses right `societe.creer`, party record scope.

The method sets the customer price level.

**Result** A record with internal service properties removed.

- `400` — price level must be between 1 and PRODUIT_MULTIPRICES_LIMIT.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.
- `500` — business operation failed.
- `501` — operation unavailable.

## `addRepresentative` — Add representative

Route `POST {id}/representative/{representative_id}`.

**Arguments** `id` (integer), `representative_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope.

The method assigns a sales representative.

**Result** The result of adding the representative association.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, user missing.

## `deleteRepresentative` — Delete representative

Route `DELETE {id}/representative/{representative_id}`.

**Arguments** `id` (integer), `representative_id` (integer).

**Access** The decision uses right `societe.supprimer`, party record scope.

The method removes a sales representative.

**Result** The result of removing the representative association.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, user missing.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — access refused.
- `404` — party missing, access refused.
- `503` — query or persistence failure.

## `addCategory` — Add category

Route `PUT {id}/categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope, category record scope.

The method adds a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, category missing.

## `deleteCategory` — Delete category

Route `DELETE {id}/categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope, category record scope.

The method removes a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, category missing.

## `getSupplierCategories` — Read supplier categories

Route `GET {id}/supplier_categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — access refused.
- `404` — party missing, access refused.
- `503` — query or persistence failure.

## `addSupplierCategory` — Add supplier category

Route `PUT {id}/supplier_categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope, category record scope.

The method adds a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, category missing.

## `deleteSupplierCategory` — Delete supplier category

Route `DELETE {id}/supplier_categories/{category_id}`.

**Arguments** `id` (integer), `category_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope, category record scope.

The method removes a category link.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, category missing.

## `getOutStandingProposals` — Read out standing proposals

Route `GET {id}/outstandingproposals`.

**Arguments** `id` (integer), `mode = 'customer'` (text).

**Access** The decision uses right `societe.lire`, party record scope.

The method totals open proposals.

**Result** A collection of matching entries.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getOutStandingOrder` — Read out standing order

Route `GET {id}/outstandingorders`.

**Arguments** `id` (integer), `mode = 'customer'` (text).

**Access** The decision uses right `societe.lire`, party record scope.

The method totals open orders.

**Result** A collection of matching entries.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getOutStandingInvoices` — Read out standing invoices

Route `GET {id}/outstandinginvoices`.

**Arguments** `id` (integer), `mode = 'customer'` (text).

**Access** The decision uses right `societe.lire`, party record scope.

The method totals open invoices.

**Result** A collection of matching entries.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getSalesRepresentatives` — Read sales representatives

Route `GET {id}/representatives`.

**Arguments** `id` (integer), `mode = 0` (integer).

**Access** The decision uses right `societe.lire`, party record scope.

The method loads assigned representatives.

**Result** A collection of matching entries.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.

## `getFixedAmountDiscounts` — Read fixed amount discounts

Route `GET {id}/fixedamountdiscounts`.

**Arguments** `id` (integer), `mode = 'customer'` (text), `filter = "none"` (text), `sortfield = "f.type"` (text), `sortorder = 'ASC'` (text).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** A collection of matching entries.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing.
- `503` — query or persistence failure.

## `createFixedAmountDiscount` — Create fixed amount discount

Route `POST {id}/fixedamountdiscounts`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `amount`, `description`, `tva_tx`, `price_base_type`, `discount_type`, `vat_src_code`.

**Access** The decision uses right `societe.creer`, party record scope.

The method applies a fixed discount. The method opens a database transaction and provides commit and rollback paths.

**Result** The record identifier.

- `400` — thirdparty id required, missing required field: amount required, missing required field: description required, invalid amount_ht: must be a positive number, invalid tva_tx: must be a positive number or zero, unknown tax basis, unknown discount type, description required.
- `401` — record outside the caller’s scope.
- `403` — access refused.
- `404` — requested record or reference missing.
- `500` — business operation failed.

## `splitdiscount` — Splitdiscount

Route `POST {id}/splitdiscount/{discountid}`.

**Arguments** `id` (integer), `discountid` (integer), `amount_ttc_1` (number), `amount_ttc_2` (number).

**Access** The decision uses both `societe.creer` and `societe.lire`, party record scope.

The method opens a database transaction and provides commit and rollback paths. Both proposed gross portions must be present and their currency-rounded sum must equal the original gross credit. The original discount must belong to the party and must not already be attached to an invoice line. The split carries source-invoice links and the original tax basis into the replacement portions. For a 120 credit, 50 and 70 qualifies on amount while 50 and 69.99 fails.

**Result** A collection of matching entries.

- `400` — thirdparty id required, discount id required, amount are required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, discount missing.
- `405` — operation unavailable.
- `409` — discount is already used.
- `500` — business operation failed.
- `503` — query or persistence failure.

## `getInvoicesQualifiedForReplacement` — Read invoices qualified for replacement

Route `GET {id}/getinvoicesqualifiedforreplacement`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.lire`, party record scope.

**Result** Invoices eligible for replacement for this party.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `405` — operation unavailable.

## `getInvoicesQualifiedForCreditNote` — Read invoices qualified for credit note

Route `GET {id}/getinvoicesqualifiedforcreditnote`.

**Arguments** `id` (integer).

**Access** The decision uses right `facture.lire`, party record scope.

**Result** Invoices eligible as the basis of a credit note for this party.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `405` — operation unavailable.

## `getCompanyNotification` — Read company notification

Route `GET {id}/notifications`.

**Arguments** `id` (integer).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** Notification subscriptions.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — notification missing, no matching rows.

## `createCompanyNotification` — Create company notification

Route `POST {id}/notifications`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, duplicate record or association.
- `404` — requested data unavailable.
- `500` — error creating party Notification, request_data missing event, business operation failed.

## `createCompanyNotificationByCode` — Create company notification by code

Route `POST {id}/notificationsbycode/{code}`.

**Arguments** `id` (integer), `code` (text), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, duplicate record or association.
- `404` — requested data unavailable, action trigger code missing.
- `500` — business operation failed.

## `deleteCompanyNotification` — Delete company notification

Route `DELETE {id}/notifications/{notification_id}`.

**Arguments** `id` (integer), `notification_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** The notification-removal result.

- `403` — missing operation rights, record outside the caller’s scope.

## `updateCompanyNotification` — Update company notification

Route `PUT {id}/notifications/{notification_id}`.

**Arguments** `id` (integer), `notification_id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope, linked-party scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — requested data unavailable.
- `500` — business operation failed.

## `getCompanyBankAccount` — Read company bank account

Route `GET {id}/bankaccounts`.

**Arguments** `id` (integer).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** The account records for the party.

- `400` — thirdparty id required.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — account missing.

## `createCompanyBankAccount` — Create company bank account

Route `POST {id}/bankaccounts`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope.

The optional caller marker is placed in event context for synchronization. The method builds the mandate reference.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — requested data unavailable.
- `500` — business operation failed.

## `updateCompanyBankAccount` — Update company bank account

Route `PUT {id}/bankaccounts/{bankaccount_id}`.

**Arguments** `id` (integer), `bankaccount_id` (integer), `request_data = null` (collection).

**Access** The decision uses right `societe.creer`, party record scope, linked-party scope.

The optional caller marker is placed in event context for synchronization. The method builds the mandate reference.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — requested data unavailable.
- `500` — business operation failed.

## `deleteCompanyBankAccount` — Delete company bank account

Route `DELETE {id}/bankaccounts/{bankaccount_id}`.

**Arguments** `id` (integer), `bankaccount_id` (integer).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** The bank-account-removal result.

- `403` — missing operation rights, record outside the caller’s scope.

## `generateBankAccountDocument` — Generate bank account document

Route `GET {id}/generateBankAccountDocument/{companybankid}/{model}`.

**Arguments** `id` (integer), `companybankid = null` (integer), `model = 'sepamandate'` (text).

**Access** The decision uses right `societe.creer`, party record scope.

The method sets the document model and generates the business document.

**Result** A record containing the `success` outcome.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — party missing, bank account missing.
- `500` — query or persistence failure, document generation failed.

## `getSocieteAccounts` — Read party accounts

Route `GET {id}/accounts/`.

**Arguments** `id` (integer), `site = null` (text).

**Access** The decision uses right `societe.lire`, party record scope.

**Result** The account records for the party.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — external account missing for this site or party.

## `getSocieteByAccounts` — Read party by accounts

Route `GET /accounts/{site}/{key_account}`.

**Arguments** `site` (text), `key_account` (text).

**Access** The decision uses right `societe.lire`, party record scope.

The lookup uses the visible entity scope for `societe`. The lookup begins at the external account key and site, then resolves the associated party. Possession of the local party identifier alone is insufficient for this lookup.

**Result** The party resolved from the site and external account key.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — account key absent or ambiguous, party missing.

## `createSocieteAccount` — Create party account

Route `POST {id}/accounts`.

**Arguments** `id` (integer), `request_data = null` (collection).

Named body fields used by the handler include `site`, `login`.

**Access** The decision uses right `societe.creer`, party record scope.

The optional caller marker is placed in event context for synchronization. A site key is associated with a party. Creation looks for an existing account under that party and site before constructing the account row.

**Result** The external account record.

- `403` — missing operation rights, record outside the caller’s scope.
- `409` — duplicate record or association.
- `422` — business rule or input rejected.
- `500` — business operation failed.

## `postSocieteAccount` — Post party account

Route `POST {id}/accounts/{site}`.

**Arguments** `id` (integer), `site` (text), `request_data = null` (collection).

Named body fields used by the handler include `key_account`, `login`, `site`.

**Access** The decision uses right `societe.creer`, party record scope.

The optional caller marker is placed in event context for synchronization.

**Result** The external account record.

- `403` — missing operation rights, record outside the caller’s scope.
- `409` — duplicate record or association.
- `422` — business rule or input rejected.
- `500` — business operation failed.

## `putSocieteAccount` — Put party account

Route `PUT {id}/accounts/{site}`.

**Arguments** `id` (integer), `site` (text), `request_data = null` (collection).

Named body fields used by the handler include `site`.

**Access** The decision uses right `societe.creer`, party record scope.

The optional caller marker is placed in event context for synchronization.

**Result** The external account record.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — external account missing for this site or party.
- `409` — duplicate record or association.
- `500` — business operation failed.

## `deleteSocieteAccount` — Delete party account

Route `DELETE {id}/accounts/{site}`.

**Arguments** `id` (integer), `site` (text).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** No response body is declared.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — requested data unavailable.
- `500` — external account missing for this site or party.

## `deleteSocieteAccounts` — Delete party accounts

Route `DELETE {id}/accounts`.

**Arguments** `id` (integer).

**Access** The decision uses right `societe.creer`, party record scope.

**Result** No response body is declared.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — external account missing for this site or party.
- `500` — external account missing for this site or party.
