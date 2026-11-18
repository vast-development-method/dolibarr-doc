# Service reads that change business records

Of the 627 effective routes, 304 use GET and reach 261 different handlers. Five of those handlers explicitly request a persistent business change or generate a document. A caller deciding whether to repeat a request needs the operation name and the last durable step. The [route register](routes.csv) gives the path and argument bindings. The [write register](../service-writes/README.md) covers the other 323 routes.

| Operation | Effect of a successful call | What matters on failure or repeat |
| --- | --- | --- |
| [Export ledger entries](accountancy.md), `exportData` | Selects eligible bookkeeping legs, ordinarily marks each one's `date_export`, invokes the file writer and returns a download description. | A file-generation error rolls back pending markings. A missing download description or an unexpected output directory is detected after commit. A failed request can therefore remove legs from an ordinary repeat selection. |
| [Clone a campaign](mailings.md), `clone` | Creates a new draft campaign. The content and recipient-copy switches both default to enabled. Target rows are associated with the new campaign identity. | A repeat that generates the same title in the same entity can fail on uniqueness. A later successful copy has its own identity. The final read can also refuse access after the clone commits. Inspect campaign and target identities before retrying. Cloning the recipient list does not send the campaign. |
| [Generate a party bank document](thirdparties.md), `generateBankAccountDocument` | After checking access and party write rights, requests a change to the party's `model_pdf`, selects the party's bank record and renders the document in the party's entity output directory. | The model write precedes bank lookup and its return value is unchecked. A missing account can return 404 after the model changed. Omitting the bank record uses the first fetched account. The selection has no ordering clause. Supply the bank record identity to select a particular account. |
| [Assign a user to a group](users.md), `setGroup` | Resolves the permitted entity and replaces the matching user/group/entity membership within a transaction. The writer dispatches `USER_MODIFY`. | A second successful call can leave exactly the same membership and dispatch the event a second time. Membership count and subscriber execution count measure different things. |
| [Reset an authorised user's password](users.md), `setPassword` | When the login and reset settings and applicable permission allow it, generates and saves a new credential. Optional notification follows the save. | A mail error can return 500 after the credential changed. Repeating the operation generates another credential. [Acting identity and credential lifecycle](credential-lifecycle.md) |

## Two marked ledger legs and a failed download

The export right, company scope, period and format determine admission. With `alreadyexport=0` the movement query selects only rows whose `date_export` is null. The selected rows are sorted by piece and row identity. The `lettering` switch controls whether matching codes and dates reach the writer. It does not erase the stored reconciliation values.

An isolated execution ran the export handler with two eligible journal legs, a controlled movement selector, a transactional store and a controlled file writer. A separate read of the two persisted rows distinguished generation from marking.

| Condition | Rows given to the writer | Marked legs after the request | Caller outcome |
| --- | ---: | ---: | --- |
| Writer rejects the export | 2 | 0 | Error, pending updates rolled back. |
| Writer succeeds with marking suppressed by `notnotifiedasexport=1` | 2 | 0 | Download description returned. |
| Writer reports success but omits download metadata | 2 | 2 | Error after commit. |
| Ordinary repeat after the preceding error | 0 | 2 | Both marked legs were excluded from selection. |
| Repeat with `alreadyexport=1` | 2 | 2 | Previously marked legs were eligible again. |

To reconstruct a disputed export, match the journal row identities, their export marks, the file actually retained and the recipient's acknowledgment. A retry that includes marked entries can produce the same financial legs twice. [Ledger layouts](../exports/ledger-layouts.md) · [Evidence of filing](../operating-boundaries/settlement-and-declarations.md)

## What a fresh read found after the other four operations

Twenty-four controlled executions exercised the service handlers with their campaign, membership, credential and document-model writers. A second connection read the stored records. Access decisions, test credentials, clock, subscriber results, output file and delivery sink were controlled. The campaign runs included its actual target and count writers.

| Operation | Input and observed outcome |
| --- | --- |
| Campaign | The default copy had two recipient rows. A copy with content, recipients and triggers suppressed had a blank body, no targets and no creation event. Two copies that generated the same title in the same entity hit the unique key. In another run, the caller could write but lacked the final read permission. The service returned 403 and the new campaign and targets were already committed. |
| Campaign targets | Rejecting the second recipient insert left a successful clone with one persisted target and a stored header count of zero. Failure to read the source target list instead returned 500 with a transaction still open. Only the writer could see the new header until the outer transaction was resolved. Explicit rollback removed it. |
| Bank document | Selecting another party's account returned 404 after the chosen model persisted. A render failure also preserved the model. An explicit owned bank record reached the renderer. With no account supplied the renderer received the first fetched account. A failed model write still allowed the renderer to report success. |
| Group assignment | A user bound to entity 2 requested membership in entity 7. The writer assigned the group in entity 2. Replaying the call replaced the membership row and emitted another event. A subscriber veto returned 500 and restored the prior row identity. A global administrator in transverse mode could select the requested entity. |
| Password change | A disabled operation or missing grant preserved the credential. A veto during the credential-change event rolled back the change before sending. Failure in optional delivery returned 500 after the new credential had committed. Successful responses were 1 for saving alone and 2 for saving with accepted notification. |
