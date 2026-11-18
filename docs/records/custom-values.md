# Configured property values

Each extension record belongs to one owning business object through `fk_object`. Its own generated ID identifies the extension row. Field definitions describe the configured properties. Their values occupy additional columns created in the appropriate extension table. The base installation declares the four common fields shown below. An installation with custom properties will have more columns.

A required or unique custom property is governed by its definition and the field-creation path. A unique key on the parent ID determines whether the physical store permits more than one extension row per owner. A reference to a polymorphic or dynamically resolved owner requires an application lookup where a database foreign key is absent.

[All record families](README.md)

## Base layouts

### Layout 1

Used by 79 extension records.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_object` | integer | No | — | Identifier of the business record holding these values. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

### Layout 2

Used by 2 extension records.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_object` | integer | No | — | Identifier of the business record holding these values. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

## Owner and constraint map

A unique owner key limits a parent to one extension row. An application association identifies a logical owner whose existence is checked by business operations.

| Extension table | Owner | Layout | Unique owner key | Declared owner reference |
| --- | --- | ---: | --- | --- |
| <a id="record-actioncomm_extrafields"></a>`actioncomm_extrafields` | [actioncomm](production.md#record-actioncomm) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-adherent_extrafields"></a>`adherent_extrafields` | [adherent](people.md#record-adherent) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-adherent_type_extrafields"></a>`adherent_type_extrafields` | [adherent_type](people.md#record-adherent_type) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-asset_extrafields"></a>`asset_extrafields` | [asset](accounting.md#record-asset) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-asset_model_extrafields"></a>`asset_model_extrafields` | [asset_model](accounting.md#record-asset_model) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-bank_account_extrafields"></a>`bank_account_extrafields` | [bank_account](cash.md#record-bank_account) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-bank_extrafields"></a>`bank_extrafields` | [bank](cash.md#record-bank) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-bom_bom_extrafields"></a>`bom_bom_extrafields` | [bom_bom](production.md#record-bom_bom) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-bom_bomline_extrafields"></a>`bom_bomline_extrafields` | [bom_bomline](production.md#record-bom_bomline) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-categorie_lang_extrafields"></a>`categorie_lang_extrafields` | [categorie_lang](categories.md#record-categorie_lang) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-categories_extrafields"></a>`categories_extrafields` | [categorie](categories.md#record-categorie) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-commande_extrafields"></a>`commande_extrafields` | [commande](commercial.md#record-commande) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-commande_fournisseur_extrafields"></a>`commande_fournisseur_extrafields` | [commande_fournisseur](commercial.md#record-commande_fournisseur) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-commande_fournisseurdet_extrafields"></a>`commande_fournisseurdet_extrafields` | [commande_fournisseurdet](commercial.md#record-commande_fournisseurdet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-commandedet_extrafields"></a>`commandedet_extrafields` | [commandedet](commercial.md#record-commandedet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-contrat_extrafields"></a>`contrat_extrafields` | [contrat](people.md#record-contrat) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-contratdet_extrafields"></a>`contratdet_extrafields` | [contratdet](people.md#record-contratdet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-delivery_extrafields"></a>`delivery_extrafields` | [delivery](commercial.md#record-delivery) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-deliverydet_extrafields"></a>`deliverydet_extrafields` | [deliverydet](commercial.md#record-deliverydet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-don_extrafields"></a>`don_extrafields` | [don](people.md#record-don) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-ecm_directories_extrafields"></a>`ecm_directories_extrafields` | [ecm_directories](content.md#record-ecm_directories) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-ecm_files_extrafields"></a>`ecm_files_extrafields` | [ecm_files](content.md#record-ecm_files) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-entrepot_extrafields"></a>`entrepot_extrafields` | [entrepot](warehouse.md#record-entrepot) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-eventorganization_conferenceorboothattendee_extrafields"></a>`eventorganization_conferenceorboothattendee_extrafields` | [eventorganization_conferenceorboothattendee](production.md#record-eventorganization_conferenceorboothattendee) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-expedition_extrafields"></a>`expedition_extrafields` | [expedition](commercial.md#record-expedition) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-expeditiondet_extrafields"></a>`expeditiondet_extrafields` | [expeditiondet](commercial.md#record-expeditiondet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-expensereport_det_extrafields"></a>`expensereport_det_extrafields` | [expensereport_det](people.md#record-expensereport_det) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-expensereport_extrafields"></a>`expensereport_extrafields` | [expensereport](people.md#record-expensereport) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facture_extrafields"></a>`facture_extrafields` | [facture](billing.md#record-facture) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facture_fourn_det_extrafields"></a>`facture_fourn_det_extrafields` | [facture_fourn_det](billing.md#record-facture_fourn_det) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facture_fourn_det_rec_extrafields"></a>`facture_fourn_det_rec_extrafields` | [facture_fourn_det_rec](billing.md#record-facture_fourn_det_rec) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-facture_fourn_extrafields"></a>`facture_fourn_extrafields` | [facture_fourn](billing.md#record-facture_fourn) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facture_fourn_rec_extrafields"></a>`facture_fourn_rec_extrafields` | [facture_fourn_rec](billing.md#record-facture_fourn_rec) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facture_rec_extrafields"></a>`facture_rec_extrafields` | [facture_rec](billing.md#record-facture_rec) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facturedet_extrafields"></a>`facturedet_extrafields` | [facturedet](billing.md#record-facturedet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-facturedet_rec_extrafields"></a>`facturedet_rec_extrafields` | [facturedet_rec](billing.md#record-facturedet_rec) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-fichinter_extrafields"></a>`fichinter_extrafields` | [fichinter](people.md#record-fichinter) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-fichinterdet_extrafields"></a>`fichinterdet_extrafields` | [fichinterdet](people.md#record-fichinterdet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-holiday_extrafields"></a>`holiday_extrafields` | [holiday](people.md#record-holiday) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-hrm_evaluation_extrafields"></a>`hrm_evaluation_extrafields` | [hrm_evaluation](people.md#record-hrm_evaluation) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-hrm_evaluationdet_extrafields"></a>`hrm_evaluationdet_extrafields` | [hrm_evaluationdet](people.md#record-hrm_evaluationdet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-hrm_job_extrafields"></a>`hrm_job_extrafields` | [hrm_job](people.md#record-hrm_job) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-hrm_skill_extrafields"></a>`hrm_skill_extrafields` | [hrm_skill](people.md#record-hrm_skill) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-inventory_extrafields"></a>`inventory_extrafields` | [inventory](warehouse.md#record-inventory) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-knowledgemanagement_knowledgerecord_extrafields"></a>`knowledgemanagement_knowledgerecord_extrafields` | [knowledgemanagement_knowledgerecord](people.md#record-knowledgemanagement_knowledgerecord) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-mrp_mo_extrafields"></a>`mrp_mo_extrafields` | [mrp_mo](production.md#record-mrp_mo) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-mrp_production_extrafields"></a>`mrp_production_extrafields` | [mrp_production](production.md#record-mrp_production) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-paiement_extrafields"></a>`paiement_extrafields` | [paiement](cash.md#record-paiement) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-partnership_extrafields"></a>`partnership_extrafields` | [partnership](parties.md#record-partnership) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-payment_various_extrafields"></a>`payment_various_extrafields` | [payment_various](cash.md#record-payment_various) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-pos_cash_fence_extrafields"></a>`pos_cash_fence_extrafields` | [pos_cash_fence](cash.md#record-pos_cash_fence) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-product_attribute_extrafields"></a>`product_attribute_extrafields` | [product_attribute](catalogue.md#record-product_attribute) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-product_attribute_value_extrafields"></a>`product_attribute_value_extrafields` | [product_attribute_value](catalogue.md#record-product_attribute_value) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-product_customer_price_extrafields"></a>`product_customer_price_extrafields` | [product_customer_price](catalogue.md#record-product_customer_price) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-product_extrafields"></a>`product_extrafields` | [product](catalogue.md#record-product) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-product_fournisseur_price_extrafields"></a>`product_fournisseur_price_extrafields` | [product_fournisseur_price](catalogue.md#record-product_fournisseur_price) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-product_lang_extrafields"></a>`product_lang_extrafields` | [product_lang](catalogue.md#record-product_lang) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-product_lot_extrafields"></a>`product_lot_extrafields` | [product_lot](warehouse.md#record-product_lot) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-product_price_extrafields"></a>`product_price_extrafields` | [product_price](catalogue.md#record-product_price) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-projet_extrafields"></a>`projet_extrafields` | [projet](production.md#record-projet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-projet_task_extrafields"></a>`projet_task_extrafields` | [projet_task](production.md#record-projet_task) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-propal_extrafields"></a>`propal_extrafields` | [propal](commercial.md#record-propal) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-propaldet_extrafields"></a>`propaldet_extrafields` | [propaldet](commercial.md#record-propaldet) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-reception_extrafields"></a>`reception_extrafields` | [reception](commercial.md#record-reception) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-receptiondet_batch_extrafields"></a>`receptiondet_batch_extrafields` | [receptiondet_batch](commercial.md#record-receptiondet_batch) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-recruitment_recruitmentcandidature_extrafields"></a>`recruitment_recruitmentcandidature_extrafields` | [recruitment_recruitmentcandidature](people.md#record-recruitment_recruitmentcandidature) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-recruitment_recruitmentjobposition_extrafields"></a>`recruitment_recruitmentjobposition_extrafields` | [recruitment_recruitmentjobposition](people.md#record-recruitment_recruitmentjobposition) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-resource_extrafields"></a>`resource_extrafields` | [resource](production.md#record-resource) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-salary_extrafields"></a>`salary_extrafields` | [salary](people.md#record-salary) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-societe_extrafields"></a>`societe_extrafields` | [societe](parties.md#record-societe) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-socpeople_extrafields"></a>`socpeople_extrafields` | [socpeople](parties.md#record-socpeople) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-stock_mouvement_extrafields"></a>`stock_mouvement_extrafields` | [stock_mouvement](warehouse.md#record-stock_mouvement) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-stocktransfer_stocktransfer_extrafields"></a>`stocktransfer_stocktransfer_extrafields` | [stocktransfer_stocktransfer](warehouse.md#record-stocktransfer_stocktransfer) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-stocktransfer_stocktransferline_extrafields"></a>`stocktransfer_stocktransferline_extrafields` | [stocktransfer_stocktransferline](warehouse.md#record-stocktransfer_stocktransferline) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-supplier_proposal_extrafields"></a>`supplier_proposal_extrafields` | [supplier_proposal](commercial.md#record-supplier_proposal) | [Layout 2](#layout-2) | Yes | Application association |
| <a id="record-supplier_proposaldet_extrafields"></a>`supplier_proposaldet_extrafields` | [supplier_proposaldet](commercial.md#record-supplier_proposaldet) | [Layout 2](#layout-2) | Yes | Application association |
| <a id="record-ticket_extrafields"></a>`ticket_extrafields` | [ticket](people.md#record-ticket) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-user_extrafields"></a>`user_extrafields` | [user](foundation.md#record-user) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-usergroup_extrafields"></a>`usergroup_extrafields` | [usergroup](foundation.md#record-usergroup) | [Layout 1](#layout-1) | Yes | Application association |
| <a id="record-website_extrafields"></a>`website_extrafields` | [website](content.md#record-website) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
| <a id="record-workstation_workstation_extrafields"></a>`workstation_workstation_extrafields` | [workstation_workstation](production.md#record-workstation_workstation) | [Layout 1](#layout-1) | No unique owner key declared | Application association |
