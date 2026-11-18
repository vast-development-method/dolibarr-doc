# Member status, renewal periods and collection of dues

A member record answers whether a person or organization has been admitted. A subscription describes a dated period of membership at an agreed amount. A customer invoice records a receivable, and a bank entry records the movement of money. An administrator can record the period alone, receive cash directly, issue an invoice or both issue and settle it. Each choice produces different records for a treasurer to reconcile.

## Admission and linked identities

| Decision | Persistent effect |
| --- | --- |
| Validate a member | Set administrative status to validated (1), record the current validation time and acting user, and publish the member-validation event. Repeating validation on an already validated record leaves it as it stands. |
| Terminate membership | Set administrative status to terminated (0), record the acting user and publish the termination event. The operation preserves the subscriptions and their dates. |
| Exclude a member | Set administrative status to excluded (−2), record the acting user and publish the exclusion event. This remains distinguishable from a resignation or ordinary expiry. |
| Offer a new subscription on the member card | Require subscription creation authority and positive administrative status. A draft (−1), terminated or excluded member gets a disabled action. An admitted member can remain in administrative status 1 after the paid-through date. |

A member can have both an application user and a billing party. Assigning a user clears the previous user links to this member, then points the selected user at the member. Assigning a billing party first releases that party from other members, then sets the member’s party reference. Clearing either association is supported.

On a changed member record, ordinary identity synchronization copies the reference, names, gender, birth date, address, email, social accounts, office and mobile numbers and language to the linked user. If a member login is optional, the existing user login survives. The linked party receives shared address, email, main phone, country, region, social accounts and language. Updating the party or user through this path suppresses reciprocal synchronization. These are field assignments to existing records. Linking the member’s billing party does not itself place the linked user into the party’s external-user role.

## Constructing the inclusive service period

1. Suggest the start on the day after the member’s paid-through date. On first enrollment suggest the validation date. The operator may supply a different start. A configured relative start can offset today, and alignment options can move the suggestion to the beginning of a month or year. The three-month option takes the first of the month three months before the prior expiry.
2. Use the duration amount and unit on the member type. Their defaults are one and year. If the operator leaves the end blank, add that duration to the start and subtract one calendar day. End-of-month and end-of-year suggestions can prefill an explicit end.
3. On creation require the end to fall strictly after the start. A start and end on the same day fails even though the dates at the ends of a valid period are inclusive. A direct call to the member subscription operation without an explicit end uses one year minus a day. The staff entry screen computes the type-specific end first and passes it through.
4. Store the member and type, inclusive dates, creation time and actor, contribution, public and private notes, external reference and optional import identifier. An omitted type inherits the member’s current type. Later changes to the member’s category do not rewrite that historical period.
5. Read all subscriptions and write the greatest nonempty end date back to the member. The period with the most recent start supplies a separate last-period end value. Neither insertion order nor a gap in the historical periods establishes uninterrupted coverage.

For example, a member has an annual period from 1 January to 31 December and a second period from 1 June to 30 September in the same year. The latest-starting entry ends in September. The member’s paid-through date remains 31 December. Removing the annual entry shortens the paid-through date to 30 September. Removing both clears it. A calendar-year period starting 1 January has 31 December as its default end even in a leap year.

## Receivable and cash choices

| Staff choice | Documents and dates |
| --- | --- |
| Record period only | Store the subscription amount and period. The staff workflow creates neither a customer receivable nor a bank movement on this route. |
| Receive directly in the bank | On the specified payment date create an account entry for the amount, instrument, label and optional cheque details. Link it back to the member and store the bank row on the subscription. |
| Invoice only | Resolve the linked customer. Create a standard sales invoice dated when generated, with a typed link to the subscription. Carry customer payment terms/method and bank defaults where available. Validate the invoice and leave payment to the receivables workflow. |
| Invoice and receive | Perform invoice creation and validation, allocate the contribution amount to that invoice on the payment date, post the receipt to the selected bank, record the bank row on the subscription and mark the invoice paid. |

The invoice has one service line, quantity one. Its tax-inclusive selling price is the subscription amount, and the line starts on the period start. The optional configured catalog item and subscription tax policy supply the item identity and VAT rate. A dues payment of 120 including 20% VAT therefore produces a line of 100 before tax and 20 tax when that rate applies. The invoice date, period start and payment date can be three different days.

The staff form requires a valid start. Both cash routes require a payment date. For a type requiring dues it checks a numeric contribution. For a nonzero amount being recorded with banking enabled it requires the transaction label and, on the cash routes, a payment method and destination account. Invoice creation needs a billing party. The complementary operation can create one from the member where the calling workflow enables automatic creation.

The staff action groups the new period and selected complementary financial actions into one transaction. A reported failure in generating the invoice or posting the receipt rolls back that action. The optional confirmation email runs after commit. Failure to send a confirmation requires a communication follow-up and does not void the recorded period.

## Correcting or removing a period

The subscription update writes a numeric amount, type, member reference, public note, period dates, creation date and direct bank reference. It reloads the member, refreshes the paid-through date and raises a modification event. Recording the amount on the subscription and maintaining a posted invoice or reconciled receipt are separate operations. The subscription update contains no invoice repricing or cash adjustment.

Deletion raises the subscription-deletion event and removes the period. If the row existed it rebuilds the member’s expiration and attempts to remove an associated bank row when one is found. A reconciled bank row can refuse deletion and roll back the operation. A missing subscription returns a distinct no-change outcome. The deletion path makes no corresponding call to cancel a sales invoice. A treasurer correcting a billed renewal therefore needs both the membership history and the associated receivable to understand the result.

The [subscription register](member-subscription-register.md) shows how period charges, bank account filters and current membership status contribute to a treasurer’s search.
