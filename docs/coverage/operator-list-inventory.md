# Operator register coverage

A search result can represent a party, a document, an individual line, a template or a payment. Identify that unit before comparing counts or adding amounts. The [register inventory](../list-filters/screen-index.csv) classifies 56 screens by their business purpose, owning module and depth of documentation. The [filter dictionary](../list-filters/README.md) describes the inputs and comparisons for 18 of them.

| Register family | Screens | Unit selected and examples |
| --- | ---: | --- |
| Business registers | 43 | Parties, customer and supplier documents, service requests, projects, claims, stock and payment records. A row on the customer payment register can settle several invoices. |
| Accounting assignment | 3 | A customer invoice line, supplier invoice line or expense line. Group by source document only after evaluating the assignment on each eligible line. [Supplier invoice assignment](../finance/supplier-account-preparation.md) · [Expense assignment](../expense-accounting/README.md) |
| Setup catalogues | 3 | A bookkeeping template, asset model or variant attribute definition. A definition may have many transactions or item variants. |
| Identity and operations | 4 | An account, access group, per-user integration credential or scheduled job. The credential list is restricted to the selected user and depends on the feature being enabled. |
| Workspace tools | 1 | A bookmark with private or shared visibility. |
| Public self-service | 1 | A requester’s support ticket, subject to public-interface settings and requester verification. |
| Development reporting | 1 | A separately enabled intra-community report. |

## What each coverage level establishes

All 56 named registers have a linked guide covering the unit selected, eligibility, filters and important differences between totals. The inventory retains module maturity separately: 55 registers belong to stable modules and the [intra-community register](../registers-accounts/intra-community.md) belongs to a development-stage module. The [literal input index](../list-filters/request-keys.csv) contains 1,222 distinct register/input pairs found across 54 registers. The local-tax list and supplier-price list use other controls.

| Lookup | Registers and decisions |
| --- | --- |
| [Commercial and operational filter guides](../list-filters/README.md) | Eighteen customer, supplier, warehouse, project, service and staffing lists, including line-based dates, category intersections and result grain. |
| [Finance and capital](../registers-accounts/README.md) | Journal legs, reusable templates, sales line assignments, fixed assets, models, loans and the development-stage declaration register. |
| [Payments and collections](../registers-payments/README.md) | Customer and supplier payments, bank accounts, miscellaneous cash, cheque deposits, remittance lines, local tax, VAT, social charges, donations and their receipts. |
| [People, catalogue and communications](../registers-operations/README.md) | Members, activities, campaigns, contacts, supplier prices, surveys, resources and variant attributes. |
| [Workforce, identity and self-service](../registers-administration/README.md) | Salary obligations, users, groups, personal integration credentials, scheduled jobs and the requester’s ticket queue. |
| [Parties and assignments](../registers-partners/README.md) | Party search, bookmarks and supplier line account assignments; company, user and chart selection each delimit a different population. |
| [Claims and reimbursements](../expense-accounting/README.md) and [membership subscriptions](../specification/people-and-services/member-subscription-register.md) | A claim line awaiting account assignment, a payment allocated to a claim, and a member's subscription charge have independent identities. |

## Related selections with different units

| Operator selection | Unit and relationship |
| --- | --- |
| [Customer order lines](../operator-reports/customer-order-line-list.md) | One line joins one order and can identify a catalogue item. An order-wide margin can repeat over several rows. |
| Bank entries | A bank movement belongs to an account. Reconciliation matches movements to a statement. An account balance aggregates multiple movements. |
| Collection or transfer batches | A batch header can contain several payment lines. Counting the eligible lines and counting the selected batches yield different totals. |
| Recurring invoice definitions | A definition contains template lines. Each generated invoice can carry the definition as its origin. Several issued documents can share it. |
| [Ledger account matching](../specification/financial/manual-ledger-and-account-matching.md) and [sales journal posting](../specification/accounting/source-journal-postings.md) | Matching selects posted entries. The sales journal starts from invoice lines and tests whether that document has already been transferred. |
| [Stock movement journal](../warehouse-corrections/movement-journal-and-counts.md) | One dated change in quantity. A count or transfer can create several movements. Lot identity, warehouse balance and transfer document are separate units. |
| [Salary settlement](../expense-accounting/README.md) | A salary obligation and its individual payments have separate identities. Reconcile the obligation with its allocated payments and linked bank movements. |

Individual card histories, navigation aliases, report variants, interactive selectors and organisation-defined fields can introduce further populations. A register selector identifies which rows are presented. Its result does not establish whether a user can execute a subsequent write or whether a posting will clear the corresponding open item.
