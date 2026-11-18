# Offers, orders and fulfilment

The header is the agreement or delivery document. Its lines identify what was agreed and later fulfilled. A source document edge gives the origin of the overall document. Allocations by originating line and quantity establish fulfilment.

**Example.** Consider two order lines for the same product, quantities 7 and 5. A shipment of 4 from the second line leaves 7 and 1 to fulfil. Grouping only by product gives 8 remaining but loses the identity required to decide which source line can be shipped next.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Customer proposal](#record-propal) | `propal` |
| [Proposal line](#record-propaldet) | `propaldet` |
| [Proposal product attachments](#record-propal_merge_pdf_product) | `propal_merge_pdf_product` |
| [Customer order](#record-commande) | `commande` |
| [Customer order line](#record-commandedet) | `commandedet` |
| [Shipment](#record-expedition) | `expedition` |
| [Shipment allocation](#record-expeditiondet) | `expeditiondet` |
| [Shipment lot allocation](#record-expeditiondet_batch) | `expeditiondet_batch` |
| [Delivery acknowledgement](#record-delivery) | `delivery` |
| [Delivery acknowledgement line](#record-deliverydet) | `deliverydet` |
| [Supplier price request](#record-supplier_proposal) | `supplier_proposal` |
| [Supplier proposal line](#record-supplier_proposaldet) | `supplier_proposaldet` |
| [Purchase order](#record-commande_fournisseur) | `commande_fournisseur` |
| [Purchase order line](#record-commande_fournisseurdet) | `commande_fournisseurdet` |
| [Goods receipt](#record-reception) | `reception` |
| [Supplier receipt allocation](#record-receptiondet_batch) | `receptiondet_batch` |

<a id="record-propal"></a>

## Customer proposal

Represents an offer to a customer, with validity date, commercial terms, sign-off and disposition.

**Storage** `propal`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_propal](categories.md#record-categorie_propal) (fk_propal), [propaldet](commercial.md#record-propaldet) (fk_propal).

The record class defines `-1` canceled, `0` draft, `1` validated, `2` signed, `3` notsigned, `4` billed. See `htdocs/comm/propal/class/propal.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_client` | varchar(255) | Yes | — | Reference supplied by the customer. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `datep` | date | Yes | — | Payment or posting date for this financial record. |
| `fin_validite` | datetime | Yes | — | End of the validity interval. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `date_signature` | datetime | Yes | — | Date the agreement or offer was signed. |
| `date_cloture` | datetime | Yes | — | When the record was closed. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `fk_user_signature` | integer | Yes | — | References [user](foundation.md#record-user) (rowid). |
| `fk_user_cloture` | integer | Yes | — | Account that recorded closure. References [user](foundation.md#record-user) (rowid). |
| `fk_statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `price` | real | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `remise_percent` | real | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `remise_absolue` | real | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `remise` | real | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_currency` | varchar(3) | Yes | — | Currency identifier for this record. |
| `fk_cond_reglement` | integer | Yes | — | Terms governing settlement and due-date calculation. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `online_sign_ip` | varchar(48) | Yes | — | Network address retained when the remote signature was submitted. |
| `online_sign_name` | varchar(64) | Yes | — | Name supplied during online signature. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `model_pdf_pos_sign` | varchar(32) | Yes | — | Saved position and dimensions of the signature area in the proposal output. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `date_livraison` | date | Yes | `NULL` | Delivery date retained on the originating record. |
| `fk_shipping_method` | integer | Yes | — | Selected dispatch or transport service. |
| `fk_warehouse` | integer | Yes | `NULL` | Warehouse or stock location. |
| `fk_availability` | integer | Yes | — | Delivery availability or lead-time term. |
| `fk_input_reason` | integer | Yes | — | Commercial origin or reason captured on the document. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `fk_delivery_address` | integer | Yes | — | Contact or address used for delivery where the field is active. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |

Source locations include `htdocs/install/mysql/tables/llx_propal.sql`, `htdocs/install/mysql/tables/llx_propal.key.sql`, `htdocs/comm/propal/class/propal.class.php:73`.

<a id="record-propaldet"></a>

## Proposal line

Represents one proposed product, service or text entry, including price, quantity, tax basis and ordering within the offer.

**Storage** `propaldet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_propal` | integer | No | — | Customer proposal identity. References [propal](commercial.md#record-propal) (rowid). |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | `0` | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `price` | real | Yes | — | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24,8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_propaldet.sql`, `htdocs/install/mysql/tables/llx_propaldet.key.sql`, `htdocs/comm/propal/class/propal.class.php:78`.

<a id="record-propal_merge_pdf_product"></a>

## Proposal product attachments

Selects and orders product documents that may be combined with a generated proposal.

**Storage** `propal_merge_pdf_product`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `file_name` | varchar(200) | No | — | Product document to include in the assembled proposal output. |
| `lang` | varchar(5) | Yes | `NULL` | Language code under which this text or presentation is stored. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_mod` | integer | No | — | Account recorded for the latest modification. |
| `datec` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_propal_merge_pdf_product.sql`, `htdocs/product/class/propalmergepdfproduct.class.php:44`.

<a id="record-commande"></a>

## Customer order

Records a customer commitment. Order fulfilment state and billed classification can change independently.

**Storage** `commande`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_order](categories.md#record-categorie_order) (fk_order), [commandedet](commercial.md#record-commandedet) (fk_commande).

The record class defines `-1` canceled, `0` draft, `1` validated, `2` shipmentonprocess, `2` accepted, `3` closed, `0` no signature, `1` signed sender, `2` signed receiver, `9` signed all. See `htdocs/commande/class/commande.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_client` | varchar(255) | Yes | — | Reference supplied by the customer. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `date_cloture` | datetime | Yes | — | When the record was closed. |
| `date_commande` | date | Yes | — | Order date. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `fk_user_cloture` | integer | Yes | — | Account that recorded closure. References [user](foundation.md#record-user) (rowid). |
| `source` | smallint | Yes | — | Source. |
| `fk_statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `amount_ht` | double(24,8) | Yes | `0` | Monetary amount before tax. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise_absolue` | real | Yes | `0` | Fixed monetary discount field retained in the stored layout. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `revenuestamp` | double(24,8) | Yes | `0` | Fixed revenue-stamp component recorded on the document. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `signed_status` | smallint | Yes | `NULL` | Recorded electronic-signature state. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `module_source` | varchar(32) | Yes | — | Feature that originated this business document. |
| `pos_source` | varchar(32) | Yes | — | Checkout terminal or other sales-channel source retained on the document. |
| `facture` | tinyint | Yes | `0` | Billing indicator on the customer order. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_currency` | varchar(3) | Yes | — | Currency identifier for this record. |
| `fk_cond_reglement` | integer | Yes | — | Terms governing settlement and due-date calculation. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `date_livraison` | datetime | Yes | `NULL` | Delivery date retained on the originating record. |
| `fk_shipping_method` | integer | Yes | — | Selected dispatch or transport service. |
| `fk_warehouse` | integer | Yes | `NULL` | Warehouse or stock location. |
| `fk_availability` | integer | Yes | — | Delivery availability or lead-time term. |
| `fk_input_reason` | integer | Yes | — | Commercial origin or reason captured on the document. |
| `fk_delivery_address` | integer | Yes | — | Contact or address used for delivery where the field is active. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `user_agent` | varchar(255) | Yes | — | Client application identification retained with the event. |

Source locations include `htdocs/install/mysql/tables/llx_commande.sql`, `htdocs/install/mysql/tables/llx_commande.key.sql`, `htdocs/commande/class/commande.class.php:71`.

<a id="record-commandedet"></a>

## Customer order line

Holds the quantity, selling terms and calculated totals for one order entry. Shipment allocations need the line identity when a product appears on several lines.

**Storage** `commandedet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_commande` | integer | No | — | Customer order identity. References [commande](commercial.md#record-commande) (rowid). |
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
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `fk_remise_except` | integer | Yes | — | Fixed credit or discount from which this row originated. |
| `price` | real | Yes | — | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24,8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `ref_ext` | varchar(255) | Yes | `NULL` | Identifier supplied by an external application or interface. |
| `fk_commandefourndet` | integer | Yes | `NULL` | References [commande_fournisseurdet](commercial.md#record-commande_fournisseurdet) (rowid). |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_commandedet.sql`, `htdocs/install/mysql/tables/llx_commandedet.key.sql`, `htdocs/delivery/class/delivery.class.php:677`.

<a id="record-expedition"></a>

## Shipment

Groups goods dispatched to a party with carrier, tracking, warehouse and validation information.

**Storage** `expedition`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [expeditiondet](commercial.md#record-expeditiondet) (fk_expedition).

The record class defines `0` draft, `1` validated, `2` closed, `-1` canceled, `3` shipment in progress. See `htdocs/expedition/class/expedition.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_customer` | varchar(255) | Yes | — | Reference provided by the customer. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `date_delivery` | datetime | Yes | `NULL` | Delivery date retained on the originating record. |
| `date_expedition` | datetime | Yes | — | Provision for the actual dispatch date in the installation definition. |
| `fk_address` | integer | Yes | `NULL` | Historical delivery address field marked deprecated by the installation declaration. |
| `fk_shipping_method` | integer | Yes | — | Selected dispatch or transport service. References [c_shipment_mode](dictionaries.md#record-c_shipment_mode) (rowid). |
| `tracking_number` | varchar(50) | Yes | — | Carrier's shipment-tracking identifier. |
| `fk_statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `billed` | smallint | Yes | `0` | Billed classification tracked separately from physical delivery. |
| `height` | float | Yes | — | Physical horizontal or vertical dimension, respectively. |
| `width` | float | Yes | — | Physical horizontal or vertical dimension, respectively. |
| `size_units` | integer | Yes | — | Unit or scale used for the associated dimensions. |
| `size` | float | Yes | — | Size or depth in the relevant physical unit. |
| `weight_units` | integer | Yes | — | Unit or scale used to interpret the associated weight. |
| `weight` | float | Yes | — | Physical weight in the associated unit. |
| `signed_status` | smallint | Yes | `NULL` | Recorded electronic-signature state. |
| `online_sign_ip` | varchar(48) | Yes | — | Network address retained when the remote signature was submitted. |
| `online_sign_name` | varchar(64) | Yes | — | Name supplied during online signature. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_expedition.sql`, `htdocs/install/mysql/tables/llx_expedition.key.sql`, `htdocs/expedition/class/expedition.class.php:77`.

<a id="record-expeditiondet"></a>

## Shipment allocation

Assigns a shipment quantity to the originating order line and warehouse. One order line can be fulfilled through multiple shipments.

**Storage** `expeditiondet`.
The primary key is `rowid`.

**Referenced by** [expeditiondet_batch](commercial.md#record-expeditiondet_batch) (fk_expeditiondet).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_expedition` | integer | No | — | Shipment to which this position belongs. References [expedition](commercial.md#record-expedition) (rowid). |
| `fk_element` | integer | Yes | — | Target record identity. Where an object type accompanies it, both values identify the target. |
| `fk_elementdet` | integer | Yes | — | Related detail-line identity. |
| `element_type` | varchar(50) | No | `'commande'` | Type discriminator identifying the class of associated object. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `fk_parent` | integer | Yes | — | Record one level above this one in the owning hierarchy. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_unit` | integer | Yes | — | Unit of measure associated with the quantity. |
| `fk_entrepot` | integer | Yes | — | Warehouse or stock location. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_expeditiondet.sql`, `htdocs/install/mysql/tables/llx_expeditiondet.key.sql`, `htdocs/commande/class/commande.class.php:2429`.

<a id="record-expeditiondet_batch"></a>

## Shipment lot allocation

Subdivides a shipment line into the batches or serial lots taken from stock.

**Storage** `expeditiondet_batch`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_expeditiondet` | int | No | — | References [expeditiondet](commercial.md#record-expeditiondet) (rowid). |
| `eatby` | date | Yes | `NULL` | Use-by date associated with a lot. |
| `sellby` | date | Yes | `NULL` | Sell-by date associated with a lot. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `qty` | double | No | `'0'` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_origin_stock` | integer | No | — | Batch-level warehouse position identified on the shipment allocation. |
| `fk_warehouse` | integer | Yes | `NULL` | Warehouse or stock location. |

Source locations include `htdocs/install/mysql/tables/llx_expeditiondet_batch.sql`, `htdocs/install/mysql/tables/llx_expeditiondet_batch.key.sql`, `htdocs/expedition/class/expedition.class.php:3073`.

<a id="record-delivery"></a>

## Delivery acknowledgement

Records acknowledgement of a delivery linked to a shipment when separate delivery receipts are enabled.

**Storage** `delivery`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [deliverydet](commercial.md#record-deliverydet) (fk_delivery).

The record class defines `0` draft, `1` validated, `-1` canceled. See `htdocs/delivery/class/delivery.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_customer` | varchar(255) | Yes | — | Reference provided by the customer. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `date_delivery` | datetime | Yes | `NULL` | Delivery date retained on the originating record. |
| `fk_address` | integer | Yes | — | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `fk_statut` | smallint | Yes | `0` | State of the delivery acknowledgement; the originating shipment keeps its own state. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_delivery.sql`, `htdocs/install/mysql/tables/llx_delivery.key.sql`, `htdocs/delivery/class/delivery.class.php:70`.

<a id="record-deliverydet"></a>

## Delivery acknowledgement line

Captures line-level quantities on the separate delivery acknowledgement.

**Storage** `deliverydet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_delivery` | integer | Yes | — | References [delivery](commercial.md#record-delivery) (rowid). |
| `fk_origin_line` | integer | Yes | — | Line on the source document to which this fulfilment line corresponds. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_deliverydet.sql`, `htdocs/install/mysql/tables/llx_deliverydet.key.sql`, `htdocs/delivery/class/delivery.class.php:75`.

<a id="record-supplier_proposal"></a>

## Supplier price request

Represents a request to a supplier and the resulting commercial offer, its validity and decision.

**Storage** `supplier_proposal`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_supplier_proposal](categories.md#record-categorie_supplier_proposal) (fk_supplier_proposal), [supplier_proposaldet](commercial.md#record-supplier_proposaldet) (fk_supplier_proposal).

The record class defines `0` draft, `1` validated, `2` signed, `3` notsigned, `4` close. See `htdocs/supplier_proposal/class/supplier_proposal.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | `NULL` | Identifier supplied by an external application or interface. |
| `fk_soc` | integer | Yes | `NULL` | Third party associated with this record. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `date_valid` | datetime | Yes | `NULL` | When validation was recorded. |
| `date_cloture` | datetime | Yes | `NULL` | When the record was closed. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | `NULL` | Account that validated the record. |
| `fk_user_cloture` | integer | Yes | `NULL` | Account that recorded closure. |
| `fk_statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `price` | double | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `remise_percent` | double | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `remise_absolue` | double | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `remise` | double | Yes | `0` | Compatibility storage in this release. Use the current business representation described for the owning record. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `fk_account` | integer | Yes | `NULL` | Financial account identifier as used by the owning record. |
| `fk_currency` | varchar(3) | Yes | `NULL` | Currency identifier for this record. |
| `fk_cond_reglement` | integer | Yes | `NULL` | Terms governing settlement and due-date calculation. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `fk_mode_reglement` | integer | Yes | `NULL` | Payment method or instrument. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | `NULL` | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `date_livraison` | date | Yes | `NULL` | Delivery date retained on the originating record. |
| `fk_shipping_method` | integer | Yes | `NULL` | Selected dispatch or transport service. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | `NULL` | Additional values encoded for the owning feature. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |

Source locations include `htdocs/install/mysql/tables/llx_supplier_proposal.sql`, `htdocs/install/mysql/tables/llx_supplier_proposal.key.sql`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:65`.

<a id="record-supplier_proposaldet"></a>

## Supplier proposal line

Specifies the requested product, quantity and supplier-quoted terms on one offer.

**Storage** `supplier_proposaldet`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_supplier_proposal` | integer | No | — | Supplier price request identity. References [supplier_proposal](commercial.md#record-supplier_proposal) (rowid). |
| `fk_parent_line` | integer | Yes | `NULL` | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | `NULL` | Catalogue item associated with this entry. |
| `label` | varchar(255) | Yes | `NULL` | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_remise_except` | integer | Yes | `NULL` | Fixed credit or discount from which this row originated. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | `0` | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | `NULL` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | `NULL` | Calculation category for the corresponding additional tax component. |
| `qty` | double | Yes | `NULL` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | double | Yes | `'0'` | Percentage discount applied to the pricing base. |
| `remise` | double | Yes | `'0'` | Discount amount or pricing reduction in the owning record. |
| `price` | double | Yes | `NULL` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `buy_price_ht` | double(24,8) | Yes | `0` | Stored unit acquisition cost before tax, usable when computing a commercial margin. |
| `fk_product_fournisseur_price` | integer | Yes | `NULL` | Supplier price entry selected as the purchase-cost source. |
| `special_code` | integer | Yes | `0` | Special treatment for the document line, interpreted by the line-handling module. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `ref_fourn` | varchar(128) | Yes | `NULL` | Reference used by the supplier for the item. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_subprice` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_subprice_ttc` | double(24,8) | Yes | `0` | Document-currency unit price, respectively before or including tax. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_supplier_proposaldet.sql`, `htdocs/install/mysql/tables/llx_supplier_proposaldet.key.sql`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:70`.

<a id="record-commande_fournisseur"></a>

## Purchase order

Records what the organisation agreed to buy, its approval and dispatch history, receipt state and supplier billing classification.

**Storage** `commande_fournisseur`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_supplier_order](categories.md#record-categorie_supplier_order) (fk_supplier_order).

The record class defines `0` draft, `1` validated, `2` accepted, `3` ordersent, `4` received partially, `5` received completely, `6` canceled, `7` canceled after order, `9` refused. See `htdocs/fourn/class/fournisseur.commande.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(180) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_supplier` | varchar(255) | Yes | — | Reference assigned or communicated by the supplier. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `0` | Associated project identity. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `date_approve` | datetime | Yes | — | When approval was recorded. |
| `date_approve2` | datetime | Yes | — | Approving date (second approval). |
| `date_commande` | date | Yes | — | Order date. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `fk_user_approve` | integer | Yes | — | Account that recorded approval. |
| `fk_user_approve2` | integer | Yes | — | User for approval (second level). |
| `source` | smallint | No | — | Source. |
| `fk_statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `billed` | smallint | Yes | `0` | Billed classification tracked separately from physical delivery. |
| `amount_ht` | double(24,8) | Yes | `0` | Monetary amount before tax. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `localtax1` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `localtax2` | double(24,8) | Yes | `0` | Value of the corresponding local tax component on the record. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `date_livraison` | datetime | Yes | `NULL` | Delivery date retained on the originating record. |
| `date_reception` | datetime | Yes | `NULL` | Receipt date. |
| `fk_account` | integer | Yes | — | Financial account identifier as used by the owning record. |
| `fk_cond_reglement` | integer | Yes | — | Terms governing settlement and due-date calculation. |
| `deposit_percent` | varchar(63) | Yes | `NULL` | Deposit percentage applicable under these terms. |
| `fk_mode_reglement` | integer | Yes | — | Payment method or instrument. |
| `fk_input_method` | integer | Yes | `0` | Order method. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_total_ht` | double(24,8) | Yes | `0` | Document-currency total before tax. |
| `multicurrency_total_tva` | double(24,8) | Yes | `0` | VAT amount in document currency. |
| `multicurrency_total_ttc` | double(24,8) | Yes | `0` | Document-currency total including tax. |

Source locations include `htdocs/install/mysql/tables/llx_commande_fournisseur.sql`, `htdocs/install/mysql/tables/llx_commande_fournisseur.key.sql`, `htdocs/fourn/class/fournisseur.class.php:88`.

<a id="record-commande_fournisseurdet"></a>

## Purchase order line

Identifies one purchased product or service and its price, quantity, supplier reference and tax totals.

**Storage** `commande_fournisseurdet`.
The primary key is `rowid`.

**Referenced by** [commandedet](commercial.md#record-commandedet) (fk_commandefourndet).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_commande` | integer | No | — | Customer order identity. |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `ref` | varchar(128) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `vat_src_code` | varchar(10) | Yes | empty string | VAT code paired with a percentage to retain its tax treatment. |
| `tva_tx` | double(7,4) | Yes | `0` | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | Yes | — | Calculation category for the corresponding additional tax component. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | real | Yes | `0` | Percentage discount applied to the pricing base. |
| `remise` | real | Yes | `0` | Discount amount or pricing reduction in the owning record. |
| `subprice` | double(24,8) | Yes | `0` | Unit price used in the net-price representation of a transaction line. |
| `subprice_ttc` | double(24,8) | Yes | `0` | Tax-inclusive unit price for the line. |
| `total_ht` | double(24,8) | Yes | `0` | Total before tax in base currency after applicable line adjustments. |
| `total_tva` | double(24,8) | Yes | `0` | VAT component of the base-currency total. |
| `total_localtax1` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_localtax2` | double(24,8) | Yes | `0` | Aggregated amount of the corresponding additional tax component. |
| `total_ttc` | double(24,8) | Yes | `0` | Total including tax in base currency. |
| `product_type` | integer | Yes | `0` | Product, service or special-line classification used by the owning document. |
| `date_start` | datetime | Yes | `NULL` | Beginning of the applicable period. |
| `date_end` | datetime | Yes | `NULL` | End of the applicable period. |
| `info_bits` | integer | Yes | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
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

Source locations include `htdocs/install/mysql/tables/llx_commande_fournisseurdet.sql`, `htdocs/install/mysql/tables/llx_commande_fournisseurdet.key.sql`, `htdocs/reception/class/reception.class.php:706`.

<a id="record-reception"></a>

## Goods receipt

Records an incoming supplier delivery and its validation state, supplier, reference and shipment information.

**Storage** `reception`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [receptiondet_batch](commercial.md#record-receptiondet_batch) (fk_reception).

The record class defines `-1` canceled, `0` draft, `1` validated, `2` closed. See `htdocs/reception/class/reception.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `ref_ext` | varchar(30) | Yes | — | Identifier supplied by an external application or interface. |
| `ref_supplier` | varchar(255) | Yes | — | Reference assigned or communicated by the supplier. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `date_delivery` | datetime | Yes | `NULL` | Delivery date retained on the originating record. |
| `date_reception` | datetime | Yes | — | Receipt date. |
| `fk_shipping_method` | integer | Yes | — | Selected dispatch or transport service. References [c_shipment_mode](dictionaries.md#record-c_shipment_mode) (rowid). |
| `tracking_number` | varchar(50) | Yes | — | Carrier's shipment-tracking identifier. |
| `fk_statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `billed` | smallint | Yes | `0` | Billed classification tracked separately from physical delivery. |
| `height` | float | Yes | — | Physical horizontal or vertical dimension, respectively. |
| `width` | float | Yes | — | Physical horizontal or vertical dimension, respectively. |
| `size_units` | integer | Yes | — | Unit or scale used for the associated dimensions. |
| `size` | float | Yes | — | Size or depth in the relevant physical unit. |
| `weight_units` | integer | Yes | — | Unit or scale used to interpret the associated weight. |
| `weight` | float | Yes | — | Physical weight in the associated unit. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_reception.sql`, `htdocs/install/mysql/tables/llx_reception.key.sql`, `htdocs/reception/class/reception.class.php:82`.

<a id="record-receptiondet_batch"></a>

## Supplier receipt allocation

Records a quantity received against a supplier order line, with warehouse and any lot information. Several splits can refer to one purchase line.

**Storage** `receptiondet_batch`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_reception` | integer | Yes | `NULL` | References [reception](commercial.md#record-reception) (rowid). |
| `fk_element` | integer | Yes | — | Supplier order line from which this received quantity originates. |
| `fk_elementdet` | integer | Yes | — | Related detail-line identity. |
| `element_type` | varchar(50) | No | `'supplier_order'` | Type discriminator identifying the class of associated object. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `qty` | float | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_unit` | integer | Yes | — | Unit of measure associated with the quantity. |
| `fk_entrepot` | integer | Yes | — | Warehouse or stock location. |
| `fk_projet` | integer | Yes | `NULL` | Associated project identity. |
| `comment` | varchar(255) | Yes | — | Free-text annotation retained with the record. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `eatby` | date | Yes | `NULL` | Use-by date associated with a lot. |
| `sellby` | date | Yes | `NULL` | Sell-by date associated with a lot. |
| `status` | integer | Yes | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `cost_price` | double(24,8) | Yes | `0` | Stored cost price used by the applicable cost and margin policy. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_receptiondet_batch.sql`, `htdocs/install/mysql/tables/llx_receptiondet_batch.key.sql`, `htdocs/reception/class/reception.class.php:87`.
