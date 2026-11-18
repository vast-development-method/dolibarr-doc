# Project pipeline, time and staff costs

## Project and task activity

The project statistics group by **project creation date**. A January cohort stays in January if its opportunity amount, probability or status changes later. The report reads the current fields, so changing those fields can change the January result. This is a creation-cohort view and cannot reconstruct the pipeline as it stood at the end of a past January.

| Measure | Population and computation |
| --- | --- |
| Projects created | Count project records in the selected project entities and months. A responsible-user filter uses the project manager field. A party filter uses the party on the project. Viewers without permission to read all projects use their authorized project list. |
| Opportunity amount | Sum recorded opportunity amounts for the selected project population, grouping by creation month. The opportunity filter can select one stage, all opportunities, open stages or projects without a stage. Open stages exclude won and lost. |
| Probability-weighted amount | For each project multiply opportunity amount by recorded percentage divided by 100. A missing percentage contributes zero. The statistics page calls this measure with automatic zeroing of won/lost stages disabled. Those projects therefore use their recorded percentages when they qualify for the chosen stage filter. |
| Tasks created | Count task records by task creation date. Tasks join to their parent projects for party filtering. Task-responsible-user and priority filters apply to the task. Restricted commercial visibility can limit the result to parent-project parties assigned to the viewer. |

Two opportunities created in March at 10,000 with 30% probability and 4,000 with 75% contribute 14,000 to the nominal March amount and 6,000 to the weighted amount. Updating the first project's probability to 60% in June changes the weighted March cohort to 9,000. Neither amount measures orders accepted or invoices issued. The project and task lists expose the responsible person, project party, status, priority and dates needed to identify the contributing records.

Source locations include `htdocs/projet/class/projectstats.class.php:buildWhere, getNbByMonth, getAmountByMonth, getWeightedAmountByMonth`, `htdocs/projet/stats/index.php:148–162, 229–235` and `htdocs/projet/class/taskstats.class.php:buildWhere, getNbByMonth`.

## Valuing actual time and calculating project margin

Task cost begins with recorded time entries of type task, keyed to a specific task and joined to their recording users. The aggregation returns elapsed seconds, monetary amount, the number of entries missing a saved hourly rate, and the number joined to a user with no current hourly rate. For each entry multiply its duration in seconds divided by 3,600 by **the rate stored on that entry**. A missing line rate contributes zero amount and still contributes its duration. A current user rate alone does not fill the stored line rate in this calculation.

An optional user narrows the time entries. The date bounds compare the recorded work timestamp inclusively and also allow entries with no timestamp. For example, an entry of 5,400 seconds at 40 and another of 1,800 seconds without a rate yield two hours, amount 60 and one missing line rate. The missing-rate count makes it possible to distinguish a zero-cost entry from completely costed time. A timesheet valued today can therefore diverge from multiplying all historic hours by today's employee rate.

The project's linked-elements view obtains these task amounts for its selected user and dates. It aggregates qualified amounts by source family. Families configured as revenue add to revenue and balance. Cost families subtract from balance. Families without a margin role can appear for reference. Where revenue is nonzero the displayed percentage is 100 times net balance divided by net revenue, rounded to one decimal. A 1,000 revenue and 350 cost result gives 650 balance and 65.0%. The percentage depends on which elements the configuration assigns to the balance. Double-counting an order and its invoice as revenue changes the result without changing project economics.

Source locations include `htdocs/projet/class/task.class.php:getSumOfAmount` and `htdocs/projet/element.php:803–828, 1096–1122, 1190–1196, 1676–1682, 1774`.

## Project income and expense by recognition basis

The financial result by project assigns invoices and their payments to the **project on the invoice**. On the invoice basis, issued and closed customer invoices add signed net and gross totals in their issue periods. Eligible supplier invoices subtract their totals in their own issue periods. Deposit handling and eligible invoice types are side-specific. On the cash basis, sum invoice-payment allocations by payment date. A project with 240 gross invoiced in June and 100 received in July reports turnover in June and a receipt of 100 in July. Reallocating an invoice's project changes where its allocated cash appears.

Salary and expense contributions use different project relationships. A salary belongs to the project on the salary record. Under the accrual basis its cost is the salary amount on the pay-period end date. Under the cash basis the report sums salary payments in the payment period and obtains the project from the salary. Expense reports instead carry project on **each expense line**. One report can therefore contribute to multiple projects. The accrual path selects qualifying reports at status 5 or above, uses report validation date and sums line net and gross values.

The cash expense query joins each qualifying expense line to its report's payments, uses payment date, and sums **distinct payment amounts per expense line**. It has no input that allocates a reimbursement among projects. For example, a single 120 payment for two lines on two projects can appear at 120 on each line. Two equal payments on the same report can also collapse within a single line's distinct-amount sum. A finance user seeking the actual cash disbursement must reconcile to the reimbursement payments. The cash project breakdown cannot determine the allocation from receipt-line amounts alone.

Source location `htdocs/compta/resultat/projects.php:318–361, 523–560, 637–671, 749–777`.

## Salaries and employee expense statistics

| Family | Grain and month | Monetary measure and scope |
| --- | --- | --- |
| Salaries | One salary record on the **end of its pay period**. Multiple salary records for an employee in one month increase count independently. | The total sums recorded salary amounts and the mean averages salary records. The basic query uses the active entity and can filter by employee or a set of employees. It does not select salary payment rows. |
| Employee expenses | One expense-report header, assigned to the month it starts. Individual receipt dates within the report do not apportion its header across months. | Sum or average header net amounts. The statistics entry point can filter by status, and the aggregation can restrict by author. Without read-all rights the permitted authors are the viewer plus their subordinates. |
| Expense report with no start date | For monthly amount and mean, missing start falls back to creation date. The monthly count's year predicate still requires the actual start year. | A record can contribute value but no count for that year. Dividing the displayed total by the separately retrieved count need not reproduce the displayed mean for this case. |

When an employee filter is not supplied the salary page chooses the viewer alone if they lack subordinate-read permission. With subordinate access but without read-all it defaults to a hierarchy selection. The salary list provides individual salary entries behind the statistics. An expense report spanning April 28–May 3 contributes its full recorded net amount to April in employee expense statistics. Its project cost can instead enter May when validated, and its reimbursed cash another month again. The month depends on the business event the reader is measuring.

Source locations include `htdocs/salaries/stats/index.php:118–134`, `htdocs/salaries/class/salariesstats.class.php:getNbByMonth, getAmountByMonth, getAverageByMonth`, `htdocs/expensereport/stats/index.php:95–104` and `htdocs/expensereport/class/expensereportstats.class.php:69–109, 137–185`.
