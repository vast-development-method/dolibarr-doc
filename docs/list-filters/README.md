# Register search and filter dictionary

Use this dictionary to answer three questions about a saved search. Which record does a result identify? Which field or relationship qualifies it? Which records could this operator see before entering the search? Selecting a party, project or user has different consequences across registers. For instance, an intervention date selects work lines, an expense start date selects a claim header, and a contract expiry month selects the earliest planned end of an open service.

| Predicate guide | Registers traced |
| --- | --- |
| [Sales and purchasing](sales-and-purchasing.md) | Customer and supplier quotations, orders and invoices. |
| [Catalog and fulfillment](catalog-and-fulfillment.md) | Products and services, warehouses, physical inventory sessions, outbound shipments and inbound receipts. |
| [People and services](people-and-services.md) | Leave requests, expense reports, service contracts, field interventions and the internal ticket queue. |
| [Projects and tasks](projects-and-tasks.md) | Projects and opportunities, project tasks and their contact and time relationships. |

## What the inventories count

The [screen index](screen-index.csv) identifies 56 named registers, including 55 in standard modules and one development report. The four guides above cover 18 registers. The inventory links the other 38 to their selection and reconciliation guides. Each of the 56 has a documented row type, scope and selection behaviour. Each register has a stable screen key shared by the two selector tables. Consult the [operator register inventory](../coverage/operator-list-inventory.md) for the scope of the register set. Cards, pickers, generated reports, dashboards and site-defined attributes have different selection rules. See [bulk operations](../bulk-operations/README.md) for actions launched after a search.

The [literal request index](request-keys.csv) records 1,222 distinct **screen and selector** pairs across all 56 registers. Fifty-four have at least one literal binding. The local-tax payment and supplier-price registers use other controls and therefore contribute zero rows. On each screen, it counts each literal argument starting with `search_` passed to an active request reader or presence test once. A row labeled **date widget prefix** identifies a date-reader prefix rather than a single posted scalar. Day, month and year are appended by the shared reader. The index includes consumed form flags and inputs that lack an effective predicate. Nonprefixed business inputs such as `socid`, `type`, `statut` and `catid` appear in the corresponding guide. A checkbox's bracket suffix denotes repeated values in the form.

The [field-derived selector table](metadata-keys.csv) covers 163 register/field pairs across ten registers. Eight registers use the declared field map to build predicates. Salaries and users read 28 fields between them but use separate, explicitly selected inputs to filter rows. Each row gives the stored field, input name, visibility, comparison and observed use. The [field-derived selection guide](field-derived-selection.md) explains date parts, role and configuration restrictions, and overlap with literal inputs. A lookup of a bare date and an inclusive date range can use different controls.

Computed category parameter names also appear in the guides. For example, the project and creator categories are `search_category_project_list` and `search_category_user_list`, while a warehouse uses `search_category_warehouse_list`. The filter builder constructs these by joining a prefix, category type and suffix. User-defined keys expand against the organization's own optional-field definitions. Literal, metadata and computed names can overlap, so adding these row counts would misstate the number of distinct functional filters.

## Predicate and date notation

| Type of comparison | Example and result |
| --- | --- |
| Text | A normal token searches a substring. Space-separated terms combine as requirements. A vertical bar supplies alternatives within a term. Fields in a positive multi-field search give alternative places to find each term. A row-ID field addressed by the text matcher is compared numerically for equality. |
| Numeric | `>=100 <200` includes 100 and excludes 200. The shared matcher normalizes numbers before comparing them. A screen that checks only whether the input is truthy can skip the literal string zero. |
| ID set or code set | A set compares membership in selected stored IDs or codes. This differs from comparing a user-entered string to a label and from asking whether a related record exists. Individual screens decide what zero, −1, −2 or an empty value means. |
| From and to dates | Unless a screen specifies otherwise, an inclusive lower date starts at 00:00:00 and its upper date ends at 23:59:59. The suffix spelling is significant. For example, the order date reader uses `search_dateorder_start_day` while a contract's date reader uses `search_date_startday`. |
| Calendar component | Where a screen uses the shared calendar-component filter, a year alone selects the full year, year plus month selects that month and adding a day selects that calendar day. A month alone tests that month across years. A day alone supplies no date restriction, and month numbers above 12 yield no matches. |

A search can change row grain. Showing work-line columns can cause several rows per intervention, while a product-category existence test can admit a commercial document once even if it contains multiple matching products. The individual chapters identify such joins, the sequence of scope and filter decisions, screen-specific omissions and cases where an apparent filter does not reach the standard query.
