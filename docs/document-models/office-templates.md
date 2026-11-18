# Editable templates, party contacts and installed fields

A generic office writer decides which records and values are available. The selected template decides which of those values appear and how often. Supplied templates are useful evidence for rebuilding a form, especially where the same field name changes meaning with the source object. A company can install different files in its template directory and expose a different subset of the writer's values.

## What the installation includes

The supplied set includes 19 text-document templates and one spreadsheet. The [installed template field index](office-template-fields.csv) maps 207 distinct brace-delimited field names in their main document bodies to the files containing them. Repeated occurrences of the same field in a file count once. The index concerns textual fields in the shipped bodies. Writer-provided values unused by those files, extensions, image frames and values in a company's own templates have separate coverage.

| Sample file in its template directory | Distinct body fields | Named repeat sections in the supplied body |
| --- | ---: | --- |
| Bill of materials | 40 | Row |
| Contract | 76 | Row |
| Customer invoice | 93 | Row |
| Manufacturing order | 39 | — |
| Customer order | 83 | Row |
| Product sheet | 45 | Row |
| Project | 110 | Tasks, task resources, task times, task files, project contacts, project files, project references and row |
| Customer proposal | 82 | Row |
| Recruitment vacancy | 64 | — |
| Shipment | 83 | Row |
| Warehouse | 33 | — |
| Supplier invoice | 77 | Row |
| Supplier order | 86 | Row |
| Supplier quotation request | 76 | Row |
| Project task | 39 | Project contacts, project files, task files, task resources and task times |
| Third party, spreadsheet | 18 | — |
| Third party, text document | 54 | — |
| Support ticket | 63 | — |
| User group | 38 | Row |
| User | 13 | — |

For example, `object_ref` appears in 17 supplied templates, `company_name` in 13, `line_qty` in nine, and `object_total_ht` in eight. A company can give its supplier and its customer different layouts even when both use `line_qty`. Creating more order lines increases the repetitions of the row, without creating more document headers. A party spreadsheet and a party text document can describe the same party and expose 18 and 54 distinct fields respectively.

The register describes the supplied template bodies. A supplied office writer without a sample file of the same family, such as the asset, member or supplier-receipt writer, still needs a selected template in the configured paths before it can render meaningful output. The [model register](model-register.csv) identifies those writers separately.

## Party data and repeated contacts

The party writer uses the source party for third-party fields, the current issuer for own-company fields, the acting user for user fields, and shared substitutions for the remaining context. It queries contact IDs whose parent is the selected party. The query has no active-contact predicate, contact-role predicate or explicit ordering. Each returned ID is fetched individually. A successfully fetched contact supplies its own values to a `companycontacts` section when present. An absent repeat section is tolerated. A failure to fetch one contact is recorded while the loop proceeds with the other contacts.

This matters when a company replaces an address label with an account-opening form. A party has two contacts, one active purchasing contact and one inactive contact from an earlier year. The ordinary party document and spreadsheet in the installed set contain no `companycontacts` repeat section. The lookup alone cannot put either contact into that section in those copies. A custom body containing that section can receive both rows because the writer queries by party without filtering their status. An address letter that specifically requires a single billing contact needs a different explicit selection.

For fields whose keys end in “logo”, the writer attempts image substitution from the resolved file. A missing asset is represented by a missing-file marker. An optional image ratio applies while performing image substitution. After the business values, translated label substitutions use the selected output language. The temporal suffix and optional party-name prefix belong to the generated filename. With no temporal suffix the same record and template can reuse a pathname. A timestamp option set to 1 uses year, month, day, hour, minute and second; writes within the same second can still resolve to the same name. The user may select office output or conversion to PDF under the office-output setting.

## Project and user documents

The project example gives a task and its related resources, times and files separate ranges. The writer iterates project tasks and within a task assembles related records. A project-file list uses the project's own document directory. A task-file list instead uses the task directory inside that project. The project-contact and project-reference sets have separate segments. A project containing two tasks, one assigned user on each, and two time records on only the first task should not produce four time records by joining every person to every time row. The time records belong under their task. The project reference block can list selected linked business records independently of the tasks.

The user template also shows why field names alone do not identify the owner. While the party writer passes the acting user to the user substitution builder, the user-record writer passes the **subject user** of the document. Generating an employee sheet as an administrator therefore fills the user fields with the employee's details. The party letter generated by that administrator uses the acting user's details in its user fields. The issuer is a separate substitution source in both cases.

The installed-field catalogue establishes field presence in a default body. Cross-record selection, translation fallback, formatting and authorization are determined by the writer and its calling operation. For the editable invoice's dated substitutions, line repetition and relationship to its originating proposals, see [Document model selection and delivery](../specification/output/document-models-and-delivery.md).
