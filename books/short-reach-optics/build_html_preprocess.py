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
        if type_dot_num.startswith("appendix"):
            # appendix.A / appendix.B.3 → Appendix A / Appendix B.3
            label_type = "Appendix"
        elif type_dot_num.startswith("chapter"):
            label_type = "Chapter"
        elif type_dot_num.startswith("table"):
            label_type = "Table"
        elif type_dot_num.startswith("figure"):
            label_type = "Figure"
        elif type_dot_num.startswith("equation"):
            label_type = "Eq."
        else:
            # Lettered appendix sections often appear as section.A.1 in aux
            if number and number[0].isalpha() and (
                len(number) == 1 or (len(number) > 1 and number[1] == ".")
            ):
                label_type = "Appendix"
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


def replace_engcheck(content: str) -> str:
    """Replace \\engcheck{title}{body} with a pandoc-friendly quote."""
    result = []
    i = 0
    tag = "\\engcheck{"
    while i < len(content):
        idx = content.find("\\engcheck{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        pos = idx + len(tag) - 1
        title, pos = extract_braced_arg(content, pos)
        body, pos = extract_braced_arg(content, pos)
        result.append(
            f"\n\n\\begin{{quote}}\\textbf{{{title}}}\\par {body}\\end{{quote}}\n\n"
        )
        i = pos
    return "".join(result)


def replace_execanswer(content: str) -> str:
    """Replace \\execanswer{...} handling nested braces."""
    result = []
    i = 0
    tag = "\\execanswer{"
    while i < len(content):
        idx = content.find("\\execanswer{", i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        arg, end = extract_braced_arg(content, idx + len(tag) - 1)
        result.append(
            f"\n\n\\begin{{quote}}\\textbf{{30-second answer (memorize).}} {arg}"
            f"\\end{{quote}}\n\n"
        )
        i = end
    return "".join(result)


def replace_fw_macro(content: str, cmd: str, heading: str) -> str:
    """Replace \\cmd{...} with a bold heading plus body (pandoc-friendly)."""
    result = []
    i = 0
    tag = f"\\{cmd}{{"
    while i < len(content):
        idx = content.find(tag, i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        arg, end = extract_braced_arg(content, idx + len(tag) - 1)
        result.append(f"\n\n\\textbf{{{heading}}} {arg}\n\n")
        i = end
    return "".join(result)


def replace_framework(content: str) -> str:
    result = []
    i = 0
    tag = "\\framework{"
    while i < len(content):
        idx = content.find(tag, i)
        if idx == -1:
            result.append(content[i:])
            break
        result.append(content[i:idx])
        arg, end = extract_braced_arg(content, idx + len(tag) - 1)
        result.append(f"\n\n\\section{{{arg}}}\n\n")
        i = end
    return "".join(result)


def replace_dectree(content: str) -> str:
    """
    Convert dectree envs to verbatim before pandoc.

    Markers let build_html_split.py rewrite the resulting indented code block
    into a semantic <pre class="dectree"> (latex reader has no raw_html).
    """
    pattern = re.compile(
        r"\\begin\{dectree\}(.*?)\\end\{dectree\}",
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        body = m.group(1)
        lines = body.splitlines()
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        tree = "\n".join(lines)
        return (
            "\n\n\\begin{verbatim}\n"
            "<<<DECTREE>>>\n"
            f"{tree}\n"
            "<<<ENDDECTREE>>>\n"
            "\\end{verbatim}\n\n"
        )

    return pattern.sub(repl, content)


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


def _split_tex_row(row: str) -> list[str]:
    """Split a tabular row on un-nested &."""
    cells: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in row:
        if ch == "{":
            depth += 1
            buf.append(ch)
        elif ch == "}":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == "&" and depth == 0:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def _tex_cell_to_html(cell: str) -> str:
    """Lightweight TeX cell cleanup for HTML tables."""
    s = cell.strip()
    s = re.sub(r"\\(?:addlinespace|midrule|toprule|bottomrule)\b[^\n\\]*", "", s)
    for _ in range(3):
        s = re.sub(
            r"\\(?:textbf|emph|textit|texttt|mathrm|text)\*{0,1}\{([^{}]*)\}",
            r"\1",
            s,
        )
    s = s.replace("\\&", "&").replace("~", " ")
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\s+", " ", s).strip()
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def replace_tabular_html(content: str) -> str:
    """
    Convert tabular environments to HTML-table markers for post-pandoc promotion.

    Wide p{\\linewidth} specs and \\addlinespace often make pandoc emit
    indented ASCII grids that Markdown treats as code blocks.
    """
    out: list[str] = []
    i = 0
    begin = "\\begin{tabular}"
    end = "\\end{tabular}"
    while True:
        idx = content.find(begin, i)
        if idx < 0:
            out.append(content[i:])
            break
        out.append(content[i:idx])
        # Skip column-spec braced arg (allow whitespace before '{')
        spec_pos = idx + len(begin)
        while spec_pos < len(content) and content[spec_pos].isspace():
            spec_pos += 1
        _spec, after_spec = extract_braced_arg(content, spec_pos)
        if not _spec and content[spec_pos:spec_pos + 1] != "{":
            out.append(content[idx : idx + len(begin)])
            i = idx + len(begin)
            continue
        end_idx = content.find(end, after_spec)
        if end_idx < 0:
            out.append(content[idx:])
            break
        body = content[after_spec:end_idx]
        body = re.sub(r"\\addlinespace(?:\[[^\]]*\])?", r"\\\\", body)
        for rule in ("toprule", "midrule", "bottomrule", "hline"):
            body = re.sub(rf"\\{rule}\b", r"\\\\", body)
        parts = re.split(r"\\\\", body)
        rows: list[list[str]] = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            cells = _split_tex_row(part)
            if all(not c.strip() for c in cells):
                continue
            rows.append([_tex_cell_to_html(c) for c in cells])
        if not rows:
            out.append(content[idx : end_idx + len(end)])
            i = end_idx + len(end)
            continue
        width = max(len(r) for r in rows)
        for r in rows:
            while len(r) < width:
                r.append("")
        html_rows = []
        for ri, r in enumerate(rows):
            tag = "th" if ri == 0 else "td"
            cells = "".join(f"<{tag}>{c}</{tag}>" for c in r)
            html_rows.append(f"<tr>{cells}</tr>")
        table_html = '<table class="book-table">' + "".join(html_rows) + "</table>"
        out.append(
            "\n\n\\begin{verbatim}\n"
            "<<<TABLE>>>\n"
            f"{table_html}\n"
            "<<<ENDTABLE>>>\n"
            "\\end{verbatim}\n\n"
        )
        i = end_idx + len(end)
    return "".join(out)


def apply_transforms(content: str) -> str:
    """Apply all regex transformations."""
    # Handle nested-brace commands first
    content = replace_keyidea(content)
    content = replace_engcheck(content)
    content = replace_execanswer(content)
    content = replace_framework(content)
    content = replace_dectree(content)
    content = replace_fw_macro(content, "fwquestion", "Interview question.")
    content = replace_fw_macro(content, "fwtesting", "What the interviewer is testing.")
    content = replace_fw_macro(content, "fwassumptions", "Assumptions to state.")
    content = replace_fw_macro(content, "fwfirst", "First thing I would check.")
    content = replace_fw_macro(content, "fwwhy", "Key concepts.")
    content = replace_fw_macro(content, "fwmeas", "Measurements.")
    content = replace_fw_macro(content, "fwfollow", "Typical follow-ups.")
    content = replace_fw_macro(content, "fwmistakes", "Common mistakes.")
    content = replace_fw_macro(content, "fwclose", "Thirty-second close.")
    content = replace_fw_macro(content, "fwdeep", "Deep dive.")
    content = replace_fillme(content)
    content = replace_failuremode(content)
    content = replace_debugstory(content)
    # Convert tabulars before pandoc so wide tables do not become code blocks
    content = replace_tabular_html(content)

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

    # Drop center wrappers; pandoc emits ::: center fences otherwise.
    content = content.replace("\\begin{center}", "")
    content = content.replace("\\end{center}", "")

    # Remove \frontmatter, \mainmatter, \backmatter, \appendix
    # Keep appendix chapter titles; lettering is restored in build_html_split.
    content = content.replace("\\frontmatter", "")
    content = content.replace("\\mainmatter", "")
    content = content.replace("\\backmatter", "")
    content = content.replace("\\appendix", "")

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

    # Pandoc cannot parse \bibitem well. Leave a placeholder; build_html_bib.py
    # overwrites the References HTML page with the full structured bibliography.
    content = re.sub(
        r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}",
        r"\n\n\\section*{References}\n\n"
        r"The full bibliography is generated for HTML from "
        r"\\texttt{sections/references.tex} "
        r"(same source as the PDF).\n\n",
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
                elif ltype == "Appendix":
                    # Avoid "Appendix~A" tilde; HTML wants a normal space.
                    text = f"Appendix {num}"
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
