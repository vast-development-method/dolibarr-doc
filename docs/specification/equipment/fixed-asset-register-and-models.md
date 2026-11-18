# Fixed asset register and reusable models

A workshop buys two identical lathes. The supplier invoice records the purchase, the asset register records what the company capitalized, and a warehouse lot can identify a particular machine by serial number. Each record has its own identity and lifecycle. Acquiring an asset and moving a product into storage can happen on different dates and through different operations.

## Register data

| Record | Data and responsibility |
| --- | --- |
| Asset model | Entity-scoped reference, optional external reference, label, asset classification, notes and state. Associated model settings provide reusable defaults. The same model reference is unique within an entity. |
| Registered asset | Record ID, entity, provisional or final reference, label, quantity, optional model, new or second-hand acquisition, asset classification, acquisition and service start dates, public and private notes, status, authorship and validation data. |
| Value and retirement details | Acquisition value before tax, recovered VAT, optional earlier carrying data, disposal date, type and amount. A flag specifies whether the asset is depreciated. |
| External evidence | An asset can link to a supplier invoice on creation, maintain attached documents and generate an asset document. A customer invoice can be associated during disposal. |

Asset classification covers intangible, tangible, in progress and financial assets. “In progress” in **classification** can describe an asset still under construction. “In progress” in the asset's **workflow** means its register record has been validated. The two fields answer different questions. Quantity defaults to one. The record does not itself split quantity into serial numbers, warehouse balances, custodians or independent commissioning/disposal dates for individual units.

A single asset record of quantity two can describe the two lathes acquired together and treated alike. If one is sold and the other kept, the disposal operation acts on the register record as a whole. A business that needs independent retirement histories can represent the lathes as separate asset records and reuse the same model on both. That preserves individual identities without interpreting a stock movement or a project task as retirement.

The asset and model fields are in `htdocs/asset/class/asset.class.php` and `htdocs/asset/class/assetmodel.class.php`. Storage and keys are in `htdocs/install/mysql/tables/llx_asset-asset.sql` and `htdocs/install/mysql/tables/llx_asset_model-asset.key.sql`.

## Model application and entry into service

The asset's model picker offers enabled models from the applicable shared entities. The model has its own draft, enabled and disabled states. Enabling a model makes it available for selection and leaves existing registered assets in their own states. A new asset can also be created without a model. Entering a received asset with no separate start date defaults the service start to its acquisition date. If a machine purchased on May 2 first enters service on May 20, supplying both fields retains that distinction.

On creation, the operation writes the asset and, when a model was selected, copies its settings into the asset's own records. Depreciation options and accounting-code mappings are merged by mode and field, with model values overwriting the corresponding destination settings. A reported copy failure rolls back the creation transaction. Updating an asset to a different selected model applies those settings again. An ordinary edit that retains the same model does not rerun that copy. Updating the model later does not retroactively rewrite each asset's saved settings through this entry path.

Validation assigns the next asset reference when the current reference is provisional or empty. Otherwise the existing reference is kept. It sets the validator, validation time and in-progress status, invokes the validation event and arranges the document directory and indexed attachments under the definitive reference. A second validation of an already validated asset returns without issuing a new reference. The asset remains identifiable independently of any later change to its supplier's invoice reference.

Creation, copy-on-model-change and validation are in `htdocs/asset/class/asset.class.php` under `create`, `setDataFromAssetModel`, `update` and `validate`. Model state operations are in `htdocs/asset/class/assetmodel.class.php`.

## Disposal and reopening

The asset card restricts access to internal users with asset read permission. Draft editing, validation, disposal and reopening use asset write permission. Deletion uses the dedicated grant, with an exception allowing a writer to delete a draft. The card offers return to draft from an in-progress asset. A disposed asset has a separate reopen action.

Disposal records a date and disposal type and can link a customer invoice. It updates the asset, marks it disposed and recalculates the dependent schedule in a transaction. A failed update or recalculation can roll back the retirement. An already disposed asset does no further work through the ordinary disposal operation. An enabled automatic document refresh runs after a successful status transaction. Warehouse stock issuance and automatic creation of a customer sales invoice are outside this operation.

Reopening a disposed asset clears disposal date, amount and type, resets the associated flags, removes customer-invoice associations through the reopen path, returns the asset to in progress and recalculates its schedule. It does not recreate physical stock or assign the equipment to an operator. For instance, correcting an accidental disposal entry can restore the register state while the actual lathe remains physically at the customer's premises. That separate physical fact must come from the shipment, stock or asset custody evidence available to the business.

The status and permissions are in `htdocs/asset/card.php`. Disposal and reopening are in `htdocs/asset/class/asset.class.php` under `dispose` and `reopen`. The document tab is in `htdocs/asset/document.php`.
