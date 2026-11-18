# Expense claims across employee, reviewer and cashier

A travel claim passes between a beneficiary, a supervisor or delegated writer, an expected reviewer, the actual approver and a cashier. The expected reviewer controls circulation of the claim. The amount that can be reimbursed comes from the approved gross total less recorded payments. An editor, reviewer and payer can be three different employees.

## Whose work appears in the queue?

| View or action | Eligible record and operator |
| --- | --- |
| Ordinary claim list | The employee who owns the claim is the acting user or a descendant in their hierarchy. If the operator can approve, the list also includes claims explicitly assigned to them for review. The date, employee and status filters further narrow the result. |
| Broad list | Read-all or its alternate read-all key removes the hierarchy restriction. Advanced all-employee writing does so when advanced permissions are enabled. The entity population still applies. |
| Open the expense card | Read-all, advanced all-employee writing, ordinary read with the author in the hierarchy, or approval authority with the operator designated reviewer. These are alternative record-level tests following the module access checks. |
| Edit employee data or attach supporting evidence | Expense creation authority and a claim owner in the actor's hierarchy, or expense creation authority and enabled advanced all-employee writing. An expected reviewer designation alone supplies no authority to edit the notes or upload receipts. |
| Decide a submitted claim | The card's approve action requires the approval grant and a visible claim in submitted state. It does not require that the designated reviewer equal the actual approver. |
| Initiate reimbursement | The payment operation requires the pay grant, an approved claim and access to its record. Receipt entry and payment registration have separate business effects. |

The new claim form calculates a suggested approver from the signed-in user's individual expense reviewer, otherwise their supervisor. The configured default reviewer overrides that suggestion, and a positive value retained from the form overrides the default. The selectable list is based on direct and group approval grants. A nonempty default together with the unchangeable-default setting fixes the selection in this form. This is distinct from testing the approver when an authorized person acts later. A manager entering a claim on someone else's behalf should distinguish the beneficiary recorded on the claim from the account used by the form to suggest the reviewer.

The service list applies its own filters. In particular, its restricted selection uses eligible employee IDs. The interactive list adds the designated reviewer's pending work through a separate condition. A claim queue built by an integration should specify which view it represents.

## State changes and evidence

| Interactive operation | Required starting state | Durable changes and role |
| --- | --- | --- |
| Submit | Draft | The scoped writer submits. A provisional reference is replaced by the issuing sequence, the submission date and actor are written and the validation event is raised. The file index and document directory are updated when a provisional reference changes. |
| Approve | Submitted | The approver becomes the recorded actual approving user with an approval time. The operation publishes an approval event. A successful decision commits before the card tries its direct approval mail. |
| Refuse | Submitted or approved | The approver records refusal details, refusing user and time. The writer clears the stored approving user. The refusal update does not clear every earlier date. |
| Revise and resubmit | Refused | A scoped writer can resubmit through the refused-claim action. The update returns the claim to submitted, retaining the earlier identifying reference. The statement changes the status alone and does not clear the stored refusal fields. |
| Cancel | Submitted or approved, also closed under additional approval or pay rights | The card also requires creation authority, a reason, and the user to be the claim author or its actual submitting user. Approval or pay in the closed-state gate grants no blanket right to cancel another employee's claim. |
| Return to draft | Submitted, or approved under pay authority | The operator also needs creation authority and must be the author, submitter or have the author in their hierarchy. |
| Mark paid | Approved | The status-only operation conditionally changes an approved claim to closed and sets its paid flag. Registering money through the payment operation additionally creates payment evidence and, with banking enabled, a bank posting. |

Use the claim list to regenerate or merge documents, send documents and, with delete rights, select records for deletion. The menu does not offer bulk approval or refusal. A supervisor who approves three submitted claims via their cards makes three individual decisions. A failed third approval leaves the first two successful decisions in place.

Submission mail goes to the expected reviewer. For approval, the card reads the claimant's email, copies the configured expense copy addresses and uses those addresses as the primary destination if the claimant has no email. For refusal, the card reads the claimant's address and composes the refusal message. The displayed sender identity and the company's outbound mail address are separately selected. A mail error can appear alongside a durably changed claim. Regeneration of a document and delivery of an email are observable outputs of the interactive workflow. The explicit approval service calls the business approval and returns a cleaned claim, without invoking the card's mail composition. Event subscribers can still act.

## A partial reimbursement and an unavailable claimant mailbox

An employee submits a claim for 345.00. The manager listed on the claim is unavailable. An internal supervisor with approval rights and record visibility approves the claim. The expected reviewer remains the original manager. The approving user and timestamp identify the supervisor who acted. If the claimant has no email and an expense copy mailbox exists, the approval notice can go to that mailbox. No cash moves on approval.

The cashier posts 200.00 against the approved claim. The payment operation totals proposed amounts at monetary precision, computes `345.00 − prior payments` and rejects a total above that remainder. With banking enabled it requires the destination account identifier in the request and writes the claim payment and corresponding bank movement in one outer transaction. A failed bank write rolls the payment back. After success the claim still has 145.00 outstanding. A further payment of 150.00 exceeds the allowed balance. A payment of 145.00 brings the recalculated remainder to zero and closes the report as paid in the same transaction. A direct status-only classification has a different record trail, so reconciliation should use the claim payment and bank evidence for the two disbursements.

The [expense rules](../specification/people-and-services/expense-scales-and-ceilings.md) explain how the claim got its original gross total.

For the accounting effect of approval, follow a [two-line expense claim from assignment to journal transfer](../expense-accounting/worked-reconciliation.md). The [employee payment registers](../expense-accounting/employee-payment-registers.md) show which reimbursements and salary payments an operator can retrieve.
