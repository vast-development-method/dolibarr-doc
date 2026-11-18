# Tax selection and regional reporting

The release supplies 234 VAT dictionary rows for 68 countries. Of these, 223 start active and 11 inactive. The [complete rate inventory](tax-rates.csv) lists each inserted row in source order. It preserves zero rates, negative local-rate choices, additional component types and inactive entries. The values describe the software distribution. They cannot establish the legally applicable rate for a jurisdiction or transaction date.

## The identity of a rate

The dictionary stores the entity, country, optional buyer department, optional code, applicable sales/purchase direction, main percentage, two local components and their calculation types, default flag, recoverable-only flag, e-invoice exemption code, note, availability and optional posting accounts on each side. It has no effective-from or effective-through date. Each release inventory row identifies its source line in `htdocs/install/mysql/data/llx_c_tva.sql`. That locator does not identify the database row on a running instance.

The unique dictionary key comprises entity, country, code, main percentage and recoverable-only flag. The buyer department and sales/purchase direction are outside this key. A second department rule with the same country, code, main rate and recovery status needs a distinct permitted key. The source rows let the database allocate identifiers and insert the installation entity. All 234 omit a buyer department, sales/purchase restriction, explicit default and accounting codes. Their defaults are therefore country-level, both directions, default flag off and posting accounts unset. Eighteen rows supply nonempty rate codes. The same numeric main percentage can represent several distinct treatments.

The CSV gives both local value and type per component. Zero in an omitted local field corresponds to the table default. A colon-separated list is a set of choices, never an instruction to add all the entries together. Local type 1 applies on the pre-main-tax amount for goods and services, 3 for goods only and 5 for services only. Their counterparts 2, 4 and 6 use a base including the main tax. Type zero contributes no local component through these calculation branches.

Release references include `htdocs/install/mysql/tables/llx_c_tva.sql:21–40`, `htdocs/install/mysql/tables/llx_c_tva.key.sql`, `htdocs/install/mysql/data/llx_c_tva.sql:48–425` and `htdocs/core/lib/price.lib.php:245–295,337–389`.

## Which rate is proposed

1. The transaction context supplies seller, buyer and usually a product or service. Missing country codes fall back to the operating company's country. When the electronic-services setting applies to the defined intra-community consumer branch, the buyer country determines the initial product/country lookup.
2. Otherwise a seller outside the VAT scheme produces zero. Next, an active buyer-department rule, if configured, takes precedence. The department query orders by explicit default first, descending rate, ascending code, then recoverable-only flag. No standard seed row provides this override.
3. For a domestic transaction, the product's tax rate and optional code take precedence when available in the supported country context. For a supplier transaction with a matching supplier-price identifier, its rate and code take priority over the product sale rate. The domestic branch also recognizes the specific FR/MC and MQ/GP groupings.
4. When the product-country lookup falls through, it selects the first active country row in the allowed entities, ordering by default flag descending, main rate descending, code ascending and recoverable-only flag ascending. The installation may instead force a value, including a coded value. The special forced setting `none` produces an empty suggestion. With ordinary lookup and no matching row, the helper retains zero.
5. On the remaining intra-community path, the buyer's organization classification and, by default, the validity of its VAT identifier distinguish the seller-product-rate branch from the zero-rate branch. Configuration can treat a business with an unknown identifier as qualifying for zero. There is an optional seller-product-rate path for individual customers outside that community. Other unmatched cases retain a zero suggestion. An extension can supply a replacement.

The selector loads active records for the requested countries and accessible entities, then retains records appropriate to the sales/purchase direction. Resolving an existing dictionary row by internal ID retrieves its recorded components directly. Resolving a percentage with optional code instead requires an active matching country row. The lookup uses seller country by default or buyer country under the electronic-services option. A rate-only lookup with multiple matching entries and no explicit ordering cannot reliably distinguish their local component definitions.

Release references include `htdocs/core/lib/functions.lib.php:8226–8290,8368–8449,8543–8702` and `htdocs/core/class/html.form.class.php:7905–7946,8107–8139`.

## Examples from installed records

| Data and transaction | Result in the ERP |
| --- | --- |
| India, net 100, code `C+S-18` | The row supplies 0% main VAT, 9% local component one and 9% local component two, both type 1. When enabled and applied, the amounts are 0, 9 and 9, producing gross 118. `I-18` instead supplies 18% main VAT and two zero local components, also gross 118. With the Indian automatic switch enabled on the domestic path, different seller/buyer state IDs convert the split code to the integrated code, and equal IDs convert the integrated code back. The equality comparison does not check that both states are populated. |
| Spain, net 100, 21% row | The row offers a 5.2% type-3 local charge for goods and type-5 service withholding choices of −19, −15 or −9%. For a qualifying goods line, 21 plus 5.20 gives gross 126.20. For a qualifying service with −15 selected, 21 less 15 gives gross 106. The company and counterparty local-tax flags and the configured counterparty value govern application. A single line does not incur both the goods-only surcharge and the services-only withholding. |
| Canada, net 200, 5% row | With the local component active, the main tax is 10 and the 9.975% type-1 component is 19.95, yielding 229.95. The seed row has no buyer-department identifier. The country file also contains commented province examples. They supply no extra selectable provincial rates. |
| Gabon, net 100, code `TPS95C` | The source note mentions 9.5 but the stored main rate is 10, plus a type-1 local component of 1. With that component applicable, amounts are 10 and 1. The neighbouring `TPS95` row also stores main rate 10 but no local charge. The rate and code fields determine lookup and calculation. Display text has no calculation role. |
| Netherlands, unknown domestic product, ordinary fallback | The distributed rows are active 0%, active 9% and inactive 21%. Without a configured override or explicit default, the active-country sort selects 9%. A migrated or edited installation may hold a different active set. |
| France, four inactive 8.5% entries | Codes `85`, `85NPR`, `85NPROM` and `85NPROMOMR` distinguish recovery and local components. The country selector excludes all four while inactive. The direct row-ID lookup can still return their recorded component fields. |

Release references include `htdocs/install/mysql/data/llx_c_tva.sql:86–91,129–146,178–187,245–247,323–326`, `htdocs/core/lib/functions.lib.php:8048–8178,8625–8644` and `htdocs/core/lib/price.lib.php:337–389`.

## Revenue stamps and environmental charges

Revenue stamps use a separate country dictionary with a fixed/percentage discriminator. Nine active rows ship across four countries. Tunisia has one fixed amount, 0.4. Greece has 1.2%, 2.4%, 3.6% and a fixed 1.0. Mexico has 1.5% and 3%. Türkiye has 0.00948% and 0.00189%. The invoice selector filters to active rows for the company's country and preselects a sole choice. For a percentage, the customer invoice editor rounds the net invoice amount to two decimals, multiplies by the rate divided by 100, rounds the resulting stamp to two decimals, and submits that amount. For a fixed selection, it submits the selected amount directly. At a net amount of 250, the Greek 2.4% choice yields 6.00 while the fixed choice yields 1.00.

The environmental-charge dictionary supplies 19 active French entries, each identified by code, label, pre-tax price, collecting organization and country. For example, codes `32051` and `32061` carry prices of 0.42 and 0.84. The selector reads active entries, orders them by country, organization and code, and displays the price alongside the organization. Its selection value is a dictionary row ID. These figures describe a cost per listed category. They do not enter the main VAT percentage lookup.

Release references include `htdocs/install/mysql/data/llx_c_revenuestamp.sql:26–43`, `htdocs/install/mysql/data/llx_c_ecotaxe.sql:34–52`, `htdocs/core/class/html.formother.class.php:283–312,333–365` and `htdocs/compta/facture/card.php:5984–6017`.

## From regional tax columns to a reporting period

Each invoice line can carry main tax, local tax one and local tax two. For the monthly local-tax report the operator chooses component one or two. The report reads sales and purchases by that component and month, calculates the recognized amounts under the configured tax timing, then subtracts recognized purchases from recognized sales. It labels the report using the company's country. A localized label cannot change the source value or move a local component into the main-tax column. When the Indian example is fully recognized, the split line contributes 9 to each applicable local column. The integrated line contributes 18 to the main column.

The period selection is a separate decision. Explicit start and end take precedence. A requested month selects its first through last days. Explicit quarters use January–March, April–June, July–September and October–December. Without an explicit period, the frequency setting can choose the last complete month, a completed quarter aligned to the configured fiscal start, or a one-year window starting in the configured fiscal month. Assuming a January fiscal start, in mid-May a quarterly default uses January through March, while a monthly default uses April. The date-selection control does not infer the applicable filing frequency from a seeded rate.

The local-tax payment section groups each recorded amount twice, once by value-date month as claimed and once by payment-date month as paid. Each query filters to the current entity and chosen component. A 60 payment with a March value date and an April payment date will appear under March claimed and April paid when the period contains both months. These are two views of one payment. Adding the two columns would double-count it.

Release references include `htdocs/compta/localtax/index.php:209–253,323–324,479–498,518–548,579–601`, `htdocs/compta/tva/initdatesforvat.inc.php:32–96` and [Tax recognition and remittance](../specification/accounting/tax-recognition-and-remittance.md).
