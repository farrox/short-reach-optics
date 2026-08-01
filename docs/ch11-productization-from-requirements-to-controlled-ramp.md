---
layout: default
title: "Ch 11: Productization: From Requirements to Controlled Ramp"
---

# 11 Productization: From Requirements to Controlled Ramp

    

This chapter shows how a technically sound optical design becomes a controlled product. It is one lifecycle, not five separate interview subjects. Detail that used to live in separate readiness, qualification, manufacturing, and operations chapters is relocated: lifecycle tables and discipline definitions in Appendix F; manufacturing depth in Appendix G; link-operation and fabric survey in Appendix H. Failure analysis remains Chapter 12.

*Read first:* the spine below, the discipline table (Table 11.1), and the eight interview questions.

*Deep dive:* relocated narratives behind the appendix pointers above.

**Key idea.** Productization is the path from a product claim to a controlled ramp with residual risk that you can name. Architecture margin, measurement integrity, lifetime mechanisms, factory control, and bounded field exposure are one argument. Memorizing EVT/DVT/PVT labels or long process catalogs is not the point.

## One lifecycle

Use this order when you reason about readiness. Calendar work may overlap. A later gate cannot replace missing earlier evidence.

> Define the product claim $\rightarrow$ close the architecture $\rightarrow$ characterize margins $\rightarrow$ verify the design $\rightarrow$ validate the system $\rightarrow$ qualify lifetime risks $\rightarrow$ validate the factory $\rightarrow$ run a controlled pilot $\rightarrow$ ramp and monitor.

The eleven-step table follows in this chapter (Table 11.2, §11.3). Phase-name translation and ownership detail remain in the relocated narrative (§11.4, Table 11.4).

##### Define the product claim.

Write measurable requirements at named reference planes: optical, electrical, thermal, management, reliability, and manufacturing. Name the release decision each requirement supports. Without a claim, later data has no decision context.

##### Close the architecture.

Ask whether optical, electrical, thermal, control, lifetime, and factory budgets have a credible path. Catch thin margins before hardware makes changes expensive. Derating and corner intent belong here (Appendix F.21.1, §11.9.2).

##### Characterize margins.

Map nominal behavior, spread, sensitivities, and failure edges. Build a behavioral model before you treat a number as a requirement result (§11.9.4).

##### Verify the design.

Compare evidence with frozen requirements at named planes and conditions. Verification answers "does it meet the contract?" It does not by itself prove intended-use fitness or lifetime.

##### Validate the system.

Prove the product works in the intended host, peer, fiber, firmware, thermal, and workload envelope. System validation is narrower than productization (Table 11.1, Appendix F.21.3).

##### Bring-up before characterization.

Bring-up proves that hardware, firmware, management states, and a basic link work reproducibly. Until that state exists, characterization numbers are not interpretable. Name power rails, clocks, CMIS or equivalent state, optical enable sequence, and the first BER or FEC observation that shows the link is alive (§11.11, §11.9.3).

## Evidence disciplines in one table

Keep the distinctions. Do not turn them into a dozen interview definitions.

<table class="book-table"><tr><th>Discipline</th><th>Primary question</th><th>Main output</th><th>What it does not replace</th></tr><tr><td>Characterization</td><td>How does the design behave and vary?</td><td>Behavioral model, distributions, sensitivities, failure boundaries</td><td>Requirement verification or release approval</td></tr><tr><td>Verification</td><td>Does measured evidence meet the frozen requirement?</td><td>Traceable requirement result with conditions and uncertainty</td><td>Intended-use evidence</td></tr><tr><td>System validation</td><td>Is the complete product suitable for its intended system use?</td><td>Supported operating and interoperability envelope</td><td>Lifetime qualification or factory capability</td></tr><tr><td>Reliability qualification</td><td>Will time and exposure cause unacceptable permanent degradation?</td><td>Mechanism-specific life and environmental confidence</td><td>Every-unit screening or manufacturing reproducibility</td></tr><tr><td>Manufacturing validation</td><td>Can the production system repeatedly build, measure, trace, and control the design?</td><td>Production capability, measurement confidence, control plan, ramp evidence</td><td>System validation or life qualification</td></tr><tr><td>Production acceptance testing</td><td>Should this unit or population proceed?</td><td>Pass, fail, hold, rework, or disposition record</td><td>Complete mechanism coverage or design qualification</td></tr><tr><td>Pilot deployment</td><td>Does a bounded production-representative population behave as predicted operationally?</td><td>Controlled field evidence and expansion decision</td><td>Uncontrolled mass deployment</td></tr><tr><td>Fleet monitoring</td><td>Does the deployed population match the release model?</td><td>Trends, cohorts, alerts, incident evidence, next-revision learning</td><td>Root-cause confirmation by itself</td></tr></table>
**Table 11.1.** Evidence disciplines and the decisions they can honestly support. Abbreviations: Appendix L.

The same measurement can serve more than one discipline; the claim and decision change, not the instrument.

Program names such as EVT, DVT, and PVT are company containers, not universal proof categories. Interpret a phase gate by asking which build, which evidence, which residual risks, and which decision (§11.4, Table 11.3).

## The optical product-readiness lifecycle

## Why program-phase names are not enough

EVT[^15], DVT[^16], and PVT[^17] are company containers for program timing, not universal technical definitions. Sample size, exit criteria, and which evidence lands in which phase vary by organization. Manufacturing-gate lookup for the same names lives in Table G.1. Expanded EVT/DVT/PVT goal lists live in Appendix F.17.1.

**Key idea.** EVT, DVT, and PVT describe program timing and maturity. Characterization, verification, system validation, reliability qualification, and manufacturing validation describe what the evidence proves. When someone says EVT, DVT, or PVT, ask four questions. Which hardware and software configuration is included? Which engineering evidence is expected? Which risks remain intentionally open? What decision or exit gate does the phase enable?

After pilot, programs often speak of MP[^18] and sustaining. Those labels still need an exit decision.

<table class="book-table"><tr><th>Program label</th><th>Common emphasis</th><th>Typical product-readiness work</th></tr><tr><td>EVT</td><td>Architecture and engineering learning</td><td>Architecture review, prototype bring-up, risk retirement, early characterization, measurement development</td></tr><tr><td>DVT</td><td>Design evidence and intended-use closure</td><td>Characterization completion, requirement verification, margin, interoperability, system validation, substantial qualification evidence</td></tr><tr><td>PVT</td><td>Production-intent and ramp readiness</td><td>Production-reference freeze, manufacturing validation, measurement-system analysis, ATP coverage, process capability, controlled ramp evidence</td></tr><tr><td>Pilot / limited deployment</td><td>Bounded operational evidence</td><td>Cohort deployment, enhanced telemetry, success criteria, rollback, fleet comparison</td></tr><tr><td>MP / sustaining</td><td>Controlled volume and field learning</td><td>Ramp, SPC, supplier controls, fleet monitoring, failure analysis, next-revision feedback</td></tr></table>
**Table 11.3.** Illustrative mapping from program-phase labels to product-readiness work. EVT, DVT, and PVT are not standards, and their activities overlap. Always ask what hardware population, evidence, and exit decision the phase label represents. Reliability planning may begin in EVT, representative qualification may run through DVT, and corrective requalification may continue into PVT.

##### Who owns which evidence.

<table class="book-table"><tr><th>Topic</th><th>Primary owner</th></tr><tr><td>IM/DD architecture and link budget</td><td>ch:imdd</td></tr><tr><td>Noise, sensitivity, RIN, BER, and metric interpretation</td><td>ch:models</td></tr><tr><td>Sources and modulation</td><td>ch:lasers</td></tr><tr><td>WDM and wavelength control</td><td>ch:wdm</td></tr><tr><td>Advanced packaging, 2.5D/3D, and CPO design judgment</td><td>ch:packaging</td></tr><tr><td>AI/HPC rack architecture, fat-tree, rails, oversubscription</td><td>ch:hpc</td></tr><tr><td>Product-readiness sequence and system-validation decisions</td><td>ch:product-readiness</td></tr><tr><td>Reliability qualification</td><td>ch:reliability</td></tr><tr><td>Manufacturing validation and production control</td><td>ch:manufacturing</td></tr><tr><td>Optical-link operation, FEC, recovery, telemetry, and availability</td><td>ch:networking</td></tr><tr><td>AI fabric context (topologies, module styles, CPO/XPO survey)</td><td>app:ai-fabric-context</td></tr><tr><td>Failure analysis and recurrence control</td><td>ch:failure-modes</td></tr><tr><td>Instruments, procedures, and test-reference material</td><td>app:measurement-reference</td></tr><tr><td>Decision navigation</td><td>app:decision-trees</td></tr></table>
**Table 11.4.** Where detailed ownership lives. The productization chapter keeps the readiness sequence and decisions.

## Mechanism-driven qualification

Reliability qualification is a bounded confidence argument, not a copied test list.

> Claim $\rightarrow$ mechanism $\rightarrow$ stress $\rightarrow$ observable $\rightarrow$ acceptance $\rightarrow$ samples $\rightarrow$ confidence $\rightarrow$ decision $\rightarrow$ handoff.

The stress must accelerate the field mechanism without creating a different one. Define observables and acceptance before the stress runs. Representative samples matter; one convenient lot is not the released population. Zero failures still leave a one-sided upper bound, not a zero rate (Appendix F.8, Appendix F.10.1, Appendix F.10).

HTOL and similar stresses support life claims. Burn-in is an optional production screen. Neither replaces the other (Appendix F.7, Appendix F). Standards such as GR-468 supply methods and language; they are not the whole engineering argument (Appendix F.13).

##### Reversible heat versus permanent wear.

A temperature sweep on a healthy unit asks how the product behaves while hot. A qualification stress asks whether the exposure caused lasting change. Do not treat a hot pass as proof that the same corner is safe after aging (Table F.4).

##### Failure timing.

Early fails, random-in-time fails, and wear-out fails point to different controls. Infant mortality may justify a screen. Wear-out needs a life model and derating. Mixing them into one FIT number without stating the regime hides the decision (Appendix F.10.2, Appendix F.11).

##### FIT and DPPM in one breath.

One FIT is one failure per $10^9$ device-hours. DPPM counts defective units in a named population and window. FIT uses time exposure; DPPM uses inspected units. A FIT claim needs population, exposure, failure definition, model, and confidence. Component FIT is not fabric availability (Appendix F.10.1, Appendix H.25.1).

##### Acceleration validity.

An Arrhenius or other acceleration model is only useful when the named mechanism is active in the assumed regime and the stress did not invent a new failure physics. If the stress creates a different mechanism, the result does not support the field claim (Appendix F.9).

## Factory evidence

Manufacturing validation asks whether the production system can repeatedly build, measure, trace, and control the released design.

Freeze the production reference first: design, BOM, process, firmware, test software, fixtures, limits, and approved suppliers (Appendix G.9). Build representative populations and keep genealogy (Appendix G.10).

Trust the measurement system before you interpret yield (Appendix G.11). Separate first-pass yield from final yield: final yield can hide rework and unstable process health (Appendix G.12, Appendix G.12.1). Establish stability before $C_p$/$C_{pk}$. Remember the three limit sets: control limits describe process behavior, specification limits define product acceptance, and ATP limits disposition units (Table G.5, Appendix G.13).

Validate that ATP catches known bad cases, not only good units (Appendix G.14). Every reaction plan needs a trigger, owner, containment, evidence, restart rule, and follow-up (Table G.8). Ramp only when evidence supports the next volume step (Appendix G.17, Appendix G).

##### First-pass versus final yield.

Suppose 1000 eligible units enter a route. Nine hundred pass on the first valid attempt (FPY $=90\%$). After retest and approved rework, 990 are eventually accepted (final yield $=99\%$). The nine-point gap is the recovery path. Track it by failure mode, station, supplier, lot, and rework action. A release story that quotes only 99% hides the process health signal (Appendix G.12.1, Table G.4).

##### Stability before capability.

Plot the distribution, confirm the process is stable over time, then compute $C_p$/$C_{pk}$ against the specification. An unstable process makes capability numbers unreliable. Control limits are not specification limits; ATP limits are a third set used to ship, hold, or reject (Table G.5, Appendix G.13).

##### Representation before sample size.

Sample the populations that actually vary: wafers or lots, assembly lines, firmware revisions, and suppliers. Genealogy must survive rework. A large sample of the wrong population still misleads (Appendix G.10, Appendix G.10.1).

## Pilot, ramp, and fleet feedback

Link-up is not link health. A product can pass bring-up and still hurt a workload through rising corrected-error demand, short bursts, or recovery storms. The operational translation of physical margin lives in Appendix H and the relocated operations narrative (Appendix H.18, Appendix H.17).

A pilot is a bounded field experiment: identifiable units, production-intent configuration, enhanced telemetry, exit rules, and rollback (Appendix H.26, §11.9.8). A small shipment without those controls is not a pilot.

Expand only when metrics match the release model and no unexplained cohort appears. Pause when risk is widening, unexplained, or hard to contain. Fleet monitoring feeds escapes and margin discoveries back into requirements, ATP, qualification, and the next revision (§11.9.11, Appendix H.25.1).

##### What the system sees.

Translate physical impairment into system language before you argue health. Pre-FEC activity shows burden on the physical link. Corrected errors show FEC working while margin may be shrinking. Uncorrectables and retrains are recovery events with duration and repeat count. Average BER can hide short dangerous bursts (Appendix H.17, Appendix H.20, Appendix H.21).

##### Severity and cohorts.

Operational severity follows workload consequence, not only optical symptoms. Compare affected and unaffected groups that share lot, host, firmware, site, or age. Correlation narrows ownership; it does not prove mechanism (Appendix H.23, Appendix H.24, Chapter 12).

##### Availability is not FIT.

Fabric availability also depends on event duration, redundancy, reroute, and repair time. A rare per-link event can become frequent at fleet scale (Appendix H.25.1, Appendix H.25).

## What to protect when schedule is cut

Protect, in order:

1.  measurable requirements and named reference planes;

2.  measurement integrity (otherwise later data lies);

3.  thin architectural margins that cannot be recovered in the factory;

4.  mechanism coverage for the dominant life risks;

5.  factory controls that prevent shipping unknown populations;

6.  a reversible pilot before uncontrolled exposure.

Compress schedule by overlapping work and shrinking sample depth where residual risk is already bounded. Do not skip the claim, the architecture close, or measurement trust.

## Steps 1--11

Use Table 11.2 as the wall chart. The subsections below keep the step labels and handoff rules. Derating examples, characterization maps, and Step 5 evidence-domain detail live in Appendix F.21, Appendix F.21.1.

### Step 1: Define the requirements

Define performance, environment, reliability, manufacturing, and operational requirement classes with owners and named planes (§1.1, Table 7.4).

*Evidence and handoff:* Freeze a signed requirements slice; refuse hardware spend until success is defined.

### Step 2: Review the architecture

Close optical-power, noise, bandwidth, electrical, thermal, wavelength-control, reliability, manufacturing, and serviceability budgets on stated assumptions (§1.1, Table 7.10). Apply mechanism-based derating so temperature, aging, process spread, and measurement uncertainty do not consume the last margin (Appendix F.21.1).

*Evidence and handoff:* Proceed to bring-up only when budgets close or open items are named with redesign triggers.

### Step 3: Bring up the hardware

Establish a known, reproducible operating state. Separate integration fails from product-performance questions (§11.11).

*Evidence and handoff:* Continue when identity, supply rails, management-ready state, basic optical power, lock, and a simple link are reproducible.

### Step 4: Characterize the behavior

Map nominal behavior, distributions, sensitivities, interactions, failure boundaries, and signatures. Averages can hide weak tails (Appendix F.21.2, Appendix F.18).

*Evidence and handoff:* Name thin ledgers and candidate corners; proceed to Step 5, derate, or redesign before loaded-fleet claims.

### Step 5: Verify requirements and validate system use

 

Verification closes frozen requirements at named planes. System validation closes intended use across supported hosts, peers, firmware, fiber plants, and workloads (Appendix F.18, Appendix F.21.3). Track optical, electrical, thermal, and control ledgers separately (Appendix E.5, Table F.9). Golden-host margin is not the ecosystem exit (§11.11, Appendix F.21.3).

*Evidence and handoff:* Freeze requirement results, margin boundaries, and supported combinations before qualification claims rely on them.

### Step 6: Qualify reliability

Convert the operating envelope and credible mechanisms into a bounded life and environmental confidence argument. This is not a harder system-validation suite (Chapter 11, §11.5).

*Evidence and handoff:* Accept, derate, or hold life risk before unrestricted ramp.

### Step 7: Validate manufacturing

Prove the factory can reproduce and control the supported design: production reference, measurement system, yield, ATP, genealogy, and reaction plans (Chapter 11, §11.6).

*Evidence and handoff:* Authorize controlled production exposure only when multi-lot yield and escape detection support it.

### Step 8: Run a controlled pilot

Bounded production-representative deployment with cohort identity, success criteria, enhanced telemetry, and rollback (Appendix F.18, Chapter 11, §11.7).

*Evidence and handoff:* Expand, hold, restrict, or roll back from exit metrics versus the release model.

### Step 9: Ramp mass production

Sustain volume under ATP, SPC, supplier, and change controls after pilot exit (Chapter 11, Table G.1).

*Evidence and handoff:* Increase volume only while factory, supplier, and early-field indicators remain controlled.

### Step 10: Monitor the fleet

Compare deployed cohorts with the release model. Correlation prioritizes hypotheses; it does not confirm a mechanism (Appendix H.19, §12.10, Chapter 12).

*Evidence and handoff:* Contain, sustain, or investigate; return evidence to the appropriate earlier readiness step when the release model fails.

### Step 11: Feed learning into the next revision

Convert fleet and manufacturing evidence into changed requirements, designs, qualification, ATP, or controls (§1.1).

*Evidence and handoff:* Write next-revision targets with owners, or explicitly accept residual risk without change.

## Choosing evidence within a step

An experiment is not inherently characterization, verification, validation, or qualification. Its category is determined by the claim being made (Appendix F.18). Use the lowest-cost evidence that changes the decision. State reference plane, condition, population, uncertainty, and applicability. Reuse evidence across claims only when those conditions support the new claim.

A first discriminating measurement should separate broad ownership classes; for an optical-link symptom, named-plane power is often an inexpensive first split between gross attenuation and signal-quality hypotheses (Appendix I.13, §6.8).

> **Engineering heuristic.** Name the reference plane before you name the instrument. A pretty eye at the wrong plane is a wrong answer.

**Key idea.** Product readiness is a sequence of decisions, not a catalog of tests. Each step should produce evidence for one explicit decision and identify the uncertainty that remains.

## Bring-up and production-representative corners

Bring-up proves a module and system can be powered, managed, and linked the way production will run them. A quiet room-temperature BERT result is not system validation.

1.  Confirm identity, rails, temperature, and firmware.

2.  Reach the required management-ready state.

3.  Enable the intended lanes or light under host control.

4.  Establish the optical path and verify basic power.

5.  Establish electrical lock and lane alignment.

6.  Run basic traffic and capture a reproducible baseline.

A module forced into an emitting state and passing BER has not passed bring-up if its required management sequence, safe state, diagnostics, alarms, and recovery behavior are incorrect. That includes pluggable and external-laser forms such as ELSFP[^19]. Register-level CMIS detail lives in Appendix E.7, Appendix E.

##### Production-representative corners.

<table class="book-table"><tr><th>Corner class</th><th>Representative challenges</th></tr><tr><td>Thermal and loading</td><td>Case temperature, airflow, neighboring modules, full traffic</td></tr><tr><td>Electrical and host</td><td>Supported hosts, voltage corners, SerDes/equalization, reset and restart</td></tr><tr><td>Optical plant</td><td>Production fiber, connectors, reflections, loss, supported peers</td></tr><tr><td>Control and service</td><td>CMIS transitions, alarms, hot-swap, recovery, firmware combinations</td></tr></table>
**Table 11.4.** Production-representative corners for system validation. Mechanism detail: Chapter 7, Chapter 8, Chapter 11.

## Worked example: 800G DR4-class module

*Claim.* Ship an 800G DR4-class module for a named host family, reach, temperature range, pre-FEC BER objective, and FIT envelope.

*Architecture close.* Confirm modulator and laser headroom, host equalization assumptions, thermal path, CMIS state machine, and factory probe points. Flag any budget that closes only at nominal.

*Characterize.* Map Tx OMA, TDECQ, RIN under stated ORL, Rx sensitivity at the named BER plane, and corner sensitivities across voltage and temperature.

*Verify and validate.* Trace requirements to named planes. Run supported-host interoperability and loaded-chassis corners (§11.11).

*Qualify.* Pick mechanisms (laser wear-out, solder fatigue, moisture, electrostatic damage). Choose stresses that accelerate those mechanisms. State sample basis and residual risk (Appendix F.12).

*Factory.* Freeze BOM and firmware. Clear gauge R&R on the ATP stations that gate shipment. Track first-pass yield by failure mode. Set reaction plans for BER and extinction-ratio fallout.

*Pilot.* Deploy a bounded cohort with enhanced FEC and thermal telemetry, hold criteria, and rollback ownership. Expand only if distributions match the release model.

*Monitor.* Watch corrected-error and retrain cohorts by lot, host, and site. Feed escapes into ATP and the next revision (Appendix H.27.1, Chapter 12).

## Interview takeaway

**Key idea.** I show that the architecture can become a controlled product: claim, margin evidence, life argument, factory control, and reversible field exposure. I do not recite an NPI org chart. When evidence conflicts, I escalate the claim that is least supported, not the loudest dashboard.

## Interview Q&A

Practice aloud. Prefer first-person reasoning. Score with Appendix A.12.1. Extended productization drills live in the secondary bank (Appendix M.12, Appendix F, Appendix G).

##### Question 1. How do you know a new optical design is ready to move forward?

*Tests:* architecture margin; evidence; residual risk; decision-making.

*Spoken answer.* "I ask what claim we are trying to support next, what evidence closes the thin margins, and what residual risk remains. If the architecture still depends on an unproven budget, or if the measurement plane is undefined, I do not call it ready. Ready means the next gate has a named decision, not that every test in the lab passed once."

*Pressure follow-up.* "We have good bench BER. Why wait?"\
*Answer pivot.* "Bench BER without corners, host coverage, life mechanisms, or factory measurement trust is not a release argument."

*Trap:* "Ready means the prototype meets the datasheet at room temperature."

##### Question 2. How do characterization and system validation differ?

*Tests:* behavioral model versus intended-use evidence.

*Spoken answer.* "Characterization maps how the design behaves and where it fails. System validation asks whether the complete product works in the intended system and workload. I can characterize deeply on a reference host and still fail system validation on production hosts" (Table 11.1).

*Pressure follow-up.* "Where does verification fit?"\
*Answer pivot.* "Verification checks a frozen requirement at a named plane. It is neither a full behavioral map nor a full intended-use proof."

*Trap:* "Characterization, verification, and validation are just increasingly hard test levels."

##### Question 3. How do you build a mechanism-driven reliability plan?

*Tests:* claim, mechanism, acceleration, observable, acceptance.

*Spoken answer.* "I start from the life or environment claim, name the mechanism that could break it, choose a stress that accelerates that mechanism, define the observable and acceptance rule before stressing, then size samples for the confidence I need. Zero fails still leave an upper bound" (Appendix F.8, Appendix F.10.1).

*Pressure follow-up.* "Can we skip HTOL if burn-in looks clean?"\
*Answer pivot.* "Burn-in is a screen. It does not replace the qualification claim unless the argument explicitly says so."

*Trap:* "We passed GR-468, so reliability is done."

##### Question 4. How do you know the factory can reproduce the design?

*Tests:* measurement trust; yield; capability; controls.

*Spoken answer.* "I freeze the production reference, clear the measurement system, read first-pass yield and failure Pareto, confirm stability before capability, and check that ATP and reaction plans catch real defects. Final yield alone is not enough" (Appendix G.11, Appendix G.12, Table G.5).

*Pressure follow-up.* "Final yield is 99%. Ship?"\
*Answer pivot.* "Not until I know first-pass yield and what recovery is costing and hiding."

*Trap:* "A passing FAIR means the factory is ready at volume."

##### Question 5. What makes a pilot useful?

*Tests:* bounded exposure; observability; rollback.

*Spoken answer.* "A useful pilot has a hypothesis, production-representative hardware, enhanced telemetry, exit rules, and rollback. Expansion requires metrics that match the release model and no unexplained cohort" (Appendix H.26).

*Pressure follow-up.* "We already shipped a small lot. Is that a pilot?"\
*Answer pivot.* "Not if exposure, telemetry, and rollback were never defined."

*Trap:* "Any early customer shipment counts as a pilot."

##### Question 6. Schedule is cut. What evidence do you protect?

*Tests:* risk-based prioritization.

*Spoken answer.* "I protect requirements and planes, measurement integrity, thin architectural margins, dominant life mechanisms, factory controls that prevent unknown populations, and a reversible pilot. I compress calendar overlap before I erase those."

*Pressure follow-up.* "Management wants to skip the pilot."\
*Answer pivot.* "Then the residual risk acceptance must be explicit, owned, and reversible some other way. Skipping silently is not a plan."

*Trap:* "Cut whatever is last on the schedule."

##### Question 7. Supplier data says pass, but system behavior says otherwise. What do you do?

*Tests:* component versus system evidence.

*Spoken answer.* "I treat both as evidence under different claims. I re-check planes, conditions, populations, and whether the supplier test answers the system failure mode. I do not discard system evidence because a component ATP passed, and I do not blame the supplier until ownership is localized" (Appendix G.16, Chapter 12).

*Pressure follow-up.* "Can we ship while we investigate?"\
*Answer pivot.* "Only with bounded exposure, enhanced monitoring, and an owned containment trigger."

*Trap:* "Supplier pass clears the system fail."

##### Question 8. Give a 60-second productization plan.

*Tests:* end-to-end command of the spine.

*Spoken answer.* "Define the claim and planes, close the architecture, characterize margins, verify requirements, validate intended use, qualify the dominant life mechanisms, prove the factory can measure and control the design, run a bounded pilot with rollback, then ramp while monitoring cohorts and feeding escapes back. At each gate I name the decision, the evidence, and the residual risk."

*Pressure follow-up.* "Where do you start if hardware already exists?"\
*Answer pivot.* "I still write the claim and freeze the measurement planes first. Otherwise the existing data cannot support a release decision."

*Trap:* "Start wherever the lab is already busy."


<div class="nav-links">
  <a href="ch10-ai-and-hpc-rack-architecture">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch12-failure-analysis-from-symptom-to-confirmed-mechanism">Next &rarr;</a>
</div>
