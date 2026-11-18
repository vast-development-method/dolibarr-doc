# Warehouse corrections and reconciliation

A physical correction needs the product, warehouse, quantity, lot where applicable, posting event and unit-cost rule. The document that initiated a movement may have a separate commercial state. These chapters cover the ordinary bundled operations in release 24.0.3.

| Warehouse decision | Evidence and worked outcome |
| --- | --- |
| [Undo a supplier receipt](receipt-cost-and-reversal.md) | A two-lot receipt fails to reopen when one lot has been depleted. Restoring the missing lot permits reversal. Reclosing gives a new product average. |
| [Reverse a dispatch or reopen an order](dispatch-and-order-corrections.md) | Compares closure, cancellation, deletion and draft, including the difference between a positive signed quantity and an input-type movement. |
| [Allocate a lot to competing demands](shared-lot-and-posting-order.md) | Follows a form suggestion into draft allocations, posting and source-order completion. Explains the transaction and concurrency boundaries visible in the stock writer. |
| [Correct the journal, a count or a transfer](movement-journal-and-counts.md) | Shows why a manual reversal, a stocktake price override and an undo of transfer custody can produce different values and document states. |

[Posting policies](../policies/stock-posting-decisions.md) · [Physical record dictionary](../records/warehouse.md) · [Stock at a date](../specification/operations/stock-at-date-and-value.md)
