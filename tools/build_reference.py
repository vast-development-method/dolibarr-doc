"""Build review indexes from the exact source release used by the blueprint."""
import argparse
import csv
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "docs" / "reference"
INVENTORY = ROOT / "docs" / "coverage" / "modules.json"

# Names are logical table names without the deployment-specific prefix.
# Pinning each selection avoids importing abandoned tables or an external module
# simply because its DDL happens to ship in the installation directory.
TABLES = {
    "platform": """const rights_def user usergroup usergroup_rights user_rights usergroup_user user_param user_alert
        default_values element_contact element_element extrafields cronjob blockedlog events webhook_history webhook_target
        oauth_state oauth_token c_action_trigger""",
    "parties-sales": """societe societe_rib socpeople societe_contacts societe_commerciaux societe_remise
        societe_remise_except propal propaldet commande commandedet expedition expeditiondet expeditiondet_batch
        expedition_package c_payment_term c_shipment_mode c_propalst c_prospectlevel c_type_contact partnership""",
    "catalogue-stock": """product product_association product_attribute product_attribute_value product_attribute_combination
        product_attribute_combination2val product_attribute_combination_price_level product_batch product_lot product_stock
        stock_mouvement stocktransfer_stocktransfer stocktransfer_stocktransferline entrepot product_warehouse_properties
        inventory inventorydet product_price product_price_by_qty product_customer_price product_customer_price_log
        product_thirdparty c_units c_product_nature c_productbatch_qcstatus""",
    "purchasing": """supplier_proposal supplier_proposaldet commande_fournisseur commande_fournisseurdet commande_fournisseur_log
        reception receptiondet_batch product_fournisseur_price product_fournisseur_price_log facture_fourn facture_fourn_det
        facture_fourn_rec facture_fourn_det_rec paiementfourn paiementfourn_facturefourn c_incoterms""",
    "cash-and-invoicing": """facture facturedet facture_rec facturedet_rec paiement paiement_facture bank bank_account bank_url
        bank_import bank_record bank_record_link bordereau_cheque pos_cash_fence takepos_floor_tables multicurrency multicurrency_rate
        prelevement prelevement_bons prelevement_demande prelevement_lignes prelevement_rejet c_paiement c_invoice_subtype
        c_tva c_revenuestamp tva localtax chargesociales paiementcharge payment_various payment_vat""",
    "ledger-capital": """accounting_account accounting_fiscalyear accounting_journal accounting_system accounting_bookkeeping
        accounting_bookkeeping_tmp accounting_bookkeeping_piece accounting_balance_snapshot accounting_analytic_axis
        accounting_analytic_account accounting_analytic_distribution asset asset_model asset_depreciation asset_accountancy_codes_economic
        asset_accountancy_codes_fiscal asset_depreciation_options_economic asset_depreciation_options_fiscal loan loan_schedule
        payment_loan c_asset_disposal_type""",
    "projects-production": """bom_bom bom_bomline mrp_mo mrp_production workstation_workstation workstation_workstation_resource
        workstation_workstation_usergroup projet projet_task element_time actioncomm actioncomm_resources actioncomm_reminder
        resource element_resources eventorganization_conferenceorboothattendee c_lead_status""",
    "people-service": """holiday holiday_config holiday_users holiday_logs c_holiday_types c_hrm_public_holiday expensereport
        expensereport_det expensereport_rules expensereport_ik payment_expensereport paymentexpensereport_expensereport
        salary payment_salary user_employment hrm_job hrm_job_user hrm_evaluation hrm_evaluationdet hrm_skill hrm_skilldet hrm_skillrank
        recruitment_recruitmentjobposition recruitment_recruitmentcandidature contrat contratdet fichinter fichinterdet fichinter_rec
        fichinterdet_rec ticket knowledgemanagement_knowledgerecord c_ticket_type c_ticket_category c_ticket_severity c_ticket_resolution""",
    "community-and-content": """adherent adherent_type subscription don payment_donation website website_page
        opensurvey_sondage opensurvey_formquestions opensurvey_user_formanswers opensurvey_user_studs opensurvey_comments
        mailing mailing_cibles mailing_advtarget mailing_unsubscribe notify notify_def notify_def_object
        emailcollector_emailcollector emailcollector_emailcollectoraction emailcollector_emailcollectorfilter
        c_email_senderprofile c_email_templates""",
    "documents-and-tools": """categorie categorie_product categorie_contact categorie_project categorie_member categorie_warehouse
        ecm_directories ecm_files document_model import_model export_model bookmark printing printing_receipt printing_receipt_template
        ai_request_log user_clicktodial c_barcode_type c_socialnetworks""",
}


def write_csv(path, headings, rows):
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(headings)
        writer.writerows(rows)


# These compatibility columns have an explicit successor or a retired purpose.
# Other physical fields stay visible even when an old DDL comment disputes their use.
OMIT_COLUMNS = {
    "blockedlog": {"certified", "actionrefisunique", "signature_backward"},
    "oauth_token": {"token"},
    "socpeople": {"no_email"},
    "propal": {"price", "remise_percent", "remise_absolue", "remise"},
    "facture": {"remise_percent", "remise_absolue", "remise"},
    "facturedet": {"remise", "price"},
    "inventorydet": {"qty_regulated"},
    "supplier_proposal": {"remise_percent", "remise_absolue", "remise"},
    "facture_rec": {"remise", "remise_percent", "remise_absolue", "vat_src_code"},
    "facturedet_rec": {"price"},
    "expensereport": {"paid", "integration_compta"},
    "salary": {"num_payment"},
    "don": {"country"},
}


def read_table(path, table):
    rows = []
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        code = line.partition("--")[0]
        text = code.strip().rstrip(",")
        if not text or text.startswith(("(", ")")) or re.match(
            r"^(create|primary|unique|constraint|index|key|engine)\b", text, re.I
        ):
            continue
        field = re.fullmatch(r"`?(\w+)`?\s+([\w]+(?:\s*\([^)]*\))?)(.*)", text)
        if not field:
            raise ValueError(f"Unrecognized declaration {path.name}:{line_no}: {text}")
        name, sql_type, tail = field.groups()
        if name in OMIT_COLUMNS.get(table, set()):
            continue
        if re.search(r"\bUNSIGNED\b", tail, re.I):
            sql_type += " unsigned"
        primary = bool(re.search("PRIMARY KEY", tail, re.I))
        default = re.search(r"\bDEFAULT\s+('[^']*'|[^\s,]+)", tail, re.I)
        rows.append((name, sql_type.lower(), "required" if primary or re.search("NOT NULL", tail, re.I)
                     else "nullable", default[1] if default else "", "primary" if primary else "", line_no))
    return rows


def build_tables(upstream):
    directory = upstream / "htdocs/install/mysql/tables"
    definitions = {p.name.split(".")[0].split("-")[0][4:]: p for p in directory.glob("llx_*.sql")
                   if ".key." not in p.name}
    constraints = []
    tables_seen = set()
    for area, selection in TABLES.items():
        rows = []
        for table in selection.split():
            if table in tables_seen:
                raise ValueError(f"Repeated table {table}")
            tables_seen.add(table)
            path = definitions[table]
            declared = re.search(r"^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?llx_(\w+)", path.read_text(), re.I | re.M)
            if not declared:
                raise ValueError(f"Missing table declaration in {path.name}")
            columns = read_table(path, declared[1])
            rows.extend((declared[1], *c[:-1], path.name, c[-1]) for c in columns)
            key_file = path.with_suffix(".key.sql")
            if key_file.is_file():
                constraints.extend(read_keys(key_file))
        write_csv(CATALOGUE / (area + ".csv"),
                  ("table", "field", "storage_type", "nullability", "default_expression",
                   "inline_key", "source_file", "line"), rows)
    write_csv(CATALOGUE / "relationships.csv", ("table", "kind", "fields", "references_table",
              "references_fields", "source_file", "line"), constraints)


def read_keys(path):
    """Index the pinned DDL's single-line ALTER statements for FK/unique/PK."""
    keys = []
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.partition("--")[0].strip()
        declaration = re.match(r"ALTER\s+TABLE\s+llx_(\w+)\b", line, re.I)
        if not declaration:
            continue
        table = declaration[1]
        foreign = re.search(r"FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+llx_(\w+)\s*\(([^)]+)\)", line, re.I)
        unique = re.search(r"\b(UNIQUE(?:\s+(?:INDEX|KEY))?|PRIMARY\s+KEY)\s*(?:\w+\s*)?\((.+)\)", line, re.I)
        if foreign:
            keys.append((table, "foreign", *[i.strip() for i in foreign.groups()], path.name, number))
        elif unique:
            keys.append((table, "unique" if "UNIQUE" in unique[1].upper() else "primary",
                         unique[2].strip(), "", "", path.name, number))
        elif re.search(r"UNIQUE|PRIMARY|FOREIGN", line, re.I):
            raise ValueError(f"Unrecognized key at {path}:{number}")
    return keys


def signature_parameters(text, offset):
    """Read the outer parameter list, allowing nested calls/arrays and quoted defaults."""
    depth = 1
    parameters = []
    token = re.compile(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|\$(\w+)|[()]""")
    for match in token.finditer(text, offset):
        if match[1] and depth == 1:
            parameters.append(match[1])
        elif match[0] == "(":
            depth += 1
        elif match[0] == ")":
            depth -= 1
            if not depth:
                return " ".join(parameters)
    raise ValueError("Unterminated API method parameter list")


def build_services(upstream):
    rows = []
    base = upstream / "htdocs"
    named_public = re.compile(r"^\s*public\s+function\s+(\w+)\s*\(", re.M)
    for path in sorted(base.rglob("api_*.class.php")):
        descriptor_path = path.relative_to(upstream).as_posix()
        if any(p in path.relative_to(base).parts for p in ("modulebuilder", "zapier", "includes")):
            continue
        if path.name in {"api_access.class.php", "api_login.class.php"}:
            continue
        body = path.read_text()
        # Preserve offsets for permalinks and PHPDoc lookup while removing code
        # samples or retired handlers that are inside strings and comments.
        lexical = re.compile(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\n]*|\#[^\n]*""", re.S)
        mask = lexical.sub(lambda item: re.sub(r"[^\n]", " ", item[0]), body)
        for match in named_public.finditer(mask):
            name = match[1]
            if name.startswith("_"):
                continue
            start_of_method = body.rfind("\n", 0, match.start(1)) + 1
            comment_end = body.rfind("*/", 0, start_of_method)
            doc = ""
            if comment_end >= 0 and not body[comment_end + 2:start_of_method].strip():
                doc = body[body.rfind("/**", 0, comment_end):comment_end]
            if re.search(r"@deprecated\b", doc, re.I):
                continue
            route = re.search(r"@url[^\S\n]+(GET|POST|PUT|PATCH|DELETE)\b([^\n]*)", doc, re.I)
            rows.append((descriptor_path, name, signature_parameters(body, match.end()),
                         route[1].upper() if route else "", route[2].strip() if route else "",
                         body.count("\n", 0, match.start(1)) + 1))
    write_csv(CATALOGUE / "service-methods.csv",
              ("source_file", "method", "parameter_names", "annotated_verb", "annotated_route", "line"), rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream_checkout", type=Path)
    root = parser.parse_args().upstream_checkout.resolve()
    expected = json.loads(INVENTORY.read_text())["commit"]
    revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if revision != expected:
        parser.error(f"Expected upstream commit {expected}, found {revision}")
    changes = subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=normal", "--", "htdocs"],
        text=True
    )
    if changes:
        parser.error("The upstream htdocs tree has local edits; regenerate from a clean pinned checkout")
    CATALOGUE.mkdir(exist_ok=True)
    build_tables(root)
    build_services(root)


if __name__ == "__main__":
    main()
