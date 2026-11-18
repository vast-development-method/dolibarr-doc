# Field, relationship and service reference

The functional chapters use business names. These indexes map them back to the installation definitions and API handlers in release 24.0.3. They can be queried with a spreadsheet or CSV reader. All source filenames resolve within the [pinned release tree](locators/reference.md#ref-40d65a157ee2).

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

Each row names the logical table without its configurable prefix, field, declared storage type, column nullability, default expression, inline primary key and the source file/line. A blank default means the DDL omitted a default expression. The text `NULL` means an explicit default. A column accepting null at storage level can be mandatory at a particular business transition. The model uses the upstream installation DDL as a common reference across engines. [Source table definitions](locators/reference.md#ref-7e3b6182cd8d)

[Declared relationships and keys](relationships.csv) lists foreign keys, unique indexes and primary keys from the corresponding key files. For example, the invoice's customer is a declared reference to the party. A document link combines IDs with type discriminators and enforces uniqueness on the ordered endpoints. A missing database foreign key leaves open the possibility of an application-managed relationship such as a source voucher, task or bank line. Trace that relationship through its business chapter before applying a deletion rule.

## REST services

Read the [service contracts by resource](../services/README.md) for arguments, defaults, scope, outcomes and failure branches. The method index can be filtered across resources.

[Service method index](service-methods.csv) lists named public methods in the selected release's API classes, their parameter names, any explicitly annotated HTTP verb and local route, and the source line. For example `createOrderFromProposal` in the customer orders handler declares `POST /createfromproposal/{proposalid}` relative to that resource. The service chapter explains the state and rights. The filename identifies the handler. A blank verb/route means the method has no explicit annotation in its adjacent documentation block. Use the [effective route register](../services/routes.csv) for the resolved verb, path, receiving method and argument locations. The installed Explorer reflects which resources and extensions a particular site exposes. [REST discovery implementation](locators/reference.md#ref-a1dfa01f5788) · [Official REST guide](locators/reference.md#ref-5a167f066088)
