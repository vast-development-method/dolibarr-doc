# Configuration and reference dictionaries

Country, state and region lookups share identifier and code variants. Dictionary reads, entity configuration and changes to active modules serve different callers. Additional-field changes identify both the business element and the field name.

The implementation locations below refer to `htdocs/api/class/api_setup.class.php`.

## `getListOfActionTriggers` — Read list of action triggers

Route `GET actiontriggers`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `elementtype = ''`, `lang = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `79–130`.

## `getOrderingMethods` — Read ordering methods

Route `GET dictionary/ordering_methods`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `152–197`.

## `getOrderingOrigins` — Read ordering origins

Route `GET dictionary/ordering_origins`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `218–263`.

## `getPaymentTypes` — Read payment types

Route `GET dictionary/payment_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses one of `propal.lire` or `commande.lire` or `facture.lire`.

The lookup uses the visible entity scope for `c_paiement`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `285–331`.

## `getListOfRegions` — Read list of regions

Route `GET dictionary/regions`.

**Arguments** `sortfield = "code_region"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `country = 0`, `filter = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

Source lines `354–404`.

## `getRegionByID` — Read region by id

Route `GET dictionary/regions/{id}`.

**Arguments** `id`.

**Result** A record with internal service properties removed.

- `404` — region missing.
- `503` — record lookup or write failed.

Source lines `419–422` with `_fetchCregion 723–735`.

## `getRegionByCode` — Read region by code

Route `GET dictionary/regions/byCode/{code}`.

**Arguments** `code`.

**Result** A record with internal service properties removed.

- `404` — region missing.
- `503` — record lookup or write failed.

Source lines `437–440` with `_fetchCregion 723–735`.

## `getListOfStates` — Read list of states

Route `GET dictionary/states`.

**Arguments** `sortfield = "code_departement"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `country = 0`, `filter = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

Source lines `466–519`.

## `getStateByID` — Read state by id

Route `GET dictionary/states/{id}`.

**Arguments** `id`.

**Result** A record with internal service properties removed.

- `404` — state missing.
- `503` — record lookup or write failed.

Source lines `534–537` with `_fetchCstate 748–760`.

## `getStateByCode` — Read state by code

Route `GET dictionary/states/byCode/{code}`.

**Arguments** `code`.

**Result** A record with internal service properties removed.

- `404` — state missing.
- `503` — record lookup or write failed.

Source lines `552–555` with `_fetchCstate 748–760`.

## `getListOfCountries` — Read list of countries

Route `GET dictionary/countries`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `filter = ''`, `lang = ''`, `sqlfilters = ''`, `loadregions = 0`, `loadstates = 0`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — record lookup or write failed.

Source lines `583–642`.

## `getCountryByID` — Read country by id

Route `GET dictionary/countries/{id}`.

**Arguments** `id`, `lang = ''`, `loadregions = 0`, `loadstates = 0`.

The wrapper accepts a language argument but passes an empty language to its shared country resolver. The region and state expansion switches are forwarded.

**Result** A record with internal service properties removed.

- `400` — `id` missing or out of range.
- `404` — country missing.
- `503` — record lookup or write failed.

Source lines `661–667` with `_fetchCcountry 777–804`.

## `getCountryByCode` — Read country by code

Route `GET dictionary/countries/byCode/{code}`.

**Arguments** `code`, `lang = ''`, `loadregions = 0`, `loadstates = 0`.

The shared country resolver receives the requested code and subdivision flags. This wrapper passes an empty language to it.

**Result** A record with internal service properties removed.

- `404` — country missing.
- `503` — record lookup or write failed.

Source lines `686–689` with `_fetchCcountry 777–804`.

## `getCountryByISO` — Read country by iso

Route `GET dictionary/countries/byISO/{iso}`.

**Arguments** `iso`, `lang = ''`, `loadregions = 0`, `loadstates = 0`.

The shared country resolver receives the requested ISO value and subdivision flags. This wrapper passes an empty language to it.

**Result** A record with internal service properties removed.

- `404` — country missing.
- `503` — record lookup or write failed.

Source lines `707–710` with `_fetchCcountry 777–804`.

## `getAvailability` — Read availability

Route `GET dictionary/availability`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses right `commande.lire`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `826–871`.

## `getListOfEventTypes` — Read list of event types

Route `GET dictionary/event_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `type = ''`, `module = ''`, `active = 1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `944–991`.

## `getListOfExpenseReportsTypes` — Read list of expense reports types

Route `GET dictionary/expensereport_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `module = ''`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses right `expensereport.lire`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `1013–1061`.

## `getListOfHolidayTypes` — Read list of holiday types

Route `GET dictionary/holiday_types`.

**Arguments** `sortfield = "sortorder"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `fk_country = ''`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Access** The decision uses right `holiday.read`.

The lookup uses the visible entity scope for `c_holiday_types`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `1083–1141`.

## `getListOfPublicHolidays` — Read list of public holidays

Route `GET dictionary/public_holiday`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `fk_country = ''`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Access** The decision uses right `holiday.lire`.

The lookup uses the visible entity scope for `c_hrm_public_holiday`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `1163–1221`.

## `getListOfContactTypes` — Read list of contact types

Route `GET dictionary/contact_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `type = ''`, `module = ''`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `1244–1297`.

## `getListOfCivilities` — Read list of civilities

Route `GET dictionary/civilities`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `module = ''`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `1319–1365`.

## `getListOfCurrencies` — Read list of currencies

Route `GET dictionary/currencies`.

**Arguments** `multicurrency = 0`, `sortfield = "code_iso"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `multicurrency`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `1386–1440`.

## `getListOfExtrafields` — Read list of extrafields

Route `GET extrafields`.

**Arguments** `sortfield = "t.pos"`, `sortorder = 'ASC'`, `elementtype = ''`, `sqlfilters = ''`.

**Access** The decision uses administrator status or configured login exception.

The lookup uses the visible entity scope for `extrafields`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `1458–1531`.

## `deleteExtrafieldsFromNames` — Delete extrafields from names

Route `DELETE extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname`, `elementtype`.

**Access** The decision uses administrator status.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — extrafield missing.
- `500` — removal failed.

Source lines `1544–1567`.

## `getExtrafields` — Read extrafields

Route `GET extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname`, `elementtype`.

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `extrafields`.

**Result** A collection of matching entries.

- `403` — access refused.
- `404` — extrafield missing.
- `503` — query or persistence failure.

Source lines `1583–1646`.

## `postExtrafields` — Post extrafields

Route `POST extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname`, `elementtype`, `request_data = null`.

Named body fields used by the handler include `label`, `alwayseditable`, `default`, `totalizable`, `printable`, `showintooltip`, `required`, `langfile`, `computed`, `unique`, `param`, `perms`, `size`, `type`, `list`, `help`, `pos`.

**Access** The decision uses administrator status.

The method adds an additional-field definition.

**Result** The record identifier.

- `400` — invalid request data.
- `403` — access refused.
- `409` — duplicate record or association.
- `500` — business operation failed.

Source lines `1662–1736`.

## `updateExtrafields` — Update extrafields

Route `PUT extrafields/{elementtype}/{attrname}`.

**Arguments** `attrname`, `elementtype`, `request_data = null`.

Named body fields used by the handler include `label`, `alwayseditable`, `default`, `totalizable`, `printable`, `showintooltip`, `required`, `langfile`, `computed`, `unique`, `param`, `perms`, `size`, `type`, `list`, `help`, `pos`.

**Access** The decision uses administrator status.

The method amends an additional-field definition.

**Result** The record identifier.

- `400` — invalid request data.
- `403` — access refused.
- `404` — extrafield missing.
- `500` — business operation failed.

Source lines `1752–1823`.

## `getListOfTowns` — Read list of towns

Route `GET dictionary/towns`.

**Arguments** `sortfield = "zip,town"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `zipcode = ''`, `town = ''`, `active = 1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `1845–1892`.

## `getPaymentTerms` — Read payment terms

Route `GET dictionary/payment_terms`.

**Arguments** `sortfield = "sortorder"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Access** The decision uses one of `propal.lire` or `commande.lire` or `facture.lire`.

The lookup uses the visible entity scope for `c_payment_term`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `1914–1960`.

## `getShippingModes` — Read shipping modes

Route `GET dictionary/shipping_methods`.

**Arguments** `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `c_shipment_mode`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `1980–2024`.

## `getListOfMeasuringUnits` — Read list of measuring units

Route `GET dictionary/units`.

**Arguments** `sortfield = "rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2044–2085`.

## `getListOfLegalForm` — Read list of legal form

Route `GET dictionary/legal_form`.

**Arguments** `sortfield = "rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `country = 0`, `active = 1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2106–2150`.

## `getListOfStaff` — Read list of staff

Route `GET dictionary/staff`.

**Arguments** `sortfield = "id"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2170–2211`.

## `getListOfsocialNetworks` — Read list ofsocial networks

Route `GET dictionary/socialnetworks`.

**Arguments** `sortfield = "rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `c_socialnetworks`.

**Result** A collection of matching records.

- `400` — invalid request data, invalid filter expression.
- `503` — query or persistence failure.

Source lines `2231–2279`.

## `getTicketsCategories` — Read tickets categories

Route `GET dictionary/ticket_categories`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `c_ticket_category`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2300–2344`.

## `getTicketsSeverities` — Read tickets severities

Route `GET dictionary/ticket_severities`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `c_ticket_severity`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2365–2409`.

## `getTicketsTypes` — Read tickets types

Route `GET dictionary/ticket_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

The lookup uses the visible entity scope for `c_ticket_type`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2430–2475`.

## `getThirdpartiesTypes` — Read parties types

Route `GET dictionary/thirdparty_types`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Result** A collection of matching entries.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2496–2540`.

## `getListOfIncoterms` — Read list of incoterms

Route `GET dictionary/incoterms`.

**Arguments** `sortfield = "code"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `lang = ''`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2560–2603`.

## `getListOfVAT` — Read list of vat

Route `GET dictionary/vat`.

**Arguments** `sortfield = "taux"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `active = 1`, `fk_country = -1`, `sqlfilters = ''`.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `503` — query or persistence failure.

Source lines `2623–2675`.

## `getCompany` — Read company

Route `GET /company`.

**Access** The decision uses administrator status or configured login exception.

**Result** A record with internal service properties removed.

- `403` — access refused.

Source lines `2688–2735`.

## `getEstablishments` — Read establishments

Route `GET /establishments`.

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `establishment`.

**Result** A collection of matching entries.

- `403` — access refused.
- `503` — query or persistence failure.

Source lines `2748–2777`.

## `getEtablishmentByID` — Read etablishment by id

Route `GET establishments/{id}`.

**Arguments** `id`.

**Access** The decision uses administrator status.

The lookup uses the visible entity scope for `establishment`.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — establishment missing.
- `503` — record lookup or write failed.

Source lines `2790–2809`.

## `getConf` — Read conf

Route `GET conf/{constantname}`.

**Arguments** `constantname`.

**Access** The decision uses administrator status or configured login exception.

**Result** The selected configuration value as text.

- `400` — error Bad or unknown value for constantname.
- `403` — access refused, access or input restriction.

Source lines `2824–2841`.

## `getConfs` — Read confs

Route `GET conf/`.

**Access** The decision uses administrator status or configured login exception.

The lookup uses the visible entity scope for `const`.

**Result** A collection of matching entries.

- `403` — access refused.
- `503` — query or persistence failure.

Source lines `2857–2886`.

## `getCheckIntegrity` — Read check integrity

Route `GET checkintegrity`.

**Arguments** `target`.

**Access** The decision uses administrator status or configured login exception.

The result carries a comparison code and comment, expected and current checksums and detailed output.

**Result** A record with `resultcode`, `resultcomment`, `expectedchecksum`, `currentchecksum`, `out`.

- `403` — access refused.
- `404` — no signature file known.
- `500` — business operation failed, document-root entry missing from the manifest.

Source lines `2902–3209`.

## `getModules` — Read modules

Route `GET /modules`.

**Access** The decision uses administrator status or configured login exception.

**Result** The enabled-module collection.

- `403` — access refused.

Source lines `3222–3235`.

## `getModulesList` — Read modules list

Route `GET /modules/status/{origin}`.

**Arguments** `status = "active"`, `origin = 'all'`.

**Access** The decision uses administrator status or configured login exception.

The status selector accepts active, disabled or all. The origin selector can distinguish core and external modules. Each result carries the module name, origin, activation flag, publisher and version.

**Result** A map keyed by module with name, origin, active state, publisher and version.

- `403` — access refused.

Source lines `3248–3306`.

## `enableModules` — Enable modules

Route `PUT /modules/{modulename}/enable`.

**Arguments** `modulename`.

**Access** The decision uses administrator status or configured login exception.

**Result** A record with `result`, `message`.

- `403` — access refused.
- `404` — module missing.

Source lines `3319–3322` with `_moduleOnOff 3349–3385`.

## `disableModules` — Disable modules

Route `PUT /modules/{modulename}/disable`.

**Arguments** `modulename`.

**Access** The decision uses administrator status or configured login exception.

**Result** A record with `result`, `message`.

- `403` — access refused.
- `404` — module missing.

Source lines `3334–3337` with `_moduleOnOff 3349–3385`.
