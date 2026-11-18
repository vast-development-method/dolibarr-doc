# Parties, trade and service documents events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. An agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. The [subscriber register](../event-effects/event-selection.csv) gives the full selection rules, including configurable and generic handlers. See the [event contract](README.md) for shared dispatch and subscription rules.

| Event | Setup meaning or origin | Emitting operation | Specific subscriber branches |
| --- | --- | --- | --- |
| `COMPANY_CREATE` | Third party created (setup dictionary) | `societe.create` | Agenda, Automation connector |
| `COMPANY_DELETE` | Third party deleted (setup dictionary) | `societe.delete` | Payment provider |
| `COMPANY_LINK_SALE_REPRESENTATIVE` | Operation signal | `societe.add_commercial` | No dedicated branch listed |
| `COMPANY_MODIFY` | Third party update (setup dictionary) | `societe.update` · `societe.mergeCompany` | Agenda, Payment provider, Automation connector |
| `COMPANY_RIB_CREATE` | Third party payment information created (setup dictionary) | `companybankaccount.create` | No dedicated branch listed |
| `COMPANY_RIB_DELETE` | Third party payment information deleted (setup dictionary) | `companybankaccount.delete` | No dedicated branch listed |
| `COMPANY_RIB_MODIFY` | Third party payment information updated (setup dictionary) | `companybankaccount.update` | No dedicated branch listed |
| `COMPANY_SENTBYMAIL` | Mails sent from third party card (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `COMPANY_UNLINK_SALE_REPRESENTATIVE` | Operation signal | `societe.del_commercial` | No dedicated branch listed |
| `CONTACT_CREATE` | Contact address created (setup dictionary) | `contact.create` | Agenda, Directory synchronisation, Automation connector |
| `CONTACT_DELETE` | Contact address deleted (setup dictionary) | `contact.delete` | Directory synchronisation |
| `CONTACT_ENABLEDISABLE` | Operation signal | `contact.setstatus` | No dedicated branch listed |
| `CONTACT_MODIFY` | Contact address update (setup dictionary) | `contact.update` · `contact.update_perso` | Agenda, Directory synchronisation, Automation connector |
| `CONTACT_SENTBYMAIL` | Mails sent from third party card (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `CONTRACT_CREATE` | Operation signal | `contrat.create` | Party default contact roles |
| `CONTRACT_DELETE` | Contract deleted (setup dictionary) | `contrat.delete` | No dedicated branch listed |
| `CONTRACT_MODIFY` | Contract modified (setup dictionary) | `contrat.update` | Notification |
| `CONTRACT_REOPEN` | Operation signal | `contrat.reopen` | No dedicated branch listed |
| `CONTRACT_SENTBYMAIL` | Contract sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `CONTRACT_VALIDATE` | Contract validated (setup dictionary) | `contrat.validate` | Agenda |
| `EXPEDITIONLINEBATCH_CREATE` | Operation signal | `expeditionlinebatch.create` | No dedicated branch listed |
| `FICHINTER_CLASSIFY_BILLED` | Intervention set billed (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `FICHINTER_CLASSIFY_UNBILLED` | Intervention set unbilled (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `FICHINTER_CLOSE` | Intervention is done (setup dictionary) | `fichinter.setClose` | Agenda, Notification |
| `FICHINTER_CREATE` | Operation signal | `fichinter.create` | Agenda, Party default contact roles |
| `FICHINTER_DELETE` | Intervention is deleted (setup dictionary) | `fichinter.delete` | Agenda |
| `FICHINTER_MODIFY` | Intervention modified (setup dictionary) | `fichinter.update` · `fichinter.setRefClient` | Agenda, Notification |
| `FICHINTER_REOPEN` | Intervention opened (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `FICHINTER_SENTBYMAIL` | Intervention sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `FICHINTER_UNVALIDATE` | Operation signal | `fichinter.setDraft` | No dedicated branch listed |
| `FICHINTER_VALIDATE` | Intervention validated (setup dictionary) | `fichinter.setValid` | Agenda, Notification |
| `LINECONTRACT_ACTIVATE` | Operation signal | `contratligne.active_line` | No dedicated branch listed |
| `LINECONTRACT_CLOSE` | Operation signal | `contratligne.close_line` | No dedicated branch listed |
| `LINECONTRACT_DELETE` | Operation signal | `contrat.deleteLine` | No dedicated branch listed |
| `LINECONTRACT_INSERT` | Operation signal | `contrat.addline` · `contratligne.insert` | No dedicated branch listed |
| `LINECONTRACT_MODIFY` | Operation signal | `contrat.updateline` · `contratligne.update` | No dedicated branch listed |
| `LINEFICHINTER_CREATE` | Operation signal | `fichinterligne.insert` | No dedicated branch listed |
| `LINEFICHINTER_DELETE` | Operation signal | `fichinterligne.deleteLine` | No dedicated branch listed |
| `LINEFICHINTER_MODIFY` | Operation signal | `fichinterligne.update` | No dedicated branch listed |
| `LINEORDER_DELETE` | Operation signal | `orderline.delete` | No dedicated branch listed |
| `LINEORDER_INSERT` | Operation signal | `orderline.insert` | No dedicated branch listed |
| `LINEORDER_MODIFY` | Operation signal | `orderline.update` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_CREATE` | Operation signal | `fournisseur.insert` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_DELETE` | Operation signal | `fournisseur.delete` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_DISPATCH` | Operation signal | `fournisseur.dispatchProduct` | No dedicated branch listed |
| `LINEORDER_SUPPLIER_MODIFY` | Operation signal | `fournisseur.update` | No dedicated branch listed |
| `LINEPROPAL_DELETE` | Operation signal | `propaleligne.delete` | No dedicated branch listed |
| `LINEPROPAL_INSERT` | Operation signal | `propaleligne.insert` | No dedicated branch listed |
| `LINEPROPAL_MODIFY` | Operation signal | `propaleligne.update` | No dedicated branch listed |
| `LINERECEPTION_CREATE` | Operation signal | `receptionlinebatch.create` | No dedicated branch listed |
| `LINERECEPTION_DELETE` | Operation signal | `receptionlinebatch.delete` | No dedicated branch listed |
| `LINERECEPTION_INSERT` | Operation signal | `receptionlinebatch.insert` | No dedicated branch listed |
| `LINERECEPTION_MODIFY` | Operation signal | `receptionlinebatch.update` | No dedicated branch listed |
| `LINESHIPPING_DELETE` | Operation signal | `expeditionligne.delete` | No dedicated branch listed |
| `LINESHIPPING_INSERT` | Operation signal | `expeditionligne.insert` | No dedicated branch listed |
| `LINESHIPPING_MODIFY` | Operation signal | `expeditionligne.update` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_DELETE` | Operation signal | `supplier_proposal.delete` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_INSERT` | Operation signal | `supplier_proposal.insert` | No dedicated branch listed |
| `LINESUPPLIER_PROPOSAL_MODIFY` | Operation signal | `supplier_proposal.update` | No dedicated branch listed |
| `ORDER_CANCEL` | Customer order canceled (setup dictionary) | `commande.cancel` | Agenda, Notification |
| `ORDER_CLASSIFY_BILLED` | Customer order classify billed (setup dictionary) | `commande.classifyBilled` | Workflow, Agenda |
| `ORDER_CLOSE` | Customer order classify delivered (setup dictionary) | `commande.cloture` | Workflow, Agenda, Notification |
| `ORDER_CREATE` | Operation signal | `commande.create` | Notification, Party default contact roles, Automation connector |
| `ORDER_DELETE` | Customer order deleted (setup dictionary) | `commande.delete` | No dedicated branch listed |
| `ORDER_MODIFY` | Customer order modified (setup dictionary) | `commande.setDiscount` · `commande.set_date` · `commande.setDeliveryDate` · `commande.availability` · `commande.demand_reason` · `commande.set_ref_client` · `commande.update` | No dedicated branch listed |
| `ORDER_REOPEN` | Operation signal | `commande.set_reopen` | No dedicated branch listed |
| `ORDER_SENTBYMAIL` | Customer order sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `ORDER_SUPPLIER_APPROVE` | Purchase order request approved (setup dictionary) | `fournisseur.approve` | Agenda, Notification |
| `ORDER_SUPPLIER_CANCEL` | Purchase order request canceled (setup dictionary) | `fournisseur.cancel` | Agenda, Notification |
| `ORDER_SUPPLIER_CLASSIFY_BILLED` | Purchase order set billed (setup dictionary) | `fournisseur.classifyBilled` | Agenda |
| `ORDER_SUPPLIER_CREATE` | Operation signal | `fournisseur.create` | Agenda, Party default contact roles |
| `ORDER_SUPPLIER_DELETE` | Purchase order deleted (setup dictionary) | `fournisseur.delete` | No dedicated branch listed |
| `ORDER_SUPPLIER_MODIFY` | Purchase order request modified (setup dictionary) | `fournisseur.update` · `fournisseur.setDeliveryDate` · `fournisseur.set_id_projet` | No dedicated branch listed |
| `ORDER_SUPPLIER_RECEIVE` | Purchase order request received (setup dictionary) | `fournisseur.Livraison` | Agenda |
| `ORDER_SUPPLIER_REFUSE` | Purchase order request refused (setup dictionary) | `fournisseur.refuse` | Agenda, Notification |
| `ORDER_SUPPLIER_SENTBYMAIL` | Purchase order sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `ORDER_SUPPLIER_SUBMIT` | Purchase order request submited (setup dictionary) | `fournisseur.commande` | Agenda, Notification |
| `ORDER_SUPPLIER_VALIDATE` | Purchase order validated (setup dictionary) | `fournisseur.valid` | Agenda, Notification |
| `ORDER_UNVALIDATE` | Operation signal | `commande.setDraft` | No dedicated branch listed |
| `ORDER_VALIDATE` | Customer order validate (setup dictionary) | `commande.valid` | Agenda, Notification |
| `PROPAL_CANCEL` | Operation signal | `propal.setCancel` | No dedicated branch listed |
| `PROPAL_CLASSIFY_BILLED` | Customer proposal set billed (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROPAL_CLOSE_REFUSED` | Customer proposal closed refused (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda, Notification |
| `PROPAL_CLOSE_SIGNED` | Customer proposal closed signed (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Workflow, Agenda, Notification |
| `PROPAL_CREATE` | Operation signal | `propal.create` | Party default contact roles |
| `PROPAL_DELETE` | Customer proposal deleted (setup dictionary) | `propal.delete` | No dedicated branch listed |
| `PROPAL_MODIFY` | Customer proposal modified (setup dictionary) | `propal.update` · `propal.set_date` · `propal.set_echeance` · `propal.setDeliveryDate` · `propal.set_availability` · `propal.set_demand_reason` · `propal.set_ref_client` · `propal.setDraft` · `propal.availability` · `propal.demand_reason` | Agenda |
| `PROPAL_REOPEN` | Operation signal | `propal.reopen` | No dedicated branch listed |
| `PROPAL_SENTBYMAIL` | Commercial proposal sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROPAL_VALIDATE` | Customer proposal validated (setup dictionary) | `propal.valid` | Agenda, Notification |
| `PROPOSAL_SUPPLIER_CLOSE_REFUSED` | Price request closed refused (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROPOSAL_SUPPLIER_CLOSE_SIGNED` | Price request closed signed (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROPOSAL_SUPPLIER_CREATE` | Operation signal | `supplier_proposal.create` | Party default contact roles |
| `PROPOSAL_SUPPLIER_DELETE` | Price request deleted (setup dictionary) | `supplier_proposal.delete` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_MODIFY` | Price request modified (setup dictionary) | `supplier_proposal.update` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_REOPEN` | Operation signal | `supplier_proposal.reopen` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_SENTBYMAIL` | Price request sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROPOSAL_SUPPLIER_UNVALIDATE` | Operation signal | `supplier_proposal.setDraft` | No dedicated branch listed |
| `PROPOSAL_SUPPLIER_VALIDATE` | Price request validated (setup dictionary) | `supplier_proposal.valid` | Agenda |
| `RECEPTION_CLOSED` | Operation signal | `reception.setClosed` | Workflow |
| `RECEPTION_CREATE` | Operation signal | `reception.create` | No dedicated branch listed |
| `RECEPTION_DELETE` | Operation signal | `reception.delete` | No dedicated branch listed |
| `RECEPTION_MODIFY` | Operation signal | `reception.update` | No dedicated branch listed |
| `RECEPTION_REOPEN` | Operation signal | `reception.reOpen` | No dedicated branch listed |
| `RECEPTION_SENTBYMAIL` | Reception sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `RECEPTION_UNVALIDATE` | Operation signal | `reception.setDraft` | No dedicated branch listed |
| `RECEPTION_VALIDATE` | Reception validated (setup dictionary) | `reception.valid` | Workflow, Agenda |
| `SHIPPING_CANCEL` | Operation signal | `expedition.cancel` | No dedicated branch listed |
| `SHIPPING_CLOSED` | Operation signal | `expedition.setClosed` | Workflow |
| `SHIPPING_CREATE` | Operation signal | `expedition.create` | No dedicated branch listed |
| `SHIPPING_DELETE` | Shipping sent is deleted (setup dictionary) | `expedition.delete` | No dedicated branch listed |
| `SHIPPING_MODIFY` | Shipping modified (setup dictionary) | `expedition.update` | Notification |
| `SHIPPING_REOPEN` | Operation signal | `expedition.reOpen` | No dedicated branch listed |
| `SHIPPING_SENTBYMAIL` | Shipping sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `SHIPPING_VALIDATE` | Shipping validated (setup dictionary) | `expedition.valid` | Workflow, Agenda, Notification |
