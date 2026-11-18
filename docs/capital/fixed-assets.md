# Fixed assets, depreciation and disposal

An asset links an acquisition to its schedule of depreciation, the ledger entries derived from that schedule, and any eventual disposal. In 24.0.3 the descriptor declares the module stable. The wiki provides the operator terminology but its instruction to enable development mode predates the pinned descriptor. [Asset descriptor](../reference/locators/capital.md#ref-a4100dd92778) · [Operator guide](../reference/locators/capital.md#ref-75a7035cf2d1)

## Records and ownership

| Record | Fields and relationship | Meaning |
| --- | --- | --- |
| Asset | Entity, reference, label, optional model, quantity, acquisition and in-service dates, price excluding tax, recovered VAT, opening depreciation and date, state | The asset owns its schedule. A missing in-service date at creation defaults to its acquisition date. An optional supplier invoice is linked through the document relation table. |
| Asset model | Accounting codes and per-mode depreciation options | Values are copied to the individual asset when a model is applied. A change to the asset's model can replace those settings. |
| Depreciation option | Asset or model owner, economic or accelerated mode, base, duration and unit, method and conditional coefficient | Economic is the primary mode. The accelerated block is exposed by an economic-mode option. The standard form offers annual or monthly periods. |
| Depreciation line | Asset, mode, period reference, effective date, amount, cumulative amount and debit/credit accounts | An empty period reference identifies an opening line. A ledger entry of document type `asset` points to a posted depreciation line through its detail ID. |
| Disposal | Disposed date, amount excluding tax, reason/type, flags for depreciation in the disposal period and taxation, optional customer invoice link | The disposal is recorded on the existing asset. The two invoice links represent different business events. |

Sources: [Asset record](../reference/locators/capital.md#ref-3dfc9266f859) · [Creation and model copy](../reference/locators/capital.md#ref-d6260217968d) · [Model options and accounts](../reference/locators/capital.md#ref-5a6a02a81824) · [Mode fields](../reference/locators/capital.md#ref-2b825aff398d)

## Operations and effects

| Operation | Operator and precondition at the card | Result and failure boundary |
| --- | --- | --- |
| Create and validate | Internal user with asset write access. The card offers validation on a draft (0). | Assign a final reference if empty or provisional. Set validated (1), validator and timestamp and raise `ASSET_VALIDATE`. A negative trigger result rolls back the database change. Revalidation of an already validated record returns no change. |
| Recalculate a schedule | Known asset and configured options. The options screen excludes assets marked non-depreciable. | Load mode settings and ledger accounts. For each retained mode, continue from the latest posted cumulative amount or the opening amount. Remove unposted projections for that mode, keeping opening rows when posted history exists. Replace projections in one database transaction. The calculator returns immediately for a non-depreciable asset. |
| Dispose | The card offers disposal on a validated asset to a user with write access. Supply date, type, proceeds and the two flags. | Update disposal fields, optionally link a customer invoice, set disposed (9), emit `ASSET_DISPOSED`, and recalculate. A negative result from update, state change or recalculation rolls back. Repeat disposal returns no change. |
| Reopen | Disposed asset and write access | Clear disposal date, amount, type and flags, remove the customer invoice relation(s), restore validated state, emit `ASSET_REOPEN` and recalculate. This operation does not issue a credit note or reverse an accounting journal. |
| Return to draft or delete | The card exposes return to draft on a validated asset. Delete is available with delete access or with write access on a draft. | Return to draft uses `ASSET_UNVALIDATE`. Carry document identity, state, permissions and accounting references separately in an implementation. |

Sources: [Card permissions and actions](../reference/locators/capital.md#ref-dc746aba4f5d) · [Card states](../reference/locators/capital.md#ref-18c17dcc3fad) · [Validation](../reference/locators/capital.md#ref-53c489408285) · [Disposal and reopening](../reference/locators/capital.md#ref-1d88f6bf413d)

## Reproducing the schedule

1. Start at the later of acquisition and entry into service. The planned end is start plus the configured duration minus one day. In monthly mode use calendar month ends. Annual mode uses fiscal periods and looks for the next fiscal year before assuming another twelve-month period.
2. Subtract the opening depreciation amount from the configured depreciation base. Divide by the number of periods and round to monetary-total precision. When a prior ledger posting exists in that mode, use the latest posted date and cumulative amount to locate the continuation. An opening date without a nonzero opening amount raises an error on the opening-line path.
3. In a partial monthly period multiply the periodic amount by the inclusive day count capped at the configured month length, then divide by that length. The default is 30. In February, a count of at least 28 becomes 30. In annual mode the normal denominator is 360 by default. Use actual days on the shortened/extended fiscal-year branches. An optional setting rounds intermediate amounts upward to an integer. On the period containing the planned end, use base minus cumulative to absorb rounding.
4. If disposal falls in a period and its depreciation flag is off, stop before inserting that period. If on, use the disposal date to calculate eligible days. The generated row carries the period-end date. A declining-balance coefficient and method choices appear in setup, but the pinned schedule loop calculates the periodic amount from base and duration. A rebuild claiming a distinct reducing-balance or exceptional formula needs separate evidence.

[Calculation and posted-row handling](../reference/locators/capital.md#ref-e84e3fec9a0d) · [Proration, rounding and next fiscal year](../reference/locators/capital.md#ref-352a9f257240)

**Worked case.** Set the acquisition and in-service dates to 1 January 2026, the economic base to 1,000.00, monthly duration to three, opening depreciation to zero, and monetary precision to two decimals. The January, February and March amounts are 333.33, 333.33 and 333.34. Their cumulative amounts are 333.33, 666.66 and 1,000.00. If only January is posted, recalculation in the same mode preserves its source line ID. In a separate run, disposal on 15 February with disposal-period depreciation disabled leaves only January's charge. [Positive schedule example](../../examples/capital/asset-schedule--quarter.json) · [Projection schema](../../schemas/capital/asset-schedule.schema.json)

## Ledger handoff and acceptance

The journal reader selects eligible entity records with status greater than zero, a nonempty depreciation reference and the requested posted/unposted state. A pair of date limits and the configured accounting binding start date further restrict candidates. General-journal asset transfer can be disabled. For a depreciation amount of 333.33, the configured expense account receives a debit and accumulated depreciation a credit of 333.33. An asset still in draft contributes no candidate rows. [Journal routing and selection](../reference/locators/capital.md#ref-b61900cac5c2) · [Line eligibility and accounting sides](../reference/locators/capital.md#ref-378071aed90a)

For an eligible disposal with acquisition value 1,000.00, cumulative depreciation 333.33 and proceeds 500.00 excluding tax, the first journal block debits the carrying-value expense 666.67 and accumulated depreciation 333.33 and credits the asset 1,000.00. With tax enabled and a configured 15% rate, the second debits receivable 575.00, credits proceeds 500.00 and credits collected tax 75.00. With the tax flag off the receivable equals proceeds. This is a software configuration example. The journal falls back to 20 when the configured integer disposal VAT rate is nonpositive. A consumer reconciling disposal should also examine any linked sales invoice for the same transaction. [Disposal calculations](../reference/locators/capital.md#ref-6a1e3659ac10)

The portable schema describes an economic schedule projection. Consumers verify that cumulative values equal prior cumulative plus the current amount and that dates are strictly increasing within a mode. These are business assertions across rows. The schema checks field shapes, modes, dates and decimal representations.
