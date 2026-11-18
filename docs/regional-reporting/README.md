# Regional reporting and evidence

A tax rate, a calculated liability, an internally recorded declaration and a file supplied to an authority represent different business facts. Use the producer and record identity below to trace a figure from its source to the output available.

| Question | Read |
| --- | --- |
| Why does a March VAT enquiry disagree with a March bank statement or with the VAT detail for the same dates? | [Periods, party thresholds, declarations and payments](period-and-authority-reconciliation.md) |
| What drives a local withholding report, and which country owns a reported sale or purchase? | [Local components and geographic reporting](local-components-and-geography.md) |
| What is carried by a rate code, an exemption reason or a recoverable-only tax treatment? | [Exemption metadata and stored tax](exemption-and-stored-tax.md) |
| How is the distributed French donor receipt populated and how does it differ from cash collected? | [French donation receipt](french-donation-receipt.md) |

## Outputs and their limits

| Business evidence | What the core operation creates or displays |
| --- | --- |
| VAT/month, party and rate enquiries | On-screen aggregations with transaction detail. The rate-detail screen also has a print presentation. The report handlers pass an empty export link. They have no submit-to-authority or authority-response operation. |
| VAT declaration card | An operator enters the record, including amount and dates, and can request a linked payment. The card has its own identity and status. These fields are supplied through the declaration workflow. Opening the turnover or rate report does not populate a signed statutory submission. |
| File linked to a declaration | The declaration's documents view holds uploaded material under its VAT reference and shows associated files. Keeping an authority acknowledgment here makes it retrievable with the declaration. Upload alone makes no assertion about who accepted the return. |
| Regional ledger extract | The accounting export registry includes two French audit-file layouts, selectors 1000 and 1010, with different mappings of piece and entry dates. These are journal records with debit/credit, supporting references and optional document evidence. Their scope and receipt by another party are separate from the VAT workflows. [Ledger export formats](../exports/ledger-layouts.md) |
| French donation certificate | A generated donor-facing HTML document with regional text, issuer settings, donor particulars and recorded amount. The writer persists a file. |
| Intra-community trade declarations | The DEB/DES module is a development feature with a conditional menu. The standard workflow provides no corresponding filing operation. |

For example, a tax officer can read the calculated monthly liability, record an authority declaration for a different amount because of an adjustment, attach the supporting document, and enter the later remittance. Those four facts each have an owner. To reproduce an as-of position, retain which trading rows entered the original calculation, the declaration's value date and amount, the actual payment dates, and any filing evidence associated with the declaration.

The [country setup reference](../localization/README.md) describes what the installer supplies in the chart and tax dictionaries.
