# Register periods, counted tender and closing differences

A cashier can explain a drawer shortage only if the opening float, money earned during the period and money counted at closing remain separate. The register control stores those facts for one terminal. It also publishes the turnover accumulated through the period end. A count closes a register period independently of bank statement reconciliation or journal transfer.

## Identifying the period

A control carries the issuing entity, register application, terminal number, year and optional month and day, closing time, opening cash, status, author and validator. An omitted month and day identifies a year. A month with no day identifies a month. All three parts identify a day. The closing instant is persisted as calendar components, including hour, minute and second. Creating the card normally defaults the closing time to 23:59:59. The card derives the start of an existing control from its closing date and period unit, then advances the lower bound by one second. The detailed print report independently derives calendar-day, month or year limits. A custom close time deserves particular attention when reconciling a card with its printed detail.

The card rejects external users. An internal operator needs a register execution right to view it, and the active register's execution right to start or close through this card. Starting requires the register application, terminal and a year. The opening amount must be supplied before the control can be created. Zero is a meaningful opening amount. The card uses the terminal's configured cash account to suggest it from the sum of bank operations dated before the period start. The operator can enter the actual float instead. Cheque and card have no opening float in this calculation.

Source locations: `htdocs/compta/cashcontrol/cashcontrol_card.php:103–200,218–277,529–571`, `htdocs/compta/cashcontrol/report.php:116–130`, `htdocs/compta/cashcontrol/class/cashcontrol.class.php:68–99,259–339`.

## Calculated and declared amounts

| Quantity | Calculation and meaning |
| --- | --- |
| Cash earned | Sum the signed customer-payment allocations that belong to the register source, terminal, entity and period and have the cash payment-mode code. Cash returned to a customer reduces the total. |
| Cheques or cards earned | Apply the same selection separately to the cheque and card codes. A payment under a different code can appear in detailed reporting under another category. It does not automatically enter one of these three stored totals. |
| Expected closing cash | Opening cash plus cash earned. Cash handed over in excess of a sale, then returned as change, contributes only the allocated sale amount to earned cash. |
| Expected closing cheques and cards | The period's respective earnings. The closing table adds an opening balance only to the cash column. |
| Declared balance | The amount the cashier actually counts or confirms for each of the three modes. A discrepancy remains visible after closing. |
| Lifetime turnover | The corresponding signed payments accumulated from the available history through the control's end date, filtered to that terminal and mode. A separate earliest-record date is looked up by entity and register application across terminals. |

The ordinary query selects by payment date and sums the allocation attached to each invoice. The audit-log calculation used in the designated French configuration takes the event creation date and event amount from the immutable customer-payment log. An accountant comparing the two bases needs both the date of payment and the date its posting event was recorded. A sale invoice dated Monday can contribute to Wednesday's control when its payment falls on Wednesday.

Source locations: `htdocs/compta/cashcontrol/cashcontrol_card.php:304–420,566–624,970–1011`, `htdocs/compta/cashcontrol/report.php:127–158,263–316`, `htdocs/takepos/invoice.php:422–449`.

## Closing, reopening and trading

Closing saves three calculated earnings, three declarations and the lifetime amounts, then sets the control to closed, records the validator and validation date, and emits the register-close event. The card wraps the update and closure in the same database transaction and rolls back when either operation reports failure. The control uses status 0 for draft and 1 for closed. The close routine treats an already closed record as already processed. The ordinary card offers reopening to a register operator where the audit configuration permits the button. Reopening returns the control to draft. A discrepancy displayed at close does not create a correcting bank entry.

Before the normal checkout handler accepts another transaction, it searches for a closed control for the current entity and terminal. It matches the current year and either the full year, the current month, or the specific current day. Finding a covering control blocks the action. Closing a month can therefore have a wider effect than closing a shift. Two terminals can trade in the same entity while one is closed. The persisted closing time on an individual count does not turn this checkout guard into an hourly guard.

Source locations: `htdocs/compta/cashcontrol/cashcontrol_card.php:218–226,299–430,1017–1048`, `htdocs/compta/cashcontrol/class/cashcontrol.class.php:233–235,419–476`, `htdocs/takepos/invoice.php:279–309`.

## Worked drawer close

Terminal 2 starts with 120.00 in the drawer. Customers settle 90.00 and 35.00 in cash and receive one cash refund of 12.00. A second customer settles 85.00 by card. The three signed cash allocations sum to 113.00. The expected cash is 233.00 and the expected card total is 85.00. The cashier counts 231.00 and confirms the full card batch. Closing retains the 113.00 cash turnover and the 231.00 declaration, displays the 2.00 cash difference, and closes the terminal for the period. The amount to investigate is 2.00. Posting another sale for 2.00 would increase expected cash and widen the discrepancy.
