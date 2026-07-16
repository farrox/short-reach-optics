---
layout: default
title: "Ch 8: Reliability and manufacturing at scale"
---

# Reliability and manufacturing at scale

A link that closes in the lab can still fail the business case if lasers die in the field or suppliers cannot hold yield. At gigawatt, multi-generation scale, reliability and manufacturability stop being afterthoughts and become design constraints: they decide whether you put the laser on the ASIC package or in a replaceable module, how hard you derate, and what ATP language you freeze with partners. This chapter covers the vocabulary of failure at scale, the qualification flows that project field life, and the supplier-execution work these systems demand.

## The language of scale: FIT and DPPM

Fleet arguments need two different numbers. One is about life in the field; the other is about quality at the factory door.

FIT (failures in time)

: failures per $10^{9}$ device-hours. Multiply a per-laser FIT by the number of lasers in a fleet and by hours to estimate failures per day.

DPPM (defective parts per million)

: the manufacturing-quality counterpart, measured at incoming or outgoing inspection.

[^18]

## Qualification flows

Optoelectronics inherited a common qualification language from telecom: *Telcordia GR-468-CORE*. The core stress tests still show up on every laser and module program:

- HTOL (high-temperature operating life) and burn-in.

- Temperature cycling and damp heat.

- Electrostatic-discharge and mechanical stress.

*Arrhenius* acceleration underpins life projection: raising temperature accelerates wear-out by a factor set by the activation energy, so a bounded high-temperature test projects years of field life. Screening (burn-in) removes infant-mortality parts before deployment.

##### GR-468 in practice.

Telcordia GR-468-CORE is the common qualification language for optoelectronic modules and discrete lasers. For optical engineers the actionable pieces are test-plan alignment (map your ATP to GR-468 stress sequences such as HTOL, temperature cycle, damp heat, and ESD so supplier and customer agree on pass/fail), activation energy (FIT projections use Arrhenius acceleration; document $E_a$ and confidence bounds when converting 1000-hour HTOL to field years), sample-size humility (qualification lots are small; production SPC catches drift that qual missed, [8.2](#tab:npi)), and boundary clarity: qualify the laser die, the hermetic package, and the module assembly separately when failures split across those boundaries ([\[sec:photonic-packaging,sec:laser-aging,sec:elsfp\]](#sec:photonic-packaging,sec:laser-aging,sec:elsfp)).

##### GR-1221: the passive-component companion.

GR-468 covers active optoelectronics. Its companion, *Telcordia GR-1221-CORE* (Generic Reliability Assurance Requirements for Passive Optical Components), covers the parts GR-468 does not: connectors, fiber couplers, WDM filters and MUX/DEMUX, splitters, and isolators . It uses the same style of stress sequence (damp heat, temperature cycling, mechanical, and aging tests) but scores pass/fail on insertion loss and return loss rather than on LIV. A short-reach link that leans on an on-package or blind-mate MUX and on external multi-wavelength sources carries a passive reliability budget that lives in GR-1221, not GR-468 ([\[sec:connector-reliability,ch:wdm\]](#sec:connector-reliability,ch:wdm)). Split the qual the same way you split the FIT: active laser die under GR-468, silicon under JESD47, passive optics under GR-1221.

##### ATP sketch: EML module or ELSFP.

A short acceptance sketch lives with the qual hooks in [5.9](#sec:elsfp); the full ATP-as-contract, SPC, and 8D workflow is in [8.7](#sec:supplier-exec). Failures that pass qual but fail field usually sit in derating policy or connector contamination ([\[sec:laser-aging,sec:fleet-triage\]](#sec:laser-aging,sec:fleet-triage)).

## Electronics reliability: driver, TIA, and DSP silicon

GR-468 covers the optoelectronic parts of the link: the laser die, the photodiode, and the hermetic or non-hermetic package around them. The modulator driver, TIA, retimer, and DSP ([\[sec:drivers,sec:pd-tia\]](#sec:drivers,sec:pd-tia)) are ordinary CMOS or SiGe BiCMOS ICs, and they wear out and fail by a different, better-documented set of mechanisms. Treat them with the semiconductor industry's own qualification language, not with Arrhenius laser-aging math borrowed from [5.8](#sec:laser-aging).

##### JESD47: the silicon-side GR-468.

JEDEC JESD47 is the baseline stress-test-driven qualification flow for a new IC, a device family, or a process change: temperature cycling, HTOL, HTSL (high-temperature storage life), autoclave or HAST (highly accelerated stress test) for moisture, and mechanical shock and vibration . It plays the same role for driver and TIA silicon that GR-468 plays for the laser: a common list of stresses that a supplier runs once and a customer accepts instead of renegotiating a qual plan on every design win.

##### ESD and latch-up: failure modes GR-468 does not test.

Two mechanisms are specific to ICs and absent from the laser-side wear-out map in [8.1](#tab:wearout-map):

ESD

: a discharge event during handling or assembly damages a gate oxide or junction. Component-level classification uses the human-body model (HBM) and charged-device model (CDM) test standards, *ANSI/ESDA/JEDEC JS-001* and *JS-002* . A driver or TIA datasheet HBM/CDM rating is the number that protects the part on the factory floor, at fiber-attach and wire-bond stations where a laser die is also exposed.

Latch-up

: a parasitic thyristor structure in CMOS turns on under an overvoltage or current-injection event and holds a low-impedance path until power is cycled. *JESD78* defines the overvoltage and $\pm100$ mA current-injection test that classifies susceptibility by supply and signal pin . A latched driver IC can look like a dead laser on the bench (no light, no LIV signature) until you check the supply current instead of the optical path.

Both mechanisms are 100%-screen or design-margin items, not something you project with an activation energy. If a driver fails ESD or latch-up in the field, that is a manufacturability or design-margin bucket item ([7.10](#sec:fleet-triage)), not a wear-out FIT argument.

##### AEC-Q100: a borrowed grade, not a requirement.

*AEC-Q100* is the automotive industry's qualification standard for ICs, built on the same JEDEC JESD47/JESD22 stress methods with tighter ESD targets and named temperature grades from Grade 3 ($-40$ to $85$°C) up to Grade 0 ($-40$ to $150$°C) . Datacenter optics does not require Q100; the fleet lives in a controlled data hall, not an engine bay. It is still a useful signal: a driver, TIA, or retimer die that also ships in an automotive part number typically carries a published Q100 grade, and that grade is a fast proxy for the ESD/latch-up margin and temperature-cycle depth behind the datasheet, without re-running the qual plan yourself.

##### Where this lands in the ATP.

Fold IC-level qual into the same acceptance and SPC structure used for the laser ([\[tab:atp-laser,sec:supplier-exec\]](#tab:atp-laser,sec:supplier-exec)): require the supplier's JESD47 qual report and HBM/CDM/latch-up ratings for driver and TIA die at DVT, add an ESD handling audit to the incoming-QC checklist alongside laser LIV/SMSR sampling, and treat a driver/TIA silicon revision the same way you treat a laser die revision or a CMIS firmware rev: an ECO that needs first-article requalification, not a silent BOM swap.

## Wear-out modes to know

Arrhenius math, derating, and the worked FIT example live in [5.8](#sec:laser-aging). This section is the mechanism catalog: how each failure shows up in ATP and telemetry, and which triage bucket owns it ([7.10](#sec:fleet-triage)). Do not run process CAPA on a wear-out part, and do not burn FIT math on a dirty connector.

##### Infant mortality versus wear-out versus packaging.

Field failures come in three clocks, and mixing them up wastes CAPA. Infant mortality is early fails from latent defects; burn-in and HTOL screens remove them before ship ([8.2.0.0.1](#sec:gr468)). Wear-out is gradual or sudden end-of-life in the laser or EAM under temperature, current, and optical power, projected with Arrhenius and derating ([5.8](#sec:laser-aging)). Packaging and assembly faults (FAU align, epoxy creep, solder voids, connector wear) often dominate field returns once lasers are screened ([8.5](#sec:photonic-packaging)). Destructive physical analysis (facet cross-section, EDX, FAU section) is required when the signature is ambiguous or when you need evidence for supplier 8D ([8.7](#sec:supplier-exec)).

##### Mechanism map.

[8.1](#tab:wearout-map) is the working list for laser-bearing modules and CPO/ELS paths. Customize limits in the ATP; keep the classification discipline.

[]

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Mechanism                        Observable                                                            ATP / telemetry                                                            Triage bucket
  -------------------------------- --------------------------------------------------------------------- -------------------------------------------------------------------------- --------------------------------------
  COD (facet)                      Sudden dark or hard fail; was healthy                                 Dark LIV; DPA facet; date-code cluster?                                    Reliability (COD) or mfg (ESD)

  Gradual facet / active region    $I_\mathrm{th}$ up, slope down over life                              LIV trend vs ship ATP; HTOL lot history                                    Reliability (wear-out)

  SMSR collapse                    Side modes rise; modal noise / BER                                    OSA SMSR vs floor at $T$                                                   Reliability; watch aging

  EAM aging (EML)                  TDECQ/RLM creep at fixed bias                                         EAM bias sweep + DCA; bias creep log                                       Reliability (EAM)

  RIN rise                         BER floor up; feedback sensitive                                      RIN @ ORL; isolator / connector check                                      Perf if ORL; reliability if isolator

  TEC / thermal control            Unlock or $\lambda$ walk; LIV may look fine                           TEC current, case $T$, lock status                                         Perf (lock) or reliability (TEC)

  Coupling / FAU / solder          Loss step, intermittent LOS, shock-related                            ORL, mate cycles, DPA FAU/solder                                           Manufacturability / packaging

  Driver/TIA latch-up (ESD)        Sudden hard fail; no light, no LIV signature; supply current spikes   Supply current vs bias; JESD78 rating; date-code cluster?                  Mfg (ESD) or design margin

  Connector wear / contamination   ORL creep after repeated mate cycles; RIN floor rise                  Mate-cycle count vs IEC 61300-2-2 rating; endface grade (IEC 61300-3-35)   Manufacturability / packaging
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Wear-out and packaging mechanisms versus observables. Arrhenius projection and derating for the laser rows: [5.8](#sec:laser-aging). Electronics stress qualification: [8.3](#sec:ic-reliability). Connector reliability: [8.5.0.0.1](#sec:connector-reliability). Field classification workflow: [7.10](#sec:fleet-triage).

*Catastrophic optical damage* (COD) is the sudden facet failure under optical or electrical overstress. Gradual facet and active-region degradation move threshold and slope on a slower clock. EAM aging shifts the absorption curve and shows up as transmitter and dispersion eye closure quaternary (TDECQ) or RLM drift before the DFB LIV looks dead. TEC and lock failures mimic optical wear-out until you bisect heater versus laser ([6.7](#sec:lock-validation)). Coupling and FAU faults belong with packaging, not with Arrhenius $E_a$ arguments.

## Photonic packaging and module-level failures

Fleet FIT is not only laser wear-out. Once lasers are screened and derated, module and packaging failures often dominate field returns: the part that shipped with a clean LIV still loses light after shock, humidity, or a thousand ELSFP mate cycles. Fiber attach and FAU alignment fail from shock, humidity ingress, and epoxy creep; CPO fiber-array units add assembly steps that wafer test cannot catch ([9.10](#sec:cpo-status)). Hybrid stacks (TFLN-on-Si, InP laser on Si, flip-chip drivers) introduce solder voids, underfill cracks, and RF return-loss drift ([\[sec:tfln-mzm,sec:drivers\]](#sec:tfln-mzm,sec:drivers)). Thermal paths matter too: uncooled datacom versus liquid-cooled XPO/CPO, and TEC failure that looks like wavelength drift off grid or off ring ([\[sec:siring,ch:wdm\]](#sec:siring,ch:wdm)).

##### Connector reliability: MPO, mating cycles, and endface quality.

Multi-fiber connectors are the highest-touch mechanical interface in the fleet: every ELSFP swap, every fiber-attach unit (FAU) rework, and every cable-plant install mates and unmates an MPO. The MPO/MT ferrule family (rectangular, 6.4 mm $\times$ 2.5 mm, guide-pin aligned, 8/12/16/24 fibers per row) is standardized in *IEC 61754-7*, split into one-fibre-row and two-fibre-row parts . That standard fixes geometry, not lifetime; lifetime comes from two companion test methods. *IEC 61300-2-2* specifies the mate/unmate cycling test connector datasheets are rated against, and *IEC 61300-3-35* grades endface scratches, pits, and debris into pass/fail zones on the fiber core and cladding . TIA-568.3 sets 500 cycles as the structured-cabling mating-durability floor; MPO/MTP-class connectors in practice are commonly rated well above 1000 cycles, but that headroom erodes fast with the wrong cleaning discipline ([7.2.2](#sec:optical-channel)).

Three practical consequences follow for an ELSFP or CPO fiber-attach program. First, ORL creep is a mating-cycle and cleaning problem before it is a laser problem: a rising RIN floor after repeated ELS swaps ([8.1](#tab:wearout-map)) is diagnosed with an IEC 61300-3-35-style endface inspection, not a laser FA request. Second, mate-cycle count belongs in the same telemetry you already read for CMIS and DDM ([7.7](#sec:cmis)); track it per connector, not per module, since a connector can outlive several module swaps or vice versa. Third, write the mating-cycle and endface-grade limits into the ATP explicitly ([8.3](#tab:atp-laser)) rather than inheriting a generic MPO datasheet number: an ELS bank that hot-swaps weekly reaches a 500-cycle floor in under ten years, and a CPO fiber array that is field-serviced more aggressively reaches it faster still.

ELSFP cycling adds connector wear and contamination that raise ORL ([\[sec:optical-channel,sec:elsfp\]](#sec:optical-channel,sec:elsfp)); the mating-cycle and endface-grade limits above are exactly the numbers that turn "the connector feels loose" into an ATP line item instead of a guess.

Destructive physical analysis (cross-section, EDX) and structured 8D/CAPA with suppliers close the loop from RMA to design rule ([\[sec:supplier-exec,sec:fleet-triage\]](#sec:supplier-exec,sec:fleet-triage)). Without that loop, packaging FIT gets mis-attributed to laser Arrhenius models and the wrong part gets redesigned.

## Production test at volume

### Test time is a cost, coverage is a risk

Every second in the acceptance test plan (ATP) times millions of units is line capacity and real money. Every skipped measurement is escaped DPPM in the field ([8.1](#sec:fit-dppm)). The core tension in high-volume manufacturing is not "test or don't test" but how much coverage you buy per second. The expensive optical steps are thermal soak and corner runs, TDECQ on a sampling scope, BER dwell long enough to trust a low pre-FEC target, laser burn-in, and mate-cycle stress on ELSFP connectors. Some screens are statistical (sample burn-in from a lot, audit TDECQ on a subset). Others must be 100%: CMIS state machine sanity, basic LIV/SMSR pass, and any test that catches a safety or enable-sequence fault ([\[sec:cmis,sec:laser-safety\]](#sec:cmis,sec:laser-safety)).

### Where the test happens: wafer, die, module, system

Push defect detection as far upstream as correlation allows. Wafer-level or PIC probe catches process shifts (waveguide loss, ring resonance drift, bad heaters) before fiber attach and packaging spend. Killing a bad die at probe is orders of magnitude cheaper than an RMA ([8.5](#sec:photonic-packaging)). Module ATP is the full functional test: optical power class, TDECQ or proxy, sensitivity spot-check, CMIS bring-up, and connector/ORL on ELS parts. System or golden-host bring-up catches interop: media type, firmware rev, equalizer defaults, and the corners in [7.8.0.0.2](#sec:prod-corners). Wafer test cannot catch fiber attach, FAU alignment, epoxy creep, or connector wear. Those failures must survive to module ATP and, for some signatures, to fleet telemetry ([7.10](#sec:fleet-triage)).

### ATE-to-bench correlation

Production testers are built for speed and cost, not lab fidelity. The number that matters is correlation: does the ATE TDECQ, OMA, or sensitivity track the DCA/BERT reference within a known offset and spread? Set ATP limits with guardbands derived from that spread. A drifting tester or a stale golden unit shows up as a yield cliff or a DPPM escape. Keep a golden module (and golden laser subassembly for ELS), run gauge R&R across testers and shifts, and correlate CMIS monitors to bench instruments the same way you correlate TDECQ ([7.7](#sec:cmis)). If the ATE and the DCA disagree, fix the correlation before you argue with the supplier about spec.

### Screens, guardbanding, and SPC

Burn-in and HTOL screens trade infant-mortality escape rate against test time and cost ([\[sec:wearout-modes,sec:gr468\]](#sec:wearout-modes,sec:gr468)). Test limits are usually guardbanded tighter than the customer spec so field DPPM stays inside target under drift. SPC control charts on LIV, SMSR, RIN, TDECQ, and mate-cycle yield by lot, site, and date code catch a process shift before it becomes an 8D ([8.7](#sec:supplier-exec)). Production test is a yield, DPPM, and cost trade under a fixed reliability target. It is not a pass/fail checkbox after the optics already work on a golden bench.

## Supplier execution playbook

The supplier path is milestones, performance targets, quality, and manufacturability triage. That is not a soft skill. It is a concrete contract: requirements, gates, acceptance tests, process control, and corrective action when a lot goes wrong.

##### NPI gates and exit criteria.

[8.2](#tab:npi) is the usual stage map. For lasers and IM/DD modules, write exit criteria that a supplier can fail clearly, not slogans.

[]

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Gate    Question               Laser / optics exit criteria (examples)                                                                                                                                                                       Who signs
  ------- ---------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------
  EVT     Does it work at all?   First light; CMIS bring-up sequence ([7.8](#sec:bringup)); LIV/SMSR/RIN on engineering samples; one link closes BER                                       Optical eng + supplier FAE

  DVT     Spec across corners?   Full ATP at $T$/$V$ corners; prod-rep corners ([7.8.0.0.2](#sec:prod-corners)); TDECQ/OMA/sensitivity; GR-468 stress plan frozen; FIT model agreed   Optical eng + reliability

  PVT     Buildable at yield?    Multi-lot yield vs ATP; SPC charts live; burn-in escape rate; FAIR on production tooling; bring-up on production host                                                                                         Optical eng + SQE / mfg

  MP      Sustained quality?     Steady DPPM; RMA Pareto owned; ECO control on CMIS/firmware and process                                                                                                                                       Program + supplier QM
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** NPI gates with laser-relevant exit criteria. EVT/DVT/PVT/MP are stage names, not a schedule; dates and sample sizes belong in the program plan with the supplier.

Hold a gate if the exit data are missing. Shipping PVT material without frozen ATP limits is how field NFF and FIT arguments start ([7.10](#sec:fleet-triage)).

##### Requirements and ATP are the contract.

ATP and the requirements doc are the contract. Write both and keep them versioned together:

1.  **Requirements / PRD slice for the laser path:** fill [\[tab:laser-prd,sec:laser-reqs\]](#tab:laser-prd,sec:laser-reqs) (power class, grid, RIN@ORL, SMSR, derating, CMIS, FIT). Version it with the ATP.

2.  **Acceptance test plan (ATP):** the measurable tests that prove those requirements on every ship lot (or on a defined sample). Map each ATP line to a GR-468 or design-validation stress where life is claimed ([8.2.0.0.1](#sec:gr468)).

[8.3](#tab:atp-laser) is a working ATP checklist for an EML pluggable or an ELSFP CW module. Customize limits from the datasheet and the link budget; do not invent numbers in the ATP itself.

[]

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  ATP item                             Instrument / method                            Pass intent                                           Ties to
  ------------------------------------ ---------------------------------------------- ----------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  LIV ($I_\mathrm{th}$, slope, kink)   SMU + power meter                              kink-free bias window at rated $T$                    wear-out, derate ([5.6](#sec:laser-params))

  SMSR                                 OSA                                            single-mode vs. spec floor                            modal noise, aging

  RIN (intrinsic + stressed ORL)       PD + ESA                                       $\mathrm{RIN}_x\mathrm{OMA}$ / quiet floor            BER floor ([4.3.1](#sec:rin-values))

  Wavelength / grid                    OSA / wavemeter                                channel ID; $d\lambda/dT$                             WDM lock ([6](#ch:wdm))

  Optical power class                  power meter                                    ELSFP / MSA class met                                 link budget

  EAM bias / chirp (EML)               bias sweep + DCA                               ER, RLM, TDECQ at baud                                Tx quality ([7.3](#sec:tdecq))

  CMIS / TWI bring-up                  host or CMIS tool                              registers, alarms, state machine                      field telemetry

  Connector / ORL                      mate cycles + ORL meter                        cycles + endface grade vs IEC 61300 limits            packaging ([\[sec:connector-reliability,sec:elsfp\]](#sec:connector-reliability,sec:elsfp))

  Burn-in screen                       HTOL sample or 100% screen                     infant mortality culled                               GR-468 ([8.2.0.0.1](#sec:gr468))

  Driver/TIA ESD, latch-up             supplier JESD47/HBM/CDM report; sample audit   rating on file; no latch-up under current injection   IC reliability ([8.3](#sec:ic-reliability))

  Thermal class                        chamber at case $T$                            LIV/RIN/CMIS still pass                               derate policy
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Acceptance checklist for laser-bearing modules (EML or ELSFP). Limits are program-specific; the structure is what you negotiate with the supplier.

##### Incoming QC and SPC.

Qual lots are small. Production catches drift that qual missed.

- **Incoming:** sample or 100% screen against a subset of the ATP (at least power, CMIS, and a laser LIV/SMSR sample). Track DPPM by date code and site.

- **SPC**: control charts on $I_\mathrm{th}$, slope, SMSR, Tx power, and burn-in fallout. A process shift is a hold, not a hope.

- **First-article / FAIR:** when tooling, epi, or assembly site changes, rerun a defined FAIR package before open PO volume. Treat CMIS firmware revs the same way as process changes.

##### Excursions: 8D / CAPA.

When a lot fails ATP, incoming, or field triage lands in the manufacturability bucket ([7.10](#sec:fleet-triage)), run structured corrective action:

1.  **Contain:** quarantine WIP and ship holds; identify suspect date codes in the fleet.

2.  **Evidence pack:** failing ATP rows, CMIS dumps, LIV/SMSR/RIN plots, DPA photos (facet, solder, FAU cross-section) compared to a golden unit.

3.  **8D / CAPA**: root cause with the supplier (process step, material lot, firmware), corrective action, and preventive control (ATP tighten, SPC limit, poke-yoke).

4.  **Verify:** re-run FAIR on the corrected process; watch field RMA codes for that date-code family for a defined burn-in window.

Do not close 8D on "operator error" without a control that would have caught it at ATP. If FA shows laser wear-out on a young unit, it may be a reliability screen gap, not a supplier process bug; reclassify with [7.10](#sec:fleet-triage) before you argue FIT.

##### Milestone hygiene with partners.

Align the partner calendar to gates, not slideware:

- freeze requirements before DVT samples are built;

- freeze ATP limits before PVT yield is claimed;

- freeze FIT/$E_a$ assumptions before reliability marketing numbers ship;

- require ECO notice on laser die revision, TEC vendor, FAU epoxy, driver/TIA silicon revision ([8.3](#sec:ic-reliability)), and CMIS firmware.

Your job in those meetings is to name the measurement that would kill the gate. If nobody can point to an ATP row or a corner, the milestone is not real.

**Key idea.** Reliability at scale is mechanism discipline plus supplier gates. Classify failures with the wear-out map ([8.1](#tab:wearout-map)) before you argue FIT or open 8D. Laser wear-out gets Arrhenius and GR-468; driver and TIA silicon gets JESD47, HBM/CDM ESD, and latch-up ratings ([8.3](#sec:ic-reliability)); MPO connectors get mating-cycle and endface-grade limits ([8.5.0.0.1](#sec:connector-reliability)). Supplier execution is a gated contract: requirements and ATP at DVT, multi-lot SPC and FAIR at PVT, then 8D with evidence when a lot or field Pareto says manufacturability. Do not run process CAPA on a wear-out failure, and do not burn FIT math on a dirty or worn connector.

## From component FIT to fabric availability

The FIT arithmetic in [5.8.0.0.4](#sec:fit-example) gives a rate: about $0.6$ laser failures per day for a fleet of $5\times10^5$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin ([5.9](#sec:elsfp)), but it does not say what a failure costs or how a running job survives one. Two facts turn a per-component rate into a fabric problem.

First, a training or large inference job is synchronous. A collective ([9.7](#sec:collectives)) waits for its slowest member, so a single dead or slow link stalls the whole group, not just one endpoint ([9.6](#sec:inference-bottlenecks)). A link that flaps for a second is a stall for every accelerator in that collective. The optical FIT the earlier chapters budget therefore matters out of proportion to its share of the parts count.

Second, at cluster scale failures are continuous, not rare. Meta's published Llama 3 run is the clearest public data point: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . GPU and HBM3 faults dominated at close to half; network switch and cable faults were 35 events, 8.4% of the total. The optical link is a minority of hard job stops, but 8.4% of a failure every three hours is still tens of network events per run, and the ELS, module, and connector FIT this chapter budgets ([\[sec:fit-dppm,sec:connector-reliability\]](#sec:fit-dppm,sec:connector-reliability)) lands in exactly that bucket.

So the design question shifts. It is no longer "how reliable is one link" but "how does a fabric of $10^5$ links keep a job running through a failure every few hours." The answers are architectural, and the optical engineer feeds each one.

Redundancy and rails.

: Rail-optimized topologies ([9.2](#sec:topologies)) already give parallel planes; dual-plane and dual-ToR designs let a lost link degrade bandwidth instead of dropping an endpoint. Redundancy multiplies the link and laser count, which feeds straight back into the FIT budget: more resilience is more parts that can fail.

Detection and reroute.

: Transient faults stay below the job. KP4 FEC ([3.12](#sec:kp4)) absorbs the error bursts a marginal link throws; link-level retry and sub-second link-flap detection plus adaptive routing steer traffic off a degraded link before the scheduler notices. Vendor fabrics (NVIDIA Spectrum-X and Quantum, Broadcom Tomahawk) advertise adaptive or "cognitive" routing and link-level retry for this. Treat the specifics as vendor orientation, but the mechanism is why transient optical faults rarely reach the hard-stop bucket above.

Topology reconfiguration.

: When a link or rack dies for good, an optical circuit switch re-wires the topology around it in milliseconds, so the scheduler routes around the dead node instead of stalling the pod ([9.9](#sec:ocs)) . Component FIT still applies; the fabric survives each failure by re-wiring optically.

Sparing and field service.

: Hot spare nodes and lanes cover the interval between failure and repair. Field-replaceable external lasers ([5.9](#sec:elsfp)) make a dead laser a faceplate swap rather than a fabric outage, which is the architectural reason ELS decouples laser FIT from switch FIT. The connector mating-cycle and endface budget ([8.5.0.0.1](#sec:connector-reliability)) sets how many of those swaps the plant survives.

The cost of a failure closes the loop. A hard interruption is lost compute plus the time to detect, reroute or reschedule, and restart from the last checkpoint. Fast detection and reroute shrink that lost time, which is the fabric-level reason the module work in this chapter pays off: derating ([5.8](#sec:laser-aging)), burn-in and screens ([8.2.0.0.1](#sec:gr468)), and a tight ATP ([8.7](#sec:supplier-exec)) lower the failure rate, and a resilient fabric lowers the cost of each failure that slips through. The two multiply.

**Key idea.** Component FIT sets the failure *rate*; the fabric sets the failure *cost*. A synchronous collective makes one bad link everyone's stall ([9.7](#sec:collectives)), and at cluster scale failures are continuous: Meta's Llama 3 run saw a failure about every three hours, network faults 8.4% of them, at roughly 90% effective uptime . The fabric survives that with redundant rails, FEC and fast reroute, OCS topology reconfiguration ([9.9](#sec:ocs)), and field-replaceable lasers ([5.9](#sec:elsfp)). Lowering per-link FIT and lowering per-failure cost multiply, which is why link reliability sets how large a dependable fabric can grow.


<div class="nav-links">
  <a href="ch7-optical-validation">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch9-ai-datacenter-networking">Next &rarr;</a>
</div>
