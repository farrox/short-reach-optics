# Book template (XeLaTeX + tufte-book)

A barebone starting point for book-length LaTeX documents. Copy this directory,
edit the metadata in `main.tex`, add chapters under `sections/`, and build with
`./compile.sh`.

## Quick start

```bash
cp -R book_template my-new-book
cd my-new-book
# Edit main.tex (title, subtitle, author) and sections/*.tex
./compile.sh
```

Output: `main.pdf`.

## Layout

- **Class:** `tufte-book` — asymmetric margins, sidenotes, full-width floats
- **Engine:** XeLaTeX (required for `fontspec` and bundled TTFs)
- **Body face:** Alegreya Sans (`fonts/`, SIL Open Font License)

## Files

| File | Role |
|------|------|
| `main.tex` | Document shell — title page, front matter, chapter inputs, appendices, references |
| `preamble.tex` | Fonts, packages, hyperref/cleveref, title page, custom macros |
| `sections/preface.tex` | Front-matter chapter (edit or replace) |
| `sections/copyright.tex` | Copyright / license page |
| `sections/ch01_getting_started.tex` | Sample chapter — delete when no longer needed |
| `sections/appendix_a_template.tex` | Sample appendix |
| `sections/references.tex` | Manual `\bibitem` bibliography |
| `aux/template.bib` | Optional BibTeX stub (not wired by default) |
| `fonts/` | Alegreya Sans TTFs |
| `compile.sh` | Three-pass XeLaTeX build |
| `check_overfull.sh` | Scan `main.log` for overfull hbox warnings |

## Adding chapters

1. Create `sections/ch02_my_topic.tex` with `\chapter{...}`, sections, and content.
2. Add `\input{sections/ch02_my_topic}` to `main.tex` after the previous chapter.
3. For every `\citep{key}` / `\citet{key}`, add a matching `\bibitem[...]{key}` in `sections/references.tex`.

To group several former chapters into one numbered chapter, use a wrapper file:

```latex
\setcounter{tocdepth}{1}
\chapter{Combined topic}
\input{sections/part_a}
\input{sections/part_b}
\setcounter{tocdepth}{2}
```

## Macros (`preamble.tex`)

| Macro | Use |
|-------|-----|
| `\subtitle{...}` | Subtitle on the title page |
| `\keyidea{...}` | Highlighted takeaway box |
| `\aside{...}` | Margin sidenote (alias for `\sidenote`) |
| `\term{...}` | Italic first-use of a term |
| `\code{...}` | Inline monospace |
| `\fillme{id}{title}{brief}{sources}{target}` | Visible draft stub — remove before publishing |

## Build requirements

TeX Live, MacTeX, or full MiKTeX with **tufte-latex** and **fontspec**. On a
minimal MiKTeX install you may need:

```text
tufte-latex sauerj (optparams.sty) xifthen ifmtarg xltxtra changepage \
paralist textcase natbib placeins multirow siunitx mdwtools
```

Run `xelatex main.tex` three times on the first build (TOC and cross-references).
`compile.sh` does this automatically.

Optional strict layout check:

```bash
CHECK_OVERFULL=1 FAIL_MAX_PT=30 ./compile.sh
```

## Fonts

See `fonts/README.md`. Alegreya Sans is vendored under the SIL OFL. EB Garamond
TTFs are included as an optional fallback if you prefer a serif body face.
