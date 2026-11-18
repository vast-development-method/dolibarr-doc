# Installation and operating roles

These 41 physical definitions cover feature-specific stores, reserved structures, a retired state store and a diagnostic log. Each has a field and key definition in the [relational model](../relational-model/README.md). Its operating role determines when an installation or a business action actually writes rows.

## Feature and extension exclusions

| Table | Reason |
| --- | --- |
| `bookcal_availabilities` | Experimental booking-calendar module. |
| `bookcal_availabilities_extrafields` | Experimental booking-calendar module. |
| `bookcal_calendar` | Experimental booking-calendar module. |
| `bookcal_calendar_extrafields` | Experimental booking-calendar module. |
| `budget` | Budget schema reserved for a separately provided feature. |
| `budget_lines` | Budget schema reserved for a separately provided feature. |
| `c_price_expression` | Experimental formula pricing module. |
| `c_price_global_variable` | Experimental formula pricing module. |
| `c_price_global_variable_updater` | Experimental formula pricing module. |
| `deplacement` | Retired travel-expense structure outside the expense claim workflow. |
| `intracommreport` | Development-stage reporting module. |
| `product_perentity` | Separate multi-entity extension schema. |
| `quickmemo_memo` | Experimental shared memo module. |
| `quickmemo_memo_extrafields` | Experimental shared memo module. |
| `quickmemo_memo_user` | Experimental shared memo module. |
| `session` | Installer-disabled table family. |
| `societe_perentity` | Separate multi-entity extension schema. |
| `zapier_hook` | Experimental connector. |

## Reserved structures, retired state and diagnostic logging

The [operation-by-operation register](operational-evidence.md) classifies all 23 definitions and identifies which active records each business action uses. Twenty-one are schema-only in the standard business workflows. One stores diagnostic requests when enabled. One is a retired authorization-state table.

| Record | Stored concept and operating role |
| --- | --- |
| `accounting_analytic_account` | Analytic account definition. |
| `accounting_analytic_axis` | Analytic reporting axis. |
| `accounting_analytic_distribution` | Allocation of a source line to an analytic account. |
| `accounting_balance_snapshot` | Dated account-balance snapshot. |
| `accounting_bookkeeping_piece` | Standalone journal-piece header. |
| `accounting_groups_account` | Bridge joining a ledger account ID to a reporting category ID. |
| `ai_request_log` | Request log with confirmed gated writers, an administrative viewer and a retention purge. |
| `bank_import` | One imported bank transaction with source data and a potential duplicate reference. |
| `bank_record` | Bank statement header. |
| `bank_record_link` | Association between a statement header and an imported source transaction. |
| `c_product_thirdparty_relation_type` | Dictionary for product/party relationship kinds. |
| `c_recruitment_origin` | Dictionary for application origins. The application holds an optional field. Its standard editor omits the origin selector. |
| `commande_fournisseur_log` | Dedicated supplier-order action log. |
| `element_categorie` | Generic element/category association. Current classification also uses object-specific association tables. |
| `expedition_package` | Dedicated shipment package header. Package types have a separate dictionary. |
| `notify_def_object` | Object-specific notification declaration. |
| `oauth_state` | Deprecated standalone provider state table. The current database adapter reads and writes state on the token row. |
| `onlinesignature` | Standalone signature submission store. Signature processing also sets fields on commercial documents. |
| `opensurvey_formquestions` | Survey questionnaire field definitions. |
| `opensurvey_user_formanswers` | Answers for structured questionnaire fields. |
| `paymentexpensereport_expensereport` | General-purpose expense payment allocation bridge. The payment table separately identifies its claim. |
| `product_thirdparty` | Generic third-party product relationship. |
| `user_employment` | Dated employment history. Employment information also appears on the user account. |

[All record families](README.md)
