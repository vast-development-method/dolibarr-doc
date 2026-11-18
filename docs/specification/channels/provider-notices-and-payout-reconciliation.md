# Payment notices, payouts and disputes

A payer's browser return, a processor's payment confirmation and a transfer from the processor to the operating bank can occur on different days. Each concerns different records. The processor notice handler verifies the signed event, resolves the service environment and, for a connected multi-company account, can select the entity associated with the provider account. An extension can claim the event before the built-in handlers run.

See `htdocs/public/stripe/ipn.php:119–205`.

## Matching a confirmed payment

The identifier used to find a pending payment request is the provider payment-intent identifier together with the provider site. Its local row includes the business-record links, expected amount, collection type and processing flag. The branch for an unknown intent acknowledges and ignores it. A provider transaction is insufficient by itself to select an invoice.

| Local request | Incoming success handling |
| --- | --- |
| Card or unspecified card type | When the matching request still has processing flag zero, the card branch repairs the request flag. A card request already marked processed does not need that repair. |
| Bank debit | The branch selects a matching debit request already at processing flag one. For a matching confirmed bank-debit method it prepares an invoice payment using the local requested amount. The currency determines which allocation field receives it. |
| Previously posted debit | Before creating a new receipt, the handler searches the payment records for the provider service and external payment identity. An existing receipt changes the duplicate-handling path. |

The request flag and the posted payment row answer different questions. A bank debit can have been presented for collection while the final receipt has yet to be recorded. Reconciliation compares the intent identity, local request, invoice allocation and bank entry. Treating every successful card notice as a new customer payment would duplicate the browser-side settlement.

See `htdocs/public/stripe/ipn.php:375–450`, `460–516` and `524–603`.

## Scheduled and completed payouts

With automatic payout recording enabled, a scheduled payout updates the expected-next-payout setting. A scheduled-notice email can be sent according to configuration. The completed-payout branch clears that setting and resolves two configured accounts, one for receipts held by the processor and one for the operating-bank transfer.

For distinct accounts it converts the provider amount to currency units, records a negative entry on the processor account and a positive entry on the transfer account. It stores the provider payout reference as the operation number on the bank entries and creates reciprocal links. The two entries and their links share a database transaction. The next-payout setting is changed before that transfer transaction, so a cleared schedule does not establish that both bank entries posted. A successful posting can be followed by a completion notice.

A processor settles a payout of 950 after collecting several unrelated invoices. The clearing account decreases by 950 and the operating bank increases by 950. Those two entries explain the transfer without paying any of the invoices a second time. On a replay or an ambiguous delivery outcome, the payout reference on both bank entries provides the reconciliation key. The local receipt identifier for a customer payment serves a different purpose.

See `htdocs/public/stripe/ipn.php:207–252`, `253–323` and `324–360`.

## Disputed and withdrawn funds

The funds-withdrawn event obtains the provider’s dispute amount and fee information, resolves the local payment request and invoice, and logs both the provider dispute amount and the locally recorded amount. Amount equality is not an active gate in this release. The automatic reversal uses the amount on the local payment request.

When the dispute needs a response, the handler can return a closed invoice to validated state, record the dispute as an agenda activity and set the invoice dispute flag. These actions share a transaction. This branch records a dispute that staff need to handle and leaves the payment reversal for the applicable withdrawal path.

The other withdrawal branch prepares a negative payment allocation against the original invoice. Eligibility depends on its accounting transfer state, whether the withdrawal payment already exists and whether the processor bank account is configured. The eligible branch records the negative payment and posts its bank entry. An already-accounted invoice requires separate treatment of the accounting impact. The fee amount captured in the notice or payment note does not itself represent a posted expense.

For a matching full dispute of 120, a negative allocation of 120 reverses the receipt effect where the automatic reversal is allowed. If the processor reports 100 against the same local 120 receipt, the eligible automatic reversal still uses 120. The bank settlement and local reversal then differ by 20, which requires reconciliation. The event type, provider intent, dispute status, original amount, invoice accounting status and presence of an existing negative allocation all affect the outcome.

See `htdocs/public/stripe/ipn.php:1022–1139`, `1140–1203`, `1204–1288` and `1289–1335`.
