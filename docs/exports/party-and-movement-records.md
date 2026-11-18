# LDCompta movements and party records

A single sales invoice can create a subsidiary receivable and several revenue or tax rows with the same piece number. Format 110 (version 9) emits one E record per selected ledger row. Format 120 (version 10) can also emit a C record containing customer details before the first movement of a document. The exporter processes records in the selected order. A later payment or credit can produce its own movement and party records.

Both versions use a semicolon delimiter, CRLF, and no header. Empty positions remain present as consecutive separators. There is no common quoting pass over these rows. An embedded semicolon or line break in an inserted name or label can therefore change the apparent row or field boundaries for the recipient.

## Posting columns common to both versions

| Position | Identifier | Meaning |
| ---: | --- | --- |
| 1 | TYPE | E for an entry. |
| 2 | JNAL | First two bytes of the journal code. |
| 3 | NECR | Individual ledger movement ID. |
| 4 | NPIE | Shared piece number. |
| 5 | DATP | Document date, YYYYMMDD. |
| 6 | LIBE | Operation label. Version 9 passes it through. Version 10 requests right truncation to 25 characters. |
| 7 | DATH | Payment due date, YYYYMMDD when available on the supplied row. |
| 8 | CNPI | Invoice nature selected from the type and amount as shown below. Other document families get an empty field. |
| 9 | RACI | Empty. General and subsidiary accounts have their own fields. |
| 10 | MONT | Absolute debit less credit in the operating language's monetary presentation. Version 9 forces two decimal places. Version 10 requests two-place rounding using the normal display settings, which can retain more precision or apply a display limit. |
| 11 | CODC | Stored debit or credit direction. |
| 12 | CPTG | General account, with the configured general-account length policy. |
| 13 | DATE | Version 9 uses row creation date. Version 10 repeats the document date. Both use YYYYMMDD. |
| 14 | CLET | Matching/lettering code. |
| 15 | DATL | The lettering-date value on the supplied movement, written directly. The interactive ledger reader supplies a converted timestamp here. |
| 16 | CPTA | Formatted subsidiary account where one exists, otherwise empty. |
| 17 | C.N.A.T | F for a supplier invoice carrying a subsidiary account, C for a customer invoice carrying one, empty otherwise. |

The amount in position 10 is unsigned. The piece nature and debit/credit direction serve different purposes.

| Invoice family | Version 9 nature decision | Version 10 nature decision |
| --- | --- | --- |
| Supplier | AF if debit less credit is positive, FF otherwise. | AF if the row's stored amount is negative, FF otherwise. |
| Customer | AC if debit less credit is negative, FC otherwise. | AC if the row's stored amount is negative, FC otherwise. |

Consider a customer invoice dated 30 April, transferred to the ledger on 2 May, with a debit to receivables and a credit to revenue. If both ledger rows carry a positive stored amount, version 10 gives both FC. Version 9 gives FC to the debit row and AC to the credit row. In both versions the two lines still balance and have independent D and C indicators. For field 13 version 9 writes 20260502 and version 10 writes 20260430. Treating the exported nature as a single voucher-level property would lose the version 9 result.

## Trailing movement fields

The field sequence diverges at position 18. The headerless formats need these empty slots in their original order.

| Version 9 positions | Output fields in order | Content |
| --- | --- | --- |
| 18–21 | SECT, CTRE, NORL, DATV | Four empty fields. |
| 22 | REFD | Source document reference. |
| 23–24 | CODH, NSEQ | Empty. |
| 25–27 | MTDV, CODV, TXDV | Literal 0, empty, literal 0. |
| 28–35 | MOPM, BONP, BQAF, ECES, TXTL, ECRM, DATK, HEUK | Eight empty fields. |

| Version 10 positions | Output fields in order | Content |
| --- | --- | --- |
| 18–20 | CTRE, NORL, DATV | Three empty fields. |
| 21 | REFD | Source document reference. |
| 22 | NECA | Literal 0. |
| 23–26 | CSEC, CAFF, CDES, QTUE | Four empty fields. |
| 27–29 | MTDV, CODV, TXDV | Literal 0, empty, literal 0. |
| 30–37 | MOPM, BONP, BQAF, ECES, TXTL, ECRM, DATK, HEUK | Eight empty fields. |

The exchange amount and exchange rate slots are always zero in both layouts. The currency slot is empty. The originating ledger can still hold an amount in document currency. That information has no corresponding value in these two exports.

## Customer information in version 10

Before an entry whose source reference differs from the preceding reference, the writer looks up a party by customer code equal to the ledger row's third-party code. The previous reference starts empty. The lookup uses customer code even for a movement originating in another document family. It has no explicit entity predicate or explicit ordering. The reader of the movements applies its own entity scope earlier. A successful lookup with a row yields a C record followed by the E record. A missing match skips only C. Contiguous rows with the same reference reuse the previous comparison and emit only E after the first. For references A, B, A with successful lookups, the third row can emit the A customer's details again.

| C positions | Fields in order | Emitted values |
| --- | --- | --- |
| 1–6 | TYPE, NOCL, NMCM, LIBI, TITR, RSSO | Literal C, customer code, three empty fields and party name. |
| 7–11 | CAD1, CAD2, CAD3, COPO, BUDI | Three address segments, postal code and first 40 bytes of town. |
| 12–14 | CPAY, PAYS, NTEL | Empty country-code field, first 40 bytes of the resolved country name, phone. |
| 15–20 | TLEX, TLPO, TLCY, NINT, COMM, SIRE | Five empty fields and the SIRET identifier stripped of spaces. |
| 21–28 | RIBP, DOBQ, IBBQ, COBQ, GUBQ, CPBQ, CLBQ, BIBQ | Eight empty fields. |
| 29–38 | MOPM, DJPM, DMPM, REFM, SLVA, PLCR, ECFI, CREP, NREP, TREP | Ten empty fields. |
| 39–48 | MREP, GRRE, LTTA, CACT, CODV, GRTR, NOFP, BQAF, BONP, CESC | Ten empty fields. |

A multiline address is split at line feeds. The writer removes tabs and carriage returns from each segment, keeps up to 40 characters per segment and exports the first three segment positions. An absent segment yields no address content in its slot. For a single-line address, tabs and carriage returns become spaces. The byte substrings start at offsets 0, 41 and 82, taking 40 bytes apiece. Input bytes at offsets 40 and 81 are therefore skipped rather than becoming the first byte of the next field. This branch can split a multibyte character.

[Ledger export register](ledger-layouts.md)
