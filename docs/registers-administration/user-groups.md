# User groups and permission counts

One row represents a `usergroup` with its name, note, entity, creation date and modification time. Membership rows join on `usergroup_user.fk_usergroup`, and group grants join on `usergroup_rights.fk_usergroup`. Both joins are optional. New groups with neither members nor grants still appear.

| Decision | Register rule |
| --- | --- |
| Read | Requires user-read permission or administrator access. With advanced permissions, a nonadministrator also needs the group-read grant. Edit and deletion rights are evaluated separately with advanced group-specific grants where enabled. |
| Entity | Normally include global entity zero and the current entity. With multiple companies and the primary entity selected, transverse mode or a global administrator can select all groups with a nonnull entity. Centralized multi-company management can limit local editing rights even where groups are visible. |
| Name and notes | The all-fields search adds its condition over group name `nom` and `note`. The separately read group-search value does not contribute its computed expression to the base selection. |
| Totals | Group by the group's ID and displayed fields. Count distinct assigned user IDs and distinct assigned permission IDs. The pagination count uses distinct groups. This measures explicit group assignments, separate from a member's combined effective permissions. |
| Dates | Creation and modification belong to the group definition. The built-in selection adds no creation or modification range and does not infer when each member joined. |

A group with users A and B and three different rights has six joined combinations before aggregation. It displays one group, two users and three rights. If one right is also granted directly to A, the group's explicit permission count stays three.
