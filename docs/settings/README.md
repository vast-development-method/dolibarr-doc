# Business setup decisions

This catalogue covers **47 operator settings on 14 setup screens** in release 24.0.3. Each setting has a visible control, at least one identified business operation that reads it, and a description of its observable effect. The chapters name module prerequisites, choices, declared initial values and read-time defaults where established. A company can override defaults. Each field's stored name serves as a locator for the pinned implementation.

| Business question | Settings | Setup screens |
| --- | ---: | --- |
| [Which defaults apply to a party, contact, sales pack or purchase line?](parties-and-catalogue.md) | 6 | Third parties and products |
| [Which policies govern quotations, orders, dispatch and supplier approvals?](commercial.md) | 16 | Customer proposals, customer orders, shipments, supplier orders and supplier price requests |
| [How are invoices issued, work billed in stages and payments reported?](billing-and-payments.md) | 11 | Customer invoices, progress invoices, customer payments and supplier payments |
| [When do projects close, expenses qualify and leave balances change?](projects-and-workforce.md) | 14 | Projects, expense reports and leave |

Settings can act at four different times. A **default** supplies a value on a new record or form. An **admission rule** permits or blocks an attempted action. A **posting policy** decides when an accepted event affects a balance. A **presentation policy** changes the report or outward document generated from stored data. For example, a default supplier pack size affects line quantities, an expense period restriction affects saving a line, monthly leave deductions affect the entitlement ledger, and grouping payments affects the report.

The counts cover the controls named in these four chapters. Other settings for the same modules, further setup screens, installation overrides, third-party extensions, hidden constants and experimental options are outside this catalogue. [Company configuration](../policies/company-and-settings.md) describes how settings resolve across entities. [Stock posting decisions](../policies/stock-posting-decisions.md) describes which business event posts a movement.
