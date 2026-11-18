# Exemption labels, recoverable-only VAT and reported tax

The ERP keeps a numerical rate, a short source code, an optional exemption reason and a recoverable-only indicator. These support different decisions. Two invoices can have the same payable total and still have different stored tax amounts, rate groups and explanatory information.

| Value | Owner and interpretation | Observable consumer |
| --- | --- | --- |
| VAT liability and company exemption reason | Company configuration controls whether the issuer uses VAT. The company form offers a free-text exemption code when VAT is unused. A French company sees an example in the empty field. | A saved issuer reason belongs to the entity. An example shown in an empty input supplies no stored value. |
| Tax source code | A country tax-dictionary entry can associate a source code with a percentage. The selected line can retain that code. | VAT rate detail appends the line's source code to the numerical rate group when supplied. Geography-based turnover groups by numerical rate and product type. |
| Exemption reason on a dictionary row | A distinct optional field, up to 32 characters in the physical declaration, can hold a reason associated with that tax entry. | Administration exposes the field, the rate selector's cache contains it and the configuration service can return it. The standard VAT dictionary rows supply no values in this field. |
| Recoverable-only VAT | A separate flag on the dictionary row indicates the special treatment. The line pricing routine has a corresponding bit in its treatment flags. | The routine can calculate a tax value while excluding it from the amount charged to the customer. |
| Applied tax amounts | Invoice lines store net, main tax, gross, local component one and local component two. Monetary precision and line pricing rules apply before enquiry. | The rate report reads stored net and tax values. Its rate key looks at percentage and source code. Its aggregation has no dimension for dictionary exemption reason. |

The installed French dictionary includes an inactive 8.5% ordinary row and three inactive recoverable-only 8.5% rows with different codes and local-tax combinations. Routine active-rate selection excludes those four while their activation flags remain off. An operator explicitly configuring such a treatment, or a posted document retaining its original line facts, is a different source of evidence from the current active list. The ERP's rates are configuration data. They do not establish an issuer's qualification for a relief.

## Pricing from a net or gross basis

Assume one line, no discounts, no local taxes, two decimal places for amounts and ordinary decimal rounding. Use an 8.5% line configured with recoverable-only treatment. For a **net input** of 100, the line calculator uses a zero charged rate to obtain gross 100. It separately evaluates the nominal gross of 108.50 and subtracts the net base to store a tax value of 8.50. A normal line at the same percentage would have net 100, main tax 8.50 and gross 108.50. A zero-rate line would have net and gross of 100 and tax of zero.

For a **gross input** of 100, the special treatment keeps gross 100 and net 100. The nominal tax is instead calculated by comparing the fixed gross with the net it would imply under ordinary 8.5% pricing. The ordinary implied net rounds to 92.17, so stored main tax is 7.83. The choice of which price the operator supplied therefore affects the stored tax even where the customer sees the same 100 due.

For both special lines, taking the payable gross less the net gives zero. The main VAT rate report reads the stored 8.50 or 7.83 instead. For invoice-based sales the line contributes on the document date. For payment-based recognition the gross **actually payable** is the denominator for the allocation. On the net-input example, collecting 50 of 100 produces a nominal tax share of 4.25 under proportional presentation. A calculation that assumes the gross must be 108.50 produces a different result. Nondecimal rounding increments have a subsequent price-recomposition branch, so the arithmetic here assumes that option is unset.

A customer's invoice can retain a zero rate with a source code and a zero tax amount. The option to exclude zero VAT in reports tests the rate or stored tax amount. A nonempty reason by itself cannot preserve the zero/zero row through that filter. When the filter is disabled, separately coded zero-rate groups may remain visible as tax-base evidence. The shared rate reader does not look up today's dictionary reason to classify a past invoice.

The [regional rate dictionary](../localization/tax-rates.csv) lists the distributed rows.
