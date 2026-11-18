# Document identity and reference numbering

A buyer can quote a purchase order number before a supplier ever sends an invoice. A cashier later needs a sales invoice number that can appear on a receipt or be searched in a ledger. Neither number identifies the row on its own across every kind of document. Preserve the object type, internal identifier, issuing entity and business reference separately. A customer's own purchase-order reference is another field.

## When a number becomes a business fact

Customer orders and invoices can start with a provisional reference. Validation uses the numbering model selected for the document. The highest sequence number already visible in scope is one of its inputs. Reading a proposed next number does not reserve a number. A draft preview and a committed validated reference serve different purposes. Once a related receipt, printed document or accounting transfer depends on the final reference, preserve the internal originating record as well as the displayed reference.

The order, proposal, customer invoice, shipment and supplier receipt tables each declare a unique pair of reference and entity. For these tables a second row of the same kind in the same entity cannot persist with the same reference. Identical text in two different document types is possible. The mask calculator itself reads prior references. When two simultaneous operations calculate the same candidate, the uniqueness constraint is a separate boundary. A consumer cannot treat its own next-number preview as proof of a successful allocation.

## Choosing the series

| Decision | Behaviour |
| --- | --- |
| Record kind | The configurable invoice model selects its standard, replacement, credit or deposit series according to the invoice type. A replacement can inherit the standard mask when its own mask is absent. An enabled deposit series and a credit series use their respective masks. An empty selected mask prevents generation. |
| Company scope | Invoice numbering asks for the entities sharing the invoice-number sequence. For another document kind, inspect the entity or sharing key supplied by its numbering model. A shared sequence can span several entities even when each entity enforces its own storage uniqueness. |
| Document date | The configurable invoice model passes the invoice date when available. The generic calculator falls back to the current date when its caller supplies none. A backdated document can therefore use a prior period's series. |
| Counter | A mask needs a general counter or a counter within the party token. The general counter normally needs three or more digits; a setting permits a shorter general counter. A nonempty party counter shorter than three digits fails its own check. |
| Per-party component | The source code uses the supplier code for supplier orders, invoices and payments, and the customer code for other party-based objects. It removes accents, truncates and pads the code to the requested width. Two contacts of the same party do not obtain separate party codes just because different people placed the orders. |
| Scope boundaries | The calculator selects matching formatted references and applies entity, period and caller-supplied filters where applicable. The generic routine can be used for numbers other than invoices. Two distinct masks that produce the same final references can still collide. |

## Periods, offsets and exhaustion

The zeros in the sequence token set its width. A reset option can start a new annual period, start at a specified fiscal month or restart every month. For a reset after January, the calculator needs adjacent year/month or month/year tokens to locate both parts of prior references. It rejects a one-digit year in that case. For a January reset the year alone can identify the period. The fiscal start option draws its month from company settings. Changing the company setting can therefore affect which past references qualify for the next number.

An offset sets the starting counter baseline. In next-number mode the counter is incremented and padded. When offset-only-on-first is disabled, a retrieved count below the offset can be raised to the offset before increment. An overflow beyond the configured width is an error. Increasing the width is a series design decision because it changes which strings match the format.

For example, use `INV{yyyy}{mm}-{000@99}` with no offset. If the November 2026 series contains `INV202611-001` and `INV202611-002`, the next candidate for another November invoice is `INV202611-003`. With an empty December series the first December candidate is `INV202612-001`. A December entry backdated to November consults the November scope. With three digits, the next value after `999` cannot be represented. A different rule applies when year and month are part of the displayed reference but the mask does not request a reset; display tokens alone do not define a monthly sequence.

## Evidence

- Generic masks, party tokens, period windows and offsets: `htdocs/core/lib/functions2.lib.php`, `get_next_value`, lines 805–1400.
- Invoice type, sharing key and effective date: `htdocs/core/modules/facture/mod_facture_mercure.php`, `getNextValue`. Customer orders: `htdocs/core/modules/commande/mod_commande_saphir.php`, `getNextValue`.
- Entity-level uniqueness: `htdocs/install/mysql/tables/llx_facture.key.sql`, `llx_commande.key.sql`, `llx_propal.key.sql`, `llx_expedition.key.sql` and `llx_reception.key.sql`.
