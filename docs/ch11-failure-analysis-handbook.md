---
layout: default
title: "Ch 11: Failure analysis handbook"
---

# 11 Failure analysis handbook

*Read first:* incident workflow; power loss; BER waterfall shift versus floor; eye/TDECQ; lane imbalance; thermal versus aging; yield drop.

*Deep dive:* BER-floor RIN/MPI separation; contamination inspect-before-clean procedure; aging-versus-thermal router.

*Reference:* FA checklist table; FA output categories.

This chapter is a symptom-first field guide. Start with what the bench, production line, or fleet reports, then run one incident path every time.

Preserve the failing state before reseat, reboot, or clean. Those actions often destroy the only evidence that separates contact, firmware, and true wear (Appendix D.16). Next name the population: unit, lane, lot, vendor, site, or fleet. Contain when the population can grow; a perfect mechanism story does not unship yesterday's lot. Classify time behavior (sudden, gradual, intermittent) and which margin ledger moved first (power, noise, timing, spectrum, or control). Choose one measurement that can kill or promote the leading hypotheses at the access you have (black-box versus engineering; Appendix A.2, Appendix D.11). Confirm ownership with a controlled swap, stress, or physical evidence before you call a mechanism confirmed. Do not say "data proves" for the last surviving hypothesis alone.

##### Correction versus recurrence control.

A corrective action repairs the current mechanism. A recurrence control prevents or detects the next occurrence. Cleaning a connector is a correction; inspect-before-connect is a recurrence control. Repairing a station fixture is a correction; a golden-unit drift alarm is a recurrence control. Recalibrating wavelength is a correction; a control-headroom telemetry alarm is a recurrence control.

##### Recurrence-control closure.

An incident is not closed when the unit recovers. Close only when a production or fleet control catches the same signature next time. The best control may be design, supplier process, incoming inspection, ATP, sampled audit, SPC, telemetry, service procedure, or qualification (Appendix D.3, §7.3.13). Each symptom section ends with a short *Recurrence control* line for that signature. Name the FA output category when you file the case (§11.13).

> **Why experienced engineers preserve state before reseating?**
>
> Because reseat, reboot, and clean often destroy the only evidence that separates contact, firmware, and true wear. Scope without a snapshot is theater.

> **Engineering heuristic.** If two explanations fit equally well, prefer the one that requires the fewest independent failures.

<pre class="dectree" aria-label="Preserve"><code>Preserve
  |
Scope
  |
Classify
  |
Locate margin
  |
Falsify
  |
Confirm
  |
Correct
  |
Prevent</code></pre>
This is the only general incident sequence. Symptom-specific trees later in the chapter are local routes inside it. The debugging pyramid in §1.16, the power-versus-signal fork in §4.8, the fleet router in Table 7.7, and the wall-chart trees in Appendix D are the same method at different scales. Earlier chapters own mechanism physics. This chapter owns order of operations. Symptom routes:

Power loss

: Split launch-power loss from coupling, connector, MUX, fiber, monitor, and receiver-plane errors (§11.1).

BER increase

: Named-plane waterfall first; classify shift versus floor, then power, eye, noise, timing, and spectrum (§11.2, §11.2.1).

Eye closure or low ER

: Split bandwidth, drive, bias, reflection, dispersion, and resonance alignment (§11.6, §11.3).

Lane imbalance

: Split source, modulator or ring, filter or MUX, fiber attach, driver, and receiver (§11.4).

Temperature sensitivity

: Track power, wavelength, lock error, TEC or heater headroom, receiver margin, and package stress (§11.12).

Wavelength drift

: Split source movement from filter, ring, TEC, and control-loop movement (§11.5).

Intermittent bursts

: Preserve counters before reseating. Check connector contamination, ORL, supply noise, lock state, and weak attach (§11.8).

Yield drop

: Clear the tester, then split lot, site, process step, assembly, firmware, and calibration (§11.10).

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

4.  Preserve telemetry, then inspect connectors before cleaning (§11.9). Measure insertion loss and ORL. Use a golden fiber and module swap to separate field plant from module.

5.  For a weak lane, compare sibling lanes and per-lane coupling. Lot or lane clustering points toward assembly or MUX variation.

##### Corrective action and recurrence control.

Repair the first plane where power diverges. Correct calibration or monitor coefficients before changing source bias. Add a power check at the earliest production plane that can catch the signature and retain golden-path baselines for fleet comparison. *Recurrence control:* ATP or sample power at that plane; golden-path baselines.

## BER increase: waterfall shift or floor

Interview path: name the optical plane, sweep a waterfall at that plane, then classify shift versus floor before picking instruments. One operating-point BER is not a classification.

<pre class="dectree" aria-label="BER up"><code>BER up
  |
Name plane
  |
Waterfall (BER vs power)
  |-- power not held --&gt; power path (§11.1)
  |-- shift --&gt; sensitivity / OMA / IL / eye / timing
  |-- floor --&gt; §11.2.1
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

3.  If the curve floors, continue in §11.2.1 and split intrinsic RIN, electrical noise, ORL, MPI, and crosstalk.

4.  Use FEC error timing and lane correlation to separate random noise from bursts and shared disturbances. Preserve counters before reseating if the pattern is intermittent.

##### Corrective action and recurrence control.

Restore the margin ledger that moved, then repeat the full BER sweep at loaded corners. Store waterfall shape, not only pass/fail BER, so later fleet changes can be classified without guessing. Interview study treatment: Appendix A.8.9. *Recurrence control:* earliest reliable control for the confirmed ledger (ATP or sensitivity sample, SPC, telemetry, or qualification), not pass/fail BER alone.

### BER floor

##### Observed behavior.

Pre-FEC BER improves as you increase transmit or received power, then stops improving and flattens at a constant floor regardless of how much more power you add. The FEC histogram may still look random (steady RIN) or bursty (MPI, intermittents); the floor shape alone does not decide that split.

##### Likely hypotheses.

A BER floor means additional received power no longer removes the dominant impairment. That is a diagnostic pattern, not one mechanism. RIN can create a floor when signal-proportional intensity noise dominates the receiver budget: $\sigma_\mathrm{RIN} \propto I$, so $Q$ can saturate at $Q_\mathrm{max} = 1/\sqrt{\mathrm{RIN}_\mathrm{lin} \cdot \mathrm{BW}}$ under a dominant-RIN model (§4.3). Do not define every floor as RIN-limited. Other leading mechanisms include multipath interference (MPI), bias-rail noise that converts to equivalent intensity noise (§5.8), pattern-dependent distortion or residual ISI, crosstalk, timing or CDR limits, and DSP or equalization limits.

MPI may produce deterministic interference, power-independent floors, pattern sensitivity, environmental sensitivity, or time-correlated errors depending on coherence, path delay, motion, and modulation. Useful evidence includes ORL dependence, delay-related structure on an ESA, aggressor dependence, pattern dependence, thermal or mechanical sensitivity, and FEC error timing. Do not treat "bursty FEC histogram" alone as proof of MPI.

##### Required access.

- **Black-box / bookended:** attenuation sweep, pre-FEC BER and FEC timing, Tx/Rx power telemetry, temperature, host/module swap, lane remap.

- **Engineering access:** intrinsic RIN, product-board RIN, $\mathrm{RIN}_x\mathrm{OMA}$ at a named ORL, optical eye, controlled reflector, ESA, optical breakout.

##### Measurements and isolation.

1.  Confirm the floor exists: sweep received power (or Tx OMA) at a named reference plane and plot BER vs. power. A floor appears as a horizontal asymptote.

2.  Where engineering access exists, bisect optical vs. electrical RIN: quiet SMU (intrinsic) versus product bias board. If the floor moves, the electrical path is injecting noise (§5.8).

3.  Sweep ORL with a controlled reflector. If the floor worsens with lower ORL, the path is feedback-sensitive. Check isolator, connector, and fiber-attach cleanliness.

4.  Gather MPI evidence (ORL, delay structure, pattern, thermal/mechanical, FEC timing). Treat MPI as a leading mechanism until confirmed.

5.  Compare measured $\mathrm{RIN}_x\mathrm{OMA}$ at the stated ORL against the named PMD revision and ATP limit (for example $-136$ dB/Hz at 17.1 dB ORL for a cited DR-class clause ). State the plane and condition.

##### Corrective action and recurrence control.

If intrinsic RIN is confirmed as the limiter, replace or derate. If electrical RIN, fix the bias supply. If ORL-driven, clean or replace connectors and verify isolator function. If MPI is confirmed from multiple reflections, reduce mated interfaces or improve their ORL. Update the earliest economical control (ATP, sampled audit, SPC, or telemetry), not every deep FA measurement. *Recurrence control:* RIN@ORL sample or ORL audit at the stated plane.

## Low extinction ratio

##### Observed behavior.

Transmitter OMA looks low on the DCA even though average power is in range. TDECQ may or may not fail depending on how the reference equalizer compensates.

##### Likely hypotheses.

Linear extinction ratio is $\mathrm{ER}_\mathrm{lin}=P_1/P_0$ (for PAM4 outer levels use $P_3/P_0$). In decibels, $\mathrm{ER}_\mathrm{dB}=10\log_{10}(\mathrm{ER}_\mathrm{lin})$ and $\mathrm{ER}_\mathrm{lin}=10^{\mathrm{ER}_\mathrm{dB}/10}$. Low ER means the off level is too high or the on level is too low. In an EML, ER is set by EAM reverse bias; in a DML, by modulation depth relative to threshold.

An idealized receiver OMA penalty for finite ER is $$\mathrm{PP}_\mathrm{dB}
=
10\log_{10}\!\left(\frac{\mathrm{ER}_\mathrm{lin}+1}{\mathrm{ER}_\mathrm{lin}-1}\right).$$ At 10 dB ER the penalty is $\sim$0.87 dB; at 6 dB ER it rises to $\sim$2.2 dB (§4.4). This is an idealized receiver-penalty model, not a measured compliance quantity such as TDECQ.

##### Measurements, mechanism isolation, and confirmation.

1.  Measure ER on the DCA (outer OMA / average power, or directly from the histogram levels). Compare against the PMD limit.

2.  **EML:** Sweep EAM bias. ER should peak at the optimal bias point; if the curve has shifted (aged EAM), the operating point needs recalibration. Check EAM bias DAC code vs. datasheet.

3.  **DML:** Check bias current vs. LIV. If bias is close to threshold, modulation depth is limited. Increase bias (but watch thermal rollover and RIN).

4.  **MZM:** Check quadrature bias. If the MZM has drifted off quadrature ($V_\pi/2$ point), extinction degrades. Log the bias-control loop error signal; a saturated loop indicates drift beyond correction range.

5.  **Ring:** Check resonance alignment. If the ring is detuned from the laser wavelength, extinction drops. Monitor the thermal tuner current and wavelength-lock error.

##### Corrective action and recurrence control.

Recalibrate the modulator operating point. For EML aging, update the EAM bias setpoint in firmware or flag the module for replacement if the absorption curve has shifted beyond the correctable range. For MZM drift, verify the bias controller and its monitor PD. For rings, retune or check for neighbor thermal crosstalk (§6.5). *Recurrence control:* ER or modulator-bias check in ATP or cal audit.

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

##### Corrective action and recurrence control.

Confirmed FAU misalignment supports a manufacturing or process control change (incoming inspection or first-article coupling). A thermal gradient supports TEC zoning redesign or derating of the hot lane. Confirmed source wear-out supports lot action and a review of burn-in or life screening effectiveness. Driver mismatch supports IC supplier channel-flatness work. Call each mechanism only after the discriminating evidence above closes. *Recurrence control:* per-lane coupling or TDECQ first-article / SPC, or the earliest reliable control for the confirmed owner.

## Wavelength drift

##### Observed behavior.

In a WDM system, one or more channels walk off the ITU grid or the ring/filter passband. BER degrades as the channel moves off the receiver filter or MUX/DEMUX passband. In ring-modulator CPO, this manifests as sudden unlock of the wavelength control loop.

##### Likely hypotheses.

Laser wavelength moves with temperature and bias current. If the TEC or wavelength-locker servo cannot track, the channel walks off its assigned slot. In microring systems, resonance also moves strongly with temperature, and neighbor heaters create thermal crosstalk that pushes adjacent channels (§6.4, §6.5).

##### Measurements, mechanism isolation, and confirmation.

1.  Measure wavelength on an OSA or wavemeter. Compare to the target grid.

2.  **Laser-side:** Check TEC current. If saturated (at max or min drive), the thermal load exceeds TEC capacity. Check case temperature and airflow.

3.  **Locker-side:** Read the wavelength-locker error signal. A healthy loop holds near zero; drift means the servo is losing lock. Check locker etalon alignment and PD balance.

4.  **Ring CPO:** Check the ring thermal tuner DAC code. If it has railed (max heater power), the ring cannot reach the target wavelength. Check for neighbor heating (all adjacent lanes at full traffic and max case $T$).

5.  **Aging:** Progressive drift over weeks or months raises leading hypotheses of source mode hop, locker/TEC capacity loss, or control recalibration drift. Confirm with wavelength history, TEC or heater headroom, and lock-error trend before naming the mechanism.

##### Corrective action and recurrence control.

TEC saturation: reduce case temperature (improve airflow or liquid cooling) or derate the laser operating current. Ring unlock: increase heater headroom in the design, reduce thermal crosstalk with layout changes, or shift the CW-WDM source grid to re-center the ring tuning range. Aging: schedule preventive replacement (ELSFP hot-swap, §5.14). *Recurrence control:* TEC headroom and lock-error telemetry alarms.

## Eye closure (high TDECQ)

##### Observed behavior.

TDECQ exceeds the PMD limit even though average power and ER look acceptable. The DCA eye appears compressed or distorted after the reference equalizer is applied.

##### Likely hypotheses.

TDECQ measures how much noise the transmitter can tolerate before BER exceeds the FEC threshold, relative to an ideal transmitter (§7.6). High TDECQ means the equalized eye is poor. Common causes: (1) insufficient EO bandwidth (modulator or driver roll-off), (2) poor level linearity (RLM $<$ 0.95; driver or modulator compression), (3) pattern-dependent effects (ISI from bandwidth limit, reflections, or impedance mismatch), (4) chromatic dispersion on FR-class fiber eating into the margin.

##### Measurements, mechanism isolation, and confirmation.

1.  Inspect the raw (unequalized) eye on the DCA. Is it bandwidth-limited (rounded transitions), compressed (uneven levels), or noisy (RIN/jitter)?

2.  **Bandwidth:** Measure EO $S_{21}$ of the modulator (if accessible) or the combined Tx path. Compare to the Nyquist frequency. If 3-dB BW is below Nyquist, bandwidth is the limiter.

3.  **RLM:** Compute relative level mismatch from the DCA histogram. If $\mathrm{RLM} < 0.95$, the PAM4 levels are unevenly spaced. Check driver linearity (swept DAC code) and modulator transfer function (bias sweep).

4.  **Reflections:** Check $S_{11}$ of the RF path (driver to modulator) and the optical return loss. Reflections cause post-cursor ISI the FFE cannot fully cancel.

5.  **Dispersion:** Measure TDECQ with and without the test fiber (TECQ vs. TDECQ). If TDECQ is significantly worse than TECQ, dispersion is the marginal contributor. Check Tx wavelength and chirp against the fiber length and dispersion coefficient.

##### Corrective action and recurrence control.

Bandwidth: upgrade driver or modulator (higher-BW die or peaking network). RLM: tune driver pre-emphasis (DAC levels for each PAM4 symbol). Reflections: fix wirebond, impedance discontinuity, or connector. Dispersion: tighten wavelength tolerance or shorten the fiber (re-route). *Recurrence control:* TDECQ/RLM sample tied to the failing corner.

## Thermal runaway

##### Observed behavior.

Module temperature rises continuously until shutdown (CMIS over-temperature alarm) or until the laser degrades catastrophically. May start subtly: BER creeps up as case $T$ rises during traffic ramp or with neighbor-lane loading.

##### Likely hypotheses.

In a faceplate pluggable, double-digit-watt module power must leave through the cage and heatsink . If airflow is blocked, the cage is overloaded, or the TEC inside the module is fighting a losing battle against junction temperature, the thermal loop runs away. In CPO, the optical engine sits on the switch substrate beside the ASIC; cooling-path faults concentrate heat on the source and ring controls . Both sources are vendor or research orientation, so the product thermal model remains authoritative.

##### Measurements, mechanism isolation, and confirmation.

1.  Read CMIS module temperature and compare to the module's rated case $T$ range. If case $T$ exceeds the max, the system cooling is inadequate.

2.  **Check TEC current.** A TEC at max drive current is saturated; it cannot pump more heat. The junction temperature is higher than the case $T$ suggests.

3.  **Measure LIV at temperature.** If threshold rises and slope drops steeply with $T$, the laser is near thermal rollover (§5.13). The operating point may be marginal.

4.  **Neighbor loading.** Bring all lanes and neighbor modules to full traffic simultaneously. If the problem only appears under full-cage load, the thermal design margin is insufficient.

5.  **Airflow audit.** Inspect the faceplate for blocked vents, incorrect fan speed, or missing blanking panels (bypass airflow). For liquid-cooled systems (CPO, XPO), check coolant flow rate and inlet temperature.

##### Corrective action and recurrence control.

System-level: improve airflow, lower ambient, or reduce module count per cage. Module-level: derate the laser (lower bias current reduces self-heating) or switch to a lower-power module style (LPO instead of retimed, §10.5.1). CPO: ensure the cold-plate thermal interface material (TIM) is intact and the liquid loop meets flow-rate spec. Long-term: specify a tighter thermal class in the laser requirements (§5.6). *Recurrence control:* loaded-cage thermal class in ATP or DV plan.

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

##### Corrective action and recurrence control.

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

4.  Measure insertion loss and ORL across the mated pair at the named plane. Compare to the link-budget allocation (§7.9).

5.  Retest BER and sensitivity. Clearing after cleaning supports contamination as the leading mechanism; confirm with IL/ORL and watch for recurrence. Log connector location and date code.

##### Corrective action and recurrence control.

After evidence is preserved: clean, re-inspect, and verify IL/ORL and BER. Preventive: dust caps on unused ports, "inspect before connect" in the service runbook, sealed cassettes or trunk cables that minimize open-ferrule exposure. For high-power paths (ELSFP, CW-WDM), burn damage requires replacement, not re-cleaning. Track contamination RMAs as a distinct failure code (not "laser failure") so FIT accounting stays honest (§7.14).

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

##### Corrective action and recurrence control.

Restore the changed process or measurement input, add a statistical control at the first observable point, revise ATP only with correlation data, and require a new first-article check before releasing volume (§9.2). *Recurrence control:* SPC at the first separating observable; FAIR after change.

## Aging, thermal response, and margin erosion

Use time scale and recovery to route the incident. A reversible shift during a temperature or neighbor-load sweep is a thermal operating-point problem. A baseline that moves over stress hours or field months is aging. A sudden permanent step after a cycle points toward damage or an assembly defect, not ordinary thermal response.

1.  Return the unit to its starting temperature and operating point. Record whether power, wavelength, bias, TDECQ, and BER recover.

2.  Compare with ship and pre-stress data. Permanent LIV, spectrum, or bias-curve movement supports aging or damage.

3.  Repeat the temperature sweep with source, wavelength-selective element, receiver, and neighbors isolated in turn.

4.  Update the power, noise, timing, spectral, and control ledgers (§5.19). Several small shifts can explain a BER failure even when each component remains inside its stand-alone limit.

5.  Route reversible thermal loss to cooling, control, calibration, or derating. Route cumulative change to HTOL and life-model review. Route lot-clustered permanent steps to manufacturing failure analysis.

On margin versus power, see §5.19: add margin only on the ledger that is empty; do not raise launch power by habit.

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

##### Corrective action and recurrence control.

Restore thermal headroom, correct calibration and control limits, reduce coupling, or derate the operating point. Add the loaded-neighbor temperature ramp to the ATP or the product-readiness plan step that missed it (Chapter 7). *Recurrence control:* loaded-neighbor temperature ramp in ATP or requirement-verification / system-validation evidence.

## Failure-analysis checklist

##### Failure-analysis output categories.

Every FA result should land in one bucket before the case closes:

Design or architecture issue

: Fix architecture or derate.

Manufacturing or process issue

: Fix manufacturing or assembly.

Supplier issue

: Fix incoming quality or supplier process.

Test or monitoring escape

: Improve detection (ATP, sample, SPC, telemetry).

System or integration issue

: Fix host, plant, topology, or deployment interaction.

Software or control issue

: Fix firmware, calibration, or control-loop behavior.

No confirmed mechanism

: Investigation remains open. Keep an owner, containment, next experiment, and review date. Do not treat unknown mechanism as a completed outcome.

The checklist in Table 11.1 is a lifecycle, not a suggestion list. Each step removes a class of uncertainty before the next step spends lab time. Skip Preserve and you often destroy the only evidence that separated host, plant, and product.

<table class="book-table"><tr><th>Step</th><th>Question</th><th>Required record</th></tr><tr><td>Preserve</td><td>What evidence will a reseat, reboot, clean, or retest destroy?</td><td>CMIS, BER and FEC history, rails, temperature, firmware, fixture, and time</td></tr><tr><td>Scope</td><td>One unit, lane, lot, vendor, site, or fleet?</td><td>Population and correlation plot</td></tr><tr><td>Classify</td><td>Sudden or gradual, constant or intermittent, thermal or cumulative?</td><td>Timeline and recovery test</td></tr><tr><td>Locate margin</td><td>Did power, noise, timing, spectrum, or control move first?</td><td>Golden comparison and margin ledger</td></tr><tr><td>Falsify</td><td>Which measurement best separates the leading hypotheses?</td><td>Expected result for each hypothesis before the test</td></tr><tr><td>Confirm</td><td>Does the fault follow the suspected block under a controlled swap or stress?</td><td>Repeated failure and passing control</td></tr><tr><td>Correct</td><td>Does the fix restore the original failing condition with margin?</td><td>Before and after data at loaded corners</td></tr><tr><td>Prevent</td><td>Where can production or fleet monitoring catch recurrence earliest?</td><td>Earliest reliable control, owner, and due date</td></tr></table>
**Table 11.1.** Failure-analysis checklist. The incident is not closed until the cause is reproduced, corrected, and covered by a recurrence control.

### Reading the failure-analysis checklist

##### Preserve.

What volatile evidence will a reseat, reboot, clean, or retest destroy? Snapshot CMIS, BER/FEC history, rails, temperature, firmware, fixture, and time before any invasive action. Photograph endfaces before cleaning if contamination is plausible. **Exit when** the failing-state pack is filed. **Decision:** proceed to scope, or stop ops from "just reseating." **Risk if skipped:** the fail clears and you learn nothing.

##### Scope / classify / locate (short).

Name the population (unit, lot, vendor, site, fleet) before instruments (§7.14). Record sudden versus gradual and whether cool-down recovers. Name which ledger moved first: power, noise, timing, spectrum, or control (Appendix A.8.4). **Exit when** population, time class, and first-moving ledger are evidenced. **Risk if skipped:** wrong containment width or the wrong instrument tour.

##### Falsify.

Which single measurement best separates the leading hypotheses? Write expected results before you run the test. **Exit when** one measurement kills or promotes the leading set. **Decision:** move survivors to Confirm, or reopen Locate margin. **Risk if skipped:** confirmation bias.

##### Confirm / correct (short).

Confirm the fault follows the suspected block under swap or stress, then show before/after margin at the original failing corner. **Exit when** ownership is assigned and the fix restores that corner. **Risk if skipped:** you "fix" the wrong block or ship a lab-only cure.

A swap is an ownership experiment, not automatically a root-cause experiment. A module swap may also disturb connectors, reset firmware, alter thermal contact, and change calibration state. Record every condition that changes and, where possible, reverse the swap to verify that the symptom follows the intended variable.

##### Prevent.

Where can production or fleet monitoring catch recurrence earliest? Choose the earliest reliable and economical control: design, supplier process, incoming inspection, ATP, sampled audit, SPC, telemetry, service procedure, or qualification. Version the chosen control with owner and due date. **Exit when** recurrence control is owned and the cohort is under watch. **Decision:** close the incident, or monitor-only if rate and impact justify it (Table A.1). **Risk if skipped:** you solve one RMA and train the factory to recreate it.

### Evidence states

> **Evidence states**\
>
> Observation
>
> : A directly measured fact (example: pre-FEC errors rose at $72$°C).
>
> Correlation
>
> : Two observations move together (example: failures concentrate in lot A).
>
> Leading hypothesis
>
> : The mechanism that currently best explains the evidence.
>
> Ownership localization
>
> : The symptom follows a block, path, station, or population under controlled change.
>
> Mechanism confirmation
>
> : The physical or electrical mechanism is reproduced or supported by discriminating and, where appropriate, physical evidence.
>
> Confirmed root cause
>
> : The mechanism, enabling condition, and control gap are understood well enough that the corrective action prevents recurrence.
>
> A surviving hypothesis and a localized block are not automatically a confirmed root cause.

### Incident record template

The checklist produces one compact record. Do not invent a second lifecycle; fill these fields as you walk the steps:

Observed symptom

: What the fleet, line, or bench reported.

Affected population

: Lane, module, lot, site, supplier, firmware, fleet.

First occurrence and frequency

: When it started and how often it returns.

Operating condition

: Temperature, traffic, host, plant, dwell.

Reference plane

: Named optical or electrical plane for the measurement.

Volatile telemetry preserved

: CMIS, FEC, rails, EQ, route, workload time.

Recent changes

: Firmware, lots, fixtures, routes, maintenance.

Containment

: What was held, drained, or watched, and why.

Leading hypotheses

: Ranked survivors after falsify.

Next discriminating measurement

: Expected result for each survivor.

Confirmed mechanism status

: Observation / localization / confirmed / open.

Corrective action

: What repaired the current mechanism.

Recurrence control

: What prevents or detects the next occurrence.

Owner and due date

: Who owns the open work and when it is reviewed.

### Why the steps occur in this order

Preserve first because reseat and reboot destroy state. Scope next so containment width matches the population. Classify and locate margin before falsify so you pick the cheap separating test. Confirm before correct so you do not ship a story. Prevent last so the factory and fleet catch the next escape. Later steps must not compensate for a missing preserve pack or a wrong scope.

## Interview takeaway

**Key idea.** A useful failure analysis starts with a symptom and ends with a new control. Preserve the failing state, split shared from local behavior, clear the measurement system, and choose one measurement that can falsify the leading hypothesis. Return fleet and production evidence to the appropriate product-readiness step: requirement, architecture, characterization, system validation, reliability qualification, manufacturing validation, ATP, or fleet control. The corrective action is incomplete until production or fleet data show that the same signature no longer escapes.

Junior mistake: reseat first, or close without a recurrence control (§7.14, Appendix B, Appendix C, Appendix F).

### Interview Q&A: Failure Analysis

Practice speaking these answers aloud. Prefer first-person incident reasoning over instrument inventories. Detail lives in §11.13, §11.13.2, §4.8, §7.14.

##### Question 1. Walk me through your failure-analysis process.

*Tests:* complete incident structure and disciplined ordering.

*Spoken answer.* "I begin by preserving the failing state because a reboot, reseat, clean, or retest may erase the evidence. Then I scope the population: lane, module, host, lot, supplier, site, firmware, or fleet. I classify the time behavior as sudden, gradual, or intermittent and identify whether power, noise, timing, spectrum, or control moved first. I choose the lowest-cost measurement that separates the leading hypotheses, while containing the affected population if exposure can grow. I call a mechanism confirmed only after controlled reproduction, a swap that follows the suspected block, or physical evidence. The case closes when the original failing condition is restored with margin and a recurrence control changes" (§11.13).

*Pressure follow-up.* "Which step do engineers most commonly skip?"\
*Answer pivot.* "Preserving state and scoping the population. Teams often reseat the unit, lose the evidence, and then spend days trying to recreate a failure they already had."

*Trap:* "I reproduce the problem, identify the bad component, replace it, and retest."

##### Question 2. What evidence do you preserve before reseating, rebooting, cleaning, or power cycling?

*Tests:* evidence preservation and incident metadata.

*Spoken answer.* "I would capture volatile evidence before changing the system: module and host state, CMIS pages, alarms, transmit and receive power, lane-resolved BER and FEC history, retrains, loss-of-lock events, temperature, supply rails, firmware and configuration, equalizer state where available, route and workload timing, and the exact failure chronology. If contamination is plausible, I photograph and inspect the endface before cleaning. I also record the physical topology, serial numbers, lots, host ports, peer modules, fibers, and recent changes. The goal is to preserve enough state to distinguish contact, software, thermal, optical, and wear mechanisms later."

*Pressure follow-up.* "Operations already reseated the module and the problem disappeared. What do you do?"\
*Answer pivot.* "I treat the recovery as evidence, not resolution. I preserve what remains, identify exactly what changed during the reseat, inspect the original path, and reproduce under controlled connector, thermal, firmware, and mechanical conditions."

*Trap:* "I reseat first because that quickly tells me whether the module is bad."

##### Question 3. How do you scope a failure and decide containment?

*Tests:* population reasoning, exposure, and reversible action.

*Spoken answer.* "I first determine whether the symptom is isolated to one lane, one module, one host port, one fiber path, one lot, one site, one firmware revision, or a broader fleet cohort. I use serial genealogy, installation age, topology, supplier and date code, and event timing to find where good and bad populations separate. Containment should match that evidence. I may drain one link, hold a lot, pause one supplier revision, or increase telemetry while the mechanism remains open. I do not wait for perfect root-cause certainty when the affected population can continue growing, but I also avoid stopping an unrelated fleet without evidence."

*Pressure follow-up.* "The failure correlates with one date code. Do you stop the entire lot?"\
*Answer pivot.* "I would provisionally contain the affected cohort if impact justifies it, while checking whether date code is confounded with site, host, firmware, station, or installation age. Correlation guides containment width; it does not confirm mechanism" (§11.13.2).

*Trap:* "I contain only the failed units until root cause is proven."

##### Question 4. BER is rising, but average received power is stable. What do you do next?

*Tests:* power versus signal quality and BER-waterfall reasoning.

*Spoken answer.* "Stable average power makes gross loss less likely, but it does not clear the optical path. I would name the receive reference plane and run a BER-versus-power waterfall. If the curve shifts, I investigate receiver sensitivity, OMA, eye quality, timing, dispersion, and insertion loss. If it forms a floor, I investigate signal-proportional noise, RIN, reflections or MPI, crosstalk, rail noise, pattern dependence, timing, and equalization limits. I also inspect the lane-resolved FEC timing because steady random errors and short bursts suggest different mechanisms. I would not increase launch power until I know which margin ledger is empty" (§11.2, §4.8).

*Pressure follow-up.* "What if attenuation improves BER initially, but the curve then flattens?"\
*Answer pivot.* "That is a shifted curve with a floor. More power repairs one impairment until another becomes dominant. I need to explain both before declaring the link healthy."

*Trap:* "Power is stable, so I would replace the receiver."

##### Question 5. One lane is weak while the sibling lanes are healthy. How do you isolate it?

*Tests:* shared versus local ownership and lane-remap evidence.

*Spoken answer.* "One weak lane strongly raises local hypotheses: source or modulator variation, one driver or TIA channel, fiber-array alignment, one MUX path, local receiver behavior, or a thermal gradient. I compare per-lane power, OMA, wavelength, TDECQ, BER, FEC timing, bias or control headroom, and temperature. If supported, I remap the electrical lane or use a known-good electrical channel to see whether the symptom follows the optical path or the electrical channel. I compare coupling and sibling-lane behavior before blaming shared firmware or the common thermal system" (§11.4).

*Pressure follow-up.* "The failure follows the module after a host-port swap. Is the module root cause confirmed?"\
*Answer pivot.* "It localizes ownership toward the module, but it does not confirm the internal mechanism. I still have to separate its source, modulation, coupling, filtering, receiver, firmware, and connector interfaces."

*Trap:* "One lane failed, so the laser array contains a bad emitter."

##### Question 6. The link fails intermittently and recovers after reseating or power cycling. How do you investigate it?

*Tests:* intermittent evidence, triggered capture, and state-reset ambiguity.

*Spoken answer.* "I would avoid treating recovery as a fix. Before disturbance I want event-triggered FEC, retrain and lock history, CMIS state, power, temperature, rail and clock behavior, wavelength-control state, and neighbor activity. I scope whether bursts share time across lanes or modules. Then I apply one controlled disturbance at a time: connector motion, thermal ramp, neighbor loading, rail loading, firmware transition, or vibration. A reseat can clean contamination, change fiber stress, restore a contact, and reset firmware simultaneously, so it is not a discriminating experiment unless those effects are separated" (§11.8).

*Pressure follow-up.* "The supplier cannot reproduce the failure during a short room-temperature bench test."\
*Answer pivot.* "That is a no-fault-found result, not evidence that the field was healthy. I would reproduce the original temperature, dwell, traffic, connector, firmware, and state-transition conditions and provide the original event history."

*Trap:* "If power cycling clears the failure, it is probably firmware."

##### Question 7. A module fails only at high temperature. How do you separate thermal response from aging or permanent damage?

*Tests:* reversibility, chronology, and margin-ledger comparison.

*Spoken answer.* "I return the unit to its original temperature and operating point and record whether power, wavelength, bias, control headroom, TDECQ, sensitivity, and BER recover. A repeatable reversible shift suggests operating-point or thermal-margin behavior. A baseline that has moved relative to ship or pre-stress data suggests aging or damage. I then isolate source, wavelength-selective element, receiver, neighbors, and cooling path to identify which ledger moves first. A sudden permanent step after cycling suggests damage or assembly failure rather than ordinary aging" (§11.12).

*Pressure follow-up.* "The unit recovers fully after cooling. Can it ship?"\
*Answer pivot.* "Not automatically. If the intended envelope includes the failing temperature or loaded-neighbor condition, the design lacks required margin even though the change is reversible."

*Trap:* "If the unit recovers at room temperature, there is no reliability issue."

##### Question 8. How do you investigate wavelength drift or loss of wavelength lock?

*Tests:* source versus filter/control ownership.

*Spoken answer.* "I measure actual wavelength and align it in time with case temperature, laser bias, TEC current, ring or heater code, lock error, neighbor activity, and BER. I ask whether the source moved, the filter or ring moved, or the control loop exhausted its authority. A railed TEC or heater indicates lost control headroom, not necessarily a bad laser. I repeat with neighbors off and on, and where possible I hold the source fixed while moving the wavelength-selective element, then reverse the experiment. The corrective action depends on whether the limitation is thermal design, calibration, source stability, crosstalk, or loop behavior" (§11.5).

*Pressure follow-up.* "The error disappears after recalibration. Is recalibration the final corrective action?"\
*Answer pivot.* "Only if the required setpoint remains stable with adequate control headroom. If the calibration keeps moving or the actuator rails, recalibration is masking physical drift rather than correcting the mechanism."

*Trap:* "Wavelength drift means the laser wavelength specification is too loose."

##### Question 9. A module passed ATP but begins failing after 90 days, and failures cluster by one lot. Is this a manufacturing escape or reliability failure?

*Tests:* classification across manufacturing, qualification, and field aging.

*Spoken answer.* "I would not classify it from those facts alone. The ninety-day clock and lot clustering raise both an early-life reliability mechanism and a process or material escape. I would compare installation-age distributions, first-pass ATP data, rework history, supplier genealogy, thermal exposure, host and site mix, and the physical failure signature. If evidence connects the mechanism to an uncontrolled process or a detectable condition that production controls missed, it is a manufacturing escape. If representative hardware passed production correctly but a life mechanism was inadequately covered, it is a qualification gap. It may also be both" (Chapter 9, Chapter 8, §9.6).

*Pressure follow-up.* "Should ATP be tightened immediately?"\
*Answer pivot.* "I may add temporary containment, but a permanent ATP change requires a validated observable correlated to the mechanism. Some aging mechanisms are better controlled by design, supplier process, qualification, or sampled audit."

*Trap:* "It passed ATP, so the factory is cleared and qualification must be wrong."

##### Question 10. Yield drops suddenly, or two production stations disagree. What is your first move?

*Tests:* measurement clearing before product or supplier ownership.

*Spoken answer.* "I contain suspect work in process and freeze test software, limits, calibration, fixtures, firmware, and recent changes. Before blaming product or supplier material, I run golden and range-spanning units across the stations and compare failed units on the trusted reference bench. Then I stratify first-pass failures and parameter distributions by test row, station, fixture, shift, operator, material lot, assembly site, firmware, and build order. The first point where good and bad populations separate determines the next experiment. I do not relax limits or open supplier corrective action until measurement-system effects and confounding are addressed" (§11.10, Chapter 9).

*Pressure follow-up.* "One station reads 0.4 dB lower, but all units still pass specification. Is that acceptable?"\
*Answer pivot.* "Not without understanding the offset. It may consume guardband, distort yield comparisons, and hide future drift. I would correct or formally account for the station bias before relying on its data."

*Trap:* "The lower-yield station should use a corrected acceptance limit."

##### Question 11. The supplier returns "no fault found." How do you respond?

*Tests:* supplier evidence package and reproducibility.

*Spoken answer.* "I would first compare their test conditions with the original failure conditions: temperature, traffic, host, firmware, fiber plant, connector state, dwell, reference plane, and event timing. I provide the failing-state pack, population data, expected symptom, and the conditions required to reproduce it. I ask them to preserve the returned unit and avoid automatic cleaning, firmware reset, or recalibration before inspection. If the mechanism remains unconfirmed, the case stays open with an interim containment and explicit next experiment. No-fault-found is an investigation state, not a root-cause category."

*Pressure follow-up.* "The unit passes every supplier test. Do you return it to service?"\
*Answer pivot.* "Only if the original risk is bounded and the service decision is explicit. For an intermittent high-impact failure, I may keep it out of service while using it for controlled reproduction."

*Trap:* "If the supplier cannot reproduce it, the issue belongs to the customer environment."

##### Question 12. Give me a 60-second failure-analysis plan for an optical fleet incident.

*Tests:* complete Staff-level incident answer.

*Spoken answer.* "I begin by preserving the failing state and aligning module, host, link, topology, and workload timestamps. Then I scope the affected population by lane, module, lot, supplier, firmware, site, and install age and apply reversible containment where exposure can grow. I classify the symptom by time behavior and identify whether power, noise, timing, spectrum, or control moved first. I choose the lowest-cost measurement that separates the leading hypotheses, such as a BER waterfall, controlled swap, loaded thermal sweep, ORL test, or station correlation. I call the mechanism confirmed only after reproduction, controlled ownership evidence, or physical analysis. I verify the corrective action at the original failing corner and close only after a requirement, qualification, ATP, SPC, supplier, telemetry, or service control changes."

*Pressure follow-up.* "What would make you stop deployment before mechanism confirmation?"\
*Answer pivot.* "A growing or correlated population, high workload impact, weak ability to bound exposure, or a potentially destructive mechanism. Containment can be reversible; the cost of waiting may not be."

*Trap:* "I would reproduce the failure, replace the suspected module, and monitor the fleet."

Score each answer using the shared chapter-interview rubric in Appendix A.12.1. Repeat any answer that does not preserve evidence, scope the population, select a discriminating measurement, and identify both containment and recurrence control.


<div class="nav-links">
  <a href="ch10-ai-datacenter-networking">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch12-one-week-optical-systems-interview-review">Next &rarr;</a>
</div>
