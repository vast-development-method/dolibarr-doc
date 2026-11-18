# From ten units purchased to cash collected

A warehouse buys ten units, delivers six to a customer in two shipments and settles both invoices. The buyer, storekeeper, sales clerk, cashier and accountant see different parts of the same transaction. Reproducing their closing balances requires line quantities, tax amounts, allocations and document links.

## Conditions for the example

One entity, currency, warehouse, physical product and bank account. Both invoices use a hypothetical 20% tax on net prices. All values have two decimal places. Start with zero stock, zero cash and zero outstanding balances for these documents. Enable stock changes at supplier reception validation and customer shipment validation. Use positive quantities, no discounts or fees, no returns, no lots, no credits, no exchange difference and no other stock-posting event. The buyer has obtained all required order approvals. The accountant has bound sales, purchases, tax, bank and counterparty accounts in an open period. These choices fix the branches of the example. [Purchase and receipt guards](../supply/purchasing.md) · [Warehouse balances and valuation](../supply/stock.md) · [Shipment and invoice origins](../sales/dispatch-to-invoice.md)

## Records and effects

The three money columns show balances attributable to this scenario. A positive payable means the supplier is owed money. Bank movements show cash entering or leaving the example account.

| Business operation | Physical units on hand | Customer owes | Owed to supplier | Bank movement to date |
| --- | ---: | ---: | ---: | ---: |
| Record and approve the supplier order for 10 units at 8.00 net | 0 | 0.00 | 0.00 | 0.00 |
| Validate receipt of 10 units against the supplier order line | 10 | 0.00 | 0.00 | 0.00 |
| Validate supplier invoice for 80.00 net plus 16.00 tax | 10 | 0.00 | 96.00 | 0.00 |
| Validate customer order for 6 units at 15.00 net each | 10 | 0.00 | 96.00 | 0.00 |
| Validate first shipment of 4 against the order line | 6 | 0.00 | 96.00 | 0.00 |
| Validate second shipment of 2 against the same line | 4 | 0.00 | 96.00 | 0.00 |
| Issue one customer invoice from the order for 90.00 net plus 18.00 tax | 4 | 108.00 | 96.00 | 0.00 |
| Allocate customer's first payment of 60.00 and record its bank movement | 4 | 48.00 | 96.00 | 60.00 |
| Allocate customer's second payment of 48.00, requesting closure, and record its bank movement | 4 | 0.00 | 96.00 | 108.00 |
| Pay supplier 96.00, requesting closure, and record its bank movement | 4 | 0.00 | 0.00 | 12.00 |

Keep both shipment lines' pointers to the customer order line. The header links connect the supplier receipt/bill to the supplier order, and the shipments/invoice to the customer order. There are two customer receipt-to-invoice allocations and one supplier payment-to-bill allocation. Statement reconciliation can later match the three bank movements without changing the quantities or the amount due on either invoice. [Customer allocations](../finance/collections.md) · [Supplier allocations](../supply/payables.md) · [Document links](../platform/document-relationships.md)

## Independent checks for the accountant and storekeeper

| Check | Calculation | Expected result |
| --- | --- | ---: |
| Remaining stock at the assumed acquisition cost | (10 − 4 − 2) × 8.00 | 32.00 |
| Commercial margin using an acquisition cost of 8.00 | 6 × (15.00 − 8.00) | 42.00 |
| Net tax represented by these two illustrative documents | Sales tax 18.00 − purchase tax 16.00 | 2.00 |
| Bank movement from the three payments | 60.00 + 48.00 − 96.00 | 12.00 |
| Sales journal at transfer | Debit customer 108.00, credit revenue 90.00 and output tax 18.00 | Balanced |
| Cash received at transfer | Debit bank 60.00 and 48.00, credit customer 60.00 and 48.00 | Balanced |

Margin, closing stock value, tax difference and bank movement are four distinct outputs. Ledger posting also has its own transfer conditions. Validating the sales invoice establishes the customer claim; the accountant's journal transfer writes the accounting movement. [Commercial cost basis](../commerce/commercial-margins.md) · [Posting and period controls](../finance/bookkeeping.md)

## Rebuild acceptance

1. After the first shipment, a query by order line finds four shipped. A second valid two-unit allocation brings the total to six. Reading the same order a second time produces the same result.
2. A draft second shipment can reserve quantity in the shipment allocation check. With stock posting on validation, its existence alone leaves the physical balance at six.
3. Re-read balances after the first payment. Cash has increased by 60.00, the validated customer invoice still has 48.00 due and the supplier bill still has 96.00 due.
4. A journal transfer with a missing binding on a nonzero sales line must leave that invoice unposted. Bind it and retry the outstanding transfer. The same invoice supplies one balanced sales movement.
5. Fetch the settlement state as well as the remaining balance. Exact settlement with automatic closure disabled can leave an open invoice with zero due.

[Portable event and balance schema](../../schemas/trade/trade-cycle.schema.json) · [Worked event sequence with expected balances](../../examples/trade/trade-cycle--warehouse.json)
