# Document ownership, indexing and sharing

A file can exist as a binary in a document directory, as an index entry describing it and as an attachment to a business object. A folder organizes the first two. The attachment’s source type and source ID identify the business owner. These identities matter when a user renames a file, issues a public copy, removes its index entry or records approval on the owning agreement.

## File and folder identity

| Value | Meaning |
| --- | --- |
| Index row ID, entity, relative directory and filename | Identify the indexed item and its location. A path lookup uses the entity, normally the current entity unless an explicit one is supplied. Source-object lookup has a separate type-and-ID index. |
| Path reference | The default reference is derived from the path and filename. It identifies a location, so a rename can affect it. |
| Content fingerprint | A label used by the indexing operation can hold the file content fingerprint. Copies of identical content can have the same fingerprint while occupying different locations. |
| Share value | An independently issued key authorizing public access to this item. Sharing can be revoked without deleting the content or changing the owner. |
| Origin and authorship | Record the source object, whether the file was generated, uploaded or otherwise indexed, its creating and modifying users, position and descriptive metadata. |
| Manual folder | Record parent, label, description, creation information and cached document count. Its relative directory is assembled from the ancestor chain. |

Creating an index row requires a filename and directory, normalizes the path and can derive a position from the existing entries in that directory. Creating a manual folder checks the full folder path under its parent, creates the folder record and corresponding physical directory, and emits a directory-created event. Two same-named leaf folders in different branches describe different directories.

The folder’s cached file count can be incremented, decremented or refreshed. It is a summary for browsing. An index lookup can work from location, content, share value or business owner depending on the operation. A current attachment list for a specific invoice should identify that invoice as source, instead of treating all files with its printable reference in their names as belonging to it.

Implementation evidence appears in `htdocs/install/mysql/tables/llx_ecm_files.sql`, `htdocs/install/mysql/tables/llx_ecm_files.key.sql`, `htdocs/ecm/class/ecmfiles.class.php` (`create`, `fetch`) and `htdocs/ecm/class/ecmdirectory.class.php` (`create`, `getRelativePath`, `changeNbOfFiles`, `refreshcachenboffile`).

## Rename, publish and revoke

The file card distinguishes document read, upload and setup permissions. Editing file metadata or sharing from this card uses setup permission. Upload authority alone does not establish that this user may change a public share setting. The ordinary download route applies module/document permission and, where appropriate, access to the underlying business record. The index contains an access-control-list field reserved for future per-file use. This field alone does not define a current per-file authorization engine.

On a rename, the editor checks whether the destination name is occupied, moves the underlying file and updates its index through the file-move operation. It retains the protected suffix for file types stored with that suffix. When an existing indexed file is shared, generate a share value only if it lacks one. Leaving sharing enabled on the next edit preserves the existing public link. Disabling it clears the value. When the file is present but an index row must be created, the editor can calculate the content fingerprint and create the row.

A public link resolves the share value to the file and its stored location. It can be opened without a staff session. The resolver derives the module and entity from the located file and checks any explicitly supplied module against it. A revoked or invalid key cannot resolve this item. An ordinary authenticated user may still be entitled to the same file by the source document after the public link is revoked. The reverse also holds: public access to the shared file confers no authority to edit the customer, contract or ticket in staff screens.

A service manager can therefore share a generated intervention PDF with a customer and later revoke access while retaining the work record. An online acknowledgment is a different action. The intervention signing operation records the receiver’s signature state on that intervention and emits its modification event. Looking up a shared PDF or toggling the share value does not execute that approval transition.

Implementation evidence appears in `htdocs/ecm/file_card.php:119–121,144–245,380–404`, `htdocs/document.php:193–255,301–351` and `htdocs/core/ajax/onlineSign.php` (intervention receiver-signature action).

## Removing material

Deleting a file index object invokes its deletion event, removes extension values and deletes the index row. The index object’s operation contains no physical unlink. Physical removal is the responsibility of the file or directory operation which owns that action. An index-only removal and destruction of the underlying bytes are therefore distinguishable events.

Folder deletion has separate database-only and physical modes. A physical non-recursive delete attempts to remove the directory itself and can fail when it contains files. Recursive removal first processes child folder records, then attempts recursive physical removal of the root folder and its contents. A database-only action skips physical removal. Reported directory or event errors can roll the database changes back. The filesystem and the relational store are distinct resources, and physical deletion has no general database rollback mechanism.

The administrator’s purge tool can target temporary material, old temporary material, logs or document files. Age-based choices compare the stored file modification time with the configured age in seconds. The full-document option requires explicit confirmation. A purge of old files is a physical storage operation. Customer inactivity, membership expiry and the business rules for removing personal attributes are evaluated by the separate [retention policy](retention-and-personal-data.md).

Implementation evidence appears in `htdocs/ecm/class/ecmfiles.class.php:846–901`, `htdocs/ecm/class/ecmdirectory.class.php:415–496`, `htdocs/admin/tools/purge.php:58–82,126–152` and `htdocs/core/class/utils.class.php` (`purgeFiles`).
