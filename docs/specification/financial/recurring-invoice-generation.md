# Recurring customer and supplier invoices

A recurring agreement has three dates with different meanings. The next generation date is the commercial date of the next invoice, the last generation date records the actual run, and the invoice due date follows its payment terms. A delayed run can therefore create a backdated invoice whose due date has already arrived. Each occurrence creates a separate invoice with its own lifecycle, balance and settlement history.

## Template, occurrence and party

| Record | Required relationship or rule |
| --- | --- |
| Customer template | Owns an entity, customer, reference, payment terms, billing lines and the schedule. A recurring issue uses the template's customer. A manually reused template with no recurrence can supply lines for a different customer. |
| Supplier template | Owns a supplier, supplier reference, commercial terms, optional project, description, template lines and a separate schedule. Supplier invoices use a dedicated series of generated supplier references. |
| Generated invoice | Stores the source template ID in its own header. It can inherit other linked business documents from the template. The explicit source field identifies the occurrence without recursively treating every earlier invoice as another origin. |
| Schedule | Stores interval count and unit, scheduled date, completed occurrences, maximum occurrences, suspension flag and actual last generation time. A maximum of zero permits an unbounded number of occurrences. Suspension leaves the schedule and prior occurrences in place. |
| Delivery policy | On customer templates the validate setting distinguishes draft generation, automatic validation and validation with automatic mail delivery. Document production and selected document and mail models are additional inputs. Supplier automation has validation and document-generation steps. |

The ordinary customer card uses invoice-create rights for editing. With advanced permissions enabled, validation has a separate grant. The supplier card resolves combined or split supplier-invoice permissions according to configuration. A right to edit terms does not supply the validation result of the account that runs a scheduled job.

## Selecting due occurrences

The scheduler selects templates in the current entity with a positive interval, suspension off, remaining capacity and a scheduled date no later than the end of the current day. An empty next date also qualifies. An operator may restrict processing to one template. The supplier path has a configurable maximum number of candidates per invocation. A hook can adjust candidate selection. Each selected template is visited once during that invocation.

For a monthly agreement due on 1 May and still outstanding on 10 July, the next generated invoice normally bears 1 May. The following scheduled date becomes 1 June. A subsequent invocation can generate June, then another can generate July. A limit of two total occurrences ends this sequence after June when the count originally stood at zero. A run with no due template produces no invoice.

When an existing scheduled date participates in the calculation, the engine advances from that commercial date by the configured calendar interval in server time. Monthly renewals therefore use a calendar duration. A template without a scheduled date starts from the run time inside the invoice creation path. The supplier worker also updates the template using its original in-memory schedule after creating the invoice. For an initially empty supplier date, this second calculation can persist an empty date again. When interpreting which supplier occurrences remain due, use the stored next date and generated count.

## What the customer invoice inherits

The new invoice begins as a standard draft. Its entity, available links and delivery terms come from the template. The project, payment terms, payment method, destination bank account, public note, private note and document model can take explicit form values with the template as fallback. Commercial terms shared by the entire recurring template include the delivery term code and place. Additional fields use supplied invoice values first and fill absent or empty values from the template. The default author is the actor creating the invoice. A setting can preserve the template's author instead.

A generated line retains the template's quantity, description, selected product, commercial line type, reduction, tax code/rate and local taxes as passed into line creation. Automatic service start and end are line-level choices. A prepaid monthly occurrence dated 1 April can produce a service line running from 1–30 April. The postpaid rule on the same occurrence produces 1–31 March. A line that does not request the start or end fill leaves that value unset on this path. Document totals are recomputed from the created lines. Where multicurrency is enabled, the generation call can request a current exchange rate according to the template. A stored currency code alone therefore cannot explain a changing company-currency amount across occurrences.

For a 100.00 monthly service plus 15% VAT, each otherwise identical occurrence has net 100.00, tax 15.00 and gross 115.00. Two validated occurrences with no settlements leave 230.00 gross billed and two separately payable invoices. Editing the template quantity before the third occurrence changes the next creation. It does not edit the earlier invoices.

## Supplier references and buying data

For a scheduled supplier invoice, invoice creation appends an underscore and the next occurrence number to the template supplier reference. For a template reference RENT, a starting completed count of 4 produces RENT_5. The generated invoice keeps its own internal reference and an explicit source-template ID. Payment-term calculation determines the due date. The recurring line's net buying price, tax details, quantity, unit, discount and supplier item reference feed the generated supplier line.

In resolving buying-cost context when a template has no recorded cost, the implementation first considers the configured cost-price basis. With inventory enabled it can use weighted average for the cost-price or weighted-average policy. A final fallback looks up a supplier offer. This is distinct from the unit amount explicitly copied into the bill. Retain both the supplier bill line value and the underlying pricing assumptions when tracing a recurring purchase.

## Validation, delivery and interruption

The customer worker starts a transaction per template. A failed invoice creation, validation or checked document generation cancels that occurrence. It tracks the error for the specific template, so another template in the same run can succeed. The issuer's output distinguishes generation and mail delivery. When automatic sending is requested on a validated invoice, the worker selects a mail template, tries external billing contacts and falls back to the customer's email. Sender override, CC, BCC, translation and attachment settings belong to the mail template and document configuration. A mail-send failure can be reported alongside successful invoice generation. The external mail delivery and the commercial and banking records have separate lifecycles.

The supplier worker also opens a transaction per candidate. Its decision to validate, build the document and commit uses a cumulative batch error counter. An earlier error can therefore cause subsequent invoices in the same invocation to roll back. Previously committed supplier invoices remain. The supplier worker's final template update does not test its result before committing. Customer invoice creation also advances the counter/date through separate calls without testing each return at that point. The durable source-template ID, generated reference, generation count and stored next date together determine whether a retry is appropriate. A second invoice for the same commercial period would create a second payable or receivable.
