# Supplier enquiry, approval and receiving

A buyer can start with a price request or enter a purchase order directly. The order authorises a purchase, a reception records a delivery, a stock movement changes a warehouse balance, and the supplier invoice establishes the payable. The same product and supplier IDs connect the records. An order may have several receptions, including several batches for one line. [Purchase order guide](../reference/locators/supply.md#ref-cd56b5bb389c) · [Order structure](../reference/locators/supply.md#ref-3ba481b180d4) · [Receipt detail](../reference/locators/supply.md#ref-552692a267d7)

## From enquiry to commitment

A supplier price request starts as a draft. Validation assigns its final reference and records the validator and date. Purchase-disabled items normally block validation. Configuration can bypass that check. A decision records the closing actor, date and private note. Acceptance and refusal emit distinct business events. The signed request has status 2, refused 3 and subsequently classified closed 4. The supplier order is a separately identified document with its own approval requirements. [Enquiry validation](../reference/locators/supply.md#ref-5a090df903ab) · [Enquiry decision](../reference/locators/supply.md#ref-323c215df114)

| Purchase order state | Entry and meaning |
| --- | --- |
| Draft (0) | Assemble supplier, currency, terms, project if relevant and order lines. A named product line can retain its vendor reference and tax-exclusive price. |
| Validated (1) | Check product purchasing eligibility unless disabled. Replace a provisional reference, stamp validator and time and emit the validation event. |
| Approved (2) | Record approver and date. When a nonzero approval threshold is enabled, a tax-exclusive total **at or above** the threshold needs both approval records. The first recorded level leaves status 1 until the other is present. |
| Sent to supplier (3) | Record order date, method and optional comment. This creates an audit event for submission. |
| Partially received (4) or completely received (5) | Record dispatch details and determine fulfilment using the selected receiving workflow. The order's billed flag is independent of this status. |
| Cancelled (6), cancelled after ordering (7), refused (9) | Cancellation, non-delivery after sending and approval refusal retain distinct outcomes. |

The card can perform first approval immediately after validation when the user can approve, direct approval is allowed and warehouse selection is unnecessary. For integrations, the order validation and approval actions are distinct. Validation uses create permission in normal mode and the advanced validation right in advanced mode. Approval applies the supplier-order approval right. The card exposes a separate second-level permission for its second-approval control. Placing the order requires the order-placement right. [State codes](../reference/locators/supply.md#ref-72b1482006a6) · [Validate](../reference/locators/supply.md#ref-9ea4b773a598) · [Approve](../reference/locators/supply.md#ref-17b58ecd7dfc) · [Order card](../reference/locators/supply.md#ref-763a6063578f) · [Place order](../reference/locators/supply.md#ref-862008650cf6)

## Which event adds purchased stock?

Stock setup makes the following options mutually exclusive for inbound automatic posting within an entity. There is a separate choice for customer-side posting. [Configuration](../reference/locators/supply.md#ref-b63a7e4bd806)

| Selected inbound event | Quantity, warehouse and price source |
| --- | --- |
| Final order approval | Each catalogue line's ordered quantity, supplied warehouse and tax-exclusive unit price. Percentage discount reduces cost unless excluded by configuration. The code's option name says “validate”, but the change occurs at approval. [Approval posting](../reference/locators/supply.md#ref-f9176c608c82) |
| Direct supplier-order dispatch | Actual dispatched quantity and warehouse, with the price passed by the caller. An enabled supplier-return option routes negative dispatch through the outgoing movement path. [Direct dispatch](../reference/locators/supply.md#ref-399445e5a674) |
| Validate reception | Quantities, warehouses, batch/date detail and unit cost from reception splits joined to purchase order lines. Unlinked free reception lines do not join this stock-posting loop. [Validate reception](../reference/locators/supply.md#ref-a873057222b9) |
| Close reception | The same line-level business inputs, posted when a validated receipt changes to closed. Draft closure fails. A repeated close of an already closed object adds no movement. [Close receipt](../reference/locators/supply.md#ref-6035856307cb) |
| Validate supplier invoice | Invoice catalogue quantities and selected warehouse. An ordinary bill receives goods and a supplier credit note issues them. A percentage discount is included in cost unless configured otherwise. [Invoice posting](../reference/locators/supply.md#ref-661160244234) |

## Validate an order-linked receipt

1. Build receipt splits against specific order-line IDs. Each split records the warehouse, quantity, optional batch and dates, and its unit cost. When stock is active and the line has a catalogue product, a warehouse is normally required. With batch tracking active, the line rejects a missing batch for a tracked item and a supplied batch for an untracked item. Product date requirements also apply.
2. Validate a draft. The document receives a reference, validation date and actor. In validation-posting mode eligible splits produce stock movements. A zero-quantity split, or a negative split when negative receptions are disabled, is skipped by the movement loop.
3. Recalculate order progress using dispatch rows for this order. Draft receipts are excluded. When dispatch approvals are enabled only approved splits are counted. The normal equality check compares totals **by product**, including the presence of product keys. Order lines for the same product therefore aggregate at this stage. The optional over-receipt policy uses a different comparison. On closure a separate check compares cumulative closed quantities **by original order line** against the ordered quantities.
4. The validation transaction also invokes the receipt-validation event. A failed stock movement or trigger causes rollback. A validated receipt can subsequently close under its own guard. [Create receipt split](../reference/locators/supply.md#ref-eb5289818022) · [Validation transaction](../reference/locators/supply.md#ref-b968bc22fa73) · [Quantity comparisons](../reference/locators/supply.md#ref-950042065c73) · [Close and compare order lines](../reference/locators/supply.md#ref-a255f3e8dc19)

### Operation contracts

| Operation | Inputs and authority | Success or failure visible to the caller |
| --- | --- | --- |
| Approve order | Order ID, warehouse if posting here, approval level. The REST action checks create permission and order access before invoking domain approval. | Returns an approval message. A successful first approval can leave the order awaiting the other level. Read status when advancing the workflow. |
| Validate receipt | Receipt ID. REST requires reception-create and access to the record. With advanced rights the domain also requires reception validation permission. | Returns a refreshed receipt. Missing record → 404, failed access → 403, already processed → 304, domain failure → 500. |
| Close receipt | Receipt ID, reception-create and access to the record | Returns the refreshed closed receipt. The database update requires the persisted state to be validated and checks the affected-row count before adding stock. |
| Receive directly against a supplier order | Order ID and splits for product, quantity, warehouse and vendor cost. The route checks order-create and resource access. | Each dispatch commits independently before the route recalculates order status. If a later split fails, read previously recorded splits before retrying. Replaying the entire request can duplicate earlier receipts. |

[Supplier order REST actions](../reference/locators/supply.md#ref-4d36d0377019) · [Direct receiving route](../reference/locators/supply.md#ref-fd1b2d98ae59) · [Reception REST actions](../reference/locators/supply.md#ref-4a171159ff76) · [Closing route](../reference/locators/supply.md#ref-b093739988aa)

### Acceptance scenarios

- **Threshold equality.** With an approval threshold of 500 and tax-exclusive order total 500, record the first level. Expect status 1 and its approval stamp. Record the second level. Expect status 2 and, if approval-based stock posting was selected, one inbound posting for each eligible line.
- **Split delivery.** Order 12 units of a tracked product. Validate a receipt for 7 to warehouse A, leaving a draft receipt for 5 to B. With validation-based stock posting, A increases by 7, B stays unchanged and the order is partial. Validate the second receipt. B increases by 5 and the order becomes fully received under normal equality rules.
- **Failed batch.** Try to receive a tracked item without a batch. The add-line action fails. A receipt awaiting closure in close-posting mode can validate successfully without changing stock. Closing it once posts its eligible quantities.
- **Billing and delivery.** In receipt-based stock mode, invoicing the 12 units after receipt adds zero additional units. An invoice can be traced to the order and receipt through document links. The billed classification follows its own workflow rules. [Invoice links](../reference/locators/supply.md#ref-224134907490) · [Billed workflow](../reference/locators/supply.md#ref-f6232995d323)

The [receipt schema](../../schemas/supply/purchase-receipt.schema.json) represents a positive, warehouse-tracked delivery against a purchase order. Product tracking in each example is an input to the example. An implementation must fetch the authoritative tracking policy and line membership before posting. [Accepted split](../../examples/supply/purchase-receipt--split.json)
