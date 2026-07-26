# Errata — Short-Reach Optics for AI Compute (v1.0.0)

Release-candidate audit against freeze baseline `d12cc0f` (373 pages). Later
clarifications (including the validation-ladder prose rewrite) are logged below.
No new frameworks or chapters.

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

## Typographical fixes

- None beyond the wording edits above in this pass.

## Future ideas (not committed)

- Exhaustive caption retrofit for every ASCII `dectree` (title + takeaway).
- Full glossary pass renaming remaining colloquial “root cause” in historical
  industry phrases where the term is conventional (kept only where confirmed).
- Optional HTML search index beyond TOC (out of scope for freeze).
- Deeper CEI-224G draft clause citations as IAs stabilize (numbers are
  provisional where marked).
