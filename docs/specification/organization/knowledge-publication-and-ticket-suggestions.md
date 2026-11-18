# Knowledge editing, publication and ticket suggestions

A knowledge record holds a question and a formatted answer. It carries a business reference, entity, optional language, author, modifier, validating user and lifecycle status. Its general categories organize the knowledge collection. Its optional ticket group determines where a help-desk requester may be offered the answer. Assigning a general category does not set the ticket group.

## Authoring and revision

| Operation | Stored or observable result |
| --- | --- |
| Create | Create a record with its own question, reference and entity. The record can be prepared before writing an answer. A draft does not qualify for ticket suggestions. |
| Revise | Update the question, answer, language or association on the current record and retain the same identity. The update operation writes the existing object. Its business data model exposes no immutable succession of article editions or version-specific publication dates. |
| Validate | Replace a provisional reference with the next reference from the numbering scheme, set state 1, write the validating user and run the validation event. An already validated record returns a no-change result. |
| Withdraw for editing | The staff card offers return-to-draft on a validated record. The resulting state 0 removes the current record from validated-only readers. |
| Cancel and reopen | The cancel operation applies to a validated record and sets 9. Reopen applies to a canceled record and sets it back to validated. Readers will see its current answer when it again meets the publication criteria. |
| Clone | Create a separate draft with a fresh identity, default provisional reference and copy-marked question. Clear the old creation identity and unique custom values and handle the new object’s contacts through the clone flow. The old and new records can then be maintained independently. |

When a provisional reference changes, the validator updates document-index paths and filenames and attempts to rename the physical document directory so existing attachments follow the record. Removing the record calls the business deletion operation and attempts to remove its reference-specific document directory. The document index and physical files are separate resources.

A writer can revise a factual answer on the existing article. If the answer must disappear while it is being reconsidered, returning it to draft removes it from suggestions immediately. Creating another language’s article by cloning leaves the original available and produces another independent draft. Cloning alone provides no shared revision numbering, automatic translation synchronization or supersession date.

Implementation evidence appears in `htdocs/install/mysql/tables/llx_knowledgemanagement_knowledgerecord-knowledgemanagement.sql`, `htdocs/knowledgemanagement/class/knowledgerecord.class.php` (`createFromClone`, `update`, `delete`, `validate`, `setDraft`, `cancel`, `reopen`) and `htdocs/knowledgemanagement/knowledgerecord_card.php:488–531`.

## Suggesting a solution to a requester

The ticket suggestion reader matches the requested ticket-group **code** against an active dictionary entry. It joins the knowledge record by that group’s identifier. On the public route the group also has to be marked public. It returns a record only if it is validated, has a nonempty stored answer and satisfies the language condition. The condition admits the requested language and the reader’s unspecified-language values. It does not select an arbitrary translation from a different language.

The response presents the question as a title, the reference, the answer and its URL field when populated. The response contains candidate answers. Selecting a help topic does not assign the ticket, change its progress or close it. A matching answer with no ticket-group association has no route into this suggestion list. The staff-facing knowledge collection and the public help route therefore expose different subsets.

For example, a Spanish-language answer assigned to an active public group becomes eligible for that group’s Spanish query when validated and populated. Reclassifying the group as internal removes it from the public query without deleting the article. Clearing the answer removes it from the eligible results even if its validation state remains 1. Removing a general category alone leaves the ticket-group join intact.

## Permissions by entry point

Staff read, write and delete grants are separate. A writer can delete a draft through the staff card, while a later-state record calls for delete authority. With advanced rights active, the card distinguishes the advanced validation right from ordinary write. The programmatic validation operation checks knowledge write and returns distinguishable outcomes for missing object, already validated and unsuccessful mutation. Retrieving one knowledge record through the business service checks read authority and access to that record. The separate general-category lookup checks category read. An anonymous request for ticket suggestions follows the publication predicates above.

Implementation evidence appears in `htdocs/core/ajax/fetchKnowledgeRecord.php:60–110`, `htdocs/knowledgemanagement/knowledgerecord_card.php:88–93` and `htdocs/knowledgemanagement/class/api_knowledgemanagement.class.php` (`get`, `getCategories`, `validate`, `cancel`).
