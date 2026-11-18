# Ledger export formats and row contracts

A customer invoice can generate several posted ledger rows sharing a piece number. Payment generates another piece. An exporter decides which identifiers to preserve, whether a subsidiary account replaces the control account, and how to represent debit and credit. Two files can reconcile to the same journal total while having incompatible columns.

## Which rows leave the ERP

The interactive export requires the movement-export grant. Confirmation uses the current filters, sort order and entity scope, with no page limit. Already exported rows are normally excluded. The re-export option changes that population. The operator can omit lettering from the output without clearing it from the ledger. Export and validation dates on the selected rows have distinct controls. Downloading a previously generated file and generating another extract have different consequences. See [trial balances, exports and fiscal close](../specification/financial/trial-balances-and-ledger-exports.md) for the marking transaction and the service's period choices.

There are 21 named built-in formats. The registry gives each a numeric selector. An extension can add others. The table identifies the distinctive representation and a release-relative writer line in `htdocs/accountancy/class/accountancyexport.class.php`.

| ID | Format | Record representation | Writer line |
| ---: | --- | --- | ---: |
| 1 | Configurable | Ten ordered fields, independently configurable date, separator and line ending. Carries both sides and a signed difference. | 1374 |
| 10 | Agiris | Semicolon-separated with account number plus label, debit, credit, absolute amount and direction. Text fields pass through an encoding conversion. | 1289 |
| 15 | EBP | Comma-separated, repeats document date at the end, selects the auxiliary account where present. | 1246 |
| 20 | Cegid | Semicolon-separated, preserves both general and auxiliary accounts. Direction and unsigned amount are separate. | 665 |
| 25 | Cogilog | Tab-separated, resolves the source invoice number, replaces the general account with the auxiliary where present and emits debit or credit according to direction. | 701 |
| 30 | Coala | Semicolon-separated with separate debit and credit, piece number, reference, literal entry marker and separate auxiliary account. | 765 |
| 35 | BOB50 | Semicolon-separated with a general/customer/supplier discriminator and one account column in the recognised cases. | 802 |
| 40 | Ciel XIMPORT | Concatenated padded fields with a version trailer and carriage-return/line-feed ending. | 857 |
| 45 | Sage 50 Swiss | Twenty-column comma-separated header. Supports collective postings by comparing nearby rows with the same piece. The document date uses dots. | 1962 |
| 50 | Charlemagne | A translated tab-separated header introduces amount, direction and positions for three analytical code/label pairs. | 2536 |
| 60 | Quadratus | Fixed-position movement records. Auxiliary values and optional source-document attachments have separate handling. | 912 |
| 70 | Winfic | Fixed-position records with operation date and entry day in different representations, using the document date for both. | 1159 |
| 100 | OpenConcerto | Seven semicolon-separated fields, including account, source reference, label, debit and credit. | 1336 |
| 110 | LDCompta | Semicolon-separated entry records, with a two-character journal prefix and a source-specific subsidiary treatment. | 2116 |
| 120 | LDCompta 10 | Includes separate party-information and movement record types. A customer record and a journal row have different shapes. | 2256 |
| 130 | Gestimum V3 | Enriches invoice rows with the invoice reference and party name. Skips entries whose debit and credit are both zero. Uses a literal EUR indicator. | 2614 |
| 135 | Gestimum V5 | Carries document reference and piece separately, formats the document date without slashes, and ends with a literal EUR indicator. | 2722 |
| 200 | iSuite Expert | Semicolon-separated. Exports document date and year/month/day components. Text conversion uses Windows-1252. Generic customer/supplier accounts can be replaced by a trimmed auxiliary number. | 2773 |
| 205 | ISTEA | Twelve quoted fields. Resolves a party label per piece, computes separate account representations and converts output to ISO-8859-1. | 1412 |
| 1000 | FEC | Tab-separated, 21 named fields, with separate piece/entry dates, actual export date policy, lettering, optional document file and source invoice reference. | 1474 |
| 1010 | FEC variant | Same header as 1000. Uses a different mapping of document and creation dates. | 1720 |

## Positional mappings for separated records

The following sequences run from the first output column to the last. A general account and a subsidiary account are strings. Applying numeric conversion before an account-length policy can discard meaningful leading zeroes. The account helpers apply the configured length rules. Amounts formatted for display, normalised numeric amounts and FEC-style amounts use distinct formatters.

| ID | Column order | Conditions and transformations |
| ---: | --- | --- |
| 1 | Piece, document date, source reference, operation label, general account, auxiliary account, debit, credit, debit less credit, journal | The label is surrounded with single quotes when the writer's separator expression matches it. Account lengths are applied independently. The writer joins fields directly. |
| 10 | Piece, operation label, document date, operation label, account number, account label, document reference, debit, credit, absolute difference, direction, lettering code, journal | Date is DDMMYYYY. An auxiliary account selects both the auxiliary number and the subsidiary label. |
| 15 | Movement row ID, document date, journal, account, operation label, piece, absolute difference, direction, document date | Date is DDMMYYYY. Auxiliary number takes precedence. The label is quoted and shortened to 40 characters, the quoted piece to 15. |
| 20 | Document date, journal, general account, auxiliary account, direction, absolute difference, operation label, source reference | Date is DDMMYYYY. The last two fields lose accents. By default the FEC formatter emits two decimal places, a decimal comma and no thousands separator. |
| 25 | Journal, document date, invoice reference, account, blank, label, document date, debit, credit, source reference, label | Date is DDMMYYYY. Customer invoice reference is the issued reference. A supplier invoice supplies the vendor's reference. The opposite amount field is empty for a normal debit or credit entry. |
| 30 | Document date, journal, general account, piece, source reference, debit, credit, literal E, auxiliary account | Date is DD/MM/YYYY. Both accounts have their own positions even when the auxiliary is empty. |
| 35 | Piece, document date, discriminator, account, debit, credit, label | Date is DD/MM/YYYY. General-only rows use G. With an auxiliary, a general prefix of 411 yields C and 401 yields F. An unrecognised prefix with an auxiliary has no discriminator appended, so subsequent fields move one place. The label is shortened to 32 characters. |
| 100 | Document date, journal, account, source reference, operation label, debit, credit | Date is DD/MM/YYYY. Auxiliary takes precedence. Separate monetary columns preserve both sides. |
| 200 | Piece, document date, year, month, day, source reference, cleaned operation label, account, first label segment, debit, credit, stored amount, journal | Date is DD/MM/YYYY. A general account equal to the configured-width 411 or 401 control account uses the auxiliary number with trailing zeroes removed. Others use the general number. |
| 205 | Piece, document date, source reference, piece-level party label, account with prefix match, preferred account, associated general account, business label, shortened operation description, debit, credit, journal | Date is DD/MM/YYYY. A prior pass collects labels from subsidiary accounts beginning with 4. A bank line uses the shortened operation description for the business label. A non-bank entry uses the account label or subsidiary label. |

## Fixed fields and dated evidence

For Ciel, in output order, the movement writer uses a piece padded to five characters, two-character journal, eight-character document date, eight-character due date, 12-character source reference, 11-character account, 25-character combined reference/description, 13-character right-aligned FEC-formatted absolute amount, one-character direction, 18 blank positions, a 34-character operation label and the literal trailer `O2003`. Both dates use YYYYMMDD. The piece uses padding alone, so an overlength piece can exceed the nominal width. The account uses the subsidiary when available. A design that always truncates the piece at five characters would change the observed output.

For FEC and its variant, the writer omits rows with zero on both sides. With a document dated 30 April but a ledger creation date of 2 May, format 1000 emits 30 April as the entry date and 2 May as the piece date. Format 1010 emits 2 May as the entry date and 30 April as the piece date. Both retain the piece number and the document reference. The same source balance can consequently group into different periods in an external application that relies on the imported entry date.

## Worked debit and credit

Suppose a tax-free sale of 100 produces piece 72 in journal SALES, dated 30 April 2026. The receivable row debits general account 411000 and carries subsidiary C004. The revenue row credits 700000 and has no subsidiary. Both use source reference INV-72. Assume the configured account lengths leave these account codes intact.

| Interpretation | Receivable row | Revenue row |
| --- | --- | --- |
| Configurable format, debit / credit / signed amount | 100 / 0 / +100 | 0 / 100 / −100 |
| Cegid, account pair / direction / absolute amount with default numeric formatting | 411000 and C004 / D / 100,00 | 700000 and empty / C / 100,00 |
| OpenConcerto, selected account and monetary side | C004, debit 100 | 700000, credit 100 |
| BOB50, discriminator and account | C and C004 | G and 700000 |

The two signed amounts sum to zero. The Cegid amount column on its own sums to 200. The receiver must apply the direction to balance the piece. OpenConcerto exports the customer subsidiary in the account column, so reconstructing the control account in the receiving system also needs its chart or subsidiary mapping.

The release registry and dispatch are at `htdocs/accountancy/class/accountancyexport.class.php:50–94,144–199,245–341,495–558`. Row selection and marking are at `htdocs/accountancy/bookkeeping/export.php:504–610,611–735`. General and subsidiary account lengths are at `htdocs/core/lib/accounting.lib.php:152–219`. Numeric presentation is at `htdocs/core/lib/functions2.lib.php:2783–2804`. Full byte positions for the other fixed-width records, all package-specific auxiliary record types and per-recipient import behaviour are separate from the ten positional mappings above.
