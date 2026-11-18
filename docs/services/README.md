# Service contracts

Each chapter describes one service resource. Operation identifiers retain their wire spelling. Arguments appear in declaration order. An omitted default in the argument list means the parameter has no declaration default. A default of null can still lead to a missing-field response when required values are absent from the request body. An empty list is written as `[]`.

A route shown beside an operation is the relative route explicitly registered on that operation. Other operations are identified by their resource and method. Response codes refer to failure branches in the operation and its cited local delegates. Domain validators, the authentication layer and document delivery can also return errors.

| Resource | Operations |
| --- | ---: |
| [General-ledger export](accountancy.md) | 1 |
| [Members](members.md) | 21 |
| [Membership types](memberstypes.md) | 5 |
| [Membership subscriptions](subscriptions.md) | 5 |
| [Document exchange](documents.md) | 5 |
| [Email templates](emailtemplates.md) | 8 |
| [Business record links](objectlinks.md) | 5 |
| [Configuration and reference dictionaries](setup.md) | 50 |
| [Service status](status.md) | 1 |
| [Bills of materials](boms.md) | 10 |
| [Classification and category membership](categories.md) | 12 |
| [Calendar activities](agendaevents.md) | 5 |
| [Email campaigns and targets](mailings.md) | 15 |
| [Customer proposals](proposals.md) | 19 |
| [Customer orders and fulfillment](orders.md) | 23 |
| [Bank accounts and transactions](bankaccounts.md) | 14 |
| [Customer invoices and settlement](invoices.md) | 31 |
| [Customer payment records](paiements.md) | 4 |
| [Contracts and service activation](contracts.md) | 13 |
| [Donations](donations.md) | 6 |
| [Event registrations](eventattendees.md) | 8 |
| [Outbound shipments](shipments.md) | 8 |
| [Expense reports and reimbursements](expensereports.md) | 19 |
| [Field interventions](interventions.md) | 14 |
| [Supplier invoices and disbursements](supplier-invoices.md) | 15 |
| [Supplier orders](supplier-orders.md) | 13 |
| [Leave requests](holidays.md) | 10 |
| [Knowledge articles](knowledgemanagement.md) | 8 |
| [Production orders](mos.md) | 9 |
| [Currencies and exchange rates](multicurrencies.md) | 8 |
| [Partnership records](partnerships.md) | 5 |
| [Product catalog, prices and variants](products.md) | 45 |
| [Product lots](productlots.md) | 5 |
| [Stock movements](stockmovements.md) | 3 |
| [Warehouses and balances](warehouses.md) | 6 |
| [Projects and project participation](projects.md) | 18 |
| [Project tasks and time entries](tasks.md) | 14 |
| [Inbound receipts](receptions.md) | 8 |
| [Vacancies and applications](recruitments.md) | 10 |
| [Salary liabilities and payments](salaries.md) | 8 |
| [Party contacts](contacts.md) | 10 |
| [Business partners and related accounts](thirdparties.md) | 43 |
| [Supplier quotations](supplier-proposals.md) | 5 |
| [Support tickets and correspondence](tickets.md) | 10 |
| [Users, groups and subscriptions](users.md) | 22 |
| [Outbound event targets](webhook.md) | 6 |
| [Manufacturing workstations](workstations.md) | 3 |

## Shared entry points and scope

[Credential lifecycle and acting identity](credential-lifecycle.md) describes the shared login exchange and the access layer used to resolve each protected request. They precede business dispatch and are documented separately from the 47 service resources and their 586 operations. The module-builder starter is scaffolding for new development. The optional Zapier connector is marked experimental in the release and falls outside the stable resource inventory.

[Method and route index](../reference/service-methods.csv) · [Stable module inventory](../coverage/README.md)
