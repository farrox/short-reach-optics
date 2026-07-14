#!/usr/bin/env python3
"""
Split the full pandoc Markdown output into per-chapter pages
with Jekyll front matter and navigation links.
"""
import os
import re
import sys

DOCS_DIR = sys.argv[1] if len(sys.argv) > 1 else "../../docs"
MD_FILE = ".build/full_book.md"


def slugify(title: str) -> str:
    """Turn a chapter title into a filename slug."""
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


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
        lines.append(f"- [**{num}.** {title}]({filename})")

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

    content = "\n".join([
        "---",
        "layout: default",
        f'title: "Ch {num}: {title}"',
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


def main():
    if not os.path.exists(MD_FILE):
        print(f"ERROR: {MD_FILE} not found. Run pandoc first.", file=sys.stderr)
        sys.exit(1)

    with open(MD_FILE) as f:
        content = f.read()

    # Post-process: clean up pandoc artifacts that don't render in Jekyll
    # Remove {reference-type="..." reference="..."} attributes
    content = re.sub(r'\{reference-type="[^"]*"\s+reference="[^"]*"\}', '', content)
    # Remove {#label} attributes from headings (Jekyll doesn't use them)
    content = re.sub(r'\s*\{#[^}]+\}', '', content)
    # Remove []{#label label="..."} empty spans
    content = re.sub(r'\[\]\{#[^}]+\s+label="[^"]*"\}', '', content)
    # Clean up empty links like [4.1]() 
    content = re.sub(r'\[([^\]]+)\]\(\)', r'\1', content)

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
        fname = write_chapter(num, title, body, DOCS_DIR, prev_link, next_link)

    # Write index
    write_index(chapters, DOCS_DIR)
    print(f"  Written {len(chapters)} chapter files + index.md")


if __name__ == "__main__":
    main()
