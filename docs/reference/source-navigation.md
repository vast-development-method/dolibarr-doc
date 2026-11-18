# Find a workflow and its records

Follow the transaction from the operator's action to the record carrying its result. A balance, state change or document often depends on more than one entity.

| Operator task | Decision or calculation | Record or service to follow |
| --- | --- | --- |
| Register a customer or supplier | [Party roles and contacts](../sales/parties-and-contacts.md) | [Party identifiers and relationship fields](../records/parties.md) |
| Validate a sales order | [From accepted offer to order and partial billing](../specification/commercial/sales-conversion-and-partial-billing.md) | [Order actions and grants](../services/orders.md) |
| Approve supplier commitments | [Quote selection, approval thresholds and order details](../specification/commercial/supplier-sourcing-and-approval.md) | [Supplier order service](../services/supplier-orders.md) |
| Receive or issue stock | [Lot identity and warehouse quantities](../specification/operations/lot-identity-and-traceability.md) | [Stock positions, movements and lot references](../records/warehouse.md) |
| Validate a customer invoice | [Validation, settlement and credit notes](../finance/customer-invoices.md) | [Invoice header, lines and allocations](../records/billing.md) |
| Inspect a bank movement | [Statement assignment, cheque deposit and returned receipt](../specification/financial/bank-statements-and-cheque-deposits.md) | [Bank and cash records](../records/cash.md) |
| Post a journal entry | [Source document, account mapping and journal transfer](../specification/accounting/source-journal-postings.md) | [Ledger, chart and accounting period](../records/accounting.md) |
| Estimate batch and unit costs | [Workstation time, materials and services](../specification/planning/workstation-requirements-and-cost.md) | [Bill of materials service](../services/boms.md) |
| Plan or complete a production run | [Nested requirements and production posting](../specification/operations/nested-production-orders.md) | [Production records](../records/production.md) |
| Grant project access or schedule a resource | [Task hierarchy, assignments and booking overlap](../specification/operations/task-hierarchy-and-resource-booking.md) | [Project and participant service](../services/projects.md) |
| Activate a service period | [Agreement validation, service activation and repeat visits](../specification/people-and-services/contract-services-and-work-templates.md) | [Contract operations](../services/contracts.md) |
| Route a support request | [Ticket assignment, conversation and resolution](../specification/people-and-services/ticket-routing-and-conversation.md) | [Ticket service](../services/tickets.md) |
| Approve a staff absence | [Leave routing and group decisions](../workforce-operations/leave-routing-and-group-decisions.md) | [Entitlement calculation and movements](../specification/people-and-services/leave-entitlement-ledger.md) |
| Review an expense claim | [Review and reimbursement](../workforce-operations/expense-review-and-reimbursement.md) | [Claim lines, mileage and ceilings](../specification/people-and-services/expense-scales-and-ceilings.md) |
| Check membership coverage | [Renewal periods and receipts](../specification/people-and-services/member-renewals-and-collections.md) | [Membership subscription register](../specification/people-and-services/member-subscription-register.md) |
| Assign participants to an appointment | [Series, reminders and participants](../specification/planning/calendar-series-and-reminders.md) | [Calendar activity service](../services/agendaevents.md) |
| Reconcile attendance with registrations | [Capacity, registration and payment](../specification/planning/event-capacity-registration-and-payments.md) | [Attendee service](../services/eventattendees.md) |
| Review a scheduled operation | [Job attempts, overlap and recovery](../specification/administration/job-attempts-and-recovery.md) | [Platform fields](platform.csv) |
| Verify financial event evidence | [Signatures, predecessor links and period boundaries](../specification/administration/evidence-and-period-archives.md) | [Business event catalogue](../events/README.md) |

The [field and relationship reference](README.md) supports cross-domain queries. For example, a resource attachment establishes which appointment and resource are linked. The scheduling decision also depends on the start and end of existing assignments. A list of foreign keys alone cannot explain whether the second booking will be accepted.
