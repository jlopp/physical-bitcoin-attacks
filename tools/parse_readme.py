#!/usr/bin/env python3
"""Parse the attack table in README.md into attacks.json.

Most rows in the README put the entire summary in the label of the first link
(e.g. ``[Man robbed of $1.8M of ETH](url) [(original link)](url)``), so the
description is built by replacing each link with its *label* rather than by
deleting the link outright. Boilerplate labels such as "(original link)" are
left out of the description but are still kept in the "links" list.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "tools" / "raw_attacks.json"

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
# Same as LINK_RE, but also captures the optional single space in front of the
# link so a dropped boilerplate link doesn't leave a dangling space behind.
TEXT_LINK_RE = re.compile(r"([ \t]?)\[([^\]]*)\]\(([^)]*)\)")
DATE_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
# "    10|| Date |" style numbered-row prefixes.
ROW_PREFIX_RE = re.compile(r"^\s*\d+\s*\|\|")
# Markdown escapes for characters that would otherwise break a table cell.
ESCAPE_RE = re.compile(r"\\([_*`|~\[\]])")

# Link labels that carry no information; omitted from the description body
# (they are still recorded in the "links" list).
BOILERPLATE_LABELS = {
    "(original link)",
    "original link",
    "(en)",
    "en",
    "(more)",
    "more",
    "(link)",
    "link",
    "(source)",
    "source",
}

# Cells that are table chrome rather than data.
CHROME_CELLS = {"date", "victim", "location", "description"}


def parse_date(date_str):
    date_str = date_str.strip()
    m = DATE_RE.search(date_str)
    year = int(m.group(1)) if m else None
    return {"raw": date_str, "year": year}


def parse_links(text):
    return [{"label": html.unescape(label.strip()), "url": url.strip()}
            for label, url in LINK_RE.findall(text)]


def render_text(text):
    """Flatten markdown inline markup into the plain-text summary."""
    DROP = "\x00"  # marker for a boilerplate link removed from the body
    MARK = "\x01"  # marker for the start of a kept link label

    def replace_link(match):
        label = match.group(2).strip()
        if label.lower() in BOILERPLATE_LABELS:
            return DROP
        return match.group(1) + MARK + label

    out = TEXT_LINK_RE.sub(replace_link, text)
    # A dropped link between two sentences leaves them fused, e.g.
    # "... seized via Tether<drop> Ringleader was later arrested."
    out = re.sub(r"(?<=[\w)\]\"'])" + DROP + r"(?=\s+[A-Z])", ". ", out)
    # Elsewhere the drop just stood in for a space, or for nothing at all
    # when the next token is punctuation (", [forum post by victim](...)").
    out = re.sub(r"\s*" + DROP + r"\s*([,.;:!?])", r"\1", out)
    out = out.replace(DROP, " ")
    # A link label that starts a new sentence but was written in lower case,
    # e.g. "... were later arrested and convicted.<link> appeal judgment".
    out = re.sub(r"(?<=[.!?] )" + MARK + r"(\w)", lambda m: m.group(1).upper(), out)
    out = out.replace(MARK, "")
    out = ESCAPE_RE.sub(r"\1", out)
    out = html.unescape(out)
    # Dropped links can leave empty parens behind, e.g. "( )".
    out = re.sub(r"\(\s*\)", "", out)
    out = re.sub(r"\s+", " ", out)
    return out.strip(" |")


def is_row(line):
    """True for a table row, including numbered ones like "    10|| Date |"."""
    row = line.strip()
    if ROW_PREFIX_RE.match(row):
        return True
    return row.startswith("|")


def split_row(line):
    """Split a markdown table row into its cells, keeping intentional blanks."""
    row = line.strip()
    if ROW_PREFIX_RE.match(row):
        row = row.split("||", 1)[1].strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def is_chrome(cells):
    """True for the header row and the |:---:| separator row."""
    if len(cells) < 4:
        return True
    first = cells[0].strip().lower()
    if first in CHROME_CELLS:
        return True
    return set(cells[0]) <= {":", "-", " "}


def main():
    lines = README.read_text(encoding="utf-8").splitlines()
    attacks = []
    for line in lines:
        if not is_row(line):
            continue
        cells = split_row(line)
        if is_chrome(cells):
            continue
        date_cell, victim, location = cells[0], cells[1], cells[2]
        description = " ".join(cells[3:]) if len(cells) > 3 else ""
        attacks.append({
            "date": parse_date(date_cell),
            "victim": render_text(victim),
            "location": render_text(location),
            "description": render_text(description),
            "links": parse_links(description),
        })

    OUT.write_text(json.dumps(attacks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"parsed {len(attacks)} attacks -> {OUT}")
    empty = sum(1 for a in attacks if not a["description"])
    print(f"{len(attacks) - empty} described, {empty} without description")
    locs = sorted({a["location"] for a in attacks})
    print(f"{len(locs)} distinct locations:")
    for loc in locs:
        print(f"  {loc}")


if __name__ == "__main__":
    main()
