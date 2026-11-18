# Configuration and reference dictionaries

Country, state and region lookups share identifier and code variants. Dictionary reads, entity configuration and changes to active modules serve different callers. Additional-field changes identify both the business element and the field name.

## `getListOfActionTriggers` — Read list of action triggers

Route `GET actiontriggers`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `elementtype = ''` (text), `lang = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getOrderingMethods` — Read ordering methods

Route `GET dictionary/ordering_methods`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getOrderingOrigins` — Read ordering origins

Route `GET dictionary/ordering_origins`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getPaymentTypes` — Read payment types

Route `GET dictionary/payment_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses one of `propal.lire` or `commande.lire` or `facture.lire`.

The lookup uses the visible entity scope for `c_paiement`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getListOfRegions` — Read list of regions

Route `GET dictionary/regions`.

**Arguments** `sortfield = "code_region"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `country = 0` (integer), `filter = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

## `getRegionByID` — Read region by id

Route `GET dictionary/regions/{id}`.

**Arguments** `id` (integer).

**Result** A record with internal service properties removed.

- `404` — region missing.
- `503` — record lookup or write failed.

## `getRegionByCode` — Read region by code

Route `GET dictionary/regions/byCode/{code}`.

**Arguments** `code` (text).

**Result** A record with internal service properties removed.

- `404` — region missing.
- `503` — record lookup or write failed.

## `getListOfStates` — Read list of states

Route `GET dictionary/states`.

**Arguments** `sortfield = "code_departement"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `country = 0` (integer), `filter = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

## `getStateByID` — Read state by id

Route `GET dictionary/states/{id}`.

**Arguments** `id` (integer).

**Result** A record with internal service properties removed.

- `404` — state missing.
- `503` — record lookup or write failed.

## `getStateByCode` — Read state by code

Route `GET dictionary/states/byCode/{code}`.

**Arguments** `code` (text).

**Result** A record with internal service properties removed.

- `404` — state missing.
- `503` — record lookup or write failed.

## `getListOfCountries` — Read list of countries

Route `GET dictionary/countries`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `filter = ''` (text), `lang = ''` (text), `sqlfilters = ''` (text), `loadregions = 0` (integer), `loadstates = 0` (integer).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

## `getCountryByID` — Read country by id

Route `GET dictionary/countries/{id}`.

**Arguments** `id` (integer), `lang = ''` (text), `loadregions = 0` (integer), `loadstates = 0` (integer).

The wrapper accepts a language argument but passes an empty language to its shared country resolver. The region and state expansion switches are forwarded.

**Result** A record with internal service properties removed.

- `400` — `id` missing or out of range.
- `404` — country missing.
- `503` — record lookup or write failed.

## `getCountryByCode` — Read country by code

Route `GET dictionary/countries/byCode/{code}`.

**Arguments** `code` (text), `lang = ''` (text), `loadregions = 0` (integer), `loadstates = 0` (integer).

The shared country resolver receives the requested code and subdivision flags. This wrapper passes an empty language to it.

**Result** A record with internal service properties removed.

- `404` — country missing.
- `503` — record lookup or write failed.

## `getCountryByISO` — Read country by iso

Route `GET dictionary/countries/byISO/{iso}`.

**Arguments** `iso` (text), `lang = ''` (text), `loadregions = 0` (integer), `loadstates = 0` (integer).

The shared country resolver receives the requested ISO value and subdivision flags. This wrapper passes an empty language to it.

**Result** A record with internal service properties removed.

- `404` — country missing.
- `503` — record lookup or write failed.

## `getAvailability` — Read availability

Route `GET dictionary/availability`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getListOfEventTypes` — Read list of event types

Route `GET dictionary/event_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `type = ''` (text), `module = ''` (text), `active = 1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfExpenseReportsTypes` — Read list of expense reports types

Route `GET dictionary/expensereport_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `module = ''` (text), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses right `expensereport.lire`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getListOfHolidayTypes` — Read list of holiday types

Route `GET dictionary/holiday_types`.

**Arguments** `sortfield = "sortorder"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `fk_country = ''` (text), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Access** The decision uses right `holiday.read`.

The lookup uses the visible entity scope for `c_holiday_types`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getListOfPublicHolidays` — Read list of public holidays

Route `GET dictionary/public_holiday`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `fk_country = ''` (text), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Access** The decision uses right `holiday.lire`.

The lookup uses the visible entity scope for `c_hrm_public_holiday`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getListOfContactTypes` — Read list of contact types

Route `GET dictionary/contact_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `type = ''` (text), `module = ''` (text), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfCivilities` — Read list of civilities

Route `GET dictionary/civilities`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `module = ''` (text), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfCurrencies` — Read list of currencies

Route `GET dictionary/currencies`.

**Arguments** `multicurrency = 0` (integer), `sortfield = "code_iso"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `multicurrency`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfExtrafields` — Read list of extrafields

Route `GET extrafields`.

**Arguments** `sortfield = "t.pos"` (text), `sortorder = 'ASC'` (text), `elementtype = ''` (text), `sqlfilters = ''` (text).

**Access** The decision uses administrator status or configured login exception.

The lookup uses the visible entity scope for `extrafields`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `deleteExtrafieldsFromNames` — Delete extrafields from names

Route `DELETE extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname` (text), `elementtype` (text).

**Access** The decision uses administrator status.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — extrafield missing.
- `500` — removal failed.

## `getExtrafields` — Read extrafields

Route `GET extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname` (text), `elementtype` (text).

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `extrafields`.

**Result** A collection of matching entries.

- `403` — access refused.
- `404` — extrafield missing.
- `503` — query or persistence failure.

## `postExtrafields` — Post extrafields

Route `POST extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname` (text), `elementtype` (text), `request_data = null` (collection).

Named body fields used by the handler include `label`, `alwayseditable`, `default`, `totalizable`, `printable`, `showintooltip`, `required`, `langfile`, `computed`, `unique`, `param`, `perms`, `size`, `type`, `list`, `help`, `pos`.

**Access** The decision uses administrator status.

The method adds an additional-field definition.

**Result** The record identifier.

- `400` — invalid request data.
- `403` — access refused.
- `409` — duplicate record or association.
- `500` — business operation failed.

## `updateExtrafields` — Update extrafields

Route `PUT extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname` (text), `elementtype` (text), `request_data = null` (collection).

Named body fields used by the handler include `label`, `alwayseditable`, `default`, `totalizable`, `printable`, `showintooltip`, `required`, `langfile`, `computed`, `unique`, `param`, `perms`, `size`, `type`, `list`, `help`, `pos`.

**Access** The decision uses administrator status.

The method amends an additional-field definition.

**Result** The record identifier.

- `400` — invalid request data.
- `403` — access refused.
- `404` — extrafield missing.
- `500` — business operation failed.

## `getListOfTowns` — Read list of towns

Route `GET dictionary/towns`.

**Arguments** `sortfield = "zip,town"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `zipcode = ''` (text), `town = ''` (text), `active = 1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getPaymentTerms` — Read payment terms

Route `GET dictionary/payment_terms`.

**Arguments** `sortfield = "sortorder"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Access** The decision uses one of `propal.lire` or `commande.lire` or `facture.lire`.

The lookup uses the visible entity scope for `c_payment_term`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `getShippingModes` — Read shipping modes

Route `GET dictionary/shipping_methods`.

**Arguments** `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `c_shipment_mode`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfMeasuringUnits` — Read list of measuring units

Route `GET dictionary/units`.

**Arguments** `sortfield = "rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfLegalForm` — Read list of legal form

Route `GET dictionary/legal_form`.

**Arguments** `sortfield = "rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `country = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfStaff` — Read list of staff

Route `GET dictionary/staff`.

**Arguments** `sortfield = "id"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfsocialNetworks` — Read list ofsocial networks

Route `GET dictionary/socialnetworks`.

**Arguments** `sortfield = "rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `c_socialnetworks`.

**Result** A collection of matching records.

- `400` — invalid request data, invalid filter expression.
- `503` — query or persistence failure.

## `getTicketsCategories` — Read tickets categories

Route `GET dictionary/ticket_categories`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `c_ticket_category`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getTicketsSeverities` — Read tickets severities

Route `GET dictionary/ticket_severities`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `c_ticket_severity`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getTicketsTypes` — Read tickets types

Route `GET dictionary/ticket_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

The lookup uses the visible entity scope for `c_ticket_type`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getThirdpartiesTypes` — Read parties types

Route `GET dictionary/thirdparty_types`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfIncoterms` — Read list of incoterms

Route `GET dictionary/incoterms`.

**Arguments** `sortfield = "code"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `lang = ''` (text), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getListOfVAT` — Read list of vat

Route `GET dictionary/vat`.

**Arguments** `sortfield = "taux"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `active = 1` (integer), `fk_country = -1` (integer), `sqlfilters = ''` (text).

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

## `getCompany` — Read company

Route `GET /company`.

**Access** The decision uses administrator status or configured login exception.

**Result** A record with internal service properties removed.

- `403` — access refused.

## `getEstablishments` — Read establishments

Route `GET /establishments`.

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `establishment`.

**Result** A collection of matching entries.

- `403` — access refused.
- `503` — query or persistence failure.

## `getEtablishmentByID` — Read etablishment by id

Route `GET establishments/{id}`.

**Arguments** `id` (integer).

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `establishment`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — establishment missing.
- `503` — record lookup or write failed.

## `getConf` — Read conf

Route `GET conf/{constantname}`.

**Arguments** `constantname` (text).

**Access** The decision uses administrator status or configured login exception.

**Result** The selected configuration value as text.

- `400` — error Bad or unknown value for constantname.
- `403` — access refused, access or input restriction.

## `getConfs` — Read confs

Route `GET conf/`.

**Access** The decision uses administrator status or configured login exception.

The lookup uses the visible entity scope for `const`.

**Result** A collection of matching entries.

- `403` — access refused.
- `503` — query or persistence failure.

## `getCheckIntegrity` — Read check integrity

Route `GET checkintegrity`.

**Arguments** `target` (text).

**Access** The decision uses administrator status or configured login exception.

The result carries a comparison code and comment, expected and current checksums and detailed output.

**Result** A record with `resultcode`, `resultcomment`, `expectedchecksum`, `currentchecksum`, `out`.

- `403` — access refused.
- `404` — no signature file known.
- `500` — business operation failed, document-root entry missing from the manifest.

## `getModules` — Read modules

Route `GET /modules`.

**Access** The decision uses administrator status or configured login exception.

**Result** The enabled-module collection.

- `403` — access refused.

## `getModulesList` — Read modules list

Route `GET /modules/status/{origin}`.

**Arguments** `status = "active"` (text), `origin = 'all'` (text).

**Access** The decision uses administrator status or configured login exception.

The status selector accepts active, disabled or all. The origin selector can distinguish core and external modules. Each result carries the module name, origin, activation flag, publisher and version.

**Result** A map keyed by module with name, origin, active state, publisher and version.

- `403` — access refused.

## `enableModules` — Enable modules

Route `PUT /modules/{modulename}/enable`.

**Arguments** `modulename` (text).

**Access** The decision uses administrator status or configured login exception.

**Result** A record with `result`, `message`.

- `403` — access refused.
- `404` — module missing.

## `disableModules` — Disable modules

Route `PUT /modules/{modulename}/disable`.

**Arguments** `modulename` (text).

**Access** The decision uses administrator status or configured login exception.

**Result** A record with `result`, `message`.

- `403` — access refused.
- `404` — module missing.
