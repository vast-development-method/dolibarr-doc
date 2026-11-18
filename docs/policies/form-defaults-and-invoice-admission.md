# Form defaults and invoice admission

An accounts clerk sees a proposed value when opening a form, supplies the customer reference, then issues the invoice. Three points in that sequence can produce a different result. A page preference selects the initial value. The form can require an entry before submission. Issuing the document applies its own business rules to the stored customer and invoice.

## Choosing defaults for an entity and operator

The configuration record carries a page, optional query conditions, mode, field key, value, user and entity. The administration page writes shared entries with user zero in the active entity. The loader reads shared entries and entries for the specific user, scoped to the user's entity and the active entity. It indexes the result by page, mode, query conditions or unqualified page, then by field. This allows a filter on an outstanding-invoice list to differ from a default on a new-invoice form. The common loader does not define a contractual winning row for indistinguishable duplicate entries.

| Mode | Observable change |
| --- | --- |
| Creation default | Suggests a field at data entry. The common reader handles opening the create action with the parameter absent, object-level defaults and eligible configured values. A value supplied in the request can change the outcome. |
| List filter | Supplies an initial search criterion. A list can consequently show fewer rows on first entry even though the user has access to more. |
| Sort order | Changes the default ordering on the matching page. Manual sorting has a separate request path. |
| Focus | Positions the cursor at a named field on an eligible rendered form. |
| Mandatory field on the page | The page's form submission handler evaluates the configured input. It treats a cancellation separately and accounts for a rich-text field's editor contents. |

A customer-reference rule applied only at the form belongs in a specification of the operator interaction. A requirement on issuing an invoice is a separate contract that another client can encounter when it calls the business operation. Source locations are `htdocs/admin/defaultvalues.php:120–196`, `htdocs/user/class/user.class.php:835–880` and `htdocs/core/lib/functions.lib.php:1170–1310,13199–13283`.

## Issuing a customer invoice

| Decision in the issue operation | Result |
| --- | --- |
| Initial state and lines | A non-draft invocation returns without issuing again. A draft needs at least one line. |
| Actor | In ordinary mode the actor needs invoice creation authority. With advanced permissions enabled the operation requires the dedicated invoice-validation grant. |
| Effective date | For a provisional or empty reference the force-date option sets the invoice date at issue and recalculates the due date. |
| Chronology policy | The query takes the latest invoice date of the same invoice type, within the visible invoice entity set, among records carrying a validation date. Equality passes. The helper also allows a draft through its previously numbered-reference branch. |
| Domestic business identifiers | Each configured professional identifier is considered separately. The condition applies to a company when the issuer has a known country and the customer's country equals it. |
| Customer contact and tax data | The email setting requires a valid address. The VAT-number setting distinguishes taxable customers in the European scope from all taxable customers. Each branch reads the customer's tax-liability and identification fields. |
| Customer's reference | A dedicated invoice-validation setting makes the customer reference on the document mandatory. This concerns the customer's purchase reference, independently of the invoice's own public number. |
| Replacing a prior invoice | The source invoice must exist. The operation looks for an already validated replacement. A competing replacement, an absent source or a failed cancellation of the source stops the transaction. |
| Public reference and amount | A supplied fixed number, a number assigned to the provisional document, or the existing non-provisional number feeds the transition. The operation recalculates prices and persists the validator and validation date as part of issue. |

The chronology exception tests the position of the provisional marker using a truth-value conversion. An absent marker and a marker starting at offset zero both satisfy that part of the draft exception. A conventional provisional reference with an opening parenthesis places the marker at offset one. Reproducing behaviour for imported references requires preserving their original spelling. A generic “dates always increase” rule would give different results.

Consider a customer who gives their own purchase order reference as `PO-174`. With the reference requirement enabled on invoice validation, the stored customer-reference field needs that value before issue. A reference typed only into a free-text invoice note leaves the field empty. With forced issue date enabled, an invoice prepared on the last day of April and first issued in May can receive a May invoice date and a newly calculated payment deadline. The customer reference and document number continue to identify different records in a reconciliation.

Sources are `htdocs/compta/facture/class/facture.class.php:3612–3666,3668–3745,3749–3824,6583–6622`. The [payment-terms chapter](../specification/financial/payment-terms-and-settlement-adjustments.md) describes the due-date calculation. The [numbering chapter](identity-and-numbering.md) describes how a series supplies the public reference.
