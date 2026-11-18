# Failure, delivery and replay

## Following a single dispatch

Consider three eligible subscribers in priority order. If they return −4, 7 and −2, all three execute and the dispatcher returns −2. It collects the errors from the first and last. When only the first and last are enabled and return 5 and 0, the dispatcher returns 1. A zero from the party contact subscriber can coexist with newly inserted contact links. A positive from a notification subscriber can coexist with zero recipients.

An originating operation can open a transaction, write its record, call the subscribers and roll back after a negative aggregate. Each subscriber receives the same database connection unless it creates another. The dispatcher compares the connection's nesting depth on entry and return from each subscriber. A subscriber that opens a level and returns zero is counted as failed if the depth changed. The unclosed level remains on the connection. A thrown error bypasses this exit check. The enclosing operation's own exception handling and the database connection's lifetime then determine what happens to staged writes.

| Effect when a later subscriber fails | Evidence to examine before repeating the operation |
| --- | --- |
| Change to an order, activity or other record on the originating connection | Reload the affected records and typed links after the originating transaction ends. A successful subscriber return alone establishes no commit. |
| Accepted mail, directory operation or provider update | Check the destination's durable identifier and status. A local rollback cannot reverse these effects. Different handlers propagate failures differently. |
| Completed webhook POST | Match the target, event and document identity against receiver evidence. A timeout does not establish whether the receiver committed. Each redelivery is a new POST. |
| Webhook history | Check the per-target error text alongside the status, response at the receiver and originating record. History uses an independent connection. |
| Automatic task or intervention | Count existing rows for the project or ticket origin before repeating. Neither handler checks for an earlier equivalent row. |
| Order derived from a signed offer | The subscriber first looks for a linked order. The close-order-to-invoice branch directly requests conversion. Inspect both link direction and target before treating a replay as complete. |

## Two webhook destinations on one event

The webhook subscriber trims each entry in the target's comma-separated event list and tests code membership. Automatic targets qualify by default. A manual target requires `sendmanualtriggers` on the event object. An explicit `sendtrigger` or `testsend` action can qualify a target independently of its normal status, still subject to the code match. The body contains `triggercode` and a serialised `object`. The subscriber removes database handles as it traverses the payload. It sends before starting that target's history transaction.

Suppose automatic target A returns HTTP 503 and automatic target B then returns 201. A target counts as an accepted POST for a 2xx response with no transport error. For nonblocking A, the subscriber logs the failure and still attempts B. Its direct return is one successful POST. The aggregate dispatcher sees one positive subscriber. For blocking A, B is still attempted, but the subscriber returns negative and the aggregate reports a failed subscriber.

History holds the event code, body, target ID, URL, status and error text. A fresh connection is opened for history when the first target is attempted, with a transaction per target. The error-text variable resets for each destination. The counter used for the history status spans the whole target loop.

| Destination in execution order | Transport result | Recorded status | Recorded text |
| --- | --- | ---: | --- |
| A | HTTP 503 | −1 | Failure for A |
| B | HTTP 201, accepted | −1 | Empty |

Thus B's negative status in this sequence can accompany a successful delivery. If the originating transaction rolls back, committed histories and accepted remote requests still exist. A separate failure can leave an accepted delivery without any history row. The history writer reports insertion errors with a negative integer, while this caller tests for a false result. A negative integer takes the commit branch. In an isolated run an accepted POST followed by a history result of −1 left the dispatcher result positive and added no history row. Repeating the event sends to A and B again. A third target in manual mode remains idle unless the event or explicit send action qualifies it. There is no automatic deduplication in this loop. Receiver-side reconciliation needs the originating record identity, event and the business transition the receiver acted on.

## Event-project task failure

For an event project with the configured labels “Prepare”, “Fail” and “Close”, the planning subscriber starts a database transaction and attempts tasks in order. If the second task creation reports a negative result, the handler attempts to combine its own error collection with the task errors. On a freshly constructed subscriber this collection is unset. Execution raises a type error at that point. The third task and later subscribers are skipped, the planning subscriber's own rollback branch is bypassed and its transaction level remains open. The first staged task's eventual persistence depends on how the caller resolves the open transaction.

With two successful labels “Prepare” and “Close”, dispatching the same qualifying validation event twice requests four task inserts. New tasks point at the project ID and each uses the configured label. No event, project/label or task-origin lookup suppresses the second pair. A user re-validating a project should inspect tasks already created under it.

## What was exercised

An isolated execution used the dispatcher, commercial workflow, ticket contract setter, event-project planner and webhook subscriber. The database, linked records, intervention creation, task insertion, target history and HTTP transport were controlled. The 42 assertions covered module gating and priority, failure aggregation and depth, four invoice-setting combinations, ticket contract lookup and intervention propagation, project-task failure and replay, automatic/manual webhook selection, blocking and nonblocking transport failure, independent history, failed history insertion and replay. These checks distinguish reached write calls and recorded fixture state. Live recipient acceptance, database isolation and end-to-end ERP operations depend on the selected deployment.
