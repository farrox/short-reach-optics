---
layout: default
title: "Ch 8: Reliability and manufacturing at scale"
---

# 8 Reliability and manufacturing at scale

A link that closes in the lab can still fail the business case if lasers die in the field or suppliers cannot hold yield. At gigawatt, multi-generation scale, reliability and manufacturability stop being afterthoughts and become design constraints: they decide whether you put the laser on the ASIC package or in a replaceable module, how hard you derate, and what ATP language you freeze with partners. This chapter covers the vocabulary of failure at scale, the qualification flows that project field life, and the supplier-execution work these systems demand.

## The language of scale: FIT and DPPM

Fleet arguments need two different numbers. One is about life in the field; the other is about quality at the factory door. A rate without population definition, observation time, and confidence is not a fleet claim (Appendix D.16).

FIT (failures in time)

: failures per $10^{9}$ device-hours. State the population unit (laser die, module, or link), observed versus predicted FIT, confidence interval, useful-life / constant-hazard assumption, and whether the system is treated as repairable. Multiply a per-unit FIT by population and hours only after those definitions are fixed.

DPPM (defective parts per million)

: Distinguish incoming defects, outgoing defects, and escaped field defects. Always state the denominator, time window, and whether rework and retest are included.

**Key idea.** Zero failures do not prove a zero failure rate. 0 failures in 20 units is not the same evidence as 0 failures in 1,000 units. 0 failures after $10^{3}$ device-hours is not the same evidence as 0 failures after $10^{6}$ device-hours. Evidence strength depends on sample-hours, one-sided upper confidence bounds, censoring, and whether lots and sites are representative. Qualification and production SPC complement each other; neither alone is a fleet claim.

[^18]

## Qualification flows

Qualification measures remaining margin after stress. Debugging is what you do when that remaining margin hits zero. Use the same canonical validation lifecycle as Appendix A.8.5, Appendix D.2 (requirements through controlled pilot and fleet monitoring); this chapter owns the environmental, reliability, manufacturing, and ATP gates. Keep the customer view and the vendor view distinct: the vendor designs internals; the customer characterizes externally visible behavior and decides deployment (Appendix A.8.6, Appendix A.8.7, Appendix D).

<pre class="dectree" aria-label="Requirement"><code>Requirement
  |
Budget (life / FIT / DPPM / power)
  |
Allocation (die / package / module / host)
  |
Verification (GR-468 / GR-1221 / JESD47 / ATP)
  |
Production + fleet monitoring</code></pre>
> **Margin budgeting**
>
> Every stress spends margin: temperature, voltage, ripple, contamination, insertion loss, connector wear, vibration, aging, process variation. Qual verifies what remains, not only that the part still links.

> **Customer view vs vendor view**
>
> Vendor: internals, device physics, implementation.\
> Customer: BER, sensitivity, FEC, telemetry, environmental sweeps, interop.\
> Engineering samples (Tx-only, Rx-only, breakout, PRBS) open isolation; otherwise stay on the external surface.

The vendor designs the internals. The customer characterizes externally observable behavior and owns the deployment decision. For a bookended product, begin with BER, FEC, sensitivity, telemetry, environment, and interop. Request engineering access (Tx-only, Rx-only, breakout, external eye or TDECQ) only when that surface cannot decide. Do not assume a module reports a conventional optical eye (Appendix D.11, Appendix A.8.7).

Optoelectronics inherited a common qualification language from telecom: *Telcordia GR-468-CORE*. The core stress tests still show up on every laser and module program:

- HTOL (high-temperature operating life) for life or mechanism evidence.

- Burn-in as a production infant-mortality screen when justified.

- Temperature cycling and damp heat.

- Electrostatic-discharge and mechanical stress.

Keep the jobs distinct: **burn-in** screens infant mortality from a production population; **qualification HTOL** gathers life or mechanism evidence under accelerated operation; a production burn-in is a manufacturing screen only when separation, cycle time, and cost justify it. Do not imply that every GR-468-style HTOL is a per-unit screen.

*Arrhenius* acceleration underpins life projection only when the named failure mechanism is temperature-accelerated in the assumed regime: raising temperature accelerates wear-out by a factor set by the activation energy for that mechanism. Do not apply one $E_a$ to mixed mechanisms.

##### GR-468 in practice.

Telcordia GR-468-CORE is the common qualification language for optoelectronic modules and discrete lasers. Map each stress onto the qualification evidence path in Appendix D.3; do not invent a second sequence here.

A 1,000-hour life test may justify a 100% room-temperature proxy, a sampled hot audit, a process monitor, or no direct production screen at all. Do not map every GR-468 stress sequence into 100% ATP. Document $E_a$ and confidence bounds when converting HTOL hours to field years, keep sample-size humility (§8.1, Table 8.5), and qualify the laser die, hermetic package, and module assembly separately when failures split across those boundaries (§8.8, §5.13, §5.14).

##### Qualification planning matrix.

Qualification engineering starts from mechanisms, not from a museum of tests. The matrix is illustrative: fill cells for the product class and claimed life.

<table class="book-table"><tr><th>Failure mechanism</th><th>Stress</th><th>Observable</th><th>Acceptance</th><th>Production control</th></tr><tr><td>Laser degradation</td><td>Temperature / lifetime (HTOL)</td><td>Power, wavelength, BER</td><td>Named limit vs life claim</td><td>ATP / SPC / burn-in proxy</td></tr><tr><td>Solder fatigue</td><td>Temperature cycling</td><td>Resistance, BER, opens</td><td>Post-stress continuity / BER</td><td>Process control, FAIR</td></tr><tr><td>Contamination / corrosion</td><td>Humidity / damp heat</td><td>Loss, ORL, leakage</td><td>IL/ORL / functional limits</td><td>Handling, sealing, audit</td></tr><tr><td>Connector wear</td><td>Mate cycling</td><td>Insertion loss, ORL</td><td>Cycle-count IL budget</td><td>Supplier / hygiene control</td></tr></table>
**Table 8.1.** Qualification planning matrix. Each row is mechanism $\rightarrow$ stress $\rightarrow$ observable $\rightarrow$ acceptance $\rightarrow$ production control (Appendix D.3; interview form Appendix C.15). Decision unlocked: which mechanism-stress-observable row is missing before you claim life.

Interview and wall-chart form of the same path: Appendix C.15, Appendix D.3.

##### Sample strategy and confidence.

Weak answer: "We test 20 units." Strong answer: the sample strategy depends on the failure-rate target, the confidence requirement, cost, and population variation. State lots, date codes, suppliers, manufacturing sites or lines, process corners, and whether the claim is zero-failure upper-bound or observed rate (§8.1, Appendix D.16). A rate without population, observation time, and confidence is not a fleet claim.

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

GR-468 covers active optoelectronics. Its companion, *Telcordia GR-1221-CORE* (Generic Reliability Assurance Requirements for Passive Optical Components), covers the parts GR-468 does not: connectors, fiber couplers, WDM filters and MUX/DEMUX, splitters, and isolators . It uses the same style of stress sequence (damp heat, temperature cycling, mechanical, and aging tests) but scores pass/fail on insertion loss and return loss rather than on LIV. A short-reach link that leans on an on-package or blind-mate MUX and on external multi-wavelength sources carries a passive reliability budget that lives in GR-1221, not GR-468 (§8.8, Chapter 6). Split the qual the same way you split the FIT: active laser die under GR-468, silicon under JESD47, passive optics under GR-1221.

##### ATP sketch: EML module or ELSFP.

A short acceptance sketch lives with the qual hooks in §5.14; the full ATP-as-contract, SPC, and 8D workflow is in §8.10. Failures that pass qual but fail field usually sit in derating policy or connector contamination (§5.13, §7.12).

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

##### Where this lands in the ATP.

Fold IC-level qual into the same acceptance and SPC structure used for the laser (Table 8.6, §8.10): require the supplier's JESD47 qual report and HBM/CDM/latch-up ratings for driver and TIA die at DVT, add an ESD handling audit to the incoming-QC checklist alongside laser LIV/SMSR sampling, and treat a driver/TIA silicon revision the same way you treat a laser die revision or a CMIS firmware rev: an ECO that needs first-article requalification, not a silent BOM swap.

## Wear-out modes to know

Arrhenius math, derating, and the worked FIT example live in §5.13. This section is the mechanism catalog: how each failure shows up in ATP and telemetry, and which triage bucket owns it (§7.12). Do not run process CAPA on a wear-out part, and do not burn FIT math on a dirty connector.

##### Infant mortality versus wear-out versus packaging.

Field failures come in three clocks, and mixing them up wastes CAPA. Infant mortality is early fails from latent defects; burn-in and HTOL screens remove them before ship (§8.2). Wear-out is gradual or sudden end-of-life in the laser or EAM under temperature, current, and optical power, projected with Arrhenius and derating (§5.13). Packaging and assembly faults (FAU align, epoxy creep, solder voids, connector wear) often dominate field returns once lasers are screened (§8.8). Destructive physical analysis (facet cross-section, EDX, FAU section) is required when the signature is ambiguous or when you need evidence for supplier 8D (§8.10).

##### Mechanism map.

Table 8.2 is the working list for laser-bearing modules and CPO/ELS paths. Customize limits in the ATP; keep the classification discipline.

<table class="book-table"><tr><th>Mechanism</th><th>Observable</th><th>ATP / telemetry</th><th>Triage bucket</th></tr><tr><td>COD (facet)</td><td>Sudden dark or hard fail; was healthy</td><td>Dark LIV; DPA facet; date-code cluster?</td><td>Reliability (COD) or mfg (ESD)</td></tr><tr><td>Gradual facet / active region</td><td>I_th up, slope down over life</td><td>LIV trend vs ship ATP; HTOL lot history</td><td>Reliability (wear-out)</td></tr><tr><td>SMSR collapse</td><td>Side modes rise; modal noise / BER</td><td>OSA SMSR vs floor at T</td><td>Reliability; watch aging</td></tr><tr><td>EAM aging (EML)</td><td>TDECQ/RLM creep at fixed bias</td><td>EAM bias sweep + DCA; bias creep log</td><td>Reliability (EAM)</td></tr><tr><td>RIN rise</td><td>BER floor up; feedback sensitive</td><td>RIN @ ORL; isolator / connector check</td><td>Perf if ORL; reliability if isolator</td></tr><tr><td>TEC / thermal control</td><td>Unlock or walk; LIV may look fine</td><td>TEC current, case T, lock status</td><td>Perf (lock) or reliability (TEC)</td></tr><tr><td>Coupling / FAU / solder</td><td>Loss step, intermittent LOS, shock-related</td><td>ORL, mate cycles, DPA FAU/solder</td><td>Manufacturability / packaging</td></tr><tr><td>Driver/TIA latch-up (ESD)</td><td>Sudden hard fail; no light, no LIV signature; supply current spikes</td><td>Supply current vs bias; JESD78 rating; date-code cluster?</td><td>Mfg (ESD) or design margin</td></tr><tr><td>Connector wear / contamination</td><td>ORL creep after repeated mate cycles; RIN floor rise</td><td>Mate-cycle count vs IEC 61300-2-2 rating; endface grade (IEC 61300-3-35)</td><td>Manufacturability / packaging</td></tr></table>
**Table 8.2.** Wear-out and packaging mechanisms versus observables. Arrhenius projection and derating for the laser rows: §5.13. Electronics stress qualification: §8.3. Connector reliability: §8.8. Field classification workflow: §7.12.

### Reading the wear-out map

Table 8.2 is a triage map, not a life calculator. Each row asks which mechanism fits the observable, which ATP or telemetry line can confirm it, and which owner should act. Arrhenius projection and derating live in §5.13; this section teaches how to classify before you CAPA.

##### COD (facet).

**Purpose.** Is the sudden dark or hard fail catastrophic facet damage, or a handling / electrical overstress that looks like it?

**Uncertainty removed.** Before classification you only know the unit stopped emitting after looking healthy. After it you know whether the facet failed, whether the lot clusters, and whether the owner is reliability (COD) or manufacturing (ESD).

**Activities.** Compare ship ATP light--current--voltage (LIV) to a dark return. Run destructive physical analysis (DPA) on the facet when the signature is ambiguous. Check date-code clustering before assuming random wear-out.

**Measurements and evidence.** A previously healthy unit that goes dark with no LIV kink history points at sudden facet failure. DPA facet damage separates *catastrophic optical damage* (COD) from a dead driver or open bond. Date-code clusters pull the case toward ESD or process escape rather than end-of-life wear.

**Exit criteria.** **Exit when** dark LIV, DPA (if needed), and cohort data place the fail in COD versus ESD/mfg, with a named owner.

**Decision unlocked.** Open reliability CAPA and life review for COD, or tighten handling / ESD screens for a manufacturing cluster.

**Risk if skipped.** You burn Arrhenius math on an ESD lot, or you run process CAPA on true facet wear-out.

##### Gradual facet / active region.

**Purpose.** Is threshold rising and slope falling on a wear-out clock that life models must cover?

**Uncertainty removed.** Before aging readouts you do not know whether a soft BER creep is bias drift, calibration, or real diode wear. After LIV trends versus ship ATP you know whether the device physics moved permanently.

**Activities.** Trend $I_\mathrm{th}$ and slope against ship baselines across HTOL intervals and field returns. Compare lot history before blaming one unit.

> **Engineering heuristic.** Compare ship ATP LIV to the return before you invent a new wear mechanism. Monitor and setpoint faults mimic diode aging until the curves disagree.

**Measurements and evidence.** Rising threshold and falling slope at fixed temperature separate diode wear from a monitor or setpoint change. HTOL lot history ties the rate to the activation energy you claim in the life model (§5.13).

**Exit criteria.** **Exit when** LIV trends show permanent wear (or clear its absence) and the rate supports or falsifies the derate and FIT claim.

**Decision unlocked.** Accept derate and replacement planning, tighten bias/temperature policy, or hold ship for life risk.

**Risk if skipped.** Soft fails look like "random BER" until the fleet hits end-of-life together.

##### SMSR collapse.

**Purpose.** Did side-mode suppression fail so modal noise or BER rises while average power still looks fine?

**Uncertainty removed.** Before spectrum checks you may chase Tx eye or Rx sensitivity for a modal problem. After OSA SMSR versus the floor at temperature you know whether single-mode purity failed.

**Activities.** Measure side-mode suppression ratio (SMSR) on an optical spectrum analyzer across temperature and age. Compare to the ATP floor and to ship records.

**Measurements and evidence.** SMSR collapse raises modal noise and BER without a simple power-drop story. Temperature-dependent SMSR loss that worsens with age is a reliability signal, not a one-time set-and-forget spec.

**Exit criteria.** **Exit when** SMSR versus temperature and age either clears the floor with margin or names the fail as modal / aging risk.

**Decision unlocked.** Tighten SMSR ATP and aging screens, derate temperature, or reject the lot / design for modal risk.

**Risk if skipped.** Intermittent BER under temperature looks like connector or SerDes noise while the laser left single-mode operation.

##### EAM aging (EML).

**Purpose.** Is the electro-absorption modulator (EAM) absorption curve shifting while the DFB LIV still looks healthy?

**Uncertainty removed.** Before bias and eye trends you may blame the laser diode for transmitter and dispersion eye closure quaternary (TDECQ) or relative level mismatch (RLM) creep. After EAM sweeps you know whether the modulator aged.

**Activities.** Hold laser bias policy fixed. Sweep EAM bias with a sampling scope / DCA. Log bias creep and TDECQ/RLM versus time and temperature.

**Measurements and evidence.** TDECQ or RLM creep at fixed optical power with a restoring EAM bias sweep points at modulator aging, not facet wear. Bias-creep logs separate slow absorption shift from a one-time calibration error.

**Exit criteria.** **Exit when** EAM bias and eye metrics either stay inside the control window across age or show a named aging rate with an owner.

**Decision unlocked.** Add EAM aging to life and ATP screens, retune bias tables, or hold EML ship for modulator risk.

**Risk if skipped.** You replace "good" DFBs while the EAM curve walks the eye closed.

##### RIN rise.

**Purpose.** Did relative intensity noise (RIN) rise because of optical return loss (ORL) / feedback, or because an isolator or source path degraded?

**Uncertainty removed.** Before quiet versus stressed ORL RIN you cannot tell performance (reflection environment) from reliability (isolator or source). After the split you know which triage bucket owns the BER floor.

**Activities.** Measure RIN at stated ORL and bandwidth. Inspect connectors and isolator path. Compare clean versus stressed floors (§4.3.1).

**Measurements and evidence.** A BER floor that tracks ORL and recovers when reflections fall is a performance / plant problem. A floor that stays high after ORL is controlled and isolator integrity fails is a reliability path.

**Exit criteria.** **Exit when** RIN@ORL and plant checks assign the floor to ORL/performance or to isolator/source reliability.

**Decision unlocked.** Fix connectors and reflection budget, or open reliability work on isolator / source packaging.

**Risk if skipped.** You derate a healthy laser for dirty plant, or you polish connectors forever on a dead isolator.

##### TEC / thermal control.

**Purpose.** Is unlock or wavelength walk a cooler / control fault while the diode LIV is still fine?

**Uncertainty removed.** Before TEC current, case temperature, and lock status you may treat every wavelength walk as laser aging. After the bisect you know whether the cooler or lock loop failed (§6.7).

**Activities.** Log TEC current, case $T$, and lock status with wavelength. Cool down and recover. Compare LIV before and after unlock events.

**Measurements and evidence.** Healthy LIV with rising TEC current, unlock flags, or $\lambda$ walk that tracks case $T$ points at thermal control. Permanent LIV shift after the same event points back at the diode.

**Exit criteria.** **Exit when** telemetry and recovery tests place the event in lock / TEC performance or in TEC hardware reliability.

**Decision unlocked.** Retune lock/thermal policy, replace TEC path, or open diode aging if LIV moved.

**Risk if skipped.** You scrap lasers for control faults, or you ignore a dying TEC until WDM unlocks fleet-wide.

##### Coupling / FAU / solder.

**Purpose.** Is the optical or mechanical attach path intermittent or stepped, rather than the semiconductor wearing out?

**Uncertainty removed.** Before mate, ORL, and DPA work you may assign shock-related LOS to laser FIT. After packaging evidence you know the owner is manufacturability.

**Activities.** Measure ORL and mate cycles. Correlate to shock or service events. Section FAU and solder when needed.

**Measurements and evidence.** Step loss, intermittent LOS, and shock correlation with clean semiconductor metrics point at fiber-array unit (FAU) align, epoxy, or solder. DPA confirms the mechanical path.

**Exit criteria.** **Exit when** packaging evidence (or a clean DPA clear) assigns the fail to attach / FAU / solder versus diode physics.

**Decision unlocked.** Open assembly CAPA, tighten attach screens, or clear packaging and return to reliability rows.

**Risk if skipped.** Life models absorb packaging escapes, and the next lot fails the same way.

##### Driver / TIA latch-up (ESD).

**Purpose.** Is the sudden hard fail electronics latch-up or ESD, with no optical LIV aging signature?

**Uncertainty removed.** Before supply-current and rating checks a dark module looks like COD. After electrical evidence you know whether the IC path failed.

**Activities.** Compare supply current versus bias. Review JESD78 / ESD ratings and date-code clusters. Confirm no light and no laser LIV signature of wear.

**Measurements and evidence.** Supply current spikes, latch-up under injection, and date-code clusters with a dark but undamaged facet path point at manufacturing ESD or design margin on the driver/TIA, not facet COD.

**Exit criteria.** **Exit when** electrical signature and rating evidence clear or confirm ESD/latch-up ownership.

**Decision unlocked.** Tighten handling and ESD screens, or reopen IC design margin (§8.3).

**Risk if skipped.** You open laser DPA on every dark return and miss a handling epidemic.

##### Connector wear / contamination.

**Purpose.** Did repeated mate cycles or endface contamination raise ORL and the RIN / BER floor without semiconductor wear?

**Uncertainty removed.** Before mate-cycle and endface grade checks soft floors look like laser aging. After IEC 61300 evidence you know the plant and packaging own the trend.

**Activities.** Count mate cycles versus IEC 61300-2-2 rating. Grade endfaces (IEC 61300-3-35). Correlate ORL creep to service actions (§8.8).

**Measurements and evidence.** ORL creep after mates, recoverable with clean/replace, and endface fails are manufacturability / packaging. Permanent semiconductor LIV or SMSR shift is not this row.

**Exit criteria.** **Exit when** mate history, ORL, and endface grade explain the floor, or when clean connectors leave a residual that returns you to RIN/reliability.

**Decision unlocked.** Change service practice, connector rating, or ATP mate screens; do not open laser life CAPA for dirty MT.

**Risk if skipped.** Fleet polish and reseat theater continues while the real limit is mate-cycle budget.

### Why triage buckets matter more than mechanism names

Classify before corrective action. Reliability rows (COD, gradual wear, SMSR, EAM, true isolator/source RIN) need life models, derate, and supplier physics work. Performance rows (ORL-driven RIN, lock/thermal control) need plant, bias, and control fixes. Manufacturing and packaging rows (ESD, FAU, solder, connector) need process, handling, and ATP screens. Mixing buckets wastes CAPA and teaches the wrong lesson to the next lot (§7.12).

Later evidence must not rewrite an earlier wrong bucket without new data. A clean facet DPA does not confirm the connector was innocent if ORL was never measured. An HTOL pass does not clear a date-code ESD cluster.

### Learning summary

COD / ESD dark fails

: Sudden dark: facet physics or electrical overstress?

Gradual LIV wear

: Threshold up, slope down: life and derate.

SMSR / EAM / RIN

: OSA vs PD+ESA (not the same instrument): which ledger?

TEC / lock

: Wavelength walk with healthy LIV: control before diode.

FAU / solder / connector

: Step loss and mate history: packaging, not FIT.

## The reliability bathtub: three failure regimes

Field failures follow three regimes with different clocks and different fixes. Mixing them wastes corrective action on the wrong mechanism.

Infant mortality (early life)

: Latent defects from manufacturing: weak solder joints, marginal laser die, contamination, firmware bugs that trip on first thermal cycle. Burns down rapidly with time. Fixed by burn-in, screening, tighter ATP, and first-article control (§8.2).

Useful life (constant rate)

: Random failures at a roughly steady FIT: cosmic-ray-induced single-event upsets, handling damage during unrelated service actions, and isolated material defects that passed all screens. Fixed by redundancy, field-replaceable modules, and design margin. Note: connector wear and contamination accumulate with mate cycles and are usage-driven degradation (§8.8), not constant-rate random failures; budget them separately from the flat-hazard FIT.

Wear-out (end of life)

: Physics-driven degradation: laser facet, active region, EAM absorption curve shift, TEC aging, epoxy creep. Onset depends on temperature, current, optical power, and time. Fixed by derating, Arrhenius-based life projection, and planned replacement intervals (§5.13).

A rising failure rate after years of service is wear-out and calls for replacement planning, not supplier 8D. A cluster of early failures on a new lot is infant mortality and calls for tighter screens. A steady trickle with no date-code correlation is useful-life random and calls for redundancy and fast repair. The triage tree in §7.12 forces this classification before corrective action starts.

## Yield analysis

Yield is not one number. It splits by stage and by failure mode, and each split points at a different owner.

Wafer / die yield

: Process-limited: waveguide loss, ring resonance spread, heater shorts, photodiode dark current. Caught at wafer probe. Owner: foundry SPC.

Assembly yield

: Packaging-limited: fiber-array attach alignment, solder voids, wirebond pull, epoxy placement. Caught at module ATP. Owner: assembly supplier.

Test yield (first-pass)

: ATP-limited: units that fail one or more acceptance criteria on first pass. May include measurement-system false rejects (gauge R&R). Owner: test engineering.

Escaped DPPM (post-screen field failures)

: Units that passed all screens but fail in the fleet. Each escape is either a preventable coverage gap (the screen exists but missed the defect) or a residual latent failure that no cost-effective screen separates from good units. Owner: quality and reliability engineering.

<table class="book-table"><tr><th>Yield stage</th><th>Main limit</th><th>First catch</th><th>Owner</th><th></th></tr><tr><td>Wafer / die</td><td>Waveguide, resonance, heater, PD dark</td><td>Wafer probe</td><td>Foundry SPC</td><td></td></tr><tr><td>Assembly</td><td>FAU align, solder, wirebond, epoxy</td><td>Module ATP</td><td>Assembly supplier</td><td></td></tr><tr><td>Test (first-pass)</td><td>ATP fails; may include false rejects</td><td>ATP station + GR\</td><td>R</td><td>Test engineering</td></tr><tr><td>Escaped DPPM</td><td>Passed screens; failed in fleet</td><td>Field RMA / triage</td><td>Quality / reliability</td><td></td></tr></table>
**Table 8.3.** Yield stages, first catch, and owner. Split escapes further in Table 8.4.

Track yield by ATP row, lot, supplier site, tester, and date code. A yield drop that correlates with one tester is likely a measurement problem. A yield drop that correlates with one supplier lot is likely a process problem. A yield drop with no observed correlation requires further investigation: verify gauge repeatability, expand stratification (shift, fixture, material lot, firmware), and test guardband or specification mismatch as hypotheses before concluding. Do not open supplier corrective action until the measurement system is cleared (§8.9).

> **Engineering heuristic.** Clear the tester with a golden unit before you escalate a supplier. Station drift masquerades as a process excursion more often than engineers admit.

> **What this usually means.** A golden unit fails on only one production station
>
> *Usually:* fixture, calibration, cable, software limit, or operator path on that station
>
> *Not:* a sudden die-level failure of every good unit that station has ever seen

## Escaped defect analysis

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
Recurrence control</code></pre>
Provisional containment, scope refinement, mechanism confirmation, and recurrence control are different actions. Apply Appendix D.9, Appendix D.12, Appendix D.16 to separate immediate hold from FA and from the ATP, sample, SPC, or telemetry change that closes the loop. Organize the spent margin with the five ledgers before naming a component (§5.19, §4.8).

An escaped defect is a unit that passed every production screen and failed in the field. Post-screen field failures split into two categories with different corrective actions:

<table class="book-table"><tr><th>Class</th><th>Meaning</th><th>Typical action</th><th>Lands in</th></tr><tr><td>Preventable coverage</td><td>Screen could have caught it</td><td>Add/tighten ATP or SPC</td><td>Escape DPPM, CAPA</td></tr><tr><td>Residual latent</td><td>No cost-effective screen</td><td>FIT / redundancy / replace</td><td>Residual FIT model</td></tr></table>
**Table 8.4.** Escape classes. Preventable rows change production; residual rows change the life model.

##### Preventable coverage escapes.

A defect that a cost-effective screen could have caught but did not, because the screen was absent, miscalibrated, or insufficiently stressed. Each one requires an ATP or process-control change. Common mechanisms in optical modules:

- **Contamination:** particles trapped during assembly that only move under thermal cycling or vibration, shifting coupling or raising ORL intermittently.

- **Marginal alignment:** fiber-attach or FAU position within spec at room temperature but outside at the thermal corner, creating a temperature-dependent loss that the ATP chamber did not run.

- **Weak solder or wirebond:** passes pull test but fatigues under repeated thermal cycling, creating intermittent opens or increased resistance.

- **Firmware corner:** a state-machine path or calibration table entry that production never exercises but the fleet hits on a specific boot sequence, temperature bin, or host interaction.

- **Packaging stress:** residual mechanical stress from underfill cure or lid attach that relaxes over time, shifting alignment or birefringence.

For each preventable escape, trace the failure signature back to the earliest point in the production flow where it could have been caught, and add or tighten the screen there.

> **Engineering heuristic.** An escape without an ATP or SPC change is unfinished work. Containment stops the bleed; the control stops the next lot.

##### Residual latent failures.

A defect that no cost-effective screen can separate from good units at the time of test. Examples include cosmic-ray-induced single-event upsets, rare material inclusions below detection limits, and process-marginal units that sit inside all guardbands but fail under a specific field combination of temperature, ORL, and neighbor load. These go into the residual FIT model, not into ATP. Document why no reasonable screen exists so the decision is auditable and revisitable as test technology improves.

## Photonic packaging and module-level failures

Fleet FIT is not only laser wear-out. Once lasers are screened and derated, module and packaging failures often dominate field returns: the part that shipped with a clean LIV still loses light after shock, humidity, or a thousand ELSFP mate cycles. Fiber attach and FAU alignment fail from shock, humidity ingress, and epoxy creep; CPO fiber-array units add assembly steps that wafer test cannot catch (§9.10). Hybrid stacks (TFLN-on-Si, InP laser on Si, flip-chip drivers) introduce solder voids, underfill cracks, and RF return-loss drift (§3.14.3). Thermal paths matter too: uncooled datacom versus liquid-cooled XPO/CPO, and TEC failure that looks like wavelength drift off grid or off ring (§3.14.3, Chapter 6).

##### Connector reliability: MPO, mating cycles, and endface quality.

Multi-fiber connectors are the highest-touch mechanical interface in the fleet: every ELSFP swap, every fiber-attach unit (FAU) rework, and every cable-plant install mates and unmates an MPO. The MPO/MT ferrule family (rectangular, 6.4 mm $\times$ 2.5 mm, guide-pin aligned, 8/12/16/24 fibers per row) is standardized in *IEC 61754-7*, split into one-fibre-row and two-fibre-row parts . That standard fixes geometry, not lifetime; lifetime comes from two companion test methods. *IEC 61300-2-2* specifies the mate/unmate cycling test connector datasheets are rated against, and *IEC 61300-3-35* grades endface scratches, pits, and debris into pass/fail zones on the fiber core and cladding . TIA-568.3 sets 500 cycles as the structured-cabling mating-durability floor; MPO/MTP-class connectors in practice are commonly rated well above 1000 cycles, but that headroom erodes fast with the wrong cleaning discipline (§7.2.2).

Three practical consequences follow for an ELSFP or CPO fiber-attach program. First, ORL creep is a mating-cycle and cleaning problem before it is a laser problem: a rising RIN floor after repeated ELS swaps (Table 8.2) is diagnosed with an IEC 61300-3-35-style endface inspection, not a laser FA request. Second, mate-cycle count belongs in the same telemetry you already read for CMIS and DDM (§7.8); track it per connector, not per module, since a connector can outlive several module swaps or vice versa. Third, write the mating-cycle and endface-grade limits into the ATP explicitly (Table 8.6) rather than inheriting a generic MPO datasheet number: an ELS bank that hot-swaps weekly reaches a 500-cycle floor in under ten years, and a CPO fiber array that is field-serviced more aggressively reaches it faster still.

ELSFP cycling adds connector wear and contamination that raise ORL (§7.2.2, §5.14); the mating-cycle and endface-grade limits above are exactly the numbers that turn "the connector feels loose" into an ATP line item instead of a guess.

Destructive physical analysis (cross-section, EDX) and structured 8D/CAPA with suppliers close the loop from RMA to design rule (§8.10, §7.12). Without that loop, packaging FIT gets mis-attributed to laser Arrhenius models and the wrong part gets redesigned.

## Production test at volume

> **Before production**
>
> ATP $\cdot$ SPC $\cdot$ telemetry $\cdot$ supplier gates $\cdot$ monitoring owners $\cdot$ RMA-to-ATP feedback (Appendix D.17).

### Test time is a cost, coverage is a risk

Every second in the acceptance test plan (ATP) times millions of units is line capacity and real money. Every skipped measurement creates uncontrolled escape risk; it is not automatically a field DPPM event (§8.1). The core tension in high-volume manufacturing is how much coverage you buy per second. The expensive optical steps are thermal soak and corner runs, TDECQ on a sampling scope, BER dwell long enough to trust a low pre-FEC target, laser burn-in, and mate-cycle stress on ELSFP connectors. Some screens are statistical (sample burn-in from a lot, audit TDECQ on a subset). Safety and enable-sequence faults usually require 100% coverage. For source-level production where LIV or SMSR are directly available and correlated to escape risk, they may be 100% screens. For closed modules, use the validated module-level proxy or a documented sampling plan (§7.8, §5.15, Table 8.6).

> **Tradeoff.** More production screening vs cost
>
> *Improves:* Escape detection and earlier catch
>
> *Worsens:* Cycle time, tester cost, and false rejects that burn good units
>
> *When acceptable:* When a named mechanism has a cheap, reliable detection signature
>
> *Experienced decision:* Choose the cheapest control that reliably detects the failure mode: 100% ATP, sample audit, SPC, or supplier process control.

> **Tradeoff.** Burn-in vs cycle time
>
> *Improves:* Infant-mortality removal when the screen separates
>
> *Worsens:* Line capacity, cost, and stress on healthy units
>
> *When acceptable:* When escape data and mechanism justify the screen on this population
>
> *Experienced decision:* Keep burn-in only while it buys escapes you cannot catch cheaper elsewhere.

### Where the test happens: wafer, die, module, system

Push defect detection as far upstream as correlation allows. Wafer-level or PIC probe catches process shifts (waveguide loss, ring resonance drift, bad heaters) before fiber attach and packaging spend. Killing a bad die at probe is orders of magnitude cheaper than an RMA (§8.8). Module ATP is the full functional test: optical power class, TDECQ or proxy, sensitivity spot-check, CMIS bring-up, and connector/ORL on ELS parts. System or golden-host bring-up catches interop: media type, firmware rev, equalizer defaults, and the corners in §7.9. Wafer test cannot catch fiber attach, FAU alignment, epoxy creep, or connector wear. Those failures must survive to module ATP and, for some signatures, to fleet telemetry (§7.12).

### ATE-to-bench correlation and gauge R&R

Production testers are built for speed and cost, not lab fidelity. Correlation asks whether ATE TDECQ, OMA, or sensitivity tracks the DCA/BERT reference within a known offset and spread. Teach the measurement system explicitly:

Repeatability

: Same station, operator, and unit.

Reproducibility

: Across stations, shifts, and operators.

Bias

: Production station versus reference lab.

False reject / false accept

: Guardband from measurement uncertainty.

Golden-unit stability and station drift

: Catch a stale golden or drifting ATE before it becomes a yield cliff or DPPM escape.

Keep a golden module (and golden laser subassembly for ELS), run gauge R&R across testers and shifts, and correlate CMIS monitors to bench instruments the same way you correlate TDECQ (§7.8). If the ATE and the DCA disagree, fix the correlation before you argue with the supplier about spec.

### Screens, guardbanding, and SPC

Burn-in (infant-mortality screen) and HTOL (life/mechanism evidence) trade different risks against test time and cost (§8.4, §8.2). Test limits are usually guardbanded tighter than the customer spec so field DPPM stays inside target under drift. SPC control charts on LIV, SMSR, RIN, TDECQ, and mate-cycle yield by lot, site, and date code catch a process shift before it becomes an 8D (§8.10). Production test is a yield, DPPM, and cost trade under a fixed reliability target. It is not a pass/fail checkbox after the optics already work on a golden bench.

## Supplier execution playbook

The supplier path is milestones, performance targets, quality, and manufacturability triage. That is not a soft skill. It is a concrete contract: requirements, gates, acceptance tests, process control, and corrective action when a lot goes wrong.

> **Why experienced engineers care about production lots?**
>
> Because manufacturing escapes almost always correlate with process history. Lot, date code, site, and firmware tags often beat another night on one returned unit.

> **Engineering heuristic.** Ask for the process change list before you invent new physics. Most lot escapes sit next to a real change record.

> **Tradeoff.** Second source vs qualification burden
>
> *Improves:* Supply resilience and pricing leverage
>
> *Worsens:* Validation, interop matrix, and manufacturing differences
>
> *When acceptable:* When supply or concentration risk exceeds the qual cost
>
> *Experienced decision:* Qualify second sources based on risk and evidence, not ideology.

Lab hero samples versus manufacturable yield: same tradeoff as in Chapter 7. Optimize the system you can build, not the best bench unit.

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
Production validation is replayable and decision-oriented (Appendix D.13).

##### NPI gates and exit criteria.

New product introduction (*NPI*) gates are the manufacturing face of the validation ladder. Table 8.5 is the usual stage map. Write exit criteria a supplier can fail without ambiguity, not slogans. EVT/DVT/PVT/MP are stage names, not a calendar; dates and sample sizes belong in the program plan.

<table class="book-table"><tr><th>Gate</th><th>Main question</th><th>Evidence required</th><th>Decision unlocked</th></tr><tr><td>EVT</td><td>Does it operate at all?</td><td>First light; CMIS bring-up; basic LIV/SMSR/RIN; one link closes BER</td><td>Continue / redesign integration</td></tr><tr><td>DVT</td><td>Does it meet spec across corners?</td><td>Full ATP at T/V; prod-rep corners; stress plan + FIT model frozen</td><td>Enter qual / PVT / hold</td></tr><tr><td>Qual</td><td>Env / reliability evidence ready?</td><td>Named mechanisms; sample plan; confidence (sec:tree-qual-evidence)</td><td>Enter PVT / hold</td></tr><tr><td>PVT</td><td>Is it buildable at yield?</td><td>Multi-lot yield; SPC; burn-in escape; FAIR; production-host bring-up</td><td>Enter pilot / hold</td></tr><tr><td>Pilot</td><td>Do assumptions hold in a bounded field trial?</td><td>Known serials/lots; enhanced telemetry; exit/rollback criteria</td><td>Open MP / restrict</td></tr><tr><td>MP</td><td>Is quality sustained?</td><td>Steady DPPM; owned RMA Pareto; ECO control; fleet feedback</td><td>Keep shipping / CAPA / restrict</td></tr></table>
**Table 8.5.** NPI gates as a decision map. Pilot sits between PVT and MP; MP is sustained production plus fleet feedback, not "fleet monitoring" alone.

##### EVT (engineering validation test).

**Purpose:** demonstrate the design can operate, not that it is ready for fleet corners. **Uncertainty removed:** basic integration and first-order laser health on engineering samples. **Activities:** CMIS bring-up sequence (§7.9), first light, LIV/SMSR/RIN on samples, one link to a usable BER. **Exit:** ready state, light, and a closing BER on a known-good path. **Decision:** continue to DVT, or debug integration / redesign. **Risk if skipped:** DVT matrices run on parts that never reliably link.

##### DVT (design validation test).

**Purpose:** demonstrate the requirements slice across temperature, voltage, and production-representative corners, with a frozen life plan. **Uncertainty removed:** whether margin and named stress coverage close before volume tooling. **Activities:** full ATP at $T$/$V$, prod-rep corners (§7.9), TDECQ/OMA/sensitivity, freeze GR-468-class stress plan and FIT model. **Exit:** corner closures plus agreed life evidence plan. **Decision:** enter PVT, hold, or redesign. **Risk if skipped:** PVT yield work hides missing corner coverage.

##### PVT (production validation test).

**Purpose:** demonstrate the supplier can build the qualified result at yield on production tooling and hosts. **Uncertainty removed:** lot variation, process control, and ATP escape coverage. **Activities:** multi-lot yield versus ATP, live SPC, burn-in escape rate, FAIR on production tooling, bring-up on the production host. **Exit:** yield and SPC support open volume. **Decision:** open MP volume or hold for process CAPA. **Risk if skipped:** shipping PVT material without frozen ATP limits seeds field NFF and dishonest FIT arguments (§7.12).

##### Pilot (controlled field confirmation).

**Purpose:** confirm qual assumptions on a bounded field population before open volume. **Evidence:** known serials and lots, representative hosts and environments, enhanced telemetry, success and rollback criteria, defined observation duration (§7.1.10). **Exit:** pilot criteria met or restrict/reject. **Decision:** open MP or hold.

##### MP (mass production).

**Purpose:** sustain quality after ramp. **Uncertainty removed:** whether DPPM, RMA ownership, and ECO control remain stable. **Activities:** track DPPM, own RMA Pareto by mechanism, control ECOs on CMIS/firmware and process. **Exit:** steady quality with clear owners. **Decision:** keep shipping, restrict, or open CAPA. **Risk if skipped:** silent process drifts until the fleet trips.

##### Why NPI order matches the ladder.

EVT maps to engineering bring-up. DVT covers characterization, margin, interoperability, and frozen stress intent after architecture feasibility. Qualification owns mechanism-based reliability evidence. PVT is manufacturing validation. Controlled pilot is bounded field confirmation. MP is sustained volume with SPC/ECO/RMA control; fleet monitoring and feedback continue after MP (§7.1.11, §7.1.10, §7.1.12, §7.1.13). Do not use an EVT hero sample as PVT evidence, and do not treat MP as fleet monitoring alone.

Hold a gate if the exit data are missing.

##### Requirements and ATP are the contract.

ATP and the requirements doc are the contract. Write both and keep them versioned together:

> **Engineering heuristic.** If a requirement has no ATP or sample line, it is a wish. If an ATP line has no requirement, it is cost without a decision.

1.  **Requirements / PRD slice for the laser path:** fill Table 5.4, §5.6 (power class, grid, RIN@ORL, SMSR, derating, CMIS, FIT). Version it with the ATP.

2.  **Acceptance test plan (ATP):** the measurable tests that prove those requirements on every ship lot (or on a defined sample). Map each ATP line to a GR-468 or design-validation stress where life is claimed (§8.2).

Table 8.6 is a working ATP checklist for an EML pluggable or an ELSFP CW module. Customize limits from the datasheet and the link budget; do not invent numbers in the ATP itself.

<table class="book-table"><tr><th>Item</th><th>Method</th><th>Control class</th><th>Pass intent</th><th>Ties to</th></tr><tr><td>LIV (I_th, slope, kink)</td><td>SMU + power meter</td><td>100\% ATP (source) / module proxy</td><td>kink-free bias window</td><td>wear-out, derate</td></tr><tr><td>SMSR</td><td>OSA</td><td>100\% ATP (source) / lot sample</td><td>single-mode vs.\ floor</td><td>modal noise</td></tr><tr><td>Intrinsic RIN</td><td>PD + ESA</td><td>Lot sample / FA</td><td>quiet source floor</td><td>BER floor budget</td></tr><tr><td>Stressed RIN_xOMA</td><td>PD + ESA @ ORL</td><td>Lot sample / 100\% if escape</td><td>stressed Tx metric</td><td>named PMD</td></tr><tr><td>Wavelength / grid</td><td>OSA / wavemeter</td><td>100\% ATP or sample</td><td>channel ID</td><td>WDM lock</td></tr><tr><td>Optical power class</td><td>power meter</td><td>100\% ATP</td><td>class met</td><td>link budget</td></tr><tr><td>EAM / TDECQ (EML)</td><td>bias + DCA</td><td>Lot sample / audit</td><td>ER, RLM, TDECQ</td><td>Tx quality</td></tr><tr><td>CMIS / TWI bring-up</td><td>host / CMIS tool</td><td>100\% ATP</td><td>state machine</td><td>telemetry</td></tr><tr><td>Connector / ORL</td><td>mate + ORL meter</td><td>Periodic audit / sample</td><td>cycles + endface</td><td>packaging</td></tr><tr><td>Burn-in (infant)</td><td>production screen</td><td>100\% or lot sample</td><td>infant culled</td><td>not HTOL life</td></tr><tr><td>HTOL life evidence</td><td>accelerated life</td><td>Qualification only</td><td>mechanism + FIT claim</td><td>GR-468</td></tr><tr><td>Driver/TIA ESD</td><td>JESD47 report</td><td>Qualification / audit</td><td>rating on file</td><td>IC reliability</td></tr><tr><td>Thermal class</td><td>chamber</td><td>Lot sample / SPC</td><td>LIV/RIN/CMIS pass</td><td>derate</td></tr><tr><td>Process monitors</td><td>SPC charts</td><td>SPC / process</td><td>drift detection</td><td>escape prevention</td></tr><tr><td>Fleet cohort metrics</td><td>telemetry</td><td>Fleet telemetry</td><td>trend / alarm</td><td>recurrence</td></tr></table>
**Table 8.6.** Control checklist for laser-bearing modules (EML or ELSFP). Control class separates 100% ATP, lot sample, audit, qualification-only, SPC, and fleet telemetry. Intrinsic RIN and stressed $\mathrm{RIN}_x\mathrm{OMA}$ are different metrics.

### Reading the ATP checklist

Each ATP line is a screen with a purpose, not a museum of instruments (Table 8.6). Limits come from the requirements slice. The notes below teach the rows that most often mis-classify escapes; the rest are Risk-if-omitted only.

##### LIV ($I_\mathrm{th}$, slope, kink).

Without ship LIV you cannot separate a dead bias window from later eye or BER fails, and wear-out triage has no baseline (§5.7, §8.4). **Exit when** the unit shows a kink-free window inside the bias policy. **Decision:** ship, reject, or tighten bias/derate. **Risk if omitted:** kinked diodes age into soft BER with nothing to compare.

##### RIN (intrinsic + stressed ORL).

Quiet-bench RIN does not prove field reflection survival (§4.3.1). **Exit when** quiet and stressed RIN meet the BER-floor budget. **Decision:** ship, require isolation, or reject. **Risk if omitted:** clean-bench parts floor under field ORL.

##### EAM bias / chirp (EML).

Average power can pass while Tx quality fails (§7.4). **Exit when** ER, RLM, and TDECQ meet limits inside the bias window. **Decision:** ship, retune tables, or reject. **Risk if omitted:** temperature and age close the eye after ship.

##### Connector / ORL.

Mate life and endface grade are packaging screens, not laser FIT (§8.8, §5.14). **Exit when** cycles and grade meet the claimed service life. **Decision:** ship, derate mate life, or reject packaging. **Risk if omitted:** service raises ORL and RIN after ship.

##### Other ATP rows (retrieve from the table).

SMSR

: **Risk if omitted:** temperature-dependent side modes look like random link errors.

Wavelength / grid

: **Risk if omitted:** WDM unlock appears as host or DSP bugs (Chapter 6).

Optical power class

: **Risk if omitted:** under-powered ports fail reach after other screens pass.

CMIS / TWI

: **Risk if omitted:** fleet triage has no trustworthy dump on the first RMA.

Burn-in

: **Risk if omitted:** early-life clusters hit by date code (§8.2).

Driver/TIA ESD

: **Risk if omitted:** dark modules from handling are mis-labeled as laser COD (§8.3).

Thermal class

: **Risk if omitted:** room-temperature ATP ships parts that fail in the sled.

### Why these ATP lines stay coupled

LIV, SMSR, and wavelength protect semiconductor and channel identity. RIN and connector/ORL protect the reflection environment. EAM/DCA protects Tx quality when the path is EML. CMIS protects field evidence. Burn-in and ESD protect infant mortality and handling. Thermal class protects the derate claim. No single line substitutes for another: a power-class pass does not clear a RIN floor, and an HTOL pass does not clear a CMIS state-machine bug.

**Exit for the ATP as a whole:** every ship lot (or defined sample) has traceable pass data against versioned limits tied to the requirements slice. **Decision unlocked:** ship, hold, or reopen DVT limits. **Risk if lines are slogans:** field escapes with no ATP hook.

### Learning summary

LIV / SMSR / wavelength

: Source and channel health at ship.

RIN / ORL / connector

: Noise and plant survive service.

EAM / power / thermal

: Eye, budget, and case $T$ close.

CMIS / burn-in / ESD

: Telemetry, infant mortality, and electronics.

##### Incoming QC and SPC.

Qual lots are small. Production catches drift that qual missed.

- **Incoming:** sample or 100% screen against a subset of the ATP (at least power, CMIS, and a laser LIV/SMSR sample). Track DPPM by date code and site.

- **SPC**: control charts on $I_\mathrm{th}$, slope, SMSR, Tx power, and burn-in fallout. A process shift is a hold, not a hope.

- **First-article / FAIR:** when tooling, epi, or assembly site changes, rerun a defined FAIR package before open PO volume. Treat CMIS firmware revs the same way as process changes.

##### Excursions: 8D / CAPA.

When a lot fails ATP, incoming, or field triage lands in the manufacturability bucket (§7.12), run structured corrective action:

1.  **Contain:** quarantine WIP and ship holds; identify suspect date codes in the fleet.

2.  **Evidence pack:** failing ATP rows, CMIS dumps, LIV/SMSR/RIN plots, DPA photos (facet, solder, FAU cross-section) compared to a golden unit.

3.  **8D / CAPA**: confirmed mechanism with the supplier (process step, material lot, firmware), corrective action, and preventive control (ATP tighten, SPC limit, poke-yoke).

4.  **Verify closure:** containment confirmed effective; mechanism reproduced or physically confirmed; corrective action removes the failure; no unacceptable regression introduced; production control detects recurrence; next lots remain stable; field cohort trend improves. Re-run FAIR alone is not enough for environmental, intermittent, or fleet-specific escapes (Appendix D.16).

Do not close 8D on "operator error" without a control that would have caught it at ATP or in process. If FA shows laser wear-out on a young unit, it may be a reliability screen gap, not a supplier process bug; reclassify with §7.12 before you argue FIT.

##### Milestone hygiene with partners.

Align the partner calendar to gates, not slideware:

- freeze requirements before DVT samples are built;

- freeze ATP limits before PVT yield is claimed;

- freeze FIT/$E_a$ assumptions before reliability marketing numbers ship;

- require ECO notice on laser die revision, TEC vendor, FAU epoxy, driver/TIA silicon revision (§8.3), and CMIS firmware.

Your job in those meetings is to name the measurement that would kill the gate. If nobody can point to an ATP row or a corner, the milestone is not real.

**Key idea.** Reliability at scale is mechanism discipline plus supplier gates. Classify with the wear-out map (Table 8.2) before FIT or 8D. Laser wear-out uses Arrhenius and GR-468; driver/TIA uses JESD47 and ESD ratings (§8.3); connectors use mate-cycle and endface limits (§8.8). Gate suppliers on ATP, multi-lot SPC, and FAIR. Do not run process CAPA on wear-out, or FIT math on a dirty connector.

## From component FIT to fabric availability

The FIT arithmetic in §5.13 gives a rate: about $0.6$ laser failures per day for a fleet of $5\times10^5$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin (§5.14), but it does not say what a failure costs or how a running job survives one. Two facts turn a per-component rate into a fabric problem.

First, a training or large inference job is synchronous. A collective (§9.7) waits for its slowest member, so a single dead or slow link stalls the whole group, not just one endpoint (§9.6). A link that flaps for a second is a stall for every accelerator in that collective. The optical FIT the earlier chapters budget therefore matters out of proportion to its share of the parts count.

Second, at cluster scale failures are continuous, not rare. Meta's published Llama 3 run is the clearest public data point: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . GPU and HBM3 faults dominated at close to half; network switch and cable faults were 35 events, 8.4% of the total. The optical link is a minority of hard job stops, but 8.4% of a failure every three hours is still tens of network events per run, and the ELS, module, and connector FIT this chapter budgets (§8.1, §8.8) lands in exactly that bucket.

So the design question shifts. It is no longer "how reliable is one link" but "how does a fabric of $10^5$ links keep a job running through a failure every few hours." The answers are architectural, and the optical engineer feeds each one.

Redundancy and rails.

: Rail-optimized topologies (§9.2) already give parallel planes; dual-plane and dual-ToR designs let a lost link degrade bandwidth instead of dropping an endpoint. Redundancy multiplies the link and laser count, which feeds straight back into the FIT budget: more resilience is more parts that can fail.

Detection and reroute.

: Transient faults stay below the job. KP4 FEC (§3.12) absorbs the error bursts a marginal link throws; link-level retry and sub-second link-flap detection plus adaptive routing steer traffic off a degraded link before the scheduler notices. Vendor fabrics (NVIDIA Spectrum-X and Quantum, Broadcom Tomahawk) advertise adaptive or "cognitive" routing and link-level retry for this. Treat the specifics as vendor orientation, but the mechanism is why transient optical faults rarely reach the hard-stop bucket above.

Topology reconfiguration.

: When a link or rack dies for good, an optical circuit switch re-wires the topology around it in milliseconds, so the scheduler routes around the dead node instead of stalling the pod (§9.9) . Component FIT still applies; the fabric survives each failure by re-wiring optically.

Sparing and field service.

: Hot spare nodes and lanes cover the interval between failure and repair. Field-replaceable external lasers (§5.14) make a dead laser a faceplate swap rather than a fabric outage, which is the architectural reason ELS decouples laser FIT from switch FIT. The connector mating-cycle and endface budget (§8.8) sets how many of those swaps the plant survives.

The cost of a failure closes the loop. A hard interruption is lost compute plus the time to detect, reroute or reschedule, and restart from the last checkpoint. Fast detection and reroute shrink that lost time, which is the fabric-level reason the module work in this chapter pays off: derating (§5.13), burn-in and screens (§8.2), and a tight ATP (§8.10) lower the failure rate, and a resilient fabric lowers the cost of each failure that slips through. The two multiply.

## Engineering lens

### How it works

At fleet scale, reliability and manufacturability are design constraints: a modest per-part FIT times millions of parts is a steady stream of failures. The chapter's qualification, yield, and supplier discipline all aim at keeping that stream small and classifiable.

### How it is measured

Reliability is measured as a distribution over stress and time. Qualification records failures by mechanism, stress, lot, and sample history. Production records yield, fallout by ATP row, measurement distributions, gauge repeatability, and escaped defects per million. Fleet data add install age, temperature, firmware, supplier lot, return code, and no-fault-found rate. Keep the chain from wafer or die measurement through module ATP to field return so a drift can be traced to its first observable point (§8.9, §8.10, §7.12).

### How it fails

Programs fail at scale through wear, variation, and escapes. Wear shifts a unit after ship. Variation produces a weak tail across wafer, lot, site, or assembly line. An escape is a defect the current screen cannot see or a control that was not run. Yield can drop because the product changed, the process moved, incoming material moved, calibration changed, or the tester moved. Do not open supplier corrective action until the measurement system is cleared.

\> \*\*Failure mode: Yield drop\*\* \> \> \*\*Symptoms.\*\* First-pass yield falls from its stable baseline, often on one ATP row, tester, lot, or shift. \> \> \*\*Likely causes.\*\* Process drift, supplier-lot variation, assembly change, calibration or fixture drift, software revision, or a changed guardband. \> \> \*\*Measurements.\*\* Pareto by test and lot, golden-unit history, gauge repeatability, station correlation, incoming data, and destructive analysis on selected failures. \> \> \*\*Mitigations.\*\* Contain suspect material, clear the tester, identify the first changed input, correct it, and verify with a controlled lot before release.

### How it is debugged

For a yield fall, freeze software, limits, and suspect material. Split by tester, shift, lot, supplier site, and ATP row. Golden unit across stations; failing unit on a reference bench. Station-follows means repair the measurement system; unit-follows means upstream process and mechanism FA. Contain first, confirm second, change the process third, verify on fresh data.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* Module yield fell sharply after a supplier lot change. \> \> \*\*Investigation.\*\* The failure Pareto pointed to one-lane TDECQ. Golden units passed all stations, and failed units kept the bad lane on the reference bench. Cross-sections showed a shifted fiber-array attach. \> \> \*\*Finding.\*\* The electrical path and testers were stable. \> \> \*\*Root cause.\*\* An assembly fixture change moved one fiber row outside its coupling window. \> \> \*\*Resolution.\*\* The lot was held, the fixture was restored, first-article coupling checks were tightened, and the supplier control plan was revised.

## Interview takeaway

**Key idea.** Production readiness joins mechanism-based qualification, a stable measurement system, controlled supplier changes, and field data that preserve lot history. When yield or fleet health moves, contain the population, clear the test system, find the first changed input, and verify the corrective control with new data.

Junior mistake: treat zero fails in a small HTOL lot as a FIT claim, or escalate a supplier before the measurement system is cleared (§8.2, Chapter 10, Appendix B).

##### Three questions to test yourself.

1.  Why does qualification on a small sample not guarantee field reliability?

2.  Yield dropped from 95% to 70% on one ATP row. What are your first three actions?

3.  Which corrective action changes a control so the same defect cannot escape again?


<div class="nav-links">
  <a href="ch7-optical-validation">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch9-ai-datacenter-networking">Next &rarr;</a>
</div>
