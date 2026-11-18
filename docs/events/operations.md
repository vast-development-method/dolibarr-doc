# Production, projects and stock events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. A numbered agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch rules and source keys.

| Event | Setup meaning or origin | Direct emission site | Specific subscriber branches |
| --- | --- | --- | --- |
| `ACTION_CLONE` | Named operation signal | `comm/action/class/actioncomm.class.php:846 (createFromClone)` | No dedicated branch listed |
| `ACTION_CREATE` | Action added (dictionary row at line 200) | `comm/action/class/actioncomm.class.php:770 (create)` | Notification 171 |
| `ACTION_DELETE` | Named operation signal | `comm/action/class/actioncomm.class.php:1184 (delete)` | No dedicated branch listed |
| `ACTION_MODIFY` | Named operation signal | `comm/action/class/actioncomm.class.php:1379 (update)` | No dedicated branch listed |
| `BOM_CLOSE` | BOM disabled (dictionary row at line 171) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_DELETE` | BOM deleted (dictionary row at line 173) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_REOPEN` | BOM reopen (dictionary row at line 172) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_UNVALIDATE` | BOM unvalidated (dictionary row at line 170) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `BOM_VALIDATE` | BOM validated (dictionary row at line 169) | `bom/class/bom.class.php:981 (validate)` | No dedicated branch listed |
| `MRP_MO_CANCEL` | MO canceled (dictionary row at line 178) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_DELETE` | MO deleted (dictionary row at line 177) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_PRODUCED` | MO produced (dictionary row at line 176) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MRP_MO_VALIDATE` | MO validated (dictionary row at line 175) | `mrp/class/mo.class.php:1244 (validate)` | No dedicated branch listed |
| `PRODUCTFOURNISSEURPRICE_VALIDATE` | Named operation signal | `product/class/productfournisseurprice.class.php:601 (validate)` | No dedicated branch listed |
| `PRODUCTLOT_CREATE` | Named operation signal | `product/stock/class/productlot.class.php:473 (create)` | No dedicated branch listed |
| `PRODUCTLOT_DELETE` | Named operation signal | `product/stock/class/productlot.class.php:758 (delete)` | No dedicated branch listed |
| `PRODUCTLOT_MODIFY` | Named operation signal | `product/stock/class/productlot.class.php:676 (update)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_CREATE` | Named operation signal | `variants/class/ProductAttribute.class.php:266 (create)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_DELETE` | Named operation signal | `variants/class/ProductAttribute.class.php:487 (delete)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_MODIFY` | Named operation signal | `variants/class/ProductAttribute.class.php:434 (update)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_CREATE` | Named operation signal | `variants/class/ProductAttributeValue.class.php:220 (create)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_DELETE` | Named operation signal | `variants/class/ProductAttributeValue.class.php:444 (delete)` | No dedicated branch listed |
| `PRODUCT_ATTRIBUTE_VALUE_MODIFY` | Named operation signal | `variants/class/ProductAttributeValue.class.php:391 (update)` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_CREATE` | Named operation signal | `fourn/class/fournisseur.product.class.php:721 (update_buyprice)` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_DELETE` | Named operation signal | `fourn/class/fournisseur.product.class.php:351 (remove_product_fournisseur_price)` | No dedicated branch listed |
| `PRODUCT_BUYPRICE_MODIFY` | Named operation signal | `fourn/class/fournisseur.product.class.php:612 (update_buyprice)` | No dedicated branch listed |
| `PRODUCT_CREATE` | Product or service created (dictionary row at line 131) | `product/class/product.class.php:1283 (create)` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_CREATE` | Named operation signal | `product/class/productcustomerprice.class.php:390 (create)` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_DELETE` | Named operation signal | `product/class/productcustomerprice.class.php:1113 (delete)` | No dedicated branch listed |
| `PRODUCT_CUSTOMER_PRICE_MODIFY` | Named operation signal | `product/class/productcustomerprice.class.php:966 (update)` | No dedicated branch listed |
| `PRODUCT_DELETE` | Product or service deleted (dictionary row at line 133) | `product/class/product.class.php:1876 (delete)` | No dedicated branch listed |
| `PRODUCT_DEL_MULTILANGS` | Named operation signal | `product/class/product.class.php:2190 (delMultiLangs)` | No dedicated branch listed |
| `PRODUCT_MODIFY` | Product or service modified (dictionary row at line 132) | `product/class/product.class.php:1773 (update)` · `product/class/product.class.php:2248 (setAccountancyCode)` | No dedicated branch listed |
| `PRODUCT_PRICE_MODIFY` | Named operation signal | `product/class/product.class.php:3051 (updatePrice)` | No dedicated branch listed |
| `PRODUCT_SET_MULTILANGS` | Named operation signal | `product/class/product.class.php:2160 (setMultiLangs)` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_ADD` | Named operation signal | `product/class/product.class.php:5142 (add_sousproduit)` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_DELETE` | Named operation signal | `product/class/product.class.php:5266 (del_sousproduit)` | No dedicated branch listed |
| `PRODUCT_SUBPRODUCT_UPDATE` | Named operation signal | `product/class/product.class.php:5201 (update_sousproduit)` | No dedicated branch listed |
| `PROJECT_CLOSE` | Project closed (dictionary row at line 153) | `projet/class/project.class.php:1306 (setClose)` | Agenda 1349 |
| `PROJECT_CREATE` | Project creation (dictionary row at line 148) | `projet/class/project.class.php:558 (create)` | Agenda 1261 |
| `PROJECT_DELETE` | Project deleted (dictionary row at line 151) | `projet/class/project.class.php:1118 (delete)` | Agenda 1338 |
| `PROJECT_MODIFY` | Project modified (dictionary row at line 150) | `projet/class/project.class.php:677 (update)` | Agenda 1298 |
| `PROJECT_SENTBYMAIL` | Project sent by mail (dictionary row at line 152) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Agenda 1320 |
| `PROJECT_VALIDATE` | Project validation (dictionary row at line 149) | `projet/class/project.class.php:1253 (setValid)` | Agenda 1280 |
| `RESOURCE_CREATE` | Named operation signal | `resource/class/dolresource.class.php:235 (create)` | No dedicated branch listed |
| `RESOURCE_DELETE` | Named operation signal | `resource/class/dolresource.class.php:567 (delete)` | No dedicated branch listed |
| `RESOURCE_MODIFY` | Named operation signal | `resource/class/dolresource.class.php:420 (update)` · `resource/class/dolresource.class.php:767 (updateElementResource)` | No dedicated branch listed |
| `STOCKTRANSFERLINE_VALIDATE` | Named operation signal | `product/stock/stocktransfer/class/stocktransferline.class.php:574 (validate)` | No dedicated branch listed |
| `STOCKTRANSFER_CLOSE` | Stock transfer closed (dictionary row at line 139) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification 177 |
| `STOCKTRANSFER_CREATE` | Stock transfer created (dictionary row at line 135) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification 173 |
| `STOCKTRANSFER_MODIFY` | Stock transfer modified (dictionary row at line 136) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification 174 |
| `STOCKTRANSFER_UNVALIDATE` | Stock transfer back to draft (dictionary row at line 138) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | Notification 176 |
| `STOCKTRANSFER_VALIDATE` | Stock transfer validated (dictionary row at line 137) | `product/stock/stocktransfer/class/stocktransfer.class.php:644 (validate)` | Notification 175 |
| `STOCK_MOVEMENT` | Named operation signal | `product/stock/class/mouvementstock.class.php:691 (_create)` | No dedicated branch listed |
| `TASK_COMMENT_CREATE` | Named operation signal | `core/class/comment.class.php:142 (create)` | No dedicated branch listed |
| `TASK_COMMENT_DELETE` | Named operation signal | `core/class/comment.class.php:319 (delete)` | No dedicated branch listed |
| `TASK_COMMENT_MODIFY` | Named operation signal | `core/class/comment.class.php:268 (update)` | No dedicated branch listed |
| `TASK_CREATE` | Task created (dictionary row at line 196) | `projet/class/task.class.php:500 (create)` | Agenda 1365 |
| `TASK_DELETE` | Task deleted (dictionary row at line 198) | `projet/class/task.class.php:872 (delete)` | Agenda 1402 |
| `TASK_MODIFY` | Task modified (dictionary row at line 197) | `projet/class/task.class.php:752 (update)` · `projet/class/task.class.php:2937 (mergeTask)` | Agenda 1384 |
| `TASK_TIMESPENT_CREATE` | Named operation signal | `projet/class/task.class.php:1681 (addTimeSpent)` | No dedicated branch listed |
| `TASK_TIMESPENT_DELETE` | Named operation signal | `projet/class/task.class.php:2274 (delTimeSpent)` | No dedicated branch listed |
| `TASK_TIMESPENT_MODIFY` | Named operation signal | `projet/class/task.class.php:2151 (updateTimeSpent)` | No dedicated branch listed |
| `WAREHOUSE_CREATE` | Named operation signal | `product/stock/class/entrepot.class.php:301 (create)` | No dedicated branch listed |
| `WAREHOUSE_DELETE` | Named operation signal | `product/stock/class/entrepot.class.php:451 (delete)` | No dedicated branch listed |
| `WAREHOUSE_MODIFY` | Named operation signal | `product/stock/class/entrepot.class.php:414 (update)` | No dedicated branch listed |
