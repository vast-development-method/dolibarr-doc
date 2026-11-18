# Barcode identities and printable labels

A barcode value identifies something in a business context. The encoding specifies how to draw it. The numbering rule assigns values to records, and the label layout determines what else appears on the page. Printing ten copies of one product's code creates ten labels for that same identifier. It does not create ten serial numbers or ten inventory units.

## Assignment and uniqueness

Product records and third-party records each hold a barcode and an encoding identifier. The storage key for each family is the combination of barcode, encoding and entity. Different families have independent tables and numbering rules. A scan that can refer either to a company or a product requires contextual lookup. Product code and warehouse lot text also remain separate identifiers. For example, all boxes of a product may share its product code while originating from different lots.

The standard numbering rules use separate configurable masks for products and for third parties. Each asks its record family for the next value under the selected mask. A missing mask prevents the standard generator from allocating a value. With a 13-character EAN-13 result ending in a check-character marker, the generator takes the first twelve digits and substitutes the calculated check digit at the end. For a payload of `400638133393` the result is `4006381333931`. Leading zeros are meaningful parts of the identifier. A serial counter alone cannot reproduce the full printed value unless the prefix, padding, symbology and check-character rules are also known.

The ordinary product edit verifies the configured barcode system's rules and can distinguish an invalid format, a required but empty barcode and a duplicate. The standard product availability query looks for the same barcode value across the accessible product entities, excluding the record currently edited. It compares the value without using the encoding as a separate match condition. The standard third-party availability query also excludes the current record but searches the third-party table by value across entities. Consequently, normal allocation can reject a duplicate even when the underlying composite storage key would permit it. Product variants that need to be independently scanned need independently identifiable product codes.

The record keys are in `htdocs/install/mysql/tables/llx_product.key.sql` and `htdocs/install/mysql/tables/llx_societe.key.sql`. The pricing-independent numbering, availability and check-digit paths are in `htdocs/core/modules/barcode/mod_barcode_product_standard.php`, `htdocs/core/modules/barcode/mod_barcode_thirdparty_standard.php` and `htdocs/core/lib/barcode.lib.php`. Product record verification is in `htdocs/product/class/product.class.php`.

## Initializing an existing catalog

Catalog initialization is an administrative operation. It can initialize missing product/service codes or missing third-party codes using the configured numbering rule for that family. The operations require the respective product or third-party read permission in addition to administrator access. Each pass limits the number of rows taken from the queue, with 1,000 as the default configured batch size. The write for an individual record obtains the generated value and stores it on that record. A subsequent run can process records still lacking codes. A separate erase action explicitly clears current codes. Filling an empty catalog and replacing existing printed identities have different effects on goods already labeled.

The independent operation paths are in `htdocs/barcode/codeinit.php`. Numbering and print settings are managed in `htdocs/admin/barcode.php`.

## Build a sheet

A user with barcode read rights can supply a value and encoding or select a product or third party. The selected record supplies its barcode and type. A family default can provide the type where it is empty. The operator can choose whether the product reference appears above the symbol and the product label appears below it. Otherwise the sheet uses the configured header, footer and side text. Drawing a manually entered symbol does not update the selected record's master data.

The build action requires a nonempty value and encoding. The chosen encoding resolves to its rendering engine. An unsupported encoding/engine combination or failed symbol generation prevents the document from being produced. The input length limit is 51,200 characters before encoding. The selected symbology can have much tighter constraints. A label sheet requires a label model and at least one sticker. The single-sheet request accepts up to 1,000 copies. A requirement of 1,250 product labels consequently needs more than one request through this screen, using the same value for copies of the same product.

The physical format record carries paper size and orientation, measurement unit, margins, columns, rows, horizontal and vertical spacing, label width and height, font size and optional custom page dimensions. These belong to the sheet. Encoding type, data and rendering engine belong to the symbol. A three-column sheet with ten rows provides thirty positions per page, so 75 identical labels occupy two full pages and fifteen positions on the third when starting with a fresh sheet. The PDF output is a printable artifact, independently of inventory or customer transactions.

Selection and validation are in `htdocs/barcode/printsheet.php`. The layouts and formats are in `htdocs/core/modules/printsheet/modules_labels.php` and `htdocs/install/mysql/tables/llx_c_format_cards.sql`. Encodings are defined in `htdocs/install/mysql/tables/llx_c_barcode_type.sql`.
