# Geography, tax defaults and monetary rounding

The tax default is an operational suggestion produced from the parties, product, dictionary and instance settings. The invoice line stores the chosen rate and code. Separate steps calculate line amounts, accumulate document totals and settle tax obligations. This chapter follows the software's rules in 24.0.3. [Line calculations](../finance/customer-invoices.md) · [VAT remittance](../treasury/bank-and-obligations.md)

## Reference data

| Record | Key facts |
| --- | --- |
| Country | Two-letter code, three-letter and numeric codes, active flag and European Community membership indicator. Dolibarr's membership check uses its country-code list. |
| Region and department/state | A region belongs to a country. A department can point to a region. A buyer's department ID can qualify a VAT default. Country names translated for display are unsuitable as join keys. |
| VAT dictionary row | Entity, country, VAT code, main percentage, sale/purchase/all indicator, default and active flags, recoverable-only indicator, optional buyer department, selling and purchasing account codes and two local-tax specifications. The upstream unique key uses entity, country, code, rate and recoverable-only flag. The local rates have separate applicability types. |
| Authorisation | The general dictionary screen admits administrators. Users with the chart-of-accounts permission also have access to the VAT, social-charge and expense-fee-type dictionaries. This exception does not grant general access to all dictionaries. |

[Country fields](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_c_country.sql) · [Geography lookup](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/company.lib.php#L901-L948) · [Tax dictionary](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_c_tva.sql) · [VAT identity](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_c_tva.key.sql) · [Dictionary permissions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/admin/dict.php#L149-L165)

## Rate selection

The default resolver first substitutes the configured organisation country for a missing seller or buyer country and determines each party's Community membership. Its ordered cases include the following.

1. A configured electronic-commerce option tests Community membership and the buyer's company/VAT-ID status. A qualifying private-buyer case selects product VAT for the buyer's country before the following rules run.
2. If no earlier rule determined the result, a seller outside the VAT regime supplies zero. Otherwise an active department-specific row for the buyer can take precedence over the product default. Among competing rows sort by default flag descending, rate descending, code ascending and recoverable-only ascending.
3. For the same country, or explicitly grouped territories, resolve the product VAT in the seller's country. A configured Indian split/combined-code branch also checks whether the parties' states match. For a product in the organisation's country, the lookup can use its sales rate/code or a specific supplier price's VAT details. The fallback country lookup chooses an active row using the same default-first ordering.
4. For different countries both in the Community, the remaining branch distinguishes a company buyer passing the configured VAT-ID rule from other buyers. The former receives zero, the latter the seller-country product rate. A separate option can apply a product rate to private buyers outside the Community. The residual default is zero. The source comments describe a transport-specific rule but omit its implementation, so this release adds no special automatic transport branch. A hook can override a proposed value.

[Country/product resolution](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L8369-L8444) · [Ordered default rules](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L8539-L8701)

**Acceptance.** In a domestic test with e-commerce override off and a VAT-registered seller, set product VAT to 10%. Configure two active rates for the buyer department, 7% marked default and 12% unmarked. The assigned suggestion is 7% with its dictionary code. Deactivate the two department rows and the 10% product default can be selected. Mark the seller outside the VAT regime and the default becomes zero, ahead of the department lookup. These rates exercise decision order.

## Local-tax applicability

Either local-tax slot can be configured independently. The six applicability types implement two bases and three sets of line types. The actual local rate also depends on the buyer, seller and local-tax settings. Preserve the rate code alongside the percentage when several dictionary rows have the same percentage. [Rate lookup](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L8305-L8355) · [Tax-on-gross branches](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/price.lib.php#L243-L297) · [Tax-on-net branches](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/price.lib.php#L336-L389)

| Type codes | Applies to | Base for odd code | Base for even code |
| --- | --- | --- | --- |
| 1 / 2 | Products and services | Excluding main VAT | Including main VAT |
| 3 / 4 | Products | Excluding main VAT | Including main VAT |
| 5 / 6 | Services | Excluding main VAT | Including main VAT |

For a discounted net line of 100.00, 10% main VAT and one applicable 5% local tax, type 1 produces 5.00 local tax; type 2 produces 5.50. Type 3 on a service produces zero. Test each component before checking the total.

## Rounding and reconciliation

The amount normaliser distinguishes unit, total, stock and currency-unit precision. Parse localized numeric input at the input boundary; preserve numeric values and the applicable rounding policy in calculations. When `MAIN_ROUNDING_RULE_TOT` sets an increment, the pricing engine rounds the relevant line components to that increment. On a tax-exclusive input line, it rounds net, VAT and both local taxes individually and recomputes gross. On a tax-inclusive line it rounds gross, VAT and local taxes, then derives net. [Precision categories](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L7917-L7949) · [Increment rounding](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/price.lib.php#L390-L409)

The ordinary automatic document mode totals rounded lines. An enabled rounding-of-total mode compares cumulative VAT for each rate against the tax on cumulative net (or tax extracted from cumulative gross) and can adjust the current line by the difference. A discrepancy greater than ten times the monetary quantum is rejected on that path. Expense reports explicitly force line rounding. The cumulative correction path is implemented for company currency, so retain separately computed foreign-currency amounts when reconciling. [Document settings](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/class/commonobject.class.php#L4091-L4159) · [Per-rate adjustment](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/class/commonobject.class.php#L4286-L4337)

**Acceptance.** With two invoice lines of 0.03 net at 20%, two decimal places and no rounding increment, each line independently yields 0.01 VAT, giving 0.02 under line rounding. Under cumulative rounding of that rate, 0.06 × 20% = 0.012 rounds to 0.01, so the second line corrects the cumulative VAT by 0.01. Both lines still sum to 0.06 net and the document gross is 0.07. Repeat at different VAT rates to verify that one rate's difference is never assigned to another rate's group.
