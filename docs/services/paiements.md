# Customer payment records

A payment is an allocation-bearing financial record. Looking up or amending the payment itself is distinct from settling a specific invoice or creating a receipt across several invoices.

The implementation locations below refer to `htdocs/compta/facture/class/api_paiements.class.php`.

## `get` — Read a customer payment

**Arguments** `id`.

**Access** The decision uses right `facture.lire`, linked-record access decision.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — paiement missing.
- `503` — query or persistence failure.

Source lines `75–90` with `_checkAccessToPaymentForExternalUser 280–300`.

## `index` — List records

**Arguments** `sortfield = "t.rowid"`, `sortorder = 'ASC'`, `limit = 100`, `page = 0`, `sqlfilters = ''`, `properties = ''`.

**Access** The decision uses right `facture.lire`.

The properties selector projects the returned fields.

**Result** A collection of matching records.

- `400` — invalid filter expression.
- `403` — access refused.
- `503` — query or persistence failure.

Source lines `112–171`.

## `put` — Update a customer payment

**Arguments** `id`, `request_data = null`.

**Access** The decision uses right `facture.creer`, linked-record access decision, right `facture.lire`.

The optional caller marker is placed in event context for synchronization.

**Result** A record with internal service properties removed.

- `403` — access refused.
- `404` — paiement missing.
- `500` — business operation failed.
- `503` — query or persistence failure.

Source lines `190–225` with `_checkAccessToPaymentForExternalUser 280–300`, `get 75–90`.

## `delete` — Delete a customer payment

**Arguments** `id`.

**Access** The decision uses right `facture.paiement`, linked-record access decision.

**Result** Acknowledgement under `success` with `code`, `message`.

- `403` — access refused.
- `404` — paiement missing.
- `409` — removal failed.
- `500` — removal failed.
- `503` — query or persistence failure.

Source lines `241–267` with `_checkAccessToPaymentForExternalUser 280–300`.
