# General-ledger export

Exports booked entries for a reporting period. The caller chooses whether previously exported entries qualify, whether to include lettering and whether a successful export should mark entries as exported. The returned metadata identifies the generated document for a separate download.

The implementation locations below refer to `htdocs/accountancy/class/api_accountancy.class.php`.

## `exportData` — Export data

Route `GET exportdata`.

**Arguments** `period` (text), `date_min = ''` (text), `date_max = ''` (text), `format = ''` (text), `lettering = 0` (integer), `alreadyexport = 0` (integer), `notnotifiedasexport = 0` (integer).

**Access** The decision uses right `accounting.mouvements.export`.

The method generates the accounting export. The method opens a database transaction and provides commit and rollback paths. Named periods include the current or previous month, three or six months, current or previous calendar year, current or previous fiscal year and the current plus previous fiscal years. A custom period accepts date bounds. The export defaults to sorting by bookkeeping piece and then entry identifier. Turning on lettering adds reconciliation information. The already-exported flag changes row eligibility and the no-notification flag controls marking.

**Result** A record with `modulepart`, `relative_path`, `filename`, `mimetype`.

- `403` — access refused.
- `404` — accountancy export period missing, requested data unavailable, accountancy export format missing.
- `500` — business operation failed, accounting export generated no downloadable file.

Source lines `91–294`.
