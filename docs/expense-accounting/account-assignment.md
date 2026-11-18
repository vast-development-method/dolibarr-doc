# Assign expense lines to the chart of accounts

The selected account is an integer ID in `expensereport_det.fk_code_ventilation`. The suggested number is text in `c_type_fees.accountancy_code`. The journal ultimately records `accounting_account.account_number`. A category code, a chart row ID and a posted account number are different identifiers.

## What appears in each view

| View | Row selection | Meaning of the displayed account |
| --- | --- | --- |
| Pending assignments | Join header `expensereport.rowid` to detail `fk_expensereport`. Use claims of the current accounting entity, status `5` approved or `6` closed, and `fk_code_ventilation <= 0`. Zero gross is eligible. | `fk_c_type_fees → c_type_fees.id`. Resolve the category's `accountancy_code` against `account_number`, chart version and current entity. The manual suggestion join has no additional active-account predicate. |
| Assigned lines | Same entity and two states, `fk_code_ventilation > 0`, with an inner join from this ID to the chart row. | The actual bound account. A stale positive ID that cannot join to an account is absent from this list. |
| One assignment | A detail ID, its parent in the accounting entity and a positive parent status. | Display the currently bound account beside the fee type and line description. |

Both lists filter by claim reference, employee login, fee label, line comments, net amount, account number, VAT rate and detail expense date. The pending register's line-ID search actually compares the **header** ID, even though it displays the detail ID. The assigned register compares the detail ID. A search by account number also changes meaning across these views, from the suggested number to the saved one. On opening the pending list without an explicit lower date, the configured binding start can supply the initial lower bound. Displaying the optional validation date does not change the detail-date filter. A database null is outside both numeric binding predicates. The detail column permits null and defaults to zero, so imports that intend to leave a line available for preparation should store zero.

## What the accounting operator can change

An internal user requires the accounting module and the `accounting.bind.write` grant to prepare claims or open the transfer. This differs from the employee's expense-entry right and from the claim approver's decision.

| Operation | Effect and outcome |
| --- | --- |
| Bind a selection from the pending list | Read the chosen chart ID individually for each checked detail. A missing or nonpositive choice produces a line-specific error. Each positive selection is saved separately. An unresolved line can remain even when the other choices succeeded. |
| Replace a selection from the assigned list | A single transaction updates the selected details to one chart ID. Zero removes their assignments. Negative input is rejected. |
| Save one line | Store the selected chart ID, converting a negative selection to zero. Cancel leaves the assignment untouched. |
| Clean invalid assignments | For this entity, clear nonzero assignments whose account ID is outside the selected chart and entity. This cleanup tests chart membership and leaves disabled accounts that still belong to the chart. It commits separately from automatic assignment. |
| Apply historical suggestions | After cleanup, scan approved and closed claims of this entity with nonpositive bindings. An optional month and year restrict the detail date. Match the fee code to an **active** account in the selected chart and entity. At most 10,000 returned rows are processed per pass. Save only if the detail is still unbound. Missing suggestions count as unresolved and do not prevent valid ones committing. A database failure rolls back this assignment pass. |

A category mapping change affects future suggestions. Editing the selected account changes the source detail and the journal preview for a pending claim. Posted rows retain the account number, label and amount captured at transfer. A chart cleanup can therefore return a previously booked line to the pending-assignment view while the parent still counts as already in the ledger.
