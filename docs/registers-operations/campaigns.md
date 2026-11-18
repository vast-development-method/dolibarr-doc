# Email campaigns

The campaign register requires the mailing read grant. External users also require the external-user authorisation setting. The base selection requires `mailing.entity` equal to the current entity. Creation and sending times are displayed, but the built-in list query has no creation or send-date range. Its default ordering is descending creation time.

| Input | Predicate and effect on the result |
| --- | --- |
| No `filteremail` | One header row per campaign, with an optional project obtained through `mailing.fk_project`. The selected `nbemail` is the stored campaign count. |
| `filteremail` | Requires a target in `mailing_cibles` whose `fk_mailing` is the campaign and whose email equals the supplied address. Adds the target's `statut` alongside the campaign's status. The unit becomes a matching target row. The branch mixes a comma join with a project outer join that refers to the campaign alias. Engines that restrict names in that join's scope can reject the statement before returning target rows. |
| `search_ref` or fallback `sref` | Numeric comparison against the campaign's internal `rowid`. |
| `search_title`, `search_subject` | Substring patterns on `titre` and `sujet`. |
| `search_messtype` | Without an email filter, match within the message type. With an email filter, compare with the supplied pattern without automatically adding leading or trailing wildcards. |
| `projectid`, `search_refproject`, `search_project` | Exact project ID, keyword match on project reference, keyword match on project title. Selecting a project field eliminates an unlinked campaign. |
| `search_all` | Requires a match in campaign title, subject or body **and** a second keyword search against the title alone. With a single plain term, matching the body alone cannot qualify the row. |

For example, a campaign titled **Annual invitation** with the subject **Membership renewal** appears under a subject search for “renewal”. A global search for “renewal” excludes it because its title lacks that term. A sent campaign can also show a failed individual target: the two displayed statuses describe different records. Counting campaign headers cannot by itself reconcile deliveries.
