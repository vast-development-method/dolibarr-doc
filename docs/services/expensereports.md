# Expense reports and reimbursements

Claim lines, approval decisions and reimbursement payments have separate identities. Validation, approval, denial, cancellation and setting a report paid are independently authorized transitions.

The implementation locations below refer to `htdocs/expensereport/class/api_expensereports.class.php`.

## `get` — Read an expense report

**Arguments** `id`.

**Access** The decision uses right `expensereport.lire`, expense report record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

Source lines `109–126`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `user_ids = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses right `expensereport.lire`.

The lookup uses the visible entity scope for `expensereport`. The properties selector projects the returned fields. The method resolves descendant records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `149–232`.

## `post` — Create an expense report

**Arguments** `request_data = null`.

The request-field validator requires `fk_user_author`, `date_debut`, `date_fin`.

**Access** The decision uses right `expensereport.creer`, right `expensereport.writeall_advance`.

The optional caller marker is placed in event context for synchronization. The method resolves descendant records.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `246–297` with `_validate 1258–1271`.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id`.

**Access** The decision uses right `expensereport.lire`, expense report record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

Source lines `315–335`.

## `postLine` — Add a line

Route `POST {id}/line`.

**Arguments** `id`, `request_data = null`.

The request-field validator requires `date`, `fk_c_type_fees`, `qty`, `value_unit`, `vatrate`.

Named body fields used by the handler include `comments`, `fk_project`, `fk_c_exp_tax_cat`, `type`, `fk_ecm_files`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method adds a line. The report must be in draft. A claim line is a separate item on the employee’s expense report and can be changed while that draft is still open.

**Result** The identifier returned by the line insertion.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `353–396` with `_validateLine 1303–1316`.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`, `request_data = null`.

Named body fields used by the handler include `comments`, `fk_c_type_fees`, `fk_project`, `vatrate`, `qty`, `value_unit`, `date`, `fk_c_exp_tax_cat`, `fk_ecm_files`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method amends a line. The report must still be draft to edit a claim line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing, expense report line missing.
- `500` — business operation failed.

Source lines `417–467`.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id`, `lineid`.

**Access** The decision uses right `expensereport.creer`, expense report record scope, right `expensereport.lire`.

The method removes a line. The report must still be draft to remove a claim line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing, line missing.
- `500` — removal failed.

Source lines `485–524` with `get 109–126`.

## `put` — Update an expense report

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `expensereport.creer`, expense report record scope, right `expensereport.lire`.

The optional caller marker is placed in event context for synchronization. The report can be amended in draft or refused state.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `543–592` with `get 109–126`.

## `delete` — Delete an expense report

**Arguments** `id`.

**Access** The decision uses right `expensereport.supprimer`, expense report record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — removal failed.

Source lines `606–631`.

## `setToDraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method changes the record state.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already draft).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `648–671`.

## `validate` — Validate an expense report

Route `POST {id}/validate`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `692–715`.

## `approve` — Approve

Route `POST {id}/approve`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `expensereport.approve`, expense report record scope.

The method approves the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already approved).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `737–760`.

## `deny` — Deny

Route `POST {id}/deny`.

**Arguments** `id`, `details`, `notrigger = 0`.

**Access** The decision uses right `expensereport.approve`, expense report record scope.

The method records refusal.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already denied).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `783–808`.

## `setPaid` — Set paid

Route `POST {id}/setpaid`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `expensereport.to_paid`, expense report record scope.

The method records paid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already approved).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `829–852`.

## `cancel` — Cancel

Route `POST {id}/cancel`.

**Arguments** `id`, `detail`, `notrigger = 0`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method cancels the record.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, expense report already canceled.
- `404` — expense report missing.
- `500` — business operation failed.

Source lines `871–895`.

## `getAllPayments` — Read all payments

Route `GET /payments`.

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`.

**Access** The decision uses right `expensereport.lire`.

The lookup uses the visible entity scope for `expensereport`. The method resolves descendant records.

**Result** A collection of matching records.

- `403` — access refused.
- `503` — query or persistence failure.

Source lines `914–960`.

## `getPayment` — Read payment

Route `GET /payments/{pid}`.

**Arguments** `pid`.

**Access** The decision uses right `expensereport.lire`, expense report record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — paymentexpensereport missing, expense report missing.

Source lines `974–997`.

## `addPayment` — Add payment

Route `POST {id}/payments`.

**Arguments** `id`, `request_data = null`.

The request-field validator requires `fk_typepayment`, `datep`, `amounts`.

Named body fields used by the handler include `accountid`.

**Access** The decision uses right `expensereport.to_paid`, expense report record scope.

The method reads recorded payments, posts and links the bank entry, and records paid status. The method opens a database transaction and provides commit and rollback paths. The handler requires an approved report. Posting a reimbursement creates a payment for the report. Its financial allocation and bank entry can be reconciled separately from the approval decision.

**Result** The record identifier.

- `400` — required request field absent, expense report must be approved to be paid, amount exceeds the open balance, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

Source lines `1013–1085` with `_validatepayment 1280–1293`.

## `updatePayment` — Update payment

Route `PUT {id}/payments/{idp}`.

**Arguments** `id`, `idp`, `request_data = null`.

**Access** The decision uses right `expensereport.to_paid`, expense report record scope, right `expensereport.lire`.

The method reads recorded payments.

**Result** A record with internal service properties removed.

- `400` — amount exceeds the open balance.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — payment of expense report missing, payment id does not belongs to the Expense id, expense report missing, paymentexpensereport missing.
- `500` — business operation failed.

Source lines `1102–1159` with `getPayment 974–997`.
