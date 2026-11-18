# Other shared records events

Each entry identifies an operator-selectable event or a named signal emitted by a business operation. A numbered agenda entry identifies a dedicated branch for building the activity. Notification indicates built-in eligibility subject to subscription. Workflow indicates a branch whose settings govern downstream changes. See the [event contract](README.md) for shared dispatch rules and source keys.

| Event | Setup meaning or origin | Direct emission site | Specific subscriber branches |
| --- | --- | --- | --- |
| `CATEGORY_CREATE` | Named operation signal | `categories/class/categorie.class.php:638 (create)` | No dedicated branch listed |
| `CATEGORY_DELETE` | Named operation signal | `categories/class/categorie.class.php:792 (delete)` | No dedicated branch listed |
| `CATEGORY_DEL_MULTILANGS` | Named operation signal | `categories/class/categorie.class.php:2306 (delMultiLangs)` | No dedicated branch listed |
| `CATEGORY_MODIFY` | Named operation signal | `categories/class/categorie.class.php:751 (update)` · `categories/class/categorie.class.php:946 (add_type)` · `categories/class/categorie.class.php:1006 (del_type)` | No dedicated branch listed |
| `CATEGORY_SET_MULTILANGS` | Named operation signal | `categories/class/categorie.class.php:2276 (setMultiLangs)` | No dedicated branch listed |
| `LINK_CREATE` | Named operation signal | `core/class/link.class.php:141 (create)` | No dedicated branch listed |
| `LINK_DELETE` | Named operation signal | `core/class/link.class.php:404 (delete)` | No dedicated branch listed |
| `LINK_MODIFY` | Named operation signal | `core/class/link.class.php:221 (update)` | No dedicated branch listed |
| `MAILING_CREATE` | Named operation signal | `comm/mailing/class/mailing.class.php:279 (create)` | No dedicated branch listed |
| `MAILING_DELETE` | Named operation signal | `comm/mailing/class/mailing.class.php:755 (delete)` | No dedicated branch listed |
| `MAILING_MODIFY` | Named operation signal | `comm/mailing/class/mailing.class.php:346 (update)` | No dedicated branch listed |
| `MYECMDIR_CREATE` | Named operation signal | `ecm/class/ecmdirectory.class.php:217 (create)` | No dedicated branch listed |
| `MYECMDIR_DELETE` | Named operation signal | `ecm/class/ecmdirectory.class.php:458 (delete)` | No dedicated branch listed |
| `MYECMDIR_MODIFY` | Named operation signal | `ecm/class/ecmdirectory.class.php:276 (update)` | No dedicated branch listed |
| `OBJECT_LINK_DELETE` | Named operation signal | `core/class/commonobject.class.php:4902 (deleteObjectLinked)` | No dedicated branch listed |
| `OBJECT_LINK_INSERT` | Named operation signal | `core/class/commonobject.class.php:4551 (add_object_linked)` | No dedicated branch listed |
| `OBJECT_LINK_MODIFY` | Named operation signal | `core/class/commonobject.class.php:4840 (updateObjectLinked)` | No dedicated branch listed |
| `OPENSURVEY_CREATE` | Named operation signal | `opensurvey/class/opensurveysondage.class.php:303 (create)` | No dedicated branch listed |
| `OPENSURVEY_DELETE` | Named operation signal | `opensurvey/class/opensurveysondage.class.php:478 (delete)` | No dedicated branch listed |
| `OPENSURVEY_MODIFY` | Named operation signal | `opensurvey/class/opensurveysondage.class.php:436 (update)` | No dedicated branch listed |
| `TARGET_VALIDATE` | Named operation signal | `webhook/class/target.class.php:626 (validate)` | No dedicated branch listed |
| `TVA_CREATE` | Named operation signal | `compta/tva/class/tva.class.php:213 (create)` | No dedicated branch listed |
| `TVA_DELETE` | Named operation signal | `compta/tva/class/tva.class.php:430 (delete)` | No dedicated branch listed |
| `TVA_MODIFY` | Named operation signal | `compta/tva/class/tva.class.php:279 (update)` | No dedicated branch listed |
