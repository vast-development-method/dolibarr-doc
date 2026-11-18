# Swiss general ledger, education and commercial accounting formats

This chapter maps selectors 45, 50, 130 and 135. A posting with piece 72, an invoice reference and two balanced rows illustrates three separate decisions. The piece can identify a voucher, the reference can identify a customer's document and the record ID can identify one journal line. Different recipients expect each in a different position.

## Sage 50 Swiss, format 45

The header and rows use commas and CRLF. Each header has 20 field names. The writer uses the configured export separator *as data* twice within a row and uses a literal comma to join the fields. A configured comma in those positions is unquoted, so splitting a data row on commas can produce more fields than the header. The actual field assignments follow.

| Positions | Names | Contents |
| --- | --- | --- |
| 1–3 | Blg, Datum, Kto | Piece number, document date as DD.MM.YYYY, formatted general account. |
| 4–5 | S/H, Grp | S for a debit and H otherwise. First character of journal code. |
| 6 | GKto | Formatted party code from the writer's account-counterpart input when present. Otherwise, if the piece equals the remembered piece, use its remembered first general account through the subsidiary formatting policy. For a newly encountered piece write `div`. |
| 7–10 | SId, SIdx, KIdx, BTyp | Configured export separator as field 7, then 0 three times. |
| 11–12 | MTyp, Code | 2 for a collective posting, 1 otherwise. Code contains a quoted empty string. |
| 13–15 | Netto, Steuer, FW-Betrag | Absolute debit less credit, literal `0.00` for tax and literal `0.00` for foreign amount. |
| 16–17 | Tx1, Tx2 | Quoted label and reference texts as resolved below. |
| 18–20 | PkKey, OpId, Flag | 0, configured export separator as data, 0. |

The writer decides whether an individual row belongs to a collective posting using neighboring **selected** rows. It tests for the same piece two positions before, two after, or immediately before and after the current position. Three adjacent rows with piece 72 therefore all use 2. Two adjacent rows with piece 72 and surrounding rows of different pieces use 1. A gap of one intervening different row can also trigger the two-positions-away branch. The prior-piece and first-account memory changes after emitting the first row of each new run. The standard export reader populates a third-party code on each row but leaves the distinct counterpart input used for field 6 unassigned. On that path a pair for piece 72 typically starts with `div`, followed by its first general account.

The label formatter strips markup, decodes entities using the requested Windows-1251 target and normalises whitespace. It attempts to restrict each incoming account label and reference to 29 characters. It clears the first text if it is LIQ, LIQ Beleg ok, or no longer than three bytes. An empty first text takes the reference, clearing the second field. With both texts present and their combined byte lengths below 27, it joins them using space, slash, space into the first field and clears the second. An account label `Bank` and reference `PAY-72` therefore give Tx1 `Bank / PAY-72` and an empty Tx2. The header and row do not run through a single export-wide charset conversion.

Release sources are `htdocs/accountancy/class/accountancyexport.class.php:127–138,1962–2104,2833–2853`, `htdocs/core/lib/functions.lib.php:9057–9113` and `htdocs/accountancy/class/bookkeeping.class.php:1293–1336`.

## Charlemagne, format 50

The producer emits a localised tab-separated header, then a row per selected movement with LF line endings. Only column 8 has an invariant header label, S. The other labels use the output language and several are truncated. Header translation is independent of the currency of the underlying entry.

| Column | Data | Representation |
| ---: | --- | --- |
| 1 | Document date | YYYYMMDD. |
| 2 | Journal | First six characters. |
| 3 | Account | Subsidiary if present, otherwise general, up to 15 characters. |
| 4 | Account label | General-account label, up to 60 characters, including when column 3 selected a subsidiary. |
| 5 | Piece reference | Source document reference, up to 20 characters. |
| 6 | Operation | Replace tabs, carriage returns and line feeds with spaces and take up to 60 characters. |
| 7–8 | Amount, S | Display-formatted absolute debit less credit and the stored direction. |
| 9–14 | Three analytical code/label pairs | All six data values are empty. The labels still appear on the header. |

For piece 72 with subsidiary C004, general label Receivables and document reference INV-72, the account/label pair is C004 and Receivables. The piece column receives INV-72 even though the internal piece number is 72. No analytical distribution or cost centre is conveyed in columns 9–14. The source is `htdocs/accountancy/class/accountancyexport.class.php:2536–2601`.

## Gestimum versions 3 and 5, formats 130 and 135

Both writers skip a movement when its debit and credit are both zero. They separate fields with commas and terminate records with CRLF. Positions 1–5 have the same business meanings. Position 1 is the ledger row ID. Position 2 is the document date, using DD/MM/YYYY in version 3 and DDMMYYYY in version 5. Position 3 takes the first four bytes of the journal code. Position 4 looks at the first three bytes of the general account. For 411 or 401 it uses the subsidiary with **general-account** length formatting, including when the subsidiary is absent. Otherwise it uses the formatted general account truncated to 15 bytes. Position 5 is empty.

| Position | Version 3 | Version 5 |
| ---: | --- | --- |
| 6 | Resolved source-invoice reference, followed by space-hyphen-space and party name when available. Remove double quotes, truncate to 40 characters, then emit directly. | Operation label with double quotes removed, truncated to 40 and enclosed in double quotes. |
| 7 | Piece number with double quotes removed, up to ten characters. | Source reference, similarly cleaned, truncated to 40 and quoted. |
| 8 | Literal EUR. | Piece, similarly cleaned, truncated to ten and quoted. |
| 9–10 | Normalised absolute debit less credit and stored direction. | Normalised absolute debit less credit and stored direction. |
| 11 | Empty matching code. | Document date repeated as DDMMYYYY. |
| 12 | Payment due date, YYYYMMDD when available. | Empty. |
| 13–14 | End of the 12-field row. | Empty and literal EUR. |

Version 3 looks up the issued reference and company name for customer and supplier invoices using the source document ID and separate caches per family. The supplier lookup returns the ERP's supplier-invoice reference, which can differ from the reference printed on the vendor's document. A missing lookup leaves the ledger reference and an empty company name. A comma in the combined name or reference can create another field for a simple recipient because version 3 emits the text without enclosing quotes. Version 5 encloses its three text fields in quotes.

Consider a 125.50 receivable posted in a company with NAD base currency. With journal SALES, row 316, account 411000, subsidiary C004, reference INV-72, piece 72 and operation Installation, version 5 writes the following complete row before CRLF.

```text
316,30042026,SALE,C004,,"Installation","INV-72","72",125.5,D,30042026,,,EUR
```

The EUR indicator is hard-coded in both layouts. Neither writer uses that indicator to perform a currency conversion. A receiver interpreting the amount as euros would misstate the original NAD amount. The source ledger amount, company currency and exchange rate must remain independent inputs to any multi-currency design. The release writers are at `htdocs/accountancy/class/accountancyexport.class.php:2614–2710,2722–2767`. [Ledger format register](ledger-layouts.md)
