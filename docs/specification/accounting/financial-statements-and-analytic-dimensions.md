# Financial statements, reporting groups and analytical dimensions

## Change the chart used for reporting

The operating entity selects a chart definition. Its internal identifier resolves to a chart version, which determines which account directory entries belong to it. Ledger entries retain their stored account numbers, journal, dates and source references. Invoice and expense allocations can also reference an account directory row. Changing the selected chart changes how reports resolve accounts. This operation supplies no migration between old and new account numbers or directory rows.

Chart management requires the chart-of-accounts permission. Before switching away from a chart already in use, the administration form counts customer invoice lines, supplier invoice lines and expense report lines bound to accounts of the outgoing chart and entity. It also counts any bookkeeping rows in the entity. A positive total asks the operator to confirm the change. Confirmation loads the country-specific chart data, applying an identifier offset that preserves account-parent relationships and separates entities. The service then stores the selected chart identifier. A chart load warning can be followed by the selection change. Selecting a chart does not establish that every required account was loaded successfully.

For example, a posted purchase points to account number 6010. If the incoming chart has an active entry numbered 6010 under a different reporting category, the historical movement can contribute to that new category when a report is regenerated. If the new chart lacks that account, it cannot contribute to a report based on the new chart's list of category members. Its ledger debit remains available to inquiries reading movements directly.

## Build a custom statement

A report definition organizes a set of categories. A category has a code, label, report identifier, company or shared country scope, entity, activation flag, presentation position, balance direction and category type. A simple category gathers account balances. A calculated category contains a formula over category codes. The bookkeeping report chooses active categories for the selected report, entity and company country or country-neutral group. It processes them in increasing position. A company without a country or with no applicable categories cannot derive a populated statement from this path.

| Operation | Actual behavior |
| --- | --- |
| Select accounts for a simple category | Resolve the current chart version, then select active accounts of this entity whose direct category identifier matches. Directory accounts with no active mapping do not enter this category. |
| Sum movements | Select the entity's ledger movements by account number and document date. The sign is debit less credit when the category direction is 1, and credit less debit otherwise. Empty account lists contribute zero. |
| Compare periods | The report shows previous period, selected period and monthly columns. The balance service uses a full calendar month when an explicit month and year are supplied, taking precedence over the separate date bounds. A partial-month selection can therefore differ from a ledger inquiry bounded by exact starting and ending days. |
| Evaluate a calculated row | The report substitutes prior category results into the formula separately for previous period, selected period and each monthly comparison. An inactive category is supplied as zero. A bad formula is displayed as an error. The display position must place dependencies before the category that uses them. |

Consider a June statement with revenue of 1,000 credit and sales returns of 100 debit. If both accounts belong to a credit-positive sales group, net sales displays 900. With cost of goods of 540 debit in a debit-positive cost group, a subsequent formula subtracting cost from net sales displays 360. If cost is an inactive group, its contribution in that expression is zero. The organization must decide which balances belong in each section; account numbers alone do not supply a complete financial statement.

The account-category component also provides a separate many-to-many relation. A category can add or remove an account, enumerate linked accounts and ask which reports contain a particular account. Adding an existing pair returns a no-change result. The custom statement renderer above calls the account's direct-category lookup for its simple rows. A link present solely in the many-to-many relation does not place the account into that renderer's calculation. This distinction matters when importing or maintaining several statements for the same chart.

## Different scopes for a balance, a statement and an analytical allocation

A general ledger balance reads the posted accounts for an entity, including those with no report-category mapping. A custom financial statement additionally depends on the selected chart, active account, category membership, report scope, formula and balance direction. A cost-center distribution would require yet another fact identifying the share of a source line assigned to an analytical account. A general-account category cannot express that a single expense is split 70/30 between departments.

The stable schema defines the following three records.

| Record | Required identity and business meaning | Accounting constraints |
| --- | --- | --- |
| Analytical axis | Entity, code, label, active flag and creator identify a classification such as department. | Code is unique per entity. Creation and update metadata are recorded. |
| Analytical account | Entity, code, label, owning axis and creator identify a member. Optional fields include description and start/end dates. | Code is unique per entity, rather than separately per axis. The account table requires an axis identifier. |
| Analytical distribution | Source-line identifier and source type, analytical account identifier, optional amount, percentage defaulting to 100, entity and creator. | The installed key links the share to an analytical account. The source link is polymorphic and depends on its source type. |

These definitions can represent two distribution rows for a 1,000 expense linked to the same invoice line, with 70% assigned to one department and 30% to another. The documented journal and statement operations do not consume these three tables. The schema supplies no percentage-total constraint, precedence rule for percentage versus amount, automatic rounding-residual assignment, cost-center validation against the document date or recovery behavior after an edited invoice line. A reporting-group sum in the active ERP therefore cannot be interpreted as a completed 700/300 analytical allocation.
