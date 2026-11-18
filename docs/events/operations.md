# Production, projects and stock events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. An agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch and subscription rules.

| Event | Setup meaning or origin | Emitting operation | Specific subscriber branches |
| --- | --- | --- | --- |
| `ACTION_CLONE` | Operation signal | `actioncomm.createFromClone` | No dedicated branch listed |
| `ACTION_CREATE` | Action added (setup dictionary) | `actioncomm.create` | Notification |
| `ACTION_DELETE` | Operation signal | `actioncomm.delete` | No dedicated branch listed |
| `ACTION_MODIFY` | Operation signal | `actioncomm.update` | No dedicated branch listed |
| `BOM_CLOSE` | BOM disabled (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_DELETE` | BOM deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_REOPEN` | BOM reopen (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_UNVALIDATE` | BOM unvalidated (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_VALIDATE` | BOM validated (setup dictionary) | `bom.validate` | No dedicated branch listed |
| `MRP_MO_CANCEL` | MO canceled (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_DELETE` | MO deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_PRODUCED` | MO produced (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_VALIDATE` | MO validated (setup dictionary) | `mo.validate` | No dedicated branch listed |
| `PRODUCTFOURNISSEURPRICE_VALIDATE` | Operation signal | `productfournisseurprice.validate` | No dedicated branch listed |
| `PRODUCTLOT_CREATE` | Operation signal | `productlot.create` | No dedicated branch listed |
| `PRODUCTLOT_DELETE` | Operation signal | `productlot.delete` | No dedicated branch listed |
| `PRODUCTLOT_MODIFY` | Operation signal | `productlot.update` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_CREATE` | Operation signal | `ProductAttribute.create` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_DELETE` | Operation signal | `ProductAttribute.delete` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_MODIFY` | Operation signal | `ProductAttribute.update` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_CREATE` | Operation signal | `ProductAttributeValue.create` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_DELETE` | Operation signal | `ProductAttributeValue.delete` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_MODIFY` | Operation signal | `ProductAttributeValue.update` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_CREATE` | Operation signal | `fournisseur.update_buyprice` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_DELETE` | Operation signal | `fournisseur.remove_product_fournisseur_price` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_MODIFY` | Operation signal | `fournisseur.update_buyprice` | No dedicated branch listed |
| `PRODUCT_CREATE` | Product or service created (setup dictionary) | `product.create` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_CREATE` | Operation signal | `productcustomerprice.create` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_DELETE` | Operation signal | `productcustomerprice.delete` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_MODIFY` | Operation signal | `productcustomerprice.update` | No dedicated branch listed |
| `PRODUCT_DELETE` | Product or service deleted (setup dictionary) | `product.delete` | No dedicated branch listed |
| `PRODUCT_DEL_MULTILANGS` | Operation signal | `product.delMultiLangs` | No dedicated branch listed |
| `PRODUCT_MODIFY` | Product or service modified (setup dictionary) | `product.update` · `product.setAccountancyCode` | No dedicated branch listed |
| `PRODUCT_PRICE_MODIFY` | Operation signal | `product.updatePrice` | No dedicated branch listed |
| `PRODUCT_SET_MULTILANGS` | Operation signal | `product.setMultiLangs` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_ADD` | Operation signal | `product.add_sousproduit` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_DELETE` | Operation signal | `product.del_sousproduit` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_UPDATE` | Operation signal | `product.update_sousproduit` | No dedicated branch listed |
| `PROJECT_CLOSE` | Project closed (setup dictionary) | `project.setClose` | Agenda |
| `PROJECT_CREATE` | Project creation (setup dictionary) | `project.create` | Agenda |
| `PROJECT_DELETE` | Project deleted (setup dictionary) | `project.delete` | Agenda |
| `PROJECT_MODIFY` | Project modified (setup dictionary) | `project.update` | Agenda |
| `PROJECT_SENTBYMAIL` | Project sent by mail (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda |
| `PROJECT_VALIDATE` | Project validation (setup dictionary) | `project.setValid` | Agenda |
| `RESOURCE_CREATE` | Operation signal | `resource.create` | No dedicated branch listed |
| `RESOURCE_DELETE` | Operation signal | `resource.delete` | No dedicated branch listed |
| `RESOURCE_MODIFY` | Operation signal | `resource.update` · `resource.updateElementResource` | No dedicated branch listed |
| `STOCKTRANSFERLINE_VALIDATE` | Operation signal | `stocktransferline.validate` | No dedicated branch listed |
| `STOCKTRANSFER_CLOSE` | Stock transfer closed (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification |
| `STOCKTRANSFER_CREATE` | Stock transfer created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification |
| `STOCKTRANSFER_MODIFY` | Stock transfer modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification |
| `STOCKTRANSFER_UNVALIDATE` | Stock transfer back to draft (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification |
| `STOCKTRANSFER_VALIDATE` | Stock transfer validated (setup dictionary) | `stocktransfer.validate` | Notification |
| `STOCK_MOVEMENT` | Operation signal | `mouvementstock._create` | No dedicated branch listed |
| `TASK_COMMENT_CREATE` | Operation signal | `comment.create` | No dedicated branch listed |
| `TASK_COMMENT_DELETE` | Operation signal | `comment.delete` | No dedicated branch listed |
| `TASK_COMMENT_MODIFY` | Operation signal | `comment.update` | No dedicated branch listed |
| `TASK_CREATE` | Task created (setup dictionary) | `task.create` | Agenda |
| `TASK_DELETE` | Task deleted (setup dictionary) | `task.delete` | Agenda |
| `TASK_MODIFY` | Task modified (setup dictionary) | `task.update` · `task.mergeTask` | Agenda |
| `TASK_TIMESPENT_CREATE` | Operation signal | `task.addTimeSpent` | No dedicated branch listed |
| `TASK_TIMESPENT_DELETE` | Operation signal | `task.delTimeSpent` | No dedicated branch listed |
| `TASK_TIMESPENT_MODIFY` | Operation signal | `task.updateTimeSpent` | No dedicated branch listed |
| `WAREHOUSE_CREATE` | Operation signal | `entrepot.create` | No dedicated branch listed |
| `WAREHOUSE_DELETE` | Operation signal | `entrepot.delete` | No dedicated branch listed |
| `WAREHOUSE_MODIFY` | Operation signal | `entrepot.update` | No dedicated branch listed |
