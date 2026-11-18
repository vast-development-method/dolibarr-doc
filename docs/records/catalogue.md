# Product catalogue, prices and variants

Keep product identity independent of its supplier offers, customer-specific tariffs, quantity breaks and variant combinations. Unit selling price, minimum price, purchase cost and inventory valuation answer different business questions.

**Example.** A product priced at 60.00 for a supplier offer of 12 units has a quoted unit cost of 5.00. Keep the supplier, product, break quantity and price on the same offer. A 5.00 unit cost is insufficient evidence of which supplier quotation was used.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Product or service](#record-product) | `product` |
| [Translated product text](#record-product_lang) | `product_lang` |
| [Kit component](#record-product_association) | `product_association` |
| [Sales tariff version](#record-product_price) | `product_price` |
| [Quantity price break](#record-product_price_by_qty) | `product_price_by_qty` |
| [Price-level variation](#record-product_pricerules) | `product_pricerules` |
| [Customer-specific selling price](#record-product_customer_price) | `product_customer_price` |
| [Customer tariff event](#record-product_customer_price_log) | `product_customer_price_log` |
| [Supplier offer](#record-product_fournisseur_price) | `product_fournisseur_price` |
| [Supplier tariff event](#record-product_fournisseur_price_log) | `product_fournisseur_price_log` |
| [Variant axis](#record-product_attribute) | `product_attribute` |
| [Variant option](#record-product_attribute_value) | `product_attribute_value` |
| [Parent and variant](#record-product_attribute_combination) | `product_attribute_combination` |
| [Variant composition](#record-product_attribute_combination2val) | `product_attribute_combination2val` |
| [Variant tariff adjustment](#record-product_attribute_combination_price_level) | `product_attribute_combination_price_level` |

<a id="record-product"></a>

## Product or service

Defines a saleable or purchasable item. Item type, units, inventory policy, pricing and costing influence downstream documents.

**Storage** `product`.
The primary key is `rowid`.
Additional unique keys comprise `ref`, `entity` / `barcode`, `fk_barcode_type`, `entity`.

**Referenced by** [categorie_product](categories.md#record-categorie_product) (fk_product), [contratdet](people.md#record-contratdet) (fk_product), [mrp_production](production.md#record-mrp_production) (fk_product), [product_customer_price](catalogue.md#record-product_customer_price) (fk_product), [product_fournisseur_price](catalogue.md#record-product_fournisseur_price) (fk_product), [product_lang](catalogue.md#record-product_lang) (fk_product), [product_price](catalogue.md#record-product_price) (fk_product), [product_stock](warehouse.md#record-product_stock) (fk_product), [product_warehouse_properties](warehouse.md#record-product_warehouse_properties) (fk_product).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref_ext` | varchar(128) | Yes | — | Identifier supplied by an external application or interface. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_parent` | integer | Yes | `0` | Record one level above this one in the owning hierarchy. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | mediumtext | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note` | mediumtext | Yes | — | Free-text annotation retained with the record. |
| `customcode` | varchar(32) | Yes | — | Customs or commodity classification code used for the item. |
| `fk_country` | integer | Yes | `NULL` | Country associated with the record. References [c_country](dictionaries.md#record-c_country) (rowid). |
| `fk_state` | integer | Yes | `NULL` | Administrative subdivision identity in an address. |
| `price` | double(24,8) | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `price_ttc` | double(24,8) | Yes | `0` | Tax-inclusive price. |
| `price_min` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_min_ttc` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_base_type` | varchar(3) | Yes | `'HT'` | Identifies whether the price was entered before or including tax. |
| `price_label` | varchar(255) | Yes | — | Label attached to a price or pricing condition. |
| `cost_price` | double(24,8) | Yes | `NULL` | Stored cost price used by the applicable cost and margin policy. |
| `default_vat_code` | varchar(10) | Yes | — | Tax treatment proposed as the default when using this entry. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `recuperableonly` | integer | No | `'0'` | Marks the VAT treatment recorded as recoverable-only in the source tax configuration. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `tosell` | tinyint | Yes | `1` | Availability for sales. |
| `tobuy` | tinyint | Yes | `1` | Availability for purchases. |
| `tobatch` | tinyint | No | `0` | Lot or serial tracking policy for the product. |
| `sell_or_eat_by_mandatory` | tinyint | No | `0` | Determines which product expiry dates the lot process requires. |
| `batch_mask` | varchar(32) | Yes | `NULL` | Pattern used to assign lot or serial identifiers to this item. |
| `fk_product_type` | integer | Yes | `0` | Classifies the catalogue record as goods or a service. |
| `duration` | varchar(6) | Yes | — | Duration of the activity or period in the unit used by the owning feature. |
| `seuil_stock_alerte` | float | Yes | `NULL` | Stock quantity at which the low-stock alert applies. |
| `url` | varchar(255) | Yes | — | Web address or navigation target. |
| `barcode` | varchar(180) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `NULL` | Symbology used for the barcode. References [c_barcode_type](dictionaries.md#record-c_barcode_type) (rowid). |
| `accountancy_code_sell` | varchar(32) | Yes | — | Account code used for the respective sales or purchase accounting mapping. |
| `accountancy_code_sell_intra` | varchar(32) | Yes | — | Sales account for the corresponding intra-community or export treatment. |
| `accountancy_code_sell_export` | varchar(32) | Yes | — | Sales account for the corresponding intra-community or export treatment. |
| `accountancy_code_buy` | varchar(32) | Yes | — | Account code used for the respective sales or purchase accounting mapping. |
| `accountancy_code_buy_intra` | varchar(32) | Yes | — | Purchase account for the corresponding intra-community or import treatment. |
| `accountancy_code_buy_export` | varchar(32) | Yes | — | Purchase account for the corresponding intra-community or import treatment. |
| `partnumber` | varchar(32) | Yes | — | Part or serial reference stored on the master record. |
| `net_measure` | float | Yes | `NULL` | Net measure recorded for the item, interpreted with its unit. |
| `net_measure_units` | tinyint | Yes | `NULL` | Unit for the recorded net measure. |
| `weight` | float | Yes | `NULL` | Physical weight in the associated unit. |
| `weight_units` | tinyint | Yes | `NULL` | Unit or scale used to interpret the associated weight. |
| `length` | float | Yes | `NULL` | Item length in the associated length unit. |
| `length_units` | tinyint | Yes | `NULL` | Unit corresponding to this physical dimension. |
| `width` | float | Yes | `NULL` | Physical horizontal or vertical dimension, respectively. |
| `width_units` | tinyint | Yes | `NULL` | Unit corresponding to this physical dimension. |
| `height` | float | Yes | `NULL` | Physical horizontal or vertical dimension, respectively. |
| `height_units` | tinyint | Yes | `NULL` | Unit corresponding to this physical dimension. |
| `surface` | float | Yes | `NULL` | Item area in its associated surface unit. |
| `surface_units` | tinyint | Yes | `NULL` | Unit corresponding to the recorded area. |
| `volume` | float | Yes | `NULL` | Item volume in its associated volume unit. |
| `volume_units` | tinyint | Yes | `NULL` | Unit corresponding to the recorded volume. |
| `stockable_product` | integer | No | `1` | stockable_product. |
| `stock` | real | Yes | — | Aggregate stock figure kept for the product. Warehouse and lot rows provide the location-level quantities. |
| `pmp` | double(24,8) | No | `0` | Weighted average inventory value per unit. |
| `fifo` | double(24,8) | Yes | — | Reserved product-level valuation field. The installation declaration marks it unused. |
| `lifo` | double(24,8) | Yes | — | Reserved product-level valuation field. The installation declaration marks it unused. |
| `fk_default_warehouse` | integer | Yes | `NULL` | Warehouse proposed by default for the item. |
| `fk_default_bom` | integer | Yes | `NULL` | Bill of materials proposed by default for the item. |
| `fk_default_workstation` | integer | Yes | `NULL` | Workstation proposed for the production operation. |
| `canvas` | varchar(32) | Yes | `NULL` | Alternate form or presentation model selected for the object. |
| `finished` | tinyint | Yes | `NULL` | References [c_product_nature](dictionaries.md#record-c_product_nature) (code). |
| `lifetime` | integer | Yes | `NULL` | Shelf-life setting for the item. |
| `qc_frequency` | integer | Yes | `NULL` | Quality inspection frequency. |
| `hidden` | tinyint | Yes | `0` | Historical visibility flag retained in the product table. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `fk_price_expression` | integer | Yes | — | Reserved relationship to the optional formula-pricing component. |
| `desiredstock` | float | Yes | `0` | Desired replenished stock level. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. References [c_units](dictionaries.md#record-c_units) (rowid). |
| `price_autogen` | tinyint | Yes | `0` | Stored indicator for automatic price generation. |
| `fk_project` | integer | Yes | `NULL` | Associated project identity. |
| `mandatory_period` | tinyint | Yes | `0` | Mandatory periods. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `packaging` | float(24,8) | Yes | `NULL` | Packaging quantity or unit arrangement. |

Source locations include `htdocs/install/mysql/tables/llx_product.sql`, `htdocs/install/mysql/tables/llx_product.key.sql`, `htdocs/product/class/product.class.php:75`.

<a id="record-product_lang"></a>

## Translated product text

Stores display text and explanations in a chosen language while preserving the product identity.

**Storage** `product_lang`.
The primary key is `rowid`.
An additional unique key comprises `fk_product`, `lang`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product` | integer | No | `0` | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `lang` | varchar(5) | No | `0` | Language code under which this text or presentation is stored. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note` | mediumtext | Yes | — | Free-text annotation retained with the record. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_lang.sql`, `htdocs/install/mysql/tables/llx_product_lang.key.sql`, `htdocs/product/class/product.class.php:2075`.

<a id="record-product_association"></a>

## Kit component

Relates a parent item to a child with a component quantity, ordering and stock-handling setting.

**Storage** `product_association`.
The primary key is `rowid`.
An additional unique key comprises `fk_product_pere`, `fk_product_fils`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product_pere` | integer | No | `0` | Parent product of the assembly relationship. |
| `fk_product_fils` | integer | No | `0` | Component product included in the parent assembly. |
| `qty` | double | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `incdec` | integer | Yes | `1` | Identifies whether a stock change on the parent also changes this component. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_association.sql`, `htdocs/install/mysql/tables/llx_product_association.key.sql`, `htdocs/product/class/product.class.php:1950`.

<a id="record-product_price"></a>

## Sales tariff version

Records the selling price for a product and level, with its date, price-entry basis and tax configuration.

**Storage** `product_price`.
The primary key is `rowid`.

**Referenced by** [product_price_by_qty](catalogue.md#record-product_price_by_qty) (fk_product_price).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `date_price` | datetime | No | — | Date associated with the price version. |
| `price_level` | smallint | Yes | `1` | Sales price level or tier. |
| `price` | double(24,8) | Yes | `NULL` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `price_ttc` | double(24,8) | Yes | `NULL` | Tax-inclusive price. |
| `price_min` | double(24,8) | Yes | `NULL` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_min_ttc` | double(24,8) | Yes | `NULL` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_base_type` | varchar(3) | Yes | `'HT'` | Identifies whether the price was entered before or including tax. |
| `default_vat_code` | varchar(10) | Yes | — | Tax treatment proposed as the default when using this entry. |
| `tva_tx` | double(7,4) | No | `0` | VAT percentage for this price or line. |
| `recuperableonly` | integer | No | `'0'` | Marks the VAT treatment recorded as recoverable-only in the source tax configuration. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `price_label` | varchar(255) | Yes | — | Label attached to a price or pricing condition. |
| `tosell` | tinyint | Yes | `1` | Availability for sales. |
| `price_by_qty` | integer | No | `0` | Whether quantity-based pricing is enabled for this price entry. |
| `fk_price_expression` | integer | Yes | — | Reserved relationship to the optional formula-pricing component. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_price` | double(24,8) | Yes | `NULL` | Price expressed in the secondary currency. |
| `multicurrency_price_ttc` | double(24,8) | Yes | `NULL` | Tax-inclusive price in the secondary currency. |

Source locations include `htdocs/install/mysql/tables/llx_product_price.sql`, `htdocs/install/mysql/tables/llx_product_price.key.sql`, `htdocs/product/class/product.class.php:2364`.

<a id="record-product_price_by_qty"></a>

## Quantity price break

Adds a quantity-dependent price or reduction to a sales tariff. A product tariff can have several break quantities.

**Storage** `product_price_by_qty`.
The primary key is `rowid`.
An additional unique key comprises `fk_product_price`, `quantity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product_price` | integer | No | — | References [product_price](catalogue.md#record-product_price) (rowid). |
| `price` | double(24,8) | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `price_base_type` | varchar(3) | Yes | `'HT'` | Identifies whether the price was entered before or including tax. |
| `quantity` | double | Yes | `NULL` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `remise_percent` | double | No | `0` | Percentage discount applied to the pricing base. |
| `remise` | double | No | `0` | Discount amount or pricing reduction in the owning record. |
| `unitprice` | double(24,8) | Yes | `0` | Unit price attached to the tariff break. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_price` | double(24,8) | Yes | `NULL` | Price expressed in the secondary currency. |
| `multicurrency_price_ttc` | double(24,8) | Yes | `NULL` | Tax-inclusive price in the secondary currency. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_price_by_qty.sql`, `htdocs/install/mysql/tables/llx_product_price_by_qty.key.sql`, `htdocs/product/class/product.class.php:2393`.

<a id="record-product_pricerules"></a>

## Price-level variation

Specifies the base level and percentage variation used to derive another level's price and minimum price.

**Storage** `product_pricerules`.
The primary key is `rowid`.
An additional unique key comprises `level`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `level` | integer | No | — | Price level on which the resulting rule is used. |
| `fk_level` | integer | No | — | Base price level to which the rule applies its variation. |
| `var_percent` | real | No | — | Percentage variation from the base price. |
| `var_min_percent` | real | No | — | Percentage variation used to calculate the minimum price. |

Source locations include `htdocs/install/mysql/tables/llx_product_pricerules.sql`, `htdocs/install/mysql/tables/llx_product_pricerules.key.sql`, `htdocs/product/class/product.class.php:7333`.

<a id="record-product_customer_price"></a>

## Customer-specific selling price

Specifies a negotiated product selling price for a particular customer including basis, tax and currency information.

**Storage** `product_customer_price`.
The primary key is `rowid`.
An additional unique key comprises `fk_product`, `fk_soc`, `date_begin`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `ref_customer` | varchar(128) | Yes | — | Reference provided by the customer. |
| `date_begin` | date | Yes | — | Start of the applicable interval. |
| `date_end` | date | Yes | — | End of the applicable period. |
| `price` | double(24,8) | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `price_ttc` | double(24,8) | Yes | `0` | Tax-inclusive price. |
| `price_min` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_min_ttc` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_base_type` | varchar(3) | Yes | `'HT'` | Identifies whether the price was entered before or including tax. |
| `default_vat_code` | varchar(10) | Yes | — | Tax treatment proposed as the default when using this entry. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `recuperableonly` | integer | No | `'0'` | Marks the VAT treatment recorded as recoverable-only in the source tax configuration. |
| `localtax1_tx` | varchar(20) | Yes | `'0'` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | varchar(20) | Yes | `'0'` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `discount_percent` | real | Yes | `0` | Discount expressed as a percentage. |
| `fk_user` | integer | Yes | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `price_label` | varchar(255) | Yes | — | Label attached to a price or pricing condition. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_customer_price.sql`, `htdocs/install/mysql/tables/llx_product_customer_price.key.sql`, `htdocs/product/class/product.class.php:7303`.

<a id="record-product_customer_price_log"></a>

## Customer tariff event

Captures a historical change to the product/customer price so an earlier value can be inspected independently.

**Storage** `product_customer_price_log`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `fk_soc` | integer | No | `0` | Third party associated with this record. |
| `ref_customer` | varchar(30) | Yes | — | Reference provided by the customer. |
| `date_begin` | date | Yes | — | Start of the applicable interval. |
| `date_end` | date | Yes | — | End of the applicable period. |
| `price` | double(24,8) | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `price_ttc` | double(24,8) | Yes | `0` | Tax-inclusive price. |
| `price_min` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_min_ttc` | double(24,8) | Yes | `0` | Minimum sales price, before or including tax as indicated by the field name. |
| `price_base_type` | varchar(3) | Yes | `'HT'` | Identifies whether the price was entered before or including tax. |
| `default_vat_code` | varchar(10) | Yes | — | Tax treatment proposed as the default when using this entry. |
| `tva_tx` | double(7,4) | Yes | — | VAT percentage for this price or line. |
| `recuperableonly` | integer | No | `'0'` | Marks the VAT treatment recorded as recoverable-only in the source tax configuration. |
| `localtax1_tx` | varchar(20) | Yes | `'0'` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | varchar(20) | Yes | `'0'` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `discount_percent` | real | Yes | `0` | Discount expressed as a percentage. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `price_label` | varchar(255) | Yes | — | Label attached to a price or pricing condition. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_customer_price_log.sql`, `htdocs/product/class/productcustomerprice.class.php:684`.

<a id="record-product_fournisseur_price"></a>

## Supplier offer

Holds a supplier's reference, quantity break, purchase price, discount and procurement terms for a product.

**Storage** `product_fournisseur_price`.
The primary key is `rowid`.
Additional unique keys comprise `ref_fourn`, `fk_soc`, `quantity`, `entity` / `barcode`, `fk_barcode_type`, `entity`.

The record class defines `0` draft, `1` validated, `9` canceled. See `htdocs/product/class/productfournisseurprice.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `ref_fourn` | varchar(128) | Yes | — | Reference used by the supplier for the item. |
| `desc_fourn` | text | Yes | — | Descfourn. |
| `fk_availability` | integer | Yes | — | Delivery availability or lead-time term. |
| `price` | double(24,8) | Yes | `0` | Supplier price for the quoted purchasing quantity. |
| `quantity` | double | Yes | — | Minimum quantity for the supplier offer. |
| `remise_percent` | double | No | `0` | Percentage discount applied to the pricing base. |
| `remise` | double | No | `0` | Discount amount or pricing reduction in the owning record. |
| `unitprice` | double(24,8) | Yes | `0` | Unit price attached to the tariff break. |
| `charges` | double(24,8) | Yes | `0` | Charges. |
| `default_vat_code` | varchar(10) | Yes | — | Tax treatment proposed as the default when using this entry. |
| `barcode` | varchar(180) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `NULL` | Symbology used for the barcode. References [c_barcode_type](dictionaries.md#record-c_barcode_type) (rowid). |
| `tva_tx` | double(7,4) | No | — | VAT percentage for this price or line. |
| `localtax1_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax1_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `localtax2_tx` | double(7,4) | Yes | `0` | Percentage rate of the corresponding additional tax component. |
| `localtax2_type` | varchar(10) | No | `'0'` | Calculation category for the corresponding additional tax component. |
| `info_bits` | integer | No | `0` | Combined option bits. Interpret the flags in the owning document's line logic. |
| `fk_user` | integer | Yes | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `fk_supplier_price_expression` | integer | Yes | — | Fksupplierpriceexpression. |
| `delivery_time_days` | integer | Yes | — | Deliverytimedays. |
| `supplier_reputation` | varchar(10) | Yes | — | Supplierreputation. |
| `packaging` | real | Yes | `NULL` | Packaging quantity or unit arrangement. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_unitprice` | double(24,8) | Yes | `NULL` | Unit price in the secondary currency. |
| `multicurrency_price` | double(24,8) | Yes | `NULL` | Price expressed in the secondary currency. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_product_fournisseur_price.sql`, `htdocs/install/mysql/tables/llx_product_fournisseur_price.key.sql`, `htdocs/product/class/product.class.php:1901`.

<a id="record-product_fournisseur_price_log"></a>

## Supplier tariff event

Captures an earlier supplier price entry together with its purchase conditions and change time.

**Storage** `product_fournisseur_price_log`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | — | When the row was created. |
| `fk_product_fournisseur` | integer | No | — | Supplier price entry whose change is logged. |
| `price` | double(24,8) | Yes | `0` | Price retained at this point in the workflow. Its unit or tax basis follows the owning record. |
| `quantity` | double | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_multicurrency` | integer | Yes | — | Configured document currency record. |
| `multicurrency_code` | varchar(3) | Yes | — | Currency code used for the document-currency values. |
| `multicurrency_tx` | double(24,8) | Yes | `1` | Exchange rate retained for the transaction or price record. |
| `multicurrency_unitprice` | double(24,8) | Yes | `NULL` | Unit price in the secondary currency. |
| `multicurrency_price` | double(24,8) | Yes | `NULL` | Price expressed in the secondary currency. |

Source locations include `htdocs/install/mysql/tables/llx_product_fournisseur_price_log.sql`, `htdocs/product/class/product.class.php:1899`.

<a id="record-product_attribute"></a>

## Variant axis

Defines a configurable attribute such as colour or size used to differentiate sellable variants.

**Storage** `product_attribute`.
The primary key is `rowid`.
An additional unique key comprises `ref`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(255) | No | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_product_attribute-variants.sql`, `htdocs/install/mysql/tables/llx_product_attribute-variants.key.sql`, `htdocs/variants/class/ProductAttribute.class.php:57`.

<a id="record-product_attribute_value"></a>

## Variant option

Identifies one permissible value on a variant axis.

**Storage** `product_attribute_value`.
The primary key is `rowid`.
An additional unique key comprises `fk_product_attribute`, `ref`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product_attribute` | integer | No | — | Variant attribute. |
| `ref` | varchar(180) | No | — | Business reference used to identify the document or master record. |
| `value` | varchar(255) | No | — | Label or value of this available product option. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |

Source locations include `htdocs/install/mysql/tables/llx_product_attribute_value-variants.sql`, `htdocs/install/mysql/tables/llx_product_attribute_value-variants.key.sql`, `htdocs/variants/class/ProductAttribute.class.php:62`.

<a id="record-product_attribute_combination"></a>

## Parent and variant

Relates a parent product to its distinct child product and stores the combination's price, weight and reference variations.

**Storage** `product_attribute_combination`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product_parent` | integer | No | — | Master product from which the variant is derived. |
| `fk_product_child` | integer | No | — | Variant product represented by this combination. |
| `variation_price` | double(24,8) | No | — | Price adjustment for this variant relative to its base product. |
| `variation_price_percentage` | integer | Yes | — | Interprets the variant price adjustment as a percentage where selected. |
| `variation_weight` | real | No | — | Weight adjustment recorded for the variant. |
| `variation_ref_ext` | varchar(255) | Yes | — | External reference for this variant combination. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

Source locations include `htdocs/install/mysql/tables/llx_product_attribute_combination-variants.sql`, `htdocs/product/class/product.class.php:5751`.

<a id="record-product_attribute_combination2val"></a>

## Variant composition

Connects a product combination to an attribute and selected option. All selected options together describe the variant.

**Storage** `product_attribute_combination2val`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | int (generated) | No | — | Internal row identifier. |
| `fk_prod_combination` | int | No | — | Variant combination receiving the attribute value. |
| `fk_prod_attr` | int | No | — | Attribute being assigned to the combination. |
| `fk_prod_attr_val` | int | No | — | Selected value from the attribute's allowed values. |

Source locations include `htdocs/install/mysql/tables/llx_product_attribute_combination2val-variants.sql`, `htdocs/variants/class/ProductAttribute.class.php:854`.

<a id="record-product_attribute_combination_price_level"></a>

## Variant tariff adjustment

Stores combination-specific price adjustments for a particular sales price level.

**Storage** `product_attribute_combination_price_level`.
The primary key is `rowid`.
An additional unique key comprises `fk_product_attribute_combination`, `fk_price_level`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_product_attribute_combination` | integer | No | `1` | Associated parent and variant identifier. |
| `fk_price_level` | integer | No | `1` | Selling price level for this variant's adjustment. |
| `variation_price` | double(24,8) | No | — | Price adjustment for this variant relative to its base product. |
| `variation_price_percentage` | integer | Yes | — | Interprets the variant price adjustment as a percentage where selected. |

Source locations include `htdocs/install/mysql/tables/llx_product_attribute_combination_price_level-variants.sql`, `htdocs/install/mysql/tables/llx_product_attribute_combination_price_level-variants.key.sql`, `htdocs/variants/class/ProductCombination.class.php:459`.
