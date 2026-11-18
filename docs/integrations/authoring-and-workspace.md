# Authoring, personal workspace and document output

The integration boundary determines what to persist. Text generation returns content to a form. A bookmark persists a navigation target. An IP lookup or avatar render enriches a view. An IPP print operation submits a job against an existing document. Keep these distinct from changing the underlying customer, invoice or project.

## AI-assisted authoring

The feature registry marks email and webpage generation, translation, summarisation, spelling correction, rephrasing and extra-field text generation as stable. Setup selects a service and model options. The editor sends instructions, a function and output format. The business operation can apply configured prefix/suffix prompts or defaults for its purpose. Plain-text requests remove markup from the instructions. For a quoted email or page the output can use HTML. The successful response supplies generated content to the form. Saving the resulting field or sending an email remains a separate user action.

| Business contract | Input or outcome |
| --- | --- |
| Generate a draft | Supply an enabled module, configured provider, supported text task, nonempty instructions and desired output format. The form uses distinct operation names, including `textrephraser` in the rephrasing request. |
| Handle failure | Empty instructions produce HTTP 400. Provider quota exhaustion is surfaced as 429. Other upstream failures are propagated where an error code is available. Preserve the operator's original text on error in a rebuild. |
| Feature availability | The feature registry labels document parsing experimental, and the assistant, MCP server and tool configuration tabs require an elevated feature level. They are outside the stable authoring contract. |

**Acceptance.** Request a plain-text summary and verify the returned text can be reviewed before any business document changes. Simulate provider quota exhaustion and verify the caller observes a distinguishable failure. The [authoring request schema](../../schemas/integrations/authoring-request.schema.json) uses business names and a positive-length instruction string. It covers the stable text operations above.

## Bookmarks, feeds and editors

| Capability | Record or input | Observable behaviour and acceptance |
| --- | --- | --- |
| Bookmarks | An entity-scoped title, URL, optional owner, display position and target behaviour | An ordinary user's list includes their own and shared bookmarks (owner empty or zero). A different user's private bookmark is omitted. An editor may delete their own bookmark. The separate delete permission allows broader deletion. Verify that a user's links retain their stored order when sorting by position. |
| External RSS | Administrator-configured feed URL per box, maximum items and refresh delay | The box requests a cached feed through the parser, supports RSS and Atom item structures, and caps the display count. The default box call uses 5 items and a 3,600-second cache delay. On refresh failure the box displays a status with the last fetch time when available. Verify the failure message independently of the ERP transaction records. |
| Rich-text editing | Calling form supplies field, content, toolbar, read-only setting and whether the field permits an enhanced editor | CKEditor is the default rich editor. The editor wrapper falls back to a plain textarea when the form disallows the enhancement or JavaScript/AJAX is unavailable. With the enhanced HTML editor, existing plain-text line breaks are converted for display. The enclosing form owns validation and persistence. |

## Telephony and display enrichment

| Capability | Inputs and authority | Observable result |
| --- | --- | --- |
| ClickToDial | Phone field, configured telephony URL pattern and optional per-user extension/settings. The user-specific URL takes precedence. | The phone formatter supplies a clickable telephony action. Substitution resolves the destination number and selected user settings. Completion of a call is determined by the telephony service. Verify the same contact can dial through the correct extension for two different users. |
| GeoIP MaxMind | A configured data file and an address. For a GeoIP2 Country database the reader uses its country lookup. For a City database it reads the embedded country. | Returns the country's ISO code on success and an empty result on a failed lookup. Treat this as inferred IP geography and retain the actual address on the party or transaction independently. |
| Gravatar | Enabled service, email address, absence of a local photo in the form fallback and permission from the calling form to use an external source | The fallback builds a URL from the SHA-256 hash of the trimmed, lowercased email and requested size. The remote service can supply an identicon. With an existing local image, the form renders its own file. Verify the two render paths for the same record. |

## Direct printing and receipt printing

Direct printing accepts an existing output file and its business module. The IPP driver selects a printer and copy count for the user, module and driver. If no preference matches it selects the configured default printer. If neither exists it returns a missing-default error. The driver resolves the file in the module's output directory and conveys a known document MIME type before submitting it to CUPS. Acceptance by the print server is observable earlier than physical printing. The administrative jobs view queries enabled drivers.

Receipt printing uses a printer record and a receipt template applied to the source business object. The service renders supported template tokens and reports device or template errors. Test by printing a posted invoice twice and checking the invoice ID, balance and stock ledger after the reprint. Only the output is duplicated. Terminal kitchen/order printing and settlement are described in [Point of sale](../commerce/point-of-sale.md).
