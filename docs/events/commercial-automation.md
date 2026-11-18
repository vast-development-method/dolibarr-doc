# Commercial decisions that can update other records

These are selectable policies. At a site with automatic order creation turned off, signing an offer changes the offer alone. At a site with the policy on, the same action also attempts to create the buyer’s commitment record. Record the enabled capabilities and switches alongside the workflow definition.

## From acceptance to fulfilment

| Originating decision | Additional conditions | Dependent record and failure boundary |
| --- | --- | --- |
| Customer accepts a proposal | Orders enabled; automatic creation from a signed proposal enabled | Load existing document links first. An already linked order prevents creation in this handler. Otherwise create an order from the proposal with its origin context and propagate failure. The online-signature path equips its technical actor for this specific creation. |
| Customer order closes | Invoicing enabled; automatic invoice from closed order enabled | Invoke the order-to-invoice operation. On successful creation, if the order has no account, the party has one, and bank selection was not requested during order entry, attempt to assign the party's bank account to the invoice. A failure in account assignment is returned. |
| Shipment validates or closes | Apply the separately configured trigger moment; order/shipment records must be linked | Compare accumulated shipment quantities to ordered quantities using the workflow's product grouping. Services normally drop out when stock for services is disabled. If complete, request order closure under the shipment actor's already checked action. The line-based closure path and the policy-based grouping are distinct. |
| Supplier receipt validates or closes | The matching received-on-validation or received-on-close switch is enabled | Compare related receipt and order quantities under the receiving workflow. A complete match can request the supplier order's fully received status. Its billed classification is a separate decision. |

The automatic offer-to-order branch checks for an existing linked order before creation. The close-to-invoice branch shown here directly invokes the conversion operation. A consumer that sees the same event more than once must inspect actual links and documents before repeating an external action. A status label alone cannot establish whether the downstream record persisted.

## When does an order count as billed?

Suppose one validated order totals 1,000.00 before tax. It has two linked invoices at 600.00 and 400.00. The release supports more than one policy, with different meanings.

**Single-invoice comparison.** On validation of an invoice, the policy selects linked orders and adds the pre-tax amounts of orders in qualifying states. It compares the resulting total with the current invoice at total-amount precision. A 600.00 invoice differs from the 1,000.00 order. The setting allowing classification despite amount differences can override this comparison. The implementation uses one loop to sum eligible orders and a second loop to request billed classification on linked orders. A linked object's own transition still governs its result.

**Cumulative comparison.** The special cumulative rule requires exactly one source order for the invoice. It reloads the invoices linked to that order. Every invoice must be validated or closed, with the currently validating invoice accepted explicitly. It compares the sum of pre-tax invoice amounts with the order amount at total precision. Once both 600.00 and 400.00 qualify, the order can be marked billed. Another attached draft invoice blocks this rule even if the eligible rows already sum to 1,000.00. An invoice consolidated from two orders fails the one-source condition. The amount-mismatch override from the first policy is outside this rule.

**Payment-based classification.** A further option reacts when the invoice is classified paid. This is a distinct event from invoice validation and a distinct policy from cumulative billing. In a rebuild, preserve the configured driving event and the record being classified. A bank statement match does not itself establish any of those preconditions.

Comparable proposal, supplier-order, supplier-quotation and receipt policies use typed links and their own eligible states. For example, validating a supplier invoice can cause the workflow to compare purchase orders and then supplier quotes to the bill. A reception can also be marked billed when the appropriate policy is enabled. None of these classifications substitutes for a payment allocation or a physical stock posting.

## From a support request to service delivery

Ticket creation can attempt to locate a contract when the ticketing, contract and workflow modules, the contract-link option, a configured product category and a ticket third party are present. Depending on policy, the lookup can also traverse the party's parent companies. It considers contracts in draft or validated state with eligible initial/open service lines for the category. The selection code counts matches and applies its single-contract rule before attaching an association; users should be able to inspect the actual linked contract on the resulting ticket.

A separate policy can create a field intervention from a ticket. The resulting intervention has its own owner, business reference and lifecycle. Opening an intervention provides evidence of a service task; it supplies neither proof that the technician performed the work nor authority to bill the customer.

Implementation locators: `htdocs/core/triggers/interface_20_modWorkflow_WorkflowManager.class.php`, lines 76–174 (acceptance and order close), 175–307 (sales billing), 308–447 (purchase and settlement classification), 448–618 (fulfilment), 624–681 (ticket handoffs) and the concluding `shouldClassify` routine. For the document-level comparison see [partial dispatch and billing](../sales/dispatch-to-invoice.md).
