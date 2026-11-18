# Applying online funds to an order, membership or event

The payment return identifies both the provider transaction and the business item the payer selected. After the funding result is established, the receiving workflow has to decide which record to invoice, what period or right to grant, and what to do if financial posting fails.

## Paying for a customer order

The order tag identifies the order to load. The handler resolves a configured payment mode or looks up the provider's mode in the payment-mode dictionary, falling back to card. With invoicing enabled, a nonzero final amount and a positive mode identifier, it begins an accounting transaction.

1. Create the invoice from the order's lines and amounts. Mark the order billed and validate the invoice. A difference between the order total and the amount received does not generate an adjustment line.
2. Allocate the final paid amount to this invoice. The payment records the provider site and the longer provider transaction identifier when one is present, otherwise the ordinary transaction identifier.
3. The order return path accepts the entity currency. It reports a different currency as an error and stops the normal local payment creation. The allocation routine can close covered invoices and regenerate their documents.
4. Post the payment to the resolved provider bank account. The branch reports missing account configuration and posting errors. It commits on success and rolls back on its error path.

For an order of 120 and a final receipt of 100 in the entity currency, the invoice retains its 120 total. The order can be marked billed because the full order was invoiced. The payment covers 100 and 20 remains outstanding, assuming no other settlement. A gateway can already have collected the money when a local bank posting fails. Recovery therefore starts with the provider transaction, the local payment's external identity and the invoice allocation.

## Membership activation and coverage

For a membership with a configured fixed charge the new-member branch verifies the received amount against the expected charge when that expected charge is nonzero. A configured global minimum activates an additional comparison with the global and member-type minima. An incompatible payment currency produces an error. An excluded member cannot be revalidated through the paid-subscription return. For an eligible member the branch validates the member and initializes missing validation time as needed.

The default coverage start is the member's validation date. When an existing end date is available, the new period initially starts one day after it. If there is no prior end date, a configured offset can shift the start from the payment time. Month or year alignment can move the computed start to the first day of that month or year. The three-month setting separately derives the first day of the month three months before the previous end date. With a configured duration the routine advances the start and end together by whole periods while the provisional end is in the past, then subtracts one day to obtain the inclusive end date.

Once the subscription row exists, its configured complementary action determines the financial records.

| Mode | Active areas used by the selector | Outcome |
| --- | --- | --- |
| Direct bank | Banking | Single bank entry for the subscription |
| Bank through invoice | Banking, party management and invoicing | Customer invoice, payment and bank entry |
| Invoice only | Banking, party management and invoicing | Invoice |
| None | Selected when no qualifying mode applies | Subscription without those complementary financial postings |

The complementary operation receives the subscription identifier, coverage start, payment date, amount, mode, account and provider transaction. It may create a party for an unlinked member. The local transaction commits before optional external-user provisioning and subscription email delivery. User provisioning first counts existing users linked to the member. An email issue after commit can leave the membership fully active and the receipt already posted. Retrying delivery should refer to that existing subscription.

## Attendee registration and exhibitor proposal

An attendee payment has two identifiers. The payment reference identifies an existing invoice. The attendee tag identifies the registration. The handler validates the invoice before beginning the subsequent payment transaction. It allocates the receipt to that invoice in entity currency and requires a bank posting. When these steps succeed, it fetches the tagged attendee, calls validation, sets the attendee's amount to the final paid amount, stamps the subscription time and saves. The successful transaction precedes the attendee's confirmation email. The recipient is the attendee's address, with additional recipients depending on the party and company-address data.

The two identifiers need separate reconciliation. A validated invoice alone says nothing about whether the later bank posting and registration update completed. The payment handler expressly checks the attendee fetch for a negative result, but does not inspect the return values of its subsequent attendee validation and update calls before the commit decision. The local payment record and the registration state are therefore distinct evidence of completion.

The booth or conference payment branch also loads the invoice from the payment reference, resolves the mode and records the receipt and bank posting. Its domain action sets the tagged booth or conference to *suggested*. This is a proposal-stage status. Organizers still control the later acceptance of the event content. The booth branch's confirmation-mail handling has different conditions and timing from the attendee branch.
