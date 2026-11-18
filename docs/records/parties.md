# Third parties, contacts and relationships

A party supplies the commercial identity across purchases and sales. Contacts are separate records. A typed document contact assignment identifies the role for one document, while a default party contact can supply that role on future documents.

**Example.** One company can be both a customer and a supplier, with several contacts. A person designated as the contact for a particular shipment need not be the default billing contact. Retain the party, the role definition and the document assignment as separate identities.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Third party](#record-societe) | `societe` |
| [Contact or address](#record-socpeople) | `socpeople` |
| [Sales assignment](#record-societe_commerciaux) | `societe_commerciaux` |
| [Default contact role](#record-societe_contacts) | `societe_contacts` |
| [External account mapping](#record-societe_account) | `societe_account` |
| [Party price-level history](#record-societe_prices) | `societe_prices` |
| [Party bank and mandate details](#record-societe_rib) | `societe_rib` |
| [Customer percentage discount history](#record-societe_remise) | `societe_remise` |
| [Supplier percentage discount history](#record-societe_remise_supplier) | `societe_remise_supplier` |
| [Fixed credit or discount](#record-societe_remise_except) | `societe_remise_except` |
| [Partnership agreement](#record-partnership) | `partnership` |
| [Document contact assignment](#record-element_contact) | `element_contact` |
| [Typed document relationship](#record-element_element) | `element_element` |
| [Resource association](#record-element_resources) | `element_resources` |

<a id="record-societe"></a>

## Third party

Identifies an organisation or individual that buys, sells or is being prospected. Commercial documents can keep separate role and address snapshots.

**Storage** `societe`.
The primary key is `rowid`.
Additional unique keys comprise `prefix_comm`, `entity` / `code_client`, `entity` / `code_fournisseur`, `entity` / `barcode`, `fk_barcode_type`, `entity`.

**Referenced by** [adherent](people.md#record-adherent) (fk_soc), [categorie_fournisseur](categories.md#record-categorie_fournisseur) (fk_soc), [categorie_societe](categories.md#record-categorie_societe) (fk_soc), [commande](commercial.md#record-commande) (fk_soc), [commande_fournisseur](commercial.md#record-commande_fournisseur) (fk_soc), [contrat](people.md#record-contrat) (fk_soc), [delivery](commercial.md#record-delivery) (fk_soc), [expedition](commercial.md#record-expedition) (fk_soc), [facture](billing.md#record-facture) (fk_soc), [facture_fourn](billing.md#record-facture_fourn) (fk_soc), [facture_fourn_rec](billing.md#record-facture_fourn_rec) (fk_soc), [facture_rec](billing.md#record-facture_rec) (fk_soc), [fichinter](people.md#record-fichinter) (fk_soc), [product_customer_price](catalogue.md#record-product_customer_price) (fk_soc), [projet](production.md#record-projet) (fk_soc), [propal](commercial.md#record-propal) (fk_soc), [reception](commercial.md#record-reception) (fk_soc), [societe_account](parties.md#record-societe_account) (fk_soc), [societe_commerciaux](parties.md#record-societe_commerciaux) (fk_soc), [societe_contacts](parties.md#record-societe_contacts) (fk_soc), [societe_remise_except](parties.md#record-societe_remise_except) (fk_soc), [societe_rib](parties.md#record-societe_rib) (fk_soc), [socpeople](parties.md#record-socpeople) (fk_soc).

The record class defines `0` ceased, `1` inactivity. See `htdocs/societe/class/societe.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `nom` | varchar(128) | Yes | — | Name under which this record is presented or identified. |
| `name_alias` | varchar(128) | Yes | — | Alternate or trading name. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `statut` | tinyint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `parent` | integer | Yes | — | Parent. |
| `status` | tinyint | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `code_client` | varchar(24) | Yes | — | Customer Code. |
| `code_fournisseur` | varchar(24) | Yes | — | Vendor Code. |
| `tp_payment_reference` | varchar(25) | Yes | — | Payment identifier assigned to the counterparty for use in payment instructions. |
| `accountancy_code_customer_general` | varchar(32) | Yes | `NULL` | General receivables account selected for transactions with this customer. |
| `code_compta` | varchar(32) | Yes | — | Customer accounting code. |
| `accountancy_code_supplier_general` | varchar(32) | Yes | `NULL` | General payables account selected for transactions with this supplier. |
| `code_compta_fournisseur` | varchar(32) | Yes | — | Vendor accounting code. |
| `address` | varchar(255) | Yes | — | Postal or street address. |
| `zip` | varchar(25) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `fk_departement` | integer | Yes | `0` | Administrative subdivision identity in an address. |
| `fk_pays` | integer | Yes | `0` | Country associated with the record. |
| `geolat` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geolong` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geopoint` | point | Yes | `NULL` | Geographic point value retained by the location field. |
| `georesultcode` | varchar(16) | Yes | — | Geocoding result or accuracy code. |
| `phone` | varchar(30) | Yes | — | Telephone number. |
| `phone_mobile` | varchar(30) | Yes | — | Mobile telephone number. |
| `fax` | varchar(30) | Yes | — | Fax number. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `email` | varchar(128) | Yes | — | Email address associated with this record. |
| `fk_account` | integer | Yes | `0` | Financial account identifier as used by the owning record. |
| `socialnetworks` | text | Yes | `NULL` | Social contact handles associated with the party or person. |
| `fk_effectif` | integer | Yes | `0` | Workforce. |
| `fk_typent` | integer | Yes | `NULL` | Third-party type. |
| `fk_forme_juridique` | integer | Yes | `0` | Business entity type. |
| `birth` | date | Yes | — | Birth date. |
| `fk_currency` | varchar(3) | Yes | — | Currency identifier for this record. |
| `siren` | varchar(128) | Yes | — | Idprof1. |
| `siret` | varchar(128) | Yes | — | Idprof2. |
| `ape` | varchar(128) | Yes | — | Idprof3. |
| `idprof4` | varchar(128) | Yes | — | Idprof4. |
| `idprof5` | varchar(128) | Yes | — | Idprof5. |
| `idprof6` | varchar(128) | Yes | — | Idprof6. |
| `euid` | varchar(64) | Yes | — | EUID. |
| `tva_intra` | varchar(20) | Yes | — | VAT ID. |
| `capital` | double(24,8) | Yes | `NULL` | Principal of the loan. |
| `fk_stcomm` | integer | No | `0` | Commercial Status. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `prefix_comm` | varchar(5) | Yes | — | Historical commercial numbering prefix retained in storage. |
| `client` | tinyint | Yes | `0` | Commercial customer and prospect role. The client/prospect combination can coexist with supplier status. |
| `fournisseur` | tinyint | Yes | `0` | Supplier role of this party. |
| `supplier_account` | varchar(32) | Yes | — | Supplier account. |
| `fk_prospectlevel` | varchar(12) | Yes | — | Prospect potential rating. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `customer_bad` | tinyint | Yes | `0` | Customer bad. |
| `customer_rate` | real | Yes | `0` | Customer rate. |
| `supplier_rate` | real | Yes | `0` | Supplier rate. |
| `remise_client` | real | Yes | `0` | Customer discount percentage. |
| `remise_supplier` | real | Yes | `0` | Supplier discount percentage. |
| `mode_reglement` | integer | Yes | — | Default settlement instrument for the relevant commercial role. |
| `cond_reglement` | tinyint | Yes | — | Default settlement terms for the relevant commercial role. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `transport_mode` | tinyint | Yes | — | Transport-method information retained for optional trade reporting. |
| `mode_reglement_supplier` | tinyint | Yes | — | Default settlement instrument for the relevant commercial role. |
| `cond_reglement_supplier` | tinyint | Yes | — | Default settlement terms for the relevant commercial role. |
| `transport_mode_supplier` | tinyint | Yes | — | Transport-method information retained for optional trade reporting. |
| `fk_shipping_method` | integer | Yes | — | Selected dispatch or transport service. |
| `tva_assuj` | tinyint | Yes | `1` | Sales tax used. |
| `vatexemptcode` | varchar(24) | Yes | — | Code identifying the reason for VAT exemption. |
| `vat_reverse_charge` | tinyint | Yes | `0` | Indicates the reverse-charge tax treatment on a purchase. |
| `localtax1_assuj` | tinyint | Yes | `0` | Use second tax. |
| `localtax1_value` | double(7,4) | Yes | — | Local Tax1 value. |
| `localtax2_assuj` | tinyint | Yes | `0` | Use third tax. |
| `localtax2_value` | double(7,4) | Yes | — | Local Tax2 value. |
| `barcode` | varchar(180) | Yes | — | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `0` | Symbology used for the barcode. |
| `price_level` | integer | Yes | — | Sales price level or tier. |
| `outstanding_limit` | double(24,8) | Yes | `NULL` | Max. for outstanding bill. |
| `order_min_amount` | double(24,8) | Yes | `NULL` | Order min amount. |
| `supplier_order_min_amount` | double(24,8) | Yes | `NULL` | Supplier order min amount. |
| `default_lang` | varchar(6) | Yes | — | Default language selected for communication or display. |
| `logo` | varchar(255) | Yes | `NULL` | Logo. |
| `logo_squarred` | varchar(255) | Yes | `NULL` | Logo squarred. |
| `canvas` | varchar(32) | Yes | `NULL` | Alternate form or presentation model selected for the object. |
| `fk_warehouse` | integer | Yes | `NULL` | Warehouse or stock location. |
| `webservices_url` | varchar(255) | Yes | — | Webservices url. |
| `webservices_key` | varchar(128) | Yes | — | Webservices key. |
| `accountancy_code_sell` | varchar(32) | Yes | — | Account code used for the respective sales or purchase accounting mapping. |
| `accountancy_code_buy` | varchar(32) | Yes | — | Account code used for the respective sales or purchase accounting mapping. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_societe.sql`, `htdocs/install/mysql/tables/llx_societe.key.sql`, `htdocs/societe/class/societe.class.php:81`.

<a id="record-socpeople"></a>

## Contact or address

Identifies a person or address, optionally attached to a third party. Document-specific responsibility is assigned separately.

**Storage** `socpeople`.
The primary key is `rowid`.

**Referenced by** [categorie_contact](categories.md#record-categorie_contact) (fk_socpeople), [societe_contacts](parties.md#record-societe_contacts) (fk_socpeople).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `name_alias` | varchar(255) | Yes | — | Alternate or trading name. |
| `fk_parent` | integer | Yes | — | Record one level above this one in the owning hierarchy. |
| `civility` | varchar(6) | Yes | — | Person's form of address. |
| `lastname` | varchar(50) | Yes | — | Person's family name. |
| `firstname` | varchar(50) | Yes | — | Person's given name. |
| `address` | varchar(255) | Yes | — | Postal or street address. |
| `zip` | varchar(25) | Yes | — | Postal code. |
| `town` | varchar(255) | Yes | — | Town or city. |
| `fk_departement` | integer | Yes | — | Administrative subdivision identity in an address. |
| `fk_pays` | integer | Yes | `0` | Country associated with the record. |
| `geolat` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geolong` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geopoint` | point | Yes | `NULL` | Geographic point value retained by the location field. |
| `georesultcode` | varchar(16) | Yes | — | Geocoding result or accuracy code. |
| `birthday` | date | Yes | — | Birthday. |
| `poste` | varchar(255) | Yes | — | Job title of the contact within its organisation. |
| `phone` | varchar(30) | Yes | — | Telephone number. |
| `phone_perso` | varchar(30) | Yes | — | Personal telephone number. |
| `phone_mobile` | varchar(30) | Yes | — | Mobile telephone number. |
| `fax` | varchar(30) | Yes | — | Fax number. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `socialnetworks` | text | Yes | `NULL` | Social contact handles associated with the party or person. |
| `photo` | varchar(255) | Yes | — | Reference to an image attached to this person or object. |
| `no_email` | smallint | No | `0` | Compatibility flag. Opt-outs for campaigns are retained in mailing_unsubscribe. |
| `priv` | smallint | No | `0` | Visibility. |
| `fk_prospectlevel` | varchar(12) | Yes | — | Prospect potential rating. |
| `fk_stcommcontact` | integer | No | `0` | Prospect status. |
| `fk_user_creat` | integer | Yes | `0` | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `default_lang` | varchar(6) | Yes | — | Default language selected for communication or display. |
| `canvas` | varchar(32) | Yes | — | Alternate form or presentation model selected for the object. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `statut` | tinyint | No | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

Source locations include `htdocs/install/mysql/tables/llx_socpeople.sql`, `htdocs/install/mysql/tables/llx_socpeople.key.sql`, `htdocs/core/class/notify.class.php:492`.

<a id="record-societe_commerciaux"></a>

## Sales assignment

Associates a third party with a user responsible for its commercial relationship. This link can affect an internal user's record visibility.

**Storage** `societe_commerciaux`.
The primary key is `rowid`.
An additional unique key comprises `fk_soc`, `fk_user`, `fk_c_type_contact_code`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_user` | integer | Yes | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `fk_c_type_contact_code` | varchar(32) | No | `'SALESREPTHIRD'` | Contact-role code for the commercial assignment. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_societe_commerciaux.sql`, `htdocs/install/mysql/tables/llx_societe_commerciaux.key.sql`, `htdocs/core/class/html.form.class.php:2070`.

<a id="record-societe_contacts"></a>

## Default contact role

Associates a party and contact with a defined role, for reuse when populating business documents.

**Storage** `societe_contacts`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_soc`, `fk_c_type_contact`, `fk_socpeople`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `date_creation` | datetime | No | — | When the row was created. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_c_type_contact` | int | No | — | Role that establishes what the contact represents on a particular object type. References [c_type_contact](dictionaries.md#record-c_type_contact) (rowid). |
| `fk_socpeople` | integer | No | — | Contact identity. Some generic role assignments resolve differently for internal and external contacts. References [socpeople](parties.md#record-socpeople) (rowid). |
| `tms` | timestamp | Yes | — | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_societe_contacts.sql`, `htdocs/install/mysql/tables/llx_societe_contacts.key.sql`, `htdocs/contact/class/contact.class.php:1366`.

<a id="record-societe_account"></a>

## External account mapping

Records a party's account on a named external or hosted site, with identity, login status and timestamps.

**Storage** `societe_account`.
The primary key is `rowid`.
Additional unique keys comprise `entity`, `login`, `site`, `fk_website` / `entity`, `fk_soc`, `key_account`, `site`, `fk_website`.

The record class defines `1` enabled, `0` disabled. See `htdocs/societe/class/societeaccount.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `login` | varchar(128) | No | — | Login name of the account. |
| `pass_encoding` | varchar(24) | Yes | — | Encoding scheme associated with the stored credential. |
| `pass_crypted` | varchar(128) | Yes | — | Stored encoded credential. |
| `pass_temp` | varchar(128) | Yes | — | Temporary credential/reset value recorded by the account mechanism. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_website` | integer | Yes | — | Website concerned. |
| `site` | varchar(128) | No | — | Type of Web site. |
| `site_account` | varchar(128) | Yes | — | External Site Account. |
| `key_account` | varchar(128) | Yes | — | Key Account. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_last_login` | datetime | Yes | — | Last login. |
| `date_previous_login` | datetime | Yes | — | Previous login. |
| `date_last_reset_password` | datetime | Yes | — | Previous Reset Password. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | Yes | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_societe_account.sql`, `htdocs/install/mysql/tables/llx_societe_account.key.sql`, `htdocs/societe/class/societeaccount.class.php:48`.

<a id="record-societe_prices"></a>

## Party price-level history

Dates the price level selected for a third party and records the user who made the change.

**Storage** `societe_prices`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_soc` | integer | Yes | `0` | Third party associated with this record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `price_level` | tinyint | Yes | `1` | Sales price level or tier. |

Source locations include `htdocs/install/mysql/tables/llx_societe_prices.sql`, `htdocs/societe/class/societe.class.php:3121`.

<a id="record-societe_rib"></a>

## Party bank and mandate details

Identifies one set of bank coordinates held for a customer or supplier. Mandate information and preferred account selection belong to this record.

**Storage** `societe_rib`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `label`, `fk_soc`.

The record class defines `0` open, `1` closed. See `htdocs/societe/class/companybankaccount.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `type` | varchar(32) | No | `'ban'` | Type. |
| `label` | varchar(180) | Yes | — | Display label for the record. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `bank` | varchar(255) | Yes | — | Name of the financial institution for the account details. |
| `code_banque` | varchar(128) | Yes | — | Domestic bank code. |
| `code_guichet` | varchar(6) | Yes | — | Domestic branch code. |
| `number` | varchar(255) | Yes | — | Number. |
| `cle_rib` | varchar(5) | Yes | — | Check digits for the domestic bank account identifier. |
| `bic` | varchar(20) | Yes | — | Bank identifier code for the receiving institution. |
| `bic_intermediate` | varchar(11) | Yes | — | Identifier of the intermediary financial institution. |
| `iban_prefix` | varchar(100) | Yes | — | International bank account number field used with the selected banking details. |
| `cci` | varchar(100) | Yes | — | Country-specific interbank account code. |
| `domiciliation` | varchar(255) | Yes | — | Bank or branch domiciliation details. |
| `proprio` | varchar(60) | Yes | — | Name of the bank-account holder. |
| `owner_address` | varchar(255) | Yes | — | Address recorded for the bank-account holder. |
| `default_rib` | smallint | No | `0` | Selects the default set of bank details. |
| `state_id` | integer | Yes | — | Administrative subdivision identity in an address. |
| `fk_country` | integer | Yes | — | Country associated with the record. |
| `currency_code` | varchar(3) | Yes | — | Currency identifier for this record. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `rum` | varchar(32) | Yes | — | Rum. |
| `date_rum` | date | Yes | — | Date rum. |
| `frstrecur` | varchar(16) | Yes | `'FRST'` | Frstrecur. |
| `last_four` | varchar(4) | Yes | — | Last four. |
| `card_type` | varchar(255) | Yes | — | Card type. |
| `cvn` | varchar(255) | Yes | — | Cvn. |
| `exp_date_month` | integer | Yes | — | Exp date month. |
| `exp_date_year` | integer | Yes | — | Exp date year. |
| `country_code` | varchar(10) | Yes | — | Country code. |
| `approved` | integer | Yes | `0` | Approved. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `ending_date` | date | Yes | — | Ending date. |
| `max_total_amount_of_all_payments` | double(24,8) | Yes | — | Max total amount of all payments. |
| `preapproval_key` | varchar(255) | Yes | — | Preapproval key. |
| `starting_date` | date | Yes | — | Starting date. |
| `total_amount_of_all_payments` | double(24,8) | Yes | — | Total amount of all payments. |
| `stripe_card_ref` | varchar(128) | Yes | — | External system ID. |
| `stripe_account` | varchar(128) | Yes | — | External System Customer Account. |
| `ext_payment_site` | varchar(128) | Yes | — | External payment service or provider identifier. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `date_signature` | datetime | Yes | — | Date the agreement or offer was signed. |
| `online_sign_ip` | varchar(48) | Yes | — | Network address retained when the remote signature was submitted. |
| `online_sign_name` | varchar(64) | Yes | — | Name supplied during online signature. |
| `comment` | varchar(255) | Yes | — | Free-text annotation retained with the record. |
| `ipaddress` | varchar(68) | Yes | — | Ipaddress. |
| `status` | integer | No | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_societe_rib.sql`, `htdocs/install/mysql/tables/llx_societe_rib.key.sql`, `htdocs/core/class/html.form.class.php:6181`.

<a id="record-societe_remise"></a>

## Customer percentage discount history

Records the customer discount rate, date and author applicable to the party.

**Storage** `societe_remise`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Third party associated with this record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `remise_client` | double(7,4) | No | `0` | Customer discount percentage. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |

Source locations include `htdocs/install/mysql/tables/llx_societe_remise.sql`, `htdocs/societe/class/societe.class.php:2011`.

<a id="record-societe_remise_supplier"></a>

## Supplier percentage discount history

Records the supplier discount rate and the actor who entered it.

**Storage** `societe_remise_supplier`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Third party associated with this record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `remise_supplier` | double(7,4) | No | `0` | Supplier discount percentage. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |

Source locations include `htdocs/install/mysql/tables/llx_societe_remise_supplier.sql`, `htdocs/societe/class/societe.class.php:2012`.

<a id="record-societe_remise_except"></a>

## Fixed credit or discount

Retains a monetary benefit available to a party, its tax and currency components, source invoice and eventual application to a bill or a bill line.

**Storage** `societe_remise_except`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Party that owns the available discount or credit. References [societe](parties.md#record-societe) (rowid). |
| `discount_type` | integer | No | `0` | Identifies a customer adjustment (0) or supplier adjustment (1). |
| `datec` | datetime | Yes | — | When the row was created. |
| `amount_ht` | double(24,8) | No | — | Monetary amount before tax. |
| `amount_tva` | double(24,8) | No | `0` | VAT component of the available adjustment. |
| `amount_localtax1` | double(24,8) | No | `0` | First local tax component of the adjustment. |
| `amount_localtax2` | double(24,8) | No | `0` | Second local tax component of the adjustment. |
| `amount_ttc` | double(24,8) | No | `0` | Adjustment amount including tax. |
| `tva_tx` | double(7,4) | No | `0` | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | No | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | No | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `fk_user` | integer | No | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `fk_facture_line` | integer | Yes | — | Customer invoice line to which a credit has been applied. References [facturedet](billing.md#record-facturedet) (rowid). |
| `fk_facture` | integer | Yes | — | Customer invoice identifier. References [facture](billing.md#record-facture) (rowid). |
| `fk_facture_source` | integer | Yes | — | Customer invoice from which this replacement, credit or adjustment originates. References [facture](billing.md#record-facture) (rowid). |
| `fk_invoice_supplier_line` | integer | Yes | — | Supplier bill line to which a credit has been applied. References [facture_fourn_det](billing.md#record-facture_fourn_det) (rowid). |
| `fk_invoice_supplier` | integer | Yes | — | Supplier invoice identifier. References [facture_fourn](billing.md#record-facture_fourn) (rowid). References [facture_fourn](billing.md#record-facture_fourn) (rowid). |
| `fk_invoice_supplier_source` | integer | Yes | — | Supplier invoice that originated the credit or deposit. |
| `description` | text | No | — | Descriptive text associated with this entry. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | — | Exchange rate retained for the transaction or price record. |
| `multicurrency_amount_ht` | double(24,8) | No | `0` | Tax-exclusive adjustment in the document currency. |
| `multicurrency_amount_tva` | double(24,8) | No | `0` | VAT on the adjustment in the document currency. |
| `multicurrency_amount_ttc` | double(24,8) | No | `0` | Tax-inclusive adjustment in the document currency. |

Source locations include `htdocs/install/mysql/tables/llx_societe_remise_except.sql`, `htdocs/install/mysql/tables/llx_societe_remise_except.key.sql`, `htdocs/core/class/discount.class.php:242`.

<a id="record-partnership"></a>

## Partnership agreement

Records the partner, agreement type, effective period, administrative state and reason for refusal or termination. The row identifies its creator and latest modifier. The approval operation writes the approved state and emits an acceptance event with the acting user.

**Storage** `partnership`.
The primary key is `rowid`.
Additional unique keys comprise `ref`, `entity` / `fk_type`, `fk_soc`, `date_partnership_start` / `fk_type`, `fk_member`, `date_partnership_start`.

The record class defines `0` draft, `1` validated, `2` approved, `3` refused, `9` canceled. See `htdocs/partnership/class/partnership.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `status` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_type` | integer | No | `0` | Named type selected from the relevant dictionary. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_member` | integer | Yes | — | Association member identity. |
| `email_partnership` | varchar(64) | Yes | — | Email address specific to this partnership. |
| `date_partnership_start` | date | No | — | Start date. |
| `date_partnership_end` | date | Yes | — | End date. |
| `reason_decline_or_cancel` | text | Yes | — | Reason for refusal or cancellation. |
| `date_creation` | datetime | No | — | When the row was created. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `url_to_check` | varchar(255) | Yes | — | Url to check. |
| `count_last_url_check_error` | integer | Yes | `'0'` | Number of URL check errors. |
| `last_check_backlink` | datetime | Yes | — | Date of last URL check. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |

Source locations include `htdocs/install/mysql/tables/llx_partnership-partnership.sql`, `htdocs/install/mysql/tables/llx_partnership-partnership.key.sql` and `htdocs/partnership/class/partnership.class.php:773–885`.

<a id="record-element_contact"></a>

## Document contact assignment

Assigns a contact in a named role to a document. The role determines the kind of document and whether the referenced person is an employee or third-party contact.

**Storage** `element_contact`.
The primary key is `rowid`.
An additional unique key comprises `element_id`, `fk_c_type_contact`, `fk_socpeople`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datecreate` | datetime | Yes | — | When the row was created. |
| `statut` | smallint | Yes | `5` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `element_id` | int | No | — | Identity of the document receiving the role. The contact-type definition supplies its document family. |
| `mandatory_signature` | tinyint | Yes | — | Marks the assigned contact's signature as required on the document. |
| `fk_c_type_contact` | int | No | — | Role that establishes what the contact represents on a particular object type. References [c_type_contact](dictionaries.md#record-c_type_contact) (rowid). |
| `fk_socpeople` | integer | No | — | Person referenced by this assignment. The contact type selects the internal-user or external-contact namespace. |

Source locations include `htdocs/install/mysql/tables/llx_element_contact.sql`, `htdocs/install/mysql/tables/llx_element_contact.key.sql`, `htdocs/contact/class/contact.class.php:1275`.

<a id="record-element_element"></a>

## Typed document relationship

Associates source and target records using both their type and internal identifier. It supports tracing conversions between documents that have independent lifecycles.

**Storage** `element_element`.
The primary key is `rowid`.
An additional unique key comprises `fk_source`, `sourcetype`, `fk_target`, `targettype`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_source` | integer | No | — | Source identity interpreted with sourcetype. |
| `sourcetype` | varchar(64) | No | — | Object kind for the corresponding endpoint of the relationship. |
| `fk_target` | integer | No | — | Target identity interpreted with targettype. |
| `targettype` | varchar(64) | No | — | Object kind for the corresponding endpoint of the relationship. |
| `relationtype` | varchar(64) | Yes | `NULL` | Kind of relationship between the two linked objects. |

Source locations include `htdocs/install/mysql/tables/llx_element_element.sql`, `htdocs/install/mysql/tables/llx_element_element.key.sql`, `htdocs/core/class/discount.class.php:605`.

<a id="record-element_resources"></a>

## Resource association

Associates a resource and its type with a business record and its type. Duration, mandatory participation and occupancy are properties of this association.

**Storage** `element_resources`.
The primary key is `rowid`.
An additional unique key comprises `resource_id`, `resource_type`, `element_id`, `element_type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `element_id` | integer | Yes | — | Target record identity. Where an object type accompanies it, both values identify the target. |
| `element_type` | varchar(64) | Yes | — | Type discriminator identifying the class of associated object. |
| `resource_id` | integer | Yes | — | Identity of the assigned resource or user, interpreted with its type. |
| `resource_type` | varchar(64) | Yes | — | Selects the namespace of the resource ID. |
| `busy` | integer | Yes | — | Occupancy indicator for the resource assignment. |
| `mandatory` | integer | Yes | — | Whether participation or association is required. |
| `duree` | real | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `fk_user_create` | integer | Yes | — | Account recorded as creator or author. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

Source locations include `htdocs/install/mysql/tables/llx_element_resources.sql`, `htdocs/install/mysql/tables/llx_element_resources.key.sql`, `htdocs/core/class/commonobject.class.php:6079`.
