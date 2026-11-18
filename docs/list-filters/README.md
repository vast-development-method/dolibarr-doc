# Register search and filter dictionary

Use this dictionary to answer three questions about a saved search. Which record does a result identify? Which field or relationship qualifies it? Which records could this operator see before entering the search? Selecting a party, project or user has different consequences across registers. For instance, an intervention date selects work lines, an expense start date selects a claim header, and a contract expiry month selects the earliest planned end of an open service.

| Predicate guide | Registers traced in release 24.0.3 |
| --- | --- |
| [Sales and purchasing](sales-and-purchasing.md) | Customer and supplier quotations, orders and invoices. |
| [Catalog and fulfillment](catalog-and-fulfillment.md) | Products and services, warehouses, physical inventory sessions, outbound shipments and inbound receipts. |
| [People and services](people-and-services.md) | Leave requests, expense reports, service contracts, field interventions and the internal ticket queue. |
| [Projects and tasks](projects-and-tasks.md) | Projects and opportunities, project tasks and their contact and time relationships. |

## What the inventories count

The [screen index](screen-index.csv) enumerates every tracked file under `htdocs/` whose basename is exactly `list.php` in the release tree. Of its 56 paths, 55 belong to stable modules. The four guides trace predicates on 18. Three more stable paths have partial screen evidence elsewhere and 34 await their first screen trace. One development report falls outside the stable scope. The [operator list inventory](../coverage/operator-list-inventory.md) records the ownership and evidence behind those classifications. Entity and analysis screens using other filenames, cards, AJAX pickers, generated reports, dashboards, external add-ons and site-defined attributes are outside this filename count. For the bulk actions launched after a search, see the [selection and bulk operation guide](../bulk-operations/README.md).

The [literal request index](request-keys.csv) records 683 distinct **screen and selector** pairs on the 18 traced paths. On each screen, it counts each literal argument starting with `search_` passed to an active request reader or presence test once. Its line number is the first such use on that screen. A row labeled **date widget prefix** identifies a date-reader prefix rather than a single posted scalar. Day, month and year are appended by the shared reader. The index includes consumed form flags and inputs that lack an effective predicate. Nonprefixed business inputs such as `socid`, `type`, `statut` and `catid` appear in the corresponding guide. A checkbox's bracket suffix denotes repeated values in the form.

The [field-derived selector table](metadata-keys.csv) adds 67 declarations on three lists that read fields by name from object metadata. Each row gives the header field, translation label key, declared list visibility, comparison used for a direct value, metadata source line and query range. A visibility of zero hides the field. Negative values normally start unselected and absolute value 3 is excluded from the standard selectable list columns. Feature settings and screen-specific controls can further limit what appears. A direct date field in this table describes how a bare value is treated. The guides identify the separate date-range controls that actually function.

Computed category parameter names also appear in the guides. For example, the project and creator categories are `search_category_project_list` and `search_category_user_list`, while a warehouse uses `search_category_warehouse_list`. The source constructs these by joining a prefix, category type and suffix. User-defined keys expand against the organization's own optional-field definitions. Literal, metadata and computed names can overlap, so adding these row counts would misstate the number of distinct functional filters.

## Predicate and date notation

| Type of comparison | Example and result |
| --- | --- |
| Text | A normal token searches a substring. Space-separated terms combine as requirements. A vertical bar supplies alternatives within a term. Fields in a positive multi-field search give alternative places to find each term. A row-ID field addressed by the text matcher is compared numerically for equality. |
| Numeric | `>=100 <200` includes 100 and excludes 200. The shared matcher normalizes numbers before comparing them. A screen that checks only whether the input is truthy can skip the literal string zero. |
| ID set or code set | A set compares membership in selected stored IDs or codes. This differs from comparing a user-entered string to a label and from asking whether a related record exists. Individual screens decide what zero, −1, −2 or an empty value means. |
| From and to dates | Unless a screen specifies otherwise, an inclusive lower date starts at 00:00:00 and its upper date ends at 23:59:59. The suffix spelling is significant. For example, the order date reader uses `search_dateorder_start_day` while a contract's date reader uses `search_date_startday`. |
| Calendar component | Where a screen uses the shared calendar-component filter, a year alone selects the full year, year plus month selects that month and adding a day selects that calendar day. A month alone tests that month across years. A day alone supplies no date restriction, and month numbers above 12 yield no matches. |

A search can change row grain. Showing work-line columns can cause several rows per intervention, while a product-category existence test can admit a commercial document once even if it contains multiple matching products. The individual chapters identify such joins, the sequence of scope and filter decisions, screen-specific omissions and cases where an apparent filter does not reach the standard query.

Sources for the shared comparison, date and metadata rules are `htdocs/core/lib/functions.lib.php:1014–1066,13538–13673,13686–13781`, `htdocs/core/lib/date.lib.php:401–431` and `htdocs/ticket/class/ticket.class.php:266–277`.
