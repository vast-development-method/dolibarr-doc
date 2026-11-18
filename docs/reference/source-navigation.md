# Find the release evidence behind a workflow

Start with the operator task. The wiki names the feature as it appears in the application. The class reference shows its related operations and inherited behavior. The last column identifies the implementation path and line at the pinned revision. The 24.0 class reference identified its release as **24.0.3** on 18 November 2026. Its branch URL and the wiki can change as releases are published. [User documentation index](locators/reference.md#ref-1a9793c85089) · [Doxygen 24.0 index](locators/reference.md#ref-352461dedf3f) · [Release baseline](../baseline.md)

## Trading, cash and production

| Operator task | Official user guide | Doxygen class | Pinned 24.0.3 implementation |
| --- | --- | --- | --- |
| Register a customer or supplier | [Third parties](locators/reference.md#ref-1f038a43f982) | [Societe](locators/reference.md#ref-1476bf4973ff) | [Create the party](locators/reference.md#ref-2b4b39fa416c) |
| Validate a customer order | [Sales orders](locators/reference.md#ref-59440c23d218) | [Commande](locators/reference.md#ref-b16d24c7d6e4) | [Validate the order](locators/reference.md#ref-e5cbb396f782) |
| Approve supplier commitments | [Purchase orders](locators/reference.md#ref-cd56b5bb389c) | [CommandeFournisseur](locators/reference.md#ref-1a6083cebed4) | [Approve the purchase order](locators/reference.md#ref-5336406570d8) |
| Receive or issue stock | [Stocks](locators/reference.md#ref-12c0ebbd93ce) | [MouvementStock](locators/reference.md#ref-396752fcde2e) | [Issue and receipt entry points](locators/reference.md#ref-f637e7749c70) |
| Validate an invoice | [Customer invoices](locators/reference.md#ref-07f1d5ed7e3b) | [Facture](locators/reference.md#ref-a895172fafc9) | [Validate the customer invoice](locators/reference.md#ref-07006bf93cec) |
| Inspect an account movement | [Banks and cash](locators/reference.md#ref-99e1649c65ee) | [Account](locators/reference.md#ref-32d0a2d40f9e) | [Add a bank line](locators/reference.md#ref-69f85ba0b6cb) |
| Record a ledger entry | [Double-entry accounting](locators/reference.md#ref-5415216013fc) | [BookKeeping](locators/reference.md#ref-f74caaa01894) | [Create the entry](locators/reference.md#ref-068f5fb03b9f) |
| Estimate material and service costs | [Bill of materials](locators/reference.md#ref-7c48a5b3bb1d) | [BOM](locators/reference.md#ref-d271916c305b) | [Calculate batch and unit cost](locators/reference.md#ref-3ad29baef801) |
| Plan a production run | [Manufacturing orders](locators/reference.md#ref-d38a5a4eeb1d) | [Mo](locators/reference.md#ref-fc381544a793) | [Expand BOM components](locators/reference.md#ref-34c5dc24a74d) |

## Projects, services, people and administration

| Operator task | Official user guide | Doxygen class | Pinned 24.0.3 implementation |
| --- | --- | --- | --- |
| Determine who may read a project | [Projects](locators/reference.md#ref-4764ec6a4765) | [Project](locators/reference.md#ref-f0b82230890a) | [Evaluate project access](locators/reference.md#ref-d9dce159c80c) |
| Manage a service contract | [Contracts](locators/reference.md#ref-b899e4e0c73e) | [Contrat](locators/reference.md#ref-13b06688a2be) | [Validate the agreement](locators/reference.md#ref-bec92ac564d7) |
| Create a support request | [Tickets](locators/reference.md#ref-b947d9d46d62) | [Ticket](locators/reference.md#ref-d0006c1139fa) | [Create the ticket](locators/reference.md#ref-f3a46325df9e) |
| Approve a staff absence | [Leave requests](locators/reference.md#ref-4da7a57b0e7e) | [Holiday](locators/reference.md#ref-2d5d002d972d) | [Approve the request](locators/reference.md#ref-88c09de4e30a) |
| Approve an expense claim | [Expense reports](locators/reference.md#ref-f9ce480320f5) | [ExpenseReport](locators/reference.md#ref-cca58ef81667) | [Approve the report](locators/reference.md#ref-84bb1a5345d8) |
| Check membership coverage | [Membership](locators/reference.md#ref-3a7d887bb215) | [Adherent](locators/reference.md#ref-14e168893444) | [Refresh the member end date](locators/reference.md#ref-8717782528ee) |
| Assign participants to a calendar entry | [Agenda](locators/reference.md#ref-0577617120a9) | [ActionComm](locators/reference.md#ref-6db626bd168c) | [Create the event and its assignments](locators/reference.md#ref-4b45981346dd) |
| Inspect resources attached to an event | [Resources](locators/reference.md#ref-1e7147efda7b) | [Dolresource](locators/reference.md#ref-5dd77cca2382) | [Fetch resource associations](locators/reference.md#ref-8f7e7e6a95b8) |
| Review a scheduled operation | [Scheduled jobs](locators/reference.md#ref-c29dbd6a070a) | [Cronjob](locators/reference.md#ref-b82fa0ad8e52) | [Run one attempt](locators/reference.md#ref-1966948f2214) |
| Verify a signed event | [Unalterable archives](locators/reference.md#ref-c3dd1694f582) | [BlockedLog](locators/reference.md#ref-f97f3823821e) | [Verify a record signature](locators/reference.md#ref-deeca07aa9b3) |

**A verified documentation difference.** The Resources wiki's module information box lists module ID 0. The 24.0.3 resource descriptor declares **63000**. Use the descriptor and the [module inventory](../coverage/modules.json) when mapping installation IDs. For the booking conflict rule, follow the resource assignment screen: it performs the overlap check before adding the relationship. Looking only at the resource class would miss that caller-level rule. [Wiki module information](locators/reference.md#ref-1e7147efda7b) · [Descriptor](locators/reference.md#ref-d0c271df2f34) · [Assignment and overlap check](locators/reference.md#ref-ff92d470b528)
