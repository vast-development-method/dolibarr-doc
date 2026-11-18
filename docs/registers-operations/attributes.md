# Product variant attribute definitions

An internal user with `variants.read` can open this register when variants are enabled. It selects `product_attribute` from the eligible attribute entities, with `search_current_entity` selecting current-only scope instead of shared scope. Its result is one grouped row per attribute definition. Default ordering is by `position`.

Two optional child sets participate. Values join through `product_attribute_value.fk_product_attribute`. Combinations join through `product_attribute_combination2val.fk_prod_attr`. The list independently counts distinct value row IDs and distinct combination IDs (`fk_prod_combination`). It does not count stock balances, active values only, or occurrences of a value on each product. An attribute with no children remains visible with both counts zero.

| Input | Predicate |
| --- | --- |
| `search_rowid`, `search_position` | Numeric comparisons on the definition, before grouping. |
| `search_ref`, `search_ref_ext`, `search_label` | Keyword tests on each stored field. Global `search_all` uses these three text fields. |
| `search_nb_of_values`, `search_nb_products` | Numeric comparisons after grouping on distinct value and combination counts respectively. An entered zero is supported. |
| Date or status filter | The generic register builder can apply date ranges and status tests to declared fields. This attribute definition declares row ID, two references, label and position, with no date or status among them. |

An attribute with three values and usage in four distinct combinations returns **3** and **4**, even if joining both child sets produces twelve intermediate rows. A second, unused attribute with two values returns **2** and **0**. Selecting zero combinations retains the second. A combination count of four does not establish that four different parent item designs use the attribute.

The row data and pagination count are calculated separately. The count query wraps the grouped, filtered result in an outer count. Its result reader uses the number of returned count rows rather than the scalar count inside that row. When a full count is enabled this can yield a displayed total of one even when the data query returns multiple distinct attributes. To reconcile a configuration export, count the qualifying grouped attributes themselves.
