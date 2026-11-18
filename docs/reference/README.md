# Field, relationship and service reference

The functional chapters use business names. These indexes map them back to the installation definitions and API handlers in Dolibarr 24.0.3. They can be queried with a spreadsheet or CSV reader. All source filenames resolve within the [pinned release tree](https://github.com/Dolibarr/dolibarr/tree/5c6c7ff6a5112413b1c27221c8d11750afad56f8).

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

Each row names the logical table without its configurable prefix, field, declared storage type, column nullability, default expression, inline primary key and the source file/line. A blank default means the DDL omitted a default expression. The text `NULL` means an explicit default. A column accepting null at storage level can be mandatory at a particular business transition. The model uses the upstream installation DDL as a common reference across engines. [Source table definitions](https://github.com/Dolibarr/dolibarr/tree/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables)

[Declared relationships and keys](relationships.csv) lists foreign keys, unique indexes and primary keys from the corresponding key files. For example, the invoice's customer is a declared reference to the party. A document link combines IDs with type discriminators and enforces uniqueness on the ordered endpoints. A missing database foreign key leaves open the possibility of an application-managed relationship such as a source voucher, task or bank line. Trace that relationship through its business chapter before applying a deletion rule.

## REST services

[Service method index](service-methods.csv) lists named public methods in the selected release's API classes, their parameter names, any explicitly annotated HTTP verb and local route, and the source line. For example `createOrderFromProposal` in the customer orders handler declares `POST /createfromproposal/{proposalid}` relative to that resource. The service chapter explains the state and rights; the filename identifies the handler. A blank verb/route means the method has no explicit annotation in its adjacent documentation block. Consult the installed Explorer for convention-based routing, serialization, availability and parameters. [REST discovery implementation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/api/index.php#L243-L332) · [Official REST guide](https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_(developer))

## Reproduce the indexes

From this repository:

```sh
git clone --branch 24.0.3 --depth 1 https://github.com/Dolibarr/dolibarr.git ../dolibarr-24.0.3
python3 tools/build_reference.py ../dolibarr-24.0.3
git diff --exit-code -- docs/reference
```

The builder requires the pinned Git revision and reads the tables explicitly selected in its source. It omits the explicitly listed superseded columns and excludes external module tables, prototypes and migration history from the selection. It retains physical fields that 24.0.3 still uses despite stale comments, including contract status and the supplier-order source. Key rows retain the table name actually named by each ALTER statement, including upstream filename/table discrepancies. They can reference a column outside this selection. The service index omits the module template, Zapier, the authentication helper, the discouraged password-to-token login API, underscored helpers and explicitly deprecated methods. A method index entry gives a navigation point; only the behavioural chapters describe verified operation semantics. [Selection and extraction rules](../../tools/build_reference.py)
