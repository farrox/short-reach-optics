#!/usr/bin/env python3
"""
Export sections/references.tex into a web-native bibliography Markdown page.

Writes/replaces the References chapter under docs/ so HTML readers do not need
the PDF for supporting sources. Source of truth remains references.tex.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from html import escape

BOOK_DIR = os.path.dirname(os.path.abspath(__file__))
REFS_TEX = os.path.join(BOOK_DIR, "sections", "references.tex")
CITEURLS = os.path.join(BOOK_DIR, "sections", "citeurls.tex")
ACCESS_DATE = "2026-07-25"

SECTION_ORDER = [
    ("Standards and MSAs", "standards"),
    ("Peer-reviewed papers", "papers"),
    ("Books and foundational references", "books"),
    ("Reliability and manufacturing standards", "reliability"),
    ("Vendor datasheets", "datasheets"),
    ("Vendor announcements and demonstrations", "announcements"),
    ("Public deployment disclosures", "deployment"),
    ("Research roadmaps", "roadmaps"),
    ("Other sources", "other"),
]


def parse_citeurls() -> dict[str, str]:
    urls: dict[str, str] = {}
    if not os.path.exists(CITEURLS):
        return urls
    text = open(CITEURLS, encoding="utf-8").read()
    for m in re.finditer(r"\\defciteurl\{([^}]+)\}\{([^}]+)\}", text):
        urls[m.group(1)] = m.group(2)
    for m in re.finditer(
        r"\\defciteurllocal\{([^}]+)\}\{[^}]+\}\{([^}]+)\}", text
    ):
        urls[m.group(1)] = m.group(2)
    return urls


def strip_tex(s: str) -> str:
    """Lightweight TeX → plain/Markdown for bibliography lines."""
    s = s.replace("\\&", "&").replace("\\%", "%")
    s = s.replace("\\,", " ").replace("~", " ")
    s = s.replace("\\emph{", "*").replace("\\textit{", "*")
    s = s.replace("\\textbf{", "**").replace("\\texttt{", "`")
    # Bare commands without arguments
    s = re.sub(
        r"\\(?:newblock|noindent|raggedright|centering|par|bigskip|medskip|smallskip)\b\s*",
        " ",
        s,
    )
    # \href{url}{text} and \citehref{key}{text}
    s = re.sub(
        r"\\href\{([^}]+)\}\{([^}]*)\}",
        lambda m: f"[{m.group(2)}]({m.group(1)})",
        s,
    )
    s = re.sub(
        r"\\citehref\{[^}]+\}\{([^}]*)\}",
        r"\1",
        s,
    )
    # Nested-ish one-arg macros (repeat for shallow nesting)
    for _ in range(3):
        s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# Manual overrides run before keyword heuristics (bibkey -> (section_id, source_type)).
# Keep Miller / Sackinger in books even when abstracts mention IEEE journals.
CATEGORY_OVERRIDES: dict[str, tuple[str, str]] = {
    "miller2009": ("books", "research"),
    "miller2017": ("books", "research"),
    "sackinger2018": ("books", "research"),
}


def classify(key: str, short: str, body: str) -> tuple[str, str]:
    """Return (section_id, source_type_label)."""
    if key in CATEGORY_OVERRIDES:
        return CATEGORY_OVERRIDES[key]
    blob = f"{key} {short} {body}".lower()

    if any(
        x in blob
        for x in (
            "gr-468",
            "gr468",
            "jesd",
            "telcordia",
            "hast",
            "iec 61300",
            "iec61300",
        )
    ):
        return "reliability", "standard"

    if any(
        x in blob
        for x in (
            "ieee",
            "oif",
            "cei-",
            "cmis",
            "msa",
            "802.3",
            "802.1",
            "itu-t",
            "ibta",
            "uelink",
            "ualink",
            "uec",
        )
    ) or key.startswith(
        ("ieee", "oif", "cei", "cmis", "elsfp", "lpo", "cwwdm")
    ):
        stype = "draft" if "draft" in blob or "ballot" in blob else "standard"
        return "standards", stype

    if any(
        x in blob
        for x in ("wiley", "cambridge", "springer", "oxford", "säckinger", "sackinger")
    ):
        return "books", "research"

    if any(
        x in blob
        for x in (
            "datasheet",
            "data sheet",
            "product brief",
            "gn183",
            "tn147",
        )
    ):
        return "datasheets", "production datasheet"

    if any(
        x in blob
        for x in (
            "announcement",
            "unveil",
            "press release",
            "demonstration",
            "demo",
            "booth",
            "ofc 2026 demo",
        )
    ):
        stype = "demonstration" if "demo" in blob or "demonstration" in blob else "vendor announcement"
        return "announcements", stype

    if any(x in blob for x in ("deployment", "deployed", "in production at", "hyperscaler")):
        return "deployment", "deployment disclosure"

    if any(x in blob for x in ("roadmap", "framework", "study group", "cfi", "white paper roadmap")):
        return "roadmaps", "roadmap"

    if any(
        x in blob
        for x in (
            "arxiv",
            "nature",
            "journal",
            "photonics",
            "ofc",
            "ecoc",
            "proceedings",
            "jlt",
            "optics express",
        )
    ):
        return "papers", "research"

    return "other", "research"


def parse_bibitems(tex: str) -> list[dict]:
    # Drop comments
    lines = []
    for line in tex.splitlines():
        if line.lstrip().startswith("%"):
            continue
        lines.append(line)
    tex = "\n".join(lines)

    m = re.search(
        r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}",
        tex,
        re.DOTALL,
    )
    if not m:
        return []
    body = m.group(0)
    parts = re.split(r"\\bibitem", body)[1:]
    entries = []
    for part in parts:
        hm = re.match(
            r"\[([^\]]*)\]\{([^}]+)\}(.*)",
            part,
            re.DOTALL,
        )
        if not hm:
            continue
        short, key, rest = hm.group(1), hm.group(2), hm.group(3)
        # Stop before next would-be (already split)
        rest = rest.strip()
        # Year from short label
        ym = re.search(r"\((\d{4}(?:--\d{2,4})?)\)", short)
        year = ym.group(1) if ym else ""
        section_id, source_type = classify(key, short, rest)
        # Extract first URL if present
        url_m = re.search(r"\\href\{([^}]+)\}", rest)
        url = url_m.group(1) if url_m else ""
        entries.append(
            {
                "key": key,
                "short": strip_tex(short),
                "year": year,
                "body": strip_tex(rest),
                "section": section_id,
                "source_type": source_type,
                "url": url,
            }
        )
    return entries


def render_markdown(entries: list[dict], citeurls: dict[str, str]) -> str:
    by_sec: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_sec[e["section"]].append(e)

    lines = [
        "---",
        "layout: default",
        'title: "References"',
        "---",
        "",
        "# References",
        "",
        "Complete bibliography for *Short-Reach Optics for AI Compute*.",
        "Source of truth is `sections/references.tex` (same entries as the PDF).",
        f"Volatile web sources: access date **{ACCESS_DATE}** unless a revision date is stated in the entry.",
        "",
        "Source-type labels: **standard**, **draft**, **research**, **production datasheet**,",
        "**demonstration**, **vendor announcement**, **roadmap**, **deployment disclosure**,",
        "**editorial inference**.",
        "",
        "Architectural arguments belong in the chapters; entries below are supporting sources.",
        "",
    ]

    for title, sid in SECTION_ORDER:
        group = by_sec.get(sid, [])
        if not group:
            continue
        lines.append(f"## {title}")
        lines.append("")
        for e in sorted(group, key=lambda x: (x["year"] or "9999", x["short"].lower())):
            url = e["url"] or citeurls.get(e["key"], "")
            label = e["short"] or e["key"]
            anchor = f"ref-{e['key']}"
            head = f'<a id="{escape(anchor)}"></a>**{escape(label)}**'
            lines.append(head)
            lines.append("")
            meta = f"*Source type:* {e['source_type']}"
            if e["year"]:
                meta += f" · *Date:* {e['year']}"
            if url and any(
                x in e["source_type"]
                for x in ("announcement", "demonstration", "roadmap", "deployment", "draft")
            ):
                meta += f" · *Accessed:* {ACCESS_DATE}"
            lines.append(meta)
            lines.append("")
            body = e["body"]
            if url and url not in body:
                lines.append(f"{body} ([link]({url}))")
            else:
                lines.append(body)
            lines.append("")
            lines.append(f'<span class="bibkey">`{e["key"]}`</span>')
            lines.append("")
            lines.append("---")
            lines.append("")

    # Endnotes / clarifications placeholder section
    lines.append("## Endnotes and worked clarifications")
    lines.append("")
    lines.append(
        "Chapter sidenotes and inline clarifications remain in the chapter HTML pages."
    )
    lines.append(
        "This page holds bibliographic sources only; interpretive arguments stay with the teaching text."
    )
    lines.append("")
    return "\n".join(lines)


def find_refs_filename(docs_dir: str) -> str:
    for name in os.listdir(docs_dir):
        if name.startswith("ch") and name.endswith(".md") and "reference" in name:
            return os.path.join(docs_dir, name)
    return os.path.join(docs_dir, "ch15-references.md")


def main() -> int:
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BOOK_DIR, "../../docs")
    docs_dir = os.path.abspath(docs_dir)
    tex = open(REFS_TEX, encoding="utf-8").read()
    citeurls = parse_citeurls()
    entries = parse_bibitems(tex)
    if not entries:
        print("ERROR: no bibitems parsed", file=sys.stderr)
        return 1
    md = render_markdown(entries, citeurls)
    out = find_refs_filename(docs_dir)
    # Preserve nav footer from existing page if present
    nav = ""
    if os.path.exists(out):
        old = open(out, encoding="utf-8").read()
        m = re.search(r"(<nav class=\"chapter-nav\">.*?</nav>)", old, re.DOTALL)
        if m:
            nav = "\n" + m.group(1) + "\n"
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
        if nav:
            f.write(nav)
    print(f"  Wrote {len(entries)} bibliography entries → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
