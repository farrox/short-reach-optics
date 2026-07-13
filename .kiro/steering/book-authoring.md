---
inclusion: always
---

# Working style

- **Bias toward adding, not asking.** When something is relevant and helpful,
  add it proactively: new sections, references, tables, context. Lean toward
  adding more now and trimming later rather than pausing to ask permission each
  time. Only stop to ask for genuinely destructive actions or real scope changes.
- **Flag, don't gate.** After adding, note any caveats (unverified numbers,
  preprints, conflicting sources) in the reply instead of withholding the content.
- **Verify facts before they enter the book.** Use web search to confirm specs,
  dates, and claims (vendor announcements and standards move fast). Prefer primary
  sources (vendor white papers, press releases, standards drafts) and mark
  preprints/announcements as provisional.

# Building the optics book

- **ALWAYS compile after every content edit, no exceptions.** After changing any
  `.tex` (or references/figures), rebuild before ending the turn. Do not report an
  edit as done until it has compiled cleanly (full page count, no undefined
  refs/citations, no new errors) and, for float/table/layout changes, been visually
  checked. Never leave the book in an unverified state.
- The book lives in `books/short-reach-optics/`. Its root is
  `main.tex` there, **not** the repo-root `main.tex` (that's the résumé).
- Compile with `xelatex` run 2–3× for cross-refs:
  `cd books/short-reach-optics && ./compile.sh` (preferred; builds
  into `.build/` and atomically replaces `main.pdf` so the viewer never reads a
  partial file). Raw `xelatex` in the book dir also works but risks blank PDF
  tabs if the viewer opens mid-pass.
- The `working_directory` shell param has not reliably taken here, so always `cd`
  into the book dir explicitly before compiling.
- After a build, confirm page count is the full book (tens of pages) and check for
  undefined references/citations, not just a zero exit code.
- **Always visually check changed pages, not just the log.** After editing floats
  or tables, render the affected pages to PNG and inspect them (e.g.
  `MPLCONFIGDIR=.mplcache XDG_CACHE_HOME=.cache ./.venv/bin/python` with `fitz`:
  open `main.pdf`, `get_pixmap(matrix=fitz.Matrix(3,3)).save(...)`), then read the
  image. Watch for caption/margin overlaps, content running off the page edge, and
  collisions the log may not flag. Also grep the log for `Overfull \hbox ([1-9][0-9]`.
- **Wide (multi-column) tables:** tufte's normal `\caption` is a *margin* note, which
  collides with a full-width table body (or runs off-page). Use a `table*` fullwidth
  float with a MANUAL caption instead: `\refstepcounter{table}\label{...}` at the top
  (so `\Cref` resolves), then after the tabular a full-width paragraph
  `{\raggedright\footnotesize\textbf{Table~\thetable.} ...\par}`. Do NOT use the
  `fullwidth` environment for this (its `\caption` runs off-page and it throws a
  constant benign overfull). Keep narrow 2--3 col tables as normal `table`+`\caption`.
- Preamble note: `tufte-book` letterspacing is routed through `microtype`'s
  `\textls` (not `soul`) to avoid running-head crashes; keep that patch.
- Float references: tufte-book + amsmath breaks `\ref`/`\Cref` to figures/tables
  (they resolve to the section or blank; tufte-latex issues #185--187). The
  preamble has `\AtBeginDocument{\robustify\label}`; ALWAYS place `\label` INSIDE
  the `\caption{...\label{...}}` for every figure and table. Keep it that way.
- Math font: the preamble loads `\usepackage[italic]{mathastext}` (after
  amsmath/amssymb and the Alegreya main font) so math digits and variables use
  Alegreya to match the body; operators, delimiters, and Greek stay Computer
  Modern. Keep it, otherwise math numerals (e.g. `$-136$`) revert to CM and clash
  with the text. (unicode-math was tried and fails: mapping a text font into a
  math range triggers the `ssty`/scriptfont machinery Alegreya lacks.)
- Python sims live in `sims/` with a local `.venv`; regenerate figures with
  `MPLCONFIGDIR=.mplcache XDG_CACHE_HOME=.cache ./.venv/bin/python sims/make_figures.py`
  (the cache vars avoid fontconfig/matplotlib write errors in the sandbox).
- LaTeX Workshop is configured (user `settings.json`) to build every project with
  XeLaTeX via `latexmk -xelatex`, so in-IDE builds match the CLI. Don't add
  pdflatex recipes or `% !TEX program` magic comments.
- **Auto-recompile hooks:** manual `.tex` saves in the book use LaTeX Workshop
  `onSave` (`book/.vscode/settings.json`). Agent/Tab edits trigger
  `.cursor/hooks/recompile-on-tex-save.sh` via `afterFileEdit` /
  `afterTabFileEdit` in `.cursor/hooks.json` (2 s debounce, log at
  `.cursor/hooks/tex-compile.log`).

# Content and citation conventions

- **Cite every new fact.** When adding a spec, number, date, or vendor claim, add a
  matching entry to `sections/references.tex` and `\cite` it. Match the existing
  format exactly: `\bibitem[ShortLabel(Year)]{key}` followed by a `\newblock` line,
  and put the concrete numbers in that annotation line (so the source doubles as a
  quick-reference). Reuse an existing key rather than duplicating a source. Wrap
  bibliography titles in `\href{url}{...}` and register the same URL in
  `sections/citeurls.tex` for sidenote/inline `\citehref{key}{...}` links.
  Drop local copies in `books/short-reach-optics/docs/` as
  `{bibkey}.pdf` (directory gitignored except `docs/README.md`; URLs in
  `citeurls.tex` work without local files).
  `{bibkey}.pdf`; `\defciteurllocal` prefers the local file and falls back to
  the DOI/URL when the PDF is missing.
- **Mark provisional sources.** Preprints (arXiv), draft standards (e.g. CEI-224G
  draft IAs), and vendor announcements are provisional: say so in the bibliography
  annotation and, when a number leans on them, flag it in the reply.
- **Cross-reference, don't duplicate.** Point at existing chapters/sections with
  `\Cref{}` instead of re-explaining a concept. Before renaming or deleting a
  section, grep for its `\label` so you catch every reference first.
- **Stay in scope: short reach.** The book covers short-reach interconnects
  (in-package out to a few hundred meters). Do not reintroduce 2~km+ campus/DCI,
  long-haul, or coherent-detection detail unless asked; a brief mention-and-defer is
  fine.
- **Numbers and units.** Use `--` (en dash) for ranges (`14--18~W`, `2025--26`), a
  tie `~` before units, and `$\sim$` / `$\approx$` / `$\ge$` / `$\times$`
  consistently. Digits already route through Alegreya via `mathastext`; keep new
  math consistent with that.
- **Voice.** Use direct second person ("you") for explanations and derivations, and
  an impersonal, declarative voice for factual claims and specs. No first-person
  singular. Don't switch voice mid-passage.
- **Acronyms.** Expand every acronym on first use in a chapter and tag the
  introduced term with `\term{}`; use the acronym alone afterward.
- **Chapter shape.** End each chapter with a `\keyidea{...}` box that distills the
  takeaway in a few sentences.
