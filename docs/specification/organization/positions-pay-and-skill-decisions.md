# Employee assignments, compensation fields and skill decisions

An employment record establishes dates and remuneration. A position assigns a user to a job profile for a date range. A job profile defines required skills. An evaluation freezes those requirements and records a particular assessment. These records have different owners and can change independently over a career.

## Work assignment and remuneration

| Record | Business dates and fields | Use |
| --- | --- | --- |
| Employee user | Employment start/end, employee indicator, supervisor, expense approver, leave approver, account validity dates | Identifies the person, reporting hierarchy and routing choices. Account validity dates and employment dates have separate fields. |
| Position | Employee, job profile, mandatory start, optional end, description, author/modifier, optional contract link and ending comment | Preserves a dated assignment to a specific job. The optional contract relation depends on the contract module. |
| Employment terms | Entity, employee, reference, job text, status, start/end, monthly salary, monthly supplement and weekly hours | The schema supports a separate employment-period record. The ordinary user form writes the current values on the employee. Its save action has no demonstrated automatic historical snapshot for each salary change. |
| Current compensation | Hourly and daily rates, monthly salary and supplement, weekly hours | Used as distinct numeric inputs. A field intervention can estimate value from the hourly rate. Actual [salary obligations and payments](../people-and-services/employee-payables.md) have their own period, amount and cash links. |

The position card distinguishes HR read, write and delete. The employee-position lookup returns all matching employee rows in record order, including historical and future assignments. To find who held a job on a date, the caller needs an effective-date condition. First or last row by identity alone cannot answer it. A job profile change does not rewrite an existing position’s dates.

The user card applies an additional salary-visibility decision before accepting changes to hourly rate, daily rate, salary, salary supplement or weekly hours. With the relevant modules active, internal actors qualify through employee-scope salary read, all-salary read or HR employee read. Employee-scope salary access considers the selected employee in the allowed hierarchy. The no-salary/no-HR-module fallback uses administration, new-record or hierarchy conditions. A user’s ability to change other account details does not automatically make the compensation fields writable. Numeric inputs are normalized separately, with blank values distinguished from an explicitly entered zero at form intake.

Implementation evidence appears in `htdocs/hrm/position_card.php:65–79`, `htdocs/hrm/class/position.class.php` (`getForUser`, field definition), `htdocs/user/card.php:165–174,349–375,552–582` and `htdocs/install/mysql/tables/llx_user_employment.sql`.

## Establishing the comparison baseline

A skill definition owns the meaning of each ordered level. A rank association identifies the skill, rank and an owner type and ID. A rank owned by a job expresses a target. A rank owned by a user expresses that user’s current attained level. Joining only on skill and numeric owner ID is ambiguous because job IDs and user IDs are independent sequences.

Creating an evaluation saves the header and reads the job’s current required ranks. For each it attempts to create an evaluation line containing the new evaluation ID, skill and required level. Consequently the assessed baseline is a snapshot. If a job’s target rises from 2 to 4 tomorrow, an evaluation created today can still show 2. The loop retains successfully created lines and returns the header creation result. The presence of a header by itself does not establish that every target line was copied.

Staff save the assessed rank against the skill. The not-applicable choice is encoded as −1. The pre-validation form flags an evaluation with no selected rating other than zero/blank. The ordinary validation authority comes from evaluation write, or from an explicit advanced validation grant with advanced permissions enabled. The list requires evaluation read. Without the read-all grant it filters to the acting user and their reporting hierarchy. The comparison screen also recognizes its advanced comparison permission.

Implementation evidence appears in `htdocs/hrm/class/evaluation.class.php:251–281`, `htdocs/hrm/evaluation_card.php:93–110,138–177` and `htdocs/hrm/evaluation_list.php:146–165,299–302`.

## Publishing assessed skills to the employee

Closing the evaluation copies each assessed skill to the employee’s rank set. Existing skill records are matched by skill identity and updated where found. Missing ones are created with employee ownership, the line’s rank and creator/modifier information. A negative not-applicable rank can reach employee skill storage through this route. Other skills already recorded for the employee and absent from the evaluation are left alone.

Closure performs multiple writes. Certain creation failures are counted, and the existing-rank update path does not examine every update result before requesting closed status. Reopening places the evaluation back in validated state. It does not reverse the employee skill assignments previously published. The “last evaluation” helper orders by assessment date descending, limits the result to one, and applies no status filter. It can return a more recent draft even when an earlier closed evaluation supplied the employee’s current rank.

A group comparison computes the **highest nonnegative recorded employee rank per skill** among the selected employees. It then counts employee-rank rows tied at that maximum. The result describes demonstrated coverage and concentration of expertise. For ranks 2, 4, 4 and −1, the displayed group maximum is 4 and the number at that maximum is two. A job-profile comparison reads the required rank for the same skill independently. Comparing 4 against a job target of 3 says that someone in the group meets the target. It does not show that everyone meets it. An employee with no recorded rank supplies no rank to the calculation.

Implementation evidence appears in `htdocs/hrm/evaluation_card.php:194–243`, `htdocs/hrm/class/skillrank.class.php:356–371`, `htdocs/hrm/class/evaluation.class.php:646–671` and `htdocs/hrm/compare.php:399–432,531–579,597–632`.
