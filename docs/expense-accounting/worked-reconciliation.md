# Reconcile a two-line claim through settlement

Claim `E-41` belongs to one employee in one entity. The subsidiary is `EMP-17`, the configured employee liability is `2200`, and the input VAT account is `1400`. The following example uses one currency, separate VAT accounting, open periods and illustrative account numbers and tax rates. All figures are monetary units.

| Detail | Calculation from receipt | Net | VAT | Gross | Initial binding |
| --- | --- | ---: | ---: | ---: | --- |
| Lodging | Two inclusive units at 57.50, 15% tax | 100.00 | 15.00 | 115.00 | Account `6100` |
| Transport | One inclusive unit at 46.00, 15% tax | 40.00 | 6.00 | 46.00 | `0`, pending |
| **Claim** | | **140.00** | **21.00** | **161.00** | |

1. The employee submits the claim. A visible submitted claim can be approved by a user with approval authority. At approval the state becomes `5`. No claim-payment or bookkeeping row is created by this decision.
2. The pending assignment list shows transport. Lodging admits the claim to journal selection. The second pass finds nonzero transport gross with a zero binding, so the attempted transfer leaves zero booked rows. The draft CSV can nevertheless display lodging expense 100, VAT 15 and gross 115.
3. Bind transport to account `6200` and run the same period. The two detail rows now produce one piece with the following four ledger rows. Both receipt IDs remain available through the parent, even though each booked row stores a single detail ID.

| General account | Subsidiary | Debit | Credit |
| --- | --- | ---: | ---: |
| `6100` lodging | | 100.00 | 0.00 |
| `6200` transport | | 40.00 | 0.00 |
| `1400` recoverable VAT | | 21.00 | 0.00 |
| `2200` employee control | `EMP-17` | 0.00 | 161.00 |
| **Totals** | | **161.00** | **161.00** |

4. Repeat the default transfer. The parent has existing ledger rows and is omitted. Reassigning transport to `6250` after transfer changes the line record. Its existing 40 debit remains on `6200`. Where an accounting reclassification is authorised, a separate balanced correction would debit `6250` 40 and credit `6200` 40. The assignment operation itself creates neither entry.
5. Record a bank reimbursement of 60. The payment register shows 60. Gross less the recorded payments is 101. When the bank journal is transferred for an ordinary outgoing reimbursement, it debits employee control 60 and credits bank 60. A second reimbursement of 101 clears the remaining operational balance. Transferring that second bank movement clears the remaining accounting liability too. Final expense is 140 and tax is 21. There are two payment events and only one original expense movement.

## Changes to one input

| Variation | Expected result |
| --- | --- |
| Inclusive expense policy, applied before first transfer | Debit lodging 115 and transport 46. Credit employee control 161. Separate recoverable tax is zero. |
| Bind both costs to `6100` | Separate-tax transfer yields one expense debit of 140, one input VAT debit of 21 and one liability credit of 161. |
| Negative transport adjustment of net −40 and VAT −6, lodged as the second line alongside positive lodging | Debit lodging 100. Credit transport 40. Debit input VAT 9. Credit employee control 69. Both sides total 109. |
| Add local tax of 3 to lodging, preserving VAT 15 and increasing lodging gross to 118 | Claim gross is 164. Split posting debits 140 in expenses, 21 VAT and 3 local tax and credits 164 to control. The draft CSV can show debits of 161 and credits of 164 because the local-tax row is absent from that format. |
| Replace transport's zero binding with a database null before first transfer | The line disappears from both the pending predicate and the transfer's unbound-line count. The lodged subset can post 115 gross against 100 expense and 15 VAT. The resulting piece balances but falls short of the claim by 46. Reconcile the claim gross to the booked control credit as well as balancing the piece. |
| The claim starts in period A and ends in period B | Selecting A finds the claim. With end-date posting enabled, the ledger tests B. If fiscal controls reject B the transaction rolls back. Selecting B simply because of the intended posting date can omit the original claim. |

## Portable reconciliation cases

The [expense claim transfer schema](../../schemas/finance/expense-claim-transfer.schema.json) describes an approved, positive claim with recoverable VAT and no existing movement in an open period. Each attempt captures every detail's binding at that point. `accountId` represents the saved chart ID and `accountNumber` its resolved general account. `committedEntries` contains the rows actually retained after that attempt. The examples use NAD and can be reconciled in any one currency under the same amounts and assumptions.

| Case | Expected accounting result |
| --- | --- |
| [Prepared after a blocked attempt](../../examples/finance/expense-claim-transfer--prepared.json) | An initial zero binding on the second detail blocks the entire 161.00 claim. Binding that detail produces debits of 161.00 and an employee-control credit of 161.00. |
| [Null binding on a nonzero detail](../../examples/finance/expense-claim-transfer--null-binding.json) | The same 161.00 claim enters through lodging. Transport has a null binding, its 46.00 gross fails to enter both the selected-line set and the zero-or-negative binding count, and a balanced movement of 115.00 is committed. The unrecognised employee liability is 46.00. |

For each case match one binding to each detail ID, sum all detail gross amounts and compare that sum with the declared claim gross. Select positive bindings for the journal amounts. A nonzero gross detail with a non-null nonpositive binding blocks the transfer. When it proceeds, group the selected costs by account, group VAT to the input account, and credit their gross to the employee control. Compare both journal sides to each other and independently compare the booked control credit to the full claim gross. JSON Schema checks field structure, binding representation, row directions and permitted outcomes. Reconciliation establishes cross-record arithmetic and identity.
