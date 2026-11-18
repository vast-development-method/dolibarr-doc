# Fixed asset register

The fixed asset register reads `asset` headers. It requires enabled asset management, an internal user, the asset-area access check and the asset-read grant. Write and delete actions use separate grants. The normal entity set follows asset sharing. The current-entity option limits the same query to the current entity. A configured-property left join uses `asset.rowid = asset_extrafields.fk_object` when custom fields are present.

| Selection | Stored decision |
| --- | --- |
| Search across fields | Match keywords against `ref` and `label`. Individual text criteria can target other enabled declared fields. |
| Asset identification and classification | Record ID and quantity are numeric. Select the model with `fk_asset_model`. Acquisition class distinguishes new (0) and used (1). Asset class distinguishes intangible (0), tangible (1), in-progress (2) and financial (3). |
| Lifecycle | Select draft (0), validated (1) or cancelled (9). Passing −1 omits the status filter. A listed choice of zero remains a real selection for enumerations that define it. |
| Valuation and disposal | Numeric criteria can target untaxed acquisition value, recovered VAT, untaxed reversal value and untaxed disposal value. Depreciation eligibility, disposal type and the disposal flags are separate properties. |
| Date windows | Acquisition, start, reversal, disposal, creation, modification and validation dates have independent inclusive lower and upper bounds when applicable. |
| Other criteria | User selectors and import identifiers identify who created, changed or validated the header or which import supplied it. Active configured-field filters and extensions can further restrict the result. |

With counting enabled, the query counts the rows produced by its joins before pagination. Normal ordering starts with ascending header ID. The selected numeric measure columns accumulate displayed quantities, acquisition values, recovered VAT, reversal values and disposal values independently. There is no join to the depreciation schedule in the register. An asset with acquisition value 1,000 and three depreciation periods still contributes one header with acquisition value 1,000. To determine net book value, reconcile that header with the chosen depreciation basis and posted schedule. [Fixed asset calculations](../capital/fixed-assets.md)
