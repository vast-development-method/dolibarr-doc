# Invoice corrections, deposits and customer credits

A replacement supersedes an issued document. A credit note documents a reduction or refund. A deposit records an advance against a later sale. The source invoice, the customer's available credit, its application and any cash refund have separate records. A ledger trace can therefore explain why a customer's balance moved even when no bank entry exists.

| Action | Eligibility and authority | Durable outcome |
| --- | --- | --- |
| Choose an invoice to replace | The customer-filtered selector includes accessible entities and unpaid validated invoices or unpaid invoices abandoned with reason `abandon`. It requires no payment allocation and no invoice already pointing to the source through the joined source-invoice field. | Creating a draft replacement establishes the source relationship. When validating it, fetch the source and reject a different validated replacement. Abandon the source with reason `replaced` within the validation transaction. |
| Choose an invoice to credit | The selector admits validated or closed documents and excludes credit notes and originals with a replacement. Under progress credit-note configuration, only the highest eligible progress-invoice row ID per cycle is offered. Otherwise progress invoices are excluded. | A credit note can reference the original and preserve a signed correction. Validation of one sourced on a final progress invoice clears that source's final flag. An unpaid cash refund and a credit available for future use represent different disposition choices. |
| Generate a deposit from a commercial origin | Supported source kinds are proposal and customer order. Check date (including future-date policy), requested payment terms, a deposit-enabled term on the origin, and an origin deposit percentage. | Create a separate deposit invoice with source reference, customer, project and currency/rate. Bucket deposit lines by VAT rate **and source VAT code**. Optional automatic validation follows generation. |
| Convert to available credit | Native API requires invoice-create permission, access to the source invoice and an unset paid flag. It looks for an existing adjustment from that source. The outer conversion gate admits deposit, credit note and standard invoices in this path. Ordinary payment closure has its own deposit-conversion path. | Credit note/deposit conversion creates positive adjustment amounts by VAT-rate buckets, including company and foreign net/VAT/gross. The API sums eligible lines with nonzero net and product type below 9, then takes absolute component values. Following successful conversion it closes a non-deposit source, while the deposit branch commits without calling that close operation. |
| Apply as invoice line | Native invoice API checks create permission and destination access. The line operation also checks that the credit belongs to the invoice customer, and rejects a credit already bound at header level. | Insert a negative adjustment line, recalculate invoice totals and link the adjustment to that line in the transaction. Applied tax components reduce the invoice itself. |
| Apply as settlement | Native use-credit-note API checks create permission, destination invoice resource access and existence of the adjustment. The link helper accepts either a line ID or a header ID in one call. | Bind the adjustment to the destination invoice header. Its value enters the applicable credit/deposit sum. No new negative invoice line or bank cash receipt is required. The REST method's own prechecks differ from the line route, so independently verify ownership and availability when designing a normalized cross-customer service. |

[Correction selectors][eligible] · [Validation transaction][replacement] · [Progress correction][creditprogress] · [Deposit generation][deposit] · [Source conversion][convert] · [Line consumption][lineapply] · [Settlement path][settlement] · [Target links][links]

## Tax bases and amounts

For a percentage deposit with multi-VAT splitting, let the intended gross deposit be origin gross × deposit percent / 100. For each VAT-rate/code bucket, the fraction is its gross divided by origin gross (zero if origin gross is zero). Multiply this fraction by the intended gross deposit, then divide by (1 + numeric VAT rate / 100) to obtain the net line input. The non-split-setting branch also forms VAT-keyed lines, using the percentage of each included line's net. The exact final amounts pass through line precision and tax rules. These steps describe this source-generation operation, which treats marked special lines separately. [Deposit buckets and lines][deposit]

For a standard invoice with excess settlement, the API's conversion arithmetic sets available credit = sum of cash allocations + sum of header-bound credit/deposit adjustments − invoiced gross, with zero VAT on that excess. Use an actual positive surplus in this operation. A legal or tax rate is not implied by the worked examples. For a negative credit note, refunding in cash uses a negative allocation and bank movement. Converting it instead makes a positive usable credit. Applying the same financial entitlement twice would double the customer benefit. [Excess credit calculation][excess] · [Cash refunds and allocation](../finance/collections.md)

## Goods returned with a credit note

With stock enabled, invoice-based stock movements active and a warehouse selected, validating a credit note calls the stock reception operation for referenced product lines, passing the line quantity, warehouse and batch. A deposit skips invoice-based stock movements. Reverting the validated credit note to draft takes the opposite stock direction and aborts the draft transition if the movement operation reports an error. Creating the usable monetary credit and posting a cash refund are separate operations from this physical return. [Invoice validation][stock] · [Return to draft][unstock]

## Acceptance criteria

| Case | Given and action | Observe |
| --- | --- | --- |
| EX-ADJ-01 | Invoice A is validated, unpaid and free of allocation/source links. Issue and validate a replacement B. | A is abandoned with reason replaced, B retains A's ID and B has its own final reference. The sales journal skips an unposted original marked replaced. If A already has a cash allocation, it is absent from the replacement selector. |
| EX-ADJ-02 | Order has 115.00 gross at 15% VAT and 80.00 at 0%. Deposit 20%, ordinary VAT, no other charges. | Total deposit 39.00, made of 20.00 net + 3.00 VAT in the first bucket and 16.00 net in the zero-rate bucket. Source order remains 195.00 gross. |
| EX-ADJ-03 | A credit note contains −50.00 net at 15%, −7.50 VAT and −10.00 net at 0%. Convert an eligible source. | Available adjustments of 57.50 gross at 15% and 10.00 gross at 0%, both traceable to the source. No refund is created by conversion. |
| EX-ADJ-04 | Apply an available 11.50 credit (10.00 net, 1.50 VAT) to an unpaid 115.00 bill. | As a bill line, issued gross becomes 103.50. As a header settlement against an already issued invoice, gross remains 115.00 and outstanding is 103.50. Read the recorded destination type before computing the balance. |
| EX-ADJ-05 | An eligible standard invoice totals 100.00, cash allocations are 110.00, no applied adjustments. Convert excess. | A 10.00 adjustment becomes available, with zero VAT. Cash allocations keep their original amounts. |
| EX-ADJ-06 | Try to delete available adjustments from one source after one of the source's adjustment rows has already been applied. | The source-group deletion check finds the consumed line/header association and rejects deletion. |
| EX-ADJ-07 | Stock changes at invoice validation. A customer returns two units of a stock-managed product and receives a credit note for the goods. | Validating the credit note receives two units into the selected warehouse. Verify the quantity movement independently of whether the customer elects a cash refund or reusable credit. |

The service contract's [application command](../../schemas/finance-exceptions/apply-credit.schema.json) names a single destination mode. Matching customer, unused status, sufficient balance and concurrency are service-level checks. A rebuild should atomically claim a credit before applying it and verify that exactly one eligible record changed. [Adjustment deletion and links][adjustment]

[eligible]: ../reference/locators/finance-exceptions.md#ref-758f1ed40a00
[replacement]: ../reference/locators/finance-exceptions.md#ref-f93355c1536c
[creditprogress]: ../reference/locators/finance-exceptions.md#ref-17ef3197566d
[deposit]: ../reference/locators/finance-exceptions.md#ref-3bd5145796e6
[convert]: ../reference/locators/finance-exceptions.md#ref-c799eedbfa84
[excess]: ../reference/locators/finance-exceptions.md#ref-aa0ab384ca5a
[lineapply]: ../reference/locators/finance-exceptions.md#ref-92a14856b8ac
[settlement]: ../reference/locators/finance-exceptions.md#ref-71914fffb84e
[links]: ../reference/locators/finance-exceptions.md#ref-b78181d3fca1
[adjustment]: ../reference/locators/finance-exceptions.md#ref-c417c07d52d7
[stock]: ../reference/locators/finance-exceptions.md#ref-2c131f43a23b
[unstock]: ../reference/locators/finance-exceptions.md#ref-fc83a0ecbade
