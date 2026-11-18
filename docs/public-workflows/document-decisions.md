# Customer decisions and signed document copies

The public signing invitation identifies the document family, reference and, where applicable, organization. The recipient sees the counterparty and document reference. A customer offer also shows the gross amount, including the document currency alongside the organization currency where they differ. Opening or downloading the document is separate from submitting the decision.

## Which business record changes

| Invitation | Effect on successful signing | Independent business operation |
| --- | --- | --- |
| Customer offer | An issued offer moves to signed. The offer receives a decision date, source address and signer name when supplied. The signed-close event runs and the party is classified as a customer. | Order conversion, invoicing and collection each have their own operations. |
| Service contract | Writes the header signature state “receiver signed online” and raises the contract modification event. | Activation and expiration are maintained on the individual contracted services. |
| Field intervention | Writes the intervention signature state “receiver signed online” and raises the intervention modification event. | Service execution, time recording and billing have their own records. |
| Shipment | Writes the shipment signature state “receiver signed online” and raises the shipment modification event. | The shipment's operational state and movements of stock are handled by fulfillment operations. |
| Party bank account / mandate | Stores signature date, source address and optional signer name on the particular bank account record. A generated mandate can be the document receiving the signature. | A withdrawal request, bank file and collection result are separate from mandate evidence. |

The shared signature state dictionary uses 0 for unsigned, 1 for sender-signed, 2 for receiver-signed, 3 for receiver-signed online and 9 for all signatures. The contract, intervention and shipment paths set the field to 3. It is a single classification field. It does not accumulate the individual parties' signatures as independent approvals or automatically progress from 1 to 9. An implementation that needs to answer who acknowledged a particular version must retain the corresponding document evidence.

Supported families and offer amounts appear in `htdocs/public/onlinesign/newonlinesign.php:163–185,340–384`. The effects are in `htdocs/core/ajax/onlineSign.php:303–360,479–497,619–636,812–850,968–987`. Common signature-state values and persistence are in `htdocs/core/class/commonsignedobject.class.php:46–55,129–166`. See [Contract services](../specification/people-and-services/contract-services-and-work-templates.md) and [Shipment signatures](../specification/equipment/carriers-delivery-notes-and-signatures.md) for operational status changes.

## Offer acceptance, refusal and repeated decisions

An issued proposal is presented for a decision against its current main document. Where the original is missing, the page can request the standard document generator. On signing, the recipient draws the signature and can enter their name. The save button becomes available after a signature is drawn. Clearing the drawing disables it. A failed save displays an error. The successful save returns to the record's confirmation view.

The offer must be issued when the acceptance operation starts. The actual status update checks that it is still issued and requires an affected record. If staff have already changed the state or another acceptance won the race, a second signed transition cannot claim the same offer. The signed-close event and customer classification run before the business transaction commits. A failure in this sequence rolls back the status change. Signature files are written earlier and have their own lifecycle, so the stored offer state is the source of truth for acceptance.

Refusal is a separate choice. The page asks the recipient to confirm, records the refused state and decision date, and emits the refused-close event after committing the change. A rejection does not require a drawing. On return to an accepted or refused offer the page distinguishes the result just submitted from a previously recorded outcome. A signature date by itself is therefore insufficient for “accepted on” reporting. Always interpret it with the outcome.

For example, three issued offers are opened on Tuesday. One is downloaded, one is explicitly refused and one is signed. The first is still issued with no new decision. The second and third can both have Tuesday decision dates, but only the third qualifies as customer acceptance. None of these public operations creates an invoice. [Offer revisions, conversion and commercial state](../specification/commercial/customer-offer-lifecycle.md)

The public offer presentation and refusal are in `htdocs/public/onlinesign/newonlinesign.php:198–225,250–256,384–433,711–724,736–787,790–814`. The eligibility check, evidence and conditional write are in `htdocs/core/ajax/onlineSign.php:125–161,285–361`.

## The signed artifact

The captured signature image and the signed copy have separate identities. For a supported PDF source, the standard process imports the source document, places a signature onto the appropriate page or pages, writes a dated derivative and indexes it as the new main document. It retains the original. In the offer path, the configured specific page, all-pages option and the document's signature-page metadata participate in placement. With no page supplied by configuration or metadata the final page receives the signature. The image is accompanied by a date and the submitted name. The release has no corresponding image-insertion operation for an OpenDocument text file.

After an offer has been accepted or billed, the public display checks that the indexed main file is identifiable as a signed copy and compares its modification time with the unsigned source. A newer available signed copy can be offered for download. If someone regenerates the original later, file dates and the offer's signed status can describe different versions. Reproducing the signed terms requires preserving the copy that actually received the signature.

Bank mandates have additional source selection. The standard mandate model identifies the source by the bank reference and unique mandate reference. For other bank PDF models the signing operation uses the last generated main PDF and derives a dated signed filename from it. It indexes the new file against the account-related document. This distinction matters where a party has multiple bank accounts or a deployment uses a different bank document model. A signed mandate relates to one account record.

For an intervention, contract or shipment, use the signed document and signature field to establish receipt. The public return screen uses a successful-return message for contracts and interventions. An ordinary later visit can again present the signing control. Its appearance alone does not establish whether an earlier signed copy exists. The shipment screen also consults the sender-signed classification when it decides what to display. These public page rules differ from the issued-offer state gate.

File selection, placement and indexing appear in `htdocs/core/ajax/onlineSign.php:164–179,204–292,393–404,479–496,533–539,618–635,681–703,791–806,887–905,968–986,1009–1024`. The public copy and return-state rules appear in `htdocs/public/onlinesign/newonlinesign.php:404–429,553–588,792–836`.
