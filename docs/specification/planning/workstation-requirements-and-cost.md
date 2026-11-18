# Workstation staffing, equipment and production cost

A workstation describes a capability in the factory. A production plan can name that workstation against a timed operation. The station definition supplies staffing expectations and an hourly estimate. Separate transactions record consumption, finished production or a dated event involving the station.

## Configuring the station

A station has a business reference, label, entity, current status, type, required operator count, estimated operator hourly rate and estimated machine hourly rate. The type distinguishes human, machine and mixed operation. The station can reference multiple user groups and multiple resources. A selected group designates a team associated with the station. The resource association identifies a piece of equipment or other resource associated with it. Each link has the station ID and related group or resource ID. These sets contain no dates, shifts, named operator attendance or quantity of available slots.

On create, submitted group and resource identifiers are normalized and deduplicated. The operation first creates the station, then records its links. A failed creation of a required association rolls the creation back. An update with an array of group or resource identifiers replaces the corresponding set, so an explicitly empty array clears it. A non-array leaves that set alone on this path. In the update routine, the deletion and recreation of child links occurs before the common station update and the loop does not propagate individual relation-insert results. Reading the stored associations is how to determine the effective team and equipment set after a partial failure.

A product can name the station as its default. A recipe line can select it for that operation and a manufacturing plan copies the leaf recipe line's selected station. A manually added service operation takes the service product's default station. A service with a duration unit can provide the initial time quantity and unit. These links allow two different recipes for the same commercial product to use different equipment and cost assumptions.

The station record and relation updates are in `htdocs/workstation/class/workstation.class.php`. The relation tables are `htdocs/install/mysql/tables/llx_workstation_workstation_usergroup-workstation.sql` and `htdocs/install/mysql/tables/llx_workstation_workstation_resource-workstation.sql`. Plan derivation is in `htdocs/mrp/class/mo.class.php` and `htdocs/mrp/mo_production.php`.

## Estimating a timed operation

For a service recipe line, convert its quantity to hours using the line unit's seconds per unit. When a workstation is active and selected, multiply those hours by **operator hourly estimate plus machine hourly estimate**. The required operator count is descriptive in this calculation. It does not multiply the operator rate. With no workstation, a service with a known standard duration uses `line hours ÷ service duration in hours × service unit cost`. With no usable standard duration the fallback uses quantity times its unit cost.

A station requires two operators, has an operator estimate of 45 per hour and a machine estimate of 15 per hour. A ninety-minute service line contributes `1.5 × (45 + 15) = 90` to the recipe cost. Replacing its station with one costing 65 plus 15 raises the same operation to 120. Neither amount depends on which individual logs the job. A service priced at 200 per four hours without a selected station would contribute 75 for the same 90 minutes.

Recipe cost sums the service and material line amounts. For a recipe with a positive base output quantity, unit cost divides the rounded recipe total by that output. For example, the original 90 station cost and 210 of other component cost for a batch of six give an estimated cost of 50 per output unit. The manufacturing order also builds an estimate from its own planned consumption lines, including manually added operations. For a timed input with a station it divides the calculated station amount by the order quantity for its per-output contribution. A supplier price, average material cost, product cost and hourly workstation estimate can therefore enter a calculation at different stages. A change to the estimate is distinct from the actual unit value carried by an output stock receipt.

Recipe and manufacturing-order calculations are in `htdocs/bom/class/bom.class.php` under `calculateCosts` and in `htdocs/mrp/mo_production.php`.

## Capacity and calendars

A manufacturing order carries optional planned start and finish timestamps. The order's plan records product, role, quantity, unit, station and other production attributes per line. Posted actuals refer back to the plan line and record the operator who entered the posting. These facts can answer which station was intended for a 90-minute operation and which user reported its completion. They do not identify two specific operators expected to work from 08:00 to 09:30 or record that either person attended for that period.

The station agenda lists its related calendar activities and provides an event creation action to users with appropriate agenda rights. Creating a manufacturing plan with a default station does not, in that plan-creation transaction, create a calendar reservation, assign a shift, compare concurrent station load to the required operator count or move other manufacturing orders' dates. Two orders can consequently have overlapping planned dates and refer to the same station. Whether a dated calendar allocation blocks another use of its equipment depends on the relevant busy resource links.

The header dates are defined by `htdocs/mrp/class/mo.class.php`. Production line fields are in `htdocs/install/mysql/tables/llx_mrp_production-mrp.sql`. Calendar activity and associated permissions are in `htdocs/workstation/workstation_agenda.php`.
