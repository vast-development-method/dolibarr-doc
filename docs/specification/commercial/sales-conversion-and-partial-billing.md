# Converting offers and billing orders in parts

An offer, order and invoice each has its own commercial date, identity and lifecycle. Conversion carries agreed information into the destination document and creates an origin relationship. The buyer's approval, the seller's fulfillment and the buyer's payment can occur at different times. Keeping the document relationships preserves that history even when all three carry the same amounts.

## Offer to order

A direct conversion requires offer-read and order-create permissions, a source identifier and access to that offer. It returns the new order with its links. The route returns a bad request for a missing identifier, access denied for insufficient rights, and missing resource for an unknown offer. The direct handler delegates creation without requiring a signed status or checking for an existing order. The optional automated workflow is more restrictive. An acceptance event starts it, and an existing linked order suppresses another automatic creation. For online acceptance the workflow enables order creation for the technical signature user.

| Destination information | Population |
| --- | --- |
| Order header | Set order date to the current date. Inherit party and entity, project, payment terms, deposit, payment mode, bank, trade terms and location, availability, demand reason, delivery date, method and address, warehouse, contact and customer reference. |
| Monetary line | Copy product or free description, entered net unit price, discount percentage or exceptional-discount link, tax rates and VAT code, quantity, unit and service period. Retain line rank, hierarchy and special classification. Calculate margin inputs from the original sale and acquisition information. |
| Origin | Record both the source document link and each order line's origin type and originating offer-line identifier. New order and line identities are allocated independently. Additional linked origins can accompany the conversion. |
| Notes and custom fields | Copy private and public notes unless propagation of source notes is disabled. Copy source line custom values. At header level only custom attributes also defined on the destination order are propagated. |
| Foreign currency | Carry the source currency code. Reuse the offer rate when configured. Otherwise look up the rate for the new order date if a rate is needed. An unavailable currency identity falls back to the entity currency at a rate of one. |

The new order can be validated immediately when configured. Without that setting it remains a new order awaiting its own validation. A later change to a selling price list does not reprice the order's copied lines. Conversely, an exchange rate can legitimately differ when the order date differs and conversion is configured to select the rate again.

## Order to invoice

The invoice service requires order-read and invoice-create rights and resource access to the requested order. A missing identifier is invalid. Draft, cancelled and already-classified-as-billed orders are ineligible and return a business refusal. The conversion begins a new invoice with the source lines' quantities, unit prices, discounts, net, tax and gross components, currency information, product identities, units and dates. It carries applicable project and delivery information, optional notes, origin references and custom attributes. The user performing the operation becomes the invoice author.

The ordinary order conversion iterates the order lines. It does not subtract earlier partial invoices from the copied quantities. A still-unbilled order can therefore produce more than one draft, each initially containing the full order quantities. For an order of ten units at net 9, an initial invoice for four must express four units before issue. If a second ordinary conversion follows, its starting quantity is ten. Editing it to six yields the intended second net invoice of 54. Leaving ten yields cumulative billing of 126 against a net order of 90.

The optional order-closure workflow can create an invoice automatically on the closing event. If the order lacks a bank account, the workflow can assign the party's bank account to the new invoice when account selection during ordering was disabled. A client recovering from a timeout during conversion should resolve the order's linked invoices before issuing another creation request. An unbilled order and an existing draft invoice can coexist.

## When validation marks earlier documents as billed

| Enabled invoice-validation rule | Comparison and effect |
| --- | --- |
| One invoice against linked orders | Sum net amounts of linked orders in validated, shipment-in-progress or closed state and compare with the current invoice net. If the configured comparison accepts the result, classify the linked orders as billed. |
| One invoice against linked proposals | Sum net amounts of signed or billed proposals directly linked to this invoice. Apply the configured comparison and classify the linked proposals as billed if accepted. A link reachable only through another document is distinct from a direct invoice-to-offer link. |
| One invoice against linked shipments | Sum the net amounts of validated or closed linked shipments. Exact equality at monetary-total precision with invoice net marks the linked shipments billed. |
| Several invoices against one order | Require exactly one order linked to the current invoice. Gather that order's linked invoices. The current invoice counts during its own validation. Every other invoice must be validated or closed. Sum their signed net totals and compare with the order net at monetary-total precision. Equality classifies that order as billed. |

The single-invoice order and proposal comparisons can be configured to allow differing amounts. The multiple-invoice comparison uses explicit equality independently of that override. With the multiple-invoice rule and the example above, net 36 plus net 54 closes the billing amount when both are validated. An additional linked draft prevents this rule from marking the order billed, even if the first two alone already add to 90. Under that same rule, cumulative net 126 never meets an order of 90. These are amount comparisons. They do not verify per-line shipped quantities or invoice payment allocations.
