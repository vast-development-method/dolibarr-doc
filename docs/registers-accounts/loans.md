# Loan register

Open the loan area with loan-read access. The write grant controls creation. The query reads `loan` within the current entity and left-joins `payment_loan` by `payment_loan.fk_loan = loan.rowid`. A loan without any payment remains visible. The explicit search inputs are the internal reference, label and original capital.

| Input or displayed value | Interpretation |
| --- | --- |
| Reference | A supplied nonempty reference compares with the integer loan row ID. |
| Label | Apply keyword matching to `loan.label`. |
| Amount | Apply a numeric comparison to `loan.capital`. A plain literal zero is skipped by the input truth test. An explicit comparison such as `=0` reaches the numeric search. |
| Starting and ending dates | Show the agreement dates on each result. The standard selector does not filter on the dates merely because it displays them. |
| Principal repaid | Sum `payment_loan.amount_capital` across linked payments and group by the loan's ID, label, capital, paid flag and dates. The aggregation omits interest, insurance, charges and scheduled instalments. |
| Status in the tabular list | A paid flag of 1 displays paid. An unpaid flag of 0 with a positive sum of paid principal displays started. With no positive sum, flag 0 displays unpaid. |

Default order is descending loan ID. The full-count query removes the payment join and grouping so it counts matching loans. A loan for 10,000 with two payments, each containing 400 principal and 60 interest, appears once. The status test sees 800 principal. The receipts total 920, and the original capital remains 10,000. A search for amount 800 therefore misses this loan. Use the [loan schedule and settlement](../capital/loan-schedule-and-settlement.md) to reconcile principal, ancillary charges and the bank movement.
