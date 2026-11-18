# Manufacturing workstations

This read service exposes a single workstation by identifier or reference and a list of workstations. A production order's output and consumed materials are posted through the manufacturing service.

The implementation locations below refer to `htdocs/workstation/class/api_workstations.class.php`.

## `get` — Read a workstation

Route `GET {id}`.

**Arguments** `id`.

**Access** The decision uses right `workstation.workstation.read`, workstation record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id or ref.
- `401` — record outside the caller’s scope.
- `403` — access or input restriction.
- `404` — workstation missing.

Source lines `71–74` with `_fetch 311–333`.

## `getByRef` — Read by business reference

Route `GET ref/{ref}`.

**Arguments** `ref`.

**Access** The decision uses right `workstation.workstation.read`, workstation record scope.

**Result** A record with internal service properties removed.

- `400` — bad value for parameter id or ref.
- `401` — record outside the caller’s scope.
- `403` — access or input restriction.
- `404` — workstation missing.

Source lines `91–94` with `_fetch 311–333`.

## `index` — List records

**Arguments** `sortfield = "t.ref"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses right `workstation.workstation.read`.

The properties selector projects the returned fields.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — invalid filter expression.
- `403` — access or input restriction.
- `503` — query or persistence failure.

Source lines `111–183`.
