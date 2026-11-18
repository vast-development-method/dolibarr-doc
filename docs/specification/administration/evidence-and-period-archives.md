# Financial event evidence and period archives

A financial event record captures selected facts at a business transition. The invoice's live state, its file attachments, the message sent about it, a bank transaction, an event-delivery receipt and an archived financial event each answer different questions. The journal captures configured event families, including invoice validation and transmission, customer payment creation and deletion and applicable cash-control events. It does not snapshot every routine edit to every enterprise record.

## Event payload and ordering

The retained event records its event kind, source module and point-of-sale context when applicable, affected object type, identifier, reference, business date, event creation time, actor and amounts. The version and format identify how to read the stored object representation. For invoice evidence the snapshot can retain commercial-party and issuer details and identifiable invoice-line facts. Payment events can carry the related references and amounts. A deletion event records a reversal according to the event's signed-amount convention. A payment creation and its deletion therefore remain distinct occurrences even when their net financial effect is zero.

Business date and log creation time are independent. An invoice dated March 30 and validated April 2 can contribute to commercial March reporting while its validation evidence is recorded in the April archive. Editing a party afterwards changes its current master record. Archiving the captured event uses the stored representation rather than rebuilding the invoice from the party's present address or current prices.

A new event obtains its predecessor and computes its signature from the preceding signature and the event's signed content. The predecessor query can lock the prior database row while extending the chain. Completion or rollback releases the transaction's lock. The chain also maintains a last-record marker in its configured storage. A failure maintaining the required evidence can make event creation fail. For a business operation whose caller handles a negative trigger result transactionally, that is a reason the originating transition can fail too.

A row identifier, signature and predecessor together give evidence about **sequence**. Identity and business date alone do not determine sequence when several documents share a date or a prior-period instrument is entered later. Cash collection for a March invoice in April produces another event with its own business meaning and predecessor. It does not overwrite the validation record.

## Selecting a period and preserving boundaries

An archive selection is for one entity and a calendar month or year. It requires the read/export entitlement on the export action. The period selection uses event **creation time**, with inclusive UTC database bounds. Sort by creation time, then row identity. The first selected row obtains its predecessor from outside the selected range where necessary. If the month is empty the archive path explicitly identifies that there was no data from which to load a predecessor.

The exporter checks rows in order, advancing the predecessor signature as it goes. To assess the far boundary it can inspect the next record following the archived range, or the chain's end marker when the exported period reaches the current tail. Period validation therefore involves the boundaries as well as rows printed inside the file. A single isolated row cannot establish the completeness of a month. The archive carries event identifiers, references, actor, amounts, links, payload, format version and signature, along with period and export metadata.

The export writes a file-level content digest and a keyed digest to the final trailer. These apply to the archive bytes written before that trailer. Event signatures describe continuity of records. The file digest describes a specific exported representation. Two exports covering the same completed month can have different export metadata and file digests while referring to the same underlying financial events.

## Complete, incomplete and failed exports

| Outcome | Retained meaning |
| --- | --- |
| Completed historical period | The file is produced with completed-period identification. The exporter records a new archive-export event in the financial journal. That event occurs when the export is performed and carries the requested period. |
| Current or future-ending period | If the selected period end has not passed, mark the file incomplete and warn the operator. The completed-export event is reserved for completed periods. New business events may still fall within the selected month. |
| Cannot record the completed export | Failure preparing or inserting the export event cancels the export and removes the generated file in that branch. The existence of underlying financial events remains a separate fact. |

For an April 2 validation, an April export taken on April 15 is incomplete even if the invoice was already fully paid. An export taken after April closes includes events that arrived later in the month. The completed export leaves its own audit event at the later export time. Export is a copy operation. It does not impose a new deletion date on the source record, attachment or financial journal.

Scheduled privacy cleanup targets configured objects and fields using the object's own delete or update operation. For anonymization it can retain the business object's identifier, replace designated master fields and transform custom fields marked personal. That process changes the records selected by the configured policy. The financial archive logic is a separate operation and reads previously captured event data. A redacted current contact therefore does not establish that an earlier signed invoice snapshot, delivered message, indexed document or exported file was also redacted. Conversely, retaining a financial archive does not prove the current contact record still contains those details.
