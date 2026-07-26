---
layout: default
title: "Ch 8: Reliability Qualification: Building the Lifetime Confidence Argument"
---

# 8 Reliability Qualification: Building the Lifetime Confidence Argument

*Read first:* FIT versus DPPM; qualification argument; sample confidence; burn-in versus HTOL; wear-out families.

*Deep dive:* Arrhenius life projection; GR-468 stress detail; connector mate-cycle physics.

*Reference:* qualification planning matrix; wear-out map.

> **Reliability qualification at a glance**\
>
> - Start with the requirement. Define the life, environment, handling, and performance claim that needs support.
>
> - Identify credible failure mechanisms. Ask what physical or electrical process could violate that claim.
>
> - Select an acceleration method. Choose a stress that meaningfully accelerates the mechanism without creating an unrelated failure.
>
> - Define observables. Decide what measurable change reveals degradation before running the stress.
>
> - Define acceptance criteria. State how much change is allowable and why.
>
> - Choose representative samples. Cover relevant lots, suppliers, sites, process corners, and product variation.
>
> - Interpret the evidence. Connect observed degradation, confidence, and model assumptions to a bounded decision.
>
> - Feed the result into production controls. Determine what must be controlled, screened, sampled, or monitored after qualification (Chapter 9).
>
> Qualification is not evidence because a standard test was performed. It is evidence when a named stress, observable, sample plan, and acceptance criterion support a specific reliability decision.

A five-year lifetime requirement cannot be verified by operating a product for five years before release. Reliability engineering therefore works indirectly. The team identifies the physical mechanisms that could cause the product to degrade, selects stresses that accelerate those mechanisms, measures signatures that reveal change, and determines whether the resulting evidence supports the intended use and lifetime.

The stress itself is not the argument. HTOL, humidity, temperature cycling, ESD, vibration, and connector cycling answer different questions. Running all of them does not automatically create confidence, and omitting one is not automatically irresponsible. The qualification plan must connect each activity to a credible threat.

Qualification also differs from characterization. A temperature sweep during characterization asks how a healthy product behaves while it is hot or cold. A qualification stress asks whether exposure causes permanent change. Reversible movement and lasting degradation require different evidence and different decisions.

Finally, qualification does not prove that every future production unit will be reliable. It establishes bounded confidence for the tested design, sample population, mechanisms, stresses, durations, observables, and assumptions. Chapter 9 addresses whether production can reproduce that qualified population consistently.

## What qualification is, and is not

Keep these jobs distinct:

Characterization

: Maps behavior and distributions across corners.

Verification

: Checks measured results against frozen requirements.

Validation

: Demonstrates that the complete product is suitable for its intended system use (Chapter 7).

Reliability qualification

: Builds confidence that named lifetime and environmental mechanisms do not violate the intended claim.

Production screening

: Attempts to detect unacceptable units or early-life defects at manufacturing scale (Chapter 9).

Burn-in

: A possible production screen for specific early-life mechanisms. Burn-in is not automatically qualification and does not replace qualification HTOL.

*Module example.* Characterization maps LIV and BER versus temperature. Verification checks that ship power and BER meet the PRD. Validation shows the module works in the target host and plant. Qualification HTOL asks whether biased high-temperature exposure permanently shifts threshold or slope beyond the life claim. Burn-in may cull infant mortality on the line; it does not prove five-year wear-out life.

## The language of scale: FIT and DPPM

Fleet arguments need two different numbers. One is about life in the field; the other is about quality at the factory door. A rate without population definition, observation time, and confidence is not a fleet claim (Appendix D.16).

FIT (failures in time)

: failures per $10^{9}$ device-hours. State the population unit (laser die, module, or link), observed versus predicted FIT, confidence interval, useful-life / constant-hazard assumption, and whether the system is treated as repairable. Multiply a per-unit FIT by population and hours only after those definitions are fixed.

DPPM (defective parts per million)

: Distinguish incoming defects, outgoing defects, and escaped field defects. Always state the denominator, time window, and whether rework and retest are included.

**Key idea.** Zero failures do not prove a zero failure rate. 0 failures in 20 units is not the same evidence as 0 failures in 1,000 units. 0 failures after $10^{3}$ device-hours is not the same evidence as 0 failures after $10^{6}$ device-hours. Evidence strength depends on sample-hours, one-sided upper confidence bounds, censoring, and whether lots and sites are representative. Qualification and production SPC complement each other; neither alone is a fleet claim.

[^16]

## Qualification flows

Qualification is a life and variation argument, not a list of stresses. A requirement such as five-year operation is too abstract to test directly. You identify the mechanisms that could violate it, choose stresses that accelerate those mechanisms, monitor an observable signature, and decide whether the resulting evidence is sufficient for the claim (Appendix D.3, Appendix A.8.5).

Debugging is what you do when remaining margin hits zero. Qualification asks how much margin remains after the expected stresses. Place this work in §7.1 Step 6; manufacturing validation and ATP live in Chapter 9. Keep the customer view and the vendor view distinct: the vendor designs internals; the customer characterizes externally visible behavior and decides deployment (Appendix A.8.6, Appendix A.8.7).

<pre class="dectree" aria-label="Requirement"><code>Requirement
  |
Budget (life / FIT / DPPM / power)
  |
Allocation (die / package / module / host)
  |
Verification (GR-468 / GR-1221 / JESD47 / ATP)
  |
Production + field monitoring</code></pre>
> **Margin budgeting**
>
> Every stress spends margin: temperature, voltage, ripple, contamination, insertion loss, connector wear, vibration, aging, process variation. Qual verifies what remains, not only that the part still links.

> **Customer view vs vendor view**
>
> Vendor: internals, device physics, implementation.\
> Customer: BER, sensitivity, FEC, telemetry, environmental sweeps, interop.\
> Engineering samples (Tx-only, Rx-only, breakout, PRBS) open isolation; otherwise stay on the external surface.

For a bookended product, begin with BER, FEC, sensitivity, telemetry, environment, and interop. Request engineering access only when that surface cannot decide (Appendix D.11).

##### Worked story: gradual laser degradation.

Walk one mechanism end to end before opening the matrix. The requirement is a named life claim, for example five years at the use condition and thermal class in the PRD. The threat is gradual active-region wear: threshold rises and slope falls over life. That is not COD (sudden dark after a healthy ship LIV) and not ESD or latch-up (hard fail with supply signature and no optical aging trend).

The evidence strategy is representative lots and sites under justified HTOL: elevated temperature and bias chosen because they accelerate that mechanism, with sample size, stress hours, and confidence stated (§8.3, §8.2). HTOL is useful only when that acceleration argument holds. Observables are LIV and system proxies versus the ship baseline: $I_\mathrm{th}$, slope efficiency, wavelength, launch power or BER drift, recorded before and during stress at named planes.

Acceptance is a bounded change after projection that still supports the life claim. Document $E_a$ and confidence when converting HTOL hours to field years, and do not apply one $E_a$ to mixed mechanisms. Production control is decided last and owned in Chapter 9: a room-temperature LIV/power ATP proxy, a sampled hot audit, SPC on $I_\mathrm{th}$ and slope, or an explicit statement that no cost-effective 100% screen separates the weak tail. A production burn-in may cull infant mortality; it does not replace this life argument.

Other mechanisms (solder fatigue, contamination, connector wear) follow the same template. Table 8.1 is the reference fill-in, not the primary explanation.

##### Qualification planning matrix.

The matrix restates the laser story (and siblings) as mechanism $\rightarrow$ stress $\rightarrow$ observable $\rightarrow$ acceptance $\rightarrow$ production control. Fill cells for the product class and claimed life; do not treat blank rows as covered.

<table class="book-table"><tr><th>Failure mechanism</th><th>Stress</th><th>Observable</th><th>Acceptance</th><th>Production control</th></tr><tr><td>Laser degradation</td><td>Temperature / lifetime (HTOL)</td><td>I_th, slope, , BER</td><td>Named limit vs life claim</td><td>ATP / SPC / sampled audit / none</td></tr><tr><td>Solder fatigue</td><td>Temperature cycling</td><td>Resistance, BER, opens</td><td>Post-stress continuity / BER</td><td>Process control, FAIR</td></tr><tr><td>Contamination / corrosion</td><td>Humidity / damp heat</td><td>Loss, ORL, leakage</td><td>IL/ORL / functional limits</td><td>Handling, sealing, audit</td></tr><tr><td>Connector wear</td><td>Mate cycling</td><td>Insertion loss, ORL</td><td>Cycle-count IL budget</td><td>Supplier / hygiene control</td></tr></table>
**Table 8.1.** Qualification planning matrix (reference). Same template as the laser-degradation story above. Interview form: Appendix C.15, Appendix D.3. Decision unlocked: which mechanism-stress-observable row is missing before you claim life.

##### GR-468 in practice.

Optoelectronics inherited a common qualification language from telecom: *Telcordia GR-468-CORE*. Map each stress onto the qualification evidence path in Appendix D.3; do not invent a second sequence. Core stresses that still show up on every laser and module program: HTOL for life or mechanism evidence; burn-in as a production infant-mortality screen when justified; temperature cycling and damp heat; ESD and mechanical stress.

Keep the jobs distinct: **burn-in** screens infant mortality from a production population; **qualification HTOL** gathers life or mechanism evidence under accelerated operation. Do not imply that every GR-468-style HTOL is a per-unit screen. A 1,000-hour life test may justify a 100% room-temperature proxy, a sampled hot audit, a process monitor, or no direct production screen at all. Document $E_a$ and confidence bounds when converting HTOL hours to field years, keep sample-size humility (§8.2, Chapter 9), and qualify the laser die, hermetic package, and module assembly separately when failures split across those boundaries (§8.7, §5.13, §5.14).

*Arrhenius* acceleration underpins life projection only when the named failure mechanism is temperature-accelerated in the assumed regime.

##### Sample strategy and confidence.

Weak answer: "We test 20 units." Strong answer: the sample strategy depends on the failure-rate target, the confidence requirement, cost, and population variation. State lots, date codes, suppliers, manufacturing sites or lines, process corners, and whether the claim is zero-failure upper-bound or observed rate (§8.2, Appendix D.16). A rate without population, observation time, and confidence is not a fleet claim.

> **Engineering heuristic.** A small sample that saw zero failures does not prove field life. It sets an upper bound. State that bound, or do not make the claim.

> **Tradeoff.** More qualification vs faster release
>
> *Improves:* Confidence and fewer late escapes
>
> *Worsens:* Schedule, cost, and delayed learning in the field
>
> *When acceptable:* When remaining risk is high and reversible controls cannot cover it
>
> *Experienced decision:* Prioritize tests by risk $\times$ uncertainty $\times$ impact. Do not test everything equally.

##### GR-1221: the passive-component companion.

GR-468 covers active optoelectronics. Its companion, *Telcordia GR-1221-CORE* (Generic Reliability Assurance Requirements for Passive Optical Components), covers the parts GR-468 does not: connectors, fiber couplers, WDM filters and MUX/DEMUX, splitters, and isolators . It uses the same style of stress sequence (damp heat, temperature cycling, mechanical, and aging tests) but scores pass/fail on insertion loss and return loss rather than on LIV. A short-reach link that leans on an on-package or blind-mate MUX and on external multi-wavelength sources carries a passive reliability budget that lives in GR-1221, not GR-468 (§8.7, Chapter 6). Split the qual the same way you split the FIT: active laser die under GR-468, silicon under JESD47, passive optics under GR-1221.

##### Handoff to manufacturing.

Qualification bounds life risk for representative hardware. Whether production can reproduce that result, screen escapes, and hold SPC is developed in Chapter 9. Failures that pass qual but fail field usually sit in derating policy, connector contamination, or a manufacturing coverage gap (§5.13, §7.12, §9.5).

## Electronics reliability: driver, TIA, and DSP silicon

GR-468 covers the optoelectronic parts of the link: the laser die, the photodiode, and the hermetic or non-hermetic package around them. The modulator driver, TIA, retimer, and DSP (§3.14.3, §4.5) are ordinary CMOS or SiGe BiCMOS ICs, and they wear out and fail by a different, better-documented set of mechanisms. Treat them with the semiconductor industry's own qualification language, not with Arrhenius laser-aging math borrowed from §5.13.

##### JESD47: the silicon-side GR-468.

JEDEC JESD47 is the baseline stress-test-driven qualification flow for a new IC, a device family, or a process change: temperature cycling, HTOL, HTSL (high-temperature storage life), autoclave or HAST (highly accelerated stress test) for moisture, and mechanical shock and vibration . It plays the same role for driver and TIA silicon that GR-468 plays for the laser: a common list of stresses that a supplier runs once and a customer accepts instead of renegotiating a qual plan on every design win.

##### ESD and latch-up: failure modes GR-468 does not test.

Two mechanisms are specific to ICs and absent from the laser-side wear-out map in Table 8.2:

ESD

: a discharge event during handling or assembly damages a gate oxide or junction. Component-level classification uses the human-body model (HBM) and charged-device model (CDM) test standards, *ANSI/ESDA/JEDEC JS-001* and *JS-002* . A driver or TIA datasheet HBM/CDM rating is the number that protects the part on the factory floor, at fiber-attach and wire-bond stations where a laser die is also exposed.

Latch-up

: a parasitic thyristor structure in CMOS turns on under an overvoltage or current-injection event and holds a low-impedance path until power is cycled. *JESD78* defines the overvoltage and $\pm100$ mA current-injection test that classifies susceptibility by supply and signal pin . A latched driver IC can look like a dead laser on the bench (no light, no LIV signature) until you check the supply current instead of the optical path.

Both mechanisms are 100%-screen or design-margin items, not something you project with an activation energy. If a driver fails ESD or latch-up in the field, that is a manufacturability or design-margin bucket item (§7.12), not a wear-out FIT argument.

##### AEC-Q100: a borrowed grade, not a requirement.

*AEC-Q100* is the automotive industry's qualification standard for ICs, built on the same JEDEC JESD47/JESD22 stress methods with tighter ESD targets and named temperature grades from Grade 3 ($-40$ to $85$°C) up to Grade 0 ($-40$ to $150$°C) . Datacenter optics does not require Q100; the fleet lives in a controlled data hall, not an engine bay. It is still a useful signal: a driver, TIA, or retimer die that also ships in an automotive part number typically carries a published Q100 grade, and that grade is a fast proxy for the ESD/latch-up margin and temperature-cycle depth behind the datasheet, without re-running the qual plan yourself.

##### Where this lands after qualification.

Carry IC-level qual into the production acceptance and SPC structure in Chapter 9: require the supplier's JESD47 qual report and HBM/CDM/latch-up ratings for driver and TIA die at DVT, add an ESD handling audit to the incoming-QC checklist alongside laser LIV/SMSR sampling, and treat a driver/TIA silicon revision the same way you treat a laser die revision or a CMIS firmware rev: an ECO that needs first-article requalification, not a silent BOM swap.

## Wear-out modes to know

Arrhenius math, derating, and the worked FIT example live in §5.13. This section is the mechanism catalog: how each failure shows up in ATP and telemetry, and which triage bucket owns it (§7.12). Do not run process CAPA on a wear-out part, and do not burn FIT math on a dirty connector.

##### Infant mortality versus wear-out versus packaging.

Field failures come in three clocks, and mixing them up wastes CAPA. Infant mortality is early fails from latent defects; burn-in and HTOL screens remove them before ship (§8.3). Wear-out is gradual or sudden end-of-life in the laser or EAM under temperature, current, and optical power, projected with Arrhenius and derating (§5.13). Packaging and assembly faults (FAU align, epoxy creep, solder voids, connector wear) often dominate field returns once lasers are screened (§8.7). Destructive physical analysis (facet cross-section, EDX, FAU section) is required when the signature is ambiguous or when you need evidence for supplier 8D (§9.2).

##### Mechanism map.

Table 8.2 is the working list for laser-bearing modules and CPO/ELS paths. Customize limits in the ATP; keep the classification discipline.

<table class="book-table"><tr><th>Mechanism</th><th>Observable</th><th>ATP / telemetry</th><th>Triage bucket</th></tr><tr><td>COD (facet)</td><td>Sudden dark or hard fail; was healthy</td><td>Dark LIV; DPA facet; date-code cluster?</td><td>Reliability (COD) or mfg (ESD)</td></tr><tr><td>Gradual facet / active region</td><td>I_th up, slope down over life</td><td>LIV trend vs ship ATP; HTOL lot history</td><td>Reliability (wear-out)</td></tr><tr><td>SMSR collapse</td><td>Side modes rise; modal noise / BER</td><td>OSA SMSR vs floor at T</td><td>Reliability; watch aging</td></tr><tr><td>EAM aging (EML)</td><td>TDECQ/RLM creep at fixed bias</td><td>EAM bias sweep + DCA; bias creep log</td><td>Reliability (EAM)</td></tr><tr><td>RIN rise</td><td>BER floor up; feedback sensitive</td><td>RIN @ ORL; isolator / connector check</td><td>Perf if ORL; reliability if isolator</td></tr><tr><td>TEC / thermal control</td><td>Unlock or walk; LIV may look fine</td><td>TEC current, case T, lock status</td><td>Perf (lock) or reliability (TEC)</td></tr><tr><td>Coupling / FAU / solder</td><td>Loss step, intermittent LOS, shock-related</td><td>ORL, mate cycles, DPA FAU/solder</td><td>Manufacturability / packaging</td></tr><tr><td>Driver/TIA latch-up (ESD)</td><td>Sudden hard fail; no light, no LIV signature; supply current spikes</td><td>Supply current vs bias; JESD78 rating; date-code cluster?</td><td>Mfg (ESD) or design margin</td></tr><tr><td>Connector wear / contamination</td><td>ORL creep after repeated mate cycles; RIN floor rise</td><td>Mate-cycle count vs IEC 61300-2-2 rating; endface grade (IEC 61300-3-35)</td><td>Manufacturability / packaging</td></tr></table>
**Table 8.2.** Wear-out and packaging mechanisms versus observables. Arrhenius projection and derating for the laser rows: §5.13. Electronics stress qualification: §8.4. Connector reliability: §8.7. Field classification workflow: §7.12.

### Reading the wear-out map

Table 8.2 is a triage map, not a life calculator. Classify before corrective action. Reliability rows need life models and derate. Performance rows need plant and control fixes. Manufacturing and packaging rows need process and ATP screens. Mixing buckets wastes CAPA (§7.12). Arrhenius projection lives in §5.13; this section teaches how to read the map in three families.

##### Semiconductor wear.

COD, gradual active-region degradation, SMSR collapse, and EAM aging change the diode or modulator physics. COD appears as sudden dark after a healthy ship LIV; gradual wear appears as rising $I_\mathrm{th}$ and falling slope; SMSR collapse raises modal noise while average power can still look fine; EAM aging creeps TDECQ/RLM at fixed laser bias. Separate them with dark LIV and facet DPA (COD versus ESD), LIV trends versus ship ATP (wear), OSA SMSR versus temperature and age (modal), and EAM bias sweeps with eye metrics (modulator). Controls are life review and derate for wear, SMSR/aging ATP for modal risk, and EAM life/ATP screens for modulator aging. Do not burn Arrhenius math on an ESD lot, and do not replace "good" DFBs while the EAM curve walks the eye closed.

##### Control and electronics.

TEC/lock faults, driver/TIA latch-up or ESD, and ORL-driven RIN rise change the environment or the electronics path more often than the laser die. Unlock or $\lambda$ walk with healthy LIV points at cooler or lock; sudden hard fail with supply-current spikes and no optical aging signature points at ESD/latch-up; a BER floor that tracks ORL points at reflections before isolator death. Separate them with TEC current, case $T$, and lock status; supply current and JESD ratings with date-code clusters; RIN at stated ORL versus clean plant (§4.3.1, §8.4, §6.7). Controls are lock/thermal policy, ESD handling screens, and connector/reflection budget, not laser FIT CAPA for every soft floor.

##### Packaging and optical interfaces.

Coupling, FAU/solder, and connector wear or contamination produce step loss, intermittent LOS, shock correlation, or ORL creep after mates. Semiconductor metrics often stay clean. Separate them with ORL, mate-cycle history, endface grade (IEC 61300), and DPA of FAU/solder when needed (§8.7). Controls are assembly CAPA, attach screens, service hygiene, and connector ratings. Life models must not absorb packaging escapes.

Later evidence must not rewrite an earlier wrong bucket without new data. A clean facet DPA does not clear a connector if ORL was never measured. An HTOL pass does not clear a date-code ESD cluster.

## The reliability bathtub: three failure regimes

Field failures follow three regimes with different clocks and different fixes. Mixing them wastes corrective action on the wrong mechanism.

Infant mortality (early life)

: Latent defects from manufacturing: weak solder joints, marginal laser die, contamination, firmware bugs that trip on first thermal cycle. Burns down rapidly with time. Fixed by burn-in, screening, tighter ATP, and first-article control (§8.3).

Useful life (constant rate)

: Random failures at a roughly steady FIT: cosmic-ray-induced single-event upsets, handling damage during unrelated service actions, and isolated material defects that passed all screens. Fixed by redundancy, field-replaceable modules, and design margin. Note: connector wear and contamination accumulate with mate cycles and are usage-driven degradation (§8.7), not constant-rate random failures; budget them separately from the flat-hazard FIT.

Wear-out (end of life)

: Physics-driven degradation: laser facet, active region, EAM absorption curve shift, TEC aging, epoxy creep. Onset depends on temperature, current, optical power, and time. Fixed by derating, Arrhenius-based life projection, and planned replacement intervals (§5.13).

A rising failure rate after years of service is wear-out and calls for replacement planning, not supplier 8D. A cluster of early failures on a new lot is infant mortality and calls for tighter screens. A steady trickle with no date-code correlation is useful-life random and calls for redundancy and fast repair. The triage tree in §7.12 forces this classification before corrective action starts.

## Photonic packaging and module-level failures

Fleet FIT is not only laser wear-out. Once lasers are screened and derated, module and packaging failures often dominate field returns: the part that shipped with a clean LIV still loses light after shock, humidity, or a thousand ELSFP mate cycles. Fiber attach and FAU alignment fail from shock, humidity ingress, and epoxy creep; CPO fiber-array units add assembly steps that wafer test cannot catch (§10.10). Hybrid stacks (TFLN-on-Si, InP laser on Si, flip-chip drivers) introduce solder voids, underfill cracks, and RF return-loss drift (§3.14.3). Thermal paths matter too: uncooled datacom versus liquid-cooled XPO/CPO, and TEC failure that looks like wavelength drift off grid or off ring (§3.14.3, Chapter 6).

##### Connector reliability: MPO, mating cycles, and endface quality.

Multi-fiber connectors are the highest-touch mechanical interface in the fleet: every ELSFP swap, every fiber-attach unit (FAU) rework, and every cable-plant install mates and unmates an MPO. The MPO/MT ferrule family (rectangular, 6.4 mm $\times$ 2.5 mm, guide-pin aligned, 8/12/16/24 fibers per row) is standardized in *IEC 61754-7*, split into one-fibre-row and two-fibre-row parts . That standard fixes geometry, not lifetime; lifetime comes from two companion test methods. *IEC 61300-2-2* specifies the mate/unmate cycling test connector datasheets are rated against, and *IEC 61300-3-35* grades endface scratches, pits, and debris into pass/fail zones on the fiber core and cladding . TIA-568.3 sets 500 cycles as the structured-cabling mating-durability floor; MPO/MTP-class connectors in practice are commonly rated well above 1000 cycles, but that headroom erodes fast with the wrong cleaning discipline (§7.2.2).

Three practical consequences follow for an ELSFP or CPO fiber-attach program. First, ORL creep is a mating-cycle and cleaning problem before it is a laser problem: a rising RIN floor after repeated ELS swaps (Table 8.2) is diagnosed with an IEC 61300-3-35-style endface inspection, not a laser FA request. Second, mate-cycle count belongs in the same telemetry you already read for CMIS and DDM (§7.8); track it per connector, not per module, since a connector can outlive several module swaps or vice versa. Third, write the mating-cycle and endface-grade limits into the ATP explicitly (Table 9.3) rather than inheriting a generic MPO datasheet number: an ELS bank that hot-swaps weekly reaches a 500-cycle floor in under ten years, and a CPO fiber array that is field-serviced more aggressively reaches it faster still.

ELSFP cycling adds connector wear and contamination that raise ORL (§7.2.2, §5.14); the mating-cycle and endface-grade limits above are exactly the numbers that turn "the connector feels loose" into an ATP line item instead of a guess.

Destructive physical analysis (cross-section, EDX) and structured 8D/CAPA with suppliers close the loop from RMA to design rule (§9.2, §7.12). Without that loop, packaging FIT gets mis-attributed to laser Arrhenius models and the wrong part gets redesigned.

## From component FIT to fabric availability

The FIT arithmetic in §5.13 gives a rate: about $0.6$ laser failures per day for a fleet of $5\times10^5$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin (§5.14), but it does not say what a failure costs or how a running job survives one. Two facts turn a per-component rate into a fabric problem.

First, a training or large inference job is synchronous. A collective (§10.7) waits for its slowest member, so a single dead or slow link stalls the whole group, not just one endpoint (§10.6). A link that flaps for a second is a stall for every accelerator in that collective. The optical FIT the earlier chapters budget therefore matters out of proportion to its share of the parts count.

Second, at cluster scale failures are continuous, not rare. Meta's published Llama 3 run is the clearest public data point: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . GPU and HBM3 faults dominated at close to half; network switch and cable faults were 35 events, 8.4% of the total. The optical link is a minority of hard job stops, but 8.4% of a failure every three hours is still tens of network events per run, and the ELS, module, and connector FIT this chapter budgets (§8.2, §8.7) lands in exactly that bucket.

So the design question shifts. It is no longer "how reliable is one link" but "how does a fabric of $10^5$ links keep a job running through a failure every few hours." The answers are architectural, and the optical engineer feeds each one.

Redundancy and rails.

: Rail-optimized topologies (§10.2) already give parallel planes; dual-plane and dual-ToR designs let a lost link degrade bandwidth instead of dropping an endpoint. Redundancy multiplies the link and laser count, which feeds straight back into the FIT budget: more resilience is more parts that can fail.

Detection and reroute.

: Transient faults stay below the job. KP4 FEC (§3.12) absorbs the error bursts a marginal link throws; link-level retry and sub-second link-flap detection plus adaptive routing steer traffic off a degraded link before the scheduler notices. Vendor fabrics (NVIDIA Spectrum-X and Quantum, Broadcom Tomahawk) advertise adaptive or "cognitive" routing and link-level retry for this. Treat the specifics as vendor orientation, but the mechanism is why transient optical faults rarely reach the hard-stop bucket above.

Topology reconfiguration.

: When a link or rack dies for good, an optical circuit switch re-wires the topology around it in milliseconds, so the scheduler routes around the dead node instead of stalling the pod (§10.9) . Component FIT still applies; the fabric survives each failure by re-wiring optically.

Sparing and field service.

: Hot spare nodes and lanes cover the interval between failure and repair. Field-replaceable external lasers (§5.14) make a dead laser a faceplate swap rather than a fabric outage, which is the architectural reason ELS decouples laser FIT from switch FIT. The connector mating-cycle and endface budget (§8.7) sets how many of those swaps the plant survives.

The cost of a failure closes the loop. A hard interruption is lost compute plus the time to detect, reroute or reschedule, and restart from the last checkpoint. Fast detection and reroute shrink that lost time, which is the fabric-level reason the module work in this chapter pays off: derating (§5.13), burn-in and screens (§8.3), and a tight ATP (§9.2) lower the failure rate, and a resilient fabric lowers the cost of each failure that slips through. The two multiply.

## Engineering lens

### How it works

At fleet scale, a modest per-part FIT times millions of parts is a steady stream of failures. Qualification, derating, and mechanism classification keep that stream small and classifiable. Manufacturing validation (Chapter 9) then asks whether the factory can reproduce the qualified population.

### How it is measured

Reliability is measured as a distribution over stress and time. Qualification records failures and drift by mechanism, stress, lot, and sample history. Convert accelerated hours to field years only with a named mechanism, stated $E_a$, and confidence bounds (§8.2, §8.3). Fleet data add install age, temperature, firmware, supplier lot, and return code so wear-out and infant mortality are not mixed (§7.12).

### How it fails

Programs fail at life through wrong mechanisms, weak samples, and overstated acceleration. A stress without a mechanism is only exposure. Zero fails in a small lot is an upper bound, not a FIT claim. Arrhenius math on an ESD cluster or dirty connector wastes CAPA.

### How it is debugged

Classify the bathtub regime and wear-out map bucket before corrective action (§8.6, Table 8.2). Confirm the mechanism with LIV, supply current, ORL, and DPA as needed. Escalate supplier process CAPA only when the bucket is manufacturing; escalate life model and derate when the bucket is wear-out.

## Interview takeaway

**Key idea.** Reliability qualification is a mechanism-driven confidence argument. Begin with the lifetime or environmental claim, identify how it could be violated, select a credible acceleration method, define observable degradation, and choose representative samples and acceptance criteria before running the stress. The result supports a bounded decision; it does not guarantee every production unit. Chapter 9 explains how production reproduces and controls the qualified design.

Junior mistake: treat zero fails in a small HTOL lot as a FIT claim, or treat a temperature sweep as temperature qualification (§8.3, §8.1).

### Interview Q&A: Reliability Qualification

Practice speaking these answers aloud. Prefer first-person reasoning over stress inventories. Detail lives in §8.3, Table 8.1, §8.1. Score your answer using the chapter-end spoken-answer rubric (Appendix A.12.1).

##### Question 1. What is reliability qualification, and how does it differ from validation?

*Tests:* life claim versus system suitability.

*Spoken answer.* "Qualification is a bounded confidence argument that the design continues to meet requirements through intended life and environment. Validation asks whether the product is suitable for system use now. A temperature sweep can validate hot operation; HTOL or cycling asks whether exposure causes permanent degradation. Same gear, different question and acceptance rule" (Chapter 7, §8.1).

*Pressure follow-up.* "Does passing a standard qualify the product?"\
*Answer pivot.* "Only if each stress maps to a named mechanism, observable, sample plan, and decision. A green checklist alone is not the argument."

*Trap:* listing HTOL, humidity, cycling, and vibration.

##### Question 2. How do you design a qualification plan?

*Tests:* mechanism-driven planning.

*Spoken answer.* "I start with the life and environment claim. Then I list credible mechanisms, pick stresses that accelerate those mechanisms, define observables and acceptance before stress, and choose representative lots and sites. Each result must map to release, derating, redesign, production control, or more evidence" (Table 8.1).

*Pressure follow-up.* "The standard requires a low-risk test. What do you do?"\
*Answer pivot.* "I run or waive it with a written mechanism rationale and owner, not silently. Customer or regulatory gates may still force the row."

*Trap:* "follow GR-468 and run the matrix."

##### Question 3. What is the difference between a failure mode and a failure mechanism?

*Tests:* symptom versus physics.

*Spoken answer.* "Mode is the symptom: low power, high BER, dead lane. Mechanism is the physical process: active-region wear, solder fatigue, corrosion, contamination. Several mechanisms can share one mode, so qual and ATP must target mechanisms" (Table 8.2).

*Pressure follow-up.* "Name two mechanisms for low optical power."\
*Answer pivot.* "Laser wear reducing slope, or coupling or connector loss. Different stresses and screens."

*Trap:* swapping mode and mechanism.

##### Question 4. Why can accelerated testing support a field-life claim?

*Tests:* same-mechanism acceleration.

*Spoken answer.* "Only when the stress accelerates the same mechanism expected in use. For temperature-activated wear, Arrhenius may translate hours to field years if $E_a$ and assumptions fit that mechanism. A severe unrelated fail is not a life prediction. I state physics, model, observables, and uncertainty" (§8.3, §5.13).

*Pressure follow-up.* "How do you know the activation energy?"\
*Answer pivot.* "Mechanism-specific supplier data, literature, or fitted degradation on this process. I do not borrow one $E_a$ across mixed failure mechanisms."

*Trap:* "hotter means faster; convert hours to years."

##### Question 5. Explain HTOL and what you would monitor.

*Tests:* access-aware observables.

*Spoken answer.* "HTOL biases the part at elevated temperature to accelerate wear tied to powered operation. I need trusted baselines and intermediate reads, because units can stay functional while drifting. On engineering-access units I measure LIV, threshold, slope, SMSR, and sampled RIN. On bookended production modules I use external proxies: optical power, OMA, wavelength, BER, module current, telemetry, and control headroom. Supplier reports may carry die LIV when the customer only sees the module."

*Pressure follow-up.* "Why is chamber temperature not enough?"\
*Answer pivot.* "Junction or active-region temperature drives many mechanisms. Chamber air without bias or thermal path context can mis-rank stress."

*Trap:* "run hot for a thousand hours and see if it still works."

##### Question 6. What does temperature cycling qualify?

*Tests:* package mechanics.

*Spoken answer.* "Repeated expansion mismatch: solder, bonds, adhesives, fiber attach, alignment. I watch continuity, intermittent lanes, power, sensitivity, BER, and permanent post-cycle shift versus reversible temperature behavior."

*Pressure follow-up.* "Measure in situ or only after cycling?"\
*Answer pivot.* "Periodic or in-situ catches intermittents that a final functional check can miss."

*Trap:* treating cycling as hot/cold operation check.

##### Question 7. What is damp-heat testing trying to reveal?

*Tests:* moisture mechanisms.

*Spoken answer.* "Corrosion, leakage, material or interface degradation, contamination movement. Biased or unbiased depending on mechanism. I look at leakage, loss, ORL, power, BER, and selected DPA, not only a post-test link pass."

*Pressure follow-up.* "Why might bias matter?"\
*Answer pivot.* "Bias can drive electrochemical paths that unbiased storage never sees."

*Trap:* "checks if the package is waterproof."

##### Question 8. Why do ESD qualification if units already pass functional test?

*Tests:* latent damage.

*Spoken answer.* "ESD can kill, leave latent damage, or burn margin while the unit still links. Qual checks the protection network against the handling claim. Production controls cover handling. Final function alone can miss latent damage" (§8.4).

*Pressure follow-up.* "Can ATP screen latent ESD reliably?"\
*Answer pivot.* "Often no. Leakage or sensitivity shifts may need targeted screens; many latent cases need process control, not 100% detection."

*Trap:* "operators might touch the board."

##### Question 9. How do you choose sample size for qualification?

*Tests:* confidence, not folklore.

*Spoken answer.* "No universal count. I size to the rate or degradation claim, confidence, hours, acceleration, and lot diversity. Zero fails in twenty units is an upper bound, not zero field rate. I report bound, sample-hours, censoring, model assumptions, and remaining risk. Sufficiency means the release decision is supported, not that uncertainty is gone" (§8.2, §8.3).

*Pressure follow-up.* "Is lot diversity worth more than more units from one lot?"\
*Answer pivot.* "Usually yes for process and supplier risk. Identical twins inflate false confidence."

*Trap:* "we always use twenty or thirty units."

##### Question 10. What should you do when a qualification test fails?

*Tests:* contain, confirm, scoped requal.

*Spoken answer.* "Verify setup, preserve state, scope the population, separate mode from mechanism, and confirm with discriminating evidence. Contain, decide design, process, supplier, derating, or more data, then repeat enough qual to show the mechanism is addressed. I do not blindly restart the whole matrix."

*Pressure follow-up.* "Failure is outside intended use. Still a fail?"\
*Answer pivot.* "I still investigate relevance. If the stress is unrepresentative, I document that. I do not hide a real mechanism behind a claim of overstress."

*Trap:* "FA the unit and rerun the test."

##### Question 11. What is the difference between qualification, burn-in, and production screening?

*Tests:* life evidence versus screens.

*Spoken answer.* "Qualification supports design-life claims on representative samples. Burn-in is an optional production screen for specific early-life defects. Broader screening is every-unit or sample ATP and process control. Burn-in does not replace qual; qual does not prove every shipped unit was built correctly" (§8.1, Chapter 9).

*Pressure follow-up.* "When is burn-in justified?"\
*Answer pivot.* "When escape data and mechanism show it separates infant fails cheaper than alternatives, and the stress does not damage healthy units."

*Trap:* "burn-in is qualification on every unit."

##### Question 12. Give me a 60-second answer for qualifying a new optical transceiver.

*Tests:* time-boxed qual argument.

*Spoken answer.* "Start from life, environment, handling, and performance claims. Name credible mechanisms, pick accelerations, define observables and acceptance, and sample across lots and sites. Monitor trends, interpret with confidence and model limits, confirm fails to a mechanism, and translate into release, derating, redesign, supplier control, or manufacturing monitors. State the supported claim and remaining risk."

*Pressure follow-up.* "Walk a laser-aging argument."\
*Answer pivot.* "Illustrative five-year continuous claim. Threat: active-region wear raising threshold and cutting slope or OMA. On engineering-access samples I baseline LIV, SMSR, and sampled RIN; on bookended modules I use power, OMA, wavelength, BER, current, and headroom. Biased high-temperature stress with a justified acceleration model, intermediate reads, and drift limits tied to remaining system margin. Result supports release, derating, supplier limit, or redesign; production may sample LIV or bias SPC afterward, but that does not replace the qual argument."

*Trap:* "run the standard stress list."


<div class="nav-links">
  <a href="ch7-optical-validation">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch9-manufacturing-validation-and-production-readiness">Next &rarr;</a>
</div>
