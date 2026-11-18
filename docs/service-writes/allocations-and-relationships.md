# Allocation maps, assigned roles and attached files

## Allocating one payment

`POST /invoices/paymentsdistributed` takes an `arrayofamounts` object keyed by invoice ID. For each invoice, select one amount basis. Use `amount` for base currency or `multicurrency_amount` for invoice currency. Set the unused member to zero. The selected member can be an explicit payment or the string `remain`. Supplying a positive amount or `remain` on both sides produces HTTP 400.

For example, send the following allocation member alongside `datepaye`, `paymentid`, `closepaidinvoices` and `accountid`.

```json
{
  "arrayofamounts": {
    "41": {"amount": 40, "multicurrency_amount": 0},
    "57": {"amount": "remain", "multicurrency_amount": 0}
  }
}
```

The service fetches each invoice and computes its remaining balance on the selected currency basis. It subtracts previous payments, applied credits and applied deposits from gross, then rounds to the configured amount precision. If invoice 41 has gross 100, previous cash 25 and applied credit 5, its opening balance is 70. If invoice 57 has gross 80 and an applied deposit of 10, its balance is also 70. The request allocates 40 and 70, creating a payment of 110 in the common base currency and leaving balances of 30 and zero.

An allocation whose absolute amount exceeds the absolute balance is rejected unless `accepthigherpayment` is enabled. A credit-note allocation takes a negative sign. The payment holds base- and invoice-currency maps indexed by the same invoice IDs. Passing `yes` for `closepaidinvoices` requests closure through payment creation. When banking is enabled the service records the bank operation and then commits. For cheque payments the issuer is checked after the payment writer runs. The missing-issuer exception contains no local rollback call. Check payment identity, allocation, invoice state and bank entry after an interrupted request.

| Staff payment | Input and controls | Persisted result |
| --- | --- | --- |
| `POST /salaries/{id}/payments` | `paiementtype`, `datepaye`, `chid` and `amounts` are validated. Supply `accountid` when banking is enabled. Only the selected salary ID can be a key in `amounts`, for example `{"72":125}` for salary 72. | The salary payment receives the selected salary ID. An empty `fk_typepayment` takes the payment method from `paiementtype`. Payment creation and the optional bank entry precede commit. A failed writer or failed bank insertion causes an explicit rollback. |
| `POST /expensereports/{id}/payments` | The report must be approved. The action validates `fk_typepayment`, `datep` and `amounts`, and requires a positive `accountid` with banking enabled. It adds the rounded map values and compares their sum with gross less previous payments. | The underlying writer stores the sum in one payment row attached to the selected expense report. Map keys do not dispatch amounts across claims. A zero sum fails. Payment amendment verifies that the payment belongs to the selected report, protects its identity and adds the old payment back when calculating the replacement ceiling. |

## Catalogue combinations and supplier prices

`POST /products/{id}/variants` takes `features` as a map from attribute ID to value ID, for example `{"3":18,"5":24}`. The operation converts both sides to integer IDs, looks up the attributes and values and fetches the base product. It forwards the pair set, `weight_impact`, `price_impact`, `price_impact_is_percent` and optional `reference` and `ref_ext` to combination creation. A numeric impact is passed as a number. Other impact input can resolve to the writer's unspecified value.

`POST /products/ref/{ref}/variants` looks up the parent by reference and then searches for a combination with the same pairs. A match returns the existing combination ID. Thus submitting the same pair set with a revised impact through this operation does not revise the stored combination. The ID-addressed route invokes the creation writer directly.

`POST /products/{id}/purchase_prices` takes quantity, buying price and basis, supplier ID, supplier reference and the other named price conditions listed in the register. Its `localtaxes_array` is positional. Index 0 is the first tax type, 1 its rate, 2 the second tax type and 3 its rate. Supplier and product determine the commercial relationship. Quantity expresses the supplier's price threshold. Foreign currency, buying price and exchange inputs are separate named arguments.

### Updating several selling-price levels

With multiple selling prices enabled, `POST /products` and `PUT /products/{id}` read parallel maps keyed by level number from 1 through the configured limit. Each level uses `multiprices_base_type` and `multiprices_tva_tx`. A tax-exclusive level reads the sale and minimum from `multiprices` and `multiprices_min`. A tax-inclusive level reads `multiprices_ttc` and `multiprices_min_ttc`. A blank level basis falls back to the product's basis when writing the price.

Creation saves the product first and calls the level writer only for positive prices. It returns the product ID without checking each level writer's result. Updating starts from the existing product and issues a price write when a level's basis, tax rate or compared prices change. In the tax-exclusive branch the incoming minimum is compared to the previous **selling price**, which can trigger a write even when the stored minimum stayed the same. The update reports failure when its final writer result is nonpositive. Compare saved levels individually if processing stops partway through. The product amendment rejects an attempt to set `stock_reel`. Physical quantity changes through inventory movements.

## Project, task and calendar assignments

`POST /projects/{id}/contacts` assigns `fk_socpeople` to the project under `type_contact` and `source`. The handler's optional `affect_to_tasks` controls a second set of writes.

| Value of `affect_to_tasks` | Task assignment |
| --- | --- |
| Omitted or null | Adds the project contact only. |
| Empty array | Visits every task returned for this project. |
| Nonempty array of IDs | Visits only returned project tasks with an ID in the supplied set. An ID outside that selection adds no assignment. |

A project role of `PROJECTLEADER` yields the task role `TASKEXECUTIVE`. Other project roles yield `TASKCONTRIBUTOR`. The parent assignment precedes the task loop. A later task failure can leave the parent and earlier roles committed. Reconcile by project, task, person, role and source before retrying.

For `POST /agendaevents`, the owner and event type are mandatory. The record writer uses `userassigned` for internal participants and `socpeopleassigned` for contact participants. Each internal participant record identifies a user with `id` and can carry `mandatory`, `transparency` and `answer_status`. The user-assignment writer accepts a scalar entry as a person ID, skips duplicate positive user IDs within the insertion pass and defaults the three status values to zero when empty. With no user assignments the event writer supplies its owner. On event creation the contact map instead takes the contact ID from the key, such as `{"27":1}`, and writes all three status fields as zero. The assignment table records the event ID, participant type and participant ID separately. [Calendar operations](../services/agendaevents.md)

## Typed links, custom fields and attachments

| Write | Structure and effects |
| --- | --- |
| `POST /objectlinks` | Provide `fk_source`, `sourcetype`, `fk_target` and `targettype`. `relationtype` qualifies the link and `notrigger` controls event dispatch where supported. The endpoint checks access to the endpoints before the relationship writer operates. A numeric ID alone cannot identify a typed endpoint. [Document relationships](../platform/document-relationships.md) |
| `POST` or `PUT /setup/extrafields/{elementtype}/{attrname}` | The path identifies a definition, and `label` is checked explicitly. Definition members include `type`, `size`, `pos`, `default`, `required`, `unique`, `param`, `computed`, `alwayseditable`, `perms`, `list`, `help`, `langfile`, `totalizable` and `printable`. The writer receives `param` as definition-specific configuration. The handler reads `showintooltip` but does not pass it in the definition writer's argument list. Creation first checks whether the definition exists and returns 409 for a collision. |
| `POST /documents/upload` | Named arguments identify `modulepart`, `filename`, optional document reference or subdirectory, file content and encoding. The handler merges nonempty `array_options` into file metadata. These are values attached to the file record. The definition operation above changes how an object type describes custom fields. Overwrite permission, directory creation, position, cover, thumbnail and share each have their own arguments. [File operations](../services/documents.md) |
| `POST /tickets/newmessage` | The body requires `track_id` and `message`. Optional `attachments` is a list. Each member needs a usable `filename` to be processed and can supply `filecontent`, `fileencoding` and `mimetype`. The handler decodes `base64` when selected and otherwise uses the supplied bytes. An omitted content value becomes an empty string. |

For example, a ticket attachment member `{"filename":"note.txt","fileencoding":"base64","filecontent":"T0s=","mimetype":"text/plain"}` supplies the two bytes `OK`. An item without a usable name is skipped. The handler stages, moves and indexes each file before creating the message action with the resulting filenames and MIME types. An existing destination name receives a suffix. A later failure can therefore leave earlier files in place. Reconcile the action and its indexed files before replay. The default response contains the ticket ID. Supplying a truthy `return_action_id` returns both `ticket_id` and `action_id`.
