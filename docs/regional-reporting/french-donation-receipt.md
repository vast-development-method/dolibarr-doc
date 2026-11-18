# French donation receipt and its source records

The donations module registers a French HTML receipt model identified as Cerfa 11580*04. The entity can choose a different model. The generated artifact is a document for the donor. Issuing the artifact, settling the pledge, posting a bank movement and submitting a return to an authority are distinct operations.

## Selection, authority and identity

When the caller supplies a model, the donation uses it. Otherwise it takes the saved model on that donation, then the entity default, with the French model as the built-in fallback. The model declares itself enabled independently of the issuing country's code. The donation card's document widget offers generation to a donation reader when the donation is unpaid or the user is an administrator. The common document-build action also checks creation authority or an explicit generation capability. The widget's visibility alone is insufficient to establish that the generation action will admit a request. The writer creates the ordinary output directory from the sanitized donation reference and writes an HTML file of the same reference. The number printed in the receipt's sequence box comes from the donation's internal ID. A specimen follows a separate fixed output name.

The donation owns its recorded donor identity and optional party link. When a linked party loads successfully, the writer uses its name only if **all three** stored donation name fields are blank after trimming. A party's single name goes into the organization/name slot, including when that party represents an individual. The first-name field remains as recorded on the donation. For address, postal code and town, fallback occurs independently for each missing value. A donor can therefore have the donation's originally entered street and the currently linked party's town in the same regenerated receipt. When both organization and surname are present the renderer separates them with a line break. A failed party lookup or a completely blank name is logged. Those conditions alone do not terminate the writer.

| Output fact | Source and effect |
| --- | --- |
| Recipient organization | Current issuing company's name, address, postal code, town and stated purpose. These can change after the donation was entered. |
| Donor | Stored donation identity and per-field party fallback as described above. |
| Receipt sequence | Donation row ID. The output filename uses the sanitized public donation reference. |
| Amount | Stored donation amount, both as formatted digits and spelled out. The writer does not sum received instalments or consult the bank to produce it. |
| Date of transfer or gift | Donation date. The date by the signature area is the date of document generation. A second generation on another day can produce a different signature date. |
| Article selections | For a French issuing company the three independent entity flags govern the printed checkboxes labelled 200, 238 bis and 978. Each defaults to off. A non-French issuer produces empty replacements for those boxes. The fixed French template still contains its explanatory text. |

## Fixed layout, language and money

The body of the distributed template is French. It supplies a literal euro unit alongside the numeric amount, and the number-to-words routine defaults to French euro and centime units. Although the writer prepares currency-name and currency-code substitutions, those slots are absent from this template. Selecting a different currency label does not convert the amount. A multilingual or multicurrency consumer therefore needs to model the **actual selected document** independently of the donation's monetary configuration.

The writer selects a payment-mode ID stored on a fetched donation, then the form's mode ID as fallback. The dictionary code maps cheque to the cheque box, cash to the cash box, and bank transfer, debit or card to a shared electronic-payment box. An unrecognized mode leaves all three choices unselected in the prepared fragment. In this release the distributed layout requests `__ModePaiement__` while the writer substitutes `__DONATION_PAYMENT_MODE__`. The general translator handles the different parenthesized translation syntax, and the plain-text mode label is inside a template comment. Consequently the file generated from this exact template does not show those prepared mode checkboxes as intended. The monetary gift-type checkbox in the fixed form is preselected. Neither checkbox block is evidence of a payment allocation.

## Reconcile a donor's copy to the cash book

Consider a pledge for 250 recorded on 4 March. The donor has paid one instalment of 100 on 12 March. An authorized operator generates the receipt on 19 March while the pledge is unpaid. The receipt's numeric amount is 250 and its gift date is 4 March. The signature area shows the generation date of 19 March. The separate payment and bank records support 100 of cash, leaving a pledge balance of 150. The receipt operation has no path for allocating the outstanding 150 or changing the reported payment date. If the operator regenerates after a linked party's town has changed and the donation stored no town, the document can acquire the new town. The stable evidence of a copy already supplied is the generated file itself.

Sources are `htdocs/core/modules/modDon.class.php:68–105,157–170`, `htdocs/don/card.php:98–105,367–373,939–950`, `htdocs/core/actions_builddoc.inc.php:65–109`, `htdocs/don/class/don.class.php:1052–1074`, `htdocs/core/modules/dons/html_cerfafr.modules.php:46–68,79–113,126–146,157–231,246–284,304–326`, `htdocs/core/modules/dons/html_cerfafr.html:30–39,58–65,183–199,215–255,298–303` and `htdocs/core/lib/functions.lib.php:11082–11129`. See [donation creation, payment and closure](../engagement/membership-and-donations.md).
