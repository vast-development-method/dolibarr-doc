# Sales decisions on partial dispatch and billing

Run the following command from the repository root with Python 3. It uses the standard library and reads the scenarios alongside the script.

```sh
python3 conformance/sales/check.py
```

The [scenarios](scenarios.json) supply inputs and expected results for four independent rules. Each case names its configuration and the business condition it exercises. The [executable reference model](check.py) derives actual results from those inputs. It compares quantities as exact decimals and rounds money half-away-from-zero to the scenario's total precision. A mismatch prints the case ID, expected result and actual result and exits with a failure status. [Dolibarr total rounding](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L7923-L7942)

| Rule | Question answered | Source |
| --- | --- | --- |
| `allocation` | Does the optional order-line ceiling allow a proposed positive goods quantity after existing allocations? Draft rows count, cancelled rows do not, and an edit excludes its own prior quantity. | [Allocation guard](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expedition/class/expeditionligne.class.php#L870-L911) |
| `completion` | After the current shipment event, do the core line-level test and optional product-level workflow each request order closure? Inputs are linked rows for the same order, with states as they stand during the event. `workflowEvents` is empty when that workflow is disabled. | [Core closure](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/expedition/class/expedition.class.php#L2981-L3009) · [Status threshold](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/commande/class/commande.class.php#L2460-L2489) · [Workflow product roll-up](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/triggers/interface_20_modWorkflow_WorkflowManager.class.php#L447-L527) |
| `cumulativeBilling` | On validating one invoice with a single source order, does the sum of eligible linked invoice nets equal the order net at total precision? A separate draft blocks the rule. | [Linked-invoice classification](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/triggers/interface_20_modWorkflow_WorkflowManager.class.php#L275-L308) |
| `directBilling` | On validating an invoice linked to one or more orders, is the aggregate eligible order net sufficient to pass the classification gate? Equality is required unless the explicit override is active. | [Eligible order statuses](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/triggers/interface_20_modWorkflow_WorkflowManager.class.php#L175-L202) · [Comparison and override](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/triggers/interface_20_modWorkflow_WorkflowManager.class.php#L697-L706) |

For example, two order lines for the same SKU request 4 and 6. Dispatching 5 and 5 can pass the optional product-level workflow while failing the core comparison by line. This case supplies the stored allocations directly, as it requires data admitted without the optional quantity ceiling. A second group starts with 180 and 270 in invoices against an order of 450 and varies invoice state, source count, decimal precision and workflow settings. [Business flow and service boundaries](../../docs/sales/dispatch-to-invoice.md)

The checks model decisions read from Dolibarr 24.0.3. They do not execute a Dolibarr server, database writes, stock movements, permissions or trigger failure paths. A closure request describes an attempted transition. The core shipment close path does not inspect the order-close result. A live integration test must re-read both records. Quantity inputs here are bounded decimal examples, with no assertion of bit-for-bit equivalence to native floating-point arithmetic on arbitrary values.

Verified with the pinned cases: `24/24 sales decision scenarios passed`.
