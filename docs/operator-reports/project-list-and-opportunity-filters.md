# Project visibility and opportunity filters

The project list starts with one row per eligible project. It reads the project header, its optional party, parent project, opportunity stage and creating user. Project membership, the customer's sales team, authorship and an external business contact are four distinct relationships. They can all point to different people.

## Which records reach the list

The page requires project read permission. In the normal entity scope it uses the set of entities available for projects. A reader without the read-all-projects right receives public projects plus private projects on which the reader has an internal project contact assignment. The membership test uses the project ID, a contact type defined for projects with internal source, and the reader's user ID. Membership on another business object does not satisfy it. Read-all skips the membership restriction. An explicit party context on the list then keeps only projects with that exact party, including for read-all users.

| Selector | Field or relationship used on the eligible population |
| --- | --- |
| Public / private | Exact value of the public flag. Selecting private cannot enlarge the set the reader is allowed to see. |
| My projects | Sets the internal project user selector to the current reader. Public projects without that membership disappear from this selection. |
| Internal project user | Project's internal contact assignment to the selected account. All internal project role types qualify. |
| Project contact | A project assignment using an external contact type and the selected contact person ID. Its match further narrows the accessible projects. |
| Sales representative | Current assignment on the project's party. Selecting unassigned matches projects with no representative link on their party, including projects without a party. |
| Author | Search the login or first/last name of the account that created the project. The creator is displayed even if other users manage the work. |
| Party | Fixed party ID limits to that party. A text search on the party name also searches its alias when the separate alias column is hidden. When shown, name and alias have separate conditions. |
| Parent | Search by parent reference or title. With subprojects enabled, omitting children requires the parent ID to be null. |

For example, Ada has ordinary project read access. Project A is public with no members. B is private, assigned to Ada on an internal project role. C is private, belongs to a customer represented by Ada and has no internal assignment to Ada. D is private and records Ada as creator, also without that assignment. The default membership gate admits A and B. “My projects” admits B only. Filtering by representative can narrow the first two rows, but does not introduce C. Another reader with read-all permission can see all four before selecting other filters. This example assumes one shared project entity, matching lifecycle filters and no additional restrictions.

## Lifecycle, stage and purpose

The ordinary initial lifecycle selection is draft and validated/open, codes 0 and 1. Entering through the global search parameter omits this default. An explicit state list applies its selected values, the 99 shortcut means 0 or 1, and an unrestricted state selection admits closed projects too. “Late” forces state 1 and requires planned end strictly earlier than the current time less the configured project warning delay. A missing end date and an end date exactly at the threshold both fail.

Opportunity stage is a separate selector. A project may be operationally open after winning an opportunity. Project status and opportunity stage must both satisfy their filters.

| Opportunity choice | Rows admitted |
| --- | --- |
| Particular stage ID | Project stores precisely that stage ID. |
| All assigned stages | Stage ID exists and differs from the unassigned sentinel −1. |
| Open opportunities | An assigned stage other than the dictionary stages with codes WON or LOST. |
| Without an open opportunity (`notopenedopp`) | No stage, sentinel −1, or WON. A LOST project is outside this specific selection. |
| No opportunity stage | Null stage or sentinel −1. |

The flags for using opportunities, tasks, time billing and event organization are independent filters. Event projects can also be filtered by conference-proposal acceptance, booth-proposal acceptance, registration price and booth price. The economic inputs are opportunity amount, stored probability and budget. The weighted amount column derives opportunity amount × probability / 100. Thus 24,000 at 35 yields 8,400. This row calculation leaves a missing factor null at query level. Stage selection does not substitute a new probability. A won project with 35 still has a calculated weighting of 35% of its recorded amount.

## Dates and categories

| Operator selection | Project value | Consequence |
| --- | --- | --- |
| Planned start or planned end | Start and end are distinct project header dates. Each accepts its own inclusive lower and upper bounds, and each also supports date-part filtering. | Searching for projects starting in May and ending in June requires both conditions. A project spanning the same interval but starting in April is absent. |
| Created or modified | Record creation timestamp and last modification timestamp each accept an independent inclusive range. | A change in June can return an April-created project under the modification range. |
| Project categories | Membership of the project in the selected categories. | “All” needs every selected category. “Any” accepts one match. An unassigned category choice means the project has no category membership. |
| User categories | Categories of the **project creator**, reached via the joined author record. | Tagging an assigned project manager has no effect on this filter unless the manager is also the creator. A “none” selection means the creator has no user-category membership. |

If two categories and “none” are combined with “any”, untagged projects and projects meeting either tag qualify. Using “all” for a tag together with “none” leaves no matches. These existence tests preserve one project row when it satisfies several categories.

The project statistics page answers questions grouped by creation period. The project list instead exposes individual records and can filter the independent planned, creation and modification dates. [Project pipeline, time and staff costs](../reporting/projects-time-and-staff-costs.md)
