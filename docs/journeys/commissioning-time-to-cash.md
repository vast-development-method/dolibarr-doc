# Commissioning time, customer billing and cash collection

Two technicians commission equipment for a customer. They record four chargeable hours on the site task and one internal hour on a separate handover task. The engagement is billed in two-hour service units. Payroll cost, customer price and money received are all visible, and none can be derived from the number of hours alone.

## Opening position and billing basis

The customer is attached to a validated project. Time billing is enabled. The site task is billable and has four planned hours. The handover task is nonbillable. The same commissioning service is assigned to both billable entries. One service unit represents two hours and sells to this customer at 240 before tax. The service has 20% VAT and no discount, using one currency. The invoice conversion uses one line per selected time entry and the service selling price. The contract has no deposit, credit application, withholding or separate material charge in this example. For the bank reconciliation, use an opening account balance of 1,000 and assume no other bank entries in the interval.

| Worker and task | Recorded seconds | Hourly rate on entry | Recorded labor cost | Quantity eligible for billing |
| --- | ---: | ---: | ---: | ---: |
| Technician A, site | 5,400 | 40 | 60 | `1.5 ÷ 2 = 0.75` service units |
| Technician B, site | 9,000 | 60 | 150 | `2.5 ÷ 2 = 1.25` service units |
| Technician C, internal handover | 3,600 | 35 | 35 | None |

The time recorder needs permission to enter time for the applicable task and worker. The project remains a cost carrier even for the nonbillable work. The site task records 14,400 seconds and 210 labor cost. Handover records 3,600 seconds and 35. The combined cost is 245. Recorded rates belong to individual entries, so rerunning the cost sum after a later change to Technician B's master rate ordinarily still uses the rate recorded on the entry. Editing the entry can refresh its rate under the applicable policy. Reaching the four planned hours does not automatically measure task progress or authorize billing.

Task time, rate capture and invoice conversion are described in [Project work, actual cost and time billing](../operations/project-time.md). Detailed cost and report scope are in [Project budgets and realized margin](../specification/planning/project-budget-and-realized-margin.md). Source operations are in `htdocs/projet/class/task.class.php` and `htdocs/projet/tasks/time.php`.

## Converting the work into an invoice

The billing user has invoice creation rights and selects the two uninvoiced site entries. The conversion obtains the customer from the project, retains the project on the new draft invoice, and creates one service line per selected entry. Both lines price a fractional two-hour unit. The service quantity on this invoice is two, although the amount of chargeable labor is four hours.

| Invoice line | Service units | Unit price | Tax-exclusive | VAT | Tax-inclusive |
| --- | ---: | ---: | ---: | ---: | ---: |
| Site entry A | 0.75 | 240 | 180 | 36 | 216 |
| Site entry B | 1.25 | 240 | 300 | 60 | 360 |
| Invoice total | 2.00 | | 480 | 96 | 576 |

Each source time row receives the invoice ID and the specific invoice-line ID generated for it. Those entries fall out of the normal uninvoiced selection. The nonbillable handover remains associated with the project and has no invoice-line backlink. A second invoice for this same work cannot be justified by simply reading the customer's four hours from the task total. A project with no customer cannot enter this billing path. If a later line fails during generation, the conversion's rollback covers the new lines and their corresponding billing links.

Finance validates the draft. The customer owes 576 under the case assumptions, while the project has 480 of tax-exclusive sales value. Nothing in invoice validation produces four more time entries or a bank receipt. The billing conversion is in `htdocs/projet/tasks/time.php`. Invoice validation and balance operations are in `htdocs/compta/facture/class/facture.class.php` and [Customer invoicing](../finance/customer-invoices.md).

## Two payments and one settled invoice

| Event | Cash allocation on invoice | Still due | Bank balance after recording deposit |
| --- | ---: | ---: | ---: |
| Invoice validated | 0 | 576 | 1,000 |
| First customer payment allocated and banked | 200 | 376 | 1,200 |
| Second customer payment allocated and banked | 376 | 0 | 1,576 |

Each payment creates its own receipt. The payment-to-invoice associations identify 200 and 376 on this invoice. The bank-posting operation records each receipt against the chosen account and links the payment to the bank entry. With the option to close fully paid invoices selected, the first payment leaves the invoice open and the second can close it as paid. A zero outstanding balance and the explicit paid/closed state are separate fields of evidence when the automatic closure option is off. A bank statement line subsequently matched to the bank record should not create another receipt for the same payment.

A finance user reconstructs `576 − 200 − 376 = 0` from the allocations. The project manager sees 480 in eligible customer invoices and labor costs of 245, giving a tax-exclusive contribution of 235 and a margin of `235 ÷ 480 × 100 = 49.0%` at one decimal. This assumes the default positive invoice and negative task-time contributions, financial access, and no other project transactions. If the overview includes only paid customer invoices, the 480 becomes eligible at closure. Collecting the second payment must not add another 376 to project sales. Warehouse stock remains unchanged throughout this service case.

The payment record, allocations, bank link and optional invoice closure are implemented in `htdocs/compta/paiement/class/paiement.class.php`. The report's paid-invoice option and denominator are in `htdocs/projet/element.php`. See [Customer collections](../finance/collections.md) and [Bank statements and deposits](../specification/financial/bank-statements-and-cheque-deposits.md).
