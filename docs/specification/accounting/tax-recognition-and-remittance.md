# Tax recognition by invoice, receipt and remittance

A sale can contribute to a tax report when it is invoiced, when the customer pays, or partly on each basis when the invoice contains different kinds of lines. Sending the resulting amount to a tax authority is a third event, with its own payment and bank transaction. The ERP records each of these separately.

## Select the recognition date

The reporting setup has four independent choices covering sales of goods, sales of services, purchases of goods and purchases of services. A choice of invoice selects rows by invoice date. A payment basis selects rows by the dated allocation of a customer or supplier payment to that invoice. For goods, the source query selects product-type zero with no service start or end date. For services, it selects service-type one or any line with a service start or end date. A free-text line carrying a service date can therefore move to the service rule even when its stored type says goods. Delivery date, bank value date and bank reconciliation date do not determine either calculation.

Both invoice paths select document status 1 or 2 in the corresponding source entities. They include standard, replacement, credit and progress documents, and include deposit invoices unless the corresponding customer or supplier deposits-as-payments configuration excludes them. The payment query includes the deposit document type among its eligible types. The detail page supplies an inclusive explicit start and end. The helper's separate quarter-number path uses a strict lower-bound comparison on the first day of the quarter. A caller using that path can get a different boundary result from one supplying the equivalent pair of dates.

VAT reports can separate identical numeric percentages by the line's tax-source code. For example, 20% with code A and 20% with code B can be distinct rate groups. An installation can filter out zero-rate/zero-tax rows. For a local-tax report the group key uses the selected additional-tax rate. The detailed records retain invoice and line values, invoice identity and date, party, product and service period, main and local tax amounts and, for payment rows, allocated amount and payment date. A purchase-side branch additionally reads paid expense reports and their reimbursement payments in the period.

## Apportion a partial settlement

In the ordinary mixed or payment-based detail calculation, the payment fraction equals amount allocated **to the invoice** divided by that invoice's gross amount. For each applicable line, multiply both net base and recorded line tax by this fraction. On an invoice-basis line the fraction is one. The detailed page also has a debit-option display mode that uses a fraction of one. Changing only this presentation parameter does not change the four query-side settings used to select dates and rows. For a zero-gross denominator the detail code leaves the fraction at one.

Consider a customer invoice dated 20 March. It includes goods of 100 plus 20 tax and services of 200 plus 40 tax, for a gross invoice of 360. Configure goods on invoice and services on payment. If the customer pays 90 on 8 April and 270 on 12 May, March recognizes the goods base of 100 and tax of 20. April recognizes services base of 50 and tax of 10 because 90/360 is one quarter. May recognizes the remaining services base of 150 and tax of 30. No operator assigned the first payment to the goods line. The division uses the gross invoice even though only service rows are being apportioned. A payment covering several invoices contributes only the allocation to this invoice.

The report distinguishes line totals from detail rows. When a single invoice line joins to several payments, the source reader adds its original full totals once per line and retains separate dated payment details. Summing the original line tax from every detail row would overstate the invoice. The recognized total follows the calculated payment shares. The purchase detail uses the same proportional principle with its independent purchase settings.

## Price a line with additional taxes or withholding

The line pricing operation receives two independent optional local-tax definitions. Each has a type and percentage plus an indicator controlling use. Local tax can apply to a net base or to a base that includes the main VAT. Both matter to the payable gross amount. The implementation computes separate results for the unit price, undiscounted line and discounted line and uses the corresponding unit or monetary precision.

| Type | Eligible line | Tax base |
| --- | --- | --- |
| 1 | Goods or services | Excluding main VAT |
| 2 | Goods or services | Including main VAT |
| 3 | Goods only | Excluding main VAT |
| 4 | Goods only | Including main VAT |
| 5 | Services only | Excluding main VAT |
| 6 | Services only | Including main VAT |

For a service priced at 100 excluding main VAT and 20 main VAT, an enabled type 5 additional tax of −15% contributes −15 and produces gross 105. This signed rate can represent an amount withheld. On the same service, a positive type 6 rate of 5% contributes 6 on the VAT-inclusive base of 120, yielding gross 126 when used alone. If the 5% option is configured for goods only, it contributes zero to this service. These values illustrate the software's configured calculation without specifying a jurisdictional rate.

The counterparty report separates amounts retained by customers on sales from amounts retained on supplier transactions. It selects the first or second local-tax field and can filter by counterparty net turnover and exclude parties with zero local tax. Local-tax remittance is a separate record with tax type, label, payment date, value date, positive amount, entity, creator and optional note. With banking active it requires an account and payment mode and registers a negative bank movement. The transaction records the link back to that movement.

## Record and correct a VAT payment

The VAT card represents a declared amount and the period to which it relates. Authorized users can edit the period, payment method and bank account or change paid/unpaid status. The payment record separately carries a dated amount, method, payment reference, creator, note and bank relation. A payment requires a date and nonzero total. Negative amounts are accepted by the VAT payment service. A positive tax remittance produces an outgoing bank entry and a negative remittance produces an incoming entry. The payment-to-bank link and authority-charge link allow tracing from the bank register to the source charge.

On the card, record creation, payment creation and bank registration in the combined flow are enclosed in transactions. Failure registering the requested bank payment rolls back the payment operation. Optional closure checks the charge's remaining amount after payments and marks it paid when rounded remainder reaches zero. Reopening changes the charge status. Payment deletion follows its own transaction. A linked bank line is deleted first. If bank deletion fails, the operation retains the payment. The VAT charge can be deleted only when its payment-total inquiry succeeds and returns zero. The check uses the signed total, so offsetting payments can yield a different result from a count of payment records.
