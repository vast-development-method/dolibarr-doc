# Contract services and repeat field interventions

A contract describes an agreement with a customer. Its service lines describe what can be opened, allowed to expire or formally closed. An intervention records dated work against a customer, optionally a project and a contract. A reusable intervention template preserves a pattern of work for future visits. Each record has a different clock.

## Service activation, expiry and closure

| Service line state | Operational interpretation |
| --- | --- |
| Initial (0) | Agreed service still awaiting activation. Its planned start and end can already exist. |
| Open (4) with no planned end, or an end at or after the observation time | Active service. The header counts it among current open services. |
| Open (4) with a planned end strictly before the observation time | Expired service. It moves to the expired count when the clock passes its planned end, without a persisted transition or closing actor. |
| Closed (5) | Explicit shutdown with an actual end and closing actor. An operator may reopen the line. |

An operator with contract-activation authority opens an initial or closed service. Record the actual start, opening user, comment and optionally a replacement planned end. Clear the actual closure date on reopening. The bulk operation can explicitly preserve each existing planned end by passing the preserve-existing-date option. The close action has separate deactivation authority. It records actual end, closing user and comment on any service that is not already closed, including a service that never opened.

The contract stores an earliest planned end across open lines. Closing a line recalculates the minimum among the remaining open lines, ignoring null ends. Activation which changes the planned end also recalculates it. The bulk activation path that retains individual dates skips this recalculation in the line update. A reader computing an expiry roster directly from the open lines therefore has more information than a reader using the cached header date.

Bulk activation fetches the lines, skips any already open, uses a common actual opening time (now if omitted), and validates the header if still draft. Bulk closure skips closed lines, uses the operation time as the actual end on the others and also validates a draft header. Both operations group their changes in a transaction. Closing every service through this workflow can leave the agreement header validated. Returning a validated header to draft is a distinct header action with its own event.

An agreement has an open telephone-assistance line ending 30 September and an open on-site line ending 31 December. After 30 September, the first line counts as expired until staff close it. At that point the remaining dated open service has the December deadline. A third open service with no planned end counts as current and supplies no candidate date for the minimum.

## Time and value on the work record

An intervention starts in draft and accepts detail lines in that state. A detail has a description, actual activity date, duration in seconds, a line type and position. The line operation accepts extension values if supplied. Updating the work total sums durations of lines whose type is other than 9 and writes the earliest and latest activity dates on the header. With no qualifying entries, the total is zero and both dates are empty. The latest activity date is the maximum dated line. Adding its duration to determine a finish timestamp would change the meaning of this field.

The line reader exposes hours as duration divided by 3,600, rounded to two decimal places. The monetary estimate operation independently fetches the header creator’s hourly rate, multiplies the hours of each loaded line by that rate and normalizes the monetary total after summing. It has no per-technician rate lookup at this stage. Two 45-minute entries and one 30-minute entry at 60 currency units per hour produce 120. The rate-based estimate does not generate or settle an invoice.

## Saving a visit as a reusable template

The template creation card requires a title, customer and permission to create interventions. Setting a frequency requires a next execution date and a nonzero maximum generation count. The template data includes customer, entity, description, private and public notes, author, duration, print model, frequency and unit, next date, last-generation date and generation counters.

The create operation reads the original intervention and copies its duration, notes and print model. If the selected customer is the original customer it also copies the project and contract references from the original. When the customer changes, both references are cleared. That rule prevents a visit sold to one customer from silently retaining another customer’s agreement.

Template details are copied in order with descriptions, dates, seconds, positions and applicable commercial inputs. At template-line insertion, quantity defaults to one when empty and participates in the line price calculation. The stored row includes catalog reference, line type, discount, unit price, net amount, tax, gross amount and unit. Creating the template rolls back if a source line cannot be inserted. A template can therefore retain more commercial information than the subsequent manual work ticket uses.

## Generating a visit from the template

1. Resolve the template and fetch its detail. When it owns a customer, reuse that customer and the template’s project and contract. A template without a customer uses the customer chosen for the new visit.
2. Copy the entity, duration, description and public/private notes. Take custom header values supplied on the generation form. Create the new intervention with its own identity.
3. For each template line, add a work entry using the description and duration. Date it at generation time. This action passes no commercial price breakdown or line-specific custom values and does not carry the historical visit date into the new work ticket.
4. Increment the template’s completed generation count and set its last-generation timestamp. If the maximum is at or below the resulting count the template status is set to 1. Manually changing the next scheduled date is a separate operation. The manual generation handler neither advances that date nor calls intervention validation, irrespective of an auto-validation field in the model.

The manual action checks header creation but does not inspect each line insertion result or the counter update before redirecting to the new visit. A saved header or incremented count alone is insufficient evidence that every suggested line was reproduced. Deleting the template removes the template’s own details and header, while generated visits have their own identities.
