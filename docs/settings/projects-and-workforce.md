# Project work, expenses and leave

These fourteen controls appear on the project, expense-report and leave setup screens. A calendar exclusion changes a day count. A timesheet limit constrains when work can be recorded. A monthly posting policy changes when an approved absence reaches a balance. Those are separate decisions even when they involve the same employee and dates.

## Decide which project is eligible and when work is complete

| Operator control | Choice and effect |
| --- | --- |
| Manage opportunities in projects (`PROJECT_USE_OPPORTUNITIES`) | The visible switch enables or disables opportunity management. The module declares an initial value of 1. When the feature is enabled and the project is used as an opportunity, its form and update logic work with the opportunity status and related information. |
| Manage project tasks (`PROJECT_HIDE_TASKS`) | The operator control has inverse wording to the stored setting. With the hide flag unset, the project form offers task tracking. Setting the flag hides the task-management choice and dependent task controls. |
| Select projects belonging to another party (`PROJECT_ALLOW_TO_LINK_FROM_OTHER_COMPANY`) | When a document has a party, an empty setting admits that party's projects and projects with no linked party. A comma-separated list adds the listed party IDs. The value `all` lifts that particular party filter. The project selector still applies project entity and authorised-project criteria. |
| Close a project when all tasks finish (`PROJECT_CLASSIFY_CLOSED_WHEN_ALL_TASKS_DONE`) | With the switch on, a successful task update loads the parent. If the project is validated and every task's progress is at least 100, it invokes the normal project-close operation. With an unfinished sibling, this task update leaves the project open. |
| Limit retrospective timesheet entry (`PROJECT_TIMESHEET_PREVENT_AFTER_MONTHS`) | Enter a whole number of months of zero or more. Zero leaves this age restriction inactive. A positive value sets a rolling cutoff calculated from the current time minus that number of calendar months. Task-time creation, modification and deletion paths compare the entry date against the cutoff. |

See [project and time operations](../operations/project-time.md) and [project record access](../permissions/decisions.md).

## Admit expense lines

| Operator control | Choice and effect |
| --- | --- |
| Require a project on expenses (`EXPENSEREPORT_PROJECT_IS_REQUIRED`) | The switch appears when projects are enabled. The expense card checks for a selected project on line creation and update. The project belongs to that expense line. |
| Start a claim with this month's dates (`EXPENSEREPORT_PREFILL_DATES_WITH_CURRENT_MONTH`) | When enabled, an empty start receives the first day and an empty end the last day of the current month. Each missing boundary is filled independently. An explicitly entered date survives this defaulting step. |
| Enter tax-inclusive line amounts only (`EXPENSEREPORT_FORCE_LINE_AMOUNTS_INCLUDING_TAXES_ONLY`) | When enabled, the line editor disables tax-exclusive unit price input and the assisted rate-entry flow fills the tax-inclusive amount. This selects the editable basis for the input, while VAT and totals remain part of the expense. |
| Block lines outside the claim period (`EXPENSEREPORT_BLOCK_LINE_CREATION_IF_NOT_BETWEEN_DATES`) | No makes an out-of-range date a warning on an otherwise valid line. Yes makes it an error on creation and update. The comparison includes the whole last day of the claim. |

For a claim from 1 to 30 June, a line on 30 June falls inside the date window. A line on 1 July triggers the configured warning or refusal. If projects are mandatory, moving that line into June leaves the separate project requirement to satisfy. See [expense reports](../people-services/expenses.md).

## Calculate working days and debit the leave balance

| Operator control | Choice and effect |
| --- | --- |
| Monday is usually nonworking (`MAIN_NON_WORKING_DAYS_INCLUDE_MONDAY`) | Default off. Turning it on removes Mondays from the usual working-day count. |
| Friday is usually nonworking (`MAIN_NON_WORKING_DAYS_INCLUDE_FRIDAY`) | Default off. Turning it on removes Fridays from the usual working-day count. |
| Saturday is usually nonworking (`MAIN_NON_WORKING_DAYS_INCLUDE_SATURDAY`) | Default on. Turning it off allows ordinary Saturdays to count as working days. The applicable public-holiday calendar remains relevant. |
| Sunday is usually nonworking (`MAIN_NON_WORKING_DAYS_INCLUDE_SUNDAY`) | Default on. Turning it off allows ordinary Sundays to count as working days. |
| Deduct entitlement at month end (`HOLIDAY_DECREASE_AT_END_OF_MONTH`) | Off debits a balance-affecting request on approval. On defers the debit to monthly balance processing, which selects approved leave in the processed period. Approval and deduction can then have different dates. |

For a full-day request spanning Friday through Monday with no public holiday, the default calendar counts Friday and Monday. Making Friday nonworking reduces the count to one. Changing when entitlement is debited preserves that calendar calculation. See [leave entitlement](../people-services/leave.md).
