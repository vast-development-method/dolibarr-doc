# Donations and receipts

## Donation register

One row represents a donation in `don` within the donation entity population. It can retain individual donor names, a free-text organisation name `societe`, or a linked party `fk_soc → societe.rowid`. Project `fk_projet → projet.rowid` and party are optional joins. The donation can therefore appear before a CRM party is linked. The donation area controls entry and has distinct read, write and delete grants.

The reference filter searches `don.ref` and `don.rowid`. The individual's name filter searches `lastname` and `firstname`. One organisation filter searches the donation's stored `societe` text, and the linked-party filter searches the party master's `nom`. A renamed master does not rewrite the captured donor text. All-field search includes the row ID, donation reference and personal names. The amount filter compares the donation's own `amount`. The inclusive date range and default descending order use `datedon`. The status list tests `fk_statut`, with the unrestricted choice leaving all states eligible. Standard transitions include draft, validated and paid. The register does not join settlement amounts into its primary row.

## Donation payment register

Each `payment_donation.rowid` is an individual receipt. Its `fk_donation` joins to `don.rowid`, and the linked donation must pass the donation entity filter. Method `fk_typepayment`, donation party `fk_soc` and bank movement `fk_bank` are optional joins. The bank-account row is reached through the movement's `fk_account`. This view reports `payment_donation.datep` and `payment_donation.amount`. A donation without any receipt appears only in the parent register.

| Receipt filter | Matched value |
| --- | --- |
| Reference | Receipt `rowid`. The linked donation has its own identifier. |
| Date and amount | Inclusive range on payment `datep` and numeric comparison on receipt `amount`. |
| Account and method | Positive bank-account ID compared to the movement's account. Method compared to the dictionary **code**. |
| Cheque or transfer | Text search on the receipt's `num_payment`. |
| Company | Linked party's `nom`. A free-text donor organisation without a corresponding party cannot match that predicate. |
| All-field search | The declared fields are payment row ID, linked party name, cheque/transfer reference and amount. This search requests a field spelt `num_paiement` while the payment record defines `num_payment`. In the standard schema that query can fail. The dedicated reference-number filter uses the stored spelling. |

A donation for 500 is entered in period A. Actual receipts are 200 in A and 150 in B, giving recorded receipts of 350 and 150 still to collect. Searching donations dated in A finds the original 500. Searching receipts paid in B finds 150. Filtering the receipts by the donor's newly linked master name can succeed even when the donation's free-text-organisation search for that same name does not. Cash collection, donor history and the remaining commitment can be reconciled through the common donation ID.
