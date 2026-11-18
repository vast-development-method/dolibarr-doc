# Campaign targets, delivery and suppression

A campaign has its own title, entity, message content and send state. Its recipient rows carry an address, source record, recipient tag and delivery state. A campaign title is unique within its entity, and an email address can occur only once within a campaign. One party address discovered by two audience selectors consequently represents one delivery destination in that campaign.

See `htdocs/install/mysql/tables/llx_mailing-mailing.key.sql:20`, `htdocs/install/mysql/tables/llx_mailing_cibles-mailing.key.sql:20` and `htdocs/comm/mailing/class/mailing.class.php:205–214`.

## Audience construction and reuse

A suppression row records the address, entity and unsubscribe group. The unique key includes all three. Audience selectors differ in how they use that register. The standard party selector checks for an address across suppression rows without an entity condition in its address subquery. The partnership selector checks address and current entity together. A suppression stored by entity A can therefore also remove that address from entity B's standard party audience, while the partnership selector for B considers B's suppression records. The campaign's option for including unsubscribed recipients changes those selectors' eligibility decisions.

Cloning creates a fresh draft with its own title. Content and recipients are separate choices. Keeping recipients builds new target rows against the new campaign. A cloned audience should therefore be understood as materialized recipients on a new campaign, independently of the delivery history of the original.

See `htdocs/core/modules/mailings/thirdparties.modules.php:154–189`, `htdocs/core/modules/mailings/partnership.modules.php:118–131`, `htdocs/comm/mailing/class/mailing.class.php:587–680` and `htdocs/install/mysql/tables/llx_mailing_unsubscribe.key.sql:20`.

## Delivery states

| Record | Stored state | Meaning in delivery |
| --- | --- | --- |
| Campaign | 0 draft | Outside the scheduled sender's eligible campaign set. |
| Campaign | 1 validated | Ready to start. Scheduled delivery moves it to partially sent as processing begins. |
| Campaign | 2 partially sent | A later batch can resume. The sender evaluates eligible targets again. |
| Campaign | 3 completely sent | No remaining eligible targets at completion of the scheduled batch. |
| Target | −1 error or 0 unsent | Eligible for selection by the scheduled sender. A prior error is retryable. |
| Target | 1 sent | A successful send attempt was recorded. Recipient reading is tracked separately. |
| Target | 2 read | The recipient activity has been marked read. |
| Target | 3 do not contact | The target is outside the scheduled sender's pending population. |

The browser and scheduled senders each have their own batch limit. When the scheduled sender has both a positive configuration limit and a positive invocation limit, it selects up to the lesser of the two. It selects targets with status below one for the selected campaign. For each successful send it records status 1 and a send timestamp. A send failure records status −1 and a timestamp. At the end, the scheduled sender counts targets still below one and marks the campaign complete when none remain. The browser path similarly uses its attempted population and success/error counts to choose partial or complete.

External delivery and the local update are distinct steps. If the transport accepts a message but the write of status 1 fails, an eligible target can remain for another run. A sent timestamp records the application's send outcome. It does not establish a later read or a customer's response. Changes to a prospect's communication status are separate side effects in the configured tracking path.

See `htdocs/comm/mailing/class/mailing.class.php:1128–1141`, `scripts/emailings/mailing-send.php:122–191`, `scripts/emailings/mailing-send.php:341–443` and `htdocs/comm/mailing/card.php:185–250,453–478`.

## Unsubscribe and recovery

The public action validates a recipient-specific request and resolves the campaign target from its tag. An unknown tag, an empty stored address or a target already at do-not-contact state stops the normal update. The handler marks the target as do-not-contact and attempts to insert the stored target address into the campaign entity's unsubscribe register with the empty group. An existing identical suppression can make that insert redundant. Subsequent audience selectors that consult the register can exclude that address even for a new campaign.

Resetting one failed recipient requires the target to belong to the specified campaign and currently have status −1. It changes that target to 0. Resetting all recipients updates every target in the campaign to 0. The latter operation can therefore requeue previously sent rows as well as do-not-contact rows. That bulk reset has no corresponding deletion in the entity's unsubscribe register. An operator resuming one delivery error can use the single-target operation to preserve the campaign's other delivery outcomes.

For example, a campaign has 80 sent targets, one failed target and nine unsent targets. The scheduled sender has ten eligible rows. A batch of five successes leaves five eligible and the campaign partial. If the failing address unsubscribes while awaiting its retry, its target changes to 3 and the pending count drops by one. Rebuilding a future party audience also consults the suppression register, subject to the campaign's inclusion setting.

See `htdocs/public/emailing/mailing-unsubscribe.php:77–124,137–166` and `htdocs/comm/mailing/class/mailing.class.php:825–882`.
