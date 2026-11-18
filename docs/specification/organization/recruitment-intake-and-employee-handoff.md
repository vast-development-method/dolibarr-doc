# Vacancy intake, offer decisions and employee setup

A vacancy identifies the work to be filled. An application identifies a person’s interest and the employer’s decision. A user record identifies the employee who can subsequently be assigned work. The vacancy can identify a recruiter, proposed supervisor, establishment, number of hires sought, planned date and indicative pay. The application has its own reference, identity details, origin, proposed remuneration, optional vacancy link and eventual employee link.

## Public intake

The public recruitment interface must be enabled in addition to the recruitment module. A draft vacancy is unavailable on the public detail page. A displayed vacancy can subsequently close. The submit action rereads its state and accepts applications only while it is validated/open. It requires a vacancy reference, surname and legitimate email address and uses the configured public-submission controls.

The public duplicate lookup compares the submitted email against existing applications in the relevant entity scope. It contains no vacancy condition and no filter for application state. A person already considered for one position can therefore be turned away by the public submission form for a second position using the same address. That result concerns the public intake channel. It does not mean a vacancy has exhausted its headcount.

A successful submission assigns the vacancy, personal/contact inputs, description and submission address to the new application, handles eligible custom fields, then creates and validates the record in one database transaction. The receiving recruiter sees a submitted application. Explicit recruiter entry is a separate route and can represent a candidate without a vacancy. The validation that admits an application for review has no effect on pay or employee rights.

## Decision rights and results

| Action on the ordinary card | Stored result |
| --- | --- |
| Submit a draft application | Move from draft 0 to validated 1. |
| Employer declines a submitted applicant | Application refused 8. No contract has been offered. |
| Employer makes an offer to a submitted applicant | Contract proposed 3. The proposed amount remains identifiable independently of the applicant’s requested amount and the pay advertised for the vacancy. |
| Applicant accepts the proposed contract | Contract signed 5. The user account is still a separate record. |
| Applicant declines the proposed contract | Contract refused 6. The reporting consequence differs from the employer declining an application. |
| Close recruitment on the vacancy | Record the vacancy outcome and append the closing text to its private notes when supplied. Existing applications retain their own decisions. |

The offer-or-decline and close-as forms require a positive selected outcome and only apply the change when the stored application is in the expected state. The ordinary decision writes use recruitment write authority. The application card uses the recruitment job-position permission family for reading, writing and deleting applications. Drafts offer deletion to a writer. After draft, deletion calls for the delete grant.

One vacancy may seek two hires. If the first person signs and the second declines the offer, the answers are two applications in states 5 and 6. Neither count is enough to determine the vacancy’s current publication state. Closing that vacancy separately prevents a further public submission.

## Converting a signed applicant into an employee

The signed application presents account creation to an operator with user-creation authority when no user is linked. The operator supplies a login. The action reads the vacancy’s proposed supervisor and creates an internal employee user. It copies given and family names, birth date, personal mobile and email. The application email supplies both the personal email and the user’s email. The initial salary value comes from proposed remuneration. An employer and applicant who agreed 3,200 after the applicant requested 3,600 therefore initialize the employee at 3,200.

After creation the action stores the new user ID on the application. Account creation failure rolls back the transaction. The subsequent application update is called without testing its return value before the outer commit. The account and the visible application link are distinct observable outcomes after an interrupted or failed handoff.

Creating this user does not assign the employee a job-profile position, release a payroll disbursement or complete every other candidate for the vacancy. An authorized operator subsequently records the work assignment and employment terms. The user’s supervisor and their leave or expense approvers are distinct role fields.
