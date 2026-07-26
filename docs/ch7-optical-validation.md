---
layout: default
title: "Ch 7: Optical validation"
---

# 7 Optical validation

*Read first:* validation lifecycle prose; bring-up; core measurements; CMIS sequence; production-like corners; fleet triage.

*Deep dive:* instrument theory of operation; Method A/B link-budget accounting; CMIS register map detail.

*Reference:* job definitions table, ladder Stage/Question/Evidence/Decision table, bring-up checklist, corner checklist.

A datasheet that closes on a quiet bench is not a product. A quiet-bench close proves one corner under one setup. It does not prove that the link meets its requirements across the temperatures, hosts, connectors, production spread, and lifetime the fleet will actually see.

*Validation* is the process of building enough justified confidence to make those product decisions. Passing tests is an output, not the purpose. The job is to remove the uncertainty that blocks the next call: continue, redesign, derate, qualify, open volume, or hold. Debugging asks which margin ledger was exhausted. Qualification asks how much margin remains after the expected stresses. Both are uncertainty reduction that ends in a decision (Appendix D, Appendix D.16). This chapter sequences that work from a single device to a deployed fleet (§7.1), then covers bring-up under production-like corners and the hypothesis-driven debug method the work demands.

Companies overload EVT, DVT, PVT, and "verification" differently. Unless noted otherwise, this book freezes meanings by *job*, not by org chart. Abbreviations are collected in Appendix G.

##### How the jobs differ.

*Characterization* maps how the design behaves. It discovers distributions, sensitivities, and cliffs. A characterization cliff improves understanding; it does not automatically fail the product. BER versus temperature, wavelength drift, receiver sensitivity, RIN, and bias trends belong here when the question is still "what happens when you change $X$?"

*Verification* asks a narrower question: does this implementation meet a stated requirement with a named method and reference plane? Transmit power, BER at a stated FEC objective, wavelength accuracy, and thermal operating range are verification when the requirement, plane, and method are already frozen.

*Validation* asks whether the product works for the intended customer and system use. Hosts, cable plant, temperatures, workloads, and install practice are in scope. A verified BER on a golden bench is not validation of the fleet claim.

*Qualification* asks whether you have evidence the design survives expected variation and life. The evidence is mechanism-based stress and sample humility, not a ritual checklist. HTOL, temperature cycling, humidity, and multi-lot process corners matter only when each stress maps to a named mechanism and an acceptance rule.

*Production test* asks whether you can repeatedly detect unacceptable units at volume. Factory and incoming screens catch escapes; they do not prove life. *ATP* (acceptance test) is one form of that process: a replayable accept/reject decision applied per unit, per lot, or by a documented sampling plan.

##### One module, five jobs.

Take a temperature BER sweep on a new EML module. Mapping BER versus case temperature to find cliffs is characterization. Checking that BER stays below the frozen FEC objective at the named plane and method is verification. Running that check on the production host, cable plant, and install practice is validation. Running HTOL or humidity on a sample lot to bound life for a named mechanism is qualification. Running a fast lot screen for power, CMIS, and a sampled TDECQ row is production test. Same hardware, five different questions.

The split matters because the classic program failures are category errors: treating characterization cliffs as automatic product failure, treating ATP as life proof, or treating HTOL as host interoperability. The rest of this chapter is written to keep those jobs from collapsing into one another.

<table class="book-table"><tr><th>Term</th><th>Question</th><th>Decision it unlocks</th></tr><tr><td>Characterization</td><td>How does it behave?</td><td>Model / derate / redesign before loaded work</td></tr><tr><td>Verification</td><td>Does it meet a stated requirement?</td><td>Pass / fail that requirement at a named plane</td></tr><tr><td>Validation</td><td>Does it work for intended system use?</td><td>Approve / restrict system claim</td></tr><tr><td>Qualification</td><td>Does it survive expected variation and life?</td><td>Accept / derate / hold life risk</td></tr><tr><td>Production test</td><td>Can we detect unacceptable units at volume?</td><td>Screen / sample / hold lot</td></tr><tr><td>ATP</td><td>Replayable accept/reject process?</td><td>Ship / fail unit or lot</td></tr></table>
The validation flow in §7.1 is the ordered way these jobs are sequenced so expensive evidence is not asked to answer the wrong question.

## The validation flow

### One lifecycle, beginning before hardware

Validation does not begin when a module reaches the bench. It begins when the team decides what the product must accomplish and whether the proposed architecture can plausibly accomplish it. Requirements define success. Architecture work determines whether optical power, noise, thermal, electrical, reliability, manufacturing, and service assumptions can close together before tooling and hardware make changes expensive.

Once hardware exists, the nature of the uncertainty changes. Bring-up establishes that the unit is alive, configured correctly, and measurable. Characterization then builds the behavioral model: how performance moves with temperature, voltage, optical loss, reflections, lane, unit, and lot. These steps are deliberately separate. A module that links once is not characterized, and a detailed characterization sweep is difficult to interpret when basic operation is unstable.

Margin and interoperability place that behavioral model inside the intended system. The question is no longer merely how the module behaves in isolation, but whether enough headroom remains across supported hosts, peers, firmware, cable plants, thermal loading, and operating corners. This is where the team defines the real shipping envelope.

Reliability qualification asks a different question: whether time, stress, and environmental exposure cause permanent degradation. Manufacturing validation then asks whether the qualified result can be reproduced across lots, tools, suppliers, and production measurements. Qualification supports confidence in the design; manufacturing validation supports confidence in the process.

A controlled pilot tests the remaining assumptions in a bounded field population. Mass production scales only after the pilot exit is justified and the production controls are operating. Fleet monitoring continues because deployment can reveal mechanisms, interactions, and population effects that no laboratory campaign completely predicts. Those findings must flow back into the next requirements, architecture, qualification plan, ATP, supplier control, or service procedure.

This is one lifecycle. Simulation, bench measurement, qualification stress, and field evidence are not competing paths. They are different evidence sources selected within the appropriate step (Appendix D.16, Appendix D.2).

> **Why experienced engineers walk steps in this order?**
>
> Because each step removes a different uncertainty. A late-step pass cannot repair a missing requirement or unstable bring-up; treating HTOL as production readiness is the classic mix-up.

### Step 1: Define the requirements

The first validation step is not a measurement. It is defining what success means so you do not validate the wrong product. Without a requirements slice you do not know which BER, envelope, lifetime, volume, or deployment environment later measurements must close.

Write performance, environment, reliability, manufacturing, and operational requirement classes with owners and, where applicable, named planes (§1.1, Table 5.4). Weak answer: "We test BER." Strong answer: first define target BER, operating envelope, lifetime, manufacturing volume, and deployment environment; then design validation around the risks. The evidence here is a signed contract, not a bench plot.

**Representative evidence:** Signed requirements slice with owners, planes, and unambiguous pass/fail language.\
**Exit:** The slice is specific enough that architecture and later steps have pass criteria, or hardware work is refused until it is.\
**Decision:** Architecture target and validation scope, or hold until success is defined.\
**Interview trap:** Jumping to instruments before success criteria exist.

Once success is defined, the team can determine whether any architecture can meet it.

### Step 2: Review the architecture

Determine whether the architecture can meet the requirements before hardware exists. Validation starts on paper and in models (§1.1, Table 5.9). Even with clear requirements, optical power, thermal budget, electrical margin, reliability target, and manufacturing cost may not close together.

Close budgets under stated assumptions, or redesign before buying tooling. A quiet-bench prototype is not architecture proof. Simulation and paper budgets are Step 2 evidence when assumptions are named and later checkable; they do not replace later steps.

**Representative evidence:** Closed or explicitly open budget lines; named assumptions; redesign triggers.\
**Exit:** Architecture is feasible under stated assumptions, or redesign is chosen before tooling.\
**Decision:** Proceed to hardware bring-up, or redesign.\
**Interview trap:** Skipping reliability and manufacturing cost until DVT.

Once the important budgets close under stated assumptions, hardware work has a defensible target.

### Step 3: Bring up the hardware

Answer whether the hardware is alive and measurable. Bring-up is not qualification. Separate bench bring-up (trusted setup, interpretable measurements), system integration bring-up (target host init and traffic), and later margin/interop work. Before bring-up you do not know whether a failure is integration or product physics.

Confirm emit, receive, CDR lock, and usable pre-FEC BER at named planes before arguing about margin or life (§7.9, Table 7.4). The output is a known configuration that becomes the baseline for every later comparison, not a claim that the product is ready.

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
**Decision:** Continue into characterization, or stop and debug integration.\
**Interview trap:** Deep FA before basic operation, or treating loaded chassis corners as bring-up exit evidence.

Once operation is reproducible, measurements can be used to model behavior rather than debug basic integration.

### Step 4: Characterize the behavior

Create the behavioral model. The output is not pass/fail. The output is how the system behaves. Characterization is exploratory: finding a cliff improves understanding; it does not automatically fail the product. Before this step you know one corner works. After it you know how distributions move with stress variables and which ledgers (power, noise, timing, spectral, control) are thin.

Map temperature, voltage, optical stress, and unit/lot distributions. On the transmitter path, measure TDECQ, OMA, ER, and level linearity; with component access, add LIV, RIN, and SMSR (§7.4, §7.7, §5.7). Characterization still studies the product largely as an isolated object.

**Representative evidence:** Response surfaces; distribution summaries; thin-ledger list; candidate guardbands.\
**Exit:** Population behavior versus required corners is mapped, thin ledgers are named, and you decide whether derate or redesign is needed before loaded-fleet work.\
**Decision:** Proceed to system validation, derate the envelope, or redesign.\
**Interview trap:** Treating a hero sample at $25^\circ$C as the fleet model, or parking life projection inside characterization.

Once normal behavior and thin margins are mapped, the product can be challenged in realistic system combinations.

### Step 5: Validate margin and interoperability

 

Characterization tells how the product moves. Margin testing tells where it fails. Interoperability tells whether that boundary changes across hosts, peers, firmware, channels, and operating environments. These are one system question, not two lifecycle steps.

##### Establish remaining margin.

A product does not fail because it reaches a nominal limit. It fails because all margins are consumed. Ask how much capability survives when temperature, voltage, loss, ORL, aging intent, and manufacturing variation stack under production-like stress (§7.9, §5.19). Compare pre-FEC BER, telemetry, retrain count, and control headroom against the characterization baseline. Track optical, electrical, thermal, reliability, and manufacturing margin categories separately, then stack once. Do not subtract the same physical effect twice under two names. Quiet-bench margin is not rack margin.

*Margin waterfall (illustrative accounting, not a universal budget).*

> Initial optical margin\
> $-$ temperature penalty\
> $-$ connector / plant loss\
> $-$ aging penalty\
> $-$ contamination / ORL penalty\
> $-$ manufacturing variation\
> $=$ remaining field margin

Allocate margin where uncertainty is highest (§5.19).

##### Challenge the supported ecosystem.

A component can pass isolated validation and still fail as a system. Prove supported host, peer, firmware, and channel combinations retain required headroom. Margin on a golden host does not prove the supported ecosystem. Exercise host ASIC / SerDes, peer module or second source, firmware and CMIS revision, faceplate temperature and airflow, and fiber/cable plant. Assign failures to host, peer, software, environment, or channel before changing laser bias tables.

> **Tradeoff.** Golden-host speed vs interop risk
>
> *Improves:* Fast bring-up and clean debug on a known good station
>
> *Worsens:* Hidden host, firmware, or plant sensitivity until volume
>
> *When acceptable:* When golden-host data are a stage gate, not the exit criteria for the ecosystem
>
> *Experienced decision:* Use golden hosts for speed; require representative hosts before calling interop done.

**Representative evidence:** Cliff locations and remaining headroom by ledger; margin waterfall without double-counted penalties; loaded-corner results (Table 7.5); supported combination list and documented restrictions.\
**Exit:** Failure cliffs and remaining headroom are known at the named plane and loaded corners, and supported host/peer/firmware/channel combinations retain required headroom or a documented restriction defines where the product may ship.\
**Decision:** Approve the shipping envelope and supported ecosystem, restrict deployment or SKUs, or send the design back.\
**Interview trap:** Calling golden-host margin the ecosystem exit, or subtracting the same impairment twice under two names.

Once the present-day shipping envelope is understood, qualification can ask whether time and exposure change it.

### Step 6: Qualify reliability

Build mechanism-based evidence that the design survives expected variation and life. Temperature sweeps during characterization show how a healthy product behaves while it is hot or cold. Reliability stresses ask whether exposure causes permanent degradation. Keep operational environment test (works while exposed), reliability stress (exposure causes unacceptable permanent change), and life projection (justified field-life claim) distinct.

Do not run stresses only because a checklist names them. Follow failure mechanism $\rightarrow$ acceleration method $\rightarrow$ stress $\rightarrow$ pre/post observable $\rightarrow$ acceptance criterion $\rightarrow$ confidence (§8.3, §8.4, Appendix D.3). A stress without a failure mechanism is only exposure. Deep FIT/DPPM math lives in Chapter 8.

**Representative evidence:** Pre/post stress margins; mechanism notes; sample and confidence statement; production-proxy candidates.\
**Exit:** Sample plan, mechanism, and projected life support the requirements slice, or ship is explicitly held for life risk.\
**Decision:** Accept life risk for the envelope, derate life or use conditions, or hold.\
**Interview trap:** Treating HTOL as host interoperability or as production readiness.

Reliability qualification is developed in Chapter 8, including mechanism selection, accelerated stress, observables, sample confidence, and acceptance decisions.

Once life risk is bounded for representative hardware, the next question is whether production can reproduce that result.

### Step 7: Validate manufacturing

The factory is part of the design. Qualification proves the design. Manufacturing validation proves the process: build it repeatedly, measure it repeatedly, and detect bad units. Engineering samples often receive unusual attention; volume readiness requires manufacturing distributions, not only the best units.

This is the PVT question: whether yield, process control, and ATP coverage survive lot-to-lot variation (§9.5, §9.2, Table 9.2). DVT belongs earlier; do not park it inside this step. Prove ATP/sample/SPC coverage against known escapes with replay, separation, and production repeatability.

**Representative evidence:** Multi-lot yield; classified ATP/sample/SPC coverage; measurement capability; FAIR; escape-detection proof (Appendix D.16, §9.5).\
**Exit:** Multi-lot yield, screen coverage, SPC stability, and FAIR evidence support opening volume, or shipment is held for process control.\
**Decision:** Open volume toward pilot, hold shipment, or demand corrective action before ramp.\
**Interview trap:** Calling two hand-selected lots "multi-lot" evidence.

Manufacturing validation is developed in Chapter 9, including production-intent builds, traceability, measurement-system analysis, yield, ATP, SPC, supplier control, and staged ramp.

Once the process and its screens are controlled, a bounded deployment can test the remaining assumptions.

### Step 8: Run a controlled pilot

A pilot is not merely a small production shipment. It is a controlled experiment designed to determine whether validation and qualification assumptions remain true in deployment. Lab and factory evidence may still miss install practice, traffic mix, or environment.

Use known serial numbers and lots, representative hosts, enhanced telemetry, and explicit success and rollback criteria (§7.12). Telemetry should reveal whether BER, FEC behavior, retrains, temperature, optical power, lane behavior, and cohort rates match expected distributions.

**Representative evidence:** Pilot cohort database; field BER/FEC and telemetry trends versus lab baselines; exit metrics.\
**Exit:** Pilot success/rollback criteria are met, or risk drives restrict or reject.\
**Decision:** Expand deployment, restrict, pause a supplier or lot, or reopen an earlier step.\
**Interview trap:** Calling open volume a pilot, or learning the escape from customer outage instead of a bounded trial.

Once pilot evidence matches the release model, production can expand under sustained controls.

### Step 9: Ramp mass production

Sustain volume with process control after pilot exit. Depth lives in Table 9.2, Chapter 9. Pilot success does not prove ECO discipline, SPC stability, and RMA burn-down at volume. Hold or open volume based on control, not on hope that pilot luck continues.

**Representative evidence:** SPC trends; yield; RMA rates by code; ECO impact checks.\
**Exit:** SPC, ECO, and RMA loops support sustained volume, or volume is held.\
**Decision:** Open / hold volume; trigger supplier corrective action.\
**Interview trap:** Treating pilot luck as proof of sustained control.

Once volume is open, fleet evidence becomes the continuing check on process and design assumptions.

### Step 10: Monitor the fleet

Validation does not end at shipment. Keep escapes and drift detectable after release (§7.12, Table 7.6). Unknown failure modes, aging, supplier drift, and environmental effects appear only at scale. Every telemetry field must answer what decision it enables. Trend and disagreement alarms catch dying units; hard thresholds catch dead ones.

There is no terminal exit: ownership transfers into steady operations when schema, owners, and cohort baselines are in place.

**Representative evidence:** Schema-stable telemetry; cohort baselines; alarm history; RMA codes split by vendor and mechanism class.\
**Exit:** Ownership transfer into operations with schema, owners, and cohort baselines in place (ongoing control, not silence).\
**Decision:** Continue ship, restrict, pause a supplier or lot, or reopen an earlier step when cohort evidence falsifies a qual assumption.\
**Interview trap:** Collecting telemetry that enables no decision.

Fleet observations have value only when they change the next product or its controls.

### Step 11: Feed learning into the next revision

Close the loop into the next requirements and architecture revision. Fleet and FA evidence that does not change the product is wasted. Separate one-off install errors from systematic design or process debt (§1.1). Fleet tickets that never become requirements, or fixes without screen changes, leave the next escape open.

**Representative evidence:** Revision backlog with owners: requirement changes, architecture changes, ATP updates, derates.\
**Exit:** Next-revision targets are written with owners, or residual risk is explicitly accepted without change.\
**Decision:** Next-revision targets, ATP updates, or documented accept risk.\
**Interview trap:** Closing RMAs without an owned control or requirements update.

The output becomes the input to Step 1 of the next revision.

### Choosing evidence within a step

At any step, use the least expensive evidence that can responsibly answer the current question.

- Use a model when the assumptions are understood and the result can later be checked.

- Use a bench experiment when controlled measurement can separate the important hypotheses.

- Use qualification stress when the uncertainty concerns permanent degradation or lifetime.

- Use pilot or fleet evidence when the condition cannot be represented credibly in the laboratory.

The evidence source does not determine the lifecycle step. The engineering question does. Simulation may support Step 2 architecture review, while a validated model may also support a Step 5 margin decision. A chamber experiment may support characterization or qualification depending on whether it measures reversible operation or permanent degradation.

> **Before open volume**
>
> Step 1 requirements $\cdot$ Step 2 architecture $\cdot$ Step 3 bring-up $\cdot$ Step 4 characterization $\cdot$ Step 5 margin/interop $\cdot$ Step 6 qualification $\cdot$ Step 7 manufacturing/ATP $\cdot$ Step 8 pilot $\cdot$ Step 9--10 fleet control (Appendix D.17, Table 7.2).

For every metric at every step, state measurement, reference plane, condition, access level, and the decision unlocked (§3.9, Appendix A.2, Appendix D.16). Bad: "receiver sensitivity is $-15$ dBm." Good: sensitivity at the module optical input under the named BER target, temperature, wavelength, and FEC assumptions. A number without a plane and a method is not a measurement.

> **Engineering heuristic.** Name the reference plane before you name the instrument. A pretty eye at the wrong plane is a wrong answer.

**Key idea.** Validation is a sequence of decisions, not a catalog of tests. Begin by defining success and closing the architecture on paper. Establish interpretable hardware, build the behavioral model, challenge system margin, qualify life, prove manufacturing control, and then compare the model with pilot and fleet reality. Each step should produce evidence for one explicit decision and identify the uncertainty that remains.

## The core IM/DD measurements

Once the flow is clear, the measurement list is organized around isolation: transmitter, channel, and receiver. That split is older than PAM4. Long before TDECQ, field engineers learned that a dark link can be a dead laser, a dirty connector, or a dead TIA, and that guessing which one burns hours. Bisecting those three domains is still how you keep debug from turning into simultaneous retunes of everything.

### Transmitter

Start with the light leaving the faceplate or the CPO fiber array. For PAM4, the headline metric is *TDECQ* (transmitter and dispersion eye closure quaternary): a reference equalizer is applied to the captured eye and the residual penalty is reported in dB (§7.4). Alongside it you read *OMA* (outer), extinction ratio, and *RLM* (level linearity), plus wavelength, spectral width, and RIN with a bias-driver versus feedback bisect (§5.7, §5.8, §4.3.1).

What else you add depends on the transmitter style. Laser-bearing modules need LIV, threshold, slope, SMSR, and chirp checks for DMLs (§5.7, §5.4). External MZMs (TFLN or silicon) need EO $S_{21}$, $V_\pi$, quadrature bias versus temperature, and driver-path eye symmetry at baud (§3.14.3, §7.4). Microring banks need resonance alignment, thermal tuning, neighbor crosstalk, and peaking-network EO $S_{21}$ (§3.14.3, Chapter 6). The point of the list is not completeness for its own sake: it is knowing which instrument answers which hypothesis when the eye closes.

### Channel

If the transmitter looks clean into a golden receiver and the link still fails, the channel is next. Insertion loss from fiber, connectors, MUX/de-MUX (§6.3), and on-chip coupling (§3.14.3) is the first ledger line. Use the specified maximum loss for the exact connector class, number of interfaces, cleanliness condition, and reference plane; do not treat "1--3 dB per mated pair" as a universal normal loss. Chromatic dispersion (§3.11) matters more on FR-class SMF sweeps than on short DR links. Optical return loss (ORL) is the quiet killer: reflections can create optical feedback noise, multipath interference, deterministic distortion, and power-independent error floors. That is why many DR/FR modules still carry isolators while some CPO engines rely on design margin and monitor photodiodes instead (§4.3.1, Chapter 5). Fiber attach (MPO/MTP, FAU, grating couplers) shows up as both yield and reliability (§8.7).

### Receiver

Receiver work asks whether the front-end can still decide bits at the OMA that survives the channel. Measure sensitivity (minimum OMA for the named BER objective at a stated plane, pattern, and EQ) and stressed-receiver sensitivity with a calibrated stressor for margin (§7.5), plus overload before the TIA saturates. Underneath those system numbers sit the photodiode/TIA pair: responsivity, bandwidth, and input-referred noise (§4.5, Chapter 4).

### Link level

Only after Tx, channel, and Rx each look sane do you trust a full-link verdict: pre-FEC BER against the KP4 threshold (§3.12), post-FEC BER, FEC symbol-error histograms (§7.3.1), and a signed link-budget ledger from transmitter OMA to receiver sensitivity with penalties and remaining margin. That ledger is the document you argue from in DVT; the BER alone is not.

## Measurement mapping

The metrics above are scattered across Tx, channel, Rx, and link level because that is how you debug them. Table 7.3 collects the same metrics into one reference: what is measured, the instrument, why it matters, and the failure signature that points back to it. Use the chapter subsections for the debug logic; use this table to look up an instrument fast.

<table class="book-table"><tr><th>Metric</th><th>Instrument</th><th>Why it matters</th><th>Failure signature</th></tr><tr><td>OMA / TDECQ</td><td>DCA + reference equalizer</td><td>Scores transmitter quality against an ideal source; governs PAM4 acceptance (sec:tdecq)</td><td>TDECQ rises with no average-power change; points to bandwidth, RLM, or bias</td></tr><tr><td>Extinction ratio / RLM</td><td>DCA level histograms</td><td>Sets OMA at fixed average power (sec:sensitivity); poor RLM inflates TDECQ</td><td>Compressed inner eyes with passing average power</td></tr><tr><td>Wavelength / SMSR</td><td>OSA or wavemeter</td><td>Confirms grid placement and single-mode purity (sec:laser-params)</td><td>Side modes rise with T or age; line walks off grid</td></tr><tr><td>RIN</td><td>PD + ESA or dedicated RIN analyzer</td><td>Can create a power-independent BER floor when signal-proportional intensity noise dominates (sec:rin)</td><td>BER improves with power then flattens (a floor); not every floor is RIN</td></tr><tr><td>Insertion loss / ORL</td><td>Power meter + ORL meter</td><td>First ledger line; reflections can cause feedback noise, MPI, distortion, or floors (sec:optical-channel)</td><td>Burst or patterned errors with stable average power; ORL dependence</td></tr><tr><td>Receiver sensitivity</td><td>BERT + calibrated attenuator</td><td>Minimum OMA at target BER, the budget's bottom line (sec:sensitivity,sec:secq)</td><td>Waterfall shifts uniformly right without flooring</td></tr><tr><td>Pre-FEC BER / FEC histogram</td><td>BERT + FEC counters</td><td>The single number every other metric feeds; histogram shape reveals mechanism (sec:kp4)</td><td>Clustered errors point to bursts; sparse errors point to Gaussian noise margin</td></tr><tr><td>CMIS state / DDM</td><td>Host or CMIS tool</td><td>Confirms management layer before blaming optics (sec:cmis)</td><td>Module never reaches ModuleReady; DDM disagrees with bench truth</td></tr></table>
**Table 7.3.** Measurement mapping: metric, instrument, rationale, and failure signature in one reference. Row explanations follow; chapter subsections give the full treatment of each metric.

### Reading the measurement map

Use the table for lookup. Use the notes below when a metric is new, or when you need the decision the measurement unlocks.

##### OMA / TDECQ.

TDECQ asks how much worse this transmitter is than an ideal source after a reference equalizer. Outer OMA is the optical swing the receiver actually uses. Together they answer whether the Tx path still has signal-quality margin. **Exit when** TDECQ and OMA meet the PMD/ATP at the named pattern and temperature. **Decision:** continue, retune bias/equalization, or reject the transmitter path. **Risk if skipped:** you chase receiver noise while the eye was already out of budget.

##### Extinction ratio / RLM.

Extinction ratio and level separation mismatch (RLM) set how much OMA you get at fixed average power and how linear the PAM4 levels are. Poor RLM inflates TDECQ even when average power looks fine. **Exit when** ER/RLM meet the mask at the failing corner. **Decision:** retune modulator bias or driver, or accept a derate. **Risk if skipped:** average-power APC hides a collapsing outer eye.

##### Wavelength / SMSR.

Wavelength placement and side-mode suppression ask whether the spectral ledger still closes: on-grid for filters or rings, single-mode under temperature and age. **Exit when** the line sits in the allowed window with SMSR in spec. **Decision:** retune lock/thermal control, derate temperature, or replace the laser. **Risk if skipped:** BER failures get blamed on RIN when the line walked onto a filter edge.

##### RIN.

Relative intensity noise sets how far $Q$ can rise with power. Measure with a quiet bias path and under controlled ORL so you separate intrinsic laser noise from feedback. **Exit when** RIN at the stated ORL meets the budget. **Decision:** fix reflections/supply, replace the laser, or stop raising launch into a floor. **Risk if skipped:** you keep adding photons to a non-power-limited impairment (Appendix A.8.9).

##### Insertion loss / ORL.

Insertion loss is the first power-ledger line. ORL asks whether reflections are seeding RIN or bursts. **Exit when** loss and ORL are inside the plant assumptions used in the link budget. **Decision:** clean/replace connectors, add isolation, or reopen the budget. **Risk if skipped:** burst tickets look like random laser death.

##### Receiver sensitivity.

Sensitivity is the minimum OMA for the named BER objective at a stated plane, pattern, and EQ, the budget's bottom line. A parallel waterfall shift with no floor usually means the Rx path or channel loss changed. **Exit when** sensitivity meets the ledger with stated pattern and stress. **Decision:** golden-swap ownership, derate reach, or redesign Rx. **Risk if skipped:** Tx FA on an Rx-limited link.

##### Pre-FEC BER / FEC histogram.

Pre-FEC BER is the system score every other metric feeds. An FEC *symbol-error histogram* is not a DCA eye histogram. KP4 is Reed--Solomon RS(544,514) on 10-bit symbols (§3.12). The decoder or host FEC counters report how many of those symbols were wrong before correction, usually as errors per codeword or as errors versus time / codeword index. That distribution is the histogram.

Average BER alone does not classify the failure. Two links can share the same pre-FEC BER and fail for different reasons:

- **Sparse / Poisson-like:** most codewords have zero or one error; rare twos and threes. Fits steady noise (thermal, steady RIN, Gaussian-ish margin).

- **Bursty / clustered:** long quiet stretches, then clumps of many errors in a short window (several bad symbols or consecutive bad codewords). Fits time-local events: MPI or reflections, connector intermittents, unlock, supply or clock glitches, vibration.

KP4 can correct up to 15 symbol errors per codeword. Sparse errors usually stay correctable. A burst can dump many errors into one codeword, so you see uncorrectables or flapping even when the long-run BER still looks acceptable. Shape separates sparse Gaussian-like errors from clustered bursts; a bursty histogram alone is not proof of MPI. Confirm with ORL, timing, swaps, and plant disturbance (§11.2, Appendix A.8.9). **Exit when** BER and histogram support the claimed mechanism class. **Decision:** contain, clean, retune, or open FA. **Risk if skipped:** average BER hides a bursty escape that ATP never stressed.

> **What this usually means.** BER waterfall floor that more launch power does not fix
>
> *Usually:* RIN, MPI, crosstalk, receiver saturation, or another non-power-limited impairment (Appendix A.8.9)
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

: the stressed-eye counterpart used on the receiver side under a named PMD, adding a calibrated stressor to test margin rather than transmitter quality alone. Distinguish SECQ from a general stressed-receiver sensitivity test. See §7.5.

RLM (relative level mismatch)

: measures how evenly the four PAM4 levels are spaced; poor RLM (uneven levels) inflates TDECQ.

Because TDECQ folds several impairments into one number, the way it fails is diagnostic: uneven levels point to modulator or driver linearity (RLM); residual eye closure the equalizer cannot fix points to excess ISI or limited bandwidth; a noise-limited result points to low OMA, RIN, or reflections. For external MZMs (TFLN or silicon), also check EO $S_{21}$ bandwidth, $V_\pi$ and bias quadrature drift with temperature, and RF return loss on the driver-to-modulator path (§3.14.3). This is why *LPO*, which removes the module's own DSP, raises the stakes on transmitter quality: there is less downstream equalization to hide behind, so TDECQ-class metrics become even more central.

## SECQ and stressed-receiver testing

*SECQ* (stressed eye closure quaternary) mirrors TDECQ on the *receiver* for a named PMD and clause: instead of scoring transmitter quality with a reference equalizer, the test applies a calibrated optical stressor (attenuation, ISI template, optional RIN) and asks how much margin remains before the receiver hits that clause's target pre-FEC metric.

Stressed-receiver sensitivity and overload tests (§4.4) use the same philosophy but are not automatically the same procedure as SECQ. Bracket the operating OMA range with impairments the link will see in the field, and name the PMD, FEC architecture, error model, metric, and test duration. For LPO, where the module DSP is gone, stressed Rx margin on the host-side receiver (§3.6, §10.5.1) is as important as TDECQ on the transmitter.

## Instruments

A failing PAM4 link rarely announces which block is wrong. Ask the investigation question first, then pick the gear that can separate the leading hypotheses. Loopback topology tells you which side of the optical connector owns the fault (§7.2.2).

Where is the power?

: Power meter for average power; DCA for OMA. Walk planes before you change bias.

Did the eye or levels move?

: (digital communication analyzer) for PAM4 eyes, TDECQ, OMA, RLM (§7.4). Needs a reference receiver filter matched to the PHY under test.

Did BER shift or floor?

: for pre- and post-FEC BER and FEC symbol histograms (§3.12); / stressor for calibrated attenuation and optional ISI on sensitivity sweeps.

Is the spectrum or grid wrong?

: / wavemeter for wavelength, SMSR, side modes, and linewidth where supported (Chapter 5).

Is intensity noise the floor?

: PD + ESA or a dedicated RIN analyzer under a defined ORL (§4.3.1).

Does temperature own it?

: Thermal chamber + TEC controller for corners; essential for rings and laser grids (§3.14.3, Chapter 6).

Use electrical loopback (host SerDes), optical loopback (Tx$\to$Rx on module), and golden-host/golden-module interop to bisect faults. If the fault follows the module under golden-host swap, stop blaming the SerDes; if it stays with the host, stop opening laser FA.

## Building a link budget

A link budget is a signed dB (or power) ledger from transmitter to receiver. For IM/DD short reach, start from outer OMA at the Tx faceplate and subtract every loss and penalty until you compare against receiver sensitivity (with target BER and KP4 pre-FEC threshold, §3.12, §4.4).

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
Keep power budget, signal-quality penalties, timing, thermal, and control authority as separate ledgers when the impairment is not a pure optical-power number (§5.19, Appendix D.10).

##### Walkthrough before Method A or B.

Name the reference plane (usually Tx faceplate OMA). Subtract each loss once: coupling, connectors, fiber or waveguide, and any plant allocation you have evidence for. Compare the remaining power to receiver sensitivity at the named BER / FEC objective. Choose Method A or Method B for transmitter quality; do not tax TDECQ twice by subtracting a compliance OMA/TDECQ limit and an independent TDECQ penalty.

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

Method A: Composite compliance

: Use the PMD's specified OMA/TDECQ relationship. Do not subtract TDECQ again as an independent link-budget penalty.

Method B: Engineering decomposition

: Use a separate measured transmitter-quality penalty only when the accounting method is defined and does not duplicate the compliance limit.

##### Illustrative ledger (single-mode DR-class sketch).

Start from Tx OMA on the DCA (or from average power and ER) at a named plane. Subtract connector/coupling loss using the specified maximum for the connector class, interface count, and cleanliness (an illustrative poor or multi-interface allocation can land near 1--3 dB per mated pair; that is not a universal normal loss). Subtract fiber loss ($\sim$0.3--0.4 dB/km at 1310 nm; often negligible at 500 m) and MUX/de-MUX if WDM (2--5 dB per stage, §6.3). Apply penalties with Method A or Method B above; add dispersion (§3.11) and reflection/MPI terms (§7.2.2, §4.3.1) only when not already absorbed. Compare the remainder to stressed sensitivity at the *named* PMD's pre-FEC objective (for a KP4-class optical PMD under its random-error model, often near $2.4\times10^{-4}$; state FEC, metric, and test duration). Keep production margin appropriate to fleet corners. Numbers here are an illustrative DR-class sketch, not universal limits. Electrical budgets parallel this for the host-to-module path: COM and pre-FEC BER (§10.5.2, §3.6). LPO requires *both* ledgers to close without module DSP help.

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

You touch CMIS on every bring-up and every field triage. It is how the host learns what module is seated, when lasers may turn on, what Tx/Rx power and temperature look like, and whether a link failed at the management layer or the optical layer. A module that passes BER on a bench with lasers forced on but cannot reach ModuleReady on a production host will fail in the fleet (§7.9).

### The module state machine

CMIS defines a module state machine the host drives. After presence detect and power application, the module stays in low power until the host releases `LPModeL` (or the CMIS 5.x `LowPwr` equivalent). The host reads identifier pages, clears sticky interrupts, and steps the module toward ModuleReady. Only then should Tx lanes or ELS lasers enable. ELSFP modules that emit before ModuleReady are a reject: the host did not authorize light (§5.14).

Data paths have their own state machines in CMIS 5.x (data path states, and network path states for media-side links). For bring-up, map the sequence in §7.9 onto these transitions: presence and Vcc, CMIS init and ModuleReady, enable light, optical path check, electrical lock, traffic, snapshot. Skipping step 2 and jumping to BER is how interop failures hide until production.

### The memory map: pages, monitors, control

The lower memory map holds module identity, status, interrupt flags, and alarm thresholds. Upper pages hold application descriptors, lane controls, tunable-laser support, versatile diagnostics (VDM), and command-data-block (CDB) firmware messaging . Hosts select an application (lane count, host interface, media type) before bringing up traffic.

*DDM* (digital diagnostic monitoring) is the telemetry layer you read at scale: per-lane Tx and Rx optical power, laser bias current when exposed, module temperature, supply voltage, LOS/LOL flags, and alarm/warning bits. On WDM parts you also get wavelength or channel ID. This is exactly what §7.12 reads before anyone reaches for a DCA. On bring-up, dump the register map you will use in the field and treat that dump as the golden reference for later RMA comparisons.

### CMIS as a validation deliverable

CMIS correctness is part of production readiness, not a firmware afterthought. ATP should prove the state machine reaches ModuleReady across voltage and thermal corners; DDM monitors track bench truth (CMIS Tx power versus DCA, module temperature versus case $T$); alarms fire at the right thresholds; and firmware revision is ECO-controlled like laser die revision (§9.2). Multi-source interop failures are often CMIS, media-type, or firmware mismatches, not marginal TDECQ (§7.9). At fleet scale the register map is the only eyes you have on a module in the rack. If CMIS is wrong, triage starts blind.

## Module and system bring-up

Characterization proves a sample can meet metrics on a quiet bench. Bring-up proves a module (then a system) can be powered, managed, and linked the way production and the fleet will actually run it. Lab-to-production programs fail in the gap between those two if you only ever test golden hosts, clean fiber, and room-temperature faceplates.

##### Module bring-up sequence.

Run this order on every new module (pluggable, ELSFP, or CPO engine with CMIS). Do not skip ahead to BER: a link that "works" with lasers forced on and CMIS ignored will fail the first host that enforces the state machine (§5.14).

1.  **Presence and power.** Detect module (`ModPrsL` or equivalent). Apply rails in the host power sequence. Confirm Vcc and module temperature in CMIS. Stay in low power (`LPModeL` asserted or ModuleLowPwr) until management is sane.

2.  **CMIS init.** Read identifier, vendor, firmware rev, supported media. Clear sticky interrupts. Confirm the state machine can reach ModuleReady (or the pluggable equivalent) under host command. Dump the register map you will use in the field; that dump is your bring-up golden reference.

3.  **Enable light.** Exit low power; enable Tx lanes / ELS lasers only after ModuleReady. Confirm Tx optical power and laser bias (if exposed) against the power class. Lasers that come up before the host asks are a reject for ELSFP (§5.14).

4.  **Optical path.** Mate fiber (clean first). Check Rx power and LOS. Optical loopback first if the host path is unproven.

5.  **Electrical lock.** Bring host SerDes / module CDR. Confirm LOL clear, equalizer taps not pegged (§3.6). For LPO, this is the host eye and COM path (§10.5.2, §3.14.3).

6.  **Traffic.** PRBS or live FEC traffic. Pre-FEC BER vs. KP4 threshold (§3.12); glance at FEC symbol-error histogram shape.

7.  **Quality snapshot.** On a Tx-capable path: OMA/RLM/TDECQ or module diagnostics that proxy them (§7.4). Record CMIS + BER + case $T$ together so later triage has a baseline (§7.12).

The numbered sequence above is primary. Table 7.4 is a wall-chart quick reference only; do not maintain a second conflicting procedure.

<table class="book-table"><tr><th>Step</th><th>Action</th><th>Pass signal</th><th>Fail first look</th></tr><tr><td>1</td><td>Presence / Vcc / temp</td><td>CMIS alive, rails in range</td><td>cable, seat, PSU</td></tr><tr><td>2</td><td>CMIS state machine</td><td>ModuleReady (or equiv.)</td><td>firmware, TWI, LPMode</td></tr><tr><td>3</td><td>Enable Tx / ELS</td><td>Tx power in class; lasers on only when commanded</td><td>bias driver, enable pin, APC</td></tr><tr><td>4</td><td>Fiber / Rx power</td><td>Rx power up; LOS clear</td><td>dirty MT, polarity, break</td></tr><tr><td>5</td><td>CDR / SerDes lock</td><td>LOL clear; taps not saturated</td><td>host SI, LPO COM, retimer</td></tr><tr><td>6</td><td>Pre-FEC BER</td><td>below KP4 target with margin</td><td>Tx quality, ORL, Rx sensitivity</td></tr><tr><td>7</td><td>Snapshot</td><td>CMIS dump + BER + T logged</td><td>(needed for RMA later)</td></tr></table>
**Table 7.4.** Module bring-up checklist. LOS = loss of signal; LOL = loss of lock. Limits come from the ATP and PMD, not from this table.

##### Production-representative corners.

Bench corners ($T$, $V$) are necessary and not sufficient. Chassis thermal, host rails, and ORL belong before Design Validation Test (DVT) exit on a representative unit. The full set in Table 7.5 belongs before Production Validation Test (PVT) exit (Table 9.2).

<table class="book-table"><tr><th>Corner</th><th>What to run</th><th>Why it catches</th><th>Points to</th></tr><tr><td>Chassis thermal</td><td>Module in target rack/sled at airflow and power load; not only a quiet chamber on a bench fixture</td><td>Faceplate T and TEC load differ from chamber setpoints</td><td>derate, TEC, ring unlock</td></tr><tr><td>Host rails live</td><td>Bias / CMIS powered from host supplies with SerDes traffic on</td><td>Switching noise into laser bias looks like RIN (sec:laser-drivers)</td><td>PSRR, ground, APC</td></tr><tr><td>Dirty fiber / ORL</td><td>Controlled contamination or ORL stress on MT/FAU; clean vs dirty BER</td><td>Field installs are not lab-clean; ORL raises RIN and bursts</td><td>connector, isolator, feedback</td></tr><tr><td>Cable plant</td><td>Production fiber length, MPO count, and bend radius</td><td>Extra loss and reflections eat margin the ledger assumed</td><td>link budget (sec:link-budget)</td></tr><tr><td>ELS hot-swap</td><td>Pull/replace ELSFP under traffic (or under controlled traffic stop per CMIS)</td><td>Service action the architecture promised (sec:elsfp)</td><td>state machine, mate cycles</td></tr><tr><td>Neighbor load</td><td>Adjacent modules/lanes at full traffic and max case T</td><td>Crosstalk, shared supply droop, thermal crosstalk on rings</td><td>WDM lock, SI, PSU</td></tr><tr><td>LPO / linear path</td><td>Host COM and pre-FEC BER without module DSP crutch</td><td>LPO fails here first (sec:224g-deploy,sec:com,sec:drivers)</td><td>host FIR, module linearity</td></tr><tr><td>Voltage corners</td><td>Host Vcc min/max with traffic</td><td>Brown-out and CMIS glitches</td><td>power design, ATP</td></tr></table>
**Table 7.5.** Production-representative corners. A quiet BERT at 25 $^\circ$C with pristine fiber is characterization, not production readiness.

### Reading the production-corner map

Quiet $T$/$V$ characterization maps the part. Table 7.5 is the checklist. Read it in four groups before you invent new corners.

##### Thermal and loading.

Chassis thermal and neighbor load ask whether sled airflow, faceplate gradient, shared heat, and tray traffic leave TEC, lock, and BER with margin. Chamber case-$T$ alone does not answer that.

##### Electrical and host.

Host rails live, voltage corners, and LPO / linear path ask whether SerDes traffic, supply noise, brown-out, and host FIR/COM still close the link when the module cannot hide behind a retimer.

##### Optical plant.

Dirty fiber / ORL and cable plant ask whether production MPO count, bends, and field cleanliness match the signed loss and reflection assumptions.

##### Service and interaction.

ELS hot-swap asks whether the replaceability story survives a live maintenance window: CMIS state, mate cycles, and recovery under the traffic policy you claim.

Chassis thermal, host rails, and ORL are the minimum before DVT exit on a representative unit. The full set belongs before PVT exit (Table 9.2). Later fleet monitoring must not invent coverage these corners never ran.

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

- **Host path:** run the same sequence on the target NIC/switch ASIC SerDes, not only the lab BERT. LPO and half-retimed modules expose host FIR/CTLE mistakes that a retimed module hid (§10.5.1, §10.3).

- **Multi-lane / multi-module:** bring all lanes on a port, then neighbors in the same cage or tray. Watch thermal rise, supply droop, and CMIS temp alarms when the tray is loaded.

- **Golden swap:** known-good module in the suspect host slot, then suspect module in a known-good slot. That single swap splits host vs. module before you open FA (§7.12).

- **Interop:** at least one other vendor host or module if the program claims multi-source. Interop failures are usually CMIS, media type, or electrical eye, not laser physics.

- **ELS / CPO:** external laser modules add a second bring-up: ELSFP state machine and optical mate to the engine, then engine bring-up with light present (§5.14, §10.10). A dark engine with a healthy ELS is an optical connector or FAU problem until proven otherwise.

##### Exit criteria before "bring-up done."

Call *bench bring-up* done when CMIS state machine and enable sequence are correct, the unit emits and receives light in class, CDR locks, pre-FEC BER is usable on a trusted setup at a named plane, and a CMIS+BER+$T$ snapshot is filed. Call *system integration bring-up* done when the same sequence closes on the target host, golden-swap has split host vs. module issues, and multi-lane / neighbor load has not opened a new basic failure mode. Do *not* require loaded chassis-thermal / host-rail / ORL margin closure to declare bring-up done; that is Stage 3 margin and interop evidence (§7.1.6, Table 7.5). Everything after bring-up is characterization depth, margin/interop, supplier gates (§9.2), or fleet triage (§7.12).

**Key idea.** Bring-up is a sequence (presence $\to$ CMIS $\to$ light $\to$ lock $\to$ BER $\to$ snapshot), then a system proof on the real host. Production-representative corners prove remaining headroom; they do not redefine bench bring-up. A quiet bench pass is not DVT.

## The debug mindset

Debug at this level is data-driven, not opinion-driven. The method is disciplined bisection: change one domain at a time, and let the measurement tell you whether the transmitter, the channel, or the receiver moved.

1.  Isolate transmitter versus channel versus receiver, using loopbacks.

2.  Sweep temperature and voltage to expose corner-dependent failures.

3.  Correlate failures to DSP equalizer tap values (§3.6) and FEC symbol-error statistics (§3.12); these tell you *how* the link fails.

The third step is where modern PAM4 links differ from older eye-mask work. Tap saturation and FEC histograms often reveal the failure mode before a single waveform screenshot does. Treat those as primary evidence, not as afterthoughts logged once BER already fails.

[^15]

## The debugging fork in validation

Apply the debugging fork (§4.8) before sweeping parameters or changing firmware: check the power meter or CMIS Rx power monitor first. If power moved, the fault is in the optical path (laser, coupling, connector, fiber, MUX); if power held but BER or TDECQ worsened, it is signal quality (bandwidth, noise, jitter, bias, equalization, reflection). This one check prevents the most common validation mistake: retuning an equalizer or laser bias when the real cause is a dirty connector. Then check which margin ledger moved (§5.19) before descending to component physics.

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
> Scope $\cdot$ time behavior $\cdot$ population $\cdot$ power or quality $\cdot$ highest-value measurement $\cdot$ decision $\cdot$ recurrence control (Appendix D.17).

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

: the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (§7.4, §10.5.2, §3.14.3).

Reliability

: the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (§8.5, §5.13, §8.3, §5.14).

Manufacturability

: a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (§9.2, §8.7).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label. Chapter 11 expands the same method into symptom-led bench and fleet procedures.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; §5.14).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (§3.12), equalizer tap saturation (§3.6).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $\to$ bucket).

Table 7.6 is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

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
Scope sets severity and priors. Correlation after isolation unlocks contain, pause, replace, or supplier escalate (Appendix D.5).

<table class="book-table"><tr><th>Symptom</th><th>First telemetry check</th><th>Bucket</th><th>Confirm on bench / FA</th><th>Typical fix owner</th></tr><tr><td>Link never comes up (fresh install)</td><td>CMIS presence, Vcc, Tx power flatline, LOS</td><td>Mfg or install</td><td>Visual fiber/connector; golden module swap; CMIS dump</td><td>Ops install; supplier ATP if lot-correlated</td></tr><tr><td>Intermittent LOS / burst errors</td><td>Rx power dropouts; FEC bursts; ORL events</td><td>Perf (ORL) or mfg (contam.)</td><td>Clean/inspect MT; ORL meter; RIN vs ORL (sec:laser-drivers,sec:rin-values)</td><td>Ops cleaning; packaging if repeat RMA</td></tr><tr><td>Pre-FEC BER high, power OK</td><td>Tap saturation; RLM/TDECQ if logged; case T</td><td>Perf</td><td>DCA TDECQ/RLM; host COM; LPO vs retimed path (sec:tdecq,sec:com)</td><td>Host SI / module Tx design</td></tr><tr><td>BER rises only at high case T</td><td>Module temp alarm; Tx power drop; walk</td><td>Perf or reliability</td><td>LIV at T; OSA grid; TEC current; EAM bias (sec:laser-aging)</td><td>Derate / TEC / laser supplier</td></tr><tr><td>Slow BER creep over weeks/months</td><td>Bias current up for same Tx power; SMSR if monitored</td><td>Reliability</td><td>LIV/SMSR vs ship ATP; Arrhenius lot history</td><td>Laser wear-out; ELS replace</td></tr><tr><td>Sudden hard fail, was healthy</td><td>Last good CMIS snapshot; neighbor links OK</td><td>Reliability (COD) or mfg (ESD)</td><td>Dark LIV; DPA on facet/solder; date-code cluster?</td><td>FA + supplier 8D</td></tr><tr><td>One date code / site fails early</td><td>Lot Pareto; burn-in escape rate</td><td>Mfg</td><td>Incoming SPC vs ATP; FA on sample of lot</td><td>Supplier CAPA; hold shipment</td></tr><tr><td>WDM / ring unlock, power OK</td><td>Channel ID; thermal of neighbors; lock-loop status</td><td>Perf</td><td>Resonance tune; crosstalk; CW-WDM line power (sec:lock-validation,sec:thermal-xtalk,sec:cwwdm-laser)</td><td>Lock firmware / thermal design</td></tr><tr><td>ELSFP swap restores link</td><td>Old module CMIS vs new; connector cycles</td><td>Reliability or mfg (connector)</td><td>Inspect MT; mating-cycle count; laser LIV in returned module (sec:elsfp)</td><td>Laser vs connector split in FA</td></tr></table>
**Table 7.6.** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $=$ performance (design/operating point); reliability $=$ time-dependent wear; mfg $=$ lot/process/install excursion. Row notes follow.

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

Ask whether the external laser, the connector, or the engine owned the fail. Compare old versus new CMIS and connector cycles. Confirm MT inspect and LIV on the returned module. **Decision:** split RMA codes for laser versus connector. **Risk if skipped:** FIT burns down the wrong wear-out mode (§5.14).

### Why triage order matters

Scope before mechanism. Telemetry before destructive FA. Bucket before owner. Confirm before CAPA. Closing the loop into ATP is part of the incident, not optional paperwork. Reversing that order produces NFF piles and merged RMA codes that make life models dishonest.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $T$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with Table 7.6. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (§5.13).

    - Manufacturability: quarantine lot, incoming hold, supplier 8D with DPA photos and ATP deltas (§9.2).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Worked paths (three common tickets).

*"High temp only."* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate). A permanent LIV or spectrum shift at temperature that matches an aged lot raises $P(\mathrm{aging})$ and justifies moving the ticket toward reliability; cool-down recovery without baseline shift keeps it in performance. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (§3.14.3, Chapter 6).

*"Random burst errors, average power fine."* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, treat feedback/ORL as the leading performance hypothesis until confirmed. If ORL is fine and bursts track a date code, treat intermittent fiber attach as the leading manufacturing hypothesis. If bursts grow over months at fixed ORL, suspect laser or driver aging (§5.8, §5.13).

*"ELSFP replace fixed it; returned module looks alive on the bench."* Alive LIV with high ORL sensitivity or a dirty MT face supports connector/ORL over laser wear-out; confirm with IL/ORL and recurrence. Dead or kinked LIV supports a reliability path. Split those RMA codes or FIT math blames the wrong mode (§5.14, §8.7).

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

Use the least complex instrument that can falsify the current hypothesis. Table 7.3 maps every key metric to its instrument, rationale, and failure signature in one lookup; the bring-up sequence (§7.9) orders those instruments into a workflow.

### How it fails

Validation fails when the setup, sample, or acceptance rule does not match the product. Common misses are a stale calibration, the wrong reference plane, a golden host that hides interop risk, pristine fiber that hides ORL sensitivity, short BER dwell, one lane tested without neighbors, and chamber temperature used as a substitute for measured case temperature. These are test escapes even when the device physics is sound.

\> \*\*Failure mode: Low optical power\*\* \> \> \*\*Symptoms.\*\* A lane is dark or below its launch-power limit. \> \> \*\*Likely causes.\*\* A laser or enable fault, coupling loss, connector contamination, fiber polarity, calibration error, or a power-meter setup mistake. \> \> \*\*Measurements.\*\* Known source and meter, inspection scope, CMIS state and bias, power at successive planes, and a golden fiber or module. \> \> \*\*Mitigations.\*\* Correct the setup first, then repair the failing source, attach, connector, or control path. Add the signature at the earliest production test that can catch it.

### How it is debugged

Preserve the failing state and record software, firmware, calibration, fixture, cables, temperature, and supply. Verify the meter with a known source. Walk from power to spectrum to waveform to BER, moving one reference plane at a time. Use a golden swap to split host, module, and fiber. Only then stress temperature, voltage, ORL, and neighbors. Every corrective action needs a repeated failing test, a repeated passing test, and a guard against recurrence in ATP or telemetry.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* A new module lot showed low optical power on one station. \> \> \*\*Investigation.\*\* The same units passed on a second station. A known source exposed an offset in the first power-meter path. \> \> \*\*Finding.\*\* The lot was good, and the station was reading low. \> \> \*\*Root cause.\*\* A reference jumper had been replaced without updating the path-loss calibration. \> \> \*\*Resolution.\*\* The station was recalibrated, jumper identity was placed under change control, and a start-of- shift source check was added.

## Interview takeaway

**Key idea.** Validation is a chain of evidence. Start with calibrated power and management state, move through spectrum and waveform, then trust BER only after the blocks and reference planes are known. Run the target host, chassis, fiber, and neighbor corners before calling the product ready.

Junior mistake: call a golden-host BER pass "production ready," or open supplier FA before clearing the tester (Table 7.2, Chapter 9, Appendix D).

### Interview Q&A: Optical Validation

Practice speaking these answers aloud. Prefer first-person reasoning over definitions. Detail lives earlier in this chapter (§7.1, Table 7.2). Score your answer using the chapter-end spoken-answer rubric (Appendix A.12.1).

##### Question 1. What is the purpose of optical validation?

*Tests:* evidence-to-decision.

*Spoken answer.* "Validation builds enough evidence to decide whether the product is suitable for its intended system use. I treat it as a sequence of release decisions, not a catalog of tests."

*Pressure follow-up.* "What decision should validation enable?"\
*Answer pivot.* "Continue, redesign, derate, qualify, open volume, or hold, with named remaining risk."

*Trap:* treating validation as "run BER and temperature."

##### Question 2. What is the difference between characterization, verification, validation, qualification, and production test?

*Tests:* terminology discipline.

*Spoken answer.* "Characterization maps behavior and distributions. Verification checks a frozen requirement at a named plane. Validation asks whether the complete product works for intended system use. Qualification bounds permanent degradation from life and environment. Production test detects unacceptable units at volume. Same meters can serve all five; the question and decision differ" (§7.1, Chapter 8, Chapter 9).

*Pressure follow-up.* "Where does burn-in fit?"\
*Answer pivot.* "Burn-in is a production screen for early-life defects when justified. It does not replace life qualification."

*Trap:* calling them "levels of testing."

##### Question 3. Why is the validation sequence ordered, and which activities can overlap?

*Tests:* order and overlap.

*Spoken answer.* "Earlier steps make later evidence interpretable. Requirements and architecture come before hardware spend. Bring-up before characterization so sweeps mean something. Characterization before margin so cliffs are not a surprise. Life and manufacturing evidence answer different residual uncertainties after the shipping envelope is clear. Some work can overlap in calendar time, for example architecture refresh while bring-up runs, or manufacturing validation while qualification samples age, but a later pass cannot substitute for missing earlier evidence" (Table 7.2).

*Pressure follow-up.* "Can you start qualification before characterization finishes?"\
*Answer pivot.* "You can start planning, but without a behavioral model you risk stressing the wrong observables and accepting the wrong drift."

*Trap:* reciting Steps without saying why order matters.

##### Question 4. What happens during architecture review?

*Tests:* budget and derating priors.

*Spoken answer.* "I ask whether the design can plausibly meet requirements before hardware makes changes expensive. I close optical, noise, thermal, electrical, reliability, and manufacturing budgets on stated assumptions, and I name the thin margins that validation must challenge. Architecture review is a path check, not life proof."

*Pressure follow-up.* "Where do derating rules come from?"\
*Answer pivot.* "Vendor qual data, prior measurements, physics-of-failure models, field history, and design guidelines. They are priors. Qualification later checks whether this design and process support the claim" (Chapter 8).

*Trap:* "I simulated the link budget and it closed."

##### Question 5. What is the objective of hardware bring-up?

*Tests:* reproducible baseline.

*Spoken answer.* "Bring-up establishes a known, reproducible operating state: identity, rails, firmware, CMIS, light, lock, alarms, basic power, and a simple link. I am not proving full margin yet. I am separating integration fails from product-performance questions" (§7.9).

*Pressure follow-up.* "What is your first action if ready state never appears?"\
*Answer pivot.* "Freeze the setup, dump CMIS and rails, and isolate host versus module before any deep optical sweep."

*Trap:* "power on and check BER."

##### Question 6. What is characterization trying to produce?

*Tests:* behavioral model.

*Spoken answer.* "A behavioral model: nominals, distributions, sensitivities, and recognizable signatures. The output is which margins are thin and which corners to challenge in system validation, not only pass or fail."

*Pressure follow-up.* "What belongs on every unit versus a sample?"\
*Answer pivot.* "Cheap identity and power checks can be every-unit; expensive waterfalls and stressed RIN stay sample or audit unless escape data forces otherwise."

*Trap:* "measure over temperature."

##### Question 7. Give an illustrative temperature characterization sweep.

*Tests:* conditions before causality.

*Spoken answer.* "Illustrative only. Sweep one lane at fixed attenuation, fixed pattern and dwell, pre-FEC BER, with the transmitter allowed to drift rather than held in constant-power control. Suppose case temperature goes 20 to 75°C: Tx power falls from about $+1.8$ to $+0.9$ dBm, bias rises from about 45 to 60 mA, RIN in a named band worsens from about $-155$ to $-149$ dB/Hz, and pre-FEC BER approaches $10^{-7}$. That maps the complete-link response. It does not isolate the BER mechanism, because received power also moved. Next I would repeat BER at fixed received power to see whether quality degraded independently of average power. I would not claim RIN caused the BER change from the first sweep alone."

*Pressure follow-up.* "What else could move BER while power falls?"\
*Answer pivot.* "Eye closure, ORL, control saturation, or a host EQ corner. Fixed-$P_\mathrm{rx}$ and ORL checks separate those."

*Trap:* blaming RIN from a coupled temperature sweep.

##### Question 8. What is the difference between margin validation and interoperability validation?

*Tests:* cliffs versus ecosystem.

*Spoken answer.* "Margin finds failure boundaries by consuming optical, electrical, thermal, and control headroom. Interoperability asks whether those boundaries move across hosts, peers, firmware, and cable plants. Same lifecycle step, different conclusions" (§7.1.6).

*Pressure follow-up.* "Why not test only the reference host?"\
*Answer pivot.* "Reference-host margin can look fine while a production host EQ or CMIS path moves the cliff."

*Trap:* "margin is internal; interop is another vendor."

##### Question 9. How would you run an optical-margin test?

*Tests:* waterfall and planes.

*Spoken answer.* "Trusted baseline at a named plane and BER condition, then stepped attenuation with a full BER waterfall, not only the fail point. Repeat at relevant $T$/$V$ corners and combine credible stresses. Report onset, boundary, uncertainty, and remaining margin without double-counting penalties" (§7.7).

*Pressure follow-up.* "How would you measure jitter margin?"\
*Answer pivot.* "Inject controlled jitter on the electrical path with a qualified BERT, sweep amplitude and composition, and compare the BER or lock boundary to the allowed input jitter at documented EQ and CDR settings."

*Trap:* "add loss until it fails."

##### Question 10. How do you choose the next validation measurement?

*Tests:* information per cost.

*Spoken answer.* "I pick the cheapest measurement that separates the strongest surviving hypotheses and changes the decision. Telemetry and controlled swaps before internal probing or DPA. I care what uncertainty it removes and what action each result unlocks."

*Pressure follow-up.* "When is destructive analysis justified?"\
*Answer pivot.* "When non-destructive evidence cannot separate owners and the release or containment decision is blocked."

*Trap:* "run full optical characterization."

##### Question 11. Why is pilot deployment part of validation?

*Tests:* bounded field experiment.

*Spoken answer.* "A pilot tests whether lab and factory models survive deployment. Bounded serials, enhanced telemetry, exit criteria, and rollback. Compare BER, FEC, retrains, temperature, power, and cohort rates to the release model. It is not a small shipment" (§7.1.9).

*Pressure follow-up.* "What would justify expanding the pilot?"\
*Answer pivot.* "Exit metrics met, no unexplained cohort, and containment still reversible if the next stage fails."

*Trap:* "customers are happy."

##### Question 12. Give me a 60-second answer for validating a new optical module.

*Tests:* time-boxed program.

*Spoken answer.* "Define measurable requirements and the release call. Review whether architecture budgets close. Bring up reproducibly, characterize distributions and cliffs, then validate margin and interoperability on production-like hosts and plants. Qualify named life mechanisms and validate manufacturing measurement, ATP, and yield. Run a controlled pilot, ramp under monitoring, and feed escapes back into requirements or controls."

*Pressure follow-up.* "Schedule is cut in half. What do you protect?"\
*Answer pivot.* "Requirements, bring-up integrity, the thinnest margin corners, and a reversible pilot. I cut nice-to-have sweeps before I cut decision-critical evidence."

*Trap:* listing BER, temperature, reliability, and interop with no order.


<div class="nav-links">
  <a href="ch6-wdm-and-wavelength-locked-lasers">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch8-reliability-qualification-building-the-lifetime-confidence-argument">Next &rarr;</a>
</div>
