# Chart models and report assignments

The chart registry contains **46 active chart models for 39 countries**, describing **39,311 account definitions** in the corresponding country files. These totals count account-number entries, including grouping accounts with children. Two entries start inactive. Repeated numbers under different model codes represent different chart entries. A selection of one model can load more account definitions than the selected model contains.

The [complete chart inventory](chart-models.csv) gives one row per model and dataset. Filter `availability` to `registered` for the 46 models offered by the standard selector. The country code and name identify the country dictionary entry. The counts distinguish all accounts, inactive accounts, and predefined income and expense classifications. The dataset column distinguishes the German-language Swiss alternative from the standard country chart.

## Keys and account hierarchies

A model has an internal identifier, country, version code, label and active flag. The entity stores its selected model identifier. Each account within it has an entity, model version, account number, internal identifier, parent identifier, predefined group and label. The unique account key combines number, entity and model version. The account number is a string. Its length and leading zeros can carry meaning. The parent field references the parent's internal identifier. Constructing parents by truncating the printed number can produce a different hierarchy.

For example, product sales account `4010` in `US-BASE` has source row ID 1070 and parent ID 4000. Under the same model, product cost `5010` has row ID 1077 and parent ID 5000. The latter's predefined type is `COGS`. Report membership follows the account's type or its assigned report category. A parent number beginning with 5 establishes neither rule by itself.

## Loading and changing the chart

1. A user with chart-of-accounts permission selects an active registry entry. The selector sorts by country code and model version. It offers registry entries across countries.
2. When an entity changes an existing selection, the action counts bound customer invoice, supplier invoice and expense report lines against the outgoing chart. It also counts bookkeeping rows in the entity. A nonzero count requests confirmation.
3. The model's country code determines the file loaded. The loader reads the complete country file. For the usual entity-first record layout, it adds the country-file offset, when supplied, plus 100,000,000 times the entity identifier to source row and parent identifiers. Root parent zero is preserved.
4. The action records the selected registry identifier. Resolved model version restricts subsequent account lookup. The load action can produce a warning and still proceed to set the selection. Existing ledger numbers and historical bound-line identifiers receive no automatic conversion.

For Germany, choosing either `SKR03` (2,243 entries) or `SKR04` (2,421) opens the same German file. Choosing one selects its version for account lookup. For France, `PCG25-DEV` has 838 definitions, of which suspense accounts `472` and `473` start inactive. The farm chart `PCGAFR14-DEV` defines those same numbers as active in its own hierarchy. The date-like parts of the identifiers distinguish models and do not activate an annual transition.

## Country-file exceptions

| Record set | Effect on the selectable inventory |
| --- | --- |
| Fifteen SYSCOHADA country models | Each has a separate country entry and model identifier and supplies 1,227 account numbers. Each has 106 rows in the predefined income types and 250 in the expense types. An account bound to the Benin model retains that model identity even if another country has the same account number and label. |
| `AT-BASE-2` | Austria's country file also contains 205 entries under this alternate version. The registry lists only `AT-BASE` for Austria. Loading the file can introduce the alternate rows without creating another selector choice. |
| `PCG15-PYME-AD` | The Andorran file describes 393 accounts. The default registry contains no Andorran model. The presence of that file alone supplies no normal selection. |
| Swiss German-language account file | The default Swiss country file and the alternate German-language file both contain 254 accounts under `PCG_SUISSE`. They share the model identifier. The country loader selects the unsuffixed Swiss file. For account `4000`, one file supplies a French label and the other a German label. |
| `CO-PUC` | The 2,502 Colombian definitions all include a subtype column. The account table does not declare this column and the standard chart-loading rewrite does not strip it. The inventory records these definitions but cannot treat them as 2,502 successfully loaded accounts on the supplied clean schema. |
| `NSCF` | The 812 Algerian definitions use insert-if-absent statements starting with an explicit row identifier. They omit the entity column. The table defaults entity to 1 and the offset rewrite matches a different, entity-first row layout. Direct loading of this file merits particular care when interpreting the active entity's available accounts. |

## How a chart contributes to income and expense

In bookkeeping mode, the monthly result report joins each ledger account number to the selected version and entity. Its income filter accepts `INCOME` and `OTHER_REVENUE`. It sums credit less debit. Its expense filter accepts `EXPENSE`, `COGS` and `OTHER_EXPENSES`. It sums debit less credit. The query groups by document reference, general account, subsidiary account, subsidiary label, predefined type and posting month. For the same joined account, a reversal reduces the corresponding monthly figure.

Exactly **34 of the 46 registered models** contain accounts carrying those literal predefined types. The other twelve are `AT-BASE`, `PCG_SUISSE`, `PC-MIPYME`, `CO-PUC`, `SKR03`, `SKR04`, `DK-STD`, `EC-SUPERCIAS`, `PCG08-PYME-CAT`, `Ε.Λ.Π.`, `SAT/24-2019` and `US-GAAP-BASIC`. The CSV records zero recognized rows for each. These models can contain perfectly identifiable revenue and cost accounts. For instance, the US GAAP model calls its classes `REVENUE`, `EXPENSES` and `OTHER_INCOME_EXPENSES`. Those strings fall outside the predefined query. The Catalan and Spanish models also differ in this respect despite sharing a country and similar account numbers.

Suppose May bookkeeping in `US-BASE` credits 1,000 to product sales `4010`, credits 20 to interest income `7010` and debits 400 to product cost `5010`. The report recognizes 1,020 income and 400 expense. A further debit of 50 to `4010` in May reduces the reported income to 970. The same balances held on accounts carrying the US GAAP model's native types would be absent from this particular query. For Japan, 22 income rows and 135 expense rows match. The pack also contains distinct extraordinary income and expense types outside the query, so nonzero matches do not imply coverage of every result account.

## What comes preassigned to a personalized report

The accounting module supplies one country-neutral report, code `REP`. The initial dataset attaches three active categories to report identifier 1 in the installation entity. None of the country account files supplies a direct personalized-category identifier or an account-to-category link. **No country pack in this inventory ships account assignments for the personalized statement.** A chart with recognized predefined types can populate the separate monthly income/expense query immediately after posting while its personalized report still needs account assignments.

| Position | Code | Calculation supplied |
| --- | --- | --- |
| 10 | `INCOMES` | Simple category, credit less debit on its assigned accounts. The suggested 7-series range is comment text. |
| 20 | `EXPENSES` | Simple category, also credit less debit. The suggested 6-series range is comment text. Debit expenses appear as negative signed balances. |
| 30 | `PROFIT` | Formula `INCOMES+EXPENSES`, evaluated after the two earlier positions. |

For the May example, assigning `4010` and `7010` directly to `INCOMES` and `5010` to `EXPENSES` yields 970, −400 and 570 after the reversal. Assigning only `4010` to income gives 950, −400 and 550. The unmatched interest remains in the ledger. The category membership is operational data. The display's example number ranges do not automatically enroll newly created accounts. Category selection includes the company country and country-neutral code zero, scoped to the entity, selected report and active status. The model also stores many-to-many account links for category maintenance. The personalized result renderer resolves ordinary rows by the direct category field. A many-to-many link on its own does not reproduce this example.
