# Document files, categories and commercial presentation

A customer invoice can belong to a business workflow, produce a payment demand in a chosen language and have a generated file indexed under its own reference. Categories organise records across domains, while document folders organise files. Those associations have different identities and permission checks.

## Classifying business records

A category has an entity, type, parent and label. Its composite key makes a name unique for that type under the same parent in the same entity. A product can belong to many categories through link records. The product record keeps the same identity when classifications change. Adding an existing association reports an already-linked outcome. Where recursive category assignment is enabled, assigning the child can add missing ancestor links. Deleting a category moves its immediate children to its parent and removes the applicable membership links.

The operation to attach a product to a category by ID requires category-read and product- or service-create permission. It retrieves the target record and delegates the membership change. Other record types have independent permission tests. **Acceptance:** create “Parts” under two different product-category parents, assign one product to both, then delete one category. The surviving category still points to the product and any immediate children of the deleted category move up one level.

## Indexing documents

| Business object | Key | Lifecycle |
| --- | --- | --- |
| Manual document directory | Folder ID, parent and entity. A database key covers label, parent and entity. | A folder has a relative path. Subfolders can be created underneath it. The directory card distinguishes read, setup and upload permissions. |
| File index entry | Relative directory path + filename + entity | Records generated/uploaded classification, content fingerprint and originating business object where known. Two different filenames with identical bytes are still independently addressable. |
| Generated main document | Source object type + ID, linked to a generated file | When the generator supplies the output path, the common object indexes the file. A generator can request that the record point to this file as its main document. |

The manual ECM folder card requires read access, uses setup permission for directory changes, and checks upload permission and the upload setting before accepting a file. The automatic document browser builds sections for enabled business modules with their domain read permissions. Regenerating an invoice to the same indexed path refreshes its content fingerprint and source metadata. It need not create a second file index row. File storage and metadata are separate operations: indexing can report a warning after document generation. A rebuild should verify the generated file and its source linkage separately.

## Rendering an invoice and its subtotals

An enabled invoice document model accepts the invoice, output language, source template and display options. For the shipped ODT/ODS invoice generator, the source template is mandatory. The generator assembles substitution data for the business, customer, invoice, contact when present and current user, then processes line substitutions. Extensions can add substitutions. The result can be an office document or a PDF with the appropriate conversion setting. Monetary values originate in the invoice and its lines. Regenerating a translated document must leave invoice amounts, allocations and status intact.

Subtotals are supported for sales proposals, customer orders, invoices and recurring invoices, shipments, supplier price requests, purchase orders and supplier bills. Special structural lines use a signed nesting level and zero commercial price. Positive levels open groups. A subtotal scans preceding lines backwards until a title at the same or shallower level, accumulating line net amounts; a separate routine reads the transaction-currency net amounts. A label is required. For example, an outer section with a 60 line and an inner section with a 40 line displays inner subtotal 40 and outer subtotal 100. The commercial rows still total 100. Counting the two displayed subtotals again would double-count those rows.

## Barcodes and delivery terms

A barcode links an encoded value and a symbology to a catalogue item. Product persistence checks the configured barcode model and the database has a unique key for barcode, barcode type and entity. The label-printing route requires barcode-read permission. It can resolve the value and encoding from a product or a third party, select an encoder and render the label sheet. Printing a second label represents the same identifier and causes no warehouse movement. A missing value or encoding is a label-generation error.

For commercial records that support Incoterms, the stored pair is the selected dictionary term ID and its named location. Updating the pair writes both fields to the document; clearing the term clears the stored location. The PDF presenter resolves the term code and includes the location. For example, selecting FCA with “Windhoek” prints the commercial reference with its named place. This setter and presenter do not create freight charges or alter the invoice tax base.
