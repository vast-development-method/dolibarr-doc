# Bookkeeping register

One row is one leg in `accounting_bookkeeping`, scoped to the accountancy entity set. The screen requires enabled accounting, an internal user and the movement-read grant. Creating, deleting and exporting entries have distinct grants. Default ordering is by `piece_num`, then line `rowid`, both ascending. A journal piece can occupy several rows and can straddle a page boundary.

| Operator input | Selection on the stored leg |
| --- | --- |
| Movement number, debit or credit | Numeric tests on `piece_num`, `debit` or `credit`. A number alone requests equality. |
| General or auxiliary account | A simple value matches the beginning of `numero_compte` or `subledger_account`. Separate start and end inputs apply inclusive comparisons on the stored account strings. A category resolves its member account numbers and adds a membership predicate on `numero_compte`. |
| Journals | Match the selected journal codes in `code_journal`. A comma-separated code list can express multiple choices. |
| Document and narrative | Document type, document reference, operation label, direction, lettering code and import key use keyword predicates on their respective leg fields. |
| Open for reconciliation | Require `lettering_code IS NULL`. A stored empty string differs from null on engines that distinguish the two. Display of the lettering column depends on enabling lettering. |
| Business date | `doc_date` accepts inclusive start/end bounds or a separately supplied exact document date. |
| Audit and settlement dates | Independent inclusive bounds apply to creation, modification, export, validation and due dates. Selecting an export period tests `date_export`, while selecting a due period tests `date_lim_reglement`. |

On an initial visit an operator with export rights can receive fiscal-year bounds automatically when neither date is supplied. The page skips that initialization for a restored search, a movement-number or starting-account search, navigation or an explicitly submitted filter. It uses the configured fiscal year, otherwise a year containing the current instant, otherwise the configured opening month to derive a year. Supplied filters are combined. An available full count counts matching legs. Debit and credit column totals accumulate the displayed rows for the corresponding selected columns.

Consider piece 42 with one receivable debit of 115, a sales credit of 100 and a tax credit of 15. A search for the piece returns three legs and balances at 115 on each side when all three are displayed. Restricting to the sales account returns one credit of 100. Compare the complete piece when testing balance. [Bookkeeping operations](../finance/bookkeeping.md)
