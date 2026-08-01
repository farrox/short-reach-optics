---
layout: default
title: "Appendix C: Engineering decision trees"
---

# Appendix C: Engineering decision trees

This appendix is the wall chart. It collects the universal reasoning frameworks used throughout the book, independent of any interview question. Open it when you need the pattern without the surrounding prose. Interview pressure maps are in Appendix C; the drill philosophy is in Appendix A.

Debugging and qualification are the same philosophy at different times. Debugging asks which margin was exhausted. Qualification asks how much margin remains after the expected stresses. Both end on an engineering decision and a recurrence control.

## Universal debugging decision tree

<pre class="dectree" aria-label="Universal debugging decision tree"><code>Universal debugging decision tree
  |
Problem
  |
Scope and time behavior
  |
Stable average received power?
  |-- NO  --&gt; Power ledger / optical path
  |-- YES --&gt; Signal-quality path
              Tx / channel / Rx / DSP
              noise / timing / spectral / control
  |
Highest-value isolate
  |
Leading mechanism
  |
Controlled confirmation
  |
Decision + owner + timeline + reversibility
  |
Follow-up control (ATP / SPC / telemetry / supplier)</code></pre>
Stable average power deprioritizes gross optical loss but does not eliminate fast power fluctuations, clipping, monitor averaging, or reflection-dependent effects. A surviving hypothesis is only the leading mechanism until confirmed by reproduction, controlled swap, stress dependence, rollback, or physical evidence (§6.8, Appendix I.13, Appendix D.16).

> **Why experienced engineers ask about scope before touching the lab?**
>
> Because scope eliminates enormous parts of the hypothesis space. Unit, lot, vendor, site, and fleet each point at different owners and different next measurements.

> **Engineering heuristic.** If two explanations fit equally well, prefer the one that requires the fewest independent failures.

## Optical product-readiness lifecycle wall chart (Steps 1--11)

<pre class="dectree" aria-label="Product-readiness lifecycle (same as tab:ladder)"><code>Product-readiness lifecycle (same as tab:ladder)
  |
Step 1: Define requirements
  |
Step 2: Review architecture
  |
Step 3: Bring up hardware
  |
Step 4: Characterize behavior
  |
Step 5: Verify requirements and validate system use
  |
Step 6: Qualify reliability
  |
Step 7: Validate manufacturing
  |
Step 8: Controlled pilot
  |
Step 9: Ramp mass production
  |
Step 10: Monitor the fleet
  |
Step 11: Feed learning / next revision</code></pre>
Same order as Table 11.2, not a second Staff loop. Do not treat a bring-up pass as margin evidence, or an HTOL pass as production readiness (§11.3, Appendix A.8.5, Appendix F.1.1).

*Legend.* Program phases: EVT, DVT, PVT, pilot, MP. Engineering disciplines: characterization, verification, system validation, reliability qualification, manufacturing validation, production control, fleet monitoring. Program phases group work. Engineering disciplines define the evidence (§11.4, Appendix F.18).

Step 6 (qualify reliability): mechanism $\rightarrow$ stress $\rightarrow$ observable $\rightarrow$ acceptance $\rightarrow$ confidence. See Chapter 11.

Step 7 (validate manufacturing): production reference $\rightarrow$ representative builds $\rightarrow$ trusted measurement $\rightarrow$ yield/ATP/SPC $\rightarrow$ ramp. See Chapter 11.

## Qualification evidence tree

<pre class="dectree" aria-label="Qualification evidence tree"><code>Qualification evidence tree
  |
Requirement
  |
Named failure mechanism
  |
Stress that accelerates that mechanism
  |
Representative sample and confidence
  |
Observable before and after stress
  |
Acceptance criterion
  |
Production proxy
  |
Ship / restrict / reject</code></pre>
Use inside the reliability gate of Appendix D.2. The lifecycle says *when*; this tree says *what evidence* is defensible (Appendix D.16, Appendix F.1.1).

> **Why experienced engineers insist on mechanism $\rightarrow$ stress $\rightarrow$ observable?**
>
> Because a stress without a named mechanism is theater, and an observable without an acceptance rule cannot support a ship decision.

## Power-versus-quality diagnostic fork

<pre class="dectree" aria-label="Power-versus-quality diagnostic fork"><code>Power-versus-quality diagnostic fork
  |
BER or link degrade
  |
Stable average received power?
  |-- NO  --&gt; Power ledger / optical path
  |           laser / coupling / connector / fiber / MUX / monitor
  |-- YES --&gt; Signal-quality path
              Tx / channel / Rx / DSP
              noise / timing / spectral / control
  |
Highest-value measurement
  |
Leading mechanism -&gt; controlled confirmation
  |
Decision + recurrence control</code></pre>
One check before retuning equalizers or bias tables (§6.8, Appendix D.1).

> **Engineering heuristic.** Name the power-versus-quality branch before you name a laser, TIA, or connector. Parts without a branch are guesses.

## Scope and population

<pre class="dectree" aria-label="Scope and population"><code>Scope and population
  |
Initial symptom
  |
Scope analysis (how large?)
  |-- lane / module / host / rack / site
  |-- PN / firmware / lot / vendor / fleet
  |
Technical isolation
  |
Correlation analysis (which cohort?)
  |-- lot / date code / FW / cal / platform / location
  |
Containment and corrective action</code></pre>
Scope sets severity and priors. Correlation after isolation unlocks contain, pause, replace, or supplier escalate (§12.10, Appendix G.12).

> **Engineering heuristic.** Population behavior is usually more informative than one failing unit. A cohort plot often beats another hour on the same sample.

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
Sudden and gradual are priors that reorder the bench, not confirmed-mechanism claims (Chapter 12).

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
Bisect domains before opening packages (§6.8, Appendix I.2).

## Supplier qualification

<pre class="dectree" aria-label="Supplier qualification"><code>Supplier qualification
  |
Requirements (customer-visible)
  |
Characterization (multi-lot distributions, not hero units)
  |
Margin under stress
  |
Qualification (named mechanisms)
  |
Production readiness (FAIR, ATP, SPC)
  |
Fleet monitoring (RMA, telemetry)</code></pre>
Customer view measures external behavior. Vendor view owns internals (Appendix A.8.7, Appendix G.16).

## Supplier escape containment flow

<pre class="dectree" aria-label="Supplier escape containment flow"><code>Supplier escape containment flow
  |
Escape detected
  |
Provisional containment
  |
Scope analysis
  |
Refine contained population
  |
Investigate / confirm mechanism
  |
Corrective action
  |
Recurrence control
  |
Decision closure: owner / timeline / reversibility / follow-up</code></pre>
> **Engineering heuristic.** Contain first when the population can grow. Perfect mechanism stories do not unship yesterday's lot.

Use provisional containment when the population can grow, then refine the hold after scope analysis. The system owner keeps responsibility for evidence quality and verifying corrective action (Appendix G.18, §12.10, Appendix D.16).

## Margin-consumption flow

<pre class="dectree" aria-label="Margin-consumption flow"><code>Margin-consumption flow
  |
Nominal system margin
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
This is a conceptual margin flow. Measure net margin at a defined reference plane and avoid double-counting overlapping penalties (§7.19, Appendix E.5).

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
An optical eye is measured externally with suitable access. Do not assume the module reports a conventional eye unless that capability exists (Appendix A.8.7).

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
Containment, confirmed mechanism, and prevention are three different actions (Appendix G.18).

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
Production validation is replayable and decision-oriented (Appendix G.16, Appendix G.14).

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
Unknown mechanism is not a freeze. Decide with weighted evidence (Appendix A.6, Appendix D.14).

## Evidence block

Use this block for validation reports, qualification plans, supplier reviews, fleet incidents, and interview answers. Speak evidence language in order: observation ("I measured..."), correlation ("these units share..."), hypothesis ("this suggests..."), confirmation ("I reproduced..."), decision ("I will..."). Do not say "data proves" until confirmation exists.

<pre class="dectree" aria-label="Evidence block"><code>Evidence block
  |
Claim: what are we trying to establish?
  |
Population: units, lots, hosts, environments
  |
Measurement: metric + reference plane + condition
  |
Access: Level 0--4 (Appendix A.2)
  |
Condition: T, V, pattern, ORL, traffic, dwell
  |
Evidence strength: n, repeatability, confidence
  |
Decision: what action is justified?
  |
Control: how recurrence or drift is detected</code></pre>
##### Decision closure.

Every tree that ends in an action should close with:

<pre class="dectree" aria-label="Decision closure"><code>Decision closure
  |
Decision: what action now?
  |
Owner: who is accountable?
  |
Timeline: when must it complete?
  |
Reversibility: how hard to undo?
  |
Follow-up control: ATP / SPC / telemetry / supplier CA</code></pre>
Example (supplier defect): stop shipment of the scoped lot; owner Operations plus Quality; follow-up is supplier corrective action and the production or fleet control that would catch the next escape.

Chapter 11, Chapter 12, Appendix C point here rather than restating the list.

##### Boundaries (trees are not proof).

Decision trees prioritize the next measurement. They do not convert a symptom into a confirmed mechanism. A controlled swap localizes ownership only to the extent that other variables remain unchanged. A passing retest is not closure: restore the original failing condition with margin and implement a recurrence control (Chapter 12, Chapter 11, Appendix A.12).

## Decision-Tree Interview Drills

Compact navigation drills. Enter the correct route quickly. Do not invent a second lifecycle; re-enter Appendix D.2, Table 11.2 when the decision requires it. Score spoken answers with Appendix A.12.1 if useful; use Appendix A.12 for full case practice.

##### Scenario 1. BER rises while average power remains stable.

*First action.* Preserve lane-resolved BER and FEC history and identify the receive reference plane.\
*Route.* BER shift-versus-floor (§6.8, Appendix D.4).\
*Evidence needed.* BER waterfall, OMA or transmitter-quality evidence, receiver sensitivity, ORL or reflection evidence, timing and equalizer behavior.\
*Decision point.* Which ledger limits first: power, noise, timing, spectrum, or control.\
*Common trap.* Stable average power clears the optical path.

##### Scenario 2. One station disagrees with the laboratory reference.

*First action.* Hold suspect production output and preserve software, limits, calibration, and fixture state.\
*Route.* Measurement-system and station-correlation (Chapter 11, Appendix D.14).\
*Evidence needed.* Golden and range-spanning units, repeatability, cross-station bias, and trusted reference-bench measurements.\
*Decision point.* Separate station bias from product variation before changing limits or supplier ownership.\
*Common trap.* Correct the station by changing its acceptance limit.

##### Scenario 3. Qualification sample fails after temperature cycling.

*First action.* Preserve the stressed state and compare with the pre-stress baseline.\
*Route.* Package-fatigue and intermittent-mechanism (Chapter 11, Appendix D.3).\
*Evidence needed.* Continuity, intermittent monitoring, optical alignment, BER, physical inspection, lot genealogy, and cycle chronology.\
*Decision point.* Isolated, lot-correlated, process-related, or design-wide.\
*Common trap.* One failure automatically invalidates the entire qualification matrix.

##### Scenario 4. Failures cluster by date code after 90 days.

*First action.* Scope by installation age, supplier lot, production history, host, site, and firmware.\
*Route.* Manufacturing-escape versus reliability-gap (Chapter 11, Appendix D.9).\
*Evidence needed.* ATP first-pass data, rework history, degradation signature, physical evidence, and qualification coverage.\
*Decision point.* Manufacturing, qualification, system, or mixed ownership.\
*Common trap.* Date-code correlation proves supplier root cause.

##### Scenario 5. One wavelength reports locked but has poor BER.

*First action.* Verify absolute wavelength, channel assignment, actuator headroom, and transmitter quality.\
*Route.* Source-versus-ring/filter alignment (Chapter 8, §8.4).\
*Evidence needed.* OSA or wavemeter, heater or TEC code, lock error, OMA, filter alignment, and BER during controlled source and filter sweeps.\
*Decision point.* Locked state correct, marginal, or on the wrong resonance.\
*Common trap.* A locked-status bit proves correct grid placement.

##### Scenario 6. A module swap clears the failure.

*First action.* Record every variable changed by the swap and preserve the original module, fiber, and port.\
*Route.* Controlled-swap ownership (Chapter 12, Appendix D.5).\
*Evidence needed.* Reverse swap, original-condition reproduction, connector inspection, firmware state, thermal contact, and path comparison.\
*Decision point.* Symptom follows module, port, fiber, contact disturbance, or reset state.\
*Common trap.* The swapped module is the confirmed root cause.

##### Scenario 7. Link flaps disappear after power cycling.

*First action.* Preserve remaining event history and identify which states were reset.\
*Route.* Intermittent and state-transition (Chapter 11, Appendix D.6).\
*Evidence needed.* Retrains, FEC bursts, CMIS transitions, host events, thermal state, rail behavior, and firmware logs.\
*Decision point.* Software or control recovery versus electrical, optical, thermal, or contact mechanisms.\
*Common trap.* Power-cycle recovery proves firmware ownership.

##### Scenario 8. One lane degrades under neighbor loading.

*First action.* Capture lane and neighbor state, thermal telemetry, control codes, and error timing.\
*Route.* Local thermal-crosstalk or shared-resource (Chapter 8, §8.5, Appendix D.5).\
*Evidence needed.* Neighbor on/off experiment, temperature mapping, wavelength or lock state, electrical crosstalk evidence, and lane remap where supported.\
*Decision point.* Symptom follows optical channel, electrical lane, local thermal path, or shared supply.\
*Common trap.* One-lane behavior proves a defective source.

## Before you start: three checklists

> **Before debugging**
>
> - Scope (lane / module / host / rack / site / lot / vendor / fleet)
>
> - Time behavior (sudden or gradual)
>
> - Stable average received power? (power vs signal-quality path)
>
> - Highest-value isolate chosen
>
> - Leading mechanism stated (not yet confirmed RC)
>
> - Decision unlocked with owner, timeline, and recurrence control

> **Before qualification**
>
> - Nominal function demonstrated
>
> - Operating margin known
>
> - Environmental and reliability stresses mapped to mechanisms
>
> - Interoperability headroom retained on supported combos
>
> - Manufacturing variation and ATP escape detection covered
>
> - Controlled pilot exit criteria and fleet telemetry owners set

> **Before production**
>
> - Requirements and margin demonstrated
>
> - Environment and interop verified
>
> - Reliability risk addressed with named confidence
>
> - Lot / site / date-code variation characterized
>
> - ATP / sample / SPC controls classified
>
> - Supplier controls reviewed; pilot exit and fleet monitor ready

**Key idea.** These trees are the book's reusable method. Chapters supply the physics and the numbers. This appendix supplies the order of thought.


<div class="nav-links">
  <a href="ch15-thirty-second-interview-frameworks">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch17-optical-measurement-and-test-reference">Next &rarr;</a>
</div>
