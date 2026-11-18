# Members

The register starts from `adherent` and requires `fk_adherent_type = adherent_type.rowid`. Country, state and linked party are optional. A member with an unresolved type drops out, while one without a linked company can still appear. The access check uses the membership area, and the query limits member rows to the allowed membership entities. The result and its total count members. Individual subscription payments are absent from the base join.

| Input | Predicate |
| --- | --- |
| `search_type`, `search_status` | Positive type equals the joined type ID. Status accepts a list of member `statut` values. Legacy `statut` overrides the status input when supplied. |
| `search_filter` or legacy `filter` | `withoutsubscription` selects a null `datefin`. `waitingsubscription` additionally requires type `subscription = 1`. `uptodate` selects `datefin >= now` or a null end for a type with `subscription = 0`. `outofdate` selects a non-null end strictly before now. |
| `search_categ` or fallback `catid` | A positive selected ID must occur in `categorie_member` for the member. −2 requires absence of every category link. The built-in path reads a single selection into its category condition. |
| `search_id`, `search_ref`, `search_morphy`, `search_civility`, `search_firstname`, `search_lastname`, `search_gender`, `search_login` | Keyword matching on the corresponding member fields, using `rowid` for ID. An unspecified or −1 organisation/person selector is ignored. The ID input is parsed as an integer but passed to the text matcher. |
| `search_company`, `search_email`, `search_no_email` | Company searches linked party name or the member's saved company text. Email searches `email`. With mailing enabled, a positive no-email selection requires an opt-out record with this email. Zero requires a nonempty email with no opt-out record. |
| `search_address`, `search_zip`, `search_town`, `search_state`, `search_country`, `search_phone`, `search_phone_perso`, `search_phone_mobile`, `search_import_key` | Keyword tests on the address, postal code, town, state name, corresponding telephone or import key. Country is an ID-list filter on `adherent.country`. |
| `search_datec_start/end`, `search_datem_start/end` | Inclusive day-component bounds on creation `datec` and modification `tms` respectively. These bounds are independent of `datefin`. |
| `search_all` | Searches reference, login, surname, given name, saved company text, email, address, postal code, town, all three phones and public/private notes. The dedicated company search also reaches linked party name. |

If two members lack a subscription end and only one belongs to a subscription-paying type, both appear under **without subscription**, one under **waiting**, and the other under **up to date**. A member whose end equals the comparison instant still qualifies as up to date. A supplied party context alone does not add a party-ID predicate to this register.
