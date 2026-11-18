# Field, relationship and service reference

Use these indexes to move from a [business workflow](source-navigation.md) to its stored fields, relationships and service operations. Each CSV can be opened in a spreadsheet or joined by its column names.

The [record dictionary](../records/README.md) accounts for the installation table population and explains the operational status of each family. The CSVs below are a selected structural index covering 233 tables and 4,277 column positions. A declaration in that index establishes its storage shape. See the [installation boundaries](../records/installation-boundaries.md) before treating an analytical distribution, import staging table or other declaration as an active workflow.

## Storage fields

| Area | Operations you can trace |
| --- | --- |
| [Platform](platform.csv) | Users and groups, configuration, grants, typed object links and webhook history |
| [Parties and sales](parties-sales.csv) | Commercial contacts, proposal lines, customer order lines and shipment allocations |
| [Catalogue and inventory](catalogue-stock.csv) | Variants, batches, per-warehouse balances, stock counts and movements |
| [Purchasing](purchasing.csv) | Vendor offers, order approval, receipts, supplier invoices and payment allocation |
| [Cash and billing](cash-and-invoicing.csv) | Invoice lines and tax, balances, cash desk, bank reconciliation, credit transfer and collection |
| [Ledger and capital](ledger-capital.csv) | Accounts, journals, fiscal periods, assets, depreciation and loans |
| [Projects and manufacturing](projects-production.csv) | Bills of materials, planned and actual consumption, workstations, task time and reservations |
| [People and service](people-service.csv) | Leave, expenses, reimbursements, skills, contracts, interventions and tickets |
| [Community and publishing](community-and-content.csv) | Members, subscriptions, gifts, public content, surveys, mailing targets and notifications |
| [Documents and tools](documents-and-tools.csv) | Classification, indexing, import/export mappings, printing and auxiliary configuration |

Each row identifies its table, field, storage type, nullability, default expression and inline primary key. A blank default means the declaration omits a default expression. The text `NULL` denotes an explicit null default. A column that accepts null in storage can still be mandatory when a transaction changes state.

[Declared relationships and keys](relationships.csv) lists foreign keys, unique indexes and primary keys for these table families. For example, the invoice's customer is a declared reference to the party. A document link combines IDs with type discriminators and enforces uniqueness on the ordered endpoints. A missing database foreign key leaves open the possibility of an application-managed relationship such as a source voucher, task or bank line. Trace that relationship through its business chapter before applying a deletion rule.

## REST services

Read the [service contracts by resource](../services/README.md) for arguments, defaults, scope, outcomes and failure branches. The method index can be filtered across resources.

The [method index](service-methods.csv) gives the public resource and method, ordered parameters and any explicit HTTP verb and local route. For example, `createOrderFromProposal` on the orders resource declares `POST /createfromproposal/{proposalid}` relative to that resource. Empty verb and route cells mean the operation relies on routing conventions. Join the method index to the [effective route register](../services/routes.csv) on resource and method/handler to find the verb, full relative path and input locations. For the two declarations displaced by another handler, see [route selection](../services/route-selection.md).
