# Assessment and hiring queues

A supervisor looking for assessments starts with an employee hierarchy. A recruiter opening applications from a vacancy starts with a vacancy identifier. These selections answer different questions. The applicant can still be a person outside the employee directory. The lists expose the following standard operations on selected rows.

| List | Grants read by the list | Selection menu |
| --- | --- | --- |
| Job profiles, employee positions and skills | The shared HR `all` family supplies `read`, `write` and `delete`. | Delete with the delete grant. |
| Employee assessments | The `evaluation` family supplies `read`, `readall`, `write` and `delete`. | Delete with assessment delete. Skill publication requires opening the assessment. |
| Vacancies | The recruiting `recruitmentjobposition` family supplies `read`, `write` and `delete`. | Delete with vacancy delete. The decision to close a vacancy is on the individual record. |
| Applications | The same recruiting grants as vacancies. Opening the vacancy's application list restricts results to its identifier. | Validate is offered. The execution handler requires recruiting write. Delete appears with recruiting delete. |

The common deletion routine collapses repeated identifiers before fetching records. An object that implements the erasability check can reject removal because it still has children. This produces a warning and allows processing to continue. A zero result from deletion also contributes messages without aborting. A missing selected row or negative deletion result aborts processing and rolls back the database transaction. In a mixed selection, the success count describes only objects actually deleted.

## Who can see personal information

An assessment list requires assessment read and an internal user. Without `evaluation.readall`, the list filters on the assessed employee being the actor or one of their descendants. The assessment's employee picker additionally requires an active user. A recruiter who can read applications acquires neither assessment right through that recruiting grant. The assessment field definitions omit both public and private notes from the ordinary field display. The notes and attachments pages separately apply assessment record access and require assessment read. The notes editor and attachment actions use assessment write.

An application queue displays the applicant's name, email, phone and vacancy among its default columns. Birth date, requested remuneration, proposed remuneration and linked employee are available as optional columns in the standard field selector. Both note fields and the submission IP address have zero list visibility and are omitted from that selector. Turning off a compensation column changes the presentation for that list. A reader can select it again. Consequently, a saved view with names and email alone promises less information on screen, but it grants exactly the same underlying recruiting access.

## From a reviewed assessment to current employee skills

A draft assessment with lines offers validation using ordinary assessment write or, with advanced permissions enabled, the dedicated assessment validation grant. On a validated assessment, the standard card enables its Close button using the delete grant. The write-based alternative in that button condition tests for closed status inside the validated-only branch and cannot enable the button there. The close action itself requires assessment write. A user with both write and delete can complete the ordinary card workflow. Someone who can validate under advanced permissions may therefore be unable to publish the outcome. A closed assessment offers Reopen using assessment write.

Closure loads the employee's existing skill ranks once. It matches each assessment line by skill, updates existing ranks and creates missing ranks. These writes take place one line at a time. If the employee initially has no ranks, a failed creation is counted and the card withholds closure. With a nonempty initial set, the loop does not inspect every update or creation result before marking the assessment closed. Reopening returns the assessment to validated status, retaining the employee ranks previously written.

For example, an employee has machine setup at rank 1. Their assessment gives setup rank 3 and adds inspection at rank 2. After successful closure the employee profile shows both values. Reopening to correct setup leaves the published rank at 3 until a later action changes that profile. The [position and skills specification](../specification/organization/positions-pay-and-skill-decisions.md) covers skill baselines and comparisons between employees and teams.

## Receive multiple applications, then decide each offer

Bulk validation fetches each application in selection order and validates it under the operator's identity. A successful draft becomes received, awaiting interview. It retains an existing definitive reference or receives one when its current reference is provisional or empty. The validation event precedes the migration of indexed attachments from a provisional reference. The action also attempts to rename the physical directory and matching filenames. The database transaction controls the indexed records. Physical renames and effects produced by event consumers can outlast a database rollback.

An already received application returns zero. The list treats this as a stopping error, as it does a failed fetch or negative validation result. Consider draft A, received B, draft C selected in that order. In the default shared transaction, A's database changes roll back on B and C is untouched. When `MAIN_MASSVALIDATE_RECRUITMENTCANDIDATURE_NO_GLOBAL_TRANSACTION` is enabled, A commits on its own. B stops the run, and C still awaits intake. Automatic document generation, when enabled, runs after each positive validation. A negative generation result displays an error without undoing that successful validation by itself.

Reception leaves the offer, employment terms and employee identity undecided. On the individual card, recruiting write permits a decision to decline or propose a contract on a received application. The next decision operates on a proposed contract and records signed or declined. Only the signed card with no linked user presents the employee-creation action, which requires user creation authority. The [recruitment handoff](../specification/organization/recruitment-intake-and-employee-handoff.md) describes how proposed pay, supervisor and personal contact fields reach the employee record.
