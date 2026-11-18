# Bookkeeping templates

The template catalogue reads one `accounting_transaction_template` heading in the accounting entity set. Its entry permission is the chart-of-accounts grant, also used for add and delete actions on this screen. A template contains instructions for a later journal transaction. Opening the list or counting its rows does not create a bookkeeping entry.

| Selection | Behaviour |
| --- | --- |
| All-fields search | Uses the template `code`. A word that appears exclusively in `label` is found through the label filter. |
| Header text | `code`, `label` and `import_key` use keyword matching when supplied as individual filters. Spaces join required terms and a vertical bar supplies alternatives. |
| Identifiers | The header ID and available entity field take numeric tests. Creator and modifier select the user attached to the template. An empty selection or the all-values sentinel omits an individual user restriction. |
| Dates | Independent inclusive bounds on `date_creation` and `tms` run from the beginning of the first selected day to the end of the last. |
| Custom fields | When custom definitions exist, the reader left-joins their values by header ID. Extension predicates may narrow the result. |

The normal query sorts headings by the first declared field, `rowid`, ascending and reads one additional result for pagination. With full counts enabled the count follows the filtered joins. The standard template fields carry no numeric page measure.

For a template with code `RENT`, label `Monthly premises` and three debit/credit instructions, a code search for `RENT` returns one heading. A global search for `premises` misses this template while a label search finds it. Retrieve its three instructions through `accounting_transaction_template_det.fk_transaction_template` when constructing the posting. An actual journal piece has its own source, date, period and legs. [Journal records](../records/accounting.md#record-accounting_transaction_template)
