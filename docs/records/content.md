# Communication, publishing and documents

Persist the content or rule separately from an individual delivery, recipient, inbound action or file. A website scopes its content, a campaign scopes its recipient list, and indexed file metadata refers to separately stored content.

**Example.** Two campaigns can address the same email destination. The recipient row represents one destination in one campaign. Delivery success on the first campaign does not mark the recipient of the second as sent.

[All record families](README.md) · [Field conventions](README.md#reading-a-record)

| Business record | Storage name |
| --- | --- |
| [Website](#record-website) | `website` |
| [Site page](#record-website_page) | `website_page` |
| [Survey](#record-opensurvey_sondage) | `opensurvey_sondage` |
| [Survey response](#record-opensurvey_user_studs) | `opensurvey_user_studs` |
| [Poll comment](#record-opensurvey_comments) | `opensurvey_comments` |
| [Bulk mailing](#record-mailing) | `mailing` |
| [Recipient filter](#record-mailing_advtarget) | `mailing_advtarget` |
| [Mailing recipient](#record-mailing_cibles) | `mailing_cibles` |
| [Mail opt-out](#record-mailing_unsubscribe) | `mailing_unsubscribe` |
| [Notification history](#record-notify) | `notify` |
| [Notification subscription](#record-notify_def) | `notify_def` |
| [Inbound mail collector](#record-emailcollector_emailcollector) | `emailcollector_emailcollector` |
| [Mail processing action](#record-emailcollector_emailcollectoraction) | `emailcollector_emailcollectoraction` |
| [Mail selection condition](#record-emailcollector_emailcollectorfilter) | `emailcollector_emailcollectorfilter` |
| [Document directory](#record-ecm_directories) | `ecm_directories` |
| [Indexed document](#record-ecm_files) | `ecm_files` |
| [Document template registration](#record-document_model) | `document_model` |
| [Attached web link](#record-links) | `links` |
| [Object comment](#record-comment) | `comment` |
| [Translated property](#record-object_lang) | `object_lang` |
| [Translation override](#record-overwrite_trans) | `overwrite_trans` |
| [Saved import layout](#record-import_model) | `import_model` |
| [Saved export layout](#record-export_model) | `export_model` |
| [Outbound event target](#record-webhook_target) | `webhook_target` |
| [Outbound delivery attempt](#record-webhook_history) | `webhook_history` |
| [Delegated authorisation token](#record-oauth_token) | `oauth_token` |
| [Printer association](#record-printing) | `printing` |
| [Receipt printer](#record-printer_receipt) | `printer_receipt` |
| [Receipt layout](#record-printer_receipt_template) | `printer_receipt_template` |

<a id="record-website"></a>

## Website

Identifies a managed site and its publication settings. Pages reference the site independently.

**Storage** `website`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [website_page](content.md#record-website_page) (fk_website).

The stored state codes are `0` draft, `1` validated.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `type_container` | varchar(16) | No | `'page'` | Default classification of content in the site. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `maincolor` | varchar(16) | Yes | — | Theme colour configured for the site. |
| `maincolorbis` | varchar(16) | Yes | — | Theme colour configured for the site. |
| `lang` | varchar(8) | Yes | — | Language code under which this text or presentation is stored. |
| `otherlang` | varchar(255) | Yes | — | Additional languages available for the site. |
| `status` | integer | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `fk_default_home` | integer | Yes | — | Site page designated as the default landing page. |
| `use_manifest` | integer | Yes | — | Enables use of the site's web application manifest. |
| `virtualhost` | varchar(255) | Yes | — | Host name assigned to this site. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `paymentframemode` | integer | Yes | `0` | Payment-page presentation mode. Zero uses a full page. Mode one embeds payment and leaves confirmation outside the frame. Mode two also embeds confirmation. |
| `lastaccess` | datetime | Yes | — | Most recent recorded access to the site. |
| `lastpageid` | integer | Yes | `0` | Identifier of the last accessed page recorded in the site statistics. |
| `pageviews_previous_month` | bigint unsigned | Yes | `0` | Number of page views in the preceding monthly bucket. |
| `pageviews_month` | bigint unsigned | Yes | `0` | Page views accumulated in the current month. |
| `pageviews_total` | bigint unsigned | Yes | `0` | Cumulative number of page views across months. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `name_template` | varchar(255) | Yes | — | Name of the template imported for this site. |

<a id="record-website_page"></a>

## Site page

Stores a page or reusable container, its URL identity, content, metadata and publication or historical state.

**Storage** `website_page`.
The primary key is `rowid`.
An additional unique key comprises `fk_website`, `pageurl`.

**Referenced by** [categorie_website_page](categories.md#record-categorie_website_page) (fk_website_page).

The stored state codes are `0` draft, `1` validated.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_website` | integer | No | — | Website concerned. References [website](content.md#record-website) (rowid). |
| `type_container` | varchar(16) | No | `'page'` | Content container classification of this page. |
| `pageurl` | varchar(255) | No | — | Page name/alias. |
| `aliasalt` | varchar(255) | Yes | — | Alias Alt. |
| `title` | varchar(255) | Yes | — | Display title. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `image` | varchar(255) | Yes | — | Image. |
| `keywords` | varchar(255) | Yes | — | Keywords. |
| `metarobots` | varchar(128) | Yes | — | Page-level directives for search engine indexing. |
| `lang` | varchar(6) | Yes | — | Language code under which this text or presentation is stored. |
| `fk_page` | integer | Yes | — | Parent page ID. |
| `allowed_in_frames` | integer | Yes | `0` | Allowed in Frames. |
| `htmlheader` | text | Yes | — | Html Header. |
| `content` | mediumtext | Yes | — | Content. |
| `status` | integer | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `grabbed_from` | varchar(255) | Yes | — | Grabbed From. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `author_alias` | varchar(64) | Yes | — | Author Alias. |
| `date_creation` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `object_type` | varchar(255) | Yes | — | Object type used with a separate record identifier. |
| `fk_object` | varchar(255) | Yes | — | Identifier of the business record holding these values. |
| `keep_history` | integer | Yes | `5` | Retention limit for page revisions. Zero keeps all revisions, one keeps the latest, and higher values retain that number of changes. |

<a id="record-opensurvey_sondage"></a>

## Survey

Defines a poll's title, type, owner, closing date and participation settings.

**Storage** `opensurvey_sondage`.
The primary key is `id_sondage`.

The stored state codes are `0` draft, `1` validated, `2` closed.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id_sondage` | varchar(16) | No | — | Survey or poll identity. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `commentaires` | text | Yes | — | Comments. |
| `mail_admin` | varchar(128) | Yes | — | Mailadmin. |
| `nom_admin` | varchar(64) | Yes | — | Nomadmin. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `titre` | text | No | — | Display title. |
| `date_fin` | datetime | Yes | — | End of the applicable period. |
| `status` | integer | Yes | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `format` | varchar(2) | No | — | Format. |
| `mailsonde` | tinyint | No | `0` | Mailsonde. |
| `allow_comments` | tinyint | No | `1` | Allowcomments. |
| `allow_spy` | tinyint | No | `1` | Allowspy. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `sujet` | text | Yes | — | Subject of the message or poll. |

<a id="record-opensurvey_user_studs"></a>

## Survey response

Associates a respondent and answer data with a particular poll.

**Storage** `opensurvey_user_studs`.
The primary key is `id_users`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id_users` | integer (generated) | No | — | Respondent identifier in the survey answer table. |
| `nom` | varchar(64) | No | — | Name under which this record is presented or identified. |
| `id_sondage` | varchar(16) | No | — | Survey or poll identity. |
| `reponses` | varchar(200) | No | — | Answer selections retained for the poll response. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `date_creation` | datetime | No | — | When the row was created. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

<a id="record-opensurvey_comments"></a>

## Poll comment

Retains a participant comment in the context of its poll.

**Storage** `opensurvey_comments`.
The primary key is `id_comment`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `id_comment` | integer unsigned (generated) | No | — | Identity of the survey comment. |
| `id_sondage` | char(16) | No | — | Survey or poll identity. |
| `comment` | text | No | — | Free-text annotation retained with the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `usercomment` | text | Yes | — | Comment submitted for the survey. |
| `date_creation` | datetime | No | — | When the row was created. |
| `ip` | varchar(250) | Yes | — | Network address recorded for the relevant submission or event. |

<a id="record-mailing"></a>

## Bulk mailing

Defines a campaign, its sender, subject, body, status and processing dates.

**Storage** `mailing`.
The primary key is `rowid`.
An additional unique key comprises `titre`, `entity`.

The stored state codes are `0` draft, `1` validated, `2` sentpartialy, `3` sentcompletely.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `messtype` | varchar(16) | Yes | `'email'` | Campaign message channel, such as email or SMS. |
| `titre` | varchar(128) | Yes | — | Display title. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `sujet` | varchar(128) | Yes | — | Subject of the message or poll. |
| `body` | mediumtext | Yes | — | Message content prepared for the campaign. |
| `bgcolor` | varchar(8) | Yes | — | Background colour used by the message. |
| `bgimage` | varchar(255) | Yes | — | Background image used by the message. |
| `evenunsubscribe` | smallint | Yes | `0` | Campaign setting that permits delivery despite a recorded mailing opt-out. |
| `cible` | varchar(60) | Yes | — | Historical targeting field read on the campaign header. The recipient rows identify the people selected. |
| `nbemail` | integer | Yes | — | Recorded number of campaign recipients. |
| `email_from` | varchar(160) | Yes | — | Sender email address. |
| `name_from` | varchar(128) | Yes | — | Display name used for the sender. |
| `email_replyto` | varchar(160) | Yes | — | Email address proposed for replies to the campaign. |
| `email_errorsto` | varchar(160) | Yes | — | Address intended to receive delivery error messages. |
| `tag` | varchar(128) | Yes | — | Tag. |
| `date_creat` | datetime | Yes | — | When the row was created. |
| `date_valid` | datetime | Yes | — | When validation was recorded. |
| `date_appro` | datetime | Yes | — | Date the campaign was approved. |
| `date_envoi` | datetime | Yes | — | Date of sending. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `fk_user_valid` | integer | Yes | — | Account that validated the record. |
| `fk_user_appro` | integer | Yes | — | Approval-user field marked unused in the installation declaration. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `joined_file1` | varchar(255) | Yes | — | One of the attachment reference slots for the outgoing campaign. |
| `joined_file2` | varchar(255) | Yes | — | One of the attachment reference slots for the outgoing campaign. |
| `joined_file3` | varchar(255) | Yes | — | One of the attachment reference slots for the outgoing campaign. |
| `joined_file4` | varchar(255) | Yes | — | One of the attachment reference slots for the outgoing campaign. |
| `statut` | smallint | Yes | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `fk_project` | integer | Yes | `NULL` | Associated project identity. |

<a id="record-mailing_advtarget"></a>

## Recipient filter

Persists selection criteria used to construct a campaign's recipient set.

**Storage** `mailing_advtarget`.
The primary key is `rowid`.
An additional unique key comprises `name`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `name` | varchar(180) | No | — | Name under which this record is presented or identified. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_element` | integer | No | — | Target record identity. Where an object type accompanies it, both values identify the target. |
| `type_element` | varchar(180) | No | — | Type discriminator identifying the class of associated object. |
| `filtervalue` | text | Yes | — | Value supplied to the audience selection filter. |
| `fk_user_author` | integer | No | — | Account recorded as creator or author. |
| `datec` | datetime | No | — | When the row was created. |
| `fk_user_mod` | integer | No | — | Account recorded for the latest modification. |
| `tms` | timestamp | No | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

<a id="record-mailing_cibles"></a>

## Mailing recipient

Identifies a recipient for one campaign and retains per-recipient sending status and tracking information.

**Storage** `mailing_cibles`.
The primary key is `rowid`.
An additional unique key comprises `fk_mailing`, `email`.

The stored state codes are `0` notsent, `1` sent, `2` read, `3` readandunsubscribed, `-1` error.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_mailing` | integer | No | — | Bulk mailing campaign identity. |
| `fk_contact` | integer | No | — | Contact or address identity. |
| `lastname` | varchar(160) | Yes | — | Person's family name. |
| `firstname` | varchar(160) | Yes | — | Person's given name. |
| `email` | varchar(160) | No | — | Email address associated with this record. |
| `other` | varchar(255) | Yes | — | Additional information carried by the selected recipient. |
| `tag` | varchar(64) | Yes | — | Per-recipient token used to identify an unsubscribe request. |
| `statut` | smallint | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `source_url` | varchar(255) | Yes | — | Location of the object from which this recipient was selected. |
| `source_id` | integer | Yes | — | Identifier of the source object in the selected object family. |
| `source_type` | varchar(32) | Yes | — | Object family from which the recipient originated. |
| `date_envoi` | datetime | Yes | — | Date of sending. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `error_text` | varchar(255) | Yes | — | Delivery error recorded against the recipient after a failed send. |

<a id="record-mailing_unsubscribe"></a>

## Mail opt-out

Records a destination or object that has opted out of mailings and the relevant date.

**Storage** `mailing_unsubscribe`.
The primary key is `rowid`.
An additional unique key comprises `email`, `entity`, `unsubscribegroup`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `unsubscribegroup` | varchar(128) | Yes | empty string | Subscription group to which the address opt-out applies. |
| `ip` | varchar(128) | Yes | — | Network address recorded for the relevant submission or event. |
| `date_creat` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |

<a id="record-notify"></a>

## Notification history

Records an event-based notification and its business object, recipient and delivery destination.

**Storage** `notify`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `daten` | datetime | Yes | — | Time the notification was recorded. |
| `fk_action` | integer | No | — | Action or event type selected for the record. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_contact` | integer | Yes | — | Contact or address identity. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `type` | varchar(16) | Yes | `'email'` | Type. |
| `type_target` | varchar(16) | Yes | — | Selects how the notification recipient was resolved, such as a contact, user or fixed address. |
| `objet_type` | varchar(24) | No | — | Object type used with a separate record identifier. |
| `objet_id` | integer | No | — | Target identity within the associated object type. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |

<a id="record-notify_def"></a>

## Notification subscription

Defines which event and party, contact or user should produce a notification.

**Storage** `notify_def`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | date | Yes | — | When the row was created. |
| `fk_action` | integer | No | — | Action or event type selected for the record. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_contact` | integer | Yes | — | Contact or address identity. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `email` | varchar(255) | Yes | — | Email address associated with this record. |
| `threshold` | double(24,8) | Yes | — | Monetary threshold used in deciding whether a notification qualifies. |
| `context` | varchar(128) | Yes | — | Limits a notification to its configured event context. |
| `type` | varchar(16) | Yes | `'email'` | Type. |

<a id="record-emailcollector_emailcollector"></a>

## Inbound mail collector

Defines a mailbox ingestion configuration, processing options, status and execution details.

**Storage** `emailcollector_emailcollector`.
The primary key is `rowid`.
An additional unique key comprises `ref`, `entity`.

**Referenced by** [emailcollector_emailcollectoraction](content.md#record-emailcollector_emailcollectoraction) (fk_emailcollector), [emailcollector_emailcollectorfilter](content.md#record-emailcollector_emailcollectorfilter) (fk_emailcollector).

The stored state codes are `0` disabled, `1` enabled.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `host` | varchar(255) | Yes | — | Host of email IMAP server. |
| `port` | varchar(10) | Yes | `'993'` | Port of email IMAP server. |
| `hostcharset` | varchar(16) | Yes | `'UTF-8'` | Host charset. |
| `imap_encryption` | varchar(16) | Yes | `'ssl'` | Imap Encryption. |
| `norsh` | integer | Yes | `0` | No RSH. |
| `login` | varchar(128) | Yes | — | Login name of the account. |
| `acces_type` | integer | Yes | `0` | Authentication method. |
| `oauth_service` | varchar(128) | Yes | — | Oauth service. |
| `password` | varchar(128) | Yes | — | Password. |
| `source_directory` | varchar(255) | No | `'Inbox'` | Mailbox source directory. |
| `target_directory` | varchar(255) | Yes | — | Mailbox target directory. |
| `maxemailpercollect` | integer | Yes | `100` | Max number of emails collected per collect. |
| `datelastresult` | datetime | Yes | — | Time associated with the most recent job result. |
| `codelastresult` | varchar(16) | Yes | — | Latest result code. |
| `lastresult` | text | Yes | — | Outcome retained for the most recent execution. |
| `datelastok` | datetime | Yes | — | Date of latest collect success. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `position` | integer | No | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

<a id="record-emailcollector_emailcollectoraction"></a>

## Mail processing action

Defines an ordered operation attached to an inbound mail collector.

**Storage** `emailcollector_emailcollectoraction`.
The primary key is `rowid`.
An additional unique key comprises `fk_emailcollector`, `type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_emailcollector` | integer | No | — | Inbound collector governing the rule. References [emailcollector_emailcollector](content.md#record-emailcollector_emailcollector) (rowid). |
| `type` | varchar(128) | No | — | Type. |
| `actionparam` | text | Yes | — | Param For Action. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `position` | integer | Yes | `0` | Ordering value used within the relevant list, hierarchy or document. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

<a id="record-emailcollector_emailcollectorfilter"></a>

## Mail selection condition

Defines an ordered condition used to select messages for a collector.

**Storage** `emailcollector_emailcollectorfilter`.
The primary key is `rowid`.
An additional unique key comprises `fk_emailcollector`, `type`, `rulevalue`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_emailcollector` | integer | No | — | Inbound collector governing the rule. References [emailcollector_emailcollector](content.md#record-emailcollector_emailcollector) (rowid). |
| `type` | varchar(128) | No | — | Type. |
| `rulevalue` | varchar(128) | Yes | — | Value Of Rule. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | No | — | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

<a id="record-ecm_directories"></a>

## Document directory

Describes the named folder, parent, path and access metadata of a document grouping.

**Storage** `ecm_directories`.
The primary key is `rowid`.
An additional unique key comprises `label`, `fk_parent`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `label` | varchar(64) | No | — | Display label for the record. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_parent` | integer | Yes | — | Record one level above this one in the owning hierarchy. |
| `description` | varchar(255) | No | — | Descriptive text associated with this entry. |
| `cachenbofdoc` | integer | No | `0` | Cached number of documents in the directory. |
| `fullpath` | varchar(750) | Yes | — | Stored full path of the document directory. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `date_c` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_c` | integer | Yes | — | Account recorded as creator or author. References [user](foundation.md#record-user) (rowid). |
| `fk_user_m` | integer | Yes | — | Account recorded for the latest modification. References [user](foundation.md#record-user) (rowid). |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `acl` | text | Yes | — | Directory access-control information. |

<a id="record-ecm_files"></a>

## Indexed document

Records a file's path, metadata and optional originating object. The file contents have their own storage lifecycle.

**Storage** `ecm_files`.
The primary key is `rowid`.
An additional unique key comprises `filepath`, `filename`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `ref` | varchar(128) | Yes | — | Business reference used to identify the document or master record. |
| `label` | varchar(128) | No | — | Display label for the record. |
| `share` | varchar(128) | Yes | — | Token identifying the publicly shared link. |
| `share_pass` | varchar(32) | Yes | — | Protected access value for opening a shared item. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `filepath` | varchar(255) | No | — | File Path. |
| `filename` | varchar(255) | No | — | File Name. |
| `src_object_type` | varchar(64) | Yes | — | Source Type. |
| `src_object_id` | integer | Yes | — | Source ID. |
| `agenda_id` | integer | Yes | — | ID event. |
| `fullpath_orig` | varchar(750) | Yes | — | Full path origin. |
| `description` | varchar(255) | Yes | — | Descriptive text associated with this entry. |
| `keywords` | varchar(750) | Yes | — | Keywords. |
| `content` | text | Yes | — | Content. |
| `cover` | varchar(32) | Yes | — | Cover. |
| `position` | integer | Yes | — | Ordering value used within the relevant list, hierarchy or document. |
| `gen_or_uploaded` | varchar(12) | Yes | — | File origin. |
| `extraparams` | varchar(255) | Yes | — | Additional values encoded for the owning feature. |
| `date_c` | datetime | Yes | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_c` | integer | Yes | — | Account recorded as creator or author. |
| `fk_user_m` | integer | Yes | — | Account recorded for the latest modification. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `acl` | text | Yes | — | File access-control information. |
| `geolat` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geolong` | double(24,8) | Yes | `NULL` | Latitude or longitude for a geographic location. |
| `geopoint` | point | Yes | `NULL` | Geographic point value retained by the location field. |
| `georesultcode` | varchar(16) | Yes | — | Geocoding result or accuracy code. |

<a id="record-document_model"></a>

## Document template registration

Makes a named output model available to the corresponding business document type.

**Storage** `document_model`.
The primary key is `rowid`.
An additional unique key comprises `nom`, `type`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `nom` | varchar(50) | Yes | — | Name under which this record is presented or identified. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `type` | varchar(64) | No | — | Type. |
| `libelle` | varchar(255) | Yes | — | Display label for the record. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |

<a id="record-links"></a>

## Attached web link

Stores the target URL and label associated with a business object.

**Storage** `links`.
The primary key is `rowid`.
An additional unique key comprises `objectid`, `objecttype`, `label`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `datea` | datetime | No | — | Starting date recorded on the external link. |
| `url` | varchar(255) | No | — | Web address or navigation target. |
| `label` | varchar(255) | No | — | Display label for the record. |
| `objecttype` | varchar(255) | No | — | Object type used with a separate record identifier. |
| `objectid` | integer | No | — | Identifier of the business object owning the link. |
| `share` | varchar(128) | Yes | — | Token identifying the publicly shared link. |
| `share_pass` | varchar(32) | Yes | — | Protected access value for opening a shared item. |

<a id="record-comment"></a>

## Object comment

Retains a user's commentary against a typed business record.

**Storage** `comment`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `description` | text | No | — | Descriptive text associated with this entry. |
| `fk_user_author` | integer | Yes | `NULL` | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | `NULL` | Account recorded for the latest modification. |
| `fk_element` | integer | Yes | `NULL` | Target record identity. Where an object type accompanies it, both values identify the target. |
| `element_type` | varchar(50) | Yes | `NULL` | Type discriminator identifying the class of associated object. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `import_key` | varchar(125) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

<a id="record-object_lang"></a>

## Translated property

Stores a property value for a named object type, record and language.

**Storage** `object_lang`.
The primary key is `rowid`.
An additional unique key comprises `fk_object`, `type_object`, `property`, `lang`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `fk_object` | integer | No | `0` | Identifier of the business record holding these values. |
| `type_object` | varchar(32) | No | — | Object family that defines the translated property. |
| `property` | varchar(32) | No | — | Name of the object property being translated. |
| `lang` | varchar(5) | No | empty string | Language code under which this text or presentation is stored. |
| `value` | text | Yes | — | Translated value of the named property in the selected language. |
| `import_key` | varchar(14) | Yes | `NULL` | Identifier carried by an import operation for grouping or tracing imported rows. |

<a id="record-overwrite_trans"></a>

## Translation override

Supplies a local replacement for a translation key under the relevant language and entity.

**Storage** `overwrite_trans`.
The primary key is `rowid`.
An additional unique key comprises `entity`, `lang`, `transkey`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `lang` | varchar(5) | Yes | — | Language code under which this text or presentation is stored. |
| `transkey` | varchar(128) | Yes | — | Translation key whose displayed text is overridden. |
| `transvalue` | text | Yes | — | Local text supplied for the translation key. |

<a id="record-import_model"></a>

## Saved import layout

Stores a named mapping for repeating an import procedure.

**Storage** `import_model`.
The primary key is `rowid`.
An additional unique key comprises `label`, `type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `0` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | `0` | User account associated with this record. |
| `label` | varchar(50) | No | — | Display label for the record. |
| `type` | varchar(64) | No | — | Type. |
| `field` | text | No | — | Field selection stored by the saved exchange profile. |

<a id="record-export_model"></a>

## Saved export layout

Stores a named selection or layout for recurring data exports.

**Storage** `export_model`.
The primary key is `rowid`.
An additional unique key comprises `label`, `type`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | Yes | `0` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `fk_user` | integer | No | `0` | User account associated with this record. |
| `label` | varchar(50) | No | — | Display label for the record. |
| `type` | varchar(64) | No | — | Type. |
| `field` | text | No | — | Field selection stored by the saved exchange profile. |
| `filter` | text | Yes | — | Filter settings saved with the export selection. |

<a id="record-webhook_target"></a>

## Outbound event target

Configures a destination, matching event codes and whether delivery failure should block the caller.

**Storage** `webhook_target`.
The primary key is `rowid`.

The stored state codes are `0` draft, `1` validated, `1` automatic trigger, `2` manual trigger, `9` canceled.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `entity` | integer | No | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `ref` | varchar(128) | No | — | Business reference used to identify the document or master record. |
| `label` | varchar(255) | Yes | — | Display label for the record. |
| `type` | integer | No | `0` | Delivery failure policy for the target, including whether a failure is blocking. |
| `description` | text | Yes | — | Descriptive text associated with this entry. |
| `note_public` | text | Yes | — | Note intended for external-facing output where the document model includes it. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `fk_user_modif` | integer | Yes | — | Account recorded for the latest modification. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | No | `0` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |
| `url` | varchar(255) | No | — | Web address or navigation target. |
| `connection_method` | varchar(255) | Yes | — | Authentication mechanism configured for outgoing webhook requests. |
| `connection_data` | varchar(255) | Yes | — | Authentication parameters required by the selected connection method. |
| `trigger_codes` | text | Yes | — | Set of business events this target subscribes to. |

<a id="record-webhook_history"></a>

## Outbound delivery attempt

Records what event was sent to which target and the outcome retained for subsequent investigation.

**Storage** `webhook_history`.
The primary key is `rowid`.

The stored state codes are `1` success, `-1` error.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `trigger_code` | varchar(128) | No | — | Event that caused the delivery. |
| `trigger_data` | text | No | — | Payload retained for the delivery attempt. |
| `fk_target` | integer | No | — | Endpoint identity. Interpret it with its source or target type for a polymorphic relation. |
| `url` | varchar(255) | No | — | Web address or navigation target. |
| `error_message` | text | Yes | — | Error message received. |
| `note_private` | text | Yes | — | Internal note for users handling the record. |
| `date_creation` | datetime | No | — | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `fk_user_creat` | integer | No | — | Account recorded as creator or author. |
| `import_key` | varchar(14) | Yes | — | Identifier carried by an import operation for grouping or tracing imported rows. |
| `status` | integer | No | `1` | Lifecycle state of this record. Numeric values are specific to the owning workflow. |

<a id="record-oauth_token"></a>

## Delegated authorisation token

Stores the provider-specific token data and identities attached to a delegated connection.

**Storage** `oauth_token`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `service` | varchar(36) | Yes | — | Provider or credential family used to interpret the token. |
| `token` | text | Yes | — | Legacy storage. Use the current business representation described for the owning record. |
| `tokenstring` | text | Yes | — | Credential material in the representation expected by its provider. |
| `tokenstring_refresh` | text | Yes | — | Provider-specific material used to refresh an expiring credential. |
| `expire_at` | datetime | Yes | — | Time after which the credential expires. |
| `state` | text | Yes | — | Provider-dependent scope or state data associated with the credential. |
| `fk_soc` | integer | Yes | — | Third party associated with this record. |
| `fk_user` | integer | Yes | — | User account associated with this record. |
| `fk_adherent` | integer | Yes | — | Association member identity. |
| `restricted_ips` | varchar(200) | Yes | — | Network addresses permitted to use this credential. |
| `datec` | datetime | Yes | `NULL` | When the row was created. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `entity` | integer | Yes | `1` | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
| `lastaccess` | datetime | Yes | — | Most recent access recorded for this credential. |
| `apicount_previous_month` | bigint unsigned | Yes | `0` | Number of accesses recorded for the preceding monthly bucket. |
| `apicount_month` | bigint unsigned | Yes | `0` | Number of accesses recorded in the current month. |
| `apicount_total` | bigint unsigned | Yes | `0` | Cumulative recorded accesses for this credential. |

<a id="record-printing"></a>

## Printer association

Associates a printer, driver and copy count with a module and user.

**Storage** `printing`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `tms` | timestamp | Yes | `CURRENT_TIMESTAMP` | Timestamp maintained when the stored row changes. |
| `datec` | datetime | Yes | — | When the row was created. |
| `printer_name` | text | No | — | Name used to identify the configured printer. |
| `printer_location` | text | No | — | Physical or organisational location assigned to the device. |
| `printer_id` | varchar(255) | No | — | Device identity supplied to the print service. |
| `copy` | integer | No | `'1'` | Number of copies requested for a print submission. |
| `module` | varchar(16) | No | — | Feature or extension to which this entry belongs. |
| `driver` | varchar(16) | No | — | Configured print backend for the device. |
| `userid` | integer | Yes | — | User whose printer configuration is being stored. |

<a id="record-printer_receipt"></a>

## Receipt printer

Defines a receipt printer available to the sales terminal.

**Storage** `printer_receipt`.
The primary key is `rowid`.
An additional unique key comprises `name`, `entity`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `name` | varchar(128) | Yes | — | Name under which this record is presented or identified. |
| `fk_type` | integer | Yes | — | Named type selected from the relevant dictionary. |
| `fk_profile` | integer | Yes | — | Receipt printer configuration profile. |
| `parameter` | varchar(128) | Yes | — | Setting value used with the receipt printer profile. |
| `entity` | integer | Yes | — | Organisational entity owning or scoping this row. Sharing rules depend on record type. |

<a id="record-printer_receipt_template"></a>

## Receipt layout

Stores the named receipt format for an entity.

**Storage** `printer_receipt_template`.
The primary key is `rowid`.

| Field | Stored type | Null allowed | Declared default | Meaning |
| --- | --- | --- | --- | --- |
| `rowid` | integer (generated) | No | — | Internal row identifier. |
| `name` | varchar(128) | Yes | — | Name under which this record is presented or identified. |
| `template` | text | Yes | — | Template contents used to render the printed receipt. |
| `entity` | integer | Yes | — | Organisational entity owning or scoping this row. Sharing rules depend on record type. |
