# Recurring billing, direct debits and credit transfers

A recurring invoice template sets billing dates. A debit instruction asks a bank to collect money. A credit transfer instructs the bank to pay a supplier or employee. These have separate identifiers and lifecycles. Generating the invoice or the bank file produces no evidence of cash settlement. [Recurring invoice selector][recur] · [Order model][order]

## Bill on schedule

Scheduled and interactive generation select templates from the active entity with positive frequency, an unset or due next date through the end of the current server day, suspension off, and generated count below the cap (zero cap means unlimited). The new draft uses the scheduled date where available. A template can request validation, document generation and sending. Exchange rates can be refreshed during generation. The template stores its next date and generated count separately from the issued invoice. A collection request is an additional business record, even for periodic invoices. [Selection, generation and validation][recur] · [Template schedule update][schedule]

## Prepare and settle a bank file

| Phase | Inputs and authority | Writes and business outcome |
| --- | --- | --- |
| Select requested payments | Pending requests in the selected entity, source IDs, source kind, account, execution date. For invoice sources the generator selects validated, unpaid documents of positive gross. For salaries it selects unpaid, positive salary records. Requests already processed or carrying an external payment ID are excluded. | For invoice counterparties the generator joins the default bank identity of bank-account type. Eligible request amounts, party bank details and mandate data supply the file lines. A simulated run stops before persisting the real order. |
| Create a real order | Debit-order creation permission or bank-transfer creation permission. For real direct debit, accept sequence FRST (first), RCUR (recurring), OOFF (one-off), FNAL (final). Supply the selected requests and configured or explicit bank account. | Create batch reference and header, attach processed requests and line-to-source details. The shipped SEPA generators emit pain.008.001.02 for direct debit and pain.001.001.03 for credit transfer. Each includes transaction count and control sum. Direct-debit payment information includes sequence and requested collection date. Credit transfer includes requested execution date. |
| Mark transmitted | A sender with the direction-specific send permission records transmission method and date on a draft file. | Order becomes transmitted (1). This records the handoff. A separate operation takes the bank movement date. |
| Record bank credit or debit | Transmitted order, date on or after transmission, selected bank account. Direct-debit credit permission or credit-transfer debit permission. | Group allocations by customer/supplier, or by employee for salaries. Record invoice or salary payments with the order reference, update qualifying paid states, write corresponding bank movements and mark lines processed. The header reaches status 2, credited for collections or debited for outbound transfers. A payment or bank write error rolls back the settlement transaction. |
| Record returned customer debit | Existing debit-order line, rejection reason and date, originating order. | Record a negative payment for the rejected allocation, write the linked opposite bank movement and reopen the invoice. The original receipt stays available for tracing. |

The normal card workflow offers settlement only from transmitted state. The settlement implementation conditionally updates the header but does not test the affected-row count before processing payments. For a rebuild, make claiming the transition and posting its resulting cash rows one atomic operation sized to the order. That stronger replay guarantee is an implementation requirement for the rebuild. [Generation and eligibility][generate] · [Encoding and totals][encode] · [Action rights][rights] · [Settlement][settle] · [Rejection][reject]

### Worked acceptance cases

| Case | Given and operation | Observable result |
| --- | --- | --- |
| TR-ORD-01 | Template due today, 3 of 3 occurrences already generated. Run recurring billing. | Template excluded. Setting maximum to zero permits future due occurrences while active. |
| TR-ORD-02 | A 100.00 customer debit and a 50.00 debit for two distinct customers enter one real one-off order, one bank row per customer, both in EUR. | File has two transactions, control sum 150.00. Marking transmitted leaves cash outstanding. On settlement, two receipts allocate 100.00 and 50.00, each with the order reference. |
| TR-ORD-03 | Order transmitted 12 November. Attempt settlement with a bank movement date of 11 November. | Date guard rejects before creating payments. |
| TR-ORD-04 | Bank returns the first 100.00 debit after settlement. Record a rejection for that line. | The first invoice reopens, its negative allocation restores the 100.00 receivable and the linked counter-entry reverses its receipt in the bank. The other customer remains settled. |
| TR-ORD-05 | Outgoing transfer against an unpaid supplier invoice or a salary. | Selected source determines payee, allocation type and outgoing bank label. The same numeric terminal state means debited on this order. |

[Bank-order schema](../../schemas/treasury/bank-order.schema.json) · [One-off debit example](../../examples/treasury/bank-order--debit.valid.json). The normalized command captures one order kind and source category. Eligibility, actual mandate data, amount aggregation and lifecycle guards require the live records.

[recur]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/facture/class/facture-rec.class.php#L1390-L1546
[schedule]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/facture/class/facture-rec.class.php#L2279-L2308
[order]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/class/bonprelevement.class.php#L159-L217
[generate]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/class/bonprelevement.class.php#L1097-L1568
[encode]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/class/bonprelevement.class.php#L2049-L2252
[rights]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/card.php#L83-L193
[settle]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/class/bonprelevement.class.php#L590-L844
[reject]: https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/compta/prelevement/class/rejetprelevement.class.php#L123-L245
