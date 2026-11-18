# When two postings overlap

A receipt or journal transfer can commit every row in its own transaction and still disagree with another committed transaction. The decisive questions are when each posting reads the old state, which keys the database enforces, and which amounts the operator can independently reconcile afterward.

| Review question | Evidence |
| --- | --- |
| Can two accepted receipts have two movement rows and the wrong quantity or average cost? | [Warehouse quantities, lot detail and valuation](warehouse-and-lot-balances.md) |
| What distinguishes a repeated source posting from a legitimate second journal leg? | [Journal transfers and piece allocation](journal-transfers.md) |
| What should an operator inspect after an uncertain outcome? | [Movement journal and counts](../warehouse-corrections/movement-journal-and-counts.md), [posted bookkeeping rows](../registers-accounts/bookkeeping.md) and [expense claim control totals](../expense-accounting/worked-reconciliation.md) |

## How the outcomes were established

Independent connections to an isolated InnoDB database ran the relevant business reads, signed movement inserts, balance assignments, piece selection and ledger-leg inserts. The fixture created the physical product, warehouse, lot, movement and bookkeeping tables with their declared types, constraints and indexes. Each connection controlled a separate transaction. A third connection read the committed balances in autocommit mode. The tested stock policy kept empty warehouse rows, used one stock entity and five decimals for average unit cost. Separate tests ran the public stock receipt method for an existing untracked warehouse balance and the ledger writer for a sales transfer. Each used two independent PHP processes. The other stock cases exercised the database decisions directly. For the sales case each process called `BookKeeping::create` for both legs inside an outer source transaction, checked an open fiscal period and used the numbering rule with an empty printable reference. A database adapter forwarded each process’s SQL to its own physical connection in both tests. The test used one entity, a sale of 100 without tax and two account codes. A fresh process repeated the first leg after commit. The document controller and extension triggers were outside these runs.

| Isolation and setting | Meaning for these observations |
| --- | --- |
| Repeatable read, snapshot conflict checking enabled | A transaction continues reading its snapshot. An attempted write can fail because another transaction has changed its target since that snapshot. This was the tested server's initial setting. For this engine the switch is `innodb_snapshot_isolation`. |
| Repeatable read, snapshot conflict checking disabled | A transaction can retain an earlier read and write a value calculated from it after another transaction commits. |
| Read committed, snapshot conflict checking enabled | A later ordinary lookup sees a newer committed row. An absolute value already calculated in application memory can still be stale. |
| Serializable | Shared reads and competing updates can deadlock. In the stock test one transaction survived, the database rejected the other, and a fresh transaction reread the new balances. |

These are observed schedules on the stated engine. Database engines, settings, document-level serialization and extensions can select different outcomes. A sequential retry after a known rollback, an overlapping independent request and a repeat after a successful but unacknowledged commit have different accounting effects.
