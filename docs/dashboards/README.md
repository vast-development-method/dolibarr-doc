# Dashboards and personal work queues

An operator can see three different measures on the home page. A work queue counts all qualifying items and the subset considered late. A state-board tile asks its domain for a population count. A configurable shortlist shows selected records in a specified order. An order can appear in all three. Each calculation has its own grain, permission checks and date basis.

| To answer | Read |
| --- | --- |
| What can a user place on a dashboard, and what does each widget display? | [Widget catalogue](widget-catalogue.md) |
| Which work remains, when is it late, and how does the home page combine the counts? | [Home work queues](home-work-queues.md) |
| Why do a shortlist, a chart and a report disagree on the same day? | [Reconciling dashboard figures](reconciling-figures.md) |
| What fields does one successful work queue expose to another interface? | [Workboard row schema](../../schemas/reporting/workboard-row.schema.json) and [worked invoice example](../../examples/reporting/workboard-row.json) |

## Registering and placing a widget

The dashboard catalogue covers 62 widgets. **58** have fixed, matching targets in module declarations. These include widgets hidden by default and widgets whose declared page name does not match a registered page. **Two feed types** use setup data to create individual definitions. **Two more files** implement charts without a matching current registration. The [catalogue](widget-catalogue.md) accounts for each implementation once. The combined versus split supplier module setting selects which supplier descriptors apply. Repeated declarations of a shared widget do not identify different dashboards.

A widget definition stores the source key, entity, optional user and optional note. The note distinguishes feed instances that share one renderer. A placement references a definition, entity, numeric page, user and column/order. The placement key is unique on entity, definition, page and user. User zero is a shared placement. During ordinary module enablement, the registrar looks up the definition by file and entity and, if populated, note. It creates missing definitions and seeds shared placements for matching zone names. Definition-only initialization skips those placements. An existing definition does not trigger another round of default placements during this pass.

| Ordinary zone | Exact name | Page consuming that zone |
| --- | --- | --- |
| 0 | Home | ERP home |
| 1 | UsersHome | Users |
| 2 | MembersHome | Members |
| 3 | ThirdpartiesHome | Business partners |
| 4 | productindex | Products and services |
| 11 | TicketsHome | Support tickets |
| 20 | interventionindex | Field interventions |
| 27 | AccountancyHome | Accounting |

The registrar compares the descriptor’s default page name with the zone name. The membership, accounting, support and knowledge descriptors request `membersindex`, `accountancyindex` or `ticketindex` for 12 implemented widgets. None of these strings matches the corresponding zone name. With fresh module registration these definitions are available for placement, and the default-placement loop creates no shared rows for them. Existing installations may already have placements. Two additional declarations, a member list and a new-versus-closed ticket chart, resolve to no widget. The dashboard skips both.

Feed setup has distinct semantics. Adding an RSS source creates a definition distinguished by a feed number and title. Module initialization can also discover saved feed-title settings and register such instances. The social-network setup creates a named definition and stores its associated source settings in the current entity. A feed definition created in either setup screen still needs a page placement to appear. Renaming or removing a feed affects the data behind that particular instance.

## How visibility and personalization interact

1. The administrator enables a definition on a page. The add operation checks existing placements for the shared layout and users who already personalized that zone, then adds a missing one to the less populated column. Ties go to the left. Removing a definition from active layouts by the administrator deletes placements for that definition across the current entity, including personalized layouts.
2. A user without a personalized layout receives shared placements for the zone. Once their personal layout flag is set, rendering selects their own placements. Shared placements they have omitted can be offered in the add-widget list. Closing a widget is a personal layout change.
3. Saving a personal layout sets its user-and-zone flag and replaces that user's placement rows in the current entity and zone in a transaction. Column letters and positions reconstruct the order. Saving an empty layout can leave a personalized page with no visible widgets.
4. The renderer loads the matching widget, checks its enabled state and module dependencies, then applies its hidden flag. Each dependency group must be satisfied. A pipe inside one group permits alternative modules. Some widgets enforce the read grant inside their data loader. Page placement alone grants no business permission.
5. The user’s shortlist limit takes precedence over the site setting and defaults to five rows. Each widget decides how to apply it. Period series, grouped summaries, feed limits and full-population totals have their own rules.

The page-specific counters and charts built directly by a domain home page can still appear when its configurable zone is empty. For instance, the annual ticket status chart on the support page has its own calendar and access filters.
