# Partner approval and continued eligibility

The partnership module records a typed, dated relationship managed either for third parties or for association members. The mode defaults to third party. The card requires a record to have the corresponding party link for the selected mode. A partnership may keep its own contact email, public/private notes, reason for refusal or cancellation, and data used to check a partner website. The creator may be absent on a public submission. [Bundled module](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/modules/modPartnership.class.php#L49-L82) · [Record](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_partnership-partnership.sql) · [Mode and access](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/partnership_card.php#L87-L113)

## Decisions and access

| Operation | Card workflow | Effect |
|---|---|---|
| Validate | Draft (0) to validated (1) | Assign the final reference if still provisional |
| Approve | Validated to approved (2) | The approved relationship becomes eligible for applicable continued-eligibility jobs |
| Refuse | Validated to refused (3) | The card requires a reason and saves it with the decision |
| Terminate | Approved to canceled (9) | Mark the relationship inactive |
| Reopen | Refused or canceled to approved | Restore approved status directly. The object emits a reopen event |

The card separates read, write and delete. Writers can also delete drafts. Standard management uses the write grant for validation, acceptance and refusal; the module defines no separate approver role. The REST adapter offers reads and CRUD on the underlying partnership. The card's decision methods implement the state-specific workflow. Creating a record through REST validates required fields, checks write permission and returns the new ID; a caller can supply its identity for processing by event handlers. [Card actions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/partnership_card.php#L148-L237) · [Available decisions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/partnership_card.php#L613-L655) · [Reopen implementation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/class/partnership.class.php#L925-L993) · [API create](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/class/api_partnerships.class.php#L194-L224)

## Membership and website checks

The descriptor registers two daily jobs. The member-expiry job is enabled in its definition, and the backlink job starts disabled. A scheduler must actually run them. The membership job returns immediately in third-party mode. In member mode it requires a positive configured grace period in days. It selects approved partnerships attached to a subscription-paying member type where the member's subscription expiry is **strictly earlier** than the current time minus that grace period. The batch size defaults to 25. This comparison reads the member subscription and can end a partnership even when it has a separate agreement end date. [Job definitions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/modules/modPartnership.class.php#L255-L286) · [Eligibility and batching](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/class/partnershiputils.class.php#L78-L157)

The optional website job selects approved partnerships with no prior check or with a last check at least 24 hours old. It uses the partnership URL override when present and otherwise the partner's website. An unsuccessful check increments a consecutive error counter; a successful check resets the count and clears the reason. With the default positive lower threshold of 3 and upper threshold of 5, counts 4 and 5 enter the warning branch; the sixth consecutive failure enters the cancellation branch. The lower threshold must be positive for that branch logic. These are processing thresholds, not proof that an email reached its recipient. [Selection](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/class/partnershiputils.class.php#L292-L345) · [Thresholds and effects](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/partnership/class/partnershiputils.class.php#L374-L498)

| Acceptance case | Expected observation |
|---|---|
| Refuse a validated application without a reason on the card | Validation message; the application remains validated |
| Reopen a refused partnership | State is approved immediately |
| Expiry equals the grace cutoff exactly | The strict comparison excludes the member on that run |
| Member type does not require subscriptions | The expiry job does not select that member's partnership |
| An approved partnership's last website check was 12 hours ago | The check excludes it even if the scheduler runs again |
| Five consecutive failed backlink checks with default thresholds, followed by success | The sixth check succeeds; error count returns to zero and the partnership remains approved |

The [decision schema](../../schemas/knowledge-partners/partnership-decision.schema.json) models actions accepted by a rebuilding client. It encodes the refusal reason; permission and prior state require the application service.
