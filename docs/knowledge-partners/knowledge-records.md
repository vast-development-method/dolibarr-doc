# Knowledge records for support teams

The business record is a referenceable question and answer. Authors can attach a language and associate the record with a ticket category. General article categories are a separate classification used to organize and filter records. The ticket-category field is enabled when the ticket module is active. Keep these two category identifiers distinct when mapping the record into a search index. [Guide](https://wiki.dolibarr.org/index.php/Module_Knowledge_Management) · [Fields](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/knowledgerecord.class.php#L93-L111) · [General categories](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/knowledgerecord.class.php#L1174-L1193)

| Concern | Behavior |
|---|---|
| Identity and content | Internal ID, entity, reference, required question, optional rich-text answer, language, creation and modification metadata, validator, attachments and optional ticket category |
| Draft → validated | Write permission. Resolve a provisional reference, store validated (1), stamp the validator and run the validation trigger inside the transaction |
| Retire and restore | Retire only a validated record; state 9 is displayed as obsolete. Reopen an obsolete record to validated. Draft (0) remains a separate editorial state |
| Search | The record listing can filter by general category and supplied search criteria. Clients building a published list should explicitly filter status 1 as the main collection has no unconditional validated-state filter |
| Permissions | Read, write and delete are separate record grants. Reading the category collection for a record also calls for category-read authority |

[Storage](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/install/mysql/tables/llx_knowledgemanagement_knowledgerecord-knowledgemanagement.sql) · [Validation](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/knowledgerecord.class.php#L576-L696) · [Transitions](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/knowledgerecord.class.php#L709-L773) · [REST reads](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/api_knowledgemanagement.class.php#L73-L191)

The REST adapter exposes record retrieval by ID, listing with filtering, and create/update/delete. The category endpoint is relative `GET knowledgerecords/{id}/categories`; validation and cancellation are separately annotated `POST {id}/validate` and `POST {id}/cancel` on the adapter. Validation returns the refreshed business object. An already-validated record returns a no-change response (304), an unknown record yields 404 and a missing write grant yields 403. A supported answer may contain formatted content. Preserve its intended presentation and the entity and language accompanying it when generating a knowledge view. [Service methods](https://github.com/Dolibarr/dolibarr/blob/5c6c7ff6a5112413b1c27221c8d11750afad56f8/htdocs/knowledgemanagement/class/api_knowledgemanagement.class.php#L458-L520)

| Acceptance case | Expected observation |
|---|---|
| Draft question with no answer is stored | Empty answer is permitted by the record definition. The editorial state remains draft |
| An author validates, retires, then reopens a record | It returns to validated. The existing record ID and its classification are retained |
| Article has general category A and suggested ticket group B; client selects category A | The list joins the general category membership; B remains the separate ticket-group association |

The [record schema](../../schemas/knowledge-partners/knowledge-record.schema.json) models the identity, editorial state and searchable content used by this flow.
