# Integrated enterprise resource planning

This blueprint describes how an integrated ERP records agreements, moves stock, pays people, issues invoices and posts to the ledger. Follow a transaction to see who can perform it, which fields change, how quantities and money are calculated, and how a correction reaches the other records. [How to interpret the specification](docs/baseline.md)

**Start with the [worked trading cycle](docs/trade/worked-cycle.md).** Trace ten units received and six sold through two shipments, two collections, a supplier payment and the ledger. The example explains why stock value, commercial margin, cash and tax end at different amounts. The [rebuild contract](docs/platform/rebuild-contract.md) shows which records own each fact and which results an equivalent implementation should reproduce.

## Read the detailed blueprint

| To understand | Start here |
| --- | --- |
| How the decisions in a business process fit together | [Detailed business specifications](docs/specification/README.md) |
| Who owns an amount, quantity, status or relationship | [Complete physical field and key catalogue](docs/relational-model/README.md) · [Application field relationships](docs/relational-model-usage/README.md) · [Business record dictionary](docs/records/README.md) · [Installation structures and their status](docs/records/installation-boundaries.md) |
| What an integration can request and receive | [Service contracts by resource](docs/services/README.md) · [Effective routes and argument binding](docs/services/route-selection.md) · [Credential lifecycle and acting identity](docs/services/credential-lifecycle.md) · [Write payloads and child records](docs/service-writes/README.md) · [Reads that change business records](docs/services/reads-with-effects.md) |
| Which changes can trigger action in another module | [Business events and subscribers](docs/events/README.md) · [Commercial automation](docs/events/commercial-automation.md) · [Subscriber settings, order and replay](docs/event-effects/README.md) |
| Why two reports disagree | [Reporting and reconciliation](docs/reporting/README.md) · [Accounting layouts](docs/exports/ledger-layouts.md) · [Country charts and tax dictionaries](docs/localization/README.md) |
| How policy changes a transaction | [47 operator settings](docs/settings/README.md) · [Company settings](docs/policies/company-and-settings.md) · [Reference numbers](docs/policies/identity-and-numbering.md) · [Stock posting](docs/policies/stock-posting-decisions.md) · [Invoice admission](docs/policies/form-defaults-and-invoice-admission.md) |
| How to reconcile a whole transaction | [Trading and settlement](docs/trade/worked-cycle.md) · [Make to order with a shortage](docs/journeys/building-against-a-shortage.md) · [Commissioning time to cash](docs/journeys/commissioning-time-to-cash.md) |

## Follow a decision across modules

| When you need to reproduce this result | Follow these operations |
| --- | --- |
| A customer accepts a foreign-currency offer and pays in instalments | [Rate selection through final settlement](docs/international/currency-from-quotation-to-settlement.md) · [Language, addresses and negotiated wording](docs/international/language-and-business-identity.md) · [Recipient document and template fields](docs/document-models/README.md) · [Rendered invoice, attachment and delivery history](docs/document-lifecycle/README.md) |
| An operator bills several deliveries or reverses a lot receipt after some units have shipped | [Selection, grouped billing and collection](docs/bulk-operations/README.md) · [Conversion failure and recovery](docs/conversion-recovery/README.md) · [Warehouse and manufacturing reversals](docs/warehouse-corrections/README.md) |
| A visitor applies, registers, donates or signs, or an employee delegates an approval | [Public entry points and records created](docs/public-workflows/README.md) · [Approval, staffing and service teams](docs/workforce-operations/README.md) |
| A list count disagrees with a tile, printed sheet or monthly report | [All 56 operator registers](docs/coverage/operator-list-inventory.md) · [Filters by screen](docs/list-filters/README.md) · [Dashboard widgets and overdue queues](docs/dashboards/README.md) · [Catalogue, sales and project measures](docs/operator-reports/README.md) |
| A tax enquiry, journal export and filed document show different amounts or dates | [Regional reporting and evidence](docs/regional-reporting/README.md) · [Ledger layouts by selector](docs/exports/ledger-layouts.md) · [Audit-file dates and currency](docs/exports/audit-file-dates-and-currency.md) |
| Two people post the same invoice or receive stock at the same time | [Concurrent stock, lot and ledger posting](docs/concurrent-posting/README.md) |
| A sent invoice, payment confirmation or statutory return is disputed | [Invoice delivery and relay evidence](docs/delivery-evidence/README.md) · [Settlement and declaration evidence](docs/operating-boundaries/settlement-and-declarations.md) |
| An installation has extra fields, or a record card shows a different history from its register | [Configured records, histories and reports](docs/operating-boundaries/README.md) |

## Find a business operation

| Business question | Read |
| --- | --- |
| Who can act on a record? What commits together? | [Execution, entity scope and access](docs/platform/execution-and-access.md) · [Document origins and relationship contracts](docs/platform/document-relationships.md) |
| How does an offer become a fulfilled sale? | [Parties and contacts](docs/sales/parties-and-contacts.md) · [Proposals and orders](docs/sales/proposals-and-orders.md) · [Dispatch and invoice origin](docs/sales/dispatch-to-invoice.md) · [Returns, cancellations and refunds](docs/returns/customer-returns.md) |
| How is a supplier order priced, approved and received? | [Catalogue, variants and prices](docs/supply/catalogue.md) · [Purchasing and receiving](docs/supply/purchasing.md) · [Warehouse valuation and transfers](docs/supply/stock.md) · [Supplier invoices and payments](docs/supply/payables.md) |
| How are an invoice and its outstanding balance calculated? | [Customer invoice lines and corrections](docs/invoice-processing/README.md) · [Discounts and rounding](docs/finance/customer-invoices.md) · [Collection and reconciliation](docs/finance/collections.md) · [Progress billing and retention](docs/finance-exceptions/progress-and-retention.md) · [Credits, replacements and deposits](docs/finance-exceptions/corrections-and-deposits.md) · [Invoice rounding examples](docs/finance/rounding-examples.md) |
| What posts to the ledger and when? | [Chart, account binding and report selection](docs/additional-domains/chart-and-reporting.md) · [Bookkeeping](docs/finance/bookkeeping.md) · [Supplier account assignment and journal transfer](docs/finance/supplier-account-preparation.md) · [Fiscal close](docs/treasury/fiscal-close.md) · [Tax geography and rounding](docs/additional-domains/tax-geography-and-rounding.md) |
| How do funds move? | [Payment orders and collections](docs/treasury/payment-orders.md) · [Online settlement](docs/treasury/online-payments.md) · [Bank transfers and obligations](docs/treasury/bank-and-obligations.md) |
| What happens at a till and how is margin calculated? | [Point of sale](docs/commerce/point-of-sale.md) · [Commercial margins](docs/commerce/commercial-margins.md) |
| How are equipment and debt accounted for? | [Fixed assets and depreciation](docs/capital/fixed-assets.md) · [Loans and repayments](docs/capital/loans.md) · [Scheduled versus actual instalments](docs/capital/loan-schedule-and-settlement.md) |
| How do production and project costs arise? | [Bills of materials, workstations and manufacturing orders](docs/operations/manufacturing.md) · [Production quantities, actuals and costing](docs/production-control/README.md) · [Project time, costs and billing](docs/operations/project-time.md) |
| How are employees hired, approved and reimbursed? | [Recruitment and skills](docs/workforce/recruitment-and-skills.md) · [Leave requests](docs/people-services/leave.md) · [Employee balances and monthly accrual](docs/employee-balances/README.md) · [Expense reimbursement](docs/people-services/expenses.md) · [Expense assignment, reimbursement and journal posting](docs/expense-accounting/README.md) |
| How are services and partner relationships delivered? | [Contracts, tickets and interventions](docs/people-services/service-delivery.md) · [Knowledge records](docs/knowledge-partners/knowledge-records.md) · [Partnerships](docs/knowledge-partners/partnerships.md) |
| How do membership and events connect to payments? | [Membership, subscriptions and donations](docs/engagement/membership-and-donations.md) · [Agenda, resources and registrations](docs/engagement/agenda-and-events.md) |
| How does information enter or leave the ERP? | [Import and export](docs/data-exchange/import-export.md) · [Documents, classification and subtotals](docs/data-exchange/documents-and-classification.md) · [Websites and portal visibility](docs/communications/web-and-portal.md) · [Mailing and email collection](docs/communications/email.md) · [Surveys](docs/communications/surveys.md) |
| What runs unattended or integrates with another system? | [Jobs and retention](docs/administration/scheduling-and-retention.md) · [Audit, logs and extensions](docs/administration/audit-and-extensions.md) · [Identity, directories and files](docs/integrations/identity-directories-and-files.md) · [Authoring, printing and desktop tools](docs/integrations/authoring-and-workspace.md) |

## Look up an implementation detail

- [Stable module inventory](docs/coverage/README.md) classifies all 95 bundled descriptors and explains which 84 meet the stable filter. The [other 11 module definitions](docs/coverage/conditional-modules.md) have their own operating guide. [Module-to-chapter map](docs/coverage/guide-map.json)
- [Workflow navigation](docs/reference/source-navigation.md) connects operator tasks to their transaction, record and service contracts.
- [Field, key and service indexes](docs/reference/README.md) connect the business models to installation columns, relationships and API handlers. [Permission declarations](docs/permissions/README.md)
- [JSON Schemas](schemas/) and [worked data examples](examples/) describe selected business operations. Each schema defines its own input or projection. Cross-record rules, balances, permissions, database transactions and side effects are specified in the corresponding chapter.

[Coverage by operation, record and observable outcome](docs/coverage/checkpoint.md)
