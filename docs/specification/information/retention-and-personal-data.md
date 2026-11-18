# Retention periods, deletion and anonymization

A retention rule combines an object population, action and delay in calendar months. An administrator configures delays for the current entity. Only submitted settings are changed. A missing, zero or negative delay disables the corresponding action. Enabling the module registers an active daily scheduled job. The scheduler supplies the acting user for ordinary object updates and deletions.

The module also defines consent and opposition-to-processing or prospecting indicators on the relevant party, contact and member records. These record a person’s expressed choices. The scheduled retention selectors described below use dates, relationships and document history. Changing one of those indicators alone does not instruct the scheduler to remove the person immediately.

## Eligibility

Let the cutoff be the run time minus the configured number of calendar months. A record timestamp must be strictly earlier than the cutoff. Recent activity and subscription exclusions look for changes strictly later than the cutoff. Different policies choose different timestamps, so a common “last changed” predicate on every object produces different results.

| Population | Selection and action |
| --- | --- |
| Customers, prospects and dual customer/prospects who are not suppliers | The party’s modification timestamp must be old, it must have no recent activity linked by party, and it must have no sales invoice. Each population has its own anonymization delay. The invoice exclusion has no age cutoff. |
| Parties that are neither a customer nor a prospect nor a supplier | Same age, activity and sales-invoice criteria. Independent delays permit deletion and anonymization. Deletion is considered first. |
| Suppliers | The supplier flag determines membership in this population. Use party modification time, recent party activity and presence of any supplier invoice. Even an old purchase invoice excludes the supplier from this rule. |
| Contacts of parties in those groups | Join to the parent party to determine classification. Use the contact’s own modification timestamp, absence of recent activity linked to the contact and absence of the relevant kind of invoice at its parent. Supplier contacts use purchase invoices. Only linked contacts qualify under these joins. |
| Members, when membership is enabled | Use the membership paid-through date instead of the member’s modification time. Require absence of recent member activity and recently modified subscriptions. A member with no paid-through date does not meet a strictly-earlier expiry condition. The rule supports anonymization. |
| Job applications, when recruitment is enabled | Select old application modifications with no recently modified activity linked to that application. The configured action is deletion. |

An eligible supplier last edited 30 months ago may still be retained indefinitely by this particular rule if a supplier invoice exists. A lapsed member recently renewed or corrected in the subscription register is excluded by the recent-subscription check, even if the member header still shows an old end date. Neither case can be decided from the displayed age of the master record alone.

## What changes on an eligible record

Deletion calls the object’s ordinary deletion operation. Where a child-reference check is available and reports use, the worker skips deletion without treating that skip as an error. Anonymization can still be considered for a skipped object under its own active rule. For example, an outstanding commercial relationship can prevent hard deletion, while a configured anonymization rule with its own eligibility conditions can retain references under the same record ID.

Anonymization replaces configured name components with field-specific anonymous names incorporating the row ID. Other populated fields receive the profile’s replacement. A populated email can become an ID-specific address in the reserved example domain. Profiles can replace addresses, postcodes, phone numbers, professional identifiers, location coordinates, network addresses and social account values. The member profile additionally covers notes, birth date and administrative status. The policy does not traverse arbitrary textual material looking for a person’s name. An attachment or a past generated document can thus still contain an earlier value.

The custom-attribute pass considers personal attributes defined for this object’s storage type in the shared or current entity. Only loaded, nonempty values are replaced. Multi-select and checkbox fields are cleared to an empty collection, boolean and radio fields to zero, date/time fields to 1 January 1900, and recognized numeric fields to zero. Remaining types receive a fixed redacted text marker. The worker performs the ordinary object update and then requests an extension-value write after a positive update result.

## Execution and limits

The worker processes deletion before anonymization for each policy, maintains separate updated and deleted totals and wraps the run in a database transaction. Reported errors cause rollback. A referenced object skipped for deletion differs from an object whose delete operation returned an error. A successful run can legitimately process zero records. The administrator’s configured delay and the scheduled actor authorize the job to process eligible records without individual human approval.

The stable worker keeps a single set of **numeric row IDs** already attempted during the run. This set spans object types and is populated after calling the action handler. Consequently, if a candidate party and an unrelated candidate contact both have row ID 42, processing the party can make the contact skip this run. The reported totals count operations completed during that run. This is a property of the implementation that matters when interpreting a retention report.

Retention applies to the operational records and fields named by the policy. Old temporary files and log cleanup use distinct administrators’ actions, thresholds and physical storage operations. Revoking a shared document key can prevent future access through that key but does not rewrite copies already downloaded or update the source customer.
