# Resources

A row represents one resource master in the permitted resource entities. Reading requires `resource.read`. The list can resolve its type through `resource.fk_code_type_resource = c_type_resource.code`, its state through `fk_state` and country through `fk_country`. These are left joins. A missing type label need not exclude a resource until the user filters on that label. Defined additional fields can be joined through the resource row ID. The default order is ascending resource reference.

| Input | Predicate |
| --- | --- |
| `search_all` | Keyword search over resource `ref` and `description`. It does not include the type or location. |
| `search_ref`, `search_type` | Keyword search on resource reference and on the joined type's **label**, respectively. |
| `search_address`, `search_zip`, `search_town`, `search_state` | Keyword search on the corresponding resource address fields or on the state dictionary's name. |
| `search_country` | Selected IDs match the stored `fk_country`. Blank and −1 leave the country unrestricted. |
| `search_phone`, `search_email`, `search_url` | Keyword search on the respective stored contact or address field. |
| `search_max_users` | Numeric comparison on the resource's declared `max_users`. A literal zero alone does not activate the truth-tested input. A comparison expression can select zero. |

A room whose reference is R1 and whose description is “upstairs meeting room” can be found by a global “upstairs” search. A type-label search for “meeting” requires a matching type label even if its description contains that word. If its maximum is 20, a numeric capacity filter of at least 12 admits the room regardless of existing bookings. The register has no reservation join, date-availability predicate, free-slot computation or occupancy subtraction.
