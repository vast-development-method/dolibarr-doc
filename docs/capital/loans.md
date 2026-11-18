# Loans, instalments and bank settlement

A loan agreement defines the borrowed principal, the term and the account codes. An instalment schedule expresses amounts due. A repayment records what was paid. Keeping those three records distinct lets a user record repayments without first constructing a schedule, or reconcile actual payments with scheduled terms. [Loan agreement](../reference/locators/capital.md#ref-31db9fb4d13a) · [Schedule](../reference/locators/capital.md#ref-fe1c9ec98eac) · [Repayment](../reference/locators/capital.md#ref-da613a1bc2ec)

## Agreement and schedule

* **Create.** A loan writer supplies positive principal, a start date and an end date. Store the entity, label, annual percentage rate, instalment count, total insurance, author, optional project and the three accounts for principal, interest and insurance. With double-entry accounting enabled, creation rejects a missing code for any of the three, even when insurance is zero. [Creation checks](../reference/locators/capital.md#ref-bef73345ff56)
* **Generate and save.** The schedule screen requires the loan calculation permission. Writing a schedule also requires loan write permission. One record per term stores due date, principal, interest, insurance and eventual payment and bank references. The first due date is the agreement start, subsequent terms are monthly. The screen saves the series in one transaction and rolls it back on a term creation error. A loan already started or paid with no existing schedule cannot acquire a schedule through this screen. [Schedule permissions and persistence](../reference/locators/capital.md#ref-134f49937c33)
* **Calculate.** At each term let `C` be remaining principal, `r` the annual percentage divided by 1,200, and `n` the remaining number of terms. For a nonzero rate the principal-plus-interest instalment is `C × r / (1 − (1 + r)^−n)`. At zero rate use `C / n`. Round the instalment and `C × r` to monetary-total precision independently. Principal repaid is their difference. Carry the rounded remaining principal to the next term and recompute. Round total insurance divided by the term count, then apply the difference between that rounded allocation and total insurance to the first term. [Annuity](../reference/locators/capital.md#ref-74d4115d6535) · [Per-term amounts and dates](../reference/locators/capital.md#ref-78f335a60fb2)

A principal of 1,200.00 at 12% per year, repaid over two months with 10.00 insurance and two decimal places, yields the following amounts.

| Term | Starting principal | Principal paid | Interest | Insurance | Cash outflow | Ending principal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1,200.00 | 597.01 | 12.00 | 5.00 | 614.01 | 602.99 |
| 2 | 602.99 | 602.99 | 6.03 | 5.00 | 614.02 | 0.00 |

## Repayment service contract

| Step | Inputs or checks | Observable effect |
| --- | --- | --- |
| Resolve the term | A loan writer selects the loan. The scheduled path selects the first term lacking a bank link. | With a schedule, interest comes from the term. For an unscheduled payment the user can supply interest as well as principal and insurance. |
| Accept payment | Require a payment date and payment method, an account when the bank module is active, nonzero remaining principal input and a nonzero combined payment. A term already carrying a bank link is rejected. | Persist actual principal, insurance and interest separately, linked to the agreement and actor. The amount sent to the bank is the sum of all three. |
| Record cash and schedule | Bank module enabled in this example. | Create one outgoing bank movement for the negative combined amount. Link the payment and the loan. On the matching scheduled term set its bank and repayment IDs. Changed repayment components invoke the remaining-schedule calculation. A failed payment insert, bank write or required schedule update rolls back the enclosing payment transaction. |
| Read remaining principal | Sum the principal component of repayments for this loan. | Outstanding principal equals agreement principal less that sum. Recording the first payment normally changes unpaid (0) to started (2). The paid state (1) is an explicit card action; the button tests the rounded outstanding amount. |
| Transfer to bank journal | The loan payment and bank line have been linked and principal, insurance and interest accounts have been configured. | The journal resolves the payment via its bank line and accumulates its three components to their configured counterpart accounts. For the first term above, credit cash 614.01 and debit principal 597.01, interest 12.00 and insurance 5.00. |

Sources: [Payment action](../reference/locators/capital.md#ref-e1a155957997) · [Payment persistence](../reference/locators/capital.md#ref-6a7eaf278df2) · [Bank and started status](../reference/locators/capital.md#ref-e77c20467bfa) · [Principal aggregation](../reference/locators/capital.md#ref-e6d8651635ef) · [Paid action availability](../reference/locators/capital.md#ref-831d6b3798b8) · [Bank journal](../reference/locators/capital.md#ref-f730d16f1609)

## Acceptance criteria

1. Save both scheduled payments in the example. The two principal amounts sum to 1,200.00. Interest totals 18.03 and insurance totals 10.00. The bank decreases by 1,228.03. After only the first payment, the principal balance is 602.99.
2. With an annual rate of zero and three terms, principal 300.00 gives principal 100.00 per term. Total insurance 10.00 produces 3.34 on the first term and 3.33 on each following term.
3. Submit different interest for a scheduled payment. The stored payment uses scheduled interest. A payment with three zero components is rejected.
4. Use a loan calculation account without write access. It can read the schedule but cannot save the proposed terms. With double-entry accounting enabled, creating an agreement with an empty interest account fails before persistence.
5. Treat the repayment split as immutable evidence for reconciliation. The [banked repayment projection](../../schemas/capital/loan-repayment.schema.json) carries all three amounts and an outgoing cash delta. Consumers check the arithmetic and referenced agreement, term and bank line. [Valid first payment](../../examples/capital/loan-repayment--first-term.json)

The sequential duplicate check uses a bank-line marker on the term. For off-date payments, changed principal or insurance, bank-disabled repayments and the effect of deleting a repayment, follow the [three-term schedule and settlement reconciliation](loan-schedule-and-settlement.md).
