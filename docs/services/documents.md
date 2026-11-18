# Document exchange

The document service distinguishes a stored file, a generated business document and a file listing for a business element. Identity includes the document area, relative path and owning record where applicable.

The implementation locations below refer to `htdocs/api/class/api_documents.class.php`.

## `index` — List records

Route `GET /download`.

**Arguments** `modulepart` (text), `original_file = ''` (text).

**Access** The decision uses linked-party scope.

**Result** A record with `filename`, `content-type`, `filesize`, `content`, `encoding`.

- `400` — bad value for parameter modulepart, bad value for parameter original_file.
- `403` — access or input restriction, access refused.
- `404` — file missing.

Source lines `72–145`.

## `builddoc` — Builddoc

Route `PUT /builddoc`.

**Arguments** `modulepart` (text), `original_file = ''` (text), `doctemplate = ''` (text), `langcode = ''` (text).

**Access** The decision uses linked-party scope.

The method generates the business document. The return identifies the template and rendering language alongside the filename, MIME type, byte size and base64-encoded document bytes.

**Result** A record with `filename`, `content-type`, `filesize`, `content`, `langcode`, `template`, `encoding`.

- `400` — bad value for parameter modulepart, bad value for parameter original_file.
- `403` — access or input restriction, access refused.
- `404` — invoice missing, supplier invoice missing, order missing, proposal missing, contract missing, shipment missing, mo missing, expense report missing, holiday missing, product missing, warehouse missing, intervention missing, file missing.
- `500` — document generation failed.

Source lines `178–440`.

## `getDocumentsListByElement` — Read documents list by element

Route `GET /`.

**Arguments** `modulepart` (text), `id = 0` (integer), `ref = ''` (text), `sortfield = ''` (text), `sortorder = ''` (text), `limit = 100` (integer), `page = 0` (integer), `content_type = ''` (text), `pagination_data = false` (boolean).

**Access** The decision uses right `societe.lire`, right `user.user.lire`, right `adherent.lire`, right `propal.lire`, right `supplier_proposal.read`, right `commande.lire`, one of `fournisseur.commande.lire` or `supplier_order.lire`, right `expedition.lire`, right `facture.lire`, one of `fournisseur.facture.lire` or `supplier_invoice.lire`, right `produit.lire`, one of `agenda.myactions.read` or `agenda.allactions.read`, right `expensereport.read`, right `holiday.read`, right `ticket.read`, right `knowledgemanagement.knowledgerecord.read`, right `categorie.lire`, right `contrat.lire`, right `ficheinter.lire`, right `projet.lire`, right `mrp.read`, right `societe.contact.lire`, right `stock.lire`.

Authorization is selected by the requested document area. Rights for unrelated business areas in the list of access decisions are alternative branches. The record selector accepts an identifier or business reference for the selected area.

**Result** An ordered collection. With `pagination_data` enabled, `data` carries the rows and `pagination` carries `total`, `page`, `page_count`, `limit`.

- `400` — bad value for parameter modulepart, bad value for parameter id or ref.
- `403` — access refused.
- `404` — document area disabled or unsupported, no document for the requested business record.
- `500` — unsupported operation or value.
- `503` — query or persistence failure.

Source lines `471–713`.

## `post` — Create a document

Route `POST /upload`.

**Arguments** `filename` (text), `modulepart` (text), `ref = ''` (text), `subdir = ''` (text), `filecontent = ''` (text), `fileencoding = ''` (text), `overwriteifexists = 0` (integer), `createdirifnotexists = 1` (integer), `position = 0` (integer), `cover = ''` (text), `array_options = []` (collection), `generateThumbs = 0` (integer), `share = 0` (integer).

**Access** The decision uses right `ecm.upload`.

The method generates image previews. The named area determines where the content can be stored. A write can optionally create the target directory, replace an existing file, generate previews or mark the uploaded file shareable. The default preserves an existing file of the same name.

**Result** The stored filename.

- `400` — invalid request data, access refused, directory missing, duplicate record or association.
- `403` — access refused, access or input restriction.
- `404` — owning record missing.
- `500` — business operation failed, reference incompatible with this document area, unsupported operation or value, file write failed, file move failed.

Source lines `766–1106`.

## `delete` — Delete a document

Route `DELETE /`.

**Arguments** `modulepart` (text), `original_file` (text).

**Access** The decision uses linked-party scope.

**Result** Acknowledgement under `success` with `code`, `message`.

- `400` — bad value for parameter modulepart, bad value for parameter original_file.
- `403` — access or input restriction, access refused.
- `404` — file missing.

Source lines `1127–1208`.
