---
layout: default
title: "Ch 10: Failure Analysis: From Symptom to Confirmed Mechanism"
---

# 10 Failure Analysis: From Symptom to Confirmed Mechanism

Operational monitoring detects and bounds the anomaly: FEC activity, retrains, cohorts, severity, and initial containment (Chapter 9, Appendix H). This chapter begins when the issue becomes an investigation that must confirm mechanism and ownership. Earlier chapters own the underlying physics (Chapter 6, Chapter 7, Chapter 8). Symptom recipes and the fleet-bucket map live in Appendix I.

The only general incident sequence is:

> Preserve $\rightarrow$ scope and contain $\rightarrow$ classify the symptom and timing $\rightarrow$ locate the first-moving margin $\rightarrow$ falsify leading hypotheses $\rightarrow$ confirm mechanism and ownership $\rightarrow$ correct $\rightarrow$ prevent recurrence $\rightarrow$ verify effectiveness.

<pre class="dectree" aria-label="Preserve"><code>Preserve
  |
Scope
  |
Classify
  |
Locate margin
  |
Falsify
  |
Confirm
  |
Correct
  |
Prevent</code></pre>
Order matters. Preserve first because reseat, reboot, and clean destroy state. Scope next so containment width matches the population. Classify and locate margin before falsify so you pick the cheap separating test. Confirm before correct so you do not ship a story. Prevent and verify last so the factory and fleet catch the next escape.

The debugging pyramid (§1.16), power-versus-signal fork (§6.8, Appendix I.13), fleet map (Table I.1), and wall-chart trees (Appendix D) are the same method at different scales. They are aids, not competing spines.

## What failure analysis must produce

Every FA result should land in a named bucket before the case closes:

Design or architecture issue

: Fix architecture or derate.

Manufacturing or process issue

: Fix manufacturing or assembly.

Supplier issue

: Fix incoming quality or supplier process.

Test or monitoring escape

: Improve detection (ATP, sample, SPC, telemetry).

System or integration issue

: Fix host, plant, topology, or deployment interaction.

Software or control issue

: Fix firmware, calibration, or control-loop behavior.

No confirmed mechanism

: Investigation remains open. Keep an owner, containment, next experiment, and review date. Do not treat unknown mechanism as a completed root cause.

 The checklist in Table 10.1 is a lifecycle, not a suggestion list. Each step removes a class of uncertainty before the next step spends lab time.

<table class="book-table"><tr><th>Step</th><th>Question</th><th>Required record</th></tr><tr><td>Preserve</td><td>What evidence will a reseat, reboot, clean, or retest destroy?</td><td>CMIS, BER and FEC history, rails, temperature, firmware, fixture, and time</td></tr><tr><td>Scope</td><td>One unit, lane, lot, vendor, site, or fleet?</td><td>Population and correlation plot</td></tr><tr><td>Classify</td><td>Sudden or gradual, constant or intermittent, thermal or cumulative?</td><td>Timeline and recovery test</td></tr><tr><td>Locate margin</td><td>Did power, noise, timing, spectrum, or control move first?</td><td>Golden comparison and margin ledger</td></tr><tr><td>Falsify</td><td>Which measurement best separates the leading hypotheses?</td><td>Expected result for each hypothesis before the test</td></tr><tr><td>Confirm</td><td>Does the fault follow the suspected block under swap, stress, or physical evidence?</td><td>Ownership boundary and confirmation status</td></tr><tr><td>Correct</td><td>What repairs the current failure?</td><td>Action taken and restored margin</td></tr><tr><td>Prevent</td><td>Where will production or fleet monitoring catch recurrence earliest?</td><td>Named control and effectiveness check</td></tr></table>
**Table 10.1.** Failure-analysis checklist. Fill these fields as you walk the sequence.

### Evidence states

> **Evidence states**\
>
> Observation
>
> : A symptom or correlation was recorded.
>
> Hypothesis
>
> : A mechanism could explain the observation.
>
> Supported hypothesis
>
> : Several observations are consistent with it.
>
> Isolated owner
>
> : Controlled comparison localizes the responsible block.
>
> Reproduced mechanism
>
> : The symptom is recreated by the proposed cause.
>
> Physically confirmed
>
> : Direct physical or electrical evidence supports the mechanism.
>
> Closed action
>
> : Recurrence control is deployed and shown effective.
>
> A surviving hypothesis and a localized block are not automatically a confirmed mechanism. Do not say "data proves" for the last surviving hypothesis alone.

## Preserve the failing state

Preserve the failing state before reseat, reboot, clean, or power cycle. Those actions often destroy the only evidence that separates contact, firmware, and true wear (Appendix D.16).

Capture at least:

- telemetry snapshot (power, temperature, rails, alarms, control demand);

- logs and counters (pre-FEC or corrected-error activity, uncorrectables, retrains, loss of lock, recovery duration);

- environmental and workload state;

- firmware, configuration, and host or peer identity;

- optical plant (fiber path, connectors, ports);

- genealogy (serial, lot, site, date code, installation age);

- photos before cleaning or disassembly when contamination is plausible;

- chain of custody for units held for FA.

> **Why experienced engineers preserve state before reseating?**
>
> Because reseat, reboot, and clean often destroy the only evidence that separates contact, firmware, and true wear. Scope without a snapshot is theater.

## Scope and contain

Name the population: unit, lane, host, lot, supplier, site, firmware, or fleet cohort. Use affected and unaffected denominators. Contain when the population can grow. A perfect mechanism story does not unship yesterday's lot.

Containment should match the evidence. Drain one link, hold a lot, pause one revision, or increase telemetry while the mechanism remains open. Do not wait for perfect certainty when exposure can continue growing, and do not stop an unrelated fleet without evidence (Appendix H.24, Chapter 9).

## Classify the symptom and failure clock

Use three axes before instruments:

Time behavior

: Sudden, gradual, or intermittent.

Extent

: Local (one lane or path) versus shared (host, plant, lot, site).

First-moving ledger

: Power, noise, timing, spectrum, thermal, or control.

Classify before you open a deep measurement campaign. The first-moving margin often selects the discriminating experiment (§7.19, Appendix I.13).

## Build and rank hypotheses

One symptom can have many mechanisms. Rank hypotheses by mechanism plausibility, existing evidence, severity, and testability. Distinguish correlation from causation. For each leading hypothesis, write what result would weaken it before you run the next test.

> **Engineering heuristic.** If two explanations fit equally well, prefer the one that requires the fewest independent failures.

## Select the next discriminating experiment

Choose one measurement that can kill or promote the leading hypotheses at the access you have (black-box versus engineering; Appendix A.2, Appendix D.11). Prefer information per cost:

1.  existing telemetry and preserved counters;

2.  named-plane optical or electrical measurements;

3.  reversible swaps (module, fiber, host port, peer);

4.  controlled stresses (thermal, ORL, traffic, power);

5.  engineering-access measurements;

6.  destructive analysis last (Appendix I).

> **Engineering heuristic.** Never spend an hour on a DCA or spectrum sweep when a five-minute golden swap or attenuator step can eliminate half the tree.

## Confirm mechanism and ownership

Call a mechanism confirmed only with one or more of:

- repeatable reproduction under the named condition;

- fault follows a controlled swap;

- physical evidence;

- mechanism-specific stress response;

- independent evidence consistency.

A swap localizes ownership. It may not prove the microscopic mechanism. Do not treat the last surviving hypothesis as proof (§10.1.1).

## Correct, prevent, and verify

##### Correction versus recurrence control.

A corrective action repairs the current mechanism. A recurrence control prevents or detects the next occurrence. Cleaning a connector is a correction; inspect-before-connect is a recurrence control. Repairing a station fixture is a correction; a golden-unit drift alarm is a recurrence control. Recalibrating wavelength is a correction; a control-headroom telemetry alarm is a recurrence control.

Do not choose the corrective action until the mechanism and ownership boundary are sufficiently supported. If confirmed, possible controls include design change, supplier process, incoming inspection, ATP, sample audit, SPC, telemetry, service procedure, or qualification (Appendix D.3, §9.9.11).

##### Recurrence-control closure.

An incident is not closed when the unit recovers. Close only when a production or fleet control catches the same signature next time. Verify effectiveness with at least one of: fresh production lots; controlled reproduction no longer fails; fleet cohort rate returns to baseline; monitoring detects the signature; no unacceptable side effects.

## Three compact examples

These examples show method, not device tutorials. Full recipes: Appendix I.

### Low optical power: source versus path versus monitor

Preserve counters and DDM. Scope lane versus module versus host. Compare launch power, path loss, and monitor reading at named planes. Ask whether the source degraded, the path attenuated, or the monitor lied. Use attenuator steps and reversible fiber or module swaps before laser FA. Detail: Appendix I.1.

### BER degradation: waterfall shift versus floor versus bursts

Name the receive plane. Stable average power makes gross loss less likely but does not clear the optical path. Classify waterfall shift, elevated floor, or burst-dominated behavior before invoking RIN, MPI, or equalization stories (Chapter 6, Appendix I.2, Appendix I.2.1). A floor is a diagnostic pattern, not one mechanism.

### Intermittent retrains

Operational detection and cohort bounding belong to Chapter 9. For mechanism confirmation: preserve state before reseat; compare affected and unaffected cohorts; run reversible module, fiber, and host-port swaps; correlate thermal, ORL, and supply events; hand destructive confirmation to the reference routes when needed (Appendix I.8, Appendix H.27).

## Fleet handoff and reference routes

Lab debug asks what is broken on this unit. Fleet triage asks which bucket owns the fix. After operational detection in Chapter 9, use the fleet map in Table I.1, Appendix I.14 to assign performance, reliability, manufacturability, plant, or host ownership. Contain the population and clear the measurement system before opening supplier FA.

For yield drops: clear the measurement system, contain affected WIP, stratify by genealogy, and identify the first process step where good and bad populations diverge. Full MSA, capability, ATP, and SPC methodology live in Chapter 9; the FA yield recipe is in Appendix I.10.

Excursion procedure (8D/CAPA/DPA): Appendix I.14.2. Symptom encyclopedia: Appendix I.

## Interview takeaway

**Key idea.** Staff-level failure analysis starts with a symptom and ends with a new control. I preserve the failing state, scope the population, classify timing and the first-moving margin, and choose one measurement that can falsify the leading hypothesis. I confirm mechanism and ownership before I prescribe a fix, and I close only when a recurrence control is deployed and shown effective.

Junior mistake: reseat first, or close without a recurrence control (§10.2, §10.8, Appendix I).

### Interview Q&A: Failure Analysis

Practice speaking these answers aloud. Prefer first-person incident reasoning. Detail lives in §10.1, §10.1.1, Appendix I, Chapter 9.

##### Question 1. Walk me through your failure-analysis process.

*Tests:* complete incident structure and disciplined ordering.

*Spoken answer.* "I preserve the failing state first, then scope the population and contain if exposure can grow. I classify sudden versus gradual versus intermittent behavior and which margin ledger moved first. I pick the lowest-cost measurement that separates the leading hypotheses. I confirm mechanism and ownership with reproduction, a controlled swap, or physical evidence. I close only when a recurrence control is in place and shown effective" (§10.1).

*Pressure follow-up.* "Which step do engineers most commonly skip?"\
*Answer pivot.* "Preserve and scope. Teams reseat, lose the evidence, and then try to recreate a failure they already had."

*Trap:* "I find the bad part, replace it, and retest."

##### Question 2. What evidence do you preserve before reseating, rebooting, cleaning, or power cycling?

*Tests:* evidence preservation and incident metadata.

*Spoken answer.* "I capture volatile state before changing the system: identity and genealogy, CMIS and alarms, optical power, FEC and retrain history, temperature and rails, firmware, host and peer, plant path, and chronology. If contamination is plausible, I photograph the endface before cleaning. The goal is to separate contact, software, thermal, optical, and wear later" (§10.2).

*Pressure follow-up.* "Ops already reseated and it recovered."\
*Answer pivot.* "Recovery is evidence, not closure. I preserve what remains, name what changed, and reproduce under controlled conditions."

*Trap:* "Reseat first to see if the module is bad."

##### Question 3. How do you scope a failure and decide containment?

*Tests:* population reasoning, exposure, and reversible action.

*Spoken answer.* "I ask whether the symptom is one lane, module, host, fiber, lot, site, firmware, or a broader cohort. I compare affected and unaffected denominators. Containment matches that width: drain a link, hold a lot, or raise telemetry. I do not wait for perfect certainty when the population can grow" (§10.3, Appendix H.24).

*Pressure follow-up.* "It correlates with one date code. Stop the lot?"\
*Answer pivot.* "I may provisionally contain that cohort while checking confounding with site, host, firmware, or station. Correlation guides width; it does not confirm mechanism."

*Trap:* "Contain only failed units until root cause is proven."

##### Question 4. BER is rising, but average received power is stable. What do you do next?

*Tests:* power versus signal quality and BER-waterfall reasoning.

*Spoken answer.* "Stable average power makes gross loss less likely, but it does not clear the path. I name the receive plane, classify waterfall shift versus floor versus bursts, then pick a falsifying measurement. I do not jump to RIN or equalizer stories from the average alone" (Appendix I.13, Appendix I.2, Chapter 6).

*Pressure follow-up.* "Is it RIN?"\
*Answer pivot.* "RIN is one floor hypothesis. I need a measurement that can weaken MPI, reflection, unlock, and host impairment too."

*Trap:* "Stable power means the optics are fine."

##### Question 5. One lane is weak while the sibling lanes are healthy. How do you proceed?

*Tests:* local versus shared ownership.

*Spoken answer.* "Sibling health makes shared host power or plant less likely, but I still preserve state and check whether the weak lane follows the module, fiber, or host port under reversible swaps. Then I ask whether the first-moving ledger was power, spectrum, or noise" (Appendix I.4).

*Pressure follow-up.* "A module swap fixed it. Root cause?"\
*Answer pivot.* "Ownership points at the module or module--path. That is not yet a microscopic mechanism."

*Trap:* "Sibling lanes healthy means replace the weak laser."

##### Question 6. The link fails intermittently and recovers after reseating or cleaning. What now?

*Tests:* preserve-before-disturb and contact versus wear.

*Spoken answer.* "I treat reseat recovery as a clue, not a diagnosis. If state was destroyed, I document what changed, inspect endfaces, check ORL, and reproduce with controlled mate cycles before claiming wear-out. Operational retrain counting belongs to productization and operations reference; mechanism confirmation belongs here" (Appendix I.8, Chapter 9).

*Pressure follow-up.* "Cleaning fixed it. Close the ticket?"\
*Answer pivot.* "Cleaning is a correction. Closure needs inspect-before-connect or another recurrence control and effectiveness evidence."

*Trap:* "Intermittent plus reseat recovery means bad module."

##### Question 7. A module fails only at high temperature. How do you separate thermal margin from aging?

*Tests:* thermal classification and aging router.

*Spoken answer.* "I preserve thermal and control telemetry, check whether the failure recovers cool, and separate reversible thermal margin from cumulative aging. I use the aging-versus-thermal router rather than assuming wear-out from temperature alone" (Appendix I.12, Appendix I.11).

*Pressure follow-up.* "Ship LIV looks fine. Still aging?"\
*Answer pivot.* "Ship LIV alone does not clear thermal lock, bias tables, or receiver noise rise under load."

*Trap:* "High-temperature fail means Arrhenius wear-out."

##### Question 8. How do you investigate wavelength drift or loss of lock?

*Tests:* spectrum versus control ownership.

*Spoken answer.* "I preserve wavelength, lock error, and control demand, then ask whether the source moved, the filter or ring moved, or the control loop lost headroom. I falsify with named-plane spectrum and thermal steps before redesigning the locker" (Appendix I.5, Chapter 8).

*Pressure follow-up.* "TEC current is high. Replace the laser?"\
*Answer pivot.* "High control demand supports a thermal or lock hypothesis. I still confirm ownership before disposition."

*Trap:* "Any unlock is a bad laser."

##### Question 9. A module passed ATP but begins failing after 90 days, and field FIT looks high. How do you respond?

*Tests:* escape classification and control gap.

*Spoken answer.* "I preserve field evidence, scope the cohort, and ask whether this is wear-out, an infant escape, plant practice, or a detection gap. Component FIT is not fleet availability. I confirm mechanism before changing life models or ATP" (Appendix H.25.1, §10.1).

*Pressure follow-up.* "Tighten ATP immediately?"\
*Answer pivot.* "Only if the confirmed escape has a practical detection signature. Otherwise I may burn capacity without catching the mechanism."

*Trap:* "Field fail after ATP means ATP was worthless."

##### Question 10. Yield drops suddenly, or two production stations disagree. What is your FA approach?

*Tests:* measurement-first manufacturing investigation.

*Spoken answer.* "I clear the measurement system first, contain affected WIP, stratify by genealogy and station, and find the first step where good and bad populations diverge. Full MSA, capability, and SPC live in manufacturing validation; FA does not recreate that chapter" (Chapter 9, Appendix I.10).

*Pressure follow-up.* "Open supplier CAPA now?"\
*Answer pivot.* "Not until station correlation and golden units clear the tester."

*Trap:* "Yield drop means supplier material is bad."

##### Question 11. The supplier returns "no fault found." How do you respond?

*Tests:* NFF handling and evidence package.

*Spoken answer.* "NFF is a triage result, not a clean bill of health. I check whether we sent sufficient failing-state evidence, whether the supplier tested the same condition, and whether the fault is intermittent or host-plant dependent. I may need better reproduction, a joint debug, or a different bucket" (Appendix I.14, Appendix I.14.2).

*Pressure follow-up.* "Close as NFF and move on?"\
*Answer pivot.* "Track NFF rate. Rising NFF with clean LIV often points at install practice or intermittents, not Arrhenius."

*Trap:* "Supplier NFF means the module was never bad."

##### Question 12. Give me a 60-second failure-analysis plan for an optical incident.

*Tests:* end-to-end method under time pressure.

*Spoken answer.* "Preserve state. Scope and contain. Classify timing and the first-moving margin. Pick one falsifying experiment. Confirm ownership before corrective action. Close only with a recurrence control and an effectiveness check. Use the operations reference for operational detection and the FA reference for symptom recipes" (Chapter 9, Appendix I).

*Pressure follow-up.* "Where do you start if collectives slow after a rack expansion?"\
*Answer pivot.* "Operational cohort and retrain evidence first, then preserve failing links and run reversible swaps before destructive FA."

*Trap:* "Start by redesigning the product."


<div class="nav-links">
  <a href="ch9-productization-from-requirements-to-controlled-ramp">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-one-week-optical-systems-interview-review">Next &rarr;</a>
</div>
