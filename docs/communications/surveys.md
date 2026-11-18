# Publishing a poll and recording votes

An OpenSurvey poll has an internal ID, public survey key, entity, title, creator, ordered choices, closing date, state and options for visibility, comments and notifying the organiser. A vote links the survey key and participant name to a positional response vector. A comment belongs to the same survey and retains its author and creation date. This chapter follows the standard public poll path in 24.0.3. [Poll fields](../reference/locators/communications.md#ref-bc812e16d23d) · [Vote storage](../reference/locators/communications.md#ref-55ebb3a0c95a)

| Operation | Actor and preconditions | Observable result |
| --- | --- | --- |
| Validate, close or reopen | OpenSurvey readers can view the administration card. Writers control these changes. | Validate and reopen both set validated (1). Close sets closed (2). Draft is 0. The public survey index selects validated surveys. |
| Cast a ballot | Public poll enabled, voting period open, nonempty voter name. | Read one answer for every ordered choice. In the yes/no/blank presentation, 1 means yes, 0 means no and 2 is undecided/blank. If a choice field is omitted the input loop sets 0. The server checks for an existing name on that survey and rejects duplicates. |
| Comment | Comments enabled, date/state gate allows modifications, and the public session has already voted using that participant name. | Save the comment against the survey. Expired or closed polls reject comment submissions. |
| View results | Visibility rule allows viewing the other participants' answers. | The page can show individual answers and aggregate them by choice. When other participants' votes are hidden, the result display uses the current session's participant identities. |

[Lifecycle and permissions](../reference/locators/communications.md#ref-5e03bf756c99) · [Public listing](../reference/locators/communications.md#ref-af94b1f96276) · [Submission and comments](../reference/locators/communications.md#ref-e653c15d984c) · [Result display](../reference/locators/communications.md#ref-8a8797ad249c) · [Totals](../reference/locators/communications.md#ref-bff8564ea1d5)

**Worked ballot.** If the choices are Monday, Tuesday and Wednesday, an input vector of `[1,0,2]` means yes, no and undecided in that order. It adds one affirmative response to Monday. A second vote under the same name and survey must fail before another row is inserted. Another survey has an independent set of voter names. Closing the poll prevents a fresh ballot even before the specified closing date. If its closing day has already elapsed, reopening the state alone does not extend voting.

**Acceptance boundary.** The public listing and the voting deadline are distinct checks. The participation screen computes its modification window using the end of the closing day and closed state. The [ballot schema](../../schemas/communications/poll-ballot.schema.json) preserves answer order and the three possible values. The application must additionally compare vector length with the current poll's choice count and check voter uniqueness at submission time. [Valid ballot](../../examples/communications/poll-ballot--weekdays.json)
