# Partner applications, approval and reinstatement

A partnership is a dated agreement of a defined type with a business party or member. The agreement has its own reference, entity, start, optional end, status, notes and reason for refusal or termination. The partner’s identity and the partnership decision have different lifetimes. Finding an existing customer or member does not grant them an approved partnership.

## Identity and repeat agreements

Creation requires a positive party or member link and forces the initial state to draft. A request cannot create a pre-approved agreement by submitting that status in its initial payload. Staff choose the type from active entries in the partnership-type dictionary.

The reference is unique within the entity. Separate unique keys combine type, partner and starting date for the party and member relations respectively. The same party can hold successive agreements of the same type with different start dates. Two otherwise identical agreements on the same starting date collide even if their end dates differ. The optional end date records the contractual period. Cancellation is a distinct, explicit state change.

A party can also appear in the customer register. Changing the partnership’s decision preserves that master identity. A member renewal likewise remains a separate dated membership obligation. No partnership approval operation in this workflow automatically issues a dues invoice or grants a user account.

Related records include [Partnership agreement](../../records/parties.md#record-partnership).

## Public request and party matching

When the public application interface is active, the form requires a type, company name, applicant’s family and given names and a valid email. It initializes the request as draft, dates creation and the requested partnership start to the submission time and records the applicant’s network address. It processes permitted custom fields before creating the agreement.

The organization-matching path looks for the supplied company name. If it fails to find a company under that name but finds the submitted email on an existing company, it asks the applicant to correct the name. It does not attach that request to a company solely because the email matches. If neither lookup succeeds, it creates a party from the submitted name, address, region, country, email and URL, using the applicant’s name as an alias. An ambiguous company-name result is an error.

For an existing unambiguously identified party, the flow links that party and fills previously empty address and contact details. Existing populated details survive the public form. For example, a public applicant entering a different address for the known organization does not replace the address already on file through this fill-missing branch. The public form reaches ordinary partnership creation after its entry checks. Staff validation and acceptance remain later decisions.

## State changes and authority

| Staff action | Before | After and observable effect |
| --- | --- | --- |
| Validate draft | Draft 0 | Validated 1. Allocate the final reference if required. The request is ready for a decision. |
| Approve | Validated 1 on the card | Approved 2. Preserve the final reference, store the approved state and publish the acceptance event. |
| Refuse | Validated 1 on the card | Refused 3. Require an explanation, store it with the refusal and update the agreement. |
| Terminate | Approved 2 | Canceled 9. The cancellation operation acts on an approved agreement. |
| Reinstate | Refused 3 or canceled 9 | Approved 2. The reopen operation directly restores approval without returning the agreement to the validated queue. |
| Return to draft | Offered for a non-draft on the staff card | Return the record to drafting through the separate draft action. |

Validation and approval on the staff card use partnership write authority. An operator can hold this authority without being named in the application as its contact. The acceptance method writes the reference and approved state and emits an acceptance event with the actor. A data consumer should not assume the existence of a dedicated per-approval timestamp or signer field written by this operation. The card can regenerate the agreement document after validation or approval, selecting the output language and reporting a generation warning independently of the recorded state change.

Staff readers, writers and deleters have distinct grants. A writer can delete a draft through the staff card. The programmatic delete operation requires the delete grant. Resource reads and list access use the caller’s available partnership scope. Separate document, contact and agenda records can remain associated with an agreement across changes in status.

For example, a partnership starting 1 April can be refused for missing evidence, then reinstated when evidence arrives. Reinstatement changes the original agreement to approved under its existing ID. Creating a second agreement of the same type for the same party with the same 1 April start is a different operation and would encounter the uniqueness rule.
