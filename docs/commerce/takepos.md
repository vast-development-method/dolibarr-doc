# TakePOS sales, tender and register closure

A till sale is a customer invoice. Starting a sale assigns an entity, party, TakePOS source and terminal. The till finds an open ticket by its temporary terminal-and-place reference, so parallel tables or sales can keep separate baskets. The installation needs a valid customer for the ticket. A terminal's default party serves a walk-in customer. Catalogued items, tax, invoice settlement and inventory then use the corresponding ERP records. [Operator guide](../reference/locators/commerce.md#ref-a152434f855c) · [Module dependencies](../reference/locators/commerce.md#ref-29bfcd329438) · [Ticket lookup and defaults](../reference/locators/commerce.md#ref-ddef3f44ce5b) · [Ticket creation](../reference/locators/commerce.md#ref-eb1269da596d)

## Record and command boundaries

| Record | Business identity and relationships | Actions |
| --- | --- | --- |
| Terminal configuration | Terminal number, default party, optional project, warehouse and bank account per tender method | Select the active terminal. TakePOS run permits entering a sale and taking payment. A separate permission controls existing line prices, quantities and discounts. Changing a line already sent for preparation requires the ordered-line right. |
| Open ticket | Invoice ID, provisional reference, terminal, place, entity, party, invoice detail | Add a catalogue item, free line or note. Preparation orders can be printed before settlement. A receipt uses the sale's underlying invoice. |
| Settlement | Payment linked to the invoice, payment method, invoice allocation and bank account | Record part or all of the balance in company currency. Cash change is recorded as a separate payment attribute. |
| Register control | Entity and terminal, day/month/year, opening amount, expected and declared cash/card/cheque totals, creator, validator and status | Closing a period prevents further till actions in its period. The invoice handler looks for a closed current day, month or year for this terminal and entity. |

[Terminal settings](../reference/locators/commerce.md#ref-a45a43249799) · [TakePOS rights](../reference/locators/commerce.md#ref-2b8f7976177d) · [Edits after order printing](../reference/locators/commerce.md#ref-7247ac47a3c7) · [Register structure](../reference/locators/commerce.md#ref-03f4cbf74afc) · [Period guard](../reference/locators/commerce.md#ref-4828aa0ff96c)

## Settle a sale

1. Resolve the invoice and the terminal's account for the payment method, or the selected account when account selection is enabled. A bank account is required for an immediate tender when banking is enabled. An empty draft cannot be settled.
2. Validate a draft invoice. With stock enabled, batch tracking disabled and terminal stock changes allowed, validation forces the stock issue at the terminal warehouse. With batch tracking enabled, the separate stock path uses the line's warehouse when present, otherwise the terminal warehouse, and issues the selected lot. The batch path runs only on the call that validates the draft.
3. For an ordinary positive balance, allocate the entered tender up to the balance. In the upstream handler a missing/nonpositive tender amount defaults to the balance. Store excess cash separately. For delayed tender, leave the invoice open and apply configured delayed payment terms if any.
4. Post an immediate payment to the invoice and bank. Recompute the balance. At exactly zero the handler attempts to mark the invoice paid and set its payment method. A remaining positive balance allows another tender on the same validated invoice. Payment creation, bank posting and POS stock issue report failures into the transaction decision. The paid-status call updates the in-memory flags on success, but a failed call does not increment the error count. The payment-method result is ignored. The outer transaction may therefore commit the payment even if the final invoice state or method was not recorded. After an interrupted or inconsistent settlement, reconcile the allocated payment, remaining balance and stored invoice status before retrying.
5. For a return, the explicit credit-note action creates a new credit note against the source invoice and reverses line values. It can receive stock back into inventory under the terminal stock settings. Issuing a credit note and disbursing a refund are separate accounting operations.

[Validation and account selection](../reference/locators/commerce.md#ref-0127d44b4d1b) · [Payment allocation and closure](../reference/locators/commerce.md#ref-109acbfc2bf1) · [Batch stock and transaction result](../reference/locators/commerce.md#ref-442ab71e3346) · [Credit note and stock return](../reference/locators/commerce.md#ref-1e709028b214)

### Peripheral and payment integrations

Order printers use a terminal's destination and template. The print service renders the document with that template, sends it to the configured printer and can return a device or rendering error. Reprint the existing ticket after a device failure. For Stripe Terminal, the payment screen obtains a reader connection, creates a payment intent, collects the payment method, processes and requests capture, then submits the TakePOS card tender in a separate request. These operations span the provider, browser and ERP. On interrupted settlement the integration must reconcile the provider transaction and local invoice balance before retrying a charge. SumUp also crosses an application boundary and its callback records status in the cashier session. These are integration boundaries observed in the ERP’s shipped code. Provider processing and certification are outside this release pin. [Order printing](../reference/locators/commerce.md#ref-a7c9d50da6b1) · [Template and device interface](../reference/locators/commerce.md#ref-6c20943860a4) · [Card reader and intent](../reference/locators/commerce.md#ref-59404a524a64) · [Settlement requests](../reference/locators/commerce.md#ref-2948cce06cc8) · [SumUp result](../reference/locators/commerce.md#ref-023b66b44f47)

## Acceptance cases

| Case | Given and action | Expected result |
| --- | --- | --- |
| POS-1 | A 115.00 ticket has one lot-tracked unit. Terminal stock issue is enabled. Take 40.00 cash, then 75.00 card. | First tender validates the ticket, issues one unit and leaves 75.00. Second tender creates another payment allocation and closes the invoice. Stock has fallen by one unit in total. |
| POS-2 | A cashier receives 120.00 cash for the same unpaid 115.00 ticket and records the 5.00 change. | Allocated payment is 115.00. Cash change is separately recorded as 5.00. |
| POS-3 | Choose delayed settlement on a draft with a positive total. | Invoice becomes validated with the amount outstanding. No immediate payment or bank entry is created. |
| POS-4 | Close today's register control on terminal 1. Attempt a new sale there, then on a separately configured open terminal 2. | Terminal 1 reports the closed control. That control does not close terminal 2. |
| POS-5 | The provider captured a card payment but the local settlement request was interrupted. | The two systems can be in different states. Reconciliation checks the provider outcome and the invoice's recorded payments before posting or retrying. This is a rebuild acceptance criterion. |

The [tender schema](../../schemas/commerce/pos-tender.schema.json) defines explicit positive-sale tender instructions and delayed settlement. The positive amount is an integration convention that makes an operator's tender explicit. It supports split payments without invoking the native handler's full-balance default.
