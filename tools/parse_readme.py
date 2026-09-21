#!/usr/bin/env python3
"""Parse the attack table in README.md into attacks.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "tools" / "raw_attacks.json"

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def parse_date(date_str):
    date_str = date_str.strip()
    m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", date_str)
    year = int(m.group(1)) if m else None
    return {"raw": date_str, "year": year}


def parse_links(text):
    return [{"label": label.strip(), "url": url.strip()}
            for label, url in LINK_RE.findall(text)]


def strip_links(text):
    return LINK_RE.sub("", text).strip()


def main():
    lines = README.read_text(encoding="utf-8").splitlines()
    attacks = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Handle numbered-row prefixes like "    10|| Date |"
        if "||" in line:
            line = line.split("||", 1)[1]
        cells = [c.strip() for c in line.split("|")]
        # cells: ['', date, victim, location, description, '']
        cells = [c for c in cells if c != ""] if cells and cells[0] == "" else cells
        if len(cells) < 4:
            continue
        date_cell, victim, location, description = cells[0], cells[1], cells[2], " ".join(cells[3:])
        if date_cell.lower() == "date" or set(date_cell) <= {":", "-", " "}:
            continue
        attacks.append({
            "date": parse_date(date_cell),
            "victim": strip_links(victim),
            "location": strip_links(location),
            "description": strip_links(description),
            "links": parse_links(description),
        })
    OUT.write_text(json.dumps(attacks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"parsed {len(attacks)} attacks -> {OUT}")
    locs = sorted({a["location"] for a in attacks})
    print(f"{len(locs)} distinct locations:")
    for l in locs:
        print(f"  {l}")


if __name__ == "__main__":
    main()
