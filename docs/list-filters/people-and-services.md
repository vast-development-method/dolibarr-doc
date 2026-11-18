# Leave, expense, contract, intervention and ticket lists

## Leave and expense reports

The leave list returns a request joined to two users, its employee and designated reviewer. Both joins must find a user. The expense list returns a claim header joined to its author. Two claims by the same employee appear separately even when their periods coincide. Each list applies its own entity scope before applying the following filters.

| Selector | Leave request | Expense report |
| --- | --- | --- |
| `search_all` | Searches the request reference, description, employee's last name, first name and login. | Searches the claim reference, public note, author's last name, first name and login. Internal users also search the private note. |
| `search_ref` | Request reference text. | Claim reference text. |
| Employee selection | `search_employee` equals the beneficiary ID. | `search_user` equals the report author ID. |
| Reviewer and type | `search_valideur` equals the designated reviewer ID. `search_type` accepts leave type IDs as a set. | The standard list has no reviewer or line expense-type criterion. Assigned reviewer can independently affect visibility. |
| `search_status` | Single stored state, with 1 draft, 2 awaiting review, 3 approved, 4 canceled and 5 refused. | Matches the selected report status IDs. `statut` provides a fallback value. |
| Date | `search_{day,month,year}_{start,end,create}` selects calendar components of leave start, end or creation, respectively. | `search_date_start`, `search_date_startend` are the lower and upper bounds on the claim's start. `search_date_end`, `search_date_endend` are the lower and upper bounds on its end. Each prefix takes the suffix `day`, `month` or `year`, with no intervening underscore. |
| Amount | Duration is a calculated column. | `search_amount_ht` and `search_amount_ttc` compare the header's net and gross totals numerically. The page reads and displays `search_amount_vat` but its standard query does not compare the VAT total. |

An employee tab with positive `id` fixes the employee filter. Without leave read-all, the request query restricts beneficiaries to the current user's hierarchy. For claims, the ordinary hierarchy restriction additionally admits a report assigned to the operator when they have approval rights. The broad expense visibility grants bypass this clause. Searching for a reviewer on leave therefore answers a different question from opening the expenses someone is allowed to approve. The leave modification column renders `search_month_update` and `search_year_update` without a corresponding list query condition. The expense header stores approval and validation dates but its period selectors above compare the period of expenditure.

For example, against a July 31–August 2 claim, a lower bound of August 1 on the **start** excludes the claim. The same bound on the **end** includes it. To find claims that overlap August, use start on or before August 31 and end on or after August 1.

## Contracts

The result starts with the contract header and joins its party, country, state and party type. Service-line expiry is an aggregate over its services. A selected internal contact adds a contact-role join, so one agreement can match more than one role held by the same person. `socid` fixes the counterparty, with the external user's own company taking precedence. The header must be in the contract entity scope.

| Selectors | Predicate |
| --- | --- |
| `search_contract`, `search_ref_customer`, `search_ref_supplier` | The first searches either the exact numeric header ID or the contract reference. The others search the separately stored customer and supplier references. |
| `search_name`, `search_email`, `search_phone`, `search_phone_mobile` | Party name and email are independent. Each phone box searches both the fixed and mobile number. |
| `search_zip`, `search_town`, `search_state`, `search_country`, `search_type_thirdparty` | Postal code, town and joined state name use text. Country and third-party type use IDs. |
| `search_note_public`, `search_note_private`, `search_all` | Target the respective header notes. Search-all uses the contract's marked fields (contract reference, both counterparty references and both notes) plus party name. The note fields can participate in the predicate outside the visible columns. |
| `search_user`, `search_sale` | A positive user selects an internal contact role on the contract. A positive sales representative instead matches a sales assignment to the party. Sales value −2 selects a party with no representative. |
| `search_category_customer_list`, `search_category_customer_operator` | Customer category membership on the party. Operator 1 combines alternatives. The default combines requirements. Value −2 tests absence of any party category. |
| `search_product_category`, `search_category_product_operator` | Membership of products on this contract's service lines. −2 selects contracts without a category relationship for any line product. The input is wrapped as one entry and converted to an integer before building its category conditions. |
| `search_date_{start,end}`, `search_date_creation_{start,end}`, `search_date_modif_{start,end}` | Inclusive date bounds on contract date, row creation and last modification, respectively. Append `day`, `month` and `year` to each prefix. |
| `search_dfmonth`, `search_dfyear`, `search_op2df` | Calculate the earliest planned end among open service lines (state 4). With a year and operator, ≤ compares against the selected month's last day, ≥ against its first day, and the other operator selects within that month. A contract with no such date cannot satisfy these comparisons. |
| `search_signed_status`, `search_status` | Nonnegative signature status compares the stored signature state. The separately read general status defaults to 1, but the standard list query never compares it to header status. |

An agreement with open services expiring in June and September matches a June earliest-expiry search. The September service alone cannot make the agreement pass a September earliest-expiry search. A closed June service drops out of the calculation.

## Field interventions

An intervention always matches its party and entity. `socid` selects a party. Restricted internal readers match parties assigned to themselves or, when subordinate visibility is active, their subordinates. Project and contract modules supply optional joins. Selecting a detail column joins the intervention's work lines when details are enabled. This can produce more than one row for the same intervention and changes what its dates mean.

| Selectors | Predicate |
| --- | --- |
| `search_ref`, fallback `search_inter`, `search_ref_client` | Intervention reference and separately stored customer reference. |
| `search_company`, `search_projet_ref`, `search_contrat_ref` | Party name, linked project reference and linked contract reference. |
| `search_desc`, `search_all` | Description searches the header and, when the work-line join is active, the line description. Search-all also searches reference, party name and public note, plus private note for internal users. |
| `search_status`, `search_signed_status` | Nonnegative workflow state and signature state are tested independently. |
| `search_date_start`, `search_date_end` | Append `day`, `month` or `year`. The bounds compare the actual work-line date and apply only with the detail join active. Neither bounds the header creation date. |
| `search_category_fichinter_list`, `search_category_fichinter_operator`, `catid` | Intervention tags. A supplied category ID seeds the selection if the explicit list is empty. Operator 1 gives any, the default gives all and −2 selects interventions without tags. |

With one header and two work lines dated Monday and Friday, a detail view bounded to Friday returns the Friday line. Hiding all work-line columns yields the header view, where the work-line date predicate is inactive.

## Internal ticket queue

The result is one ticket with an optional party. Ticket read is required. `socid` selects the party and defaults to the external user's company for an external reader. In internal `mode=mine`, the ticket must be assigned to the operator or, when assigned-only viewing is off, created by them. Assigned-only viewing applies to nonadministrators even on the ordinary list.

| Selectors | Predicate |
| --- | --- |
| `search_all`, `search_societe` | Search-all uses the reference, tracking identifier, origin email, reply-to, origin mail references, subject and stored party ID plus the joined party's alias, postal code and town. Use the separate company box for party name. |
| `search_fk_project`, `search_fk_contract` | Positive linked project or contract ID. `projectid` and `contractid` are fallbacks. A supplied `project_ref` is resolved to a project ID. |
| `search_fk_user_create`, `search_fk_user_assign` | Positive creator and assignee IDs. These are separate relationships even when one person holds both roles. |
| `search_fk_statut` | The multiselect accepts explicit states. `openall` expands to 0, 1, 2, 3, 5 and 7. `closeall` expands to solved 8 and canceled 9. The suspended option can be hidden individually while still belonging to the open-group expansion. |
| `search_type_code`, `search_category_code`, `search_severity_code`, `search_progress` | Type is a string-code set. Category and severity pass their selected codes to the text matcher. Progress uses numeric comparisons. |
| `search_date_{start,end}`, `search_dateread_{start,end}`, `search_dateclose_{start,end}` | Append `day`, `month` or `year`. These are inclusive bounds on creation, first-read and close time. On navigation, the page serializes the upper close date under creation-end parameter names. A subsequent page can therefore apply a different end-date restriction. |

The [field-derived selector table](metadata-keys.csv) names each ticket field consumed by the generic reader and identifies its field definition. Some fields are hidden in the standard list and some depend on configuration. The date controls above are the ones wired to explicit date comparisons. Although the input loop constructs generic date suffixes, the ticket predicate loop does not translate those suffixed names back to the underlying date column. A service implementing the screen can use the three named date ranges as its standard date contract.
