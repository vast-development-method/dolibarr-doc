# How Dolibarr executes an ERP operation

A customer order, a shipment and an invoice each own their lifecycle. A shared party identifies the customer. A document link records the origin. Lines, quantities, settlement allocations and accounting entries each retain their own evidence. A program rebuilding this behaviour needs an operation boundary around each business decision. Moving a document to its next state by updating a single status field can miss stock, numbering, links and triggers.

## What an installation enables

| Record or decision | Stable-release behaviour | Consequence for a rebuild |
| --- | --- | --- |
| Configuration value | The persistent key is the pair of name and entity. Global settings and settings in an entity can coexist. | Resolve the effective company and settings before evaluating a rule. |
| Module descriptor | Supplies activation key, dependencies, rights, and optional integration points. A module's own version and its maturity are separate from the ERP release tag. | Keep installation capabilities separate from a user's grants. |
| Enable operation | Checks prerequisites, initializes the requested module, then recursively enables applicable dependencies when requested. Dependency keys may be country-specific. The result contains activation/permission counts and errors. | If a dependency fails, inspect the returned errors and actual enabled modules when retrying. An entire dependency tree has no single guaranteed commit. |
| Module initialization | The common transaction registers the activation flag, module parts, constants, boxes, scheduled jobs, permission definitions and menus as applicable. It also calls directory creation. | Database rollback can undo database writes. File creation is a separate side effect. |
| UI vs service | REST has its own module, authentication and resource handlers. The Explorer discovers resources by enabled module. The resource method performs its own permission and object checks. | Use active installation configuration and the individual operation contract to decide what a caller can do. |

[Configuration key](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_const.key.sql) · [Activation and dependency recursion](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/admin.lib.php#L1203-L1341) · [Common initialization](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/modules/DolibarrModules.class.php#L557-L655) · [REST discovery](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/api/index.php#L243-L332) · [Operator's API guide](https://wiki.dolibarr.org/index.php/Module_Web_Services_API_REST_(developer))

## Permissions belong to an operation on a record

1. Resolve the actor and entity. The REST entry point accepts an entity selection. Authentication resolves a user and verifies the applicable token and entity constraints. Supplying an entity identifier alone grants no business rights.
2. Resolve the capability. Permission definitions have a module, action and optional subaction. Direct assignments and group assignments feed effective rights. Advanced permissions have a configuration gate. Business terms can resolve to different stored names, for example invoice to `facture` and shipping to `expedition`. Disabling a module makes its ordinary `hasRight` check fail.
3. Apply object-level visibility. Depending on the resource this checks entity, parent entity, the external user's linked third party, or an internal salesperson's assignments. For example, an external user cannot acquire the “view all customers” capability through a grant. The table, sharing key and party column matter for each resource.
4. Apply the operation's own state, amount and ownership checks. Read access to a bill establishes neither the right to post a payment nor that an existing payment may be altered.

Core entity resolution normally includes the current entity. A defined set of shared metadata, such as users, user groups and extra field definitions, also includes entity 0. A multicompany provider or a hook can supply different sets. A single blanket filter for every table would produce different results. [Authentication](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/api/class/api_access.class.php#L182-L283) · [Permission lookup](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/user/class/user.class.php#L913-L1049) · [Direct and group rights](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/user/class/user.class.php#L1385-L1541) · [Record access](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/security.lib.php#L922-L1200) · [Entity sets](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/lib/functions.lib.php#L638-L697)

## Transactions, hooks and external effects

The common database interface tracks nesting depth on one connection. An inner begin increments that depth. An inner commit or rollback decrements it. The outermost call sends the database commit or rollback. A child returning an error must communicate it to the owner of the outer transaction. An inner rollback alone supplies no savepoint semantics. [Transaction implementation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/db/DoliDB.class.php#L216-L279)

A hook runs in a named extension context. Its result can add output or replace default behaviour at that call site. A business trigger runs handlers for an action on an object with actor and configuration context. The dispatcher collects errors and returns a negative count on failure. The calling domain operation decides whether that result aborts its transaction. The two link-creation paths in the [document relationship chapter](document-relationships.md) illustrate why that check matters. [Hook manager](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/class/hookmanager.class.php#L194-L213) · [Trigger dispatch](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/class/interfaces.class.php#L211-L279) · [Wiki trigger guide](https://wiki.dolibarr.org/index.php/Triggers_system)

The bundled webhook handler selects targets by event code and activation mode, and sends a payload with the event code and an object snapshot. HTTP 2xx with no transport error counts as success. A blocking target failure contributes to a negative trigger result. A nonblocking delivery failure records a warning. Delivery history uses a separate connection. An outbound delivery can therefore be observed even when the originating database transaction later rolls back. Sending money, fulfilling an order or updating a remote stock balance requires independent reconciliation at the receiver. [Webhook delivery and history](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/core/triggers/interface_95_modWebhook_WebhookTriggers.class.php#L66-L202)

## Acceptance cases

| Given | Action | Observable result |
| --- | --- | --- |
| The same setting name exists for entities 1 and 2 | Read the configured entity's entry | Both records can coexist and retain distinct values. A second row with the same name and entity violates the key. |
| A user has a grant for an ordinary inactive business module | Check the module's action permission | Permission evaluates to false. |
| An external contact has a login for customer A and an invoice belongs to B | Apply the invoice party restriction | The external contact cannot see B's invoice through that check. |
| A parent starts a transaction and a child opens a nested transaction | Child rolls back, parent propagates failure and rolls back | The outer rollback discards both sets of database writes. |
| A receiver accepts a webhook and a later business step fails | Outer operation rolls back | Local business writes can disappear while the receiver retains the request. |
