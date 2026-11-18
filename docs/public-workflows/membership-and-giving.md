# Applying for membership, renewing and giving

A visitor can apply for membership, pay dues against a known member or pledge a donation. The application owns identity and membership type, a subscription owns a period of cover, and a donation owns the donor's stated gift. The same name and email can legitimately occur in all three. Use the identity returned by the relevant form when continuing into payment.

## New applicant or returning member

The membership module and public enrollment setting must both be enabled. The public member directory has a separate setting. In a multi-organization installation, the registration page selects the requested organization before it loads settings and processes the application.

When the option to search existing members is active, submitting the form first tries to recognize a validated member within the applicable membership entities. Each matching strategy requires exactly one result.

| Search order | Input and scope | Business result of a unique match |
| --- | --- | --- |
| 1. Member login | Login is used when member logins are required and a login has been supplied. | Offer a dues payment against the matched member. |
| 2. Organization | Organization applicant, linked party name and member email. | Offer a dues payment against the member linked to that party. A free-text company name on an unlinked member does not establish the relationship used in this search. |
| 3. Individual | Given name, family name and member email for a natural person. | Offer a dues payment against that individual. Email alone is insufficient. |

The matching step presents a confirmation. At this point the original member has no new subscription and no second application has been written. An ambiguous strategy does not select an arbitrary row. A visitor who continues with a new application must still satisfy the ordinary creation rules. A draft applicant falls outside the validated-member lookup. A repeat application is therefore **not** a general retry mechanism for recovering a pending application.

## Application fields and outcome

| Input or setting | Rule at application |
| --- | --- |
| Nature and identity | Natural persons supply given and family names. Legal persons supply an organization name. The form recognizes those two natures. |
| Type | A positive type is required. With ordinary selection it must be one of the active choices. A configured fixed type supplies the stored membership type. The stored nature can also be fixed by setup. |
| Country | Country is required. A configured fixed country takes precedence over the selected country. |
| Login policy | When logins are required, creation requires an email, an unused login and a matching pair of nonempty passwords. Optional birthday components must describe a usable date when a birth month is supplied. |
| Profile | The applicant supplies contact and postal details and can supply a private note, photo and birthday. With directory publication enabled, the public checkbox records the visitor's choice. |
| Linked party | An optional setting creates a business party from the new member. A failure in this step contributes to failure of the application transaction. |

Successful creation stores a **draft member** (−1). Where a member email and usable enrollment template are available, it can send the member a notice with additional text from the type. An independently configured organization email can notify staff. Notices are attempted during processing. Their delivery is distinct from the commit, and inability to deliver the notification does not itself cancel a successfully written member.

For ordinary completion the form uses an explicit return destination, then the configured post-enrollment destination, then the built-in acknowledgment. Online dues collection overrides these destinations. It sends the member reference and entered amount to the payment service and can restrict the method to the one selected in configuration. It compares the entered amount with the greater of the general minimum and the type minimum. An amount below that result causes rollback. Entering 25 with a general minimum of 20 and a type minimum of 30 therefore fails even though 25 meets the general minimum. A committed application followed by an abandoned checkout remains a different event from a failed application.

For the subscription period and the later payment operation see [Member renewals and collections](../specification/people-and-services/member-renewals-and-collections.md) and [Payment allocation by source](../specification/channels/payment-to-order-membership-and-event.md).

## Public directory and detail

The directory list selects the requested entity, validated membership state (1) and the public flag. Its columns are name, company, email, postal code, town and photo. It does not join subscription periods to test paid-through dates. A validated, publicly listed member with a lapsed subscription can therefore still appear. A newly saved draft who selected public visibility does not yet qualify for the list. Staff validation and the applicant's publication choice serve independent purposes.

The public detail view honors the member's public flag and shows the membership type, nature, names, gender, company, complete postal address, country, email, birthday, optional photo and public comments. The application comment field goes into the private note. Storing a comment there does not supply the displayed public comment. Directory viewing has no effect on member approval or coverage.

## Public gifts and project attribution

The donation module and its separate public-form setting must be enabled. A valid nonempty email is checked if supplied. The submission requires an amount and rejects a value below the configured minimum. The standard page shows the amount field when the online-payment setting has a nonempty value. Its default display takes the greater of zero, the current input and the configured minimum. In particular, the disabled-method sentinel (−1) still displays the amount field and suppresses the checkout handoff.

The form records a draft donation with the time of submission, donor names and company text, postal details, country and region identifiers, email, stated amount, publication choice, private comment and applicable extra attributes. A project-specific form shows the title of the resolved project and preserves its identifier on the draft when projects or event organization are enabled. Donor text is held directly on the gift. This creation path does not create a customer, member, dues period or donor receipt. A further successful pledge by the same donor creates another gift.

After writing the draft, the form can continue to a return page or a local acknowledgment. With an online method selected, the handoff uses the **donation identifier**, optionally the donor email and method. Collection is a later operation. The online payment handler uses the received amount, payment type, currency and external transaction reference. The donation payment here supports the organization currency. Where configured, it also posts the payment to the selected bank account. The donation identifier links the payment to the pledge even when the donor has no linked customer account.

For example, on a project appeal with a minimum of 10, a pledge of 40 without a completed checkout contributes one draft gift for 40 to that project's records and zero payment rows. A later successful collection can create one payment linked to the same gift. A donor certificate is generated by a separate document operation. An acknowledgment page, bank entry and certificate answer three different questions.

For the certificate's source amount and fields see [French donation receipt](../regional-reporting/french-donation-receipt.md).
