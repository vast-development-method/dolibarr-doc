# Project, opportunity and task filters

## Project register

One result identifies one project. The same header can represent an opportunity, a time-billing engagement or an event. The query joins its party, party country, opportunity stage, project creator and parent project. Internal and external assignments enter through existence tests. Without project read-all, the page narrows results to the user's authorized project IDs. A positive `socid` restricts the project party. A positive `search_entity` selects the stated entity. The ordinary path uses the shared project entity set.

| Selectors | Business test |
| --- | --- |
| `search_id`, `search_ref`, `search_label` | Numeric project ID comparison, reference text and title text respectively. |
| `search_parent_ref`, `search_parent_label`, `search_omitChildren` | Match the direct parent reference or title. With subprojects enabled, the value `on` for omit-children requires a null parent. |
| `search_all` | Searches the reference, title, description, notes and location marked for broad search, plus party name, alias and customer code. The private note is removed from the project search-all field set for external readers. |
| `search_societe`, `search_societe_alias` | With the alias column hidden, a populated name box searches both name and alias. When the alias column is selected they have separate predicates. |
| `search_societe_country`, `search_societe_ref_customer`, `search_societe_ref_supplier` | Text on the joined country code and on the party's customer and supplier account codes. |
| `search_project_user`, `search_project_contact` | Positive assigned person ID with a project contact role of internal or external origin, respectively. `mode=mine` sets the internal user criterion to the operator. |
| `search_sale`, `search_login` | A positive ID requires that representative assignment on the party. −2 requires that the party have no assigned representative. Login searches login, first name and last name of the project creator. |
| `search_category_project_list`, `search_category_project_operator`, `search_category_user_list`, `search_category_user_operator` | Project tags and tags on its creator, respectively. Positive IDs test direct memberships. −2 means no category of that kind. Operator 1 gives any, the default gives all. |
| `search_public`, `search_status`, `search_status_multiselect` | Public/private flag is an equality. Workflow state is a set. Value 99 selects draft and open (0 and 1). The multiselect flag changes how selected states are read. Default states are 0 and 1 unless broad search was supplied. |
| `search_option` | `late` sets status to open and requires a project end earlier than current time minus the project warning delay. A project without an end date fails that comparison. |
| `search_opp_status` | A positive value fixes the stage ID. `all` requires a stage other than null or −1. `openedopp` requires such a stage outside WON and LOST. `notopenedopp` includes unstaged projects and WON. `none` includes only null or −1. A LOST opportunity does not satisfy `notopenedopp` in this register. |
| `search_opp_percent`, `search_opp_amount`, `search_budget_amount` | Numeric probability, unweighted opportunity amount and project budget. The displayed weighted amount is derived separately as amount × probability ÷ 100. A plain zero for the probability is skipped by its truth test. |
| `search_usage_opportunity`, `search_usage_task`, `search_usage_bill_time`, `search_usage_event_organization` | Filter the header's four independent usage flags. Explicit zero selects projects without that use. |
| `search_accept_conference_suggestions`, `search_accept_booth_suggestions` | Compare the corresponding event intake flags on the project. |
| `search_price_registration`, `search_price_booth`, `search_import_key` | Numeric registration price, numeric booth price and text of the import marker. |
| `search_sday`, `search_smonth`, `search_syear`, `search_eday`, `search_emonth`, `search_eyear` | Calendar components of project start and end respectively. |
| `search_date_{start,end,creation,modif}_{start,end}` | Inclusive lower or upper bound on project start, project end, creation or last modification. Append `day`, `month` and `year` to identify the selected calendar date. |

For example, a project created by an engineer and managed by a consultant can qualify under the engineer's user category and the consultant's internal assignment at the same time. Selecting the consultant's category instead searches the creator's memberships and can remove that row. Neither category assigns a person to the project.

## Task register

A task must belong to a project in the shared project entities. The ordinary project visibility restriction applies to its parent. A positive `id` selects one project. Showing billed or to-bill time joins time entries and groups the result by task, separating their duration according to whether an invoice is linked. These duration columns do not add a numeric filter. The ordinary task register starts on open projects by default. A nonempty broad search removes that default project-state restriction.

| Selectors | Business test |
| --- | --- |
| `search_project_ref`, `search_project_title` | Parent project reference and title, independent of the task's own reference and label. |
| `search_task_ref`, `search_task_label`, `search_task_description` | Task reference, label or description text. |
| `search_task_ref_parent` | Task's direct parent ID must be among the tasks whose reference matches the entered text. |
| `search_all` | Task reference, label, description, public note and, for internal users, private note. The project title and party name have their own fields. |
| `search_task_progress`, `search_task_budget_amount` | Numeric comparison against the task's recorded progress or budget. The guard skips the bare string zero. A comparison expression such as `=0` enters the numeric matcher. |
| `search_projectstatus`, `search_task_status` | Exact project and task states respectively. Project selector 99 excludes closed project state 2. Task selector −1 leaves the task state unrestricted. |
| `search_project_user`, `search_task_user` | A positive ID must match an internal contact role on the project or on the task respectively. Each has its own role type and record ID. `mode=mine` sets **task** user. On the project register the same mode sets **project** user. |
| `search_societe`, `search_societe_alias` | Text on the project's party. The name box also searches the alias when the alias column is hidden, following the same branch as the project register. |
| `search_categ`, `search_category_customer_list`, `search_category_customer_operator` | The first looks up the selected category on the enclosing project, with −2 selecting an uncategorized project. The latter pair filters that project's party categories, using all/any membership and −2 for no category. |
| `search_date_{start,end}`, `search_datelimit_{start,end}` | Append `day`, `month` and `year`. First pair limits the task's **start** time, second pair its **deadline**. |
| `search_opp_status` | Read and carried to navigation for certain values, without a corresponding base task-query criterion. Project opportunity stage filtering is provided in the project register. |

Consider an open project containing a completed design task and an unfinished installation task. Selecting the default open-project status still returns both tasks. Selecting a task status adds a second criterion. Assignment to the project alone will not satisfy the task's `mine` view unless the person also has an internal task contact role.
