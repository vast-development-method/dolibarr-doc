# Operator list coverage in release 24.0.3

The release contains **56 tracked application files whose basename is exactly `list.php`**. Of these, 55 have stable module owners. Eighteen have field-by-field filter guides. **37 stable paths still need a full selector trace**, including three with screen-specific evidence in other chapters. One further file belongs to a development module. These counts measure a reproducible subset of navigation. A percentage for the entire interface or the ERP would require a broader inventory. [Release baseline](../baseline.md) · [Annotated screen inventory](../list-filters/screen-index.csv)

| Predicate coverage | Paths | What a reader can establish |
| --- | ---: | --- |
| Predicate guide | 18 | The guide identifies selected records, input names, comparisons, role and entity scope, and screen-specific differences. |
| Partial screen evidence | 3 | Chapters trace bookmark visibility, third-party representative assignment and the supplier invoice line assignment queue. The last also follows selected lines through posting. These screens are outside the 18-register selector dictionary. [Workspace and bookmarks](../integrations/authoring-and-workspace.md) · [Third-party selection and sales attribution](../operator-reports/people-and-sales-attribution.md) · [Supplier account preparation](../finance/supplier-account-preparation.md) |
| Open for selector trace | 34 | Screen purpose and release ownership are recorded. Coverage of related records or workflows elsewhere does not establish the screen's selection behavior. |
| Excluded by maturity | 1 | `htdocs/intracommreport/list.php:181–191` explicitly requires the intra-community reporting module. Its descriptor declares development maturity at `htdocs/core/modules/modIntracommreport.class.php:53`. |
| **Total** | **56** | **55 stable-owned, one development-owned, zero unresolved owners.** |

## What operators actually open

The filename contains both ordinary transaction registers and lists with narrower audiences. Each candidate has one primary surface for counting. The descriptor column in the CSV can name multiple modules when a selection is shared or a supplier workflow supports both permission arrangements.

| Primary surface | Count | Examples and remaining distinctions |
| --- | ---: | --- |
| Business register | 43 | Quotations, orders, invoices, parties, contacts, payment records, bank accounts, asset records, loans, stock, service cases and projects. The 18 detailed guides all belong here. Twenty-five other business registers remain, including the partially traced third-party register. |
| Accounting assignment queue | 3 | These pages work on customer invoice **lines**, supplier invoice **lines** and expense **lines**. A single source document can create several assignment decisions. |
| Setup catalogue | 3 | Bookkeeping templates, fixed-asset models and product variant **attribute definitions** are reusable records. The variants list selects attributes, while the ordinary product register selects items. |
| Identity and operations | 4 | Users, groups, per-user API token records and scheduled jobs. The token list is scoped to a user. The user card exposes it when API access and the token-table option are enabled. |
| Workspace tools | 1 | The bookmarks register includes ownership and visibility behavior. |
| Public self-service | 1 | The public ticket page uses the public-interface setting and requester verification. Internal ticket queue filters describe a different entry point. |
| Development report | 1 | The release tree retains the intra-community list under its development descriptor. |

Source examples include `htdocs/accountancy/customer/list.php:302–321`, `htdocs/accountancy/supplier/list.php:306–325`, `htdocs/accountancy/expensereport/list.php:276–291`, `htdocs/variants/list.php:72–74,246–270`, `htdocs/user/card.php:2200–2214`, `htdocs/user/api_token/list.php:45–63` and `htdocs/public/ticket/list.php:92–96,120–126,133–167`.

## Other filenames with distinct business selections

A reviewer looking only for `list.php` would miss the following operator entry points. These examples identify additional selection contracts and give a path to existing behavior documentation where available. Their number does not increase the 56-file denominator.

| Entry point under `htdocs/` | Unit selected and reason it matters |
| --- | --- |
| `commande/list_det.php:421–437` | An individual customer order line joins its order and catalog item. Several lines can belong to one order, and order margin can repeat on those lines. [Customer order line report](../operator-reports/customer-order-line-list.md) |
| `compta/bank/bankentries_list.php:585–615` | A bank transaction belongs to an account. The bank-account directory counts accounts, while this register supports reconciliation at entry level. |
| `compta/prelevement/orders_list.php:215–231` | Direct-debit and credit-transfer **batch headers**. The exact-basename register at `compta/prelevement/list.php:145–179,207–218` joins the batch to its payment lines. |
| `compta/facture/invoicetemplate_list.php:320–338,400–416` | Recurring invoice definitions and their template lines. An issued invoice may reference one of these templates, and many issued invoices may come from the same definition. |
| `accountancy/bookkeeping/listbyaccount.php:24–30` and `accountancy/journal/sellsjournal.php:170–221` | Account-ordered ledger entries support matching. The sales journal instead considers source invoice lines and whether the invoice has already been transferred to bookkeeping. [Account matching](../specification/financial/manual-ledger-and-account-matching.md) · [Source journal posting](../specification/accounting/source-journal-postings.md) |
| `product/stock/movement_list.php:639–684,971–988` | Each movement records a dated quantity change. A warehouse or physical-count session can lead to many movements. [Movement journal](../warehouse-corrections/movement-journal-and-counts.md) |
| `product/stock/productlot_list.php:80,244–260` and `product/stock/stocktransfer/stocktransfer_list.php:235–254` | Lot master records and stock transfer documents each have their own search. A lot can appear in several movements, and a transfer can cover several lines. |

## How to continue the inventory

Use the supplier assignment and purchase-journal trace as a reference for the customer and expense assignment queues, then follow those records into their source journals. The expected evidence includes which line appears, which account is presented, what happens after a binding change, and which list confirms that a posting reached the ledger. [Supplier account preparation](../finance/supplier-account-preparation.md)

The payment registers form a second tractable group: customer, supplier, expense reimbursement, donation, miscellaneous, VAT and local tax payments, followed by the bank-entry and remittance-batch registers.

For another release, enumerate tracked files below `htdocs/` and compare the final path component exactly with `list.php`. Record the release's file tree before applying the stable-module selection. Identify ownership from each page's records, module guard, permission or module navigation and the version in its top-level descriptor. The CSV provides the page line ranges and the descriptor path and line for that evidence. The cross-reference uses paths from the documentation repository root. [Module maturity inventory](modules.json)

This pass found no exact-basename matches in vendor/include trees, framework internals, custom add-ons or generator scaffolding. For instance, `htdocs/modulebuilder/template/myobject_list.php` is an authoring template with a different filename. The accounting `admin/template/list.php` is a working register of bookkeeping templates with a chart-of-accounts permission and a query on persisted records. It belongs in the inventory. Menu aliases, tabs, parameterized modes, dashboards, AJAX selectors, cards, generated reports and endpoint collections require separate discovery. [Bookkeeping template source locator in the inventory](../list-filters/screen-index.csv)
