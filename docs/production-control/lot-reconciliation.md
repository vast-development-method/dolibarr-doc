# Tracing a job across stock and lots

A workshop records two input lots and three serialised outputs. The production rows establish that the lots and serials participated in the job. They do not assign an individual input lot to each individual output serial. A recall inquiry needs to know the difference between the set of possible affected serials and a demonstrated serial-level allocation.

## The evidence carried by each record

| Question | Selection and field relationship |
| --- | --- |
| Which requirements belong to this job? | Read `mrp_production` where `fk_mo` is the order and `role` is `toconsume` or `toproduce`. Retain each `rowid`, product, unit and quantity. Two occurrences of the same product can be independent requirements. |
| How much fulfilment remains on one planned line? | Sum signed `qty` for its matching actual role with `fk_mrp_production` equal to that plan's `rowid`. Check the order and product match when reconciling. A missing sum gives zero. A negative raw remainder identifies excess fulfilment. |
| Which warehouse changed? | The actual's `fk_stock_movement` references `stock_mouvement.rowid`. Read the signed `value`, `fk_entrepot`, `batch` and `datem` on that movement. An actual without a movement provides no physical change to add to stock. |
| What was the job's net warehouse effect after a correction? | Start from distinct journal rows with `origintype = 'mo'` and `fk_origin` equal to the order. Group by product, warehouse and batch. Include surviving original movements, compensations and new postings even if a prior actual was deleted. |
| What is on hand now? | Locate `product_stock` by `fk_product` and `fk_entrepot`. Its `reel` is the aggregate. A tracked item's `product_batch` rows join through `fk_product_stock` and hold `batch` and `qty` for that warehouse. These balances include receipts, shipments, transfers, counts and other jobs as well. |
| Which lot master supplies dates? | Join `product_lot` on **both** `fk_product` and `batch`. Its `eatby` and `sellby` are the lot dates. The same printed lot code can appear on a different product. |

The order's movement inquiry filters to warehouses in the permitted stock entities. It joins journal product and warehouse and can add user and lot details. When service stock is disabled, only physical products are selected. Month and year filters apply to movement time. Product reference, product label, warehouse, movement ID, lot, author, movement code, label, movement type and signed quantity further narrow the result. An order's simple movement count uses its two-part origin. A narrower list after applying warehouse, item or date criteria can legitimately differ from that count.

## Worked recall and correction

One job, order 70, plans six inserts, product 11, and three pump heads, product 22. Warehouse 1 initially has four inserts under lot X and four under lot Y. Warehouse 2 has no pump heads. There are no other movements in this fixture. The input plan is row 700 and the output plan is row 701.

| Step | Production actual or correction | Stock movement | Quantity remaining against the plan |
| --- | --- | --- | --- |
| Issue inserts from X | Actual 710, `consumed`, parent 700, quantity 4 | Movement 910, product 11, warehouse 1, X, −4 | 2 inserts |
| Issue inserts from Y | Actual 711, `consumed`, parent 700, quantity 2 | Movement 911, product 11, warehouse 1, Y, −2 | 0 inserts |
| Receive three separately numbered heads | Actuals 712, 713 and 714, each `produced`, parent 701, quantity 1 | Movements 912, 913, 914, product 22, warehouse 2, one each of S1, S2 and S3 | 0 heads |
| Remove the incorrect S3 output using its line and movement | Actual 714 is removed on a permitted correction | Movement 915 issues one S3 from warehouse 2. Original movement 914 remains. | 1 head |
| Post S4 as the actual third output on an eligible reopened job | Actual 715, `produced`, parent 701, quantity 1 | Movement 916, product 22, warehouse 2, S4, +1 | 0 heads |

After correction there are five surviving actuals and seven journal movements. The input balances are X zero and Y two. The output balances are S1, S2 and S4 one each, S3 zero. The zero-quantity warehouse lot rows can disappear while the journal still records S3 twice and the lot master can remain. A search restricted to the surviving actuals misses the history of S3. A search restricted to all journal entries without netting includes a serial that is no longer held. The order's actuals and movements supply no individual pairing of lot X to S1, S2 or S4. Recording such a pairing would require a separate issue-to-output allocation.

These queries express the two independent reconciliations using the dictionary's base table names. The order ID is fixed to the worked example. A deployed report must apply its normal order and warehouse access scope.

```sql
SELECT p.rowid AS plan_id, p.role, p.qty AS planned,
       COALESCE(SUM(a.qty), 0) AS posted,
       p.qty - COALESCE(SUM(a.qty), 0) AS remaining
FROM mrp_production AS p
LEFT JOIN mrp_production AS a
       ON a.fk_mrp_production = p.rowid
      AND a.fk_mo = p.fk_mo
      AND a.fk_product = p.fk_product
      AND ((p.role = 'toconsume' AND a.role = 'consumed')
        OR (p.role = 'toproduce' AND a.role = 'produced'))
WHERE p.fk_mo = 70 AND p.role IN ('toconsume', 'toproduce')
GROUP BY p.rowid, p.role, p.qty
ORDER BY p.rowid;
```

```sql
SELECT fk_product, fk_entrepot, batch,
       COUNT(*) AS movement_count, SUM(value) AS net_change
FROM stock_mouvement
WHERE origintype = 'mo' AND fk_origin = 70
GROUP BY fk_product, fk_entrepot, batch
ORDER BY fk_product, fk_entrepot, batch;
```

The first query returns planned/posted/remaining totals of 6/6/0 for row 700 and 3/3/0 for row 701. The second returns −4 for X, −2 for Y, +1 each for S1, S2 and S4, and zero across two movements for S3. Retain the zero result in an investigation. It distinguishes an originally reported serial that was corrected from one that never appeared on this job.

## Portable reconciliation output

The [reconciliation schema](../../schemas/operations/production-lot-reconciliation.schema.json) describes a read-only report for a single order. Build all four collections from the same consistent observation, under the viewer's permitted product and warehouse scope. A full-order reconciliation requires access to the full populations. Use the snapshot only for its visible scope when records are restricted. A plan or actual may exist without a warehouse change. Report a missing relationship as null. Record the plan's unit when known. Each product in the worked job is counted in individual units and has no explicit unit ID.

| Observation | Input and output plans | Surviving actuals | Distinct order movements | Serial evidence |
| --- | --- | ---: | ---: | --- |
| [After reversing S3](../../examples/operations/production-lot-reconciliation--partial-reversal.json) | Inputs 6/6 posted, outputs 2/3 posted, one head still required | 4 | 6 | S3 has two movements and net zero. Its earlier production actual has been removed. |
| [After receiving S4](../../examples/operations/production-lot-reconciliation--replacement.json) | Inputs 6/6 and outputs 3/3 posted, both remainders zero | 5 | 7 | S3 retains its two offsetting entries. S4 contributes one new receipt. |

The schema checks field presence, allowed roles, movement types and nullable links. The two queries above recompute these totals. Each plan's posted quantity equals the matching surviving actuals, and each warehouse group counts distinct movement identities and sums their signed quantities. The source movement identifies the order. The two S3 movements and the known correction explain the reversal in this example. The journal carries no dedicated link pairing movement 915 to movement 914. Movement totals give changes attributable to the order, and opening balances plus any unrelated movements are needed for physical stock on hand.
