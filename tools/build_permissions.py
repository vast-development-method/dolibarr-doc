#!/usr/bin/env python3
"""Build the permission declaration index from the exact upstream commit in the module inventory."""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "permissions"
INVENTORY = ROOT / "docs" / "coverage" / "modules.json"
# Preserve quoted strings, including URLs, while removing comments without changing source line numbers.
LEXEME = re.compile(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/|\#[^\n]*""", re.S)
SLOT = re.compile(r"^\$this->rights\[(\$r|\d+)\]\[(\d+|self::KEY_\w+)\]\s*=\s*(.*);$")
FAMILY = re.compile(r"""\$this->rights_class\s*=\s*['"](\w+)['"];""")
INITIALIZE = re.compile(r"\$this->rights\s*=\s*(?:\[\]|array\(\))\s*;")
COUNTER = re.compile(r"\$r\s*=\s*(\d+)\s*;")
GUARD = re.compile(r"if\s*\((.*)\)\s*\{\s*$")
COLUMNS = ("descriptor", "id", "namespace", "first_level", "second_level", "default_grant",
           "english_label", "descriptor_label", "declaration_guard", "id_expression", "source")
MODULE_COLUMNS = ("descriptor", "declarations", "conditional", "namespace", "setup_hidden_when", "source")


def remove_comments(text):
    def replace(match):
        token = match[0]
        return token if token[0] in ("'", '"') else re.sub(r"[^\n]", " ", token)
    return LEXEME.sub(replace, text)


def permission_id(expression, module_id, counter):
    if expression.isdigit():
        return int(expression)
    expr = re.sub(r"\s+", "", expression).replace("$this->numero", str(module_id))
    if "$r" in expr:
        if counter is None:
            raise ValueError(f"Undefined counter in {expression}")
        expr = expr.replace("$r", str(counter))
    if re.fullmatch(r"\d+(?:\+\d+)*", expr):
        return sum(map(int, expr.split("+")))
    concat = re.fullmatch(r"(\d+)\.(\d+)", expr)
    if concat:
        return int(concat[1] + concat[2])
    formatted = re.fullmatch(r'(\d+)\.sprintf\("%02d",(\d+)\+(\d+)\)', expr)
    if formatted:
        return int(formatted[1] + f"{int(formatted[2]) + int(formatted[3]):02d}")
    raise ValueError(f"Unsupported permission ID expression: {expression}")


def literal(text):
    if text.isdigit():
        return int(text)
    translated = re.fullmatch(r"\$langs->trans\('([^']+)'\)", text)
    if translated:
        return translated[1]
    if len(text) >= 2 and text[0] in ("'", '"') and text[-1] == text[0]:
        return text[1:-1].replace("\\" + text[0], text[0]).replace("\\\\", "\\")
    raise ValueError(f"Unsupported permission field: {text}")


def extract(module, contents, source_url, constants, translations):
    code = remove_comments(contents)
    match = FAMILY.search(code)
    namespace = match[1] if match else module["key"].lower()
    groups = []
    scopes = []
    current = None
    counter = None
    for number, line in enumerate(code.splitlines(), 1):
        line = line.strip()
        if init := COUNTER.fullmatch(line):
            counter = int(init[1])
        elif line in ("$r++;", "++$r;") and counter is not None:
            counter += 1
        # Literal braces in strings are data, not block boundaries.
        structural = LEXEME.sub("''", line)
        condition = GUARD.fullmatch(line)
        for brace in re.finditer(r"[{}]", structural):
            if brace[0] == "{":
                scopes.append(condition[1] if condition else "")
            elif scopes:
                scopes.pop()
        if "$this->rights[" not in line and not re.search(r"\$this->rights\b", line):
            continue
        if INITIALIZE.fullmatch(line):
            continue
        field = SLOT.fullmatch(line)
        if not field:
            raise ValueError(f"Unsupported permissions declaration in {module['key']}:{number}: {line}")
        index, name, value = field.groups()
        slot = int(name) if name.isdigit() else constants[name.removeprefix("self::")]
        if slot == 0:
            current = {"id": permission_id(value, module["id"], counter), "expression": value,
                       "index": index, "line": number, "guards": [guard for guard in scopes if guard]}
            groups.append(current)
        elif current is None or current["index"] != index or slot in current:
            raise ValueError(f"Unexpected permission field order in {module['key']}:{number}")
        else:
            current[slot] = literal(value)
    rows = []
    for right in groups:
        if not right.get(1) or not right.get(4):
            raise ValueError(f"Missing label or first-level key in {module['key']}:{right['line']}")
        rid = right["id"]
        label = right[1]
        english = translations.get(f"Permission{rid}", translations.get(label, label))
        rows.append((module["key"], rid, right.get(6, namespace), right[4], right.get(5, ""),
                     right.get(3, 0), english, label, " && ".join(right["guards"]),
                     right["expression"], source_url + f"#L{right['line']}"))
    hidden = re.search(r"\$this->hidden\s*=\s*([^;]+);", code)
    return namespace, hidden[1] if hidden else "", rows


def csv_text(header, rows):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream_checkout", type=Path)
    parser.add_argument("--check", action="store_true", help="compare tracked files without writing")
    args = parser.parse_args()
    data = json.loads(INVENTORY.read_text())
    revision = data["commit"]
    upstream = args.upstream_checkout.resolve()
    actual = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if actual != revision:
        parser.error(f"Expected upstream {revision}, found {actual}")
    # Read Git objects so uncommitted changes to a checkout cannot silently change the reference.
    def at_commit(path):
        return subprocess.check_output(["git", "-C", str(upstream), "show", f"{revision}:{path}"]).decode()

    directory = data["descriptor_directory"]
    base = at_commit(directory + "/DolibarrModules.class.php")
    constants = {key: int(value) for key, value in re.findall(r"const (KEY_\w+)\s*=\s*(\d+);", base)}
    languages = subprocess.check_output(
        ["git", "-C", str(upstream), "ls-tree", "--name-only", "-r", revision, "htdocs/langs/en_US"], text=True)
    translations = {}
    for path in sorted(languages.splitlines()):
        if path.endswith(".lang"):
            for line in at_commit(path).splitlines():
                key, sep, value = line.partition("=")
                if sep:
                    translations.setdefault(key, value)
    permissions = []
    modules = []
    for module in data["modules"]:
        if not module["eligible"]:
            continue
        path = f"{directory}/mod{module['key']}.class.php"
        url = f"https://github.com/Dolibarr/dolibarr/blob/{revision}/{path}"
        namespace, hidden, rows = extract(module, at_commit(path), url, constants, translations)
        modules.append((module["key"], len(rows), sum(bool(row[8]) for row in rows), namespace, hidden, url))
        permissions.extend(rows)
    ids = [row[1] for row in permissions]
    if len(ids) != len(set(ids)):
        raise ValueError("Overlapping permission IDs need review before publishing")
    artifacts = {"declarations.csv": csv_text(COLUMNS, permissions),
                 "descriptors.csv": csv_text(MODULE_COLUMNS, modules)}
    for name, content in artifacts.items():
        path = OUTPUT / name
        if args.check:
            if not path.is_file() or path.read_bytes() != content.encode():
                parser.error(f"Reference differs: {path}")
        else:
            OUTPUT.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode())
    print(f"{len(permissions)} declarations across {len(modules)} eligible descriptors")


if __name__ == "__main__":
    main()
