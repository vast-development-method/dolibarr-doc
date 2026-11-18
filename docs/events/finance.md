# Cash, billing and accounting events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. An agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. The [subscriber register](../event-effects/event-selection.csv) gives the full selection rules, including configurable and generic handlers. See the [event contract](README.md) for shared dispatch and subscription rules.

| Event | Setup meaning or origin | Emitting operation | Specific subscriber branches |
| --- | --- | --- | --- |
| `ASSETMODEL_VALIDATE` | Operation signal | `assetmodel.validate` | No dedicated branch listed |
| `ASSET_ACCOUNTANCY_CODES_MODIFY` | Operation signal | `assetaccountancycodes.updateAccountancyCodes` | No dedicated branch listed |
| `ASSET_DEPRECIATION_OPTIONS_MODIFY` | Operation signal | `assetdepreciationoptions.updateDeprecationOptions` | No dedicated branch listed |
| `ASSET_VALIDATE` | Operation signal | `asset.validate` | No dedicated branch listed |
| `BANKACCOUNTLINE_DELETE` | Operation signal | `account.delete` | No dedicated branch listed |
| `BANKACCOUNT_CREATE` | Operation signal | `account.create` | No dedicated branch listed |
| `BANKACCOUNT_MODIFY` | Operation signal | `account.update` | No dedicated branch listed |
| `BILLREC_CREATE` | Template invoices created (setup dictionary) | `facture-rec.create` | No dedicated branch listed |
| `BILLREC_DELETE` | Template invoices deleted (setup dictionary) | `facture-rec.delete` | No dedicated branch listed |
| `BILLREC_MODIFY` | Template invoices update (setup dictionary) | `facture-rec.update` · `facture-rec.setFrequencyAndUnit` · `facture-rec.setNextDate` · `facture-rec.setMaxPeriod` · `facture-rec.setGeneratePdf` · `facture-rec.setModelPdf` · `facture-rec.setMailTemplate` | No dedicated branch listed |
| `BILL_CANCEL` | Customer invoice canceled (setup dictionary) | `facture.setCanceled` | Agenda, Notification |
| `BILL_CREATE` | Operation signal | `facture.create` | Party default contact roles |
| `BILL_DELETE` | Customer invoice deleted (setup dictionary) | `facture.delete` | Immutable log |
| `BILL_MODIFY` | Customer invoice modified (setup dictionary) | `facture.update` · `facture.set_ref_client` · `facture.setInputReason` · `facture.setDiscount` · `facture.setFinal` | Immutable log |
| `BILL_PAYED` | Customer invoice payed (setup dictionary) | `facture.setPaid` | Workflow, Agenda, Notification |
| `BILL_SENTBYMAIL` | Customer invoice sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda, Immutable log |
| `BILL_SUPPLIER_CANCELED` | Supplier invoice cancelled (setup dictionary) | `fournisseur.setCanceled` | Agenda |
| `BILL_SUPPLIER_CREATE` | Operation signal | `fournisseur.create` | Agenda, Party default contact roles |
| `BILL_SUPPLIER_DELETE` | Supplier invoice deleted (setup dictionary) | `fournisseur.delete` | Immutable log |
| `BILL_SUPPLIER_MODIFY` | Supplier invoice modified (setup dictionary) | `fournisseur.update` | No dedicated branch listed |
| `BILL_SUPPLIER_PAYED` | Supplier invoice payed (setup dictionary) | `fournisseur.setPaid` | Agenda |
| `BILL_SUPPLIER_SENTBYMAIL` | Supplier invoice sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda, Immutable log |
| `BILL_SUPPLIER_UNPAYED` | Operation signal | `fournisseur.setUnpaid` | No dedicated branch listed |
| `BILL_SUPPLIER_UNVALIDATE` | Supplier invoice unvalidated (setup dictionary) | `fournisseur.setDraft` | Agenda |
| `BILL_SUPPLIER_VALIDATE` | Supplier invoice validated (setup dictionary) | `fournisseur.validate` | Workflow, Agenda, Immutable log |
| `BILL_UNPAYED` | Operation signal | `facture.setUnpaid` | No dedicated branch listed |
| `BILL_UNVALIDATE` | Customer invoice unvalidated (setup dictionary) | `facture.setDraft` | Agenda, Immutable log |
| `BILL_VALIDATE` | Customer invoice validated (setup dictionary) | `facture.validate` | Workflow, Agenda, Notification, Immutable log |
| `BOOKKEEPING_CREATE` | Operation signal | `bookkeeping.create` · `bookkeeping.createStd` | No dedicated branch listed |
| `BOOKKEEPING_DELETE` | Operation signal | `bookkeeping.delete` · `bookkeeping.deleteMvtNum` | No dedicated branch listed |
| `BOOKKEEPING_MODIFY` | Operation signal | `bookkeeping.update` | No dedicated branch listed |
| `CASHCONTROL_CLOSE` | Operation signal | `cashcontrol.close` | Immutable log |
| `CASHCONTROL_VALIDATE` | Operation signal | `cashcontrol.valid` | No dedicated branch listed |
| `CURRENCYRATE_CREATE` | Operation signal | `currencyrate.create` | No dedicated branch listed |
| `CURRENCYRATE_DELETE` | Operation signal | `currencyrate.delete` | No dedicated branch listed |
| `CURRENCYRATE_MODIFY` | Operation signal | `currencyrate.update` | No dedicated branch listed |
| `CURRENCY_CREATE` | Operation signal | `multicurrency.create` | No dedicated branch listed |
| `CURRENCY_DELETE` | Operation signal | `multicurrency.delete` | No dedicated branch listed |
| `CURRENCY_MODIFY` | Operation signal | `multicurrency.update` | No dedicated branch listed |
| `DISCOUNT_MODIFY` | Operation signal | `discount.link_to_invoice` · `discount.unlink_invoice` | No dedicated branch listed |
| `DONATION_PAYMENT_CREATE` | Operation signal | `paymentdonation.create` | Immutable log |
| `DONATION_PAYMENT_DELETE` | Operation signal | `paymentdonation.delete` | Immutable log |
| `DONATION_PAYMENT_MODIFY` | Operation signal | `paymentdonation.update` | No dedicated branch listed |
| `DON_CREATE` | Operation signal | `don.create` | No dedicated branch listed |
| `DON_DELETE` | Operation signal | `don.delete` | Immutable log |
| `DON_MODIFY` | Operation signal | `don.update` | Immutable log |
| `DON_VALIDATE` | Operation signal | `don.valid_promesse` | Immutable log |
| `LINEBILLREC_DELETE` | Operation signal | `facture-rec.delete` | No dedicated branch listed |
| `LINEBILLREC_MODIFY` | Operation signal | `facture-rec.update` | No dedicated branch listed |
| `LINEBILL_DELETE` | Operation signal | `factureligne.delete` | No dedicated branch listed |
| `LINEBILL_INSERT` | Operation signal | `factureligne.insert` | No dedicated branch listed |
| `LINEBILL_MODIFY` | Operation signal | `factureligne.update` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_CREATE` | Operation signal | `fournisseur.insert` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_DELETE` | Operation signal | `fournisseur.delete` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_MODIFY` | Operation signal | `fournisseur.update` | No dedicated branch listed |
| `LINESUPPLIERBILLREC_DELETE` | Operation signal | `fournisseur.delete` | No dedicated branch listed |
| `LINESUPPLIERBILLREC_MODIFY` | Operation signal | `fournisseur.update` | No dedicated branch listed |
| `LOCALTAX_CREATE` | Operation signal | `localtax.create` | No dedicated branch listed |
| `LOCALTAX_DELETE` | Operation signal | `localtax.delete` | No dedicated branch listed |
| `LOCALTAX_MODIFY` | Operation signal | `localtax.update` | No dedicated branch listed |
| `ORDER_CLASSIFY_UNBILLED` | Operation signal | `commande.classifyUnBilled` | No dedicated branch listed |
| `ORDER_SUPPLIER_CLASSIFY_UNBILLED` | Operation signal | `fournisseur.classifyUnBilled` | No dedicated branch listed |
| `PAYMENTSALARY_CREATE` | Operation signal | `paymentsalary.create` | No dedicated branch listed |
| `PAYMENTSOCIALCONTRIBUTION_CREATE` | Operation signal | `paymentsocialcontribution.create` | No dedicated branch listed |
| `PAYMENTVAT_CREATE` | Operation signal | `paymentvat.create` | No dedicated branch listed |
| `PAYMENT_ADD_TO_BANK` | Operation signal | `paiement.addPaymentToBank` | No dedicated branch listed |
| `PAYMENT_CUSTOMER_CREATE` | Operation signal | `paiement.create` | Immutable log |
| `PAYMENT_CUSTOMER_DELETE` | Operation signal | `paiement.delete` | Immutable log |
| `PAYMENT_SUPPLIER_CREATE` | Operation signal | `paiementfourn.create` | Immutable log |
| `PAYMENT_SUPPLIER_DELETE` | Operation signal | `paiementfourn.delete` | Immutable log |
| `PAYMENT_VARIOUS_CREATE` | Operation signal | `paymentvarious.create` | No dedicated branch listed |
| `PAYMENT_VARIOUS_DELETE` | Operation signal | `paymentvarious.delete` | No dedicated branch listed |
| `PAYMENT_VARIOUS_MODIFY` | Operation signal | `paymentvarious.update` | No dedicated branch listed |
| `RECEPTION_BILLED` | Operation signal | `reception.setBilled` | No dedicated branch listed |
| `SALARY_CREATE` | Operation signal | `salary.create` | No dedicated branch listed |
| `SALARY_MODIFY` | Operation signal | `salary.update` | No dedicated branch listed |
| `SHIPPING_BILLED` | Operation signal | `expedition.setBilled` | No dedicated branch listed |
| `SOCIALCONTRIBUTION_CREATE` | Operation signal | `chargesociales.create` | No dedicated branch listed |
| `SOCIALCONTRIBUTION_MODIFY` | Operation signal | `chargesociales.update` | No dedicated branch listed |
| `SUPPLIERBILLREC_CREATE` | Operation signal | `fournisseur.create` | No dedicated branch listed |
| `SUPPLIERBILLREC_DELETE` | Operation signal | `fournisseur.delete` | No dedicated branch listed |
| `SUPPLIERBILLREC_MODIFY` | Operation signal | `fournisseur.update` | No dedicated branch listed |
| `TVA_ADDPAYMENT` | Operation signal | `tva.addPayment` | No dedicated branch listed |
