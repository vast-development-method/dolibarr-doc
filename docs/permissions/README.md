# Permission declarations and effective access

The [permission index](declarations.csv) gives the numeric ID, declaring module, rights namespace, first- and second-level keys, English label, default grant, declaration condition and source line for **323 permission declarations**. The [descriptor index](descriptors.csv) covers all **84 eligible bundled module descriptors**, including 22 that declare no permission of their own. For example, the API descriptor contains a commented example for managing an API key. It adds zero permission definitions to this snapshot. API operations still enforce rights on the business resources they expose. [API descriptor](../reference/locators/permissions.md#ref-197e7cc03f7a) · [Stock movement API](../reference/locators/permissions.md#ref-0da08592f70f)

## Reading the indexes

| Column | Meaning |
| --- | --- |
| `id`, `id_expression` | Numeric ID registered with the permission store and the original expression used to derive it. The 40 computed IDs include arithmetic, decimal concatenation and a zero-padded suffix. For instance, the reception validate permission has ID 941603. |
| `namespace`, `first_level`, `second_level` | Keys on the permission definition, preserving spelling and case. A blank second level is a two-part capability such as stock/create (`stock`, `creer`). The runtime can map an application's alternative name to these keys. |
| `english_label`, `descriptor_label` | The former uses an English `Permission<ID>` entry when present, then an English translation of the descriptor label, then the descriptor text. The latter retains the declared fallback label or translation key. A site's advanced-permission UI can display an alternate label. |
| `default_grant` | Declared default for new users, with omitted defaults interpreted as zero by registration. The sole enabled default in this snapshot is 40001, reading currencies and rates. Installed defaults and explicit assignments can differ. |
| `declaration_guard` | Enclosing conditions that affect whether the declaration executes, in addition to enabling the module. Blank means the declaration itself is unconditional. |
| `setup_hidden_when` in the descriptor index | Expression explicitly assigned to the descriptor's visibility property. A blank value means no explicit assignment appeared. The property controls module setup visibility; it does not grant a capability. |

Three stock declarations (1008, 1014 and 1015) are guarded by feature level ≥ 2. They are included as conditional declarations for inventory reconciliation and lie outside the baseline functionality described by the business chapters. The supplier order's second approval is conditional on its threshold option. The supplier module split changes which descriptors are available. The shared supplier descriptor has an outer conditional declaration; the split order and invoice descriptors have a conditional setup-visibility flag. [Stock gates](../reference/locators/permissions.md#ref-93266818bc70) · [Shared supplier condition](../reference/locators/permissions.md#ref-ac7bebb33038) · [Order visibility](../reference/locators/permissions.md#ref-763c47f77d14) · [Conditional approval](../reference/locators/permissions.md#ref-e45ee9e507c7) · [Advanced labels](../reference/locators/permissions.md#ref-745826240a90)

## How a declaration becomes a decision

1. **Register a definition for an entity.** During module setup, registration checks the activation constant and materialises definitions. It uses a composite key of permission ID and entity. Administrative grants may also be initialised in this operation. [Registration](../reference/locators/permissions.md#ref-db44eb050902) · [Definition key](../reference/locators/permissions.md#ref-7db682fd09ea)
2. **Build the user's effective rights.** The loader reads user assignments and assignments through group membership, with entity filters. It filters advanced right groups when advanced permissions are disabled and caches loaded rights. New-user defaults are a distinct assignment path. [Rights loading](../reference/locators/permissions.md#ref-f3204ed1aa03) · [Default assignments](../reference/locators/permissions.md#ref-12626c89196f) · [User grants](../reference/locators/permissions.md#ref-e96f84ac72d6) · [Group grants](../reference/locators/permissions.md#ref-c1e6c98535df)
3. **Resolve a capability in context.** The runtime handles module names, aliases and the supplier split, checks module enablement, applies specific restrictions for external users and evaluates the permission levels. Field and record operations can impose further conditions. For example, the reception validation API requires creation permission and access to the target reception. With advanced permissions enabled the domain action also requires the advanced validation right. A default setting, an administrator flag or a category of permissions alone cannot establish that a particular user can act on a particular record. [Capability evaluation](../reference/locators/permissions.md#ref-4a2220021f82) · [Reception API](../reference/locators/permissions.md#ref-b36e417f596d) · [Domain validation guard](../reference/locators/permissions.md#ref-ed60afbd63ef)

### Acceptance cases

- A user with no direct grant but an applicable group assignment can load that capability for the active entity. An assignment in an unrelated entity does not satisfy the ordinary same-entity query.
- Receiving a purchase in normal and advanced permission modes can yield different outcomes with the same basic reception-create grant. Verify the route check, domain check and record scope separately.
- A newly activated module with zero declarations creates no new rights rows of its own. Its screens can still require another module's permission or administrative access.
- A user with a direct third-party export grant who is linked to an external third party is denied by the explicit external-user check for this operation.

[Six operation-level decisions](decisions.md) trace party access, order approval, invoice issue, expense delegation, project membership and warehouse visibility from the entry point to the underlying record.
