# How to establish whether an invoice was sent

The customer asks for invoice INV-104. Its sent counter is zero, but the mail relay has a queued message with the invoice attached. Both records can be correct. Mail submission takes place before the transaction that updates the invoice and records its send event.

## Follow one submission

1. The document send action takes the sender, recipients, subject, body and attachments from the prepared message. A selected filename identifies the file read for this attempt. The [document lifecycle](../document-lifecycle/README.md) explains regeneration, substitution language and the file index.
2. The mail service selects the transport for the sending context. A negative send-hook result aborts. A replacement hook returning one reports success and assumes responsibility for delivery. The standard transport is skipped in that case.
3. The socket transport submits the sender and each envelope recipient. A refused recipient stops this transport before message data. A data-ready reply allows the body and attachments to be transmitted. The positive reply **after the end of data** records the relay accepting responsibility for this message. A request for a delivery or read receipt is a header in the submitted message. A receipt itself is a separate communication.
4. On send success the document action starts its database transaction. It carries the message ID, sender, recipients, subject, message body, track identifier and attachment descriptors forward. For an invoice with the send event enabled, it increments `facture.email_sent_counter` and emits `BILL_SENTBYMAIL`. A negative subscriber result rolls back that transaction. The mail already accepted by the relay remains there.
5. A transport failure returns to the compose view and skips the invoice post-send transaction. After transport success the action queues a success notice and redirects. A subscriber error can leave both that notice and a post-send error. Inspect the persisted invoice and activity records when the messages disagree.

## What the same invoice can leave behind

Each row starts with counter 0, one recipient and the same PDF. The invoice action's post-send block and normal socket mailer were exercised against a private relay and a transactional store. A controlled subscriber recorded receipt of the event or returned an error. The replacement-hook row exercises a handler that explicitly reports success without opening a transport connection.

| Condition | Message bytes accepted by the relay | Persistent invoice counter | Committed subscriber record | Operator result |
| --- | ---: | ---: | ---: | --- |
| Relay accepts the complete message and the subscriber succeeds | 1 | 1 | 1 | Success notice and redirect |
| Relay accepts, then the subscriber reports an error | 1 | 0 | 0 | Post-send error and success notice. The database change rolls back. |
| A replacement hook reports success and supplies no transport | 0 | 1 | 1 | Success notice. Delivery evidence belongs to the hook. |
| Relay refuses the envelope recipient | 0 | 0 | 0 | Warning and return to compose. No message data was transmitted. |
| Relay stores the message, then the connection drops before the sender receives the acknowledgment | 1 | 0 | 0 | Warning and return to compose. A repeat can submit another copy. |

In a separate trial the relay received the entire body but returned a temporary storage failure after the end of data. The mailer returned failure, opened one connection and made no automatic retry. For each stored message the relay recovered the named attachment and its content digest matched the original PDF. The receipt-request header was present. This establishes the recipient-side payload at the controlled relay. Establishing delivery to a customer mailbox calls for the downstream delivery result, and establishing that somebody read a message calls for separate recipient evidence.

## Reconcile a disputed send

| Observation | Record to inspect and action it supports |
| --- | --- |
| Counter is zero and the operator saw a transport warning | Match sender, recipient, message ID if available, invoice reference and attachment to relay history. A refusal before message data and a missing acknowledgment after storage can produce the same invoice state. |
| Relay has the message, while invoice history is empty | Check the post-send transaction and subscriber result. Restore an accurate correspondence record under the organisation's policy. Resending constitutes another delivery attempt. |
| Invoice history contains a send, while the normal relay has no message | Check which transport or replacement handler owned the send. Its handoff record is the evidence for that channel. |
| Recipient has a PDF in a different language or with a different amount | Compare the actual transmitted attachment or its digest with the retained document, the invoice identity and its rendering language. Regenerating the current file can give different bytes at the same location. |
| Recipient denies receipt after the relay acknowledged the body | Use the queue reference, recipient-specific final delivery or bounce, and, if provided, a recipient acknowledgment. Each belongs to a different step. |

A fresh submission can assign a fresh message ID to the same invoice and attachment. In the controlled lost-acknowledgment case a successful repeat produced a second stored message. The invoice reference connects both attempts to their business document, but does not make sending idempotent. [Send history and retention](../document-lifecycle/README.md) · [Mail campaigns and recipient records](../communications/email.md)
