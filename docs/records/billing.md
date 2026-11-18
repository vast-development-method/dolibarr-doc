# Sales and supplier invoices

Customer and supplier invoices establish different liabilities. Templates generate future documents independently of their invoice identities and references. Cash allocations, credits and journal transfers are distinct downstream records.

**Example.** A customer invoice of 100.00 with a 70.00 receipt allocation and a 10.00 applied credit has 20.00 remaining in the simple same-currency case. Its issued total remains 100.00. Reading only the payment header can misstate settlement when that receipt paid more than one invoice.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Customer invoice](#record-facture) | `facture` |
| [Customer invoice line](#record-facturedet) | `facturedet` |
| [Recurring customer billing template](#record-facture_rec) | `facture_rec` |
| [Recurring customer billing line](#record-facturedet_rec) | `facturedet_rec` |
| [Supplier invoice](#record-facture_fourn) | `facture_fourn` |
| [Supplier invoice line](#record-facture_fourn_det) | `facture_fourn_det` |
| [Recurring supplier billing template](#record-facture_fourn_rec) | `facture_fourn_rec` |
| [Recurring supplier billing line](#record-facture_fourn_det_rec) | `facture_fourn_det_rec` |

<a id="record-facture"></a>

## Customer invoice

Carries the receivable, invoice kind, customer, currency, dates, close reason and document totals.

**Storage** `facture`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_invoice](categories.md#record-categorie_invoice) (fk_invoice), [facture](billing.md#record-facture) (fk_facture_source), [facturedet](billing.md#record-facturedet) (fk_facture), [paiement_facture](cash.md#record-paiement_facture) (fk_facture), [societe_remise_except](parties.md#record-societe_remise_except) (fk_facture), [societe_remise_except](parties.md#record-societe_remise_except) (fk_facture_source).

The stored state codes are `0` draft, `1` validated, `2` closed, `3` abandoned.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_client` | varchar(255) | Yes | — | Reference supplied by the customer. |
| `type` | smallint | No | `0` | Document kind, including standard, replacement, credit, deposit and progress billing. |
| `subtype` | smallint | Yes | `NULL` | Additional classification within the main type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `datef` | date | Yes | — | Invoice date in billing records. |
| `date_pointoftax` | date | Yes | `NULL` | Tax point date where the relevant accounting treatment uses it. |
| `date_valid` | date | Yes | — | When validation was recorded. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_closing` | datetime | Yes | — | When the record was closed. |
| `paye` | smallint | No | `0` | Stored settlement marker also read by collection logic. State and closing reason distinguish how an invoice was closed. |
| `remise_percent` | real | Yes | `0` | Compatibility header percentage. Line values and applied adjustments carry the current invoice discount calculation. |
| `remise_absolue` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `remise` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `close_code` | varchar(16) | Yes | — | Reason for closing an invoice, including a settlement that leaves an unpaid difference. |
| `close_missing_amount` | double(24,8) | Yes | — | Field for the amount left outstanding at closure. Reconcile actual allocations to calculate the outstanding balance. |
| `close_note` | varchar(128) | Yes | — | Explanation retained with the closure. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `revenuestamp` | double(24,8) | Yes | `0` | Fixed revenue-stamp component recorded on the document. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_statut` | smallint | No | `0` | Lifecycle state. A closed document can carry a reason for a short or exceptional settlement. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `fk_user_closing` | integer | Yes | — | Account that recorded closure. |
| `module_source` | varchar(32) | Yes | — | Feature that originated this business document. |
| `pos_source` | varchar(32) | Yes | — | Checkout terminal or other sales-channel source retained on the document. |
| `pos_print_counter` | integer | Yes | `0` | Print Count. |
| `email_sent_counter` | integer | Yes | `0` | Recorded count of invoice or receipt email sends. |
| `fk_fac_rec_source` | integer | Yes | — | Recurring template from which the invoice was generated. |
| `fk_facture_source` | integer | Yes | — | Customer invoice from which this replacement, credit or adjustment originates. References [facture](billing.md#record-facture) (rowid). |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `increment` | varchar(10) | Yes | — | Generation sequence when the invoice originates from a recurring template. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_currency` | varchar(3) | Yes | — | Currency identifier for this record. |
| `fk_cond_reglement` | integer | No | `1` | Terms governing settlement and due-date calculation. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `date_lim_reglement` | date | Yes | — | Date by which payment falls due. |
| `payment_reference` | varchar(25) | Yes | — | Reference passed to or returned by the payment arrangement. |
| `fk_thirdparty_rib_id` | integer | Yes | — | Bank details chosen for the third party. |
| `dispute_status` | integer | Yes | `0` | Recorded dispute state. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `fk_input_reason` | integer | Yes | `NULL` | Commercial origin or reason captured on the document. References [c_input_reason](dictionaries.md#record-c_input_reason) (rowid). |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `fk_transport_mode` | integer | Yes | — | Selected mode of transport. |
| `prorata_discount` | real | Yes | `NULL` | Percentage used to apportion an invoice discount across tax rates. |
| `situation_cycle_ref` | integer | Yes | — | Progress-billing cycle shared by successive invoices for the same work. |
| `situation_counter` | smallint | Yes | — | Sequence within the progress-billing cycle. |
| `situation_final` | smallint | Yes | — | Marks the final invoice in the progress-billing cycle. |
| `retained_warranty` | real | Yes | `NULL` | Retention percentage applied to the eligible gross amount. |
| `retained_warranty_amount` | double(24,8) | Yes | `NULL` | Stored retention figure. The invoice calculation can recompute it from progress and retention settings. |
| `retained_warranty_date_limit` | date | Yes | `NULL` | Due date for the retained portion. |
| `retained_warranty_fk_cond_reglement` | integer | Yes | `NULL` | Payment term used for the retained portion. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `is_also_delivery_note` | tinyint | No | `0` | Indicates that the invoice can serve as a delivery document under the selected configuration. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

<a id="record-facturedet"></a>

## Customer invoice line

Records the quantity, tax base, discounts and tax amounts for one item or service billed. Source-line and credit information link certain corrections to earlier activity.

**Storage** `facturedet`.
The primary key is `rowid`.
An additional unique key comprises `fk_remise_except`, `fk_facture`.

**Referenced by** [societe_remise_except](parties.md#record-societe_remise_except) (fk_facture_line).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_facture` | integer | No | — | Customer invoice identifier. References [facture](billing.md#record-facture) (rowid). |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `subprice` | double(24,8) | Yes | — | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `price` | double(24,8) | Yes | — | Legacy storage. Use the current business representation described for the owning record. |
| `total_ht` | double(24,8) | Yes | — | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | — | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | — | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24,8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `batch` | varchar(128) | Yes | — | Batch or serial identifier used on stock positions and movements. |
| `fk_warehouse` | integer | Yes | — | Warehouse or stock location. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_contract_line` | integer | Yes | — | Contract service line. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_code_ventilation` | integer | No | `0` | Account binding recorded for distribution to the ledger. |
| `situation_percent` | real | Yes | `100` | Progress percentage recorded on the line for this billing stage. |
| `fk_prev_id` | integer | Yes | — | Preceding progress-invoice line in the same billing cycle. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `ref_ext` | varchar(255) | Yes | `NULL` | Identifier supplied by an external application or interface. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

<a id="record-facture_rec"></a>

## Recurring customer billing template

Stores the commercial header and scheduling rules from which customer invoices can be generated.

**Storage** `facture_rec`.
The primary key is `rowid`.
An additional unique key comprises `titre`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `titre` | varchar(200) | No | — | Display title. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `subtype` | smallint | Yes | `NULL` | Additional classification within the main type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `suspended` | integer | Yes | `0` | Whether scheduled generation is suspended. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `remise` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `remise_percent` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `remise_absolue` | real | Yes | `0` | Legacy storage. Use the current business representation described for the owning record. |
| `vat_src_code` | varchar(10) | Yes | empty string | Legacy storage. Use the current business representation described for the owning record. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `revenuestamp` | double(24,8) | Yes | `0` | Fixed revenue-stamp component recorded on the document. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_projet` | integer | Yes | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `fk_cond_reglement` | integer | No | `1` | Terms governing settlement and due-date calculation. |
| `fk_mode_reglement` | integer | Yes | `0` | Payment method or instrument. |
| `date_lim_reglement` | date | Yes | — | Date by which payment falls due. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_societe_rib` | integer | Yes | — | Bank details chosen for the third party. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `modelpdf` | varchar(255) | Yes | — | Selected document output model. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `usenewprice` | integer | Yes | `0` | Whether recurring generation uses updated pricing. |
| `usenewcurrencyrate` | integer | Yes | `0` | Whether recurring generation obtains a new exchange rate. |
| `frequency` | integer | Yes | — | Repeat interval in units specified by the associated frequency field. |
| `unit_frequency` | varchar(2) | Yes | `'m'` | Time unit in which a recurring interval is expressed. |
| `rule_for_lines_dates` | varchar(255) | Yes | `'prepaid'` | Rule for lines dates. |
| `date_when` | datetime | Yes | `NULL` | Next scheduled occurrence or generation date. |
| `date_last_gen` | datetime | Yes | `NULL` | Time of the last generated occurrence. |
| `nb_gen_done` | integer | Yes | `NULL` | Number of generated occurrences recorded on the template. |
| `nb_gen_max` | integer | Yes | `NULL` | Occurrence limit stored on the template. |
| `auto_validate` | integer | Yes | `0` | Requests automatic validation of generated documents. |
| `fk_email_template` | integer | Yes | `NULL` | Selected message template. |
| `generate_pdf` | integer | Yes | `1` | Requests generation of the document output. |

<a id="record-facturedet_rec"></a>

## Recurring customer billing line

Supplies reusable line details for future invoices generated from a template.

**Storage** `facturedet_rec`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_facture` | integer | No | — | Customer invoice identifier. |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `subprice` | double(24,8) | No | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `price` | double(24,8) | Yes | — | Legacy storage. Use the current business representation described for the owning record. |
| `total_ht` | double(24,8) | Yes | — | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | — | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | — | Total including tax in base currency. |
| `date_start_fill` | integer | Yes | `0` | Selects automatic population of the corresponding service-period boundary during invoice generation. |
| `date_end_fill` | integer | Yes | `0` | Selects automatic population of the corresponding service-period boundary during invoice generation. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24,8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `special_code` | integer unsigned | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_contract_line` | integer | Yes | — | Contract service line. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

<a id="record-facture_fourn"></a>

## Supplier invoice

Records a supplier payable, its supplier-side reference, billed values, tax and settlement state.

**Storage** `facture_fourn`.
The primary key is `rowid`.
Additional unique keys comprise `ref`, `entity` / `ref_supplier`, `fk_soc`, `entity`.

**Referenced by** [categorie_supplier_invoice](categories.md#record-categorie_supplier_invoice) (fk_supplier_invoice), [facture_fourn_det](billing.md#record-facture_fourn_det) (fk_facture_fourn), [societe_remise_except](parties.md#record-societe_remise_except) (fk_invoice_supplier).

The stored state codes are `0` draft, `1` validated, `2` closed, `3` abandoned.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(180) | No | — | Business reference used to identify the document or master record. |
| `ref_supplier` | varchar(180) | No | — | Reference assigned or communicated by the supplier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `type` | smallint | No | `0` | Supplier document kind, including credits and deposits. |
| `subtype` | smallint | Yes | `NULL` | Additional classification within the main type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `datef` | date | Yes | — | Invoice date in billing records. |
| `date_pointoftax` | date | Yes | `NULL` | Tax point date where the relevant accounting treatment uses it. |
| `date_valid` | date | Yes | — | When validation was recorded. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_closing` | datetime | Yes | — | When the record was closed. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `paye` | smallint | No | `0` | Stored payment classification. Outstanding cash requires reconciling allocations and applied credits. |
| `amount` | double(24,8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `remise` | double(24,8) | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `close_code` | varchar(16) | Yes | — | Reason for closing an invoice, including a settlement that leaves an unpaid difference. |
| `close_missing_amount` | double(24,8) | Yes | — | Field for the amount left outstanding at closure. Reconcile actual allocations to calculate the outstanding balance. |
| `close_note` | varchar(128) | Yes | — | Explanation retained with the closure. |
| `vat_reverse_charge` | tinyint | Yes | `0` | Indicates the reverse-charge tax treatment on a purchase. |
| `tva` | double(24,8) | Yes | `0` | Total VAT amount of the supplier invoice. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `revenuestamp` | double(24,8) | Yes | `0` | Fixed revenue-stamp component recorded on the document. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `fk_user_closing` | integer | Yes | — | Account that recorded closure. |
| `fk_fac_rec_source` | integer | Yes | — | Recurring template from which the invoice was generated. |
| `fk_facture_source` | integer | Yes | — | Customer invoice from which this replacement, credit or adjustment originates. |
| `fk_projet` | integer | Yes | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_cond_reglement` | integer | Yes | — | Terms governing settlement and due-date calculation. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `date_lim_reglement` | date | Yes | — | Date by which payment falls due. |
| `payment_reference` | varchar(25) | Yes | — | Reference passed to or returned by the payment arrangement. |
| `fk_thirdparty_rib_id` | integer | Yes | — | Bank details chosen for the third party. |
| `dispute_status` | integer | Yes | `0` | Recorded dispute state. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `fk_transport_mode` | integer | Yes | — | Selected mode of transport. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |

<a id="record-facture_fourn_det"></a>

## Supplier invoice line

Holds the purchased product or expense, quantity, price and tax distribution for a supplier bill.

**Storage** `facture_fourn_det`.
The primary key is `rowid`.
An additional unique key comprises `fk_remise_except`, `fk_facture_fourn`.

**Referenced by** [societe_remise_except](parties.md#record-societe_remise_except) (fk_invoice_supplier_line).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_facture_fourn` | integer | No | — | Supplier invoice identifier. References [facture_fourn](billing.md#record-facture_fourn) (rowid). |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `ref` | varchar(128) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `pu_ht` | double(24,8) | Yes | — | Unit selling price before tax. |
| `pu_ttc` | double(24,8) | Yes | — | Tax-inclusive unit selling price. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `total_ht` | double(24,8) | Yes | — | Total before tax in base currency after applicable line adjustments. |
| `tva` | double(24,8) | Yes | — | Extended VAT amount for the supplier invoice line. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | — | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `fk_code_ventilation` | integer | No | `0` | Account binding recorded for distribution to the ledger. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

<a id="record-facture_fourn_rec"></a>

## Recurring supplier billing template

Describes a repeat supplier bill and the schedule for generating subsequent bills.

**Storage** `facture_fourn_rec`.
The primary key is `rowid`.
An additional unique key comprises `titre`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `titre` | varchar(200) | No | — | Display title. |
| `ref_supplier` | varchar(180) | No | — | Reference assigned or communicated by the supplier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `subtype` | smallint | Yes | `NULL` | Additional classification within the main type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `suspended` | integer | Yes | `0` | Whether scheduled generation is suspended. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `amount` | double(24, 8) | No | `0` | Monetary amount. Its operational meaning follows the record purpose. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_projet` | integer | Yes | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_cond_reglement` | integer | Yes | — | Terms governing settlement and due-date calculation. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `date_lim_reglement` | date | Yes | — | Date by which payment falls due. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `modelpdf` | varchar(255) | Yes | — | Selected document output model. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `usenewprice` | integer | Yes | `0` | Whether recurring generation uses updated pricing. |
| `usenewcurrencyrate` | integer | Yes | `0` | Whether recurring generation obtains a new exchange rate. |
| `frequency` | integer | Yes | — | Repeat interval in units specified by the associated frequency field. |
| `unit_frequency` | varchar(2) | Yes | `'m'` | Time unit in which a recurring interval is expressed. |
| `date_when` | datetime | Yes | `NULL` | Next scheduled occurrence or generation date. |
| `date_last_gen` | datetime | Yes | `NULL` | Time of the last generated occurrence. |
| `nb_gen_done` | integer | Yes | `NULL` | Number of generated occurrences recorded on the template. |
| `nb_gen_max` | integer | Yes | `NULL` | Occurrence limit stored on the template. |
| `auto_validate` | integer | Yes | `0` | Requests automatic validation of generated documents. |
| `generate_pdf` | integer | Yes | `1` | Requests generation of the document output. |

<a id="record-facture_fourn_det_rec"></a>

## Recurring supplier billing line

Provides the product, value and tax entries reused on generated supplier bills.

**Storage** `facture_fourn_det_rec`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_facture_fourn` | integer | No | — | Supplier invoice identifier. |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `ref` | varchar(50) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `pu_ht` | double(24,8) | Yes | — | Unit selling price before tax. |
| `pu_ttc` | double(24,8) | Yes | — | Tax-inclusive unit selling price. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `total_ht` | double(24,8) | Yes | — | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | — | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | — | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | integer | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | integer | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `special_code` | integer unsigned | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
