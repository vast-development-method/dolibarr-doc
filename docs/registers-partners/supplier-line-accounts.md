# Supplier invoice lines awaiting account assignment

The row key is `facture_fourn_det.rowid`. Each pending line joins its own header through `fk_facture_fourn` and the header's supplier through `facture_fourn.fk_soc`. Country, catalogue product and suggested accounts use left joins. A free-text purchase line can enter the register without a product or suggested account. A header with no detail contributes zero rows.

## Eligibility and identity

The screen requires accounting to be active, an internal user with `accounting.bind.write`, and a selected chart. It restricts invoices to the accounting entity, tests `facture_fourn.fk_statut > 0`, and requires `facture_fourn_det.fk_code_ventilation <= 0` and `product_type <= 2`. A null assignment is outside the comparison. The allowed header types are standard, replacement, credit note and progress invoice, plus deposit when supplier deposits are accounted for as invoices. An earlier assigned detail does not disqualify an unassigned sibling. Ledger transfer status is outside this selection.

## Search controls

| Input | Records or fields searched |
| --- | --- |
| `search_lineid`, `search_amount` | Numeric comparisons on line `rowid` and signed tax-exclusive `total_ht`. A reference amount of 100 and a credit of −100 match different signed predicates. |
| `search_invoice`, `search_societe` | Invoice search matches internal `ref` or supplier `ref_supplier`. Supplier search matches `societe.nom`. The separately read `search_ref_supplier` has no independent predicate. |
| `search_ref`, `search_label`, `search_desc` | Product reference searches `product.ref`. Label searches `product.label` or the invoice's `libelle`. Description searches the line's own `description`. |
| `search_vat`, `search_tvaintra` | The first normalizes the input numerically and compares it with the line's `tva_tx`. The other searches the supplier's `tva_intra`. A product's current rate is available to the suggestion workflow but does not replace the document's line rate in the filter. |
| `search_account` | Text match on the joined active domestic product purchase account's `account_number`. The join requires the chart version and current entity. Regional, export and supplier-specific suggestions have separate account joins. Searching for a number displayed by one of those other suggestions can omit the line. |
| Date controls | Start and end accept day, month and year on `facture_fourn.datef` from the start of the first day through the final second of the last day. A configured binding start supplies the lower limit on ordinary entry if the caller omits one. Clearing filters also clears the already prepared lower bound for that request. |
| `search_country` | Ordinary input searches the supplier country code. `special_allnotme` excludes the operating country. `special_eec` uses the configured European country list, `special_eecnotme` removes the operating country from that set and `special_noteec` selects outside it. A missing joined country fails each ordinary non-null comparison. |

When products or parties share master records with per-entity settings, their purchase account numbers come from the corresponding entity override. The four joins resolve domestic, intra-community and export product accounts and the supplier purchase account against active accounts in the local chart. The order is invoice date, invoice reference, then detail ID. Default direction is ascending unless the pending-assignment sort option selects descending. The count, when enabled, counts rows returned by the full ordered selector. The paged query then takes one extra row.

## Worked queue change

A validated standard invoice has line 41 for 100, assignment zero, line 42 for 50, already assigned, and line 43 for 20, assignment zero. Lines 41–43 are ordinary goods or services. A draft carries a fourth unassigned line for 90. The queue initially contains 41 and 43, at 120 in tax-exclusive value. An amount filter `>=50` selects only 41. Removing the amount filter and assigning an account to 41 while leaving 43 without a selection saves 41 and reports the unresolved 43. The refreshed queue now contains 43 at 20. The saved account affects purchase-journal preparation. A subsequent change to an assigned line has its own controls and posting consequences. [Account suggestion, reassignment and journal transfer](../finance/supplier-account-preparation.md)
