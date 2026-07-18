#!/usr/bin/env python3
"""
Pre-process the tufte-book LaTeX source into a single file
that pandoc can convert to HTML cleanly.

1. Reads main.tex, expands all \\input{} directives recursively.
2. Strips/replaces custom commands pandoc cannot parse.
3. Writes .build/combined_for_html.tex ready for pandoc.
"""
from __future__ import annotations

import os
import re
import sys

BOOK_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BOOK_DIR, ".build")
OUTPUT_FILE = os.path.join(BUILD_DIR, "combined_for_html.tex")

# --- URL map from citeurls.tex ---
CITE_URLS: dict[str, str] = {}

# --- Label→number map from .aux ---
LABEL_MAP: dict[str, tuple[str, str]] = {}  # key → (type, number)


def parse_aux_labels():
    """Parse .build/main.aux for \\newlabel entries to build label→number map."""
    aux_path = os.path.join(BUILD_DIR, "main.aux")
    if not os.path.exists(aux_path):
        print("  WARNING: main.aux not found; cross-references will not resolve.")
        return
    with open(aux_path, "r") as f:
        content = f.read()
    # Match \newlabel{key}{{number}{page}{title}{type.number}{}}
    # Example: \newlabel{sec:bringup}{{7.9}{124}{Module and system bring-up}{section.7.9}{}}
    for m in re.finditer(
        r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{[^}]*\}\{[^}]*\}\{([^}]*)\}\{[^}]*\}\}",
        content,
    ):
        key = m.group(1)
        number = m.group(2)
        type_dot_num = m.group(3)  # e.g. "section.7.9", "chapter.7", "table.7.2"
        if key.endswith("@cref"):
            continue
        # Determine type prefix for display
        if type_dot_num.startswith("chapter"):
            label_type = "Chapter"
        elif type_dot_num.startswith("table"):
            label_type = "Table"
        elif type_dot_num.startswith("figure"):
            label_type = "Figure"
        elif type_dot_num.startswith("equation"):
            label_type = "Eq."
        else:
            label_type = "§"
        LABEL_MAP[key] = (label_type, number)
    print(f"  Loaded {len(LABEL_MAP)} label→number mappings from main.aux")


def parse_citeurls():
    """Extract key→url mappings from sections/citeurls.tex."""
    path = os.path.join(BOOK_DIR, "sections", "citeurls.tex")
    with open(path, "r") as f:
        content = f.read()
    # Match \defciteurl{key}{url}
    for m in re.finditer(r"\\defciteurl\{([^}]+)\}\{([^}]+)\}", content):
        CITE_URLS[m.group(1)] = m.group(2)
    # Match \defciteurllocal{key}{localpath}{url} — use the URL (3rd arg)
    for m in re.finditer(
        r"\\defciteurllocal\{([^}]+)\}\{[^}]+\}\{([^}]+)\}", content
    ):
        CITE_URLS[m.group(1)] = m.group(2)


def expand_inputs(filepath: str, seen: set | None = None) -> str:
    """Recursively expand \\input{path} directives."""
    if seen is None:
        seen = set()
    filepath = os.path.abspath(filepath)
    if filepath in seen:
        return ""
    seen.add(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    base_dir = os.path.dirname(filepath)

    def replace_input(m):
        rel = m.group(1)
        if not rel.endswith(".tex"):
            rel += ".tex"
        full = os.path.join(base_dir, rel)
        if os.path.exists(full):
            return expand_inputs(full, seen)
        return ""  # skip missing files

    content = re.sub(r"\\input\{([^}]+)\}", replace_input, content)
    return content


# --- Regex-based transformations ---

# Commands to remove entirely (they produce no visible output in HTML)
REMOVE_PATTERNS = [
    # \firstterm{...} — margin note on first use, not needed in HTML
    r"\\firstterm\{[^}]*\}",
    # \firstcite{...} — margin citation on first use
    r"\\firstcite\{[^}]*\}",
    # \fillme{...}{...}{...}{...}{...} — draft stub (5 args)
    r"\\fillme\{[^}]*\}\{[^}]*\}\{[^}]*\}\{[^}]*\}\{[^}]*\}",
    # \declaretermsnip{...}{...}
    r"\\declaretermsnip\{[^}]*\}\{[^}]*\}",
    # \declarecitesnip{...}{...}
    r"\\declarecitesnip\{[^}]*\}\{[^}]*\}",
    # \defciteurl{...}{...}
    r"\\defciteurl\{[^}]*\}\{[^}]*\}",
    # \defciteurllocal{...}{...}{...}
    r"\\defciteurllocal\{[^}]*\}\{[^}]*\}\{[^}]*\}",
    # \makeatletter ... \makeatother blocks (remove inline ones)
    r"\\makeatletter",
    r"\\makeatother",
    # Various internal re-definitions pandoc won't understand
    r"\\let\\cite\\citep",
    r"\\let\\@tufte@normal@cite\\citep",
    # \robustify\label
    r"\\AtBeginDocument\{\\robustify\\label\}",
    # Tufte's \newthought{...} → just bold in HTML (handled below)
    # \refstepcounter{table}
    r"\\refstepcounter\{[^}]*\}",
    # Remove \label outside of environments pandoc handles
    # (pandoc handles \label in figures/tables itself)
]

# Commands to replace with simpler equivalents pandoc understands
REPLACE_PATTERNS = [
    # \term{text} → \emph{text}
    (r"\\term\{([^}]*)\}", r"\\emph{\1}"),
    # \code{text} → \texttt{text}
    (r"\\code\{([^}]*)\}", r"\\texttt{\1}"),
    # \aside{text} → \footnote{text} (pandoc renders footnotes nicely)
    (r"\\aside\{", r"\\footnote{"),
    # \mcite{key}{text} → \footnote{text} (drop the key)
    (r"\\mcite\{[^}]*\}\{([^}]*)\}", r"\\footnote{\1}"),
    # \newthought{text} → \textbf{text}
    (r"\\newthought\{([^}]*)\}", r"\\textbf{\1}"),
    # \keyidea{text} is handled separately (nested braces)
]


def replace_citehref(content: str) -> str:
    """Replace \\citehref{key}{text} with \\href{url}{text} using the URL map."""

    def replacer(m):
        key = m.group(1)
        text = m.group(2)
        url = CITE_URLS.get(key, "")
        if url:
            return f"\\href{{{url}}}{{{text}}}"
        return text  # fallback: just the text

    return re.sub(r"\\citehref\{([^}]+)\}\{([^}]+)\}", replacer, content)


def strip_preamble_for_pandoc(content: str) -> str:
    """
    Remove the tufte-book preamble and replace with a minimal one pandoc can handle.
    Keep everything between \\begin{document} and \\end{document}.
    Also strip any leftover \\newcommand etc. that leaked into the body.
    """
    # Find document body
    begin = content.find("\\begin{document}")
    end = content.find("\\end{document}")
    if begin == -1 or end == -1:
        print("ERROR: Could not find \\begin{document}/\\end{document}", file=sys.stderr)
        sys.exit(1)

    body = content[begin + len("\\begin{document}") : end]

    # Remove any duplicate \begin{document} that leaked from expansion
    body = body.replace("\\begin{document}", "")

    # Strip \newcommand, \renewcommand, \providecommand definitions from body
    # These have the form \newcommand{\name}[nargs]{definition}
    # or \newcommand{\name}{definition}
    # Use brace-counting to handle nested braces in definitions
    def strip_command_defs(text: str) -> str:
        """Remove \\newcommand, \\renewcommand, \\providecommand definitions."""
        patterns = ["\\newcommand", "\\renewcommand", "\\providecommand"]
        for pat in patterns:
            while pat in text:
                idx = text.find(pat)
                # Find the end of this definition by skipping braced args
                pos = idx + len(pat)
                # Skip optional * 
                if pos < len(text) and text[pos] == '*':
                    pos += 1
                # Skip the command name arg {\\name}
                if pos < len(text) and text[pos] == '{':
                    _, pos = extract_braced_arg(text, pos)
                # Skip optional [nargs]
                if pos < len(text) and text[pos] == '[':
                    close = text.find(']', pos)
                    if close != -1:
                        pos = close + 1
                # Skip optional [default]
                if pos < len(text) and text[pos] == '[':
                    close = text.find(']', pos)
                    if close != -1:
                        pos = close + 1
                # Skip the definition body {...}
                if pos < len(text) and text[pos] == '{':
                    _, pos = extract_braced_arg(text, pos)
                text = text[:idx] + text[pos:]
        return text

    body = strip_command_defs(body)

    # Also strip \expandafter, \gdef, \csname...\endcsname, \ifcsname...\fi patterns
    body = re.sub(r"\\expandafter[^{}\n]*", "", body)
    body = re.sub(r"\\gdef[^{}\n]*\{[^}]*\}\{[^}]*\}", "", body)

    # Strip remaining \let commands
    body = re.sub(r"\\let\\[a-zA-Z@]+\\[a-zA-Z@]+", "", body)

    # Strip %... comment lines  
    body = re.sub(r"(?m)^%.*$", "", body)

    # Strip \definecolor{...}{...}{...}
    body = re.sub(r"\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", body)

    # Strip \AtBeginDocument{...}
    def strip_at_begin_doc(text):
        while "\\AtBeginDocument{" in text:
            idx = text.find("\\AtBeginDocument{")
            pos = idx + len("\\AtBeginDocument")
            _, pos = extract_braced_arg(text, pos)
            text = text[:idx] + text[pos:]
        return text
    body = strip_at_begin_doc(body)

    # Strip \subtitle{...}
    body = re.sub(r"\\subtitle\{[^}]*\}", "", body)

    # Strip duplicate \title, \author, \date from body
    body = re.sub(r"\\title\{[^}]*\}", "", body)
    body = re.sub(r"\\author\{[^}]*\}", "", body)
    body = re.sub(r"\\date\{[^}]*\}", "", body)

    # Strip \tableofcontents (pandoc generates its own TOC)
    body = body.replace("\\tableofcontents", "")

    # Minimal preamble pandoc needs
    preamble = r"""
\documentclass{article}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{listings}
\title{Short-Reach Optics for AI Compute}
\author{Ed (Ehsan) Shah Hosseini}
\date{}
"""
    return preamble + "\n\\begin{document}\n" + body + "\n\\end{document}\n"


def extract_braced_arg(content: str, start: int) -> tuple[str, int]:
    """
    Starting at content[start] which should be '{', extract the full
    brace-balanced argument including nested braces.
    Returns (argument_text, end_index) where end_index is after the closing '}'.
    """
    if start >= len(content) or content[start] != '{':
        return ("", start)
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return (content[start + 1 : i], i + 1)
        i += 1
    return (content[start + 1 :], len(content))


def replace_keyidea(content: str) -> str:
    """Replace \\keyidea{...} handling nested braces."""
    result = []
    i = 0
    tag = "\\keyidea{"
    while i < len(content):
        idx = content.find("\\keyidea{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        # extract the braced arg starting at the '{'
        arg, end = extract_braced_arg(content, idx + len(tag) - 1)
        result.append(f"\n\n\\textbf{{Key idea.}} {arg}\n\n")
        i = end
    return "".join(result)


def replace_fillme(content: str) -> str:
    """Remove \\fillme{...}{...}{...}{...}{...} handling nested braces."""
    result = []
    i = 0
    tag = "\\fillme{"
    while i < len(content):
        idx = content.find("\\fillme{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        # skip 5 braced args
        pos = idx + len(tag) - 1
        for _ in range(5):
            _, pos = extract_braced_arg(content, pos)
        i = pos
    return "".join(result)


def replace_failuremode(content: str) -> str:
    r"""Replace \failuremode{name}{symptoms}{causes}{measurements}{mitigations}."""
    result = []
    i = 0
    tag = "\\failuremode{"
    while i < len(content):
        idx = content.find("\\failuremode{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        pos = idx + len(tag) - 1
        args = []
        for _ in range(5):
            arg, pos = extract_braced_arg(content, pos)
            args.append(arg)
        name, symptoms, causes, measurements, mitigations = args
        result.append(
            f"\n\n> **Failure mode: {name}**\n>\n"
            f"> **Symptoms.** {symptoms}\n>\n"
            f"> **Likely causes.** {causes}\n>\n"
            f"> **Measurements.** {measurements}\n>\n"
            f"> **Mitigations.** {mitigations}\n\n"
        )
        i = pos
    return "".join(result)


def replace_debugstory(content: str) -> str:
    r"""Replace \debugstory{observed}{investigation}{finding}{rootcause}{resolution}."""
    result = []
    i = 0
    tag = "\\debugstory{"
    while i < len(content):
        idx = content.find("\\debugstory{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        pos = idx + len(tag) - 1
        args = []
        for _ in range(5):
            arg, pos = extract_braced_arg(content, pos)
            args.append(arg)
        observed, investigation, finding, rootcause, resolution = args
        result.append(
            f"\n\n> **Debug story**\n>\n"
            f"> **Observed.** {observed}\n>\n"
            f"> **Investigation.** {investigation}\n>\n"
            f"> **Finding.** {finding}\n>\n"
            f"> **Root cause.** {rootcause}\n>\n"
            f"> **Resolution.** {resolution}\n\n"
        )
        i = pos
    return "".join(result)


def apply_transforms(content: str) -> str:
    """Apply all regex transformations."""
    # Handle nested-brace commands first
    content = replace_keyidea(content)
    content = replace_fillme(content)
    content = replace_failuremode(content)
    content = replace_debugstory(content)

    # Then handle citehref (needs the URL map)
    content = replace_citehref(content)

    # Remove patterns
    for pattern in REMOVE_PATTERNS:
        content = re.sub(pattern, "", content)

    # Replace patterns
    for pattern, replacement in REPLACE_PATTERNS:
        content = re.sub(pattern, replacement, content)

    # Remove \sidenote{...} → \footnote{...}
    content = re.sub(r"\\sidenote\{", r"\\footnote{", content)
    # Remove \marginnote{...} → \footnote{...}
    content = re.sub(r"\\marginnote\{", r"\\footnote{", content)

    # Remove table* → table, figure* → figure (pandoc doesn't like starred)
    content = content.replace("\\begin{table*}", "\\begin{table}")
    content = content.replace("\\end{table*}", "\\end{table}")
    content = content.replace("\\begin{figure*}", "\\begin{figure}")
    content = content.replace("\\end{figure*}", "\\end{figure}")

    # Remove \begin{fullwidth}...\end{fullwidth}
    content = content.replace("\\begin{fullwidth}", "")
    content = content.replace("\\end{fullwidth}", "")

    # Remove \frontmatter, \mainmatter, \backmatter
    content = content.replace("\\frontmatter", "")
    content = content.replace("\\mainmatter", "")
    content = content.replace("\\backmatter", "")

    # Remove \maketitle (pandoc handles title from metadata)
    content = re.sub(r"\\maketitle", "", content)

    # Remove \addcontentsline{...}{...}{...}
    content = re.sub(r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", content)

    # Remove \clearpage, \newpage
    content = content.replace("\\clearpage", "")
    content = content.replace("\\newpage", "")

    # Remove \sloppy, \setlength commands
    content = re.sub(r"\\sloppy", "", content)
    content = re.sub(r"\\setlength\{[^}]*\}\{[^}]*\}", "", content)

    # Remove \small, \footnotesize, \normalsize, \large, etc.
    for cmd in [
        "\\small",
        "\\footnotesize",
        "\\normalsize",
        "\\large",
        "\\Large",
        "\\LARGE",
        "\\huge",
        "\\Huge",
    ]:
        content = content.replace(cmd, "")

    # \centering → nothing (CSS handles centering)
    content = content.replace("\\centering", "")

    # Remove \noindent
    content = content.replace("\\noindent", "")

    # Remove \raggedright
    content = content.replace("\\raggedright", "")

    # Remove \par\medskip, \par\smallskip, etc.
    content = re.sub(r"\\par\\(med|small|big)skip", "\n\n", content)
    content = re.sub(r"\\(med|small|big)skip", "\n", content)

    # Remove the thebibliography environment (pandoc can't parse \bibitem well)
    content = re.sub(
        r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}",
        r"\n\n\\section*{References}\n\nSee the PDF version for the full bibliography.\n\n",
        content,
        flags=re.DOTALL,
    )

    # \Cref{...} and \cref{...} → resolved cross-references from .aux
    def resolve_cref(m):
        keys = m.group(1).split(",")
        parts = []
        seen = set()
        for key in keys:
            key = key.strip()
            if key in LABEL_MAP:
                ltype, num = LABEL_MAP[key]
                if ltype == "§":
                    text = f"§{num}"
                else:
                    text = f"{ltype}~{num}"
            else:
                # Fallback: strip prefix and humanize
                text = key.replace("sec:", "").replace("ch:", "Ch. ").replace("tab:", "Table ").replace("fig:", "Fig. ")
            if text not in seen:
                seen.add(text)
                parts.append(text)
        return ", ".join(parts)

    content = re.sub(r"\\[Cc]ref\{([^}]*)\}", resolve_cref, content)

    # Fix table numbers: replace \thetable with the number from the nearest \label
    def resolve_thetable(content: str) -> str:
        """Replace \\thetable with the table number from the nearest preceding \\label{tab:...}."""
        # Find all \label{tab:...} positions and their resolved numbers
        label_positions = []
        for m in re.finditer(r"\\label\{(tab:[^}]+)\}", content):
            key = m.group(1)
            if key in LABEL_MAP:
                _, num = LABEL_MAP[key]
                label_positions.append((m.start(), num))

        # Replace each \thetable with the number of the closest preceding table label
        result = []
        last_end = 0
        for m in re.finditer(r"\\thetable", content):
            # Find the closest preceding label
            pos = m.start()
            num = "?"
            for lpos, lnum in reversed(label_positions):
                if lpos < pos:
                    num = lnum
                    break
            result.append(content[last_end:m.start()])
            result.append(num)
            last_end = m.end()
        result.append(content[last_end:])
        return "".join(result)

    content = resolve_thetable(content)

    # Remove \cite{...} → just strip (references are in PDF)
    content = re.sub(r"\\cite\{[^}]*\}", "", content)
    # Remove \citep{...}
    content = re.sub(r"\\citep\{[^}]*\}", "", content)

    return content


def main():
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Parse URL map
    parse_citeurls()
    print(f"  Loaded {len(CITE_URLS)} citation URLs")

    # Parse label→number map from .aux (requires prior compilation)
    parse_aux_labels()

    # Expand inputs
    main_tex = os.path.join(BOOK_DIR, "main.tex")
    print(f"  Expanding inputs from {main_tex}")
    combined = expand_inputs(main_tex)

    # Strip preamble, keep body
    combined = strip_preamble_for_pandoc(combined)

    # Apply transformations
    print("  Applying macro transformations...")
    combined = apply_transforms(combined)

    # Write output
    with open(OUTPUT_FILE, "w") as f:
        f.write(combined)
    print(f"  Written: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
