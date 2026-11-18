# Movement corrections, stocktake costs and transfer custody

A warehouse supervisor correcting a quantity can reverse a journal row, record a new adjustment, undo a transfer leg or post a count. Each operation identifies the goods differently. A journal movement explains an event. A lot position tells how much is currently available. A transfer document also records which side currently holds custody. A count records how much a person actually observed.

## Reversing selected journal movements

The stock movement list requires movement-creation authority for the confirmed reverse action. It selects the submitted movement IDs, loads each record, and processes the selection in a transaction. If a selected reversal fails, the list rolls back the group. The selection query does not specify row order or require like movement types. Selecting two rows with the same transfer code does not transform them into a transfer-document transition.

| Original movement type | Compensating type | New signed quantity |
| --- | --- | --- |
| Transfer or adjustment entry, 0 | Transfer or adjustment exit, 1 | Negative of original |
| Transfer or adjustment exit, 1 | Transfer or adjustment entry, 0 | Negative of original |
| Ordinary issue, 2 | Ordinary receipt, 3 | Negative of original |
| Ordinary receipt, 3 | Ordinary issue, 2 | Negative of original |

The compensating movement uses the product, warehouse and lot from the selected record. The writer uses the acting user, current movement time and unit price zero. It prefixes the original label and constructs a movement code from `REVERT-` plus the original code, falling back to the original movement timestamp when the original has no code. The source movement survives with its original quantity and price. The journal action makes no change to a linked supplier receipt, invoice, count or shipment header. A shared code can group several movements. The reversal method does not look up a previously written compensation by source movement ID. Selecting the same original again can produce another compensation if the normal stock rules permit it.

The movement method is invoked on the fetched original, so ordinary source and project context can flow into the writer through that object. Supplying zero unit price does not unwind a previously incorporated acquisition price. The [receipt cost calculation](receipt-cost-and-reversal.md) explains the special zero-price treatment for supplier-order and supplier-invoice origins. The new row does not reproduce the old posting date, actor, price or additional fields merely because it points back to the same commercial transaction.

A change of +5 and its later −5 net to zero in quantity. Their timestamps place them in two different period-end reports if the reversal occurred after cutoff. A receipt document that remains validated can still show five received against its order while the warehouse movement history nets to zero. Recover the document through its own correction path when the receiving status also needs to change.

## Posting a count while trade is in progress

A counted quantity, expected opening quantity and quantity at posting can all differ. The count reads the current quantity at posting, including the current lot position when tracking is enabled. It applies the counted quantity less this live comparison at stock precision. A missing current lot is compared with zero. An unobserved row is skipped. An explicit zero is a count. For a tracked row the live balance search is case-insensitive. The movement still passes the batch text from the count line to the stock writer. A differently cased identifier can therefore match the stocktake's comparison while the outgoing sufficiency decision uses its own string comparison. Use the stored identifier consistently when a negative adjustment must pass the latter decision.

For a nonzero difference the action writes an input-type correction when the count is larger, an output-type correction when smaller. It writes the returned movement ID to the count line and updates the stored comparison quantity if it changed. On an unchanged count the branch that writes this movement ID and comparison quantity is skipped. The action leaves an explanation of quantity changes in the movement journal. Count posting also has an independent cost branch when managing actual average cost is enabled. A supplied nonzero actual price on an observed row replaces the **whole product's** average. A zero price entry does not reset it to zero. Where product sharing and per-entity average cost are both enabled, the update also targets the current entity's existing price row. The option controlling shared accounting codes is independent.

**Worked two-lot count.** Location E starts with six units of lot A and four of lot B. While counting, a receipt adds two to B, taking its live comparison to six. The observer records A=5, B=6, with actual costs 11 on A and 14 on B, in that count-line ID order. A posts −1, B posts no quantity adjustment, and the product closes at 11 units. The final product average is 14 because the observed B row applies its nonzero cost after A. Valuation at the current average is 154. Multiplying A by 11 and B by 14 instead gives 139, a lot-specific valuation the count did not store. With the manual-cost option off, the A issue preserves the previous product average. If the observer left B blank, B's row would skip the observation branch and its cost would not overwrite A's.

The count wraps processing and recorded-status handling in a transaction. Movement and line-update failures are inspected. The final call to mark the count recorded does not inspect that operation's return before committing. A failure result or an interrupted response needs the count state, line movement IDs and physical quantities read together. A separately reversed count movement does not replace the count line's pointer to the original correction.

[Opening and posting a stocktake](../specification/operations/stocktake-and-transfer.md)

## Immediate transfer and transfer document

An immediate warehouse-to-warehouse transfer from the movement list uses the current product average as its source/destination unit price and submits both warehouse legs in the surrounding transaction. The source and destination must differ. For a tracked item, the action requires a lot. The lot-aware correction uses the selected batch and its dates. A failed leg rolls the pair back. Because the two calls belong to the same transfer action there is no normal in-transit interval between two posted business decisions.

A transfer document captures cost earlier. Draft line creation or editing stores the then-current product average. Departure and undo-arrival produce outgoing-type movements with price zero. Arrival and undo-departure produce incoming-type movements priced at the captured line average. The line writer resolves the batch dates when available. Applying the incoming leg can change the current product average if it diverged from the stored transfer cost while the goods were in transit.

**Worked delayed arrival.** Begin with 12 units at 10. A transfer line for four captures unit cost 10. Departure removes four, leaving eight units at 10. A supplier then delivers eight more at 14. The product now has 16 units at 12, worth 192 at current average. Arrival reintroduces the four in-transit units at the captured 10. The new whole-product average is `(16 × 12 + 4 × 10) / 20 = 11.60`. The ending warehouses together hold 20 units worth 232, equal to opening value 120 plus supplier acquisition 112. While goods were in transit, warehouse-only value omitted four units at 10. Undoing the arrival through its source transfer issues four and preserves 11.60. Undoing departure then receives four at 10. Reversing the two legs can restore physical custody without restoring the original price history.

The transfer card commits a leg's collection of movements before writing the header's new status and actual time. A subsequent header or event failure can leave upstream goods movement already committed. The header state, selected source/destination, lot, operation code and quantities together identify which part occurred. A movement-list reversal compensates quantities only; it does not change the transfer's in-transit status or its timestamps.
