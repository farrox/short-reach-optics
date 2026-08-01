---
layout: default
title: "Appendix I: Failure Analysis Reference"
---

# Appendix I: Failure Analysis Reference

This appendix is a symptom-route lookup for failure analysis. The investigation method (preserve, scope, falsify, confirm, correct, prevent) lives in Chapter 12. Use these routes after the population is scoped and the failing state is preserved. Do not treat a recipe as a substitute for the canonical sequence.

*Read first:* power loss; BER waterfall versus floor; intermittent failures; contamination; yield drop.

*Reference:* debugging fork; fleet triage map; 8D/CAPA/DPA.

## Power loss

<pre class="dectree" aria-label="Power loss"><code>Power loss
  |
External meter vs CMIS
  |
Plane walk (source -&gt; coupling -&gt; MUX -&gt; connector -&gt; Rx)
  |
LIV at failing T
  |
Decision: source / path / monitor
  |
Recurrence: earliest ATP power check</code></pre>
##### Observed behavior.

Received power or OMA falls at one or more lanes. BER may remain stable at first, then rise as receiver margin is consumed. The module monitor and an external power meter may disagree.

##### Likely hypotheses.

Launch power can fall because the laser is disabled, thermally rolled over, or aged. Power can disappear after the source through modulator loss, coupling shift, MUX loss, fiber bend, connector contamination, or a wrong reference-plane calibration. A drifting monitor photodiode can report loss that does not exist.

##### Measurements, mechanism isolation, and confirmation.

1.  Compare CMIS Tx and Rx power, external power at the faceplate, bias current, and case temperature. Disagreement identifies the first suspect plane.

2.  Walk optical power plane by plane with a known source and calibrated meter. Do not change bias or equalization while locating the loss.

3.  Rerun LIV at the failing temperature. A moved LIV raises $P(\mathrm{source})$; a stable LIV raises $P(\mathrm{path\ or\ monitor})$ until confirmed. Do not treat either as a confirmed mechanism before controlled confirmation.

4.  Preserve telemetry, then inspect connectors before cleaning (Appendix I.9). Measure insertion loss and ORL. Use a golden fiber and module swap to separate field plant from module.

5.  For a weak lane, compare sibling lanes and per-lane coupling. Lot or lane clustering points toward assembly or MUX variation.

##### If confirmed: possible controls and recurrence.

Repair the first plane where power diverges. Correct calibration or monitor coefficients before changing source bias. Add a power check at the earliest production plane that can catch the signature and retain golden-path baselines for fleet comparison. *Recurrence control:* ATP or sample power at that plane; golden-path baselines.

## BER increase: waterfall shift or floor

Interview path: name the optical plane, sweep a waterfall at that plane, then classify shift versus floor before picking instruments. One operating-point BER is not a classification.

<pre class="dectree" aria-label="BER up"><code>BER up
  |
Name plane
  |
Waterfall (BER vs power)
  |-- power not held --&gt; power path (Appendix I.1)
  |-- shift --&gt; sensitivity / OMA / IL / eye / timing
  |-- floor --&gt; Appendix I.2.1
  |
Decision + ATP / telemetry control</code></pre>
##### Observed behavior.

Pre-FEC BER rises. A waterfall is BER versus received power from a VOA sweep at a named reference plane. The curve either moves to higher power (shift), stops improving at a horizontal asymptote (floor), or shows both (soft floor on a shift).

##### Likely hypotheses by ownership.

Group candidates before instrumenting:

Source / transmitter

: Lost OMA, eye closure, RIN, pattern dependence.

Optical path

: Insertion loss, connector/ORL or MPI, MUX or fiber plant.

Receiver / host

: Sensitivity, equalization limits, timing, host SerDes.

Power and timing

: Rails, clocks, shared disturbances across lanes.

Control and software

: Bias, lock, firmware state transitions.

Environment and assembly

: Temperature, vibration, attach, contamination.

A shifted waterfall supports lost power, sensitivity, eye, timing, or dispersion: the link still responds to more photons, but the power needed for a given BER has moved. A floor supports signal-proportional noise, reflection, crosstalk, or bursty impairments: past a point, more power does not help. FEC error timing further splits the cases: randomly sprinkled errors fit Gaussian or steady RIN; clustered bursts fit MPI, connector intermittents, or shared supply and clock events.

##### Measurements, mechanism isolation, and confirmation.

1.  Name the plane, then sweep received power and plot BER. Confirm shift, floor, or both.

2.  If the waterfall shifted, compare received OMA, TDECQ, receiver sensitivity, equalizer taps, wavelength, and temperature with the golden baseline. Golden-swap Tx and Rx to assign ownership.

3.  If the curve floors, continue in Appendix I.2.1 and split intrinsic RIN, electrical noise, ORL, MPI, and crosstalk.

4.  Use FEC error timing and lane correlation to separate random noise from bursts and shared disturbances. Preserve counters before reseating if the pattern is intermittent.

##### If confirmed: possible controls and recurrence.

Restore the margin ledger that moved, then repeat the full BER sweep at loaded corners. Store waterfall shape, not only pass/fail BER, so later fleet changes can be classified without guessing. Interview study treatment: Appendix A.8.9. *Recurrence control:* earliest reliable control for the confirmed ledger (ATP or sensitivity sample, SPC, telemetry, or qualification), not pass/fail BER alone.

### BER floor

##### Observed behavior.

Pre-FEC BER improves as you increase transmit or received power, then stops improving and flattens at a constant floor regardless of how much more power you add. The FEC histogram may still look random (steady RIN) or bursty (MPI, intermittents); the floor shape alone does not decide that split.

##### Likely hypotheses.

A BER floor means additional received power no longer removes the dominant impairment. That is a diagnostic pattern, not one mechanism. RIN can create a floor when signal-proportional intensity noise dominates the receiver budget: $\sigma_\mathrm{RIN} \propto I$, so $Q$ can saturate at $Q_\mathrm{max} = 1/\sqrt{\mathrm{RIN}_\mathrm{lin} \cdot \mathrm{BW}}$ under a dominant-RIN model (§6.3). Do not define every floor as RIN-limited. Other leading mechanisms include multipath interference (MPI), bias-rail noise that converts to equivalent intensity noise (§7.8), pattern-dependent distortion or residual ISI, crosstalk, timing or CDR limits, and DSP or equalization limits.

MPI may produce deterministic interference, power-independent floors, pattern sensitivity, environmental sensitivity, or time-correlated errors depending on coherence, path delay, motion, and modulation. Useful evidence includes ORL dependence, delay-related structure on an ESA, aggressor dependence, pattern dependence, thermal or mechanical sensitivity, and FEC error timing. Do not treat "bursty FEC histogram" alone as proof of MPI.

##### Required access.

- **Black-box / bookended:** attenuation sweep, pre-FEC BER and FEC timing, Tx/Rx power telemetry, temperature, host/module swap, lane remap.

- **Engineering access:** intrinsic RIN, product-board RIN, $\mathrm{RIN}_x\mathrm{OMA}$ at a named ORL, optical eye, controlled reflector, ESA, optical breakout.

##### Measurements and isolation.

1.  Confirm the floor exists: sweep received power (or Tx OMA) at a named reference plane and plot BER vs. power. A floor appears as a horizontal asymptote.

2.  Where engineering access exists, bisect optical vs. electrical RIN: quiet SMU (intrinsic) versus product bias board. If the floor moves, the electrical path is injecting noise (§7.8).

3.  Sweep ORL with a controlled reflector. If the floor worsens with lower ORL, the path is feedback-sensitive. Check isolator, connector, and fiber-attach cleanliness.

4.  Gather MPI evidence (ORL, delay structure, pattern, thermal/mechanical, FEC timing). Treat MPI as a leading mechanism until confirmed.

5.  Compare measured $\mathrm{RIN}_x\mathrm{OMA}$ at the stated ORL against the named PMD revision and ATP limit (for example $-136$ dB/Hz at 17.1 dB ORL for a cited DR-class clause ). State the plane and condition.

##### If confirmed: possible controls and recurrence.

If intrinsic RIN is confirmed as the limiter, replace or derate. If electrical RIN, fix the bias supply. If ORL-driven, clean or replace connectors and verify isolator function. If MPI is confirmed from multiple reflections, reduce mated interfaces or improve their ORL. Update the earliest economical control (ATP, sampled audit, SPC, or telemetry), not every deep FA measurement. *Recurrence control:* RIN@ORL sample or ORL audit at the stated plane.

## Low extinction ratio

##### Observed behavior.

Transmitter OMA looks low on the DCA even though average power is in range. TDECQ may or may not fail depending on how the reference equalizer compensates.

##### Likely hypotheses.

Linear extinction ratio is $\mathrm{ER}_\mathrm{lin}=P_1/P_0$ (for PAM4 outer levels use $P_3/P_0$). In decibels, $\mathrm{ER}_\mathrm{dB}=10\log_{10}(\mathrm{ER}_\mathrm{lin})$ and $\mathrm{ER}_\mathrm{lin}=10^{\mathrm{ER}_\mathrm{dB}/10}$. Low ER means the off level is too high or the on level is too low. In an EML, ER is set by EAM reverse bias; in a DML, by modulation depth relative to threshold.

An idealized receiver OMA penalty for finite ER is $$\mathrm{PP}_\mathrm{dB}
=
10\log_{10}\!\left(\frac{\mathrm{ER}_\mathrm{lin}+1}{\mathrm{ER}_\mathrm{lin}-1}\right).$$ At 10 dB ER the penalty is $\sim$0.87 dB; at 6 dB ER it rises to $\sim$2.2 dB (§6.4). This is an idealized receiver-penalty model, not a measured compliance quantity such as TDECQ.

##### Measurements, mechanism isolation, and confirmation.

1.  Measure ER on the DCA (outer OMA / average power, or directly from the histogram levels). Compare against the PMD limit.

2.  **EML:** Sweep EAM bias. ER should peak at the optimal bias point; if the curve has shifted (aged EAM), the operating point needs recalibration. Check EAM bias DAC code vs. datasheet.

3.  **DML:** Check bias current vs. LIV. If bias is close to threshold, modulation depth is limited. Increase bias (but watch thermal rollover and RIN).

4.  **MZM:** Check quadrature bias. If the MZM has drifted off quadrature ($V_\pi/2$ point), extinction degrades. Log the bias-control loop error signal; a saturated loop indicates drift beyond correction range.

5.  **Ring:** Check resonance alignment. If the ring is detuned from the laser wavelength, extinction drops. Monitor the thermal tuner current and wavelength-lock error.

##### If confirmed: possible controls and recurrence.

Recalibrate the modulator operating point. For EML aging, update the EAM bias setpoint in firmware or flag the module for replacement if the absorption curve has shifted beyond the correctable range. For MZM drift, verify the bias controller and its monitor PD. For rings, retune or check for neighbor thermal crosstalk (§8.5). *Recurrence control:* ER or modulator-bias check in ATP or cal audit.

## Lane imbalance

##### Observed behavior.

In a multi-lane module (DR4, FR4, DR8), one or more lanes show significantly different OMA, TDECQ, or pre-FEC BER compared with siblings in the same module. The weak lane may be marginal or failing while others are healthy.

> **What this usually means.** One lane only, siblings healthy
>
> *Usually:* lane-specific optics, attach, driver or TIA channel, or local thermal gradient
>
> *Not:* a shared firmware image bug as the first explanation, unless remapping proves otherwise

##### Likely hypotheses.

Multi-lane modules share a substrate, laser array (or CW-WDM source), and thermal environment. Lane-to-lane variation comes from: (1) die-level non-uniformity in the laser or modulator array (threshold, slope, $V_\pi$, coupling), (2) packaging variation in fiber-array alignment (one channel of the FAU slightly misaligned), (3) driver or TIA channel mismatch on the electronic IC, or (4) thermal gradient across the die (edge lanes hotter or cooler than center lanes).

##### Measurements, mechanism isolation, and confirmation.

1.  Measure all lanes: OMA, ER, TDECQ, RIN, wavelength. Identify the outlier.

2.  **Is it optical or electrical?** Swap the electrical lane assignment (if the host supports lane remapping) or test the suspect optical lane with a known-good driver channel. If the problem follows the optical path, it is laser/modulator/fiber-attach. If it follows the electrical channel, it is driver/TIA.

3.  **Check coupling.** Measure per-lane fiber-coupled power with an integrating sphere or power meter array. A single weak lane with normal LIV suggests FAU misalignment.

4.  **Thermal map.** Use an IR camera or CMIS per-lane monitors (if available) to check for hot spots. Edge lanes near the package wall or near a TEC boundary may run hotter.

5.  **Time-growing imbalance.** A lane that worsens over time raises the probability of lane-specific source, modulator, receiver, coupling, packaging, or control degradation. Do not immediately call it laser aging. Where engineering access exists, compare LIV, bias, lock error, and coupling at $t_0$ and now before naming the mechanism.

##### Required access.

Black-box path: per-lane power/BER/FEC, host lane remap, sibling comparison, temperature. Engineering-access path: LIV, optical eye, TDECQ, per-lane coupling, bias sweeps, FAU inspection.

##### If confirmed: possible controls and recurrence.

Confirmed FAU misalignment supports a manufacturing or process control change (incoming inspection or first-article coupling). A thermal gradient supports TEC zoning redesign or derating of the hot lane. Confirmed source wear-out supports lot action and a review of burn-in or life screening effectiveness. Driver mismatch supports IC supplier channel-flatness work. Call each mechanism only after the discriminating evidence above closes. *Recurrence control:* per-lane coupling or TDECQ first-article / SPC, or the earliest reliable control for the confirmed owner.

## Wavelength drift

##### Observed behavior.

In a WDM system, one or more channels walk off the ITU grid or the ring/filter passband. BER degrades as the channel moves off the receiver filter or MUX/DEMUX passband. In ring-modulator CPO, this manifests as sudden unlock of the wavelength control loop.

##### Likely hypotheses.

Laser wavelength moves with temperature and bias current. If the TEC or wavelength-locker servo cannot track, the channel walks off its assigned slot. In microring systems, resonance also moves strongly with temperature, and neighbor heaters create thermal crosstalk that pushes adjacent channels (§8.4, §8.5).

##### Measurements, mechanism isolation, and confirmation.

1.  Measure wavelength on an OSA or wavemeter. Compare to the target grid.

2.  **Laser-side:** Check TEC current. If saturated (at max or min drive), the thermal load exceeds TEC capacity. Check case temperature and airflow.

3.  **Locker-side:** Read the wavelength-locker error signal. A healthy loop holds near zero; drift means the servo is losing lock. Check locker etalon alignment and PD balance.

4.  **Ring CPO:** Check the ring thermal tuner DAC code. If it has railed (max heater power), the ring cannot reach the target wavelength. Check for neighbor heating (all adjacent lanes at full traffic and max case $T$).

5.  **Aging:** Progressive drift over weeks or months raises leading hypotheses of source mode hop, locker/TEC capacity loss, or control recalibration drift. Confirm with wavelength history, TEC or heater headroom, and lock-error trend before naming the mechanism.

##### If confirmed: possible controls and recurrence.

TEC saturation: reduce case temperature (improve airflow or liquid cooling) or derate the laser operating current. Ring unlock: increase heater headroom in the design, reduce thermal crosstalk with layout changes, or shift the CW-WDM source grid to re-center the ring tuning range. Aging: schedule preventive replacement (ELSFP hot-swap, §7.14). *Recurrence control:* TEC headroom and lock-error telemetry alarms.

## Eye closure (high TDECQ)

##### Observed behavior.

TDECQ exceeds the PMD limit even though average power and ER look acceptable. The DCA eye appears compressed or distorted after the reference equalizer is applied.

##### Likely hypotheses.

TDECQ measures how much noise the transmitter can tolerate before BER exceeds the FEC threshold, relative to an ideal transmitter (Appendix E.3). High TDECQ means the equalized eye is poor. Common causes: (1) insufficient EO bandwidth (modulator or driver roll-off), (2) poor level linearity (RLM $<$ 0.95; driver or modulator compression), (3) pattern-dependent effects (ISI from bandwidth limit, reflections, or impedance mismatch), (4) chromatic dispersion on FR-class fiber eating into the margin.

##### Measurements, mechanism isolation, and confirmation.

1.  Inspect the raw (unequalized) eye on the DCA. Is it bandwidth-limited (rounded transitions), compressed (uneven levels), or noisy (RIN/jitter)?

2.  **Bandwidth:** Measure EO $S_{21}$ of the modulator (if accessible) or the combined Tx path. Compare to the Nyquist frequency. If 3-dB BW is below Nyquist, bandwidth is the limiter.

3.  **RLM:** Compute relative level mismatch from the DCA histogram. If $\mathrm{RLM} < 0.95$, the PAM4 levels are unevenly spaced. Check driver linearity (swept DAC code) and modulator transfer function (bias sweep).

4.  **Reflections:** Check $S_{11}$ of the RF path (driver to modulator) and the optical return loss. Reflections cause post-cursor ISI the FFE cannot fully cancel.

5.  **Dispersion:** Measure TDECQ with and without the test fiber (TECQ vs. TDECQ). If TDECQ is significantly worse than TECQ, dispersion is the marginal contributor. Check Tx wavelength and chirp against the fiber length and dispersion coefficient.

##### If confirmed: possible controls and recurrence.

Bandwidth: upgrade driver or modulator (higher-BW die or peaking network). RLM: tune driver pre-emphasis (DAC levels for each PAM4 symbol). Reflections: fix wirebond, impedance discontinuity, or connector. Dispersion: tighten wavelength tolerance or shorten the fiber (re-route). *Recurrence control:* TDECQ/RLM sample tied to the failing corner.

## Thermal runaway

##### Observed behavior.

Module temperature rises continuously until shutdown (CMIS over-temperature alarm) or until the laser degrades catastrophically. May start subtly: BER creeps up as case $T$ rises during traffic ramp or with neighbor-lane loading.

##### Likely hypotheses.

In a faceplate pluggable, double-digit-watt module power must leave through the cage and heatsink . If airflow is blocked, the cage is overloaded, or the TEC inside the module is fighting a losing battle against junction temperature, the thermal loop runs away. In CPO, the optical engine sits on the switch substrate beside the ASIC; cooling-path faults concentrate heat on the source and ring controls . Both sources are vendor or research orientation, so the product thermal model remains authoritative.

##### Measurements, mechanism isolation, and confirmation.

1.  Read CMIS module temperature and compare to the module's rated case $T$ range. If case $T$ exceeds the max, the system cooling is inadequate.

2.  **Check TEC current.** A TEC at max drive current is saturated; it cannot pump more heat. The junction temperature is higher than the case $T$ suggests.

3.  **Measure LIV at temperature.** If threshold rises and slope drops steeply with $T$, the laser is near thermal rollover (§7.13). The operating point may be marginal.

4.  **Neighbor loading.** Bring all lanes and neighbor modules to full traffic simultaneously. If the problem only appears under full-cage load, the thermal design margin is insufficient.

5.  **Airflow audit.** Inspect the faceplate for blocked vents, incorrect fan speed, or missing blanking panels (bypass airflow). For liquid-cooled systems (CPO, XPO), check coolant flow rate and inlet temperature.

##### If confirmed: possible controls and recurrence.

System-level: improve airflow, lower ambient, or reduce module count per cage. Module-level: derate the laser (lower bias current reduces self-heating) or switch to a lower-power module style (LPO instead of retimed, Appendix H.5.1). CPO: ensure the cold-plate thermal interface material (TIM) is intact and the liquid loop meets flow-rate spec. Long-term: specify a tighter thermal class in the laser requirements (§7.6). *Recurrence control:* loaded-cage thermal class in ATP or DV plan.

## Intermittent failures

<pre class="dectree" aria-label="Intermittent / burst"><code>Intermittent / burst
  |
Preserve state (do not reseat yet)
  |
Scope time + change history
  |
ORL / connector / supply / lock / attach
  |
Decision: contain / clean / redesign / earliest control
  |
Recurrence: dwell + FEC histograms / service / telemetry</code></pre>
##### Observed behavior.

Links flap, lose lock, or show bursts of FEC errors while average power and a short bench BER test look normal. The symptom may clear after reseating, cooling, or restarting firmware.

> **What this usually means.** Intermittent bursts that clear on reseat or cool-down
>
> *Usually:* connector or mate stress, ORL or MPI, supply noise, lock loss, weak attach, or firmware state
>
> *Not:* a confirmed wear-out FIT story from a short room-temperature BER pass

##### Likely hypotheses by ownership.

Optical path

: Connector contamination, mate stress, ORL or MPI, weak fiber attach.

Source / transmitter

: Lock loss, bias or wavelength control excursions.

Receiver / host

: Electrical contact, SerDes recovery, host reset paths.

Power and timing

: Supply noise, shared rail or clock bursts.

Control and software

: Firmware state, CMIS transitions, recalibration.

Environment and assembly

: Thermal cycling, vibration, package stress.

Reseating can remove the evidence by cleaning a contact, changing fiber stress, and resetting a state machine at the same time, so it is not a discriminating experiment unless those effects are separated.

> **Engineering heuristic.** Treat cool-down recovery as a clue, not a fix. Capture the failing corner before the unit returns to room temperature forever.

##### Measurements, mechanism isolation, and confirmation.

1.  Freeze CMIS state, FEC error timing, LOS or LOL history, temperatures, rails, lock error, and neighbor activity before touching hardware.

2.  Scope the pattern across lane, module, tray, rack, lot, and firmware revision. Shared timing points toward power, cooling, firmware, or a shared source.

3.  Correlate bursts with Rx power, ORL, supply and clock spurs, lock-loop state, vibration, and temperature. Use trigger capture rather than averages.

4.  Run controlled disturbance tests one at a time: connector motion, thermal ramp, neighbor load, rail load, and firmware state transition.

5.  Repeat on a golden unit and fixture. If the fault follows the unit, inspect fiber attach, solder, contacts, and control logs before destructive analysis.

##### If confirmed: possible controls and recurrence.

Fix the confirmed contact, attach, supply, lock, or firmware cause. Add event-triggered telemetry and a production stress that reproduces the fault. Keep intermittent and no-fault-found RMA codes separate from laser wear-out.

> **Engineering heuristic.** A rising NFF rate is often a triage and evidence problem, not proof that the field is healthy. Separate intermittent codes from wear-out before you trust the FIT.

*Recurrence control:* event-triggered FEC telemetry plus a dwell stress.

## Connector contamination

##### Observed behavior.

Intermittent link failures, burst errors, or elevated BER that clears after reseating or cleaning a connector. Rx power may fluctuate or show sudden drops. Often affects one direction of a duplex link.

##### Likely hypotheses.

A particle of dust on an MT, LC, or MPO ferrule endface scatters and absorbs light, raising insertion loss and back-reflection (lowering ORL). Debris in the core zone can cause large loss even when most of the ferrule looks clean. Elevated ORL feeds back into the laser and raises RIN, causing burst errors even when average power looks acceptable. In high-power CW-WDM and ELSFP systems, trapped particles can burn onto the fiber endface and cause permanent damage.

##### Measurements and isolation.

Preserve evidence before you disturb the mating:

<pre class="dectree" aria-label="Preserve telemetry and failure history"><code>Preserve telemetry and failure history
  |
Photograph and inspect before disturbance
  |
Record contamination and damage
  |
Clean and re-inspect
  |
Measure insertion loss and ORL
  |
Retest BER and sensitivity</code></pre>
1.  Capture CMIS/host counters, timestamps, Tx/Rx power, alarms, and which port failed before reseating or cleaning.

2.  Photograph and inspect with a fiber-endface scope (200--400$\times$) before disturbance. Record particles in the core zone, scratches, pits, residue, and burn marks.

3.  Clean and re-inspect (dry-click cleaner or lint-free wipe with IPA). If the endface still fails IEC 61300-3-35 zone criteria, replace the jumper .

4.  Measure insertion loss and ORL across the mated pair at the named plane. Compare to the link-budget allocation (Appendix E.5).

5.  Retest BER and sensitivity. Clearing after cleaning supports contamination as the leading mechanism; confirm with IL/ORL and watch for recurrence. Log connector location and date code.

##### If confirmed: possible controls and recurrence.

After evidence is preserved: clean, re-inspect, and verify IL/ORL and BER. Preventive: dust caps on unused ports, "inspect before connect" in the service runbook, sealed cassettes or trunk cables that minimize open-ferrule exposure. For high-power paths (ELSFP, CW-WDM), burn damage requires replacement, not re-cleaning. Track contamination RMAs as a distinct failure code (not "laser failure") so FIT accounting stays honest (§12.10).

> **Engineering heuristic.** Inspect before you clean, and photograph before you disturb. Cleaning first can erase the only evidence that the mate was dirty.

*Recurrence control:* inspect-before-connect runbook; contamination RMA code.

## Yield drop

##### Observed behavior.

First-pass yield falls below its stable baseline. The loss may cluster on one ATP row, lane, tester, shift, supplier lot, assembly site, or firmware revision.

> **Engineering heuristic.** Calibration drift is usually more likely than simultaneous hardware failure across a previously healthy population.

##### Likely hypotheses.

Process drift, incoming material variation, fiber-array alignment, die-attach or solder change, tester or fixture drift, stale calibration, a software limit change, or a guardband that no longer matches measurement spread.

##### Measurements, mechanism isolation, and confirmation.

1.  Contain suspect work in process and freeze tester software, limits, fixtures, and calibration records.

2.  Build a Pareto by ATP row, lot, date code, site, tester, and shift. Do not average away a one-lane or one-station signature.

3.  Run a golden unit across stations and the same failed unit on the reference bench. This clears the measurement system before supplier action begins.

4.  Compare upstream wafer, die, assembly, and incoming data at the first point where good and bad populations separate.

5.  Select failure analysis that distinguishes the remaining mechanisms, then verify the correction on a controlled lot and watch the field code.

##### If confirmed: possible controls and recurrence.

Restore the changed process or measurement input, add a statistical control at the first observable point, revise ATP only with correlation data, and require a new first-article check before releasing volume (Appendix G.16). *Recurrence control:* SPC at the first separating observable; FAIR after change.

## Aging, thermal response, and margin erosion

Use time scale and recovery to route the incident. A reversible shift during a temperature or neighbor-load sweep is a thermal operating-point problem. A baseline that moves over stress hours or field months is aging. A sudden permanent step after a cycle points toward damage or an assembly defect, not ordinary thermal response.

1.  Return the unit to its starting temperature and operating point. Record whether power, wavelength, bias, TDECQ, and BER recover.

2.  Compare with ship and pre-stress data. Permanent LIV, spectrum, or bias-curve movement supports aging or damage.

3.  Repeat the temperature sweep with source, wavelength-selective element, receiver, and neighbors isolated in turn.

4.  Update the power, noise, timing, spectral, and control ledgers (§7.19). Several small shifts can explain a BER failure even when each component remains inside its stand-alone limit.

5.  Route reversible thermal loss to cooling, control, calibration, or derating. Route cumulative change to HTOL and life-model review. Route lot-clustered permanent steps to manufacturing failure analysis.

On margin versus power, see §7.19: add margin only on the ledger that is empty; do not raise launch power by habit.

The corrective action must restore margin at combined corners. A room-temperature retest does not close a high-temperature incident, and one clean HTOL readout does not explain a reversible lock failure.

## Temperature sensitivity

##### Observed behavior.

BER, TDECQ, optical power, or lock stability degrades during a case-temperature ramp or under loaded-neighbor conditions. The unit may recover when cooled.

##### Likely hypotheses.

Laser threshold and slope drift, wavelength movement, ring-resonance drift, TEC or heater saturation, EAM or MZM bias error, receiver-noise rise, package stress, or a thermal gradient that affects one lane.

##### Measurements, mechanism isolation, and confirmation.

1.  Record case temperature, external optical power, wavelength, bias, TEC or heater current, lock error, OMA, ER, TDECQ, and pre-FEC BER on one time axis.

2.  Repeat with neighbors off and on. A shared shift points toward thermal or supply coupling; a lone lane points toward its local path.

3.  Hold the source fixed and move the wavelength-selective element, then reverse the test. This splits laser drift from ring or filter drift.

4.  Rerun LIV and receiver sensitivity hot and cold. Separate lost launch power from lost receiver margin.

5.  Inspect package and cooling interfaces if optical and electrical blocks pass alone but fail in the assembled system.

##### If confirmed: possible controls and recurrence.

Restore thermal headroom, correct calibration and control limits, reduce coupling, or derate the operating point. Add the loaded-neighbor temperature ramp to the ATP or the product-readiness plan step that missed it (Chapter 11). *Recurrence control:* loaded-neighbor temperature ramp in ATP or requirement-verification / system-validation evidence.

## The debugging fork: power versus signal quality

Apply the debugging fork (§6.8) before sweeping parameters or changing firmware: check the power meter or CMIS Rx power monitor first. If power moved, the fault is in the optical path (laser, coupling, connector, fiber, MUX); if power held but BER or TDECQ worsened, it is signal quality (bandwidth, noise, jitter, bias, equalization, reflection). This one check prevents the most common incident mistake: retuning an equalizer or laser bias when the real cause is a dirty connector. Then check which margin ledger moved (§7.19) before descending to component physics.

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
> Scope $\cdot$ time behavior $\cdot$ population $\cdot$ power or quality $\cdot$ highest-value measurement $\cdot$ decision $\cdot$ recurrence control (Appendix D.18).

> **Engineering heuristic.** A passing BER on a golden host is not production readiness. Interop, margin, and manufacturing control still have their own questions.

## Fleet triage map and field buckets

Lab debug asks: *what is broken on this unit?* Fleet triage asks: *which bucket does this failure belong in, and who owns the fix?* The investigation method lives in Chapter 12. Optical programs at fleet scale own that bucket split across performance, reliability, and manufacturability. Wrong bucket wastes weeks.

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

: the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (Appendix E.3, Appendix H.5.2, §3.14.3).

Reliability

: the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (Appendix F.11, §7.13, Appendix F.1.1, §7.14).

Manufacturability

: a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (Appendix G.16, Appendix F.11.4).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label. Use the symptom procedures earlier in this chapter for bench confirmation.

##### Field classification is not qualification planning.

The discriminations in this section belong here: COD versus ESD damage on a dark unit, date-code and lot clusters that point at a manufacturing escape, a clean facet cross-section that leaves a connector unexplained until ORL is measured, and the rule that later evidence does not silently rewrite an earlier bucket. All of it starts from a failure that already happened and ends with an owner. Qualification works the other direction: it starts from a claim and asks which mechanisms could violate it before any unit fails. Those mechanism families, and the exposure and acceptance each one needs, are in Appendix F.11, Table F.5. Do not plan a qualification from triage buckets, and do not close a field ticket with a qualification table.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; §7.14).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (§3.12), equalizer tap saturation (Chapter 5).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $\to$ bucket).

Table I.1 is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

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
**Table I.1.** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $=$ performance (design/operating point); reliability $=$ time-dependent wear; mfg $=$ lot/process/install excursion. Row notes follow.

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

Ask whether the external laser, the connector, or the engine owned the fail. Compare old versus new CMIS and connector cycles. Confirm MT inspect and LIV on the returned module. **Decision:** split RMA codes for laser versus connector. **Risk if skipped:** FIT burns down the wrong wear-out mode (§7.14).

### Why triage order matters

Scope before mechanism. Telemetry before destructive FA. Bucket before owner. Confirm before CAPA. Closing the loop into ATP is part of the incident, not optional paperwork. Reversing that order produces NFF piles and merged RMA codes that make life models dishonest.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $T$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with Table I.1. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (§7.13).

    - Manufacturability: quarantine lot, incoming hold, then structured 8D/CAPA with DPA when the physical mechanism is not yet confirmed (Appendix I.14.2, Appendix G.16).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Excursions: 8D / CAPA and DPA.

When a lot fails ATP or incoming, or field triage lands in the manufacturability bucket, run structured corrective action. Manufacturing validation owns the production consequence sequence (detect, contain, scope, ownership, earliest control, verify on fresh lots; Appendix G.18). This section owns mechanism confirmation and the supplier corrective-action loop.

1.  **Contain:** quarantine WIP and ship holds; identify suspect date codes in the fleet.

2.  **Evidence pack:** failing ATP rows, CMIS dumps, LIV/SMSR/RIN plots, and DPA photos (facet, solder, FAU cross-section) compared to a golden unit.

3.  **8D / CAPA**: confirmed mechanism with the supplier (process step, material lot, firmware), corrective action, and preventive control (ATP tighten, SPC limit, poka-yoke).

4.  **Verify closure:** containment confirmed effective; mechanism reproduced or physically confirmed; corrective action removes the failure; no unacceptable regression introduced; production control detects recurrence; next lots remain stable; field cohort trend improves. Re-run FAIR alone is not enough for environmental, intermittent, or fleet-specific escapes (Appendix D.16, Appendix G.5).

Do not close 8D on "operator error" without a control that would have caught it at ATP or in process. If FA shows laser wear-out on a young unit, it may be a reliability screen gap, not a supplier process bug; reclassify with the buckets above before you argue FIT. Production-control and supplier-gate context: Chapter 11, Appendix G.16, Appendix G.

##### Worked paths (three common tickets).

*"High temp only."* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate). A permanent LIV or spectrum shift at temperature that matches an aged lot raises $P(\mathrm{aging})$ and justifies moving the ticket toward reliability; cool-down recovery without baseline shift keeps it in performance. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (§3.14.3, Chapter 8).

*"Random burst errors, average power fine."* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, treat feedback/ORL as the leading performance hypothesis until confirmed. If ORL is fine and bursts track a date code, treat intermittent fiber attach as the leading manufacturing hypothesis. If bursts grow over months at fixed ORL, suspect laser or driver aging (§7.8, §7.13).

*"ELSFP replace fixed it; returned module looks alive on the bench."* Alive LIV with high ORL sensitivity or a dirty MT face supports connector/ORL over laser wear-out; confirm with IL/ORL and recurrence. Dead or kinked LIV supports a reliability path. Split those RMA codes or FIT math blames the wrong mode (§7.14, Appendix F.11.4).

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


<div class="nav-links">
  <a href="ch20-ai-fabric-context">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch22-optical-systems-staff-engineer-interview-questions">Next &rarr;</a>
</div>
