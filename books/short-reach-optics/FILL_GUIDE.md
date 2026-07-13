# Skeleton fill guide (handoff for another LLM)

Four sections in the book are stubbed as skeletons: headings plus `%` comment notes
on what to write. Your job is to turn each into finished prose. This file is the
brief. Read it fully before editing.

## What the book is

`Short-Reach Optics for AI Compute`. A technical book on short-reach optical
interconnects for AI compute (in-package out to a few hundred meters): energy,
lasers, IM/DD, WDM, validation, reliability, and AI-datacenter networking.

- Book root: `books/short-reach-optics/main.tex`
- Chapters: `books/short-reach-optics/sections/ch*.tex`
- Bibliography: `sections/references.tex`; citation URLs: `sections/citeurls.tex`
- Local source PDFs: `books/short-reach-optics/docs/{bibkey}.pdf` (gitignored; optional for offline use)

## Build and verify (do this after every edit, no exceptions)

```bash
cd books/short-reach-optics && ./compile.sh
```

A section is NOT done until:
1. It compiles with exit 0 AND the PDF is the full book (~121 pages, not a stub).
2. No new undefined references or citations in the log.
3. Every `\Cref{}` you add resolves to a real `\label` (see the label table below).
4. Every new fact, number, date, or vendor claim has a matching `\cite`.

Do one section per pass. Compile between sections so a break is easy to localize.

## Writing rules (strict — these are Ed's house style)

- **No em dashes anywhere.** No `---`, and no `--` used as a dash. Use commas,
  periods, or parentheses, or split the sentence. `--` is allowed ONLY as an en
  dash inside numeric ranges (`14--18~W`, `2025--26`).
- **No LLM tone.** No hedging ("it's worth noting"), no cheerleading, no
  throat-clearing ("Certainly"), no summary wrap-ups ("In summary", "Overall"),
  no formulaic transitions ("Moreover", "Furthermore", "Additionally", "That said").
  Do not open a passage by restating the heading.
- **No inflated contrast framing.** Avoid "It's not just X, it's Y", "Think of it
  as", and rule-of-three lists added for rhythm.
- **Banned words** (unless the source uses them first): leverage, utilize, delve,
  spearhead, robust, holistic, synergy, ecosystem, landscape, cutting-edge,
  transformative, groundbreaking, comprehensive, facilitate, streamline, impactful,
  best-in-class, world-class, state-of-the-art, extensive, proven, seamless,
  innovative, dynamic, robustly. Replace with a concrete fact, number, or constraint,
  or delete. Do not use "optimize" as filler.
- **Plain, short sentences.** One idea per sentence. American English. No
  exclamation points. No first-person singular.
- **Voice:** direct second person ("you") for explanations and derivations;
  impersonal declarative for factual claims and specs. Do not switch mid-passage.
- **Prose, not bullets.** The skeletons use subsections; fill them with paragraphs.
  Only keep a `\begin{itemize}`/`description` if the surrounding chapter clearly
  favors one for a genuine list (most of these should be prose).
- **Length:** each of the four sections should land around one page. Density over
  decoration. Do not pad to fill.
- **Acronyms:** expand on first use in the chapter and tag with `\term{}`; use the
  acronym alone afterward. If the term is defined elsewhere first, don't redefine.
- **Ranges/units:** `--` for ranges, tie `~` before units (`10~km`, `1.5~W`), and
  `$\sim$` / `$\approx$` / `$\ge$` / `$\times$` consistently.
- **End-of-chapter `\keyidea{}` boxes already exist; do not add new ones** for these
  sections (they sit mid-chapter).

## Facts and citations

- **Cite every new spec, number, date, or vendor claim.** Add a `\bibitem` to
  `sections/references.tex` matching the existing format exactly:
  `\bibitem[ShortLabel(Year)]{key}` then a `\newblock` annotation line that carries
  the concrete numbers. Wrap the title in `\href{url}{...}` and register the URL in
  `sections/citeurls.tex`. Reuse an existing key rather than duplicating a source.
- **Verify before you write.** Use web search to confirm current specs and dates;
  prefer primary sources (standards docs, vendor white papers, IEC text). Mark
  preprints, draft standards, and announcements as provisional in the annotation.
- **Do not invent numbers.** If a value is uncertain, state the range and cite the
  source, or leave a clearly marked `% TODO(verify): ...` comment rather than
  fabricating. Do not upgrade a claim beyond what the source supports.

## Cross-reference labels (verified — use these exact strings)

| Concept | Label |
|---|---|
| First-principles energy chapter | `ch:firstprinciples` |
| IM/DD chapter | `ch:imdd` |
| Lasers chapter | `ch:lasers` |
| WDM chapter | `ch:wdm` |
| Validation chapter | `ch:validation` |
| Reliability/mfg chapter | `ch:reliability` |
| Networking chapter | `ch:networking` |
| Power wall / energy per bit | `sec:power` |
| 224G deployment (LPO/COM/TDECQ) | `sec:224g-deploy` |
| 448G modulation debate | `sec:448g` |
| ELS/ELSFP | `sec:elsfp` |
| Module bring-up | `sec:bringup` |
| CMIS (new) | `sec:cmis` |
| Production-representative corners | `sec:prod-corners` |
| Fleet triage | `sec:fleet-triage` |
| GR-468 | `sec:gr468` |
| Wear-out modes | `sec:wearout-modes` |
| Photonic packaging failures | `sec:photonic-packaging` |
| HVM production test (new) | `sec:hvm-test` |
| Supplier execution playbook | `sec:supplier-exec` |
| Laser safety (new) | `sec:laser-safety` |
| Coherent boundary (new) | `sec:coherent-boundary` |

Note: the FIT/DPPM section in Ch6 has no `\label`; if you need to point at it, add
`\label{sec:fit-dppm}` to its `\section{The language of scale: FIT and DPPM}` line
first, then `\Cref` it. Some skeleton comments reference approximate labels
(`sec:power-wall`, `sec:wearout`, `sec:supplier-playbook`); the correct strings are
`sec:power`, `sec:wearout-modes`, `sec:supplier-exec`.

---

## Section 1 — Where coherent takes over

- **File:** `sections/ch02_imdd_fundamentals.tex`, section `sec:coherent-boundary`
  (right after "Reach regimes, and the scope of this book").
- **Goal:** defend the IM/DD scope with a first-principles crossover argument, so
  the interview question "IM/DD vs coherent roadmap?" has a real answer, not "out of
  scope." ~1 page.
- **Subsections and content:**
  1. *The two detection schemes, in one paragraph* — IM/DD sends power, detects power
     (square-law photodiode), discards phase/polarization. Coherent sends
     amplitude+phase on two polarizations, mixes against a local-oscillator laser,
     recovers the full field in DSP. Coherent needs a narrow-linewidth LO, I/Q
     modulator, dual-pol front end, and heavy ADC/DSP. State the cost bluntly: more
     parts, more power, more silicon.
  2. *Why short reach stays IM/DD* — below ~500 m the loss/dispersion budget is small
     enough that direct detection closes the link; IM/DD wins on pJ/bit, die area,
     latency, and BOM. Tie to `ch:firstprinciples` and `sec:power`.
  3. *What coherent buys, and its price* — spectral efficiency (QAM + pol-mux),
     electronic dispersion compensation, LO-gain sensitivity. Price: LO linewidth,
     I/Q modulator, ADC/DSP power and latency, packaging complexity.
  4. *The crossover, and where it is moving* — line sits near 2 km today (campus/DCI
     coherent, intra-DC IM/DD). Inward pressure: 224G+ per-lane tightening IM/DD
     SNR/TDECQ margin, coherent-lite / coherent-for-scale-out proposals. Outward
     pressure: power, and LPO/CPO stripping cost from the short-reach path. Verdict:
     for AI compute fabric IM/DD stays the workhorse through the 224G generation;
     the open question is 448G. Cross-ref `sec:448g`, `sec:224g-deploy`.
- **Numbers to find and cite:** coherent DSP energy (pJ/bit) vs IM/DD DSP; typical
  400ZR/coherent module power vs an 800G IM/DD module; LO linewidth requirement for
  the target QAM. Sources: OIF 400ZR/800ZR, recent coherent-lite papers (mark
  provisional), any coherent-vs-IMDD survey.

## Section 2 — Module management: CMIS

- **File:** `sections/ch05_validation.tex`, section `sec:cmis` (right before
  "Module and system bring-up").
- **Goal:** one focused home for the management layer the book already uses in
  bring-up (`sec:bringup`) and fleet triage (`sec:fleet-triage`). ~1 page.
- **Housekeeping first:** `\firstterm{CMIS}` currently lives in
  `ch07_ai_datacenter_networking.tex` (~line 232), which comes AFTER this section.
  Move the first-use definition here (`\term{CMIS}\firstterm{CMIS}`) and downgrade
  the Ch7 mention to a plain reference. Confirm no double `\firstterm` after.
- **Subsections and content:**
  1. *What CMIS is, and why an optical engineer cares* — Common Management Interface
     Specification (SFF/OIF), a vendor-neutral host-to-module register interface over
     a two-wire bus: identity, monitors, control, and at 224G/448G link-training +
     host SI tuning extensions. It is the host/module contract; bring-up, interop,
     and every field read go through it.
  2. *The module state machine* — Low Power to ModuleReady plus datapath states; the
     host, not the module, enables lasers; ELSFP lasers up before ModuleReady are a
     reject (`sec:elsfp`). Map the bring-up steps in `sec:bringup` onto transitions.
  3. *The memory map: pages, monitors, control* — paged/banked registers; lower page
     identity/status/interrupts, upper pages advanced monitors/thresholds/app-select/
     CDB firmware. DDM/DOM monitors (`\term{DDM}`): per-lane Tx/Rx power, laser bias,
     module temp, supply voltage, alarm thresholds. This is what `sec:fleet-triage`
     reads first.
  4. *CMIS as a validation deliverable* — check in ATP: state machine reaches
     ModuleReady across V/T corners; monitors read true (CMIS Tx power vs DCA, CMIS
     temp vs case T); alarms fire at the right thresholds; firmware ECO-controlled
     (`sec:supplier-exec`). Interop failures are usually CMIS/media-type/firmware, not
     the optics. Land it: at fleet scale the register map is your only eyes on a
     module in the field.
- **Numbers/refs:** current CMIS revision (e.g. 5.x) and the SFF/OIF document number;
  which form factors mandate it (QSFP-DD/OSFP/QSFP112). Source: SFF-8636 / CMIS spec,
  OIF. Reuse existing keys if present.

## Section 3 — Optical safety and laser classes

- **File:** `sections/ch03_lasers.tex`, section `sec:laser-safety` (right after the
  ELSFP validation paragraph, before "CW-WDM source validation").
- **Goal:** the safety responsibility a laser lead owns, made real by gigawatt fleet
  scale and field-replaceable ELS. ~1 page.
- **Subsections and content:**
  1. *Hazard and laser classes* — IEC 60825-1 (and 21 CFR 1040) classes. 1310/1550 nm
     is invisible and beyond the retinal-hazard band but still a corneal/thermal
     hazard; single-mode power in a ~9 um core is high radiance. Class 1 vs 1M (safe
     unless collected by optics) vs 3R/3B. Say where short-reach modules land.
  2. *Hazard level = aggregate, not per-lane* — the safety case scales with total
     launched power; CW-WDM/ELS banks and CPO shelves concentrate many lines; MT/MPO
     ferrules break out many fibers, so one open connector can exceed a per-fiber
     class. ELS architecture and fiber count drive the classification (`sec:elsfp`).
  3. *Open-fiber protection: APR and ALS* — `\term{APR}` (automatic power reduction) /
     `\term{ALS}` (automatic laser shutdown): drop or cut power on LOS/open-fiber,
     then restart-pulse to probe for re-mate. Tie to the CMIS host-commanded-laser
     rule (`sec:bringup`, `sec:cmis`). This is what makes a live fiber safe to pull
     during ELS hot-swap.
  4. *What validation and ops owe* — verify APR/ALS trip threshold and timing in ATP;
     label modules/cages with class; interlocks and procedures for MPO service;
     document max launched power per port. Fold the APR/ALS check into the ELS
     hot-swap corner (`sec:prod-corners`).
- **Numbers/refs:** Class 1/1M accessible-emission limits at 1310/1550 nm; typical
  per-fiber launch vs an aggregated MPO/ELS port; APR/ALS behavior per ITU-T G.664.
  Sources: IEC 60825-1, ITU-T G.664, ELSFP MSA. Add bibitems as needed.

## Section 4 — Production test at volume

- **File:** `sections/ch06_reliability_manufacturing.tex`, section `sec:hvm-test`
  (between "Photonic packaging and module-level failures" and "Supplier execution
  playbook").
- **Goal:** the manufacturability leg: the mechanics of testing millions of units.
  ~1 page. Tie to NPI gates (`tab:npi`), ATP (`sec:supplier-exec`), DPPM/FIT.
- **Subsections and content:**
  1. *Test time is a cost, coverage is a risk* — every ATP second times millions is
     line capacity and money; every skipped measurement is escaped DPPM. Name the
     expensive optical steps: thermal soak/corners, TDECQ on a DCA, low-BER dwell,
     burn-in. What can be gated-and-sampled vs what must be 100%.
  2. *Where the test happens: wafer, die, module, system* — wafer/PIC probe (known-
     good-die) kills process defects cheaply pre-package; module ATP is the full
     functional/optical test; system/host bring-up catches interop. Push coverage
     upstream where it correlates. Note what wafer test cannot catch (fiber attach,
     FAU, connector), which must survive to module ATP (`sec:photonic-packaging`).
  3. *ATE-to-bench correlation* — production testers are fast and cheap, not lab-grade.
     What matters is correlation: does ATE TDECQ/OMA/sensitivity track the DCA/BERT
     reference within a known offset and spread? Set guardbands from the spread. Keep
     golden-unit and cross-tester gauge R&R discipline. Tie to CMIS monitor
     correlation (`sec:cmis`).
  4. *Screens, guardbanding, and SPC* — burn-in/HTOL screen for infant mortality
     (`sec:wearout-modes`) vs its cost and escape rate; test limits guardbanded
     tighter than spec to hold field DPPM; SPC on LIV/SMSR/RIN/TDECQ by lot/site/
     date-code to catch a shift before it becomes an 8D (`sec:supplier-exec`). Land
     it: production test is a yield/DPPM/cost optimization under a fixed reliability
     target.
- **Numbers/refs:** representative ATP test-time targets and cost-of-test framing;
  KGD/wafer-test coverage for silicon photonics; gauge R&R acceptance thresholds.
  Sources: SiPh wafer-test literature, cost-of-test references; mark any vendor
  numbers provisional.

---

## Order of work (suggested)

1. CMIS (`sec:cmis`) — also do the `\firstterm` move; it's the highest-value gap.
2. Coherent boundary (`sec:coherent-boundary`) — most likely interview trap.
3. Production test (`sec:hvm-test`).
4. Laser safety (`sec:laser-safety`).

After each: compile, confirm ~121 page count, zero undefined refs/citations, then
move on. Remove the `% SKELETON` / `% TODO` comment block from a section once its
prose is complete.
