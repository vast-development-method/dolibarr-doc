# Report local components, withheld amounts and geography

A regional tax percentage can change the invoice gross, the VAT line total, one of two local components, or more than one of these. The counterparty report, rate report and country turnover report read different fields. To reproduce an enquiry, retain the requested component, the line's applied rate and source code, and the dates and amounts of the underlying allocations.

## Which regional enquiries appear

The standard tax menu uses the company's country and its active tax dictionary. Local component one and component two each have independent availability. A country needs an active applicable dictionary record with a nonzero component **type** in an accessible dictionary entity. The company must also mark itself liable for that specific component. A type with a percentage of zero can still make the component available. The hide-VAT-menus setting encloses the main VAT and both local-component groups. None of these navigation decisions changes an invoice's previously stored local amounts.

The local-component party view requires a component selector and access to the tax-charge area. Its calculation/display mode comes from the applicable company option. These are the actual side selections in this view:

| Company local calculation mode | Sales retained by customers | Purchases retained from suppliers | Difference line |
| ---: | --- | --- | --- |
| 0 | Shown | Shown | Sales component less purchase component |
| 1 | Hidden | Shown | Omitted |
| 2 | Shown | Hidden | Omitted |

The report uses the displayed counterparty's domestic or intra-community identification data as a label. The amount grouping is by party identity. Parties with the same tax identification value can still have separate rows. Each visible row must have a nonzero signed total for the chosen component. A positive turnover minimum compares strictly against the original net amount across included lines. A zero-net result after sales and credits fails a positive minimum even if tax remains after rounding or differently taxed lines.

## Partial payment and withholding

Take a sale of services with net 100, ordinary VAT 20 and a signed local withholding of −15. The payable gross is 105. The customer pays 52.50 in March and 52.50 in April. Assume payment-based sales services, ordinary proportional presentation, and a local mode that shows sales. The party summary uses the tax reader's original line totals. Because a relevant allocation exists in each month, selecting March shows net 100 and local −15 on the party's row. Selecting April separately produces the same original amounts. A selection covering both payments normally contributes the original line once in this aggregation. Adding two separately run party reports would double-count the withholding.

The monthly sales calculation instead uses the payment-to-gross fraction against the stored local component. Each monthly payment yields 52.50 / 105 × (−15) = −7.50. Main VAT and the regional withholding retain independent signs. The local report can display a negative sales-side amount even though the receipt of 52.50 is positive. On the monthly purchase side the source query selects by the purchase timings while the display's apportionment branch reads sales timings. When the two differ, the purchase figure needs reconciliation to the dated supplier allocations, as described for the [monthly VAT comparison](period-and-authority-reconciliation.md).

With a turnover minimum of 100 this party's original net of exactly 100 is excluded. Set the minimum to 99 and it is admitted. Withholding is still excluded from this party report for a party whose selected component sums to precisely zero, even if its net turnover is large. The detail-by-rate view can be used to inspect individual lines on opposite sides of zero.

## What country and rate mean in a turnover report

The country-by-rate view in the accounts area is a report of **net invoiced turnover**. It groups by current third-party country, stored invoice line type and numeric main VAT percentage. It omits the rate's explanatory source code from the grouping. A missing country stays in an unassigned geographic group. Changing the party's master country can reclassify an earlier invoice in a later run. The country selected for a commercial tax rule, the delivery address, the issuing company's country and this report's country may represent different places.

The report uses document dates and active invoice entity scope. The monthly columns rotate into fiscal-start order, with twelve fixed month columns. Date ranges longer than a year, or an end preceding the start, are replaced with an end one year after the start minus one second. The view selects invoice/accrual accounting for these rows. Its cash-basis branch explains the absence of a line-by-line allocation. Main VAT by rate, by contrast, can apportion cash using a report convention.

Suppose a party has two issued sales lines, each net 100 at 20%, one carrying source code A and the other source code B. The country report shows 200 in one goods/country/20% row for that month. VAT detail can show two rate-code groups with 20 tax each. If the same entity also records an unvalidated supplier draft, the purchase country breakdown can include the draft's net amount, whereas ordinary purchase VAT eligibility starts at validated/paid. In the supplier country query the status and type restrictions are built on the sales query after it has already executed. The supplier request executes its own date and entity predicates. This explains a net mismatch even when both users choose the same dates.

The chart's axes measure different things. A zero-rate sale contributes its net base to the geographic report. A “hide zero VAT” option in the shared tax readers can remove its row from VAT enquiries. Local withholding does not create a second turnover row. Freight destination, document currency conversion and regulatory filing codes are absent from the country grouping.

See [regional rate selection](../localization/tax-selection.md) for how the invoice received its rates.
