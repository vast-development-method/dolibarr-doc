# Shipment and reception notes

A shipping clerk needs to know which items left the warehouse and under which lot numbers. A receiving clerk needs to know how much arrived against a particular purchase line. Delivery and reception notes use the order as context and the logistics transaction as evidence of the quantity handled. Their optional monetary columns follow different calculations.

## Delivery note

The Rouget delivery note, used when neither a saved nor a configured shipment model is available, loads the originating document and, when available, prints the source order reference, customer reference and order date. The shipment detail reader retrieves both the ordered quantity and the quantity shipped from each warehouse. Consecutive detail records for one source line are gathered into one product line. The combined quantity sums shipped quantities, while the warehouse-detail list keeps the warehouse, shipped amount and individual shipment detail identifier. The first warehouse identifier on the combined line is cleared when several detail rows contribute.

The model has independent controls for ordered quantity, shipped quantity, weight/volume, volume alone and display of prices excluding tax. For a physical product the writer multiplies unit weight and volume by quantity shipped. Each measure uses the product's unit and a configurable rounding precision, defaulting to five decimal places. Hiding volume can leave weight visible. Service-type items do not acquire a computed product weight simply because a quantity was shipped.

An order for 12 units, each weighing 1.25 kg, has a delivery of five. With both quantity columns and weight enabled the note shows 12 ordered, five shipped and 6.25 kg. If two lots supplied two and three of those five, their separate detail descriptions can show their lot, quantity, use-by and sell-by dates when recorded. With the warehouse-on-shipment option, the description can append the originating warehouse reference after resolving the stock record for that lot. A shipment without batch details does not acquire a warehouse label through this lot-specific branch.

When the cost display is enabled, the note shows the prepared net line amount beside the unit price. On a shipment line with one source detail, that value uses shipped quantity, unit price and the line discount. For multiple warehouse details grouped into one product line, the source loader adds each detail's price to the shipment header totals but assigns each detail's calculated net amount to the combined line as it iterates. The last assigned line amount can differ from the sum displayed at shipment level. Combining split quantities with an independently recomputed monetary total would conceal this release behavior.

Release references include `htdocs/expedition/class/expedition.class.php:2187–2248,2273–2332,3333–3352`, `htdocs/core/modules/expedition/doc/pdf_rouget.modules.php:513–527,578–614,1015–1047` and `htdocs/core/lib/pdf.lib.php:2257–2299`.

New installations configure Espadon. Its line columns, contact source and measured totals are described in [Shipping, transfer and progress certificate layouts](../../document-models/physical-and-stage-documents.md).

## Supplier receipt note

A receipt detail can retain its purchase-order-line identifier and inherit the ordered quantity, unit price, tax and discount from that line. The receiving record retains the actual received quantity. With lot tracking enabled, a received lot contributes its identifier, quantity and dates to the line's batch details. The default receipt form prints the source supplier order when available. It can use the order's external shipping contact for the address block and can include an assigned internal contact in the header.

For adjacent receipt rows originating from the same supplier order line, the form prints and adds the ordered quantity only on the first row. It prints the received quantity on every row. The suppression compares with the immediately previous source-line identifier. It is not a global distinct-order calculation across an arbitrarily reordered dataset. Hiding ordered quantities with the receipt option suppresses that column and its ordered total.

Suppose a supplier order line for ten pieces arrives in two lots of four and three. With the two receipt rows adjacent, the note shows ten ordered once and received quantities four and three. It can show distinct batches and dates for both rows. Seven pieces arrived. The note does not indicate the other three pieces arrived simply because the expected quantity was ten.

The optional price display computes each received amount as unit price times *received* quantity, rounded to monetary precision, then sums the displayed amounts. The source receipt's own value calculation applies the purchase line discount. At a unit price of 20 and a line discount of 10%, receipt of four plus three prints net row amounts 80 and 60 under this option, total 140. The receipt source value on the same inputs is 126 before main tax. Using the displayed line valuation to book the liability would therefore overstate this example by 14.

The receipt summary obtains actual quantity, total weight and total volume from the logistics document. Measured weight can replace the calculated weight. Entered package width, height and depth can determine a measured volume, which supersedes the product-derived total for display. The summary uses suitable units for the resulting measures. A physical package can legitimately weigh more than the sum of its catalog item weights.

Release references include `htdocs/reception/class/reception.class.php:1649–1703,2586–2608` and `htdocs/core/modules/reception/doc/pdf_squille.modules.php:542–590,730–789,993–1040,1073–1092`.

## Build and disclose the right copy

Shipment uses the common document-building action. It requires source create/modify permission or explicit document-generation capability. The reception card's dedicated build action uses reception-read permission. That action can persist a selected model, choose an explicit language in multilingual mode, fall back to the supplier's language, and deliver any generation error to the operator. The ability to obtain either note is therefore determined by the source card and action.

An operator can request the same shipment with prices on an internal copy and without prices under the settings of the recipient-facing model. The two copies can describe the same items and batches. Generating a note does not create a new stock movement, close the order or initiate a customer or supplier payment.

Release references include `htdocs/expedition/card.php:155–163,222–230`, `htdocs/core/actions_builddoc.inc.php:60–92` and `htdocs/reception/card.php:705–731`.
