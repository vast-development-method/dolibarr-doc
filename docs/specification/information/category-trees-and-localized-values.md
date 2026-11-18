# Category trees, object membership and localized values

A category has a durable identifier, business type, parent identifier, label, description, color, visibility, display position and entity. The category is one node. The object it classifies, such as a product, customer, supplier, invoice, manufacturing order or project task, retains its own identity. A typed association links the two. A product can belong to multiple categories and a category can contain many products.

## Naming and moving a node

A root category has parent zero. Within the visible category entity scope the duplicate search considers type, parent and label. Two product categories named “Replacement” can coexist below distinct parents. A customer and a product category can also use that label under the root. Renaming or moving a category checks the destination sibling set, excluding the current row from the collision test. A label is therefore unsuitable as a global category identifier.

The edit operation normalizes the parent, rejects self-parenting, and on a parent change walks upward from the proposed parent. If it encounters the moving category it rejects the move. This prevents selecting either a child or a deeper descendant as the new parent. On success the entity keeps the same category and association identifiers. A path such as “Equipment / Replacement” is a value derived from the ancestry and may change on a move. References to a category should persist its ID.

Creation/update flows can also save optional attributes, maintain language overrides and emit the relevant category event. The staff card requires read access, and creating or editing the category requires category creation authority. Visibility on the node is separate metadata. A visible category does not grant editing permission on its member records.

Implementation evidence appears in `htdocs/categories/class/categorie.class.php` (`create`, `update`, `already_exists`, `get_full_arbo`), `htdocs/categories/card.php:51–53,131–198` and `htdocs/categories/edit.php:71–113`.

## Classifying and removing objects

| Operation | Result |
| --- | --- |
| Add an object to a category | Insert the category/object pair in the association storage for the type. A duplicate is reported distinctly. This does not create a second copy of the object. |
| Add with recursive classification enabled | After a successful new association, inspect the parent. If the object is absent there, add to the parent recursively. An existing parent association stops that recursive path. Ancestor memberships acquired this way are actual associations. |
| Remove an object from a category | Remove the specified pair for that type and publish the unlink event. The operation acts on this pair alone. Ancestor assignments created on an earlier recursive add can remain. |
| Delete a category | Emit the deletion event, reparent the category’s immediate children to its parent, delete category-side links and associated detail, remove the node. The affected objects retain their own business records. |

Consider a root “Field”, child “Pump” and grandchild “Seal”. Adding an item to Seal under recursive classification can give it three direct associations. Removing the Seal association leaves Pump and Field unless separately removed. Deleting Pump promotes Seal to be a direct child of Field. Objects previously linked exclusively to Pump do not thereby acquire membership in Seal. A tree browser displaying descendants and a report counting direct members can legitimately return different results.

An object-membership lookup traverses the type-specific association, while a tree lookup traverses parentage. Both views can be scoped to one subtree or object without treating a repeated label as an identifier. The category tree reader can load a language override for label and description as it composes a full path. A missing translated label falls back to the category’s base label when building the tree.

Implementation evidence appears in `htdocs/categories/class/categorie.class.php` (`delete`, `add_type`, `del_type`, `containsObject`, `getListForItem`, `get_full_arbo`, `containing`).

## Stored translations

An object translation is keyed by object and language. Numeric identifiers, reference codes, product quantities and category links remain on the original object. The translation row holds descriptive values. Changing its text affects the reader’s language-specific view of the same record.

| Object | Values and write rules |
| --- | --- |
| Category | For the current language use the active category label and description. For supplied other languages, write the language-specific label and description. Existing rows update in place and missing rows are inserted. Deleting a translation targets only the category/language pair. |
| Product or service | Maintain its label and description. A setting permits the additional descriptive field to be translated as a note. For a supplied non-current-language translation a label is required. A missing label is a language-specific error even if a description was supplied. |
| Generated commercial document | Choose an explicit requested output language where enabled, otherwise the third party’s default language, otherwise the active language. The public-note regeneration action supplies this language to the document writer. |

Loading category translations provides a map of all stored language values. When a row matches the current language it also supplies the active label and description. Clearing a translation and deleting its row differ. For example, a supplied empty alternate-language category can leave an existing language row with blank values. The delete-translation action removes the row explicitly. The translation card applies the category’s object access and distinguishes authority to add and delete.

“Pump” and “Pompe” can thus be the published labels of product ID 81 without generating separate inventory balances. A French label on a product and a French description on a category are independently owned by their respective records. Renaming the category changes the navigational labels in that language without renaming its products.

Implementation evidence appears in `htdocs/categories/class/categorie.class.php` (`setMultiLangs`, `delMultiLangs`, `getMultiLangs`), `htdocs/categories/traduction.php:78–82`, `htdocs/product/class/product.class.php` (`setMultiLangs`, `delMultiLangs`, `getMultiLangs`) and `htdocs/core/actions_setnotes.inc.php:52–81`.
