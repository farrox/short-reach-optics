---
layout: default
title: "Ch 12: Thirty-second interview frameworks"
---

# Thirty-second interview frameworks

This appendix is the operating manual for answering under time pressure. The philosophy lives in §A. Here each topic is a reusable reasoning template: question, thirty-second close, decision tree, measurements, follow-ups, and mistakes. Memorize the green boxes. Expand only where the interviewer asks.

[]

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure (unit $\rightarrow$ lot $\rightarrow$ vendor $\rightarrow$ fleet). Apply the power-versus-quality fork: chase eye, bias, wavelength, noise, or receiver. Therefore I would isolate with a golden swap and a bias sweep, then decide contain, retune, or ATP change.

::: dectree
BER up, power stable \| Scope: unit / lot / vendor / fleet \| Power fork: power held -\> quality or Rx \| Golden swap Tx vs Rx \|-- Tx --\> eye / bias / wavelength / RIN \|-- Rx --\> TIA / sensitivity / EQ \| Decision -\> control (ATP / table / lot)
:::

[]

> **30-second answer (memorize).** Power moved, so stay on the power ledger. First scope the failure. Confirm with an external meter at a named plane, then bisect source enable, coupling, connectors, MUX loss, and monitor-PD / APC honesty. Therefore I would contain if lot-correlated, clean or replace the plant if local, and update ATP or hygiene rules so it does not recur.

::: dectree
Power down \| Scope \| External meter @ named plane \| Monitor vs external agree? \|-- NO --\> APC / monitor-PD / cal \|-- YES --\> source / coupling / connector / MUX \| Population? \|-- lot/vendor --\> contain + FA \|-- single --\> plant or unit repair \| Decision + control
:::

[]

> **30-second answer (memorize).** First scope: one lane, one unit, or a pattern across the lot? Compare sibling lanes, then optical-versus-electrical swap to split path from driver or TIA. Therefore I would fix assembly or the array element that owns the fault, and add the screen that would have caught it.

::: dectree
One weak lane \| Siblings OK? \|-- NO --\> shared supply / thermal / host \|-- YES --\> lane-local \| Opt vs elec swap \|-- optical --\> FAU / coupling / PIC lane \|-- electrical --\> driver / TIA / SerDes \| Lot pattern? \| Decision: rework / screen / supplier
:::

[]

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure and whether cool-down recovers. At the failing temperature, read eye, bias sweep, wavelength, and control headroom. Therefore I would fix the table or thermal design and put that loaded corner in the ATP.

::: dectree
Hot BER, power stable \| Scope + cool-down recovers? \|-- YES --\> operating point / table / control \|-- NO --\> aging / permanent damage \| At failing T: eye, bias sweep, OSA, TEC/heater codes \| Control ledger exhausted? \|-- YES --\> thermal design / tuning range \|-- NO --\> cal table / wavelength / Rx \| Decision: retune + ATP corner
:::

[]

> **30-second answer (memorize).** Aging changes the LIV. Drift changes the setpoint on a healthy LIV. External LIV plus recovery after recalibration separates them. Time behavior confirms: monotonic climb versus a step after a table or firmware change. Therefore I would route aging to life/derate/replace and drift to table control plus an ATP loaded-corner check.

::: dectree
Symptom (bias up / BER up) \| External LIV vs ship data \|-- LIV moved --\> aging --\> life / derate / replace \|-- LIV OK ----\> drift path \| Monitor vs external power \| Bias sweep / table reload recovers? \|-- YES --\> calibration / firmware \|-- NO --\> deeper FA
:::

[]

> **30-second answer (memorize).** Freeze the requirements slice, not the incumbent datasheet. Characterize distributions across lots and temperature from the customer view: OMA, RIN at ORL, wavelength, eye, and life with a named HTOL mechanism. Therefore I would gate open volume on FAIR, ATP correlation, and split RMA codes, not on a hero sample.

::: dectree
Second source \| Freeze requirements (customer-visible) \| Distributions vs means (lots, T) \| HTOL + named mechanism \| ATP correlation + FAIR \| Fleet codes split by supplier \| Decision: qualify / hold / reject
:::

[]

> **30-second answer (memorize).** Validation is staged uncertainty reduction. Walk bring-up, characterization, margin, interop, environment, reliability, production, and fleet. Each stage answers a question the previous could not. Therefore I would refuse any test that answers no new question and watch the ledgers margin budgeting says will be spent first.

::: dectree
New transceiver \| Bring-up -\> Characterization -\> Margin \| Interop -\> Environment -\> Reliability \| ATP / manufacturing -\> Pilot -\> Fleet \| Each stage: question? uncertainty? decision?
:::

[]

> **30-second answer (memorize).** First scope: unit, lot, vendor, rack, datacenter, or fleet? Ask trend and change history. Classify performance versus reliability versus manufacturability before pulling hardware. Therefore I would contain if growing and supplier-specific, or monitor-only if tiny, flat, and no customer impact, with an owner on the next control.

::: dectree
Fleet symptom \| Scope ladder \| Rate / trend / customer impact \|-- tiny, flat, no impact --\> monitor only \|-- growing / supplier --\> contain now \| Bucket: performance / reliability / manufacturability \| Decision + owner + telemetry control
:::

[]

> **30-second answer (memorize).** Evidence beats an unknown mechanism. Stop shipment of Supplier B affected lots, continue Supplier A, expand the ATP hot-corner screen, open FA with DPA on fails, and watch RMA daily. Therefore I would contain today and keep the FA path open rather than wait for SEM before acting.

::: dectree
Escape signal \| Scope: supplier / lot / corner / rate \| Mechanism known? \|-- NO --\> still decide \| Contain B + continue A \| ATP screen + FA/DPA + telemetry \| Close when mechanism + control proven
:::

[]

> **30-second answer (memorize).** A floor means multiplicative noise: SNR stops improving as power rises. Prioritize RIN under ORL, MPI from reflections, weak PSRR, and crosstalk. Therefore I would confirm floor versus shift on a waterfall, then remove the noise source rather than raise OMA.

::: dectree
BER vs power \| Shape? \|-- parallel shift --\> sensitivity \|-- floor ---------\> multiplicative noise \| ORL / RIN / MPI / PSRR / crosstalk \| Fix noise source, not launch
:::

[]

> **30-second answer (memorize).** Preserve the failing state and telemetry before you reseat, clean, or reboot. Scope time and change: dwell, temperature, vibration, firmware, connector. Prefer burst/FEC histograms and long dwell over a single golden retest. Therefore I would contain if lot-correlated, tighten dwell/ATP if escape, and refuse to close an NFF without a reproduction plan.

::: dectree
Intermittent \| Preserve state / telemetry \| Triggers: T, time, mate, vibration, FW \| Reproduce with dwell / stress \| Scope population \| Decision: contain / ATP dwell / monitor
:::

[]

> **30-second answer (memorize).** Name the escape path and the measurement that would have caught it at a named plane and corner. Size the new limit from characterization and repeatability, correlate stations, and set a reaction plan. Therefore I would ship the ATP change with an owner and a metric, not a hope that operators will be careful.

::: dectree
Escape \| Which uncertainty ATP missed? \| New measurement / corner / limit \| Guard band from repeatability \| Station correlation \| Reaction plan + owner \| Ship ATP change
:::

[]

> **30-second answer (memorize).** Log what discriminates hypotheses: per-lane power, bias, pre-FEC BER and FEC histograms; module temperature and actuator drive; LOS/LOL and firmware with context. Alarm on trends and disagreements, not only hard thresholds. Therefore I would instrument the ledgers margin testing said die first.

::: dectree
Telemetry purpose: early margin erosion \| Per-lane: power, bias, pre-FEC BER \| Module: T, TEC/heater, rails, lock \| Events + lot/age/rack context \| Alarms: trends / disagreements
:::

[]

> **30-second answer (memorize).** Start from customer-visible requirements and a margin budget: which stresses will spend which ledgers. Map stresses to mechanisms, run HTOL only with a named activation energy, and prove ATP can catch escapes at rate. Therefore I would gate ship on remaining margin after environment, interop, and life, not on a checklist of rituals.

::: dectree
Qual plan \| Customer requirements + margin budget \| Stress -\> mechanism -\> ledger spent \| HTOL with named Ea \| ATP catches escapes? \| Ship gate = remaining margin OK
:::

[]

> **30-second answer (memorize).** State evidence, confidence weights, and residual risk. Decide with today's evidence: contain the scoped population, keep a healthy path shipping, open FA, and add the ATP or telemetry control that would catch the next escape. Therefore I would not wait for certainty before ownership actions.

::: dectree
Unknown mechanism \| Evidence + scope + rate/trend \| Priors: common modes first \| Decision today (contain / ship / derate) \| FA path + control + owner \| Update when mechanism closes
:::

**Key idea.** Open the matching framework, deliver the thirty-second box, walk the tree, end on the decision and the control. Philosophy is in §A; this appendix is how you speak it under pressure.


<div class="nav-links">
  <a href="ch11-one-week-optical-systems-interview-review">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch13-engineering-decision-trees">Next &rarr;</a>
</div>
