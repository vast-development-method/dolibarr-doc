# Production orders

Creating or validating the order establishes its production record. Posting production pairs outputs with component consumption and can create stock movements. The service offers [bulk and per-plan-line posting](../production-control/posting-modes.md). With saved plan lines, bulk posting uses the full planned quantities even after an earlier partial fulfilment.

## `get` — Read a production order

Route `GET {id}`.

**Arguments** `id` (integer).

**Access** The decision uses right `mrp.read`, mrp record scope.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mo missing.

## `getCategories` — Read categories

Route `GET {id}/categories`.

**Arguments** `id` (integer), `sortfield = "s.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 0` (integer), `page = 0` (integer).

**Access** The decision uses right `categorie.lire`.

The method reads classification links.

**Result** The classifications assigned to the selected record.

- `403` — access refused.
- `503` — query or persistence failure.

## `index` — List records

**Arguments** `sortfield = "t.rowid"` (text), `sortorder = 'ASC'` (text), `limit = 100` (integer), `page = 0` (integer), `sqlfilters = ''` (text), `properties = ''` (text).

**Access** The decision uses right `mrp.read`.

The selection includes a representative-assignment restriction in its customer-visibility branch. The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

## `post` — Create a production order

**Arguments** `request_data = null` (collection).

**Access** The decision uses right `mrp.write`.

The optional caller marker is placed in event context for synchronization.

**Result** The record identifier.

- `400` — required request field absent.
- `403` — access refused.
- `500` — business operation failed.

## `put` — Update a production order

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `mrp.write`, mrp record scope, right `mrp.read`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mo missing.
- `500` — business operation failed.

## `validate` — Validate a production order

Route `POST {id}/validate`.

**Arguments** `id` (integer), `notrigger = 0` (integer).

**Access** The decision uses right `mrp.write`, mrp record scope.

The method validates the record.

**Result** A record with internal service properties removed.

- `304` — no transition applied (possibly already validated).
- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mo missing.
- `500` — business operation failed.

## `delete` — Delete a production order

**Arguments** `id` (integer).

**Access** The decision uses right `mrp.delete`, mrp record scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — missing operation rights, record outside the caller’s scope.
- `404` — mo missing.
- `500` — removal failed.

## `produceAndConsumeAll` — Produce and consume all

Route `POST {id}/produceandconsumeall`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `mrp.write`.

The optional caller marker is placed in event context for synchronization. The method attaches a source record, posts an outbound stock movement, posts an inbound stock movement, loads source-document line links, and changes the record state. The order must already be validated or in progress. The request can carry inventory labels and movement codes as well as consumption and output rows. Stock movement identifiers and production-order tracking rows are recorded separately. A stock movement is associated with the warehouse supplied for its row.

**Result** The record identifier.

- `403` — access refused.
- `404` — mo missing.
- `405` — operation unavailable.
- `500` — business operation failed, field objectid required in required, field qty required in required, field fk_warehouse must be > 0 in, product must be in batch, errorfieldrequiredforproduct warehouse required, errorfieldrequiredforproduct batch required.

## `produceAndConsume` — Produce and consume

Route `POST {id}/produceandconsume`.

**Arguments** `id` (integer), `request_data = null` (collection).

**Access** The decision uses right `mrp.write`.

The optional caller marker is placed in event context for synchronization. The method posts an outbound stock movement, posts an inbound stock movement, loads source-document line links, and changes the record state. The input distinguishes the planned line, actual quantity and warehouse. Output and component rows create opposite stock directions. Batch-managed products require the corresponding lot information where stock is posted. The command evaluates remaining quantities and the requested closing behavior.

**Result** The record identifier.

- `403` — access refused.
- `404` — mo missing.
- `405` — operation unavailable.
- `500` — business operation failed, field objectid required in required, unsupported state or operation, field qty with lower or higher then 0 required in required, field fk_warehouse required in required.
