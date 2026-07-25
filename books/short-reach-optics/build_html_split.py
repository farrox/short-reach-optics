#!/usr/bin/env python3
"""
Split the full pandoc Markdown output into per-chapter pages
with Jekyll front matter and navigation links.
"""
from __future__ import annotations

import os
import re
import sys

DOCS_DIR = sys.argv[1] if len(sys.argv) > 1 else "../../docs"
MD_FILE = ".build/full_book.md"

# Visible HTML titles for appendix chapters. Filenames keep chN-… slugs.
APPENDIX_TITLES = {
    "One-week optical systems interview review": ("A", "One-week optical systems interview review"),
    "Thirty-second interview frameworks": ("B", "Thirty-second interview frameworks"),
    "Engineering decision trees": ("C", "Engineering decision trees"),
    "Abbreviations and terminology": ("D", "Abbreviations and terminology"),
    "Abbreviations": ("D", "Abbreviations and terminology"),
}


def slugify(title: str) -> str:
    """Turn a chapter title into a filename slug."""
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def display_meta(num: str, title: str) -> tuple[str, str, str]:
    """
    Return (file_num, display_prefix, display_title).
    Appendices keep numeric file slugs but show Appendix A/B/C/D in titles.
    """
    if title in APPENDIX_TITLES:
        letter, clean = APPENDIX_TITLES[title]
        return num, f"Appendix {letter}", clean
    # Pandoc may already emit "A One-week…" after a future numbering fix
    m = re.match(r"^([A-D])\s+(.+)$", title)
    if m:
        letter, clean = m.group(1), m.group(2).strip()
        if clean in APPENDIX_TITLES or any(
            clean == v[1] for v in APPENDIX_TITLES.values()
        ):
            return num, f"Appendix {letter}", clean
    return num, f"Ch {num}", title


def split_chapters(content: str) -> list[tuple[str, str, str]]:
    """
    Split Markdown content by H1 (# ...) headings.
    Returns list of (number, title, body) tuples.
    The TOC block (before first H1) is discarded from chapters.
    """
    # Find all H1 headings (lines starting with single #)
    pattern = re.compile(r"^# (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))

    if not matches:
        return [("0", "Full Book", content)]

    chapters = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end]
        # Extract chapter number from title like "1 Why the interconnect matters"
        num_match = re.match(r"^(\d+)\s+", title)
        if num_match:
            num = num_match.group(1)
            clean_title = title[num_match.end():]
        else:
            num = str(i)
            clean_title = title
        chapters.append((num, clean_title, body))

    return chapters


def write_index(chapters: list[tuple[str, str, str]], docs_dir: str):
    """Write the index.md with links to all chapters."""
    lines = [
        "---",
        "layout: default",
        'title: "Table of Contents"',
        "---",
        "",
        "# Short-Reach Optics for AI Compute",
        "",
        "*From First Principles to the State of the Art: Energy, Lasers, IM/DD, WDM, and Validation*",
        "",
        "**Ed (Ehsan) Shah Hosseini**",
        "",
        "---",
        "",
        "## Chapters",
        "",
    ]

    for num, title, _ in chapters:
        slug = slugify(title)
        filename = f"ch{num}-{slug}"
        _, prefix, display_title = display_meta(num, title)
        if prefix.startswith("Appendix"):
            lines.append(f"- [**{prefix}.** {display_title}]({filename})")
        else:
            lines.append(f"- [**{num}.** {display_title}]({filename})")

    lines.extend([
        "",
        "---",
        "",
        "*This is the online study-guide version. See the PDF for full figures and bibliography.*",
        "",
    ])

    path = os.path.join(docs_dir, "index.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Written: {path}")


def write_chapter(
    num: str, title: str, body: str, docs_dir: str,
    prev_link: str | None, next_link: str | None
):
    """Write a single chapter .md file with front matter and nav."""
    slug = slugify(title)
    filename = f"ch{num}-{slug}.md"
    _, prefix, display_title = display_meta(num, title)

    # Rewrite H1 to the visible appendix/chapter title
    body = re.sub(
        r"^# .+$",
        f"# {prefix}: {display_title}" if prefix.startswith("Appendix")
        else f"# {num} {display_title}",
        body,
        count=1,
        flags=re.MULTILINE,
    )

    # Build navigation
    nav_lines = []
    nav_lines.append("")
    nav_lines.append('<div class="nav-links">')
    if prev_link:
        nav_lines.append(f'  <a href="{prev_link}">&larr; Previous</a>')
    else:
        nav_lines.append("  <span></span>")
    nav_lines.append('  <a href="./">Table of Contents</a>')
    if next_link:
        nav_lines.append(f'  <a href="{next_link}">Next &rarr;</a>')
    else:
        nav_lines.append("  <span></span>")
    nav_lines.append("</div>")
    nav_block = "\n".join(nav_lines)

    page_title = (
        f"{prefix}: {display_title}"
        if prefix.startswith("Appendix")
        else f"Ch {num}: {display_title}"
    )

    content = "\n".join([
        "---",
        "layout: default",
        f'title: "{page_title}"',
        "---",
        "",
        body.strip(),
        "",
        nav_block,
        "",
    ])

    path = os.path.join(docs_dir, filename)
    with open(path, "w") as f:
        f.write(content)
    return filename


def promote_dectrees(content: str) -> str:
    """Turn marked verbatim trees into copyable <pre><code> blocks."""
    pattern = re.compile(
        r"(?:^[ \t]*<<<DECTREE>>>\s*\n)(.*?)(?:^[ \t]*<<<ENDDECTREE>>>\s*\n?)",
        re.MULTILINE | re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        body = m.group(1)
        # Strip common indent pandoc adds to verbatim blocks.
        lines = body.splitlines()
        cleaned = []
        for line in lines:
            cleaned.append(re.sub(r"^[ \t]{0,4}", "", line))
        while cleaned and not cleaned[0].strip():
            cleaned.pop(0)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()
        tree = "\n".join(cleaned)
        tree = (
            tree.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        return (
            '<pre class="dectree" aria-label="Decision tree">'
            f"<code>{tree}</code></pre>\n"
        )

    return pattern.sub(repl, content)


def clean_pandoc_artifacts(content: str) -> str:
    """Post-process pandoc Markdown before splitting into pages."""
    content = promote_dectrees(content)
    # Drop leftover pandoc fenced-div open/close lines (::: center, :::).
    # Use [ \t] not \s so newlines are not swallowed into the match.
    content = re.sub(r"(?m)^:::[ \t]*.*$", "", content)
    # Remove {reference-type="..." reference="..."} attributes
    content = re.sub(r'\{reference-type="[^"]*"\s+reference="[^"]*"\}', '', content)
    # Empty spans from labels: []{#id}, []{#id label="..."}, []{#id .class}
    content = re.sub(r'\[\]\{#[^}]+\}', '', content)
    # Remove remaining {#label} attributes from headings
    content = re.sub(r'\s*\{#[^}]+\}', '', content)
    # Clean up empty links like [4.1]()
    content = re.sub(r'\[([^\]]+)\]\(\)', r'\1', content)
    # Drop leftover bare [] lines (stripped label spans)
    content = re.sub(r'(?m)^\s*\[\]\s*$', '', content)
    # Collapse runs of blank lines created by removals
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def main():
    if not os.path.exists(MD_FILE):
        print(f"ERROR: {MD_FILE} not found. Run pandoc first.", file=sys.stderr)
        sys.exit(1)

    with open(MD_FILE) as f:
        content = f.read()

    content = clean_pandoc_artifacts(content)

    # Remove any existing chapter .md files in docs (except index, config, layout)
    for fname in os.listdir(DOCS_DIR):
        if fname.startswith("ch") and fname.endswith(".md"):
            os.remove(os.path.join(DOCS_DIR, fname))

    chapters = split_chapters(content)
    print(f"  Found {len(chapters)} chapters")

    # Generate filenames for nav links
    filenames = []
    for num, title, _ in chapters:
        slug = slugify(title)
        filenames.append(f"ch{num}-{slug}")

    # Write each chapter
    for i, (num, title, body) in enumerate(chapters):
        prev_link = filenames[i - 1] if i > 0 else None
        next_link = filenames[i + 1] if i < len(chapters) - 1 else None
        write_chapter(num, title, body, DOCS_DIR, prev_link, next_link)

    # Write index
    write_index(chapters, DOCS_DIR)
    print(f"  Written {len(chapters)} chapter files + index.md")


if __name__ == "__main__":
    main()
