---
layout: default
title: "Appendix C: Engineering decision trees"
---

# Appendix C: Engineering decision trees

This appendix is the wall chart. It collects the universal reasoning frameworks used throughout the book, independent of any interview question. Open it when you need the pattern without the surrounding prose. Interview pressure maps are in Appendix B; the drill philosophy is in Appendix A.

Debugging and qualification are the same philosophy at different times. Debugging asks which margin was exhausted. Qualification asks how much margin remains after the expected stresses. Both end on an engineering decision and a recurrence control.

## Universal debugging tree

<pre class="dectree" aria-label="Problem"><code>Problem
  |
Scope (unit -&gt; lot -&gt; vendor -&gt; fleet)
  |
Population / time behavior
  |
Power changed?
  |-- YES --&gt; Power ledger --&gt; optical path
  |-- NO  --&gt; Quality / receiver
  |
Isolation (highest-value measurement)
  |
Root cause (surviving hypothesis)
  |
Decision (contain / retune / derate / RMA / monitor)
  |
Recurrence control (ATP / SPC / telemetry / FA)</code></pre>
Use when BER rises, a link flaps, a lane is weak, or a corner fails. Name the ledger before naming a component (§4.8, §7.11).

## Universal qualification tree

<pre class="dectree" aria-label="Requirements"><code>Requirements
  |
Bring-up
  |
Nominal characterization
  |
Margin characterization
  |
Interoperability
  |
Environmental and reliability qualification
  |
Manufacturing and ATP readiness
  |
Controlled pilot
  |
Fleet deployment and monitoring
  |
Ship / restrict / reject</code></pre>
Each gate removes a different uncertainty. Do not treat a bring-up pass as margin evidence, or an HTOL pass as production readiness. Shorter ladders in Table 7.1, Table 7.2 are grouped views of this same order (§7.1, Appendix A.6.5, §8.2).

## Power-versus-quality fork

<pre class="dectree" aria-label="BER or link degrade"><code>BER or link degrade
  |
Received power changed?
  |-- YES --&gt; Power ledger
  |           laser / coupling / connector / fiber / MUX / monitor
  |-- NO  --&gt; Signal quality
              eye / noise / jitter / bias / EQ / RIN / Rx
  |
Highest-value measurement
  |
Decision + recurrence control</code></pre>
One check before retuning equalizers or bias tables (§4.8, §7.11).

## Scope and population

<pre class="dectree" aria-label="Initial symptom"><code>Initial symptom
  |
Scope analysis (how large?)
  |-- unit / lane / rack / site / PN / vendor / lot / fleet
  |
Technical isolation
  |
Correlation analysis (which cohort?)
  |-- lot / date code / FW / cal / platform / location
  |
Containment and corrective action</code></pre>
Scope sets severity and priors. Correlation after isolation unlocks contain, pause, replace, or supplier escalate (§7.12, §8.6).

## Sudden versus gradual

<pre class="dectree" aria-label="Failure onset"><code>Failure onset
  |
Sudden?
  |-- config / handling / firmware / mechanical / power event
  |
Gradual?
  |-- aging / drift / margin erosion / contamination / cal movement
  |
Prioritize measurements (priors, not conclusions)</code></pre>
Sudden and gradual are priors that reorder the bench, not root-cause claims (Chapter 10).

## Transmitter, channel, or receiver

<pre class="dectree" aria-label="Power or quality path chosen"><code>Power or quality path chosen
  |
Golden swap / loopback
  |-- Tx --&gt; eye / LIV / bias / wavelength / RIN
  |-- Channel --&gt; connector / fiber / MUX / ORL
  |-- Rx --&gt; sensitivity / TIA / EQ / host
  |
Evidence
  |
Owner + decision</code></pre>
Bisect domains before opening packages (§7.10, §10.2).

## Supplier qualification

<pre class="dectree" aria-label="Requirements (customer-visible)"><code>Requirements (customer-visible)
  |
Characterization (distributions, not samples)
  |
Margin under stress
  |
Qualification (named mechanisms)
  |
Production readiness (FAIR, ATP, SPC)
  |
Fleet monitoring (RMA, telemetry)</code></pre>
Customer view measures external behavior. Vendor view owns internals (Appendix A.6.7, §8.10).

## Supplier escape and containment

<pre class="dectree" aria-label="Escape detected"><code>Escape detected
  |
Contain scoped population
  |
Scope (unit / lot / vendor / site)
  |
Evidence (plane, corner, telemetry)
  |
Root cause class
  |
Supplier / FA path
  |
ATP or screen update
  |
SPC / reaction plan
  |
Fleet monitoring</code></pre>
Contain first when the population can grow. The system owner keeps responsibility for evidence quality and verifying corrective action (§8.7, §7.12).

## Margin-budget flow

<pre class="dectree" aria-label="Nominal system margin"><code>Nominal system margin
  |
Temperature debit
  |
Voltage / power-quality debit
  |
Channel / connector debit
  |
Manufacturing variation
  |
Aging / wear
  |
Interoperability variation
  |
Remaining margin
  |
Above deployment requirement?
  |-- YES --&gt; proceed
  |-- NO  --&gt; redesign / restrict / recalibrate / reject</code></pre>
Design allocates budgets. Validation often measures the net externally visible result. Do not double-count internal penalties the test cannot separate (§5.19, §7.7).

## Black-box versus engineering access

<pre class="dectree" aria-label="Bookended product"><code>Bookended product
  |
End-to-end qualification
  |-- BER / FEC / telemetry / sensitivity
  |-- environment / interoperability
  |
Enough confidence to decide?
  |-- YES --&gt; deployment decision
  |-- NO  --&gt; request engineering access
              Tx-only / Rx-only / breakout / diagnostics
              |
              Isolate margin</code></pre>
An optical eye is measured externally with suitable access. Do not assume the module reports a conventional eye unless that capability exists (Appendix A.6.7).

## Recurrence-control loop

<pre class="dectree" aria-label="Production escape"><code>Production escape
  |
Contain risk now
  |
Investigate mechanism
  |
Correct process
  |
Update screening or ATP
  |
Verify next lot
  |
Monitor fleet</code></pre>
Containment, root cause, and prevention are three different actions (§8.7).

## Production feedback loop

<pre class="dectree" aria-label="Design requirements"><code>Design requirements
  |
Qualification
  |
ATP
  |
Production data
  |
Fleet data
  |
Failure analysis
  |
Updated limits or screens
  |
Next production cycle</code></pre>
Production validation is replayable and decision-oriented (§8.10, §8.9).

## Measurement-selection loop

<pre class="dectree" aria-label="Current evidence"><code>Current evidence
  |
Rank hypotheses
  |
Choose measurement that removes
the largest number of hypotheses
  |
Update beliefs
  |
Enough evidence to decide?
  |-- NO  --&gt; next measurement
  |-- YES --&gt; take action</code></pre>
**Key idea.** Great engineers perform the minimum measurement that eliminates the largest number of hypotheses.

## Unknown failure

<pre class="dectree" aria-label="Observation (facts, not hopes)"><code>Observation (facts, not hopes)
  |
Hypotheses (short ranked list)
  |
Highest-value measurement
  |
Evidence (what died)
  |
Decision with today's confidence
  |
Continue measuring?
  |-- YES --&gt; next measurement
  |-- NO  --&gt; control + owner + residual risk</code></pre>
Unknown mechanism is not a freeze. Decide with weighted evidence (Appendix A.4, Appendix C.13).

## Before you start: three checklists

> **Before debugging**
>
> Scope $\cdot$ unit/rack/lot/vendor/fleet $\cdot$ sudden or gradual $\cdot$ power changed? $\cdot$ signal-quality uncertainty $\cdot$ highest-value measurement $\cdot$ decision unlocked $\cdot$ containment now $\cdot$ recurrence control.

> **Before qualification**
>
> Nominal function $\cdot$ operating margin $\cdot$ environmental stresses $\cdot$ interoperability $\cdot$ aging/reliability $\cdot$ manufacturing variation $\cdot$ ATP escape detection $\cdot$ controlled pilot $\cdot$ fleet telemetry.

> **Before production**
>
> Requirements met $\cdot$ margin demonstrated $\cdot$ environment covered $\cdot$ interop verified $\cdot$ reliability risk addressed $\cdot$ lot variation characterized $\cdot$ ATP defined $\cdot$ supplier controls reviewed $\cdot$ pilot exit criteria $\cdot$ fleet monitoring ready.

**Key idea.** These trees are the book's reusable method. Chapters supply the physics and the numbers. This appendix supplies the order of thought.


<div class="nav-links">
  <a href="ch12-thirty-second-interview-frameworks">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch14-abbreviations-and-terminology">Next &rarr;</a>
</div>
