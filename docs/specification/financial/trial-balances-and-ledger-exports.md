# Trial balances and ledger exports

## Read balances at the correct level

A general trial balance sums movement debits and credits separately by general account in the current accounting entity. Subsidiary mode requires a nonblank subsidiary account and groups by general account, subsidiary number **and subsidiary label**. The same party number carried under two general accounts yields two groups. A change in its stored label can also create separate groups. Unassigned rows still count toward the general account. The report takes its labels and amounts from the posted rows and account directory. It does not derive the totals from sales or payments a second time.

Analysts can filter by journal, document date, general or subsidiary account range or prefix, document or line identity and piece number. The unmatched option selects rows with a null lettering code. A partial match with an assigned code consequently falls outside this filter. The balance for the selected period is debit less credit. Each amount links to the corresponding account inquiry with the requested date bounds.

Suppose receivables has three posted movements. Customer A is debited 180 and credited 100. A final debit of 30 carries no subsidiary number. The general account shows 210 debit, 100 credit and a period balance of 110. The subsidiary report shows A with 180 debit, 100 credit and a balance of 80. The 30 difference is traceable to the unassigned movement.

An optional opening-balance display sums *all* debits less credits before the start date by general account. The displayed closing balance becomes opening plus period debit less period credit. This opening query has no journal, account-class or fiscal-start restriction. It can include historical opening entries alongside their originating movements. In subsidiary mode the same general-account opening is looked up for each displayed group. A general opening of 400 is therefore repeated on two subsidiary rows sharing that account. These figures cannot establish an independently calculated opening balance for either customer.

Consulting the balance requires movement-read permission. The list offers full result exports as a table or a formatted document. The export controls use the movement-export grant while the report-export action itself uses movement-read permission. These are distinct from the permission and bookkeeping timestamps of the movement export.

Release references include `htdocs/accountancy/class/bookkeeping.class.php:1353–1466` and `htdocs/accountancy/bookkeeping/balance.php:141–149,228–278,354–380,513–558,635–676`.

## Export movements for another accounting system

The interactive export requires the movement-export grant. Its selection uses the active movement filters and excludes previously exported rows unless re-export is enabled. The operation loads all matching rows even when the screen is paginated. The operator selects the exchange format, inclusion of available supporting files, whether to omit matching codes and dates from the output, and whether to mark exported movements as exported or validated. Omitting matching data leaves stored matches intact.

File generation runs before the transaction updates the selected movements. Marking export and marking validation are independent choices. Re-export permits timestamps to be refreshed. If generation fails or a requested movement update fails, the database changes roll back and the page returns an error. Download begins after commit. A client-side interruption after commit can therefore leave movements marked exported even if the user did not receive the complete file. The operator needs re-export capability to include such movements again.

The configurable delimited format writes, in order, piece number, document date, source reference, operation label, formatted general account, formatted subsidiary account, debit, credit, debit less credit and journal code. It uses the configured field separator, line ending and date format. A label containing the separator is surrounded by single quotation marks in this writer. The layout matters to receivers that expect standard double-quote escaping.

Release references include `htdocs/accountancy/bookkeeping/export.php:589–746` and `htdocs/accountancy/class/accountancyexport.class.php:245–261,1374–1405`.

## Accounting audit-file layout

The first audit-file writer emits a header and tab-separated rows with carriage-return and line-feed endings. It skips movements where debit and credit are both zero. The interactive export's status-marking loop processes the selected movements, so a zero-valued row can acquire an export timestamp while contributing no output row. Dates use eight digits in year, month, day order.

| Position | Content emitted |
| --- | --- |
| 1–4 | Journal code and label, numeric piece number and movement document date. |
| 5–8 | Formatted general account and label, formatted subsidiary account and label. |
| 9–11 | Document reference, movement creation date and operation label. Tab and newline characters in textual fields are replaced to preserve column boundaries. |
| 12–16 | Debit, credit, matching code, matching date and validation date. |
| 17–18 | Foreign amount and currency code when populated on the row supplied to the writer. The standard screen and service export reader omits these fields. [Audit-file currency and evidence](../../exports/audit-file-dates-and-currency.md) |
| 19–21 | Due date, invoice reference and representative invoice filename where found. The customer reference comes from the invoice; the supplier reference comes from the supplier's own reference. |

When source documents are included, the writer looks for the customer's generated invoice document or the most recent matching supplier-uploaded document. It skips the generated supplier printout in this search. A cached file association by piece number avoids adding the same attachment repeatedly. An unmatched file leaves the filename field empty. The format registry also exposes a second audit-file variant and specialized accounting-package layouts. Those writers have their own sequence, formatting and attachment rules.

Release references include `htdocs/accountancy/class/accountancyexport.class.php:144–199,495–558,1474–1697,1720–1765`.

## Service contract for a downloadable export

The export-data operation requires the same movement-export grant. Supported scopes include current or previous month, the previous three or six complete months, current or previous calendar year, current or previous fiscal year, current and previous fiscal years together, or custom bounds. Previous fiscal year is resolved from the day before the current fiscal period starts. A custom scope requires at least one supplied bound. Individually parseable bounds are applied inclusively to document date. Rows are ordered by ascending piece number followed by movement identifier.

The caller supplies a registered format number or a displayed format name. Omission selects the configurable format. Separate options include already-exported entries, include lettering and suppress recording the export time. By default the service stamps the movements it exports. It returns a document descriptor with module, relative path within accounting output, filename and media type. Retrieval of the bytes is a subsequent document operation. An unrecognized period or format gives a not-found outcome, lack of export rights gives a forbidden outcome, and generation or bookkeeping failure gives a server error.

The service updates timestamps and generates the file in one database transaction. It verifies the resulting file descriptor after commit. A descriptor failure at this last stage can therefore coincide with committed timestamps. Retrying the default selection need not reproduce the first file. Suppressing the export mark when deliberately producing a repeatable extract, or explicitly including previously exported rows, changes this outcome.

The release reference is `htdocs/accountancy/class/api_accountancy.class.php:83–292`.

## Closing balances, opening entries and stored snapshots

The fiscal-close service requires a source period with an end date and a target period starting strictly after it. In generation mode it joins the source period's movements to account numbers in the current entity's selected chart. It considers only the configured balance-sheet and income-statement groups. The signed measure here is **credit less debit**. A positive balance-sheet closing balance becomes an opening credit, a negative one an opening debit, and a zero balance is omitted. Optional subsidiary separation groups by subsidiary number after normalizing empty string to null. The label is looked up separately. The results use the target start date and retain the source period identity and label. A zero income-group result produces no profit or loss row.

For an account reclassified from an included to an excluded group in the selected chart before closing, the current classification determines whether it contributes. An account appearing in both configured groups follows the income-result branch. The balance-sheet amounts and income result are recomputed from the ledger when closing. Closing with entry generation disabled changes fiscal status without creating opening movements. Reopening from the fiscal-year card is available under the period-reopen option and updates the period status. That action does not remove opening movements from a previous closing run.

A separate installed balance-snapshot relation defines entity, fiscal year, general account number and label, optional subsidiary number and label, debit, credit, snapshot time and last-modification time. It declares a unique index over entity, year, general account and subsidiary number. The published balance inquiry and fiscal-close services above read ledger movements directly. No release operation was found that populates this snapshot relation or uses it to supply either result. A rebuild would need an additional business decision before treating snapshots as an automatic effect of closure.

Release references include `htdocs/accountancy/class/bookkeeping.class.php:3008–3277`, `htdocs/accountancy/admin/fiscalyear_card.php:176–189` and `htdocs/install/mysql/tables/llx_accounting_balance_snapshot-accounting.sql`, with its companion `llx_accounting_balance_snapshot-accounting.key.sql`.
