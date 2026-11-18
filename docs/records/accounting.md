# Accounting, taxes, fixed assets and borrowing

A document or a bank movement can produce journal legs. Accounts, auxiliary accounts, journals and periods qualify those legs. Assets and loans have their own calculation schedules, associated cash transactions and accounting accounts.

**Example.** For a sale of 100.00 plus 15.00 tax, the customer line can carry a debit of 115.00, with revenue and tax credits of 100.00 and 15.00. Reconstruct the journal movement from its legs. The commercial invoice and any later bank receipt have their own source identities.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Chart model](#record-accounting_system) | `accounting_system` |
| [Ledger account](#record-accounting_account) | `accounting_account` |
| [Report category membership](#record-accounting_category_account) | `accounting_category_account` |
| [Fiscal period](#record-accounting_fiscalyear) | `accounting_fiscalyear` |
| [Journal](#record-accounting_journal) | `accounting_journal` |
| [Ledger posting line](#record-accounting_bookkeeping) | `accounting_bookkeeping` |
| [Staged ledger line](#record-accounting_bookkeeping_tmp) | `accounting_bookkeeping_tmp` |
| [Journal template](#record-accounting_transaction_template) | `accounting_transaction_template` |
| [Journal template line](#record-accounting_transaction_template_det) | `accounting_transaction_template_det` |
| [Statutory charge](#record-chargesociales) | `chargesociales` |
| [Statutory charge payment](#record-paiementcharge) | `paiementcharge` |
| [VAT liability](#record-tva) | `tva` |
| [Local tax liability](#record-localtax) | `localtax` |
| [VAT payment](#record-payment_vat) | `payment_vat` |
| [Fixed asset](#record-asset) | `asset` |
| [Asset model](#record-asset_model) | `asset_model` |
| [Economic depreciation accounts](#record-asset_accountancy_codes_economic) | `asset_accountancy_codes_economic` |
| [Fiscal depreciation accounts](#record-asset_accountancy_codes_fiscal) | `asset_accountancy_codes_fiscal` |
| [Economic depreciation parameters](#record-asset_depreciation_options_economic) | `asset_depreciation_options_economic` |
| [Fiscal depreciation parameters](#record-asset_depreciation_options_fiscal) | `asset_depreciation_options_fiscal` |
| [Depreciation schedule row](#record-asset_depreciation) | `asset_depreciation` |
| [Loan agreement](#record-loan) | `loan` |
| [Loan instalment](#record-loan_schedule) | `loan_schedule` |
| [Loan payment](#record-payment_loan) | `payment_loan` |

<a id="record-accounting_system"></a>

## Chart model

Identifies a chart of accounts and its country or version, from which account mappings can be drawn.

**Storage** `accounting_system`.
The primary key is `rowid`.
An additional unique key comprises `pcg_version`.

**Referenced by** [accounting_account](accounting.md#record-accounting_account) (fk_pcg_version).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_country` | integer | Yes | — | Country associated with the record. |
| `pcg_version` | varchar(32) | No | — | Version of the selected chart of accounts. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `active` | smallint | Yes | `0` | Whether this entry is enabled for selection or use. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_system.sql`, `htdocs/install/mysql/tables/llx_accounting_system.key.sql`, `htdocs/accountancy/class/lettering.class.php:543`.

<a id="record-accounting_account"></a>

## Ledger account

Defines a general account, its chart, label and classification. Its account number and row identity serve different purposes.

**Storage** `accounting_account`.
The primary key is `rowid`.
An additional unique key comprises `account_number`, `entity`, `fk_pcg_version`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | bigint (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_pcg_version` | varchar(32) | No | — | References [accounting_system](accounting.md#record-accounting_system) (pcg_version). |
| `pcg_type` | varchar(60) | No | — | Chart classification used to resolve predefined account groups. |
| `account_number` | varchar(32) | No | — | Account number retained on the record. |
| `account_parent` | integer | Yes | `0` | Parent account in the chart hierarchy. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `labelshort` | varchar(255) | Yes | `NULL` | Abbreviated description of the ledger account. |
| `fk_accounting_category` | integer | Yes | `0` | Financial reporting category identity. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |
| `centralized` | tinyint | No | `0` | Centralisation flag configured for the account. |
| `reconcilable` | tinyint | No | `0` | Indicates that entries on this account may be matched. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_account.sql`, `htdocs/install/mysql/tables/llx_accounting_account.key.sql`, `htdocs/install/mysql/tables/llx_accounting_system.key.sql`, `htdocs/accountancy/class/lettering.class.php:542`.

<a id="record-accounting_category_account"></a>

## Report category membership

Connects a general ledger account with a reporting category.

**Storage** `accounting_category_account`.
The primary key is `rowid`.
An additional unique key comprises `fk_accounting_category`, `fk_accounting_account`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_accounting_category` | integer | Yes | — | Financial reporting category identity. |
| `fk_accounting_account` | bigint | Yes | — | General ledger account identity. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_category_account-accounting.sql`, `htdocs/install/mysql/tables/llx_accounting_category_account-accounting.key.sql`, `htdocs/accountancy/class/accountancycategory.class.php:929`.

<a id="record-accounting_fiscalyear"></a>

## Fiscal period

Records period start and end, entity, and whether operations have closed the period for posting.

**Storage** `accounting_fiscalyear`.
The primary key is `rowid`.

The record class defines `0` open, `1` closed. See `htdocs/core/class/fiscalyear.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `date_start` | date | Yes | — | Beginning of the applicable period. |
| `date_end` | date | Yes | — | End of the applicable period. |
| `statut` | tinyint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_fiscalyear.sql`, `htdocs/accountancy/class/lettering.class.php:570`.

<a id="record-accounting_journal"></a>

## Journal

Defines a journal code, name, nature and operating status within an entity.

**Storage** `accounting_journal`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

**Referenced by** [bank_account](cash.md#record-bank_account) (fk_accountancy_journal).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(32) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `nature` | smallint | No | `1` | Journal family. The declaration distinguishes general, sales, purchases, bank, expense claims and opening entries. |
| `active` | smallint | Yes | `0` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_journal.sql`, `htdocs/install/mysql/tables/llx_accounting_journal.key.sql`, `htdocs/compta/bank/class/account.class.php:1133`.

<a id="record-accounting_bookkeeping"></a>

## Ledger posting line

Stores one debit or credit leg, its account and auxiliary account, date, journal, piece and source. A balanced movement consists of multiple legs.

**Storage** `accounting_bookkeeping`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `piece_num` | integer | No | — | Internal journal movement/piece number grouping related posting legs. |
| `doc_date` | date | No | — | Accounting date of the source document. |
| `doc_type` | varchar(30) | No | — | Type of source document or transaction. |
| `doc_ref` | varchar(300) | No | — | Commercial reference of the posting source. |
| `fk_doc` | integer | No | — | Internal identity of the source document. |
| `fk_docdet` | integer | No | — | Source-document line identity where the posting belongs to one line. |
| `thirdparty_code` | varchar(32) | Yes | — | Auxiliary party identifier used in bookkeeping. |
| `subledger_account` | varchar(32) | Yes | — | Auxiliary account identifier used alongside a general account. |
| `subledger_label` | varchar(255) | Yes | — | Display label for the auxiliary account. |
| `numero_compte` | varchar(32) | No | — | Account number retained on the record. |
| `label_compte` | varchar(255) | No | — | Account description retained on the posting. |
| `label_operation` | varchar(255) | Yes | — | Description of the transaction posted. |
| `debit` | double(24,8) | No | — | Value entered on the debit side of the posting. |
| `credit` | double(24,8) | No | — | Value entered on the credit side of the posting. |
| `montant` | double(24,8) | Yes | — | Monetary value retained on the record. |
| `sens` | varchar(1) | Yes | `NULL` | Direction/sign convention used by the owning reporting or posting operation. |
| `multicurrency_amount` | double(24,8) | Yes | — | Amount allocated or paid in the secondary currency. |
| `multicurrency_code` | varchar(255) | Yes | — | Currency code used for the document-currency values. |
| `matching_general` | tinyint | No | `0` | General-account matching marker used by the bookkeeping process. |
| `lettering_code` | varchar(255) | Yes | — | Matching identifier connecting related open-item postings. |
| `date_lettering` | datetime | Yes | — | Date recorded for open-item matching. |
| `date_lim_reglement` | datetime | Yes | `NULL` | Date by which payment falls due. |
| `fk_user_author` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `code_journal` | varchar(32) | No | — | Journal code retained on the posting. |
| `journal_label` | varchar(255) | Yes | — | Journal description retained on the posting. |
| `date_validated` | datetime | Yes | — | Date on which validation was recorded. |
| `date_export` | datetime | Yes | `NULL` | Date recorded when the value was exported. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_bookkeeping-accounting.sql`, `htdocs/asset/class/asset.class.php:750`.

<a id="record-accounting_bookkeeping_tmp"></a>

## Staged ledger line

Stores a provisional journal line in the temporary posting mode. Transfer and validation determine its subsequent handling.

**Storage** `accounting_bookkeeping_tmp`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `doc_date` | date | No | — | Accounting date of the source document. |
| `doc_type` | varchar(30) | No | — | Type of source document or transaction. |
| `doc_ref` | varchar(300) | No | — | Commercial reference of the posting source. |
| `fk_doc` | integer | No | — | Internal identity of the source document. |
| `fk_docdet` | integer | No | — | Source-document line identity where the posting belongs to one line. |
| `thirdparty_code` | varchar(32) | Yes | — | Auxiliary party identifier used in bookkeeping. |
| `subledger_account` | varchar(32) | Yes | — | Auxiliary account identifier used alongside a general account. |
| `subledger_label` | varchar(255) | Yes | — | Display label for the auxiliary account. |
| `numero_compte` | varchar(32) | Yes | — | Account number retained on the record. |
| `label_compte` | varchar(255) | No | — | Account description retained on the posting. |
| `label_operation` | varchar(255) | Yes | — | Description of the transaction posted. |
| `debit` | double(24,8) | No | — | Value entered on the debit side of the posting. |
| `credit` | double(24,8) | No | — | Value entered on the credit side of the posting. |
| `montant` | double(24,8) | No | — | Monetary value retained on the record. |
| `sens` | varchar(1) | Yes | `NULL` | Direction/sign convention used by the owning reporting or posting operation. |
| `multicurrency_amount` | double(24,8) | Yes | — | Amount allocated or paid in the secondary currency. |
| `multicurrency_code` | varchar(255) | Yes | — | Currency code used for the document-currency values. |
| `matching_general` | tinyint | No | `0` | General-account matching marker used by the bookkeeping process. |
| `lettering_code` | varchar(255) | Yes | — | Matching identifier connecting related open-item postings. |
| `date_lettering` | datetime | Yes | — | Date recorded for open-item matching. |
| `date_lim_reglement` | datetime | Yes | — | Date by which payment falls due. |
| `fk_user_author` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `code_journal` | varchar(32) | No | — | Journal code retained on the posting. |
| `journal_label` | varchar(255) | Yes | — | Journal description retained on the posting. |
| `piece_num` | integer | No | — | Internal journal movement/piece number grouping related posting legs. |
| `date_validated` | datetime | Yes | — | Date on which validation was recorded. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_bookkeeping_tmp-accounting.sql`, `htdocs/accountancy/class/bookkeeping.class.php:759`.

<a id="record-accounting_transaction_template"></a>

## Journal template

Identifies a reusable journal entry pattern.

**Storage** `accounting_transaction_template`.
The primary key is `rowid`.
An additional unique key comprises `code`, `entity`.

**Referenced by** [accounting_transaction_template_det](accounting.md#record-accounting_transaction_template_det) (fk_transaction_template).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `code` | varchar(128) | No | — | Machine-readable code identifying a dictionary entry or feature value. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_transaction_template-accounting.sql`, `htdocs/install/mysql/tables/llx_accounting_transaction_template-accounting.key.sql`, `htdocs/accountancy/class/bookkeepingtemplate.class.php:48`.

<a id="record-accounting_transaction_template_det"></a>

## Journal template line

Defines the posting accounts and values used on a reusable journal entry.

**Storage** `accounting_transaction_template_det`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_transaction_template` | integer | No | — | References [accounting_transaction_template](accounting.md#record-accounting_transaction_template) (rowid). |
| `general_account` | varchar(32) | No | — | Account number. |
| `general_label` | varchar(255) | No | — | Financial account label. |
| `subledger_account` | varchar(32) | Yes | — | Auxiliary account identifier used alongside a general account. |
| `subledger_label` | varchar(255) | Yes | — | Display label for the auxiliary account. |
| `operation_label` | varchar(255) | Yes | — | Operation Label. |
| `debit` | double(24,8) | Yes | — | Value entered on the debit side of the posting. |
| `credit` | double(24,8) | Yes | — | Value entered on the credit side of the posting. |

Source locations include `htdocs/install/mysql/tables/llx_accounting_transaction_template_det-accounting.sql`, `htdocs/install/mysql/tables/llx_accounting_transaction_template_det-accounting.key.sql`, `htdocs/accountancy/class/bookkeepingtemplate.class.php:155`.

<a id="record-chargesociales"></a>

## Statutory charge

Records a liability such as a tax or social contribution, its due dates and amount.

**Storage** `chargesociales`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(16) | Yes | — | Business reference used to identify the document or master record. |
| `date_ech` | datetime | No | — | Payment due date of the contribution. |
| `libelle` | varchar(80) | No | — | Display label for the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user` | integer | Yes | `NULL` | User account associated with this record. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `fk_type` | integer | No | — | Named type selected from the relevant dictionary. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `paye` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `periode` | date | Yes | — | Accounting or contribution period for the charge. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_chargesociales.sql`, `htdocs/compta/sociales/class/chargesociales.class.php:52`.

<a id="record-paiementcharge"></a>

## Statutory charge payment

Records a payment against a statutory charge and the related account movement.

**Storage** `paiementcharge`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_charge` | integer | Yes | — | Contribution liability against which the payment is recorded. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepaiement` | integer | No | — | Payment method or instrument. |
| `num_paiement` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_paiementcharge.sql`, `htdocs/compta/sociales/class/chargesociales.class.php:390`.

<a id="record-tva"></a>

## VAT liability

Holds a declared VAT obligation for a period with dates and amount.

**Storage** `tva`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `datep` | date | Yes | — | Payment or posting date for this financial record. |
| `datev` | date | Yes | — | Value/effective date in financial records. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepayment` | integer | Yes | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `paye` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_tva.sql`, `htdocs/compta/tva/class/tva.class.php:48`.

<a id="record-localtax"></a>

## Local tax liability

Records a local-tax obligation and the period and account details supporting its payment.

**Storage** `localtax`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `localtaxtype` | tinyint | Yes | — | Selects the local-tax family. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | date | Yes | — | Payment or posting date for this financial record. |
| `datev` | date | Yes | — | Value/effective date in financial records. |
| `amount` | double | Yes | — | Monetary amount. Its operational meaning follows the record purpose. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_localtax.sql`, `htdocs/compta/localtax/class/localtax.class.php:41`.

<a id="record-payment_vat"></a>

## VAT payment

Connects a tax settlement amount and date to a VAT liability and bank movement.

**Storage** `payment_vat`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_tva` | integer | Yes | — | Associated vat liability identifier. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepaiement` | integer | No | — | Payment method or instrument. |
| `num_paiement` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_payment_vat.sql`, `htdocs/compta/tva/class/tva.class.php:842`.

<a id="record-asset"></a>

## Fixed asset

Holds acquisition, service, model, depreciation and disposal information for an individual capital asset.

**Storage** `asset`.
The primary key is `rowid`.

**Referenced by** [asset_accountancy_codes_economic](accounting.md#record-asset_accountancy_codes_economic) (fk_asset), [asset_accountancy_codes_fiscal](accounting.md#record-asset_accountancy_codes_fiscal) (fk_asset), [asset_depreciation](accounting.md#record-asset_depreciation) (fk_asset), [asset_depreciation_options_economic](accounting.md#record-asset_depreciation_options_economic) (fk_asset), [asset_depreciation_options_fiscal](accounting.md#record-asset_depreciation_options_fiscal) (fk_asset).

The record class defines `0` draft, `1` validated, `9` disposed. See `htdocs/asset/class/asset.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `fk_asset_model` | integer | Yes | — | Asset template/model supplying defaults. References [asset_model](accounting.md#record-asset_model) (rowid). |
| `reversal_amount_ht` | double(24,8) | Yes | — | Reversal amount (without taxes). |
| `acquisition_value_ht` | double(24,8) | Yes | `NULL` | Acquisition amount (without taxes). |
| `recovered_vat` | double(24,8) | Yes | — | Recovered VAT. |
| `reversal_date` | date | Yes | — | Reversal date. |
| `date_acquisition` | date | No | — | Acquisition date. |
| `date_start` | date | No | — | Beginning of the applicable period. |
| `qty` | real | No | `1` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `acquisition_type` | smallint | No | `0` | Type of acquisition. |
| `asset_type` | smallint | No | `0` | Fixed asset classification. |
| `not_depreciated` | boolean | Yes | `false` | Not depreciated. |
| `disposal_date` | date | Yes | — | Date of disposal. |
| `disposal_amount_ht` | double(24,8) | Yes | — | Disposal value. |
| `fk_disposal_type` | integer | Yes | — | References [c_asset_disposal_type](dictionaries.md#record-c_asset_disposal_type) (rowid). |
| `disposal_depreciated` | boolean | Yes | `false` | Depreciate the year of transfer. |
| `disposal_subject_to_vat` | boolean | Yes | `false` | Disposal subject to VAT. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_asset-asset.sql`, `htdocs/install/mysql/tables/llx_asset-asset.key.sql`, `htdocs/asset/class/asset.class.php:48`.

<a id="record-asset_model"></a>

## Asset model

Defines reusable defaults for an asset class and the account or depreciation settings inherited when creating an asset.

**Storage** `asset_model`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `ref`.

**Referenced by** [asset](accounting.md#record-asset) (fk_asset_model), [asset_accountancy_codes_economic](accounting.md#record-asset_accountancy_codes_economic) (fk_asset_model), [asset_accountancy_codes_fiscal](accounting.md#record-asset_accountancy_codes_fiscal) (fk_asset_model), [asset_depreciation_options_economic](accounting.md#record-asset_depreciation_options_economic) (fk_asset_model), [asset_depreciation_options_fiscal](accounting.md#record-asset_depreciation_options_fiscal) (fk_asset_model).

The record class defines `0` draft, `1` validated, `9` canceled. See `htdocs/asset/class/assetmodel.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `asset_type` | smallint | No | — | Fixed asset classification. |
| `fk_pays` | integer | Yes | `0` | Country associated with the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_asset_model-asset.sql`, `htdocs/install/mysql/tables/llx_asset_model-asset.key.sql`, `htdocs/asset/class/assetmodel.class.php:50`.

<a id="record-asset_accountancy_codes_economic"></a>

## Economic depreciation accounts

Associates economic depreciation and disposal account choices with the asset or model references in the record.

**Storage** `asset_accountancy_codes_economic`.
The primary key is `rowid`.
Additional unique keys comprise `fk_asset` / `fk_asset_model`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_asset` | integer | Yes | — | Fixed asset linked to this entry. References [asset](accounting.md#record-asset) (rowid). |
| `fk_asset_model` | integer | Yes | — | Asset template/model supplying defaults. References [asset_model](accounting.md#record-asset_model) (rowid). |
| `asset` | varchar(32) | Yes | — | Asset. |
| `depreciation_asset` | varchar(32) | Yes | — | Depreciation. |
| `depreciation_expense` | varchar(32) | Yes | — | Depreciation expense. |
| `value_asset_sold` | varchar(32) | Yes | — | Value of asset disposed. |
| `receivable_on_assignment` | varchar(32) | Yes | — | Receivable on disposal. |
| `proceeds_from_sales` | varchar(32) | Yes | — | Proceeds from disposal. |
| `vat_collected` | varchar(32) | Yes | — | Collected VAT. |
| `vat_deductible` | varchar(32) | Yes | — | Recovered VAT on assets. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_asset_accountancy_codes_economic-asset.sql`, `htdocs/install/mysql/tables/llx_asset_accountancy_codes_economic-asset.key.sql`, `htdocs/asset/class/assetaccountancycodes.class.php:39`.

<a id="record-asset_accountancy_codes_fiscal"></a>

## Fiscal depreciation accounts

Associates fiscal depreciation and disposal account choices with the asset or model references in the record.

**Storage** `asset_accountancy_codes_fiscal`.
The primary key is `rowid`.
Additional unique keys comprise `fk_asset` / `fk_asset_model`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_asset` | integer | Yes | — | Fixed asset linked to this entry. References [asset](accounting.md#record-asset) (rowid). |
| `fk_asset_model` | integer | Yes | — | Asset template/model supplying defaults. References [asset_model](accounting.md#record-asset_model) (rowid). |
| `accelerated_depreciation` | varchar(32) | Yes | — | Fiscal account code for accelerated depreciation. |
| `endowment_accelerated_depreciation` | varchar(32) | Yes | — | Fiscal account code for the accelerated depreciation charge. |
| `provision_accelerated_depreciation` | varchar(32) | Yes | — | Fiscal provision account code for accelerated depreciation. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_asset_accountancy_codes_fiscal-asset.sql`, `htdocs/install/mysql/tables/llx_asset_accountancy_codes_fiscal-asset.key.sql`, `htdocs/asset/class/assetaccountancycodesfiscal.class.php:38`.

<a id="record-asset_depreciation_options_economic"></a>

## Economic depreciation parameters

Stores method, rate, duration and base settings used for economic depreciation.

**Storage** `asset_depreciation_options_economic`.
The primary key is `rowid`.
Additional unique keys comprise `fk_asset` / `fk_asset_model`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_asset` | integer | Yes | — | Fixed asset linked to this entry. References [asset](accounting.md#record-asset) (rowid). |
| `fk_asset_model` | integer | Yes | — | Asset template/model supplying defaults. References [asset_model](accounting.md#record-asset_model) (rowid). |
| `depreciation_type` | smallint | No | `0` | Selected depreciation calculation method. |
| `accelerated_depreciation_option` | boolean | Yes | `false` | Enables the fiscal accelerated depreciation option for the asset or model. |
| `degressive_coefficient` | double(24,8) | Yes | — | Coefficient applied to declining-balance depreciation. |
| `duration` | smallint | No | — | Duration of the activity or period in the unit used by the owning feature. |
| `duration_type` | smallint | No | `0` | Unit used for the depreciation duration. |
| `amount_base_depreciation_ht` | double(24,8) | Yes | — | Tax-exclusive basis from which depreciation is calculated. |
| `amount_base_deductible_ht` | double(24,8) | Yes | — | Tax-exclusive deductible basis used for the applicable depreciation schedule. |
| `total_amount_last_depreciation_ht` | double(24,8) | Yes | — | Cumulative tax-exclusive depreciation already recognised at the last recorded point. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_asset_depreciation_options_economic-asset.sql`, `htdocs/install/mysql/tables/llx_asset_depreciation_options_economic-asset.key.sql`, `htdocs/asset/class/asset.class.php:604`.

<a id="record-asset_depreciation_options_fiscal"></a>

## Fiscal depreciation parameters

Stores method, rate, duration and base settings used for fiscal depreciation.

**Storage** `asset_depreciation_options_fiscal`.
The primary key is `rowid`.
Additional unique keys comprise `fk_asset` / `fk_asset_model`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_asset` | integer | Yes | — | Fixed asset linked to this entry. References [asset](accounting.md#record-asset) (rowid). |
| `fk_asset_model` | integer | Yes | — | Asset template/model supplying defaults. References [asset_model](accounting.md#record-asset_model) (rowid). |
| `depreciation_type` | smallint | No | `0` | Selected depreciation calculation method. |
| `degressive_coefficient` | double(24,8) | Yes | — | Coefficient applied to declining-balance depreciation. |
| `duration` | smallint | No | — | Duration of the activity or period in the unit used by the owning feature. |
| `duration_type` | smallint | No | `0` | Unit used for the depreciation duration. |
| `amount_base_depreciation_ht` | double(24,8) | Yes | — | Tax-exclusive basis from which depreciation is calculated. |
| `amount_base_deductible_ht` | double(24,8) | Yes | — | Tax-exclusive deductible basis used for the applicable depreciation schedule. |
| `total_amount_last_depreciation_ht` | double(24,8) | Yes | — | Cumulative tax-exclusive depreciation already recognised at the last recorded point. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_asset_depreciation_options_fiscal-asset.sql`, `htdocs/install/mysql/tables/llx_asset_depreciation_options_fiscal-asset.key.sql`, `htdocs/asset/class/asset.class.php:601`.

<a id="record-asset_depreciation"></a>

## Depreciation schedule row

Dates a depreciation amount and cumulative charge for an asset and method, including the corresponding debit and credit accounts.

**Storage** `asset_depreciation`.
The primary key is `rowid`.
An additional unique key comprises `fk_asset`, `depreciation_mode`, `ref`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_asset` | integer | No | — | Fixed asset linked to this entry. References [asset](accounting.md#record-asset) (rowid). |
| `depreciation_mode` | varchar(255) | No | — | Basis of the schedule entry, such as economic or fiscal depreciation. |
| `ref` | varchar(255) | No | — | Business reference used to identify the document or master record. |
| `depreciation_date` | datetime | No | — | Date associated with the depreciation entry. |
| `depreciation_ht` | double(24,8) | No | — | Tax-exclusive depreciation amount for this entry. |
| `cumulative_depreciation_ht` | double(24,8) | No | — | Tax-exclusive accumulated depreciation through this entry. |
| `accountancy_code_debit` | varchar(32) | Yes | — | Account to debit for the recorded depreciation. |
| `accountancy_code_credit` | varchar(32) | Yes | — | Account to credit for the recorded depreciation. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |

Source locations include `htdocs/install/mysql/tables/llx_asset_depreciation-asset.sql`, `htdocs/install/mysql/tables/llx_asset_depreciation-asset.key.sql`, `htdocs/asset/class/asset.class.php:607`.

<a id="record-loan"></a>

## Loan agreement

Records borrowed capital, interest, costs, insurance, term and the account used for repayments.

**Storage** `loan`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `label` | varchar(80) | No | — | Display label for the record. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `capital` | double(24,8) | No | `0` | Principal of the loan. |
| `insurance_amount` | double(24,8) | Yes | `0` | Insurance amount recorded for the loan. |
| `datestart` | date | Yes | — | Beginning of the applicable period. |
| `dateend` | date | Yes | — | End of the applicable period. |
| `nbterm` | real | Yes | — | Number of scheduled loan terms. |
| `rate` | double | No | — | Rate used in the associated calculation. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `capital_position` | double(24,8) | Yes | `0` | Capital outstanding at the stored position date. |
| `date_position` | date | Yes | — | Effective date associated with the loan position. |
| `paid` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `accountancy_account_capital` | varchar(32) | Yes | — | Account used for the named component of a loan. |
| `accountancy_account_insurance` | varchar(32) | Yes | — | Account used for the named component of a loan. |
| `accountancy_account_interest` | varchar(32) | Yes | — | Account used for the named component of a loan. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `active` | tinyint | No | `1` | Whether this entry is enabled for selection or use. |

Source locations include `htdocs/install/mysql/tables/llx_loan-loan.sql`, `htdocs/loan/class/loan.class.php:48`.

<a id="record-loan_schedule"></a>

## Loan instalment

Breaks one scheduled repayment into principal, interest and other charges on a due date.

**Storage** `loan_schedule`.
The primary key is `rowid`.
An additional unique key comprises `fk_loan`, `datep`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_loan` | integer | Yes | — | Loan agreement concerned. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount_capital` | double(24,8) | Yes | `0` | Principal component of the instalment or payment. |
| `amount_insurance` | double(24,8) | Yes | `0` | Insurance component of the instalment or payment. |
| `amount_interest` | double(24,8) | Yes | `0` | Interest component of the instalment or payment. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_payment_loan` | integer | Yes | — | Associated loan payment identifier. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_loan_schedule-loan.sql`, `htdocs/install/mysql/tables/llx_loan_schedule-loan.key.sql`, `htdocs/loan/class/loanschedule.class.php:42`.

<a id="record-payment_loan"></a>

## Loan payment

Records a repayment with its loan, principal, interest, insurance and bank posting where specified.

**Storage** `payment_loan`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_loan` | integer | Yes | — | Loan agreement concerned. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount_capital` | double(24,8) | Yes | `0` | Principal component of the instalment or payment. |
| `amount_insurance` | double(24,8) | Yes | `0` | Insurance component of the instalment or payment. |
| `amount_interest` | double(24,8) | Yes | `0` | Interest component of the instalment or payment. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

Source locations include `htdocs/install/mysql/tables/llx_payment_loan.sql`, `htdocs/loan/class/loan.class.php:366`.
