# Counterparty consolidation and commercial exposure

The common party identifier connects CRM, sales, purchasing, banking and accounting. A customer that is also a supplier can have different order minimums, payment history, discounts and commercial codes for the two roles. Consolidating a duplicate party changes where those records are found. It does not itself extinguish an outstanding balance.

## Direction and authorization of a merge

A merge names the party to **keep** first and the party to **retire** second. Both must exist and the operator needs party creation rights and access to each record. The same identifier supplied twice is a bad request. Missing records and denied access have different error responses. Success returns the surviving party. Replaying a previously completed request with the same retired identifier fails lookup. External clients holding the retired identifier need the identity of the survivor.

| Attribute or relationship | Resolution |
| --- | --- |
| Customer, prospect and supplier roles | Combine the customer/prospect role bits and the supplier role flags so the surviving record retains both parties' roles. |
| Identity, addresses, financial defaults | The survivor supplies the primary name. Empty values in an explicit list inherit from the retired record. The list includes postal and communication details, professional and VAT identifiers, trade terms, sales and supplier discounts, price level, credit limit, both order minimums, payment defaults for purchasing, commercial and accounting codes and preferred language. |
| Empty numeric values | Numeric zero counts as empty in the inheritance operation. If the survivor has a zero credit limit and the retiring party has 2,500, the survivor receives 2,500. A company type of −1 is also replaced. |
| Alias | Inherit the retiring alias if the survivor's is empty. If the alias remains empty and the names differ, the fallback assigns the **survivor's own name** to the alias. The retired party's name is separately available in the merge event. |
| Notes and custom fields | Append public to public and private to private, survivor first. For individual custom fields copy the retiring value only when the survivor's value is empty. |
| Classification and hierarchy | Combine category assignments separately for customers and suppliers. With parent-company handling enabled, reassign the retired party's direct children to the survivor. |
| Sales representatives | Resolve duplicate assignments for the same representative before redirecting the retiring assignments. The survivor retains one relationship to each representative. |

If a customer code, supplier code or barcode collides between the two records, the merge clears all three identifiers on the retiring record before updating the survivor. This sequencing matters when the survivor inherits an identifier under a uniqueness constraint.

The merge delegates relationship replacement to each participating domain. The standard set covers contacts and activities, quotes, customer and supplier orders, invoices and recurring templates on both sides, shipments, receptions, contracts, projects, supplier product prices, members, bank accounts and several other records. Some areas, including manufacturing, service interventions, tickets, donations and partnerships, participate when their tables exist. Party-owned bank details, account references and discounts are redirected as part of the same process. An extension can handle its own relationships with the old and new identifiers.

A failed participating domain replacement or extension can roll back the business transaction. Before deletion the survivor emits a company-modified event carrying the origin identifier and name. The operation deletes the retired party through the normal deletion routine and attempts to move its documents under the survivor's directory using their relative paths. Individual filesystem moves are not checked as a group before database commit. A successful response confirms the party consolidation. Attachment availability must be determined from the actual stored files.

## Measuring exposure after consolidation

The party's commercial aggregates can be requested for customers and suppliers. Each uses the party identity and the document type's permitted entities. A document reference in one projection can also appear as the source for another transaction. Adding quotation, order and invoice amounts indiscriminately would count successive stages of the same transaction several times.

| Measure | Included value |
| --- | --- |
| Quote or order net and gross totals | Sum the stored net and gross totals of all matching headers, including drafts. Return their references. |
| Quote or order “opened” | Sum the gross values of all matching headers whose status differs from draft. This includes other non-draft states, even a closed commercial document. The computation assigns no payment allocations to quotations or orders. |
| Invoice net and gross totals | Sum non-draft invoices except an abandoned invoice marked as replaced. Other abandoned invoices may remain in turnover totals. |
| Invoice “opened” | For an unpaid invoice outside draft, closed and abandoned states, start with gross and subtract payments allocated to the invoice, applied credit notes and applied deposits. Sum the resulting balances. |
| Supplier credit still available | For a converted supplier credit note, also subtract its unused credit amount. This can reduce overall supplier exposure and can produce a negative open value. |
| Late-only request | Restrict the invoice query to due dates strictly before the user's start of today. Invoices due today do not enter this projection. This date restriction also changes the net and gross totals and the references returned by the query. |

Three offers with gross amounts of 115 issued, 230 signed and 57.50 draft give a gross offer total of 402.50 and an opened offer value of 345. On an eligible invoice for 115, a payment allocation of 60, applied credit of 10 and deposit of 5 leave **40** opened. Receiving the remaining 40 can reduce the open invoice measure to zero without changing its invoiced turnover. On the supplier side, an unused converted credit of 12 reduces a payable exposure of 40 to 28.

The invoice response contains one reference map for the selected rows and a second for invoices whose calculated balance is nonzero. A closed or zero-balance invoice can appear only in the first. The customer-offer page displays open invoice exposure against a configured nonzero party credit limit and signals excess when the balance is **greater than** the limit. Equality does not trigger this display warning.
