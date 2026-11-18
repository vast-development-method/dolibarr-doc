# People, membership and support events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. An agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch and subscription rules.

| Event | Setup meaning or origin | Emitting operation | Specific subscriber branches |
| --- | --- | --- | --- |
| `CONFERENCEORBOOTHATTENDEE_VALIDATE` | Operation signal | `conferenceorboothattendee.validate` | No dedicated branch listed |
| `CONFERENCEORBOOTH_VALIDATE` | Operation signal | `conferenceorbooth.validate` | No dedicated branch listed |
| `EXPENSE_REPORT_APPROVE` | Expense report approved (setup dictionary) | `expensereport.setApproved` | Notification |
| `EXPENSE_REPORT_CANCEL` | Operation signal | `expensereport.set_cancel` | No dedicated branch listed |
| `EXPENSE_REPORT_CREATE` | Expense report created (setup dictionary) | `expensereport.create` | No dedicated branch listed |
| `EXPENSE_REPORT_DELETE` | Expense report deleted (setup dictionary) | `expensereport.delete` | No dedicated branch listed |
| `EXPENSE_REPORT_DENY` | Operation signal | `expensereport.setDeny` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_CREATE` | Operation signal | `expensereportline.insert` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_DELETE` | Operation signal | `expensereport.deleteLine` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_MODIFY` | Operation signal | `expensereportline.update` | No dedicated branch listed |
| `EXPENSE_REPORT_MODIFY` | Expense report modified (setup dictionary) | `expensereport.update` | No dedicated branch listed |
| `EXPENSE_REPORT_PAID` | Expense report billed (setup dictionary) | `expensereport.setPaid` | No dedicated branch listed |
| `EXPENSE_REPORT_UNPAID` | Operation signal | `expensereport.setUnpaid` | No dedicated branch listed |
| `EXPENSE_REPORT_VALIDATE` | Expense report validated (setup dictionary) | `expensereport.setValidate` | Notification |
| `HOLIDAY_APPROVE` | Holiday approved (setup dictionary) | `holiday.approve` | Notification |
| `HOLIDAY_CANCEL` | Holiday canceled (setup dictionary) | `api_holidays.cancel` | No dedicated branch listed |
| `HOLIDAY_CREATE` | Holiday created (setup dictionary) | `holiday.create` | No dedicated branch listed |
| `HOLIDAY_DELETE` | Holiday deleted (setup dictionary) | `holiday.delete` | No dedicated branch listed |
| `HOLIDAY_MODIFY` | Holiday modified (setup dictionary) | `holiday.update` | No dedicated branch listed |
| `HOLIDAY_VALIDATE` | Holiday validated (setup dictionary) | `holiday.validate` | Notification |
| `HRM_EVALUATION_CREATE` | HR Evaluation created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_DELETE` | HR Evaluation deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_MODIFY` | HR Evaluation modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_UNVALIDATE` | HR Evaluation back to draft (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_VALIDATE` | HR Evaluation validated (setup dictionary) | `evaluation.validate` | No dedicated branch listed |
| `HRM_JOB_VALIDATE` | Operation signal | `job.validate` | No dedicated branch listed |
| `HRM_POSITION_VALIDATE` | Operation signal | `position.validate` | No dedicated branch listed |
| `HRM_SKILLDET_VALIDATE` | Operation signal | `skilldet.validate` | No dedicated branch listed |
| `HRM_SKILLRANK_VALIDATE` | Operation signal | `skillrank.validate` | No dedicated branch listed |
| `HRM_SKILL_VALIDATE` | Operation signal | `skill.validate` | No dedicated branch listed |
| `KNOWLEDGERECORD_CANCEL` | Knowledgerecord cancel (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_CREATE` | Knowledgerecord created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_DELETE` | Knowledgerecord deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_MODIFY` | Knowledgerecord modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_REOPEN` | Knowledgerecord reopen (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_SENTBYMAIL` | Mails sent from knowledgerecord file (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_UNVALIDATE` | Knowledgerecord unvalidated (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_VALIDATE` | Knowledgerecord Evaluation validated (setup dictionary) | `knowledgerecord.validate` | No dedicated branch listed |
| `MEMBER_CREATE` | Operation signal | `adherent.create` | No dedicated branch listed |
| `MEMBER_DELETE` | Member deleted (setup dictionary) | `adherent.delete` | Agenda |
| `MEMBER_EXCLUDE` | Member excluded (setup dictionary) | `adherent.exclude` | Agenda |
| `MEMBER_MODIFY` | Member modified (setup dictionary) | `adherent.update` · `adherent.mergeMembers` | Agenda |
| `MEMBER_NEW_PASSWORD` | Operation signal | `adherent.setPassword` | No dedicated branch listed |
| `MEMBER_RESILIATE` | Member resiliated (setup dictionary) | `adherent.resiliate` | Agenda |
| `MEMBER_SENTBYMAIL` | Mails sent from member card (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MEMBER_SUBSCRIPTION_CREATE` | Member subscribtion recorded (setup dictionary) | `subscription.create` | Agenda |
| `MEMBER_SUBSCRIPTION_DELETE` | Member subscribtion deleted (setup dictionary) | `subscription.delete` | Agenda |
| `MEMBER_SUBSCRIPTION_MODIFY` | Member subscribtion modified (setup dictionary) | `subscription.update` | Agenda |
| `MEMBER_TYPE_CREATE` | Operation signal | `adherent_type.create` | No dedicated branch listed |
| `MEMBER_TYPE_DELETE` | Operation signal | `adherent_type.delete` | No dedicated branch listed |
| `MEMBER_TYPE_DEL_MULTILANGS` | Operation signal | `adherent_type.delMultiLangs` | No dedicated branch listed |
| `MEMBER_TYPE_MODIFY` | Operation signal | `adherent_type.update` | No dedicated branch listed |
| `MEMBER_TYPE_SET_MULTILANGS` | Operation signal | `adherent_type.setMultiLangs` | No dedicated branch listed |
| `MEMBER_VALIDATE` | Member validated (setup dictionary) | `adherent.validate` | Agenda |
| `PARTNERSHIP_ACCEPT` | Operation signal | `partnership.approve` | No dedicated branch listed |
| `PARTNERSHIP_CREATE` | Partnership created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_DELETE` | Partnership deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_MODIFY` | Partnership modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_SENTBYMAIL` | Mails sent from partnership file (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_VALIDATE` | Operation signal | `partnership.validate` | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_CREATE` | Candidature created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_DELETE` | Candidature deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_MODIFY` | Candidature modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_SENTBYMAIL` | Mails sent from candidature record (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_VALIDATE` | Operation signal | `recruitmentcandidature.validate` | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_CREATE` | Job created (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_DELETE` | Job deleted (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_MODIFY` | Job modified (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_SENTBYMAIL` | Mails sent from job record (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_VALIDATE` | Operation signal | `recruitmentjobposition.validate` | No dedicated branch listed |
| `TICKET_ASSIGNED` | Ticket assigned (setup dictionary) | `ticket.assignUser` | Agenda |
| `TICKET_CLOSE` | Ticket closed (setup dictionary) | `ticket.close` | No dedicated branch listed |
| `TICKET_CREATE` | Ticket created (setup dictionary) | `ticket.create` | Workflow |
| `TICKET_DELETE` | Ticket deleted (setup dictionary) | `ticket.delete` | No dedicated branch listed |
| `TICKET_MODIFY` | Ticket modified (setup dictionary) | `ticket.update` · `ticket.markAsRead` · `ticket.setReadDate` | No dedicated branch listed |
| `TICKET_SENTBYMAIL` | Ticket message sent by email (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `USERGROUP_MODIFY` | Operation signal | `usergroup.addrights` · `usergroup.delrights` | No dedicated branch listed |
| `USER_CREATE` | User created (setup dictionary) | `user.create` · `user.create_from_contact` | No dedicated branch listed |
| `USER_DELETE` | User update (setup dictionary) | `user.delete` | No dedicated branch listed |
| `USER_ENABLEDISABLE` | User update (setup dictionary) | `user.setstatus` | No dedicated branch listed |
| `USER_MODIFY` | User update (setup dictionary) | `user.addrights` · `user.delrights` · `user.setForcePasswordChange` · `user.update` · `user.SetInGroup` · `user.RemoveFromGroup` | No dedicated branch listed |
| `USER_NEW_PASSWORD` | User update (setup dictionary) | `user.setPassword` | No dedicated branch listed |
| `USER_SENTBYMAIL` | Email sent (setup dictionary) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
