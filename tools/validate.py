"""Validate portable contracts, coverage, links and optional release evidence."""
import argparse
import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DIALECT = "https://json-schema.org/draft/2020-12/schema"
SOURCE = re.compile(r"https://github\.com/Dolibarr/dolibarr/(blob|tree)/([^/\s)]+)(?:/([^\s)\]<>#\x22]+))?(?:#(L[0-9]+(?:-L[0-9]+)?))?")
INLINE = re.compile(r"\]\(([^\s()]+(?:\([^()\s]*\)[^\s()]*)*)\)")
DEFINITION = re.compile(r"^\[[^\]]+\]:\s*<?(\S+?)>?\s*$", re.M)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contracts():
    validators = {}
    outcomes = defaultdict(set)
    for path in sorted((ROOT / "schemas").rglob("*.schema.json")):
        schema = load(path)
        require(schema.get("$schema") == DIALECT, f"Unexpected dialect in {path}")
        Draft202012Validator.check_schema(schema)
        key = path.relative_to(ROOT / "schemas").as_posix().removesuffix(".schema.json")
        validators[key] = Draft202012Validator(schema, format_checker=FormatChecker())
    count = 0
    for path in sorted((ROOT / "examples").rglob("*.json")):
        match = re.fullmatch(r"(.+?)(?:--.+)?\.(valid|invalid)\.json", path.name)
        require(match is not None, f"Unlabelled example {path}")
        key = (path.parent.relative_to(ROOT / "examples") / match[1]).as_posix()
        require(key in validators, f"No matching schema for {path}")
        valid = match[2] == "valid"
        errors = list(validators[key].iter_errors(load(path)))
        require(valid == (not errors), f"{path.name} expected {match[2]}: {[e.message for e in errors]}")
        outcomes[key].add(valid)
        count += 1
    for key in validators:
        require(outcomes[key] == {True, False}, f"Missing positive or negative fixture for {key}")
    return len(validators), count


def coverage():
    directory = ROOT / "docs/coverage"
    catalogue = load(directory / "modules.json")
    mapping = load(directory / "guide-map.json")
    require(mapping["commit"] == catalogue["commit"] and mapping["release"] == catalogue["release"],
            "Guide map uses a different upstream release")
    modules, guide_entries = catalogue["modules"], mapping["modules"]
    require(len({m["id"] for m in modules}) == len(modules) == len({m["key"] for m in modules}),
            "Repeated descriptor or module ID in inventory")
    require(Counter(m["maturity"] for m in modules) == catalogue["maturity_counts"],
            "Incorrect inventory maturity counts")
    eligible = {m["key"] for m in modules if m["eligible"]}
    require(eligible == {m["key"] for m in modules if m["maturity"] == "stable"}, "Maturity/scope mismatch")
    require(len(guide_entries) == len(eligible) and {m["key"] for m in guide_entries} == eligible,
            "Guide map must cover each stable descriptor exactly once")
    for entry in guide_entries:
        require(entry["guides"] and entry["focus"].strip(), f"Missing mapping detail: {entry}")
        for target in entry["guides"]:
            require((ROOT / target).is_file(), f"{entry['key']} links to missing {target}")
    return catalogue


def markdown_paths():
    return [ROOT / "README.md", *(ROOT / "docs").rglob("*.md"), *(ROOT / "conformance").rglob("*.md")]


def check_local_links():
    count = 0
    for page in markdown_paths():
        body = page.read_text()
        for target in INLINE.findall(body) + DEFINITION.findall(body):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = (page.parent / unquote(url.path)).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), f"{page.relative_to(ROOT)}: missing {target}")
            count += 1
    return count


def verify_sources(checkout, catalogue):
    sha = catalogue["commit"]
    head = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    require(head == sha, f"Expected {sha}, found {head}")
    files = {p.name[3:-10] for p in (checkout / "htdocs/core/modules").glob("mod*.class.php")}
    require(files == {m["key"] for m in catalogue["modules"]}, "Upstream descriptor set differs")

    @lru_cache(maxsize=None)
    def line_count(path):
        with path.open("rb") as source:
            return sum(1 for _ in source)

    def check_location(path, start, end):
        require(path.is_file(), f"Missing source file {path}")
        require(1 <= start <= end <= line_count(path), f"Out-of-range lines {start}-{end} in {path}")

    refs = set()
    for path in [*markdown_paths(), ROOT / "docs/coverage/modules.json",
                 ROOT / "docs/permissions/declarations.csv", ROOT / "docs/permissions/descriptors.csv"]:
        for kind, rev, location, anchor in SOURCE.findall(path.read_text()):
            require(rev == sha, f"{path.name}: unpinned source {rev}")
            source = checkout / unquote(location).rstrip(".,")
            require(source.exists(), f"{path.name}: missing upstream path {location}")
            if anchor:
                ends = [int(n) for n in re.findall(r"\d+", anchor)]
                check_location(source, ends[0], ends[-1])
            refs.add((kind, rev, location, anchor))
    rows = 0
    for index in sorted((ROOT / "docs/reference").glob("*.csv")):
        with index.open(newline="") as handle:
            for row in csv.DictReader(handle):
                path = row["source_file"]
                if not path.startswith("htdocs/"):
                    path = "htdocs/install/mysql/tables/" + path
                line = int(row["line"])
                check_location(checkout / path, line, line)
                rows += 1
    return len(refs), rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, help="Local Dolibarr checkout of the pinned stable release")
    args = parser.parse_args()
    schema_count, example_count = contracts()
    catalogue = coverage()
    links = check_local_links()
    print(f"{schema_count} schemas, {example_count} fixture outcomes, {links} local links verified.")
    print(f"{len(catalogue['modules'])} module records, {catalogue['maturity_counts']['stable']} stable chapter mappings.")
    if args.upstream:
        refs, rows = verify_sources(args.upstream.resolve(), catalogue)
        print(f"{refs} distinct pinned references and {rows} indexed source locations verified.")


if __name__ == "__main__":
    main()
