# Expense reports and reimbursements

Claim lines, approval decisions and reimbursement payments have separate identities. Validation, approval, denial, cancellation and setting a report paid are independently authorized transitions.

## `get` — Read an expense report

**Arguments** `id` (integer).

**Access** The decision uses right `expensereport.lire`, expense report record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `user_ids = ''` (text), `sqlfilters = ''` (text), `properties = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `expensereport.lire`.

The lookup uses the visible entity scope for `expensereport`. The properties selector projects the returned fields. The method resolves descendant records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create an expense report

**Arguments** `request_data = null` (collection).

The request-field validator requires `fk_user_author`, `date_debut`, `date_fin`.

**Access** The decision uses right `expensereport.creer`, right `expensereport.writeall_advance`.

The optional caller marker is placed in event context for synchronization. The method resolves descendant records.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `getLines` — Read document lines

Route `GET {id}/lines`.

**Arguments** `id` (integer).

**Access** The decision uses right `expensereport.lire`, expense report record scope.

**Result** A collection of line records for the selected parent.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

## `postLine` — Add a line

Route `POST {id}/line`.

**Arguments** `id` (integer), `request_data = null` (collection).

The request-field validator requires `date`, `fk_c_type_fees`, `qty`, `value_unit`, `vatrate`.

Named body fields used by the handler include `comments`, `fk_project`, `fk_c_exp_tax_cat`, `type`, `fk_ecm_files`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method adds a line. The report must be in draft. A claim line is a separate item on the employee’s expense report and can be changed while that draft is still open.

**Result** The identifier returned by the line insertion.

- `400` — required request field absent.
- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing.
- `500` — business operation failed.

## `putLine` — Amend a line

Route `PUT {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer), `request_data = null` (collection).

Named body fields used by the handler include `comments`, `fk_c_type_fees`, `fk_project`, `vatrate`, `qty`, `value_unit`, `date`, `fk_c_exp_tax_cat`, `fk_ecm_files`.

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method amends a line. The report must still be draft to edit a claim line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing, expense report line missing.
- `500` — business operation failed.

## `deleteLine` — Remove a line

Route `DELETE {id}/lines/{lineid}`.

**Arguments** `id` (integer), `lineid` (integer).

**Access** The decision uses right `expensereport.creer`, expense report record scope, right `expensereport.lire`.

The method removes a line. The report must still be draft to remove a claim line.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, record must be in draft.
- `404` — expense report missing, line missing.
- `500` — removal failed.

## `put` — Update an expense report

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `expensereport.creer`, expense report record scope, right `expensereport.lire`.

The optional caller marker is placed in event context for synchronization. The report can be amended in draft or refused state.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, access or input restriction.
- `404` — expense report missing.
- `500` — business operation failed.

## `delete` — Delete an expense report

**Arguments** `id` (integer).

**Access** The decision uses right `expensereport.supprimer`, expense report record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — removal failed.

## `setToDraft` — Return to draft

Route `POST {id}/settodraft`.

**Arguments** `id` (integer).

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method changes the record state.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already draft).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

## `validate` — Validate an expense report

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

## `approve` — Approve

Route `POST {id}/approve`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `expensereport.approve`, expense report record scope.

The method approves the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already approved).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

## `deny` — Deny

Route `POST {id}/deny`.

**Arguments** `id` (integer), `details` (text), `notrigger = 0` (integer).

**Access** The decision uses right `expensereport.approve`, expense report record scope.

The method records refusal.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already denied).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

## `setPaid` — Set paid

Route `POST {id}/setpaid`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `expensereport.to_paid`, expense report record scope.

The method records paid status.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already approved).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.
- `500` — business operation failed.

## `cancel` — Cancel

Route `POST {id}/cancel`.

**Arguments** `id` (integer), `detail` (text), `notrigger = 0` (integer).

**Access** The decision uses right `expensereport.creer`, expense report record scope.

The method cancels the record.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope, expense report already canceled.
- `404` — expense report missing.
- `500` — business operation failed.

## `getAllPayments` — Read all payments

Route `GET /payments`.

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer).

**Access** The decision uses right `expensereport.lire`.

The lookup uses the visible entity scope for `expensereport`. The method resolves descendant records.

**Result** A collection of matching records.

- `403` — access refused.
- `503` — query or persistence failure.

## `getPayment` — Read payment

Route `GET /payments/{pid}`.

**Arguments** `pid` (integer).

**Access** The decision uses right `expensereport.lire`, expense report record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — paymentexpensereport missing, expense report missing.

## `addPayment` — Add payment

Route `POST {id}/payments`.

**Arguments** `id` (integer), `request_data = null` (collection).

The request-field validator requires `fk_typepayment`, `datep`, `amounts`.

Named body fields used by the handler include `accountid`.

**Access** The decision uses right `expensereport.to_paid`, expense report record scope.

The method reads recorded payments, posts and links the bank entry, and records paid status. The method opens a database transaction and provides commit and rollback paths. The handler requires an approved report. Posting a reimbursement creates a payment for the report. Its financial allocation and bank entry can be reconciled separately from the approval decision.

**Result** The record identifier.

- `400` — required request field absent, expense report must be approved to be paid, amount exceeds the open balance, invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — expense report missing.

## `updatePayment` — Update payment

Route `PUT {id}/payments/{idp}`.

**Arguments** `id` (integer), `idp` (integer), `request_data = null` (collection).

**Access** The decision uses right `expensereport.to_paid`, expense report record scope, right `expensereport.lire`.

The method reads recorded payments.

**Result** A record with internal service properties removed.

- `400` — amount exceeds the open balance.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — payment of expense report missing, payment id does not belongs to the Expense id, expense report missing, paymentexpensereport missing.
- `500` — business operation failed.
