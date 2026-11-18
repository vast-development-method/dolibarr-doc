# Campaign mail, event notifications and incoming email

A campaign selects a population and records progress for each address. An event notification resolves recipients when a business event occurs. An email collector consumes an incoming mailbox and applies business actions to selected messages. Each has a different unit of work and recovery boundary.

## Campaign delivery

A campaign stores its entity, author and validator, subject, body, sending identity, reply and error addresses, and status. Each target has its own address, campaign, optional source record and source type, tracking tag, send date, status and error text. The database enforces one address per campaign. The same address can participate in two campaigns. [Target table](../reference/locators/communications.md#ref-8c9477f8434b) · [Target key](../reference/locators/communications.md#ref-8bdd9ed0234a) · [Operator guide](../reference/locators/communications.md#ref-fa95d290ef0f)

| State or decision | Behaviour |
| --- | --- |
| Draft (0) | A creator prepares content and the target population. Creation, validation and deletion are separate permissions. Advanced permissions add recipient inspection, manual sending and deletion after validation/sending. The web UI checks the configured sending limit. |
| Validated (1) | Validation records its timestamp and actor. The sending form offers dispatch on a validated or partially sent campaign with recipients. |
| Partial (2) or complete (3) | On the manual path select target status below 1, prioritising pending (0) before errors (−1). Process up to the web batch limit. A transport success records sent (1) with a send date. Failure records error (−1), a date and diagnostic text. A batch with a failure or remaining candidate rows produces partial; one that successfully processes all its candidate rows produces complete. |
| Read (2) or unsubscribed (3) target | These are target statuses, independent of the campaign's aggregate status. A verified unsubscribe request updates target tracking, marks a linked contact as opting out and records the address in the entity unsubscribe table. |

[Campaign and target states](../reference/locators/communications.md#ref-64ef89c0fac9) · [Validation](../reference/locators/communications.md#ref-12e84939b47c) · [Manual action availability](../reference/locators/communications.md#ref-8036c3878b5f) · [Recipient selection](../reference/locators/communications.md#ref-26deb5cc0246) · [Delivery results](../reference/locators/communications.md#ref-5b570969612f) · [Unsubscribe](../reference/locators/communications.md#ref-432c0b5dd262)

**Acceptance.** On a validated campaign with three pending targets, give the manual sender a batch limit of two. Let the first send succeed and the second fail. Expect one sent, one error and one pending target and a partial campaign. On the next ordinary run, pending precedes error and the sent target is excluded. An external handoff can succeed before the local row update fails, so the stored status alone cannot prove exactly-once delivery. [Recipient observation schema](../../schemas/communications/mailing-target.schema.json) · [Delivery failure example](../../examples/communications/mailing-target--transport-error.json)

## Business-event notifications

The notification module's global setup requires an administrator. When a supported event occurs (such as customer invoice validation, customer order validation or expense approval), the trigger checks module activation and the supported-event list, then calls the notification sender. The global setup list also checks the event's owning module. The recipient preview can resolve subscriptions for active third-party contacts, users and globally configured destinations, and tracks whether the resulting email address is valid. The same trimmed address is a single key in that preview. The trigger returns a negative send result to the originating operation, so an operation that rolls back on trigger failure can abort. Mail already delivered outside the database remains a separate effect. [Admin access](../reference/locators/communications.md#ref-c000fc389dbe) · [Event handling](../reference/locators/communications.md#ref-ee6772add06e) · [Event catalogue](../reference/locators/communications.md#ref-fd70bfffd84f) · [Recipient resolution](../reference/locators/communications.md#ref-e9a37feb9d0c)

**Acceptance.** Subscribe an active customer contact to an order event for its own organisation. Preview the event for that organisation and check the contact's address. Repeat for a different organisation with no other subscriptions and expect the first organisation's subscription to be absent. Disable Notification and a supported event returns without attempting a send. An unsupported event also returns without dispatch.

## Incoming mailbox to ticket

| Configuration or stage | Rule and effect |
| --- | --- |
| Collector setup | An administrator defines an entity-scoped collector with mailbox, source folder, optional destination, maximum successful messages per collection, active flag, filter records and action records. Core registers a scheduled job with a five-minute interval. Actual execution requires the scheduler to run. |
| Select messages | The scheduled service asks for active collectors. An individual collector loads its filters and action records. Actions carry type, parameters, status and position and are loaded in position order. Filters and mailbox settings govern message selection. |
| Apply business actions | Supported branches include resolving/creating a third party, resolving/creating a contact, recording an agenda event, storing an attachment, or creating a project, support ticket or recruitment application. A ticket action attempts to identify an existing ticket through existing object context, ticket identity, tracking ID or message ID. A match converts the action to recording a message against the existing ticket. |
| Commit and acknowledge | Production commits business writes for each successful message. An action error rolls back that message. Test mode can execute business writes then roll them back; the lighter test mode skips the action-write loop. Successfully processed messages targeting another folder are queued for a later mailbox operation. A collector run reports per-collector results and aggregates errors. |

[Admin setup](../reference/locators/communications.md#ref-73795580a664) · [Scheduled job](../reference/locators/communications.md#ref-24419f70a034) · [Action order](../reference/locators/communications.md#ref-0d50aee14b64) · [Active collection](../reference/locators/communications.md#ref-e793d8bff2a6) · [Ticket correlation](../reference/locators/communications.md#ref-4ea999c0faf6) · [Message transaction and mailbox finalisation](../reference/locators/communications.md#ref-9916baa9d416)

**Acceptance.** Process an allowed message on a ticket-enabled collector with no matching ticket. Expect the ticket action to create one when required fields and dependencies are satisfied. Supply a reply carrying that ticket's tracking information. Expect a new event on the existing ticket. Fail a later action within a message's database transaction and verify rollback for that message. A mailbox move and its database commit occur at different times; reconciliation should inspect both before replaying a failed move.

## Social profiles on parties and contacts

The SocialNetworks module directs administrators to the social-network dictionary. A contact stores its network-to-profile values as a map. Contact reads decode that map, and an edit can propagate revised profiles to a linked user along with other synchronised properties. A third party has its own profile map. These stored addresses are contact attributes; they do not imply delivery of a campaign or subscription to an event. [Module setup](../reference/locators/communications.md#ref-1c6f4d9408a8) · [Contact synchronisation](../reference/locators/communications.md#ref-46e96b1afd13) · [Party persistence](../reference/locators/communications.md#ref-e937cb58c890)
