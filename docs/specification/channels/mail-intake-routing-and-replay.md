# Mail intake, routing and replay

A collector belongs to an entity and holds a mailbox, source folder, optional destination, enabled filters, ordered actions, last successful scan time and last run result. A message can update several linked business records. The collector treats one source message as the unit of database work.

## Selecting and interpreting a message

Mailbox selection can use sender or recipient, header or body text, size, seen or answered state and exclusions. The collector also evaluates information extracted from fetched headers. Actions have stored positions and execute in that order. The filter relation has no corresponding order guarantee.

Date selection uses a day-granular mailbox search with an overlap from the previous successful scan. With no destination folder the calculation includes the preceding day. The collector has two mail back ends. In one, using a destination can disable the date restriction by configuration. The other's date-search branch applies only when the destination is empty. An overlapping window can legitimately deliver the same message again.

A reply-only filter recognizes several localized reply prefixes and a recognized system reference. The operator can also elect to use the In-Reply-To header. The new-message filter ignores an arbitrary nonempty References header by default, since forwarded or rewritten mail can carry one. A separate setting opts into counting generic references for that filter. Mail routed from a sent folder or matching a configured outgoing sender is recorded as outgoing. Other mail starts as incoming.

See `htdocs/emailcollector/class/emailcollector.class.php:757–815`, `1350–1567`, `1700–1773`, `2053–2100` and `2730–2762`.

## From sender to business action

| Action | Resolution and write |
| --- | --- |
| Resolve an existing party | The action can use a tracked party identifier, email, name or alternate name to locate a party. When load-only lookup has no match, it can resolve a contact by email and then follow its parent party. An ambiguous match can use a configured generic party. Without that fallback ambiguity raises an action error. |
| Resolve or create a party | A genuine miss can create a party. The action uses the selected address, falling back to reply-to and sender address, and can map properties from the message. The created identifier is then available to subsequent actions. |
| Create or follow up a ticket | The collector checks an already resolved ticket object, ticket identifier, tracking reference and original message identifier. Finding a ticket changes the action from creating a ticket to recording a message event. A new ticket can use configured or dictionary defaults for type, category and severity. |
| Record an activity | With a new external Message-ID the action records direction, message identity, actor, recipient/contact and the resolved object or project where available. If an activity already exists for that Message-ID the action skips the duplicate. |
| Create a project or job application | These operations make their own external-message lookup before creation. Repetition is assessed for the specific business operation. The same message may legitimately have both a project and a corresponding activity. |

Tracking context can associate a message with an existing document such as a proposal, invoice, order, project or ticket. A resolved sender and a resolved business object answer different questions. Looking up a party by address does not establish that a particular invoice or ticket was the subject of the message.

After a new activity is successfully created on a resolved ticket, the collector reopens tickets in closed, cancelled, needs-more-information or waiting status. An existing assignee puts the ticket in assigned status. Without an assignee it moves to unread. The reopen is in the new-event branch, so rereading an already recorded message does not replay this transition.

See `htdocs/emailcollector/class/emailcollector.class.php:2375–2510`, `2785–2824`, `2924–3041`, `3162–3290`, `3467–3658` and `3779–3890`.

## Attachment identity

For intake paths using the content-aware attachment helper, the destination already holds the file population against which duplicates are compared. The helper computes a content hash, reuses an existing file with matching contents when present and chooses a suffixed filename if a different file already occupies the requested name. It skips empty contents. Stored metadata includes the actual saved name and content hash. The sender's filename alone cannot identify a business attachment. Identical bytes in two different ticket directories are separate destination populations.

See `htdocs/emailcollector/class/emailcollector.class.php:4311–4446` and `4448–4515`.

## Completion and failure

In production a successful message commits its database work. A failing message rolls back its own transaction. The successful-message count controls the configured per-run limit. When the limit is reached, the collector uses the last successful message's header date as the next checkpoint candidate. It persists a successful checkpoint only for an error-free production run.

Mail moves are deferred until the batch has been examined. The move loop and final mailbox expunge are guarded by the run error flag. A later failure can leave earlier, already-committed messages in the source folder. A move can itself fail after the business transaction commits. Retrying can therefore revisit durable activities, tickets and files. The implementation provides different replay protections for events, object creation and attachments. Operators can reconcile a specific message using its external Message-ID, the resolved ticket or project, the stored file name and the collector's run report.

For example, a waiting ticket has an assignee. Its customer's reply creates an incoming activity and moves the ticket to assigned. The next message in the batch fails a party lookup because two parties have the same address. The first transaction stays committed even if both messages remain in the source folder. When the address ambiguity is resolved and the collector runs again, the first activity's Message-ID identifies the prior write.

See `htdocs/emailcollector/class/emailcollector.class.php:3928–3986` and `3990–4088`.
