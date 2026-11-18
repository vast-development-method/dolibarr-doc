# Company scope and configuration precedence

Four different questions arise when opening a document. Which company owns it? Which companies may share that kind of record? Which settings apply to the current operation? Which records may the actor see? The ERP answers these separately. A shared catalogue does not give an external customer visibility into another customer’s invoices.

## Name and scope of a setting

A setting record contains its name, string value, entity, type, visibility and an optional note. It is unique by name and entity. Entity zero can carry an installation-wide value. Loading a company reads both zero and the active entity, with zero first. The company’s value for the same name then replaces the global value. The loader also supports deployment-provided overrides for a known setting. An enabled module can contribute additional configuration at load time.

| Starting state | Change made in entity 2 | Observable result on reload |
| --- | --- | --- |
| Name exists globally with value 1, no local row | Save local value 0 | Both rows remain. Entity 2 sees 0 absent a higher override. Another entity can still see 1. |
| Global 1 and local 0 | Save an empty string for the local value | The ordinary setter removes the local definition. The inherited global value can apply again. |
| Two entities have distinct local values | Set the name in only one entity | A normal write scoped to that entity does not delete the other entity’s row. |
| A string-valued option controls a business policy | Read it as an integer or boolean | Interpretation belongs to the consumer. Keep the absent value, the literal zero and the caller’s fallback distinct when defining an equivalent policy. |

The common write operation gives an extension the opportunity to handle the change. Its ordinary path performs the replacement inside a transaction. An empty string deletes, whereas a literal `0` persists. For selected credential-like settings it transforms the stored value before insertion. On success the in-memory company configuration is updated. Reloading is important when observing inheritance after deleting a local row; the immediate in-memory assignment and a freshly resolved effective value can differ.

## Scope of a record query

The caller supplies an element key such as an invoice, a numbering series or a user. A sharing provider can return an applicable entity set; an extension hook can further participate. In the ordinary single-company implementation many business elements return the current entity. Users, groups, certain shared metadata and some operational definitions can also include entity zero. For child rows without their own entity column, the parent supplies the scope. A polymorphic link requires resolving the actual endpoint records.

Read permission, ownership by the chosen company and the actor's access to a party remain independent predicates. An invoice query for a customer user also needs the accessible party. A background worker might instead run under a designated user in a configured entity. Applying a single global filter solely on the presence of an `entity` column would give different results for children, shared dictionaries, shared numbering and company documents.

## How configuration changes a business outcome

Consider a supplier invoice created before the accountant changes the company's default account. The document and its existing lines have IDs and may already carry captured amounts or bindings. A new operation that consults the current setup can resolve a different account. To reconstruct which outcome should occur, identify at which step a value becomes a stored fact. A company default, a document header value, an invoice-line amount and a ledger entry have distinct lifetimes.

For a stock example, the same sales document can lead to a warehouse issue at different stages depending on the selected stock policy. The warehouse movement is the durable quantity event. A programme rebuilding stock from commercial document totals alone cannot tell whether a shipment, order or invoice caused that issue. For accounting, the bank line and the related customer payment answer different questions. The relevant entity and policy must accompany the chosen originating record.
