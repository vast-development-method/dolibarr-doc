# Supplier invoices and settlement

A supplier invoice carries the supplier's document number and an independent internal number. The database enforces uniqueness of the internal reference per entity and of the supplier reference per supplier and entity. A payment has its own ID. One payment can allocate amounts to several invoices, and one invoice may receive several payments. The pair of payment ID and invoice ID is unique.

## Invoice creation and validation

The invoice card can use a supplier price request, order or reception as origin. For a reception, the card also looks up the related purchase order for document linkage. Separate fields hold the supplier's reference, internal reference, source document, line values, currency and status. Comparing these records explains a price or quantity difference. A document link alone supplies no general three-way matching or payment hold.

The model defines standard (0), replacement (1), credit note (2) and deposit (3) supplier invoice types. Each has a separate document status: draft (0), validated (1), closed (2) or abandoned (3). For the ordinary credit-note line path, quantity is positive and price negative. The code contains special handling for preserving discount lines.

Validation refetches the supplier and lines. It rejects an empty invoice and a copied supplier reference still carrying the generated copy prefix. Setup can require domestic company professional identifiers, valid email or the supplier accounting code. The final internal number, actor and time are saved when validation succeeds. In supplier-invoice stock-posting mode it also calls the movement service. In reception-based mode, validating the same bill records the liability without moving the goods again. The supplier-invoice validation event can classify linked procurement documents as billed according to workflow settings.

## Allocations, bank posting and closing

1. Supply invoice ID, date, payment method, optional amount and bank account. The single-invoice REST route checks supplier-invoice create permission and resource access. With bank enabled the account is mandatory. A positive explicit amount is used directly. If omitted, this route calculates its base amount from gross total less previous payments and deposits. Credit notes are assessed separately in the payment object's closure calculation.
2. The payment domain aggregates nonzero allocations in the input currency. It converts allocations at invoice rates, fails if a rate cannot be resolved, and rejects mixed invoice currencies on one payment. It writes the payment header and the per-invoice allocation amounts in both currencies. A combined zero total fails.
3. With automatic closing requested, evaluate **remaining = gross invoice total − allocated payments − credits used − deposits used**, rounded at total-amount precision. A zero remaining balance qualifies the invoice for closure. A paid deposit invoice can produce reusable supplier credit grouped by VAT rate. A closed invoice can also carry a settlement reason. Closing with a reason and closing with the paid flag are distinct records.
4. With the bank module active, the single-invoice route creates its supplier bank payment inside the outer payment transaction. Failure to add the bank entry rolls back the payment. The route returns the payment ID. This operation differs from marking the invoice paid, which changes its classification and records the closing actor/time.

### Acceptance scenarios

| Given | When | Expected |
| --- | --- | --- |
| One vendor already has invoice V-418 in this entity | Enter V-418 for the same vendor, then try the same number for a different vendor | The duplicate for the same vendor conflicts. The supplier-number key permits the other vendor's V-418. |
| One line for 12 units at 10 tax exclusive, 15% VAT and no discount | Validate invoice after receipt in reception-based stock mode | Net 120, VAT 18, gross 138. The invoice is validated and warehouse balances are unchanged. |
| Validated invoice 138, applied supplier credit 18, previous payment 50, deposit used 10 | Add an explicit payment of 60 and request closure | Balance is 138 − 18 − 50 − 10 − 60 = 0. The payment has a separate allocation row and the invoice closes. |
| Gross base amount 120, corresponding invoice-currency total 180 | Request an explicit partial payment of 20 in base currency | The single-invoice route supplies 30 in invoice currency. Posting a second full currency amount would overstate the allocation. |
| Bank enabled, missing account | Attempt to pay | The route returns HTTP 400 before creating the payment. |
| Two positive allocations in different invoice currencies | Try to settle both through one domain payment | Different payment currencies are rejected before the header is inserted. |

The [supplier payment schema](../../schemas/supply/supplier-payment.schema.json) describes the explicit positive-amount, single-invoice case in business terms, including the bank-module condition. Existence of the invoice, currency conversion, access, and remaining balance require application checks. [Accepted payment](../../examples/supply/supplier-payment--bank.json)
