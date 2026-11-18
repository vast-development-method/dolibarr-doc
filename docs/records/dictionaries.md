# Controlled values and regional reference data

A dictionary row identifies a controlled value used by business records. A record can retain its chosen rate, currency or label even if a dictionary later changes. Selection often depends on the entity, active flag or country.

**Example.** A document can preserve the tax rate used at issue time while its tax dictionary entry subsequently changes. Use the stored transaction amounts for the historical invoice. Use the current dictionary for the rate selection on a new document.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Accounting report row](#record-c_accounting_category) | `c_accounting_category` |
| [Report definition](#record-c_accounting_report) | `c_accounting_report` |
| [Business event code](#record-c_action_trigger) | `c_action_trigger` |
| [Activity type](#record-c_actioncomm) | `c_actioncomm` |
| [Asset disposal reason](#record-c_asset_disposal_type) | `c_asset_disposal_type` |
| [Availability term](#record-c_availability) | `c_availability` |
| [Barcode symbology](#record-c_barcode_type) | `c_barcode_type` |
| [Contribution category](#record-c_chargesociales) | `c_chargesociales` |
| [Form of address](#record-c_civility) | `c_civility` |
| [Country](#record-c_country) | `c_country` |
| [Currency](#record-c_currencies) | `c_currencies` |
| [Administrative subdivision](#record-c_departements) | `c_departements` |
| [Environmental levy rate](#record-c_ecotaxe) | `c_ecotaxe` |
| [Organisation size band](#record-c_effectif) | `c_effectif` |
| [Sender identity](#record-c_email_senderprofile) | `c_email_senderprofile` |
| [Email template](#record-c_email_templates) | `c_email_templates` |
| [Mileage tax category](#record-c_exp_tax_cat) | `c_exp_tax_cat` |
| [Mileage range](#record-c_exp_tax_range) | `c_exp_tax_range` |
| [Configurable selection list](#record-c_field_list) | `c_field_list` |
| [Label sheet format](#record-c_format_cards) | `c_format_cards` |
| [Legal form](#record-c_forme_juridique) | `c_forme_juridique` |
| [Leave type](#record-c_holiday_types) | `c_holiday_types` |
| [Department](#record-c_hrm_department) | `c_hrm_department` |
| [Employee function](#record-c_hrm_function) | `c_hrm_function` |
| [Public holiday](#record-c_hrm_public_holiday) | `c_hrm_public_holiday` |
| [Trade delivery term](#record-c_incoterms) | `c_incoterms` |
| [Order method](#record-c_input_method) | `c_input_method` |
| [Commercial source](#record-c_input_reason) | `c_input_reason` |
| [Invoice subtype](#record-c_invoice_subtype) | `c_invoice_subtype` |
| [Opportunity stage](#record-c_lead_status) | `c_lead_status` |
| [Payment instrument](#record-c_paiement) | `c_paiement` |
| [Paper format](#record-c_paper_format) | `c_paper_format` |
| [Partnership type](#record-c_partnership_type) | `c_partnership_type` |
| [Payment terms](#record-c_payment_term) | `c_payment_term` |
| [Product nature](#record-c_product_nature) | `c_product_nature` |
| [Batch quality state](#record-c_productbatch_qcstatus) | `c_productbatch_qcstatus` |
| [Proposal status dictionary](#record-c_propalst) | `c_propalst` |
| [Prospect contact level](#record-c_prospectcontactlevel) | `c_prospectcontactlevel` |
| [Prospect potential](#record-c_prospectlevel) | `c_prospectlevel` |
| [Region](#record-c_regions) | `c_regions` |
| [Revenue stamp](#record-c_revenuestamp) | `c_revenuestamp` |
| [Shipping method](#record-c_shipment_mode) | `c_shipment_mode` |
| [Package type](#record-c_shipment_package_type) | `c_shipment_package_type` |
| [Social network](#record-c_socialnetworks) | `c_socialnetworks` |
| [Party prospecting state](#record-c_stcomm) | `c_stcomm` |
| [Contact prospecting state](#record-c_stcommcontact) | `c_stcommcontact` |
| [Ticket category](#record-c_ticket_category) | `c_ticket_category` |
| [Ticket resolution](#record-c_ticket_resolution) | `c_ticket_resolution` |
| [Ticket severity](#record-c_ticket_severity) | `c_ticket_severity` |
| [Ticket type](#record-c_ticket_type) | `c_ticket_type` |
| [Transport mode](#record-c_transport_mode) | `c_transport_mode` |
| [VAT rate](#record-c_tva) | `c_tva` |
| [Contact role](#record-c_type_contact) | `c_type_contact` |
| [Page container type](#record-c_type_container) | `c_type_container` |
| [Expense type](#record-c_type_fees) | `c_type_fees` |
| [Resource type](#record-c_type_resource) | `c_type_resource` |
| [Organisation type](#record-c_typent) | `c_typent` |
| [Unit of measure](#record-c_units) | `c_units` |
| [Postal locality](#record-c_ziptown) | `c_ziptown` |

<a id="record-c_accounting_category"></a>

## Accounting report row

Defines a line of a financial report with its account selection, sign, formula and position.

**Storage** `c_accounting_category`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`, `fk_report`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_report` | integer | No | `1` | Financial report to which the category belongs. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `range_account` | varchar(255) | No | — | Account-range expression on the reporting category. |
| `sens` | tinyint | No | `'0'` | Direction/sign convention used by the owning reporting or posting operation. |
| `category_type` | tinyint | No | `'0'` | Identifies whether the report category is calculated. |
| `formula` | varchar(255) | No | — | Calculation that references other category IDs when deriving a report value. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_country` | integer | Yes | `NULL` | Country associated with the record. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_accounting_category-accounting.sql`, `htdocs/install/mysql/tables/llx_c_accounting_category-accounting.key.sql`, `htdocs/core/class/html.formaccounting.class.php:255`.

<a id="record-c_accounting_report"></a>

## Report definition

Identifies an accounting report and its country and entity context.

**Storage** `c_accounting_report`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `fk_country` | integer | Yes | `NULL` | Country associated with the record. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_accounting_report-accounting.sql`, `htdocs/install/mysql/tables/llx_c_accounting_report-accounting.key.sql`, `htdocs/core/menus/standard/eldy.lib.php:2008`.

<a id="record-c_action_trigger"></a>

## Business event code

Identifies a named business event and the record type for which it is declared.

**Storage** `c_action_trigger`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `elementtype` | varchar(64) | No | — | Type discriminator identifying the class of associated object. |
| `code` | varchar(128) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `contexts` | varchar(255) | Yes | — | Event contexts in which this trigger definition is used. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_action_trigger.sql`, `htdocs/install/mysql/tables/llx_c_action_trigger.key.sql`, `htdocs/core/class/notify.class.php:494`.

<a id="record-c_actioncomm"></a>

## Activity type

Enumerates the types assigned to calendar activities.

**Storage** `c_actioncomm`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `code` | varchar(50) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `type` | varchar(50) | No | `'system'` | Type. |
| `libelle` | varchar(128) | No | — | Display label for the record. |
| `module` | varchar(50) | Yes | `NULL` | Feature or extension to which this entry belongs. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `todo` | tinyint | Yes | — | Historical task indicator retained on the activity type. |
| `color` | varchar(9) | Yes | — | Display colour assigned to this entry. |
| `picto` | varchar(48) | Yes | — | Icon identifier used for presentation. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_actioncomm.sql`, `htdocs/install/mysql/tables/llx_c_actioncomm.key.sql`, `htdocs/api/class/api_setup.class.php:949`.

<a id="record-c_asset_disposal_type"></a>

## Asset disposal reason

Enumerates the reasons available when retiring or disposing of a fixed asset.

**Storage** `c_asset_disposal_type`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

**Referenced by** [asset](accounting.md#record-asset) (fk_disposal_type).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(50) | No | — | Display label for the record. |
| `active` | integer | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_asset_disposal_type-asset.sql`, `htdocs/install/mysql/tables/llx_c_asset_disposal_type-asset.key.sql`, `htdocs/admin/dict.php:312`.

<a id="record-c_availability"></a>

## Availability term

Supplies named lead-time or availability choices on commercial documents.

**Storage** `c_availability`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(30) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `type_duration` | varchar(1) | Yes | — | Unit or kind used to interpret the availability interval. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_availability.sql`, `htdocs/install/mysql/tables/llx_c_availability.key.sql`, `htdocs/core/class/html.form.class.php:5177`.

<a id="record-c_barcode_type"></a>

## Barcode symbology

Defines the barcode format used to interpret or print an item's barcode.

**Storage** `c_barcode_type`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

**Referenced by** [product](catalogue.md#record-product) (fk_barcode_type), [product_fournisseur_price](catalogue.md#record-product_fournisseur_price) (fk_barcode_type), [ticket](people.md#record-ticket) (fk_barcode_type).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `libelle` | varchar(128) | No | — | Display label for the record. |
| `coder` | varchar(16) | No | — | Barcode encoder selected for this symbology. |
| `example` | varchar(16) | No | — | Example value for the barcode symbology. |

Source locations include `htdocs/install/mysql/tables/llx_c_barcode_type.sql`, `htdocs/install/mysql/tables/llx_c_barcode_type.key.sql`, `htdocs/core/class/commonobject.class.php:2128`.

<a id="record-c_chargesociales"></a>

## Contribution category

Enumerates the types of social or statutory charges that can be recorded.

**Storage** `c_chargesociales`.
The primary key is `id`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer (generated) | No | — | Internal identifier in this table. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `deductible` | smallint | No | `0` | Indicates whether charges of this type are deductible. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `code` | varchar(24) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `accountancy_code` | varchar(32) | Yes | `NULL` | Account code selected for the transaction or classification. |
| `fk_pays` | integer | No | `1` | Country associated with the record. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_chargesociales.sql`, `htdocs/core/class/html.formsocialcontrib.class.php:78`.

<a id="record-c_civility"></a>

## Form of address

Provides the named honorifics available for a person.

**Storage** `c_civility`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(6) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_civility.sql`, `htdocs/install/mysql/tables/llx_c_civility.key.sql`, `htdocs/core/class/html.formcompany.class.php:494`.

<a id="record-c_country"></a>

## Country

Identifies a country by codes and display name and carries locale-specific tax and geographic settings.

**Storage** `c_country`.
The primary key is `rowid`.
Additional unique keys comprise `code` / `code_iso` / `label`.

**Referenced by** [c_regions](dictionaries.md#record-c_regions) (fk_pays), [c_ziptown](dictionaries.md#record-c_ziptown) (fk_pays), [product](catalogue.md#record-product) (fk_country), [resource](production.md#record-resource) (fk_country).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer | No | — | Internal row identifier. |
| `code` | varchar(2) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `code_iso` | varchar(3) | Yes | — | Standard geographic or currency code. |
| `numeric_code` | varchar(3) | Yes | — | Numeric ISO code for the country. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `eec` | tinyint | No | `0` | Flag used for European Community country classification. |
| `sepa` | tinyint | No | `0` | Identifies a country participating in the SEPA payment area. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `favorite` | tinyint | No | `0` | Whether the country is favoured in selection lists. |
| `phone_code` | integer | Yes | — | International telephone calling code. |
| `trunk_prefix` | varchar(5) | Yes | — | Domestic trunk prefix used in telephone numbering. |

Source locations include `htdocs/install/mysql/tables/llx_c_country.sql`, `htdocs/install/mysql/tables/llx_c_country.key.sql`, `htdocs/core/class/ccountry.class.php:45`.

<a id="record-c_currencies"></a>

## Currency

Enumerates available currencies and their standard identifiers.

**Storage** `c_currencies`.
The primary key is `code_iso`.
An additional unique key comprises `code_iso`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `code_iso` | varchar(3) | No | — | Standard geographic or currency code. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `unicode` | varchar(32) | Yes | `NULL` | Currency symbol representation. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `max_decimal_unit` | tinyint | Yes | — | Number of decimal places configured for unit prices in the currency. |
| `max_decimal_tot` | tinyint | Yes | — | Number of decimal places configured for totals in the currency. |

Source locations include `htdocs/install/mysql/tables/llx_c_currencies.sql`, `htdocs/install/mysql/tables/llx_c_currencies.key.sql`, `htdocs/core/class/translate.class.php:1180`.

<a id="record-c_departements"></a>

## Administrative subdivision

Defines a subnational division and its regional association.

**Storage** `c_departements`.
The primary key is `rowid`.
An additional unique key comprises `code_departement`, `fk_region`.

**Referenced by** [c_tva](dictionaries.md#record-c_tva) (fk_department_buyer), [c_ziptown](dictionaries.md#record-c_ziptown) (fk_county).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code_departement` | varchar(6) | No | — | Administrative subdivision code. |
| `fk_region` | integer | Yes | — | References [c_regions](dictionaries.md#record-c_regions) (code_region). |
| `cheflieu` | varchar(50) | Yes | — | Administrative capital of the geographic subdivision. |
| `tncc` | integer | Yes | — | Naming code associated with the administrative subdivision. |
| `ncc` | varchar(50) | Yes | — | Administrative subdivision name in the reference nomenclature. |
| `nom` | varchar(50) | Yes | — | Name under which this record is presented or identified. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_departements.sql`, `htdocs/install/mysql/tables/llx_c_departements.key.sql`, `htdocs/core/class/cstate.class.php:92`.

<a id="record-c_ecotaxe"></a>

## Environmental levy rate

Provides configured environmental levy codes and their amounts or rates.

**Storage** `c_ecotaxe`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(64) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `price` | double(24,8) | Yes | — | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `organization` | varchar(255) | Yes | — | Organisation administering the environmental fee schedule. |
| `fk_pays` | integer | No | — | Country associated with the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_ecotaxe.sql`, `htdocs/install/mysql/tables/llx_c_ecotaxe.key.sql`, `htdocs/core/class/html.formother.class.php:290`.

<a id="record-c_effectif"></a>

## Organisation size band

Enumerates workforce-size categories used to classify a third party.

**Storage** `c_effectif`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_effectif.sql`, `htdocs/install/mysql/tables/llx_c_effectif.key.sql`, `htdocs/core/class/html.formcompany.class.php:116`.

<a id="record-c_email_senderprofile"></a>

## Sender identity

Stores a configured outgoing email identity and related delivery settings.

**Storage** `c_email_senderprofile`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `label`, `email`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `private` | smallint | No | `0` | User. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `email` | varchar(255) | No | — | Email address associated with this record. |
| `signature` | text | Yes | — | Signature. |
| `position` | smallint | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_email_senderprofile.sql`, `htdocs/install/mysql/tables/llx_c_email_senderprofile.key.sql`, `htdocs/core/class/html.formmail.class.php:770`.

<a id="record-c_email_templates"></a>

## Email template

Defines reusable subject, content and language information for a particular sending context.

**Storage** `c_email_templates`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `label`, `lang`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `type_template` | varchar(32) | Yes | — | Typetemplate. |
| `lang` | varchar(6) | Yes | empty string | Language code under which this text or presentation is stored. |
| `private` | smallint | No | `0` | Private. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `label` | varchar(180) | Yes | — | Display label for the record. |
| `position` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `defaultfortype` | smallint | Yes | `0` | Default. |
| `enabled` | varchar(255) | Yes | `'1'` | Condition or flag determining whether the entry is available. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `email_from` | varchar(255) | Yes | — | Sender email address. |
| `email_to` | varchar(255) | Yes | — | Primary email recipients. |
| `email_tocc` | varchar(255) | Yes | — | Copy recipients. |
| `email_tobcc` | varchar(255) | Yes | — | Blind-copy recipients. |
| `topic` | text | Yes | — | Subject. |
| `joinfiles` | text | Yes | — | Joinfiles. |
| `content` | mediumtext | Yes | — | Content. |
| `content_lines` | text | Yes | — | Contentlines. |

Source locations include `htdocs/install/mysql/tables/llx_c_email_templates.sql`, `htdocs/install/mysql/tables/llx_c_email_templates.key.sql`, `htdocs/core/class/html.formmail.class.php:1815`.

<a id="record-c_exp_tax_cat"></a>

## Mileage tax category

Classifies the vehicle or expense category used to choose a mileage band.

**Storage** `c_exp_tax_cat`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `active` | integer | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_exp_tax_cat-expensereport.sql`, `htdocs/core/class/html.form.class.php:12238`.

<a id="record-c_exp_tax_range"></a>

## Mileage range

Defines a distance interval used when choosing a mileage reimbursement coefficient and offset.

**Storage** `c_exp_tax_range`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_c_exp_tax_cat` | integer | No | `1` | Expense or mileage category used to select reimbursement settings. |
| `range_ik` | double | No | `0` | Distance boundary for selection of a mileage allowance band. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `active` | integer | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_exp_tax_range-expensereport.sql`, `htdocs/core/class/html.form.class.php:12328`.

<a id="record-c_field_list"></a>

## Configurable selection list

Stores field selection metadata used by catalogue forms that enable this mechanism.

**Storage** `c_field_list`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `element` | varchar(64) | No | — | Object list on which this field can appear. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `name` | varchar(32) | No | — | Name under which this record is presented or identified. |
| `alias` | varchar(32) | No | — | Alias used to reference the selectable list field. |
| `title` | varchar(32) | No | — | Display title. |
| `align` | varchar(6) | Yes | `'left'` | Alignment of values displayed in this list column. |
| `sort` | tinyint | No | `1` | Whether the field is available for sorting. |
| `search` | tinyint | No | `0` | Whether the field is available for filtering the list. |
| `visible` | tinyint | No | `1` | Visibility policy for the field in forms and lists. |
| `enabled` | varchar(255) | Yes | `1` | Condition or flag determining whether the entry is available. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_field_list.sql`, `htdocs/product/canvas/product/actions_card_product.class.php:314`.

<a id="record-c_format_cards"></a>

## Label sheet format

Describes physical page, label, margin and spacing settings for printing sheets of cards or labels.

**Storage** `c_format_cards`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(50) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `name` | varchar(50) | No | — | Name under which this record is presented or identified. |
| `paper_size` | varchar(20) | No | — | Stock format for the sheet of cards or labels. |
| `orientation` | varchar(1) | No | — | Page orientation for the sheet layout. |
| `metric` | varchar(5) | No | — | Measurement system used by the layout. |
| `leftmargin` | double(24,8) | No | — | Distance between the corresponding page edge and the start of the printed layout. |
| `topmargin` | double(24,8) | No | — | Distance between the corresponding page edge and the start of the printed layout. |
| `nx` | integer | No | — | Number of labels or cards in the corresponding horizontal or vertical direction. |
| `ny` | integer | No | — | Number of labels or cards in the corresponding horizontal or vertical direction. |
| `spacex` | double(24,8) | No | — | Spacing between items along the indicated page axis. |
| `spacey` | double(24,8) | No | — | Spacing between items along the indicated page axis. |
| `width` | double(24,8) | No | — | Physical horizontal or vertical dimension, respectively. |
| `height` | double(24,8) | No | — | Physical horizontal or vertical dimension, respectively. |
| `font_size` | integer | No | — | Text size used for this layout. |
| `custom_x` | double(24,8) | No | — | Dimension of a custom sheet along the indicated axis. |
| `custom_y` | double(24,8) | No | — | Dimension of a custom sheet along the indicated axis. |
| `active` | integer | No | — | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_format_cards.sql`, `htdocs/admin/dict.php:298`.

<a id="record-c_forme_juridique"></a>

## Legal form

Enumerates organisation forms for a jurisdiction.

**Storage** `c_forme_juridique`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | integer | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `fk_pays` | integer | No | — | Country associated with the record. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `isvatexempted` | tinyint | No | `0` | Marks a legal form associated with VAT exemption. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_forme_juridique.sql`, `htdocs/install/mysql/tables/llx_c_forme_juridique.key.sql`, `htdocs/core/class/html.formcompany.class.php:575`.

<a id="record-c_holiday_types"></a>

## Leave type

Defines absence categories, their codes, entitlement behaviour and related settings.

**Storage** `c_holiday_types`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `affect` | integer | No | — | Determines whether this leave type changes the employee's available balance. |
| `delay` | integer | No | — | Required advance notice for a leave request of this type. |
| `newbymonth` | double(8,5) | No | `0` | Leave credited each month for this type. |
| `fk_country` | integer | Yes | `NULL` | Country associated with the record. |
| `block_if_negative` | integer | No | `0` | Controls whether a request may leave a negative balance. |
| `sortorder` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_holiday_types.sql`, `htdocs/install/mysql/tables/llx_c_holiday_types.key.sql`, `htdocs/api/class/api_setup.class.php:1095`.

<a id="record-c_hrm_department"></a>

## Department

Identifies an organisational department available in personnel records.

**Storage** `c_hrm_department`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer | No | — | Internal row identifier. |
| `pos` | tinyint | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_hrm_department.sql`, `htdocs/admin/dict.php:301`.

<a id="record-c_hrm_function"></a>

## Employee function

Enumerates occupational functions that can be assigned to personnel.

**Storage** `c_hrm_function`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer | No | — | Internal row identifier. |
| `pos` | tinyint | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `c_level` | tinyint | No | `0` | Level associated with this job function. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_hrm_function.sql`, `htdocs/admin/dict.php:302`.

<a id="record-c_hrm_public_holiday"></a>

## Public holiday

Stores dates or recurring calendar attributes treated as public holidays under the applicable geographic context.

**Storage** `c_hrm_public_holiday`.
The primary key is `id`.
Additional unique keys comprise `entity`, `code` / `entity`, `fk_country`, `dayrule`, `day`, `month`, `year`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer (generated) | No | — | Internal identifier in this table. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_country` | integer | Yes | — | Country associated with the record. |
| `fk_departement` | integer | Yes | — | Administrative subdivision identity in an address. |
| `code` | varchar(62) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `dayrule` | varchar(64) | Yes | empty string | Named recurrence rule for a movable holiday, such as an Easter-relative day. |
| `day` | integer | Yes | — | Calendar component for a fixed holiday. |
| `month` | integer | Yes | — | Calendar component for a fixed holiday. |
| `year` | integer | Yes | — | Calendar year for the holiday. Zero makes the entry applicable across years. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_c_hrm_public_holiday.sql`, `htdocs/install/mysql/tables/llx_c_hrm_public_holiday.key.sql`, `htdocs/api/class/api_setup.class.php:1175`.

<a id="record-c_incoterms"></a>

## Trade delivery term

Identifies the standard commercial delivery term selected on a document. The negotiated location is stored on that document.

**Storage** `c_incoterms`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(8) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(100) | Yes | — | Display label for the record. |
| `libelle` | varchar(255) | No | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_incoterms.sql`, `htdocs/install/mysql/tables/llx_c_incoterms.key.sql`, `htdocs/core/class/cincoterm.class.php:81`.

<a id="record-c_input_method"></a>

## Order method

Identifies the channel or means by which a commercial order was placed.

**Storage** `c_input_method`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(30) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_input_method.sql`, `htdocs/install/mysql/tables/llx_c_input_method.key.sql`, `htdocs/core/class/html.formorder.class.php:140`.

<a id="record-c_input_reason"></a>

## Commercial source

Identifies an origin or reason recorded for a commercial transaction.

**Storage** `c_input_reason`.
The primary key is `rowid`.
An additional unique key comprises `code`.

**Referenced by** [facture](billing.md#record-facture) (fk_input_reason).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(30) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_input_reason.sql`, `htdocs/install/mysql/tables/llx_c_input_reason.key.sql`, `htdocs/core/class/html.form.class.php:5266`.

<a id="record-c_invoice_subtype"></a>

## Invoice subtype

Provides named invoice classifications within an applicable invoice type or geographic context.

**Storage** `c_invoice_subtype`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `code`, `fk_country`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_country` | integer | No | — | Country associated with the record. |
| `code` | varchar(5) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(200) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_invoice_subtype.sql`, `htdocs/install/mysql/tables/llx_c_invoice_subtype.key.sql`, `htdocs/core/class/html.form.class.php:13156`.

<a id="record-c_lead_status"></a>

## Opportunity stage

Defines the named stages available for an opportunity or commercial lead.

**Storage** `c_lead_status`.
The primary key is `rowid`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(10) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `position` | integer | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `percent` | double(5,2) | Yes | — | Percentage recorded for the activity or calculation. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_lead_status.sql`, `htdocs/install/mysql/tables/llx_c_lead_status.key.sql`, `htdocs/core/class/cleadstatus.class.php:49`.

<a id="record-c_paiement"></a>

## Payment instrument

Identifies the method of settlement, such as a cheque, transfer or cash.

**Storage** `c_paiement`.
The primary key is `id`.
An additional unique key comprises `entity`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer (generated) | No | — | Internal identifier in this table. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(6) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `type` | smallint | Yes | — | Payment direction classification. Values 0, 1, 2 and 3 denote incoming, outgoing, both and other. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `accountancy_code` | varchar(32) | Yes | — | Account code selected for the transaction or classification. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_paiement.sql`, `htdocs/install/mysql/tables/llx_c_paiement.key.sql`, `htdocs/core/class/html.form.class.php:5371`.

<a id="record-c_paper_format"></a>

## Paper format

Defines physical page dimensions and display information used by document layout.

**Storage** `c_paper_format`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `width` | float(6,2) | Yes | `0` | Physical horizontal or vertical dimension, respectively. |
| `height` | float(6,2) | Yes | `0` | Physical horizontal or vertical dimension, respectively. |
| `unit` | varchar(5) | No | — | Measurement unit for paper dimensions. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_paper_format.sql`, `htdocs/core/class/html.formadmin.class.php:457`.

<a id="record-c_partnership_type"></a>

## Partnership type

Classifies the agreements available for a partner.

**Storage** `c_partnership_type`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `keyword` | varchar(128) | Yes | — | Term used to check for the configured reference on a partner website. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_partnership_type-partnership.sql`, `htdocs/install/mysql/tables/llx_c_partnership_type-partnership.key.sql`, `htdocs/partnership/class/partnership.class.php:403`.

<a id="record-c_payment_term"></a>

## Payment terms

Defines the code and timing parameters used to calculate a document's due date.

**Storage** `c_payment_term`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(16) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `sortorder` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `active` | tinyint | Yes | `1` | Whether this entry is enabled for selection or use. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `libelle_facture` | text | Yes | — | Description of the payment term presented on the invoice. |
| `type_cdr` | tinyint | Yes | — | Payment-term date calculation rule. |
| `nbjour` | smallint | Yes | — | Number of days used in computing the due date. |
| `decalage` | smallint | Yes | — | Offset used with the term's due-date rule. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_payment_term.sql`, `htdocs/install/mysql/tables/llx_c_payment_term.key.sql`, `htdocs/core/class/html.form.class.php:5090`.

<a id="record-c_product_nature"></a>

## Product nature

Enumerates additional commercial classifications for catalogue items.

**Storage** `c_product_nature`.
The primary key is `rowid`.
An additional unique key comprises `code`.

**Referenced by** [product](catalogue.md#record-product) (finished).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | tinyint | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_product_nature.sql`, `htdocs/install/mysql/tables/llx_c_product_nature.key.sql`, `htdocs/core/class/cproductnature.class.php:49`.

<a id="record-c_productbatch_qcstatus"></a>

## Batch quality state

Enumerates named quality-control states assignable to product lots.

**Storage** `c_productbatch_qcstatus`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(16) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `active` | integer | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_productbatch_qcstatus-productbatch.sql`, `htdocs/install/mysql/tables/llx_c_productbatch_qcstatus-productbatch.key.sql`, `htdocs/admin/dict.php:311`.

<a id="record-c_propalst"></a>

## Proposal status dictionary

Associates proposal status identifiers with their labels.

**Storage** `c_propalst`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | smallint | No | — | Internal identifier in this table. |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `sortorder` | smallint | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_propalst.sql`, `htdocs/install/mysql/tables/llx_c_propalst.key.sql`, `htdocs/core/class/html.formpropal.class.php:85`.

<a id="record-c_prospectcontactlevel"></a>

## Prospect contact level

Enumerates configured prospect-contact ratings.

**Storage** `c_prospectcontactlevel`.
The primary key is `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `sortorder` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `active` | smallint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_prospectcontactlevel.sql`, `htdocs/core/class/html.formcompany.class.php:226`.

<a id="record-c_prospectlevel"></a>

## Prospect potential

Identifies the potential or interest level recorded for a prospect.

**Storage** `c_prospectlevel`.
The primary key is `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `sortorder` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `active` | smallint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_prospectlevel.sql`, `htdocs/core/class/html.formcompany.class.php:175`.

<a id="record-c_regions"></a>

## Region

Defines a geographic region and its country association.

**Storage** `c_regions`.
The primary key is `rowid`.
Additional unique keys comprise `code_region` / `code_region`.

**Referenced by** [c_departements](dictionaries.md#record-c_departements) (fk_region).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code_region` | integer | No | — | Administrative region code. |
| `fk_pays` | integer | No | — | Country associated with the record. References [c_country](dictionaries.md#record-c_country) (rowid). |
| `cheflieu` | varchar(50) | Yes | — | Administrative capital of the geographic subdivision. |
| `tncc` | integer | Yes | — | Naming code associated with the region. |
| `nom` | varchar(100) | Yes | — | Name under which this record is presented or identified. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_regions.sql`, `htdocs/install/mysql/tables/llx_c_departements.key.sql`, `htdocs/install/mysql/tables/llx_c_regions.key.sql`, `htdocs/core/class/cregion.class.php:106`.

<a id="record-c_revenuestamp"></a>

## Revenue stamp

Stores stamp amounts and jurisdictional settings available to invoice calculations.

**Storage** `c_revenuestamp`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_pays` | integer | No | — | Country associated with the record. |
| `taux` | double | No | — | Percentage rate. |
| `revenuestamp_type` | varchar(16) | No | `'fixed'` | Classification of the revenue stamp. |
| `note` | varchar(128) | Yes | — | Free-text annotation retained with the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `accountancy_code_sell` | varchar(32) | Yes | `NULL` | Account code used for the respective sales or purchase accounting mapping. |
| `accountancy_code_buy` | varchar(32) | Yes | `NULL` | Account code used for the respective sales or purchase accounting mapping. |

Source locations include `htdocs/install/mysql/tables/llx_c_revenuestamp.sql`, `htdocs/core/class/html.formother.class.php:342`.

<a id="record-c_shipment_mode"></a>

## Shipping method

Identifies the carrier or delivery method selected for a shipment.

**Storage** `c_shipment_mode`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

**Referenced by** [expedition](commercial.md#record-expedition) (fk_shipping_method), [reception](commercial.md#record-reception) (fk_shipping_method).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `code` | varchar(30) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `tracking` | varchar(255) | Yes | — | Tracking information configured for the shipment method. |
| `active` | tinyint | Yes | `0` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |

Source locations include `htdocs/install/mysql/tables/llx_c_shipment_mode.sql`, `htdocs/install/mysql/tables/llx_c_shipment_mode.key.sql`, `htdocs/core/class/html.form.class.php:5866`.

<a id="record-c_shipment_package_type"></a>

## Package type

Enumerates the kinds of packaging available through the generic dictionary mechanism.

**Storage** `c_shipment_package_type`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `active` | integer | No | `1` | Whether this entry is enabled for selection or use. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_c_shipment_package_type.sql`, `htdocs/core/class/cgenericdic.class.php:163`.

<a id="record-c_socialnetworks"></a>

## Social network

Lists network identifiers available for recording social contact information.

**Storage** `c_socialnetworks`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(100) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(150) | Yes | — | Display label for the record. |
| `url` | text | Yes | — | Web address or navigation target. |
| `icon` | varchar(20) | Yes | — | Icon associated with the social network. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_socialnetworks.sql`, `htdocs/install/mysql/tables/llx_c_socialnetworks.key.sql`, `htdocs/api/class/api_setup.class.php:2242`.

<a id="record-c_stcomm"></a>

## Party prospecting state

Names the commercial prospecting states for a third party.

**Storage** `c_stcomm`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `code` | varchar(24) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `picto` | varchar(128) | Yes | — | Icon identifier used for presentation. |
| `sortorder` | smallint | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_stcomm.sql`, `htdocs/install/mysql/tables/llx_c_stcomm.key.sql`, `htdocs/admin/dict.php:295`.

<a id="record-c_stcommcontact"></a>

## Contact prospecting state

Names the commercial follow-up states for a contact.

**Storage** `c_stcommcontact`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `picto` | varchar(128) | Yes | — | Icon identifier used for presentation. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_stcommcontact.sql`, `htdocs/install/mysql/tables/llx_c_stcommcontact.key.sql`, `htdocs/admin/dict.php:308`.

<a id="record-c_ticket_category"></a>

## Ticket category

Classifies the subject area of a support request.

**Storage** `c_ticket_category`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `public` | integer | Yes | `0` | Publication or visibility selection for the record. |
| `use_default` | integer | Yes | `1` | Marks the candidate used as a default where the applicable selection permits it. |
| `fk_parent` | integer | No | `0` | Record one level above this one in the owning hierarchy. |
| `force_severity` | varchar(32) | Yes | — | Forceseverity. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `pos` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |
| `fk_ticket_type` | integer | Yes | — | Ticket type to which this category applies. |

Source locations include `htdocs/install/mysql/tables/llx_c_ticket_category-ticket.sql`, `htdocs/install/mysql/tables/llx_c_ticket_category-ticket.key.sql`, `htdocs/core/class/html.formticket.class.php:1121`.

<a id="record-c_ticket_resolution"></a>

## Ticket resolution

Enumerates the reasons or outcomes available when resolving a ticket.

**Storage** `c_ticket_resolution`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `pos` | varchar(32) | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |
| `use_default` | integer | Yes | `1` | Marks the candidate used as a default where the applicable selection permits it. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |

Source locations include `htdocs/install/mysql/tables/llx_c_ticket_resolution-ticket.sql`, `htdocs/install/mysql/tables/llx_c_ticket_resolution-ticket.key.sql`, `htdocs/core/modules/modTicket.class.php:200`.

<a id="record-c_ticket_severity"></a>

## Ticket severity

Defines the available issue severity levels.

**Storage** `c_ticket_severity`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `pos` | varchar(32) | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `color` | varchar(10) | Yes | — | Display colour assigned to this entry. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |
| `use_default` | integer | Yes | `1` | Marks the candidate used as a default where the applicable selection permits it. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |

Source locations include `htdocs/install/mysql/tables/llx_c_ticket_severity-ticket.sql`, `htdocs/install/mysql/tables/llx_c_ticket_severity-ticket.key.sql`, `htdocs/api/class/api_setup.class.php:2370`.

<a id="record-c_ticket_type"></a>

## Ticket type

Defines the kinds of support request that can be registered.

**Storage** `c_ticket_type`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `pos` | varchar(32) | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |
| `use_default` | integer | Yes | `1` | Marks the candidate used as a default where the applicable selection permits it. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |

Source locations include `htdocs/install/mysql/tables/llx_c_ticket_type-ticket.sql`, `htdocs/install/mysql/tables/llx_c_ticket_type-ticket.key.sql`, `htdocs/api/class/api_setup.class.php:2435`.

<a id="record-c_transport_mode"></a>

## Transport mode

Provides named transport modes that can be selected where the associated field is available.

**Storage** `c_transport_mode`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(3) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_transport_mode.sql`, `htdocs/install/mysql/tables/llx_c_transport_mode.key.sql`, `htdocs/core/class/html.form.class.php:5742`.

<a id="record-c_tva"></a>

## VAT rate

Stores a rate in its country, code and validity context with associated local-tax settings.

**Storage** `c_tva`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_pays`, `code`, `taux`, `recuperableonly`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_pays` | integer | No | — | Country associated with the record. |
| `fk_department_buyer` | integer | Yes | `NULL` | References [c_departements](dictionaries.md#record-c_departements) (rowid). |
| `code` | varchar(10) | Yes | empty string | Machine-readable code identifying a dictionary entry or feature value. |
| `type_vat` | smallint | No | `0` | Applicability of the VAT rate. Zero allows both directions, one denotes sales and two denotes purchases. |
| `taux` | double | No | — | VAT rate percentage for the tax code and country. |
| `localtax1` | varchar(20) | No | `'0'` | Value of the corresponding local tax component on the record. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2` | varchar(20) | No | `'0'` | Value of the corresponding local tax component on the record. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `use_default` | tinyint | Yes | `0` | Marks the candidate used as a default where the applicable selection permits it. |
| `recuperableonly` | integer | No | `0` | Marks the VAT treatment recorded as recoverable-only in the source tax configuration. |
| `einvoice_vatex` | varchar(32) | Yes | — | Exemption classification used in electronic invoicing. |
| `note` | varchar(128) | Yes | — | Free-text annotation retained with the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `accountancy_code_sell` | varchar(32) | Yes | `NULL` | Account code used for the respective sales or purchase accounting mapping. |
| `accountancy_code_buy` | varchar(32) | Yes | `NULL` | Account code used for the respective sales or purchase accounting mapping. |

Source locations include `htdocs/install/mysql/tables/llx_c_tva.sql`, `htdocs/install/mysql/tables/llx_c_tva.key.sql`, `htdocs/core/class/html.form.class.php:7917`.

<a id="record-c_type_contact"></a>

## Contact role

Identifies a role for a document type and distinguishes internal employees from external contacts.

**Storage** `c_type_contact`.
The primary key is `rowid`.
An additional unique key comprises `element`, `source`, `code`.

**Referenced by** [element_contact](parties.md#record-element_contact) (fk_c_type_contact), [societe_contacts](parties.md#record-societe_contacts) (fk_c_type_contact).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `element` | varchar(64) | No | — | Business object family to which a contact role can apply. |
| `source` | varchar(8) | No | `'external'` | Selects the employee or third-party contact namespace for the role. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | No | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_type_contact.sql`, `htdocs/install/mysql/tables/llx_c_type_contact.key.sql`, `htdocs/core/class/commonobject.class.php:1385`.

<a id="record-c_type_container"></a>

## Page container type

Enumerates structures available for a website content container.

**Storage** `c_type_container`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `typecontainer` | varchar(10) | Yes | `'page'` | Name of the supported web content container type. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_type_container-website.sql`, `htdocs/install/mysql/tables/llx_c_type_container-website.key.sql`, `htdocs/core/class/html.formwebsite.class.php:123`.

<a id="record-c_type_fees"></a>

## Expense type

Defines the expense classifications used when recording a claim.

**Storage** `c_type_fees`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer (generated) | No | — | Internal identifier in this table. |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `type` | integer | Yes | `0` | Type. |
| `accountancy_code` | varchar(32) | Yes | — | Account code selected for the transaction or classification. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_type_fees.sql`, `htdocs/install/mysql/tables/llx_c_type_fees.key.sql`, `htdocs/core/class/html.form.class.php:1761`.

<a id="record-c_type_resource"></a>

## Resource type

Classifies equipment and other resources that can be allocated to an activity.

**Storage** `c_type_resource`.
The primary key is `rowid`.
An additional unique key comprises `label`, `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_type_resource.sql`, `htdocs/install/mysql/tables/llx_c_type_resource.key.sql`, `htdocs/core/class/ctyperesource.class.php:45`.

<a id="record-c_typent"></a>

## Organisation type

Enumerates the classifications available for a third party.

**Storage** `c_typent`.
The primary key is `id`.
An additional unique key comprises `code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `code` | varchar(12) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `libelle` | varchar(128) | Yes | — | Display label for the record. |
| `fk_country` | integer | Yes | — | Country associated with the record. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `module` | varchar(32) | Yes | — | Feature or extension to which this entry belongs. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_c_typent.sql`, `htdocs/install/mysql/tables/llx_c_typent.key.sql`, `htdocs/core/class/ctypent.class.php:93`.

<a id="record-c_units"></a>

## Unit of measure

Defines a measure, its label and scaling metadata used by products or transaction lines.

**Storage** `c_units`.
The primary key is `rowid`.
An additional unique key comprises `code`.

**Referenced by** [commande_fournisseurdet](commercial.md#record-commande_fournisseurdet) (fk_unit), [commandedet](commercial.md#record-commandedet) (fk_unit), [contratdet](people.md#record-contratdet) (fk_unit), [facture_fourn_det](billing.md#record-facture_fourn_det) (fk_unit), [facture_fourn_det_rec](billing.md#record-facture_fourn_det_rec) (fk_unit), [facturedet](billing.md#record-facturedet) (fk_unit), [facturedet_rec](billing.md#record-facturedet_rec) (fk_unit), [product](catalogue.md#record-product) (fk_unit), [propaldet](commercial.md#record-propaldet) (fk_unit), [supplier_proposaldet](commercial.md#record-supplier_proposaldet) (fk_unit).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(3) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `sortorder` | smallint | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `scale` | integer | Yes | — | Scale value of the measurement unit in its unit family. |
| `label` | varchar(128) | Yes | — | Display label for the record. |
| `short_label` | varchar(5) | Yes | — | Abbreviated presentation of the unit. |
| `unit_type` | varchar(10) | Yes | — | Measurement family of the unit. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_units.sql`, `htdocs/install/mysql/tables/llx_c_units.key.sql`, `htdocs/core/class/cunits.class.php:121`.

<a id="record-c_ziptown"></a>

## Postal locality

Associates postal codes and town names with applicable geographic information.

**Storage** `c_ziptown`.
The primary key is `rowid`.
An additional unique key comprises `zip`, `town`, `fk_pays`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `code` | varchar(5) | Yes | `NULL` | Machine-readable code identifying a dictionary entry or feature value. |
| `fk_county` | integer | Yes | — | References [c_departements](dictionaries.md#record-c_departements) (rowid). |
| `fk_pays` | integer | No | `0` | Country associated with the record. References [c_country](dictionaries.md#record-c_country) (rowid). |
| `zip` | varchar(10) | No | — | Postal code. |
| `town` | varchar(180) | No | — | Town or city. |
| `town_up` | varchar(180) | Yes | — | Uppercase representation of the town name for lookup. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_c_ziptown.sql`, `htdocs/install/mysql/tables/llx_c_ziptown.key.sql`, `htdocs/api/class/api_setup.class.php:1850`.
