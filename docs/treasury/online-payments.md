# Online invoice collection through Stripe and PayPal

The payer opens an online payment page for a business source such as an invoice. Provider confirmation and local posting have separate outcomes. A successful charge can require operator reconciliation when the local invoice transaction fails. Capture the provider reference, amount, currency, target invoice and local posting outcome so the operator can match the two. [Online payment architecture][guide] · [Stripe module][stripewiki] · [PayPal module][paypalwiki]

| Stage | Stripe | PayPal |
| --- | --- | --- |
| Initiate | Enabled Stripe configuration selects provider account/environment. The integration converts display amount into provider currency units, with a zero-decimal currency list. | Enabled PayPal configuration selects its checkout credentials. The public form starts the provider checkout with the amount, currency, return location and business-source tag. |
| Verify payer return | In the payment-intent path, retrieve the intent in the configured account. Compare provider currency and amount to expected values, and require succeeded state. | The handler gets checkout details, then calls the provider to confirm the payment. It accepts the confirmation acknowledgement values Success and SuccessWithWarning and reads the provider transaction ID and payment status. |
| Identify and record | Persist provider service and external transaction ID. A Stripe record can store an extended identifier beginning with the payment-intent ID. | Persist provider service and transaction ID. As on Stripe, later use the invoice settlement record for the allocation and the configured payment bank account for cash. |
| Additional notifications | The Stripe notification handler verifies the provider-signed event. Its succeeded-intent branch distinguishes payment methods. The supported SEPA-debit request path can post the receipt and match the request. Other event types include payout and dispute-related changes. | The documented invoice return path uses the confirmed checkout result. Its evidence is the checkout confirmation and recorded local payment. |

[Provider selection][start] · [PayPal acknowledgement and Stripe verification][verify] · [Stripe event processing][ipn]

**Post a confirmed invoice payment.** The return handler checks the transaction ID against recorded customer payments and donations, including the supported extended-ID form, before local posting. It loads the target invoice and resolves the payment-mode dictionary ID. For a supported company-currency receipt, it opens a database transaction, validates a draft invoice if necessary, records payment with automatic closure enabled and, when banking is enabled, posts to the configured provider bank account (or hook-selected account). Errors in local receipt or bank posting roll back this local transaction. A return in a currency different from the company currency takes the unsupported-currency error branch on this invoice path, despite the separate [distributed collection service](../finance/collections.md) supporting foreign allocations. Preserve the distinction in integration tests. [Duplicate lookup][repeat] · [Invoice post-actions][book]

| Acceptance case | Input | Expected outcome |
| --- | --- | --- |
| TR-WEB-01 | Stripe intent for an expected EUR 25.00 reports succeeded, same currency and 2500 minor units. Validated invoice has EUR 25.00 outstanding. | One local receipt allocation, provider transaction identity and configured bank posting on success. |
| TR-WEB-02 | Same source expects EUR 25.00 but retrieved intent is pending, or amount/currency differs. | Stripe confirmation path rejects the result before normal invoice posting. |
| TR-WEB-03 | Success return arrives again for a transaction already recorded. | Existing transaction lookup prevents a second recording through this path. This sequential replay test does not establish a guarantee for simultaneous callbacks. |
| TR-WEB-04 | Provider confirms a payment, but local company-currency expectation or account configuration fails. | Report the local allocation failure against the provider transaction. Reconcile actual provider funds before any attempt to collect again. |
| TR-WEB-05 | PayPal confirm response contains failure acknowledgement, even though the customer reached the return page. | No normal successful-payment posting for that response. |

[guide]: ../reference/locators/treasury.md#ref-0158cf6e2016
[stripewiki]: ../reference/locators/treasury.md#ref-4cdd18e345c9
[paypalwiki]: ../reference/locators/treasury.md#ref-9c937445f597
[start]: ../reference/locators/treasury.md#ref-c2342ddb70b7
[verify]: ../reference/locators/treasury.md#ref-c7cd1cd025fa
[ipn]: ../reference/locators/treasury.md#ref-22ada40e613a
[repeat]: ../reference/locators/treasury.md#ref-c352dd270176
[book]: ../reference/locators/treasury.md#ref-64af0fb1d3b6
