# Document origin and related records

An order and an invoice may share a customer and have identical totals without being related. the ERP stores an explicit directed link such as proposal 41 → order 73. A later shipment can refer to the same order and carry its own lines with source order-line IDs. The document edge answers “where did this come from?” Quantities delivered and amounts allocated belong to the corresponding shipment and settlement records.

## Relationship identity

| Concept | Meaning |
| --- | --- |
| Source and target | Each endpoint is an object type paired with a row ID. Numeric row IDs alone can collide across types. A link has its own row ID for direct lookup. |
| Uniqueness | At most one stored row for the ordered tuple of source ID, source type, target ID and target type. Reversing direction describes a different edge. |
| Relation type | Optional classification. Changing this value cannot create a second row for the same ordered pair. |
| Referential integrity | Polymorphic endpoints point to different tables. The link table has no endpoint foreign keys or entity column. The endpoint types determine where existence, entity and business visibility are checked. |

[Link table](../reference/locators/platform.md#ref-a60539e97f35) · [Composite unique index](../reference/locators/platform.md#ref-62e4a9cd2f60) · [Portable relationship contract](../../schemas/platform/document-link.schema.json) · [Worked record](../../examples/platform/document-link--proposal-order.json)

## Create through a business document

When adding an origin to a document, the ERP resolves the source type, normalizes names such as order to `commande`, obtains the target's element type and allows a hook to supply that type. It inserts the edge, then normally runs `OBJECT_LINK_INSERT` with the origin in context. In this path a negative trigger result rolls back the link operation. A duplicate insert follows the database-error path. A successful inner call still depends on the enclosing business transaction.

One exception matters when tracing supplier deposits. While linking a supplier order to an invoice, the ERP looks up supplier invoices that supplied credits or deposits already applied to this invoice. It attempts to link distinct source invoices to the same order and skips the invoice itself and existing edges. These supplementary inserts are best effort. A successful primary link alone cannot prove that every supplementary link exists. [Business document linking](../reference/locators/platform.md#ref-ab4205ede3a7)

## Create or retrieve through REST

| Call relative to `/api/index.php` | Required data or rights | Result |
| --- | --- | --- |
| `POST /objectlinks` | `fk_source`, `sourcetype`, `fk_target`, `targettype`. Write/create rights and record access at **both** ends. | Success envelope with code 200 for a new row. A pre-existing matching link yields 304. Missing a mandatory field yields 400. Insufficient access yields 403. An error returned by the create operation maps to 500. |
| `GET /objectlinks/{id}` | Read rights and record visibility at both ends. | Link record, a denial, or a missing-record response. |
| `GET /objectlinks` with both typed endpoints | This lookup-by-values implementation checks create/write rights and record visibility at both ends. | The existing link or 404 after a permitted lookup with no match. |
| `DELETE /objectlinks/{id}` | Write/create rights and record access at both ends. | Removes the association. Source and target documents retain their separate lifecycles. |

The REST create path checks for an existing link, resolves both endpoint objects, and calls `OBJECTLINK_CREATE` before insert unless trigger execution was suppressed. In 24.0.3 the method increments an error counter on a negative trigger result, but the insert result governs the final commit. A consumer requiring veto semantics must identify the particular entry point. Two concurrent REST calls can both pass the precheck before one loses the unique-key race. The serial duplicate outcome of 304 is therefore insufficient as a universal retry guarantee. [REST contract](../reference/locators/platform.md#ref-2e24c4d5f7c7) · [Lookup by ID](../reference/locators/platform.md#ref-20e701e93a1f) · [Create transaction](../reference/locators/platform.md#ref-241ea4f81690)

## Acceptance cases

| Given | Action | Expected evidence |
| --- | --- | --- |
| Proposal 41 and order 73 exist and actor can write both | Create the directed association, then send the same request again | One stored row. Second serial create reports the existing relationship. |
| Actor can write the proposal and only read the order | Attempt to create the link | Access denied. No new association. |
| A proposal for ten items generated an order for six | Read the header link | It identifies the two documents. The order lines supply the quantity of six. |
| Supplier invoice 82 uses a deposit from supplier invoice 12 | Link order 32 to invoice 82 | The primary edge is 32 → 82. Under normal successful supplementary writes the order also links to invoice 12. |
| Existing source and target are identical to a proposed link with a different classification | Insert both into storage | The four-part unique index permits only one row. |
