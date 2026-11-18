# Organisation, users and access

Start with the user and current entity when resolving configuration, permissions, preferences or ownership. A permission definition becomes a usable grant through an assignment, and an operation can still impose record-specific access conditions.

**Example.** If a person receives a capability directly and through a group, removing the individual grant leaves the group path. Inspect both assignment records, then apply module enablement and object scope to the specific action.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [User account](#record-user) | `user` |
| [Access group](#record-usergroup) | `usergroup` |
| [Group membership](#record-usergroup_user) | `usergroup_user` |
| [Permission definition](#record-rights_def) | `rights_def` |
| [Individual grant](#record-user_rights) | `user_rights` |
| [Group grant](#record-usergroup_rights) | `usergroup_rights` |
| [User preference](#record-user_param) | `user_param` |
| [Contact alert subscription](#record-user_alert) | `user_alert` |
| [User telephony settings](#record-user_clicktodial) | `user_clicktodial` |
| [Employee bank details](#record-user_rib) | `user_rib` |
| [Configuration setting](#record-const) | `const` |
| [Operating establishment](#record-establishment) | `establishment` |
| [Form default](#record-default_values) | `default_values` |
| [Navigation entry](#record-menu) | `menu` |
| [Dashboard widget definition](#record-boxes_def) | `boxes_def` |
| [Dashboard widget placement](#record-boxes) | `boxes` |
| [Saved link](#record-bookmark) | `bookmark` |
| [System event log](#record-events) | `events` |
| [Protected event ledger](#record-blockedlog) | `blockedlog` |
| [Scheduled operation](#record-cronjob) | `cronjob` |

<a id="record-user"></a>

## User account

Identifies the person who signs in or performs a business action. The account carries its company context, access status and optional link to an external party.

**Storage** `user`.
The primary key is `rowid`.
Additional unique keys comprise `login`, `entity` / `fk_socpeople` / `fk_member` / `api_key`.

**Referenced by** [asset](accounting.md#record-asset) (fk_user_creat), [asset](accounting.md#record-asset) (fk_user_modif), [asset_accountancy_codes_economic](accounting.md#record-asset_accountancy_codes_economic) (fk_user_modif), [asset_accountancy_codes_fiscal](accounting.md#record-asset_accountancy_codes_fiscal) (fk_user_modif), [asset_depreciation](accounting.md#record-asset_depreciation) (fk_user_modif), [asset_depreciation_options_economic](accounting.md#record-asset_depreciation_options_economic) (fk_user_modif), [asset_depreciation_options_fiscal](accounting.md#record-asset_depreciation_options_fiscal) (fk_user_modif), [bom_bom](production.md#record-bom_bom) (fk_user_creat), [categorie_user](categories.md#record-categorie_user) (fk_user), [commande](commercial.md#record-commande) (fk_user_author), [commande](commercial.md#record-commande) (fk_user_valid), [commande](commercial.md#record-commande) (fk_user_cloture), [contrat](people.md#record-contrat) (fk_user_author), [delivery](commercial.md#record-delivery) (fk_user_author), [delivery](commercial.md#record-delivery) (fk_user_valid), [ecm_directories](content.md#record-ecm_directories) (fk_user_c), [ecm_directories](content.md#record-ecm_directories) (fk_user_m), [expedition](commercial.md#record-expedition) (fk_user_author), [expedition](commercial.md#record-expedition) (fk_user_valid), [facture](billing.md#record-facture) (fk_user_author), [facture](billing.md#record-facture) (fk_user_valid), [facture_fourn](billing.md#record-facture_fourn) (fk_user_author), [facture_fourn](billing.md#record-facture_fourn) (fk_user_valid), [facture_fourn_rec](billing.md#record-facture_fourn_rec) (fk_user_author), [facture_rec](billing.md#record-facture_rec) (fk_user_author), [fichinter_rec](people.md#record-fichinter_rec) (fk_user_author), [hrm_evaluation](people.md#record-hrm_evaluation) (fk_user_creat), [hrm_evaluationdet](people.md#record-hrm_evaluationdet) (fk_user_creat), [hrm_skill](people.md#record-hrm_skill) (fk_user_creat), [hrm_skilldet](people.md#record-hrm_skilldet) (fk_user_creat), [hrm_skillrank](people.md#record-hrm_skillrank) (fk_user_creat), [knowledgemanagement_knowledgerecord](people.md#record-knowledgemanagement_knowledgerecord) (fk_user_creat), [mrp_mo](production.md#record-mrp_mo) (fk_user_creat), [payment_salary](people.md#record-payment_salary) (fk_user), [product_customer_price](catalogue.md#record-product_customer_price) (fk_user), [product_fournisseur_price](catalogue.md#record-product_fournisseur_price) (fk_user), [projet_task](production.md#record-projet_task) (fk_user_creat), [projet_task](production.md#record-projet_task) (fk_user_valid), [propal](commercial.md#record-propal) (fk_user_author), [propal](commercial.md#record-propal) (fk_user_valid), [propal](commercial.md#record-propal) (fk_user_signature), [propal](commercial.md#record-propal) (fk_user_cloture), [reception](commercial.md#record-reception) (fk_user_author), [reception](commercial.md#record-reception) (fk_user_valid), [recruitment_recruitmentcandidature](people.md#record-recruitment_recruitmentcandidature) (fk_user_creat), [recruitment_recruitmentjobposition](people.md#record-recruitment_recruitmentjobposition) (fk_user_recruiter), [recruitment_recruitmentjobposition](people.md#record-recruitment_recruitmentjobposition) (fk_user_supervisor), [recruitment_recruitmentjobposition](people.md#record-recruitment_recruitmentjobposition) (fk_user_creat), [societe_commerciaux](parties.md#record-societe_commerciaux) (fk_user), [societe_remise_except](parties.md#record-societe_remise_except) (fk_user), [socpeople](parties.md#record-socpeople) (fk_user_creat), [stocktransfer_stocktransfer](warehouse.md#record-stocktransfer_stocktransfer) (fk_user_creat), [user_rights](foundation.md#record-user_rights) (fk_user), [usergroup_user](foundation.md#record-usergroup_user) (fk_user), [workstation_workstation](production.md#record-workstation_workstation) (fk_user_creat).

The record class defines `0` disabled, `1` enabled. See `htdocs/user/class/user.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_employee` | varchar(50) | Yes | — | Employee reference. |
| `ref_ext` | varchar(50) | Yes | — | Identifier supplied by an external application or interface. |
| `admin` | smallint | Yes | `0` | Indicates whether the account has administrator privileges. |
| `employee` | tinyint | Yes | `1` | Identifies an employee account for staff-related operations. |
| `fk_establishment` | integer | Yes | `0` | Operating establishment concerned. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `login` | varchar(50) | No | — | Login name of the account. |
| `pass_encoding` | varchar(24) | Yes | — | Encoding scheme associated with the stored credential. |
| `pass` | varchar(128) | Yes | — | Credential field in the account layout. Handle through the owning account service. |
| `pass_crypted` | varchar(128) | Yes | — | Stored encoded credential. |
| `pass_temp` | varchar(128) | Yes | — | Temporary credential/reset value recorded by the account mechanism. |
| `force_pass_change` | tinyint | Yes | `0` | Requires a password change when the user next signs in. |
| `api_key` | varchar(128) | Yes | — | Credential associated with the user for API authentication. |
| `gender` | varchar(10) | Yes | — | Gender value entered for a person. |
| `civility` | varchar(6) | Yes | — | Person's form of address. |
| `lastname` | varchar(50) | Yes | — | Person's family name. |
| `firstname` | varchar(50) | Yes | — | Person's given name. |
| `address` | varchar(255) | Yes | — | Postal or street address. |
| `zip` | varchar(25) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `fk_state` | integer | Yes | `0` | Administrative subdivision identity in an address. |
| `fk_country` | integer | Yes | `0` | Country associated with the record. |
| `birth` | date | Yes | — | Birth date. |
| `birth_place` | varchar(64) | Yes | — | Place of birth. |
| `job` | varchar(128) | Yes | — | Job title of the account holder. |
| `office_phone` | varchar(30) | Yes | — | Work telephone number. |
| `office_fax` | varchar(30) | Yes | — | Work fax number. |
| `user_mobile` | varchar(30) | Yes | — | Work mobile telephone number. |
| `personal_mobile` | varchar(30) | Yes | — | Personal mobile telephone number. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `personal_email` | varchar(255) | Yes | — | Private email address for this individual. |
| `email_oauth2` | varchar(255) | Yes | — | Separate address used to match the external sign-in identity when it differs from the user's account email. |
| `signature` | longtext | Yes | `NULL` | Signature text configured for this user. |
| `socialnetworks` | text | Yes | `NULL` | Social contact handles associated with the party or person. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_socpeople` | integer | Yes | — | Contact identity. Some generic role assignments resolve differently for internal and external contacts. |
| `fk_member` | integer | Yes | — | Association member identity. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_user_expense_validator` | integer | Yes | — | User designated to approve this employee's expense reports. |
| `fk_user_holiday_validator` | integer | Yes | — | User designated to approve this employee's leave requests. |
| `national_registration_number` | varchar(50) | Yes | — | National registration number. |
| `idpers1` | varchar(128) | Yes | — | One of the employee identification fields available for the installation. |
| `idpers2` | varchar(128) | Yes | — | One of the employee identification fields available for the installation. |
| `idpers3` | varchar(128) | Yes | — | One of the employee identification fields available for the installation. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | `NULL` | Internal note for users handling the record. |
| `model_pdf` | varchar(255) | Yes | `NULL` | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `datelastlogin` | datetime | Yes | — | Time of the latest recorded sign-in. |
| `datepreviouslogin` | datetime | Yes | — | Time of the sign-in preceding the latest one. |
| `datelastpassvalidation` | datetime | Yes | — | Credential revalidation boundary used when deciding whether older sessions remain valid. |
| `datestartvalidity` | datetime | Yes | — | Beginning of the account's validity period. |
| `dateendvalidity` | datetime | Yes | — | End of the account's validity period. |
| `flagdelsessionsbefore` | datetime | Yes | `NULL` | Cutoff supplied to session invalidation processing for this account. |
| `iplastlogin` | varchar(250) | Yes | — | Network address recorded at the latest sign-in. |
| `ippreviouslogin` | varchar(250) | Yes | — | Network address recorded at the preceding sign-in. |
| `ldap_sid` | varchar(255) | Yes | `NULL` | External directory security identifier for the account. |
| `openid` | varchar(255) | Yes | — | External identity used by an OpenID sign-in. |
| `statut` | tinyint | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `photo` | varchar(255) | Yes | — | Reference to an image attached to this person or object. |
| `lang` | varchar(6) | Yes | — | Language code under which this text or presentation is stored. |
| `color` | varchar(6) | Yes | — | Display colour assigned to this entry. |
| `barcode` | varchar(255) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `0` | Symbology used for the barcode. |
| `accountancy_code_user_general` | varchar(32) | Yes | `NULL` | General-ledger account code associated with the user. |
| `accountancy_code` | varchar(32) | Yes | — | Account code selected for the transaction or classification. |
| `nb_holiday` | integer | Yes | `0` | Recorded number of leave days for this employee and type. |
| `thm` | double(24,8) | Yes | — | Hourly cost rate captured on a time entry. |
| `tjm` | double(24,8) | Yes | — | Employee daily rate. |
| `access_hours` | varchar(128) | Yes | `NULL` | Access schedule associated with the account. |
| `salary` | double(24,8) | Yes | — | Salary value retained on the employee or employment record. |
| `salaryextra` | double(24,8) | Yes | — | Additional compensation recorded on the employee account. |
| `dateemployment` | date | Yes | — | Employment commencement or end date. |
| `dateemploymentend` | date | Yes | — | Employment commencement or end date. |
| `weeklyhours` | double(16,8) | Yes | — | Weekly working hours recorded for the employee. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `default_range` | integer | Yes | — | Default expense mileage range for this user. |
| `default_c_exp_tax_cat` | integer | Yes | — | Default expense-category selection for this user. |
| `fk_warehouse` | integer | Yes | — | Warehouse or stock location. |

Source locations include `htdocs/install/mysql/tables/llx_user.sql`, `htdocs/install/mysql/tables/llx_user.key.sql`, `htdocs/user/class/user.class.php:61`.

<a id="record-usergroup"></a>

## Access group

Groups accounts so one permission assignment can apply to several users. Membership and permission records are separate.

**Storage** `usergroup`.
The primary key is `rowid`.
An additional unique key comprises `nom`, `entity`.

**Referenced by** [usergroup_rights](foundation.md#record-usergroup_rights) (fk_usergroup), [usergroup_user](foundation.md#record-usergroup_user) (fk_usergroup).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `nom` | varchar(180) | No | — | Name under which this record is presented or identified. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_parent` | integer | Yes | `NULL` | Record one level above this one in the owning hierarchy. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `color` | varchar(6) | Yes | — | Display colour assigned to this entry. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `model_pdf` | varchar(255) | Yes | `NULL` | Selected document output model. |

Source locations include `htdocs/install/mysql/tables/llx_usergroup.sql`, `htdocs/install/mysql/tables/llx_usergroup.key.sql`, `htdocs/user/class/usergroup.class.php:52`.

<a id="record-usergroup_user"></a>

## Group membership

Associates an account with an access group for the recorded entity. Removing a direct grant does not remove permissions inherited through another membership.

**Storage** `usergroup_user`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_user`, `fk_usergroup`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `fk_usergroup` | integer | No | — | Access or personnel group. References [usergroup](foundation.md#record-usergroup) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_usergroup_user.sql`, `htdocs/install/mysql/tables/llx_usergroup_user.key.sql`, `htdocs/user/class/user.class.php:1481`.

<a id="record-rights_def"></a>

## Permission definition

Defines a permission slot, its namespace and optional subpermission. A definition describes a capability that can be granted.

**Storage** `rights_def`.
The primary key is `id`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer | No | — | Internal identifier in this table. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `module` | varchar(64) | Yes | — | Feature or extension to which this entry belongs. |
| `module_origin` | varchar(64) | Yes | — | Module that provides this permission when it differs from the module it governs. |
| `module_position` | integer | No | `0` | Display ordering for the module in the permission list. |
| `family` | varchar(64) | Yes | — | Grouping of related permission definitions. |
| `family_position` | integer | No | `0` | Display ordering within the permission families. |
| `perms` | varchar(50) | Yes | — | Main permission selector below the module. |
| `subperms` | varchar(50) | Yes | — | Permission selector within the main right. |
| `type` | varchar(1) | Yes | — | Historical permission type field retained in the declaration. |
| `bydefault` | tinyint | Yes | `0` | Flag for granting the right by default. |
| `enabled` | text | Yes | — | Condition or flag determining whether the entry is available. |

Source locations include `htdocs/install/mysql/tables/llx_rights_def.sql`, `htdocs/install/mysql/tables/llx_rights_def.key.sql`, `htdocs/user/class/user.class.php:1129`.

<a id="record-user_rights"></a>

## Individual grant

Assigns a permission definition to one account in an entity. Resolving access also requires module availability and operation-specific scope.

**Storage** `user_rights`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_user`, `fk_id`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `fk_id` | integer | No | — | Definition of the permission assigned to this principal. |

Source locations include `htdocs/install/mysql/tables/llx_user_rights.sql`, `htdocs/install/mysql/tables/llx_user_rights.key.sql`, `htdocs/user/class/user.class.php:1182`.

<a id="record-usergroup_rights"></a>

## Group grant

Assigns a permission definition to a group. Effective rights are evaluated for each member and context.

**Storage** `usergroup_rights`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_usergroup`, `fk_id`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_usergroup` | integer | No | — | Access or personnel group. References [usergroup](foundation.md#record-usergroup) (rowid). |
| `fk_id` | integer | No | — | Definition of the permission assigned to this principal. |

Source locations include `htdocs/install/mysql/tables/llx_usergroup_rights.sql`, `htdocs/install/mysql/tables/llx_usergroup_rights.key.sql`, `htdocs/user/class/user.class.php:1480`.

<a id="record-user_param"></a>

## User preference

Stores a named value for an individual account. Use the entity and account to resolve the applicable preference.

**Storage** `user_param`.
The installation definitions declare no primary key for this record.
An additional unique key comprises `fk_user`, `param`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_user` | integer | No | — | User account associated with this record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `param` | varchar(180) | No | — | Name of this user preference. |
| `value` | text | No | — | Preference value resolved for this user. |

Source locations include `htdocs/install/mysql/tables/llx_user_param.sql`, `htdocs/install/mysql/tables/llx_user_param.key.sql`, `htdocs/user/class/user.class.php:803`.

<a id="record-user_alert"></a>

## Contact alert subscription

Identifies an alert type, recipient user and contact for whom a notification has been requested.

**Storage** `user_alert`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `type` | integer | Yes | — | Type. |
| `fk_contact` | integer | Yes | — | Contact or address identity. |
| `fk_user` | integer | Yes | — | User account associated with this record. |

Source locations include `htdocs/install/mysql/tables/llx_user_alert.sql`, `htdocs/contact/class/contact.class.php:962`.

<a id="record-user_clicktodial"></a>

## User telephony settings

Holds the user-specific account information used to initiate calls through the configured telephony integration.

**Storage** `user_clicktodial`.
The primary key is `fk_user`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_user` | integer | No | — | User account associated with this record. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `login` | varchar(32) | Yes | — | Login name of the account. |
| `pass` | varchar(64) | Yes | — | Credential field in the account layout. Handle through the owning account service. |
| `poste` | varchar(20) | Yes | — | Telephone extension used for outgoing click-to-dial requests. |

Source locations include `htdocs/install/mysql/tables/llx_user_clicktodial.sql`, `htdocs/user/class/user.class.php:2957`.

<a id="record-user_rib"></a>

## Employee bank details

Identifies the bank coordinates attached to a user for employee-related transfers.

**Storage** `user_rib`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_user` | integer | No | — | User account associated with this record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `label` | varchar(30) | Yes | — | Display label for the record. |
| `bank` | varchar(255) | Yes | — | Name of the financial institution for the account details. |
| `code_banque` | varchar(128) | Yes | — | Domestic bank code. |
| `code_guichet` | varchar(6) | Yes | — | Domestic branch code. |
| `number` | varchar(255) | Yes | — | Account number of the employee bank details. |
| `cle_rib` | varchar(5) | Yes | — | Check digits for the domestic bank account identifier. |
| `bic` | varchar(11) | Yes | — | Bank identifier code for the receiving institution. |
| `bic_intermediate` | varchar(11) | Yes | — | Identifier of the intermediary financial institution. |
| `iban_prefix` | varchar(100) | Yes | — | International bank account number field used with the selected banking details. |
| `domiciliation` | varchar(255) | Yes | — | Bank or branch domiciliation details. |
| `proprio` | varchar(60) | Yes | — | Name of the bank-account holder. |
| `owner_address` | varchar(255) | Yes | — | Address recorded for the bank-account holder. |
| `state_id` | integer | Yes | — | Administrative subdivision identity in an address. |
| `fk_country` | integer | Yes | — | Country associated with the record. |
| `currency_code` | varchar(3) | Yes | — | Currency identifier for this record. |
| `default_rib` | smallint | No | `0` | Selects the default set of bank details. |

Source locations include `htdocs/install/mysql/tables/llx_user_rib.sql`, `htdocs/user/class/userbankaccount.class.php:47`.

<a id="record-const"></a>

## Configuration setting

Stores a named installation or entity setting. Distinct entities can give the same setting different values.

**Storage** `const`.
The primary key is `rowid`.
An additional unique key comprises `name`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `name` | varchar(180) | No | — | Name under which this record is presented or identified. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `value` | text | No | — | Setting value interpreted according to its declared type. |
| `type` | varchar(64) | Yes | `'string'` | Storage representation of the setting, including support for encrypted values. |
| `visible` | tinyint | No | `1` | Whether the configuration setting is visible. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

Source locations include `htdocs/install/mysql/tables/llx_const.sql`, `htdocs/install/mysql/tables/llx_const.key.sql`, `htdocs/core/class/conf.class.php:561`.

<a id="record-establishment"></a>

## Operating establishment

Identifies a physical or organisational establishment with its own location and registration details.

**Storage** `establishment`.
The primary key is `rowid`.

**Referenced by** [recruitment_recruitmentjobposition](people.md#record-recruitment_recruitmentjobposition) (fk_establishment).

The record class defines `1` open, `0` closed. See `htdocs/hrm/class/establishment.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `name` | varchar(128) | Yes | — | Name under which this record is presented or identified. |
| `address` | varchar(255) | Yes | — | Postal or street address. |
| `zip` | varchar(25) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `fk_state` | integer | Yes | `0` | Administrative subdivision identity in an address. |
| `fk_country` | integer | Yes | `0` | Country associated with the record. |
| `profid1` | varchar(20) | Yes | — | Profid1. |
| `profid2` | varchar(20) | Yes | — | Profid2. |
| `profid3` | varchar(20) | Yes | — | Profid3. |
| `phone` | varchar(30) | Yes | — | Telephone number. |
| `fk_user_author` | integer | No | — | Account recorded as creator or author. |
| `fk_user_mod` | integer | Yes | — | Account recorded for the latest modification. |
| `datec` | datetime | No | — | When the row was created. |
| `tms` | timestamp | No | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `status` | tinyint | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_establishment.sql`, `htdocs/user/class/user.class.php:588`.

<a id="record-default_values"></a>

## Form default

Registers a parameter value to preselect for a page, user or entity context. A prefilled field can still be subject to validation at submission.

**Storage** `default_values`.
The primary key is `rowid`.
An additional unique key comprises `type`, `entity`, `user_id`, `page`, `param`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `type` | varchar(10) | Yes | — | Type. |
| `user_id` | integer | No | `0` | User account identity. |
| `page` | varchar(255) | Yes | — | Relative URL. |
| `param` | varchar(255) | Yes | — | Field. |
| `value` | varchar(128) | Yes | — | Value. |

Source locations include `htdocs/install/mysql/tables/llx_default_values.sql`, `htdocs/install/mysql/tables/llx_default_values.key.sql`, `htdocs/core/class/defaultvalues.class.php:44`.

<a id="record-menu"></a>

## Navigation entry

Describes a menu entry, parent placement, access expression and destination in the configured navigation system.

**Storage** `menu`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `menu_handler` | varchar(16) | No | — | Menu implementation to which the entry belongs. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `module` | varchar(255) | Yes | — | Feature or extension to which this entry belongs. |
| `type` | varchar(4) | No | — | Positioned in the top-level or secondary navigation. |
| `mainmenu` | varchar(100) | No | — | Identifier for the top-level navigation group. |
| `leftmenu` | varchar(100) | Yes | — | Identifier for the secondary navigation entry. |
| `fk_menu` | integer | No | — | Associated navigation entry identifier. |
| `fk_mainmenu` | varchar(100) | Yes | — | Parent top-level menu identifier. |
| `fk_leftmenu` | varchar(100) | Yes | — | Parent secondary menu identifier. |
| `position` | integer | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `url` | text | No | — | Web address or navigation target. |
| `showtopmenuinframe` | integer | Yes | `0` | Allows external content to appear in a frame with the main navigation visible. |
| `target` | varchar(100) | Yes | — | Destination window or frame for the navigation link. |
| `titre` | varchar(255) | No | — | Display title. |
| `prefix` | varchar(255) | Yes | — | Pictogram reference used with the menu label. |
| `langs` | varchar(100) | Yes | — | Translation resource used to display the configured labels. |
| `level` | smallint | Yes | — | Depth of the item in its menu hierarchy. |
| `perms` | text | Yes | — | Permission expression that determines availability of the entry. |
| `enabled` | text | Yes | — | Condition or flag determining whether the entry is available. |
| `usertype` | integer | No | `0` | Determines the menu audience. Values 0, 1 and 2 select all, external and internal users respectively. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

Source locations include `htdocs/install/mysql/tables/llx_menu.sql`, `htdocs/core/class/menubase.class.php:222`.

<a id="record-boxes_def"></a>

## Dashboard widget definition

Registers a dashboard component available to place on a workspace.

**Storage** `boxes_def`.
The primary key is `rowid`.
An additional unique key comprises `file`, `entity`, `note`.

**Referenced by** [boxes](foundation.md#record-boxes) (box_id).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `file` | varchar(200) | No | — | File providing the dashboard component. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | `0` | User account associated with this record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `note` | varchar(130) | Yes | — | Free-text annotation retained with the record. |

Source locations include `htdocs/install/mysql/tables/llx_boxes_def.sql`, `htdocs/install/mysql/tables/llx_boxes_def.key.sql`, `htdocs/core/class/infobox.class.php:106`.

<a id="record-boxes"></a>

## Dashboard widget placement

Places an available widget in a dashboard context for a user or entity, with ordering and display settings.

**Storage** `boxes`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `box_id`, `position`, `fk_user`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `box_id` | integer | No | — | References [boxes_def](foundation.md#record-boxes_def) (rowid). |
| `position` | smallint | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `box_order` | varchar(3) | No | — | Position of the dashboard component in the user's arrangement. |
| `fk_user` | integer | No | `0` | User account associated with this record. |
| `maxline` | integer | Yes | — | Limit on the number of rows displayed by the component. |
| `params` | varchar(255) | Yes | — | Additional configuration values for the dashboard component. |

Source locations include `htdocs/install/mysql/tables/llx_boxes.sql`, `htdocs/install/mysql/tables/llx_boxes.key.sql`, `htdocs/core/class/infobox.class.php:106`.

<a id="record-bookmark"></a>

## Saved link

Stores a named destination for later access, with owner, visibility and position where configured.

**Storage** `bookmark`.
The primary key is `rowid`.
An additional unique key comprises `fk_user`, `entity`, `title`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_user` | integer | No | — | User account associated with this record. |
| `dateb` | datetime | Yes | — | Date stored with the bookmark. |
| `url` | text | Yes | — | Web address or navigation target. |
| `target` | varchar(16) | Yes | — | Destination window or frame for the navigation link. |
| `title` | varchar(64) | Yes | — | Display title. |
| `favicon` | varchar(24) | Yes | — | Icon reference for the bookmarked destination. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_bookmark.sql`, `htdocs/install/mysql/tables/llx_bookmark.key.sql`, `htdocs/user/class/user.class.php:1833`.

<a id="record-events"></a>

## System event log

Records a system event and associated actor, time, network context and detail.

**Storage** `events`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `type` | varchar(32) | No | — | Type. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `prefix_session` | varchar(255) | Yes | — | Prefix Session. |
| `dateevent` | datetime | Yes | — | Time at which the tracked event occurred. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `description` | varchar(250) | No | — | Descriptive text associated with this entry. |
| `ip` | varchar(250) | No | — | Network address recorded for the relevant submission or event. |
| `user_agent` | varchar(255) | Yes | — | Client application identification retained with the event. |
| `fk_object` | integer | Yes | — | Identifier of the business record holding these values. |
| `authentication_method` | varchar(64) | Yes | — | Authentication mechanism recorded for a sign-in event. |
| `fk_oauth_token` | integer | Yes | — | Associated delegated authorisation token identifier. |

Source locations include `htdocs/install/mysql/tables/llx_events.sql`, `htdocs/core/class/events.class.php:42`.

<a id="record-blockedlog"></a>

## Protected event ledger

Retains a business event payload and signature chain used to inspect its continuity. Its row identity orders the persisted records.

**Storage** `blockedlog`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `module_source` | varchar(32) | Yes | empty string | Feature that originated this business document. |
| `pos_source` | varchar(32) | Yes | empty string | Checkout terminal or other sales-channel source retained on the document. |
| `action` | varchar(50) | Yes | — | Business event type recorded in the signed entry. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `amounts` | double(24,8) | No | — | Amount data retained as part of the signed event. |
| `amounts_taxexcl` | double(24,8) | Yes | — | Tax-exclusive amount data retained as part of the signed event. |
| `ref_object` | varchar(255) | Yes | — | Business document reference captured when the event was recorded. |
| `date_object` | datetime | Yes | — | Business date of the affected document at the time of the event. |
| `type_code` | varchar(8) | Yes | empty string | Payment-method code preserved with the signed event. |
| `user_fullname` | varchar(255) | Yes | — | Name of the actor preserved in the signed event. |
| `linktoref` | text | Yes | — | Business reference of another record associated with the event. |
| `linktype` | varchar(16) | Yes | — | Kind of relationship to the other reference. |
| `object_data` | mediumtext | Yes | — | Snapshot of the recorded object included in the signed event. |
| `signature` | varchar(100) | No | — | Chained event signature incorporating the preceding signature. |
| `signature_backward` | varchar(100) | Yes | empty string | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `element` | varchar(50) | Yes | — | Family of the object whose event is recorded. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_object` | integer | Yes | — | Identifier of the business record holding these values. |
| `object_version` | varchar(32) | Yes | empty string | Release that originally recorded the event. |
| `object_format` | varchar(16) | Yes | `'V1'` | Representation used to interpret the recorded object snapshot. |
| `certified` | integer | Yes | — | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `actionrefisunique` | varchar(16) | Yes | `NULL` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `debuginfo` | mediumtext | Yes | — | Diagnostic information associated with this audit entry. |
| `note` | varchar(128) | Yes | — | Free-text annotation retained with the record. |

Source locations include `htdocs/install/mysql/tables/llx_blockedlog.sql`, `htdocs/blockedlog/class/blockedlog.class.php:1153`.

<a id="record-cronjob"></a>

## Scheduled operation

Defines a periodic job, its permitted execution window and its most recent run results. Job enablement and completion are different facts.

**Storage** `cronjob`.
The primary key is `rowid`.
An additional unique key comprises `label`, `entity`.

The record class defines `0` disabled, `1` enabled, `2` archived. See `htdocs/cron/class/cronjob.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `jobtype` | varchar(10) | No | — | Type. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `command` | varchar(255) | Yes | — | Executable command registered when the job uses command mode. |
| `classesname` | varchar(255) | Yes | — | Class file that provides the scheduled method. |
| `objectname` | varchar(255) | Yes | — | Object class selected when the schedule invokes a method. |
| `methodename` | varchar(255) | Yes | — | Operation selected for a method-based scheduled job. |
| `params` | text | Yes | — | Parameters supplied when the scheduled job executes. |
| `md5params` | varchar(32) | Yes | — | Md5params. |
| `module_name` | varchar(255) | Yes | — | Module/Application. |
| `priority` | integer | Yes | `0` | Processing or display priority. |
| `datelastrun` | datetime | Yes | — | Datelastrun. |
| `datenextrun` | datetime | Yes | — | Datenextrun. |
| `datestart` | datetime | Yes | — | Beginning of the applicable period. |
| `dateend` | datetime | Yes | — | End of the applicable period. |
| `datelastresult` | datetime | Yes | — | Time associated with the most recent job result. |
| `lastresult` | text | Yes | — | Outcome retained for the most recent execution. |
| `lastoutput` | text | Yes | — | Lastoutput. |
| `unitfrequency` | varchar(255) | No | `'3600'` | Time unit for the job's recurrence interval. |
| `frequency` | integer | No | `0` | Repeat interval in units specified by the associated frequency field. |
| `maxrun` | integer | No | `0` | Maxrun. |
| `nbrun` | integer | Yes | — | Nbrun. |
| `autodelete` | integer | Yes | `0` | Autodelete. |
| `status` | integer | No | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `processing` | integer | No | `0` | Processing. |
| `pid` | integer | Yes | — | Pid. |
| `test` | varchar(255) | Yes | `'1'` | Test. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_mod` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `fk_mailing` | integer | Yes | `NULL` | Bulk mailing campaign identity. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `libname` | varchar(255) | Yes | — | Libname. |
| `email_alert` | varchar(128) | Yes | — | Emailalert. |
| `entity` | integer | Yes | `0` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_cronjob.sql`, `htdocs/install/mysql/tables/llx_cronjob.key.sql`, `htdocs/cron/class/cronjob.class.php:45`.
