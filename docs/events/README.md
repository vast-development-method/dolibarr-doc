# Business events and their consumers

An order can move from approved to fulfilled while the linked proposal, customer invoice, warehouse balance and bank ledger are each at a different stage. An event carries the **specific decision that just occurred** to other modules. The original record retains its own state; a receiving module chooses whether to create, annotate or classify a different record.

## Event families

| Catalogue | Business question |
| --- | --- |
| [Parties, trade and service documents](trading.md) | Which event follows offer acceptance, order validation, receipt, shipment or contract modification? |
| [Cash, billing and accounting](finance.md) | Which record changed when an invoice, payment, credit, asset or ledger movement was posted? |
| [Production, projects and stock](operations.md) | Which signal describes a task, a bill of materials, production actuals or a stock movement? |
| [People, membership and support](people-and-service.md) | Which event describes a leave decision, claim, ticket, employment record or membership payment? |
| [Other shared records](other.md) | Which changes concern categories, documents, subscriptions to messages or general associations? |

The catalogue covers the 161 named entries in the standard event dictionary and additional literal emissions in the surveyed business classes and shared action handlers. Together they identify 371 distinct codes. A dictionary entry establishes a name offered to setup. A direct emission site identifies an operation that actually sends the name. Generic create/update/delete paths can construct an event name from the object type at runtime. A blank emission site means the catalogue does not assign that code to a literal call. Extension-defined names and every dynamically assembled code are outside this count.

## What reaches the next module

| Part of the contract | Meaning |
| --- | --- |
| Event name | Identifies a business transition at the originating operation. Creation, validation, settlement and deletion are separate events even for one invoice. |
| Object | Carries its identity, current fields and any context supplied by the caller. An old copy, origin ID, signed-online flag or prepared message is available only where the caller provides it. |
| Actor, language and effective configuration | Determine accountabilities, translated labels and which subscribers apply. A service-account transition can produce different follow-on access from an employee action. |
| Subscription | A handler can apply to all events or be associated with an enabled module. More than one handler can receive the same event. |
| Outcome | A negative handler outcome is collected. The dispatcher can continue to later handlers and returns a negative failure count when any failed. A domain operation that chooses to propagate that failure can roll back its transaction. |

An automatic calendar record is one possible consumer. It ignores activity events with the `ACTION_` prefix to avoid recursively creating activities. Other codes must have the corresponding automatic-agenda option enabled. The handler also has a draft-modification guard on eligible object types, dedicated cases for common documents and a generic fallback. It builds a label, note, owner and applicable document/party relationships, then creates an activity. The absence of a dedicated branch does not preclude this generic handling.

A notification subscription is a separate decision. The notification handler tests its module, a list of supported event codes and applicable recipient subscriptions. Extensions can contribute support. An event listed as notification-eligible still requires a matching recipient. A webhook instead matches configured target, event and mode, performs the outbound request and records its outcome. Delivery can precede the final commit of the originating operation. A record receiver needs its own durable identity for any payment, stock or fulfilment consequence.

## Where to read a subscriber reference

Paths in the event-family tables start below the release's `htdocs/` directory. The dictionary line is in `install/mysql/data/llx_c_action_trigger.sql`. The numbered subscriber locators refer to these files:

| Key | Implementation |
| --- | --- |
| Workflow | `core/triggers/interface_20_modWorkflow_WorkflowManager.class.php` |
| Agenda | `core/triggers/interface_50_modAgenda_ActionsAuto.class.php` |
| Notification | `core/class/notify.class.php`, the built-in supported-event list |
| Dispatcher | `core/class/interfaces.class.php`, `run_triggers` |
| External delivery | `core/triggers/interface_95_modWebhook_WebhookTriggers.class.php`, `runTrigger` |

The [commercial automation decisions](commercial-automation.md) describe specific effects with their eligibility, totals, linked records and failure conditions.
