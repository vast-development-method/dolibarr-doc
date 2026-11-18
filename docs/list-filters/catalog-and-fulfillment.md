# Catalog, warehouse, count, shipment and receipt filters

A product, a warehouse, an inventory session, an outbound shipment and an inbound receipt each have a different result grain. A reference field can identify the displayed record, a trading partner's reference or a linked delivery document. In request templates, braces denote alternatives. For example, `search_dateshipping_{start,end}{day,month,year}` expands to six parameter names, including `search_dateshipping_startday`. The ordinary date controls below use inclusive lower and upper bounds, assembled separately at 00:00:00 and 23:59:59.

## Products and services

The base row is a catalog item in the shared product entities. Opening the product, service or combined view selects the corresponding module-access check. Conditional joins supply the default workstation, the current entity's account mapping, the default-language translation, variant-parent membership, the unit and user-defined attributes. Supplier price quick search uses a correlated existence test, so three matching prices for one item still provide one match.

| Request key | Effect on the result |
| --- | --- |
| `search_id` | Numeric search on the item ID. |
| `search_ref`, `search_ref_ext`, `search_import_key` | Text search on the internal item reference, external reference and import marker respectively. |
| `search_label` | Text match on the base label or, with translations enabled, the label in the joined default language. |
| `search_default_workstation`, `search_barcode` | Text match on the joined workstation reference or on the item's own barcode. The workstation join requires that module. |
| `search_all` | Default fields are reference, label, description and note. Translation search adds translated label, description and note. Barcode support adds the item barcode. In addition, an item qualifies through a matching supplier price reference or, with barcode support, a supplier price barcode. Configuration can replace the direct-field set. The supplier-price existence branch still runs. |
| `type`, `search_type` | Opening a product or service context seeds an empty type selection. Value 1 selects service records. The product selection admits all stored types other than 1. An empty selection or −1 gives no type predicate. |
| `search_show_childproducts`, `search_show_childproducts_flag` | With variants enabled, an unselected checkbox excludes items linked as children. A selected checkbox includes children alongside other products. The companion flag identifies form resubmission. |
| `search_tosell`, `search_tobuy`, `search_stockable_product` | Each is a separate equality on the corresponding sale, purchase or stockable flag. Zero selects an explicit false value. Empty and −1 skip the condition. |
| `search_tobatch` | Equality on tracking mode. The selector offers 0 for untracked, 1 for lots and 2 for serials. |
| `search_vatrate` | Numeric search on the product tax percentage. A bare string `0` does not enter the truth-tested search branch. |
| `search_finished` | Nonnegative product nature code selects the stored `finished` value. |
| `search_country`, `state_id` | Exact item country and item state IDs. The state parameter is cast to a single integer before comparison. |
| `search_units` | With unit support enabled and a selection present, runs text-mode natural search on the joined unit ID. |
| `search_accountancy_code_sell`, `search_accountancy_code_sell_intra`, `search_accountancy_code_sell_export` | Clean the submitted account string, then text-search the corresponding domestic, intra-community or export sale mapping. The shared-per-entity setting selects the current entity's mapping row. |
| `search_accountancy_code_buy`, `search_accountancy_code_buy_intra`, `search_accountancy_code_buy_export` | The same three tests against purchase account mappings. |
| `search_date_creation_{start,end}{day,month,year}`, `search_date_modif_{start,end}{day,month,year}` | Bound creation time or last modification time independently. |
| `search_category_product_list[]`, `search_category_product_operator`, `catid` | Positive IDs test direct product memberships. Operator 0 requires every selection and 1 accepts any. Value −2 requires no product-category relation. An initial category ID seeds an empty selection. A submitted filter form uses its supplied operator, while the initial view can use the configured default. |
| `canvas` | A supplied canvas key selects the exact stored canvas and can select a specialized view. |

The standalone `search_ref_supplier` input has no matching predicate in this query. The separate `fourn_id` condition addresses a supplier-price alias outside the correlated subquery, while the outer join for that alias is commented out. A positive supplier ID can therefore produce a query error in the base view. Quick search remains the traced supplier-reference path. Measurements, physical and virtual stock totals and displayed prices do not acquire ordinary numeric filters from column selection.

## Warehouse directory

The stock-area check applies first. Each warehouse in the permitted stock entities can appear even with no stock rows. The directory left-joins the item/warehouse balance and the item, sums physical quantity, cost value and sale value, then groups by the warehouse fields. In per-entity costing mode, the cost calculation uses the entity item's average cost with fallback to the item cost. Those three aggregates have empty filter cells.

| Request key | Warehouse predicate |
| --- | --- |
| `search_all` | Text search across reference, description, location summary, street address, postal code, town, telephone and fax. |
| `search_ref`, `search_description`, `search_lieu` | Text search on the corresponding warehouse reference, description or location summary. |
| `search_address`, `search_zip`, `search_town`, `search_phone`, `search_fax` | Text search on that contact field of the warehouse itself. |
| `search_rowid`, `search_fk_departement` | Numeric search on the warehouse ID or stored state/department ID. These fields have hidden column metadata. |
| `search_fk_parent`, `search_fk_project`, `search_fk_pays` | Selected IDs for parent warehouse, project and country. Empty and unselected reference values suppress these tests. Project selector visibility depends on the project module. |
| `search_warehouse_usage`, `search_status` | Selected warehouse use (1 internal, 2 external) or status. Status uses stored `statut`. Values are 0 closed, 1 open, and optionally 2 open for internal movements. The status predicate skips −1. |
| `search_category_warehouse_list[]` | With category support, every positive ID requires direct warehouse membership. Value −2 requires no such relation. The operator is fixed to AND, so combining −2 and a positive ID cannot match. |

The metadata loop accepts `search_datec` and `search_tms` as direct field criteria. The form instead emits `search_{datec,tms}_{dtstart,dtend}{day,month,year}` for visible date columns. The input loop never assembles those components, so those range controls do not narrow the base query. `sref`, `snom` and `search_label` feed standalone variables only. The predicate loop reads `search_ref` and `search_lieu` from the request. It explicitly skips `search_entity`.

## Physical inventory sessions

External users are denied. Internal access uses stock permission, or the inventory-specific check when advanced permissions are enabled. One result is one inventory header in the permitted inventory entities. A session covering every item can contain an item in its count lines while its header has no selected product. The header's product filter will not retrieve that session by line membership.

| Request key | Inventory header predicate |
| --- | --- |
| `search_all`, `search_ref`, `search_title`, `search_import_key` | Global search uses reference alone. The three individual text inputs search reference, session title and import marker respectively. |
| `search_rowid`, `search_entity` | Numeric comparison on header ID or entity. Entity input intersects the permitted entity scope. The metadata can hide these columns. |
| `search_fk_warehouse`, `search_fk_product` | Selected ID of the warehouse or product defining the session's scope. |
| `search_fk_user_creat`, `search_fk_user_modif`, `search_fk_user_valid` | Selected ID of the creator, last modifier or validating user. |
| `search_status` | Selected status code, including 0 draft, 1 validated, 2 closed or 9 canceled. −1 disables the condition. |
| `search_categories_product` | Generic text-mode natural search on the stored header field of this name. Its metadata type is a checkbox-list and the field is excluded from selectable list columns by its visibility setting. |
| `search_{date_inventory,date_creation,tms,date_validation}_{dtstart,dtend}{day,month,year}` | Inclusive bounds on inventory value date, creation, last modification and validation respectively. The value-date column is configurable. The input loop also accepts direct `search_<field>` values for these fields. |
| `search_category_product_list[]`, `search_category_product_operator` | Separate category box builds product membership conditions for positive IDs and no-membership for −2. All/any handling resembles the catalog. The base inventory query supplies no product alias for the generated condition (`p.rowid`). A meaningful category selection can therefore fail the base query. |

Typed ID selectors skip −1 and zero when zero is absent from their metadata choices. Numeric and text fields use their corresponding natural-search modes. Quantity found, quantity before adjustment, adjusted quantity, batch and cost are detail-level fields outside the header query.

## Outbound shipments

The list checks shipment access, applies the shipment entity set and honors `socid` as the customer ID. An external user's linked party replaces the request value. The base row is one dispatch header with its business partner and geography. Global or order-contact searches request distinct result rows because they add detail or contact joins. The normal delivery-link branch assumes at most one linked delivery per dispatch.

| Request key | Shipment predicate |
| --- | --- |
| `search_ref_exp`, `search_ref_customer`, `search_tracking` | Text search on dispatch reference, customer's document reference or tracking number. |
| `search_company`, `search_town`, `search_zip`, `search_state` | Text search on the partner name, town, postal code or joined department/state name. |
| `search_country`, `search_type_thirdparty` | Membership against the partner country ID or selected positive third-party type IDs. |
| `search_status`, `search_signed_status`, `search_billed` | Each nonempty nonnegative selection compares a single integer with dispatch status, signature status or billed flag. Zero is meaningful. |
| `search_shipping_method_ids[]` | Any selected method ID may equal the shipment's shipping method. |
| `search_dateshipping_{start,end}{day,month,year}`, `search_datedelivery_{start,end}{day,month,year}` | Bound dispatch date and planned delivery date respectively. |
| `search_ref_liv`, `search_datereceipt_{start,end}{day,month,year}` | With the delivery submodule enabled, follow the shipment-to-delivery link and search the delivery's reference or bound its delivery date. |
| `search_user` | A positive user must be an internal contact on the linked source customer order. Any internal order-contact role qualifies. |
| `search_sale` | Positive user ID requires a sales representative assignment to the party, −2 requires no assignment and −1 is neutral. |
| `search_categ_cus`, `search_category_customer_operator` | Direct customer category membership. −2 selects a party with no customer category assignment. |
| `search_product_category`, `search_category_product_operator` | Follow dispatch line → source order line → product → category. A positive category needs at least one matching product. −2 requires no categorized product in the joined lines, including when those joins yield no rows. |
| `search_all` | Direct text search across dispatch reference, partner name, public note and tracking number. Internal users also search the private note. The detail join does not add item labels or line descriptions to this field set. |

Both category handlers wrap a single request value in an array, then cast that value to an integer. Their all/any branches do not implement a multi-ID request list. The note, weight, creation and modification columns have empty filter cells.

## Inbound receipts

The receipt list applies the corresponding module check and entity scope. `socid` restricts the receipt's supplier, with a linked external party overriding the requested ID. It reads receipt headers and left-joins their business partner, geography and linked delivery documents. It selects ordinary rows, so multiple matching delivery links can produce multiple rows for a receipt.

| Request key | Receipt predicate |
| --- | --- |
| `search_ref_rcp`, `search_ref_supplier`, `search_ref_liv` | Text search on receipt reference, supplier's reference on the receipt or reference of its linked delivery document. |
| `search_company`, `search_town`, `search_zip`, `search_state` | Match the supplier name, town, postal code or joined state/department name. |
| `search_country`, `search_type_thirdparty` | Membership against supplier country ID or selected positive third-party type IDs. |
| `search_status`, `search_billed` | A nonempty nonnegative selection equals the stored receipt status or billed flag. |
| `search_date_delivery_{start,end}{day,month,year}`, `search_date_create_{start,end}{day,month,year}` | Bound planned delivery date or receipt-header creation time. Received date and last modification have no separate range controls. |
| `search_note_public`, `search_note_private` | Each builds an escaped substring match on its respective receipt note. These predicates are independent of the global-search field set. |
| `search_all` | Match receipt reference, supplier's reference, supplier name or public note. Internal users also match the private note. |

The sales representative condition is commented out. The base receipt query has no filter for supplier-order contact, carrier, tracking, product category or receipt lines.

## Configured fields and list controls

Where optional attributes are defined for the listed object, the shared list mechanism accepts `search_options_<code>`. The normal join is by the record ID to the extra attribute row. Date ranges use `search_options_<code>_{start,end}{day,month,year}`. Datetime fields can additionally carry hour and minute components. The predicate depends on the attribute definition. Date bounds support one or two endpoints, a false boolean selection also matches a null value, and multiselect attributes use their collection-specific matching. Inventory invokes the shared list templates but its constructor declares optional-field management disabled.

Page number, limit, sort column and direction arrange or slice results. Selected columns determine which form controls render. Mass-action selection identifies rows for subsequent operations. None adds a business predicate by itself. Filter-submit and filter-clear controls also reset the page offset.
