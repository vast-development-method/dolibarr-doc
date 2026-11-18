# Service contracts

Each chapter describes one service resource. The chapter headings retain the method names used by the implementation. Arguments appear in declaration order. An omitted default in the argument list means the parameter has no declaration default. A default of null can still lead to a missing-field response when required values are absent from the request body. An empty list is written as `[]`.

A route shown beside an operation is the relative route explicitly annotated in its declaration. The [effective route register](routes.csv) gives the resolved verb, resource path and argument locations, including convention-based routes and index aliases. [Route selection](route-selection.md) explains the two colliding declarations. Response codes refer to failure branches in the operation and related operations. Domain validators, the authentication layer and document delivery can also return errors.

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

The table counts public method declarations. Of 586 declarations, 584 own an effective route.

## Shared entry points and scope

[Credential lifecycle and acting identity](credential-lifecycle.md) describes the shared login exchange and the access layer used to resolve each protected request. They precede business dispatch and are documented separately from the 47 service resources and their 586 method declarations. The register excludes development templates and experimental connectors.

[Method and route index](../reference/service-methods.csv) · [Stable module inventory](../coverage/README.md)

## Wire arguments and payload shapes

[Operation contracts in JSON Lines](operation-contracts.jsonl) contains one record per method, including all 1,711 declared arguments. The resource and operation form the lookup key for a contract. The named parameters preserve declaration order.

| Member | How to interpret it |
| --- | --- |
| `handlerOmissible`, `handlerDefault` | Describes calling the method after dispatch. A required positional argument has no default field. An optional argument can have an explicit null default. |
| `declaredInputType`, `annotatedShape` | The former records the ordinary input annotation. The latter adds a more specific property map, list or union where the resource supplies one. “Collection” in the reader chapters can mean a keyed object or a list. A numeric-keyed collection can serialize differently depending on its keys. |
| `routeBinding`, `annotatedBinding` | A path binding appears only when the annotated relative route contains that named parameter. A separate binding describes an explicit source annotation such as body. Other bindings depend on the dispatcher. |
| `wireRequiredAnnotation` | Present only when the wire contract explicitly marks the value required or optional. A handler can require a positional argument while its route documents that value as optional. |
| `bodyValidation` | Identifies the request-body validation routine. Fixed `nonNullMembers` must be present and non-null when that validator runs. Some resources derive their required fields from active model metadata. A configuration-dependent field has a separate condition. The list describes evidenced validator branches and can be supplemented by business-state checks in the chapter. |
| `response` | Describes the returned shape or an absent body. The source label distinguishes a directly returned shape, a delegated result and a declared return type. Property maps give concrete names where declared. An empty property schema leaves that value unconstrained. A model title identifies a record family. |

As an example, the bank-transfer handler defaults the destination-currency amount to zero. A cross-currency transfer still requires a destination amount. The operation chapter gives that conditional rule. Likewise, a default-null request-data argument may lead immediately to a missing-member error when a named field is required. Explicit null, omission in transport and a missing body member have distinct meanings.
