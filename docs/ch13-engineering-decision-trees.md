---
layout: default
title: "Ch 13: Engineering decision trees"
---

# Engineering decision trees

This appendix is the wall chart. It collects the universal reasoning frameworks used throughout the book, independent of any interview question. Open it when you need the pattern without the surrounding prose. Interview pressure maps are in §B; the drill philosophy is in §A.

Debugging and qualification are the same philosophy at different times. Debugging asks which margin was exhausted. Qualification asks how much margin remains after the expected stresses. Both end on an engineering decision and a recurrence control.

## Debugging

::: dectree
Problem \| Scope (unit -\> lot -\> vendor -\> fleet) \| Population / time behavior \| Power changed? \|-- YES --\> Power ledger --\> optical path \|-- NO --\> Quality / receiver \| Isolation (highest-value measurement) \| Root cause (surviving hypothesis) \| Decision (contain / retune / derate / RMA / monitor) \| Recurrence control (ATP / SPC / telemetry / FA)
:::

Use when BER rises, a link flaps, a lane is weak, or a corner fails. Name the ledger before naming a component (§4.8, §7.11).

## Qualification

::: dectree
New product \| Works? (bring-up) \| Margins? (characterization) \| Environment / loaded corners? \| Interoperability? \| Reliability? (mechanism + Ea) \| Manufacturing / ATP? \| Pilot \| Production \| Fleet monitoring
:::

Each gate removes a different uncertainty. Do not treat a bring-up pass as margin evidence, or an HTOL pass as production readiness (§7.1, §8.2).

## Supplier qualification

::: dectree
Requirements (customer-visible) \| Characterization (distributions, not samples) \| Margin under stress \| Qualification (named mechanisms) \| Production readiness (FAIR, ATP, SPC) \| Fleet monitoring (RMA, telemetry)
:::

Customer view measures external behavior. Vendor view owns internals. Keep the view explicit so second-source answers stay on BER, sensitivity, FEC, telemetry, and corners unless engineering samples open the box (§A.6.7, §8.10).

## Production escape

::: dectree
Escape detected \| Contain scoped population \| Scope (unit / lot / vendor / site) \| Evidence (plane, corner, telemetry) \| Root cause class \| Supplier / FA path \| ATP or screen update \| SPC / reaction plan \| Fleet monitoring
:::

Contain first when the population can grow. Mechanism can follow. Ownership language: stop ship, notify supplier, request FA, update ATP, monitor RMA (§8.7, §7.12).

## Unknown failure

::: dectree
Observation (facts, not hopes) \| Hypotheses (short ranked list) \| Highest-value measurement \| Evidence (what died) \| Decision with today's confidence \| Continue measuring? \|-- YES --\> next measurement \|-- NO --\> control + owner + residual risk
:::

Unknown mechanism is not a freeze. Decide with weighted evidence, keep a healthy path shipping when possible, and name the control that would catch the next escape (§A.4).

## Margin budgeting

::: dectree
Allocated margin \| Stresses spend ledgers \|-- temperature / voltage / ripple \|-- contamination / IL / connector wear \|-- vibration / aging / process variation \| Remaining margin after stress \| Still acceptable? \|-- YES --\> ship / continue \|-- NO --\> redesign / derate / tighten ATP
:::

Qualification exists to verify remaining margin, not merely functionality. Debugging is what you do when remaining margin hits zero (§A.6.6, §5.19).

## Before you start: three checklists

> **Before debugging**
>
> Scope $\cdot$ time behavior $\cdot$ population $\cdot$ power or quality $\cdot$ highest-value measurement $\cdot$ decision $\cdot$ recurrence control.

> **Before qualification**
>
> Functional $\cdot$ margin $\cdot$ environment $\cdot$ interoperability $\cdot$ reliability $\cdot$ manufacturing $\cdot$ fleet feedback.

> **Before production**
>
> ATP $\cdot$ SPC $\cdot$ telemetry $\cdot$ supplier gates $\cdot$ monitoring owners $\cdot$ RMA-to-ATP feedback.

**Key idea.** These trees are the book's reusable method. Chapters supply the physics and the numbers. This appendix supplies the order of thought.


<div class="nav-links">
  <a href="ch12-thirty-second-interview-frameworks">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch14-abbreviations">Next &rarr;</a>
</div>
