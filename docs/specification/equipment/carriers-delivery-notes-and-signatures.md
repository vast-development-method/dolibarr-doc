# Carriers, shipment documents and delivery acknowledgment

Dispatch, carrier tracking, signature and receipt at destination describe separate events. A shipment can leave the warehouse while its tracking number is still unknown. A document can be signed before the carrier completes delivery. The receiving party's actual delivery date is independent of the date the sender promised.

## Carrier method and tracking reference

A shipping-method dictionary row holds a code, label, description, active flag, entity and optional tracking template. The shipment stores the selected method ID and tracking number. The method list uses a localized name for the code when available and otherwise uses the dictionary label. On shipment creation the tracking value is sanitized and whitespace is removed. A shipment returned from storage reads both the carrier information and the stored number.

To construct the tracking link, load the template for the shipment's selected method. Replace the `{TRACKID}` marker with the stored tracking number. If the method or its tracking template is absent, the shipment can still display the number as text. The carrier owns the external status at the link destination. Rendering a tracking link makes no carrier booking, purchases no label and imports no carrier scan events into the shipment lifecycle. Different shipments can store different tracking numbers for separate dispatches against the same customer order.

For example, during order picking the dispatcher knows the carrier but has no consignment number. The planned delivery date and warehouse allocations can already be recorded. Once a number is assigned it can appear on the shipment and its generated document. If the carrier later reports a delay, the tracking link alone does not amend the shipment's planned delivery date or create a new dispatch. The card has a separate operation for changing the planned delivery date.

The method dictionary is in `htdocs/install/mysql/tables/llx_c_shipment_mode.sql`. Method selection, tracking display and planned date actions are in `htdocs/expedition/class/expedition.class.php` and `htdocs/expedition/card.php`.

## Contents of the shipping document

The document service resolves its model from an explicit request, then the model recorded on the shipment, then the configured shipment model and finally its built-in fallback. It loads the origin before rendering. The standard shipping PDF can show ordered quantities and dispatched quantities independently, delivery terms, tracking, descriptions and shipment weight and volume. Enabled columns and options control the printed result. The document can be regenerated in the selected output language with configurable visibility of details, descriptions or product references.

For physical measurements, the standard template can derive totals from the shipped products. A nonzero actual shipment weight stored on the header overrides the computed weight for display, using the header's weight unit. For example, two cartons of goods totaling 18 kilograms may weigh 19.4 kilograms once packed. The printed shipping weight can use 19.4 without changing the catalog's product weights, the number of cartons shipped or their inventory allocations. A subsequent print is a fresh rendering of the underlying records and supplied options.

The service is `generateDocument` in `htdocs/expedition/class/expedition.class.php`. Current standard document columns, weights and tracking behavior are in `htdocs/core/modules/expedition/doc/pdf_espadon.modules.php`.

## Customer delivery receipt

When delivery receipts are enabled, the shipment card offers creation for a validated or closed shipment to a user with delivery creation rights when it has no linked delivery receipt. The action creates a separate document, with its own reference and status, linked back to the source shipment. It copies the customer, customer reference, delivery address, project, notes, delivery terms and location. Each line retains the underlying order-line reference, product and description and starts with the shipped quantity. Additional line fields can carry through where enabled.

The shipment's **planned** delivery timestamp is deliberately omitted from the receipt's **actual** delivery date during creation from dispatch. If 7 units out of an order for 10 were shipped, the receipt created from that shipment starts with 7. It does not assert delivery of the remaining 3. If the shipper promised Thursday but the receiver takes custody on Friday, Thursday remains the promise on the shipment and Friday is entered on the receipt. This distinguishes a late delivery from a retrospectively amended promise.

The receipt gets its own provisional reference. Validation requires a customer, applicable rights and an available numbering model. Ordinary mode uses delivery creation permission, while advanced mode uses delivery validation permission. Validation issues a definitive reference for a provisional receipt, checks for an existing validated reference in the current entity, conditionally updates the draft receipt and records validation time and actor. The confirmation event participates in the operation. A failure can roll back its database effects. This is separate from posting stock according to the configured shipment lifecycle.

Creation eligibility and receipt linkage are in `htdocs/expedition/card.php` and `htdocs/expedition/class/expedition.class.php` under `create_delivery`. Line transfer and validation are in `htdocs/delivery/class/delivery.class.php` under `create_from_sending` and `valid`.

## Signature and downstream billing

The shipment also has a signature status separate from draft, validated or closed. The common signature states distinguish no signature, sender, receiver, online receiver and all parties. A qualified user can record a signature state on the shipment card. The online-signature display resolves the shipment, customer and main document, generating the document if needed. A signature applies to that shipment. It does not by itself establish that every order line was delivered, create the delivery receipt, or report payment of the customer invoice.

For example, a customer who signs for the first seven units can have a signed shipment and a separate unsigned shipment for the remaining three. Shipment-based billing can expose invoice creation on a validated or closed shipment, subject to configuration and invoice creation rights. Signature, receipt creation, close and billing each have their own action and state. An order-level report should therefore traverse the linked shipments, receipts and invoices for the specific fact it intends to report.

Signature states are in `htdocs/core/class/commonsignedobject.class.php`. The supported card and public signing paths are in `htdocs/expedition/card.php` and `htdocs/public/onlinesign/newonlinesign.php`.
