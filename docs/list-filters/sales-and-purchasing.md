# Finding quotations, orders and invoices

A customer reference can identify a quotation, an order and an invoice for the same sale. Each list searches its own document and linked parties. The customer order list also searches an external system reference. The supplier invoice list distinguishes its internal reference from the supplier's invoice number. An operator reconciling a purchase invoice to a purchase order must therefore choose the reference field on each list independently.

This chapter describes the six standard register screens. The tables give the accepted request names so a reader can reproduce a selection. Field visibility, installed modules and configured extra fields determine which controls appear.

## Rows, party scope and free-text search

All six lists start with a document header and its owning third party. The permitted entities come from the sharing rules for that document family. A positive `socid` limits the rows to that party. At list entry an external user's linked party supplies this value. Optional joins provide the project, author and geographic labels. Invoices also join the assigned bank account. A party's parent is available as a separate linked party on customer orders and customer invoices.

| Register | Fields reached by standard `search_all` | Effect of matching multiple records |
| --- | --- | --- |
| Customer quotations | Document and customer references, public note, party name, alias, town, postal code and line description. Internal search adds the quotation private note. | Each search term can reach a matching line through an existence test. Several matching lines still yield one quotation. |
| Customer orders | Document and customer order references, public note, party name, alias, town, postal code and line description. Internal search adds the order private note. | A matching line qualifies the order. A second matching line does not create another header row. |
| Customer invoices | Document and customer references, public note, party name, customer code, alias, town, postal code and line description. Internal search adds the invoice private note. | An existence test qualifies the invoice by its lines. The recurring template joins only when its title is searched. |
| Supplier quotations | Document reference and public note from its searchable field definitions, plus party name, alias, town, postal code and line description. Internal search also includes the linked project's private note. | A free-text search joins the lines and requests distinct header rows. A positive internal-contact search also requests distinct rows. |
| Supplier orders | Document reference, supplier reference and both document notes from the searchable field definitions, plus party name, alias, town, postal code and line description. | Free text joins lines and displays distinct headers. The optional total count counts the joined rows, so an order with two matching lines can contribute two to the count and one to the displayed list. |
| Supplier invoices | Document reference, supplier reference, public note, supplier name and supplier code. Internal search adds the invoice private note. The full supplied search string is also tested as a substring of an invoice line description. | Matching lines qualify a header through an existence test. A positive internal-contact filter uses a direct join without distinct header selection. Two internal contact roles for the same user on one invoice can yield two rows. |

Ordinary multi-field text search supports a substring and can combine words across searchable fields. A supplier invoice's line-description branch tests the complete supplied string. For example, a description of “annual equipment maintenance” contains each of the words “annual maintenance” but does not contain that uninterrupted phrase. For that register the line alone will not satisfy this search string. On a customer order, separate terms may each match through a separate line on the same order.

## References, parties and responsibility

| Register | Document references | Party and project selectors |
| --- | --- | --- |
| Customer quotations | `sf_ref` takes precedence over `search_ref`. `search_refcustomer` searches the customer reference. | `search_societe` and `search_societe_alias` search party name and alias. A configured customer-code display also lets the party search match the customer code. `search_refproject` searches the project reference and `search_project` its title. |
| Customer orders | `search_id` matches a positive header ID. `search_ref` takes precedence over `sref`. `search_ref_ext` matches the external reference and `search_ref_customer` the customer's reference. | `search_company`, `search_company_alias`, `search_parent_name` use the order party and its parent. `search_project_ref` searches project reference and `search_project` its title. |
| Customer invoices | `sf_ref` takes precedence over `search_ref`. `search_refcustomer` searches the customer's reference. | Same party, parent and project controls as customer orders, plus `search_customer_code` for the party's customer code. |
| Supplier quotations | `sf_ref` takes precedence over `search_ref`. | `search_company` and `search_company_alias` use the supplier. `search_project_ref` uses the project reference. |
| Supplier orders | `search_ref` searches the internal reference and `search_refsupp` the supplier reference. | `search_company`, `search_company_alias` and `search_project_ref` work as on supplier quotations. |
| Supplier invoices | `sf_ref` takes precedence over `search_ref`. `search_refsupplier` selects the supplier's reference. `search_label` selects the invoice label. | `search_company` and `search_company_alias` use the supplier. Here `search_project` searches the project **reference**. |

When the alias column is hidden and a company-name search is supplied, the name control covers both legal name and alias. With separate visible columns each control searches its own attribute. `search_town`, `search_zip` and `search_state` search party town, postal code and the linked department/state name. `search_type_thirdparty` uses the party type identifier. On quotations and orders `search_country` selects the party's country identifier. On the two invoice registers it searches the country **code** and recognizes the following groups.

| Invoice country value | Comparison |
| --- | --- |
| `special_allnotme` | Country differs from the issuing organization's country. |
| `special_eec` | Country is in the configured European community country list. |
| `special_eecnotme` | Country is in that list after removing the organization's country. |
| `special_noteec` | Country is outside that list. A missing joined country does not satisfy a country-code inequality or membership test. |

Three roles can independently qualify a document. The author-name selector searches the creator's login, given name or family name. Its key is `search_login` on five lists and `search_request_author` on supplier orders. On customer invoices `userid` also filters by creator ID, with `-1` meaning an unset creator. A positive `search_user` instead requires a linked **internal contact** of the appropriate document type. `search_sale` selects an assigned sales representative of the **party**. A positive ID requires that representative and `-2` requires a party with no representative assignment. None of these three tests implies the other two.

List entry and document read rights apply separately. For example, the customer order query independently restricts an internal user without all-party visibility to parties assigned to them, with subordinate assignments included when enabled. Several other lists initialize the representative selector from the current user. The supplier order handler uses the external-party accessor in its internal-user initialization, which returns zero for an internal user. Its normal query therefore does not implement the customer order's independent representative/subordinate predicate. Overall access also depends on the module's read permission and party scope.

## Lifecycle and lateness

| Register | Status input and additional tests |
| --- | --- |
| Customer quotations | `search_status` tests membership in stored statuses. Empty and the single value `-1` omit this predicate. The active stages include draft (0), validated (1), signed (2), declined (3) and billed (4). `search_option=late` sets status to 1 and compares the validity end to the quotation closing warning cutoff. |
| Customer orders | `search_status` values −1 through 3 are canceled, draft, validated, shipment in progress and closed. With shipping disabled, selecting 1 includes 1 and 2. Virtual value `-2` includes 1 and 2 and `-3` includes 1, 2 and 3. `search_billed` independently compares the stored billed flag. `search_option=late` selects `-2` and checks the planned delivery date, falling back to the order date if delivery is unset. Disabling the delivery date makes order date decisive. |
| Customer invoices | `search_status[]` uses stored statuses. Common values are draft (0), validated and due for payment (1), closed (2) and abandoned (3). Closing can include a partial settlement with a closing reason. `search_dispute_status=0` includes both empty and zero dispute status. Other selected dispute codes use membership. `search_option=late` forces status 1 and compares the due date to the customer payment warning cutoff. |
| Supplier quotations | `supplier_proposal_statut` takes precedence over `search_status` when present and nonempty. Nonnegative selections test stored status, including draft (0), validated (1), signed (2), declined (3) and closed (4). The standard handler provides no late preset. |
| Supplier orders | `search_status` accepts an array or a scalar list. `statut` provides a fallback and, when explicitly supplied, adds a separate membership test alongside the resolved selection. `billed` independently selects the billed flag. `search_option=late` selects validated or approved (1, 2) using the **order date**. `recv_late` selects ordered or partially received (3, 4) using the **delivery date**. Both use the supplier order warning delay. |
| Supplier invoices | `search_status[]` accepts one or more status IDs and a scalar single-status fallback is provided. The standard selector offers draft (0), unpaid (1) and paid (2). The stored abandoned status (3) can be requested explicitly. `search_option=late` forces status 1 and checks the due date against the supplier invoice warning cutoff. |

All these late presets compare the relevant date **strictly before** the cutoff of current time minus the warning delay. An ordinary upper date bound instead uses an inclusive comparison. On invoices the late preset applies the header status and contractual due date. It does not calculate the amount outstanding from individual payments.

## Date fields and inclusive endpoints

The table gives a date prefix. Append `_start` or `_end`, then append `day`, `month` and `year` directly unless the row specifies otherwise. Thus a customer quotation's earliest expiry day uses `search_date_end_startday`. Lower and upper bounds apply independently. A populated range excludes a row whose corresponding date is unset.

| Register | Prefix and corresponding business date | Endpoint details |
| --- | --- | --- |
| Customer quotations | `search_date` quotation date, `search_date_end` last day of validity, `search_date_delivery` planned delivery, `search_date_signature` signature | All four use day components and inclusive whole-day endpoints. |
| Customer orders | `search_dateorder` order date, `search_datedelivery` planned delivery, `search_datecloture` closure | Order and delivery insert another underscore before the component, e.g. `search_dateorder_start_day`. Closure accepts `search_datecloture_start` / `search_datecloture_end` as integer timestamps, falling back to components such as `search_datecloture_startday`. |
| Customer invoices | `search_date` invoice date, `search_date_valid` validation, `search_datelimit` payment due date, `search_datec` creation, `search_datem` modification | The date reader also accepts appended `hour`, `min`, `sec`. Without a time it uses midnight at the start and 23:59:59 at the end. Creation and modification explicitly use user-relative time. |
| Supplier quotations | `search_date` requested delivery, `search_date_valid` validation | The unqualified date targets the planned delivery, even though a separate creation timestamp is available for display. |
| Supplier orders | `search_date_order` order, `search_date_delivery` delivery, `search_date_valid` validation, `search_date_approve` labelled approval | The approval-labelled controls compare the **delivery date** at both ends. The actual approval date can appear in the result column. The approval and delivery inputs intersect when both are supplied. |
| Supplier invoices | `search_date` invoice date, `search_datelimit` contractual due date | Both use inclusive whole-day endpoints. Invoice date explicitly uses server time. |

## Amounts, currency and commercial attributes

Amount selections compare **stored header totals**. An expression such as `>=100 <200` accepts 100 and excludes 200. An amount of zero is a meaningful criterion on these controls. `search_multicurrency_code` compares the stored currency code exactly. `search_multicurrency_tx` uses a numeric comparison on the stored conversion rate. A document's base amount, its transaction-currency amount and its applied payments are three different measures.

| Registers | Base net / VAT / gross request keys | Transaction-currency amounts |
| --- | --- | --- |
| Both quotations and both invoices | `search_montant_ht`, `search_montant_vat`, `search_montant_ttc` | `search_multicurrency_montant_ht`, `search_multicurrency_montant_vat`, `search_multicurrency_montant_ttc` |
| Customer orders | `search_total_ht`, `search_total_vat`, `search_total_ttc` | Same transaction-currency keys as customer quotations. |
| Supplier orders | `search_total_ht`, `search_total_tva`, `search_total_ttc` | Uses `search_multicurrency_montant_tva` for VAT, with the same net and gross spellings as the other lists. |

Both invoice lists additionally compare the two stored local tax amounts through `search_montant_localtax1` and `search_montant_localtax2`. On supplier invoices `search_vat_reverse_charge` selects the stored reverse-charge indicator including zero. Blank and `-1` omit the comparison. The values supplied as `search_amount_no_tax` and `search_amount_all_tax` are read and carried in page links but add no amount predicate. Use the `search_montant_` controls for base amounts.

| Registers | Other applied attributes |
| --- | --- |
| Customer quotations and orders | Positive `search_fk_cond_reglement`, `search_fk_mode_reglement`, `search_fk_shipping_method` and `search_fk_input_reason` select the stored payment terms, payment method, shipping method and source reason. `search_warehouse` selects the assigned header warehouse. The quotation also accepts `search_availability` for its availability code ID. |
| Customer orders and invoices | `search_module_source` and `search_pos_source` match the originating module and point-of-sale terminal. Customer quotations, orders and invoices each have `search_import_key` for matching the import batch key. |
| Both invoices | `search_type` selects invoice type. The customer list accepts a set. The supplier list implements single values 0 standard, 1 replacement, 2 credit note and 3 deposit. `search_subtype` uses stored subtype membership. Positive `search_paymentmode` and `search_bankaccount` select the header's payment method and assigned bank account. Terms use `search_paymentterms` for customers and `search_paymentcond` for suppliers. These values describe the invoice instructions. A payment posted to another account does not change this selection. |
| Customer invoices | `search_fk_input_reason` selects the source reason. `search_fac_rec_source_title` searches the linked recurring invoice template's title. `search_fk_fac_rec_source` selects by template ID. |
| Supplier invoices | `search_fk_fac_rec_source` selects the originating recurring template by ID. The optional `filtre` also accepts comma-separated field/value equality pairs, with each pair written as `field:value`. All complete pairs must match. |

On customer quotations the public note control matches the quotation's note. Customer orders search both notes on the order. Supplier quotations and invoices search both notes on the document. Supplier orders apply the public note field directly. Their visible `search_note_private` control has no direct query predicate, although a private note may match a free-text search. Customer invoices present both note controls under invoice column labels, but their predicates match the linked **project's** public and private notes. The invoice's own notes participate separately in free-text search.

Customer orders read `search_shippable` without applying it to row selection. When available, `show_shippable_command` controls whether the availability information is shown. On customer quotations the independent customer-code search variable is initialized empty, while the supported company-name search can include the code as described above.

## Document, party and product categories

All six registers accept a document-category list and an operator. The stems for `search_category_<stem>_list[]` and `search_category_<stem>_operator` are `propal`, `order`, `invoice`, `supplier_proposal`, `supplier_order` and `supplier_invoice` respectively. With operator 0 a document must have **every** selected positive category. Operator 1 accepts **any** of them. The submitted form supplies its operator and the initial view can inherit the configured default. The special list entry `-2` means that the document has no category relationship. Combining `-2` and a positive ID with “all” therefore yields no matches. Combining them with “any” yields the uncategorized documents plus the selected category.

`search_product_category` checks the catalog products linked by document lines. A positive ID requires at least one line with a product in that category. With `-2`, there must be no categorized product on any line. A document containing only free-text lines qualifies, as does a document whose products lack categories. One untagged line does not qualify a document that also contains a categorized product. A category on the header or on the supplier cannot satisfy a product-category condition.

`search_categ_cus` tests the customer's category on customer quotations, orders and invoices. On supplier invoices `search_categ_sup` tests the supplier's category. For both, `-2` selects a party with no corresponding category relationship. These party selectors and the usual product selector take one selected ID in the standard form. The quotation and order handlers read `search_category_product_operator` and the customer quotation/order handlers also read `search_category_customer_operator`. The invoice handlers set the party and product operators internally to 0. Independent category families intersect.

## Worked selections

| Operator's question | Inputs and records | Expected list |
| --- | --- | --- |
| Which validated customer quotations have expired beyond the configured delay? | Set `search_option=late`. Two validated quotes end just before and exactly at the cutoff. A signed quote ended last month. | The first validated quote qualifies. Equality at the cutoff fails the strict comparison. The signed quote fails the status restriction. |
| Which open customer orders were billed? | Set `search_status=-2` and `search_billed=1`. Candidate orders have statuses 1, 2 and 3 and each is marked billed. | The orders in 1 and 2 qualify. The closed order is eligible under `-3` in the same selection. |
| Which supplier orders are late for receipt? | Use `search_option=recv_late`. A partly received purchase order has a delivery date before the warning cutoff. An approved order has the same planned date. | Only the partly received order qualifies. Applying `late` instead would evaluate the approved order using its order date. |
| Why do two invoices with identical public notes give different results? | Customer invoices A and B contain “commissioning”. Only A's project public note contains it. Search `search_note_public=commissioning`. | A qualifies. Using `search_all=commissioning` matches both through their own public notes. |
| Which eligible documents contain no categorized product? | Set `search_product_category=-2`. One document has only a free-text service. Another also has a catalog line in category 5. | The former qualifies. The latter has a category link on at least one line. |
| Which supplier orders meet a net commitment in transaction currency? | Set `search_multicurrency_code` to `USD` and `search_multicurrency_montant_ht` to `>=100`. Candidate USD net amounts are 99.99 and 100.00, with a third EUR order at 120. | Only the USD order at 100.00 qualifies. Its converted base total can differ. |

These selections describe standard list behavior. A site's declared extra fields can supply additional predicates and an installed extension can change the base search. The six lists provide no fixed inventory of those site-defined attributes.
