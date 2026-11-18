# Reconciling dashboard figures

## Unpaid invoices, exposure and cash

Consider an open customer invoice for 100 before tax and 120 including tax. The customer has already paid 20 and applied a credit of 10. The due date is next week. Before any other record changes, three screens can legitimately give different answers.

| Measure | Contribution from this invoice | Reason |
| --- | --- | --- |
| Oldest unpaid invoice shortlist | 100, if its due date ranks within the visible rows | The shortlist selects validated unpaid headers and displays original value before tax. A future due date still qualifies. The payment allocation changes the status indicator. |
| Unpaid invoice work queue | One to do, zero late, 100 toward the monetary total, assuming the ordinary nonnegative warning delay | The workboard adds header face value before tax. A partial settlement does not change that value. |
| Credit limit reached | 90 toward this customer's open exposure | The party helper takes 120 less 20 paid and 10 credited. It also deducts deposits used. A customer with a limit of exactly 90 qualifies. |
| Bank account widget | Only the posted bank movements affect the corresponding account balance | The credit application and the open invoice balance are not bank movements. Currencies are totaled independently over the displayed accounts. |

The customer and supplier oldest-unpaid shortlists fetch one more row than the visible limit to detect overflow. Their total queries reuse the customer/supplier payment allocation join and sum header value before tax without first collapsing allocations per invoice. With one 100 net invoice and two allocation rows, the shortlist row remains 100 and the footer can show 200. This is independent of how much remains due. The credit-limit widget scans its candidates and compares the separately calculated open amount. Its output can contain more customers than the ordinary shortlist limit.

Sources include `htdocs/core/boxes/box_factures_imp.php:95–133, 201–236`, `htdocs/core/boxes/box_factures_fourn_imp.php:93–115, 185–220`, `htdocs/core/boxes/box_customers_outstanding_bill_reached.php:89–149`, `htdocs/societe/class/societe.class.php:5436–5510` and `htdocs/core/boxes/box_comptes.php:89–157`. For the aging basis see [receivables aging and cash forecast](../reporting/receivables-aging-and-cash-forecast.md).

## Month, year and item frequency

Commercial comparison charts default to three years ending in the selected year, or the current year when no selection exists. They can display document count and tax-exclusive amount. Calendar months are the default. When fiscal graph mode is selected the configured fiscal starting month determines the series. Ordinary chart loads permit cached statistics for one day. Refresh bypasses that cached result and can write a new one.

| Series | Date axis | State and aggregation |
| --- | --- | --- |
| Customer and supplier invoices | Invoice date | Widget replaces the statistics provider’s selection predicate with allowed invoice entities and positive status. Default provider type or replaced-document exclusions do not survive that replacement. Its monthly methods still apply their restricted internal salesperson joins. |
| Customer and supplier orders | Order date | Order headers are counted once per qualifying row. Default criteria include drafts as well as subsequent states. A month can contain planned business that never reaches shipment. |
| Customer proposals | Proposal date | Monthly count and net header value for the proposal population, including drafts. A later signature does not transfer its value into the month of signature. |
| Distribution by item | Calendar year of the commercial document | The provider groups matched catalogue reference occurrences on document lines, sorted by count. A free-text line has no matching item reference. The selected top N appear individually and any remaining occurrences form an Other group. |

If one order contains 100 units of item A on a single line and two occurrences of item B on separate lines, the item-frequency chart gives A one occurrence and B two. The order chart counts one order. If that draft is cancelled without dispatch, adding its quantities to a shipment report would produce a different population again.

Two display settings explain other common differences. The latest-record widgets can use their document date instead of modification time. An invoice edited today with a document date last year can lead the first view and be absent from the other. The optional rolling commercial activity widget uses tax-inclusive amounts and a three-month interval by default. Its invoice components split by the paid flag. The unpaid component filters on invoice entities and date, while the paid component also applies the viewer’s party or salesperson restriction. Comparing these two populations as a settlement rate can give a misleading result.

Sources include `htdocs/core/boxes/box_graph_invoices_permonth.php:73–142, 182`, `htdocs/core/boxes/box_graph_invoices_supplier_permonth.php:71–139`, `htdocs/commande/class/commandestats.class.php:111–145, 161–178`, `htdocs/comm/propal/class/propalestats.class.php:94–125, 145–162`, `htdocs/compta/facture/class/facturestats.class.php:87–129, 151–163, 201–214, 273–290`, `htdocs/core/class/stats.class.php:338–390, 664–691` and `htdocs/core/boxes/box_activity.php:78–125, 280–296, 361–370`.

## Stage, status and scope

| Case | Expected result |
| --- | --- |
| A support team has two active tickets, one cancelled and one closed-solved, all with an active severity code. | The severity chart counts three because it excludes only solved status 8. The home open-ticket queue counts two because it also excludes cancelled status 9. The recent-ticket list can display all four. |
| A ticket was created in the current seven-day chart’s earliest displayed day. | The intake widget compares the database date strictly with a timestamp six days before now. That first day's creations can fall outside the query while the display still pads the day with zero. The graph aggregates by ticket entity. The recent-ticket lists additionally constrain an external user to their party. |
| A knowledge article is cancelled after publication. | The two recent-knowledge lists test positive status. Both validated status 1 and cancelled status 9 satisfy that predicate. The modification list can place the article first following its status change. |
| A project with an opportunity stage is still in draft. | The recent-opportunity shortlist accepts draft and open opportunity-use projects. The funnel only aggregates open projects with active nonterminal stages. The shortlist can use the authorized-project list. The funnel's grouping query works across the project entity set. |
| Two open opportunities have amounts 1,000 and 500 with stored probabilities 40% and 80%. | The pipeline face value is 1,500 and its weighted value is 800. If cumulative mode is enabled, a chart stage can include downstream stage amounts. Adding those cumulative bars can count one project multiple times. |
| An active stock item has an alert level of 10, physical stock of 7 and a purchase order for 8. | The low-stock widget still includes it because it sums physical stock only. The replenishment proposal can use incoming supply when calculating the purchase quantity. At physical stock 10 the strict alert comparison removes the item. |
| A member in two top-level tags has current coverage. | Each corresponding tag row counts that member. Aging of coverage depends on the member's subscription requirement and expiry, while annual subscription income groups transactions by their subscription start year. |
| A sent purchase order lacks an expected delivery date. | The home workload includes it in orders awaiting receipt and leaves it out of the late subset. The configurable awaiting-receipt shortlist requires a date and omits it. Adding a date in the past beyond the warning interval can put it in both the shortlist and the late subset. |

Sources include `htdocs/ticket/class/ticket.class.php:259–260, 3393–3452`, `htdocs/core/boxes/box_graph_nb_ticket_last_x_days.php:87–139`, `htdocs/core/boxes/box_graph_ticket_by_severity.php:97–102, 135–156`, `htdocs/knowledgemanagement/class/knowledgerecord.class.php:57–59`, `htdocs/core/boxes/box_funnel_of_prospection.php:145–154, 165–189, 210–229`, `htdocs/core/boxes/box_project_opportunities.php:91–114`, `htdocs/core/boxes/box_produits_alerte_stock.php:81–107`, `htdocs/adherents/class/adherentstats.class.php:194–223, 267–300` and `htdocs/core/boxes/box_supplier_orders_awaiting_reception.php:88–103`. See also [operational dashboards and replenishment](../reporting/operational-dashboards-and-replenishment.md).
