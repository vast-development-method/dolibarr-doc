# Credentials, entity and acting user

Authentication establishes whose rights, company scope and language apply to the request. Each business service subsequently makes its own operation and record-access decisions. A valid credential for an employee who can view invoices still leaves invoice settlement subject to that employee's payment rights.

## Issuing or rotating a user key

The optional credential exchange accepts a login, password, entity selector and reset choice. A blank entity selector means entity 1. A nonempty selector must be numeric. Login exchange must be enabled on the installation, and the configured authentication and user-validity decisions must admit the account. A failed credential check receives a forbidden response. Failure to load an accepted user or persist a new credential is reported as a service error.

For an existing key, a normal exchange returns the current key. For a first key or a requested rotation, the user must have permission to modify their own user record. Rotation writes a replacement to that record. Integrations using the previous user key then need the replacement for future requests. The successful response carries a result code, token, entity and message. No business record is created by this exchange.

See `htdocs/api/class/api_login.class.php:39–46`, `70–73` and `96–193`.

## Resolving a protected request

The access layer can resolve credentials stored on a user record or use the configured token table associated with users. Entity and group-membership rules affect candidate selection in multi-company configurations. Ambiguous credentials are an error. The token’s entity must match the working entity. A user record must still be enabled and within its account validity interval. Session invalidation is honored where a recorded session date applies.

Once resolved, the user’s rights are loaded. An ordinary internal user takes the user role, a user linked to a customer or supplier takes the external role and administrator status takes precedence. The dispatcher compares the resolved role against the service's allowed roles. Entity scope, a party association and operation-specific rights continue to apply at the business resource. Depending on configuration the access layer also updates usage counters. In token-table mode it records usage and last access against the selected credential.

See `htdocs/api/class/api_access.class.php:91–170`, `175–259`, `266–349` and `363–379`.

## Consequences for callers

| Situation | Result |
| --- | --- |
| An employee rotates the user key used by two integrations | The account has one replacement user key. Both integrations using the previous one require the replacement. |
| A credential exists but its user is outside the permitted validity period | Authentication fails before a business service is called. |
| An external caller is authenticated in the expected company | The resource can still restrict the visible records to the caller’s linked party and permitted business operations. |
| A sales employee can read a record but lacks the right for a financial transition | A successful read and a refused transition are compatible outcomes for one identity. |

The [service index](README.md) lists business resources separately from this shared credential lifecycle.
