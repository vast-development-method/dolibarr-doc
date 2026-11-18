# Customer invoice line account assignment

The operator assigns a general-ledger account to a sales invoice line before transferring the invoice into a journal. The queue requires enabled accounting, an internal user and the account-binding write grant. It selects invoices in the current accounting context with invoice sharing disabled.

| Decision | Effect on the queue |
| --- | --- |
| Document eligibility | Require `facture.fk_statut > 0`. Allow standard, replacement, credit and progress invoices. A deposit invoice is included unless deposits are configured as payments alone. |
| Line eligibility | Join `facturedet.fk_facture` to the header. Require `fk_code_ventilation <= 0` and `product_type <= 2`. A null comparison does not satisfy either predicate. Positive account IDs leave the queue. |
| Parties and items | The customer is required. The customer's country and the line's product are left joins, allowing a free-text line through when no item filter is applied. Entity-specific product or party account codes are read when the associated accounting options are enabled. |
| Chart | Candidate accounts join for the product's ordinary, intra-community and export sale code and the party sale code. Each candidate must match its account number, active flag, chart code and current entity. A missing candidate leaves the invoice line eligible. |
| Text and numeric search | Customer name, invoice reference, item reference or label, and line description have independent keyword filters. Line ID, stored untaxed amount and line VAT rate have numeric tests. VAT input is normalized. The account-number filter tests the ordinary product sales account join, even when another source supplies the displayed suggestion. |
| Geography and date | Customer VAT registration is searchable. Country choices include an individual code, foreign countries, the community group, that group excluding the home country, or countries outside it. A missing country fails ordinary membership or inequality comparisons. Invoice date bounds include both endpoints. A configured binding start can supply the initial lower bound. |

The list counts eligible joined lines and pages them. During progress billing, one display mode scales the printed net amount to the newly completed fraction. With current progress `p` and previous progress `q` in the same cycle, displayed net equals `total_ht × (p − q) / p`. Zero current progress displays zero in that branch. The amount filter uses stored `total_ht`. For stored net 600 at 60% after a previous 40%, the display shows 200. An amount filter for 600 still qualifies the line. For other document modes the displayed value is the stored net.

Selecting a candidate and applying the assignment writes the selected account's numeric ID to that line. A missing or nonpositive choice is reported per line. Valid selections elsewhere in the batch can succeed. A subsequent queue read omits successfully assigned lines. The journal-transfer operation has its own entry conditions. [Invoice posting](../specification/accounting/source-journal-postings.md)
