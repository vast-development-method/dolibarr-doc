# Delivering an offer, order or invoice

Commercial correspondence starts from one document. A sales user selects a template, resolves recipients, attaches files and submits the composed message. Business-event subscriptions and campaign lists are separate recipient sources with their own persistence rules. A recipient may appear in more than one channel.

## Selecting a template

The document composer searches templates applicable to the document type, its send-specific type and the all-documents type. Candidates must be visible in the relevant entity scope. Public templates are available to the operator and private templates require ownership. Active state, default-for-type and label can narrow the selection. A record attached to a disabled module is skipped. A selected template can carry subject, sender, To, CC, BCC, body, line content and an attachment preference.

Without an explicit template identifier, the resolver admits the output language, a derived main-language locale and a language-neutral row. For Spanish as used in Mexico this can admit both Mexican Spanish and Spanish as used in Spain. Selection orders **position first**, followed by language and label. A neutral template with a lower position can therefore win over a localized one. A positive explicit identifier bypasses the language-selection predicate while retaining template visibility, scope, type and other applicable filters. Selecting the document's language and selecting one specific template are independent decisions.

The template supplies the starting composition. The sending path receives the final subject and body and assembles substitutions for the document and recipients. The attachment sent is the file in the attachment list. Regenerating the quote or selecting a different output language later does not update an already submitted message.

## Resolving who gets the message

The main recipient assembly accepts a typed address list, prefilled addresses and selected identities. The current party choice uses the party's stored email when present. Selected contact identities retain their contact link for the resulting business event, and configured internal-user selection can retain user identities too. A typed standalone address can receive the message without creating a contact. The sender must resolve at least one primary recipient. A populated CC field alone does not enter the sending branch.

The composer resolves CC separately. Selected copy recipients need not have the same persisted contact linkage as selected main recipients. BCC combines manually supplied addresses with the per-document automatic-copy setting. Automatic-copy destinations for offers, customer orders and invoices are independent. Tracking uses the document kind and identifier. Sending a revised copy of the same document therefore still relates to the same business document.

Suppose a sales user sends a quote to a purchasing contact, adds a shared finance mailbox in CC and has automatic offer copies configured for an internal archive. The primary contact can appear as a linked recipient, while the CC and BCC addresses remain in message metadata. A subsequent invoice to the same party uses its own automatic invoice-copy destination. Membership of a campaign's unsubscribed address list does not by itself specify whom an operator selected on the individual document's sending form. The individual send branch builds its addressing directly from the composition.

## Transport acceptance and business history

The shared send operation hands the message, attachments and recipients to the mail transport. Successful submission precedes recording the business event. The event context can carry the message identifier, headers, addresses, subject, selected recipients and document attachments. The offer, order and invoice emit distinct sent-by-mail events. Invoice sending also increments the invoice's sent counter in the business-history transaction. On failure of that transaction, the database can roll back after a mail server already accepted the message. A zero counter or missing sent event cannot conclusively establish that no invoice was sent.

A successful request redirects away from the sending form, reducing accidental repeats through browser navigation. A fresh submission can still deliver another copy. A transport refusal, a later failure to store the sent event and a recipient failing to read a delivered message are distinct outcomes. The event describes the submission. A recipient delivery or read acknowledgment requires its own evidence.

## Subscribers to a business event

An enabled notification listens for a specific business-event code. Contact subscriptions join an active contact and a subscription for the affected party and event. User subscriptions join an active internal user and their event definition. Each result supplies the recipient, target type and preferred language. A blank email cannot yield a delivery. Administrators can also configure fixed destinations per event, including supported recipient tokens. A fixed event with an amount threshold can suppress a nonzero document net amount at or below the threshold. The conditional comparison explicitly requires a nonempty net amount, so a missing or zero total does not take that suppression branch.

The notification sender prefers its configured notification address, falling back to the ordinary outbound address. Template rendering on validation uses the definitive reference when available, even when the source object still carries a provisional reference. A successful send writes a notification record with timestamp, event, party where applicable, document type and identity, target type and actual address. A failed transport increments the error result. Notification rows describe individual successful submissions. Separate subscriptions to a business event and a direct document send can produce separate messages to the same mailbox.
