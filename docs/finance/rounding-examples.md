# Invoice rounding in the ledger currency

The choice of rounding level affects both the customer balance and the amount credited to the tax account. The following amounts use two decimal places. Each example uses a single tax rate, no local taxes and no currency conversion.

| Terms | Calculation | Net | Tax | Gross |
| --- | --- | ---: | ---: | ---: |
| Three units at 20.00 before tax, 10% discount, 15% VAT | The discount is 6.00 on the 60.00 extension. Apply the tax to 54.00. | 54.00 | 8.10 | 62.10 |
| Two separate lines at 0.03 before tax, 20% VAT, round each line | Each line has an unrounded tax of 0.006 and a rounded tax of 0.01. | 0.06 | 0.02 | 0.08 |
| The same two lines, tax rounded by rate on the document | The tax group has 0.012 tax before rounding. The stored lines must reconcile to 0.01 in that group. | 0.06 | 0.01 | 0.07 |
| Two units at 11.50 including 15% VAT | The 23.00 extended gross includes 3.00 of tax. | 20.00 | 3.00 | 23.00 |

In the two-line example the economic price and statutory rate are identical. The one-cent difference arises solely from the configured aggregation level. Carry the rate, taxable base, rounded components and document precision through to posting. If the invoice is presented in two currencies, distinguish each currency's amounts throughout the calculation. See [customer invoice calculations](customer-invoices.md) and [geographic and local tax rules](../additional-domains/tax-geography-and-rounding.md).
