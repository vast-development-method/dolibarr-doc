# Reconciled recovery cases

Consider two eligible orders with one ordinary line each: A orders one unit, B orders two. They have distinct parties except in the grouping example. There are no earlier target invoices, and the customer billing classification subscriber is inactive. The working and readback connections use separate transactions. Counts below are the committed results observed by the reader after the handler returns.

| Operation and injected condition | Durable invoice states | Detail rows / main source links | Source and output outcome |
| --- | --- | --- | --- |
| Customer drafts created for A and B | 2 drafts | 2 / 2 | No issue or render requested. Submitting the same still-eligible selection again produced four drafts, four detail rows and four source links in total. Each repeated edge had a different target ID. |
| Same customer on both A and B, group and issue | 1 issued | 2 / 2 | One render, with both source links pointing at the same target. The two line quantities total three. |
| B is already in an ineligible order state | 1 issued | 1 / 1 | A proceeds. The warning for B does not roll back A. |
| B’s customer invoice header fails, its main link vetoes after insertion, or its detail writer fails | 0 | 0 / 0 | Each failure was tested separately. A’s earlier rows also disappear. No render is reached. |
| B fails issuance after A has rendered, from customer orders or shipments | 0 | 0 / 0 | The external render sink retains A’s completed output in both runs. Database rollback alone does not remove it. |
| A’s render fails after successful customer issue | 2 issued | 2 / 2 | The builder clears the action. B still validates and its render is skipped. Neither target produced an output in this run. Recover the files on the existing invoice identities. |
| Supplier order B’s ordinary detail write fails | 0 | 0 / 0 | Both order classifications roll back as well. |
| Supplier order B’s copied-reference check rejects validation before the status update | 1 issued, 1 draft | 2 / 2 | Both source orders remain classified as billed. The earlier positive line result permits the selection to commit. Inspect B’s existing payable before creating another. |
| Supplier order B’s validation subscriber vetoes after the status update | 2 issued in storage | 2 / 2 | Both source orders remain billed. The independent reader finds B’s permanent reference and issued status despite the validator returning failure. Downstream completion must be checked separately. |
| Supplier order B’s source classification fails before writing a flag | 2 issued | 2 / 2 | Only A is classified as billed. The outer conversion does not check that classification return value. |
| Receipt billing encounters the same early rejection or late subscriber veto on B | 0 | 0 / 0 | Both cases roll back the selection and A’s completed output remains external. The receipt header associations and detail allocation links also roll back. |

## Fulfilment inputs and missing allocations

Two receipts with one line each produce two primary receipt-to-payable links and two payable-detail-to-receipt links. Group both under one supplier and the same four links lead to one payable holding three units. If the second **detail association insert** fails before writing its row, the writer returns failure but the conversion ignores it. Both invoices issue, both payable details survive, and both primary receipt links survive. Only the first detail association exists. Compare the second detail's origin and quantity to the receipt allocation before treating the receipt-level link as evidence of line-level reconciliation.

A currency mismatch on B also allowed both receipt payables to issue with every link present. A draft receipt B or a failed ordinary detail on B instead rolled back A and B before either was rendered. Repeating the admission case with a missing **shipment** B processed A alone and issued its one invoice. Grouping two fetched shipments for the same customer produced one issued invoice, two detail rows and two shipment links.

## A negative result with an open transaction

With stock-on-supplier-invoice enabled, issue A successfully and let B's movement writer return a negative value. The supplier validator has already written B’s status change and returns before closing its own transaction level. In the supplier-order run the outer caller selected the commit branch. In the receipt run it selected the rollback branch. Both returned with depth one. The writer could read **two issued headers** on its connection, while an independent connection saw **zero**. An explicit physical rollback left zero headers, details and order classifications. A PDF render had already completed for A in the receipt run. A same-connection read or a success message does not prove settlement of this case.

## Late failure on a single-source conversion

A quotation, order and contract were tried separately with a two-unit source line. The target creator wrote the draft, one two-unit detail and one source link. A hook then vetoed the conversion. Direct invocation returned failure while an independent reader found one target and one link in each of the three cases. Repeating each under a parent transaction that rolled back on the negative return left zero targets, zero detail quantities and zero links. In a separate quotation run, the optional automatic order validation returned a failure after creation. The converter still returned the positive target ID and the order remained a draft.

## Scope of the observations

The cases exercised the complete selection and issue loops for customer orders, supplier orders, shipments and receipts, including creation, party grouping, primary and detail linking, ordinary lines, classification and issue decisions. Separate issue-only runs also used prepared shipment and receipt targets. The single-source cases executed the conversion routines for quotations, orders and contracts. The supplier validator, typed-link writer, document-build action and nesting operations executed with a transactional data store and an independent reader. Source loading, selected record writers, numbering, hooks, stock failure and the external render sink were controlled test inputs. Output counts measure the calls received by that sink. Physical file content, live provider delivery and mobile or browser rendering have their own transaction and delivery contracts.

[Selected-document rules](selected-documents.md) · [Single-source rules](single-document.md) · [Recovery from the persisted records](README.md)
