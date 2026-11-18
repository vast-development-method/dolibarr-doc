# Products, variants and supplier offers

A catalogue entry connects sales, purchasing, stock and production. The internal product reference identifies what the business handles. A supplier may use a different reference, quote a different quantity and change its price without changing that internal identity.

| Record | Identity and relationships | Behaviour |
| --- | --- | --- |
| Product or service | Internal ID, reference unique within entity. Barcode, barcode type and entity also form a unique key. | Type 0 is a product and type 1 is a service. Sale eligibility, purchase eligibility and stock tracking are separate attributes. A service can move stock when marked stockable and service stock support is enabled. |
| Variant | Parent product, child product and a collection of attribute/value pairs | The child has its own product ID and reference. For example, a blue medium shirt can be stored, received and sold independently of the blue large shirt. |
| Supplier offer | Product ID, supplier ID, supplier reference, entity, minimum quantity, pack size, currency, tax rate, price and discount | The database enforces uniqueness on supplier reference, supplier, quantity and entity. Multiple quantity breaks may describe the same vendor article. |
| Document line | Reference to catalogue product when selected, description, unit price, tax, discount and quantity on the transaction | The entered commercial terms live on the order or invoice line. Subsequent catalogue changes support future transactions. |

## Pricing decisions

1. For a vendor offer entered inclusive of VAT, divide the quoted price by `1 + rate/100`. Divide the resulting total price by its quoted quantity to derive the unit price, using unit-price precision. Packaging defaults to the quoted quantity when omitted. The supplier can require a minimum of 100 and ship packs of 50.
2. For a requested quantity above zero, the lowest-price lookup considers active suppliers and offers whose minimum quantity is at most the requested quantity, within the allowed entities. It can restrict the search to one supplier. In its ordinary fixed-price branch it compares unit prices after the percentage discount. Freight charges and lead time are separate fields.
3. For a buyer on combined customer-specific and price-level pricing, the selling-price resolver looks for an effective customer price using its validity dates. If no applicable customer price exists and the buyer has a price level, it looks up the level. An optional value-added-tax rate per level changes tax selection. The resolver also supports other pricing modes.
4. A child variant's price adjustment can be an absolute amount or a percentage of the parent price. Apply the adjustment in the configured parent price basis, inclusive or exclusive of tax. With multiple price levels, the combination can have a separate adjustment for each level. A weight adjustment adds to the parent weight.

## Service and acceptance cases

| Operation | Input and actor | Observable result |
| --- | --- | --- |
| Create catalogue entry | Product-create permission, reference, label and commercial attributes | The product REST creation route creates an ID. Reusing an existing reference in the same entity conflicts with the catalogue key. |
| Read a product listing with balances | Product-read permission, stock detail requested | Stock detail is included only for a caller with stock-read permission. |
| Select purchase offer | Vendor A offers 10 for 115 including 15% VAT. Vendor B offers a minimum of 20 at 11 tax-exclusive each, with 15% discount. | At 10, only A qualifies at 10 per unit before tax. At 20, B qualifies at 9.35 and wins the discounted unit-price comparison. |
| Store a service | A stockable service and an ordinary stockable product have the same transaction quantity | With service stock support disabled, only the product qualifies for a normal stock movement. |
