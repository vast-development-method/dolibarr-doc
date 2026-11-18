# Classification and custom properties

Category definitions and category membership are separate. Each association identifies the resource family. Extra-field definitions describe configurable properties whose values are held in the associated record extension.

**Example.** A category can classify many products, and a product can belong to several categories. Count distinct product identities when building a product total across categories. Category membership does not create a second stock balance.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Category](#record-categorie) | `categorie` |
| [Translated category](#record-categorie_lang) | `categorie_lang` |
| [Bank movement classification](#record-category_bankline) | `category_bankline` |
| [Custom property definition](#record-extrafields) | `extrafields` |
| [Bank account category assignment](#record-categorie_account) | `categorie_account` |
| [Calendar activity category assignment](#record-categorie_actioncomm) | `categorie_actioncomm` |
| [Contact category assignment](#record-categorie_contact) | `categorie_contact` |
| [Intervention category assignment](#record-categorie_fichinter) | `categorie_fichinter` |
| [Supplier category assignment](#record-categorie_fournisseur) | `categorie_fournisseur` |
| [Customer invoice category assignment](#record-categorie_invoice) | `categorie_invoice` |
| [Knowledge article category assignment](#record-categorie_knowledgemanagement) | `categorie_knowledgemanagement` |
| [Association member category assignment](#record-categorie_member) | `categorie_member` |
| [Manufacturing order category assignment](#record-categorie_mo) | `categorie_mo` |
| [Customer order category assignment](#record-categorie_order) | `categorie_order` |
| [Product category assignment](#record-categorie_product) | `categorie_product` |
| [Project category assignment](#record-categorie_project) | `categorie_project` |
| [Project task category assignment](#record-categorie_project_task) | `categorie_project_task` |
| [Customer proposal category assignment](#record-categorie_propal) | `categorie_propal` |
| [Third party category assignment](#record-categorie_societe) | `categorie_societe` |
| [Supplier bill category assignment](#record-categorie_supplier_invoice) | `categorie_supplier_invoice` |
| [Purchase order category assignment](#record-categorie_supplier_order) | `categorie_supplier_order` |
| [Supplier price request category assignment](#record-categorie_supplier_proposal) | `categorie_supplier_proposal` |
| [Support ticket category assignment](#record-categorie_ticket) | `categorie_ticket` |
| [User account category assignment](#record-categorie_user) | `categorie_user` |
| [Warehouse category assignment](#record-categorie_warehouse) | `categorie_warehouse` |
| [Website page category assignment](#record-categorie_website_page) | `categorie_website_page` |

<a id="record-categorie"></a>

## Category

Defines a business classification, its grouping type, parent and display properties.

**Storage** `categorie`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `fk_parent`, `label`, `type`.

**Referenced by** [categorie_account](categories.md#record-categorie_account) (fk_categorie), [categorie_actioncomm](categories.md#record-categorie_actioncomm) (fk_categorie), [categorie_contact](categories.md#record-categorie_contact) (fk_categorie), [categorie_fichinter](categories.md#record-categorie_fichinter) (fk_categorie), [categorie_fournisseur](categories.md#record-categorie_fournisseur) (fk_categorie), [categorie_invoice](categories.md#record-categorie_invoice) (fk_categorie), [categorie_knowledgemanagement](categories.md#record-categorie_knowledgemanagement) (fk_categorie), [categorie_lang](categories.md#record-categorie_lang) (fk_category), [categorie_member](categories.md#record-categorie_member) (fk_categorie), [categorie_mo](categories.md#record-categorie_mo) (fk_categorie), [categorie_order](categories.md#record-categorie_order) (fk_categorie), [categorie_product](categories.md#record-categorie_product) (fk_categorie), [categorie_project](categories.md#record-categorie_project) (fk_categorie), [categorie_project_task](categories.md#record-categorie_project_task) (fk_categorie), [categorie_propal](categories.md#record-categorie_propal) (fk_categorie), [categorie_societe](categories.md#record-categorie_societe) (fk_categorie), [categorie_supplier_invoice](categories.md#record-categorie_supplier_invoice) (fk_categorie), [categorie_supplier_order](categories.md#record-categorie_supplier_order) (fk_categorie), [categorie_supplier_proposal](categories.md#record-categorie_supplier_proposal) (fk_categorie), [categorie_ticket](categories.md#record-categorie_ticket) (fk_categorie), [categorie_user](categories.md#record-categorie_user) (fk_categorie), [categorie_warehouse](categories.md#record-categorie_warehouse) (fk_categorie), [categorie_website_page](categories.md#record-categorie_website_page) (fk_categorie).

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_parent` | integer | No | `0` | Record one level above this one in the owning hierarchy. |
| `label` | varchar(180) | No | — | Display label for the record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `type` | integer | No | `1` | Resource family classified by this category. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `color` | varchar(8) | Yes | — | Display colour assigned to this entry. |
| `fk_soc` | integer | Yes | `NULL` | Third party associated with this record. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `visible` | tinyint | No | `1` | Visible. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie.sql`, `htdocs/install/mysql/tables/llx_categorie.key.sql`, `htdocs/categories/class/categorie.class.php:256`.

<a id="record-categorie_lang"></a>

## Translated category

Supplies a category label and description in one language.

**Storage** `categorie_lang`.
The primary key is `rowid`.
An additional unique key comprises `fk_category`, `lang`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_category` | integer | No | `0` | References [categorie](categories.md#record-categorie) (rowid). |
| `lang` | varchar(5) | No | `0` | Language code under which this text or presentation is stored. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_lang.sql`, `htdocs/install/mysql/tables/llx_categorie_lang.key.sql`, `htdocs/categories/class/categorie.class.php:1395`.

<a id="record-category_bankline"></a>

## Bank movement classification

Associates a bank movement with a bank category.

**Storage** `category_bankline`.
The installation definitions declare no primary key for this record.
An additional unique key comprises `lineid`, `fk_categ`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `lineid` | integer | No | — | Bank movement assigned to this financial classification. |
| `fk_categ` | integer | No | — | Bank classification assigned to the indicated movement. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_category_bankline.sql`, `htdocs/install/mysql/tables/llx_category_bankline.key.sql`, `htdocs/categories/class/categorie.class.php:1788`.

<a id="record-extrafields"></a>

## Custom property definition

Describes a configured field for an object type, including its type, visibility, editability and formatting. Values can reside in an object-specific extension row.

**Storage** `extrafields`.
The primary key is `rowid`.
An additional unique key comprises `name`, `entity`, `elementtype`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `name` | varchar(64) | No | — | Name under which this record is presented or identified. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `elementtype` | varchar(64) | No | `'member'` | Type discriminator identifying the class of associated object. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `type` | varchar(8) | Yes | — | Configured data-entry type used to interpret the stored property value. |
| `size` | varchar(8) | Yes | `NULL` | Size or depth in the relevant physical unit. |
| `fieldcomputed` | text | Yes | — | Calculation expression for a computed custom property. |
| `fielddefault` | text | Yes | — | Default configured for the custom property. |
| `fieldunique` | integer | Yes | `0` | Whether values of this custom property should be unique. |
| `fieldrequired` | integer | Yes | `0` | Whether entry of a value is required for the custom property. |
| `perms` | varchar(255) | Yes | — | Permission condition for access to the configurable field. |
| `enabled` | varchar(255) | Yes | — | Condition or flag determining whether the entry is available. |
| `module` | varchar(64) | Yes | — | Feature or extension to which this entry belongs. |
| `pos` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `alwayseditable` | integer | Yes | `0` | Whether the extra field may be edited outside ordinary draft editing. |
| `emptyonclone` | integer | Yes | `0` | Whether to clear the field when copying the business object. |
| `param` | text | Yes | — | Parameters for the configured property, including possible selections where applicable. |
| `list` | varchar(255) | Yes | `'1'` | Visibility setting for forms and lists. A negative setting makes the field initially hidden in a list but available for selection. |
| `printable` | integer | Yes | `0` | Includes the property in supported document outputs. |
| `showintooltip` | integer | Yes | `0` | Includes the property in supported object tooltips. |
| `totalizable` | boolean | Yes | `FALSE` | Includes the property's values in supported list totals. |
| `langs` | varchar(64) | Yes | — | Translation resource used to display the configured labels. |
| `help` | text | Yes | — | Explanatory text displayed to the person entering the property. |
| `aiprompt` | text | Yes | — | Optional prompt retained for installations using assisted field completion. |
| `css` | varchar(128) | Yes | — | Presentation style for this property on create and edit forms. |
| `cssview` | varchar(128) | Yes | — | Presentation style for this property on detail views. |
| `csslist` | varchar(128) | Yes | — | Presentation style for this property in lists. |
| `personal_data` | tinyint | Yes | `0` | Classifies this property as containing personal information. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

Source locations include `htdocs/install/mysql/tables/llx_extrafields.sql`, `htdocs/install/mysql/tables/llx_extrafields.key.sql`, `htdocs/core/class/extrafields.class.php:509`.

<a id="record-categorie_account"></a>

## Bank account category assignment

Associates a category with a bank account. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_account`.
The primary key is `fk_categorie`, `fk_account`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_account` | integer | No | — | Financial account identifier as used by the owning record. References [bank_account](cash.md#record-bank_account) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_account.sql`, `htdocs/install/mysql/tables/llx_categorie_account.key.sql`, `htdocs/compta/bank/class/account.class.php:1250`.

<a id="record-categorie_actioncomm"></a>

## Calendar activity category assignment

Associates a category with a calendar activity. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_actioncomm`.
The primary key is `fk_categorie`, `fk_actioncomm`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_actioncomm` | integer | No | — | Associated calendar activity or event. References [actioncomm](production.md#record-actioncomm) (id). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_actioncomm.sql`, `htdocs/install/mysql/tables/llx_categorie_actioncomm.key.sql`, `htdocs/comm/action/class/actioncomm.class.php:1127`.

<a id="record-categorie_contact"></a>

## Contact category assignment

Associates a category with a contact. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_contact`.
The primary key is `fk_categorie`, `fk_socpeople`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_socpeople` | integer | No | — | Contact identity. Some generic role assignments resolve differently for internal and external contacts. References [socpeople](parties.md#record-socpeople) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_contact.sql`, `htdocs/install/mysql/tables/llx_categorie_contact.key.sql`, `htdocs/contact/class/contact.class.php:1390`.

<a id="record-categorie_fichinter"></a>

## Intervention category assignment

Associates a category with a intervention. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_fichinter`.
The primary key is `fk_categorie`, `fk_fichinter`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_fichinter` | integer | No | — | Intervention report identity. References [fichinter](people.md#record-fichinter) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_fichinter-fichinter.sql`, `htdocs/install/mysql/tables/llx_categorie_fichinter-fichinter.key.sql`, `htdocs/fichinter/list.php:376`.

<a id="record-categorie_fournisseur"></a>

## Supplier category assignment

Associates a category with a supplier. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_fournisseur`.
The primary key is `fk_categorie`, `fk_soc`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_fournisseur.sql`, `htdocs/install/mysql/tables/llx_categorie_fournisseur.key.sql`, `htdocs/societe/class/societe.class.php:4684`.

<a id="record-categorie_invoice"></a>

## Customer invoice category assignment

Associates a category with a customer invoice. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_invoice`.
The primary key is `fk_categorie`, `fk_invoice`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_invoice` | integer | No | — | Customer invoice identifier. References [facture](billing.md#record-facture) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_invoice-facture.sql`, `htdocs/install/mysql/tables/llx_categorie_invoice-facture.key.sql`, `htdocs/compta/facture/class/facture.class.php:3210`.

<a id="record-categorie_knowledgemanagement"></a>

## Knowledge article category assignment

Associates a category with a knowledge article. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_knowledgemanagement`.
The primary key is `fk_categorie`, `fk_knowledgemanagement`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_knowledgemanagement` | integer | No | — | References [knowledgemanagement_knowledgerecord](people.md#record-knowledgemanagement_knowledgerecord) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_knowledgemanagement-knowledgemanagement.sql`, `htdocs/install/mysql/tables/llx_categorie_knowledgemanagement-knowledgemanagement.key.sql`, `htdocs/knowledgemanagement/class/knowledgerecord.class.php:508`.

<a id="record-categorie_member"></a>

## Association member category assignment

Associates a category with a association member. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_member`.
The primary key is `fk_categorie`, `fk_member`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_member` | integer | No | — | Association member identity. References [adherent](people.md#record-adherent) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_member.sql`, `htdocs/install/mysql/tables/llx_categorie_member.key.sql`, `htdocs/adherents/class/adherent.class.php:1163`.

<a id="record-categorie_mo"></a>

## Manufacturing order category assignment

Associates a category with a manufacturing order. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_mo`.
The primary key is `fk_categorie`, `fk_mo`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_mo` | integer | No | — | Manufacturing order identity. References [mrp_mo](production.md#record-mrp_mo) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_mo-mrp.sql`, `htdocs/install/mysql/tables/llx_categorie_mo-mrp.key.sql`, `htdocs/mrp/class/mo.class.php:977`.

<a id="record-categorie_order"></a>

## Customer order category assignment

Associates a category with a customer order. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_order`.
The primary key is `fk_categorie`, `fk_order`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_order` | integer | No | — | References [commande](commercial.md#record-commande) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_order-commande.sql`, `htdocs/install/mysql/tables/llx_categorie_order-commande.key.sql`, `htdocs/commande/class/commande.class.php:3570`.

<a id="record-categorie_product"></a>

## Product category assignment

Associates a category with a product. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_product`.
The primary key is `fk_categorie`, `fk_product`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_product.sql`, `htdocs/install/mysql/tables/llx_categorie_product.key.sql`, `htdocs/core/class/html.form.class.php:3670`.

<a id="record-categorie_project"></a>

## Project category assignment

Associates a category with a project. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_project`.
The primary key is `fk_categorie`, `fk_project`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_project` | integer | No | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_project.sql`, `htdocs/install/mysql/tables/llx_categorie_project.key.sql`, `htdocs/projet/class/project.class.php:1040`.

<a id="record-categorie_project_task"></a>

## Project task category assignment

Associates a category with a project task. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_project_task`.
The primary key is `fk_categorie`, `fk_project_task`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_project_task` | integer | No | — | References [projet_task](production.md#record-projet_task) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_project_task-project.sql`, `htdocs/install/mysql/tables/llx_categorie_project_task-project.key.sql`, `htdocs/categories/class/categorie.class.php:822`.

<a id="record-categorie_propal"></a>

## Customer proposal category assignment

Associates a category with a customer proposal. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_propal`.
The primary key is `fk_categorie`, `fk_propal`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_propal` | integer | No | — | Customer proposal identity. References [propal](commercial.md#record-propal) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_propal-propal.sql`, `htdocs/install/mysql/tables/llx_categorie_propal-propal.key.sql`, `htdocs/comm/propal/class/propal.class.php:3204`.

<a id="record-categorie_societe"></a>

## Third party category assignment

Associates a category with a third party. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_societe`.
The primary key is `fk_categorie`, `fk_soc`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_soc` | integer | No | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_societe.sql`, `htdocs/install/mysql/tables/llx_categorie_societe.key.sql`, `htdocs/contrat/class/contratstats.class.php:119`.

<a id="record-categorie_supplier_invoice"></a>

## Supplier bill category assignment

Associates a category with a supplier bill. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_supplier_invoice`.
The primary key is `fk_categorie`, `fk_supplier_invoice`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_supplier_invoice` | integer | No | — | References [facture_fourn](billing.md#record-facture_fourn) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_supplier_invoice.sql`, `htdocs/install/mysql/tables/llx_categorie_supplier_invoice.key.sql`, `htdocs/fourn/class/fournisseur.facture.class.php:1522`.

<a id="record-categorie_supplier_order"></a>

## Purchase order category assignment

Associates a category with a purchase order. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_supplier_order`.
The primary key is `fk_categorie`, `fk_supplier_order`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_supplier_order` | integer | No | — | References [commande_fournisseur](commercial.md#record-commande_fournisseur) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_supplier_order.sql`, `htdocs/install/mysql/tables/llx_categorie_supplier_order.key.sql`, `htdocs/fourn/class/fournisseur.commande.class.php:2533`.

<a id="record-categorie_supplier_proposal"></a>

## Supplier price request category assignment

Associates a category with a supplier price request. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_supplier_proposal`.
The primary key is `fk_categorie`, `fk_supplier_proposal`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_supplier_proposal` | integer | No | — | Supplier price request identity. References [supplier_proposal](commercial.md#record-supplier_proposal) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_supplier_proposal-supplier_proposal.sql`, `htdocs/install/mysql/tables/llx_categorie_supplier_proposal-supplier_proposal.key.sql`, `htdocs/supplier_proposal/class/supplier_proposal.class.php:2144`.

<a id="record-categorie_ticket"></a>

## Support ticket category assignment

Associates a category with a support ticket. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_ticket`.
The primary key is `fk_categorie`, `fk_ticket`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_ticket` | integer | No | — | Support ticket identity. References [ticket](people.md#record-ticket) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_ticket-ticket.sql`, `htdocs/install/mysql/tables/llx_categorie_ticket-ticket.key.sql`, `htdocs/ticket/class/ticket.class.php:1213`.

<a id="record-categorie_user"></a>

## User account category assignment

Associates a category with a user account. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_user`.
The primary key is `fk_categorie`, `fk_user`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_user` | integer | No | — | User account associated with this record. References [user](foundation.md#record-user) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_user.sql`, `htdocs/install/mysql/tables/llx_categorie_user.key.sql`, `htdocs/core/modules/modCategorie.class.php:474`.

<a id="record-categorie_warehouse"></a>

## Warehouse category assignment

Associates a category with a warehouse. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_warehouse`.
The primary key is `fk_categorie`, `fk_warehouse`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_warehouse` | integer | No | — | Warehouse or stock location. References [entrepot](warehouse.md#record-entrepot) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_warehouse-stock.sql`, `htdocs/install/mysql/tables/llx_categorie_warehouse-stock.key.sql`, `htdocs/product/stock/class/api_warehouses.class.php:131`.

<a id="record-categorie_website_page"></a>

## Website page category assignment

Associates a category with a website page. Query the association to find classified records without changing their own commercial or lifecycle state.

**Storage** `categorie_website_page`.
The primary key is `fk_categorie`, `fk_website_page`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `fk_categorie` | integer | No | — | Category assigned through this association. References [categorie](categories.md#record-categorie) (rowid). |
| `fk_website_page` | integer | No | — | References [website_page](content.md#record-website_page) (rowid). |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |

Source locations include `htdocs/install/mysql/tables/llx_categorie_website_page-website.sql`, `htdocs/install/mysql/tables/llx_categorie_website_page-website.key.sql`, `htdocs/core/lib/website.lib.php:1274`.
