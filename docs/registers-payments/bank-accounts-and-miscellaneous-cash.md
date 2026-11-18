# Bank accounts and miscellaneous payments

## Bank accounts

The account register selects one `bank_account.rowid` in the bank-account entity population. Chart-of-accounts management grants access to this account dictionary. Other users pass the bank-area access check. Configuring an account, editing its categories and viewing its balance have separate permissions or actions.

| Selector | Business meaning |
| --- | --- |
| Reference and label | Text search on the internal `ref` and descriptive `label`. |
| Account number | Text search on bank-facing `number`. The account's general-ledger mapping is a separate field, `account_number`. |
| Open or closed | “Opened” selects `clos = 0`. “Closed” selects `clos = 1`. Without either selection both are eligible. |
| Categories | For every positive selected ID require a `categorie_account` link with this account and category. Multiple categories intersect. The uncategorised choice requires absence of any link. Combining it with a positive category yields an empty intersection. |
| Custom fields | Searchable account custom values are joined by `fk_object` when present. Type, currency and journal have display columns. The standard query does not add predicates for these columns merely because they are visible. |

For each selected account, the balance is the sum of signed `bank.amount` for `bank.fk_account = account.rowid` with operation date `dateo` up to the instant of enquiry. Future operations are excluded even when already entered. The display uses the account's currency, and the combined total line is suppressed for a mixed-currency page. A balance of 120 in one currency and 40 in another therefore cannot justify a cash total of 160 without a conversion policy.

The reconciliation count follows a different population. For an open noncash account configured for reconciliation, it counts linked rows with `bank.rappro = 0`. It has no operation-date cutoff matching the balance cutoff. The queue distinguishes late items using value date `datev`. Cash, closed and reconciliation-disabled accounts show the corresponding ineligibility. For example, with same-currency movements +120 already reconciled, −20 unreconciled today and −10 unreconciled tomorrow, the balance is 100 today and two transactions await reconciliation.

## Miscellaneous payments

Start with one `payment_various` in its own payment entity population. A bank-area access check applies. Optional joins resolve `fk_typepayment → c_paiement.id`, `fk_bank → bank.rowid`, and `bank.fk_account → bank_account.rowid`. A payment can remain visible without a resolved bank account when the search allows it. Its account mapping `accountancy_code`, subsidiary `subledger_account`, optional project `fk_projet` and own dates belong to the payment.

| Selector | Bound value and result |
| --- | --- |
| Reference and label | Exact integer payment `rowid` and text search on `label`. |
| Dates | Inclusive independent ranges on the payment's `datep` (payment date) and `datev` (value date). |
| Debit and credit amounts | Both predicates compare `payment_various.amount` numerically. Direction is assigned when rendering the row, with `sens = 0` in debit and `sens = 1` in credit. Supplying both filters requires the same stored amount to pass both. |
| Bank account and entry | A positive account selection compares `bank.fk_account`. The bank-entry input also applies an account predicate using the selected **account** value. It does not compare the entry ID to `fk_bank`. Follow the stored `fk_bank` to identify a specific movement. |
| General account, subsidiary and method | Positive numeric general-account selection compares `accountancy_code`. Subsidiary search normally compares its text. With subsidiary selector mode and a positive selected value, it uses exact equality. A positive payment method compares `fk_typepayment` to its dictionary ID. |
| All-field search | Payment row ID, label, payment date, value date and amount. |

Two miscellaneous payments each of 35, one in each direction, both satisfy a debit-amount search of 35. In the displayed table the debit total is 35 and the credit total is 35. The two movements net to zero when viewed as cash flows. No invoice allocation or customer balance can be inferred from these records.
