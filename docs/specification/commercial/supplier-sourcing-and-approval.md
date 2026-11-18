# Supplier quotations, sourcing and purchase approval

A request for supplier terms records a supplier's answer. A supplier price record makes a repeatable offer available to purchasing. A purchase order selects what to buy, and its approval authorizes that commitment. Each has a separate identity. A quotation can be accepted without every quoted item becoming a maintained supplier price or an ordered item.

## Issuing and closing a request

A request can be validated by a user with supplier-request creation rights under ordinary permissions, or with advanced validation rights when enabled. Validation loads the supplier, normally checks that the products on the lines remain available to buy, and replaces a provisional request reference. A setting relaxes the purchase-availability check. The supplier may quote only a subset of the items requested.

Closure records its date, actor and outcome and **replaces** the private note with the submitted closing note. Acceptance, refusal and classification as billed have separate notifications. The outcome can select a different document model for regeneration. A rejected closing notification rolls back the status change.

When configured, acceptance also proposes updates to the supplier's maintained prices. Each line with positive quoted unit price passes its product, supplier, quantity, whole-line discounted net amount, supplier reference, VAT and foreign-currency net amount to price maintenance. The request's supplier item reference has a fallback to the alternate line reference. The exchange rate is retrieved for the quoted currency when enabled, with one as the initial rate. The amount for a ten-unit line quoted at 20 with 10% off is 180 for ten units. There is no second 10% reduction in the new maintenance request. Lines at zero or below are skipped. The loop does not examine each price-maintenance return value before reporting success. Acceptance establishes the quotation decision even when an individual price record still needs reconciliation.

Source locations include `htdocs/supplier_proposal/class/supplier_proposal.class.php:valid`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:cloture` and `htdocs/supplier_proposal/class/supplier_proposal.class.php:updateOrCreatePriceFournisseur`.

## Comparing available terms

The minimum-price enquiry selects a catalogue product and can be restricted to one supplier. It searches active parties and prices within their allowed entity scopes. With a positive desired quantity, an offer qualifies only when its minimum quantity is at most that quantity. A zero or unspecified desired quantity leaves the minimum-quantity filter unapplied. Each enquiry clears its prior selection.

For fixed prices the comparison amount is the supplier's net unit price multiplied by one minus its percentage discount. A successfully evaluated supplier price expression can replace the price before that comparison. Its calculated lot price is divided by offer quantity when nonzero. A strictly lower effective unit price replaces the current candidate. Equal prices keep the first encountered. The query supplies no secondary ranking rule for lead time, charges or supplier preference. The result exposes supplier identity and reference, chosen price-record identity, minimum quantity, price, discount, delivery days and currency information. A successful lookup with no candidate returns zero.

| Offer | Request for 8 | Request for 10 |
| --- | --- | --- |
| Supplier A, minimum 1, net unit 20, 10% discount | Eligible at 18 each | Eligible at 18 each |
| Supplier B, minimum 10, net unit 17, no discount | Below minimum | Eligible at 17 each |
| Minimum-price selection | Supplier A | Supplier B |

A different ranking is appropriate if the buyer must meet a delivery date, but the minimum-price operation itself compares price. Restricting the enquiry to supplier A would choose A in both examples.

Source location `htdocs/fourn/class/fournisseur.product.class.php:find_min_price_product_fournisseur`.

## Creating purchase lines from another document

The purchasing form accepts selected source line identities. Negative quantities and subtotal marker lines are skipped. For a supplier enquiry, a zero unit price omits the line. For a customer order, a zero sale price still permits procurement. A free promotional item sold to the customer can therefore cause a purchase. The supplier, origin and origin-line reference identify what the purchase fulfills.

For a supplier enquiry, the conversion uses the quoted line price, unit, quantity, discount, taxes and supplier item reference. For a customer order, the buyer selects a supplier. The form seeks the minimum effective eligible offer for that supplier and uses its identity and supplier reference. It obtains the purchase VAT in the supplier-to-company direction. It separately retrieves supplier price rows in ascending **raw** unit-price order without the minimum-quantity condition and takes the first unit price and discount. As a result, the stored purchase price can disagree with the selected price-record identity. For example, an order for eight with supplier A offering 20 from one and 16 from fifty may carry the first offer's reference and the second offer's unit price. In the absence of a qualifying offer the customer-order path initially resets the sale unit amount to zero.

The destination adds its own lines, including line description, product, unit, custom attributes and originating line identity. It stops adding lines when a destination line write fails. The supplier's minimum order value is surfaced on the purchase form as a warning. The value alone does not demonstrate that a submitted purchase has passed a supplier-side minimum.

Source locations include `htdocs/fourn/commande/card.php:1608–1732` and `htdocs/fourn/commande/card.php:2747`.

## Approval and submission

| Situation | Decision saved |
| --- | --- |
| Standard first approval below a configured threshold, or no threshold active | Records first approver and date and moves a validated order to approved. |
| Order net amount equals or exceeds the active threshold | First approval records the actor and date. The order stays validated until the second level is recorded. Equality activates both levels. |
| Second-level approval arrives first | Records second approver and date, leaves the order validated, then permits first-level approval to complete the pair. The stored fields represent two levels. The domain operation itself does not enforce different person identities. |
| Approved order placed with supplier | A user entitled to place supplier orders records the ordering method, placement date and optional comment. The new status is sent. An ordering event is emitted. |

The form can directly approve an order on validation when the actor has the approval right and settings allow it. Warehouse selection for approval-time stock and the option disabling direct approval alter that route. The approval operation requires purchase-order approval permission, records the stamp against a validated order, and may register the actor as an internal sales-follow-up contact. Only the transition completing approval can post an approval-time inventory receipt. With stock configured for that milestone, catalogue lines receive quantity in the selected warehouse. Valuation uses the line's net unit price after percentage discount unless weighted-average-cost settings exclude discounts. A failed stock movement or rejected approval event causes rollback.

Submission records how the buyer placed the order and emits the supplier-order-submitted event. The optional comment appends to existing private notes. Submission and physical receipt are separate milestones even in installations configured to recognize inventory at approval. Neither a first approval stamp nor submission alone proves that a supplier delivered.

Source locations include `htdocs/fourn/commande/card.php:1217–1238`, `htdocs/fourn/class/fournisseur.commande.class.php:approve` and `htdocs/fourn/class/fournisseur.commande.class.php:commande`.
