# Customer and supplier payment registers

The amount entering or leaving the bank belongs to the payment. Application to accounts receivable or payable belongs to the allocation between the payment and an invoice. The payment registers join both to explain the business event.

| Relationship | Customer receipt | Supplier disbursement |
| --- | --- | --- |
| Parent and allocation | `paiement.rowid → paiement_facture.fk_paiement` | `paiementfourn.rowid → paiementfourn_facturefourn.fk_paiementfourn` |
| Obligation and party | `fk_facture → facture.rowid`, then `facture.fk_soc → societe.rowid` | `fk_facturefourn → facture_fourn.rowid`, then `facture_fourn.fk_soc → societe.rowid` |
| Method and bank | Both use payment `fk_paiement → c_paiement.id`, and `fk_bank → bank.rowid → bank.fk_account → bank_account.rowid`. | Same relationships. |
| Entity and unresolved links | The payment's `entity` must be in the invoice entity population. The allocation and invoice joins are optional in the ordinary unfiltered query. | The invoice's `entity` must be in the supplier-invoice population. A payment lacking an in-scope joined invoice is absent. |
| Access | Invoice-area access. Recording and deleting payments have their own grants. | Supplier invoicing must be enabled. Read permission comes from the selected supplier-invoice permission model. |

A fixed third-party context is applied to both lists by requiring the payment to have **at least one** allocation to an invoice of that party. This is a payment-level existence test. The optional company-name search operates on the party joined to each displayed allocation. External user context supplies the user's linked third party when applicable. The sales representative predicate tests assignment of the invoice's party through `societe_commerciaux`. A restricted representative is fixed to the current actor. The “unassigned” option requires no assignment record.

## Filters and grouping

Both lists search payment reference `ref`, inclusive payment date range `datep`, company name, payment method **code**, cheque or transfer number `num_paiement`, positive bank account ID via `bank.fk_account`, and amount. All-field search uses the payment reference, party name, cheque/transfer number and payment header amount. The amount-specific search matches **either** the full payment `amount` or the allocated `amount` on the joined detail. The customer list additionally accepts the no-bank-account choice (zero or missing bank account), a search on the payment note and a creator selection. The creator choice for “none” requires `fk_user_creat` to be null. The separate unallocated-customer-payment enquiry selects payment rows without a linked invoice ID and uses its own reduced query.

Both standard views group the surviving allocation rows by payment **and party**, retaining payment, method and bank attributes. The projected allocation total is the sum of the matching allocation rows, and the joined invoice count supplies context. The displayed amount and visible subtotal use the **full payment amount for each displayed group**. An indicator appears when the invoice count exceeds one or a nonzero allocation sum differs from the payment amount. The pagination count uses distinct payment IDs and can differ from the group count.

Suppose a single customer pays 150, of which 90 is allocated to invoice A and 60 to invoice B of the same customer. An unrestricted query returns one payment-and-party row showing 150, two invoices and 150 allocated. Searching for amount 60 selects the B allocation because the header amount is 150. The displayed cash amount remains 150, and the surviving allocation total is 60. A bank reconciliation uses one payment of 150. An invoice reconciliation uses 90 and 60.

If a payment is allowed to span different parties, those two allocations can instead give two party groups, each displaying 150. Adding the two displayed header amounts gives 300 even though only 150 moved. Reconcile cash by distinct payment ID and invoice balances by allocation. The same distinction applies to supplier payments and to filtered views.
