# Service status

The authenticated status response wraps the service status, current release and login-lock setting in a success object. In a non-production environment it also exposes environment and time metadata.

The implementation locations below refer to `htdocs/api/class/api_status.class.php`.

## `index` — List records

**Result** A success envelope with release and access-lock information. Non-production adds environment and clock fields.

Source lines `49–69`.
