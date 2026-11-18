# Country reference data and financial localization

A country record lets an operator specify where a party is established. An accounting model supplies named accounts and their hierarchy. A tax dictionary supplies selectable rates and tax components. A report definition determines which ledger movements contribute to a named result. Each has its own key and lookup rules. Setting the company's country alone does not populate all four.

| Question | Reference |
| --- | --- |
| Which chart models ship, how many accounts do they describe, and which account types feed the income and expense report? | [Chart models and report assignments](chart-models-and-reports.md) and [complete chart inventory](chart-models.csv) |
| Which country and rate combinations ship, and how does the ERP choose among them? | [Tax selection, supplementary taxes and geographic exceptions](tax-selection.md) and [complete tax rate inventory](tax-rates.csv) |
| When does tax enter the report and what happens when it is remitted? | [Tax recognition and remittance](../specification/accounting/tax-recognition-and-remittance.md) |
| How are period totals, calculated report rows and account assignments resolved? | [Financial statements and analytical dimensions](../specification/accounting/financial-statements-and-analytic-dimensions.md) |

These inventories describe the installation data and selection logic of release 24.0.3. Counts include inactive definitions where indicated. Values introduced by an installation, its extensions or its own chart administration are outside the counts.

## Namibia

The country dictionary supplies the active two-letter code `NA`, three-letter code `NAM` and internal country identifier `161`. The currency dictionary separately supplies the active code `NAD`. These two entries support country and currency identification. The chart registry has no Namibian model and the country chart directory contains no Namibian account file. The VAT, revenue-stamp and environmental-charge dictionaries contain no entries for country 161. The personalized financial report supplied to all countries has no Namibia-specific categories or seeded account assignments.

For a domestic Namibian sale with a taxable seller, no product or departmental override, and ordinary country fallback, the country lookup finds no seeded VAT row. The helper retains its initial numeric zero. This outcome describes a failed default lookup and cannot establish the tax treatment of that sale. A configured product rate, installation-specific dictionary or explicit fallback can change the result. Similarly, selecting NAD has no effect on chart or report membership. A local chart requires an accounting model and account definitions, while a custom statement needs its report categories and account assignments.

Release references include `htdocs/install/mysql/data/llx_00_c_country.sql:190`, `htdocs/install/mysql/data/llx_c_currencies.sql:125`, `htdocs/install/mysql/data/llx_accounting_system.sql:52–187`, `htdocs/install/mysql/data/llx_accounting_category-accounting.sql:20–25` and `htdocs/core/lib/functions.lib.php:8368–8449,8618–8644`.
