# Currency from quotation to bank settlement

A company can keep accounts in NAD, quote a customer in USD and collect into a USD bank account. The customer wants to know the USD payable. The warehouse, receivables ledger and bank each need amounts in the unit that belongs to their own record. Preserve both monetary amounts and the exchange decision that produced them when carrying a sale across domains.

## Exchange-rate records

| Record | Identity and meaning | Selection rule |
| --- | --- | --- |
| Registered currency | Currency code and display name in the currency setup of an entity | The bank's currency, the party's preferred currency and the company's accounting currency are separate properties. Module setup registers the company's currency with a rate of one when missing. |
| Rate observation | Registered currency, effective synchronization time, entity, conversion rate and optional direct-rate value | Updating through the currency object's standard rate operation appends an observation. The rate maintenance screen also permits editing individual observations. |
| Document rate | Currency code, currency record and multiplier on the commercial document | For a company amount B, the document equivalent is B × rate. The inverse converts a document amount by dividing. The invoice keeps the selected multiplier when saved. |
| Invoice line | Base and document unit prices and calculated amounts | Quantity, discount, taxable base, taxes and rounding determine the resulting net and gross in each currency. Two rounded totals need not be exact multiples. |
| Payment allocation | Invoice ID, amount applied in each currency, currency code and rate metadata | One payment can allocate value to several compatible invoices. Each invoice balance uses its own allocations. |
| Bank movement | Account amount and, on the foreign-account path, company-currency amount | Positive customer receipts and negative supplier disbursements enter the chosen account in its currency. The allocation remains the evidence for which invoices were paid. |

Currency setup and history are in `htdocs/core/modules/modMultiCurrency.class.php:292–309`, `htdocs/multicurrency/class/multicurrency.class.php:423–505` and `htdocs/multicurrency/multicurrency_rate.php:145–200`. Invoice fields and creation are in `htdocs/compta/facture/class/facture.class.php:375–380,512–531`.

### Which rate applies on a particular date?

With ordinary selection, find the latest dated observation for the registered code in the accessible currency entity scope. With document-date selection enabled and a supplied date, first find the latest observation through the end of that date. If that query returns no row, the implementation retries without the cutoff. A document that predates the entire history can therefore take a rate recorded later. Rows with the same timestamp have no secondary ordering in this lookup. A registered code lacking an observation can appear with an empty rate because the lookup retains currencies without a matching rate row. A failed match ultimately gives ID zero and multiplier one. Customer invoice creation changes an unresolved currency ID to the company code and rate one.

For example, suppose USD observations are 0.052 on 10 June and 0.050 on 20 June, both expressed as USD per NAD. The dated selector gives an invoice dated 15 June the 0.052 rate and an invoice dated 25 June the 0.050 rate. With no earlier history, a 1 June invoice reaches the fallback and gets 0.050. With an explicit nonzero document rate, invoice creation resolves the currency ID and retains the supplied multiplier. Storage, lookup failure and conversion failure represent distinct outcomes. Evidence is in `htdocs/multicurrency/class/multicurrency.class.php:545–577,585–627` and `htdocs/compta/facture/class/facture.class.php:512–531`.

### Importing quotes from a rate service

The built-in synchronisation reads a live set of quotes. When the company's currency differs from the configured provider source, the rebasing routine looks for USD followed by the company code. It divides each quote by the USD-to-company quote. If USD/NAD is 20 and USD/EUR is 0.90, the stored EUR multiplier is 0.045 per NAD and the rebased USD multiplier is 0.05. This particular provider adapter assumes USD-anchored keys for rebasing. That convention belongs to the adapter.

For currencies already registered, the importer appends rates. A caller option also permits registering missing codes. The ordinary append path timestamps rows at insertion. The importer reads the quote set without persisting the provider's quote timestamp on that path. A failed provider response yields an error. A successful provider response with a missing rebasing quote, or unsuccessful individual writes, can still yield the normal completion result. For reconciliation, the relevant evidence is a stored observation for the requested code and date. See `htdocs/multicurrency/class/multicurrency.class.php:637–750` and `htdocs/multicurrency/class/currencyrate.class.php:98–139`.

## Converting a quotation or order into an invoice

A new order can take the party currency. A document created from an existing commercial record can take its currency code. A separate option controls whether it also inherits a nonempty originating multiplier. Invoice creation with a known code and no supplied multiplier invokes rate selection. A deposit created directly from an origin copies its code and rate. Keep the source code, chosen rate and event date as separate decision inputs. Changing the customer's default after the order is recorded has a different effect from explicitly repricing a draft.

The shared change-rate operation has two modes. One preserves the foreign unit prices on ordinary loaded lines and recalculates company prices. The other preserves company unit prices and recalculates foreign prices. A line tied to an exceptional discount, credit or deposit is skipped so that its two historical amounts survive. The change-code operation retrieves the rate without a document date, then requests the second mode. Reapplying a dated rate at every edit would yield a different result. The shared operation writes the header before iterating loaded lines and delegates to each document's update operation. Its return value alone does not establish that every line was recalculated. Sources include `htdocs/commande/card.php:2255–2288`, `htdocs/compta/facture/card.php:3907–3925`, `htdocs/compta/facture/class/facture.class.php:1790–1804` and `htdocs/core/class/commonobject.class.php:2918–3199`.

A price of 200 NAD per unit corresponds to 10 USD at 0.05. At a negotiated new rate of 0.04, preserving 10 USD produces 250 NAD per unit. Preserving 200 NAD produces 8 USD. Those choices affect sales value, gross receivables and potentially margin. The price engine derives the missing input unit price, then applies its line calculation in each monetary context. Currency-specific precision overrides are available in the foreign calculation when the caller passes a currency code. The basic customer-invoice line calls shown here pass the rate and foreign price and omit that trailing currency-code argument. See `htdocs/core/lib/price.lib.php:173–199,405–443` and `htdocs/compta/facture/class/facture.class.php:4454,4736`.

## Collecting and reconciling the amount

For customer payments the entry direction applies to the payment as a whole. With multicurrency enabled, a nonzero value in any foreign allocation selects the foreign-input collection. Otherwise the routine uses the company-input collection. Each nonzero allocation must resolve the invoice's recorded rate. Company input is multiplied by that rate. Foreign input is normally divided by it. A payment grouping invoices with different effective invoice currencies, or conflicting payment currencies, is refused. A foreign bank account is checked against the foreign currency involved. The ordinary collection route supplies no general three-way exchange between an invoice, company and unrelated third bank currency.

Customer collection has a specific final-instalment rule. When the foreign-input amount rounded at total precision equals the foreign remaining balance, take the whole outstanding company amount from that invoice. The remaining-balance query in each currency deducts earlier payments, applied deposits and applied credit notes. This allows both sides to clear despite earlier rounding. Supplier payment creation uses the invoice conversion routine for its allocations and the inspected path has no corresponding final-instalment substitution. The same foreign amount can consequently have a different company residual on a supplier invoice.

| Stage of a customer sale, two-decimal totals | Company currency (NAD) | Document currency (USD) |
| --- | ---: | ---: |
| Issued gross, at 0.05 USD per NAD | 100.01 | 5.00 |
| First receipt entered as 1.00 USD | 20.00 | 1.00 |
| Remaining after first receipt | 80.01 | 4.00 |
| Final receipt entered as exactly 4.00 USD | 80.01 | 4.00 |
| Remaining after both allocations | 0.00 | 0.00 |

For a USD bank account, the two incoming movements are 1.00 and 4.00 USD. Their company amounts are 20.00 and 80.01 NAD. Dividing the final 4.00 by 0.05 in isolation yields 80.00 and leaves one cent. Recomputing both historical collections from today's quote can also change a balance that already cleared. One reconciliation compares the bank statement with the foreign movements. Another compares settled customer receivables with the company allocations. The source payment ID connects them. Whether the invoice status was also marked paid depends on the caller's closure choice.

The customer allocation, currency constraints and movement creation are in `htdocs/compta/paiement/class/paiement.class.php:314–446,481–506,817–925,1371–1382`. The balance and supplier paths are in `htdocs/core/class/commoninvoice.class.php:314–334` and `htdocs/fourn/class/paiementfourn.class.php:174–257`. See also [payment terms and adjustments](../specification/financial/payment-terms-and-settlement-adjustments.md) and [currency services](../services/multicurrencies.md).

The [settlement projection](../../schemas/finance/foreign-currency-settlement.schema.json) and [two-instalment example](../../examples/finance/foreign-currency-settlement.json) retain both amounts for each allocation and the remaining balances after it.
