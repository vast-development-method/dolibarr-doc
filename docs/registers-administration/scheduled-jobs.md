# Scheduled jobs

One row represents a definition in `cronjob`. Running a task repeatedly updates the definition's execution fields. Ten runs of the same job still contribute one row. The base selection reads the job directly, with no required join to its author, module or prior execution history.

| Decision | Register rule |
| --- | --- |
| Permission | Reading requires the scheduled-job read grant. The create and execute permissions combine the scheduled-job write grant with administrator status. Deletion has its own grant. |
| Entity and availability | Show global definitions (`entity = 0`) and definitions belonging to the current entity. Evaluate each definition's availability condition in `test` and exclude rows whose condition is false. Passing that condition and being enabled are independent. |
| Enabled status | A supplied status in the supported zero/one range selects disabled/enabled definitions through `status`. Leaving it unspecified admits both. |
| Execution state and outcome | A supplied processing filter compares the integer `processing` flag, including zero. A supplied last-result filter uses a numeric comparison on `lastresult`. One tests whether the job is marked in progress, the other tests the most recently recorded result. |
| Label and owner module | The label filter searches within `label`. The module filter performs a text search on `module_name`. A disabled job can match either. |
| Timing and sort | The default is priority ascending, then enabled status descending. Last launch `datelastrun`, last result time `datelastresult` and next run `datenextrun` describe different moments. These displayed times are not built-in date-range selectors. When a result time exists and is at or after the recorded launch, duration is at least one second. |

For example, an enabled global reminder whose condition passes and a disabled local report whose condition passes both appear without a status filter. A third local task whose required module is unavailable is excluded even if enabled. Selecting enabled and idle keeps the reminder only if its processing flag is zero. A previous successful return code does not imply that the definition is idle now.
