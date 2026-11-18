# How operating events become journal entries

A sale, its customer payment and its bank statement can all refer to the same money. The sales journal recognizes revenue, tax and the receivable. The bank journal recognizes cash received and clears the receivable. Statement confirmation supplies bank reconciliation evidence. A source-to-ledger transfer preserves the original event's identity so that a later transfer can distinguish documents waiting to post from those already in the ledger.

## Sales with more than one deposit or a retention

A sales line uses the general account bound to its detail row, falling back to the applicable goods or services sales account when needed. Tax mapping uses the combination of tax percentage and tax-source code. Where buyer location participates in service tax determination, the lookup distinguishes buyers by country. A deposit invoice can use a separately configured deposit tax account. Other lines use the tax rule's sales-side account or the configured fallback.

When explicit deposit accounting on sales invoices is active and deposits are represented by invoices, the journal excludes deposit-consumption lines from the normal line selection. For a standard invoice it reads the applied-credit records whose originating document is a deposit invoice and whose description identifies a deposit. It accepts consumption linked directly to the invoice or to one of its lines. It accumulates every matching record once for the standard invoice, separately by amount excluding tax, tax and amount including tax. An ordinary credit note or a fixed commercial allowance does not enter this deposit reversal merely because the downstream invoice used it as a reduction.

For an invoice of 600 including 100 tax, suppose two prior deposits of 120 and 60 each contained 20% VAT. Together those applications move 150 of deposit principal and 30 of deposit tax out of their original deposit balances and reduce the gross customer receivable by 180. The invoice's remaining gross receivable is 420 before any other credits, retention or settlement. Ignoring the second deposit would overstate receivables by 60. Recognizing the deposit lines both in ordinary line totals and in the reversal block would count their effect twice.

Retained warranty follows a separate branch. When enabled with a positive percentage, each eligible line allocates its rounded gross amount times the retention percentage to the warranty balance and reduces the immediately due customer component by the same amount. An installation can restrict this operation to a final progress invoice. For a single eligible line with gross 1,200 and retention of 5%, 60 is retained and 1,140 goes to ordinary receivables. Invoice-level revenue stamp, when present and mapped, increases the customer amount once across the document's lines. Posting the sales journal requires accounting binding-write access.

Release references include `htdocs/accountancy/journal/sellsjournal.php:85–104,197–226,259–307,335–381,409–464,572–586,951–1036`.

## Purchases with recoverable, expensed or reverse-charged tax

Purchase journal candidates are beyond draft, belong to the applicable accounting source entity and start with positively bound supplier-invoice details. Standard, replacement, credit and progress invoices are eligible, as are deposit invoices when supplier deposits are represented as invoices. A second query examines candidate invoices for other nonzero gross lines with ordinary line type and no binding and flags the entire document. A bound portion of an incomplete invoice must not produce a partial journal posting.

The purchase expense or asset account comes from the bound detail. Tax lookup combines rate and source code with the supplier's country, falling back to the company's country when no supplier country is available. The tax rule's purchasing account supersedes the configured default. The normal recoverable-tax method debits the net purchase to its designated account and debits tax to separate accounts. When the setting to keep taxes with the line is active, the full gross amount goes to the expense account. The gross supplier control amount is accumulated in both cases.

For a supplier invoice of 100 plus tax of 20, the split gives debit purchase 100, debit tax 20 and credit supplier 120. The inclusive-expense setting instead gives debit purchase 120 and credit supplier 120. A charge may therefore appear as recoverable in the operational tax-detail report while the configured purchasing journal includes it in cost. The two reports answer different questions using different records.

For a flagged reverse-charge supplier invoice, the release enables the additional posting for the configured country conditions. The enterprise must have the French country setting or the explicit force-enable option. The supplier country must be in the configured European list or the setting must also include suppliers outside it. The additional charge uses the invoice line's gross amount times the product purchase tax rate, rounded to monetary precision. Local reverse-charge amounts use the corresponding product local-tax rates. Each goes to opposite sides of paired accounts. The tax dictionary's reverse-charge account, when present, overrides that side's configured fallback. These are application selection rules.

On a flagged supplier invoice for 200 with zero tax charged by the supplier and a product purchase tax rate of 20%, an eligible journal adds a 40 debit and a 40 credit for the self-assessed tax. The supplier still receives 200. If the accounts on both reverse-charge sides resolve to the same number, aggregation of the equal and opposite amounts on that account can leave zero for that tax component.

Release references include `htdocs/accountancy/journal/purchasesjournal.php:142–201,226–279,321–397,439–468,650–712`.

## Expenses owed to employees

The expense journal selects bound lines on non-draft expense reports. The date-range and accounting-start filters use the report's start date, independently of the option selecting the posting date. The posting date itself defaults to the expense report start and can instead use its end. A business trip that starts 29 May and ends 3 June can thus be selected in May while producing a June journal date. Already-posted selection uses the report identifier and expense-report source family.

A positive expense debits its bound cost account and separately recoverable taxes where configured by the journal. The gross employee amount credits the configured expense-report control account with the employee subsidiary identifier and label. Reimbursing the employee subsequently routes a separate event through the bank journal. Tax reporting for the reimbursement can use the payment date; transferring the claim itself to expenses does not record a repayment. Missing bindings on additional nonzero lines flag the report. The posting operation uses the accounting binding-write permission.

Release references include `htdocs/accountancy/journal/expensereportsjournal.php:133–164,186–244,252–280,308–349,370–409,421–460` and `htdocs/core/lib/tax.lib.php:1178–1216`.

## Bank journal source identity and routing

The bank-account master points to its accounting journal and ledger account. The journal selects transactions for accounts linked to that journal. Its date interval and accounting start date inspect operation date. A reconciliation-only selection requires the transaction's reconciled flag. Listing by value date does not override the operation date used for accounting. The source key for already-transferred detection is the bank transaction identifier and the bank document family.

When a payment method carries an accounting code, it overrides the account master's default bank ledger code. The linked business event determines the other side. Customer and supplier payments use the corresponding party controls and subsidiary codes. Expense reimbursements and salary payments can use employee controls, social charges use their charge mapping, and a miscellaneous payment can supply its own account before falling back to the bank transaction's entered account. A saved nonzero amount in the operating currency takes precedence over the bank account currency amount when constructing the base-currency movement.

A card receipt of 110 on a bank account normally assigned to a current-account ledger can therefore post to a card-clearing account if the card payment method has its own mapped account. If the customer invoice was already posted, the receipt clears the 110 customer receivable and increases the designated cash or clearing account. It does not recognize another sale. When a bank line has no usable business link or account information, the journal can expose an undefined counterpart, which needs an accounting assignment before the event can be represented faithfully.

Release references include `htdocs/accountancy/journal/bankjournal.php:88–93,149–211,311–382,439–521,540–656,682–718,779–900`.
