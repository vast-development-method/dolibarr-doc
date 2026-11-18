# Following a field to another business record

When a clerk selects a project on an invoice, three questions arise. Which project can the clerk select today? Which identifier will the invoice retain? What prevents deletion of the selected record? Each question has a different answer in the model.

The [field-to-target register](field-targets.csv) maps 265 stored fields on 75 tables to 34 target tables. It covers 263 object selectors and two dictionary selectors for which the owning field and target were resolved. For 73 of the mappings, the same field and target table also have a declared database foreign key. For the other 192, a selector alone gives no database delete or update guarantee. Use [all declared foreign keys](../relational-model/foreign-keys.csv) to check referential actions and [other application associations](../relational-model/application-associations.csv) for relationships established through an explicit field declaration or configured property ownership.

| Register column | Meaning |
| --- | --- |
| `owner_table`, `field` | The stored field on the business record. A header, detail line and linked document can each carry a different relationship. |
| `relationship_basis`, `target_table` | An object selector resolves a business record. A dictionary selector uses a reference table with a declared value key. |
| `dictionary_key` | The value returned by a dictionary selector. For an object selector the business object supplies its own identity. |
| `selector_condition` | A restriction declared on this selector, where present. Equality and membership tests refer to fields on the candidate record. The entity set is evaluated for the current organisation and sharing rules. Runtime settings, role and the particular operation can narrow the actual choice further. |
| `matching_foreign_key_target_column` | The destination column of a declared constraint on these endpoints. A blank cell means there is no matching declaration in the physical catalogue. |

## Three joins with different business meanings

| Starting field | Meaning and consequence |
| --- | --- |
| `facture.fk_soc` → `societe.rowid` | An invoice belongs to a trading party. The selected party identifies the debtor on this document. An invoice's project and its validating user are separate relationships. Two invoices for the same debtor do not necessarily share a project or a validator. |
| `bom_bom.fk_product` → `product` | The recipe's output selector admits an item whose `finished` value is null or nonzero. The input component comes from `bom_bomline.fk_product`. For a recipe consuming two distinct components, looking up the header product three times would report three outputs and lose both inputs. The selector is an application rule. [Production quantities and valuation](../production-control/README.md) |
| `asset.fk_disposal_type` → `c_asset_disposal_type.rowid` | The selector restricts choices to `active=1`. If a disposal category becomes inactive after an asset uses it, historical reporting can still join the stored identity. Applying the current input filter to the historical report can drop an existing disposal. |

A project-linked invoice illustrates the difference between input and history. Its static project selector specifies `fk_statut = 1`. An invoice deliberately left without a project and an issued invoice linked to a project that was subsequently closed represent different facts. Preserve the latter's project identity when reproducing its audit trail. On a calendar event the project selector instead carries an event-organisation condition. The same destination table supports both selections.

## What the register can establish

The catalogue covers resolved object and dictionary selectors on declared storage columns. Thirty-six rows carry a literal selector condition. An operation can set a field directly, override a control, hold a relationship on a bridge, or resolve a target from a type and an ID. Such relationships belong with their operation even when absent from the selector catalogue. In particular, a recipe line's owning recipe is `bom_bomline.fk_bom`, constrained against the recipe header. Its optional subrecipe uses the distinct `fk_bom_child`. The physical dictionary establishes the former even though the object selector alone does not resolve it. A sales order line's supplier price reference likewise identifies a price, which requires the supplier price and product records to interpret. Joining an item by a coincidentally equal price-row ID can return the wrong product.

[Record dictionary](../records/README.md) · [Document origins and allocation links](../platform/document-relationships.md) · [Complete field, key and index catalogue](../relational-model/README.md)
