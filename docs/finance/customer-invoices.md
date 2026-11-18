# Customer invoices and pricing

A customer invoice records the amount billed for goods or services. Validation assigns the commercial reference. Payment allocation, bank reconciliation and transfer to double-entry bookkeeping each have their own records and dates.

## Records and relationships

| Record | Identity and relationships | Values to retain |
| --- | --- | --- |
| Customer invoice | Stable internal ID, issuing entity, customer, commercial reference. A replacement or credit note can refer to a source invoice. A progress invoice belongs to a cycle. | Invoice and due dates, currency and rate, payment terms/method, kind, status, paid flag, closing reason, author/validator/closer, line totals by tax component |
| Invoice line | Exactly one invoice, optional product or service. A free-text line can carry its own description and price. A service can carry a date interval. | Quantity, pre-discount unit price and input price basis, discount percent, VAT code/rate, local tax rates/types, stored net/tax/gross in company and document currency, buying cost, optional revenue-account binding |
| Customer adjustment | Belongs to a customer, may originate on a deposit, credit note or overpayment. One application command takes either an invoice-line target or an invoice-header target. | Net, tax, gross, foreign amounts, source invoice and destination link. A line application affects the bill. A settlement application affects its outstanding balance. |
| Origin link | Sales order to invoice or contract to invoice. The order conversion copies the amounts, quantities, taxes and discounts onto new lines. | Preserve both records and their references so the issued bill remains intelligible when an upstream record is viewed later. |

The invoice-line table stores the selling price and acquisition cost separately. The pricing example models the selling-price inputs and tax amounts. Margin calculation also needs the acquisition cost. An invoice payment links through an allocation record, covered in [Customer payments](collections.md).

## Lifecycle and command contracts

| Command | Checks | Observable effect |
| --- | --- | --- |
| Create a draft | The API checks invoice-create permission and visibility of the customer. A supplied entity must match the caller's entity. Client-supplied record ID is rejected. The domain operation requires an invoice date. | A draft with internal ID. If a foreign currency is recognised, retain a supplied rate or resolve the configured rate. Dated lookup applies when enabled, with a latest-rate fallback. A missing currency ID falls back to company currency at rate 1. |
| Add a billable line | Invoice-create permission and record access on the API. The domain checks draft status and rejects reversed service dates. If configured, stock availability and sales-pack rounding affect the accepted quantity. | Persist line tax components and update document totals. Treat any rounded sales-pack quantity as the invoiced quantity. |
| Validate | Reload lines and party. Require a draft with at least one line. Normally require create permission. Advanced permissions require the invoice validation right in the domain, while the REST entry also checks create permission and resource access. Configuration can require billing email, customer accounting code, tax IDs or chronological numbering. | Set final reference, state, validator and timestamp. Mark the third party as a customer. In the ordinary trigger path emit `BILL_VALIDATE`. Failure during database writes, stock movement or the trigger rolls back database changes. A repeated REST validation returns 304 for no state change. |
| Replace an invoice | Replacement carries an existing source ID. Validation checks for another replacement. | Abandon the prior invoice with reason `replaced` in the replacement validation transaction. Preserve both audit trails. |
| Close or reopen | The set-to-paid REST action checks invoice-create permission and visibility. A settlement application can also request automatic closure. | Ordinary closure sets status closed and the persisted paid flag. Closure with a reason can leave the flag unset. Reopen restores validated, clears paid, closing reason, actor and date. Neither command records cash. |
| Abandon | Used for an unpaid invoice or a replaced one. | Persist abandonment and release header-bound adjustments. Abandonment alone does not return shipped merchandise to stock. |

Standard invoices, replacements, credit notes, deposits and progress invoices are distinguished by document kind. The state codes for the lifecycle are draft (0), validated (1), closed (2) and abandoned (3). A partial payment normally leaves a validated invoice open. A close reason may record short payment, bad debt or bank charges. Read the monetary balance independently of the label “closed”.

When stock is configured to move on billing, validation with a warehouse can issue a stock movement for a catalogued item. Deposit invoices bypass this branch. A credit note takes the receiving branch. The invoice, warehouse, direction and stock trigger setting determine the expected effect. For an order already physically fulfilled, inspect the installed stock trigger policy when tracing inventory.

## Pricing in a single currency

Let quantity be q, unit price u, discount percentage d, and the percentage of work included in the line calculation p (normally 100). For ordinary VAT, with local taxes disabled and standard line-first rounding, the input-basis line value is q × u × (p/100) × (1 − d/100).

| Price basis | Net | Gross | VAT |
| --- | --- | --- | --- |
| Excluding ordinary VAT | Round the input-basis line value to the configured total precision. | Independently round its unrounded value × (1 + VAT rate/100). | Subtract rounded net from rounded gross. |
| Including ordinary VAT | Divide the discounted input-basis line value by (1 + VAT rate/100), then round. | Round the discounted input-basis line value. | Subtract rounded net from rounded gross. |

With unit-first discounting enabled, round the discount on one unit and the resulting discounted unit price at the configured precision **before** multiplying by quantity and progress. Unit precision and amount precision can differ. Each of the two optional local taxes has its own rate, enablement and basis. Types 1/3/5 use a VAT-exclusive base for all items/products/services respectively. Types 2/4/6 use a main-VAT-inclusive base for the same selectors. Under the special non-collected VAT flag, the informational VAT and collectible gross follow separate branches.

The default document mode sums rounded lines. With `MAIN_ROUNDOFTOTAL_NOT_TOTALOFROUND=1`, the customer document routine instead checks cumulative VAT within each rate in persistent line-ID order and can adjust the current line's VAT and gross. The implementation identifies this adjustment as company-currency specific. The separate `MAIN_ROUNDING_RULE_TOT` can round components to a configured increment. When foreign currency is active, the pricing function runs the line calculation again with the foreign unit price. Consequently converting a rounded header total can disagree with the stored foreign total.

## Worked acceptance cases

| Case | Input and configuration | Expected result |
| --- | --- | --- |
| FIN-INV-01 | Blank draft, caller otherwise authorised, request validation. | Validation fails. No final reference or stock movement. |
| FIN-INV-02 | Quantity 3 at 20.00 net, 10% line discount, 15% ordinary VAT, full progress, two decimal amounts. | Net 54.00, VAT 8.10, gross 62.10. A fixed settlement credit of 10.00 subsequently reduces the balance to 52.10 while issued gross stays 62.10. |
| FIN-INV-03 | Quantity 2 at 11.50 gross, 15% VAT, no discount or local tax. | Net 20.00, VAT 3.00, gross 23.00. Dividing the unit gross by 1.15 establishes the VAT-exclusive unit price. |
| FIN-INV-04 | Two separate net lines of 0.03, each at 20% VAT. Two-decimal amounts, standard VAT, no cash-rounding increment. | Default mode yields VAT 0.02 and gross 0.08. Company-currency VAT-by-rate rounding yields VAT 0.01 and gross 0.07. Persist the one-cent correction on the second line. |
| FIN-INV-05 | Three units at 0.15 net, 10% discount, no VAT. | Ordinary line discounting gives 0.405, rounded to 0.41. With unit-first rounding to two decimals, discount 0.015 rounds to 0.02, leaving 0.13 × 3 = 0.39. |
| FIN-INV-06 | Invoiced line at 100.00 net, VAT 20%, local tax 2% on applicable items, no discount. | A type 1 local tax is 2.00 and gross is 122.00. A type 2 local tax is 2.40 and gross is 122.40. |
| FIN-INV-07 | Validated invoice with an empty cash journal, close with a reason and a shortfall. | Closing metadata changes. Payment allocations and bank lines stay at their previous counts. A write-off or bank transaction needs its own evidence. |

[Normalized pricing example schema](../../schemas/finance/pricing-case.schema.json) · [VAT-by-rate example](../../examples/finance/pricing-case--rate-rounding.json). The schema describes the example's data shape. [Invoice rounding examples](rounding-examples.md) show the monetary outcomes for different calculation policies.

The [invoice processing guide](../invoice-processing/README.md) gives the inputs for adding or amending a line, converting an order, applying a deposit and assigning a ledger account.
