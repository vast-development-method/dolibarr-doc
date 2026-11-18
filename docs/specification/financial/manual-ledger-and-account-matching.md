# Manual ledger movements and matching

A transfer from a sales journal can derive a balanced accounting movement from an invoice. An accountant can also build a movement directly, for example an accrued expense at period end. A movement groups its debit and credit rows under one number. Each row retains its account, side and amount. Matching records which posted rows explain one another after the movement has been created.

## Entering a movement

The record card requires movement-read access. Movement-create access authorizes creating a working movement, entering or changing its rows, and performing the promotion action. Individual line deletion on the editing card uses the create/edit permission. Deleting the whole posted movement uses the movement-delete permission. A user gaining entry access to the card therefore still has distinct editing and whole-movement deletion rights.

A working movement carries an entity, date, journal code and label, document reference and a temporary movement number. A row carries the general account and label, optional subsidiary account and label, operation narrative, debit, credit, direction and amount. Adding a row with a subsidiary account also checks that the selected general account permits auxiliary accounting. A nonzero debit and nonzero credit on one row are rejected. A missing account is rejected when submitting an amount-bearing line. The card can start with an empty working row while the operator completes the movement. An available transaction template can populate preset rows at creation.

| Month-end accrual | Debit | Credit |
| --- | ---: | ---: |
| Operating expense | 980.00 | 0.00 |
| Recoverable tax | 120.00 | 0.00 |
| Accrued payable | 0.00 | 1,100.00 |
| Movement total | 1,100.00 | 1,100.00 |

After the first two rows, the draft has a 1,100.00 debit imbalance. The card displays the discrepancy and enables normal validation only when the rounded movement totals are equal and nonzero. Correcting the last amount from 1,010.00 to 1,100.00 resolves a 90.00 difference without changing the first two rows. The normal action offered by the card and the underlying promotion routine are separate boundaries. The routine does not repeat the displayed sum comparison as a universal posting rule.

## From working number to permanent number

Promotion is one database transaction. It reads the draft date, journal and reference, allocates the next ledger movement number, and retains a supplied free reference or obtains a numbered one. It removes an entirely empty line with no account and zero on both sides. It copies account-bearing eligible lines into the ledger with the new movement number and creation time, then removes the working rows for that entity and temporary number. A checked database failure rolls back the promotion. The card follows the permanent number returned by the operation.

The period restriction used in the copy can filter which rows qualify. A movement should use the same effective date across its component rows so the journal remains balanced when promoted. Modification rules also distinguish the policy that blocks dates inside closed periods from the policy that requires a date within an active period. Under the latter, a missing period end allows later dates from its start. Read both the generated permanent number and its constituent rows when reconciling an interrupted operator action.

A posted ledger row also has a separate validation timestamp. A movement can exist in the ledger before final validation. The whole-movement delete action can remove matching when enabled, then checks its selected rows and refuses a validated posting. The receipt of a temporary movement number, permanent movement number and validation date describe three different milestones.

## Correction and reversal

To preserve the original and reverse its effect on another date, select posted rows belonging to the movement and create a return movement. The operation obtains the movement numbers from the selected line IDs and reads all lines in those movements. It swaps debit and credit on each line, reverses the direction, retains the account and available subsidiary information, and carries the original document attribution forward. The return operation uses the supplied reversal date and records the acting user. The original remains available for comparison.

Reversing the example on the first day of the next period credits expense 980.00 and recoverable tax 120.00, and debits the accrued payable 1,100.00. The net across the two periods is zero on each account. Each period still has its own balanced movement and transaction date. A later vendor bill is a separate trade document, and matching that bill to the accrual requires its own evidence.

## General-account matching

1. The operator selects posted accounting rows. Each selected general account must be marked reconcilable in the active chart. The routine determines the fiscal year using posted dates. It rejects a selection for which it finds no fiscal year or more than one fiscal year.
2. A complete match uses uppercase letters. A partial match uses lowercase letters. The configured code length defaults to three, with the first group beginning at AAA or aaa. Subsequent groups use the corresponding alphabetic sequence within the applicable account and year.
3. For a complete match, the routine compares the selected as-yet-unlettered totals of absolute debit and absolute credit after rounding to two decimal places. A mismatch prevents the operation. A partial match can identify related rows while a residual is open.
4. A partial operation skips rows already carrying a complete uppercase match. Completing a partially matched group can clear the earlier lowercase code before applying the complete code. The grouping and clearing queries in this path have different scopes, so an exported match code requires the account, entity and fiscal dates as context.
5. Matching records the code, match date and general-matching marker. A failure rolls back the matching write. Removing a general match first discovers the code, account and fiscal range of the selection, then clears group members in that scope. Selecting a single line from the group can therefore affect its partner rows.

For a reconcilable clearing account with a debit of 400.00 and credits of 150.00 and 250.00 in one fiscal year, all three rows can form one complete group. Selecting only the debit and the 150.00 credit permits partial matching and leaves 250.00 unresolved. Recording the first two rows as a partial group does not reduce the 400.00 debit or manufacture a new balancing row.

## Subsidiary-account matching

Automatic subsidiary matching builds connected groups from source documents, payment allocations, bank movements and accounting movement numbers. A payment covering two invoices can pull both invoices into the same group. The default line-discovery path uses rows with a subsidiary account, a positive source document ID and an accessible entity. The grouping then collects relevant document and bank entries. The receipt-to-invoice association supplies stronger evidence than matching two coincidentally equal amounts.

Within a candidate group, a credit contributes positively and a debit negatively to the residual. An existing code and the selected action determine whether the group can be processed. A nonzero residual prevents a new complete automatic match. When unmatching automatically, inconsistent codes within the group produce a mismatch. Groups are processed individually. Successful groups may already have changed even when another group reports an error.

Suppose two customer invoices debit the same customer account by 75.00 and 125.00. A posted bank receipt credits that customer by 200.00, allocated to both invoices. The grouped movement residual is zero and complete lettering is possible. If only 180.00 has been received, the 20.00 open balance prevents complete automatic matching. Bank statement reconciliation and the invoice payment allocations remain separate from the ledger lettering code.
