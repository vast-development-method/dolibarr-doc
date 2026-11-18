# Membership, engagement and operating registers

| Register | Unit represented by a row | Decision the register supports |
| --- | --- | --- |
| [Members](members.md) | Member with a matching member type | Identify memberships that require renewal or still await a first subscription. |
| [Contacts](contacts.md) | Contact visible under the selected privacy and party rules | Find reachable people, their roles and their party affiliations. |
| [Calendar activities](calendar.md) | Activity with a matching activity type | Identify work affecting a user, resource, project or day. |
| [Email campaigns](campaigns.md) | Campaign, or matching target row in the email-specific view | Distinguish campaign state from delivery state for one address. |
| [Surveys](surveys.md) | Survey header | Separate an open response window from the survey's saved status. |
| [Supplier products and prices](supplier-prices.md) | Product with each matching supplier price, or an unpriced product | Find purchasing offers and their quantity breaks. |
| [Resources](resources.md) | Resource master | Find a room or other resource by type, location and stated capacity. |
| [Variant attribute definitions](attributes.md) | Attribute definition with aggregate counts | Find defined values and the number of distinct combinations using the attribute. |

In the field tables, a **keyword** search applies the register's shared text matcher. Ordinary space-separated words narrow the match and a vertical bar expresses alternatives. A **numeric** search accepts comparison expressions such as `>=10`. An **ID list** tests membership of the selected numeric values. The chapters call out direct equality, literal substring patterns and filters applied after grouping when those differ. Extensions can add fields or restrict rows. The worked selections describe the built-in predicates.
