# Processing incoming mailbox messages

A mailbox collector processes one message at a time. An accepted message can identify a customer, create or reopen a ticket, record an agenda event and store documents. The mailbox UID identifies a message within its folder. The message's `Message-ID` connects it to saved business records and replies. A successful database write and a successful move to the destination folder are separately observable outcomes.

## Stored configuration and selection

| Record | Fields that govern processing |
| --- | --- |
| `emailcollector_emailcollector` | The entity, active state, host, login, connection settings, `source_directory` and optional `target_directory` identify the mailbox. `maxemailpercollect` limits successful messages. The run records `datelastresult`, `lastresult`, `codelastresult` and, on a successful production pass, `datelastok`. |
| `emailcollector_emailcollectorfilter` | `fk_emailcollector` points to its collector. Each active `type` and `rulevalue` contributes a mailbox search condition or an in-process test. |
| `emailcollector_emailcollectoraction` | `fk_emailcollector` identifies the same parent. Each active `type` and `actionparam` runs in ascending `position` order. Positions should distinguish actions whose order matters. |

The scheduled job selects active collectors. A collector requires a host, login and source folder. It begins with undeleted messages. When a last-success marker exists, the default mailbox search starts one day before that marker. A setting can suspend the date filter when a target folder is configured. The library-based adapter also limits the initial fetch to the collection maximum. Selected candidates are sorted by the parsed message date, oldest first. The processing loop separately stops after the successful-message limit or once the processed counter exceeds 1,000. An old message can be selected again, even when the collector previously completed successfully.

### Filter decisions

The setup offers 21 filter types. A stored `header` rule also has a runtime branch. Enabled tests accumulate. Provider search semantics apply to server-side criteria, while local tests use the decoded message and parsed headers.

| Filter type | Actual decision |
| --- | --- |
| `from`, `to` | Search the corresponding address field for the value. An asterisk splits the value into separate search terms that must all match the field. A leading exclamation mark negates each search term. |
| `cc`, `bcc` | The library adapter supplies the search term with its criterion. The native adapter emits the criterion without its operand. A provider can reject that search. |
| `subject`, `body` | Positive terms enter the mailbox search. With a leading exclamation mark, a local case-sensitive literal match on the decoded subject or extracted body discards the candidate. |
| `replyto` | If `Reply-To` is present, it must contain each configured literal. A message without this header passes this particular check. The local loop does not apply a negation operator. |
| `excludeemail`, `excludedomain` | Split values on commas, semicolons or line breaks and normalize case. A match on any address extracted from From or Reply-To discards the message. An excluded domain also matches its subdomains at a dot boundary. These controls act on senders and reply destinations. |
| `seen`, `unseen`, `answered`, `unanswered` | Add the corresponding mailbox flag criterion. The server's answered flag and the collector's reply classification can differ. |
| `smaller`, `larger` | The configured operand is a size in bytes. The native adapter includes it in the criterion. The library adapter builds a size criterion without its operand. |
| `withtrackingid`, `withtrackingidinmsgid`, `withouttrackingidinmsgid` | All three enable the same positive post-filter. It accepts a recognized tracking suffix in the recipient or message ID, or a References or In-Reply-To header containing the configured host signature. The control labelled “without” in this pair also selects tracked messages. |
| `withouttrackingid` | Excludes a recognized tracking suffix or a matching host in the two reply headers. |
| `isanswer` | Accepts a supported localized reply prefix in the decoded subject, a recognized signed reference on the configured or alternate host, or, when enabled, a nonempty In-Reply-To header. |
| `isnotanswer` | Discards a recognized reply prefix. Settings can also make nonempty References or In-Reply-To sufficient to discard. Its References test differs from the signed-reference check above. |
| `header` | Implements a mailbox header search from a stored rule. The setup selector omits this entry. |

The subject can therefore pass the answer filter without identifying an individual ticket. Conversely, an external Message-ID found among saved ticket references can identify a ticket independently of the subject.

## Building the message context

The collector unfolds headers, decodes the subject, separates the envelope addresses and extracts message body and attachments. It recognizes lowercase variants of Message-ID, References, In-Reply-To and Subject. It removes angle brackets from the current message ID. After the local exclusions, it begins a database transaction, clears the previous message's record identities and resolves the current message.

1. The recipient's recognized object suffix takes precedence over the current message ID's suffix. Otherwise the handler examines signed identifiers in the ordered References entries, including the alternate configured signature. The candidate list also includes the current Message-ID.
2. For an external reference, the collector first searches the ticket's `email_msgid` or stored `origin_references`. It can next search project and recruitment application `email_msgid` when those modules are active. An In-Reply-To detected by the filter does not itself enter this References list.
3. A fetched object supplies its own typed identity and related organisation, contact or project where available. A matched ticket supplies its tracking key and may have its stored reference history supplemented. If linked identities are missing, the collector looks up the sender as a contact, the contact's organisation and then an organisation with that sender address.
4. Each action receives that message's resolved context. A preceding organisation lookup or creation can supply the organisation to a later project, ticket or event. A property action can modify its own object and some operations also change the working sender or loaded contact. A newly created ticket or project has its own local creation object. An arbitrary later action must not infer its typed target merely from its position after a create.

## Action types and record effects

| Action | Selection, write and repeat behavior |
| --- | --- |
| `loadthirdparty` | Reuses an already resolved organisation. Otherwise evaluates its configured ID, name, alias or email and asks for the nearest match. A configured fallback organisation can handle an ambiguous match. On a miss it can resolve an organisation through a matching contact. An unresolved load is an action failure. |
| `loadandcreatethirdparty` | Uses the same identification rules. On a miss it initializes an organisation from the derived details, applies property assignments and invokes creation. Later actions can use the loaded organisation. |
| `recordevent` | Looks up an agenda event by `email_msgid` before insertion. A new event records the message date, addresses, subject, content, project, organisation, contact and applicable typed target. It normally uses the incoming mail event type. A sent folder or configured sending address can select the outgoing type. An existing event bypasses insertion. |
| `recordjoinpiece` | Extracts attachments and searches for nonempty business references occurring in the subject. Each fetched matching record can contribute a document directory. The operation attempts to save files for every selected directory. Missing attachments, unresolved objects and some file failures are added to the diagnostic list independently of the per-action rollback flag. Inspect files as well as the reported run state. |
| `project` | Offered when projects are enabled. A project found by `email_msgid` bypasses creation. A new project starts from the resolved organisation/contact, subject, mail date, body summary, private detail and prospect opportunity status and probability. It applies overrides, obtains a project reference and saves attachments on the creation path. |
| `ticket` | Offered when tickets are enabled. Tries the resolved ticket object ID, derived ticket ID, tracking key and current Message-ID in that order. A positive lookup changes this action into `recordevent` for this message. With no match it creates a ticket with subject, body, originating addresses, reference history, message ID, project and organisation context. Configured defaults or the default dictionary entries supply type, category and severity. The creation path can attach files. |
| `candidature` | Offered when recruitment is enabled. Checks the application by `email_msgid` and creates a draft on a miss. The new record takes the sender email, subject, body, private detail, project, entity, message ID and message date before any configured overrides. This action has no attachment save loop. |
| `loadandcreatecontact` | A stored action of this type executes although the setup selector omits it. Parameters can change the working email used by the lookup. A miss initializes and populates a contact, resolving supplied country and state names or codes before creation. |
| Action types beginning with `hook` | Site extensions can contribute choices and handle their own action. The callback receives the configured parameters, resolved identities, message text, subject, header, attachments and already-saved file metadata. A negative callback result marks the action failed. |

Ordinary object assignments in `actionparam` can be separated by a line break or semicolon. An optional element prefix restricts a rule to that record type. `SET` sets a value and `SETIFEMPTY` fills an empty value. `EXTRACT` reads BODY, SUBJECT or HEADER using the supplied expression and takes the trimmed last match or capture. A missed match can clear an existing property. Rules can populate configured fields with `options_`, use temporary extracted values and interpolate supported substitutions. For example, `ticket.subject=SETIFEMPTY:Service request` only supplies a subject to an empty ticket. An override that conflicts with a previously loaded organisation can fail ticket or project creation.

The subject-based attachment action has 23 built-in record descriptors. Standard references cover quotations, leave requests, expense claims, job positions, recruitment applications, sales orders, shipments, contracts, interventions, tickets, knowledge records, supplier quotations, invoices, products, projects, tasks, resources, bills of materials and manufacturing orders. Organisations use customer or supplier codes. Purchase orders can use the internal or supplier reference, supplier bills use internal or secondary references, and lot records use the batch identifier. A matched descriptor still has to fetch its object before a destination is added. An extension can supply a different descriptor map. Separately, a production message already linked to a purchase order can save its attachments under that order before the configured action loop.

### Replies and ticket state

Consider an original customer message with a saved ticket and an incoming reply with a distinct Message-ID. A References value identifying the original ticket establishes the target. The `ticket` action then becomes an event. If the reply's Message-ID is new to the agenda, the handler writes the event. For a linked ticket in closed, canceled, waiting or needs-more-information state, the new event returns it to assigned when an assignee exists, otherwise to unread. Ticket attachments can be stored on that path. Another delivery with the same reply Message-ID can find the existing event and skip the event-creation branch, including its reopening work.

## Commit, move and recovery

| Stage | Durable outcome or recovery evidence |
| --- | --- |
| Completed production message | The handler commits this message and increments the successful-message counter. With a target folder it queues the message UID for a later move. Without one it performs no move. Mailbox seen state can also depend on the adapter's fetch behavior. |
| Failed action | The remaining actions for this message are skipped, this message's transaction rolls back and the collector increments its run error. Other messages can commit independently. Files written and outside-system effects need their own reconciliation. |
| Test modes | Mode 1 runs the action loop and rolls back the database transaction of a successful message. Mode 2 skips the action loop and also rolls back. The target-folder move and expunge are disabled in both. File-writing paths inside actions are outside the rollback guarantee. |
| End of production batch | Actual mailbox moves require the aggregate error to be zero. A failure on one message can leave previously committed, queued successes in the source folder. The library adapter moves queued UIDs in descending numeric order. Its first failed move increments the error, prevents subsequent moves and skips expunge. |
| Native move failure | A failed UID move appends the provider error to the diagnostics without incrementing the aggregate error in that branch. Remaining moves and expunge may still be attempted. The stored run code can remain successful and advance the last-success marker despite the diagnostic. |
| Last-success marker | An error-free production run normally advances the marker to the run start. When the configured success limit stops the loop it uses that last message's header date. A test run does not persist the result. The look-back window, mailbox flags and action-specific duplicate checks determine the next pass. |

After a partial run, compare the UID and folders, the message ID on the ticket, event, project or recruitment application, and any attachments. An unchanged source mailbox alone cannot establish that the database action failed. A persisted ticket alone cannot establish that every reply attachment exists. [Email workflows](email.md) and [delivery evidence](../delivery-evidence/README.md)

## Controlled execution

The filter, ticket selection, transaction-disposition and mailbox move branches ran as PHP with a controlled ticket lookup, substitute mailbox adapters and an in-memory SQLite store. The fixtures supplied decoded headers and lookup results. They did not contact a live mail provider.

| Input | Observed outcome |
| --- | --- |
| A plain message, a message with only a recognized host in In-Reply-To, and a message with a recognized recipient suffix | Both Message-ID-labelled filters retained the second and third. The general `withouttrackingid` filter retained the first only. |
| No existing ticket, then matches by current Message-ID, tracking key and typed object ID | The first selected ticket creation. Each positive match selected event recording. A positive typed-object lookup required no subsequent ticket lookup. |
| Three production messages with an accepted row, a rejected row and another accepted row | Only rows one and three persisted. The run counted two accepted messages and one error. A successful message in mode 1 incremented the success count while its row rolled back. |
| Three queued UIDs, with the adapter rejecting UID 2 | The library branch attempted 3 and 2, stopped and skipped expunge. The native branch attempted 1, 2 and 3, retained the rejection diagnostic and invoked expunge with aggregate error zero. An existing run error or a test-mode run suppressed mailbox calls in the tested cases. |

These checks exercise collector decisions. Provider search behavior, actual mailbox moves and expunge require the corresponding mailbox observations.
