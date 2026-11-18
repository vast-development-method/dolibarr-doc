# Importing and exporting business records

An import dataset declares which business records can be written, how columns map to those records, and which fields may identify an existing row. An export dataset declares a read projection with its own fields, filters and relationships. An exported file may include display labels, joined rows or computed values that need a different import mapping.

## Dataset, mapping, profile and run

| Record | Business meaning |
| --- | --- |
| Dataset | A named definition contributed by an enabled module. It supplies supported fields, mandatory values, destination records, lookup/conversion rules and permitted identifying fields. Export definitions also supply joins, typed filters and ordering. |
| Mapping | Pairs source columns with named destination fields. Extra columns may be ignored. Required target fields need a source. CSV parsing uses a delimiter, enclosure and character set. The shipped import drivers include CSV and XLSX. |
| Profile | A named reusable definition. Import profiles store the dataset and mapping. Export profiles store dataset, ordered fields and filter selections, with a user association. A profile carries instructions for a run. |
| Run | Selected source file and row interval, treatment of the header, matching policy, trigger mode and result counts or row-level errors. The importer assigns a timestamp-based import key. It can be used to locate records that store it. It does not identify a unique external business transaction. |

### Match, simulate and commit

1. **Select a dataset.** Import requires the general import-run right and all rights declared for that dataset. The wizard rechecks dataset permission when opening later steps. Only descriptors for enabled modules participate.
2. **Prepare records.** Pick the file and map its columns. The dataset can convert a business reference to the internal foreign key and supply hidden fields such as author or parent ID. For products, required catalogue fields include reference, label, product/service type, for-sale flag and for-purchase flag.
3. **Select update keys.** Only keys allowed by the dataset are accepted. The loader combines selected predicates and adds entity scope on tables that carry an entity. A single match identifies the record to update. No match allows insertion. Several matches produce an ambiguity error. Without selected update keys the loader can attempt insertion and encounter uniqueness constraints. Running the same file again is therefore sensitive to the key choice.
4. **Simulate.** Run the selected row interval and final dataset statements in a database transaction. Report row errors, warnings, insert and update counts. The wizard rolls the database changes back even after successful simulation. This preview does not reserve IDs or guarantee that a later import sees the same database state.
5. **Execute.** The live phase rereads the file in a new transaction. Recorded row errors cause rollback. Otherwise it performs dataset post-processing and, in bulk-trigger mode, emits the aggregate event before committing. Failure in post-processing or that trigger rolls back the import. Warnings and errors are reported separately. Database rollback does not establish undo semantics for external work performed by extensions.

**Trigger choice affects consumers.** The default fallback is strict per-line mode. The generic writer maps changes to business events subject to its table and object rules. Fast bulk mode accumulates insert/update counts by table and emits one `IMPORT_BULK_DONE` with the import key and statistics. A listener expecting per-record payloads needs to distinguish these two contracts.

### Worked product import

The product dataset exposes reference as an update key. Barcode is available as an additional choice when the barcode module is active. The supplier-price dataset supports a different key set including product, supplier, supplier reference and minimum quantity. Choosing product alone on a price file can match several offers.

Suppose `BOLT-08` exists and `BOLT-10` does not. Import a catalogue file keyed by reference, changing the eight-millimetre bolt's label and adding the ten-millimetre bolt. The simulation should report one selected catalogue record for update and one for insertion before any optional related rows, leaving the original records unchanged. The live run should preserve the ID of `BOLT-08` and create `BOLT-10`. On replay, both references identify existing records. If a mandatory field on the last row generates an error, neither change commits. The [contract](../../schemas/data-exchange/product-import.schema.json) covers the fixed business projection of these five required product fields with reference matching. It represents parsed values. The native file layout and mapping remain configurable. [Valid run](../../examples/data-exchange/product-import--reference.json)

## Export selected records

The operator selects a dataset, chooses and orders output fields, enters typed filters and selects the file writer. A saved profile can restore the choices. Building a file requires the general export-read right plus dataset permission. The field-selection actions also check export-create. Export gathers declared selected fields and uses the descriptor's joins and scope. Ordinary filters are added to the query; supported aggregate filters are handled after grouping. The file writer supplies the header, ordered field titles and transformed rows. The export subsystem supplies UTF-8 CSV, ISO CSV, TSV and Excel 2007 writers.

**Acceptance.** A saved two-field export should reproduce the same ordered column titles when rebuilt against the same dataset. Data rows depend on the current filter and current business records. A user without a required dataset permission receives no generated file from the build action, even with a previously saved profile. An export of a one-to-many relationship can repeat the parent across rows; the grain follows the dataset's joins.
