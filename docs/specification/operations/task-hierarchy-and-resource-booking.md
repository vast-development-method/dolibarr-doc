# Project task schedules, assignments and shared resources

The project schedule records what work is planned, when it should happen, who is associated with it and how much effort has been recorded. A separate calendar allocation can reserve a room, vehicle or piece of equipment. A technician appearing on a task and a resource being marked busy on a calendar event have different consequences for availability.

## Time, effort and hierarchy

| Task field | Business meaning |
| --- | --- |
| Project and optional parent task | Locate the work in the project breakdown. A root task belongs directly to the project. |
| Start and end | Calendar bounds of the task. Where both are supplied, the end must be at or after the start. |
| Planned workload | Estimated effort, stored in seconds. This can differ from the elapsed interval between start and end. |
| Effective duration | Accumulated logged time associated with the task. |
| Progress and status | Percentage reported on the task and its workflow state. The dedicated state commands and effort entries have different effects. |
| Rank and priority | Ordering and prioritization attributes. Parentage is represented independently. |
| Budget and billable flag | Monetary estimate and eligibility information kept independently from planned duration and logged effort. |

The chart loads tasks for the accessible project so a child can be displayed under its parent even when only the child carries an assignment for the current user. Tasks with children become groups, root tasks use the project as their grouping parent, and individual rows display their own start, end and progress. If a row has no end the renderer uses its start for display. The chart assembles the names of internal and external contacts associated with the task. Rendering a task with a technician's name does not allocate a number of working hours to that technician.

The standard chart builds no scheduling dependency edges. Its grouping parent controls nesting. Changing a parent or moving a preceding task's finish date does not establish a finish-to-start rule in this view. A four-hour inspection planned across Monday and Tuesday can therefore appear underneath an installation scheduled to finish on Wednesday. No resource conflict follows from that hierarchy alone. A dated reservation must be assessed on its own calendar event.

The task fields and date comparison are in `htdocs/projet/class/task.class.php`. Hierarchy assembly and rendering are in `htdocs/projet/ganttview.php` and `htdocs/projet/ganttchart.inc.php`.

## Reporting progress and closing work

The task edit action stores the submitted progress. Entering exactly 100 changes the task to closed, and an intermediate nonzero value changes it to ongoing. Entering zero through this form does not explicitly reset the existing task status. The separate validate, close and reopen actions request their respective workflow states directly. Reopen returns the task to draft. A reader who needs the progress percentage must read that field in addition to status.

When automatic project closure is enabled, the task update operation loads the containing project. For a validated project it examines its tasks and requests closure only if all have progress of at least 100. Failure to close the eligible project makes the update fail. A task modification event runs within the update and can also cause rollback. This comparison uses progress over the project's tasks. It neither sums employee hours nor compares actual duration with the project budget.

For example, two tasks can have consumed all sixteen hours budgeted for them while reporting 100% and 80%. The progress-based project closure still waits for the second task. Setting that task to 100 through edit can close the validated project. With automatic closure disabled, updating the two percentages leaves project closure to a separate action.

Task actions on the card require the project creation/modification grant for edit, clone, merge, validate, close and reopen. Ordinary task deletion uses the project deletion grant. Project visibility and access to the containing record still apply. The chart's create action also evaluates project-level write access or the project's public setting.

The card commands are in `htdocs/projet/tasks/task.php`. Project-wide progress evaluation is in `htdocs/projet/class/task.class.php` under `update`.

## Cloning a task versus merging recorded work

A clone creates a new task identity in the destination project and at the requested parent. The single-task card supplies its current project and parent. Planned effort, rank and priority are carried over. Progress resets to zero unless the caller selects progress copying. The operation can copy internal and external assignees with their role codes, attached files and notes through their respective options. The time-copy option has no implementing operation in the stable cloning routine. Cloning a task with six hours already logged therefore does not create six new hours of time entries.

Date shifting is relative to the start of the **source project**, falling back to the project's creation date. For each populated task date, the result is today's midnight plus the original offset from that project anchor. A task starting eight days after its original project starts will start eight days after the new anchor when cloned with date shifting. Without the shift, the source dates remain available to the clone. The schedule is not rebalanced around weekends or personnel availability by this operation.

A merge has a different accounting effect. The destination task keeps its identity. Empty destination fields may take selected source values, including planned workload, budget and progress. Zero counts as empty in that selection. Public and private notes are concatenated independently. Additional fields fill empty destination entries. The operation updates the destination, moves time rows, recomputes its actual duration from the moved and existing time entries, adds source contact roles, invokes extension notifications and removes the source. An error during these stages rolls back the database merge.

For a destination with four hours planned and two hours logged, merging a source with three hours planned and one logged retains the four-hour plan and yields three logged hours. Planned hours are filled when empty rather than added. A source task with dependent child tasks cannot be deleted by the ordinary deletion operation. The merge cannot complete its final removal in that case. Ordinary deletion also refuses an object still identified as in use, then removes linked contacts, remaining time and extra fields before deleting an eligible task. Direct deletion and merge have very different consequences for historical hours.

Cloning, contact and time transfer, merge and deletion are in `htdocs/projet/class/task.class.php` under `createFromClone`, `mergeContactTask`, `mergeTimeSpentTask`, `mergeTask` and `delete`.

## Calendar resource conflicts

A resource allocation identifies the resource and object by both type and ID. It records whether the resource is busy and whether its attendance is mandatory. The calendar interval comes from the linked event. The resource-link page requires write permission for additions and edits and delete permission for unlinking. Before editing or deleting a link it verifies that the link belongs to the object being viewed.

When event resource conflict detection is enabled, adding or updating a busy equipment/resource assignment compares the interval with other busy reservations for that resource. The comparison includes both endpoints and a reservation wholly contained within the candidate interval. On edit the current event is excluded. A full-day event with a missing end is expanded to cover the whole calendar day. The mandatory flag and the busy flag are independent. A mandatory but nonbusy assignment does not enter this busy-resource conflict path.

A room reserved from 09:00 to 10:00 conflicts with a second busy reservation starting at exactly 10:00 on that day under the inclusive comparison. Marking the second association informational leaves the room unreserved by that association. Changing a task's parent or dates does not itself modify either event reservation. When there is a detected conflict the linking operation reports the conflicting events and keeps the requested busy link from being written. The common association operation inserts the link and invokes its add-resource event in one transaction. A failed event rolls back the insert.

The allocation record is in `htdocs/install/mysql/tables/llx_element_resources.sql`. The interval comparison and access rules are in `htdocs/resource/element_resource.php`. Event creation and date-edit behavior are in `htdocs/comm/action/card.php`. The insertion and removal transactions are in `htdocs/core/class/commonobject.class.php`.
