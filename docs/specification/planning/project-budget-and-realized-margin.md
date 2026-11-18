# Project budgets, opportunity forecasts and realized margin

An opportunity worth 50,000 at a 40% likelihood contributes a weighted opportunity amount of 20,000. That calculation says nothing about how much the project can spend or how much income it has recorded. The project keeps the commercial estimate, approved working figures and financial record associations separately.

## Measures used in planning

| Measure | Input and interpretation |
| --- | --- |
| Opportunity amount and probability | The project stores a sales estimate and a percentage. The overview displays the weighted estimate as `opportunity amount × percentage ÷ 100` where the opportunity fields apply. |
| Project budget | A monetary amount entered on the project. The project card can change it independently of task budgets or time entry. |
| Task budget and planned workload | A task has its own monetary estimate and estimated effort in seconds. Maintaining a task estimate does not post a cost or reserve that amount in a ledger. |
| Time cost | For the selected task, sum the posted time rows as `duration in seconds ÷ 3600 × stored hourly rate`. A missing hourly rate contributes zero money and still contributes time. |
| Commercial balance | The project overview groups accessible, linked transactions, applies the configured contribution sign and sums the eligible amounts. It can show both tax-exclusive and tax-inclusive results. |

If a project budget is 12,000 and two task budgets total 8,000, the remaining 4,000 is the arithmetic difference between assumptions. Saving those tasks does not create a 4,000 contingency transaction. Likewise, reporting a task as 80% complete updates a progress measure. The balance calculation does not recognize 80% of the opportunity value as revenue.

Project fields are in `htdocs/projet/class/project.class.php`. Budget entry and opportunity presentation are in `htdocs/projet/card.php` and `htdocs/projet/element.php`. Task plan fields and the work valuation query are in `htdocs/projet/class/task.class.php`.

## Attribution and the posted cost of time

The project reference used for attribution varies by record. Customer and supplier documents are linked through their project fields. Expense allocations point to a project on the expense **line**, so an employee's single expense report can charge two projects. Stock movements have a project field separate from the warehouse's optional project association. Task valuation selects time rows for tasks on the project and can restrict them to one worker or a reporting interval.

Adding time captures the worker's hourly rate from the user record. During an ordinary edit the stored rate is retained if already populated. An empty rate or the option to always update the hourly rate can replace it with the worker's current rate. The valuation therefore uses the recorded rate on each entry, even when another person logging the same task has a different rate or the worker's master rate subsequently changes. The aggregation returns time seconds and missing-rate counts as well as the amount. A time row with a null work timestamp is included by the query's date-bound conditions.

Suppose one engineer records two hours at 60 and a technician records three at 40. Five hours cost 240. A further 30 minutes with an unknown stored rate increases effort to 5.5 hours and leaves measured cost at 240. A zero monetary result for that line does not resolve its missing rate. Gross project margin derived from such entries can be larger than the margin once all rates are known.

The project relation queries are in `htdocs/projet/class/project.class.php` under `get_element_list`. Rate capture and valuation are in `htdocs/projet/class/task.class.php` under `addTimeSpent`, `updateTimeSpent` and `getSumOfAmount`.

## How income and expenditure enter the overview

The default contributing categories include customer invoices and donations as positive amounts. Supplier invoices, expenses, social charges, task labor, project stock movements, salaries and miscellaneous payments are treated as expense categories, subject to the record's own direction and the viewer's enabled modules and grants. Other associated records such as sales quotations, customer orders, shipment documents and supplier orders can be displayed without changing the default profit balance. Administrators can replace the lists of positive and negative contributors, so the policy belongs with the reported number.

A signed or billed customer quotation qualifies for its quotation total when that category is included. A replaced customer invoice is excluded from its invoice total. A paid-invoice-only option requires the customer invoice to be in its closed state. A supplier proposal or order is displayed with its purchasing sign, with the margin calculation avoiding a second sign inversion when the category is explicitly configured as an expense. The stock-movement amount uses `movement unit price × absolute movement quantity` before applying the category sign. Miscellaneous payments first apply their direction and subsequently their category sign.

The report first totals each qualified category, then adds or subtracts those totals according to its configured role. The tax-exclusive margin percentage is `100 × tax-exclusive balance ÷ tax-exclusive revenue`, rounded to one decimal place. The percentage is shown only when the revenue denominator is nonzero. For a contribution of 8,000 in customer invoices, 3,000 in supplier invoices and 240 in time cost, the tax-exclusive balance is 4,760 and the margin is 59.5%, assuming no other contributing categories. Including 3,000 of supplier orders as an additional expense while also including their supplier invoices would count two commercial stages. Matching the contribution policy to the desired reporting basis therefore matters.

A project can be visible to someone who lacks access to its financial records. Each record category has its own module and read conditions. The task labor cost category is suppressed for users who lack read access to all of the eligible financial areas, which include invoicing, payroll, expenses, donations, taxes and banking. Comparing two users' overview balances requires the same accessible record categories and the same date interval.

The financial category definitions, eligibility, amount signs and balance calculation are in `htdocs/projet/element.php`. The dates and linked record selection are in `htdocs/projet/class/project.class.php` under `get_element_list`.
