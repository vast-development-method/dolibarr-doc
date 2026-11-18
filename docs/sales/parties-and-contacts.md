# Third parties, contacts and commercial ownership

A third party is the counterparty to a sale or purchase. A single organisation can buy goods and supply services under the same identity. A contact identifies a person. A sales representative assignment connects an internal user to the account. A document contact assignment identifies the person acting in a particular role on one document. These relationships have different keys, permissions and lifetimes. [Operator guide](../reference/locators/sales.md#ref-edcee52eb432) · [Party table](../reference/locators/sales.md#ref-0186859d69c5) · [Contact table](../reference/locators/sales.md#ref-3516959cad14)

## Records and keys

| Record | Identity and cardinality | Business meaning |
| --- | --- | --- |
| Third party | Entity and internal record ID. Customer code and supplier code are each unique within an entity. Name has an ordinary index. | Identification, separate customer and supplier terms, customer discount, VAT liability, addresses, statuses and accounting codes. A name match alone cannot identify a duplicate. |
| Commercial role | One customer/prospect code and one supplier flag per party | Customer/prospect code 0 = neither, 1 = customer, 2 = prospect, 3 = both. Combine any code with the supplier flag. Customer searches include 1 and 3, prospect searches include 2 and 3. |
| Contact | Entity and record ID, optionally linked to one party | A person's name, communication channels, position, address, visibility, activation status and prospect information can vary independently of the party. |
| Representative assignment | Party, internal user and role code | A party can have several representatives. Assignment drives the restricted internal user's party list. |
| Document contact | Document ID, contact role type and person ID form a unique assignment | The role type identifies the target document family, internal or external source and role code. Resolve the person ID against the source indicated by that type. The assignment also has its own status and can require a signature. |

[Party indexes](../reference/locators/sales.md#ref-ef39fdb34de1) · [Party search and role filters](../reference/locators/sales.md#ref-25488f91c4b5) · [Representative uniqueness](../reference/locators/sales.md#ref-8159e1f47da5) · [Role dictionary](../reference/locators/sales.md#ref-597aba14ba38) · [Document assignment](../reference/locators/sales.md#ref-0693ff08d7e1) · [Assignment uniqueness](../reference/locators/sales.md#ref-ca5169913b43)

## Commands and access

| Operation | Authority and inputs | Observable result |
| --- | --- | --- |
| Create party | Party create right. REST requires a name. A country code can resolve the dictionary ID. | Returns new party ID. Customer and supplier codes follow the configured code modules and uniqueness checks. |
| List parties | Party read right, entity scope, optional commercial-role/category filters | An external user is scoped to their party. An internal user lacking visibility over all customers sees assigned parties. A dual-role party appears in both corresponding role searches. |
| Attach or remove representative | Party and user must exist and party must be accessible. Add requires party create, remove requires party delete in these REST operations. | Changes assignment and hence the restricted user's list membership. The user identity survives removal. |
| Create or transfer contact | Contact create/edit right. Creation with a party or update to a different party checks access to the new party. Update also checks access to the existing contact. | The contact can be maintained separately. The contact list includes private contacts only for their creator, subject to the other list filters. |
| Set document roles | At supported document creation events the built-in role trigger loads the party's applicable default contact roles. | Existing identical person/role pairs are filtered before missing assignments are added. A default can therefore populate a new order without editing the party. |

[Party creation](../reference/locators/sales.md#ref-19528c303387) · [Code validation](../reference/locators/sales.md#ref-0fdc5782cade) · [Representative operations](../reference/locators/sales.md#ref-1572a3f4fff2) · [Contact list](../reference/locators/sales.md#ref-ded6c0129952) · [Contact writes](../reference/locators/sales.md#ref-7040aeda4f17) · [Default role trigger](../reference/locators/sales.md#ref-8fb2e5e07f5e)

### Becoming a customer

Signing a commercial proposal or validating a sales order invokes customer promotion. For an existing prospect, the default promotion retains prospect status and sets the customer bit, producing code 3. With `SOCIETE_DISABLE_PROSPECTSCUSTOMERS` enabled, promotion produces customer-only code 1. For a party with code 0 the result is 1. Supplier status is an independent field. Quoting, accepting a quotation and carrying a sale through to payment represent different facts. [Customer promotion](../reference/locators/sales.md#ref-bbbe786bed97) · [Proposal decision](../reference/locators/sales.md#ref-e61170f47897) · [Order validation](../reference/locators/sales.md#ref-bc96a0141bf7)

### Consolidating duplicate accounts

The merge command takes a **survivor** and a **source to remove**. It rejects the same ID, requires party create/edit permission and checks access to both records. The service combines commercial role flags, fills eligible empty fields on the survivor, concatenates designated notes and unions the two customer and supplier category sets. It redirects supported document references, asks registered extensions to redirect theirs, emits a party modification event and deletes the source. The database work runs inside a transaction. File moves use the filesystem and have a separate failure boundary. References held by custom integrations require their own mapping. [Merge contract](../reference/locators/sales.md#ref-362186628534) · [Merge sequence](../reference/locators/sales.md#ref-7c8fbf965dfe)

## Acceptance cases

| Case | Given and action | Expected observation |
| --- | --- | --- |
| CRM-1 | A prospect who supplies materials signs a quote, with dual roles enabled. | The same ID is now a customer, prospect and supplier. Both customer and prospect list filters find it. |
| CRM-2 | Repeat in a separate test with dual roles disabled. | Commercial code is 1, supplier status survives. |
| CRM-3 | Two contacts belong to one visible party. A contact is private and belongs to another creator. Query the contacts collection. | The ordinary contact appears. The private contact is omitted. |
| CRM-4 | An authorised user merges a prospect into a customer after both acquired sales documents. | The survivor has both commercial bits and the supported documents now point to it. Looking up the removed party fails. A self-merge returns HTTP 400. |
| CRM-5 | Two parties in the same entity have different names. Assign both the same non-null customer code. | The unique customer-code constraint prevents the second assignment. Neither display name nor contact email is an appropriate record key. |

The [party schema](../../schemas/sales/party.schema.json) describes a portable read projection. It represents prospect/customer roles with names, exposes the supplier flag separately and uses business IDs for links. A consumer must resolve references and enforce visibility at query time.
