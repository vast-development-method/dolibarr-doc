# Record cards, activity histories and specialist reports

A customer invoice has a working card, an activity tab, a correspondence tab, entries in registers and rows on reports. Each can show different evidence for the same invoice. A receipt allocation can settle it, an agenda entry can describe a call about it, and a tax report can select its lines by tax rate. To reconcile two results, identify the row each view reads before comparing the values.

## Find a card or history

| Inventory | What one row identifies | How to use the fields |
| --- | --- | --- |
| [97 record workspaces](record-cards.csv) | An internal business or administration card, including the project task workspace. Each row gives its principal record table. Different workspaces can operate on one table. | `direct_action_values_compared` lists literal values compared for equality on that card, including actions used only during rendering. `shared_operations_included` identifies selected common routines the card includes. An action value alone establishes neither a permission nor a transition. Use the corresponding domain workflow for its preconditions and effects. |
| [67 information, activity and correspondence panels](record-panels.csv) | An internal panel that directly calls the shared record-information renderer, across 52 business record types. | The last column distinguishes 28 calls to the agenda reader, 13 to the correspondence reader, and 26 without either shared feed. A page can render record information alone even when its tab is called Activity. |
| [44 specialist statistics views](specialist-reports.csv) | Each specialist view in the internal statistics areas, including 26 organisation/portfolio views, 14 item/catalogue views and four lot/serial views. | The request-name column lists inputs read directly on the view. Directly named tables identify concrete dependencies in its query. Shared statistical calculations are listed separately because a view can get its figures entirely from a delegated reader. Blank cells indicate no directly identified entry in that column. |

The card inventory follows the internal pages named for record cards plus the task card. It excludes public portals, page fragments and rendering templates. One customer invoice card edits the commercial record. A second workspace reads the same `facture` record to assign accounting codes. The two screens have different grants, accepted actions and consequences. A group leave card and an individual request card both address `holiday`. A project can have its own tasks, while each task retains a separate `projet_task` identity. [Service and domain workflows](../specification/README.md)

## Which facts reach an object's history?

| Evidence on screen | Source and association | Interpretation |
| --- | --- | --- |
| Record information | The common renderer reads an object's populated import key, creator/modifier, validation, approval, second approval, signature, closing, reconciliation and sending properties when available. It resolves recorded user IDs to user identities and can display server and user-local times. | A modification actor describes the stored latest modification. It gives no list of intermediate editors or previous field values. The renderer can indicate an unknown actor when only the corresponding date is available. |
| Agenda | The event row uses `actioncomm.id`. Depending on the owner, the reader matches `fk_soc`, `fk_project`, an element type plus `fk_element`, or an assignment in `actioncomm_resources`. For a document the type identifies which record family owns the numeric ID. | The reader applies the visible agenda entities. Without the grant to read all actions, the agenda reader sets its user filter to the current user. Status, period, label and event-type filters can change which rows are visible. |
| Correspondence | Selects agenda records in the permitted agenda entities using the owner-specific match. For example, an invoice with an ID matches `elementtype = invoice`. A supplier invoice uses `invoice_supplier`. For a third party the direct association is `fk_soc`. | If the calling context supplies a contact with an email and the campaign module and action filters permit it, the reader can also select sent campaign recipients by matching `mailing_cibles.email` and `statut = 1`. An email address can be shared. A campaign recipient row owns different evidence from a document-specific event. |

For example, customer invoice 7 and supplier invoice 7 can belong to the same party. An event whose `fk_element` is 7 and whose `elementtype` is `invoice` belongs to the customer invoice feed. Its presence on the party feed additionally depends on its `fk_soc`. A later edit of an invoice amount can update its modification properties without adding an agenda row carrying the old amount. The supplier order information panel reads an agenda feed. The asset model and both booking-calendar activity panels render the object information without calling that feed. [Per-record panel inventory](record-panels.csv)

## Read the measure and its unit

At catalogue level, item popularity groups selected commercial detail rows by item and sums their quantities. Two lines for an item with quantities 1 and 8 contribute 9 units. The number of appearances is 2. At lot level, the purchase receipt reader follows the receipt's batch detail, while the shipment reader joins the shipment detail and its batch rows. Manufacturing references use the production lines. A lot with two partial receipts can have two receipts and a single current stock balance. The item's document history separately identifies document and line grain. [Item document history](../operator-reports/item-document-history.md)

An organisation-wide statistics page can call generic count, amount and average readers. The business family supplies the measure. For tickets the amount reader sums `timing` by month of creation. The intervention amount query selects a literal zero grouped by validation month. Neither provides accounting turnover. Project opportunities can have an amount and a separately weighted amount, while task statistics ask for a count. Read the measure, filters and recognition date with the relevant report. [Reporting and reconciliation](../reporting/README.md)

### Project outcome on accrual and cash bases

The project outcome's customer accrual branch selects invoice statuses 1 and 2 and sums the invoice header net and gross by assigned project using invoice date. It includes types 0, 1, 2 and 5, and includes type 3 unless configured to treat deposits only as payments. Its cash branch groups invoice allocations from `paiement_facture` by the invoice's project on the receipt date. That branch's end-date predicate requires a start date as well. The supplier accrual route uses types 0, 1 and 2 plus optional type 3, and the supplier cash route uses `paiementfourn_facturefourn.amount` and the supplier payment date. Visible customer entities and the active supplier entity are separate scope predicates.

Expense claims on this report use a different grain. The accrual query takes each qualifying `expensereport_det` row on a claim at status 5 or above, groups by its line ID and project, and takes its net and gross for the claim validation period. The cash query joins every selected reimbursement on the claim to each detail row. Within each line group it sums **distinct numeric payment amounts** during the payment period. It subtracts the resulting rows from the running project result.

| Two lines on one approved claim | Project P | Project Q | Total shown or paid |
| --- | ---: | ---: | ---: |
| Accrual amounts for expense lines of 60 and 40, with no tax | 60 | 40 | 100 |
| Cash display for reimbursements of 30, 30 and 15 | 45 | 45 | 90 |
| Money paid on the claim itself | | | 75 |

These results were reproduced with the declared claim, expense-line, reimbursement and project tables on a transactional database. Within one line, the two equal payments collapse to 30 and the distinct 15 brings its total to 45. The second project line joins the same payments and also contributes 45. Reimbursing the claim creates no split that assigns those 75 units of cash to P and Q. For the actual cash balance use each reimbursement record once. [Employee payment registers](../expense-accounting/employee-payment-registers.md)
