# How the ERP executes an ERP operation

A customer order, a shipment and an invoice each own their lifecycle. A shared party identifies the customer. A document link records the origin. Lines, quantities, settlement allocations and accounting entries each retain their own evidence. A program rebuilding this behaviour needs an operation boundary around each business decision. Moving a document to its next state by updating a single status field can miss stock, numbering, links and triggers.

## What an installation enables

| Record or decision | Stable-release behaviour | Consequence for a rebuild |
| --- | --- | --- |
| Configuration value | The persistent key is the pair of name and entity. Global settings and settings in an entity can coexist. | Resolve the effective company and settings before evaluating a rule. |
| Module descriptor | Supplies activation key, dependencies, rights, and optional integration points. A module's own version and its maturity are separate from the ERP release tag. | Keep installation capabilities separate from a user's grants. |
| Enable operation | Checks prerequisites, initializes the requested module, then recursively enables applicable dependencies when requested. Dependency keys may be country-specific. The result contains activation/permission counts and errors. | If a dependency fails, inspect the returned errors and actual enabled modules when retrying. An entire dependency tree has no single guaranteed commit. |
| Module initialization | The common transaction registers the activation flag, module parts, constants, boxes, scheduled jobs, permission definitions and menus as applicable. It also calls directory creation. | Database rollback can undo database writes. File creation is a separate side effect. |
| UI vs service | REST has its own module, authentication and resource handlers. The Explorer discovers resources by enabled module. The resource method performs its own permission and object checks. | Use active installation configuration and the individual operation contract to decide what a caller can do. |

[Configuration key](../reference/locators/platform.md#ref-99a1fa93886e) · [Activation and dependency recursion](../reference/locators/platform.md#ref-67d4a9fef684) · [Common initialization](../reference/locators/platform.md#ref-c01b6cdbe68f) · [REST discovery](../reference/locators/platform.md#ref-a1dfa01f5788) · [Operator's API guide](../reference/locators/platform.md#ref-5a167f066088)

## Permissions belong to an operation on a record

1. Resolve the actor and entity. The REST entry point accepts an entity selection. Authentication resolves a user and verifies the applicable token and entity constraints. Supplying an entity identifier alone grants no business rights.
2. Resolve the capability. Permission definitions have a module, action and optional subaction. Direct assignments and group assignments feed effective rights. Advanced permissions have a configuration gate. Business terms can resolve to different stored names, for example invoice to `facture` and shipping to `expedition`. Disabling a module makes its ordinary `hasRight` check fail.
3. Apply object-level visibility. Depending on the resource this checks entity, parent entity, the external user's linked third party, or an internal salesperson's assignments. For example, an external user cannot acquire the “view all customers” capability through a grant. The table, sharing key and party column matter for each resource.
4. Apply the operation's own state, amount and ownership checks. Read access to a bill establishes neither the right to post a payment nor that an existing payment may be altered.

Core entity resolution normally includes the current entity. A defined set of shared metadata, such as users, user groups and extra field definitions, also includes entity 0. A multicompany provider or a hook can supply different sets. A single blanket filter for every table would produce different results. [Authentication](../reference/locators/platform.md#ref-6485496c2a52) · [Permission lookup](../reference/locators/platform.md#ref-03e7d514bfcb) · [Direct and group rights](../reference/locators/platform.md#ref-6b58c38b898b) · [Record access](../reference/locators/platform.md#ref-941ab11c6ca8) · [Entity sets](../reference/locators/platform.md#ref-e9b4d34b827b)

## Transactions, hooks and external effects

The common database interface tracks nesting depth on one connection. An inner begin increments that depth. An inner commit or rollback decrements it. The outermost call sends the database commit or rollback. A child returning an error must communicate it to the owner of the outer transaction. An inner rollback alone supplies no savepoint semantics. [Transaction implementation](../reference/locators/platform.md#ref-0c5b92df31e0)

A hook runs in a named extension context. Its result can add output or replace default behaviour at that call site. A business trigger runs handlers for an action on an object with actor and configuration context. The dispatcher collects errors and returns a negative count on failure. The calling domain operation decides whether that result aborts its transaction. The two link-creation paths in the [document relationship chapter](document-relationships.md) illustrate why that check matters. [Hook manager](../reference/locators/platform.md#ref-9a54cfbb3c8e) · [Trigger dispatch](../reference/locators/platform.md#ref-9811c794118b) · [Wiki trigger guide](../reference/locators/platform.md#ref-6c2667ae4e74)

The bundled webhook handler selects targets by event code and activation mode, and sends a payload with the event code and an object snapshot. HTTP 2xx with no transport error counts as success. A blocking target failure contributes to a negative trigger result. A nonblocking delivery failure records a warning. Delivery history uses a separate connection. An outbound delivery can therefore be observed even when the originating database transaction later rolls back. Sending money, fulfilling an order or updating a remote stock balance requires independent reconciliation at the receiver. [Webhook delivery and history](../reference/locators/platform.md#ref-37cd57f7efd3)

## Acceptance cases

| Given | Action | Observable result |
| --- | --- | --- |
| The same setting name exists for entities 1 and 2 | Read the configured entity's entry | Both records can coexist and retain distinct values. A second row with the same name and entity violates the key. |
| A user has a grant for an ordinary inactive business module | Check the module's action permission | Permission evaluates to false. |
| An external contact has a login for customer A and an invoice belongs to B | Apply the invoice party restriction | The external contact cannot see B's invoice through that check. |
| A parent starts a transaction and a child opens a nested transaction | Child rolls back, parent propagates failure and rolls back | The outer rollback discards both sets of database writes. |
| A receiver accepts a webhook and a later business step fails | Outer operation rolls back | Local business writes can disappear while the receiver retains the request. |
