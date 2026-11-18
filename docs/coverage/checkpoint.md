# Coverage checkpoint for 24.0.3

Every descriptor that passes the release's stable filter has a [functional reading guide](guide-map.json). The [inventory](modules.json) additionally records the eleven excluded descriptors so the release-wide count can be reproduced. A guide entry specifies the business behaviour reviewed. A module can span many additional screens, country rules and configuration combinations.

## What has been verified

| Evidence | What the check establishes |
| --- | --- |
| Tagged implementation and installation DDL | Chapters trace to the pinned source. The [validator](../../tools/validate.py) checks paths, line bounds, coverage keys, cross-links and examples. |
| [Schema contracts](../../schemas/) and [fixtures](../../examples/) | Every published portable schema has at least one accepted and one rejected example. These tests check record shape, types and conditional requirements. |
| [Integrated trade cycle](../trade/worked-cycle.md) | An independent decimal calculation reconciles ten successive stock, receivable, payable and cash checkpoints. |
| [Sales decisions](../../conformance/sales/README.md) | A reference model checks 24 allocation, shipment closure and billing classification scenarios, including duplicate product lines and nearly equal totals. |
| [Actual release pricing code](../finance/pricing-verification.md) | Four blueprint invoice fixtures ran through the upstream calculator and invoice-line aggregation. A separate run compared 14 expected arrays in the upstream pricing test. |
| [Reference indexes](../reference/README.md) and [permission declarations](../permissions/README.md) | The indexes expose the source behind fields, declared keys, API methods and permissions. Effective rights and state transitions are further constrained by module settings, actor and record. |

The transaction and failure scenarios outside the recorded runtime pricing checks were traced to code. End-to-end UI and REST execution against a configured Dolibarr installation, real payment-provider callbacks and country-specific return preparation remain separate verification work.

## Resume one bounded investigation

Start with one row, its named evidence and a single test setup. Record the release SHA, config switches, actor, initial record IDs and balances. Capture the operation result, resulting rows and downstream state. Commit the chapter, its contract or regression case, and any correction to this checkpoint together. This lets the next investigation begin from the repository.

| Area already traced | Next focused parity check | Evidence to capture |
| --- | --- | --- |
| Stock and dispatch | Two customer order lines for the same SKU, split across lots and warehouses. Compare allocation caps, warehouse balances, close attempts and actual order state. | Order-line IDs, batch splits, stock movements and header flags before/after. |
| Purchasing | Run approval above a threshold, two partial receipts and a deposit-backed supplier bill under each supplier-module configuration. | Actor rights, approval stamps, receipt state, payable and typed links. |
| Invoicing and cash | Allocate in foreign currency across a rounding residual, then attempt reversal after reconciliation. | Both currency amounts, allocation IDs, bank statement and invoice closure reason. |
| Accounting | Transfer a batch with an unbound nonzero line in the middle. Correct the binding and retry. | Voucher IDs, per-document debit/credit totals, committed movements, dates and actor. |
| Manufacturing and projects | Split production across two runs, reverse one movement, and bill logged time with two workers at distinct rates. | Planned vs actual rows, stock/value changes, stored time rates and invoice backlinks. |
| Workforce and service | Exercise delegated approval with an external or unrelated actor and repeat the same transition after another operator completes it. | Rights, object scope, initial/final state, entitlement or reimbursement and activity log. |
| Commerce and payments | Interrupt the point-of-sale or bank-order workflow after a successful external payment. | Provider reference, ERP receipt, bank movement, closing status and repeat handling. |
| Extensions, documents and integration | Compare an ordinary entity and a shared-data entity on REST, portal access, import, and blocked/nonblocking webhook delivery. | Configuration, requested object, visibility, emitted events and durable history. |
| Localization and reporting | Select one jurisdiction, chart and tax profile; compare an actual posting with the operational report using the same period. | Country configuration, tax dictionary IDs, report date basis, bound accounts and totals. |

When taking a newer stable release, first compare upstream release metadata, descriptors and the affected implementation paths. Keep the 24.0.3 evidence identifiable so a change in behaviour can be explained at a precise revision. External marketplace modules need their own independently established release baseline.
