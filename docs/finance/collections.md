# Customer payments, credits and bank reconciliation

One receipt can settle several invoices. One invoice can receive several receipts. To answer “what did the bank receive?” read the receipt or its bank movement. To answer “how much of invoice A did it pay?” read the allocation for A. Both questions arise in the same collection workflow.

## Settlement calculation

For a standard invoice in one currency, outstanding = round(gross − sum of cash allocations − applied settlement credits − applied settlement deposits, amount precision). Calculate all four operands in the same currency. The ordinary balance helper treats an invoice closed with the anticipated-payment discount reason `discount_vat` as having zero due. Some API read paths compute the raw arithmetic balance directly, so retain the closing reason and the underlying operands when exposing a balance.

A percentage line discount reduces the commercial price. A fixed adjustment applied as a negative invoice line already reduces gross. A fixed credit applied to the invoice header reduces the outstanding amount separately. Subtracting a line adjustment again at settlement understates the debt. The adjustment lifecycle records origin, customer, tax components and application. The link operation rejects a request containing both an invoice ID and a line ID as targets, and also rejects a request containing neither. On full settlement of a deposit with automatic closure, the payment operation creates available adjustments grouped by VAT category if conversion has not already occurred.

## Service contracts

| Operation | Input and authority | Result and failure |
| --- | --- | --- |
| Collect the rest of one invoice | Native `POST /invoices/{id}/payments` takes a payment date, payment mode, close flag and bank account when banking is enabled. Require `facture.paiement` and invoice resource access. | Return payment ID. Native single-invoice handling populates its company amount using remaining arithmetic, but populates its foreign amount from the full invoice total. For a previously partially paid foreign invoice, the distributed operation with foreign `remain` explicitly uses the remaining foreign balance. |
| Allocate a receipt | Native `POST /invoices/paymentsdistributed` takes invoice-keyed amounts and the same payment controls. Check visibility on **every** invoice before creating a payment. The caller is instructed to group invoices of one customer. The code selects a common payment basis for the receipt. | Accept all remaining or an amount per invoice. Reject simultaneous positive specifications in both currencies on one row. Default rejects a magnitude above that invoice's remainder. Explicit acceptance of a higher payment changes that check. Return one payment ID. |
| Write payment and optional bank movement | Persist payment date, method, amount, optional reference, author and non-zero allocation rows. If requested, test closure per eligible invoice after recording its allocation. Cash receipt requires a bank account when banking is enabled, and a cheque requires an issuer on that path. | Payment creation and bank posting are enclosed by an outer transaction in the normal REST workflow. Payment-create and bank-add failures explicitly roll back. The cheque-issuer exception is raised after payment creation but before the outer commit. Validate that input up front when implementing the normalized contract. |
| Reconcile a bank movement | On the bank line, supply statement reference, reconciliation flag and user. An enabled statement naming rule can reject the reference. | Store statement reference, flag and reconciliation user on the bank line. The invoice, its cash allocation and its billed total need no alteration. |
| Remove a payment | Domain deletion checks all linked invoice statuses. A linked invoice with state above validated blocks deletion. The linked bank line must permit deletion. | Successful removal deletes payment-bank links, bank movement, allocation rows and receipt. A reconciled bank line or failing delete trigger prevents the change. |

**Normalized distributed-payment contract.** The [receipt request schema](../../schemas/finance/receipt-request.schema.json) uses one amount basis at the receipt level and maps invoice IDs to amounts. This avoids mixed-basis input, since the native implementation selects the foreign-currency column for the entire receipt when any nonempty foreign amount is present with multicurrency enabled. Amounts are positive magnitudes in this request profile. For a credit note the allocated amount is signed negative by the domain. Flags for banking and payment method tell a validator whether an account and cheque issuer are required. Resolve the method ID from the site's dictionary. Customer ownership, resource access, database balances and supported currencies need domain checks. An external reference identifies a receipt to an operator. The documented endpoint supplies no replay guarantee for that reference.

## Foreign currency and audit trail

When entering a company-currency allocation, derive the foreign amount using the invoice's exchange rate. For a partial foreign allocation, divide by the invoice rate. For a foreign allocation that exactly equals the remaining foreign balance at amount precision, use the **actual remaining company amount**. This clears both balances even if reversing the exchange calculation would leave one cent. The payment domain rejects missing conversion data and incompatible invoice or payment currencies within one receipt. Persist both amounts on the allocation. A bank account held in foreign currency records the foreign cash amount and the equivalent company-currency amount on its line.

## Acceptance criteria

| Case | Given and action | Observe |
| --- | --- | --- |
| FIN-PAY-01 | One customer has invoice A for 62.10 and B for 46.00. Apply a 10.00 credit to A. Receive 75.00, allocating 52.10 to A and 22.90 to B, auto-close on, bank enabled. | One receipt, two allocations, one bank movement +75.00. A has zero due and closes. B stays open with 23.10 due. The sum of issued invoice gross amounts remains 108.10. |
| FIN-PAY-02 | A caller can receive against A but cannot access B. Submit the same distribution. | Resource check rejects the request with 403. No receipt, bank movement or allocation is created. |
| FIN-PAY-03 | B has 23.10 due. Request 23.11 with higher-payment acceptance off. | HTTP 400 before successful posting. Outstanding stays 23.10. |
| FIN-PAY-04 | A foreign invoice has 10.00 foreign remaining and 3.34 company remaining at rate 3.00. Settle the foreign remainder with automatic closure. | Allocation is 10.00 foreign and 3.34 company. Zero in each currency. The 0.01 difference from a fresh division and rounding does not survive. |
| FIN-PAY-05 | A bank movement for 75.00 is matched to statement NOV-01. | Reconciliation changes the bank line's statement and actor. The balance on B remains 23.10. Attempted payment deletion is blocked by a closed linked invoice or a reconciled bank line. |
| FIN-PAY-06 | Pay B's exact remaining 23.10 with the close flag off. | New cash allocation leaves zero due. Automatic closure does not run. State and balance can be queried separately. |

[Valid split receipt](../../examples/finance/receipt-request--split.json) · [Sales and bank journals](bookkeeping.md)
