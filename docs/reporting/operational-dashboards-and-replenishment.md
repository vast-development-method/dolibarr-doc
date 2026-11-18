# Operational dashboards and replenishment

## Products to replenish

The replenishment screen starts with catalogue items available to buy. A supplier filter requires an in-scope supplier price for that product and supplier. Product type, warehouse, stock status and threshold controls further narrow the candidates. With warehouse thresholds enabled, the list can use the warehouse's desired or alert level with fallback to the product-level value when the local value is null. The page's shortage calculation then displays product-wide and warehouse-specific quantities as separate measures.

| Measure | Definition |
| --- | --- |
| Inventory target | The greater of desired stock and alert stock. A warning flag is shown when a nonzero alert threshold exceeds the selected current stock. |
| Open supply shown | Selected supplier-order quantity less received quantity for the item. In physical mode the normal order statuses included are validated, approved, sent and partially received. The draft option can add draft orders. Received quantity is taken for partially received orders in this comparison. |
| Buy quantity, physical mode | The greater of zero and target minus physical quantity minus open supply. Open supply can cover today's low stock without removing today's low-stock warning. |
| Buy quantity, virtual mode | The greater of zero and target minus theoretical stock. Outstanding supply is already reflected in theoretical stock under its configured policy. A second deduction of open supply would understate need. |
| Warehouse buy quantity | Use the local desired and alert thresholds and warehouse real or virtual quantity. In physical mode this expression subtracts the same product-wide open-supply figure used in the product calculation. A specific inbound purchase cannot be assumed destined for each warehouse independently. |

For a target of 20, alert of 10, current physical stock of 6 and outstanding supplier quantity of 8, the screen predicts a need for 6. The low-stock warning is still appropriate because 6 on hand is below 10. With virtual stock of 14, the virtual projection also suggests 6. If a customer order reduces theoretical stock to 11, virtual need becomes 9. A product's proposed purchase line offers a supplier-price selection. The displayed need is a planning quantity and does not in itself authorize a purchase.

## Contracts and service coverage

The contract service overview counts **contract lines**. It uses current time and each service line's lifecycle. Activated services remain running when their end date is missing or at least the current instant. An activated service with an earlier end date is expired. A closed service is classified by its closed status independently of that same date comparison. Initial services are awaiting activation. One contract with three services can contribute to three separate status buckets.

Per-contract figures on the recently modified list distinguish initial, running, expired, late and closed service counts. Late is a subset of expired when the end is earlier than now minus the configured expiry warning delay. Adding the late count to all the expired services double-counts that subset. At exact equality with the warning threshold, an expired service has not yet entered the strictly late subset. The service graphs restrict by permitted contract entities and the viewer's party or sales representative where required. The inactive-services list identifies outstanding activations on validated contracts. The expired-services list leads to activated service lines ending before now on validated contracts.

## Ticket queues and membership continuity

The ticket status graph groups ticket headers by **current status** after selecting tickets created in the requested year. It counts unread, read, awaiting additional information, assigned, in progress, waiting, closed and cancelled states. A ticket opened in December and closed the following January appears in the prior year's closed group on a later run. This graph does not estimate time spent in a status or the count of closure events in the selected year.

Tickets must be in the permitted ticket entities. Commercial visibility can restrict by assigned customer, and an external viewer sees their own party. For an internal viewer the assigned-only option can restrict scope to their own tickets unless they have management permission. The newest-unread list separately selects current unread records, sorts newest creation first and limits the number displayed. Its link opens the unread ticket list. The yearly graph and limited current queue need different date and display-limit conditions when reconciling.

The membership dashboard groups member records by membership type and classifies them at the time of the report. Draft, excluded and terminated follow the member state. For validated members whose type requires subscriptions, no expiry means awaiting subscription, expiry at or after now means current, and a past expiry means expired. If the type does not require subscriptions, a validated member counts as current regardless of the expiry. The optional lookback restricts the joined members to those whose expiry is later than the first day of the calculated starting year. A null expiry then fails the lookback and a paid-up category may change population even for a type that otherwise requires no renewal. A separate by-tag measure groups top-level tag assignments and can count a member under multiple tags. Its sum across tags is consequently a count of memberships in those tags.

## Oldest unpaid customer invoices

The collection widget selects unpaid customer invoices in validated status and allowed invoice entities. It applies the viewer's customer or sales-representative scope when required. It sorts headers by due date, earliest first, and uses the invoice reference to break ties. The query has no past-due-only condition. A future-due invoice can appear if it falls among the oldest currently unpaid. A partly paid invoice remains a candidate. The joined payment allocations supply a paid amount for the status display. The maximum number of rows controls the visible shortlist, and the full-list link opens the validated invoice list sorted by due date.

The widget footer, when shown, sums **invoice net amounts** across the qualifying joined population. It does not subtract settlements, deposits or applied credits, and it reuses the payment-allocation join without grouping by invoice. Two payment allocations can therefore repeat the same invoice's net total in the footer. For collection exposure the party's open-bills projection calculates remaining gross per invoice after settlements and applications. A partial payment can change that balance without removing the invoice from the shortlist.
