# Integrated enterprise resource planning

A language-neutral blueprint for rebuilding an integrated ERP. It describes how the ERP joins customer and supplier documents, stock, services, people, cash and accounting. Operation chapters trace business decisions through their data, permissions, state changes and failure outcomes. Schemas use portable business terms. Source locators identify the reference implementation behind individual rules. [Release baseline](docs/baseline.md)

**Start with the [worked trading cycle](docs/trade/worked-cycle.md).** Trace ten units received and six sold through two shipments, two collections, a supplier payment and the ledger. The example explains why stock value, commercial margin, cash and tax end at different amounts. The [rebuild contract](docs/platform/rebuild-contract.md) shows which records own each fact and which results an equivalent implementation should reproduce.

## Read the detailed blueprint

| To understand | Start here |
| --- | --- |
| How the decisions in a business process fit together | [Detailed business specifications](docs/specification/README.md) |
| Who owns an amount, quantity, status or relationship | [Record and field dictionary](docs/records/README.md) · [Installation structures and their status](docs/records/installation-boundaries.md) |
| What an integration can request and receive | [Service contracts by resource](docs/services/README.md) · [Credential lifecycle and acting identity](docs/services/credential-lifecycle.md) |
| Which changes can trigger action in another module | [Business events and subscribers](docs/events/README.md) · [Commercial automation](docs/events/commercial-automation.md) |
| Why two reports disagree | [Reporting and reconciliation](docs/reporting/README.md) · [Accounting layouts](docs/exports/ledger-layouts.md) · [Country charts and tax dictionaries](docs/localization/README.md) |
| How policy changes a transaction | [47 operator settings](docs/settings/README.md) · [Company settings](docs/policies/company-and-settings.md) · [Reference numbers](docs/policies/identity-and-numbering.md) · [Stock posting](docs/policies/stock-posting-decisions.md) · [Invoice admission](docs/policies/form-defaults-and-invoice-admission.md) |
| How to reconcile a whole transaction | [Trading and settlement](docs/trade/worked-cycle.md) · [Make to order with a shortage](docs/journeys/building-against-a-shortage.md) · [Commissioning time to cash](docs/journeys/commissioning-time-to-cash.md) |

## Find a business operation

| Business question | Read |
| --- | --- |
| Who can act on a record? What commits together? | [Execution, entity scope and access](docs/platform/execution-and-access.md) · [Document origins and relationship contracts](docs/platform/document-relationships.md) |
| How does an offer become a fulfilled sale? | [Parties and contacts](docs/sales/parties-and-contacts.md) · [Proposals and orders](docs/sales/proposals-and-orders.md) · [Dispatch and invoice origin](docs/sales/dispatch-to-invoice.md) · [Returns, cancellations and refunds](docs/returns/customer-returns.md) |
| How is a supplier order priced, approved and received? | [Catalogue, variants and prices](docs/supply/catalogue.md) · [Purchasing and receiving](docs/supply/purchasing.md) · [Warehouse valuation and transfers](docs/supply/stock.md) · [Supplier invoices and payments](docs/supply/payables.md) |
| How are an invoice and its outstanding balance calculated? | [Customer invoices, discounts and rounding](docs/finance/customer-invoices.md) · [Collection and reconciliation](docs/finance/collections.md) · [Progress billing and retention](docs/finance-exceptions/progress-and-retention.md) · [Credits, replacements and deposits](docs/finance-exceptions/corrections-and-deposits.md) · [Invoice rounding examples](docs/finance/rounding-examples.md) |
| What posts to the ledger and when? | [Chart, account binding and report selection](docs/additional-domains/chart-and-reporting.md) · [Bookkeeping](docs/finance/bookkeeping.md) · [Fiscal close](docs/treasury/fiscal-close.md) · [Tax geography and rounding](docs/additional-domains/tax-geography-and-rounding.md) |
| How do funds move? | [Payment orders and collections](docs/treasury/payment-orders.md) · [Online settlement](docs/treasury/online-payments.md) · [Bank transfers and obligations](docs/treasury/bank-and-obligations.md) |
| What happens at a till and how is margin calculated? | [TakePOS](docs/commerce/takepos.md) · [Commercial margins](docs/commerce/commercial-margins.md) |
| How are equipment and debt accounted for? | [Fixed assets and depreciation](docs/capital/fixed-assets.md) · [Loans and repayments](docs/capital/loans.md) |
| How do production and project costs arise? | [BOMs, workstations and manufacturing](docs/operations/manufacturing.md) · [Project time, costs and billing](docs/operations/project-time.md) |
| How are employees hired, approved and reimbursed? | [Recruitment and skills](docs/workforce/recruitment-and-skills.md) · [Leave](docs/people-services/leave.md) · [Expense reimbursement](docs/people-services/expenses.md) |
| How are services and partner relationships delivered? | [Contracts, tickets and interventions](docs/people-services/service-delivery.md) · [Knowledge records](docs/knowledge-partners/knowledge-records.md) · [Partnerships](docs/knowledge-partners/partnerships.md) |
| How do membership and events connect to payments? | [Membership, subscriptions and donations](docs/engagement/membership-and-donations.md) · [Agenda, resources and registrations](docs/engagement/agenda-and-events.md) |
| How does information enter or leave the ERP? | [Import and export](docs/data-exchange/import-export.md) · [Documents, classification and subtotals](docs/data-exchange/documents-and-classification.md) · [Websites and portal visibility](docs/communications/web-and-portal.md) · [Mailing and email collection](docs/communications/email.md) · [Surveys](docs/communications/surveys.md) |
| What runs unattended or integrates with another system? | [Jobs and retention](docs/administration/scheduling-and-retention.md) · [Audit, logs and extensions](docs/administration/audit-and-extensions.md) · [Identity, directories and files](docs/integrations/identity-directories-and-files.md) · [Authoring, printing and desktop tools](docs/integrations/authoring-and-workspace.md) |

## Look up an implementation detail

- [Stable module inventory](docs/coverage/README.md) classifies all 95 bundled descriptors and explains which 84 meet the stable filter. [Module-to-chapter map](docs/coverage/guide-map.json)
- [Source navigation](docs/reference/source-navigation.md) pairs operator documentation with the 24.0 Doxygen reference and the pinned implementation.
- [Field, key and service indexes](docs/reference/README.md) connect the business models to installation columns, relationships and API handlers. [Permission declarations](docs/permissions/README.md)
- [JSON Schemas](schemas/) and [worked data examples](examples/) describe selected business operations. Each schema defines its own input or projection. Cross-record rules, balances, permissions, database transactions and side effects are specified in the corresponding chapter.

[Specification coverage and open questions](docs/coverage/checkpoint.md)
