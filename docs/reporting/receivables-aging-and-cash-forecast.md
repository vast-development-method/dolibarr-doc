# Aging open invoices and forecasting a bank balance

## A due-date distribution

The customer and supplier invoice lists expose inclusive lower and upper bounds on invoice **due date**, a status selection and the remaining amount on each invoice. These controls support a current receivables or payables aging analysis. Band widths and the cutoff are report choices. These lists do not assign invoices automatically to a fixed set of aging columns.

For a distribution at the close of day D, select eligible open invoices and use calendar-day differences in one reporting timezone. The following non-overlapping bands are one way to express the two available due-date bounds.

| Band chosen by the reader | Inclusive due dates |
| --- | --- |
| Future due | After D |
| Due today | D |
| 1–30 days overdue | D minus 30 through D minus 1 |
| 31–60 days overdue | D minus 60 through D minus 31 |
| 61–90 days overdue | D minus 90 through D minus 61 |
| Over 90 days overdue | On or before D minus 91 |

An invoice exactly 30 days late belongs in the first overdue band. Its unpaid balance belongs there once even if it has several payments. An invoice with no due date does not satisfy either date bound. Keep such invoices identifiable separately when reconciling to all currently open items. The list's “late” option applies a different rule, comparing the due timestamp with now **minus the configured customer or supplier warning delay**. Combining that option with explicit bands can hide invoices only recently overdue.

On the customer list, the current gross balance subtracts payment allocations, credits applied and deposits applied. The invoice-currency balance is calculated separately from its own currency allocations. Closed invoices report a zero ordinary residual. A closed/paid credit note can instead display its remaining available discount as a negative balance. Supplier list processing also distinguishes ordinary remaining payment from unused credit-note balances. Decide whether the distribution is for open debit invoices or for a party's net position including credits. Grouping original gross amounts would overstate a partly settled exposure.

For example, assume a current customer invoice due 45 days earlier has gross 600, allocated payments 200, a deposit applied of 50 and credit applied of 25. Its 31–60-day balance is 325. An open second invoice due today at gross 90 with no settlement contributes 90 to due today. A third invoice already closed through full settlement contributes zero even if its due date is older. If a customer pays 100 tomorrow, rerunning the same due-date filters will show 225 on the first invoice. The due-date filters do not restrict allocations to those known on an earlier cutoff. A historical month-end aging requires balances or dated settlement activity at that earlier time. Filtering today's list by last month's due dates cannot reconstruct it.

## Planned bank transactions

The selected account's planned-transactions view combines obligations from five families into one timeline ordered by due date. It starts from the sum of all bank-line amounts already recorded against that account. Its opening-balance call includes pre-entered transactions with future operation dates. It then applies the signed remaining amount of each qualifying obligation. Zero remainders are omitted from display. A document without a due date can appear with its date marked undefined.

| Family | Expected date | Signed change to projected balance |
| --- | --- | --- |
| Customer invoices | Invoice due date | Validated, unpaid gross amount less allocated payments, deposits used and credits used. Positive receivables increase the balance. |
| Supplier invoices | Invoice due date | Start with negative gross and add payments already made. This forecast path fetches supplier invoice payments only, so applied supplier credits or deposits are handled differently from the supplier open-bills measure. A supplier credit whose stored gross is negative can increase projected cash. |
| Social contributions | Contribution due date | Negative obligation amount plus payments already made, for contributions marked unpaid. |
| Salaries | Salary period end | Negative salary amount plus salary payments already made, for salaries marked unpaid. |
| VAT payments | Recorded VAT date | Negative VAT obligation plus payments already made, for obligations marked unpaid. |

Customer invoices use their shared invoice entity scope. The other four built-in families select records in the current entity. Each includes documents assigned to the selected bank account and unassigned documents. The VAT selection also treats the negative unassigned-account sentinel as eligible. An unassigned payable can therefore appear on several account forecasts. Adding together per-account forecasts without identifying such rows would duplicate the same obligation. Each source reference opens its own document. Extensions may add transaction families or adjust a displayed remainder.

Starting at 1,000, a customer invoice due first with gross 660, 200 paid, 40 in applied deposits and 20 in applied credits contributes 400. A supplier invoice due next at 300 with 80 paid contributes minus 220. A salary balance of 100 due later reduces the projection to **1,080**. The rows show 1,400, 1,180 and 1,080 in chronological order. This projection assumes settlement of entered obligations on their recorded dates. The built-in sources supply no probabilities, sales pipeline, demand forecast or recurring cash amounts still awaiting document creation.

## Bank activity by category

The banking category report joins each bank transaction to its category assignments and groups by category identity and label in the active entity. The displayed total per category is the absolute value of the **signed sum**. The displayed mean is that absolute value divided by assignment count. It does not sum absolute transaction magnitudes. A category containing an inflow of 100 and outflow of 80 therefore shows total 20, count two and mean 10. Its footer adds absolute category subtotals and divides by total assignment count for the overall mean. A transaction tagged twice contributes to both categories, and an untagged transaction is outside this report. Clicking a category opens the bank entries for it. The category aggregation has no period or projected-obligation predicate.
