# Installation definitions outside the functional model

The installation directory includes tables for disabled features, optional external modules and structures whose operational use still needs direct evidence. Keeping them visible here allows a maintainer to identify a physical table without assigning a business workflow to it.

## Feature and extension exclusions

| Installation file | Reason |
| --- | --- |
| `llx_bookcal_availabilities-bookcal.sql` | Experimental booking-calendar module. |
| `llx_bookcal_availabilities_extrafields-bookcal.sql` | Experimental booking-calendar module. |
| `llx_bookcal_calendar-bookcal.sql` | Experimental booking-calendar module. |
| `llx_bookcal_calendar_extrafields-bookcal.sql` | Experimental booking-calendar module. |
| `llx_budget-budget.sql` | No budgets descriptor in this core release. |
| `llx_budget_lines-budget.sql` | No budgets descriptor in this core release. |
| `llx_c_price_expression-dynamicprices.sql` | Experimental formula pricing module. |
| `llx_c_price_global_variable-dynamicprices.sql` | Experimental formula pricing module. |
| `llx_c_price_global_variable_updater-dynamicprices.sql` | Experimental formula pricing module. |
| `llx_deplacement-deplacement.sql` | Retired travel-expense structure outside the expense claim workflow. |
| `llx_intracommreport-intracommreport.sql` | Development-stage reporting module. |
| `llx_product_perentity-multicompany.sql` | Separate multi-entity extension schema. |
| `llx_quickmemo_memo-quickmemo.sql` | Experimental shared memo module. |
| `llx_quickmemo_memo_extrafields-quickmemo.sql` | Experimental shared memo module. |
| `llx_quickmemo_memo_user-quickmemo.sql` | Experimental shared memo module. |
| `llx_session-disabled.sql` | Installer-disabled table family. |
| `llx_societe_perentity-multicompany.sql` | Separate multi-entity extension schema. |
| `llx_zapier_hook-zapier.sql` | Experimental connector. |

## Operational use unresolved or separately gated

These rows have installation declarations but no confirmed stable operational writer or reader for the named table in this inventory. A generic class, a migration, a commented reference or a similarly named screen does not establish its use. A later investigation can add an entry after tracing the actual storage path under a supported configuration.

| Record | Declared purpose or open question | Installation file |
| --- | --- | --- |
| `accounting_analytic_account` | Analytic account definition. | `llx_accounting_analytic_account-accounting.sql` |
| `accounting_analytic_axis` | Analytic reporting axis. | `llx_accounting_analytic_axis-accounting.sql` |
| `accounting_analytic_distribution` | Allocation of a source line to an analytic account. | `llx_accounting_analytic_distribution-accounting.sql` |
| `accounting_balance_snapshot` | Dated account-balance snapshot. | `llx_accounting_balance_snapshot-accounting.sql` |
| `accounting_bookkeeping_piece` | Standalone journal-piece header. | `llx_accounting_bookkeeping_piece-accounting.sql` |
| `accounting_groups_account` | Account grouping with code and label. | `llx_accounting_groups_account.sql` |
| `ai_request_log` | Logging table for assistant requests. The presence of this schema does not establish a stable end-user workflow for the assistant feature. | `llx_ai_request_log-ai.sql` |
| `bank_import` | Bank import batch. | `llx_bank_import-bank.sql` |
| `bank_record` | Bank statement header. | `llx_bank_record-bank.sql` |
| `bank_record_link` | Statement-to-movement association. | `llx_bank_record_link-bank.sql` |
| `c_product_thirdparty_relation_type` | Dictionary for product/party relationship kinds. | `llx_c_product_thirdparty_relation_type.sql` |
| `c_recruitment_origin` | Dictionary for application origins. The application field is present, while its form declaration is commented out. | `llx_c_recruitment_origin-recruitment.sql` |
| `commande_fournisseur_log` | Dedicated supplier-order action log. | `llx_commande_fournisseur_log.sql` |
| `element_categorie` | Generic element/category association. Current classification also uses object-specific association tables. | `llx_element_categorie.sql` |
| `expedition_package` | Dedicated shipment package header. Package types have a separate dictionary. | `llx_expedition_package.sql` |
| `notify_def_object` | Object-specific notification declaration. | `llx_notify_def_object.sql` |
| `oauth_state` | Standalone provider state table. The observed database adapter reads and writes its state on the token row. | `llx_oauth_state.sql` |
| `onlinesignature` | Standalone signature submission store. Signature processing also sets fields on commercial documents. | `llx_onlinesignature.sql` |
| `opensurvey_formquestions` | Survey questionnaire field definitions. | `llx_opensurvey_formquestions-opensurvey.sql` |
| `opensurvey_user_formanswers` | Answers for structured questionnaire fields. | `llx_opensurvey_user_formanswers-opensurvey.sql` |
| `paymentexpensereport_expensereport` | General-purpose expense payment allocation bridge. The payment table separately identifies its claim. | `llx_paymentexpensereport_expensereport.sql` |
| `product_thirdparty` | Generic third-party product relationship. | `llx_product_thirdparty.sql` |
| `user_employment` | Dated employment history. Employment information also appears on the user account. | `llx_user_employment.sql` |

[All record families](README.md)
