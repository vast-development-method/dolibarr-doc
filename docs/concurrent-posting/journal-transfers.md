# Two accounting transfers for the same source

The sales journal obtains eligible invoice lines, prepares debit and credit groups and transfers each invoice in its own transaction. An eligible source with gross 100, no tax and one revenue account yields one receivable debit of 100 and one revenue credit of 100. A successful posting makes the source disappear from the normal pending transfer selection.

## Three identities in the transfer

| Stage | Decision | Consequence |
| --- | --- | --- |
| Pending sales journal | The normal pending selection excludes source invoice IDs already present in bookkeeping with document type `customer_invoice`. | An invoice with any such leg can leave the queue. Its absence establishes neither completeness nor agreement with its issued amount. |
| Individual leg | The writer checks the current entity, `doc_type`, `fk_doc`, `numero_compte` and `label_operation`. A nonempty subsidiary account adds `subledger_account`. The detailed-source setting `ACCOUNTANCY_ENABLE_FKDOCDET` adds `fk_docdet`. Configured profit or loss accounts bypass the ordinary duplicate test. | An open fiscal period and valid account admit a candidate leg. A positive prior count rejects that leg. Debit, credit, amount, journal and piece number are outside the duplicate predicate. A label or account change can change the result of this lower-level check. |
| Piece and reference | A lookup uses document type, source ID, source reference and entity, plus the detail ID when enabled. If it finds a leg, the writer reuses the piece and reference. Otherwise it reads the entity's maximum `piece_num`, adds one and requests a reference under the selected numbering rule. An empty allocation starts at piece 1. | Multiple accounting legs can legitimately share the same piece. The piece/entity index, source indexes and printable-reference index are ordinary indexes. They do not reserve a source or implement a unique sequence. |

Each leg has its own row ID. It can join an outer source transaction. The sales journal compares its debit and credit totals before committing the source. A leg failure or unequal sides rolls that invoice's transaction back. Earlier separately committed invoices in the same batch retain their entries. A caller re-entering after a failure can examine each source independently.

## Repeating a 100-unit sale

Two independent PHP processes passed the receivable and revenue legs of invoice 41 to the ledger writer. Each held an outer transaction for both legs. They waited for each other after the first piece allocation lookup and the second duplicate-count query. Both processes had read an empty ledger for the first leg, both saw their own first leg when assigning the second leg’s piece and neither saw a competing match in time to reject it. The observer obtained the same results under read committed and both tested repeatable-read conflict settings.

| Observation after both commits | Result |
| --- | ---: |
| Source invoice gross | 100 |
| Distinct accounting leg row IDs | 4 |
| Distinct piece numbers | 1 |
| Debit in the receivable account | 200 |
| Credit in the revenue account | 200 |
| Debit less credit | 0 |
| Excess receivable against the invoice | 100 |

With extension triggers disabled the four successful calls each returned zero, set the new row ID on the posting object and committed under the enclosing transaction. A fresh call for the receivable then returned `-1` with `BookkeepingRecordAlreadyExists`. The ledger still held four rows. A sequential ordinary sales-journal lookup would already exclude invoice 41 once a prior transfer was visible. The four-leg result requires overlapping admission before either transaction can see the other's writes. Snapshot-conflict checks on rows do not by themselves reject two independent new row IDs.

The control for this case compares the invoice's expected account groups and signed amounts with actual posted groups **by entity, source type and source ID**. A zero debit-credit difference is necessary for a balanced journal. It does not establish that a source was transferred once.

## Two different invoices and one piece number

With no earlier pieces in the same entity, invoices 41 and 42 each transferred a debit and credit of 100 in separate overlapping transactions. Before either committed, both selected piece 1. The row-level duplicate test correctly distinguished the two source IDs. Afterward each invoice had exactly two legs and balanced at 100 on each side. A report selecting only entity and piece 1 combined four legs, with debit and credit of 200 each. Each invoice had the correct allocation. The piece collision changed the meaning of the grouped result.

When reviewing or correcting these entries, inspect every source identity represented by the piece, the journal, its printable reference, the accounts, subsidiary codes, labels and amounts. The numbering configuration can affect printed references independently. A piece-only deletion or correction can encompass postings from another source if their piece numbers coincide. A result that is uncertain after a timeout calls for a read of committed source legs before any resubmission.

[Sales ledger assignment and transfer](../invoice-processing/account-assignment.md) · [Expense claims and journal control](../expense-accounting/journal-transfer.md) · [Execution conditions](README.md)
