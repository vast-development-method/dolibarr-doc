# Custom attributes, formulas and record notes

A custom attribute definition belongs to a business object type and an entity scope. A custom attribute value belongs to one identified instance of that type. The label shown on a form, the internal field name and the value stored on an invoice or contact are different pieces of information. Changes to presentation should preserve that distinction.

## Attribute definition and input

| Definition property | Consequence for the record |
| --- | --- |
| Internal name and object type | Identify a value column in the object’s extension storage. Contacts and business partners map to their respective underlying object types. A header and its detail lines can have different definitions. |
| Type and parameters | Determine conversion and presentation. Options include text, numbers, currency amounts, dates, datetimes, durations, selectable values, multi-value choices, object references and visual separators. |
| Required, unique and default | A required value must satisfy the emptiness rules for its own type. A unique ordinary value can have a uniqueness constraint. Form processing may use a configured default when invoked in its default-if-missing mode. |
| Formula | Makes the value derived. Creating a computed field clears the mandatory and unique flags. A form separator also has no mandatory or unique value and gets no stored value column. |
| Visibility, permission and enablement | Control which surfaces can read or edit the extension. A list-only or view-only field can remain on reports without becoming editable on the object form. |
| Always editable, printable, totalizable, clear-on-clone, personal data | Carry separate decisions about edits, exported document presentation, aggregation, copying and personal-data cleanup. Marking a value personal makes it eligible for the configured retention operation. |

The form reader evaluates enablement, visibility and field-specific permission before taking submitted values. It skips hidden or list-only fields in an update form. On a partial submission a missing ordinary field can mean “leave it alone.” Some controls, specifically unchecked checkboxes, omit their value when the user turns them off. These receive type-specific handling so a visible choice can be cleared without overwriting unrelated fields.

A calendar date uses the date components. Local date-time uses the acting user’s time-zone treatment, while the explicit GMT type uses UTC. An input that denotes absence may also vary by type. An empty array is absent for a multi-selection. Minus one is the empty object-link choice. Zero is the empty dictionary-list choice, while a zero price, integer or decimal is a genuine numeric value. A boolean field marked mandatory follows the general empty-value rule, so a false checkbox can fail the mandatory test.

For example, an inspector recording a measured quantity of zero has supplied a value. A selector still showing “choose a warehouse” supplies no warehouse reference. Replaying an entire form submission as a single generic merge would erase distinctions between a missing value, an explicit zero and an unchecked box.

Implementation evidence appears in `htdocs/core/class/extrafields.class.php` (`addExtraField`, `updateExtraField`, `setOptionalsFromPost`, `isEmptyValue`) and `htdocs/core/class/commonobject.class.php` (`fetch_optionals`, `insertExtraFields`, `updateExtraField`).

## Formula evaluation, stored values and clones

An ordinary extension row points back to the business object. Fetching it populates optional values alongside the object. When a formula is defined and calculation is enabled, the read path can evaluate the formula using the current object even when no extension row existed. Two invoices may therefore expose the same computed indicator without a manually entered value on either one.

Writing extensions treats a formula separately from posted inputs. When stored computed fields are enabled, the write path evaluates the formula with the owning object and materializes its result. It otherwise skips writing the computed field in the normal value assignment. Re-reading, querying a stored column and running a generic export are different channels. In particular the standard export writer has an explicit unsupported result for arbitrary computed extension formulas. A user inspecting a rendered form can see a value that is unavailable in a generic export.

An object clone can clear a field marked unique or clear-on-clone. Product-combination creation also clears unique extensions to avoid conflicting with the source combination. Clone behavior depends on entering the operation with the appropriate context. It differs from an ordinary update, which keeps the record’s own identity and can change a single selected extension. The mandatory-value check in the common write path also accounts for the stored field constraint, even if the field is conditionally disabled on a form.

Implementation evidence appears in `htdocs/core/class/commonobject.class.php:6837–6958,7005–7101,7515–7594` and `htdocs/exports/class/export.class.php` (`build_file`).

## Ownership and publication of notes

A public or private note belongs to the object, e.g., a customer, order or invoice. The note action accepts the target object and an explicit note field, replaces its contents, records the modifying user and requests the object’s modification event. A blank note clears the stored value. The event name and modifier field are chosen for the underlying object. The file index, for example, uses its own modifier field. A note edit can affect subscribers to an invoice- or company-modified event without changing the invoice lines or the company identifier.

| Edit | Authorization and secondary effects |
| --- | --- |
| Public note | The calling module supplies permission to edit notes. The shared action accepts restricted formatted text. On customer and supplier quotations, orders and invoices it can regenerate the document after the note is saved. |
| Private note | Requires the calling module’s note permission and an internal user without an external-party binding. It writes the private field. The common private-note action does not regenerate a customer document. |
| Public document regeneration | When automatic generation is active it uses the selected document model, output language, and visibility options for references, descriptions and line details. A generation failure produces a warning after the successful note update. |

For example, a customer order might carry “deliver at the north gate” in its public note and internal picking instructions in its private note. Updating delivery instructions can change the regenerated order copy. A regeneration warning means that the current public note and the existing document file may disagree. Updating the private instructions alone does not create a fresh outbound order copy.

Implementation evidence appears in `htdocs/core/actions_setnotes.inc.php` and `htdocs/core/class/commonobject.class.php:3976–4058`.
