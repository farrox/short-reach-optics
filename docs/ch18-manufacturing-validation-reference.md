---
layout: default
title: "Appendix G: Manufacturing Validation Reference"
---

# Appendix G: Manufacturing Validation Reference

This appendix is a lookup reference for program-gate manufacturing evidence, laser-bearing production-control checklists, gauge and station templates, and supplier first-article packages. It does not build the manufacturing-validation argument. That narrative lives in Chapter 9: freeze the production reference, build representative populations, preserve genealogy, validate the measurement system, map yield, establish capability and guardbands, choose controls, run SPC and reaction plans, manage changes, and feed escapes back into controls.

*Read first:* which gate asks which manufacturing question; how control classes differ.

*Reference:* ATP checklist; FAIR and supplier evidence; Rapid Interview Checks.

## Program-gate manufacturing evidence

Program-phase labels (EVT, DVT, PVT, MP) are owned in §7.1, Table 7.1. They are not a second lifecycle. The table below is a manufacturing-evidence lookup: which release call the gate evidence supports when the program uses those names.

<table class="book-table"><tr><th>Gate</th><th>Question</th><th>Representative evidence</th><th>Release decision</th></tr><tr><td>EVT</td><td>Does it operate at all?</td><td>First light; CMIS bring-up; basic LIV/SMSR/RIN; one link closes BER</td><td>Continue / redesign integration</td></tr><tr><td>DVT</td><td>Does it meet spec across corners?</td><td>Full ATP at T/V; prod-rep corners; stress plan + FIT model frozen</td><td>Enter qual / PVT / hold</td></tr><tr><td>Qual</td><td>Env / reliability evidence ready?</td><td>Named mechanisms; sample plan; confidence (sec:tree-qual-evidence)</td><td>Enter PVT / hold</td></tr><tr><td>PVT</td><td>Is it buildable at yield?</td><td>Multi-lot first-pass yield; MSA; ATP coverage; process capability; traceability; supplier readiness; validated rework; FAIR; production-host bring-up</td><td>Enter pilot / hold</td></tr><tr><td>Pilot</td><td>Do assumptions hold in a bounded field trial?</td><td>Known serials/lots; enhanced telemetry; exit/rollback criteria</td><td>Open MP / restrict</td></tr><tr><td>MP</td><td>Is quality sustained?</td><td>Steady DPPM; owned RMA Pareto; ECO control; fleet feedback</td><td>Keep shipping / CAPA / restrict</td></tr></table>
**Table G.1.** NPI gates as a manufacturing evidence lookup. Pilot sits between PVT and MP. MP is sustained control, not fleet monitoring alone. Phase definitions: §7.1. Argument structure: Chapter 9.

## Laser-bearing production-control checklist

Every second of ATP costs line capacity. Every omitted screen leaves risk. Buy evidence in categories that cannot substitute for each other. Table G.2 is a working checklist for an EML pluggable or an ELSFP CW module. Customize limits from the datasheet and the link budget; do not invent numbers in the ATP itself. Control-selection logic lives in §9.7, Table 9.4.

##### Every-unit fast screens.

Power class, CMIS state and bring-up, basic lane operation, and selected electrical or optical checks that are cheap enough for 100% coverage. These catch dead units and firmware fails. They do not establish life.

##### Sampled expensive measurements.

TDECQ, intrinsic and stressed RIN, detailed spectrum/SMSR, thermal corners, and longer BER dwell. Use lot sample or audit when the signature is expensive and correlated to escape risk.

##### Qualification-only stresses.

HTOL, humidity, extensive cycling, and destructive analysis gather life or mechanism evidence. They are not per-unit ship screens (Appendix F.1.1, Appendix D.3).

##### Process controls.

SPC on LIV, SMSR, RIN, TDECQ, and mate-cycle yield; golden-unit tracking; gauge R&R; incoming quality; first-article / FAIR after tooling or site change (§9.4).

##### Fleet controls.

Telemetry, lot traceability, RMA codes split by mechanism, and recurrence monitoring (§11.16). These catch what ATP never saw.

A fast production power check does not establish life. HTOL does not prove every shipped unit has correct firmware. SPC does not detect an unmeasured mechanism. Source-level LIV, SMSR, and wavelength measurements can detect selected material or device shifts when those measurements are directly available and correlated to product risk. In a closed module, use a validated module-level proxy, supplier evidence, sampled audit, or genealogy-based control; do not claim internal measurement coverage when the production architecture does not expose it. RIN and ORL protect the reflection environment; EAM/DCA protects Tx quality on EML paths; CMIS protects field evidence. Burn-in may screen a demonstrated infant-mortality population. ESD robustness is primarily established through design qualification and handling controls; a finished-unit production screen may not reliably detect latent ESD damage. Thermal class protects the derate claim.

<table class="book-table"><tr><th>Item</th><th>Method</th><th>Control class</th><th>Pass intent</th><th>Ties to</th></tr><tr><td>LIV (I_th, slope, kink)</td><td>SMU + power meter</td><td>100\% ATP (source) / module proxy</td><td>kink-free bias window</td><td>wear-out, derate</td></tr><tr><td>SMSR</td><td>OSA</td><td>100\% ATP (source) / lot sample</td><td>single-mode vs.\ floor</td><td>modal noise</td></tr><tr><td>Intrinsic RIN</td><td>PD + ESA</td><td>Lot sample / FA</td><td>quiet source floor</td><td>BER floor budget</td></tr><tr><td>Stressed RIN_xOMA</td><td>PD + ESA @ ORL</td><td>Lot sample / 100\% if escape</td><td>stressed Tx metric</td><td>named PMD</td></tr><tr><td>Wavelength / grid</td><td>OSA / wavemeter</td><td>100\% ATP or sample</td><td>channel ID</td><td>WDM lock</td></tr><tr><td>Optical power class</td><td>power meter</td><td>100\% ATP</td><td>class met</td><td>link budget</td></tr><tr><td>EAM / TDECQ (EML)</td><td>bias + DCA</td><td>Lot sample / audit</td><td>ER, RLM, TDECQ</td><td>Tx quality</td></tr><tr><td>CMIS / TWI bring-up</td><td>host / CMIS tool</td><td>100\% ATP</td><td>state machine</td><td>telemetry</td></tr><tr><td>Connector / ORL</td><td>mate + ORL meter</td><td>Periodic audit / sample</td><td>cycles + endface</td><td>packaging</td></tr><tr><td>Burn-in (infant)</td><td>production screen</td><td>100\% or lot sample</td><td>infant culled</td><td>not HTOL life</td></tr><tr><td>HTOL life evidence</td><td>accelerated life</td><td>Qualification only</td><td>mechanism + FIT claim</td><td>GR-468</td></tr><tr><td>Driver/TIA ESD</td><td>JESD47 report</td><td>Qualification / audit</td><td>rating on file</td><td>IC reliability</td></tr><tr><td>Thermal class</td><td>chamber</td><td>Lot sample / SPC</td><td>LIV/RIN/CMIS pass</td><td>derate</td></tr><tr><td>Process monitors</td><td>SPC charts</td><td>SPC / process</td><td>drift detection</td><td>escape prevention</td></tr><tr><td>Fleet cohort metrics</td><td>telemetry</td><td>Fleet telemetry</td><td>trend / alarm</td><td>recurrence</td></tr></table>
**Table G.2.** Control checklist for laser-bearing modules (EML or ELSFP). Control class separates 100% ATP, lot sample, audit, qualification-only, SPC, and fleet telemetry. Intrinsic RIN and stressed $\mathrm{RIN}_x\mathrm{OMA}$ are different metrics.

**Exit for the ATP as a whole:** every ship lot (or defined sample) has traceable pass data against versioned limits tied to the requirements slice. **Decision:** ship, hold, or reopen DVT limits.

## ANOVA gauge R&R sketch

This is a procedure-level sketch, not a statistics course. Worksheets, acceptance tables, and attribute studies live in the AIAG measurement-systems analysis reference . Why measurement-system analysis precedes yield interpretation: §9.4.

A crossed variable study typically uses $n$ parts that span the process range, $k$ appraisers (operators, stations, or shifts), and $r$ replicates of each part$\times$appraiser cell. An ANOVA random-effects model partitions the total observed variance into part-to-part, repeatability (equipment / method variation under fixed appraisal conditions), reproducibility (appraiser or condition contribution, often including part$\times$appraiser interaction), and gauge R&R as the combined measurement contribution.

Report the study with the metric, reference plane, units under test, and the decision the measurement must support. Common summary ratios include gauge R&R as a fraction of total observed variation or of the tolerance width, and the number of distinct categories the measurement system can resolve. Treat those ratios as decision aids for a named ATP row, not as a universal green-light threshold for every optical metric. Destructive or non-replicable tests need alternate designs; do not force a crossed replicate study that the physics cannot support.

## Gauge R&R and station-correlation template

Use this checklist when teaching or auditing a production station. Background and ANOVA sketch: §9.4, Appendix G.3.

- Define the metric, reference plane, and units under test (good, marginal, failing).

- Repeatability: same station, operator, and unit; report within-station spread.

- Reproducibility: across stations, shifts, operators, and fixtures.

- Bias: production station versus reference lab (DCA, BERT, OSA, power meter).

- Stability: golden-unit trend over time; custody, recertification, and retirement criteria for the golden.

- False reject / false accept: guardband from measurement uncertainty.

- Station correlation offset and spread; decision rule for when a station is held.

- CMIS or embedded monitor correlation to the same bench instruments when telemetry is used as a production proxy.

- ANOVA gauge R&R study design and reported variance components when a quantitative measurement-system claim is required (Appendix G.3).

## FAIR and supplier evidence checklist

When tooling, epi, assembly site, driver/TIA silicon, TEC vendor, FAU epoxy, or CMIS firmware changes, require a defined first-article package before open PO volume:

- Change notice: what changed, why, affected lots, and effective date.

- Pre- and post-change genealogy for representative units.

- Measurement-system status: gauge R&R or station correlation still valid for the affected ATP rows.

- Multi-lot first-pass yield and parameter distributions for the changed population.

- Capability and guardband check on critical parameters.

- Qualification re-entry depth when life or environmental mechanisms are affected (Chapter 8, Appendix F).

- Incoming sample plan and SPC metrics with owners and reaction plans.

- ECO and firmware version control matching the production reference freeze in Chapter 9.

## Sample control-plan mapping

Requirements and the production control plan form the contract. Every requirement needs a named evidence source and owner, but that evidence may be ATP, a sampled audit, qualification, process control, supplier evidence, or fleet monitoring.

1.  **Requirements / PRD slice for the laser path:** fill Table 5.4, §5.6 (power class, grid, RIN@ORL, SMSR, derating, CMIS, FIT). Version it with the production control plan.

2.  **Acceptance test plan (ATP):** the measurable tests that prove those requirements on every ship lot (or on a defined sample) when every-unit or sampled production test is the right control. Map each ATP line to a requirement; map life claims to qualification where appropriate (Appendix F.1.1, Table G.2).

> **Engineering heuristic.** If a requirement has no evidence source, owner, or reaction plan, it is a wish. ATP is only one possible control. If an ATP line has no requirement, it is cost without a decision.

## Rapid Interview Checks

These are short prompts for self-test. Worked spoken answers live in §9.13.1.

##### Prompt.

What must be frozen before a production-intent build?\
*Check.* Hardware/BOM, suppliers, firmware, calibration, recipes, fixtures, test software, limits, and explicit deviations.

##### Prompt.

Why clear the measurement system before yield?\
*Check.* Otherwise station drift, golden aging, or bias masquerades as product or supplier failure (§9.4).

##### Prompt.

What proves an ATP screen detects defects?\
*Check.* Naturally failing units or controlled fault injection across severity; detection probability and false rejects. Passing good units is not enough.

##### Prompt.

When is a field fail a manufacturing escape?\
*Check.* Only when evidence ties the mechanism to a preventable production or test-control gap. Otherwise wear-out, interop, install, service, software, or residual latent risk (§9.11, Chapter 11).


<div class="nav-links">
  <a href="ch17-reliability-qualification-reference">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch19-ai-fabric-context">Next &rarr;</a>
</div>
