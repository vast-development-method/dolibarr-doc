# How an operation is authorised

A permission declaration identifies a capability. The decision to use it also depends on the acting account, the requested record, its business relationships, the current entity, the operation and sometimes the document's state. These six worked examples trace the interactive and service paths. The [permission catalogue](README.md) lists the module declarations. The [record dictionary](../records/README.md) describes the identities on which the decisions depend.

## From declaration to decision

The installation assigns a numeric ID to a permission definition. For example, customer orders declare 81 for reading, 82 for creating and 84 for advanced validation. The account loader reads grants assigned directly to the user, then grants assigned through the user's groups. It joins the assignments to the permission definitions in their applicable entity context. Business operations ask for named capabilities such as `commande.order_advance.validate`. A grant on an unrelated account, permission family or entity does not take part in that decision.

The interactive resource guard takes the requested feature, the loaded object or ID, and where necessary the table or relationship that establishes the owner. The service resource guard delegates to the shared object-access decision for the authenticated account. The data set used to list records can have its own selection conditions. A workflow may then check the actor again when changing a document. Three different outcomes follow from this arrangement. A user can have a general capability and lack access to a particular record. A user can have access to read that record and lack the right to change it. An authorised operation can fail a business precondition even with every necessary grant.

## Third parties — find and open a customer

**Directory.** The screen starts with the external account's associated party when one exists. For an internal account without permission to see all third parties, the list requires a sales assignment between the party and that user. Entity selection applies before presenting the results. The service directory also requires third-party read permission. It uses the external account's own party or the internal salesperson's assignments as applicable. Customer, prospect, supplier and category selections further narrow the directory.

**Card.** Loading the master record supplies the party identity. The interactive card passes the resulting ID to the third-party resource guard. The service's single-record operation checks the named read capability, fetches the requested party, then decides access to the resolved party before returning its information. A lookup by an alternative business identifier still resolves to a party record.

**Acceptance example.** Two active customers belong to the selected entity. An internal salesperson has directory read permission, lacks the all-customers permission and is assigned only to the first customer. The unfiltered directory contains the first customer only. An external customer account using the directory is scoped by its linked party.

## Customer orders — validate an order

**Screen.** The order card resolves its identifier, including lookup by reference, and applies the order resource guard to that ID. In ordinary permission mode, creation grants the validation action. With advanced permissions enabled, the screen evaluates the distinct order-validation grant. The confirmation passes the acting user and selected warehouse to the order operation. Where configuration moves stock at order validation and the lines qualify, the screen requires a warehouse. Generating a deposit invoice during confirmation also requires an eligible payment term and invoice-creation authority.

**Service and workflow.** Service validation first requires order creation, fetches the order and checks access to that particular order. The order operation applies the validation rule for the configured permission mode. Under advanced mode both the service entrance and the workflow condition must succeed. The operation recognises a previously validated order, requires a customer and, subject to configuration, verifies the sale status of referenced products. It begins the validation transaction and raises the order-validation event in the normal trigger-enabled path.

**Acceptance example.** In advanced mode a clerk can create a draft for an accessible customer while still lacking order-validation authority. Granting advanced validation makes a valid order eligible. A repeated validation of an already validated order yields no new validation. The optional deposit invoice has its own accounting-domain permission.

## Customer invoices — issue a draft

**Screen and service.** The invoice card evaluates its own resource scope and derives the validation capability from invoice creation in ordinary mode or the invoice-specific validation right in advanced mode. The confirmation calls the invoice workflow. Service validation requires invoice creation, fetches the invoice, verifies access to that record, and passes the actor to the same workflow. Order validation grants have no role in this invoice decision.

**Business preconditions.** The operation reloads the party and lines, requires draft state and at least one line, and evaluates the invoice validation grant for the active permission mode. Settings can impose additional restrictions on chronological numbering and mandatory customer details. Under the date-on-validation option, a provisional invoice takes the validation date and its payment due date is recalculated. Successful validation normally emits the invoice-validation event.

**Acceptance example.** An authorised issuer submits a draft without lines. Issuance fails and the draft remains available for editing. After adding a valid line and satisfying the applicable customer and numbering rules, the same issuer can validate it. Submitting an already issued invoice returns a no-change outcome. Payment and settlement remain separate operations.

## Employee expenses — create a claim for another person

**Screen.** The acting account and the employee whose expenses are claimed are separate identities. The form uses the account's reporting hierarchy, including the actor, to determine whose claims it can ordinarily edit. The create permission is required. With advanced permissions enabled, the write-everyone grant can expand the set of employees. Existing-report visibility also has a path for the designated validator holding approval permission. That assignment serves a different purpose from the manager-to-employee relationship.

**Service and record.** Service creation applies the creation grant and checks the requested employee against the actor, reporting hierarchy and advanced write-everyone exception. It reserves workflow-controlled fields for their dedicated transitions. The business operation requires the beginning and end of the claim period. When an employee is omitted, the acting user becomes the claimant. On storage, the creator is the acting user, the claimant is the employee, and the designated validator has a separate field. Approval records the actual approving user and its date.

**Acceptance example.** A manager with the create grant files a claim for a subordinate. The record preserves the manager as creator and the subordinate as claimant. Another employee outside the manager's hierarchy is outside ordinary creation scope. In advanced mode an account granted both creation and write-everyone can create that claim. A designated validator with approval authority can review the assigned claim without becoming its claimant.

## Projects — open a public or assigned project

**Card decision.** After the general project resource check, the project card obtains separate read, write and delete decisions. For each mode, the project's decision method accepts the corresponding all-projects capability. It also accepts the ordinary capability for a public project. For a private project it examines active project contacts. An internal contact is matched by user ID. For an external account the method compares the account's party with the party of an external contact. The capability required still depends on the requested mode.

**Selection and service.** The core project selector scopes candidate projects to the permitted project entities. Its public-or-assigned selection includes public projects and projects linked to the user through an internal project contact type. The interactive directory uses this selector when all-project visibility is absent. The service list applies the user's scope and its third-party selection when applicable. Single-project service reads require project read permission and access to the resolved project. Public visibility means public within these applicable access boundaries.

**Acceptance example.** For an internal user with ordinary project read permission and no all-projects grant, compare one public project and two private projects in the allowed entity. Link the user to one private project as an internal contact. The public and assigned private projects enter the public-or-assigned selection. A user with only the read capability does not gain project editing through the assignment.

## Warehouses — inspect a historical movement

**Ownership.** A movement has a product, warehouse, signed quantity, movement type, date, author and optional origin. Its stock entity is determined through its warehouse. The warehouse on the movement establishes the ownership boundary even when the same product has stock in several entities.

**Screen and service.** The movement list enters the stock area and queries movements through warehouses in the stock sharing scope. The screen also calculates visibility of supplier-price information according to product or service configuration and advanced price permissions. The service collection requires stock read permission and joins the warehouse to select the eligible entities. An individual service read requires movement-read permission. It fetches the selected movement and passes the warehouse relationship to the shared resource decision before returning the result.

**Acceptance example.** Two warehouses stock the same product. Only the first warehouse's entity is in the actor's stock scope. A movement at the first warehouse is eligible for the historical list, while a movement at the second warehouse is outside that selection. A permitted detail request identifies the warehouse and signed quantity from the chosen movement. Visibility of supplier-price columns in the interactive list has its own decision.

## Inputs to preserve in an independent implementation

| Operation | Record-specific input | Grant or configuration that changes the decision | Observable result |
| --- | --- | --- | --- |
| Find a customer | Account's party or salesperson-to-party assignment | Read rights, all-customer visibility and party entity set | Eligible directory rows and individually accessible records |
| Validate an order | Resolved order, customer and eligible lines | Normal or advanced validation mode, stock trigger and deposit settings | At most one validation for the already-validated case, with eligible related operations |
| Issue an invoice | Invoice state, lines and bill-to party | Invoice validation mode, chronology and required customer fields | Issuance, no change on an issued invoice, or failure on invalid data |
| Submit a claim on behalf of an employee | Creator, claimant, reporting hierarchy and period | Create grant and advanced write-everyone exception | Draft claim preserving the two identities |
| Open a project | Public flag, project contacts, project entity | Ordinary read or all-project read | Read eligibility independent of write and delete |
| Read a stock movement | Warehouse on the movement | Stock entity scope, collection/detail capabilities, separate price-display policy | Historical movement for the permitted warehouse |
