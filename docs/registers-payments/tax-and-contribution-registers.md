# VAT, local tax and social contribution registers

## VAT obligations and payments

The VAT register uses one `tva.rowid` per declaration or obligation in its VAT entity population. It left-joins the payment method on `fk_typepayment`, the planned account on `fk_account`, and remittances on `payment_vat.fk_tva = tva.rowid`. The header `amount` is the amount recorded for the obligation. The sum of remittance `amount` values supplies the paid-to-date input to the displayed status alongside the header paid flag `paye`. Tax-charge area access applies. Creating or deleting records requires the respective charge grant.

| Filter | Effect |
| --- | --- |
| Reference, label and amount | Search the obligation row ID, `label` and header amount. |
| Period end | Inclusive range on header `datev`. The default sort puts the most recent period end first. |
| Payment dates | The query supports a range on header `datep`. The standard table omits its date-entry controls. No date predicate here narrows the joined remittance rows for the paid-to-date sum. |
| Method and account | Compare the selected IDs with header `fk_typepayment` and `fk_account`. |
| Status | Compare selected nonnegative value with the stored `paye`. The rendered status also considers the joined payment sum. |

The grouped display shows one obligation even with several remittances. Where full-record counts are enabled, the count query removes grouping and counts joined rows. One obligation with two remittances can therefore contribute two to pagination's count and only one to the displayed register. For an obligation of 900 with remittances of 150 and 300, the displayed amount remains 900. Paid to date is 450. The arithmetic balance is 450. An operational VAT-on-sales report for the same period answers a different question and has a different record population.

## Social and fiscal charges

One `chargesociales` obligation in the current entity must resolve `fk_type → c_chargesociales.id`. The category supplies its classification and accounting code. Optional joins resolve `fk_account → bank_account`, `fk_mode_reglement → c_paiement`, `fk_user → user` and, with projects enabled, `fk_projet → projet`. One-to-many `paiementcharge.fk_charge` rows supply the sum paid per obligation. Grouping preserves one result per charge. The total count uses distinct charge IDs.

| Filter | Effect |
| --- | --- |
| Charge reference, label and category | Exact `chargesociales.ref`, text search on `libelle`, and exact positive `fk_type`. |
| Employee and project | A selected set restricts `fk_user`. Optional project reference uses `projet.ref` when projects are enabled. |
| Method and account | Select the charge's `fk_mode_reglement` and `fk_account`. These are stored preferences on the obligation. |
| Amount and status | Numeric search uses obligation `amount`. The status filter uses `paye`. The status presentation also receives the sum of payment rows. |
| Dates | The due-date range compares `date_ech` and the separate period range compares `periode`. Both admit their endpoints. Neither restricts settlement dates in `paiementcharge`. |

For a social charge of 600 due in period B for payroll period A, payment of 200 in A and 150 in C leaves 250 outstanding. A due-date search for B still returns amount 600 and paid-to-date 350. A cash enquiry limited to B would find neither of those two cash disbursements. The tax-charge grant used to view this register is separate from creating or deleting obligations.

## Local tax payments

The local-tax register directly selects `localtax.rowid`, `amount`, `label`, `datev` and `datep` for the current entity and the exact requested `localtaxtype`. It orders by `datev` descending. It displays `datev` as the end of the tax period and `datep` as payment date. The selector does not join remittances, filter a submitted date range or compare an amount. Tax-charge access controls entry. The creation button requires the charge creation grant.

If the view is limited, only the first records in that ordering are rendered and summed. Two eligible records with amounts 75 and 25 yield a visible total of 100. A limit of one yields the amount on the more recent period-end record. A different local-tax type contributes zero to both views even when its payment date and amount coincide.
