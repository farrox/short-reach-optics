---
layout: default
title: "Ch 13: Optical Measurement and Test Reference"
---

# 13 Optical Measurement and Test Reference

This appendix is a lookup reference for measurement selection, metric conditions, instruments, stressed-receiver methods, link-budget accounting, and CMIS diagnostics. It does not define the product-readiness lifecycle; that story lives in Chapter 7.

*Read first:* measurement selection by question; metric and plane table; TDECQ and SECQ distinctions; consistent link-budget accounting.

*Reference:* instrument quick reference; CMIS state and diagnostics; Rapid Interview Checks.

## Measurement selection by engineering question

Name the question and reference plane before selecting the instrument. Use the least complex measurement that can falsify the leading hypothesis or support the required decision.

Where is the power?

: Power meter for average power; DCA for OMA. Walk planes before you change bias.

Did modulation quality move?

: DCA for PAM4 eyes, TDECQ, OMA, RLM (Appendix E.3).

Did the spectrum or grid move?

: OSA or wavemeter for wavelength, SMSR, and side modes (Chapter 5).

Did receiver margin shift or floor?

: BERT with calibrated attenuator or stressor; FEC counters for shape (§4.4, Appendix E.4, Appendix H.19).

Is intensity noise the floor?

: PD plus ESA or a dedicated RIN analyzer under a defined ORL (§4.3.1).

Is the error random, bursty, or state-driven?

: Pre-FEC BER plus FEC histograms and management state (Appendix H.19, Appendix E.7).

Does management telemetry match bench truth?

: Host or CMIS tool versus external meter at a named plane (Appendix E.7).

Use electrical loopback, optical loopback, and golden-host or golden-module swaps to bisect ownership before opening supplier FA.

## Metric and reference-plane table

<table class="book-table"><tr><th>Metric</th><th>Required condition and plane</th><th>Typical class</th><th>Establishes</th><th>Does not establish</th></tr><tr><td>OMA / TDECQ</td><td>Named pattern, EQ, temperature; Tx optical plane</td><td>Tx quality</td><td>Modulated quality vs reference receiver</td><td>Unique physical mechanism</td></tr><tr><td>ER / RLM</td><td>Same plane as OMA</td><td>Tx levels</td><td>Level structure and usable swing</td><td>Receiver sensitivity alone</td></tr><tr><td>Wavelength / SMSR</td><td>Grid window; spectral plane</td><td>Spectral</td><td>Grid placement and mode purity</td><td>BER floor ownership</td></tr><tr><td>RIN</td><td>Stated ORL and bias quietness</td><td>Intensity noise</td><td>Signal-proportional noise contribution</td><td>That every BER floor is RIN</td></tr><tr><td>IL / ORL</td><td>Connector class, plant, cleanliness</td><td>Channel</td><td>Power and reflection assumptions</td><td>Signal-quality closure</td></tr><tr><td>Rx sensitivity</td><td>Plane, BER/FEC, pattern, stress</td><td>Receiver</td><td>Minimum OMA for objective</td><td>Unstressed field plant alone</td></tr><tr><td>Pre-FEC BER / FEC histogram</td><td>Named FEC and dwell</td><td>Link/system</td><td>Error rate and burst vs sparse shape</td><td>Confirmed mechanism alone</td></tr><tr><td>CMIS state / DDM</td><td>Host sequence; named monitors</td><td>Control</td><td>Management and diagnostic path</td><td>Optical mechanism by itself</td></tr></table>
**Table E.1.** Metric lookup: conditions, what the measurement establishes, and what it does not. Instrument choices are in Appendix E.1.

##### Channel evidence.

Insertion loss, ORL, dispersion, and filtering belong with the plant assumptions used in the link budget. Reflections can seed feedback noise, MPI, distortion, and power-independent floors even when average power is stable (§4.3.1, Chapter 5).

## TDECQ reference

*TDECQ* (transmitter and dispersion eye closure quaternary) asks how much worse a PAM4 transmitter is than an ideal source after a defined reference receiver and bounded equalizer. Use the exact PMD clause for filter, equalizer limits, histogram locations, and target error ratio.

Representative procedure: capture the optical waveform on a DCA through the clause reference receiver; apply the reference FFE; evaluate noise at the required PAM4 thresholds; report the dB ratio of ideal versus measured tolerable noise. Lower is better; the numeric cap is PMD-specific.

TDECQ is a composite metric. Uneven levels point toward modulator or driver linearity (RLM). Residual eye closure the equalizer cannot remove points toward excess ISI or limited bandwidth. A noise-limited result points toward low OMA, RIN, or reflections. Passing average power does not establish a valid PAM4 transmitter. Do not double-count TDECQ in a link budget that already embeds the compliance OMA/TDECQ relationship (Appendix E.5).

## SECQ and stressed-receiver reference

*SECQ* (stressed eye closure quaternary) is a *receiver-side* stressed-eye method under a named specification. It applies a calibrated optical stressor and asks how much margin remains before the receiver hits that clause's target pre-FEC metric.

TDECQ evaluates transmitter quality through a reference-receiver model. SECQ is not the same test as a generic stressed-receiver sensitivity sweep, even when both use attenuation and ISI. Always state the PMD, FEC architecture, error model, metric, stress calibration, and test duration. For LPO, stressed Rx margin on the host-side receiver is as important as transmitter-quality metrics (§3.6, Appendix H.5.1).

## Link-budget accounting reference

A link budget is a signed ledger from transmitter to receiver. For IM/DD short reach, start from outer OMA at a named Tx plane, subtract each loss once, and compare the remainder to receiver sensitivity at the named BER or FEC objective (§3.12, §4.4).

<pre class="dectree" aria-label="Transmitter output (OMA)"><code>Transmitter output (OMA)
  |
Coupling loss
  |
Connector loss
  |
Fiber / waveguide loss
  |
Transmitter-quality and other penalties (one convention)
  |
Receiver input
  |
Sensitivity requirement
  |
Remaining margin</code></pre>
Use one internally consistent convention. State whether transmitter-quality effects are embedded in the compliance requirement or represented as a separate engineering penalty, and never count the same impairment twice. Do not mix average-power and OMA budgets, reference planes, or embedded and explicit transmitter penalties.

Keep power, signal-quality, timing, thermal, and control authority as separate ledgers when the impairment is not a pure optical-power number (§5.19, Appendix D.10). Distinguish design allocation from measured net margin across the operating envelope.

## Instrument quick reference

Power meter

: Average optical power at a named plane; does not measure OMA or eye quality.

DCA / sampling oscilloscope

: Eyes, TDECQ, OMA, RLM with a reference receiver matched to the PHY.

BERT and FEC counters

: Pre- and post-FEC BER, dwell, and histogram shape.

VOA / calibrated stressor

: Controlled attenuation and optional ISI for sensitivity and stressed-receiver work.

OSA / wavemeter

: Wavelength, SMSR, side modes.

ORL / reflection setup

: Plant return-loss condition for RIN and burst investigations.

RIN measurement

: PD plus ESA or RIN analyzer under defined ORL and quiet bias.

Chamber / TEC

: Temperature corners for reversible operation and lock behavior.

CMIS / host tools

: Management state, DDM correlation, alarms, and recovery.

## CMIS and diagnostic reference

*CMIS* (Common Management Interface Specification) is the vendor-neutral management layer between a host and a module that implements it. Form factors and optional pages vary; do not imply identical behavior across pluggables, ELSFP, and CPO engines .

The host drives a module state machine toward ModuleReady before authorizing light. Data-path and network-path states in later CMIS revisions refine lane enable. A module forced into an emitting state that passes BER has not passed bring-up if the required management sequence, safe state, diagnostics, alarms, and recovery behavior are incorrect (§7.11).

*DDM* provides per-lane Tx/Rx power, bias when exposed, temperature, rails, LOS/LOL, and alarms. On bring-up, dump the register map you will use in the field and treat disagreement between DDM and an external meter as a finding. ATP should prove ModuleReady across voltage and thermal corners and ECO-control firmware like other production revisions (Appendix G.16).

Operational use of management state is decision-oriented, not a register inventory (Chapter 7, Appendix H.22):

- Management state must be trustworthy before counters drive containment.

- Every counter needs a semantic definition, accumulation window, and reset behavior.

- Polling cadence sets what bursts and short recoveries you can observe.

- A reset or clear can erase the failing evidence; preserve dumps before recovery when the event matters.

- Alarm latching and clearing must be understood before a "cleared" flag is treated as healthy.

Exact page, bank, and bit maps remain vendor- and revision-specific; keep them in the product management reference, not in the operational chapter.

## Rapid Interview Checks

##### Prompt.

What does a passing average-power measurement fail to establish?\
*Check.* Modulation quality, eye closure, level linearity, and signal-quality margin.

##### Prompt.

What must accompany a sensitivity number?\
*Check.* Optical reference plane, BER or FEC condition, pattern, temperature, wavelength, and stress method when claimed (Chapter 7, §4.4).

##### Prompt.

How does SECQ differ from generic stressed sensitivity?\
*Check.* SECQ is a named stressed-eye method under a clause; generic stressed sensitivity is not automatically SECQ (Appendix E.4).

##### Prompt.

What does a locked flag fail to prove?\
*Check.* Margin, interoperability, and that the supported plant and host corners remain closed.

##### Prompt.

Why can TDECQ be double counted?\
*Check.* Embedding compliance OMA/TDECQ and also subtracting an independent TDECQ penalty taxes the same impairment twice (Appendix E.5).

##### Prompt.

Which decision should precede instrument selection?\
*Check.* Name the question, population, condition, and reference plane; then choose the least complex measurement that changes the decision (Appendix E.1).


<div class="nav-links">
  <a href="ch12-engineering-decision-trees">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch14-reliability-qualification-reference">Next &rarr;</a>
</div>
