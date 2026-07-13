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

## Non-OIF standards coverage and known gaps

The book leans on OIF specifications (CEI electrical interfaces, CMIS, ELSFP,
400ZR/800ZR, co-packaging framework) throughout. This section tracks the non-OIF
standards bodies the book already cites and the ones it still under-covers, so a
future pass can close the gaps deliberately rather than by accident.

### Non-OIF standards already covered

| Body / spec | Where it appears | Notes |
|---|---|---|
| IEEE 802.3 (802.3dj, 802.3bj/KP4 FEC, 400G/lane study group, DR/FR PMD naming, TDECQ) | Ch2 IM/DD, Ch7 networking | The PHY-layer backbone of the book |
| LPO MSA | Ch7 (dedicated section) | Linear pluggable optics |
| CW-WDM MSA | Ch4 WDM | O-band comb grids for dense integration |
| ITU-T G.694.1 / G.694.2 | Ch4 WDM (`sec:why-wdm`) | DWDM 193.1 THz frequency grid and CWDM 20 nm wavelength grid. Added; grounds the grid ladder |
| ITU-T G.664 | Ch3 lasers (`sec:laser-safety`) | Optical safety, APR/ALS |
| IEC 60825-1 | Ch3 lasers (`sec:laser-safety`) | Laser hazard classes |
| Telcordia GR-468-CORE | Ch6 reliability (`sec:gr468`) | Optoelectronic device qualification |
| UALink, UEC, SNIA SFF, OCP | Ch7 networking (SDO map) | Scale-up / scale-out fabric bodies |
| COBO, QSFP-DD MSA, OSFP MSA | Ch7 networking | Pluggable form-factor MSAs, developed alongside CMIS, not just named |
| UCIe | Ch7 networking (`sec:trace-loss`) | Chiplet die-to-die interconnect, cited against the XSR/CPO discussion |
| ITU-T G.652 / G.657 | Ch2 IM/DD (`sec:optical-channel`) | Single-mode fiber loss/dispersion and bend-insensitive fiber grounding the reach budget |
| ISO/IEC 11801, TIA-492 | Ch2 IM/DD (`sec:optical-channel`) | Cabling classes (OM4/OM5, OS1/OS2) mapped onto SR/DR reach classes |
| JEDEC JESD47, JS-001/JS-002 (ESD), JESD78 (latch-up), AEC-Q100 | Ch6 reliability (`sec:ic-reliability`) | Driver/TIA/DSP silicon qualification, alongside the GR-468 optical qualification |
| IEC 61754-7 (MPO), IEC 61300-2-2, IEC 61300-3-35 | Ch6 reliability (`sec:connector-reliability`) | MPO ferrule geometry, mating-cycle rating, and endface-inspection grading |
| Telcordia GR-1221-CORE | Ch6 reliability (`sec:connector-reliability`) | Passive optical component reliability (connectors, couplers, WDM filters, isolators), the passive counterpart to GR-468 |
| InfiniBand / IBTA | Ch7 networking (scale-out) | NDR/XDR port rates at 200G/lane, shared QSFP/OSFP + MPO optics with Ethernet. XDR announcement marked provisional |
| IEEE 802.1AE (MACsec), 802.1X | Ch7 networking (line-rate security) | Line-rate L2 encryption and its PHY latency/power cost |
| PCI-SIG PCIe 7.0, CXL 4.0 | Ch7 networking (scale-up / memory) | 128 GT/s PAM4 host fabric and coherent memory pooling; optical workgroups. Both 2025 releases, marked provisional |
| DMTF Redfish, OpenConfig (gNMI), SONiC | Ch7 networking (fleet observability) | Box/fleet telemetry and config above OIF CMIS |

### Thin coverage (referenced, not developed)

- 100G Lambda MSA (named only)

### Known gaps, ranked

No open non-OIF standards gaps. The previous ranked gap (IBTA link specs) is now
covered in Ch7.

Resolved: ITU-T G.694 grid (Ch4), UCIe (Ch7), fiber-medium standards
G.652/G.657/ISO-IEC 11801/TIA-492 (Ch2), IC-level reliability standards
JEDEC/AEC-Q100 (Ch6), connector standards IEC 61754-7/61300 (Ch6). COBO and
QSFP-DD/OSFP were reclassified from "thin coverage" to "already covered" after a
comprehensive review found them developed in Ch7, not just named. IBTA
(InfiniBand), IEEE 802.1AE MACsec, PCI-SIG/CXL, Telcordia GR-1221, and the
DMTF/OpenConfig/SONiC management stack were added in a later non-OIF pass.
