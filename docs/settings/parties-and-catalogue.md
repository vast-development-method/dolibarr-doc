# Party defaults and product policies

Two party settings shape new records. Four catalogue settings affect commercial line preparation and the units in which parties trade. Their consumers remain distinguishable even when both settings appear on the same product setup screen.

## Create the party and its associated person

| Operator control | Choice and effect |
| --- | --- |
| Default commercial status of a new party (`THIRDPARTY_CUSTOMERTYPE_BY_DEFAULT`) | Where customer/prospect management is available, the administrator's selector offers customer (1) or prospect and customer (3), subject to which roles are enabled. The party creation card combines the saved preference with the route used to create the party. Entering via a dedicated supplier, customer or prospect action can change the suggested flags. |
| Default roles for the associated contact (`CONTACTS_DEFAULT_ROLES`) | Where creation of a related address/contact is offered, the setup lets the administrator select external contact roles. When creating the individual contact from third-party details, the operation copies these roles to the associated contact. Role selection applies to this creation path. |

See [parties and contacts](../sales/parties-and-contacts.md) and the [party record dictionary](../records/parties.md).

## Choose how a document line uses the product

| Operator control | Choice and effect |
| --- | --- |
| Sell in customer pack sizes (`PRODUCT_USE_CUSTOMER_PACKAGING`) | Available with customer orders or invoicing. The control is unavailable for the incompatible multiple-price configurations identified on the screen. When enabled, a customer order line reads the item's pack size and adjusts a non-multiple to the next pack in magnitude. The order path reports when the quantity was adjusted. |
| Buy in supplier pack sizes (`PRODUCT_USE_SUPPLIER_PACKAGING`) | Available with supplier orders or invoicing. When enabled, the supplier price update stores the purchasing pack size on that offer, with 1 used for an empty value on this path. The supplier-order line uses the pack information when adjusting the ordered quantity. Customer and supplier pack sizes can therefore differ for the same item. |
| Use the supplier's description (`PRODUIT_FOURN_TEXTS`) | Enable to use a nonempty supplier-specific description on the supplier order line. If the supplier offer has no such description, the line-preparation flow retains the previously selected product text. Further line-description composition still applies. |
| Look up product text in the counterparty's language (`PRODUIT_TEXTS_IN_THIRDPARTY_LANGUAGE`) | The control appears when multilingual operation is enabled. The supplier-order form checks the chosen language, then the supplier's default language. It uses a translated description when present and falls back to the product's regular description. The customer-order form also consumes this translation policy. |

**Worked example.** An item is sold in packs of 4 and a particular supplier offers packs of 6. For a requested quantity of 13, the sales order rounds up to 16 and the supplier order to 18 when their respective settings apply. Existing exact multiples remain exact. For a supplier with a translated catalogue entry and a supplier-specific description, the purchase-line flow first resolves the language and then uses the nonempty supplier description when that option is active.

See [catalogue and supplier offers](../supply/catalogue.md), [purchasing](../supply/purchasing.md) and [sales proposals and orders](../sales/proposals-and-orders.md).
