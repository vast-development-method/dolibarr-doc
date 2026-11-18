# Sales, shipment and purchasing settings

These 16 settings are available on five commercial setup screens. Each entry identifies where the operator makes the choice and where the running system uses it. A module activation default is identified explicitly where the model declares one.

## Customer proposals and orders

A proposal can expire, be signed and be downloaded. These are three distinct operations. Its validity period is saved with the proposal. Its signature and download controls govern what the system offers when communicating about the document. See [proposals and orders](../sales/proposals-and-orders.md).

| Operator choice | Effect |
| --- | --- |
| Default validity in days · `PROPALE_VALIDITY_DURATION` | The module supplies **15 days** on activation. The proposal form starts with this number and allows the author to replace it. Creation calculates the end of validity from the proposal date and the duration entered for that proposal. |
| Offer online signature · `PROPOSAL_ALLOW_ONLINESIGN` | The module enables this on activation. With the option on, a proposal that has left draft can display its signature link. The signer still has to complete the signature operation. Turning the option off suppresses that card link. |
| Include a proposal download link · `PROPOSAL_ALLOW_EXTERNAL_DOWNLOAD` | When on, generating a message for an existing customer proposal can fill the proposal-download template field with the last main document's link. When off, that field is empty. Generating a new copy of the proposal and sending the message are separate actions. |
| Include a customer-order download link · `ORDER_ALLOW_EXTERNAL_DOWNLOAD` | This independent switch controls the corresponding template field for an existing customer order. An order message can offer the last main order document when the setting is on and a shareable document is available. |
| Suppress manual billing classification on the order card · `ORDER_DISABLE_CLASSIFY_BILLED_FROM_ORDER` | This control is shown when invoicing is active. Enabling it hides both manual billing switches on the customer-order card. With it off, an authorised order editor can change classification on an eligible validated order when billing on shipment is inactive. Marking an unbilled order also requires a nonnegative tax-inclusive total. |

An author using the 15-day default can enter 30 on a particular proposal. Its validity end is calculated from that proposal's 30-day duration. Sending the resulting file and asking the recipient to sign it remain separate choices.

## Shipment preparation

The picking form resolves source order lines, remaining quantities and eligible warehouse or lot positions. These controls affect data entry, the ordering of suggestions, and how a recipient can acknowledge a shipment. See [dispatch through invoicing](../sales/dispatch-to-invoice.md).

| Operator choice | Effect |
| --- | --- |
| Leave shipment quantities blank · `SHIPMENT_DONT_PREFILL_QTY` | The shipment form defaults this switch to false if unset. With it off, eligible quantity inputs start with the calculated deliverable quantity. With it on, the field starts empty so the operator enters the quantity actually picked. The form can still show the supporting warehouse and lot information. |
| Show entry date for candidate lots · `SHIPPING_DISPLAY_STOCK_ENTRY_DATE` | Turning this on adds the entry-date column to shipment preparation. For each candidate warehouse lot, the lookup derives the latest matching incoming movement date by lot identifier and warehouse. It sorts candidates by that date ascending, then by lot identifier, before the remaining criteria. A replenished lot can therefore show a date later than its original arrival. |
| Offer shipment signature · `EXPEDITION_ALLOW_ONLINESIGN` | When on, the shipment card can show the recipient's signature link once the shipment has left draft. Turning it off suppresses the link. This setting belongs to shipment acknowledgement independently of the signature option on sales proposals. |

## Supplier orders

These decisions occur at three different points in a purchase's life. The order is authorised for placement, its deliveries are reviewed, and its billing status is reconciled. A delivery review can hold up completion of receiving even after the physical dispatch lines have been recorded. See [supplier ordering](../supply/purchasing.md) and [supplier bills and allocations](../supply/payables.md).

| Operator choice | Effect |
| --- | --- |
| Require two approvals at or above a threshold · `SUPPLIER_ORDER_3_STEPS_TO_BE_APPROVED` | Supply a positive amount to apply a second approval level when the order's tax-exclusive total reaches that amount. Blank or zero leaves the threshold inactive. The workflow records each level's approver and date. The order remains validated while an applicable approval is outstanding, then becomes approved. The second-level action has its own permission. |
| Review order-based receipt lines · `SUPPLIER_ORDER_USE_DISPATCH_STATUS` | The setup offers this switch when the separate reception module is inactive. With it on, the purchase-order dispatch screen presents a status for each recorded delivery line and supports review actions. Attempting to mark receiving complete fails while lines still await review. |
| Require a linked supplier bill for manual billing classification · `SUPPLIER_ORDER_DISABLE_CLASSIFY_BILLED_FROM_SUPPLIER_ORDER` | With invoicing active, switching this on makes the purchase-order card require at least one linked supplier bill before it offers the action to mark the order billed. With the switch off, the card can offer the action without a linked bill. Order state, the current billing flag and the user's rights still apply. The card has a separate branch when invoicing is inactive. |
| Include a supplier-order download link · `SUPPLIER_ORDER_ALLOW_EXTERNAL_DOWNLOAD` | With the switch on, a message concerning an existing purchase order can include a direct link to its last main document. With it off, the supplier-order download template field is empty. |

For a threshold of 5,000, a tax-exclusive order of 4,999.99 stays on single approval. At exactly 5,000 the threshold applies. After the first approval alone the order stays validated. Once both required approvals have been recorded it can move to approved.

## Supplier price requests

A request can have a provisional identifier while its prices and terms are being assembled. The numbering and document models have distinct roles when the buyer validates the request and generates its outward-facing document. See the [purchasing workflow](../supply/purchasing.md).

| Operator choice | Effect |
| --- | --- |
| Numbering model · `SUPPLIER_PROPOSAL_ADDON` | Choose the active numbering model for supplier price requests. The supplied module default is `mod_supplier_proposal_marbre`. On validation, a request whose reference is provisional or empty obtains its next number from the selected model. A request already carrying a final reference retains it. |
| Default document model · `SUPPLIER_PROPOSAL_ADDON_PDF` | The supplied activation default is `aurore`. Generation gives precedence to an explicitly requested model, then the model on the request and finally the configured default. This choice determines how the outward-facing request is rendered. |
| Draft watermark · `SUPPLIER_PROPOSAL_DRAFT_WATERMARK` | Enter the text that the supplied default PDF model stamps on a draft. An empty value produces no configured watermark. The model applies this text only while rendering a draft request. |
| Standard footer text · `SUPPLIER_PROPOSAL_FREE_TEXT` | Enter wording to accompany supplier price requests, such as purchasing terms. The supplied PDF models pass the setting to their page-footer renderer. The template, generation options and the document being produced determine its presentation. |
