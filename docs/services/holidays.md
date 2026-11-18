# Leave requests

Leave requests have submission, approval, refusal, cancellation and reopening transitions. Their authorization depends on the employee and the rights of the actor. Balance entries and request state can both change during a transition.

The implementation locations below refer to `htdocs/holiday/class/api_holidays.class.php`.

## `get` — Read a leave request

**Arguments** `id`.

**Access** The decision uses right `holiday.read`, leave request record scope.

The method loads related business records.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.

Source lines `96–113`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `user_ids = ''`, `sqlfilters = ''`, `properties = ''`, `pagination_data = false`.

**Access** The decision uses one of `holiday.read` or `holiday.readall`.

The lookup uses the visible entity scope for `holiday`. The properties selector projects the returned fields. The method resolves descendant records.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `134–234`.

## `post` — Create a leave request

**Arguments** `request_data = null`.

The request-field validator requires `fk_user`, `date_debut`, `date_fin`.

**Access** The decision uses right `holiday.write`, right `holiday.writeall`.

The optional caller marker is placed in event context for synchronization. The method resolves descendant records.

**Result** The record identifier.

- `400` — access refused, required request field absent.
- `403` — access refused.
- `500` — business operation failed.

Source lines `248–286` with `_validate 821–834`.

## `put` — Update a leave request

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `holiday.write`, right `holiday.writeall`, leave request record scope, right `holiday.read`.

The optional caller marker is placed in event context for synchronization. The method resolves descendant records. Editing the request through this operation requires draft status.

**Result** A record with internal service properties removed.

- `400` — invalid request data, access refused.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `306–361` with `get 96–113`.

## `delete` — Delete a leave request

**Arguments** `id`.

**Access** The decision uses right `holiday.delete`, leave request record scope.

Only draft, cancelled or refused requests qualify for deletion.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — removal failed.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — removal failed.

Source lines `375–405`.

## `validate` — Validate a leave request

Route `POST {id}/validate`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `holiday.write`, leave request record scope, right `holiday.writeall`.

The method resolves descendant records and validates the record. The starting state must be draft. Validation moves the request to submitted status.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `426–458`.

## `approve` — Approve

Route `POST {id}/approve`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `holiday.approve`, leave request record scope, right `holiday.writeall`.

The method approves the record, writes a leave-balance log entry, and adjusts the leave balance. The method opens a database transaction and provides commit and rollback paths. The starting state must be validated. Approval records the approver and changes the request state. With immediate deduction, the handler counts working days using the employee’s country and half-day setting, deducts them from the balance of that leave type and logs the new balance. Month-end deduction defers this adjustment.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already approved).
- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `480–540`.

## `cancel` — Cancel

Route `POST {id}/cancel`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `holiday.write`, leave request record scope, one of `holiday.writeall` or `holiday.approve`.

The method resolves descendant records, dispatches the domain event, writes a leave-balance log entry, and adjusts the leave balance. The method opens a database transaction and provides commit and rollback paths. The starting state must be validated or approved. The request first records its old state. Reversing an approved request can restore the employee’s balance, while cancelling a request awaiting approval has no prior approval debit to restore.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already canceled).
- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `561–643`.

## `refuse` — Refuse

Route `POST {id}/refuse`.

**Arguments** `id`, `detail_refuse`, `notrigger = 0`.

**Access** The decision uses right `holiday.approve`, leave request record scope, right `holiday.writeall`.

A validated request can be refused with the supplied refusal detail. The request is then in refused state.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already refused).
- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `665–701`.

## `reopen` — Reopen the record

Route `POST {id}/reopen`.

**Arguments** `id`, `notrigger = 0`.

**Access** The decision uses right `holiday.write`, leave request record scope.

The method validates the record. Only a cancelled request can be reopened. The target state is validated, which returns it to the approval workflow.

**Result** A record with internal service properties removed.

- `400` — invalid request data.
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — leave missing.
- `500` — business operation failed.

Source lines `725–751`.
