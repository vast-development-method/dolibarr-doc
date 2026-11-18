# Reading the ERP specification

A business operation starts with a particular actor, company, record and configuration. Its contract describes the admission decision, calculation, changes to durable records, failure outcome and downstream effects. A sales order, shipment, invoice, payment and ledger entry can refer to the same trade while each retains its own identity, date and state.

Worked transactions use illustrative business dates. An approval time, stock movement date, bank value date and journal date can legitimately differ for the same transaction.

Use the [record dictionary](records/README.md) for the roles of stored records, the [relational model](relational-model/README.md) for columns, keys and constraints, the [business specification](specification/README.md) for operating rules, and the [coverage register](coverage/checkpoint.md) for the boundaries of the documented behaviour.
