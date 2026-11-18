# People, membership and support events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. A numbered agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch rules and source keys.

| Event | Setup meaning or origin | Direct emission site | Specific subscriber branches |
| --- | --- | --- | --- |
| `CONFERENCEORBOOTHATTENDEE_VALIDATE` | Named operation signal | `eventorganization/class/conferenceorboothattendee.class.php:627 (validate)` | No dedicated branch listed |
| `CONFERENCEORBOOTH_VALIDATE` | Named operation signal | `eventorganization/class/conferenceorbooth.class.php:470 (validate)` | No dedicated branch listed |
| `EXPENSE_REPORT_APPROVE` | Expense report approved (dictionary row at line 144) | `expensereport/class/expensereport.class.php:1540 (setApproved)` | Notification 168 |
| `EXPENSE_REPORT_CANCEL` | Named operation signal | `expensereport/class/expensereport.class.php:1722 (set_cancel)` | No dedicated branch listed |
| `EXPENSE_REPORT_CREATE` | Expense report created (dictionary row at line 141) | `expensereport/class/expensereport.class.php:507 (create)` | No dedicated branch listed |
| `EXPENSE_REPORT_DELETE` | Expense report deleted (dictionary row at line 146) | `expensereport/class/expensereport.class.php:1248 (delete)` | No dedicated branch listed |
| `EXPENSE_REPORT_DENY` | Named operation signal | `expensereport/class/expensereport.class.php:1598 (setDeny)` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_CREATE` | Named operation signal | `expensereport/class/expensereportline.class.php:379 (insert)` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_DELETE` | Named operation signal | `expensereport/class/expensereport.class.php:2408 (deleteLine)` | No dedicated branch listed |
| `EXPENSE_REPORT_DET_MODIFY` | Named operation signal | `expensereport/class/expensereportline.class.php:533 (update)` | No dedicated branch listed |
| `EXPENSE_REPORT_MODIFY` | Expense report modified (dictionary row at line 143) | `expensereport/class/expensereport.class.php:665 (update)` | No dedicated branch listed |
| `EXPENSE_REPORT_PAID` | Expense report billed (dictionary row at line 145) | `expensereport/class/expensereport.class.php:838 (setPaid)` | No dedicated branch listed |
| `EXPENSE_REPORT_UNPAID` | Named operation signal | `expensereport/class/expensereport.class.php:1666 (setUnpaid)` | No dedicated branch listed |
| `EXPENSE_REPORT_VALIDATE` | Expense report validated (dictionary row at line 142) | `expensereport/class/expensereport.class.php:1400 (setValidate)` | Notification 167 |
| `HOLIDAY_APPROVE` | Holiday approved (dictionary row at line 206) | `holiday/class/holiday.class.php:1015 (approve)` | Notification 170 |
| `HOLIDAY_CANCEL` | Holiday canceled (dictionary row at line 207) | `holiday/class/api_holidays.class.php:596 (cancel)` | No dedicated branch listed |
| `HOLIDAY_CREATE` | Holiday created (dictionary row at line 203) | `holiday/class/holiday.class.php:387 (create)` | No dedicated branch listed |
| `HOLIDAY_DELETE` | Holiday deleted (dictionary row at line 208) | `holiday/class/holiday.class.php:1225 (delete)` | No dedicated branch listed |
| `HOLIDAY_MODIFY` | Holiday modified (dictionary row at line 204) | `holiday/class/holiday.class.php:1167 (update)` | No dedicated branch listed |
| `HOLIDAY_VALIDATE` | Holiday validated (dictionary row at line 205) | `holiday/class/holiday.class.php:835 (validate)` | Notification 169 |
| `HRM_EVALUATION_CREATE` | HR Evaluation created (dictionary row at line 211) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_DELETE` | HR Evaluation deleted (dictionary row at line 215) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_MODIFY` | HR Evaluation modified (dictionary row at line 212) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_UNVALIDATE` | HR Evaluation back to draft (dictionary row at line 214) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `HRM_EVALUATION_VALIDATE` | HR Evaluation validated (dictionary row at line 213) | `hrm/class/evaluation.class.php:572 (validate)` | No dedicated branch listed |
| `HRM_JOB_VALIDATE` | Named operation signal | `hrm/class/job.class.php:510 (validate)` | No dedicated branch listed |
| `HRM_POSITION_VALIDATE` | Named operation signal | `hrm/class/position.class.php:567 (validate)` | No dedicated branch listed |
| `HRM_SKILLDET_VALIDATE` | Named operation signal | `hrm/class/skilldet.class.php:534 (validate)` | No dedicated branch listed |
| `HRM_SKILLRANK_VALIDATE` | Named operation signal | `hrm/class/skillrank.class.php:548 (validate)` | No dedicated branch listed |
| `HRM_SKILL_VALIDATE` | Named operation signal | `hrm/class/skill.class.php:629 (validate)` | No dedicated branch listed |
| `KNOWLEDGERECORD_CANCEL` | Knowledgerecord cancel (dictionary row at line 234) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_CREATE` | Knowledgerecord created (dictionary row at line 229) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_DELETE` | Knowledgerecord deleted (dictionary row at line 236) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_MODIFY` | Knowledgerecord modified (dictionary row at line 230) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_REOPEN` | Knowledgerecord reopen (dictionary row at line 232) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_SENTBYMAIL` | Mails sent from knowledgerecord file (dictionary row at line 235) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_UNVALIDATE` | Knowledgerecord unvalidated (dictionary row at line 233) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `KNOWLEDGERECORD_VALIDATE` | Knowledgerecord Evaluation validated (dictionary row at line 231) | `knowledgemanagement/class/knowledgerecord.class.php:633 (validate)` | No dedicated branch listed |
| `MEMBER_CREATE` | Named operation signal | `adherents/class/adherent.class.php:754 (create)` | No dedicated branch listed |
| `MEMBER_DELETE` | Member deleted (dictionary row at line 120) | `adherents/class/adherent.class.php:1155 (delete)` | Agenda 1223 |
| `MEMBER_EXCLUDE` | Member excluded (dictionary row at line 119) | `adherents/class/adherent.class.php:2416 (exclude)` | Agenda 1242 |
| `MEMBER_MODIFY` | Member modified (dictionary row at line 113) | `adherents/class/adherent.class.php:1044 (update)` · `adherents/class/adherent.class.php:1380 (mergeMembers)` | Agenda 1087 |
| `MEMBER_NEW_PASSWORD` | Named operation signal | `adherents/class/adherent.class.php:1505 (setPassword)` | No dedicated branch listed |
| `MEMBER_RESILIATE` | Member resiliated (dictionary row at line 118) | `adherents/class/adherent.class.php:2367 (resiliate)` | Agenda 1204 |
| `MEMBER_SENTBYMAIL` | Mails sent from member card (dictionary row at line 114) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `MEMBER_SUBSCRIPTION_CREATE` | Member subscribtion recorded (dictionary row at line 115) | `adherents/class/subscription.class.php:263 (create)` | Agenda 1106 |
| `MEMBER_SUBSCRIPTION_DELETE` | Member subscribtion deleted (dictionary row at line 117) | `adherents/class/subscription.class.php:416 (delete)` | Agenda 1171 |
| `MEMBER_SUBSCRIPTION_MODIFY` | Member subscribtion modified (dictionary row at line 116) | `adherents/class/subscription.class.php:371 (update)` | Agenda 1139 |
| `MEMBER_TYPE_CREATE` | Named operation signal | `adherents/class/adherent_type.class.php:467 (create)` | No dedicated branch listed |
| `MEMBER_TYPE_DELETE` | Named operation signal | `adherents/class/adherent_type.class.php:596 (delete)` | No dedicated branch listed |
| `MEMBER_TYPE_DEL_MULTILANGS` | Named operation signal | `adherents/class/adherent_type.class.php:410 (delMultiLangs)` | No dedicated branch listed |
| `MEMBER_TYPE_MODIFY` | Named operation signal | `adherents/class/adherent_type.class.php:546 (update)` | No dedicated branch listed |
| `MEMBER_TYPE_SET_MULTILANGS` | Named operation signal | `adherents/class/adherent_type.class.php:381 (setMultiLangs)` | No dedicated branch listed |
| `MEMBER_VALIDATE` | Member validated (dictionary row at line 112) | `adherents/class/adherent.class.php:2315 (validate)` | Agenda 1067 |
| `PARTNERSHIP_ACCEPT` | Named operation signal | `partnership/class/partnership.class.php:824 (approve)` | No dedicated branch listed |
| `PARTNERSHIP_CREATE` | Partnership created (dictionary row at line 223) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_DELETE` | Partnership deleted (dictionary row at line 226) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_MODIFY` | Partnership modified (dictionary row at line 224) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_SENTBYMAIL` | Mails sent from partnership file (dictionary row at line 225) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `PARTNERSHIP_VALIDATE` | Named operation signal | `partnership/class/partnership.class.php:698 (validate)` | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_CREATE` | Candidature created (dictionary row at line 190) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_DELETE` | Candidature deleted (dictionary row at line 193) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_MODIFY` | Candidature modified (dictionary row at line 191) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_SENTBYMAIL` | Mails sent from candidature record (dictionary row at line 192) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTCANDIDATURE_VALIDATE` | Named operation signal | `recruitment/class/recruitmentcandidature.class.php:577 (validate)` | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_CREATE` | Job created (dictionary row at line 186) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_DELETE` | Job deleted (dictionary row at line 189) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_MODIFY` | Job modified (dictionary row at line 187) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_SENTBYMAIL` | Mails sent from job record (dictionary row at line 188) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `RECRUITMENTJOBPOSITION_VALIDATE` | Named operation signal | `recruitment/class/recruitmentjobposition.class.php:584 (validate)` | No dedicated branch listed |
| `TICKET_ASSIGNED` | Ticket assigned (dictionary row at line 157) | `ticket/class/ticket.class.php:1887 (assignUser)` | Agenda 1420 |
| `TICKET_CLOSE` | Ticket closed (dictionary row at line 158) | `ticket/class/ticket.class.php:2164 (close)` | No dedicated branch listed |
| `TICKET_CREATE` | Ticket created (dictionary row at line 155) | `ticket/class/ticket.class.php:625 (create)` | Workflow 624 |
| `TICKET_DELETE` | Ticket deleted (dictionary row at line 160) | `ticket/class/ticket.class.php:1177 (delete)` | No dedicated branch listed |
| `TICKET_MODIFY` | Ticket modified (dictionary row at line 156) | `ticket/class/ticket.class.php:1141 (update)` · `ticket/class/ticket.class.php:1761 (markAsRead)` · `ticket/class/ticket.class.php:1832 (setReadDate)` | No dedicated branch listed |
| `TICKET_SENTBYMAIL` | Ticket message sent by email (dictionary row at line 159) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
| `USERGROUP_MODIFY` | Named operation signal | `user/class/usergroup.class.php:445 (addrights)` · `user/class/usergroup.class.php:575 (delrights)` | No dedicated branch listed |
| `USER_CREATE` | User created (dictionary row at line 163) | `user/class/user.class.php:2004 (create)` · `user/class/user.class.php:2089 (create_from_contact)` | No dedicated branch listed |
| `USER_DELETE` | User update (dictionary row at line 165) | `user/class/user.class.php:1869 (delete)` | No dedicated branch listed |
| `USER_ENABLEDISABLE` | User update (dictionary row at line 167) | `user/class/user.class.php:1685 (setstatus)` | No dedicated branch listed |
| `USER_MODIFY` | User update (dictionary row at line 164) | `user/class/user.class.php:1221 (addrights)` · `user/class/user.class.php:1344 (delrights)` · `user/class/user.class.php:1733 (setForcePasswordChange)` · `user/class/user.class.php:2605 (update)` · `user/class/user.class.php:3055 (SetInGroup)` · `user/class/user.class.php:3110 (RemoveFromGroup)` | No dedicated branch listed |
| `USER_NEW_PASSWORD` | User update (dictionary row at line 166) | `user/class/user.class.php:2787 (setPassword)` | No dedicated branch listed |
| `USER_SENTBYMAIL` | Email sent (dictionary row at line 162) | Resolved by operation-specific or shared dispatch; literal call site unassigned. | No dedicated branch listed |
