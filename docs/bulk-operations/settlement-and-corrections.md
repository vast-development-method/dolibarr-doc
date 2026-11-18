# Settlement and corrections for selected invoices

An accounts clerk can record money already received, reserve a balance for a future debit, request a bank transfer to a supplier, or reverse a sale with a credit. Each produces different evidence in the invoice, bank and settlement records.

## Record payments against customer invoices

The confirmation supplies one payment date, instrument, bank account and optional private note. The operator needs the customer-payment grant. The date is required. For each selection, the operation loads an invoice, opens a separate transaction and admits a validated, unpaid invoice other than a credit note.

| Quantity | Calculation in this route |
| --- | --- |
| Base amount to register | Gross in company currency less existing payment allocations, less consumed credits, less applied deposits. The operation normalizes the result before payment. |
| Amount in invoice currency | Gross in invoice currency less existing payment allocations in that currency. This particular expression does not expressly deduct the foreign amounts of credits or deposits. |
| Optional amount policy | An adjustment subscriber can supply a non-zero alternative base remainder. Its response is not a new posted allocation. |
| Allocation and bank effect | Each qualifying invoice receives its own payment with one invoice allocation. The selected bank is assigned, payment creation is asked to close the invoice, then the payment is added to the bank. |

A literal zero base remainder produces a warning and a rollback for that invoice. Failure to assign the bank, create the payment or post it to the bank also rolls back that row. The loop proceeds to subsequent selected invoices. For an invoice of 150 with 50 previously collected, 20 applied credit and 10 applied deposit, the base payment instruction is 70. A second selected invoice with an open balance of 40 produces a separate 40 payment and bank record. An ineligible credit note in the same selection does not unwind either successful payment.

If an invoice has a foreign gross of 180, foreign cash allocations of 60 and settlement credits applied in addition, the foreign expression supplies 120 even while the base expression subtracts the credits. The posted result is also subject to the downstream payment method's own currency handling and closure rules. Preserve the two source quantities to explain differences. The scope here is the bulk payment initializer, not a general formula for all foreign balances.

[payment terms and adjustments](../specification/financial/payment-terms-and-settlement-adjustments.md)

## Request money through the bank

| Selection | Admission and amount | Evidence after a successful request |
| --- | --- | --- |
| Customer direct debit | The module and debit-order creation grant expose the action. The list evaluates invoice status, cash, credits, deposits and remaining amount. An existing untreated request is a warning. A specified payment-mode code must be direct debit. For an admitted candidate the action deducts pending request amounts, including a generated line still awaiting processing, and calls the request operation. | A dated request attached to the customer invoice. Request creation and a subsequently settled bank debit are separate events. |
| Supplier credit transfer | Requires the transfer creation grant. The list calculates the payable less payment allocations, consumed credits and deposits, then less untreated requests and pending generated transfer lines. The action checks for a positive available remainder and the transfer payment mode if one is specified. It recalculates the pending amount before creating the request. | A dated supplier transfer request. Partial prior reservations can leave room for an additional request. A completed supplier payment or bank reconciliation needs its own record. |

Both paths distinguish the candidate-screening pass from the request writer. The lists can display a warning for an invoice while continuing with other candidates. An early status warning by itself does not establish a global rejection; the subsequent candidate filter and request operation have separate conditions. In the supplier path the positive remainder is tested before opening the per-request transaction. In the customer path the request method is invoked before that local branch tests positivity. An operator reconciling a zero remainder should inspect actual request and invoice records.

Suppose the supplier payable's open base amount is 490. An untreated transfer request already reserves 100 and another generated, pending transfer line reserves 140. The available amount for this action is 250. Creation reserves 250 for transfer. The three reservations still do not amount to a confirmed withdrawal from the bank. For customer direct debit, an untreated request has an earlier exclusion even if it covers only part of the balance.

## Reverse a set of sales using credit notes

The customer invoice list offers cancellation by credit when invoice creation is allowed and inventory does not move on billing. Confirmation can display subscribed notifications associated with issuing credit notes. Each distinct source invoice is processed separately. The ordinary path accepts standard invoices, the pro forma type in the writer's type test, and deposit invoices where deposits are treated as invoices. Replacement invoices, credit notes and stage invoices fail the type gate for this bulk operation. A stored source type still needs to exist and pass the current status and settlement tests.

A qualifying original is beyond draft and has no positive prior payments, consumed credits or applied deposits. A rejected original yields a per-record explanation and processing continues. For an admitted original the new credit carries the entity, party, project, commercial reference, bank, trade terms, currency and source exchange rate. It is dated at creation and carries no payment term. Its source points to the original. The creation path copies the lines including their hierarchy and reverses monetary totals in company and document currency. Validation of the credit precedes the attempt to consume it against the original.

For conversion into settlement credit the writer groups ordinary non-zero-net lines by VAT rate and tax-source code, then creates one discount record per group. It closes the credit, takes the **last generated discount ID** and links that discount to the original. The original's remaining balance must reach zero for the transaction to commit. With one group, a net sale of 100 and VAT of 15 can yield a credit of 115, an applied credit of 115 and a fully settled original. With two non-zero groups worth 115 and 50, the single final link applies only one group's discount. Unless the original already has a zero remainder after that link, the action rolls the per-source transaction back. A design that automatically links every group describes a different outcome.

An eligible original can therefore be reversed even when a second source with a previous partial payment is skipped or a separate mixed-rate original rolls back. The correction creates documentary and settlement evidence. The ordinary reversal described here posts no customer cash receipt and generates no supplier transfer.

[Credits, replacements and deposits](../finance-exceptions/corrections-and-deposits.md)
