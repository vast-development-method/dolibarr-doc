# Customer order lines across the portfolio

The detailed order list starts at the **order line ID**. Two different rows from one order keep distinct quantities, descriptions and amounts. An order with no qualifying detail contributes zero rows. The ordinary population spans allowed customer-order entities, excludes special lines of type 9, and left-joins the catalogue. A free-text service can therefore appear with its description and an empty catalogue reference.

## Selecting a line

| Operator selection | Exact target |
| --- | --- |
| Line ID, product reference, description | Line ID, current catalogue reference, or either the catalogue label or the order-line description, respectively. The general text search covers order/customer references, line description, party name/alias, town, postcode and public note. It adds the private order note for an internal account. |
| Items for purchase | Current catalogue record is marked purchasable. Free-text lines have no matching catalogue record. |
| Goods/services only | Stored line type 0 or 1. A free-text item of one of these types can qualify. |
| Exclude free-text lines | Require a non-null catalogue product ID. |
| Product versus customer categories | Membership of the line's item versus membership of the order's customer. Each category selector has all/any choices. No-category checks for absence of a membership in the corresponding relation. |
| Order state and billed flag | The flag is the order header's billed classification. State −1 is cancelled, 0 draft, 1 validated, 2 in progress and 3 closed. The combined options −2 and −3 mean states 1/2 or 1/2/3. Selecting 1 while shipping is disabled includes both 1 and 2. A combined state does not imply a value for billed. |
| Date of order, promised delivery, closure | Each bound compares the corresponding header date inclusively. Lower dates begin at midnight, upper dates end at 23:59:59. They can be combined independently. |
| Party, conditions, method and channel | Party ID and name, alias, town, postcode, state, country, party type, payment terms, payment method, shipping method and order-entry channel all select the parent order's context. An external account's party is forced on the list. |
| User and project | Internal order contact, current party representative, order author and linked project each have separate selectors. The author search covers login, first and last name. Project filters use project reference and title. |
| Warehouse | Warehouse identified by the order header. A shipment detail or stock movement may identify a different actual warehouse. |

### Reading the amounts

The company-currency net, tax and gross amount filters apply to each line. The alternate currency code, exchange rate and alternate-currency net, tax and gross filters apply to the **order header**. Those alternate-currency amounts repeat on every matching line. For a two-line order with net 60 and 40 in company currency and whole-order net 125 in the alternate currency, filtering company net to 60 selects one line. Filtering alternate net to 125 selects both. The repeated 125 still represents a single order worth 125 in that currency.

The visible page accumulates ordered quantity and the enabled company-currency amount columns. Sorting by product reference also enables subtotals when the reference changes. A page boundary can cut a series of the same product into two groups. With filtering by an internal contact, one person assigned two internal order roles can also produce a difference between the full record count and the visible lines. The data query selects distinct rows, whereas the separate count uses the joined rows.

Optional cost, margin and rate columns require margin visibility. For every displayed line the renderer reloads **all** lines on that order and calculates the order's overall margin. For example, two lines with respective revenue/cost of 60/40 and 40/20 give a whole-order margin of 40. Showing both lines displays 40 on each and can give 80 in the detail-list margin sum. The net line total remains 100. Filtering away the second line leaves the entire 40 margin beside the first line's 60 net. This is a reason to retain the margin's document grain when reconstructing a line report.

### Checking what can ship

When enabled, the shippability column evaluates a catalogue goods line on an order between draft and closed. It subtracts the summed shipment detail quantities for that order line from the ordered quantity. Its default shipment lookup does not apply a minimum shipment status. The display compares the remainder to the product's current physical stock, with virtual stock available as context. A balance equal to the remainder qualifies. The calculation is informational and makes no new warehouse assignment or reservation. Services have no physical-stock icon.

An order for ten goods with three allocated in shipment details and seven physically available is shown as shippable on that line. The ordered quantity shown next to it remains ten. Reducing physical stock to six changes the shippability indication while leaving the ordered and allocated quantities intact. Another open order can compete for those same units. [Stock, fulfilment and production](../reporting/stock-fulfillment-and-production.md)

Source locations include `htdocs/commande/list_det.php:76–144,177–259,388–462,478–609,629–695,1501–1584,1661–1676,1846–1937,2016–2059,2120–2218,2265–2277`, `htdocs/commande/class/commande.class.php:2460–2505` and `htdocs/core/class/html.formmargin.class.php:64–118,166–199`.
