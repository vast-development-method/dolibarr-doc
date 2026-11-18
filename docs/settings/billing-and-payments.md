# Invoice issuance, retention and payment reports

These eleven controls appear on four setup screens for customer invoices, progress invoicing, customer payments and supplier payments. Each row gives the setup location first and an operation that reads the setting second. A term, percentage or mode changed today can have a different effect on a new draft, a continuing billing cycle and a report rendered for an existing document.

## Issue an invoice

| Operator control | Choice and effect | Setup and use in release 24.0.3 |
| --- | --- | --- |
| Use the validation date for issuance (`FAC_FORCE_DATE_VALIDATION`) | Yes or no. The setup reads zero if unset. For an invoice with a provisional or empty reference, validation takes the current date and recalculates the ordinary due date. With the option off, the draft's business date can be retained. | `htdocs/admin/invoice.php:872` and `htdocs/compta/facture/class/facture.class.php:3655` |
| Require chronological issuance (`INVOICE_CHECK_POSTERIOR_DATE`) | When enabled, validation checks whether the invoice would be last among documents of the same type. A later existing issue can prevent validation. This concerns the sequence of issues, while the previous control supplies a date. | `htdocs/admin/invoice.php:882` and `htdocs/compta/facture/class/facture.class.php:3660` |
| Generate Belgian structured payment references (`INVOICE_PAYMENT_ENABLE_STRUCTURED_COMMUNICATION`) | The switch appears for a company registered in Belgium. With it enabled, collection-file generation calculates a structured reference from invoice reference and type. Otherwise that part of the export uses the configured or constructed unstructured remittance text. | `htdocs/admin/invoice.php:795` and `htdocs/compta/prelevement/class/bonprelevement.class.php:2566` |

See [customer invoices](../finance/customer-invoices.md), [invoice admission](../policies/form-defaults-and-invoice-admission.md) and [payment orders](../treasury/payment-orders.md).

## Bill work in stages

| Operator control | Choice and effect | Setup and use in release 24.0.3 |
| --- | --- | --- |
| Progress billing mode (`INVOICE_USE_SITUATION`) | 0 disables the feature. In mode 1 a line's progress represents cumulative completion. In mode 2 the line carries progress for the current instalment. When validation decides whether the cycle is final, mode 2 combines current and preceding progress. For a line already at 30% and now at 55% completion, the second entry represents 55% in mode 1 and 25% in mode 2. | `htdocs/admin/invoice_situation.php:76` and `htdocs/compta/facture/class/facture.class.php:4009` |
| Permit progress credit notes (`INVOICE_USE_SITUATION_CREDIT_NOTE`) | Enables the credit-note action for a validated or later progress invoice at the end of its cycle with no subsequent invoice. The card also evaluates the user's invoice privileges. Enabling the setting leaves those eligibility and permission conditions in force. | `htdocs/admin/invoice_situation.php:86` and `htdocs/compta/facture/card.php:6960` |
| Invoice types eligible for retention (`INVOICE_USE_RETAINED_WARRANTY`) | The selector offers progress invoices alone or standard invoices together with progress invoices. The new invoice card checks the configured type set before exposing the retention fields for that invoice. | `htdocs/admin/invoice_situation.php:95` and `htdocs/compta/facture/card.php:4604` |
| Restrict retention to the final progress invoice (`INVOICE_RETAINED_WARRANTY_LIMITED_TO_FINAL_SITUATION`) | With the switch on, the display calculation tests the cycle's final flag. For a draft whose final flag has yet to be set, it inspects the completion of eligible lines. The sales journal also tests this setting before breaking out the retained amount. | `htdocs/admin/invoice_situation.php:106`, `htdocs/compta/facture/class/facture.class.php:6081` and `htdocs/accountancy/journal/sellsjournal.php:417` |
| Default percentage to retain (`INVOICE_SITUATION_DEFAULT_RETAINED_WARRANTY_PERCENT`) | The setup accepts 0 through 100 in increments of 0.01. The creation form uses a supplied or existing nonzero retention, including one carried from a preceding invoice, before using the configured percentage as the form default. | `htdocs/admin/invoice_situation.php:111` and `htdocs/compta/facture/card.php:4612` |
| Default payment term for retention (`INVOICE_SITUATION_DEFAULT_RETAINED_WARRANTY_COND_ID`) | Choose a payment term from the dictionary. The form first honours an explicitly selected retention term. With no selection it takes the default and, where available, the preceding invoice's own retention term takes priority. This term applies to the retained amount separately from the ordinary invoice term. | `htdocs/admin/invoice_situation.php:123` and `htdocs/compta/facture/card.php:4624` |

For example, use a 5% default and a retention term different from the ordinary payment term. Once a progress invoice carries a negotiated 3% and an explicit retention term, the continuation form can inherit those values. Check the final-only policy separately when deciding which stage recognises the retention. See [progress and retention](../finance-exceptions/progress-and-retention.md).

## Present grouped payment reports

| Operator control | Choice and effect | Setup and use in release 24.0.3 |
| --- | --- | --- |
| Group customer payment reports by instrument (`PAYMENTS_REPORT_GROUP_BY_MOD`) | Yes groups the customer report by payment method. The renderer detects changes of method when producing group totals. No uses the ordinary arrangement. The report reads existing payment rows. | `htdocs/admin/payment.php:296` and `htdocs/core/modules/rapport/pdf_paiement.class.php:592` |
| Group supplier payment reports by instrument (`PAYMENTS_FOURN_REPORT_GROUP_BY_MOD`) | This independent switch selects method groups for the supplier report. A company can therefore group supplier payments while keeping the customer report in its ordinary form. | `htdocs/supplier_invoice/admin/supplier_payment.php:476` and `htdocs/core/modules/rapport/pdf_paiement.class.php:619` |

See [collections](../finance/collections.md) and [supplier payments](../supply/payables.md).
