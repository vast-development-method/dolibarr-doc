# Recruitment, employee assignments and skill evaluations

Recruitment tracks vacancies and applicants. HRM tracks an employee's actual assignment and the skills required for a job. A signed offer links the two through a separate user-creation action. The two modules can be enabled independently.

## Records through an employment decision

| Record | Business identity and data |
|---|---|
| Vacancy | Entity and reference, role label, number sought, recruiter, proposed supervisor, establishment, planned date, indicative remuneration; optional third party and project |
| Application | Applicant's name and contact details, requested/proposed pay, origin, optional vacancy, state and eventual internal user ID. The vacancy foreign key permits unsolicited applications |
| Employee assignment | User, job profile, optional contract association, effective start/end dates, comments. This records who holds the job |
| Skill and rank | Each skill can define descriptions for its ordered levels. A skill-rank record names the skill, level and an object type plus ID, distinguishing a job requirement from an employee's attained level |
| Evaluation | Reference, employee, job, date and state. Each evaluated skill records required and assessed ranks plus a comment |

## Hiring workflow

The vacancy has its own draft (0), open/validated (1), recruited (3) and canceled (9) states. Closing a vacancy can append a note to its private notes and run the corresponding recruitment-completion trigger. Each application moves independently. An operator can keep recruiting against a multi-head vacancy after deciding an individual application.

| Application action | Precondition on the ordinary card | Result |
|---|---|---|
| Validate application | Draft (0), recruiter with write authority | Submitted/validated (1) |
| Make offer or decline application | Submitted (1), chosen outcome | Contract proposed (3) or application refused (8) |
| Record candidate's decision | Contract proposed (3), chosen outcome | Contract signed (5) or contract refused (6). Distinguish a candidate declining an offer from the employer declining the application |
| Create login | Card offers action on signed application when no user is linked. User-creation authority is separate from recruiting authority | Create an internal employee with chosen login, name, contact details, birth date, proposed salary and vacancy supervisor. Store resulting user ID on the application |

The standard REST adapter exposes the vacancy and application as separate resources, each with get/list/create/update/delete operations. The adapter declares `GET jobposition/{id}` relative to its own service, and `GET candidature/{id}` for the applicant. The recruitment read grant and per-record access govern lookup. A missing record yields 404. Use the card's business decision sequence above when designing an application-state command.

## Evaluation and employee skills

Create an evaluation for the employee against a specific job. the ERP looks up the job's skill-rank rows and copies the required ranks into new evaluation lines. Each evaluation therefore retains the target level in force at capture. A later job-profile change does not recalculate those stored targets. The card compares the employee's assessed rank against its corresponding required rank; either negative value displays a non-comparable result. Required rank zero denotes a skill the job does not require.

Evaluation permissions distinguish reading, editing, validating when advanced grants are enabled, deleting and reading all evaluations. Displaying comparisons and accessing personal HR data have their own grants. On the card, validation catches an entirely empty/zero set of marks. Closing copies assessed ranks into employee-owned skill records, adding or updating the matching skill. Reopen restores validated state without undoing the ranks that closure copied. The close handler performs multiple individual writes; its checked branches do not establish an all-or-nothing batch guarantee. Verify the destination ranks after an interrupted close.

| Acceptance case | Expected result |
|---|---|
| Two candidates for one vacancy; employer declines A, B declines an offer | A is in state 8, B is in state 6; neither creates an employee |
| Signed application with proposed salary and designated supervisor; recruiter's only permission is recruitment write | No create-login action. A user administrator can use that action separately |
| Evaluation captured while required rank is 3; the job now requires 4 | The existing evaluation line still carries 3. A new evaluation copies 4 |
| Evaluation records attained rank 2 against required rank 3 | Display below target. Successful close writes level 2 to the employee; reopen leaves the employee rank in place |

The [hiring decision schema](../../schemas/workforce/hiring-decision.schema.json) describes the two card decisions and their permitted inputs. Current state and actor authority are stored-record checks.
