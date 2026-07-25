---
layout: default
title: "Ch 12: Thirty-second interview frameworks"
---

# Thirty-second interview frameworks

This appendix is the operating manual for answering under time pressure. The philosophy lives in §A. Here each topic is a reusable reasoning template: question, thirty-second close, decision tree, measurements, follow-ups, and mistakes. Memorize the green boxes. Expand only where the interviewer asks.

[]

::: dectree
BER up, power stable \| Scope: unit / lot / vendor / fleet \| Power fork: power held -\> quality or Rx \| Golden swap Tx vs Rx \|-- Tx --\> eye / bias / wavelength / RIN \|-- Rx --\> TIA / sensitivity / EQ \| Decision -\> control (ATP / table / lot)
:::

[]

::: dectree
Power down \| Scope \| External meter @ named plane \| Monitor vs external agree? \|-- NO --\> APC / monitor-PD / cal \|-- YES --\> source / coupling / connector / MUX \| Population? \|-- lot/vendor --\> contain + FA \|-- single --\> plant or unit repair \| Decision + control
:::

[]

::: dectree
One weak lane \| Siblings OK? \|-- NO --\> shared supply / thermal / host \|-- YES --\> lane-local \| Opt vs elec swap \|-- optical --\> FAU / coupling / PIC lane \|-- electrical --\> driver / TIA / SerDes \| Lot pattern? \| Decision: rework / screen / supplier
:::

[]

::: dectree
Hot BER, power stable \| Scope + cool-down recovers? \|-- YES --\> operating point / table / control \|-- NO --\> aging / permanent damage \| At failing T: eye, bias sweep, OSA, TEC/heater codes \| Control ledger exhausted? \|-- YES --\> thermal design / tuning range \|-- NO --\> cal table / wavelength / Rx \| Decision: retune + ATP corner
:::

[]

::: dectree
Symptom (bias up / BER up) \| External LIV vs ship data \|-- LIV moved --\> aging --\> life / derate / replace \|-- LIV OK ----\> drift path \| Monitor vs external power \| Bias sweep / table reload recovers? \|-- YES --\> calibration / firmware \|-- NO --\> deeper FA
:::

[]

::: dectree
Second source \| Freeze requirements (customer-visible) \| Distributions vs means (lots, T) \| HTOL + named mechanism \| ATP correlation + FAIR \| Fleet codes split by supplier \| Decision: qualify / hold / reject
:::

[]

::: dectree
New transceiver \| Bring-up -\> Characterization -\> Margin \| Interop -\> Environment -\> Reliability \| ATP / manufacturing -\> Pilot -\> Fleet \| Each stage: question? uncertainty? decision?
:::

[]

::: dectree
Fleet symptom \| Scope ladder \| Rate / trend / customer impact \|-- tiny, flat, no impact --\> monitor only \|-- growing / supplier --\> contain now \| Bucket: performance / reliability / manufacturability \| Decision + owner + telemetry control
:::

[]

::: dectree
Escape signal \| Scope: supplier / lot / corner / rate \| Mechanism known? \|-- NO --\> still decide \| Contain B + continue A \| ATP screen + FA/DPA + telemetry \| Close when mechanism + control proven
:::

[]

::: dectree
BER vs power \| Shape? \|-- parallel shift --\> sensitivity \|-- floor ---------\> multiplicative noise \| ORL / RIN / MPI / PSRR / crosstalk \| Fix noise source, not launch
:::

[]

::: dectree
Intermittent \| Preserve state / telemetry \| Triggers: T, time, mate, vibration, FW \| Reproduce with dwell / stress \| Scope population \| Decision: contain / ATP dwell / monitor
:::

[]

::: dectree
Escape \| Which uncertainty ATP missed? \| New measurement / corner / limit \| Guard band from repeatability \| Station correlation \| Reaction plan + owner \| Ship ATP change
:::

[]

::: dectree
Telemetry purpose: early margin erosion \| Per-lane: power, bias, pre-FEC BER \| Module: T, TEC/heater, rails, lock \| Events + lot/age/rack context \| Alarms: trends / disagreements
:::

[]

::: dectree
Qual plan \| Customer requirements + margin budget \| Stress -\> mechanism -\> ledger spent \| HTOL with named Ea \| ATP catches escapes? \| Ship gate = remaining margin OK
:::

[]

::: dectree
Unknown mechanism \| Evidence + scope + rate/trend \| Priors: common modes first \| Decision today (contain / ship / derate) \| FA path + control + owner \| Update when mechanism closes
:::

**Key idea.** Open the matching framework, deliver the thirty-second box, walk the tree, end on the decision and the control. Philosophy is in §A; this appendix is how you speak it under pressure.


<div class="nav-links">
  <a href="ch11-one-week-optical-systems-interview-review">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch13-abbreviations">Next &rarr;</a>
</div>
