# Manufacturing, projects and resource time

A bill is a reusable definition. A manufacturing order has its own planned and actual positions. Project time and workstation resources preserve different dimensions of cost, capacity and commercial billing.

**Example.** A production order can have planned consumption for 12 components and two actual consumptions of 5 and 7. Use the actual positions and their stock movement references to explain inventory. Summing planned and actual rows would incorrectly report consumption of 24.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Bill of materials](#record-bom_bom) | `bom_bom` |
| [Bill component](#record-bom_bomline) | `bom_bomline` |
| [Manufacturing order](#record-mrp_mo) | `mrp_mo` |
| [Planned or actual production position](#record-mrp_production) | `mrp_production` |
| [Workstation](#record-workstation_workstation) | `workstation_workstation` |
| [Workstation resource assignment](#record-workstation_workstation_resource) | `workstation_workstation_resource` |
| [Workstation group assignment](#record-workstation_workstation_usergroup) | `workstation_workstation_usergroup` |
| [Project or opportunity](#record-projet) | `projet` |
| [Project task](#record-projet_task) | `projet_task` |
| [Time entry](#record-element_time) | `element_time` |
| [Reservable resource](#record-resource) | `resource` |
| [Calendar activity](#record-actioncomm) | `actioncomm` |
| [Activity participant](#record-actioncomm_resources) | `actioncomm_resources` |
| [Activity reminder](#record-actioncomm_reminder) | `actioncomm_reminder` |
| [Event registration](#record-eventorganization_conferenceorboothattendee) | `eventorganization_conferenceorboothattendee` |

<a id="record-bom_bom"></a>

## Bill of materials

Defines the output product, reference quantity and manufacturing or disassembly configuration.

**Storage** `bom_bom`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [bom_bomline](production.md#record-bom_bomline) (fk_bom).

The record class defines `0` draft, `1` validated, `9` canceled. See `htdocs/bom/class/bom.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `bomtype` | integer | Yes | `0` | Type. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `fk_warehouse` | integer | Yes | — | Warehouse or stock location. |
| `qty` | double(24,8) | Yes | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `efficiency` | double(24,8) | Yes | `1` | Yield factor for the manufactured item. The object normalises values outside the interval greater than zero and at most one back to one. |
| `duration` | double(24,8) | Yes | `NULL` | Duration of the activity or period in the unit used by the owning feature. |
| `date_creation` | datetime | No | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

Source locations include `htdocs/install/mysql/tables/llx_bom_bom-bom.sql`, `htdocs/install/mysql/tables/llx_bom_bom-bom.key.sql`, `htdocs/bom/class/bom.class.php:62`.

<a id="record-bom_bomline"></a>

## Bill component

Specifies the component and planned quantity for a bill of materials, together with efficiency, units and workstation where applicable.

**Storage** `bom_bomline`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_bom` | integer | No | — | Bill of materials identity. References [bom_bom](production.md#record-bom_bom) (rowid). |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `fk_bom_child` | integer | Yes | — | Bill of Materials. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `qty` | double(24,8) | No | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `qty_frozen` | smallint | Yes | `0` | Indicates that the planned quantity is fixed when scaling manufacturing quantities. |
| `disable_stock_change` | smallint | Yes | `0` | Suppresses stock movement for the production position where supported. |
| `efficiency` | double(24,8) | No | `1` | Manufacturing efficiency. |
| `fk_unit` | integer | Yes | — | Unit of measure associated with the quantity. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_default_workstation` | integer | Yes | `NULL` | Workstation proposed for the production operation. |

Source locations include `htdocs/install/mysql/tables/llx_bom_bomline-bom.sql`, `htdocs/install/mysql/tables/llx_bom_bomline-bom.key.sql`, `htdocs/bom/class/bom.class.php:223`.

<a id="record-mrp_mo"></a>

## Manufacturing order

Identifies the product to make, planned quantity, bill of materials, timing and state.

**Storage** `mrp_mo`.
The primary key is `rowid`.

**Referenced by** [categorie_mo](categories.md#record-categorie_mo) (fk_mo), [mrp_production](production.md#record-mrp_production) (fk_mo).

The record class defines `0` draft, `1` validated, `2` inprogress, `3` produced, `9` canceled. See `htdocs/mrp/class/mo.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `mrptype` | integer | Yes | `0` | Type. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `qty` | real | No | — | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `fk_warehouse` | integer | Yes | — | Warehouse or stock location. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. |
| `date_start_planned` | datetime | Yes | — | Date start planned. |
| `date_end_planned` | datetime | Yes | — | Date end planned. |
| `fk_bom` | integer | Yes | — | Bill of materials identity. |
| `fk_project` | integer | Yes | — | Associated project identity. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `fk_parent_line` | integer | Yes | — | Parent line for hierarchical document content. |
| `extraparams` | varchar(255) | Yes | `NULL` | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_mrp_mo-mrp.sql`, `htdocs/install/mysql/tables/llx_mrp_mo-mrp.key.sql`, `htdocs/mrp/class/mo.class.php:44`.

<a id="record-mrp_production"></a>

## Planned or actual production position

Uses a role to distinguish a material requirement, intended output, actual consumption or actual production. Actual positions can point to their plan row and stock movement.

**Storage** `mrp_production`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_mo` | integer | No | — | Manufacturing order identity. References [mrp_mo](production.md#record-mrp_mo) (rowid). |
| `origin_id` | integer | Yes | — | Originating record identity. |
| `origin_type` | varchar(10) | Yes | — | Type of originating record used to interpret the origin ID. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `fk_product` | integer | No | — | Catalogue item associated with this entry. References [product](catalogue.md#record-product) (rowid). |
| `fk_warehouse` | integer | Yes | — | Warehouse or stock location. |
| `qty` | real | No | `1` | Number of units in this position. Interpret with the record's unit and quantity direction. |
| `qty_frozen` | smallint | Yes | `0` | Indicates that the planned quantity is fixed when scaling manufacturing quantities. |
| `disable_stock_change` | smallint | Yes | `0` | Suppresses stock movement for the production position where supported. |
| `batch` | varchar(128) | Yes | — | Batch or serial identifier used on stock positions and movements. |
| `role` | varchar(10) | Yes | — | Planned input, planned output, actual consumption or actual output. The role determines how quantity is interpreted. |
| `fk_mrp_production` | integer | Yes | — | Related planned production position for this material consumption or output. |
| `fk_stock_movement` | integer | Yes | — | Stock movement that records the physical adjustment. References [stock_mouvement](warehouse.md#record-stock_mouvement) (rowid). |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `fk_default_workstation` | integer | Yes | `NULL` | Workstation proposed for the production operation. |
| `fk_unit` | integer | Yes | `NULL` | Unit of measure associated with the quantity. |

Source locations include `htdocs/install/mysql/tables/llx_mrp_production-mrp.sql`, `htdocs/install/mysql/tables/llx_mrp_production-mrp.key.sql`, `htdocs/mrp/class/mo.class.php:234`.

<a id="record-workstation_workstation"></a>

## Workstation

Defines an operation centre and its machine and labour rates or capacity attributes.

**Storage** `workstation_workstation`.
The primary key is `rowid`.

The record class defines `0` disabled, `1` enabled. See `htdocs/workstation/class/workstation.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | No | `'(PROV)'` | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `type` | varchar(7) | Yes | — | Type. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `entity` | int | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `nb_operators_required` | integer | Yes | — | Number of operators required. |
| `thm_operator_estimated` | double | Yes | — | Estimated operator THM. |
| `thm_machine_estimated` | double | Yes | — | Estimated machine THM. |

Source locations include `htdocs/install/mysql/tables/llx_workstation_workstation-workstation.sql`, `htdocs/install/mysql/tables/llx_workstation_workstation-workstation.key.sql`, `htdocs/workstation/class/workstation.class.php:48`.

<a id="record-workstation_workstation_resource"></a>

## Workstation resource assignment

Associates an equipment or resource record with a workstation.

**Storage** `workstation_workstation_resource`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_resource` | integer | Yes | — | User group. |
| `fk_workstation` | integer | Yes | — | Workstation. |

Source locations include `htdocs/install/mysql/tables/llx_workstation_workstation_resource-workstation.sql`, `htdocs/workstation/class/workstationresource.class.php:34`.

<a id="record-workstation_workstation_usergroup"></a>

## Workstation group assignment

Associates a user group with a workstation.

**Storage** `workstation_workstation_usergroup`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_usergroup` | integer | Yes | — | Access or personnel group. |
| `fk_workstation` | integer | Yes | — | Workstation. |

Source locations include `htdocs/install/mysql/tables/llx_workstation_workstation_usergroup-workstation.sql`, `htdocs/workstation/class/workstationusergroup.class.php:33`.

<a id="record-projet"></a>

## Project or opportunity

Brings documents, a party, a project lead, dates, budget and opportunity information into a shared context.

**Storage** `projet`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_project](categories.md#record-categorie_project) (fk_project), [commande](commercial.md#record-commande) (fk_projet), [facture](billing.md#record-facture) (fk_projet), [facture_fourn](billing.md#record-facture_fourn) (fk_projet), [facture_fourn_rec](billing.md#record-facture_fourn_rec) (fk_projet), [facture_rec](billing.md#record-facture_rec) (fk_projet), [fichinter_rec](people.md#record-fichinter_rec) (fk_projet), [projet_task](production.md#record-projet_task) (fk_projet), [propal](commercial.md#record-propal) (fk_projet).

The record class defines `0` draft, `1` validated, `2` closed. See `htdocs/projet/class/project.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_project` | integer | Yes | `NULL` | Associated project identity. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. References [societe](parties.md#record-societe) (rowid). |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `dateo` | date | Yes | — | Operation date for a financial transaction. |
| `datee` | date | Yes | — | End date of the project. |
| `ref` | varchar(50) | Yes | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(50) | Yes | — | Identifier supplied by an external application or interface. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `title` | varchar(255) | No | — | Display title. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `public` | integer | Yes | — | Publication or visibility selection for the record. |
| `fk_statut` | integer | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_opp_status` | integer | Yes | `NULL` | Lead status. |
| `opp_percent` | double(5,2) | Yes | — | Lead probab.. |
| `fk_opp_status_end` | integer | Yes | `NULL` | Opportunity outcome recorded when a project used as a lead is marked lost. |
| `date_close` | datetime | Yes | `NULL` | When the record was closed. |
| `fk_user_close` | integer | Yes | `NULL` | Closing user. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `email_msgid` | varchar(175) | Yes | — | Mail message identifier supplied in the message headers. |
| `email_date` | datetime | Yes | — | Date associated with the stored email. |
| `opp_amount` | double(24,8) | Yes | — | Lead amount. |
| `budget_amount` | double(24,8) | Yes | — | Monetary budget assigned to the project. |
| `usage_opportunity` | integer | Yes | `0` | Usage: Opportunity. |
| `usage_task` | integer | Yes | `1` | Usage: Tasks. |
| `usage_bill_time` | integer | Yes | `0` | Usage: Bill time. |
| `usage_organize_event` | integer | Yes | `0` | Usage: Event Organization. |
| `date_start_event` | datetime | Yes | — | Event start date. |
| `date_end_event` | datetime | Yes | — | Event end date. |
| `location` | varchar(255) | Yes | — | Place associated with the activity or object. |
| `accept_conference_suggestions` | integer | Yes | `0` | Allow people to suggest conferences. |
| `accept_booth_suggestions` | integer | Yes | `0` | Allow people to apply for a booth. |
| `max_attendees` | integer | Yes | `0` | Max number of attendees. |
| `price_registration` | double(24,8) | Yes | — | Price of registration. |
| `price_booth` | double(24,8) | Yes | — | Subscription price to stand a booth. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_projet.sql`, `htdocs/install/mysql/tables/llx_projet.key.sql`, `htdocs/projet/class/task.class.php:1188`.

<a id="record-projet_task"></a>

## Project task

Defines a unit of project work, its parent task, scheduling window, workload and reported progress.

**Storage** `projet_task`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [categorie_project_task](categories.md#record-categorie_project_task) (fk_project_task).

The record class defines `0` draft, `1` validated, `2` ongoing, `3` closed, `4` transferred, `9` canceled. See `htdocs/projet/class/task.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(50) | Yes | — | Business reference used to identify the document or master record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_projet` | integer | No | — | Associated project identity. References [projet](production.md#record-projet) (rowid). |
| `fk_task_parent` | integer | No | `0` | Task immediately above this task in the project hierarchy. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `dateo` | datetime | Yes | — | Operation date for a financial transaction. |
| `datee` | datetime | Yes | — | Scheduled finish date of the task. |
| `datev` | datetime | Yes | — | Value/effective date in financial records. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `duration_effective` | real | Yes | `0` | Cached total of time booked against the task. Individual bookings are retained separately. |
| `planned_workload` | real | Yes | `0` | Estimated effort in seconds for the task. |
| `progress` | integer | Yes | `0` | Recorded completion percentage. |
| `priority` | integer | Yes | `0` | Processing or display priority. |
| `budget_amount` | double(24,8) | Yes | — | Monetary budget assigned to the project. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. References [user](foundation.md#record-user) (rowid). |
| `fk_statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `rang` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `billable` | smallint | Yes | `1` | Whether time on the task can be billed. |

Source locations include `htdocs/install/mysql/tables/llx_projet_task.sql`, `htdocs/install/mysql/tables/llx_projet_task.key.sql`, `htdocs/projet/class/task.class.php:51`.

<a id="record-element_time"></a>

## Time entry

Records time against a typed activity and a worker. Cost rate, linked invoice line and intervention reference allow time to be costed or billed.

**Storage** `element_time`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref_ext` | varchar(32) | Yes | — | Identifier supplied by an external application or interface. |
| `fk_element` | integer | No | — | Target record identity. Where an object type accompanies it, both values identify the target. |
| `elementtype` | varchar(32) | No | — | Type discriminator identifying the class of associated object. |
| `element_date` | date | Yes | — | element_date. |
| `element_datehour` | datetime | Yes | — | Time-entry start including hour when the entry records a time of day. |
| `element_date_withhour` | integer | Yes | — | Indicates whether the booking specifies a time of day. |
| `element_duration` | double | Yes | — | Time charged to the activity, stored in seconds. |
| `fk_product` | integer | Yes | — | Catalogue item associated with this entry. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `thm` | double(24,8) | Yes | — | Hourly cost rate captured on a time entry. |
| `invoice_id` | integer | Yes | `NULL` | invoice_id. |
| `invoice_line_id` | integer | Yes | `NULL` | Invoice line associated with billing this time entry. |
| `intervention_id` | integer | Yes | `NULL` | intervention_id. |
| `intervention_line_id` | integer | Yes | `NULL` | intervention_line_id. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `note` | text | Yes | — | Free-text annotation retained with the record. |

Source locations include `htdocs/install/mysql/tables/llx_element_time.sql`, `htdocs/projet/class/task.class.php:837`.

<a id="record-resource"></a>

## Reservable resource

Identifies named equipment or another resource available for assignment to an event or activity.

**Storage** `resource`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(255) | Yes | — | Business reference used to identify the document or master record. |
| `asset_number` | varchar(255) | Yes | — | Asset reference used to identify this resource. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `fk_code_type_resource` | varchar(32) | Yes | — | Controlled classification for the resource. |
| `address` | varchar(255) | Yes | `NULL` | Postal or street address. |
| `zip` | varchar(25) | Yes | `NULL` | Postal code. |
| `town` | varchar(50) | Yes | `NULL` | Town or city. |
| `photo_filename` | varchar(255) | Yes | `NULL` | Name of the associated resource image. |
| `max_users` | integer | Yes | `NULL` | Maximum number of simultaneous users specified for the resource. |
| `phone` | varchar(30) | Yes | `NULL` | Telephone number. |
| `email` | varchar(255) | Yes | `NULL` | Email address associated with this record. |
| `url` | varchar(255) | Yes | `NULL` | Web address or navigation target. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `date_valid` | datetime | Yes | `NULL` | When validation was recorded. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | `NULL` | Account that validated the record. |
| `fk_statut` | smallint | No | `'0'` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `fk_country` | integer | Yes | `NULL` | Country associated with the record. References [c_country](dictionaries.md#record-c_country) (rowid). |
| `fk_state` | integer | Yes | `NULL` | Administrative subdivision identity in an address. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

Source locations include `htdocs/install/mysql/tables/llx_resource.sql`, `htdocs/install/mysql/tables/llx_resource.key.sql`, `htdocs/resource/class/dolresource.class.php:46`.

<a id="record-actioncomm"></a>

## Calendar activity

Represents a scheduled or completed activity with a date range, owner, type and links to business records.

**Storage** `actioncomm`.
The primary key is `id`.

**Referenced by** [categorie_actioncomm](categories.md#record-categorie_actioncomm) (fk_actioncomm).

The record class defines `0` draft, `1` suggested, `2` confirmed, `3` not qualified, `4` done, `9` canceled. See `htdocs/eventorganization/class/conferenceorbooth.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id` | integer (generated) | No | — | Internal identifier in this table. |
| `ref` | varchar(30) | No | — | Business reference used to identify the document or master record. |
| `ref_ext` | varchar(255) | Yes | — | Identifier supplied by an external application or interface. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datep` | datetime | Yes | — | Payment or posting date for this financial record. |
| `datep2` | datetime | Yes | — | End date. |
| `fk_action` | integer | Yes | — | Action or event type selected for the record. |
| `code` | varchar(50) | Yes | — | Machine-readable code identifying a dictionary entry or feature value. |
| `datec` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_author` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_mod` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_project` | integer | Yes | — | Associated project identity. |
| `fk_task` | integer | Yes | — | Task. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_contact` | integer | Yes | — | Contact or address identity. |
| `fk_parent` | integer | No | `0` | Record one level above this one in the owning hierarchy. |
| `fk_user_action` | integer | Yes | — | Account responsible for the recorded action. |
| `transparency` | integer | Yes | — | Availability indicator for the activity. Individual participant assignments can have their own value. |
| `priority` | smallint | Yes | — | Processing or display priority. |
| `visibility` | varchar(12) | Yes | `'default'` | Visibility setting specific to the record type. |
| `fulldayevent` | smallint | No | `0` | Fulldayevent. |
| `percent` | smallint | No | `0` | Percentage recorded for the activity or calculation. |
| `location` | varchar(128) | Yes | — | Place associated with the activity or object. |
| `durationp` | real | Yes | — | Durationp. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `note` | mediumtext | Yes | — | Free-text annotation retained with the record. |
| `calling_duration` | integer | Yes | — | Callingduration. |
| `email_subject` | varchar(255) | Yes | — | Emailsubject. |
| `email_msgid` | varchar(255) | Yes | — | Mail message identifier supplied in the message headers. |
| `email_from` | varchar(255) | Yes | — | Sender email address. |
| `email_sender` | varchar(255) | Yes | — | Emailsender. |
| `email_to` | varchar(255) | Yes | — | Primary email recipients. |
| `email_tocc` | varchar(255) | Yes | — | Copy recipients. |
| `email_tobcc` | varchar(255) | Yes | — | Blind-copy recipients. |
| `errors_to` | varchar(255) | Yes | — | Errorsto. |
| `reply_to` | varchar(255) | Yes | — | Replyto. |
| `recurid` | varchar(128) | Yes | — | Recurid. |
| `recurrule` | varchar(128) | Yes | — | Recurrule. |
| `recurdateend` | datetime | Yes | — | Recurdateend. |
| `num_vote` | integer | Yes | `NULL` | Number of votes. |
| `event_paid` | smallint | No | `0` | Eventpaid. |
| `status` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `max_participants` | integer | Yes | `NULL` | Maximum participant count for this calendar activity. |
| `fk_element` | integer | Yes | `NULL` | Target record identity. Where an object type accompanies it, both values identify the target. |
| `elementtype` | varchar(255) | Yes | `NULL` | Type discriminator identifying the class of associated object. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `fk_bookcal_calendar` | integer | Yes | `NULL` | Fkbookcalcalendar. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |

Source locations include `htdocs/install/mysql/tables/llx_actioncomm.sql`, `htdocs/comm/action/class/actioncomm.class.php:57`.

<a id="record-actioncomm_resources"></a>

## Activity participant

Associates a user, contact or resource with an activity, with response, required-attendance and availability settings.

**Storage** `actioncomm_resources`.
The primary key is `rowid`.
An additional unique key comprises `fk_actioncomm`, `element_type`, `fk_element`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_actioncomm` | integer | No | — | Associated calendar activity or event. |
| `element_type` | varchar(50) | No | — | Type discriminator identifying the class of associated object. |
| `fk_element` | integer | No | — | Target record identity. Where an object type accompanies it, both values identify the target. |
| `answer_status` | varchar(50) | Yes | — | Participant response recorded for the invitation. |
| `mandatory` | smallint | Yes | — | Whether participation or association is required. |
| `transparency` | smallint | Yes | `1` | Calendar availability indicator, used to distinguish busy from available participation. |

Source locations include `htdocs/install/mysql/tables/llx_actioncomm_resources.sql`, `htdocs/install/mysql/tables/llx_actioncomm_resources.key.sql`, `htdocs/comm/action/class/actioncomm.class.php:720`.

<a id="record-actioncomm_reminder"></a>

## Activity reminder

Schedules a notification for an activity and recipient at an interval before the event.

**Storage** `actioncomm_reminder`.
The primary key is `rowid`.
An additional unique key comprises `fk_actioncomm`, `fk_user`, `fk_soc`, `fk_contact`, `typeremind`, `offsetvalue`, `offsetunit`.

The record class defines `0` todo, `1` done, `-1` error. See `htdocs/comm/action/class/actioncommreminder.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `dateremind` | datetime | No | — | Date Remind. |
| `typeremind` | varchar(32) | No | — | Type Remind. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_contact` | integer | Yes | — | Contact or address identity. |
| `offsetvalue` | integer | No | — | Offset Value. |
| `offsetunit` | varchar(1) | No | — | Offset Unit. |
| `status` | integer | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `datedone` | datetime | Yes | — | Time the reminder was processed. |
| `lasterror` | varchar(128) | Yes | — | Last Error. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_actioncomm` | integer | No | — | Associated calendar activity or event. |
| `fk_email_template` | integer | Yes | — | Selected message template. |

Source locations include `htdocs/install/mysql/tables/llx_actioncomm_reminder.sql`, `htdocs/install/mysql/tables/llx_actioncomm_reminder.key.sql`, `htdocs/comm/action/class/actioncomm.class.php:1150`.

<a id="record-eventorganization_conferenceorboothattendee"></a>

## Event registration

Associates an attendee with an event session or stand and records its registration state and linked commercial record where applicable.

**Storage** `eventorganization_conferenceorboothattendee`.
The primary key is `rowid`.
Additional unique keys comprise `ref` / `fk_project`, `email`, `fk_actioncomm` / `fk_replacement`.

The record class defines `0` draft, `1` validated, `5` used, `9` canceled. See `htdocs/eventorganization/class/conferenceorboothattendee.class.php`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_actioncomm` | integer | Yes | — | Associated calendar activity or event. |
| `fk_project` | integer | No | — | Associated project identity. |
| `fk_invoice` | integer | Yes | — | Customer invoice identifier. |
| `email` | varchar(128) | Yes | — | Email address associated with this record. |
| `email_company` | varchar(128) | Yes | — | Company email. |
| `firstname` | varchar(100) | Yes | — | Person's given name. |
| `lastname` | varchar(100) | Yes | — | Person's family name. |
| `date_subscription` | datetime | Yes | — | Date Of Registration. |
| `amount` | double | Yes | `NULL` | Monetary amount. Its operational meaning follows the record purpose. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `last_main_doc` | varchar(255) | Yes | — | Location of the latest main document generated for the record. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `model_pdf` | varchar(255) | Yes | — | Selected document output model. |
| `status` | smallint | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_replacement` | integer | Yes | — | Attendee entry linked as a replacement. |

Source locations include `htdocs/install/mysql/tables/llx_eventorganization_conferenceorboothattendee.sql`, `htdocs/install/mysql/tables/llx_eventorganization_conferenceorboothattendee.key.sql`, `htdocs/eventorganization/class/conferenceorboothattendee.class.php:49`.
