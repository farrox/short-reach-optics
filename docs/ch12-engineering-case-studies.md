---
layout: default
title: "Ch 12: Engineering case studies"
---

# 12 Engineering case studies

This appendix is practice under incomplete information. The frameworks already live in Appendix A, Appendix C, Appendix D and Table 7.2. Here you apply them. Do not jump to the mechanism. Score yourself with Appendix A.12 after each case.

## Information value

The best next measurement is not the most detailed measurement. It is the measurement that eliminates the most uncertainty at acceptable cost (Appendix A.1, Appendix A.2).

<table class="book-table"><tr><th>Measurement</th><th>Cost</th><th>Information gained</th></tr><tr><td>Telemetry query</td><td>Low</td><td>Population scope, trends, lot/host tags</td></tr><tr><td>Swap / remap experiment</td><td>Low</td><td>Ownership isolation (Tx / Rx / host / plant)</td></tr><tr><td>Attenuation / BER waterfall</td><td>Medium</td><td>Margin shape: shift versus floor</td></tr><tr><td>External optical eye</td><td>Medium</td><td>Signal quality at a named plane</td></tr><tr><td>Optical / package teardown</td><td>High</td><td>Physical mechanism confirmation</td></tr></table>
**Table B.1.** Information value is uncertainty removed per cost. Decision unlocked: which next measurement to buy. Prefer Level 0--2 until those measurements stop reordering beliefs (Appendix A.2).

Bad next step: "Run full optical characterization." Better: "Compare failing and passing units from the same lot," because that separates population effects quickly.

> **Why experienced engineers rank measurements by information value?**
>
> Because the best next test is the one that reorders beliefs the most per minute and per dollar, not the one that fills the most plot panels.

> **Engineering heuristic.** Never spend an hour measuring something that a five-minute swap test can eliminate.

## How interviewers evaluate answers

Use this interview-facing summary. Full detail remains in Appendix A.12 (plane/access, causal discipline, and recurrence are scored there too).

<table class="book-table"><tr><th>Axis</th><th>Score</th><th>Meaning</th></tr><tr><td>Scope</td><td>0</td><td>Jumps to a solution.</td></tr><tr><td></td><td>1</td><td>Asks some questions.</td></tr><tr><td></td><td>2</td><td>Defines population, timeline, and ownership.</td></tr><tr><td>Hypothesis quality</td><td>0</td><td>One explanation.</td></tr><tr><td></td><td>1</td><td>Several guesses.</td></tr><tr><td></td><td>2</td><td>Mechanism-based hypothesis tree.</td></tr><tr><td>Measurement choice</td><td>0</td><td>Lists tests.</td></tr><tr><td></td><td>1</td><td>Lists useful measurements.</td></tr><tr><td></td><td>2</td><td>Chooses by information value and access level.</td></tr><tr><td>Decision quality</td><td>0</td><td>No action.</td></tr><tr><td></td><td>1</td><td>Technical fix only.</td></tr><tr><td></td><td>2</td><td>Containment + correction + prevention.</td></tr><tr><td>Communication</td><td>0</td><td>Rambling.</td></tr><tr><td></td><td>1</td><td>Technically correct but unstructured.</td></tr><tr><td></td><td>2</td><td>Clear executive frame plus engineering depth.</td></tr></table>
## Executive communication

Staff answers must travel upward. Use this frame:

Problem

: What is observed?

Impact

: Who or what is affected, and how large?

Evidence

: What was measured, at what plane and condition?

Confidence

: Observation, correlation, hypothesis, or confirmation?

Containment

: What stops growth now?

Next decision

: What unlocks the next ship or hold call?

Illustrative executive line (Case [12.5](#sec:case-fleet-ber) style): "About three percent of modules from lot X show rising pre-FEC BER after roughly 90 days. Average received power is stable. Evidence points toward analog-supply degradation correlated with that lot. Shipment from the lot is paused while supplier FA proceeds."

## Supplier conversation

Structure supplier calls the same way you structure debug (§8.10, Appendix C.10, Appendix D.9):

<pre class="dectree" aria-label="Supplier conversation framework"><code>Supplier conversation framework
  |
Observed issue
  |
Affected population
  |
Evidence (plane, condition, access)
  |
Requested analysis
  |
Containment
  |
Corrective action
  |
Verification of next lots</code></pre>
Avoid "the vendor caused this." Prefer: "The evidence indicates a supplier-process correlation requiring confirmation."

## Case 1: Fleet-wide BER degradation after deployment

##### Problem statement.

Thousands of optical modules are deployed. Pre-FEC BER rises gradually on a subset of links. Average received power is unchanged. Firmware and host platform are common. Failures correlate with one manufacturing lot. What do you do?

> **What this usually means.** Lot-scoped gradual BER rise with flat average power
>
> *Usually:* process, calibration, component supplier, or attach change inside that lot
>
> *Not:* independent random wear of unrelated serials with no shared history

##### Available information.

Illustrative: rising pre-FEC BER over weeks; Rx power telemetry flat; same CMIS firmware train; one date code / lot dominates the Pareto; sibling lots on the same hosts look healthy.

##### Missing information.

Whether cool-down recovers; whether the waterfall shifts or floors; component genealogy inside the lot; whether monitors agree with external meters; whether a process change landed in that lot.

##### Initial hypotheses.

Transmitter quality, channel / plant, receiver, DSP, control loop, environment. Gross optical loss is deprioritized while average power holds (Appendix D.4). Lot correlation raises process, calibration, or component-supplier hypotheses above exotic new physics.

##### Decision tree.

Walk Appendix D.1, Appendix D.9, Appendix C.9: scope and time behavior; power versus quality; contain if the population can grow; compare good versus bad lots before deep FA.

##### Measurements selected.

Level 0: cohort query by lot, host, temperature, firmware (Table B.1). Level 1: golden swap and dwell on failing versus passing serials. Level 2: BER waterfall and external power at the faceplate. Level 3--4 only after ownership is assigned.

##### Results (staged).

Population is lot-scoped. Average power remains flat on external meter. BER waterfalls show rising floors or soft floors on failing serials, not a uniform power shift. Good-lot siblings on the same host pass. Process history shows a solder / attach change on the failing lot (illustrative).

##### Updated hypothesis.

Leading mechanism: analog supply instability from solder attachment degradation, producing signal-quality loss with stable average optical power. Still a leading hypothesis until physical confirmation.

##### Confirmed mechanism.

Physical inspection and electrical FA confirm solder attachment failure on the analog supply path, correlating with the BER signature. That is confirmation, not the first sentence you say in the interview.

##### Containment.

Pause shipment and further deployment of the affected lot; raise monitoring on installed serials; replace highest-risk units per impact model (Appendix D.16).

##### Corrective action.

Supplier process corrective action on the attach step; incoming inspection or process monitor for the signature; split RMA codes by lot and mechanism class.

##### Qualification / ATP / telemetry update.

Add or tighten the production proxy that would have caught the signature; review whether qual stress covered this mechanism and sample diversity (Appendix D.3, Appendix C.13). Telemetry: alarm on BER trend with stable power for that cohort.

##### Fleet prevention.

Burn down the installed cohort; keep the control owner until rates fall; feed the lesson into §7.1.13.

##### Score yourself.

Use Appendix A.12, Appendix B.2. Fail the drill if you named a component before scope and containment.

##### Executive summary.

Problem: gradual BER rise. Impact: one manufacturing lot in fleet. Evidence: stable average power; lot Pareto; FA confirms solder/supply path. Confidence: confirmed for returned units; fleet correlation strong. Containment: lot hold. Next decision: supplier CA verification on next lots.

##### Deep dive.

Appendix C.1, Appendix C.9, Appendix C.10, Appendix D.9, §10.2.

## Case 2: New optical module supplier qualification

##### Problem statement.

A second-source supplier proposes an "identical" module. How do you qualify?

##### Available information.

Incumbent module is shipping. Supplier offers datasheet alignment and a small set of engineering samples. Target hosts and cable plant are known.

##### Missing information.

Multi-lot distributions; process corners; reliability mechanisms and $E_a$ justification; ATP correlation; interop matrix coverage; pilot plan.

##### Initial hypotheses.

Not "it will work if the datasheet matches." Equivalence must be defined across functional, performance, environmental, reliability, and manufacturing dimensions (Appendix C.7, Appendix C.15).

##### Decision tree.

Freeze requirements first (Table 7.2). Then walk bring-up through margin, interop, mechanism-based qualification, manufacturing validation, controlled pilot, and fleet monitoring. A hero sample is not a gate.

##### Measurements selected.

Black-box: BER, throughput, interop on claimed hosts, margin corners, power and sensitivity distributions across lots. Engineering access only when black-box evidence cannot decide. Reliability: stresses tied to named mechanisms (§8.2).

##### Results (staged).

Illustrative: means look close to the incumbent; spreads are wider on RIN or hot BER; one host/firmware combo fails interop; HTOL needs a process-specific $E_a$ argument the supplier has not yet closed.

##### Updated hypothesis.

Supplier can meet nominal function but has not yet demonstrated distributional equivalence or mechanism-justified life evidence.

##### Confirmed mechanism.

Not applicable until a specific fail mode appears. The decision now is hold or restrict, not a confirmed-mechanism narrative.

##### Containment.

Do not open volume. Limit to lab or controlled pilot serials only.

##### Corrective action.

Require multi-lot data, closed interop matrix, and FAIR before PVT/MP language is used.

##### Qualification / ATP / telemetry update.

Correlate supplier ATP to your proxy; split field RMA codes by vendor from day one; define pilot exit before broader ship (§8.2).

##### Fleet prevention.

Separate vendor codes in telemetry and RMA so a second-source escape cannot hide inside a merged bucket.

##### Score yourself.

Fail if you qualified on one golden sample or copied the incumbent datasheet as the requirement.

##### Executive summary.

Problem: second-source equivalence claim. Impact: single-vendor risk reduction versus escape risk. Evidence: incomplete lot distributions and open interop / life items. Confidence: insufficient for open volume. Containment: no volume ship. Next decision: multi-lot package and pilot exit criteria.

##### Deep dive.

Appendix C.7, Appendix C.15, §8.2, Table 7.2, §8.10.

## Case 3: Temperature-dependent BER failure

##### Problem statement.

A module works at room temperature and fails at high temperature. What do you investigate?

> **What this usually means.** Fails hot, may recover cool, average power looks stable
>
> *Usually:* thermal margin, wavelength or lock, bias tables, receiver noise, mechanics
>
> *Not:* a closed wear-out FIT claim from room-temperature ship data alone

##### Available information.

Illustrative: pre-FEC BER rises above target at high case temperature; average optical power telemetry looks stable; cool-down may or may not recover (not yet stated).

##### Missing information.

Recovery on cool-down; waterfall shape; wavelength walk; actuator headroom; host rail noise at temperature; whether siblings fail the same way.

##### Initial hypotheses.

Do not immediately blame the laser. Build a tree:

<pre class="dectree" aria-label="Temperature-dependent BER hypothesis tree"><code>Temperature-dependent BER hypothesis tree
  |
Temperature increase
  |
Laser efficiency / ER collapse
  |
Wavelength drift
  |
Receiver noise
  |
TIA bandwidth
  |
DSP adaptation
  |
Mechanical alignment
  |
Power supply / PSRR</code></pre>
##### Decision tree.

Appendix C.4, Appendix D.4, §7.1.6: scope; power versus quality; measure remaining margin at the failing temperature first.

##### Measurements selected.

Level 0--1: BER/FEC and telemetry at failing $T$; cool-down trial; sibling compare. Level 2: waterfall, external power, wavelength if telemetry weak. Level 3 (if access): bias sweep, external eye, OSA, TEC/heater codes (Appendix A.2).

##### Results (staged).

Illustrative path A: cool-down recovers; bias sweep restores the external eye; calibration table segment boundary is wrong. Path B: actuator railed; thermal design lacks headroom. Path C: waterfall floors; ORL or RIN path needs work. Pick measurements that reorder these beliefs quickly.

##### Updated hypothesis.

Leading mechanism follows the path that survived the staged cuts. Speak the update aloud after each measurement.

##### Confirmed mechanism.

Only after controlled confirmation (bias restore, thermal redesign proof, or ORL dependence). Until then it remains leading.

##### Containment.

Restrict deployment temperature or hosts if fleet risk exists; do not wait for perfect FA before ownership actions.

##### Corrective action.

Retune tables, fix thermal design, or screen the ORL-sensitive population, as dictated by the confirmed path.

##### Qualification / ATP / telemetry update.

Put the loaded hot corner in ATP; watch control-ledger headroom in telemetry.

##### Fleet prevention.

Alarm on hot BER with stable power and railed actuators.

##### Score yourself.

Fail if the first sentence was "the laser died" without a hypothesis tree.

##### Executive summary.

Problem: BER fail at high temperature, power stable. Impact: envelope risk. Evidence: (state path A/B/C after your measurements). Confidence: leading until confirmed. Containment: temperature or SKU restrict if needed. Next decision: table, thermal, or ORL control with ATP corner.

##### Deep dive.

Appendix C.4, §7.1.6, Appendix A.10.3, §10.12.

## Case 4: Qualification escape

##### Problem statement.

The product passed qualification. About six months later, field failures appear. Why did qualification miss it?

##### Available information.

Illustrative: qual report shows HTOL and environmental passes on engineering lots; field fails show a mechanism or environment not stressed, or a lot/site not represented in the qual sample.

##### Missing information.

Exact field mechanism; whether production process matches qual hardware; whether the observable used in qual could see the failure; sample diversity (lots, date codes, sites, corners).

##### Initial hypotheses.

Do not stop at "qualification was insufficient." Prefer mechanism-level explanations:

Wrong failure mechanism

: Stress did not accelerate the real wear-out.

Insufficient sample diversity

: Wrong lots, sites, or corners (§8.2).

Measurement gap

: No observable tracked the degrading signature.

Production difference

: Qual hardware or process differed from volume.

Fleet condition

: Real environment exceeded qual assumptions.

##### Decision tree.

Appendix D.3, §10.13, Appendix C.13: name the missed uncertainty; choose containment; update the evidence path and production proxy.

##### Measurements selected.

Reproduce field signature at a named plane; compare qual versus production genealogy; check whether ATP would separate good versus bad today; FA/DPA only after black-box ownership.

##### Results (staged).

Illustrative: field fails cluster on a production site absent from qual; or humidity-driven corrosion appears though damp heat used a different observable; or qual used hand-built engines while volume uses a new attach process.

##### Updated hypothesis.

State which miss class is leading. Keep others alive until ruled out.

##### Confirmed mechanism.

After FA and process compare, name the confirmed mechanism and the miss class (design, process, supplier, test escape, or still unknown).

##### Containment.

Hold affected lots/sites; expand monitoring on the field cohort.

##### Corrective action.

Fix the process or design as owned; do not only rewrite the qual report.

##### Qualification / ATP / telemetry update.

Add the stress or observable that would have caught it; widen sample strategy; add the cheapest production control that separates the signature (Appendix C.13).

##### Fleet prevention.

Keep cohort burn-down and a decision owner until rates fall; feed §7.1.13.

##### Score yourself.

Fail if your only sentence was "qualification was insufficient" without a miss class and a control update.

##### Executive summary.

Problem: field fails after passed qual. Impact: (rate / cohort). Evidence: (miss class + FA). Confidence: state confirmation level. Containment: lot/site hold. Next decision: updated qual proxy and ATP/SPC owner.

##### Deep dive.

Appendix D.3, §8.2, §10.13, Appendix C.13, §8.1. )


<div class="nav-links">
  <a href="ch11-one-week-optical-systems-interview-review">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch13-thirty-second-interview-frameworks">Next &rarr;</a>
</div>
