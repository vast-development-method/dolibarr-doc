# Percentage deposit by tax category

A deposit requested against a quotation or sales order is a new customer invoice with its own terms, tax lines and link to the originating document. The calculation uses the commercial document's negotiated `deposit_percent`. The origin's payment-term dictionary value determines eligibility. The separately supplied terms ID determines the new deposit's terms.

## Preconditions and inherited fields

The origin must be a quotation or order. The invoice date is required and must be within the allowed future limit measured from the end of the user's current day. The supplied terms ID must be positive. The origin's `cond_reglement_id` must resolve to a payment term with a nonempty deposit percentage, and the origin must itself have a nonempty `deposit_percent`.

Initialize the new deposit with the customer, project, customer reference, issue date, payment mode, new payment terms, availability, demand reason, settlement bank, trade terms and location. Inherit the origin's currency ID, currency code and exchange rate. Copy public/private notes if propagation is enabled, and the origin's configurable fields and document link. The business operation accepts explicit header overrides after copying these values.

## Two allocation policies

| Stage | Split using source gross | Take a percentage of source net |
| --- | --- | --- |
| Build buckets | Group by the pair `tva_tx` and `vat_src_code`. Skip every line with a nonempty `special_code` and sum the remaining `total_ttc` per pair. | Same bucket identity. Skip a zero quantity and a nonempty `special_code`. Accumulate each eligible `total_ht × deposit_percent / 100` into that line's bucket. |
| Derive line unit | Intended gross = source header gross × percentage / 100. Bucket share = bucket gross / source header gross (zero when source gross is zero). Gross allocated to the bucket = intended gross × share. Net input = allocated gross / (1 + numeric VAT rate / 100). | The accumulated net is the line unit input. A zero total of eligible source net also sets the unqualified zero-rate bucket to zero. |
| Write the deposit line | Skip zero bucket amounts. Insert one line per remaining bucket with quantity one, net unit input, combined rate/code, zero discount and both local-tax selectors zero. The configured deposit product can be assigned. | Uses the same line construction. In either policy the result may include several VAT rates and two different codes at the same percentage. |
| Resolve differences | Compare the generated gross to the sum of **allocated eligible bucket gross**. If different, reload deposit details and adjust the first returned line's net unit by subtracting the gross difference divided by (1 + its numeric VAT rate / 100). Reprice it using its original tax code. | There is no corresponding gross residual correction in this branch. |

Under gross splitting, an excluded special charge can cause the target for the included buckets to differ from a straight percentage of the entire header. For example, with gross 240.00 of which 40.00 is excluded, a 25% deposit gives a 60.00 header-based starting amount. The eligible share is 200/240, so the generated eligible gross target is 50.00.

The operation creates the header inside a surrounding transaction, adds its lines, runs a conversion extension point and optionally validates before committing. Checked errors in creating the header, adding or adjusting a detail, executing the extension or validating roll back this operation. A header-create event may therefore run before the first grouped deposit line exists. Validation assigns the deposit its issued identity. Recording receipt or consuming the deposit on a later invoice has separate accounting effects.

## Worked tax-code and rounding cases

Suppose a 25% deposit applies to the following ordinary source items, with no local taxes and two decimal monetary amounts. Codes A and B both represent a 15% rate. The deposit must preserve separate category identities.

| Source tax category | Source net | Source gross | Deposit net | Deposit VAT | Deposit gross |
| --- | ---: | ---: | ---: | ---: | ---: |
| 15%, A | 80.00 | 92.00 | 20.00 | 3.00 | 23.00 |
| 15%, B | 40.00 | 46.00 | 10.00 | 1.50 | 11.50 |
| 0%, Z | 60.00 | 60.00 | 15.00 | 0.00 | 15.00 |
| **Total** | **180.00** | **198.00** | **45.00** | **4.50** | **49.50** |

For a rounding difference, take two distinct zero-rated categories, each with source gross 1.01, and a 50% deposit. With unit precision sufficient to retain 0.505 and conventional half-up cent rounding, each generated line initially gives 0.51. Their sum is 1.02, while the aggregate eligible target is 1.01. The gross-split branch subtracts 0.01 from the first line's unrounded unit of 0.505. Rounding 0.495 gives 0.50, the other line stays at 0.51 and both tax codes remain present. The percentage-of-net branch leaves the two rounded 0.51 lines as generated.

See [credit, deposit and replacement operations](../finance-exceptions/corrections-and-deposits.md) for conversion into an available customer adjustment and its later application to a line or settlement.
