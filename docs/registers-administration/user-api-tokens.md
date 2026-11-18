# User API token inventory

The register belongs to a selected user with API access configured. The user-card tab depends on the API and the token-table option. Opening the page checks the selected user resource and restricts viewing to that user or an administrator. A nonadministrator needs self-write permission to manage their own token records. Reading and changing have separate eligibility.

| Decision | Register rule |
| --- | --- |
| Row identity | One `oauth_token.rowid` for the selected `fk_user` and the application's REST service. A similarly named user, a token for another person or a record for a different integration service does not belong to this list. |
| Entity | The row query offers an entity filter. In a multiple-entity installation it joins the entity directory to supply the entity name. The full pagination count is scoped to the selected user and service in the current entity and is computed without the display filters. |
| Dates | Creation filters use `datec`. Modification filters use `tms`. Each has optional independent inclusive from/to day boundaries. If both date pairs are present the record must satisfy both. Default sorting is by last modification descending. These dates do not measure actual API use. |
| Removal | Authorized confirmed removal handles distinct selected IDs within a transaction, with the selected user, REST service and current entity as the write scope. The user's other integrations have their own records. |

For example, one user has two records for the REST service and one for another service in the current entity. Filtering creation to the earlier period can display just one REST record while the unfiltered current-entity count remains two. Filtering on recent modification can find that older record if its metadata changed in the selected window.
