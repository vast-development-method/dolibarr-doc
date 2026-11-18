# Partner approval and continued eligibility

The partnership module records a typed, dated relationship managed either for third parties or for association members. The mode defaults to third party. The card requires a record to have the corresponding party link for the selected mode. A partnership may keep its own contact email, public/private notes, reason for refusal or cancellation, and data used to check a partner website. The creator may be absent on a public submission. [Bundled module](../reference/locators/knowledge-partners.md#ref-3f0542b0c5ea) · [Record](../reference/locators/knowledge-partners.md#ref-0ea088a9838a) · [Mode and access](../reference/locators/knowledge-partners.md#ref-083b8ccf5149)

## Decisions and access

| Operation | Card workflow | Effect |
|---|---|---|
| Validate | Draft (0) to validated (1) | Assign the final reference if still provisional |
| Approve | Validated to approved (2) | The approved relationship becomes eligible for applicable continued-eligibility jobs |
| Refuse | Validated to refused (3) | The card requires a reason and saves it with the decision |
| Terminate | Approved to canceled (9) | Mark the relationship inactive |
| Reopen | Refused or canceled to approved | Restore approved status directly. The object emits a reopen event |

The card separates read, write and delete. Writers can also delete drafts. Standard management uses the write grant for validation, acceptance and refusal; the module defines no separate approver role. The REST adapter offers reads and CRUD on the underlying partnership. The card's decision methods implement the state-specific workflow. Creating a record through REST validates required fields, checks write permission and returns the new ID; a caller can supply its identity for processing by event handlers. [Card actions](../reference/locators/knowledge-partners.md#ref-3610f4e62eca) · [Available decisions](../reference/locators/knowledge-partners.md#ref-424402e81493) · [Reopen implementation](../reference/locators/knowledge-partners.md#ref-2c30745b0f66) · [API create](../reference/locators/knowledge-partners.md#ref-135216e5f8c2)

## Membership and website checks

The descriptor registers two daily jobs. The member-expiry job is enabled in its definition, and the backlink job starts disabled. A scheduler must actually run them. The membership job returns immediately in third-party mode. In member mode it requires a positive configured grace period in days. It selects approved partnerships attached to a subscription-paying member type where the member's subscription expiry is **strictly earlier** than the current time minus that grace period. The batch size defaults to 25. This comparison reads the member subscription and can end a partnership even when it has a separate agreement end date. [Job definitions](../reference/locators/knowledge-partners.md#ref-3e8a8f3a020d) · [Eligibility and batching](../reference/locators/knowledge-partners.md#ref-f0cbebb828b7)

The optional website job selects approved partnerships with no prior check or with a last check at least 24 hours old. It uses the partnership URL override when present and otherwise the partner's website. An unsuccessful check increments a consecutive error counter; a successful check resets the count and clears the reason. With the default positive lower threshold of 3 and upper threshold of 5, counts 4 and 5 enter the warning branch; the sixth consecutive failure enters the cancellation branch. The lower threshold must be positive for that branch logic. These are processing thresholds, not proof that an email reached its recipient. [Selection](../reference/locators/knowledge-partners.md#ref-2423de83129b) · [Thresholds and effects](../reference/locators/knowledge-partners.md#ref-536de336a63b)

| Acceptance case | Expected observation |
|---|---|
| Refuse a validated application without a reason on the card | Validation message; the application remains validated |
| Reopen a refused partnership | State is approved immediately |
| Expiry equals the grace cutoff exactly | The strict comparison excludes the member on that run |
| Member type does not require subscriptions | The expiry job does not select that member's partnership |
| An approved partnership's last website check was 12 hours ago | The check excludes it even if the scheduler runs again |
| Five consecutive failed backlink checks with default thresholds, followed by success | The sixth check succeeds; error count returns to zero and the partnership remains approved |

The [decision schema](../../schemas/knowledge-partners/partnership-decision.schema.json) models actions accepted by a rebuilding client. It encodes the refusal reason; permission and prior state require the application service.
