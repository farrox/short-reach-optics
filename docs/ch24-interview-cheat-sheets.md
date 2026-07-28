---
layout: default
title: "Appendix M: Interview Cheat Sheets"
---

# Appendix M: Interview Cheat Sheets

Printable one-pagers for fast review before an interview. Each page is a memory trigger, not a substitute for the chapter. Read the goal, walk the checklist, say the answer out loud, then use the pressure pivot.

## Book overview

*Universal rule.* State the decision, name the evidence, explain the tradeoff, and say what you would do next.

##### Lifecycle spine.

Model the link $\rightarrow$ choose the architecture $\rightarrow$ control wavelength and margins $\rightarrow$ establish readiness $\rightarrow$ qualify life $\rightarrow$ validate manufacturing $\rightarrow$ operate the fleet $\rightarrow$ investigate failures.

<table class="book-table"><tr><th>Ch</th><th>Main question</th></tr><tr><td>4</td><td>What sets BER and margin?</td></tr><tr><td>5</td><td>How do the source and modulator behave?</td></tr><tr><td>6</td><td>How do wavelength and WDM stay controlled?</td></tr><tr><td>7</td><td>What evidence is needed before release?</td></tr><tr><td>8</td><td>Will time and exposure cause permanent degradation?</td></tr><tr><td>9</td><td>Can the factory build and control it repeatedly?</td></tr><tr><td>10</td><td>How does optical behavior affect the system and workload?</td></tr><tr><td>11</td><td>How do I find and prevent the real cause of a failure?</td></tr></table>
##### How to use these sheets.

Spend about 2--3 minutes per page. Chapters 7--11 first if time is short. Full depth: Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11.

## Chapter 4: Quantitative link behavior

*Goal.* Explain what sets bit-error rate (BER) and margin without hiding behind a single number.

##### Mental checklist.

Define planes $\rightarrow$ Build budget $\rightarrow$ Add noise $\rightarrow$ Find boundary $\rightarrow$ Measure margin $\rightarrow$ Check assumptions

##### What I need to know.

- BER is an outcome of signal, noise, bandwidth, distortion, and decision behavior.

- Average power alone does not define receiver performance.

- A waterfall shows how performance changes as margin is removed.

- A floor suggests that adding more power may not solve the problem.

- Always state the reference plane and forward-error correction (FEC) condition.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Average optical power</td><td>Receiver sensitivity at a named BER</td></tr><tr><td>Waterfall shift</td><td>Error floor</td></tr><tr><td>Pre-FEC activity</td><td>Post-FEC residual</td></tr></table>
##### Numbers worth remembering.

Margin is the distance from the operating point to the measured failure boundary.

##### Trap.

Trap: Quoting BER without plane, pattern, or FEC condition.\
Better: Name the plane and the BER or FEC objective first.

##### 60-second answer.

"I start by naming the reference plane and the BER or FEC condition. Then I build a simple budget for signal and the main noise or impairment terms, find the failure boundary, and measure how much margin remains. If the waterfall shifts, more power may help. If I see a floor, I look for noise, reflection, or decision limits instead of chasing average power."

##### Pressure.

Pressure: "Our average Rx power looks fine. Why is BER bad?"\
Pivot: "Stable average power rules out gross loss, not timing, noise, or distortion. I would pull a waterfall and check for a floor."

Depth: Chapter 4.

## Chapter 5: Sources and modulation

*Goal.* Choose and operate a source so the modulated link closes the system budget, not just a lab power target.

##### Mental checklist.

Choose source $\rightarrow$ Set operating point $\rightarrow$ Modulate $\rightarrow$ Control temperature $\rightarrow$ Check quality $\rightarrow$ Reserve headroom

##### What I need to know.

- Laser output power is not the same as useful modulated signal.

- Bias, temperature, slope efficiency, extinction, chirp, and bandwidth interact.

- The control loop needs room to respond over temperature and aging.

- The best source closes system, reliability, and manufacturing budgets, not only the best nominal lab result.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>CW launch power</td><td>Modulated OMA / usable signal</td></tr><tr><td>Nominal lab result</td><td>Worst-corner closed budget</td></tr><tr><td>Bias setting</td><td>Remaining control headroom</td></tr></table>
##### Trap.

Trap: Picking the laser with the highest room-temperature power.\
Better: Ask which source still closes margin, reliability, and factory control at the claimed corners.

##### 60-second answer.

"I choose the source from the system budget: reach, modulation, temperature, reliability, and manufacturability. I set bias and temperature with headroom for aging, then check modulated quality, not only CW power. If the loop is already at the stop at one corner, the design is not ready."

##### Pressure.

Pressure: "Why not just raise bias for more power?"\
Pivot: "Bias also moves extinction, chirp, reliability, and headroom. I would show the net margin, not one power number."

Depth: Chapter 5.

## Chapter 6: WDM and wavelength control

*Goal.* Keep channels on the grid across temperature, process, and aging with enough control authority left.

##### Mental checklist.

Set grid $\rightarrow$ Model drift $\rightarrow$ Sense error $\rightarrow$ Correct wavelength $\rightarrow$ Check authority $\rightarrow$ Handle failure

##### What I need to know.

- Wavelength is a control problem, not only a nominal setting.

- Temperature, process, aging, and neighboring channels move the operating point.

- Heater or TEC authority must remain at the worst corner.

- Passing at room temperature does not prove control across life.

- Monitor both wavelength and how hard the loop is working.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Locked flag</td><td>Remaining control headroom</td></tr><tr><td>Room-temp pass</td><td>Life and corner control</td></tr><tr><td>Source drift</td><td>Filter or ring drift</td></tr></table>
##### Trap.

Trap: Treating "locked" as proof of margin.\
Better: Check lock error and actuator demand at the worst claimed corner.

##### 60-second answer.

"I treat wavelength as a closed-loop problem. I name the grid, the drift sources, and the sense/correct path. Then I ask whether the actuator still has room at the hot and aged corners. A lock bit without headroom is not a passing control design."

##### Pressure.

Pressure: "It locks on the bench. Ship it?"\
Pivot: "Not until I see authority and wavelength error across temperature and aging, not only a room-temp lock."

Depth: Chapter 6.

## Chapter 7: Product readiness

*Goal.* Know what evidence is required before release, and which question each stage answers.

##### Mental checklist.

Define $\rightarrow$ Review $\rightarrow$ Bring up $\rightarrow$ Characterize $\rightarrow$ Verify/validate $\rightarrow$ Qualify $\rightarrow$ Validate factory $\rightarrow$ Pilot $\rightarrow$ Ramp $\rightarrow$ Monitor $\rightarrow$ Learn

##### What I need to know.

- Product readiness is the umbrella lifecycle.

- Characterization maps behavior; verification checks frozen requirements.

- System validation proves intended use.

- Reliability qualification and manufacturing validation answer different questions.

- Later evidence cannot replace missing earlier evidence.

- Program labels such as EVT, DVT, and PVT do not define what the evidence proves.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Characterization</td><td>Verification</td></tr><tr><td>System validation</td><td>Reliability qualification</td></tr><tr><td>Manufacturing validation</td><td>Qualification life claim</td></tr><tr><td>Phase label (EVT/DVT/PVT)</td><td>Evidence content</td></tr></table>
##### Trap.

Trap: Using a phase name as proof of readiness.\
Better: Translate the phase into hardware, evidence, open risks, and the exit decision.

##### 60-second answer.

"I start from the claim and the decision gate. Characterization maps the behavior. Verification checks frozen requirements. System validation proves intended use. Qualification and manufacturing validation answer life and factory questions separately. I will not use a later pass to paper over a missing earlier step."

##### Pressure.

Pressure: "We are in PVT. Are we done?"\
Pivot: "PVT is a program label. I ask what evidence exists for the remaining risks and what decision it supports."

Depth: Chapter 7, Table 7.3.

## Chapter 8: Reliability qualification

*Goal.* Build a life or environment claim from mechanism and evidence, not from a copied test list.

##### Mental checklist.

Claim $\rightarrow$ Mechanism $\rightarrow$ Stress $\rightarrow$ Observable $\rightarrow$ Acceptance $\rightarrow$ Samples $\rightarrow$ Confidence $\rightarrow$ Decision $\rightarrow$ Handoff

##### What I need to know.

- Start with the claim and failure mechanism, not a test list.

- The stress must accelerate the field mechanism without creating a different one.

- Separate reversible hot behavior from permanent degradation.

- Zero failures do not mean zero failure rate.

- HTOL is qualification evidence; burn-in is an optional production screen.

- Standards provide methods, not the complete argument.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>HTOL / qual stress</td><td>Production burn-in screen</td></tr><tr><td>Reversible thermal behavior</td><td>Permanent wear-out</td></tr><tr><td>Component FIT</td><td>System availability</td></tr></table>
##### Numbers worth remembering.

One FIT $=1$ failure per $10^9$ device-hours. Zero observed fails still leaves a one-sided upper bound on rate.

##### Trap.

Trap: Saying "we passed GR-468" as the whole reliability argument.\
Better: State the claim, mechanism, stress relevance, sample basis, and residual risk.

##### 60-second answer.

"I start from the life claim and the mechanism. I choose a stress that accelerates that mechanism, define the observable and acceptance rule, then size samples for the confidence I need. Zero fails still leave an upper bound. I handoff production screens only when the screen separates real escapes."

##### Pressure.

Pressure: "Can we skip HTOL if burn-in looks clean?"\
Pivot: "Burn-in is a screen. It does not replace the qualification claim unless the argument explicitly says so."

Depth: Chapter 8.

## Chapter 9: Manufacturing validation

*Goal.* Prove the factory can repeatedly build, measure, and control the released design.

##### Mental checklist.

Freeze $\rightarrow$ Represent $\rightarrow$ Trace $\rightarrow$ Trust measurement $\rightarrow$ Read yield $\rightarrow$ Check stability $\rightarrow$ Measure capability $\rightarrow$ Control $\rightarrow$ React $\rightarrow$ Ramp

##### What I need to know.

- Freeze the production reference; changes need approval.

- Validate the measurement system before believing yield.

- First-pass yield shows process health; final yield may hide rework.

- Look at the distribution before using capability numbers.

- Stable process first, then $C_p$ and $C_{pk}$.

- Every control needs a trigger, owner, action, and restart rule.

- Passing good units does not prove a screen catches bad ones.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Control limits</td><td>Specification limits</td></tr><tr><td>ATP / acceptance limits</td><td>Specification limits</td></tr><tr><td>First-pass yield</td><td>Final yield</td></tr><tr><td>C_p (spread)</td><td>C_pk (spread and offset)</td></tr></table>
##### Numbers worth remembering.

$C_p$ asks whether the process spread could fit the specification if centered. $C_{pk}$ includes the actual process offset.

##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab / learning build</td><td>Learn and separate variables</td></tr><tr><td>Pilot lot</td><td>Protect lot integrity; collect representative evidence</td></tr><tr><td>Production</td><td>Protect shipments; execute the reaction plan</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Using final yield to hide heavy rework.\
Better: Separate first-pass yield, retest, rework, scrap, and final yield.

##### 60-second answer.

"I freeze the production reference, build a representative population, and clear the measurement system before I trust yield. I look at first-pass yield and the distribution, establish stability, then interpret $C_p$ or $C_{pk}$. Controls need owners and reaction plans. I ramp only when evidence supports the next volume."

##### Pressure.

Pressure: "Final yield is 99%. Ship?"\
Pivot: "Not until I know first-pass yield and what the recovery path is costing and hiding."

Depth: Chapter 9, Table 9.3.

## Chapter 10: Optical links in operation

*Goal.* Connect physical margin to FEC, recovery, workload impact, and fleet decisions.

##### Mental checklist.

Observe $\rightarrow$ Read FEC $\rightarrow$ Find bursts $\rightarrow$ Check recovery $\rightarrow$ Use telemetry $\rightarrow$ Compare cohorts $\rightarrow$ Judge impact $\rightarrow$ Contain

##### What I need to know.

- Link-up is not the same as link health.

- Corrected errors can reveal shrinking margin before traffic fails.

- Average BER can hide short bursts.

- Recovery time and repeated retrains matter.

- Telemetry is useful when it separates a cause or changes an action.

- Component failure rate is not system availability.

- At fleet scale, a rare per-link event may happen frequently.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Link-up</td><td>Link health over time</td></tr><tr><td>Corrected-error rise</td><td>Service already failing</td></tr><tr><td>Component FIT</td><td>Fleet event rate and availability</td></tr></table>
##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab</td><td>Learn and reproduce</td></tr><tr><td>Pilot</td><td>Bound exposure; keep observability</td></tr><tr><td>Production fleet</td><td>Protect the workload; contain first</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Treating a link as healthy because it is up.\
Better: Check corrected errors, bursts, retrains, and recovery time.

##### 60-second answer.

"Link-up is a state; health is a distribution over time. I read FEC activity for consumed margin, look for bursts, and check recovery duration and repeats. I use telemetry that separates hypotheses, compare affected and unaffected groups, and judge severity from workload impact. Component FIT alone is not availability."

##### Pressure.

Pressure: "Post-FEC looks clean. Why worry?"\
Pivot: "Clean post-FEC can still hide rising corrected-error demand and short bursts. I would inspect those distributions before calling the link healthy."

Depth: Chapter 10.

## Chapter 11: Failure analysis

*Goal.* Find the real cause without destroying the evidence, then stop it from happening again.

##### Mental checklist.

Protect $\rightarrow$ Preserve $\rightarrow$ Scope $\rightarrow$ Classify $\rightarrow$ Hypothesize $\rightarrow$ Test $\rightarrow$ Prove $\rightarrow$ Fix $\rightarrow$ Prevent $\rightarrow$ Verify

##### What I need to know.

- Do not reset, clean, or swap before preserving evidence.

- A symptom is not a cause.

- Timing helps: sudden, gradual, or intermittent.

- Shared failures suggest a shared dependency.

- Use reversible tests first.

- A swap can isolate ownership without proving the physical mechanism.

- It is acceptable to say the mechanism is not yet confirmed.

- The case is not closed until recurrence control works on fresh data.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Failure mode / symptom</td><td>Failure mechanism</td></tr><tr><td>Correction</td><td>Recurrence control</td></tr><tr><td>Ownership from a swap</td><td>Microscopic proof</td></tr></table>
##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab</td><td>Learn quickly and reproduce</td></tr><tr><td>Vetting or pilot lot</td><td>Protect lot integrity; collect representative evidence</td></tr><tr><td>Production fleet</td><td>Protect the workload; avoid disruptive tests until safe</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Reseating first, or closing when the unit recovers.\
Better: Preserve state, then close only after a recurrence control works on fresh data.

##### 60-second answer.

"I start by protecting the workload and preserving the failing state. Then I scope the issue by lane, module, host, lot, firmware, and site. I build a short list of likely causes and use the smallest safe test, often a controlled swap, to see what the problem follows. I do not call root cause from one correlation. Once the cause is supported, I fix the immediate issue, put in a control to prevent recurrence, and verify it on fresh data."

##### Pressure.

Pressure: "What if it is in production and you cannot swap anything?"\
Pivot: "I protect the workload and collect non-disruptive evidence first. I schedule intrusive tests only after traffic is drained or risk is contained."

Depth: Chapter 11, Appendix I.

## Cross-chapter interview habits

##### How to answer technical questions.

1.  Start with the decision or distinction.

2.  State what you would check first.

3.  Explain why that check is high value.

4.  Name the main tradeoff.

5.  Say what result would change your direction.

6.  Avoid claiming more than the evidence supports.

7.  End with the action or release decision.

##### Useful phrases.

- "The first thing I would separate is..."

- "I would not interpret that result until..."

- "That raises a hypothesis, but it does not prove the cause."

- "I would choose the cheapest safe test that separates the leading causes."

- "The same measurement can support several claims, but the decision is different."

- "I would protect the workload first, then preserve enough evidence to investigate."

- "I would not call the case closed until the fix works on fresh data."

##### Universal traps.

- Jumping from correlation to cause.

- Quoting a number without plane or condition.

- Treating pass/fail as margin.

- Treating a standard as the complete engineering argument.

- Assuming a passing sample represents the whole population.

- Treating link-up as health.

- Treating final yield as process health.

- Fixing the failed unit without preventing recurrence.

*Design rule.* One page, one mental model, one spoken answer.


<div class="nav-links">
  <a href="ch23-abbreviations-and-terminology">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch25-references">Next &rarr;</a>
</div>
