# Fixed-position ledger records

The receiver needs the record type, the unit of length and the padding rules as well as the account and amount. Formats 40, 60 and 70 handle the same dated debit differently. The ranges below are one-based and inclusive. They assume plain single-byte text, ordinary-sized values and the standard truncation setting. CRLF means the two bytes carriage return and line feed. Spaces and zeroes in the following tables are actual field contents.

## Quadratus movement, format 60

Every selected ledger row emits one movement. A row with a subsidiary account first emits an account record. Both records end with CRLF and contain adjoining fields without separators. Before writing, the producer removes accents from the reference, account identifiers and labels. In the operation label, tabs and line breaks become spaces. The operation and subsidiary labels lose occurrences of a hyphen followed by a space, a typographical ellipsis and three consecutive periods.

| Positions | Width | Movement contents |
| --- | ---: | --- |
| 1 | 1 | Literal M. |
| 2–9 | 8 | Subsidiary account when present, otherwise general account. Keep the first eight characters and pad on the right with spaces. |
| 10–11 | 2 | First two characters of journal code, right-padded. |
| 12–14 | 3 | Literal 000. |
| 15–20 | 6 | Document date as DDMMYY. |
| 21 | 1 | Space. |
| 22–41 | 20 | Source reference, a space and the operation label, keeping the first 20 and padding on the right. |
| 42, 43 | 1 each | Stored direction, typically D or C, then literal plus. Credit movements also use plus here. |
| 44–55 | 12 | Absolute value of debit less credit, multiplied by 100, converted to text and left-padded with zeroes. The writer applies no separate rounding or maximum-width step. |
| 56–63 | 8 | Blank counterpart account. |
| 64–69 | 6 | Due date as DDMMYY, or 000000 if absent. |
| 70–71, 72–74 | 2, 3 | Blank matching and statistics codes. |
| 75–79 | 5 | First five characters of piece number, right-padded with spaces. |
| 80–89, 90–99 | 10 each | Blank job and quantity. |
| 100–107 | 8 | First eight characters of piece number, right-padded. |
| 108–110 | 3 | Current currency code, right-padded with spaces. |
| 111–113, 114–116 | 3 each | First three characters of journal code, right-padded, followed by three spaces. |
| 117–146 | 30 | Operation label only, truncated and right-padded. |
| 147–148 | 2 | Blank tax code. |
| 149–158 | 10 | Take the first 20 characters of source reference, then the last ten bytes of that result. Right-pad when shorter. |
| 159–168, 169–181 | 10, 13 | Reserved spaces and blank foreign amount. |
| 182–193 | 12 | Archive member name if its character length is exactly 12. Otherwise twelve spaces. |
| 194–231 | 38 | Spaces. CRLF follows the payload. |

A general receipt of 125.50 and a general credit of 125.50 both write `000000012550` in positions 44–55. The direction at position 42 determines which side of the journal each belongs to. For piece 72 the five-position and eight-position piece fields begin with 72 and end in spaces. When an attachment is found its separate name is `00000072.pdf`. Rounding an input with more than two fractional places before multiplying would produce a different output from the writer.

### Subsidiary account record

| Nominal positions | Contents |
| --- | --- |
| 1, 2–9, 10–39 | Literal C, eight-character subsidiary number and 30-character subsidiary label. The number and label are truncated then right-padded with spaces. |
| 40–98 | On a customer or supplier invoice, uppercase first seven characters of the subsidiary label followed by 52 spaces. On another document type the writer emits 59 spaces. |
| 99–106 | Configured customer or supplier control account for that invoice family, truncated and right-padded to eight. Eight spaces for other sources. |
| 107–216 | 110 spaces. |
| 217 | Literal 2 permits a partial account update on import. The suppress-third-party-update option writes a space. |
| 218 | C for a customer invoice, F for a supplier invoice, G for another source. |
| 219–453 | 235 spaces. CRLF terminates the record. |

The alphabetical key in positions 40 onward has no minimum padding of its own. For a customer with subsidiary label `ABC`, the writer emits three key bytes plus 52 spaces. The control-account field then starts at byte 95, and the account payload is 449 bytes. A seven-character key gives the nominal 453. Two ledger rows carrying the same subsidiary generate two account records even when their piece is identical.

For both movement and account rows, the truncation helper normally counts text characters with UTF-8 awareness, while padding works to a minimum byte length. The writer has no whole-row encoding conversion. A remaining multibyte symbol can make a nominally 20-character value exceed 20 bytes. Numeric padding also sets a minimum. Overwide amounts, nonstandard currency identifiers or the global setting that disables truncation can shift later fields. The ASCII examples describe the common layout and the transformation rules explain its exceptions.

### Attachment selection

With the archive option enabled, the writer identifies a source PDF by the trimmed piece number's file-cache entry. For customer invoices and expense claims, it looks for the exact sanitized document reference plus `.pdf` in that document's output folder. Supplier invoices use the supplier storage hierarchy and the most recent matching uploaded PDF with the document prefix and a suffix. The generated reference-only supplier PDF is excluded. Ordinary missing files leave the filename field blank. A repeated piece can reuse an earlier positive or negative lookup in the same run.

An attached PDF is named from the first eight characters of the piece number padded on the left with zeroes and followed by `.pdf`. For a nine-digit piece this selects the first eight digits. Two different pieces with the same first eight digits therefore request the same archive member name. The archive always starts with the exported ledger file. Archive support, creating or opening the output, and adding individual files are separate failure points from a missing source PDF. The interactive export offers source attachments for IDs 60, 1000 and 1010.

## Winfic movement, format 70

Each ledger row emits 18 data fields. An ASCII vertical bar separates the fields and a final vertical bar immediately precedes CRLF. Debit and credit are two amount fields. All fields can be located by their ordinal below for plain data without a vertical bar. The source joins the field strings directly without escaping embedded bars. The byte ranges give a common case with a two-character matching code and a piece of at most five ASCII characters.

| Field | Nominal byte positions | Value |
| ---: | --- | --- |
| 1 | 1–2 | First two journal-code characters, right-padded with spaces. |
| 2 | 4–11 | Document date, DDMMYYYY. |
| 3 | 13–18 | Five spaces followed by 1 for the folio. |
| 4 | 20–25 | Selection sequence starting at 1, left-padded to six. Takes the first six characters if necessary. |
| 5 | 27–32 | Document date repeated as DDMMYY. |
| 6 | 34–39 | Subsidiary account if present, otherwise general. First six characters, right-padded with zeroes. An account 41 becomes 410000. |
| 7 | 41–53 | Debit formatted to two decimal places with a decimal comma and no thousands separator, left-padded to 13. A non-debit row supplies zero. |
| 8 | 55–67 | Credit in the same format. A debit row supplies zero. |
| 9 | 69–98 | Accent-stripped reference and operation label joined with one space, truncated to 30 and right-padded. |
| 10 | 100–103 | Take the matching code with left truncation to two characters and repeat the result twice. Empty code produces an empty field, single A produces AA and AB produces ABAB. |
| 11 | 105–109 | Piece number with left truncation at five characters and left space-padding to five. |
| 12 | 111–114 | Four spaces for the statistic. |
| 13 | 116–123 | Due date DDMMYYYY. If absent, use the document date. |
| 14–16 | 125, 127, 129 | Literal 1 for currency indicator, a space, a space. |
| 17 | 131–141 | Literal 0,000000000. |
| 18 | 143–144 | Two spaces. The final bar occupies 145 in the nominal case. |

The left-truncation helper used by fields 10 and 11 has a distinct overflow behavior. With ordinary truncation enabled it prepends a Unicode ellipsis to the retained rightmost characters even when the writer requests truncation without dots. Matching code ABC therefore emits `…BC…BC`. A piece 123456 emits `…23456`. On UTF-8 output the ellipsis occupies three bytes. For an unmatched entry the region between the ninth and tenth separators is empty, shortening the nominal line by four. These cases explain why a repeatable export needs the actual values as well as the nominal positions. The writer supplies no whole-file transcoding.

For an unmatched debit dated 30 April 2026 with no due date, fields 2 and 13 both read 30042026 and field 5 reads 300426. A debit of 100 and a credit of equal value on the next row produce `100,00` in fields 7 and 8 respectively, including the specified left padding. Field 4 increments for each selected row, independent of the piece number.

## Ciel XIMPORT, format 40

The file contains one concatenated record per selected line. CRLF follows its nominal 142-byte payload. The general account is used unless a subsidiary is present. The configured filename option can force the name `XIMPORT.TXT`.

| Positions | Value |
| --- | --- |
| 1–5, 6–7 | Piece right-padded to at least five, then first two journal characters right-padded to two. The piece has no truncation. |
| 8–15, 16–23 | Document and due dates as YYYYMMDD, left space-padded to eight. The writer passes the due date through the date formatter. |
| 24–35, 36–46 | First 12 source-reference characters and first 11 account characters, both right-padded. |
| 47–71 | Reference and operation label concatenated directly, accents removed, first 25 right-padded. |
| 72–84, 85 | Absolute debit less credit formatted with the accounting-file numeric settings and left space-padded to 13. Separate direction. |
| 86–103, 104–137 | Eighteen blank analytical positions and first 34 accent-stripped operation-label characters, right-padded. |
| 138–142 | Literal O2003, starting with capital letter O. |

A seven-digit piece shifts all subsequent positions by two bytes. A credit of 125.50 carries the same absolute amount as its matching debit. Its direction identifies the credit. A different decimal separator or number of decimals in the accounting-file settings affects this file even though its field ordering stays the same.

See the [ledger format register](ledger-layouts.md) for selection, reconciliation and all other writers.

The [worked receivable](fixed-position-example.json) preserves the spaces, field separators and CRLF in JSON strings. Printed bytes for the same ASCII input are 144 for the Ciel row, 451 plus 233 for the two Quadratus rows, and 147 for the Winfic row. All four lengths include their line terminators.
