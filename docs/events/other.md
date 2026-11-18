# Other shared records events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. An agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch and subscription rules.

| Event | Setup meaning or origin | Emitting operation | Specific subscriber branches |
| --- | --- | --- | --- |
| `CATEGORY_CREATE` | Operation signal | `categorie.create` | No dedicated branch listed |
| `CATEGORY_DELETE` | Operation signal | `categorie.delete` | No dedicated branch listed |
| `CATEGORY_DEL_MULTILANGS` | Operation signal | `categorie.delMultiLangs` | No dedicated branch listed |
| `CATEGORY_MODIFY` | Operation signal | `categorie.update` · `categorie.add_type` · `categorie.del_type` | No dedicated branch listed |
| `CATEGORY_SET_MULTILANGS` | Operation signal | `categorie.setMultiLangs` | No dedicated branch listed |
| `LINK_CREATE` | Operation signal | `link.create` | No dedicated branch listed |
| `LINK_DELETE` | Operation signal | `link.delete` | No dedicated branch listed |
| `LINK_MODIFY` | Operation signal | `link.update` | No dedicated branch listed |
| `MAILING_CREATE` | Operation signal | `mailing.create` | No dedicated branch listed |
| `MAILING_DELETE` | Operation signal | `mailing.delete` | No dedicated branch listed |
| `MAILING_MODIFY` | Operation signal | `mailing.update` | No dedicated branch listed |
| `MYECMDIR_CREATE` | Operation signal | `ecmdirectory.create` | No dedicated branch listed |
| `MYECMDIR_DELETE` | Operation signal | `ecmdirectory.delete` | No dedicated branch listed |
| `MYECMDIR_MODIFY` | Operation signal | `ecmdirectory.update` | No dedicated branch listed |
| `OBJECT_LINK_DELETE` | Operation signal | `commonobject.deleteObjectLinked` | No dedicated branch listed |
| `OBJECT_LINK_INSERT` | Operation signal | `commonobject.add_object_linked` | No dedicated branch listed |
| `OBJECT_LINK_MODIFY` | Operation signal | `commonobject.updateObjectLinked` | No dedicated branch listed |
| `OPENSURVEY_CREATE` | Operation signal | `opensurveysondage.create` | No dedicated branch listed |
| `OPENSURVEY_DELETE` | Operation signal | `opensurveysondage.delete` | No dedicated branch listed |
| `OPENSURVEY_MODIFY` | Operation signal | `opensurveysondage.update` | No dedicated branch listed |
| `TARGET_VALIDATE` | Operation signal | `target.validate` | No dedicated branch listed |
| `TVA_CREATE` | Operation signal | `tva.create` | No dedicated branch listed |
| `TVA_DELETE` | Operation signal | `tva.delete` | No dedicated branch listed |
| `TVA_MODIFY` | Operation signal | `tva.update` | No dedicated branch listed |
