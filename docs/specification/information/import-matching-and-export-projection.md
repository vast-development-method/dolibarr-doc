# Import matching and export projection

A dataset is an operation published by an enabled module. It specifies the business objects involved, exposed fields, destination table order, mandatory values, eligible matching keys, transformations and data permissions. A saved mapping describes the correspondence between columns and this dataset. A run applies that mapping to an uploaded file. The run identifier can be attached to many records, so it is unsuitable as the business identity of an individual record.

## Import mapping and preparation

The operator selects an authorized dataset, input format and file. The delimited-text and workbook readers supply cells to a shared import operation. The operator maps source column positions to qualified business fields, selects the rows to process and chooses any supported duplicate-matching keys. A source column can be left unmapped. Moving columns in the input while retaining an old positional mapping can put valid values under the wrong business fields.

A reusable profile stores its name, dataset and ordered position-to-field pairs. Its owner is either a specific user or shared with all users. Loading it restores that correspondence. The permissions to run the import and access the dataset are evaluated for the current user independently of the profile’s visibility. The descriptor may preselect matching keys when no selection is supplied.

The simulation runs the row operations in a database transaction, records row/column errors and rolls back the transaction deliberately. Execution reads the input again and has its own transaction and generated batch identifier. Simulation does not reserve a business key, freeze the source tables or guarantee the result of later execution. Failure in a selected row during execution rolls back the database changes for the selection. Where a bulk event is requested, it must succeed before commit.

## Conversion and record identity

| Input and dataset rule | Result |
| --- | --- |
| Required mapped value missing | Record the missing mandatory value against its source position. Optional cells proceed to their type or conversion rule. |
| Numeric-looking reference for an associated object | Where the descriptor supports an ID or reference, a plain numeric value is interpreted as an ID. A reference marker can force a numeric-looking identifier to be looked up as a business reference. Conversely an ID marker explicitly requests the identifier interpretation. |
| Dictionary code or object reference | Use the lookup declared by the dataset. A code-or-label rule may fall back to a label. Missing values or ambiguities reported by the lookup identify a source-column error. |
| Unit, normalized number, accounting account or computed amount | Invoke the specific conversion declared for that field. A unit may map to its stored ID or scale. Some profiles can generate customer, supplier or document codes using the configured numbering policy. |
| Destination value absent from the file | A descriptor can inject a fixed value, an entity, a computed result or the prior parent record’s ID. A hidden contribution belongs to the receiving dataset and is applied when the associated table has fields to write. |

Matching applies only to keys allowed by the chosen dataset. The selected key values are combined with **and**, with entity scope added on tables that carry it. A disallowed key or missing matching value reported by the matcher is an error. Social-account keys have a structured-value lookup. Ordinary typed matching compares each submitted value with the corresponding stored field.

| Number of matching parent rows | Write result |
| --- | --- |
| Zero | Attempt an insert, applying destination constraints and carrying the new ID into dependent tables. |
| One | Update the chosen record and carry its existing ID into dependent tables. A successful unchanged update can affect zero stored values. |
| More than one | Fail the match with the filters that produced the ambiguity. The importer does not choose the first candidate. |
| No update keys in effect | Attempt insertion. An existing unique business key can produce a constraint error. |

Parent and child operations run in descriptor order. For a custom-field side record keyed to the parent, the importer checks whether a side record already exists and updates or inserts accordingly. A category association table can be matched by its compound link fields. Matching a duplicate link has different identity mechanics from updating a business record with a standalone row number.

For example, a contact import can distinguish two people sharing a surname by a dataset-supported composite key. If two records still satisfy every selected key, adding an extension-field cell to the input will not disambiguate them unless it participates in an allowed key. An invoice reference consisting only of digits must retain its business-reference interpretation when a receiving relation otherwise treats numbers as internal IDs.

## Events produced by an import

The ordinary strict-row mode resolves object and operation-specific events, including different names for parent creation and line insertion. Integrations can therefore observe specific business writes. The fast bulk mode counts operations by table and insert/update action and publishes one import event with the batch identifier and totals. Unknown event-mode settings fall back to strict-row mode. Integrations depending on individual line events must distinguish these two contracts when reconciling an import.

## Export fields, filters and resulting values

An export uses its own dataset definition with authorized joins, selected columns, filters and format. Operators with export-design authority can select, remove and reorder the fields. File generation checks both export-read authority and access to the chosen dataset. Output drivers can write delimited text in different encodings, tab-separated text or a workbook. The writer generates titles and iterates the resulting rows in the chosen field order.

| Filter family | How the export selects a row |
| --- | --- |
| Text | An exact string compares by equality. A value containing a percent wildcard uses pattern matching. |
| Date | A single date expression can test equality or a boundary. Two date expressions separated by a plus select an inclusive interval, using the supplied date precision. |
| Numeric or duration | Select equality, a leading comparison or an inclusive two-endpoint range. |
| Boolean | A numeric value is used directly. The affirmative text value maps to one, and the other text branch maps to zero. |
| Status or list | A numeric option compares to its value. Text compares to the string or wildcard expression. A form-selected identifier filters only when positive. |

Ordinary filters apply before aggregation. Filters over concatenated aggregate values apply after grouping. Exporting a header joined to multiple details can produce multiple rows per business document, according to the dataset’s declared joins and grouping. Counting a flat export as if every row were one invoice can overstate the number of invoices.

Selected fields can request a descriptor-defined transformation. Examples include turning a negative sentinel into blank or zero, calculating leave days from the worker’s country and half-day code, and querying the current outstanding amount on an invoice. A projected amount can differ from a stored invoice face value. The generic writer reports an unsupported-field error for arbitrary computed extensions. A saved field order is a projection of the records at the time of generation.
