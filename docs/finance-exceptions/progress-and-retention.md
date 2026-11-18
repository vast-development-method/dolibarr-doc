# Progress invoicing and retained warranty

A contractor may certify 70% completion this month after billing 30% last month. In the current incremental progress mode (`INVOICE_USE_SITUATION=2`), the new invoice stores the 40 percentage points earned this month. Contract amount, lifetime progress, this period's bill, amount retained and cash already paid each have distinct meanings.

## Record and calculation

The invoice stores the cycle reference, sequence counter, final flag, customer, issue date and totals. A line links to the previous line for the same work through `fk_prev_id`. This link allows different work items on the same project to advance independently. Each line retains price, quantity, discount, VAT, progress and resulting money. The retained warranty has a percentage, payment terms and a separate due date on the document.

1. Follow each line's predecessors for the same work. Sum stored progress increments. The history helper also adds linked credit-note line percentages for the same cycle by default. A missing predecessor reference means zero prior progress. A lookup failure takes an error path.
2. On an ordinary individual-line edit, read the requested cumulative percentage at two decimal places. Reject a target below prior progress, cap a value above 100 at 100, then store **increment = accepted cumulative target − prior progress**. The bulk edit route has its own checks. The percentage-update helper leaves marked discount lines alone. Service callers need to distinguish a command accepting a cumulative target from one receiving an already computed increment.
3. Price the new line using that increment. For ordinary tax-exclusive pricing before configured amount rounding, period net = quantity × unit net × (1 − discount/100) × increment/100. Apply the line's tax basis and rounding rules. The current-mode ratio helper returns 1 because the stored line already represents the current period. Subtracting prior invoices again would underbill.
4. Validation checks every loaded line. In incremental mode each must satisfy prior progress + this increment = 100 before the document is marked final. Validating a credit note sourced on a final progress invoice clears that source's final flag. Preserve the signed correction and source relationship so later certificates can reconstruct progress.

[Pricing and rounding](../finance/customer-invoices.md)

## Retention and availability

**Per-invoice warranty.** When there is a non-zero warranty percentage and final-only mode does not apply, the amount helper computes round(invoice gross × warranty percent / 100) at the requested precision. The invoice PDF can show gross less retained warranty as billed now, and a separate warranty amount due on the warranty date. The ordinary receivable balance still begins at full gross. Until actually settled, the retained sum remains owed.

**Final-only warranty.** For a progress cycle with final-only enabled, the amount helper requires a final flag and checks the loaded product/service lines for a stored percentage of at least 100. If those tests pass, it sums gross from the returned previous cycle invoices **plus** current gross and applies the warranty percentage once. Unavailable calculations return −1, a sentinel distinct from a zero monetary amount. The document display test and amount helper have different guards. For example, with increments 30, 40 and 30, the final invoice may legitimately be flagged final with a stored final increment of 30. With that product line loaded, the amount helper returns −1 in final-only mode even though the final flag is set. Verify both results separately.

**Sales journal.** When the warranty feature is enabled, the journal tests the positive warranty rate and, if configured, the final flag. For each included line it computes round(line gross × rate / 100, amount precision), accumulates the retained-receivable posting and deducts that portion from ordinary customer receivables. In incremental mode this uses the line's period gross. The journal calculation can differ from the document helper because they use different scope and rounding.

## Acceptance criteria

| Case | Inputs | Expected result |
| --- | --- | --- |
| EX-PROG-01 | One 1,000.00 net work item, 15% ordinary VAT, zero discount, prior progress 30%, new target 70%. | Store 40 on the new line. Bill net 400.00, VAT 60.00, gross 460.00. With 5% per-invoice retention, 23.00 is retained and 437.00 is billed now. |
| EX-PROG-02 | Prior progress 70%, submit 69% on the ordinary single-line edit route. | Reject without changing the period bill. A target of 105% on this route becomes 100%, generating a 30-point increment. |
| EX-PROG-03 | Two work lines respectively reach 100% and 80% after their current increments. | The overall invoice does not qualify as final. Reaching 100% on just the highest-value line is insufficient. |
| EX-PROG-04 | Last invoice in the 30/40/30 cycle, stored final increment 30%, final flag set, final-only warranty enabled, billable line loaded. | Verify final status independently from warranty amount. The shipped amount helper returns −1. The eligible journal line computes 5% on its period gross (345.00 × 5% = 17.25). |
| EX-PROG-05 | One invoice with two ordinary gross lines of 0.10 each and a 5% warranty, two decimal amounts. | Header-based amount 0.01. Journal line splits of 0.005 round to 0.01 each and total 0.02. Preserve traceability of the two bases. |

Evaluating the invoice and line values in EX-PROG-01 gave a 23.00 per-invoice retention. In EX-PROG-04 the display flag was true and the helper returned −1. The journal entries given above describe the posting rules.

[Progress certificate example](../../examples/finance-exceptions/progress-certificate--second.json) · [Progress certificate schema](../../schemas/finance-exceptions/progress-certificate.schema.json)
