# Customer offers, revisions and acceptance

A customer offer records what the seller proposed to one counterparty, at the prices and conditions in force when its lines were written. The identity of a particular offer matters to a signer, a subsequent order and a billed-status decision. Changing a draft, cloning a proposal, accepting its terms and invoicing it have distinct effects.

## Building the offer

The editor requires the offer-creation right. The standard permission scheme grants validation and closure to a creator. Advanced permissions distinguish validation, closure, reopening and sending. Creating an order or invoice from the offer requires the corresponding destination permission. The normal editor also enforces minimum pricing unless the advanced permission to disregard it applies.

| Line input | Recorded outcome on a draft |
| --- | --- |
| Catalogue product or free description | The line stores its own wording and pricing. A catalogue identity supplies product context for stock, tax and packaging. Free descriptions can carry a service period without a product identity. |
| Quantity, unit, rank, parent | Quantity uses stock precision. A missing or negative parent becomes the root. A missing rank or rank of −1 appends after the last rank under the same parent. The unit and parent identify how to read the quantity and display position. |
| Start and end of service | Either may be absent. When present together, start must precede or equal end. A reversed interval fails before insertion. A negative product type also fails. |
| Net or gross entry, percentage discount, VAT and local taxes | The entered basis drives calculation. The line stores net, VAT, local tax and gross amounts after discount, and separates an optional VAT code from the rate. Gross entry preserves the gross unit amount for a later edit. Net entry stores zero in the gross-entry field. |
| Currency and cost | The line stores foreign unit price and totals separately from base amounts. Supplier-price identity and acquisition unit cost accompany the commercial price for use in margin calculations. |
| Optional item | A resulting zero quantity with no other special classification receives the optional-line code. An explicitly supplied classification takes precedence. |

With the stock sufficiency option enabled, adding a stock-managed item compares requested quantity against physical stock. It returns an insufficient-stock result and rolls back when the request exceeds stock. Customer packaging is applied **after** that comparison. For example, with five on hand and packs of three, a request for five passes that comparison and the stored quantity becomes six. Pack rounding works on magnitude and preserves a negative sign. With a positive pack size, even an input of zero can become one pack. An optional item therefore needs to be interpreted from the resulting quantity and classification. This operation quotes goods without reserving a warehouse balance.

Line edits recalculate amounts and ordinarily update the header totals. Moving a child to a new group can put it after the group's existing children. A client editing only wording should carry forward the intended price basis. Reconstructing a previously entered gross price from a rounded net amount can change the extended total.

Source locations include `htdocs/comm/propal/card.php:135–149`, `htdocs/comm/propal/class/propal.class.php:addline`, `htdocs/comm/propal/class/propal.class.php:updateline` and `htdocs/core/class/commonobject.class.php:roundQtyToPackaging`.

## Issuing and revising an offer

Validation changes a draft to the issued state and records the validating user and date. A provisional or missing reference is replaced using the customer's numbering context. An existing definitive reference survives. For a provisional reference the process also renames the document directory and updates indexed file references. The validation event can reject the transition.

Reopening and cloning produce different customer histories.

| Decision | Effects |
| --- | --- |
| Return the existing offer to draft | The original document identity survives. The draft operation clears the online signer name and IP address and emits a modification event. Its update leaves the signature date and stored file artifacts alone. |
| Issue a fresh revision by cloning | The new record gets its own identity, fresh reference, current offer date and creating user. Validation user is cleared. Expiration is recalculated by adding the original validity duration in days. Customer reference is cleared by default. A separate setting clears both notes. |
| Clone to a different customer | The new customer's payment terms, deposit and method supply the defaults. Delivery address and project are cleared. External contacts from the original are excluded. For a same-customer clone the external contacts are copied. The option to ignore contacts controls copying of internal contacts. |
| Refresh contents when cloning | Price refresh and description refresh are separate inputs. For a catalogue line, the refresh can replace unit price, VAT, discount and purchase cost. Free-text lines have no catalogue entry to refresh. With both features available the clone path considers an assigned price level before its individual-customer lookup. A qualifying individual price can supply its own percentage discount. |

For a clone with price refresh, a selected supplier-price record, if still present, supplies its discounted unit cost. A missing supplier price clears that reference, leaving cost determination to line creation. A newly negotiated customer price alone leaves an already-issued offer intact. Cloning without the refresh flag preserves the offer's existing commercial starting point.

Source locations include `htdocs/comm/propal/class/propal.class.php:valid`, `htdocs/comm/propal/class/propal.class.php:createFromClone` and `htdocs/comm/propal/class/propal.class.php:setDraft`.

## Recording a decision

Staff closure appends supplied private and public notes to their respective histories. Acceptance stamps the signature date, records the internal signature user and classifies the party as a customer. Refusal selects its own event. Automatic document regeneration uses the configured model for the outcome and can be disabled. An error updating the customer or handling the closing event can roll back the business transaction.

The public signature channel has a different evidence trail. It resolves the document link and requires an issued offer and a PNG signature. It writes a timestamped image. For a supported PDF it prepares a signed document and indexes the file. Formats without signature embedding can retain the signature image separately. The state change stamps the signature time and connection address and can also record the entered name and note. The update qualifies the offer by its current issued state. If a concurrent request has already changed that state, the later request cannot accept it a second time. The image or document may already exist because file creation precedes the conditional state change.

The public acceptance event and customer-role promotion are part of the database transaction. A file on disk alone consequently cannot establish that the offer was accepted. Public refusal uses a different sequence. It records the refusal, private note and response date, commits the record, then notifies the refusal event. An event failure there can coexist with a stored refusal. Readers tracing the decision need the document status, response metadata and artifact relevant to that channel.

Source locations include `htdocs/comm/propal/class/propal.class.php:closeProposal`, `htdocs/core/ajax/onlineSign.php:120–361` and `htdocs/public/onlinesign/newonlinesign.php:198–226`.
