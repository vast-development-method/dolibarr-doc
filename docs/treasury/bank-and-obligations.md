# Bank transfers, exchange rates and operating payments

## Move money between owned accounts

The transfer entry screen requires bank-transfer permission, different source and destination accounts, payment type, date, description and amount. With equal account currencies the received amount is set equal to the sent amount. With different currencies the destination amount is supplied explicitly. If either endpoint is a cash account, the movement code becomes cash. The handler creates two bank rows, negative from the sender and positive to the receiver, and links each row to the other. It wraps all submitted rows in a database transaction. A failed second leg or link aborts the submitted batch. In the bank journal each leg uses a transfer clearing account. [Transfer workflow][transfer] · [Journal mapping][journal]

**TR-BNK-01.** Company currency EUR, transfer EUR 500.00 into a USD account that receives USD 550.00. Expect bank lines of −500.00 EUR and +550.00 USD. The destination foreign-currency line also carries +500.00 in company currency. A transfer between two EUR accounts uses the same magnitude on each side. The source invoices, if any, retain their outstanding balances. **TR-BNK-02.** Select the same account twice, or omit received amount for different currencies. The transfer fails before a valid pair can commit. [Transfer amount and linkage][transfer]

## Select a currency rate

Retain company currency, transaction currency, unit prices and totals in both, the applied rate and the relevant date. In the general currency lookup, the latest known rate is selected by synchronization time. With `MULTICURRENCY_USE_RATE_ON_DOCUMENT_DATE` enabled and a document date provided, use the latest eligible rate through the end of that date. If the dated lookup yields no row, the helper retries without the cutoff. If neither lookup succeeds, the returned missing identifier and rate 1 allow the invoice creation path to fall back to company currency. An explicitly supplied invoice rate on a recognised currency is retained. A payment at the full foreign residual can consume the exact company residual. [Rate history lookup][rates] · [Invoice currency resolution][invoice] · [Foreign settlement](../finance/collections.md)

**TR-FX-01.** A currency has rates 1.10 on 1 October and 1.12 on 1 November. For a 15 October invoice with no explicit rate, dated lookup yields 1.10. Current lookup yields 1.12. For a document predating both rows, the dated lookup's retry can return 1.12. Persist the rate actually applied so a later report can reproduce the invoice.

## Pay liabilities

| Operation | Source and access | Settlement and observable effect |
| --- | --- | --- |
| Salary | Salary is an amount owed to an employee for the recorded period, with an optional project. The payment screen allows the all-salaries reader, or a salary reader when the employee belongs to that user's permitted hierarchy. Writing a payment also requires salary-write permission. | Post dated, method-specific salary payment and its bank outflow if banking is enabled. With automatic close selected, mark the obligation paid when rounded salary amount minus recorded payments reaches zero. |
| Social contribution | Keep the contribution type, amount, due date, period, project and payee/employee link where applicable. The payment action checks tax/charges create permission. | Record payment against its contribution, bank outflow under social-contribution payment, and optional close after full settlement. |
| VAT obligation | The tax record stores the booked amount, date and account. This is a tax payable record distinct from the VAT component on any individual sales invoice. The payment action checks tax/charges create permission. | Record the dated VAT payment and optional bank outflow. With automatic close enabled, paid status follows the outstanding amount at total precision. The payment uses the amount booked on the tax record. |
| Miscellaneous payment | For a cash movement without a customer invoice or one of these liabilities, a bank editor supplies a label, direction, positive amount, payment/value dates, mode and account. When advanced accounting is enabled, the form requires an accounting account and checks whether the account accepts an auxiliary account. | Direction determines inflow or outflow. The form assumes company currency and rejects a different bank-account currency when multicurrency is enabled. The movement has its own source and counter-account. |

[Salary access and posting][salary] · [Salary status calculation][salarycalc] · [Contribution record][social] · [Contribution posting][socialpost] · [VAT posting][vat] · [VAT close calculation][vatclose] · [Miscellaneous payment][various]

| Acceptance case | Inputs | Expected result |
| --- | --- | --- |
| TR-OBL-01 | Salary obligation 2,000.00, previously paid 500.00, now pay 1,500.00 with close selected. | Salary marked paid. The new bank outflow is 1,500.00. A user outside the permitted employee hierarchy with ordinary read access cannot operate on this salary. |
| TR-OBL-02 | Contribution due 600.00, pay 200.00, then 400.00, auto-close selected. | First payment leaves 400.00 outstanding. Second permits close. The two bank lines retain the contribution-payment identity. |
| TR-OBL-03 | VAT payable 300.00, pay 100.00. | VAT obligation remains open for 200.00. A sale's taxable revenue and collected VAT on its issued invoice are unchanged by this remittance. |
| TR-OBL-04 | Enter an unallocated 12.00 company-currency bank charge as a miscellaneous debit, with an allowed expense account. | A separate cash outflow maps to the chosen counter-account. Creating an invoice allocation for it would misstate customer collections. |

[transfer]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/bank/transfer.php#L58-L234
[journal]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/accountancy/journal/bankjournal.php#L829-L968
[rates]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/multicurrency/class/multicurrency.class.php#L545-L578
[invoice]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/facture/class/facture.class.php#L514-L535
[salary]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/salaries/payment_salary.php#L61-L162
[salarycalc]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/salaries/class/paymentsalary.class.php#L258-L304
[social]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/sociales/class/chargesociales.class.php#L280-L326
[socialpost]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/paiement_charge.php#L63-L148
[vat]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/paiement_vat.php#L57-L149
[vatclose]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/tva/class/paymentvat.class.php#L220-L284
[various]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/bank/various_payment/card.php#L144-L229
