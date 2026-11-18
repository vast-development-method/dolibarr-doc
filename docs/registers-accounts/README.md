# Finance and capital registers

| Register | One row represents | Principal selection |
| --- | --- | --- |
| [Bookkeeping templates](templates.md) | One reusable journal template heading | Accounting entities, template code or label |
| [Bookkeeping](bookkeeping.md) | One posted journal leg | Piece, period, account, journal or reconciliation state |
| [Customer invoice line account assignment](customer-assignment.md) | One eligible sales invoice line awaiting its account | Document class, line state, customer, amount, tax or chart mapping |
| [Fixed assets](assets.md) | One capital asset record | Entity, asset class, lifecycle and acquisition or disposal fields |
| [Fixed asset models](asset-models.md) | One reusable asset model | Reference, label, class and availability |
| [Loans](loans.md) | One loan heading with an aggregate over its payments | Current entity, loan ID, label and original capital |

The [intra-community reporting register](intra-community.md) belongs to a development-stage reporting feature. Its saved report records and XML-generation inputs have different grains.

A row count identifies what the operator can act on. A balance or a financial statement can require a different grouping and time basis. The [relational model](../relational-model/README.md) identifies the keys behind these six registers.
