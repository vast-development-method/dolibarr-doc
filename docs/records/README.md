# Record dictionary

This dictionary describes the persistent business records used by the core ERP and the installation structures that support them. Start with the business family and follow the record relationships to subledgers, documents, movements, people or configuration. Technical storage names are locators for the pinned implementation. A different database or object model can preserve the same business identities and relationships.

## Business families

| Family | Records | Includes |
| --- | ---: | --- |
| [Organisation, users and access](foundation.md) | 20 | user account, access group, group membership |
| [Third parties, contacts and relationships](parties.md) | 14 | third party, contact or address, sales assignment |
| [Offers, orders and fulfilment](commercial.md) | 16 | customer proposal, proposal line, proposal product attachments |
| [Product catalogue, prices and variants](catalogue.md) | 15 | product or service, translated product text, kit component |
| [Warehouses, stock and counts](warehouse.md) | 10 | warehouse, warehouse balance, warehouse lot balance |
| [Manufacturing, projects and resource time](production.md) | 15 | bill of materials, bill component, manufacturing order |
| [Sales and supplier invoices](billing.md) | 8 | customer invoice, customer invoice line, recurring customer billing template |
| [Payments, bank and collection orders](cash.md) | 18 | customer receipt, receipt allocation, supplier payment |
| [Accounting, taxes, fixed assets and borrowing](accounting.md) | 24 | chart model, ledger account, report category membership |
| [Employees, membership and field services](people.md) | 34 | association member, membership class, translated membership class |
| [Communication, publishing and documents](content.md) | 29 | website, site page, survey |
| [Classification and custom properties](categories.md) | 26 | category, translated category, bank movement classification |
| [Controlled values and regional reference data](dictionaries.md) | 59 | accounting report row, report definition, business event code |
| [Configured property values](custom-values.md) | 81 | Owner links, uniqueness constraints and dynamic field storage |

## Reading a record

Each record gives its purpose, primary identity, additional uniqueness rules, relationships and field definitions. An outgoing database foreign key is identified in the field meaning with its referenced column. The reverse list names dependent records. A child can repeat a parent key unless its own primary or unique key restricts repetition. A polymorphic link uses both an object type and an ID. Some business relationships are enforced by the owning workflow instead of a database key.

Stored type and declared default refer to the installation schema. `double(24,8)` denotes the declared precision and scale of a floating storage type. Business arithmetic can apply a different rounding precision or retain different amounts in company and document currency. “Null allowed” describes the database column. A workflow may require a value on validation, approval or posting. A dash in the default column means the declaration does not specify a default. An explicit `NULL` default is shown literally.

**Numbers and documents.** Internal IDs identify stored records. User-facing references can be assigned by numbering rules at validation. Dates for creation, operation, value, posting and closure describe different events. Currency amounts, quantities and lifecycle states should be read in the context of the owning business operation.

## Scope of the installation inventory

The 24.0.3 installation ships **410 table definitions** under `htdocs/install/mysql/tables/`. This dictionary describes **288 operational, master, relationship and dictionary tables** plus **81 companion tables** for configured fields. Together they contain **4,951 declared column positions**. Companion layouts are consolidated to avoid repeating identical field definitions. Each included parent record identifies an installation declaration and a release implementation or registration that uses it.

The [installation boundary register](installation-boundaries.md) accounts for the other **41 definitions**. Eighteen belong to excluded feature or extension families. A [follow-up of the other 23 definitions](operational-evidence.md) traced one advanced request log, identified one deprecated state table and found no operational reader or writer in the examined release workflows for the remaining 21. The current table catalogue covers installed persistence. Runtime-generated custom columns, temporary query results, provider-owned data, filesystem documents and migration tables have different lifecycles. The existence of a field does not by itself establish that every configuration exposes it.
