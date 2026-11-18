# Surveys

List access requires `opensurvey.read`. The register starts with `opensurvey_sondage` within the permitted survey entities and optionally joins the creator to `user.rowid`. A survey without a current creator record remains eligible. Each row represents one survey, irrespective of how many options, questions or responses exist. Default order is descending survey end time.

| Input | Predicate |
| --- | --- |
| `search_ref` | Keyword search on the survey's `id_sondage` reference. |
| `search_title` | Keyword search on `titre`. |
| `search_status` | Selected integer status or statuses. Empty or −1 omits the condition. The declared states are 0 draft, 1 validated/open and 2 closed. |
| `search_expired` | `expired` selects `date_fin < now`. `opened` selects `date_fin >= now`. Other values leave the end-time comparison off. A null end satisfies neither comparison. |
| `search_all` | The screen reads this input for display and single-result navigation. The built-in population query has no global text predicate. No general date range is applied to modification time. |

A survey explicitly closed before its scheduled end can appear under **opened** if only the time selector is set. Adding saved status 1 removes it. A validated survey exactly at the comparison instant still satisfies the **opened** time selector. Both filters operate on the same header and neither counts submissions.
