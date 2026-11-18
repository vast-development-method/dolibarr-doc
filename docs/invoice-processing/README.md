# Customer invoice processing

A sales invoice has three independently observable results. Its detail rows establish the commercial amount due. Payment allocations and applied adjustments establish the outstanding amount. A sales journal transfers eligible invoice amounts into bookkeeping after account assignment. Each has its own identifier, permissions and correction path.

| Question | Follow the operation |
| --- | --- |
| Which fields can an integration supply on a line, and which values must it resend on amendment? | [Line inputs, writes and removals](line-commands.md) |
| What changes if the same sale is submitted as an entire invoice or converted from an order or a contract? | [Draft creation and source conversion](draft-and-conversion.md) |
| How is a percentage deposit divided between tax categories? Where does a rounding difference go? | [Deposit allocation](deposit-allocation.md) |
| When can a partly assigned invoice reach the ledger? What does an empty queue mean? | [Account assignment and sales journal](account-assignment.md) |

The [invoice and detail record dictionary](../records/billing.md) specifies the storage fields. The [pricing guide](../finance/customer-invoices.md), [rounding examples](../finance/rounding-examples.md), [collections](../finance/collections.md) and [progress and retention](../finance-exceptions/progress-and-retention.md) cover the adjoining operations.
