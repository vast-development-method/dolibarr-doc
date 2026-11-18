# Audit-file dates, currency and source documents

The two built-in audit-file writers, 1000 and 1010, emit the same 21-column tab-separated header. Each selected journal line with a nonzero debit or credit contributes one data row. A zero on both sides omits that row. CRLF ends each row. Posting direction is represented by separate debit and credit columns.

| Position | Field name | Supplied value |
| ---: | --- | --- |
| 1 | JournalCode | Stored journal code. |
| 2 | JournalLib | Translated journal label, accents removed, tabs and newlines replaced and special-character cleanup applied. |
| 3 | EcritureNum | Piece number shared by the lines of a journal entry. |
| 4 | EcritureDate | Document date in 1000. Ledger-row creation date in 1010. |
| 5–6 | CompteNum, CompteLib | General account with configured account length, then its label with control whitespace replaced and accents removed. |
| 7–8 | CompAuxNum, CompAuxLib | Formatted subsidiary account and its similarly cleaned subsidiary label. |
| 9 | PieceRef | Source-document reference stored on the ledger. Tabs and line breaks become spaces. |
| 10 | PieceDate | Ledger-row creation date in 1000. Document date in 1010. |
| 11 | EcritureLib | Operation label with control whitespace replaced, three-period sequences removed and accents stripped. |
| 12–13 | Debit, Credit | Separate debit and credit amounts using the accounting-file decimal and thousands settings. Defaults are two decimals, decimal comma and no grouping. |
| 14 | EcritureLet | Lettering code with tabs and line breaks replaced. |
| 15–16 | DateLet, ValidDate | Matching date and validation date from the movement supplied to the writer. |
| 17–18 | Montantdevise, Idevise | Direct pass-through of foreign amount and currency code when populated on the input row. |
| 19 | DateLimitReglmt | Payment due date, when present. |
| 20 | NumFacture | For a customer invoice the issued invoice number. For a supplier invoice the vendor's document reference. Other sources are blank. The writer cleans control whitespace, applies its text conversion helper and requests truncation at 17 characters. |
| 21 | FichierFacture | Member name of an attached source PDF when located and selected. Otherwise empty. |

The date fields use YYYYMMDD. A sale dated 30 April and transferred to the ledger on 2 May places 20260430 in EcritureDate and 20260502 in PieceDate for format 1000. Format 1010 swaps them. The date used to select the movements for the export is a separate choice. Picking the second format changes the two emitted fields without recalculating the debit, credit or payment deadline.

## Source currency through the normal entry points

Financial records and the general ledger storage have places for base amounts and transaction-currency data. The writer checks only the two values on the loaded row for columns 17 and 18. The standard ledger export screen and the service both call the general ledger reader named `fetchAll`. Its selection and row mapping omit the two foreign fields. The by-account reader, `fetchAllByAccount`, explicitly selects and populates them. It is a different entry point.

For a ledger posting of 1,800 in base currency for an invoice denominated at 100 in foreign currency, assume both monetary amounts and the transaction currency were stored. A normal export of the debit line can therefore carry base debit 1,800 with empty Montantdevise and Idevise. If a direct caller supplies a fully populated movement, the same writer emits the supplied foreign amount and code. It has no fallback exchange-rate lookup. A reconstruction of the original foreign balance from the normal exported file alone would be ambiguous.

The interactive export can clear lettering on the in-memory rows before sending them to the writer. That empties columns 14 and 15 while preserving the matching code on the ledger. Validation date and export date have different roles. The row data is passed to the file writer before the optional stamping of the selected persisted rows. A timestamp added by that export action does not retroactively appear in the already written row.

## Source PDF and file name

The archive workflow includes the ledger file and searches for at most one matching source PDF per piece. Source selection can independently suppress customer-invoice, supplier-invoice or expense-report files. Customer and expense documents require the exact sanitized reference plus `.pdf`. For a supplier invoice the lookup uses the supplier document's storage hierarchy, considers matching reference-prefixed uploaded PDFs in descending modification-date order and skips the generated reference-only PDF. The manifest and column 21 name the archived file using the line's document reference plus `.pdf`. A later row for the same piece reuses the earlier result. A qualifying source document missing on disk leaves an empty column and the other movements still export. The [Quadratus chapter](fixed-position-records.md) describes its different member-naming policy.

Both writers use the same fiscal filename rule because their format codes (`fec` and `fec2`) share the tested three-character prefix. It produces the issuer identifier stripped of spaces, FEC, the calculated fiscal period end as YYYYMMDD, and the text extension. The end of the reporting selection, or the current date when absent, determines which fiscal period supplies that end date. A configured timestamp suffix distinguishes successive extracts of the same period. For a fiscal year beginning in July, a selection ending in April 2026 gives a filename period end of 30 June 2026. Both formats can therefore request the same default basename for the same company and fiscal year. A filename hook can override it.

[Ledger format register](ledger-layouts.md)
