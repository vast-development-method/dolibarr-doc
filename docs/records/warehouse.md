# Warehouses, stock and counts

A movement is a dated change. A product/warehouse position is the resulting quantity. A batch position subdivides that quantity, and a lot description can be reused across warehouses. A count or transfer retains an identity separate from each movement it generates.

**Example.** A warehouse balance of 18 may consist of 7 units of lot A and 11 of lot B. Dispatching 4 from lot B gives 14 at that warehouse, comprising 7 and 7. The outbound movement and the shipment allocation explain the change. Each lot master identifies a lot independently of its balances.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Warehouse](#record-entrepot) | `entrepot` |
| [Warehouse balance](#record-product_stock) | `product_stock` |
| [Warehouse lot balance](#record-product_batch) | `product_batch` |
| [Product lot master](#record-product_lot) | `product_lot` |
| [Warehouse-specific item policy](#record-product_warehouse_properties) | `product_warehouse_properties` |
| [Stock movement](#record-stock_mouvement) | `stock_mouvement` |
| [Warehouse transfer](#record-stocktransfer_stocktransfer) | `stocktransfer_stocktransfer` |
| [Transfer item](#record-stocktransfer_stocktransferline) | `stocktransfer_stocktransferline` |
| [Stock count](#record-inventory) | `inventory` |
| [Counted position](#record-inventorydet) | `inventorydet` |

<a id="record-entrepot"></a>

## Warehouse

Identifies a stock location, address, hierarchy and operating status.

**Storage** `entrepot`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_warehouse](categories.md#record-categorie_warehouse) (fk_warehouse), [product_stock](warehouse.md#record-product_stock) (fk_entrepot), [product_warehouse_properties](warehouse.md#record-product_warehouse_properties) (fk_entrepot).

The record class defines `0` closed, `1` open all, `2` open internal. See `htdocs/product/stock/class/entrepot.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(255) | No | — | Business reference used to identify the document or master record. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_project` | integer | Yes | `NULL` | Associated project identity. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `lieu` | varchar(64) | Yes | — | Short name of location. |
| `address` | varchar(255) | Yes | — | Postal or street address. |
| `zip` | varchar(10) | Yes | — | Postal code. |
| `town` | varchar(50) | Yes | — | Town or city. |
| `fk_departement` | integer | Yes | — | Administrative subdivision identity in an address. |
| `fk_pays` | integer | Yes | `0` | Country associated with the record. |
| `phone` | varchar(30) | Yes | — | Telephone number. |
| `fax` | varchar(30) | Yes | — | Fax number. |
| `barcode` | varchar(180) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `NULL` | Symbology used for the barcode. |
| `warehouse_usage` | integer | Yes | `1` | Warehouse usage. |
| `statut` | tinyint | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_parent` | integer | Yes | `0` | Record one level above this one in the owning hierarchy. |

Source locations include `htdocs/install/mysql/tables/llx_entrepot.sql`, `htdocs/install/mysql/tables/llx_entrepot.key.sql`, `htdocs/product/stock/class/entrepot.class.php:46`.

<a id="record-product_stock"></a>

## Warehouse balance

Stores physical quantity for one product in one warehouse. Movements describe how the balance changed.

**Storage** `product_stock`.
The primary key is `rowid`.
An additional unique key comprises `fk_product`, `fk_entrepot`.

**Referenced by** [product_batch](warehouse.md#record-product_batch) (fk_product_stock).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `fk_entrepot` | integer | No | — | Warehouse or stock location. References [entrepot](warehouse.md#record-entrepot) (rowid). |
| `reel` | real | Yes | — | Physical on-hand quantity of this product in this warehouse. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_stock.sql`, `htdocs/install/mysql/tables/llx_product_stock.key.sql`, `htdocs/product/class/product.class.php:1730`.

<a id="record-product_batch"></a>

## Warehouse lot balance

Subdivides a product/warehouse stock balance by batch or serial identifier.

**Storage** `product_batch`.
The primary key is `rowid`.
An additional unique key comprises `fk_product_stock`, `batch`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product_stock` | integer | No | — | Product/warehouse balance to which this batch quantity belongs. References [product_stock](warehouse.md#record-product_stock) (rowid). |
| `eatby` | datetime | Yes | `NULL` | Use-by date associated with a lot. |
| `sellby` | datetime | Yes | `NULL` | Sell-by date associated with a lot. |
| `batch` | varchar(128) | No | — | Batch or serial identifier used on stock positions and movements. |
| `qty` | double | No | `0` | Quantity of this lot within the associated product/warehouse balance. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_batch.sql`, `htdocs/install/mysql/tables/llx_product_batch.key.sql`, `htdocs/product/class/product.class.php:1562`.

<a id="record-product_lot"></a>

## Product lot master

Describes a batch for a product, including its shelf-life dates and quality status where used. The lot master and its quantities in individual warehouses have distinct identities.

**Storage** `product_lot`.
The primary key is `rowid`.
An additional unique key comprises `fk_product`, `batch`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `note_public` | text | Yes | `NULL` | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | `NULL` | Internal note for users handling the record. |
| `eatby` | date | Yes | `NULL` | Use-by date associated with a lot. |
| `sellby` | date | Yes | `NULL` | Sell-by date associated with a lot. |
| `eol_date` | datetime | Yes | — | End of life. |
| `manufacturing_date` | datetime | Yes | — | Manufacturing date. |
| `scrapping_date` | datetime | Yes | — | Destruction date. |
| `qc_frequency` | integer | Yes | `NULL` | Quality inspection frequency. |
| `lifetime` | integer | Yes | `NULL` | Shelf-life setting for the item. |
| `barcode` | varchar(180) | Yes | `NULL` | Identifier intended for barcode scanning or printing. |
| `fk_barcode_type` | integer | Yes | `NULL` | Symbology used for the barcode. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | integer | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_lot.sql`, `htdocs/install/mysql/tables/llx_product_lot.key.sql`, `htdocs/product/class/product.class.php:6798`.

<a id="record-product_warehouse_properties"></a>

## Warehouse-specific item policy

Defines item replenishment values particular to a warehouse independently from the stock balance.

**Storage** `product_warehouse_properties`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `fk_entrepot` | integer | No | — | Warehouse or stock location. References [entrepot](warehouse.md#record-entrepot) (rowid). |
| `seuil_stock_alerte` | float | Yes | `'0'` | Stock quantity at which the low-stock alert applies. |
| `desiredstock` | float | Yes | `'0'` | Desired replenished stock level. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_product_warehouse_properties-stock.sql`, `htdocs/install/mysql/tables/llx_product_warehouse_properties-stock.key.sql`, `htdocs/product/stock/class/productstockentrepot.class.php:50`.

<a id="record-stock_mouvement"></a>

## Stock movement

Records an inventory quantity adjustment for a product, warehouse, date and origin. Its signed quantity explains the change to on-hand stock.

**Storage** `stock_mouvement`.
The primary key is `rowid`.

**Referenced by** [mrp_production](production.md#record-mrp_production) (fk_stock_movement).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datem` | datetime | Yes | — | When the stock change occurred. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `eatby` | date | Yes | `NULL` | Compatibility date. Read current use-by information from the lot for the product and batch. |
| `sellby` | date | Yes | `NULL` | Compatibility date. Read current sell-by information from the lot for the product and batch. |
| `fk_entrepot` | integer | No | — | Warehouse or stock location. |
| `value` | real | Yes | — | Signed movement quantity. An incoming movement adds units and an outgoing movement removes units. |
| `price` | double(24,8) | Yes | `0` | Unit valuation supplied with the stock movement for inventory costing. |
| `type_mouvement` | smallint | Yes | — | Stock change category, combining direction and manual or automatic origin. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `inventorycode` | varchar(128) | Yes | — | Shared operation code for movements belonging to the same count or adjustment run. |
| `fk_project` | integer | Yes | — | Associated project identity. |
| `fk_origin` | integer | Yes | — | Originating record identity. |
| `origintype` | varchar(64) | Yes | — | Type of originating record used to interpret the origin ID. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `fk_projet` | integer | No | `0` | Project-link field in the stored layout; confirm the origin-specific field used by the posting path. |

Source locations include `htdocs/install/mysql/tables/llx_stock_mouvement.sql`, `htdocs/product/class/productbatch.class.php:514`.

<a id="record-stocktransfer_stocktransfer"></a>

## Warehouse transfer

Groups the planned movement from one warehouse to another and records the transfer's state and responsible actors.

**Storage** `stocktransfer_stocktransfer`.
The primary key is `rowid`.

The record class defines `0` draft, `1` validated, `2` transfered, `3` closed. See `htdocs/product/stock/stocktransfer/class/stocktransfer.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_project` | integer | Yes | — | Associated project identity. |
| `fk_warehouse_source` | integer | Yes | — | Source warehouse. |
| `fk_warehouse_destination` | integer | Yes | — | Destination warehouse. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_creation` | datetime | No | — | When the row was created. |
| `date_prevue_depart` | date | Yes | `NULL` | Intended date of departure. |
| `date_reelle_depart` | date | Yes | `NULL` | Real date of departure. |
| `date_prevue_arrivee` | date | Yes | `NULL` | Intended date of arrival. |
| `date_reelle_arrivee` | date | Yes | `NULL` | Real date of arrival. |
| `lead_time_for_warning` | integer | Yes | `NULL` | Lead time before alert (in days). |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_incoterms` | integer | Yes | — | Trade delivery term selected for the document. |
| `location_incoterms` | varchar(255) | Yes | — | Named place associated with the selected delivery term. |

Source locations include `htdocs/install/mysql/tables/llx_stocktransfer_stocktransfer-stocktransfer.sql`, `htdocs/install/mysql/tables/llx_stocktransfer_stocktransfer-stocktransfer.key.sql`, `htdocs/product/stock/stocktransfer/class/stocktransfer.class.php:48`.

<a id="record-stocktransfer_stocktransferline"></a>

## Transfer item

Specifies an item, quantity and any batch to move under a transfer header.

**Storage** `stocktransfer_stocktransferline`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `amount` | double | Yes | `NULL` | Monetary amount. Its operational meaning follows the record purpose. |
| `qty` | real | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_warehouse_source` | integer | No | — | Entrepôt source. |
| `fk_warehouse_destination` | integer | No | — | Entrepôt de destination. |
| `fk_stocktransfer` | integer | No | — | Stock transfer. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `pmp` | double | Yes | — | Weighted average inventory value per unit. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |

Source locations include `htdocs/install/mysql/tables/llx_stocktransfer_stocktransferline-stocktransfer.sql`, `htdocs/product/stock/stocktransfer/class/stocktransfer.class.php:53`.

<a id="record-inventory"></a>

## Stock count

Identifies a counting exercise, its reference, warehouse or product scope and lifecycle.

**Storage** `inventory`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

The record class defines `0` draft, `1` validated, `2` recorded, `9` canceled. See `htdocs/product/inventory/class/inventory.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `0` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(48) | Yes | — | Business reference used to identify the document or master record. |
| `date_creation` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `fk_warehouse` | integer | Yes | `NULL` | Warehouse or stock location. |
| `fk_product` | integer | Yes | `NULL` | Catalogue item associated with this entry. |
| `categories_product` | varchar(255) | Yes | `NULL` | Or products with tags/categories. |
| `status` | integer | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `title` | varchar(255) | No | — | Display title. |
| `date_inventory` | datetime | Yes | `NULL` | Value date. |
| `date_validation` | datetime | Yes | `NULL` | Validation date. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_inventory-stock.sql`, `htdocs/install/mysql/tables/llx_inventory-stock.key.sql`, `htdocs/product/inventory/class/inventory.class.php:49`.

<a id="record-inventorydet"></a>

## Counted position

Compares the expected and counted quantity for a product, warehouse and optional batch. A movement reference can connect the resulting adjustment.

**Storage** `inventorydet`.
The primary key is `rowid`.
An additional unique key comprises `fk_inventory`, `fk_warehouse`, `fk_product`, `batch`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_inventory` | integer | Yes | `0` | Inventory. |
| `fk_warehouse` | integer | Yes | `0` | Warehouse or stock location. |
| `fk_product` | integer | Yes | `0` | Catalogue item associated with this entry. |
| `batch` | varchar(128) | Yes | `NULL` | Batch or serial identifier used on stock positions and movements. |
| `qty_stock` | double | Yes | `NULL` | Quantity expected in stock for the counted position. |
| `qty_view` | double | Yes | `NULL` | Quantity observed during the physical count. |
| `qty_regulated` | double | Yes | `NULL` | Superseded count adjustment quantity. Trace the actual adjustment using fk_movement. |
| `pmp_real` | double | Yes | `NULL` | Recorded actual or expected weighted valuation for the count position. |
| `pmp_expected` | double | Yes | `NULL` | Recorded actual or expected weighted valuation for the count position. |
| `fk_movement` | integer | Yes | — | Stock movement that records the physical adjustment. |

Source locations include `htdocs/install/mysql/tables/llx_inventorydet-stock.sql`, `htdocs/install/mysql/tables/llx_inventorydet-stock.key.sql`, `htdocs/product/inventory/class/inventory.class.php:176`.
