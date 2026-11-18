# Cash, billing and accounting events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. A numbered agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch rules and source keys.

| Event | Setup meaning or origin | Direct emission site | Specific subscriber branches |
| --- | --- | --- | --- |
| `ASSETMODEL_VALIDATE` | Named operation signal | `asset/class/assetmodel.class.php:494 (validate)` | No dedicated branch listed |
| `ASSET_ACCOUNTANCY_CODES_MODIFY` | Named operation signal | `asset/class/assetaccountancycodes.class.php:324 (updateAccountancyCodes)` | No dedicated branch listed |
| `ASSET_DEPRECIATION_OPTIONS_MODIFY` | Named operation signal | `asset/class/assetdepreciationoptions.class.php:581 (updateDeprecationOptions)` | No dedicated branch listed |
| `ASSET_VALIDATE` | Named operation signal | `asset/class/asset.class.php:1779 (validate)` | No dedicated branch listed |
| `BANKACCOUNTLINE_DELETE` | Named operation signal | `compta/bank/class/account.class.php:2446 (delete)` | No dedicated branch listed |
| `BANKACCOUNT_CREATE` | Named operation signal | `compta/bank/class/account.class.php:895 (create)` | No dedicated branch listed |
| `BANKACCOUNT_MODIFY` | Named operation signal | `compta/bank/class/account.class.php:1030 (update)` | No dedicated branch listed |
| `BILLREC_CREATE` | Template invoices created (dictionary row at line 218) | `compta/facture/class/facture-rec.class.php:557 (create)` | No dedicated branch listed |
| `BILLREC_DELETE` | Template invoices deleted (dictionary row at line 220) | `compta/facture/class/facture-rec.class.php:942 (delete)` | No dedicated branch listed |
| `BILLREC_MODIFY` | Template invoices update (dictionary row at line 219) | `compta/facture/class/facture-rec.class.php:627 (update)` · `compta/facture/class/facture-rec.class.php:2261 (setFrequencyAndUnit)` · `compta/facture/class/facture-rec.class.php:2320 (setNextDate)` · `compta/facture/class/facture-rec.class.php:2363 (setMaxPeriod)` · `compta/facture/class/facture-rec.class.php:2432 (setGeneratePdf)` · `compta/facture/class/facture-rec.class.php:2471 (setModelPdf)` · `compta/facture/class/facture-rec.class.php:2507 (setMailTemplate)` | No dedicated branch listed |
| `BILL_CANCEL` | Customer invoice canceled (dictionary row at line 66) | `compta/facture/class/facture.class.php:3579 (setCanceled)` | Agenda 499, Notification 146 |
| `BILL_CREATE` | Named operation signal | `compta/facture/class/facture.class.php:1181 (create)` | No dedicated branch listed |
| `BILL_DELETE` | Customer invoice deleted (dictionary row at line 69) | `compta/facture/class/facture.class.php:3201 (delete)` | No dedicated branch listed |
| `BILL_MODIFY` | Customer invoice modified (dictionary row at line 64) | `compta/facture/class/facture.class.php:2899 (update)` · `compta/facture/class/facture.class.php:3085 (set_ref_client)` · `compta/facture/class/facture.class.php:3145 (setInputReason)` · `compta/facture/class/facture.class.php:5087 (setDiscount)` · `compta/facture/class/facture.class.php:5937 (setFinal)` | No dedicated branch listed |
| `BILL_PAYED` | Customer invoice payed (dictionary row at line 65) | `compta/facture/class/facture.class.php:3431 (setPaid)` | Workflow 419, Agenda 481, Notification 148 |
| `BILL_SENTBYMAIL` | Customer invoice sent by mail (dictionary row at line 67) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 463 |
| `BILL_SUPPLIER_CANCELED` | Supplier invoice cancelled (dictionary row at line 96) | `fourn/class/fournisseur.facture.class.php:1814 (setCanceled)` | Agenda 1051 |
| `BILL_SUPPLIER_CREATE` | Named operation signal | `fourn/class/fournisseur.facture.class.php:845 (create)` | Agenda 965 |
| `BILL_SUPPLIER_DELETE` | Supplier invoice deleted (dictionary row at line 97) | `fourn/class/fournisseur.facture.class.php:1513 (delete)` | No dedicated branch listed |
| `BILL_SUPPLIER_MODIFY` | Supplier invoice modified (dictionary row at line 92) | `fourn/class/fournisseur.facture.class.php:1351 (update)` | No dedicated branch listed |
| `BILL_SUPPLIER_PAYED` | Supplier invoice payed (dictionary row at line 94) | `fourn/class/fournisseur.facture.class.php:1692 (setPaid)` | Agenda 1034 |
| `BILL_SUPPLIER_SENTBYMAIL` | Supplier invoice sent by mail (dictionary row at line 95) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 1016 |
| `BILL_SUPPLIER_UNPAYED` | Named operation signal | `fourn/class/fournisseur.facture.class.php:1757 (setUnpaid)` | No dedicated branch listed |
| `BILL_SUPPLIER_UNVALIDATE` | Supplier invoice unvalidated (dictionary row at line 93) | `fourn/class/fournisseur.facture.class.php:2109 (setDraft)` | Agenda 999 |
| `BILL_SUPPLIER_VALIDATE` | Supplier invoice validated (dictionary row at line 91) | `fourn/class/fournisseur.facture.class.php:1975 (validate)` | Workflow 309, Agenda 982 |
| `BILL_UNPAYED` | Named operation signal | `compta/facture/class/facture.class.php:3498 (setUnpaid)` | No dedicated branch listed |
| `BILL_UNVALIDATE` | Customer invoice unvalidated (dictionary row at line 68) | `compta/facture/class/facture.class.php:4198 (setDraft)` | Agenda 446 |
| `BILL_VALIDATE` | Customer invoice validated (dictionary row at line 63) | `compta/facture/class/facture.class.php:3966 (validate)` | Workflow 175, Agenda 429, Notification 147 |
| `BOOKKEEPING_CREATE` | Named operation signal | `accountancy/class/bookkeeping.class.php:503 (create)` · `accountancy/class/bookkeeping.class.php:822 (createStd)` | No dedicated branch listed |
| `BOOKKEEPING_DELETE` | Named operation signal | `accountancy/class/bookkeeping.class.php:1693 (delete)` · `accountancy/class/bookkeeping.class.php:1842 (deleteMvtNum)` | No dedicated branch listed |
| `BOOKKEEPING_MODIFY` | Named operation signal | `accountancy/class/bookkeeping.class.php:1598 (update)` | No dedicated branch listed |
| `CASHCONTROL_CLOSE` | Named operation signal | `compta/cashcontrol/class/cashcontrol.class.php:458 (close)` | No dedicated branch listed |
| `CASHCONTROL_VALIDATE` | Named operation signal | `compta/cashcontrol/class/cashcontrol.class.php:390 (valid)` | No dedicated branch listed |
| `CURRENCYRATE_CREATE` | Named operation signal | `multicurrency/class/currencyrate.class.php:142 (create)` | No dedicated branch listed |
| `CURRENCYRATE_DELETE` | Named operation signal | `multicurrency/class/currencyrate.class.php:277 (delete)` | No dedicated branch listed |
| `CURRENCYRATE_MODIFY` | Named operation signal | `multicurrency/class/currencyrate.class.php:243 (update)` | No dedicated branch listed |
| `CURRENCY_CREATE` | Named operation signal | `multicurrency/class/multicurrency.class.php:178 (create)` | No dedicated branch listed |
| `CURRENCY_DELETE` | Named operation signal | `multicurrency/class/multicurrency.class.php:361 (delete)` | No dedicated branch listed |
| `CURRENCY_MODIFY` | Named operation signal | `multicurrency/class/multicurrency.class.php:327 (update)` | No dedicated branch listed |
| `DISCOUNT_MODIFY` | Named operation signal | `core/class/discount.class.php:623 (link_to_invoice)` · `core/class/discount.class.php:663 (unlink_invoice)` | No dedicated branch listed |
| `DONATION_PAYMENT_CREATE` | Named operation signal | `don/class/paymentdonation.class.php:256 (create)` | No dedicated branch listed |
| `DONATION_PAYMENT_DELETE` | Named operation signal | `don/class/paymentdonation.class.php:471 (delete)` | No dedicated branch listed |
| `DONATION_PAYMENT_MODIFY` | Named operation signal | `don/class/paymentdonation.class.php:410 (update)` | No dedicated branch listed |
| `DON_CREATE` | Named operation signal | `don/class/don.class.php:468 (create)` | No dedicated branch listed |
| `DON_DELETE` | Named operation signal | `don/class/don.class.php:606 (delete)` | No dedicated branch listed |
| `DON_MODIFY` | Named operation signal | `don/class/don.class.php:557 (update)` | No dedicated branch listed |
| `DON_VALIDATE` | Named operation signal | `don/class/don.class.php:782 (valid_promesse)` | No dedicated branch listed |
| `LINEBILLREC_DELETE` | Named operation signal | `compta/facture/class/facture-rec.class.php:2613 (delete)` | No dedicated branch listed |
| `LINEBILLREC_MODIFY` | Named operation signal | `compta/facture/class/facture-rec.class.php:2804 (update)` | No dedicated branch listed |
| `LINEBILL_DELETE` | Named operation signal | `compta/facture/class/factureligne.class.php:834 (delete)` | No dedicated branch listed |
| `LINEBILL_INSERT` | Named operation signal | `compta/facture/class/factureligne.class.php:607 (insert)` | No dedicated branch listed |
| `LINEBILL_MODIFY` | Named operation signal | `compta/facture/class/factureligne.class.php:792 (update)` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_CREATE` | Named operation signal | `fourn/class/fournisseur.facture.ligne.class.php:799 (insert)` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_DELETE` | Named operation signal | `fourn/class/fournisseur.facture.ligne.class.php:425 (delete)` | No dedicated branch listed |
| `LINEBILL_SUPPLIER_MODIFY` | Named operation signal | `fourn/class/fournisseur.facture.ligne.class.php:582 (update)` | No dedicated branch listed |
| `LINESUPPLIERBILLREC_DELETE` | Named operation signal | `fourn/class/fournisseur.facture-rec.ligne.class.php:200 (delete)` | No dedicated branch listed |
| `LINESUPPLIERBILLREC_MODIFY` | Named operation signal | `fourn/class/fournisseur.facture-rec.ligne.class.php:380 (update)` | No dedicated branch listed |
| `LOCALTAX_CREATE` | Named operation signal | `compta/localtax/class/localtax.class.php:178 (create)` | No dedicated branch listed |
| `LOCALTAX_DELETE` | Named operation signal | `compta/localtax/class/localtax.class.php:330 (delete)` | No dedicated branch listed |
| `LOCALTAX_MODIFY` | Named operation signal | `compta/localtax/class/localtax.class.php:242 (update)` | No dedicated branch listed |
| `ORDER_CLASSIFY_UNBILLED` | Named operation signal | `commande/class/commande.class.php:3130 (classifyUnBilled)` | No dedicated branch listed |
| `ORDER_SUPPLIER_CLASSIFY_UNBILLED` | Named operation signal | `fourn/class/fournisseur.commande.class.php:1276 (classifyUnBilled)` | No dedicated branch listed |
| `PAYMENTSALARY_CREATE` | Named operation signal | `salaries/class/paymentsalary.class.php:303 (create)` | No dedicated branch listed |
| `PAYMENTSOCIALCONTRIBUTION_CREATE` | Named operation signal | `compta/sociales/class/paymentsocialcontribution.class.php:276 (create)` | No dedicated branch listed |
| `PAYMENTVAT_CREATE` | Named operation signal | `compta/tva/class/paymentvat.class.php:279 (create)` | No dedicated branch listed |
| `PAYMENT_ADD_TO_BANK` | Named operation signal | `compta/paiement/class/paiement.class.php:998 (addPaymentToBank)` | No dedicated branch listed |
| `PAYMENT_CUSTOMER_CREATE` | Named operation signal | `compta/paiement/class/paiement.class.php:682 (create)` | No dedicated branch listed |
| `PAYMENT_CUSTOMER_DELETE` | Named operation signal | `compta/paiement/class/paiement.class.php:767 (delete)` | No dedicated branch listed |
| `PAYMENT_SUPPLIER_CREATE` | Named operation signal | `fourn/class/paiementfourn.class.php:448 (create)` | No dedicated branch listed |
| `PAYMENT_SUPPLIER_DELETE` | Named operation signal | `fourn/class/paiementfourn.class.php:553 (delete)` | No dedicated branch listed |
| `PAYMENT_VARIOUS_CREATE` | Named operation signal | `compta/bank/class/paymentvarious.class.php:612 (create)` | No dedicated branch listed |
| `PAYMENT_VARIOUS_DELETE` | Named operation signal | `compta/bank/class/paymentvarious.class.php:391 (delete)` | No dedicated branch listed |
| `PAYMENT_VARIOUS_MODIFY` | Named operation signal | `compta/bank/class/paymentvarious.class.php:284 (update)` | No dedicated branch listed |
| `RECEPTION_BILLED` | Named operation signal | `reception/class/reception.class.php:2258 (setBilled)` | No dedicated branch listed |
| `SALARY_CREATE` | Named operation signal | `salaries/class/salary.class.php:572 (create)` | No dedicated branch listed |
| `SALARY_MODIFY` | Named operation signal | `salaries/class/salary.class.php:343 (update)` | No dedicated branch listed |
| `SHIPPING_BILLED` | Named operation signal | `expedition/class/expedition.class.php:3159 (setBilled)` | No dedicated branch listed |
| `SOCIALCONTRIBUTION_CREATE` | Named operation signal | `compta/sociales/class/chargesociales.class.php:318 (create)` | No dedicated branch listed |
| `SOCIALCONTRIBUTION_MODIFY` | Named operation signal | `compta/sociales/class/chargesociales.class.php:455 (update)` | No dedicated branch listed |
| `SUPPLIERBILLREC_CREATE` | Named operation signal | `fourn/class/fournisseur.facture-rec.class.php:546 (create)` | No dedicated branch listed |
| `SUPPLIERBILLREC_DELETE` | Named operation signal | `fourn/class/fournisseur.facture-rec.class.php:946 (delete)` | No dedicated branch listed |
| `SUPPLIERBILLREC_MODIFY` | Named operation signal | `fourn/class/fournisseur.facture-rec.class.php:641 (update)` | No dedicated branch listed |
| `TVA_ADDPAYMENT` | Named operation signal | `compta/tva/class/tva.class.php:684 (addPayment)` | No dedicated branch listed |
