# Errata — Short-Reach Optics for AI Compute (v1.0.0)

Release-candidate audit against freeze baseline `d12cc0f` (373 pages). Later
clarifications (including the validation-ladder prose rewrite) are logged below.
No new frameworks. Structural relocation of existing material is allowed.

## Technical corrections

- **Link budget / TDECQ double-count:** Clarified that TDECQ (or a TDECQ-coupled
  OMA limit / SECQ-stressed sensitivity) must not be debited twice when closing
  margin (`ch02` mental model; `ch07` MSA illustrative budget note).
- **Post-FEC / “error-free”:** Replaced universal “error-free $<10^{-12}$”
  language in the post-FEC term snip with a named residual / FLR / UCR objective
  plus duration.
- **BER plane labels:** Pre-FEC vs post-FEC and FEC-threshold context added where
  debug examples used bare $10^{-12}$ / $10^{-6}$ classes (`ch_models` debug and
  self-test; CEI-224G table caption in `ch02`).
- **Sensitivity measurement:** Receiver sensitivity wording now requires named
  BER plane, pattern, EQ, and reference plane (`ch05`).
- **RIN vs OSA:** Separated OSA (SMSR/spectrum) from PD+ESA / RIN analyzer
  (intensity noise) in reliability learning summary and BER-floor debug list
  (`ch06`, `ch_models`).
- **Premature root-cause claims:** Softened fleet triage language that treated
  ORL/RIN and ELSFP-swap signatures as confirmed mechanisms before confirmation
  evidence (`ch05`).

## Clarifications

- **Debugging pyramid:** Renamed “physical root cause” layer to “confirmed
  mechanism (evidence)” and stated the pyramid is a scope order inside the Staff
  loop, not a second philosophy (`ch01`;
  `\Cref{sec:interview-staff-pattern}`).
- **Bayesian keyidea:** Reframed as belief update *inside* the Staff loop, not
  a competing framework (`app:interview-review`).
- **Validation stage tree:** Renamed “Qualification lifecycle” wall chart to
  “Validation stage order” and tied it explicitly to `tab:ladder`
  (`app:decision-trees`).
- **Validation vs qualification vocabulary:** Laser source matrix “Validation
  burden” → “Evidence burden” with note that ATP/characterization and life
  qualification are separate jobs (`ch03`). Qual-stage prose “validates the net
  behavior” → “measures net remaining margin” (`ch05`).
- **Root-cause wording:** Glossary 8D/CAPA, escape-tree prose, and Staff
  appendix now prefer “confirmed mechanism” until evidence closes.
- **Chapter endings / navigation:** Kept existing takeaway + three questions;
  preface Incident mode now points at validation ladder and reliability homes.
  Forward maps already present in Ch1 / first-principles were left as the
  navigation spine.
- **Interview frameworks:** Validation-plan close now ends on gate decision +
  control owner; “refuse any test” → “refuse any measurement.”
- **Validation ladder prose:** Rewrote `sec:validation-workflow` as a causal
  narrative (bring-up → characterization → margin/interop → qualification →
  production → pilot/fleet) before a single Stage/Question/Evidence/Decision
  reference table. Stage subsections are short prose plus Evidence/Exit/Decision
  blocks; duplicate Purpose/Uncertainty field lists and Learning summary removed
  (`ch05`).
- **Validation chapter opening:** Replaced Question/Purpose/Examples definition
  list with causal prose on how characterization, verification, validation,
  qualification, and production test/ATP differ, then one
  Term/Question/Decision table (`tab:validation-jobs`) (`ch05`).
- **Prose-first pass (Ch5–8, Ch10):** Replaced spreadsheet-style
  Purpose/Uncertainty/Decision cards with causal prose before one reference
  table (or checklist). Ch8: qualification as life/variation argument, wear-out
  in three mechanism families, NPI maturity prose, ATP by evidence-purchase
  category, gauge R\&R wording for HTML. Ch10: incident-path opening,
  recurrence-control closure once, BER floor nested under waterfall-first BER
  increase, FA output categories moved to checklist close. Ch5: architecture
  story after source matrix, LIV/SMSR/RIN questions and bench order, calibration
  vs exhausted-margin distinction, reference labels on bias-driver/pinout/safety/
  CW-WDM survey. Ch7 leftovers: one-module five-jobs example, instruments by
  question, CMIS sequence primary with table as quick reference, production
  corners in four groups, link-budget walkthrough before Method A/B. Ch6 light
  hierarchy: MUX signal journey, capture/hold before actuators, CW-WDM
  architecture before MSA reference, SOA/polarization interview takeaways.
  Interview reading-path blurbs (Read first / Deep dive / Reference) at chapter
  tops. Net PDF pages 369 to 361.
- **Validation flow (Ch7 numbered spine):** Replaced the overlapping lifecycle
  prose, Stage/Question/Evidence/Decision table, ``New product uncertainty''
  evidence dectree, and stage-order/learning-summary restatements with one
  numbered 11-step flow: shaded Steps 1--11 overview (`tab:ladder`), causal
  ``One lifecycle'' prose, Step subsections (margin + interoperability merged
  as Step~5), ``Choosing evidence within a step,'' and a Staff takeaway. App~C
  wall chart updated to the same 11 Steps (`ch05`, `app:decision-trees`).
- **Ch8 qualification story + NPI maturity:** Expanded the laser-degradation
  worked story (requirement → threat → HTOL strategy → observables →
  acceptance → production control) to precede `tab:qual-planning-matrix` as
  reference; demoted GR-468 inventory after the matrix. Rewrote NPI as one
  EVT→…→MP maturity narrative with the gate table as retrieve
  (`ch06`).
- **Split reliability from manufacturing:** Former combined Ch8
  (`ch06_reliability_manufacturing`) is now Ch8 reliability qualification
  (`ch06_reliability.tex`, `\label{ch:reliability}`) and Ch9 manufacturing
  validation (`ch07_manufacturing.tex`, `\label{ch:manufacturing}`). Later
  chapters renumber (+1). Ch7 Steps 6--7 hand off to those chapters; App~C
  wall chart annotates the same split. HTML routes shifted; stubs remain at
  old `ch8-reliability-and-manufacturing-at-scale`,
  `ch9-ai-datacenter-networking`, and `ch10-failure-analysis-handbook`.
  PDF about 365 pages (near length-neutral versus prior ~359).
- **Ch1 orientation rewrite:** Retitled to ``From Optical Physics to a
  Shippable Interconnect'' (`ch:role`). Leads with the gap between device
  science and a shippable product, maps architecture choices and later
  chapters, then retains AI-interconnect motivation after the roadmap.
  HTML slug changed; stub at `ch1-why-the-interconnect-matters`. Ch1 about
  12 pages; PDF about 371 pages.
- **Ch7/Ch8 Interview Q\&A:** Replaced end-of-chapter cold-question lists with
  15 spoken-style interview questions each (strong answer, follow-ups,
  interviewer intent, weak answer) plus a shared 0--10 self-assessment rubric
  (`sec:validation-interview-qa`, `sec:reliability-interview-qa`). PDF about
  387 pages.
- **Ch7/Ch8 Interview Q\&A compression:** Cut each chapter to 12 compact
  questions (Spoken answer / Pressure follow-up + Answer pivot / Trap). Dropped
  long interviewer-intent and weak-answer essays. Moved the chapter-end
  spoken-answer rubric to App~A (`sec:chapter-interview-rubric`); kept the
  case/debug rubric at `sec:interview-scoring-rubric`. Corrected the
  temperature characterization case (conditions; non-causal). HTOL and
  laser-aging distinguish engineering-access vs bookended proxies. PDF about
  381 pages.
- **Ch8 Interview Q\&A coverage revision:** Replaced the 12 compact questions
  so the set tests the full qualification chain (FIT/DPPM and zero-fail
  bounds, bathtub timing, cycling/shock/vibration, damp heat and connector
  durability, GR-468/GR-1221/JESD47 ownership, acceptance/sufficiency,
  restricted release, burn-in versus qual HTOL). Corrected prose that treated
  qualification HTOL as a routine infant-mortality screen and ESD/latch-up as
  generic 100\%-screen items; deleted the competing Requirement→Budget
  dectree; marked fabric availability as a deep dive. PDF about 383 pages.
- **Ch9 Interview Q\&A and manufacturing controls:** Replaced the eight-item
  concise-answer list with 12 compact Spoken/Pressure/Trap questions
  (`sec:manufacturing-interview-qa`). Added process capability ($C_p$/$C_{pk}$),
  specification vs control vs ATP limits (`sec:process-capability`). Softened
  lot/station correlations to hypotheses; redefined potential vs confirmed
  manufacturing escapes; broadened recurrence controls beyond ATP-only;
  corrected requirements/ATP contract language; clarified golden units, ATP
  fault-injection validation, and source vs closed-module access. PDF about
  389 pages.
- **Ch10 Interview Q\&A and operational vocabulary:** Added operational events,
  FEC interpretation, retrain/flap counters, architecture ownership table, and
  MTBF/MTTR availability starter (`sec:networking-ops`). Replaced three self-test
  questions with 12 compact Spoken/Pressure/Trap questions
  (`sec:networking-interview-qa`). PDF about 397 pages.
- **Ch11 Interview Q\&A and FA discipline:** Added evidence-state vocabulary,
  expanded FA output categories, incident-record template, swap-evidence and
  correction-versus-recurrence prose; softened premature mechanism and
  ATP-default recurrence language; aligned the opening incident dectree with the
  eight-step checklist. Replaced three self-test questions with 12 compact
  Spoken/Pressure/Trap questions (`sec:failure-analysis-interview-qa`). PDF about
  405 pages.
- **Ch5 Interview Q\&A and source-selection prose:** Corrected taxonomy
  (VCSEL/DFB structures; DML mode; EML laser+EAM; SiPh platform, not a laser
  family), decision order, and requirements-vs-ATP language (`tab:laser-prd`
  Evidence / production control; life row not ATP). Softened blanket laser
  reliability-bottleneck claim; bounded qualification FIT language; added access
  ladder, transmitter-quality metrics table, five-ledger double-count caveat,
  and RIN/driver-noise spectral-density caveat. Replaced three self-test
  questions with 12 compact Spoken/Pressure/Trap questions
  (`sec:lasers-interview-qa`). PDF about 413 pages.
- **Ch6 Interview Q\&A and wavelength-control prose:** Softened locking$\neq$WDM
  / microring language; distinguished capture, hold, reacquisition, and control
  headroom; added lock-evidence and guardband ledgers, open-loop vs closed-loop,
  loop-stability signatures, and access-aware ATP language. Softened comb market
  claims and external-laser FIT wording; corrected neighbor-load recurrence
  control (not automatic ATP). Replaced three self-test questions with 12 compact
  Spoken/Pressure/Trap questions (`sec:wdm-interview-qa`). PDF about 421 pages.
- **Appendix interview-practice update:** App~A gains a Weak/Competent/Staff
  worked scoring example on the shared chapter spoken rubric
  (`sec:chapter-rubric-example`). Glossary Rapid Interview Checks
  (`sec:glossary-rapid-checks`). App~D Decision-Tree Interview Drills (8 scenarios)
  plus tree/swap/retest boundary language (`sec:tree-interview-drills`). App~B
  staged mock interviews (fleet BER bursts, yield after supplier change, hot WDM
  unlock) scored with the case rubric; slimmed `sec:case-grading` to an App~A
  pointer. No second lifecycle or appendix 12-question Interview Q\&A. PDF about
  427 pages.
- **Ch4 Interview Q\&A and quantitative-model prose:** Added model-fidelity
  ladder, reference-plane/metric table, noise-bandwidth and variance-addition
  limits, RIN metric definitions and simplified dominant-RIN ceiling language,
  sensitivity assumptions, BER-waterfall signature table, model-to-bench
  correlation, softened detector/PAM4 claims, and named recurrence controls for
  BER floors. Debug fork routes investigation without claiming mechanism
  ownership. Replaced three self-test questions with 12 compact
  Spoken/Pressure/Trap questions (`sec:models-interview-qa`). HTML aux parser
  now resolves labels whose titles contain nested braces (e.g.\ `sec:qber`).
  PDF about 435 pages.
- **Ch7 product-readiness terminology:** Retitled Chapter~7 to Optical Product
  Readiness: From Requirements to Fleet (`ch:product-readiness`; keep
  `ch:validation` alias). Product-readiness lifecycle is the 11-step umbrella;
  system validation is Step~5 only (verify requirements vs intended use).
  EVT/DVT/PVT are program-phase labels with sidenotes and mapping table.
  Updated evidence-discipline table, Step~6/~7 boundaries, Interview Q\&A,
  Ch8--11 cross-language, App~C wall chart, glossary, and App~A readiness
  ladder wording. Old HTML slug redirects from `ch7-optical-validation`.
  PDF about 441 pages.
- **Ch7 compression and measurement appendix:** Cut Chapter~7 from about 44 to
  about 16 pages (body $\sim$2150 to $\sim$840 lines) by relocating instrument,
  TDECQ/SECQ procedure, measurement-mapping, link-budget accounting, and CMIS
  register detail to new Appendix~E Optical Measurement and Test Reference
  (`app:measurement-reference`). Removed Method~A/B naming. Moved FEC histogram
  teaching to Chapter~10 (`sec:fec-symbol-histogram`) and fleet-triage plus
  power/quality fork detail to Chapter~11 (`sec:fleet-triage`,
  `sec:validation-fork`). Kept 11-step lifecycle, Step~5 split, bring-up/corners,
  and 12 Interview Q\&As. HTML references page shifted to `ch20-references`;
  stub retained at `ch19-references`. PDF about 427 pages.
- **Ch8 compression and reliability appendix:** Cut Chapter~8 from about 20 to
  about 16 PDF pages (body $\sim$978 to $\sim$841 lines including 12 Q\&As) by
  relocating standards detail (GR-468, GR-1221, JESD/ESD/latch-up, AEC-Q100),
  stress-method quick reference, sample/confidence arithmetic, full planning
  matrix, and connector/optical-interface methods to new Appendix~F Reliability
  Qualification Reference (`app:reliability-reference`). Consolidated plural
  qualification flows into one claim$\rightarrow$mechanism$\rightarrow$evidence
  argument (`sec:qual-argument`); one worked laser-aging walkthrough; HTOL versus
  burn-in stated once; replaced triage-oriented wear-out map with compact
  mechanism-family table (`tab:qual-mechanism-families`, alias
  `tab:wearout-map`). Moved fabric-availability arithmetic to Chapter~10
  (`sec:fabric-availability`); ATP/SPC/DPPM production-control depth to
  Chapter~9; date-code/8D/CAPA and field-bucket triage teaching to Chapter~11.
  Removed the Engineering lens block. Kept FIT primary and 12 Interview Q\&As.
  HTML routes: reliability reference at `ch17-reliability-qualification-reference`;
  references at `ch21-references` with stubs at `ch19-references` and
  `ch20-references`. PDF about 441 pages.
- **GR-468 as evidence source:** Rewrote Appendix~F GR-468 section as an
  evidence-source argument (incomplete ``passed GR-468'' checklist; does not
  establish readiness alone). Added ownership table covering GR-468, GR-3013,
  GR-1221, GR-1209, and JEDEC methods (`tab:gr-standards-ownership`). Moved
  Bellcore/Telcordia history to a sidenote. Kept OpenLight 2025 GR-468 report
  as a labeled industry-example case box with provisional hour counts.
  Ch8 standards table now points at GR-3013/GR-1209. PDF about 445 pages.
- **Latch-up checkpoint ownership:** Chapter~8 keeps latch-up as a short
  electronics-qualification checkpoint (susceptibility, not Arrhenius wear-out)
  with a one-row Method/Contribution/Limitation table
  (`tab:latchup-checkpoint`). JESD78 test classes, I-Test/E-Test injection,
  Class~I/~II temperature, and acceptance-current detail live in Appendix~F
  (`sec:latch-up`). A component pass does not claim module hot-plug or
  sequencing immunity. PDF about 445 pages.
- **Ch9 lean spine and manufacturing appendix:** Retitled Chapter~9 to
  Manufacturing Validation: Reproducing and Controlling the Design. Reordered
  around freeze $\rightarrow$ builds/genealogy $\rightarrow$ MSA
  (`sec:gauge-rr`) $\rightarrow$ yield $\rightarrow$ capability $\rightarrow$
  controls (`sec:hvm-test`, `tab:mfg-control-types`) $\rightarrow$ SPC/ramp
  $\rightarrow$ supplier/change (`sec:supplier-exec`) $\rightarrow$ escapes
  $\rightarrow$ case study. Relocated NPI table (`tab:npi`), laser ATP checklist
  (`tab:atp-laser`, `sec:atp-laser-read`), FAIR/gauge/control-plan templates, and
  Rapid Interview Checks to new Appendix~G Manufacturing Validation Reference
  (`app:manufacturing-reference`). Phase-label ownership stays in Chapter~7;
  detailed 8D/CAPA/DPA procedure moved to Chapter~11 (`sec:mfg-8d-capa`). Removed
  the Engineering lens. Kept the worked yield case and all 12 Interview Q\&As.
  Body cut from $\sim$794 to $\sim$509 lines; PDF Chapter~9 about 24$\rightarrow$16
  pages. HTML title mapping adds Appendix~G only (A--D lettered titles unchanged);
  old Ch9 slug redirects; references page at `ch22-references` with stubs at
  `ch19`--`ch21-references`. PDF about 447 pages.

## Typographical fixes

- None beyond the wording edits above in this pass.

## Future ideas (not committed)

- Exhaustive caption retrofit for every ASCII `dectree` (title + takeaway).
- Full glossary pass renaming remaining colloquial “root cause” in historical
  industry phrases where the term is conventional (kept only where confirmed).
- Optional HTML search index beyond TOC (out of scope for freeze).
- Deeper CEI-224G draft clause citations as IAs stabilize (numbers are
  provisional where marked).
