# Parties, trade and service documents events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. A numbered agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch rules and source keys.

| Event | Setup meaning or origin | Direct emission site | Specific subscriber branches |
| --- | --- | --- | --- |
| `COMPANY_CREATE` | Third party created (dictionary row at line 39) | `societe/class/societe.class.php:1137 (create)` | Agenda 114 |
| `COMPANY_DELETE` | Third party deleted (dictionary row at line 42) | `societe/class/societe.class.php:2604 (delete)` | No dedicated branch listed |
| `COMPANY_LINK_SALE_REPRESENTATIVE` | Named operation signal | `societe/class/societe.class.php:3174 (add_commercial)` | No dedicated branch listed |
| `COMPANY_MODIFY` | Third party update (dictionary row at line 40) | `societe/class/societe.class.php:1882 (update)` · `societe/class/societe.class.php:6198 (mergeCompany)` | Agenda 132 |
| `COMPANY_RIB_CREATE` | Third party payment information created (dictionary row at line 43) | `societe/class/companybankaccount.class.php:418 (create)` | No dedicated branch listed |
| `COMPANY_RIB_DELETE` | Third party payment information deleted (dictionary row at line 45) | `societe/class/companybankaccount.class.php:639 (delete)` | No dedicated branch listed |
| `COMPANY_RIB_MODIFY` | Third party payment information updated (dictionary row at line 44) | `societe/class/companybankaccount.class.php:505 (update)` | No dedicated branch listed |
| `COMPANY_SENTBYMAIL` | Mails sent from third party card (dictionary row at line 41) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 155 |
| `COMPANY_UNLINK_SALE_REPRESENTATIVE` | Named operation signal | `societe/class/societe.class.php:3206 (del_commercial)` | No dedicated branch listed |
| `CONTACT_CREATE` | Contact address created (dictionary row at line 180) | `contact/class/contact.class.php:577 (create)` | Agenda 170 |
| `CONTACT_DELETE` | Contact address deleted (dictionary row at line 183) | `contact/class/contact.class.php:1323 (delete)` | No dedicated branch listed |
| `CONTACT_ENABLEDISABLE` | Named operation signal | `contact/class/contact.class.php:1877 (setstatus)` | No dedicated branch listed |
| `CONTACT_MODIFY` | Contact address update (dictionary row at line 181) | `contact/class/contact.class.php:769 (update)` · `contact/class/contact.class.php:988 (update_perso)` | Agenda 188 |
| `CONTACT_SENTBYMAIL` | Mails sent from third party card (dictionary row at line 182) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `CONTRACT_CREATE` | Named operation signal | `contrat/class/contrat.class.php:1180 (create)` | No dedicated branch listed |
| `CONTRACT_DELETE` | Contract deleted (dictionary row at line 102) | `contrat/class/contrat.class.php:1227 (delete)` | No dedicated branch listed |
| `CONTRACT_MODIFY` | Contract modified (dictionary row at line 100) | `contrat/class/contrat.class.php:1438 (update)` | Notification 172 |
| `CONTRACT_REOPEN` | Named operation signal | `contrat/class/contrat.class.php:683 (reopen)` | No dedicated branch listed |
| `CONTRACT_SENTBYMAIL` | Contract sent by mail (dictionary row at line 101) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 222 |
| `CONTRACT_VALIDATE` | Contract validated (dictionary row at line 99) | `contrat/class/contrat.class.php:576 (validate)` | Agenda 205 |
| `EXPEDITIONLINEBATCH_CREATE` | Named operation signal | `expedition/class/expeditionlinebatch.class.php:186 (create)` | No dedicated branch listed |
| `FICHINTER_CLASSIFY_BILLED` | Intervention set billed (dictionary row at line 124) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 585 |
| `FICHINTER_CLASSIFY_UNBILLED` | Intervention set unbilled (dictionary row at line 125) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 602 |
| `FICHINTER_CLOSE` | Intervention is done (dictionary row at line 129) | `fichinter/class/fichinter.class.php:784 (setClose)` | Agenda 619, Notification 158 |
| `FICHINTER_CREATE` | Named operation signal | `fichinter/class/fichinter.class.php:406 (create)` | Agenda 516 |
| `FICHINTER_DELETE` | Intervention is deleted (dictionary row at line 128) | `fichinter/class/fichinter.class.php:1136 (delete)` | Agenda 636 |
| `FICHINTER_MODIFY` | Intervention modified (dictionary row at line 123) | `fichinter/class/fichinter.class.php:484 (update)` · `fichinter/class/fichinter.class.php:1669 (setRefClient)` | Agenda 550, Notification 157 |
| `FICHINTER_REOPEN` | Intervention opened (dictionary row at line 126) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `FICHINTER_SENTBYMAIL` | Intervention sent by mail (dictionary row at line 127) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 567 |
| `FICHINTER_UNVALIDATE` | Named operation signal | `fichinter/class/fichinter.class.php:611 (setDraft)` | No dedicated branch listed |
| `FICHINTER_VALIDATE` | Intervention validated (dictionary row at line 122) | `fichinter/class/fichinter.class.php:681 (setValid)` | Agenda 533, Notification 156 |
| `LINECONTRACT_ACTIVATE` | Named operation signal | `contrat/class/contratligne.class.php:951 (active_line)` | No dedicated branch listed |
| `LINECONTRACT_CLOSE` | Named operation signal | `contrat/class/contratligne.class.php:1016 (close_line)` | No dedicated branch listed |
| `LINECONTRACT_DELETE` | Named operation signal | `contrat/class/contrat.class.php:1896 (deleteLine)` | No dedicated branch listed |
| `LINECONTRACT_INSERT` | Named operation signal | `contrat/class/contrat.class.php:1663 (addline)` · `contrat/class/contratligne.class.php:882 (insert)` | No dedicated branch listed |
| `LINECONTRACT_MODIFY` | Named operation signal | `contrat/class/contrat.class.php:1852 (updateline)` · `contrat/class/contratligne.class.php:756 (update)` | No dedicated branch listed |
| `LINEFICHINTER_CREATE` | Named operation signal | `fichinter/class/fichinterligne.class.php:239 (insert)` | No dedicated branch listed |
| `LINEFICHINTER_DELETE` | Named operation signal | `fichinter/class/fichinterligne.class.php:403 (deleteLine)` | No dedicated branch listed |
| `LINEFICHINTER_MODIFY` | Named operation signal | `fichinter/class/fichinterligne.class.php:300 (update)` | No dedicated branch listed |
| `LINEORDER_DELETE` | Named operation signal | `commande/class/orderline.class.php:366 (delete)` | No dedicated branch listed |
| `LINEORDER_INSERT` | Named operation signal | `commande/class/orderline.class.php:542 (insert)` | No dedicated branch listed |
| `LINEORDER_MODIFY` | Named operation signal | `commande/class/orderline.class.php:706 (update)` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_CREATE` | Named operation signal | `fourn/class/fournisseur.orderline.class.php:412 (insert)` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_DELETE` | Named operation signal | `fourn/class/fournisseur.orderline.class.php:558 (delete)` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_DISPATCH` | Named operation signal | `fourn/class/fournisseur.commande.class.php:2399 (dispatchProduct)` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_MODIFY` | Named operation signal | `fourn/class/fournisseur.orderline.class.php:498 (update)` | No dedicated branch listed |
| `LINEPROPAL_DELETE` | Named operation signal | `comm/propal/class/propaleligne.class.php:678 (delete)` | No dedicated branch listed |
| `LINEPROPAL_INSERT` | Named operation signal | `comm/propal/class/propaleligne.class.php:636 (insert)` | No dedicated branch listed |
| `LINEPROPAL_MODIFY` | Named operation signal | `comm/propal/class/propaleligne.class.php:847 (update)` | No dedicated branch listed |
| `LINERECEPTION_CREATE` | Named operation signal | `reception/class/receptionlinebatch.class.php:322 (create)` | No dedicated branch listed |
| `LINERECEPTION_DELETE` | Named operation signal | `reception/class/receptionlinebatch.class.php:656 (delete)` | No dedicated branch listed |
| `LINERECEPTION_INSERT` | Named operation signal | `reception/class/receptionlinebatch.class.php:431 (insert)` | No dedicated branch listed |
| `LINERECEPTION_MODIFY` | Named operation signal | `reception/class/receptionlinebatch.class.php:618 (update)` | No dedicated branch listed |
| `LINESHIPPING_DELETE` | Named operation signal | `expedition/class/expeditionligne.class.php:633 (delete)` | No dedicated branch listed |
| `LINESHIPPING_INSERT` | Named operation signal | `expedition/class/expeditionligne.class.php:466 (insert)` | No dedicated branch listed |
| `LINESHIPPING_MODIFY` | Named operation signal | `expedition/class/expeditionligne.class.php:841 (update)` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_DELETE` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:3510 (delete)` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_INSERT` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:3467 (insert)` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_MODIFY` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:3660 (update)` | No dedicated branch listed |
| `ORDER_CANCEL` | Customer order canceled (dictionary row at line 59) | `commande/class/commande.class.php:949 (cancel)` | Agenda 394, Notification 149 |
| `ORDER_CLASSIFY_BILLED` | Customer order classify billed (dictionary row at line 58) | `commande/class/commande.class.php:3082 (classifyBilled)` | Workflow 147, Agenda 377 |
| `ORDER_CLOSE` | Customer order classify delivered (dictionary row at line 56) | `commande/class/commande.class.php:858 (cloture)` | Workflow 117, Agenda 360, Notification 152 |
| `ORDER_CREATE` | Named operation signal | `commande/class/commande.class.php:1275 (create)` | Notification 150 |
| `ORDER_DELETE` | Customer order deleted (dictionary row at line 61) | `commande/class/commande.class.php:3555 (delete)` | No dedicated branch listed |
| `ORDER_MODIFY` | Customer order modified (dictionary row at line 57) | `commande/class/commande.class.php:2643 (setDiscount)` · `commande/class/commande.class.php:2702 (set_date)` · `commande/class/commande.class.php:2774 (setDeliveryDate)` · `commande/class/commande.class.php:2906 (availability)` · `commande/class/commande.class.php:2970 (demand_reason)` · `commande/class/commande.class.php:3033 (set_ref_client)` · `commande/class/commande.class.php:3514 (update)` | No dedicated branch listed |
| `ORDER_REOPEN` | Named operation signal | `commande/class/commande.class.php:796 (set_reopen)` | No dedicated branch listed |
| `ORDER_SENTBYMAIL` | Customer order sent by mail (dictionary row at line 60) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 411 |
| `ORDER_SUPPLIER_APPROVE` | Purchase order request approved (dictionary row at line 81) | `fourn/class/fournisseur.commande.class.php:1393 (approve)` | Agenda 830, Notification 162 |
| `ORDER_SUPPLIER_CANCEL` | Purchase order request canceled (dictionary row at line 85) | `fourn/class/fournisseur.commande.class.php:1507 (cancel)` | Agenda 869, Notification 160 |
| `ORDER_SUPPLIER_CLASSIFY_BILLED` | Purchase order set billed (dictionary row at line 87) | `fourn/class/fournisseur.commande.class.php:1227 (classifyBilled)` | Agenda 948 |
| `ORDER_SUPPLIER_CREATE` | Named operation signal | `fourn/class/fournisseur.commande.class.php:1784 (create)` | Agenda 796 |
| `ORDER_SUPPLIER_DELETE` | Purchase order deleted (dictionary row at line 88) | `fourn/class/fournisseur.commande.class.php:2509 (delete)` | No dedicated branch listed |
| `ORDER_SUPPLIER_MODIFY` | Purchase order request modified (dictionary row at line 80) | `fourn/class/fournisseur.commande.class.php:1895 (update)` · `fourn/class/fournisseur.commande.class.php:2867 (setDeliveryDate)` · `fourn/class/fournisseur.commande.class.php:2984 (set_id_projet)` | No dedicated branch listed |
| `ORDER_SUPPLIER_RECEIVE` | Purchase order request received (dictionary row at line 84) | `fourn/class/fournisseur.commande.class.php:2789 (Livraison)` | Agenda 913 |
| `ORDER_SUPPLIER_REFUSE` | Purchase order request refused (dictionary row at line 82) | `fourn/class/fournisseur.commande.class.php:1458 (refuse)` | Agenda 847, Notification 164 |
| `ORDER_SUPPLIER_SENTBYMAIL` | Purchase order sent by mail (dictionary row at line 86) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 930 |
| `ORDER_SUPPLIER_SUBMIT` | Purchase order request submited (dictionary row at line 83) | `fourn/class/fournisseur.commande.class.php:1568 (commande)` | Agenda 891, Notification 163 |
| `ORDER_SUPPLIER_VALIDATE` | Purchase order validated (dictionary row at line 79) | `fourn/class/fournisseur.commande.class.php:845 (valid)` | Agenda 813, Notification 161 |
| `ORDER_UNVALIDATE` | Named operation signal | `commande/class/commande.class.php:744 (setDraft)` | No dedicated branch listed |
| `ORDER_VALIDATE` | Customer order validate (dictionary row at line 55) | `commande/class/commande.class.php:612 (valid)` | Agenda 343, Notification 151 |
| `PROPAL_CANCEL` | Named operation signal | `comm/propal/class/propal.class.php:2922 (setCancel)` | No dedicated branch listed |
| `PROPAL_CLASSIFY_BILLED` | Customer proposal set billed (dictionary row at line 52) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 309 |
| `PROPAL_CLOSE_REFUSED` | Customer proposal closed refused (dictionary row at line 51) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 326, Notification 155 |
| `PROPAL_CLOSE_SIGNED` | Customer proposal closed signed (dictionary row at line 50) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Workflow 76, Agenda 292, Notification 154 |
| `PROPAL_CREATE` | Named operation signal | `comm/propal/class/propal.class.php:1457 (create)` | No dedicated branch listed |
| `PROPAL_DELETE` | Customer proposal deleted (dictionary row at line 53) | `comm/propal/class/propal.class.php:3195 (delete)` | No dedicated branch listed |
| `PROPAL_MODIFY` | Customer proposal modified (dictionary row at line 48) | `comm/propal/class/propal.class.php:1956 (update)` · `comm/propal/class/propal.class.php:2290 (set_date)` · `comm/propal/class/propal.class.php:2350 (set_echeance)` · `comm/propal/class/propal.class.php:2422 (setDeliveryDate)` · `comm/propal/class/propal.class.php:2481 (set_availability)` · `comm/propal/class/propal.class.php:2546 (set_demand_reason)` · `comm/propal/class/propal.class.php:2609 (set_ref_client)` · `comm/propal/class/propal.class.php:2987 (setDraft)` · `comm/propal/class/propal.class.php:3347 (availability)` · `comm/propal/class/propal.class.php:3411 (demand_reason)` | Agenda 257 |
| `PROPAL_REOPEN` | Named operation signal | `comm/propal/class/propal.class.php:2665 (reopen)` | No dedicated branch listed |
| `PROPAL_SENTBYMAIL` | Commercial proposal sent by mail (dictionary row at line 49) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 274 |
| `PROPAL_VALIDATE` | Customer proposal validated (dictionary row at line 47) | `comm/propal/class/propal.class.php:2182 (valid)` | Agenda 240, Notification 153 |
| `PROPOSAL_SUPPLIER_CLOSE_REFUSED` | Price request closed refused (dictionary row at line 75) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 779 |
| `PROPOSAL_SUPPLIER_CLOSE_SIGNED` | Price request closed signed (dictionary row at line 74) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 762 |
| `PROPOSAL_SUPPLIER_CREATE` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:1169 (create)` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_DELETE` | Price request deleted (dictionary row at line 76) | `supplier_proposal/class/supplier_proposal.class.php:2135 (delete)` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_MODIFY` | Price request modified (dictionary row at line 72) | `supplier_proposal/class/supplier_proposal.class.php:1537 (update)` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_REOPEN` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:1758 (reopen)` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_SENTBYMAIL` | Price request sent by mail (dictionary row at line 73) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 744 |
| `PROPOSAL_SUPPLIER_UNVALIDATE` | Named operation signal | `supplier_proposal/class/supplier_proposal.class.php:2015 (setDraft)` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_VALIDATE` | Price request validated (dictionary row at line 71) | `supplier_proposal/class/supplier_proposal.class.php:1608 (valid)` | Agenda 727 |
| `RECEPTION_CLOSED` | Named operation signal | `reception/class/reception.class.php:2212 (setClosed)` | Workflow 541 |
| `RECEPTION_CREATE` | Named operation signal | `reception/class/reception.class.php:422 (create)` | No dedicated branch listed |
| `RECEPTION_DELETE` | Named operation signal | `reception/class/reception.class.php:1523 (delete)` | No dedicated branch listed |
| `RECEPTION_MODIFY` | Named operation signal | `reception/class/reception.class.php:1417 (update)` | No dedicated branch listed |
| `RECEPTION_REOPEN` | Named operation signal | `reception/class/reception.class.php:2386 (reOpen)` | No dedicated branch listed |
| `RECEPTION_SENTBYMAIL` | Reception sent by mail (dictionary row at line 110) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 708 |
| `RECEPTION_UNVALIDATE` | Named operation signal | `reception/class/reception.class.php:2532 (setDraft)` | No dedicated branch listed |
| `RECEPTION_VALIDATE` | Reception validated (dictionary row at line 109) | `reception/class/reception.class.php:789 (valid)` | Workflow 540, Agenda 689 |
| `SHIPPING_CANCEL` | Named operation signal | `expedition/class/expedition.class.php:1788 (cancel)` | No dedicated branch listed |
| `SHIPPING_CLOSED` | Named operation signal | `expedition/class/expedition.class.php:3024 (setClosed)` | Workflow 454 |
| `SHIPPING_CREATE` | Named operation signal | `expedition/class/expedition.class.php:713 (create)` | No dedicated branch listed |
| `SHIPPING_DELETE` | Shipping sent is deleted (dictionary row at line 107) | `expedition/class/expedition.class.php:1985 (delete)` | No dedicated branch listed |
| `SHIPPING_MODIFY` | Shipping modified (dictionary row at line 105) | `expedition/class/expedition.class.php:1738 (update)` | Notification 165 |
| `SHIPPING_REOPEN` | Named operation signal | `expedition/class/expedition.class.php:3300 (reOpen)` | No dedicated branch listed |
| `SHIPPING_SENTBYMAIL` | Shipping sent by mail (dictionary row at line 106) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 671 |
| `SHIPPING_VALIDATE` | Shipping validated (dictionary row at line 104) | `expedition/class/expedition.class.php:1085 (valid)` | Workflow 453, Agenda 653, Notification 166 |
