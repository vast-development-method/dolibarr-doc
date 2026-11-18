# Moving sale lines and dividing tender

A restaurant table can split the goods being invoiced, split the means of payment, or do both. Moving a sale line changes which invoice owns the charge. Accepting another tender adds an allocation against an existing invoice. Those operations have different effects on customer balances, stock and receipts.

## Moving whole lines between drafts

The terminal identifies a draft by a provisional reference incorporating the terminal and sales place. Each terminal also has a provisional split destination. The split operation first loads that destination. If it does not exist, it creates a new draft for the terminal's configured counter customer, using the current date, register source, terminal number and selected invoice entity. A terminal with no configured counter customer cannot create that destination.

The operator identifies one existing line. The transfer changes its invoice parent only if the line currently belongs to the expected provisional source for that terminal, the source invoice is draft and its entity is accessible. The original line identity, quantity, unit price and stored tax amounts travel with the line. There is no quantity parameter on this operation. Selecting a line of three coffees transfers all three. To charge the coffees separately they must first be represented on distinct lines or otherwise divided before the transfer.

Returning a line uses the terminal's split draft as source and the chosen sales place as destination. Selecting the split place itself for the return resolves to place 0. Both draft headers are refreshed and their totals recalculated. The handler creates the destination before changing the line parent and does not enclose all those steps in one outer transaction. A destination draft can therefore exist after a line failed to move. Looking up the line's owner and both draft totals distinguishes a completed transfer from an empty destination.

## One bill, several tenders

The terminal resolves a bank or cash account for the chosen payment mode, or accepts an explicitly selected one when enabled. An immediate tender with banking enabled requires a usable account. On a sale, a positive tender below the amount due is allocated at the tendered amount. Entering zero, a negative value, or a value greater than the positive outstanding balance selects the entire outstanding amount. Cash change can be retained on the payment record independently of the amount allocated. The handler submits allocations in the company currency.

A delayed tender can validate the sale and set configured credit terms without creating a payment. On a subsequent immediate tender, a successful payment operation creates a payment, links it to the invoice, adds its bank posting and recalculates the outstanding amount. At zero due the handler requests paid classification and records the selected payment method. A payment method stored on the invoice cannot explain a bill paid by multiple methods. The individual payment allocations show the actual composition.

A stock-enabled terminal configured to post stock on billing first validates the draft. For batch-managed goods the separate stock branch is conditional on the invoice having been draft on entry. A second tender against an already validated bill therefore should be traced from the new payment and bank records. It does not represent a second issue of the same goods. Payment or bank errors enter the outer error handling. A failed paid-status update is treated differently by this handler, so finding a committed allocation and a zero balance warrants reading the invoice's stored classification separately.

## Refunds at the counter

When the cashier validates a sale with a negative gross total, the register converts it to a credit note. This route looks for the highest-ID eligible earlier non-credit bill of the same customer in the accessible invoice entities with status at least validated. It attaches that source before proceeding. The cashier recording a return against a shared counter customer should therefore inspect which invoice was selected. The customer's latest sale can be different from the sale of the returned item.

The dedicated credit action starts from a particular invoice and follows its lines. Its handling of previously credited lines and of quantities, signed net/tax/gross amounts, parent lines, warehouse and batch information makes it distinct from entering a new negative sale. Returning goods and paying money also remain separate accounting facts. Trace the new credit document, stock entry where configured, payment and bank line to explain the refund.

## Worked table

A draft contains one food line for 40.00 and a grouped drinks line for 24.00. Moving the drinks to the terminal's split draft leaves gross amounts of 40.00 and 24.00. The food customer pays 15.00 cash and 25.00 by card. That original invoice has two allocations and zero remaining due. The drinks customer hands over 30.00 in cash for their separate bill. The allocation is 24.00 and the change is 6.00. The register-control figures from these transactions are cash 39.00 and card 25.00. The terminal has issued two invoices, moved one sale line and recorded three tenders.
