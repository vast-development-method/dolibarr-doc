# Document model selection, template data and delivery

## Resolve the model for an existing record

| Source document | Model resolution when a caller omits a model | Source relationships loaded |
| --- | --- | --- |
| Customer invoice | Saved invoice model, then configured model for that invoice type, then the general invoice default, then the built-in standard invoice form. Thus a credit note can have a different default from a standard invoice. | Invoice model gets the invoice, language, detail visibility switches and optional context. |
| Customer shipment | Saved shipment model, shipment default, then the built-in delivery note. | Loads the shipment origin before invoking the renderer. |
| Supplier reception | Saved reception model, reception default, then the built-in receipt note. | Loads the source when both an origin type and positive origin identifier exist. |

An explicit model overrides these fallback chains. The shared renderer accepts a model name and optionally a source template file. It searches installed model locations for the source document family. For a generic office document with no explicitly selected file it scans the configured directories in their listed order, collects supported files sorted by name within each directory and takes the first. Supplying a template file outside the supported document/template locations, referencing a missing file or selecting an unavailable generator results in a generation error. An installation extension can handle the generation request before the default selection executes.

On a successful write the renderer restores the output language's character set, removes stale previews and passes the returned output path to the document index when the file exists. A generator can request that this file become the source record's last main document. The optional metadata sidecar summarizes the current document when enabled. A generator can report success without returning a usable full path, in which case the document index update does not occur. A subsequent send operation therefore cannot infer the attachment solely from the fact that an earlier generation call succeeded.

The [customer invoice document lifecycle](../../document-lifecycle/README.md) follows a replacement file through indexing, language changes, mail and removal.

## Populate an editable invoice template

The invoice office-template model produces both header-level values and a repeating line segment. Common substitution values are merged with properties of the invoice, the user producing it, the issuing organization, the invoice party, and, when found, contact and proposal data. If several linked proposals are available, the template takes the first linked proposal from its retrieved list. A template field referring to a proposal cannot be assumed to describe all the orders or proposals contributing to a consolidated invoice.

The model derives previous, current and next month and year labels from the invoice date. A document generated in January for an invoice dated the previous December still receives December as the invoice month and January as the next month. It additionally calculates the operation classification from ordinary goods and service lines. Deposit application lines are excluded when deciding whether an invoice contains goods, services or both. Free text can receive its own substitutions. Translated labels follow the document output language.

For each invoice line the repeating segment receives a fresh line-value set and line number, enables line-specific substitutions and merges the resulting row. Fields absent from the supplied template may simply be unused. Failure to merge the completed segment or save the document yields a generation error. Output can remain editable or be converted to PDF under the office-output option. The generic invoice template receives the standard detail-hide, description-hide and reference-hide parameters, but its substitution loop does not branch on these switches. The fields included in the office template determine what the recipient sees. Rules belonging to a fixed-layout PDF model do not automatically redact an editable template.

## Prepare and send a record's document

The mail composer inspects the source record and its linked party. For ordinary business documents it prefers the readable file recorded as the last main document, with a fallback to the source's document location. Under multilingual operation the party language and explicit composer choices determine the language used. Selecting a different email template or adding and removing attachments changes the draft before sending. The send action is suppressed while the request is selecting a model, manipulating attachments or cancelling.

Recipients can come from directly entered addresses, the selected party, a linked contact and, where enabled, internal user selection. The composer keeps copies distinct from primary recipients. The actual send expands common and source-specific substitutions in **both** subject and message immediately before submitting mail. The available values include sender signature and resolved recipient addresses. An empty recipient set and an unreadable source object produce explicit failures.

A successful mail submission precedes the database transaction for post-send effects. That transaction prepares the event type, message and short description, source type and identifier, party/contact links, attachment references, tracking information and mail metadata. An option can replace the event title with the message subject. The invoice-sent event increments the invoice's sent counter and passes the business event to registered modules. A failing event handler rolls back the post-send transaction, but the mail may already have left the sender. A resend can consequently deliver a second copy despite the absence of an event or increment from the first attempt. Returning to the card after a successful send reduces accidental repeat submissions during normal navigation.
