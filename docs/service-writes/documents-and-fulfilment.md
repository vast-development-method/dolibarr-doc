# Commercial lines, warehouse allocations and production postings

## From a header to its detail rows

The buyer or supplier ID in a document header identifies the counterparty. A child row can also identify a product, another line in the same document, the original line of a different document, a unit and a supplier price. These identities serve different joins. Use a saved child ID for a later line amendment.

| Header POST | How the submitted `lines` reach the record writer |
| --- | --- |
| `/proposals` | The quotation writer turns array entries into commercial line objects. It passes line price, quantity, discount, taxes and origin into quotation detail creation. The separate bulk line operation can append a group to an existing quotation. |
| `/orders` | The sales order writer turns arrays into order lines and applies a tax-exclusive basis. A VAT source code can qualify the rate. A special group line establishes a new parent ID for dependent detail. Original document and line links can be copied into the resulting rows. |
| `/invoices` | The invoice writer creates billed detail under the new invoice. Quantity, base price, discounts, tax treatment and foreign price affect the saved totals. A deposit allocation has separate linkage and valuation rules. [Billing line commands](../invoice-processing/line-commands.md) |
| `/supplierorders` | The purchase order writer accepts array lines. It reads `ref_supplier` before the fallback `ref_fourn`, uses the tax-exclusive price basis, defaults the rank to −1 and passes zero for the supplier-price identity in this creation path. |
| `/supplierinvoices` | The supplier bill writer converts a row for its main field reads, inserts an initial detail and then updates it. It falls back from `desc` to `description`. The accesses to `special_code` and `fk_remise_except` use the original element's object properties. The loop also does not test the detail updater's return. Read back the amounts and links when using header-line creation. [Supplier billing inputs](../services/supplier-invoice-line-inputs.md) |
| `/supplierproposals` | The supplier quotation writer reads child object properties directly. Plain decoded array members do not receive the conversion applied by the purchase order writer. Verify the saved detail before using its price, supplier reference or source link. |
| `/contracts` | Header creation has no child-line insertion loop. Append service obligations through `POST /contracts/{id}/lines`. Opening or closing a service obligation subsequently acts on its saved line. |

## Appending quotation lines

`POST /proposals/{id}/line` takes one line. The plural `POST /proposals/{id}/lines` takes a collection. Each top-level item can be one named-field object or one list of line objects. An item with an empty first positional element is wrapped as one line. The operation expands one grouping level. Grouping controls iteration only. Use `fk_parent_line` to express a business parent.

| Line members passed to the writer | Meaning |
| --- | --- |
| `desc`, `label`, `fk_product`, `product_type`, `fk_unit`, `qty` | Identify and describe the quoted unit and quantity. |
| `subprice`, `tva_tx`, `localtax1_tx`, `localtax2_tx`, `remise_percent`, `multicurrency_subprice`, `fk_remise_except` | Set the tax-exclusive unit amount, rates, discount and alternate-currency price or identify an exceptional discount. |
| `fk_fournprice`, `pa_ht`, `date_start`, `date_end` | Supply buying-price information and the service interval. |
| `rang`, `special_code`, `info_bits`, `fk_parent_line`, `origin`, `origin_id`, `array_options` | Supply ordering, special processing, hierarchy, source identity and configured line values. |

The bulk operation fetches and authorizes the quotation before opening its transaction. It visits the remaining lines after a negative add result and then rolls back the entire group with HTTP 400. On success it returns the last writer result. An empty collection returns zero. A successful retry after a lost response can append the same lines again.

## Editing an existing line

| Line operation | Consequence of a field choice or omission |
| --- | --- |
| Quotation | The operation checks that the line belongs to the quotation and uses its saved fields for most omissions. Missing `price_base_type` selects `HT`. Missing `multicurrency_subprice` falls back to the stored base unit price. Provide the intended foreign price when the two prices differ. |
| Invoice or sales order | The service passes many individual values directly into the line writer, including pricing and quantity. Read the existing line and supply the values the operation consumes for the intended amendment. The PUT verb alone does not preserve all omitted fields. |
| Contract | The writer distinguishes forecast and effective service dates. The supplier-price member is `fk_fournprice` on addition and `fk_fourn_price` on amendment. |
| Bill of materials | Component addition identifies the product. Amendment updates values including quantity, rank, efficiency, frozen quantity and the stock-change flag. The update does not pass a replacement product ID to the component writer. |
| Expense report | Adding detail requires a draft parent and `date`, `fk_c_type_fees`, `qty`, `value_unit` and `vatrate`. The detail can also relate to a project and an indexed supporting file. |
| Intervention | An amendment starts from the fetched line and preserves values for omitted fields. It accepts `desc` or `description`, along with `date`, `duration` and `rang`. |

## Shipping and receiving

Both `POST /shipments` and `POST /receptions` require header `socid`, `origin_id` and `origin_type`. Each entry in `lines` identifies its source header and detail. The service prefers `fk_element` over `origin_id`, `fk_elementdet` over `origin_line_id` and `element_type` over `origin_type` when choosing the line's references.

| Movement document | Allocation input | Stored relationship |
| --- | --- | --- |
| Outbound shipment | Per line, `entrepot_id`, `qty`, `rang`, optional `array_options` and `detail_batch`. Product resolution uses the source order detail. | Ordinary detail relates a shipment and source line to the shipping warehouse. The lot writer groups detail by `fk_warehouse`, sums lot quantities within each warehouse, creates a shipment detail per group and calls each lot record's create operation with that detail's new ID. |
| Inbound reception | Per line, `fk_product`, `fk_entrepot`, `qty`, `array_options`, `batch`, `eatby`, `sellby`, `cost_price` and `status`, plus the source identifiers. | The adapter creates a receipt-line object for each submitted item. To represent different lots against one source line, each entry needs its own warehouse, quantity and lot attributes. |

On outbound shipments the adapter copies `detail_batch` directly. The child writer expects objects with readable warehouse and quantity properties and a persistence method. A plain JSON list of maps alone does not supply these objects. The header's successful creation cannot establish the number of lot rows. Reconcile saved shipment detail, warehouse and lot quantities before validating the movement. Document creation and stock posting are separate state changes.

### Dispatching against a purchase order

`POST /supplierorders/{id}/receive` takes named arguments `closeopenorder`, `comment` and `lines`. For each list entry it calls the dispatch writer with `fk_product`, `qty`, `warehouse`, `price`, line `comment`, `eatby`, `sellby`, `batch`, source line `id` and `notrigger`. The source line ID is distinct from the order ID in the path. The top-level comment accompanies final classification.

A negative dispatch result stops the loop with HTTP 500. Earlier dispatches may already persist. Only after every dispatch does the handler calculate and set the received state. A zero classification result returns 304 and a negative result returns 500. Reconcile each source line, warehouse and lot before resubmitting the undelivered balance.

## Posting manufacturing quantities

| Operation | Input identity | How to measure the result |
| --- | --- | --- |
| `POST /mos/{id}/produceandconsume` | In `arraytoconsume` and `arraytoproduce`, `objectid` is a saved **production plan line**. Each entry carries `qty`, a warehouse where stock applies and optional output valuation `pricetoproduce`. | Consumed entries precede produced entries. Actuals retain their plan identity and optional movement ID. Re-fetch the plan and compare the sum achieved against each target. |
| `POST /mos/{id}/produceandconsumeall` | When both lists are nonempty, `objectid` is a **product**. With zero or one nonempty list the bulk action takes its saved-plan branch. | The supplied-product branch can add a planned-role row and an actual tied to the same stock movement. Its actual does not identify an earlier plan row. The saved-plan branch uses whole planned quantities. |

Both routes require a validated or in-progress order and nonempty `inventorylabel` and `inventorycode`. Automatic close defaults to enabled. The movement code can occur on many movements. A caller recovering from a lost response must compare actuals and physical movements before posting more. The [posting modes](../production-control/posting-modes.md) detail the stock flags, lot restrictions, costs and close decisions for each branch.
