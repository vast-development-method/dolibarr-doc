# Widget catalogue

The 62 entries identify the shipped widget implementations at the 24.0.3 baseline. For a source key such as `actions`, read `htdocs/core/boxes/box_actions.php`. The aggregate state board has an immutable source blob locator. Module entries identify `htdocs/core/modules/mod<Name>.class.php` and the declaration line. The domain column gives the read permission or special activation condition. See [placement and access](README.md) for how a definition reaches a user’s dashboard.

## People, agenda and operations

| Widget source key | Definition | Access and activation | Population and ordering |
| --- | --- | --- | --- |
| `lastlogin` | `User:82` | Current user | Previous sign-in time and address, plus the most recent password-validation timestamp. Missing timestamps display as unknown. |
| `birthdays` | `User:83` | Internal user directory read | Enabled users with a birthday or employment anniversary in the current month. Each date qualifies independently if it falls before January 1 of the current year. A recent hire can still appear for a birthday. The two sets share a day-of-month sort and one row limit, including days already passed. |
| `bookmarks` | `Bookmark:72` | Bookmark read | Current user’s saved bookmarks in the current entity, ascending saved position. Create permission changes the shortcut. |
| `actions` | `Agenda:117` | Own agenda read | Events with progress from 0 up to, but excluding, 100. Oldest scheduled start first. Without all-agenda read, author or owner must match the viewer. |
| `actions_future` | `Agenda:118` | Own agenda read | Events strictly after now, earliest scheduled start first. There is no incomplete-progress test. Uses the same author/owner restriction as the outstanding-event shortlist. |
| `scheduled_jobs` | `Cron:93` | Scheduler read | Non-disabled global or current-entity jobs whose execution condition evaluates true. Reports last run, next candidate, jobs still processing after 24 hours and jobs with a nonempty last result. |
| Aggregate state board, blob `770a3aaf38f345ab80e93a7719090a66ae9aa7aa` | `User:84` | Internal user, per-domain grants | Counts reported by each enabled domain’s state-board provider. Per-domain suppression flags and a global switch affect visibility. Links and zero counts belong to the corresponding domain. |
| `external_rss` | Admin feed setup, `htdocs/admin/external_rss.php:106`, `ExternalRss:107` | Feed setup | One admin-configured syndication feed per definition, distinguished by its note. Parser uses the requested item maximum and a default one-hour cache. |
| `fediverse` | Admin feed setup, `htdocs/admin/fediverse.php:123` | Social networks enabled | One admin-configured social feed per definition, bound by name to its settings. A request returns recent posts up to the configured shortlist size, with a default one-hour cache. |

## Parties and the sales pipeline

| Widget source key | Definition | Access and activation | Population and ordering |
| --- | --- | --- | --- |
| `clients` | `Societe:127` | Internal party read, customers enabled | Customer or customer/prospect parties (roles 1 and 3), newest modification first. Restricted sales staff need a party assignment. |
| `prospect` | `Societe:128` | Internal party read, prospects enabled | Prospect or dual-role parties (roles 2 and 3), newest modification first. A dual-role business can appear in both lists. |
| `fournisseurs` | `SupplierOrder:112` / `SupplierInvoice:114` / `Fournisseur:145` | Internal party read, supplier capability | Supplier flag set, newest party modification first, restricted to assigned suppliers for staff with limited party visibility. |
| `contacts` | `Societe:129` | Party and contact read | Contact modification order, with the contact entity, private-owner rule and party visibility applied. External viewers use their party. |
| `goodcustomers` | `Societe:131` | Party read, customer feature and best-customer option | Ranks parties by number of invoice headers, reporting how many are marked paid. No date, document-state or amount criterion in this ranking. |
| `propales` | `Propale:134` | Proposal read | Proposals by modification or proposal date, then descending reference. Customer assignment or external party narrows the population. |
| `commandes` | `Commande:107` | Customer order read | Orders by modification or order date, then descending reference. Validated-only option keeps status 1. |
| `shipments` | `Expedition:140` | Shipment read | Sort by shipment modification, then delivery date and reference. Optional validated-only filter selects status 1. Source customer order is resolved through a document link. |
| `activity` | `Societe:130` | Feature level above zero and respective commercial reads | Rolling activity by status. Three months by default. Proposal date and no closure date, order date, invoice date and paid flag define separate populations. Amounts include tax. |
| `project` | `Projet:132` | Project read | Open projects ordered by creation date. Restricted readers use authorized project IDs. Displayed progress is the rounded arithmetic mean of task progress over counted rows. |
| `project_opportunities` | `Projet:133` | Project read, opportunities enabled | Opportunity-use projects in draft or open state with a positive stage ID, newest creation first. Applies authorized project filtering for limited readers. |
| `funnel_of_prospection` | `Projet:136` | Project read, opportunities enabled | Open projects grouped by active stage, excluding WON and LOST. Counts, face value and probability-weighted value. Stage distribution aggregates the project entity set. |
| `task` | `Projet:134` | Project read, tasks visible | Incomplete tasks (null or less than 100 percent progress) on open task-enabled projects, due date then start ascending. Scope can narrow to tasks or projects assigned to the viewer. |
| `validated_projects` | `Projet:135` | Feature level 2 or higher, project read | Normally disabled. Counts distinct qualifying tasks on open projects without a time entry by this viewer, grouped by project and ordered by project start. The query also requires one of three specific task-contact type IDs. |

## Invoices, ordering and accounting

| Widget source key | Definition | Access and activation | Population and ordering |
| --- | --- | --- | --- |
| `factures` | `Facture:108` | Customer invoice read | Positive invoice status, newest modification or invoice date, then newest ID. Assigned-party scope applies. Includes closed and abandoned statuses. |
| `factures_imp` | `Facture:107` | Customer invoice read | Validated and unpaid customer invoices in permitted invoice entities. Earliest due date, then invoice reference. Row displays original tax-exclusive value. |
| `factures_fourn` | `SupplierInvoice:116` / `Fournisseur:147` | Supplier invoice read, invoice and supplier dependencies | Current-entity supplier invoices, ordered by modification or invoice date, then reference. No validation predicate in the shortlist. |
| `factures_fourn_imp` | `SupplierInvoice:115` / `Fournisseur:146` | Supplier invoice read, invoice and supplier dependencies | Validated and unpaid supplier invoices in permitted supplier-invoice entities. Earliest due date, then supplier reference. Allocations contribute to status display. |
| `customers_outstanding_bill_reached` | `Facture:110` | Internal party read, invoices and customers enabled | Customers with a positive limit and a validated invoice are tested in newest-modified-party order. Calculated open invoice exposure at or above the limit qualifies, including equality. |
| `supplier_orders` | `SupplierOrder:113` / `Fournisseur:148` | Supplier order read | Permitted supplier orders by modification or order date, then reference. The query includes every status. |
| `supplier_orders_awaiting_reception` | `SupplierOrder:114` / `Fournisseur:149` | Supplier order read | Sent or partially received orders with a delivery date. Default sort is delivery date, then status. Object-date mode sorts by order date and reference descending. |
| `comptes` | `Banque:80` | Bank read, external access configuration | Open accounts of the current entity sorted by label and limited before summation. Shows each selected balance and separate totals for each currency represented. |
| `accountancy_last_manual_entries` | `Accounting:160` (manual placement) | Ledger movement read | Current-entity bookkeeping rows with source document ID zero. Distinct piece number, document date, operation label, amount and journal tuples sorted by descending piece number. |
| `accountancy_suspense_account` | `Accounting:161` (manual placement) | Ledger movement read | Counts bookkeeping lines in the current entity with the configured suspense account number. Requires a populated, positive suspense account setting. |
| `graph_invoices_permonth` | `Facture:109` | Customer invoice read | Count and tax-exclusive amount by invoice month. Widget selects positive status and permitted invoice entities. |
| `graph_invoices_supplier_permonth` | `SupplierInvoice:113` / `Fournisseur:143` | Supplier invoice read | Count and tax-exclusive amount by supplier invoice month with positive status and the supplier-invoice entity set. |
| `graph_orders_permonth` | `Commande:108` | Customer order read | Count and tax-exclusive value by customer order date. Standard statistics constructor includes all order statuses. |
| `graph_orders_supplier_permonth` | `SupplierOrder:111` / `Fournisseur:144` | Supplier order read | Count and tax-exclusive value by supplier order date. Supplier table is used, with the shared order statistics entity selector and no approved-only condition. |
| `graph_propales_permonth` | `Propale:133` | Proposal read | Count and tax-exclusive proposal amount by proposal date. Draft, open and closed records can contribute. |
| `graph_invoices_peryear` | No matching definition | Unregistered source | Contains a customer invoice amount-by-year calculation. No matching definition in a current module or feed setup. Excluded from the ordinary dashboard. |

## Catalogue, stock, manufacturing and service

| Widget source key | Definition | Access and activation | Population and ordering |
| --- | --- | --- | --- |
| `produits` | `Product:110` | Catalogue read for each displayed type | Permitted product or service types by modification date. Display of list prices additionally follows per-type advanced price-read permission when enabled. |
| `produits_alerte_stock` | `Product:111` | Stock read and product or service read | Sum physical stock across joined stock records, treating a missing quantity as zero. Keep a positive product alert threshold strictly above the sum. Highest threshold sorts first. |
| `graph_product_distribution` | `Product:112` / `Service:83` | Enabled items and readable commercial documents | For the selected year, count occurrences of predefined item references in proposal, order or invoice lines. Separate charts for enabled sources. Remaining references beyond the shortlist accumulate under Other. |
| `boms` | `Bom:181` | Bill of materials read | Current-entity bills of materials joined to the parent catalogue item, newest modification then descending reference. Draft and active records can appear. |
| `mos` | `Mrp:189` | Bill of materials read for visibility and production-order read for data | Current-entity production orders joined to the product, sorted by modification then reference. Optional column identifies the validating user. |
| `contracts` | `Contrat:98` | Contract read | Current-entity contract headers by modification or contract date, then reference. Applies sales assignment or the external user’s party. |
| `services_contracts` | `Service:82` | Service and contract read | Contract lines joined to party and optionally product, in contract-header modification order. The displayed modification comes from the line. Multiple lines of one contract can fill the shortlist. |
| `services_expired` | `Contrat:99` | Contract read | Open service lines, state 4, with an end at or before now on positive-status contracts. Group by contract, count matching services and sort by the earliest expiry. |
| `ficheinter` | `Ficheinter:108` | Intervention read | Current-entity intervention headers by descending modification, subject to sales assignment or the external user’s party. |

## Support, knowledge and membership

| Widget source key | Definition | Access and activation | Population and ordering |
| --- | --- | --- | --- |
| `last_ticket` | `Ticket:217` | Ticket read | Ticket headers ordered by creation date then ID descending, subject to the external viewer’s party. No unread-only restriction. |
| `last_modified_ticket` | `Ticket:218` | Ticket read | Ticket headers ordered by the greater of the ticket and extension-record modification timestamps, then ID. External users are limited to their party. |
| `graph_ticket_by_severity` | `Ticket:219` (manual placement) | Ticket read | Counts entity tickets with status other than 8 by severity. Series are built from active severity codes, with zero for missing groups. |
| `graph_nb_tickets_type` | `Ticket:221` (manual placement) | Ticket read | Same status exclusion, grouped by type. Only active type codes supply chart labels. Counts by type and severity are two views of tickets. |
| `graph_nb_ticket_last_x_days` | `Ticket:220` (manual placement) | Ticket read | Ticket creations across the ticket entity set, grouped by database date. Default seven days, requests of 15 or more mapped to 14. Pads missing chart entries with zero. |
| `graph_new_vs_close_ticket` | No matching definition | Unregistered source | Contains two same-day counts, from creation and closure dates. The ticket descriptor names a different file, so ordinary activation does not select this implementation. |
| `last_knowledgerecord` | `KnowledgeManagement:205` (manual placement) | Knowledge record read | Positive-status knowledge records by creation date and ID descending. External viewer is restricted to records belonging to their party. |
| `last_modified_knowledgerecord` | `KnowledgeManagement:209` (manual placement) | Knowledge record read | Same entity, party and status tests as recent knowledge records. Uses modification time then ID, surfacing revised older articles. |
| `birthdays_members` | `Adherent:196` | Internal membership read | Validated members with birthdays in the current month, ordered by day of month, including dates earlier this month. |
| `members_last_modified` | `Adherent:197` (manual placement) | Membership read | Member and extension modification timestamps determine the descending sort. Joins the member type and applies the member entity set. |
| `members_last_subscriptions` | `Adherent:198` (manual placement) | Membership read | Joined member, type and subscription records ordered by subscription modification time, irrespective of the subscription start. |
| `members_subscriptions_by_year` | `Adherent:199` (manual placement) | Membership read | Group subscription records by the calendar year of their start date. Report count, sum and average, newest years first. Display at most eight year rows before the ellipsis. |
| `members_by_type` | `Adherent:200` (manual placement) | Membership read | Active member types with counts of draft, pending, current, expired, excluded and terminated members. Optional lookback filters on subscription expiry. |
| `members_by_tags` | `Adherent:201` (manual placement) | Membership read and categories enabled | Status counts by assigned top-level tag. A member can occur in more than one group. The grand total sums the tag groups. |
