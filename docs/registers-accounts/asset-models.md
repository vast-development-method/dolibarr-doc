# Fixed asset models

One `asset_model` row defines a reusable asset model. The screen requires enabled asset management, an internal user and the asset-area access check. With ordinary permissions it checks the asset-read grant. With advanced permissions it additionally follows the model-specific read grant for the screen. Creation and deletion likewise use their respective ordinary or advanced model grants.

| Selection | Effect |
| --- | --- |
| Organisation | Filter `asset_model.entity` against entities accessible for asset models. |
| Name | Global keyword search targets the model reference and label. Direct filters can also use the external reference, import key and enabled text fields. |
| Class | Select intangible (0), tangible (1), in-progress (2) or financial (3). The zero choice is defined and remains selectable. |
| Availability | Draft (0), enabled (1) and disabled (9) are distinct states. The all-states sentinel −1 skips this predicate. |
| Stewardship | Creator and modifier use selector IDs. Creation and modification dates each accept an inclusive start and end. |
| Configured fields | If configured, the model's additional values are left-joined on the model ID and can contribute predicates. |

The base model field declarations have no country selector. A generic country default in list preparation therefore adds no country condition for this configuration. The list queries model headers and ordinarily sorts them by ascending ID. No base measure is marked for summation. A model referenced by five assets still appears once without a custom join that changes the row count. Selecting enabled on this register answers which templates can be used. To value the five actual assets, select their `fk_asset_model` in the [fixed asset register](assets.md).
