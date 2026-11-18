# Mileage allowances and claim ceilings

A claim detail identifies the employee through its parent report. Its own data includes the expense date, fee type, quantity, tax-inclusive unit price, VAT rate and optional source code, vehicle category, project, description and associated file. Net, VAT, local taxes and gross are stored line results. This permits an approver to see the amount retained after the mileage and ceiling policies ran.

## Creating a detail

The ordinary add-line path accepts a draft or refused report. The web form requires an expense date and a nonzero unit price, validates VAT input, and enforces project and file requirements where enabled. A line outside the report period produces a warning or blocks creation according to configuration. The underlying calculation uses a tax-inclusive price basis. It obtains the domestic tax context from the organisation because the merchant and buyer are not identified individually on this operation.

After the original amounts are calculated, the writer applies a mileage offset when configured, then evaluates expense rules, then writes the detail and updates the parent totals. A restrictive rule can alter a detail before insertion. The detail stores the resulting warning messages as well as the amount. A missing applicable mileage range causes the offset routine to return without changing the line. The add-line caller continues to the rule and insertion stages.

Implementation evidence appears in `htdocs/expensereport/card.php:1229–1286`, `htdocs/expensereport/class/expensereport.class.php:1975–2077`, `htdocs/expensereport/class/expensereportline.class.php:321–402`.

## Vehicle scale and fixed allowance

The scale has vehicle categories and ordered distance thresholds. A rate entry carries a coefficient and a fixed offset. Two selections serve different purposes.

| Decision | Selection and result |
| --- | --- |
| Suggested unit rate | The mileage calculator orders the category's thresholds by distance. A quantity strictly above one threshold and strictly below the next receives the lower threshold's coefficient. Above the highest threshold it receives the final coefficient. At an exact threshold neither open interval matches and the initial coefficient remains zero. |
| Employee's offset band | The writer obtains active ranges for the category and takes the employee's configured default position, counting from one in ascending threshold order. A missing or out-of-range position yields no offset. |
| Periodic allowance | The normal offset is one twelfth of the scale's fixed amount. With the whole-offset setting applied, it uses the full amount. Both paths use the employee/month lookup for a pre-existing mileage detail. |

The optional current-year coefficient selection increases the input quantity by the **number of mileage detail rows with a non-null quantity** belonging to that employee's validated reports in the calendar year of execution. The implementation counts rows. For two such details of 100 and 75 kilometres, this adds 2 to the proposed distance. It also uses the current year even if the report is being entered for a different year. This distinction matters near a threshold. The suggestion returns the coefficient for one unit, while the claim line multiplies by its quantity.

For the first eligible monthly detail, adjusted unit price equals **coefficient + periodic offset ÷ quantity**. With coefficient 0.60 per kilometre, annual fixed amount 120.00, normal monthly distribution, 50 kilometres and zero tax, the adjusted unit price is 0.80 and gross is 40.00. Another 50 kilometres in the same month at a supplied 0.60 has gross 30.00 without a second offset. The prior-line lookup searches by employee, year, month and mileage fee code. It excludes the current detail on edit and has no report-status or vehicle-category filter. Changing vehicles does not by itself renew the month's fixed allowance.

Implementation evidence appears in `htdocs/expensereport/class/expensereport_ik.class.php:195–246`, `htdocs/expensereport/class/expensereport.class.php:2163–2247,2764–2857`.

## Allowance-rule selection

A rule supplies its amount ceiling, period, fee type, effective start and end dates, applicable user/group/everyone scope, and restrictive flag. The selector includes rules visible to the entity, accepts the selected fee type or a wildcard, and uses inclusive effective dates. A rule may match the employee directly, through group membership, or through the all-employees setting. Matching rules are ordered by the all-users flag, group key and user key. More than one rule can act on the same detail.

A per-expense rule evaluates the line's gross. Daily, monthly and annual rules aggregate stored gross amounts for the employee and rule fee type over the appropriate date interval. While editing an existing detail, its own row is excluded and the proposed amount participates once. The aggregate query has no parent status condition. Other draft claims can therefore consume headroom. Rule selection accepts a wildcard fee type, but the period aggregation uses equality to the rule's stored fee type. An all-types periodic rule cannot be assumed to sum every fee category.

For each rule, the calculation substitutes the line value retained after earlier restrictions. Equality with the ceiling is allowed. An advisory breach records a message. A restrictive breach subtracts the excess from the current line. For a daily ceiling of 100, existing eligible gross of 70 and a proposed line gross of 45, the new detail contributes 30 and the day's total becomes 100. If the previous eligible total already exceeds the ceiling, the subtraction can produce a negative retained gross. The rule loop has no zero-floor operation. On a breach, the writer derives a revised inclusive unit amount from retained gross and quantity and recalculates the tax components. Keep the original expense evidence separately if the organisation must retain what the employee initially submitted.

Implementation evidence appears in `htdocs/expensereport/class/expensereport_rule.class.php:204–243`, `htdocs/expensereport/class/expensereportline.class.php:419–450`, `htdocs/expensereport/class/expensereport.class.php:2082–2150`.
