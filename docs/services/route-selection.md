# From a service declaration to the receiving operation

The service [route register](routes.csv) gives the HTTP verb, relative path and argument locations accepted by the dispatcher for the 47 business resources. The [operation catalogue](operation-contracts.jsonl) describes declaration defaults and payloads. Join them on resource and handler. One operation can have more than one path. A declared handler can also lose its path to another handler during registration.

## How to read a route

The paths in the register start immediately after the configured API entry point. Each path segment in braces names an argument. Query arguments belong to the query string, and body arguments are read from the request content. The catalogues use names such as `supplier_orders` for the resource identifier in the operation catalogue. The actual web path for that resource starts with `/supplierorders`. Case, punctuation and ordering of segments are preserved in the path column. Verb and path together identify the target.

| Request | Decision | What the caller supplies |
| --- | --- | --- |
| GET `/orders` | List sales orders under the caller's effective scope | List filters, page, sort order and projected properties are query arguments. |
| GET `/orders/index` | Alias for the same list | Identical handler and argument locations. |
| GET `/orders/{id}` | Read one sales order | Numeric order identity in the path and contact-list option in the query. |
| POST `/orders` | Create a sales order | The request body supplies the record expected by the create operation. |
| POST `/orders/{id}/validate` | Validate the identified order | Identity travels in the path. Warehouse and trigger options have the locations recorded for this operation. Business validation applies after routing. |
| POST `/projects/{id}/contacts` | Attach a contact using the active handler | Project ID in the path. Contact ID, role, source and optional task propagation belong to the body. |

An explicit route annotation selects its verb and path. Parameters occurring in that path become path parameters. For explicit GET and DELETE, other parameters are assigned to the query. For other verbs, the router retains an explicit location or supplies its ordinary input binding. Convention-based registration lowercases the method name and consumes its initial HTTP verb when present. Without one the router chooses GET. An index maps to the collection root. For a conventional method, required primitive parameters with recognized path names can become path segments. Other non-path arguments on GET and DELETE are normally query arguments. The register resolves these choices individually, including the difference between the single-order read and order validation.

## Final dispatch population

The 586 declarations produce **584 reachable handlers** in the registered business-resource table. **413** of these handlers have an explicit route and **171** are registered by naming convention. **43** index aliases bring the total to **627 distinct verb/path registrations**. An alias is another way to reach the same handler. None of these counts includes the separate login exchange, generated explorer pages or site-supplied modules.

Two collisions account for the difference between the declaration and handler counts. The project resource first declares additions under `addContact` and removals under `deleteContact`. Later in the same resource `addToContact` and `deleteToContact` register the same respective verb/path keys. The router assigns the last handler to each key. In particular the active add operation accepts an option to affect tasks. A client generated from the earlier declaration alone can miss that option. The [project contracts](projects.md) identify both operations and the effective transport decision.

Routing resolves the receiving handler and where its arguments come from. Module activation, credentials, entity access, operation permissions and record state determine whether a request can then succeed on an installation. The [credential lifecycle](credential-lifecycle.md) and [authorization decisions](../permissions/decisions.md) describe those subsequent steps.
