---
layout: default
title: "Ch 7: Optical validation"
---

# 7 Optical validation

A datasheet that closes on a quiet bench is not a product. A quiet-bench close proves one corner under one setup. It does not prove that the link meets its requirements across the temperatures, hosts, connectors, production spread, and lifetime the fleet will actually see.

*Validation* is the process of building enough justified confidence to make those product decisions. Passing tests is an output, not the purpose. The job is to remove the uncertainty that blocks the next call: continue, redesign, derate, qualify, open volume, or hold. Debugging asks which margin ledger was exhausted. Qualification asks how much margin remains after the expected stresses. Both are uncertainty reduction that ends in a decision (app:decision-trees, tree-evidence-block). This chapter sequences that work from a single device to a deployed fleet (validation-workflow), then covers bring-up under production-like corners and the hypothesis-driven debug method the work demands.

Companies overload EVT, DVT, PVT, and "verification" differently. Unless noted otherwise, this book freezes meanings by *job*, not by org chart. Abbreviations are collected in app:abbreviations.

##### How the jobs differ.

*Characterization* maps how the design behaves. It discovers distributions, sensitivities, and cliffs. A characterization cliff improves understanding; it does not automatically fail the product. BER versus temperature, wavelength drift, receiver sensitivity, RIN, and bias trends belong here when the question is still "what happens when you change $X$?"

*Verification* asks a narrower question: does this implementation meet a stated requirement with a named method and reference plane? Transmit power, BER at a stated FEC objective, wavelength accuracy, and thermal operating range are verification when the requirement, plane, and method are already frozen.

*Validation* asks whether the product works for the intended customer and system use. Hosts, cable plant, temperatures, workloads, and install practice are in scope. A verified BER on a golden bench is not validation of the fleet claim.

*Qualification* asks whether you have evidence the design survives expected variation and life. The evidence is mechanism-based stress and sample humility, not a ritual checklist. HTOL, temperature cycling, humidity, and multi-lot process corners matter only when each stress maps to a named mechanism and an acceptance rule.

*Production test* asks whether you can repeatedly detect unacceptable units at volume. Factory and incoming screens catch escapes; they do not prove life. *ATP* (acceptance test) is one form of that process: a replayable accept/reject decision applied per unit, per lot, or by a documented sampling plan.

The split matters because the classic program failures are category errors: treating characterization cliffs as automatic product failure, treating ATP as life proof, or treating HTOL as host interoperability. The rest of this chapter is written to keep those jobs from collapsing into one another.

<table class="book-table"><tr><th>Term</th><th>Question</th><th>Decision it unlocks</th></tr><tr><td>Characterization</td><td>How does it behave?</td><td>Model / derate / redesign before loaded work</td></tr><tr><td>Verification</td><td>Does it meet a stated requirement?</td><td>Pass / fail that requirement at a named plane</td></tr><tr><td>Validation</td><td>Does it work for intended system use?</td><td>Approve / restrict system claim</td></tr><tr><td>Qualification</td><td>Does it survive expected variation and life?</td><td>Accept / derate / hold life risk</td></tr><tr><td>Production test</td><td>Can we detect unacceptable units at volume?</td><td>Screen / sample / hold lot</td></tr><tr><td>ATP</td><td>Replayable accept/reject process?</td><td>Ship / fail unit or lot</td></tr></table>
The validation ladder in validation-workflow is the ordered way these jobs are sequenced so expensive evidence is not asked to answer the wrong question.

## The validation ladder

Validation is staged uncertainty reduction. Optical programs fail in the same places again and again: a part that looks good in characterization but cannot bring up on a production host, or a module that passes ATP and then unlocks under neighbor heat. Skipping a rung does not save time. It moves the escape into a later, more expensive stage.

### The canonical validation lifecycle

Validation is the process of building enough justified confidence to make a product decision. It is not a collection of measurements and it is not a synonym for qualification. A new optical product begins with several kinds of uncertainty at once. You may not know whether it integrates with the host, how its performance moves across operating corners, how much margin remains in a realistic system, whether aging creates permanent degradation, whether production can reproduce the engineering result, or whether laboratory assumptions remain true in the fleet.

Those questions cannot be answered by one large campaign. They require different evidence, and the evidence must be collected in a deliberate order. Each stage establishes the conditions needed to interpret the next one. A reliability result is not useful if the unit never operated correctly before stress. A clean characterization plot does not demonstrate interoperability with the target host. A qualified engineering build does not demonstrate that the supplier can reproduce the same distribution at volume.

The lifecycle therefore moves from basic operation toward increasingly realistic and increasingly expensive evidence. Requirements and architecture come first so you measure the right product; the story below starts once hardware exists.

##### Bring-up: establish an interpretable system.

The first task is not to measure maximum performance. It is to establish that the product can operate in a controlled environment and that later measurements will mean what you think they mean.

A module that does not reach the expected management state, emit light, recover timing, or pass data on a known-good host is not ready for characterization. At this point the leading uncertainty is integration: seating, power, firmware, fiber routing, configuration, host behavior, or an elementary product fault. Bring-up removes enough of that uncertainty to establish a trusted starting point.

The output of bring-up is therefore not "the product passed." It is a known configuration in which the module reaches ready state, produces and receives light, holds lock, and achieves a usable pre-FEC BER at named reference planes. That known-good configuration becomes the baseline for every later comparison. Now that operation is reproducible, you can study behavior.

##### Characterization: build the behavioral model.

A successful room-temperature link tells you very little about the operating envelope. Characterization maps how the product responds as temperature, voltage, optical return loss, lane, unit, and manufacturing lot change.

This stage is exploratory rather than purely pass/fail. The purpose is to understand distributions, sensitivities, and failure signatures. You want to know which margin ledgers are strong, which are thin, and which variables cause the response to move. Measurements such as OMA, TDECQ, wavelength, RIN, sensitivity, BER waterfalls, and control headroom are useful because together they reveal how the transmitter, channel, receiver, and control system respond to controlled changes.

Characterization produces a model of normal behavior. It tells you what varies, how quickly it varies, and which corners deserve deeper attention. It may lead to a design change or a restricted operating envelope before substantial qualification resources are spent. Characterization still studies the product largely as an isolated object. A product can look healthy in that environment and fail when placed inside the real system. Now that behavior is mapped, you can challenge it inside the system.

##### Margin and interoperability: test the product inside the system.

Margin validation asks how close the link is to failure. Interoperability asks whether the location of that failure boundary changes when the host, peer module, cable plant, firmware, thermal environment, and traffic conditions change.

These questions belong together because real systems combine impairments that are often separated on the bench. The module may experience hotter inlet air, live supply variation, adjacent-module heating, production fiber assemblies, optical reflections, host SerDes variation, management-state differences, and peer modules from another source. None of these conditions is necessarily severe by itself, but their combination may consume the remaining margin.

The purpose of this stage is not to repeat characterization with more test points. It is to challenge the behavioral model under production-representative conditions. If the model remains predictive and the required margin closes, the system corner can be approved. If it does not, the result may require a design change, a host restriction, a reduced environmental envelope, or a narrower interoperability claim. At the end of this stage you understand whether the product works today, across the intended systems and operating corners. You still do not know whether it will continue to work after prolonged exposure and aging. Now that present-day margin is understood, you can ask whether time changes it.

##### Stress qualification: determine whether time changes the answer.

Qualification introduces a different question: does exposure create permanent degradation that threatens the intended life?

Temperature sweeps during characterization show how a healthy product behaves while it is hot or cold. Reliability stresses ask whether temperature, humidity, cycling, operation, mating, or another mechanism causes the product to become permanently worse. That distinction is essential. A reversible operating-point shift is not the same problem as wear-out, fatigue, corrosion, contamination, or material degradation.

Stress selection must therefore begin with a credible failure mechanism. HTOL, temperature cycling, humidity, ESD, and connector cycling are not evidence merely because they were performed. Each stress must have a reason for being included, an observable degradation signature, an acceptance criterion, and a justified connection to the use condition or lifetime claim.

Qualification does not eliminate all life risk. It provides a bounded confidence argument for named mechanisms, samples, stresses, and assumptions. That argument supports a decision to accept the intended life, derate the use condition, gather more evidence, or hold release. Even a qualified design, however, may not be a manufacturable product. Now that design-life risk is bounded, you can ask whether production can reproduce the result.

##### Production readiness: prove repeatability and detection.

Qualification demonstrates that representative hardware can satisfy the design and life requirements. Production readiness asks whether the manufacturing process can reproduce that result across lots, tools, operators, suppliers, and time.

Engineering samples often receive unusual attention. They may use selected components, experienced technicians, extensive calibration, or bench measurements that cannot be repeated economically in production. Volume readiness therefore requires evidence from manufacturing distributions, not only from the best units.

This stage examines multi-lot yield, process stability, measurement-system correlation, ATP limits, guardbands, first-article evidence, and the ability of production screens to detect known escape mechanisms. The goal is not zero variation. The goal is controlled variation, with enough process capability and detection coverage to prevent unacceptable units from reaching the fleet. The decision is operational: open volume, restrict the ramp, improve the process or test coverage, or hold shipment. Production evidence still cannot reproduce every installation practice, rack environment, workload, and field interaction. Now that the process is controlled, deployment can test the remaining assumptions.

##### Controlled pilot and fleet monitoring: compare the model with reality.

A pilot is not merely a small production shipment. It is a controlled experiment designed to determine whether the assumptions made during validation and qualification remain true in deployment.

The pilot population should be identifiable, instrumented, and governed by explicit exit criteria. Telemetry should reveal whether BER, FEC behavior, retrains, temperature, optical power, lane behavior, and cohort rates match the expected distributions. Lot, site, host, firmware, and installation metadata matter because fleet evidence becomes useful only when failures can be grouped into meaningful populations.

If the observed behavior matches the model, deployment can expand while normal fleet monitoring continues. If it does not, the response may be to restrict a lot, pause a supplier, change installation controls, reopen qualification, modify ATP, or revise the design assumptions.

Fleet monitoring is part of validation rather than an activity that begins after validation is "finished." The fleet is where the remaining assumptions are tested. Its evidence closes the learning loop back into requirements, design, qualification, manufacturing controls, and future products.

##### Why the order matters.

The stages are ordered by the type of uncertainty they remove.

Bring-up establishes that measurements are interpretable. Characterization establishes the behavioral model. Margin and interoperability determine whether the model survives realistic system variation. Stress qualification determines whether time and exposure create permanent degradation. Production readiness determines whether the result can be reproduced and screened at volume. Pilot and fleet monitoring determine whether the laboratory model survives actual deployment.

A later stage cannot substitute for an incomplete earlier one. Interoperability testing cannot rescue unstable bring-up. HTOL cannot prove host compatibility. A qualified engineering lot cannot establish manufacturing control. A successful pilot cannot explain why the design works or guarantee that an uncontrolled factory will reproduce it.

The lifecycle is therefore not a bureaucratic sequence of gates. It is an efficient order for reducing uncertainty without asking expensive evidence to answer questions it was never designed to answer (tree-evidence-block, tree-qualification).

<table class="book-table"><tr><th>Stage</th><th>Question</th><th>Evidence</th><th>Decision</th></tr><tr><td>Requirements</td><td>What must be true?</td><td>System requirements, constraints</td><td>Architecture target</td></tr><tr><td>Architecture</td><td>Can this design meet requirements?</td><td>Budgets, simulations, tradeoffs</td><td>Proceed or redesign</td></tr><tr><td>Bring-up</td><td>Does the hardware fundamentally work?</td><td>Init, traffic, basic BER</td><td>Usable hardware</td></tr><tr><td>Characterization</td><td>How does it behave?</td><td>Sweeps, distributions, trends</td><td>Behavior understood</td></tr><tr><td>Margin</td><td>How close are the limits?</td><td>T, V, loss, ORL, stress headroom</td><td>Sufficient headroom</td></tr><tr><td>Interoperability</td><td>Does it work in real systems?</td><td>Host/peer/FW/channel matrix</td><td>Supported ecosystem</td></tr><tr><td>Qualification</td><td>Will it survive expected life?</td><td>Mechanism-based stress evidence</td><td>Release confidence</td></tr><tr><td>Manufacturing</td><td>Can we build it repeatedly?</td><td>Yield, ATP, SPC, FAIR</td><td>Production readiness</td></tr><tr><td>Pilot</td><td>Does reality match lab assumptions?</td><td>Bounded deployment</td><td>Expand / restrict / reject</td></tr><tr><td>Mass production</td><td>Can we sustain volume with control?</td><td>SPC, ECO, RMA loop</td><td>Open / hold volume</td></tr><tr><td>Fleet</td><td>Does it remain healthy?</td><td>Telemetry, cohorts, escapes</td><td>Operational control</td></tr><tr><td>Feedback</td><td>What must change next?</td><td>FA, escapes, revision inputs</td><td>Next-revision targets</td></tr></table>
**Table ?.** Canonical validation lifecycle (rapid reference). Decision unlocked: which stage exit you have evidence for, and which you do not. Wall-chart tree: tree-qualification; interview names: interview-validation-ladder. EVT/DVT/PVT/MP map in Table npi.

This is the single lifecycle. The operational notes below deepen each gate; they do not define a competing stage order. EVT/DVT/PVT names map in Table npi.

> **Why experienced engineers walk stages in this order?**
>
> Because each stage removes a different uncertainty. A late-stage pass cannot repair a missing requirement or unstable bring-up; treating HTOL as production readiness is the classic mix-up.

### Requirements definition

The first validation step is not a measurement. It is defining what success means so you do not validate the wrong product. Without a requirements slice you do not know which BER, envelope, lifetime, volume, or deployment environment later measurements must close. Write performance, environment, reliability, manufacturing, and operational requirement classes with owners and, where applicable, named planes (§1.6, Table laser-prd). Weak answer: "We test BER." Strong answer: first define target BER, operating envelope, lifetime, manufacturing volume, and deployment environment; then design validation around the risks.

**Representative evidence:** Signed requirements slice with owners, planes, and unambiguous pass/fail language.\
**Exit:** The slice is specific enough that architecture and later stages have pass criteria, or hardware work is refused until it is.\
**Decision:** Architecture target and validation scope, or hold until success is defined.

### Architecture review

Determine whether the architecture can meet the requirements before hardware exists. Validation starts on paper and in models (§1.6, Table laser-engineering-checklist). Even with clear requirements, optical power, thermal budget, electrical margin, reliability target, and manufacturing cost may not close together. Close budgets under stated assumptions, or redesign before buying tooling. A quiet-bench prototype is not architecture proof. Skipping reliability and manufacturing cost until DVT is a common failure mode.

**Representative evidence:** Closed or explicitly open budget lines; named assumptions; redesign triggers.\
**Exit:** Architecture is feasible under stated assumptions, or redesign is chosen before tooling.\
**Decision:** Proceed to hardware bring-up, or redesign.

### Engineering bring-up

Answer whether the hardware is alive and measurable. Bring-up is not qualification. Separate bench bring-up (trusted setup, interpretable measurements), system integration bring-up (target host init and traffic), and later margin/interop work. Before bring-up you do not know whether a failure is integration or product physics. Confirm emit, receive, CDR lock, and usable pre-FEC BER at named planes before arguing about margin or life (bringup, Table bringup-checklist). Deep FA before basic operation, or treating loaded chassis corners as bring-up exit evidence, wastes calendar.

> **Tradeoff.** Bring-up speed vs characterization depth
>
> *Improves:* Faster path into margin work
>
> *Worsens:* Missing baselines that make later BER tickets uninterpretable
>
> *When acceptable:* When the unit already links and emits in class on the target host
>
> *Experienced decision:* Do not skip characterization to "save time." Without a baseline, margin and FA burn calendar later.

**Representative evidence:** CMIS ready state; first-light and Rx power; CDR lock; usable pre-FEC BER on golden or target host at named planes.\
**Exit:** Unit reaches ready state, emits and receives light in class, holds lock, and shows usable pre-FEC BER with named reference planes.\
**Decision:** Continue into characterization, or stop and debug integration.

Now that operation is reproducible, you can study behavior.

### Characterization

Create the behavioral model. The output is not pass/fail. The output is how the system behaves. Characterization is exploratory: finding a cliff improves understanding; it does not automatically fail the product. Before this stage you know one corner works. After it you know how distributions move with stress variables and which ledgers (power, noise, timing, spectral, control) are thin. Map temperature, voltage, optical stress, and unit/lot distributions. On the transmitter path, measure TDECQ, OMA, ER, and level linearity; with component access, add LIV, RIN, and SMSR (tdecq, link-budget, laser-params). Do not treat a hero sample at $25^\circ$C as the fleet model, and do not park life projection inside characterization.

**Representative evidence:** Response surfaces; distribution summaries; thin-ledger list; candidate guardbands.\
**Exit:** Population behavior versus required corners is mapped, thin ledgers are named, and you decide whether derate or redesign is needed before loaded-fleet work.\
**Decision:** Proceed to margin validation, derate the envelope, or redesign.

Now that behavior is mapped, you can challenge it inside the system.

### Margin validation

A product does not fail because it reaches a nominal limit. It fails because all margins are consumed. Characterization maps the part; margin asks how much capability survives when temperature, voltage, loss, ORL, aging intent, and manufacturing variation stack under production-like stress (prod-corners, laser-margin-erosion). Compare pre-FEC BER, telemetry, retrain count, and control headroom against the characterization baseline. Track optical, electrical, thermal, reliability, and manufacturing margin categories separately, then stack once. Do not subtract the same physical effect twice under two names. Quiet-bench margin is not rack margin.

*Margin waterfall (illustrative accounting, not a universal budget).*

> Initial optical margin\
> $-$ temperature penalty\
> $-$ connector / plant loss\
> $-$ aging penalty\
> $-$ contamination / ORL penalty\
> $-$ manufacturing variation\
> $=$ remaining field margin

Allocate margin where uncertainty is highest (laser-margin-erosion).

**Representative evidence:** Cliff locations; remaining headroom by ledger; margin waterfall without double-counted penalties; loaded-corner results (Table prod-corners).\
**Exit:** Failure cliffs and remaining headroom are known at the named plane and loaded corners.\
**Decision:** Approve the fleet corner envelope, restrict deployment conditions, or send the design back.

### Interoperability validation

A component can pass validation and still fail as a system. Prove supported host, peer, firmware, and channel combinations retain required headroom. Margin on a golden host does not prove the supported ecosystem. Exercise host ASIC / SerDes, peer module or second source, firmware and CMIS revision, faceplate temperature and airflow, and fiber/cable plant. Assign failures to host, peer, software, environment, or channel before changing laser bias tables.

> **Tradeoff.** Golden-host speed vs interop risk
>
> *Improves:* Fast bring-up and clean debug on a known good station
>
> *Worsens:* Hidden host, firmware, or plant sensitivity until volume
>
> *When acceptable:* When golden-host data are a stage gate, not the exit criteria for the ecosystem
>
> *Experienced decision:* Use golden hosts for speed; require representative hosts before calling interop done.

**Representative evidence:** Supported combination list; documented restrictions; failing combination signatures.\
**Exit:** Supported host, peer, firmware, and channel combinations retain required headroom, or a documented restriction defines where the product may ship.\
**Decision:** Approve the supported ecosystem, restrict SKUs or hosts, or reopen design.

Now that present-day margin is understood, you can ask whether time changes it.

### Reliability qualification

Build mechanism-based evidence that the design survives expected variation and life. Do not run stresses only because a checklist names them. Keep operational environment test (works while exposed), reliability stress (exposure causes unacceptable permanent change), and life projection (justified field-life claim) distinct. Functional and margin stages do not answer lifetime (gr468, ic-reliability, tree-qual-evidence). Follow failure mechanism $\rightarrow$ acceleration method $\rightarrow$ stress $\rightarrow$ pre/post observable $\rightarrow$ acceptance criterion $\rightarrow$ confidence. A stress without a failure mechanism is only exposure. Deep FIT/DPPM math lives in Ch. reliability.

**Representative evidence:** Pre/post stress margins; mechanism notes; sample and confidence statement; production-proxy candidates.\
**Exit:** Sample plan, mechanism, and projected life support the requirements slice, or ship is explicitly held for life risk.\
**Decision:** Accept life risk for the envelope, derate life or use conditions, or hold.

Now that design-life risk is bounded, you can ask whether production can reproduce the result.

### Manufacturing validation

The factory is part of the design. Qualification proves the design. Manufacturing validation proves the process: build it repeatedly, measure it repeatedly, and detect bad units. A few carefully built engineering samples cannot establish volume readiness. This is the PVT question: whether yield, process control, and ATP coverage survive lot-to-lot variation (hvm-test, supplier-exec, Table npi). DVT belongs earlier; do not park it inside this stage. Prove ATP/sample/SPC coverage against known escapes with replay, separation, and production repeatability. Silent "multi-lot" that means two hand-selected lots is not evidence.

**Representative evidence:** Multi-lot yield; classified ATP/sample/SPC coverage; measurement capability; FAIR; escape-detection proof (tree-evidence-block, hvm-test).\
**Exit:** Multi-lot yield, screen coverage, SPC stability, and FAIR evidence support opening volume, or shipment is held for process control.\
**Decision:** Open volume toward pilot, hold shipment, or demand corrective action before ramp.

Now that the process is controlled, deployment can test the remaining assumptions.

### Controlled pilot

Validate assumptions in real deployment with a bounded population. Lab and factory evidence may still miss install practice, traffic mix, or environment. Use known serial numbers and lots, representative hosts, enhanced telemetry, and explicit success and rollback criteria (fleet-triage). Ask whether field reality matches lab assumptions. Calling open volume a pilot, or learning the escape from customer outage instead of a bounded trial, defeats the stage.

**Representative evidence:** Pilot cohort database; field BER/FEC and telemetry trends versus lab baselines; exit metrics.\
**Exit:** Pilot success/rollback criteria are met, or risk drives restrict or reject.\
**Decision:** Expand deployment, restrict, pause a supplier or lot, or reopen an earlier ladder stage.

### Mass production

Sustain volume with process control after pilot exit. Depth lives in Table npi, Ch. reliability. Pilot success does not prove ECO discipline, SPC stability, and RMA burn-down at volume. Hold or open volume based on control, not on hope that pilot luck continues.

**Representative evidence:** SPC trends; yield; RMA rates by code; ECO impact checks.\
**Exit:** SPC, ECO, and RMA loops support sustained volume, or volume is held.\
**Decision:** Open / hold volume; trigger supplier corrective action.

### Fleet monitoring

Validation does not end at shipment. Keep escapes and drift detectable after release (fleet-triage, Table fleet-triage). Unknown failure modes, aging, supplier drift, and environmental effects appear only at scale. Every telemetry field must answer what decision it enables. Trend and disagreement alarms catch dying units; hard thresholds catch dead ones. There is no terminal exit: ownership transfers into steady operations when schema, owners, and cohort baselines are in place.

**Representative evidence:** Schema-stable telemetry; cohort baselines; alarm history; RMA codes split by vendor and mechanism class.\
**Exit:** Ownership transfer into operations with schema, owners, and cohort baselines in place (ongoing control, not silence).\
**Decision:** Continue ship, restrict, pause a supplier or lot, or reopen an earlier ladder stage when cohort evidence falsifies a qual assumption.

### Feedback / next revision

Close the loop into the next requirements and architecture revision. Fleet and FA evidence that does not change the product is wasted. Separate one-off install errors from systematic design or process debt (§1.6). Fleet tickets that never become requirements, or fixes without screen changes, leave the next escape open.

**Representative evidence:** Revision backlog with owners: requirement changes, architecture changes, ATP updates, derates.\
**Exit:** Next-revision targets are written with owners, or residual risk is explicitly accepted without change.\
**Decision:** Next-revision targets, ATP updates, or documented accept risk.

### Which evidence class answers the uncertainty?

The lifecycle says *when*. This fork says *which class of evidence* to buy first for a named uncertainty:

<pre class="dectree" aria-label="New product uncertainty"><code>New product uncertainty
  |
What requirement is uncertain?
  |
Can simulation answer it?
  |-- YES --&gt; Model validation, then confirm critical assumptions later
  |-- NO  --&gt; Can bench measurement answer it?
              |-- YES --&gt; Characterization / margin measurement
              |-- NO  --&gt; Qualification stress
                          |
                          Field evidence (pilot / fleet) if lab cannot close it</code></pre>
Do not use this fork as a second lifecycle. Use it inside a stage when choosing between model, bench, stress, and field evidence.

> **Before open volume**
>
> Requirements $\cdot$ architecture $\cdot$ bring-up $\cdot$ characterization $\cdot$ margin $\cdot$ interop $\cdot$ qualification $\cdot$ manufacturing/ATP $\cdot$ pilot $\cdot$ fleet feedback (tree-checklists, Table ladder).

For every metric at every stage, state measurement, reference plane, condition, access level, and the decision unlocked (test-points, interview-access-levels, tree-evidence-block). Bad: "receiver sensitivity is $-15$ dBm." Good: sensitivity at the module optical input under the named BER target, temperature, wavelength, and FEC assumptions. A number without a plane and a method is not a measurement.

> **Engineering heuristic.** Name the reference plane before you name the instrument. A pretty eye at the wrong plane is a wrong answer.

## The core IM/DD measurements

Once the ladder is clear, the measurement list is organized around isolation: transmitter, channel, and receiver. That split is older than PAM4. Long before TDECQ, field engineers learned that a dark link can be a dead laser, a dirty connector, or a dead TIA, and that guessing which one burns hours. Bisecting those three domains is still how you keep debug from turning into simultaneous retunes of everything.

### Transmitter

Start with the light leaving the faceplate or the CPO fiber array. For PAM4, the headline metric is *TDECQ* (transmitter and dispersion eye closure quaternary): a reference equalizer is applied to the captured eye and the residual penalty is reported in dB (tdecq). Alongside it you read *OMA* (outer), extinction ratio, and *RLM* (level linearity), plus wavelength, spectral width, and RIN with a bias-driver versus feedback bisect (laser-params, laser-drivers, rin-values).

What else you add depends on the transmitter style. Laser-bearing modules need LIV, threshold, slope, SMSR, and chirp checks for DMLs (laser-params, dfb-eml). External MZMs (TFLN or silicon) need EO $S_{21}$, $V_\pi$, quadrature bias versus temperature, and driver-path eye symmetry at baud (simzm, tfln-mzm, tdecq). Microring banks need resonance alignment, thermal tuning, neighbor crosstalk, and peaking-network EO $S_{21}$ (siring, Ch. wdm). The point of the list is not completeness for its own sake: it is knowing which instrument answers which hypothesis when the eye closes.

### Channel

If the transmitter looks clean into a golden receiver and the link still fails, the channel is next. Insertion loss from fiber, connectors, MUX/de-MUX (wdm-hardware), and on-chip coupling (simzm, siring) is the first ledger line. Use the specified maximum loss for the exact connector class, number of interfaces, cleanliness condition, and reference plane; do not treat "1--3 dB per mated pair" as a universal normal loss. Chromatic dispersion (chirp-dispersion) matters more on FR-class SMF sweeps than on short DR links. Optical return loss (ORL) is the quiet killer: reflections can create optical feedback noise, multipath interference, deterministic distortion, and power-independent error floors. That is why many DR/FR modules still carry isolators while some CPO engines rely on design margin and monitor photodiodes instead (rin-values, Ch. lasers). Fiber attach (MPO/MTP, FAU, grating couplers) shows up as both yield and reliability (photonic-packaging).

### Receiver

Receiver work asks whether the front-end can still decide bits at the OMA that survives the channel. Measure sensitivity (minimum OMA for the named BER objective at a stated plane, pattern, and EQ) and stressed-receiver sensitivity with a calibrated stressor for margin (secq), plus overload before the TIA saturates. Underneath those system numbers sit the photodiode/TIA pair: responsivity, bandwidth, and input-referred noise (pd-tia, Ch. models).

### Link level

Only after Tx, channel, and Rx each look sane do you trust a full-link verdict: pre-FEC BER against the KP4 threshold (kp4), post-FEC BER, FEC symbol-error histograms, and a signed link-budget ledger from transmitter OMA to receiver sensitivity with penalties and remaining margin. That ledger is the document you argue from in DVT; the BER alone is not.

## Measurement mapping

The metrics above are scattered across Tx, channel, Rx, and link level because that is how you debug them. Table measurement-mapping collects the same metrics into one reference: what is measured, the instrument, why it matters, and the failure signature that points back to it. Use the chapter subsections for the debug logic; use this table to look up an instrument fast.

<table class="book-table"><tr><th>Metric</th><th>Instrument</th><th>Why it matters</th><th>Failure signature</th></tr><tr><td>OMA / TDECQ</td><td>DCA + reference equalizer</td><td>Scores transmitter quality against an ideal source; governs PAM4 acceptance (sec:tdecq)</td><td>TDECQ rises with no average-power change; points to bandwidth, RLM, or bias</td></tr><tr><td>Extinction ratio / RLM</td><td>DCA level histograms</td><td>Sets OMA at fixed average power (sec:sensitivity); poor RLM inflates TDECQ</td><td>Compressed inner eyes with passing average power</td></tr><tr><td>Wavelength / SMSR</td><td>OSA or wavemeter</td><td>Confirms grid placement and single-mode purity (sec:laser-params)</td><td>Side modes rise with T or age; line walks off grid</td></tr><tr><td>RIN</td><td>PD + ESA or dedicated RIN analyzer</td><td>Can create a power-independent BER floor when signal-proportional intensity noise dominates (sec:rin)</td><td>BER improves with power then flattens (a floor); not every floor is RIN</td></tr><tr><td>Insertion loss / ORL</td><td>Power meter + ORL meter</td><td>First ledger line; reflections can cause feedback noise, MPI, distortion, or floors (sec:optical-channel)</td><td>Burst or patterned errors with stable average power; ORL dependence</td></tr><tr><td>Receiver sensitivity</td><td>BERT + calibrated attenuator</td><td>Minimum OMA at target BER, the budget's bottom line (sec:sensitivity,sec:secq)</td><td>Waterfall shifts uniformly right without flooring</td></tr><tr><td>Pre-FEC BER / FEC histogram</td><td>BERT + FEC counters</td><td>The single number every other metric feeds; histogram shape reveals mechanism (sec:kp4)</td><td>Clustered errors point to bursts; sparse errors point to Gaussian noise margin</td></tr><tr><td>CMIS state / DDM</td><td>Host or CMIS tool</td><td>Confirms management layer before blaming optics (sec:cmis)</td><td>Module never reaches ModuleReady; DDM disagrees with bench truth</td></tr></table>
**Table ?.** Measurement mapping: metric, instrument, rationale, and failure signature in one reference. Row explanations follow; chapter subsections give the full treatment of each metric.

### Reading the measurement map

Use the table for lookup. Use the notes below when a metric is new, or when you need the decision the measurement unlocks.

##### OMA / TDECQ.

TDECQ asks how much worse this transmitter is than an ideal source after a reference equalizer. Outer OMA is the optical swing the receiver actually uses. Together they answer whether the Tx path still has signal-quality margin. **Exit when** TDECQ and OMA meet the PMD/ATP at the named pattern and temperature. **Decision:** continue, retune bias/equalization, or reject the transmitter path. **Risk if skipped:** you chase receiver noise while the eye was already out of budget.

##### Extinction ratio / RLM.

Extinction ratio and level separation mismatch (RLM) set how much OMA you get at fixed average power and how linear the PAM4 levels are. Poor RLM inflates TDECQ even when average power looks fine. **Exit when** ER/RLM meet the mask at the failing corner. **Decision:** retune modulator bias or driver, or accept a derate. **Risk if skipped:** average-power APC hides a collapsing outer eye.

##### Wavelength / SMSR.

Wavelength placement and side-mode suppression ask whether the spectral ledger still closes: on-grid for filters or rings, single-mode under temperature and age. **Exit when** the line sits in the allowed window with SMSR in spec. **Decision:** retune lock/thermal control, derate temperature, or replace the laser. **Risk if skipped:** BER failures get blamed on RIN when the line walked onto a filter edge.

##### RIN.

Relative intensity noise sets how far $Q$ can rise with power. Measure with a quiet bias path and under controlled ORL so you separate intrinsic laser noise from feedback. **Exit when** RIN at the stated ORL meets the budget. **Decision:** fix reflections/supply, replace the laser, or stop raising launch into a floor. **Risk if skipped:** you keep adding photons to a non-power-limited impairment (interview-waterfall).

##### Insertion loss / ORL.

Insertion loss is the first power-ledger line. ORL asks whether reflections are seeding RIN or bursts. **Exit when** loss and ORL are inside the plant assumptions used in the link budget. **Decision:** clean/replace connectors, add isolation, or reopen the budget. **Risk if skipped:** burst tickets look like random laser death.

##### Receiver sensitivity.

Sensitivity is the minimum OMA for the named BER objective at a stated plane, pattern, and EQ, the budget's bottom line. A parallel waterfall shift with no floor usually means the Rx path or channel loss changed. **Exit when** sensitivity meets the ledger with stated pattern and stress. **Decision:** golden-swap ownership, derate reach, or redesign Rx. **Risk if skipped:** Tx FA on an Rx-limited link.

##### Pre-FEC BER / FEC histogram.

Pre-FEC BER is the system score every other metric feeds. The FEC histogram shape separates sparse Gaussian-like errors from clustered bursts (MPI, intermittents, unlocked intervals). **Exit when** BER and histogram support the claimed mechanism class. **Decision:** contain, clean, retune, or open FA. **Risk if skipped:** average BER hides a bursty escape that ATP never stressed.

> **What this usually means.** BER waterfall floor that more launch power does not fix
>
> *Usually:* RIN, MPI, crosstalk, receiver saturation, or another non-power-limited impairment (interview-waterfall)
>
> *Not:* simple insertion loss that more photons will buy out

##### CMIS state / DDM.

Management state and digital diagnostics confirm the control and monitor path before you blame photons. Disagreement between digital diagnostics monitoring (DDM) and an external meter is itself a finding (monitor-PD or calibration). **Exit when** state progression and DDM match bench truth at the named plane. **Decision:** fix firmware/seat/power, or proceed to optics. **Risk if skipped:** weeks of optical FA on a module that never reached ready.

### Why this map is ordered by isolation

Transmitter metrics come before channel and receiver metrics because a bad Tx eye contaminates every downstream number. Channel loss and ORL come before Rx sensitivity arguments for the same reason. Link-level BER is last: it is the verdict, not the first bisect. If you start at BER alone, you still need this map to choose the next instrument.

## Transmitter and dispersion eye closure quaternary (TDECQ)

*TDECQ* (transmitter and dispersion eye closure quaternary) deserves a closer look because it is the metric that governs many PAM4 transmitter acceptance methods. It answers a specific question: *how much worse is this transmitter than an ideal one, after a realistic receiver has done what it can to clean up the signal?*

The following is a representative IEEE-style procedure. Use the exact clause and PMD under qualification for the reference receiver, equalizer constraints, histogram locations, and target error ratio.

### How it is measured

1.  **Capture.** The optical waveform is acquired on a sampling oscilloscope (a DCA) through a standardized reference receiver (often a fourth-order Bessel--Thomson filter near half the baud rate under the named PMD) so every lab measures the same bandwidth.

2.  **Equalize.** A defined *reference equalizer*, a *feed-forward equalizer* (FFE) with a small, bounded number of taps (commonly up to five in many PMDs), is applied. This models the modest equalization a real receiver would perform, so the transmitter is not penalized for *ISI* the system can remove anyway.

3.  **Histogram.** Narrow vertical histogram windows are placed inside the symbol at the positions required by the clause. The noise distribution is evaluated at the three PAM4 decision thresholds.

4.  **Compute.** The algorithm finds the RMS Gaussian noise $\sigma$ that, added to the equalized signal, would just reach the clause's target symbol error ratio (often near $4.8\times10^{-4}$ for KP4-class budgets). TDECQ is the ratio, in dB, of the noise an *ideal* transmitter could tolerate to the noise *this* transmitter can tolerate: $$\mathrm{TDECQ} = 10\log_{10}\!\left(\frac{\sigma_{\text{ideal}}}
            {\sigma_{\text{measured}}}\right).$$

A worse transmitter tolerates less added noise before failing, so $\sigma_{\text{measured}}$ shrinks and TDECQ rises. Lower is better; the numeric cap is PMD-specific.

### Related quantities and failure signatures

SECQ

: the stressed-eye counterpart used on the receiver side under a named PMD, adding a calibrated stressor to test margin rather than transmitter quality alone. Distinguish SECQ from a general stressed-receiver sensitivity test. See secq.

RLM (relative level mismatch)

: measures how evenly the four PAM4 levels are spaced; poor RLM (uneven levels) inflates TDECQ.

Because TDECQ folds several impairments into one number, the way it fails is diagnostic: uneven levels point to modulator or driver linearity (RLM); residual eye closure the equalizer cannot fix points to excess ISI or limited bandwidth; a noise-limited result points to low OMA, RIN, or reflections. For external MZMs (TFLN or silicon), also check EO $S_{21}$ bandwidth, $V_\pi$ and bias quadrature drift with temperature, and RF return loss on the driver-to-modulator path (simzm, tfln-mzm, siring). This is why *LPO*, which removes the module's own DSP, raises the stakes on transmitter quality: there is less downstream equalization to hide behind, so TDECQ-class metrics become even more central.

## SECQ and stressed-receiver testing

*SECQ* (stressed eye closure quaternary) mirrors TDECQ on the *receiver* for a named PMD and clause: instead of scoring transmitter quality with a reference equalizer, the test applies a calibrated optical stressor (attenuation, ISI template, optional RIN) and asks how much margin remains before the receiver hits that clause's target pre-FEC metric.

Stressed-receiver sensitivity and overload tests (sensitivity) use the same philosophy but are not automatically the same procedure as SECQ. Bracket the operating OMA range with impairments the link will see in the field, and name the PMD, FEC architecture, error model, metric, and test duration. For LPO, where the module DSP is gone, stressed Rx margin on the host-side receiver (equalization, conditioning) is as important as TDECQ on the transmitter.

## Instruments

A failing PAM4 link rarely announces which block is wrong. The bench is how you force the answer: each instrument isolates one failure mode, and the loopback topology tells you which side of the optical connector owns it.

DCA

: (digital communication analyzer): sampling scope for PAM4 eyes, TDECQ, OMA, RLM (tdecq). Needs a reference receiver filter matched to the PHY under test.

BERT

: bit-error ratio at pre- and post-FEC; FEC symbol histograms (kp4).

OSA / wavemeter

: wavelength, spectrum, SMSR, side modes, and linewidth where supported (Ch. lasers).

PD + ESA or dedicated RIN analyzer

: relative intensity-noise spectrum under a defined condition (rin-values).

VOA / stressor assembly

: calibrated attenuation and optional ISI for SECQ and sensitivity sweeps.

Power meter

: average power; pair with DCA for OMA.

Thermal chamber + TEC controller

: corner validation; essential for rings (siring, Ch. wdm) and laser grids.

Use electrical loopback (host SerDes), optical loopback (Tx$\to$Rx on module), and golden-host/golden-module interop to bisect faults (optical-channel). If the fault follows the module under golden-host swap, stop blaming the SerDes; if it stays with the host, stop opening laser FA.

## Building a link budget

A link budget is a signed dB (or power) ledger from transmitter to receiver. For IM/DD short reach, start from outer OMA at the Tx faceplate and subtract every loss and penalty until you compare against receiver sensitivity (with target BER and KP4 pre-FEC threshold, kp4, sensitivity).

<pre class="dectree" aria-label="Transmitter output (OMA)"><code>Transmitter output (OMA)
  |
Coupling loss
  |
Connector loss
  |
Fiber / waveguide loss
  |
Penalties (Method A or B; see below)
  |
Receiver input
  |
Sensitivity requirement
  |
Remaining margin</code></pre>
Keep power budget, signal-quality penalties, timing, thermal, and control authority as separate ledgers when the impairment is not a pure optical-power number (laser-margin-erosion, tree-margin-budget).

##### Design allocation versus validation measurement.

Distinguish margin allocation in design from margin verification in test. During design, engineers allocate transmitter output, receiver sensitivity, insertion loss, temperature degradation, aging, jitter, and manufacturing variation. During customer or system qualification, the integrator often measures net remaining margin across the operating envelope.

<pre class="dectree" aria-label="Design: allocate line items"><code>Design: allocate line items
  |
Build / integrate
  |
Test: measure net at named plane
  |
Room-T sensitivity margin
  |
Temperature / stress sweep
  |
Observed margin loss
  |
Remaining headroom
  |
Deployment decision</code></pre>
##### TDECQ accounting: two methods.

Method A --- Composite compliance

: Use the PMD's specified OMA/TDECQ relationship. Do not subtract TDECQ again as an independent link-budget penalty.

Method B --- Engineering decomposition

: Use a separate measured transmitter-quality penalty only when the accounting method is defined and does not duplicate the compliance limit.

##### Illustrative ledger (single-mode DR-class sketch).

Start from Tx OMA on the DCA (or from average power and ER) at a named plane. Subtract connector/coupling loss using the specified maximum for the connector class, interface count, and cleanliness (an illustrative poor or multi-interface allocation can land near 1--3 dB per mated pair; that is not a universal normal loss). Subtract fiber loss ($\sim$0.3--0.4 dB/km at 1310 nm; often negligible at 500 m) and MUX/de-MUX if WDM (2--5 dB per stage, wdm-hardware). Apply penalties with Method A or Method B above; add dispersion (chirp-dispersion) and reflection/MPI terms (optical-channel, rin-values) only when not already absorbed. Compare the remainder to stressed sensitivity at the *named* PMD's pre-FEC objective (for a KP4-class optical PMD under its random-error model, often near $2.4\times10^{-4}$; state FEC, metric, and test duration). Keep production margin appropriate to fleet corners. Numbers here are an illustrative DR-class sketch, not universal limits. Electrical budgets parallel this for the host-to-module path: COM and pre-FEC BER (com, eye-budget, equalization). LPO requires *both* ledgers to close without module DSP help.

## Module management: CMIS

##### Applicability header (fill for each program).

- Applicable CMIS revision:

- Applicable form factors:

- Applicable module states:

- Applicable data-path states:

- Optional diagnostics used:

- Vendor extensions permitted:

Do not imply that every CPO engine, ELSFP, pluggable, and future 448G implementation exposes identical CMIS behavior. Distinguish a standardized CMIS field, optional VDM, a vendor-specific diagnostic, and an inferred health metric.

### What CMIS is, and why an optical engineer cares

*CMIS* (Common Management Interface Specification) is the vendor-neutral management layer between a host (switch ASIC, NIC, or test fixture) and a pluggable or on-board optical module that implements it. The host talks to the module over a two-wire bus (TWI, I2C-like) through a paged register map: identity, power mode, alarms, per-lane monitors, and (in later revisions) link-training and host signal-integrity tuning extensions . Common form factors include QSFP-DD, OSFP, COBO, ELSFP, and some CPO engines that expose a CMIS contract.

You touch CMIS on every bring-up and every field triage. It is how the host learns what module is seated, when lasers may turn on, what Tx/Rx power and temperature look like, and whether a link failed at the management layer or the optical layer. A module that passes BER on a bench with lasers forced on but cannot reach ModuleReady on a production host will fail in the fleet (bringup).

### The module state machine

CMIS defines a module state machine the host drives. After presence detect and power application, the module stays in low power until the host releases `LPModeL` (or the CMIS 5.x `LowPwr` equivalent). The host reads identifier pages, clears sticky interrupts, and steps the module toward ModuleReady. Only then should Tx lanes or ELS lasers enable. ELSFP modules that emit before ModuleReady are a reject: the host did not authorize light (elsfp).

Data paths have their own state machines in CMIS 5.x (data path states, and network path states for media-side links). For bring-up, map the sequence in bringup onto these transitions: presence and Vcc, CMIS init and ModuleReady, enable light, optical path check, electrical lock, traffic, snapshot. Skipping step 2 and jumping to BER is how interop failures hide until production.

### The memory map: pages, monitors, control

The lower memory map holds module identity, status, interrupt flags, and alarm thresholds. Upper pages hold application descriptors, lane controls, tunable-laser support, versatile diagnostics (VDM), and command-data-block (CDB) firmware messaging . Hosts select an application (lane count, host interface, media type) before bringing up traffic.

*DDM* (digital diagnostic monitoring) is the telemetry layer you read at scale: per-lane Tx and Rx optical power, laser bias current when exposed, module temperature, supply voltage, LOS/LOL flags, and alarm/warning bits. On WDM parts you also get wavelength or channel ID. This is exactly what fleet-triage reads before anyone reaches for a DCA. On bring-up, dump the register map you will use in the field and treat that dump as the golden reference for later RMA comparisons.

### CMIS as a validation deliverable

CMIS correctness is part of production readiness, not a firmware afterthought. ATP should prove the state machine reaches ModuleReady across voltage and thermal corners; DDM monitors track bench truth (CMIS Tx power versus DCA, module temperature versus case $T$); alarms fire at the right thresholds; and firmware revision is ECO-controlled like laser die revision (supplier-exec). Multi-source interop failures are often CMIS, media-type, or firmware mismatches, not marginal TDECQ (bringup). At fleet scale the register map is the only eyes you have on a module in the rack. If CMIS is wrong, triage starts blind.

## Module and system bring-up

Characterization proves a sample can meet metrics on a quiet bench. Bring-up proves a module (then a system) can be powered, managed, and linked the way production and the fleet will actually run it. Lab-to-production programs fail in the gap between those two if you only ever test golden hosts, clean fiber, and room-temperature faceplates.

##### Module bring-up sequence.

Run this order on every new module (pluggable, ELSFP, or CPO engine with CMIS). Do not skip ahead to BER: a link that "works" with lasers forced on and CMIS ignored will fail the first host that enforces the state machine (elsfp).

1.  **Presence and power.** Detect module (`ModPrsL` or equivalent). Apply rails in the host power sequence. Confirm Vcc and module temperature in CMIS. Stay in low power (`LPModeL` asserted or ModuleLowPwr) until management is sane.

2.  **CMIS init.** Read identifier, vendor, firmware rev, supported media. Clear sticky interrupts. Confirm the state machine can reach ModuleReady (or the pluggable equivalent) under host command. Dump the register map you will use in the field; that dump is your bring-up golden reference.

3.  **Enable light.** Exit low power; enable Tx lanes / ELS lasers only after ModuleReady. Confirm Tx optical power and laser bias (if exposed) against the power class. Lasers that come up before the host asks are a reject for ELSFP (elsfp).

4.  **Optical path.** Mate fiber (clean first). Check Rx power and LOS. Optical loopback first if the host path is unproven.

5.  **Electrical lock.** Bring host SerDes / module CDR. Confirm LOL clear, equalizer taps not pegged (equalization). For LPO, this is the host eye and COM path (com, drivers).

6.  **Traffic.** PRBS or live FEC traffic. Pre-FEC BER vs. KP4 threshold (kp4); glance at FEC symbol-error histogram shape.

7.  **Quality snapshot.** On a Tx-capable path: OMA/RLM/TDECQ or module diagnostics that proxy them (tdecq). Record CMIS + BER + case $T$ together so later triage has a baseline (fleet-triage).

Table bringup-checklist is the short form you can put on a lab wall.

<table class="book-table"><tr><th>Step</th><th>Action</th><th>Pass signal</th><th>Fail first look</th></tr><tr><td>1</td><td>Presence / Vcc / temp</td><td>CMIS alive, rails in range</td><td>cable, seat, PSU</td></tr><tr><td>2</td><td>CMIS state machine</td><td>ModuleReady (or equiv.)</td><td>firmware, TWI, LPMode</td></tr><tr><td>3</td><td>Enable Tx / ELS</td><td>Tx power in class; lasers on only when commanded</td><td>bias driver, enable pin, APC</td></tr><tr><td>4</td><td>Fiber / Rx power</td><td>Rx power up; LOS clear</td><td>dirty MT, polarity, break</td></tr><tr><td>5</td><td>CDR / SerDes lock</td><td>LOL clear; taps not saturated</td><td>host SI, LPO COM, retimer</td></tr><tr><td>6</td><td>Pre-FEC BER</td><td>below KP4 target with margin</td><td>Tx quality, ORL, Rx sensitivity</td></tr><tr><td>7</td><td>Snapshot</td><td>CMIS dump + BER + T logged</td><td>(needed for RMA later)</td></tr></table>
**Table ?.** Module bring-up checklist. LOS = loss of signal; LOL = loss of lock. Limits come from the ATP and PMD, not from this table.

##### Production-representative corners.

Bench corners ($T$, $V$) are necessary and not sufficient. Chassis thermal, host rails, and ORL belong before Design Validation Test (DVT) exit on a representative unit. The full set in Table prod-corners belongs before Production Validation Test (PVT) exit (Table npi).

<table class="book-table"><tr><th>Corner</th><th>What to run</th><th>Why it catches</th><th>Points to</th></tr><tr><td>Chassis thermal</td><td>Module in target rack/sled at airflow and power load; not only a quiet chamber on a bench fixture</td><td>Faceplate T and TEC load differ from chamber setpoints</td><td>derate, TEC, ring unlock</td></tr><tr><td>Host rails live</td><td>Bias / CMIS powered from host supplies with SerDes traffic on</td><td>Switching noise into laser bias looks like RIN (sec:laser-drivers)</td><td>PSRR, ground, APC</td></tr><tr><td>Dirty fiber / ORL</td><td>Controlled contamination or ORL stress on MT/FAU; clean vs dirty BER</td><td>Field installs are not lab-clean; ORL raises RIN and bursts</td><td>connector, isolator, feedback</td></tr><tr><td>Cable plant</td><td>Production fiber length, MPO count, and bend radius</td><td>Extra loss and reflections eat margin the ledger assumed</td><td>link budget (sec:link-budget)</td></tr><tr><td>ELS hot-swap</td><td>Pull/replace ELSFP under traffic (or under controlled traffic stop per CMIS)</td><td>Service action the architecture promised (sec:elsfp)</td><td>state machine, mate cycles</td></tr><tr><td>Neighbor load</td><td>Adjacent modules/lanes at full traffic and max case T</td><td>Crosstalk, shared supply droop, thermal crosstalk on rings</td><td>WDM lock, SI, PSU</td></tr><tr><td>LPO / linear path</td><td>Host COM and pre-FEC BER without module DSP crutch</td><td>LPO fails here first (sec:224g-deploy,sec:com,sec:drivers)</td><td>host FIR, module linearity</td></tr><tr><td>Voltage corners</td><td>Host Vcc min/max with traffic</td><td>Brown-out and CMIS glitches</td><td>power design, ATP</td></tr></table>
**Table ?.** Production-representative corners. A quiet BERT at 25 $^\circ$C with pristine fiber is characterization, not production readiness.

### Reading the production-corner map

Quiet $T$/$V$ characterization maps the part. Table prod-corners asks whether that map survives rack, host, plant, and service abuse. Use the table for the full set. The notes below teach the two corners that most often fool a quiet bench; the rest are Exit/Decision only.

##### Chassis thermal (worked).

Chamber case-$T$ does not prove sled airflow or faceplate gradient. Run the module in the target rack at production load; log case $T$, TEC current, lock, and pre-FEC BER versus the chamber baseline. **Exit when** loaded thermal closes with margin or names a derate / TEC / unlock restriction. **Decision:** approve the envelope, restrict deployment, or redesign cooling. **Risk if skipped:** quiet-chamber passes unlock in the first dense tray.

##### LPO / linear path (worked).

Retimed modules hide host FIR and module linearity faults (224g-deploy, com, drivers). Run host COM and pre-FEC BER on the linear path. **Exit when** BER and COM meet targets on the production host, or LPO is rejected for that host class. **Decision:** approve LPO, force retimed optics, or redesign host FIR / module linearity. **Risk if skipped:** LPO ships on hope and fails on the production ASIC SerDes.

##### Other corners (retrieve from the table).

Host rails live

: **Exit when** BER and bias telemetry stay clean under host supplies with traffic. **Decision:** approve pairing or demand PSRR/ground work. **Risk:** chasing optical RIN for host noise.

Dirty fiber / ORL

: **Exit when** stressed-ORL BER meets the plant budget or forces isolator / cleaning rules. **Decision:** approve plant practice or tighten service. **Risk:** lab heroes fail the first dirty install.

Cable plant

: **Exit when** production fiber/MPO/bend closes the signed budget. **Decision:** approve plant or cut reach. **Risk:** budget fiction on long MPO chains.

ELS hot-swap

: **Exit when** swap recovers to ready and BER, or service is restricted (elsfp). **Decision:** approve field replace or forbid hot-swap. **Risk:** service story fails the first maintenance window.

Neighbor load

: **Exit when** full-traffic neighbors close lock and BER. **Decision:** approve dense packing or derate. **Risk:** single-module DVT passes; tray bring-up fails.

Voltage corners

: **Exit when** host Vcc min/max holds CMIS and BER. **Decision:** approve envelope or tighten ATP. **Risk:** brown-outs look like firmware bugs.

### Why these corners come after quiet characterization

Chassis thermal, host rails, and ORL are the minimum before DVT exit on a representative unit. The full set belongs before PVT exit (Table npi). Later fleet monitoring must not invent coverage these corners never ran.

### Learning summary

Before DVT

: Chassis thermal, host rails, and ORL on a representative unit.

Before PVT

: Full Table prod-corners set, including LPO if claimed.

Each corner

: Exit when the claim closes or a restriction is named.

##### System bring-up.

> **Tradeoff.** Best laboratory performance vs production yield
>
> *Improves:* Hero samples that win bench demos
>
> *Worsens:* Tighter tolerances, harder calibration, and escapes in volume
>
> *When acceptable:* When the manufacturable design still meets the system requirement with guardband
>
> *Experienced decision:* Optimize the system and the yield story, not the best component on a quiet bench.

A module that passes on a golden host can still fail in a real chassis:

- **Host path:** run the same sequence on the target NIC/switch ASIC SerDes, not only the lab BERT. LPO and half-retimed modules expose host FIR/CTLE mistakes that a retimed module hid (conditioning, pluggables).

- **Multi-lane / multi-module:** bring all lanes on a port, then neighbors in the same cage or tray. Watch thermal rise, supply droop, and CMIS temp alarms when the tray is loaded.

- **Golden swap:** known-good module in the suspect host slot, then suspect module in a known-good slot. That single swap splits host vs. module before you open FA (fleet-triage).

- **Interop:** at least one other vendor host or module if the program claims multi-source. Interop failures are usually CMIS, media type, or electrical eye, not laser physics.

- **ELS / CPO:** external laser modules add a second bring-up: ELSFP state machine and optical mate to the engine, then engine bring-up with light present (elsfp, cpo-status). A dark engine with a healthy ELS is an optical connector or FAU problem until proven otherwise.

##### Exit criteria before "bring-up done."

Call *bench bring-up* done when CMIS state machine and enable sequence are correct, the unit emits and receives light in class, CDR locks, pre-FEC BER is usable on a trusted setup at a named plane, and a CMIS+BER+$T$ snapshot is filed. Call *system integration bring-up* done when the same sequence closes on the target host, golden-swap has split host vs. module issues, and multi-lane / neighbor load has not opened a new basic failure mode. Do *not* require loaded chassis-thermal / host-rail / ORL margin closure to declare bring-up done; that is Stage 3 margin and interop evidence (ladder-margin, ladder-interop, Table prod-corners). Everything after bring-up is characterization depth, margin/interop, supplier gates (supplier-exec), or fleet triage (fleet-triage).

**Key idea.** Bring-up is a sequence (presence $\to$ CMIS $\to$ light $\to$ lock $\to$ BER $\to$ snapshot), then a system proof on the real host. Production-representative corners prove remaining headroom; they do not redefine bench bring-up. A quiet bench pass is not DVT.

## The debug mindset

Debug at this level is data-driven, not opinion-driven. The method is disciplined bisection: change one domain at a time, and let the measurement tell you whether the transmitter, the channel, or the receiver moved.

1.  Isolate transmitter versus channel versus receiver, using loopbacks.

2.  Sweep temperature and voltage to expose corner-dependent failures.

3.  Correlate failures to DSP equalizer tap values (equalization) and FEC symbol-error statistics (kp4); these tell you *how* the link fails.

The third step is where modern PAM4 links differ from older eye-mask work. Tap saturation and FEC histograms often reveal the failure mode before a single waveform screenshot does. Treat those as primary evidence, not as afterthoughts logged once BER already fails.

[^17]

## The debugging fork in validation

Apply the debugging fork (debug-fork) before sweeping parameters or changing firmware: check the power meter or CMIS Rx power monitor first. If power moved, the fault is in the optical path (laser, coupling, connector, fiber, MUX); if power held but BER or TDECQ worsened, it is signal quality (bandwidth, noise, jitter, bias, equalization, reflection). This one check prevents the most common validation mistake: retuning an equalizer or laser bias when the real cause is a dirty connector. Then check which margin ledger moved (laser-margin-erosion) before descending to component physics.

> **Why experienced engineers separate power from quality first?**
>
> Because average optical power is cheap to measure and rules out gross attenuation, but it says almost nothing about timing, noise, distortion, spectral alignment, or adaptation.

> **What this usually means.** Stable average power with rising BER
>
> *Usually:* timing, adaptation, noise, spectral alignment, or intermittent control
>
> *Not:* gross attenuation or a simple dirty connector as the whole story

> **Engineering heuristic.** Never spend an hour on a DCA or spectrum sweep when a five-minute golden swap or attenuator step can eliminate half the tree.

<pre class="dectree" aria-label="Observation"><code>Observation
  |
Possible ledgers (power / noise / timing / spectrum / control)
  |
Measurements (power first)
  |
Hypotheses removed
  |
Decision
  |
Recurrence control</code></pre>
> **Before debugging**
>
> Scope $\cdot$ time behavior $\cdot$ population $\cdot$ power or quality $\cdot$ highest-value measurement $\cdot$ decision $\cdot$ recurrence control (tree-checklists).

> **Engineering heuristic.** A passing BER on a golden host is not production readiness. Interop, margin, and manufacturing control still have their own questions.

## Fleet and field triage

Lab debug asks: *what is broken on this unit?* Fleet triage asks: *which bucket does this failure belong in, and who owns the fix?* Optical programs at fleet scale own that split across performance, reliability, and manufacturability. Wrong bucket wastes weeks (sending a contaminated connector to laser FA, or rewriting a SerDes FIR when the laser is rolling over).

> **Engineering heuristic.** Contain the population and clear the measurement system before you open supplier FA. A wrong ticket burns calendar time you cannot get back.

> **What this usually means.** Temperature-only failures that recover cool
>
> *Usually:* thermal margin, wavelength or lock drift, bias tables, receiver noise rise, or mechanics that move with case temperature
>
> *Not:* a permanent wear-out mechanism already proven by ship LIV alone

> **Tradeoff.** More telemetry vs operational complexity
>
> *Improves:* Faster fleet debug, better cohort plots, earlier prediction
>
> *Worsens:* Firmware cost, storage, and interpretation burden
>
> *When acceptable:* When each new field answers a named decision
>
> *Experienced decision:* Every telemetry field needs an owner and a decision it enables. Otherwise it is noise.

##### Three buckets.

Classify every field issue before deep root-cause work:

Performance

: the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (tdecq, com, siring).

Reliability

: the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (wearout-modes, laser-aging, gr468, elsfp).

Manufacturability

: a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (supplier-exec, photonic-packaging).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label. Ch. failure-modes expands the same method into symptom-led bench and fleet procedures.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; elsfp).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (kp4), equalizer tap saturation (equalization).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $\to$ bucket).

Table fleet-triage is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

<pre class="dectree" aria-label="Fleet symptom"><code>Fleet symptom
  |
Scope analysis (how large?)
  |
Technical isolation
  |
Correlation analysis (which cohort?)
  |
Bucket: performance / reliability / manufacturability
  |
Contain / FA / ATP / telemetry
  |
Fleet monitoring</code></pre>
Scope sets severity and priors. Correlation after isolation unlocks contain, pause, replace, or supplier escalate (tree-scope-population).

<table class="book-table"><tr><th>Symptom</th><th>First telemetry check</th><th>Bucket</th><th>Confirm on bench / FA</th><th>Typical fix owner</th></tr><tr><td>Link never comes up (fresh install)</td><td>CMIS presence, Vcc, Tx power flatline, LOS</td><td>Mfg or install</td><td>Visual fiber/connector; golden module swap; CMIS dump</td><td>Ops install; supplier ATP if lot-correlated</td></tr><tr><td>Intermittent LOS / burst errors</td><td>Rx power dropouts; FEC bursts; ORL events</td><td>Perf (ORL) or mfg (contam.)</td><td>Clean/inspect MT; ORL meter; RIN vs ORL (sec:laser-drivers,sec:rin-values)</td><td>Ops cleaning; packaging if repeat RMA</td></tr><tr><td>Pre-FEC BER high, power OK</td><td>Tap saturation; RLM/TDECQ if logged; case T</td><td>Perf</td><td>DCA TDECQ/RLM; host COM; LPO vs retimed path (sec:tdecq,sec:com)</td><td>Host SI / module Tx design</td></tr><tr><td>BER rises only at high case T</td><td>Module temp alarm; Tx power drop; walk</td><td>Perf or reliability</td><td>LIV at T; OSA grid; TEC current; EAM bias (sec:laser-aging)</td><td>Derate / TEC / laser supplier</td></tr><tr><td>Slow BER creep over weeks/months</td><td>Bias current up for same Tx power; SMSR if monitored</td><td>Reliability</td><td>LIV/SMSR vs ship ATP; Arrhenius lot history</td><td>Laser wear-out; ELS replace</td></tr><tr><td>Sudden hard fail, was healthy</td><td>Last good CMIS snapshot; neighbor links OK</td><td>Reliability (COD) or mfg (ESD)</td><td>Dark LIV; DPA on facet/solder; date-code cluster?</td><td>FA + supplier 8D</td></tr><tr><td>One date code / site fails early</td><td>Lot Pareto; burn-in escape rate</td><td>Mfg</td><td>Incoming SPC vs ATP; FA on sample of lot</td><td>Supplier CAPA; hold shipment</td></tr><tr><td>WDM / ring unlock, power OK</td><td>Channel ID; thermal of neighbors; lock-loop status</td><td>Perf</td><td>Resonance tune; crosstalk; CW-WDM line power (sec:lock-validation,sec:thermal-xtalk,sec:cwwdm-laser)</td><td>Lock firmware / thermal design</td></tr><tr><td>ELSFP swap restores link</td><td>Old module CMIS vs new; connector cycles</td><td>Reliability or mfg (connector)</td><td>Inspect MT; mating-cycle count; laser LIV in returned module (sec:elsfp)</td><td>Laser vs connector split in FA</td></tr></table>
**Table ?.** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $=$ performance (design/operating point); reliability $=$ time-dependent wear; mfg $=$ lot/process/install excursion. Row notes follow.

### Reading the fleet triage map

Each row is a provisional route, not a confirmed root cause. Capture telemetry first. Confirm with the smallest measurement that can falsify the bucket. Then assign an owner.

##### Link never comes up (fresh install).

Ask whether the part is seated, powered, and managed before you open laser FA. CMIS presence, supply rails, Tx power flatline, and loss-of-signal (LOS) split install from product. Confirm with visual fiber/connector checks, a golden module swap, and a frozen CMIS dump. **Decision:** ops fix, or supplier ATP if the fail tracks a lot. **Risk if skipped:** manufacturing escapes get filed as design defects.

##### Intermittent LOS / burst errors.

Ask whether the plant is reflecting or contaminating. Rx power dropouts and bursty FEC histograms point at connectors or ORL before intrinsic RIN. Confirm with inspect/clean, ORL meter, and RIN versus ORL. **Decision:** cleaning discipline or packaging FA if RMAs repeat. **Risk if skipped:** burst tickets become endless laser replacements.

##### Pre-FEC BER high, power OK.

Power held, so leave the power ledger. Tap saturation, logged TDECQ/RLM, and case temperature point at signal quality or host SI. Confirm on a DCA and with host channel operating margin (COM) thinking on linear paths. **Decision:** host SI, module Tx design, or retune. **Risk if skipped:** you reseat fiber forever on a quality-path fail.

##### BER rises only at high case $T$.

Ask whether the operating point or the device changed with heat. Telemetry for temp alarms, Tx sag, and wavelength walk comes first. Confirm with LIV at temperature, OSA, TEC/heater codes, and modulator bias. Cool-down recovery raises $P(\mathrm{operating\ point})$; permanent shift raises $P(\mathrm{aging})$. **Decision:** derate, thermal design, or supplier life action. **Risk if skipped:** ambient-only debug misses the spent control ledger.

##### Slow BER creep over weeks/months.

Ask whether wear-out is spending the noise or power ledger. Bias current rising at fixed Tx power raises $P(\mathrm{aging})$. Confirm against ship ATP baselines (LIV, SMSR, power, spectrum) and lot history; recovery after recalibration raises $P(\mathrm{control/cal})$ instead. **Decision:** replace, derate, or update burn-in. **Risk if skipped:** FIT models stay optimistic until the fleet teaches you.

##### Sudden hard fail, was healthy.

Ask whether the event is catastrophic optical damage, ESD, or a shared infrastructure hit. Neighbor links and the last good CMIS snapshot matter. Confirm with dark LIV and physical FA; check date-code clusters. **Decision:** FA plus supplier 8D, or infrastructure fix. **Risk if skipped:** one COD event becomes a false process CAPA.

##### One date code / site fails early.

Ask whether this is a manufacturing subpopulation. Lot Pareto and burn-in escape rate are the first cuts. Confirm incoming SPC versus ATP and FA on a sample. **Decision:** quarantine, CAPA, hold shipment. **Risk if skipped:** a bad lot keeps deploying while FA studies one unit.

##### WDM / ring unlock, power OK.

Ask whether the spectral or lock ledger was spent while average power looked fine. Channel ID, neighbor thermal, and lock-loop status are the telemetry. Confirm resonance tune, crosstalk, and line power. **Decision:** lock firmware or thermal design. **Risk if skipped:** unlocks get mislabeled as random BER.

##### ELSFP swap restores link.

Ask whether the external laser, the connector, or the engine owned the fail. Compare old versus new CMIS and connector cycles. Confirm MT inspect and LIV on the returned module. **Decision:** split RMA codes for laser versus connector. **Risk if skipped:** FIT burns down the wrong wear-out mode (elsfp).

### Why triage order matters

Scope before mechanism. Telemetry before destructive FA. Bucket before owner. Confirm before CAPA. Closing the loop into ATP is part of the incident, not optional paperwork. Reversing that order produces NFF piles and merged RMA codes that make life models dishonest.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $T$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with Table fleet-triage. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (laser-aging, fit-example).

    - Manufacturability: quarantine lot, incoming hold, supplier 8D with DPA photos and ATP deltas (supplier-exec).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Worked paths (three common tickets).

*"High temp only."* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate). A permanent LIV or spectrum shift at temperature that matches an aged lot raises $P(\mathrm{aging})$ and justifies moving the ticket toward reliability; cool-down recovery without baseline shift keeps it in performance. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (siring, Ch. wdm).

*"Random burst errors, average power fine."* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, treat feedback/ORL as the leading performance hypothesis until confirmed. If ORL is fine and bursts track a date code, treat intermittent fiber attach as the leading manufacturing hypothesis. If bursts grow over months at fixed ORL, suspect laser or driver aging (laser-drivers, laser-aging).

*"ELSFP replace fixed it; returned module looks alive on the bench."* Alive LIV with high ORL sensitivity or a dirty MT face supports connector/ORL over laser wear-out; confirm with IL/ORL and recurrence. Dead or kinked LIV supports a reliability path. Split those RMA codes or FIT math blames the wrong mode (elsfp, photonic-packaging).

##### RMA labels that keep FIT honest.

RMA codes should be distinct, not a single "optics fail":

- laser wear-out (LIV/SMSR/EAM baselines support aging; not proof alone);

- COD / sudden dark;

- connector / contamination / ORL;

- fiber attach / FAU;

- driver / bias electronics;

- host / SerDes / LPO eye (not module);

- NFF (no-fault-found; track these; high NFF means bad triage).

NFF rate and lot Pareto are as important as FIT. A rising NFF with clean LIV points at install practice or intermittent connectors, not Arrhenius.

## Engineering lens

### How it works

Validation is a chain of evidence, not a single pass: a number means nothing without its reference plane, its corner, and its method. The chapter's ladder, instruments, and triage tree are that evidence chain from bench to fleet.

### How it is measured

Use the least complex instrument that can falsify the current hypothesis. Table measurement-mapping maps every key metric to its instrument, rationale, and failure signature in one lookup; the bring-up sequence (bringup, prod-corners) orders those instruments into a workflow.

### How it fails

Validation fails when the setup, sample, or acceptance rule does not match the product. Common misses are a stale calibration, the wrong reference plane, a golden host that hides interop risk, pristine fiber that hides ORL sensitivity, short BER dwell, one lane tested without neighbors, and chamber temperature used as a substitute for measured case temperature. These are test escapes even when the device physics is sound.

\> \*\*Failure mode: Low optical power\*\* \> \> \*\*Symptoms.\*\* A lane is dark or below its launch-power limit. \> \> \*\*Likely causes.\*\* A laser or enable fault, coupling loss, connector contamination, fiber polarity, calibration error, or a power-meter setup mistake. \> \> \*\*Measurements.\*\* Known source and meter, inspection scope, CMIS state and bias, power at successive planes, and a golden fiber or module. \> \> \*\*Mitigations.\*\* Correct the setup first, then repair the failing source, attach, connector, or control path. Add the signature at the earliest production test that can catch it.

### How it is debugged

Preserve the failing state and record software, firmware, calibration, fixture, cables, temperature, and supply. Verify the meter with a known source. Walk from power to spectrum to waveform to BER, moving one reference plane at a time. Use a golden swap to split host, module, and fiber. Only then stress temperature, voltage, ORL, and neighbors. Every corrective action needs a repeated failing test, a repeated passing test, and a guard against recurrence in ATP or telemetry.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* A new module lot showed low optical power on one station. \> \> \*\*Investigation.\*\* The same units passed on a second station. A known source exposed an offset in the first power-meter path. \> \> \*\*Finding.\*\* The lot was good, and the station was reading low. \> \> \*\*Root cause.\*\* A reference jumper had been replaced without updating the path-loss calibration. \> \> \*\*Resolution.\*\* The station was recalibrated, jumper identity was placed under change control, and a start-of- shift source check was added.

## Interview takeaway

**Key idea.** Validation is a chain of evidence. Start with calibrated power and management state, move through spectrum and waveform, then trust BER only after the blocks and reference planes are known. Run the target host, chassis, fiber, and neighbor corners before calling the product ready.

Junior mistake: call a golden-host BER pass "production ready," or open supplier FA before clearing the tester (Table ladder, Ch. reliability, app:decision-trees).

##### Three questions to test yourself.

1.  Why is a passing BER on a golden bench not sufficient for production readiness?

2.  BER is high but optical power looks fine. Apply the debugging fork (validation-fork): what do you check next?

3.  How do you detect tester drift before it becomes a yield cliff or a field escape?


<div class="nav-links">
  <a href="ch6-wdm-and-wavelength-locked-lasers">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch8-reliability-and-manufacturing-at-scale">Next &rarr;</a>
</div>
