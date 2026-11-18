# Employees, membership and field services

An employee request, membership term, service line and intervention report each have their own effective dates. Follow the record that holds the entitlement, approved amount or service state when reconstructing a balance or obligation.

**Example.** A paid membership term of one year and a payment received six days after its start have different dates. Use the subscription period to answer whether the member is covered on a given day, and the payment date to answer when cash arrived.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Association member](#record-adherent) | `adherent` |
| [Membership class](#record-adherent_type) | `adherent_type` |
| [Translated membership class](#record-adherent_type_lang) | `adherent_type_lang` |
| [Membership subscription](#record-subscription) | `subscription` |
| [Donation pledge](#record-don) | `don` |
| [Donation payment](#record-payment_donation) | `payment_donation` |
| [Salary obligation](#record-salary) | `salary` |
| [Salary payment](#record-payment_salary) | `payment_salary` |
| [Leave request](#record-holiday) | `holiday` |
| [Leave configuration](#record-holiday_config) | `holiday_config` |
| [Leave balance change](#record-holiday_logs) | `holiday_logs` |
| [Employee leave entitlement](#record-holiday_users) | `holiday_users` |
| [Expense claim](#record-expensereport) | `expensereport` |
| [Expense claim line](#record-expensereport_det) | `expensereport_det` |
| [Mileage scale band](#record-expensereport_ik) | `expensereport_ik` |
| [Expense restriction](#record-expensereport_rules) | `expensereport_rules` |
| [Expense reimbursement](#record-payment_expensereport) | `payment_expensereport` |
| [Job profile](#record-hrm_job) | `hrm_job` |
| [Job assignment](#record-hrm_job_user) | `hrm_job_user` |
| [Skill](#record-hrm_skill) | `hrm_skill` |
| [Skill level descriptor](#record-hrm_skilldet) | `hrm_skilldet` |
| [Skill ranking](#record-hrm_skillrank) | `hrm_skillrank` |
| [Employee evaluation](#record-hrm_evaluation) | `hrm_evaluation` |
| [Assessed competency](#record-hrm_evaluationdet) | `hrm_evaluationdet` |
| [Vacancy](#record-recruitment_recruitmentjobposition) | `recruitment_recruitmentjobposition` |
| [Application](#record-recruitment_recruitmentcandidature) | `recruitment_recruitmentcandidature` |
| [Service contract](#record-contrat) | `contrat` |
| [Contract service line](#record-contratdet) | `contratdet` |
| [Intervention report](#record-fichinter) | `fichinter` |
| [Intervention activity](#record-fichinterdet) | `fichinterdet` |
| [Recurring intervention template](#record-fichinter_rec) | `fichinter_rec` |
| [Recurring intervention activity](#record-fichinterdet_rec) | `fichinterdet_rec` |
| [Support ticket](#record-ticket) | `ticket` |
| [Knowledge article](#record-knowledgemanagement_knowledgerecord) | `knowledgemanagement_knowledgerecord` |

<a id="record-adherent"></a>

## Association member

Identifies the member, membership class, external-party link, approval state and most recent coverage end date.

**Storage** `adherent`.
The primary key is `rowid`.
Additional unique keys comprise `login`, `entity` / `ref`, `entity` / `fk_soc`.

**Referenced by** [categorie_member](categories.md#record-categorie_member) (fk_member).

The record class defines `-1` draft, `1` validated, `0` resiliated, `-2` excluded. See `htdocs/adherents/class/adherent.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(128) | Yes | — | Identifier supplied by an external application or interface. |
| `gender` | varchar(10) | Yes | — | Gender value entered for a person. |
| `civility` | varchar(6) | Yes | — | Person's form of address. |
| `lastname` | varchar(50) | Yes | — | Person's family name. |
| `firstname` | varchar(50) | Yes | — | Person's given name. |
| `login` | varchar(50) | Yes | — | Login name of the account. |
| `pass` | varchar(50) | Yes | — | Credential field in the account layout. Handle through the owning account service. |
| `pass_crypted` | varchar(128) | Yes | — | Stored encoded credential. |
| `fk_adherent_type` | integer | No | — | Membership category governing the account. References [adherent_type](people.md#record-adherent_type) (rowid). |
| `morphy` | varchar(3) | No | — | Membership/person classification for a natural person or organisation. |
| `societe` | varchar(128) | Yes | — | Organisation name captured with the person or transaction. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `address` | text | Yes | — | Postal or street address. |
| `zip` | varchar(30) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `state_id` | integer | Yes | — | Administrative subdivision identity in an address. |
| `country` | integer | Yes | — | Country value; some structures keep a code or text snapshot alongside a country ID. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `socialnetworks` | text | Yes | `NULL` | Social contact handles associated with the party or person. |
| `phone` | varchar(30) | Yes | — | Telephone number. |
| `phone_perso` | varchar(30) | Yes | — | Personal telephone number. |
| `phone_mobile` | varchar(30) | Yes | — | Mobile telephone number. |
| `birth` | date | Yes | — | Birth date. |
| `birth_place` | varchar(64) | Yes | — | Place of birth. |
| `photo` | varchar(255) | Yes | — | Reference to an image attached to this person or object. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `public` | smallint | No | `0` | Publication or visibility selection for the record. |
| `datefin` | datetime | Yes | — | End date. |
| `default_lang` | varchar(6) | Yes | `NULL` | Default language selected for communication or display. |
| `note_private` | text | Yes | `NULL` | Internal note for users handling the record. |
| `note_public` | text | Yes | `NULL` | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `datevalid` | datetime | Yes | — | When validation was recorded. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_mod` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `canvas` | varchar(32) | Yes | — | Alternate form or presentation model selected for the object. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_adherent.sql`, `htdocs/install/mysql/tables/llx_adherent.key.sql`, `htdocs/adherents/class/adherent.class.php:60`.

<a id="record-adherent_type"></a>

## Membership class

Defines which eligibility and subscription arrangements apply to a class of members.

**Storage** `adherent_type`.
The primary key is `rowid`.
An additional unique key comprises `libelle`, `entity`.

**Referenced by** [adherent](people.md#record-adherent) (fk_adherent_type).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `libelle` | varchar(50) | No | — | Display label for the record. |
| `morphy` | varchar(3) | No | — | Membership/person classification for a natural person or organisation. |
| `duration` | varchar(6) | Yes | `NULL` | Duration of the activity or period in the unit used by the owning feature. |
| `subscription` | varchar(3) | No | `'1'` | Contribution. |
| `amount` | double(24,8) | Yes | `NULL` | Monetary amount. Its operational meaning follows the record purpose. |
| `caneditamount` | integer | Yes | `0` | Can edit amount. |
| `minimumamount` | double(24,8) | Yes | `NULL` | Minimum contribution specified for this membership type. |
| `amountformuladescription` | text | Yes | — | Information on the membership price. |
| `vote` | varchar(3) | No | `'1'` | Vote. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `mail_valid` | text | Yes | — | Mail Validation. |

Source locations include `htdocs/install/mysql/tables/llx_adherent_type.sql`, `htdocs/install/mysql/tables/llx_adherent_type.key.sql`, `htdocs/adherents/class/adherent_type.class.php:42`.

<a id="record-adherent_type_lang"></a>

## Translated membership class

Supplies the label, description and email content for a membership class in one language.

**Storage** `adherent_type_lang`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_type` | integer | No | `0` | Named type selected from the relevant dictionary. |
| `lang` | varchar(5) | No | `0` | Language code under which this text or presentation is stored. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `email` | text | Yes | — | Email address associated with this record. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_adherent_type_lang.sql`, `htdocs/adherents/class/adherent_type.class.php:281`.

<a id="record-subscription"></a>

## Membership subscription

Records a membership period and fee. Several periods can belong to the same member, and payment evidence can be linked separately.

**Storage** `subscription`.
The primary key is `rowid`.
An additional unique key comprises `fk_adherent`, `dateadh`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_adherent` | integer | Yes | — | Association member identity. |
| `fk_type` | integer | Yes | — | Named type selected from the relevant dictionary. |
| `dateadh` | datetime | Yes | — | Date of membership. |
| `datef` | datetime | Yes | — | Invoice date in billing records. |
| `subscription` | double(24,8) | Yes | — | Amount. |
| `fk_bank` | integer | Yes | `NULL` | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_valid` | integer | Yes | `NULL` | Account that validated the record. |
| `ref_ext` | varchar(128) | Yes | — | Identifier supplied by an external application or interface. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_subscription.sql`, `htdocs/install/mysql/tables/llx_subscription.key.sql`, `htdocs/adherents/class/subscription.class.php:45`.

<a id="record-don"></a>

## Donation pledge

Describes a donation, its donor, value, dates and processing state. One or more payments can settle the pledge.

**Storage** `don`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

The record class defines `0` draft, `1` validated, `2` paid, `-1` canceled. See `htdocs/don/class/don.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | `NULL` | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `datedon` | datetime | Yes | — | Business date of the donation or pledge. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_payment` | integer | Yes | — | Settlement record associated with the owning business object. |
| `paid` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `firstname` | varchar(50) | Yes | — | Person's given name. |
| `lastname` | varchar(50) | Yes | — | Person's family name. |
| `societe` | varchar(50) | Yes | — | Organisation name captured with the person or transaction. |
| `address` | text | Yes | — | Postal or street address. |
| `zip` | varchar(30) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `country` | varchar(50) | Yes | — | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `fk_country` | integer | No | — | Country associated with the record. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `phone` | varchar(24) | Yes | — | Telephone number. |
| `phone_mobile` | varchar(24) | Yes | — | Mobile telephone number. |
| `public` | smallint | No | `1` | Publication or visibility selection for the record. |
| `fk_projet` | integer | Yes | — | Associated project identity. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

Source locations include `htdocs/install/mysql/tables/llx_don-don.sql`, `htdocs/install/mysql/tables/llx_don-don.key.sql`, `htdocs/don/class/don.class.php:52`.

<a id="record-payment_donation"></a>

## Donation payment

Records actual money received against a donation, together with the instrument and optional bank or provider reference.

**Storage** `payment_donation`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_donation` | integer | Yes | — | Donation against which the payment is recorded. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `ext_payment_id` | varchar(255) | Yes | — | Provider's identifier for a transaction. |
| `ext_payment_site` | varchar(128) | Yes | — | External payment service or provider identifier. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_payment_donation.sql`, `htdocs/don/class/don.class.php:1187`.

<a id="record-salary"></a>

## Salary obligation

Identifies an employee-related salary amount and period. The obligation and the cash payment have separate records.

**Storage** `salary`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user` | integer | No | — | User account associated with this record. |
| `datep` | date | Yes | — | Payment or posting date for this financial record. |
| `datev` | date | Yes | — | Value/effective date in financial records. |
| `salary` | double(24,8) | Yes | — | Salary value retained on the employee or employment record. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `datesp` | date | Yes | — | Start date. |
| `dateep` | date | Yes | — | End date. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | `NULL` | Selected document output model. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `paye` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_salary.sql`, `htdocs/install/mysql/tables/llx_salary.key.sql`, `htdocs/salaries/class/salary.class.php:51`.

<a id="record-payment_salary"></a>

## Salary payment

Records a salary settlement and its actual payment account movement.

**Storage** `payment_salary`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_user` | integer | Yes | `NULL` | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `datev` | date | Yes | — | Value/effective date in financial records. |
| `salary` | double(24,8) | Yes | — | Salary value retained on the employee or employment record. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `datesp` | date | Yes | — | Start date. |
| `dateep` | date | Yes | — | End date. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_salary` | integer | Yes | — | Salary obligation identity. |

Source locations include `htdocs/install/mysql/tables/llx_payment_salary.sql`, `htdocs/install/mysql/tables/llx_payment_salary.key.sql`, `htdocs/salaries/class/salary.class.php:741`.

<a id="record-holiday"></a>

## Leave request

Records one employee's absence interval, leave type, half-day selection, validation and approval information.

**Storage** `holiday`.
The primary key is `rowid`.

The record class defines `1` draft, `2` validated, `3` approved, `4` canceled, `5` refused. See `htdocs/holiday/class/holiday.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | — | Employee taking the leave. |
| `fk_user_create` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_type` | integer | No | — | Named type selected from the relevant dictionary. |
| `date_create` | datetime | No | — | When the row was created. |
| `description` | varchar( 255 ) | No | — | Descriptive text associated with this entry. |
| `date_debut` | date | No | — | Beginning of the interval. |
| `date_fin` | date | No | — | End of the applicable period. |
| `halfday` | integer | Yes | `0` | Encoding of a partial-day absence at the start or end of a request. |
| `nb_open_day` | double(24,8) | Yes | `NULL` | Cached working days in the leave interval. Dates, half-days and the employee's calendar determine the calculated duration. |
| `statut` | integer | No | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_validator` | integer | No | — | User designated to decide the leave request. |
| `date_valid` | datetime | Yes | `NULL` | When validation was recorded. |
| `fk_user_valid` | integer | Yes | `NULL` | Account that validated the record. |
| `date_approval` | datetime | Yes | `NULL` | Date of the leave approval. |
| `fk_user_approve` | integer | Yes | `NULL` | Account that recorded approval. |
| `date_refuse` | datetime | Yes | `NULL` | When refusal or cancellation was recorded. |
| `fk_user_refuse` | integer | Yes | `NULL` | Actor recorded for refusal or cancellation respectively. |
| `date_cancel` | datetime | Yes | `NULL` | When refusal or cancellation was recorded. |
| `fk_user_cancel` | integer | Yes | `NULL` | Actor recorded for refusal or cancellation respectively. |
| `detail_refuse` | varchar( 250 ) | Yes | `NULL` | Explanation supplied on refusal. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_holiday.sql`, `htdocs/holiday/class/holiday.class.php:52`.

<a id="record-holiday_config"></a>

## Leave configuration

Stores leave-specific named settings used by the leave workflow.

**Storage** `holiday_config`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `name`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `name` | varchar(128) | No | — | Name under which this record is presented or identified. |
| `value` | text | Yes | — | Stored value of this leave-management setting. |

Source locations include `htdocs/install/mysql/tables/llx_holiday_config.sql`, `htdocs/install/mysql/tables/llx_holiday_config.key.sql`, `htdocs/holiday/class/holiday.class.php:1653`.

<a id="record-holiday_logs"></a>

## Leave balance change

Retains the employee, leave type, change source and before/after balance information for a counter change.

**Storage** `holiday_logs`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `date_action` | datetime | No | — | Time of the leave-related change. |
| `fk_user_action` | integer | No | — | Account responsible for the recorded action. |
| `fk_user_update` | integer | No | — | User whose leave balance was affected. |
| `fk_type` | integer | No | — | Named type selected from the relevant dictionary. |
| `type_action` | varchar( 255 ) | No | — | Kind of change registered in the leave history. |
| `prev_solde` | varchar( 255 ) | No | — | Entitlement balance before the recorded change. |
| `new_solde` | varchar( 255 ) | No | — | Entitlement balance after the recorded change. |

Source locations include `htdocs/install/mysql/tables/llx_holiday_logs.sql`, `htdocs/holiday/class/holiday.class.php:2304`.

<a id="record-holiday_users"></a>

## Employee leave entitlement

Stores the current balance for an employee and leave type.

**Storage** `holiday_users`.
The installation definitions declare no primary key for this record.
An additional unique key comprises `fk_user`, `fk_type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_user` | integer | No | — | User account associated with this record. |
| `fk_type` | integer | No | — | Named type selected from the relevant dictionary. |
| `nb_holiday` | real | No | `0` | Recorded number of leave days for this employee and type. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_holiday_users.sql`, `htdocs/install/mysql/tables/llx_holiday_users.key.sql`, `htdocs/holiday/class/holiday.class.php:1871`.

<a id="record-expensereport"></a>

## Expense claim

Groups an employee's expense lines over a date interval with approval, totals and reimbursement information.

**Storage** `expensereport`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

The record class defines `0` draft, `2` validated, `4` canceled, `5` approved, `6` closed, `99` refused. See `htdocs/expensereport/class/expensereport.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(50) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_number_int` | integer | Yes | `NULL` | Ref number int. |
| `ref_ext` | integer | Yes | — | Identifier supplied by an external application or interface. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `date_debut` | date | No | — | Beginning of the interval. |
| `date_fin` | date | No | — | End of the applicable period. |
| `date_create` | datetime | No | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `date_approve` | datetime | Yes | — | When approval was recorded. |
| `date_refuse` | datetime | Yes | — | When refusal or cancellation was recorded. |
| `date_cancel` | datetime | Yes | — | When refusal or cancellation was recorded. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_author` | integer | No | — | Employee whose expenses are claimed. The creator can be another authorised user. |
| `fk_user_creat` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | `NULL` | Account that validated the record. |
| `fk_user_validator` | integer | Yes | `NULL` | User who validates the expense report. |
| `fk_user_approve` | integer | Yes | `NULL` | Account that recorded approval. |
| `fk_user_refuse` | integer | Yes | `NULL` | Actor recorded for refusal or cancellation respectively. |
| `fk_user_cancel` | integer | Yes | `NULL` | Actor recorded for refusal or cancellation respectively. |
| `fk_statut` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_c_paiement` | integer | Yes | `NULL` | Payment instrument selected for the expense claim. |
| `paid` | smallint | No | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `detail_refuse` | varchar(255) | Yes | `NULL` | Explanation supplied on refusal. |
| `detail_cancel` | varchar(255) | Yes | `NULL` | Detail cancel. |
| `integration_compta` | integer | Yes | `NULL` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `fk_bank_account` | integer | Yes | `NULL` | Bank or cash account. Actual movements have their own identities. |
| `model_pdf` | varchar(255) | Yes | `NULL` | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_expensereport.sql`, `htdocs/install/mysql/tables/llx_expensereport.key.sql`, `htdocs/expensereport/class/expensereport.class.php:50`.

<a id="record-expensereport_det"></a>

## Expense claim line

Specifies the incurred expense, date, charge category, amount and possible project or evidence file.

**Storage** `expensereport_det`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_expensereport` | integer | No | — | Employee expense claim identity. |
| `docnumber` | varchar(128) | Yes | — | Accounting document reference for the expense line. |
| `fk_c_type_fees` | integer | No | — | Expense type attached to the claim line. |
| `fk_c_exp_tax_cat` | integer | Yes | — | Expense or mileage category used to select reimbursement settings. |
| `fk_projet` | integer | Yes | — | Associated project identity. |
| `comments` | text | No | — | Additional remarks for the expense entry. |
| `product_type` | integer | Yes | `-1` | Product, service or special-line classification used by the owning document. |
| `qty` | real | No | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `subprice` | double(24,8) | No | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `value_unit` | double(24,8) | No | — | Unit amount including tax for the expense. |
| `remise_percent` | real | Yes | — | Percentage discount applied to the pricing base. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `total_ht` | double(24,8) | No | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | No | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | No | `0` | Total including tax in base currency. |
| `date` | date | No | — | Business date of the individual expense. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `fk_facture` | integer | Yes | `0` | Customer invoice identifier. |
| `fk_ecm_files` | integer | Yes | `NULL` | Associated indexed document identifier. |
| `tcheck_file` | integer | Yes | `NULL` | Supporting-document review state. Zero is unreviewed, one is accepted and minus one is rejected. |
| `fk_code_ventilation` | integer | Yes | `0` | Account binding recorded for distribution to the ledger. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `rule_warning_message` | text | Yes | — | Text retained for a rule warning on the expense line. |

Source locations include `htdocs/install/mysql/tables/llx_expensereport_det.sql`, `htdocs/expensereport/class/expensereport.class.php:55`.

<a id="record-expensereport_ik"></a>

## Mileage scale band

Stores a coefficient and offset associated with a vehicle/expense category and distance band.

**Storage** `expensereport_ik`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_c_exp_tax_cat` | integer | No | `0` | Expense or mileage category used to select reimbursement settings. |
| `fk_range` | integer | No | `0` | Tax range id. |
| `coef` | double | No | `0` | Rate multiplier applied by the mileage scale. |
| `ikoffset` | double | No | `0` | Fixed amount added to the distance-based part of the allowance. |
| `active` | integer | Yes | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_expensereport_ik-expensereport.sql`, `htdocs/expensereport/class/expensereport_ik.class.php:42`.

<a id="record-expensereport_rules"></a>

## Expense restriction

Defines a dated amount restriction by expense category and user or group scope.

**Storage** `expensereport_rules`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `dates` | datetime | No | — | Dates. |
| `datee` | datetime | No | — | End date of the interval in which the rule applies. |
| `amount` | double(24,8) | No | — | Monetary amount. Its operational meaning follows the record purpose. |
| `restrictive` | tinyint | No | — | Whether the restriction is enforced by blocking the affected claim operation. |
| `fk_user` | integer | Yes | `NULL` | User account associated with this record. |
| `fk_usergroup` | integer | Yes | `NULL` | Access or personnel group. |
| `fk_c_type_fees` | integer | No | — | Expense type attached to the claim line. |
| `code_expense_rules_type` | varchar(50) | No | — | Expense rule code. |
| `is_for_all` | tinyint | Yes | `0` | Is For All. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_expensereport_rules-expensereport.sql`, `htdocs/expensereport/class/expensereport_rule.class.php:42`.

<a id="record-payment_expensereport"></a>

## Expense reimbursement

Records an employee expense payment with its amount, instrument and bank movement.

**Storage** `payment_expensereport`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_expensereport` | integer | Yes | — | Employee expense claim identity. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_payment_expensereport.sql`, `htdocs/expensereport/class/expensereport.class.php:1232`.

<a id="record-hrm_job"></a>

## Job profile

Defines an organisational job, its label and related attributes used to describe a position.

**Storage** `hrm_job`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `deplacement` | varchar(255) | Yes | — | Business travels. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_job-hrm.sql`, `htdocs/hrm/class/job.class.php:52`.

<a id="record-hrm_job_user"></a>

## Job assignment

Associates a user with a job over the assignment information retained on the row.

**Storage** `hrm_job_user`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_contrat` | integer | Yes | — | Service contract. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_job` | integer | No | — | Job profile identity. |
| `date_start` | datetime | Yes | — | Beginning of the applicable period. |
| `date_end` | datetime | Yes | — | End of the applicable period. |
| `abort_comment` | varchar(255) | Yes | — | Abandonment comment. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_job_user-hrm.sql`, `htdocs/hrm/class/position.class.php:51`.

<a id="record-hrm_skill"></a>

## Skill

Identifies a competency used to describe a role or assess an employee.

**Storage** `hrm_skill`.
The primary key is `rowid`.

**Referenced by** [hrm_skilldet](people.md#record-hrm_skilldet) (fk_skill), [hrm_skillrank](people.md#record-hrm_skillrank) (fk_skill).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `required_level` | integer | No | — | required Level. |
| `date_validite` | integer | No | — | date_validite. |
| `temps_theorique` | double(24,8) | No | — | temps_theorique. |
| `skill_type` | integer | No | — | Skill type. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_skill-hrm.sql`, `htdocs/install/mysql/tables/llx_hrm_skill-hrm.key.sql`, `htdocs/hrm/class/skill.class.php:51`.

<a id="record-hrm_skilldet"></a>

## Skill level descriptor

Associates an ordered proficiency level and its description with a skill.

**Storage** `hrm_skilldet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_skill` | integer | No | — | Competency identity. References [hrm_skill](people.md#record-hrm_skill) (rowid). |
| `rankorder` | integer | No | `'1'` | Ordering value used within the relevant list, hierarchy or document. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_skilldet-hrm.sql`, `htdocs/install/mysql/tables/llx_hrm_skilldet-hrm.key.sql`, `htdocs/hrm/class/skilldet.class.php:51`.

<a id="record-hrm_skillrank"></a>

## Skill ranking

Records a competency rank against the skill and related object named on the row.

**Storage** `hrm_skillrank`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_skill` | integer | No | — | Competency identity. References [hrm_skill](people.md#record-hrm_skill) (rowid). |
| `rankorder` | integer | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `fk_object` | integer | No | — | Identity of the subject whose competency rank is recorded. Interpret together with objecttype. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `objecttype` | varchar(128) | No | — | Object type used with a separate record identifier. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_skillrank-hrm.sql`, `htdocs/install/mysql/tables/llx_hrm_skillrank-hrm.key.sql`, `htdocs/hrm/class/job.class.php:1043`.

<a id="record-hrm_evaluation"></a>

## Employee evaluation

Records an employee assessment, its author or evaluator, period and state.

**Storage** `hrm_evaluation`.
The primary key is `rowid`.

**Referenced by** [hrm_evaluationdet](people.md#record-hrm_evaluationdet) (fk_evaluation).

The record class defines `0` draft, `1` validated, `9` canceled, `6` closed. See `htdocs/hrm/class/evaluation.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `date_eval` | date | Yes | — | Competency assessment date. |
| `fk_user` | integer | No | — | User account associated with this record. |
| `fk_job` | integer | No | — | Job profile identity. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_evaluation-hrm.sql`, `htdocs/install/mysql/tables/llx_hrm_evaluation-hrm.key.sql`, `htdocs/hrm/class/evaluation.class.php:53`.

<a id="record-hrm_evaluationdet"></a>

## Assessed competency

Attaches a skill to an evaluation and records the required and observed rank with comments.

**Storage** `hrm_evaluationdet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_skill` | integer | No | — | Competency identity. |
| `fk_evaluation` | integer | No | — | References [hrm_evaluation](people.md#record-hrm_evaluation) (rowid). |
| `rankorder` | integer | No | — | Ordering value used within the relevant list, hierarchy or document. |
| `required_rank` | integer | No | — | required Rank. |
| `comment` | text | Yes | — | Free-text annotation retained with the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_hrm_evaluationdet-hrm.sql`, `htdocs/install/mysql/tables/llx_hrm_evaluationdet-hrm.key.sql`, `htdocs/hrm/class/evaluation.class.php:167`.

<a id="record-recruitment_recruitmentjobposition"></a>

## Vacancy

Defines a position offered for recruitment and its publication and lifecycle information.

**Storage** `recruitment_recruitmentjobposition`.
The primary key is `rowid`.

The record class defines `0` draft, `1` validated, `3` recruited, `9` canceled. See `htdocs/recruitment/class/recruitmentjobposition.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `qty` | integer | No | `1` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_project` | integer | Yes | — | Associated project identity. |
| `fk_user_recruiter` | integer | Yes | — | References [user](foundation.md#record-user) (rowid). |
| `email_recruiter` | varchar(255) | Yes | — | Email recruiter. |
| `fk_user_supervisor` | integer | Yes | — | References [user](foundation.md#record-user) (rowid). |
| `fk_establishment` | integer | Yes | — | Operating establishment concerned. References [establishment](foundation.md#record-establishment) (rowid). |
| `date_planned` | date | Yes | — | Expected date. |
| `remuneration_suggested` | varchar(255) | Yes | — | Salary. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_recruitment_recruitmentjobposition-recruitment.sql`, `htdocs/install/mysql/tables/llx_recruitment_recruitmentjobposition-recruitment.key.sql`, `htdocs/recruitment/class/recruitmentjobposition.class.php:50`.

<a id="record-recruitment_recruitmentcandidature"></a>

## Application

Stores an applicant and the position applied for, with dates and processing state.

**Storage** `recruitment_recruitmentcandidature`.
The primary key is `rowid`.
An additional unique key comprises `email_msgid`.

The record class defines `0` draft, `1` validated, `3` contract proposed, `5` contract signed, `6` contract refused, `8` refused, `9` canceled. See `htdocs/recruitment/class/recruitmentcandidature.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `fk_recruitmentjobposition` | integer | Yes | — | Job. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `firstname` | varchar(128) | Yes | — | Person's given name. |
| `lastname` | varchar(128) | Yes | — | Person's family name. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `phone` | varchar(64) | Yes | — | Telephone number. |
| `date_birth` | date | Yes | — | Date of birth. |
| `remuneration_requested` | integer | Yes | — | Requested salary. |
| `remuneration_proposed` | integer | Yes | — | Proposed salary. |
| `email_msgid` | varchar(175) | Yes | — | Mail message identifier supplied in the message headers. |
| `email_date` | datetime | Yes | — | Date associated with the stored email. |
| `fk_recruitment_origin` | integer | Yes | — | Stored application origin. The release's origin field is gated in the application form declaration. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

Source locations include `htdocs/install/mysql/tables/llx_recruitment_recruitmentcandidature-recruitment.sql`, `htdocs/install/mysql/tables/llx_recruitment_recruitmentcandidature-recruitment.key.sql`, `htdocs/recruitment/class/recruitmentcandidature.class.php:50`.

<a id="record-contrat"></a>

## Service contract

Groups service lines for a customer and records the agreement reference, dates and validation state.

**Storage** `contrat`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [contratdet](people.md#record-contratdet) (fk_contrat).

The record class defines `0` draft, `1` validated, `2` closed. See `htdocs/contrat/class/contrat.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(255) | Yes | — | Business reference used to identify the document or master record. |
| `ref_customer` | varchar(255) | Yes | — | Reference provided by the customer. |
| `ref_supplier` | varchar(255) | Yes | — | Reference assigned or communicated by the supplier. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `date_contrat` | datetime | Yes | — | Date contrat. |
| `statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fin_validite` | datetime | Yes | — | End of the validity interval. |
| `date_cloture` | datetime | Yes | — | When the record was closed. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | — | Associated project identity. |
| `fk_commercial_signature` | integer | Yes | — | Sale Representative Signature. |
| `fk_commercial_suivi` | integer | Yes | — | Sale Representative follower. |
| `fk_user_author` | integer | No | `0` | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_cloture` | integer | Yes | — | Account that recorded closure. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `revenuestamp` | double(24,8) | Yes | `0` | Fixed revenue-stamp component recorded on the document. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `denormalized_lower_planned_end_date` | datetime | Yes | — | Cached planned end date from the contract's subscriptions. |
| `signed_status` | smallint | Yes | `NULL` | Recorded electronic-signature state. |
| `online_sign_ip` | varchar(48) | Yes | — | Network address retained when the remote signature was submitted. |
| `online_sign_name` | varchar(64) | Yes | — | Name supplied during online signature. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_contrat.sql`, `htdocs/install/mysql/tables/llx_contrat.key.sql`, `htdocs/contrat/class/contrat.class.php:62`.

<a id="record-contratdet"></a>

## Contract service line

Specifies a product or service, price and planned or actual start and end of the service. Each line can open or close separately.

**Storage** `contratdet`.
The primary key is `rowid`.

The record class defines `0` initial, `4` open, `5` closed. See `htdocs/contrat/class/contratligne.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_contrat` | integer | No | — | Service contract. References [contrat](people.md#record-contrat) (rowid). |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `statut` | smallint | Yes | `0` | Lifecycle of this service line, independently of the header. Opening and closing dates identify the actual service interval. |
| `label` | text | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `date_commande` | datetime | Yes | — | Order date. |
| `date_ouverture_prevue` | datetime | Yes | — | Scheduled service activation date. |
| `date_ouverture` | datetime | Yes | — | Actual service activation date. |
| `date_fin_validite` | datetime | Yes | — | Planned end of service coverage. |
| `date_cloture` | datetime | Yes | — | When the record was closed. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | `0` | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `qty` | real | No | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `product_type` | integer | Yes | `1` | Product, service or special-line classification used by the owning document. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `buy_price_ht` | double(24,8) | Yes | `NULL` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `fk_user_author` | integer | No | `0` | Account recorded as creator or author. |
| `fk_user_ouverture` | integer | Yes | — | Person who activated the service. |
| `fk_user_cloture` | integer | Yes | — | Account that recorded closure. |
| `commentaire` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_contratdet.sql`, `htdocs/install/mysql/tables/llx_contratdet.key.sql`, `htdocs/contrat/class/contrat.class.php:67`.

<a id="record-fichinter"></a>

## Intervention report

Describes work performed for a party with a reference, status and total duration.

**Storage** `fichinter`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_fichinter](categories.md#record-categorie_fichinter) (fk_fichinter), [fichinterdet](people.md#record-fichinterdet) (fk_fichinter).

The record class defines `0` draft, `1` validated, `2` billed, `3` closed. See `htdocs/fichinter/class/fichinter.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `0` | Associated project identity. |
| `fk_contrat` | integer | Yes | `0` | Service contract. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_client` | varchar(255) | Yes | — | Reference supplied by the customer. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `datei` | date | Yes | — | Datei. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `fk_statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `dateo` | date | Yes | — | Operation date for a financial transaction. |
| `datee` | date | Yes | — | End date of the intervention. |
| `datet` | date | Yes | — | Datet. |
| `duree` | real | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `signed_status` | smallint | Yes | `NULL` | Recorded electronic-signature state. |
| `online_sign_ip` | varchar(48) | Yes | — | Network address retained when the remote signature was submitted. |
| `online_sign_name` | varchar(64) | Yes | — | Name supplied during online signature. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_fichinter.sql`, `htdocs/install/mysql/tables/llx_fichinter.key.sql`, `htdocs/fichinter/class/fichinter.class.php:98`.

<a id="record-fichinterdet"></a>

## Intervention activity

Records one dated activity on an intervention and the time spent on it.

**Storage** `fichinterdet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_fichinter` | integer | Yes | — | Intervention report identity. References [fichinter](people.md#record-fichinter) (rowid). |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date` | datetime | Yes | — | Date recorded for this intervention line. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `duree` | integer | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_fichinterdet.sql`, `htdocs/install/mysql/tables/llx_fichinterdet.key.sql`, `htdocs/fichinter/class/fichinter.class.php:103`.

<a id="record-fichinter_rec"></a>

## Recurring intervention template

Stores the party, scheduling parameters and prepared header for repeat field work.

**Storage** `fichinter_rec`.
The primary key is `rowid`.
An additional unique key comprises `title`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `title` | varchar(50) | No | — | Display title. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | Yes | `NULL` | Third party associated with this record. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_contrat` | integer | Yes | `0` | Service contract. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_projet` | integer | Yes | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `duree` | real | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `modelpdf` | varchar(255) | Yes | — | Selected document output model. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `frequency` | integer | Yes | — | Repeat interval in units specified by the associated frequency field. |
| `unit_frequency` | varchar(2) | Yes | `'m'` | Time unit in which a recurring interval is expressed. |
| `date_when` | datetime | Yes | `NULL` | Next scheduled occurrence or generation date. |
| `date_last_gen` | datetime | Yes | `NULL` | Time of the last generated occurrence. |
| `nb_gen_done` | integer | Yes | `NULL` | Number of generated occurrences recorded on the template. |
| `nb_gen_max` | integer | Yes | `NULL` | Occurrence limit stored on the template. |
| `auto_validate` | integer | Yes | `NULL` | Requests automatic validation of generated documents. |
| `status` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_fichinter_rec.sql`, `htdocs/install/mysql/tables/llx_fichinter_rec.key.sql`, `htdocs/fichinter/class/fichinterrec.class.php:45`.

<a id="record-fichinterdet_rec"></a>

## Recurring intervention activity

Describes a template activity copied when an intervention is generated.

**Storage** `fichinterdet_rec`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_fichinter` | integer | No | — | Intervention report identity. |
| `date` | datetime | Yes | — | Date on the recurring intervention line. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `duree` | integer | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `total_ht` | double(24, 8) | Yes | `NULL` | Total before tax in base currency after applicable line adjustments. |
| `subprice` | double(24, 8) | Yes | `NULL` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `fk_parent_line` | integer | Yes | `NULL` | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | `NULL` | Catalogue item associated with this entry. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `tva_tx` | double(6, 3) | Yes | `NULL` | VAT percentage for this price or line. |
| `localtax1_tx` | double(6, 3) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(1) | Yes | `NULL` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(6, 3) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(1) | Yes | `NULL` | Calculation category for the corresponding additional tax component. |
| `qty` | double | Yes | `NULL` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | double | Yes | `0` | Percentage discount applied to the pricing base. |
| `fk_remise_except` | integer | Yes | `NULL` | Fixed credit or discount from which this row originated. |
| `price` | double(24, 8) | Yes | `NULL` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `total_tva` | double(24, 8) | Yes | `NULL` | VAT component of the base-currency total. |
| `total_localtax1` | double(24, 8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24, 8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24, 8) | Yes | `NULL` | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24, 8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `fk_code_ventilation` | integer | No | `0` | Account binding recorded for distribution to the ledger. |
| `special_code` | integer unsigned | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_fichinterdet_rec.sql`, `htdocs/fichinter/class/fichinterrec.class.php:46`.

<a id="record-ticket"></a>

## Support ticket

Tracks a reported issue from intake through assignment, resolution or closure, with links to the reporter and affected customer.

**Storage** `ticket`.
The primary key is `rowid`.
Additional unique keys comprise `track_id` / `ref`, `entity` / `barcode`, `fk_barcode_type`, `entity`.

**Referenced by** [categorie_ticket](categories.md#record-categorie_ticket) (fk_ticket).

The record class defines `0` not read, `1` read, `2` assigned, `3` in progress, `5` need more info, `7` waiting, `8` closed, `9` canceled. See `htdocs/ticket/class/ticket.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `track_id` | varchar(128) | No | — | Tracking ID. |
| `fk_soc` | integer | Yes | `0` | Third party associated with this record. |
| `fk_project` | integer | Yes | `0` | Associated project identity. |
| `fk_contract` | integer | Yes | `0` | Contract. |
| `origin_email` | varchar(128) | Yes | — | Reporter Email. |
| `origin_replyto` | varchar(128) | Yes | — | Reply-To in Email. |
| `origin_references` | text | Yes | — | References in Emails. |
| `fk_user_create` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_assign` | integer | Yes | — | Assigned to. |
| `subject` | varchar(255) | Yes | — | Subject. |
| `message` | mediumtext | Yes | — | Message. |
| `fk_statut` | integer | Yes | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `resolution` | integer | Yes | — | Resolution. |
| `progress` | integer | Yes | `0` | Recorded completion percentage. |
| `timing` | varchar(20) | Yes | — | Text retained by ticket persistence. The record class does not define a business unit or a workflow rule for it. |
| `type_code` | varchar(32) | Yes | — | Ticket type code selected from the support dictionary. |
| `category_code` | varchar(32) | Yes | — | Ticket group. |
| `severity_code` | varchar(32) | Yes | — | Severity. |
| `datec` | datetime | Yes | — | When the row was created. |
| `date_read` | datetime | Yes | — | Reading date. |
| `date_last_msg_sent` | datetime | Yes | — | Ticket Last Message Date. |
| `date_close` | datetime | Yes | — | When the record was closed. |
| `notify_tiers_at_create` | tinyint | Yes | — | Notify Thirdparty. |
| `email_msgid` | varchar(255) | Yes | — | Mail message identifier supplied in the message headers. |
| `email_date` | datetime | Yes | — | Date associated with the stored email. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `barcode` | varchar(255) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `NULL` | Symbology used for the barcode. References [c_barcode_type](dictionaries.md#record-c_barcode_type) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_ticket-ticket.sql`, `htdocs/install/mysql/tables/llx_ticket-ticket.key.sql`, `htdocs/ticket/class/ticket.class.php:56`.

<a id="record-knowledgemanagement_knowledgerecord"></a>

## Knowledge article

Stores a question or subject, its answer or content, publication state and ownership.

**Storage** `knowledgemanagement_knowledgerecord`.
The primary key is `rowid`.

**Referenced by** [categorie_knowledgemanagement](categories.md#record-categorie_knowledgemanagement) (fk_knowledgemanagement).

The record class defines `0` draft, `1` validated, `9` canceled. See `htdocs/knowledgemanagement/class/knowledgerecord.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `lang` | varchar(6) | Yes | — | Language code under which this text or presentation is stored. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `question` | text | No | — | Question. |
| `answer` | longtext | Yes | — | Solution. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `fk_ticket` | integer | Yes | — | Support ticket identity. |
| `fk_c_ticket_category` | integer | Yes | — | Suggested on tickets creation. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_knowledgemanagement_knowledgerecord-knowledgemanagement.sql`, `htdocs/install/mysql/tables/llx_knowledgemanagement_knowledgerecord-knowledgemanagement.key.sql`, `htdocs/knowledgemanagement/class/knowledgerecord.class.php:49`.
