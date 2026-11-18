# Writing ERP records through the service

The [write register](write-routes.csv) identifies the handler that receives each of the 323 effective write-verb routes. Of the 627 callable verb and path pairs, 154 are POST, 81 are PUT, 88 are DELETE and 304 are GET. There are no PATCH routes. Forty-four of the 47 resources expose a write verb. The accountancy, status and workstation resources expose GET routes only. The [five GET handlers with explicit business effects](../services/reads-with-effects.md) include an accounting export that can mark entries as exported.

| How the request reaches the writer | Routes | Where to read the contract |
| --- | ---: | --- |
| All arguments arrive through the path or query | 118 | The register identifies each argument's location. Closing, deleting or linking a record can change several tables even when the body is empty. |
| An object is assigned field by field | 98 | The chosen record writer determines which assigned properties persist. The register identifies explicit member branches, validation and configured field handling. |
| Individually named body arguments | 64 | Match the exact parameter names to the route and use the operation's declared types and defaults. |
| An object whose members the operation selects | 19 | Look up the operation and its literal member reads. Omission can preserve a fetched value, select a default or pass an empty value to the writer. |
| Other structured inputs with distinct child, allocation, file or definition handling | 24 | [Documents and fulfilment](documents-and-fulfilment.md) and [allocations, relationships and files](allocations-and-relationships.md) trace the input into child records. |

## Reading one register row

Use the verb and full path together. A path template can select different operations under different verbs. The resource and operation identify its [declared argument and response contract](../services/operation-contracts.jsonl). The service chapter column is a filename within the [service catalogue](../services/README.md). Multiple names in a cell are space-separated.

| Column | Interpretation |
| --- | --- |
| Path, query and body arguments | Effective router binding for this verb and path. A single body argument called `request_data` commonly receives an entire object. The input handling column describes the next step. |
| Creation or action validation | Members required by the handler's invoked record or action validator. Some validators read the active object's required field metadata. Additional checks can occur later, such as a bank account required when banking is enabled. Consult the service operation for required named arguments and conditional checks. |
| Literal body members and field branches | Names read explicitly or recognized during generic assignment in the handler. They include protected identities, caller context and control flags. A listed name can be ignored or consumed without becoming a database field. Ordinary generic assignment also sees names absent from this column. |
| Required named body arguments and omissible body argument defaults | Separate non-omissible handler parameters from the default values of omissible parameters. A default of null for an entire body leaves the operation's separate member and state checks in effect. |
| Called business operations and nested input | Identifies direct object method calls in first-appearance order, including reads, plus selected child members and collection keys. The method list excludes database, access and service helper calls. Nested input uses `[]` for a list item, brackets with a name for a map key and a vertical bar to separate sibling members in the CSV. |
| Property validation | Indicates record value handling and any specialized pass over configured optional fields. Field definitions, write permission, active settings and the final record writer govern the result. |
| Explicit transaction calls and failure statuses | Lists operations and HTTP statuses written directly in the handler. A blank cell leaves the invoked record, database driver and routing layers to determine the outcome. The presence of rollback in one branch does not establish rollback in every branch. |

For a stored field, follow its object or child identity into the [relational model](../relational-model/README.md). For the two competing project-contact declarations, the [route selection rules](../services/route-selection.md) identify which writes are reachable.

## How an object map reaches the database

For a generic record write, the normalizer visits every member of a list or map recursively. It retains each key, normalizes its value and reconstructs the collection. Names must contain only letters, digits and underscores. Scalar cleaning uses the object's field metadata when available. Numeric and monetary types go through numeric cleaning, rich text through restricted HTML, and email and password fields through their respective cleaners. When metadata does not settle the type, foreign-key names receive numeric cleaning, notes and descriptions allow restricted HTML and other scalars receive plain-text cleaning. Normalized input still passes through the specific create or update writer before anything persists.

Many update operations fetch the existing record and its optional values, then merge entries of `array_options` by key. For these operations an omitted key retains its fetched value. The configured-field normalizer recursively processes submitted members and uses the active field definition where available. An explicit value, an omitted key and a request to change the field definition have different effects. The register distinguishes this path from generic property assignment and from document or line writers that consume options as one argument.

## Controlled handler executions

Three service operations ran against an in-memory transactional store. Each execution used the operation's actual control flow with controlled permissions, parent lookups and substitute child writers. The checks establish the order and boundaries imposed by these handlers. HTTP decoding, production database drivers, deployed permissions and external subscribers sit outside this fixture.

| Operation | Input sequence | Observed result |
| --- | --- | --- |
| Bulk quotation lines | A single line of quantity 3 followed by a group with quantities 4 and 2 | Three rows persisted in order and the call returned the third row's ID. An empty collection returned zero. When a later call rejected the middle line, none of that call's rows persisted. |
| Project contact with optional tasks | No task argument, one selected task, an empty list, then a failure on the second of two tasks | The four calls assigned the project role first. The first added no task role, the second added only the selected task and the third added both project tasks. In the final call the project assignment and first task assignment survived the second task's failure. |
| Supplier order receive | The first dispatch accepted four units and the second dispatch failed. A second call sent the remaining two units | The first four units persisted without final order classification. The second call added two and ran the classification once. |

These different results determine the retry procedure. A parent ID alone cannot distinguish an accepted child from a rejected group. Read back quotation lines, task assignments or order dispatches using the same parent and child identities used in the original request.
