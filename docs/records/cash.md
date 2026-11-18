# Payments, bank and collection orders

Payment headers capture settlement transactions. Allocation rows connect them to specific obligations. A bank movement is a different record from both the payment and the statement used for reconciliation.

**Example.** A customer pays 100.00 against two invoices. Store a single 100.00 receipt and allocations of 60.00 and 40.00. The cash book must show one economic inflow. Joining the header to both allocations and summing the header amount would count 200.00.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Customer receipt](#record-paiement) | `paiement` |
| [Receipt allocation](#record-paiement_facture) | `paiement_facture` |
| [Supplier payment](#record-paiementfourn) | `paiementfourn` |
| [Supplier payment allocation](#record-paiementfourn_facturefourn) | `paiementfourn_facturefourn` |
| [Bank or cash account](#record-bank_account) | `bank_account` |
| [Bank movement](#record-bank) | `bank` |
| [Bank source link](#record-bank_url) | `bank_url` |
| [Cheque deposit slip](#record-bordereau_cheque) | `bordereau_cheque` |
| [Debit processing record](#record-prelevement) | `prelevement` |
| [Bank order batch](#record-prelevement_bons) | `prelevement_bons` |
| [Bank order request](#record-prelevement_demande) | `prelevement_demande` |
| [Bank order instruction](#record-prelevement_lignes) | `prelevement_lignes` |
| [Rejected instruction](#record-prelevement_rejet) | `prelevement_rejet` |
| [Miscellaneous payment](#record-payment_various) | `payment_various` |
| [Cash-desk closing record](#record-pos_cash_fence) | `pos_cash_fence` |
| [Point-of-sale table](#record-takepos_floor_tables) | `takepos_floor_tables` |
| [Currency setup](#record-multicurrency) | `multicurrency` |
| [Dated exchange rate](#record-multicurrency_rate) | `multicurrency_rate` |

<a id="record-paiement"></a>

## Customer receipt

Records incoming cash, its date, payment instrument and bank posting. The amount attributable to each invoice resides in the allocation records.

**Storage** `paiement`.
The primary key is `rowid`.

**Referenced by** [paiement_facture](cash.md#record-paiement_facture) (fk_paiement).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `multicurrency_amount` | double(24,8) | Yes | `0` | Amount allocated or paid in the secondary currency. |
| `fk_paiement` | integer | No | — | Payment instrument for the receipt. The allocation bridge uses a field with the same name for the receipt itself. |
| `num_paiement` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `ext_payment_id` | varchar(255) | Yes | — | Provider's identifier for a transaction. |
| `ext_payment_site` | varchar(128) | Yes | — | External payment service or provider identifier. |
| `fk_bank` | integer | No | `0` | Related bank movement. Bank account identities use a different key. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_export_compta` | integer | No | `0` | Accounting export marker for the receipt. Zero identifies a receipt that has not been exported. |
| `pos_change` | double(24,8) | Yes | `0` | Change returned to the customer at checkout where recorded. |

<a id="record-paiement_facture"></a>

## Receipt allocation

Assigns part of a receipt to one customer invoice and records the company and document-currency amounts.

**Storage** `paiement_facture`.
The primary key is `rowid`.
An additional unique key comprises `fk_paiement`, `fk_facture`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_paiement` | integer | Yes | — | Payment header whose amount is being allocated to a customer invoice. References [paiement](cash.md#record-paiement) (rowid). |
| `fk_facture` | integer | Yes | — | Customer invoice identifier. References [facture](billing.md#record-facture) (rowid). |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_amount` | double(24,8) | Yes | `0` | Amount allocated or paid in the secondary currency. |

<a id="record-paiementfourn"></a>

## Supplier payment

Records an outgoing settlement with instrument, reference, date and associated bank movement.

**Storage** `paiementfourn`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `multicurrency_amount` | double(24,8) | Yes | `0` | Amount allocated or paid in the secondary currency. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_paiement` | integer | No | — | Customer receipt identity. |
| `num_paiement` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | No | — | Related bank movement. Bank account identities use a different key. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |

<a id="record-paiementfourn_facturefourn"></a>

## Supplier payment allocation

Applies a payment amount to a supplier bill in company currency and, where applicable, document currency.

**Storage** `paiementfourn_facturefourn`.
The primary key is `rowid`.
An additional unique key comprises `fk_paiementfourn`, `fk_facturefourn`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_paiementfourn` | integer | Yes | `NULL` | Outgoing supplier payment identity. |
| `fk_facturefourn` | integer | Yes | `NULL` | Supplier invoice receiving the allocation. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_amount` | double(24,8) | Yes | `0` | Amount allocated or paid in the secondary currency. |

<a id="record-bank_account"></a>

## Bank or cash account

Describes an account, currency and opening/operating parameters under which cash movements are recorded.

**Storage** `bank_account`.
The primary key is `rowid`.
An additional unique key comprises `label`, `entity`.

**Referenced by** [categorie_account](categories.md#record-categorie_account) (fk_account).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `ref` | varchar(12) | No | — | Business reference used to identify the document or master record. |
| `label` | varchar(50) | No | — | Display label for the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `bank` | varchar(60) | Yes | — | Name of the financial institution for the account details. |
| `code_banque` | varchar(128) | Yes | — | Domestic bank code. |
| `code_guichet` | varchar(6) | Yes | — | Domestic branch code. |
| `number` | varchar(255) | Yes | — | Number. |
| `cle_rib` | varchar(5) | Yes | — | Check digits for the domestic bank account identifier. |
| `bic` | varchar(11) | Yes | — | Bank identifier code for the receiving institution. |
| `bic_intermediate` | varchar(11) | Yes | — | Identifier of the intermediary financial institution. |
| `iban_prefix` | varchar(100) | Yes | — | International bank account number field used with the selected banking details. |
| `country_iban` | varchar(2) | Yes | — | Country iban. |
| `cle_iban` | varchar(2) | Yes | — | Cle iban. |
| `domiciliation` | varchar(255) | Yes | — | Bank or branch domiciliation details. |
| `pti_in_ctti` | smallint | Yes | `0` | Places the payment-type information inside individual transactions when generating a SEPA credit-transfer file. |
| `state_id` | integer | Yes | `NULL` | Administrative subdivision identity in an address. |
| `fk_pays` | integer | No | — | Country associated with the record. |
| `proprio` | varchar(60) | Yes | — | Name of the bank-account holder. |
| `owner_address` | varchar(255) | Yes | — | Address recorded for the bank-account holder. |
| `owner_zip` | varchar(25) | Yes | — | Owner zip. |
| `owner_town` | varchar(50) | Yes | — | Owner town. |
| `owner_country_id` | integer | Yes | `NULL` | Owner country. |
| `courant` | smallint | No | `0` | Courant. |
| `clos` | smallint | No | `0` | Clos. |
| `rappro` | smallint | Yes | `1` | Bank reconciliation marker. |
| `url` | varchar(128) | Yes | — | Web address or navigation target. |
| `account_number` | varchar(32) | Yes | — | Account number retained on the record. |
| `fk_accountancy_journal` | integer | Yes | — | References [accounting_journal](accounting.md#record-accounting_journal) (rowid). |
| `currency_code` | varchar(3) | No | — | Currency identifier for this record. |
| `min_allowed` | integer | Yes | `0` | Min allowed. |
| `min_desired` | integer | Yes | `0` | Min desired. |
| `comment` | text | Yes | — | Free-text annotation retained with the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `ics` | varchar(32) | Yes | — | Creditor identifier used when issuing collection instructions. |
| `ics_transfer` | varchar(32) | Yes | — | Creditor identifier recorded for transfer instructions. |

<a id="record-bank"></a>

## Bank movement

Records the dated movement on one bank or cash account. Statement and reconciliation information describe its matching status.

**Storage** `bank`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datev` | date | Yes | — | Value date at the bank. |
| `dateo` | date | Yes | — | Operation date of the bank movement. |
| `amount` | double(24,8) | No | `0` | Signed movement in the bank account currency. |
| `amount_main_currency` | double(24,8) | Yes | — | Base-currency amount recorded for the movement. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `fk_account` | integer | Yes | — | Bank or cash account that owns this statement movement. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_rappro` | integer | Yes | — | User who recorded bank reconciliation. |
| `fk_type` | varchar(6) | Yes | — | Named type selected from the relevant dictionary. |
| `num_releve` | varchar(50) | Yes | — | Statement identifier against which the movement was matched. |
| `num_chq` | varchar(50) | Yes | — | Cheque number. |
| `numero_compte` | varchar(32) | Yes | — | Account number retained on the record. |
| `rappro` | tinyint | Yes | `0` | Bank reconciliation marker. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bordereau` | integer | Yes | `0` | Deposit slip to which the bank movement belongs. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `banque` | varchar(255) | Yes | — | Bank name retained for the instrument or account. |
| `emetteur` | varchar(255) | Yes | — | Issuer of the payment instrument. |
| `author` | varchar(40) | Yes | — | Historical author field from the bank movement structure. |
| `origin_id` | integer | Yes | — | Originating record identity. |
| `origin_type` | varchar(64) | Yes | — | Type of originating record used to interpret the origin ID. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

<a id="record-bank_url"></a>

## Bank source link

Relates a bank movement to its operational origin via a target ID, type and navigation metadata.

**Storage** `bank_url`.
The primary key is `rowid`.
An additional unique key comprises `fk_bank`, `url_id`, `type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `url_id` | integer | Yes | — | ID in the object family selected by the bank link type. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `type` | varchar(24) | No | — | Family of object referenced by the bank entry. Interpret together with url_id. |

<a id="record-bordereau_cheque"></a>

## Cheque deposit slip

Groups cheques submitted for deposit under a dated slip and bank account.

**Storage** `bordereau_cheque`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

The stored state codes are `0` draft, `1` validated.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `type` | varchar(6) | Yes | `'CHQ'` | Type. |
| `datec` | datetime | No | — | When the row was created. |
| `date_bordereau` | date | Yes | — | Business date of the cheque deposit slip. |
| `amount` | double(24,8) | No | — | Monetary amount. Its operational meaning follows the record purpose. |
| `nbcheque` | smallint | No | — | Number of cheques on the deposit slip. |
| `fk_bank_account` | integer | Yes | — | Bank or cash account. Actual movements have their own identities. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

<a id="record-prelevement"></a>

## Debit processing record

Associates a bank-order instruction with a customer invoice, a supplier invoice or a salary obligation. The instruction contains the bank-order detail.

**Storage** `prelevement`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_facture` | integer | Yes | — | Customer invoice included in this bank-order instruction, when applicable. |
| `fk_facture_fourn` | integer | Yes | — | Supplier bill included in this bank-order instruction, when applicable. |
| `fk_salary` | integer | Yes | — | Salary obligation identity. |
| `fk_prelevement_lignes` | integer | No | — | Bank-order instruction associated with this payable item. References [prelevement_lignes](cash.md#record-prelevement_lignes) (rowid). |

<a id="record-prelevement_bons"></a>

## Bank order batch

Represents a generated banking file or batch, together with its total, status and transmission and credit dates.

**Storage** `prelevement_bons`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [prelevement_lignes](cash.md#record-prelevement_lignes) (fk_prelevement_bons).

The stored state codes are `0` draft, `1` transfered, `2` credited, `2` debited, `9` canceled.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `type` | varchar(16) | Yes | `'debit-order'` | Type. |
| `ref` | varchar(12) | Yes | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `credite` | smallint | Yes | `0` | Recorded credit/settlement marker of the bank-order batch. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `date_trans` | datetime | Yes | — | Date the batch was sent for bank processing. |
| `method_trans` | smallint | Yes | — | Recorded transmission mechanism. |
| `fk_user_trans` | integer | Yes | — | Operator responsible for transmission or settlement respectively. |
| `date_credit` | datetime | Yes | — | Date the batch was credited or settled. |
| `fk_user_credit` | integer | Yes | — | Operator responsible for transmission or settlement respectively. |
| `fk_bank_account` | integer | Yes | `NULL` | Bank or cash account. Actual movements have their own identities. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

<a id="record-prelevement_demande"></a>

## Bank order request

Records a request to include a payable item in a collection or transfer batch.

**Storage** `prelevement_demande`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_facture` | integer | Yes | — | Customer invoice identifier. |
| `fk_facture_fourn` | integer | Yes | — | Supplier invoice identifier. |
| `fk_salary` | integer | Yes | — | Salary obligation identity. |
| `sourcetype` | varchar(32) | Yes | — | Object kind for the corresponding endpoint of the relationship. |
| `amount` | double(24,8) | No | — | Monetary amount. Its operational meaning follows the record purpose. |
| `date_demande` | datetime | No | — | Date of submission of the bank order request. |
| `traite` | smallint | Yes | `0` | Whether the request has moved into a generated bank-order batch. |
| `date_traite` | datetime | Yes | — | When the bank-order request was processed. |
| `fk_prelevement_bons` | integer | Yes | — | Bank-order batch containing the instruction. |
| `fk_user_demande` | integer | No | — | User who requested collection or transfer. |
| `fk_societe_rib` | integer | Yes | `NULL` | Bank details chosen for the third party. |
| `code_banque` | varchar(128) | Yes | — | Domestic bank code. |
| `code_guichet` | varchar(6) | Yes | — | Domestic branch code. |
| `number` | varchar(255) | Yes | — | Account number recorded on the bank-order request. |
| `cle_rib` | varchar(5) | Yes | — | Check digits for the domestic bank account identifier. |
| `type` | varchar(12) | Yes | empty string | Type. |
| `ext_payment_id` | varchar(255) | Yes | — | Provider's identifier for a transaction. |
| `ext_payment_site` | varchar(128) | Yes | — | External payment service or provider identifier. |

<a id="record-prelevement_lignes"></a>

## Bank order instruction

Stores the counterparty bank coordinates and amount for an individual instruction in a bank order.

**Storage** `prelevement_lignes`.
The primary key is `rowid`.

**Referenced by** [prelevement](cash.md#record-prelevement) (fk_prelevement_lignes).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_prelevement_bons` | integer | Yes | — | Bank-order batch containing the instruction. References [prelevement_bons](cash.md#record-prelevement_bons) (rowid). |
| `fk_soc` | integer | No | — | Third party associated with this record. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `client_nom` | varchar(255) | Yes | — | Debtor name captured on the collection instruction. |
| `amount` | double(24,8) | Yes | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_prelevement_demande` | integer | Yes | `0` | Associated bank order request identifier. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

<a id="record-prelevement_rejet"></a>

## Rejected instruction

Records the rejection of a bank-order line with its reason, date, amount and any associated reversal.

**Storage** `prelevement_rejet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_prelevement_lignes` | integer | Yes | — | Bank-order instruction associated with this payable item. |
| `date_rejet` | datetime | Yes | — | Date of rejection of the collection. |
| `motif` | integer | Yes | — | Recorded reason for the collection rejection. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_creation` | integer | Yes | — | User who recorded the rejection. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `afacturer` | tinyint | Yes | `0` | Indicates whether the rejected collection is marked for invoicing. |
| `fk_facture` | integer | Yes | — | Customer invoice identifier. |

<a id="record-payment_various"></a>

## Miscellaneous payment

Records cash unrelated to a standard customer or supplier invoice, with account, direction, amount and counterparty data.

**Storage** `payment_various`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | Yes | — | Business reference used to identify the document or master record. |
| `num_payment` | varchar(50) | Yes | — | Reference printed or entered for the payment instrument. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `datep` | date | Yes | — | Payment or posting date for this financial record. |
| `datev` | date | Yes | — | Value/effective date in financial records. |
| `sens` | smallint | No | `0` | Direction/sign convention used by the owning reporting or posting operation. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `fk_typepayment` | integer | No | — | Payment method or instrument. |
| `accountancy_code` | varchar(32) | Yes | — | Account code selected for the transaction or classification. |
| `subledger_account` | varchar(32) | Yes | — | Auxiliary account identifier used alongside a general account. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |
| `fk_bank` | integer | Yes | — | Related bank movement. Bank account identities use a different key. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |

<a id="record-pos_cash_fence"></a>

## Cash-desk closing record

Records expected and counted amounts for a point-of-sale cash closing and associates it with an operator and terminal.

**Storage** `pos_cash_fence`.
The primary key is `rowid`.

The stored state codes are `0` draft, `1` validated, `1` closed.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(64) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `opening` | double(24,8) | Yes | `0` | Opening. |
| `cash` | double(24,8) | Yes | `0` | Cash. |
| `card` | double(24,8) | Yes | `0` | Credit card. |
| `cheque` | double(24,8) | Yes | `0` | Cheque. |
| `cash_declared` | double(24,8) | Yes | `NULL` | Cash declared. |
| `card_declared` | double(24,8) | Yes | `NULL` | Card declared. |
| `cheque_declared` | double(24,8) | Yes | `NULL` | Cheque declared. |
| `cash_lifetime` | double(24,8) | Yes | `NULL` | Cash lifetime. |
| `card_lifetime` | double(24,8) | Yes | `NULL` | Card lifetime. |
| `cheque_lifetime` | double(24,8) | Yes | `NULL` | Cheque lifetime. |
| `lifetime_start` | datetime | Yes | `NULL` | Lifetime Start Date. |
| `status` | integer | Yes | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `date_creation` | datetime | No | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `day_close` | integer | Yes | — | Day. |
| `month_close` | integer | Yes | — | Month. |
| `year_close` | integer | Yes | — | Year. |
| `hour_close` | integer | Yes | `null` | Hour. |
| `min_close` | integer | Yes | `null` | min. |
| `sec_close` | integer | Yes | `null` | Sec. |
| `posmodule` | varchar(30) | Yes | — | Module/Application. |
| `posnumber` | varchar(30) | Yes | — | Terminal. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

<a id="record-takepos_floor_tables"></a>

## Point-of-sale table

Identifies and positions a table on a sales floor, allowing a customer bill to be associated with the service location.

**Storage** `takepos_floor_tables`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `label`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `leftpos` | float | Yes | — | Table position on the point-of-sale floor plan. |
| `toppos` | float | Yes | — | Table position on the point-of-sale floor plan. |
| `floor` | smallint | Yes | — | Floor plan containing the checkout table. |

<a id="record-multicurrency"></a>

## Currency setup

Enables a currency in an entity and records its configured code and name.

**Storage** `multicurrency`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `date_create` | datetime | Yes | `NULL` | When the row was created. |
| `code` | varchar(255) | Yes | `NULL` | Machine-readable code identifying a dictionary entry or feature value. |
| `name` | varchar(255) | Yes | `NULL` | Name under which this record is presented or identified. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | Yes | `NULL` | User account associated with this record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

<a id="record-multicurrency_rate"></a>

## Dated exchange rate

Stores exchange rates for an enabled currency at particular dates. Commercial documents can retain the rate applied at the time of issue.

**Storage** `multicurrency_rate`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `date_sync` | datetime | Yes | `NULL` | Time associated with the recorded exchange rate. |
| `rate` | double | No | `0` | Rate used in the associated calculation. |
| `rate_direct` | double | Yes | `0` | Direct exchange rate recorded for this currency observation. |
| `fk_multicurrency` | integer | No | — | Configured document currency record. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
