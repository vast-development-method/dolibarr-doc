# Scheduled work, overlapping attempts and recovery

A scheduled job row combines its definition with the **most recent attempt**. Start timestamp, completion timestamp, result, text output, process identity, processing indicator and run count describe execution. A business handler may have its own durable output, such as generated invoice identities. The job row alone cannot enumerate all objects created in a successful or interrupted attempt.

## Ownership of a run

The ordinary command runner fetches enabled, nonprocessing rows ordered by entity, priority and row identity. The URL runner orders by priority, entity and row identity. Each evaluates qualification and may select multiple jobs. An activation test, due time and optional start and end bounds control eligibility. The scheduled time must be earlier than the poll time, whereas start and end are inclusive. The selected login and the current job entity establish the execution context.

After selection, the job is fetched and the run operation independently updates its row. It sets the start time, clears the prior completion and output, sets the processing marker and process identity where available, and increments the observed run count. It commits this start marker before invoking the handler. The update uses the row identity. It does not atomically claim a row only if it is still idle. Two overlapping pollers that both selected the same idle job can reach this update. The processing indicator is valuable for excluding jobs already seen as running but does not guarantee a single execution for every due time. The business meaning of duplicates consequently depends on the handler's own keys or previously recorded work.

A failed login lookup occurs before the start marker. A failure after the committed marker can leave evidence of an attempt even if the handler made no persistent business changes. Conversely, a handler can commit business records and then fail before recording a successful end. At normal completion the job stores the handler's result, capped output and completion time, clears its process marker and restores the earlier entity context. The next attempt overwrites these latest-result fields. Where configured, a failing attempt sends an alert separately.

Source locations include `scripts/cron/cron_run_jobs.php:234–338`, `htdocs/public/cron/cron_run_jobs_by_url.php:188–211` and `htdocs/cron/class/cronjob.class.php:update, run_jobs`.

## Three different interruption outcomes

| Evidence when interrupted | Recovery behavior |
| --- | --- |
| Runtime reaches its shutdown handler | If the job still has the running marker, no recorded completion and no conflicting stored process identity, the handler records an abnormal finish and clears processing. It can include the runtime's last error in the output. Completed attempts are left alone. |
| A later runner identifies a stored process that no longer exists | On a host supporting the process probe, a missing process leads to a guarded row update matching identity, original process ID, running marker and absent completion. It sets result to failure, stores the stale-process explanation and clears the process identity and marker. An inconclusive probe is a different outcome. |
| An unfinished start is older than the configured maximum age | The runner clears its processing flag at or beyond the age threshold, 24 hours by default. This age-based update does not assign a completion time or prove the original process exited. Overlong work can consequently become eligible for a subsequent poll. |

These operations concern scheduler bookkeeping. None reverses a third-party message or invalidates a previously committed invoice. A missing completion with a known generated document and a missing completion with no generated document are therefore different business recovery cases.

Source locations include `scripts/cron/cron_run_jobs.php:190–233` and `htdocs/cron/class/cronjob.class.php:1344–1396`.

## Retry calendar and end conditions

The scheduler attempts to calculate the next time after either ordinary success or ordinary failure. A failed execution normally advances the same recurrence as a successful one. There is no independent escalating backoff or automatic replay of every missed slot in this path. When the previous due time exists, positive recurrence advances it until it reaches or passes the poll time. When it is absent, the first scheduled time derives from the configured start or current scheduling time. Whole-day and whole-week schedules preserve the server's local calendar convention, while monthly recurrence uses calendar months.

For a job due at 08:00 with an hourly interval and the next ordinary poll at 11:20, a single due execution can advance the schedule through 09:00, 10:00 and 11:00 to noon. Its next scheduled time is noon even if the 11:20 handler failed normally. If the runner terminates between the stored result and the separate rescheduling update, the previous due time may remain eligible at the next poll. The handler's completed business output then matters more than the scheduler's planned time when deciding if business work was repeated.

A configured archive-on-completion policy marks the definition archived once the number of starts reaches a positive maximum or its next scheduled time would lie **after** the configured end. A failed attempt counts toward a maximum number of runs. With a limit of three and two earlier starts, one failed third invocation can archive the schedule while its business objective remains incomplete.

Source locations include `scripts/cron/cron_run_jobs.php:338–365` and `htdocs/cron/class/cronjob.class.php:reprogram_jobs, addFrequency`.
