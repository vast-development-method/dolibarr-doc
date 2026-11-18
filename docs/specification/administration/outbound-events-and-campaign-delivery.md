# Outbound events and campaign delivery

An outbound hook delivers a business event to a target during the event's execution. A campaign stores a recipient work list and processes recipients over time. Their progress records have different meanings. A hook-history row records an attempted callback. A campaign target row can exist long before the first delivery attempt.

## Event matching and acknowledgment

A target contains a destination URL, a list of event codes, a lifecycle state and a blocking or warning delivery policy. For an ordinary event, an automatic target is eligible when the triggering action exactly matches a configured code after whitespace trimming. A manual target also requires a manual-dispatch context. The event handler skips delivery when the module is disabled or no target qualifies.

For each match the handler builds a JSON envelope containing the event code and a snapshot of the business object as supplied to that trigger. The snapshot can include lines and linked data when those were loaded on the object. A receiving service cannot assume every transition supplies the same set of loaded customer, line or relationship fields. The handler posts to the target and evaluates the response before continuing. A successful transport with HTTP status in the 200–299 range counts as accepted. A 202 therefore acknowledges submission even if the receiver processes the document later. A 4xx, 5xx or transport error is a failed attempt.

A blocking failure contributes to a negative trigger result. It can roll back the originating business operation when the caller makes that operation conditional on successful triggers. A warning-only failure is logged and does not by itself veto the business transaction. Processing continues through other matching targets. There is no atomic commit spanning multiple HTTP receivers or spanning a receiver and the originating invoice transaction.

For example, validating an invoice sends to a fulfillment receiver which returns 204 and to a finance receiver which times out. With warning-only finance delivery, the invoice can remain validated while finance has an uncertain delivery outcome. With blocking finance delivery the invoice validation can roll back, yet the fulfillment receiver already accepted its callback. A repeat of invoice validation can send the fulfillment message again. HTTP status also cannot distinguish work that the recipient accepted just before a lost response. Business reconciliation requires the receiver's document reference or event records in addition to the local result.

Source locations include `htdocs/core/triggers/interface_95_modWebhook_WebhookTriggers.class.php:runTrigger` and `htdocs/webhook/class/target.class.php`.

## Attempt history and redelivery

The handler stores the event code, serialized body, target identifier, destination URL as used, error text, status, creation timestamp and creating user. A **separate database connection** commits the history. A history row can therefore survive a rollback of the source operation. Its URL can still identify the destination of an earlier attempt after the target's configured URL changes.

The failure counter used for the history status is initialized once per event invocation. Once a target fails, a later successful target in the same dispatch can receive a history row marked error even though its own error text is empty and its response counted as a successful post. Interpret the target-specific error, remote acknowledgment, source-document outcome and delivery order together when reconciling a multi-target event.

The standard hook descriptor does not register a periodic redelivery worker. The history fields do not track a scheduled retry, per-target attempt limit, lease or confirmed downstream completion. A later invocation of the same business action evaluates the eligible targets again using its current object snapshot. It cannot be treated as automatically replaying the original stored bytes only to the receiver that failed. Direct callback delivery, independently committed history and the outcome of the source transaction are three independently observable facts.

Source locations include `htdocs/core/triggers/interface_95_modWebhook_WebhookTriggers.class.php:73–207`, `htdocs/install/mysql/tables/llx_webhook_history-webhook.sql` and `htdocs/core/modules/modWebhook.class.php:235–252`.

## The campaign work list

A campaign target stores the email address and can retain its source type, source identity, contact names and tracking tag. The batch sender selects validated or partly sent campaigns. Beginning a validated campaign marks it partially sent. Within a specific campaign, eligible target states are unsent and previously failed. A send limit can restrict the batch. Successful delivery records sent status and send time. A transport failure records error and attempt time. The sender counts outstanding targets with status below sent. Once that count reaches zero following a batch, it can mark the campaign completely sent.

| Target state | Meaning when resuming the same campaign |
| --- | --- |
| Unsent | Selected for delivery. |
| Error | The command sender can select it again. The specific error-reset operation also permits an error target to return to unsent. |
| Sent | Excluded from the unsent/error selection. |
| Read | Tracking has advanced the target past sent. It is excluded from routine delivery selection. |
| Read and unsubscribed | Excluded from routine delivery selection. Unsubscription also creates a campaign unsubscribe record for the address in its entity. |

Two successful targets and one failed target leave one recipient eligible for a later invocation. A partly sent campaign does not mean all three need resending. The transport call precedes updating the target row. An interruption between those operations can leave the address eligible despite a mail server having accepted it. A completed campaign means this sender found no remaining target below sent status. It establishes neither that every addressee opened the message nor that every mailbox ultimately delivered it.

Source locations include `scripts/emailings/mailing-send.php:122–182, 351–381, 416–445`, `htdocs/comm/mailing/class/mailing.class.php:resetTargetErrorStatus` and `htdocs/public/emailing/mailing-unsubscribe.php:112–165`.

## Recipient selection after an unsubscribe

The public unsubscribe action resolves a campaign target from its tracking reference. An unknown target or one with no email cannot complete the action. An already-unsubscribed target exits without another status change. For a valid target, the action marks that campaign target as read and unsubscribed, then records an address-level unsubscribe for the target's entity. It uses the email address stored on the target. A subsequent change to a customer's primary contact address does not turn the original unsubscribe into a party-wide subscription choice.

When populating another campaign, the form passes the campaign's include-unsubscribed setting to its chosen selector. The third-party selector excludes empty addresses and addresses already in that campaign. With ordinary suppression enabled it checks for unsubscribe entries. Its *count* of prospective recipients checks the address in the current entity. Some variants of its actual party-selection query check for the address without an entity condition. In a shared-party installation a prospect count can therefore exceed the addresses actually added. A shared mailbox already present in a campaign can also represent several parties without receiving several target rows from the same selection.

Selection and submission happen at different times. The command batch's eligible-target selection uses the target's campaign and status. It has no fresh join to the address suppression table. An unsubscribe updates the target through which the person unsubscribed and affects subsequent selector runs. It need not change a ready-to-send row already materialized for a different campaign. For example, if campaigns A and B both have the same mailbox on their target lists, unsubscribing through A sets A's target to state 3. A later campaign C built using normal suppression can omit the mailbox, while B's existing row must be considered separately.

Source locations include `htdocs/public/emailing/mailing-unsubscribe.php:103–165`, `htdocs/comm/mailing/targetemailing.php:144–157`, `htdocs/core/modules/mailings/thirdparties.modules.php:add_to_target, getNbOfRecipients` and `scripts/emailings/mailing-send.php:168–182`.
