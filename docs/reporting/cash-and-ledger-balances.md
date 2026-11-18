# Cash movements and trial balances

## Bank balance and cash flow

The bank graph starts from bank transaction lines joined to accounts in the permitted bank-account entities. It uses the **value date** on each bank line. The bank account access boundary applies at entry. The queries can restrict results to selected accounts or combine all accounts in scope. They sum the recorded bank amounts directly. The queries contain no currency conversion step for a mixed-account selection.

For a monthly balance the opening amount is the sum of all bank-line amounts dated before the first day. For each day the graph adds the day's signed movements to the running total. A day without movement carries the previous balance forward. The upper date bound for collecting a month's movements is the first day of the next month, exclusive. The monthly chart leaves future-day points blank and can plot the account's minimum desired and allowed levels alongside actual balances. The yearly balance follows the same approach from January 1.

The inflow and outflow charts split bank lines by amount sign before grouping them. A monthly detail groups by day, and the yearly cash-flow view groups by month. A debit and credit that net to zero can still create substantial inflow and outflow bars. These charts include the bank entries themselves regardless of whether they have been reconciled to a statement. A payment allocation awaiting its bank posting and an unpaid invoice do not enter the bank-line population.

Suppose the closing balance on April 30 is 800. Two value-dated lines on May 3, plus 150 and minus 40, produce a daily net change of 110 and a closing balance of 910. May 4 also shows 910 if there is no movement. A supplier invoice booked on May 4 does not reduce this balance until the corresponding bank line's value date. For reconciliation, inspect the bank account's transactions on the date used by the chart. Using invoice issue date or payment creation date can assign the same cash event to a different month.

## General and subsidiary trial balances

The trial balance starts from recorded bookkeeping entries in the active accounting entity. It groups by general ledger account and sums the debit and credit columns separately. The subsidiary-account version excludes lines with a missing or empty auxiliary account and groups by general account, auxiliary account code and auxiliary label. The same subsidiary code occurring under two control accounts therefore produces two groups. The same code under one account but with two stored labels can also create two groups.

The period applies to bookkeeping **document date**, inclusive of the selected endpoints. Without an explicit filter the screen chooses a fiscal period or falls back to configured fiscal-year dates. Journal, account range and matching/reconciliation filters can narrow the selection. Drill-down on a general account opens entries for that account. The subsidiary view opens the auxiliary account range.

| Displayed amount | Computation |
| --- | --- |
| Period debit | Sum of debit entries matching the entity, selected dates and filters. |
| Period credit | Sum of credit entries under the same conditions. |
| Period balance | Period debit minus period credit. A credit balance appears negative on this signed basis. |
| Optional opening | All prior debit less credit for the general account in the same entity, strictly before the selected period start. This query groups only by general account. |
| Closing with opening enabled | Optional opening plus the displayed period debit less displayed period credit. |

For a general account with prior debits 600 and credits 250, an opening of 350, period debit 120 and credit 80 give a closing figure of 390. A journal filter can narrow those period columns without narrowing the opening query. That query also makes no distinction between ordinary postings and opening-journal entries. In subsidiary mode the opening lookup remains keyed by general account. It therefore cannot supply a distinct pre-period balance for each subsidiary and may repeat the same opening across rows. An account without a movement matching the period selection need not have a row even if a pre-period balance exists.

The ledger balance and the cash graph can legitimately diverge. A bank transaction is grouped by value date in one projection. The corresponding bookkeeping line belongs to its ledger account, posting document date and accounting entity in the other. Reconciliation requires the actual journal entries and bank lines for the same account and cutoff.
