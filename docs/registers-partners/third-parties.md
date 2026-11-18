# Third-party register

Customers, prospects, suppliers and other organisations share the `societe` record. One party can be both a customer and a supplier. The row key is `societe.rowid`. The default order is ascending `nom`. Party names can repeat, so two parties with the same name and different IDs remain distinct records. [Party records](../records/parties.md)

## Visibility, roles and assignments

The register checks third-party access and the party entity. A user linked to a party is restricted to its row ID. For an internal user, a selected party ID narrows the result to that party. In the general list an operator without the right to see all customers is restricted to their own sales assignments. Without the supplier-read grant, the query excludes a pure supplier whose `fournisseur = 1` and `client = 0`. It can retain a supplier who is also a customer or prospect, and an unclassified party.

| List or control | Selection |
| --- | --- |
| Customers | Default `search_type=1,3` selects customer and combined prospect/customer via `client`. |
| Prospects | Default `search_type=2,3` selects prospect and combined prospect/customer. |
| Point-of-sale selection | Default `search_type=1,2,3` includes all three commercial customer/prospect states. |
| Suppliers | `search_type=4` requires the independent `fournisseur` flag to equal one. |
| Neither | `search_type=0` requires both `client` and `fournisseur` to equal zero. |
| Representative `search_sale` | Tests assignments in `societe_commerciaux`, joined by `fk_soc` and searched by `fk_user`. Positive IDs select any named representative. A sole −2 selects no assignments. Mixed positive IDs and −2 admit selected or unassigned parties. Membership is tested by existence, so a second matching representative does not duplicate a party. |
| Customer and supplier categories | `search_category_customer_list` and `search_category_supplier_list` use `categorie_societe` and `categorie_fournisseur` respectively. Positive IDs select membership and −2 selects no membership in that family. Operator 0 requires all requested tests. Operator 1 accepts any. Applying filters in both families requires satisfaction of each family. A lone legacy `search_categ_cus` or `search_categ_sup` fills an otherwise empty corresponding list. |

A parent party is a left self-join on `societe.parent`. Country, organisation type, workforce band, state, region and sales follow-up status are left-joined for descriptive fields. Region resolves through the state. Active extra-field definitions add the party's custom-value row. A missing parent or dictionary entry ordinarily leaves the party visible until a filter requires that relation.

## Field and date filters

| Inputs | Binding |
| --- | --- |
| `search_id`, `search_nom`, `search_alias`, `search_nom_only`, `search_parent_name` | A positive ID applies a numeric test to `rowid`. With the alias column hidden, a name search examines both `nom` and `name_alias`. With the alias column shown, name and alias have independent tests. The name-only control always tests `nom`. Parent name searches the parent row. |
| `search_ref_ext`, `search_customer_code`, `search_supplier_code`, `search_account_customer_code`, `search_account_supplier_code` | Search `ref_ext`, `code_client`, `code_fournisseur`, `code_compta` and `code_compta_fournisseur` respectively. Commercial and accounting codes can identify different values on the same party. |
| `search_address`, `search_zip`, `search_town`, `search_state`, `search_region`, `search_country` | Address, postal code and town are party fields. State and region search their directory names. Country filters the party's `fk_pays` against selected IDs. |
| `search_email`, `search_noemail` | Email searches the party field. Suppression tests for an unsubscribe entry with empty group and an email equal to the supplied search email in the visible party entities. This second test uses the search literal across the query. It does not correlate each returned party to its own suppression row. |
| `search_phone`, `search_phone_mobile`, `search_fax`, `search_url`, `search_cti` | The first four search the corresponding party fields. Caller lookup removes non-digits and leading zeroes from the incoming number and searches the party's main phone field. |
| `search_idprof1` through `search_idprof6`, `search_vat`, `search_barcode` | The first three map to `siren`, `siret`, `ape`. The remaining three use `idprof4`, `idprof5`, `idprof6`. VAT searches `tva_intra`. Barcode filtering requires barcode support. |
| `search_status`, `search_price_level`, `search_type_thirdparty`, `search_staff`, `search_legalform` | Match status, `price_level`, `fk_typent`, `fk_effectif` and `fk_forme_juridique` by selected numeric values. A zero administrative status is a valid filter. The organisation type selector is independent of the customer/supplier role selector. |
| `search_level`, `search_stcomm`, `search_import_key`, `search_note_public`, `search_note_private` | Prospect level uses a list of string codes, commercial status uses numeric IDs. Import key, public note and private note each search their own field. |
| Creation and modification bounds | `search_date_creation_start*` and `search_date_creation_end*` compare `datec`. The corresponding `search_date_modif_*` controls compare `tms`. Each uses year, month and day, inclusive from the lower day's start to the upper day's final second. |

The default quick search examines name, alias, commercial and accounting codes, zip, town, email, URL, VAT identity, the first three professional IDs, phone, mobile and fax. It adds professional IDs four through six when their geographic labels are defined, and barcode when enabled. Configuration can replace this list and extensions may add or replace fields. A name-only search and quick search consequently have different populations.

## Worked visibility and tag intersection

| ID | Party roles | Customer categories | Representatives |
| ---: | --- | --- | --- |
| 31 | Customer and supplier | Retail, North | 8, 9 |
| 32 | Prospect | North | 8 |
| 33 | Supplier | None | 9 |
| 34 | Neither | None | None |

All are in one visible entity. A reader permitted all customers but lacking supplier-read sees 31, 32 and 34 in the general list. Selecting Customers leaves 31. Selecting Representatives 8 and 9 in the general list leaves 31 and 32 exactly once each. Requiring both Retail and North leaves 31. Accepting either category returns 31 and 32. A supplier-authorised reader with full party visibility gets 31 and 33 from the Suppliers view. These counts represent parties, independent of the number of invoices, contacts or representatives attached.

The optional count uses the filtered joins before paging. A new search or a negative page starts at zero. The query fetches one look-ahead row. With single-result direct opening enabled, a single quick-search or caller-lookup hit may open its card. When customer/supplier cards are preferred, the commercial customer/prospect branch is tested first, so a dual-role party opens there before the supplier branch is considered.
