# Membership subscription register

A treasurer can use this register to answer “which periods began this month, for whom, and at what charge?” Each row represents one subscription. The same member can appear more than once. Comparing a register amount with bank receipts, open invoices or ledger income requires the separate financial records generated when the period was created. [Renewal and receipt choices](member-renewals-and-collections.md)

## Record identity and scope

| Relationship | Effect on the result |
| --- | --- |
| `subscription.fk_adherent → adherent.rowid` | This inner join supplies member details and the owning entity. A period has no entity column of its own. The query includes the member entities visible for this function. A member with no period contributes no row. |
| `subscription.fk_type` | Holds the type recorded for this period. Changing the member's current type leaves earlier periods available under their original type. |
| `subscription.fk_bank → bank.rowid → bank.fk_account` | A left join makes the bank account available for display and filtering. Periods with no direct bank line remain visible until an account filter is applied. |
| `adherent.rowid → adherent_extrafields.fk_object` | The optional-value join is on the member. The control definitions are read for the subscription. A deployment exposing a custom column on this register must reconcile the selected column with the joined extension table. |
| `subscription.rowid` | Identifies the period in its ordinary row link and in bulk-action selections. The stored unique key additionally covers `(fk_adherent, dateadh)`. A member can have overlapping periods with different starts. |

The register requires membership subscription access. The creation grant also controls the new-subscription and bulk deletion controls. Confirmed deletion goes through the subscription lifecycle, including handling its directly linked bank transaction. Member administrative status is fetched with the row. The built-in selection has no administrative-status predicate, even though the page carries a `statut` parameter. A terminated member's previous period therefore remains visible.

## Which fields a filter uses

Filters from different controls combine. The common text matcher accepts separate search terms, alternatives and anchored text. The amount control uses numeric comparisons.

| Control | Predicate or selection |
| --- | --- |
| Subscription reference `search_ref` | A supplied, nonempty numeric reference is converted to an integer and compared with `subscription.rowid`. A nonnumeric reference returns no rows. |
| Type `search_type` | A positive selection searches the stored period's `fk_type` through the shared text matcher. This call takes the default contains-match mode, so a text conversion of type 12 can also match a search for 2. |
| Last name, first name, login | `search_lastname` looks in both `adherent.lastname` and `adherent.societe`. `search_firstname` and `search_login` search their separate member fields. |
| Label and quick search | `search_note` searches `subscription.note`, the public label. The displayed label uses its first line. `search_all` examines subscription ID and public label. A member surname alone belongs in the surname control. |
| Bank account `search_account` | A positive choice compares the account ID on the linked bank movement. This does not inspect a bank account configured on an associated sales invoice. |
| Charge `search_amount` | Evaluates `subscription.subscription`. An expression such as `>=100 <150` applies both comparisons. A plain input string `0` is skipped by the outer truth test. `=0` reaches the numeric equality filter. |
| Year `date_select` | Uses the start date `dateadh` from the first day of the selected year inclusive to the first day of the following year exclusive. A period that began in December and continues into January belongs to the December start year. |
| Start-date range | `search_dateadh_start*` and `search_dateadh_end*` each accept year, month and day components. Valid bounds include the first instant of the lower day and the last second of the upper day. Both compare with `dateadh`. |
| Expiry range | `search_datef_start*` and `search_datef_end*` build the comparable inclusive bounds for `datef`. To find periods covering a given day, constrain start on or before that day and expiry on or after it. |

Extensions can add fields or narrow the selection. The standard joins include neither payment allocations nor bookkeeping. Creation time `datec` and last modification `tms` are optional display columns, independent of period start and end.

## Page totals and reconciliation

The operator list orders by descending start by default. It counts filtered join rows when full counts are enabled, then fetches a page plus one look-ahead row. The amount column in table mode accumulates only the displayed rows. A configured all-pages footer tries to sum a column called `d.amount` on the member alias. The standard member table has no such column. That optional calculation can consequently produce no grand-total row. For a full charge total, sum `subscription.subscription` across the filtered period IDs. The [collection service](../../services/subscriptions.md) uses ascending start by default, a zero-based page and a separate optional count.

| Period | Member and state today | Start | Expiry | Charge | Direct bank account |
| --- | --- | --- | --- | ---: | --- |
| 81 | Member 7, admitted | 15 December, prior year | 14 December, current year | 120 | Operating |
| 96 | Member 7, admitted | 1 March, current year | 30 June, current year | 40 | None |
| 109 | Member 18, terminated | 1 April, current year | 30 September, current year | 70 | Operating |

A current-year start filter selects 96 and 109, with charges of 110. At one row per page the first page shows 109 and 70, the second 96 and 40. Adding the Operating account selects only 109 and 70. Testing coverage on 15 April over both start years yields three periods, two distinct members and charges of 230. Member 7's greatest end remains 14 December. The second overlapping period increases the number of rows and the charges while leaving that paid-through date unchanged.
