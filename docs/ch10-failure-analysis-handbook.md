---
layout: default
title: "Ch 10: Failure analysis handbook"
---

# Failure analysis handbook

This chapter is a symptom-first field guide. Start with what the bench, production line, or fleet reports. Preserve the failing state until its evidence has been captured, then use the same workflow for every incident: $$\begin{split}
\text{observe} &\longrightarrow \text{scope unit, lot, vendor, site, or fleet}\\
&\longrightarrow \text{classify sudden or gradual}\\
&\longrightarrow \text{identify the changing margin}\\
&\longrightarrow \text{measure, isolate, correct, and prevent recurrence}.
\end{split}$$ Choose each measurement for its ability to separate competing hypotheses. The debugging pyramid in §1.8, the power-versus-signal fork in §4.8, and the fleet router in Table 7.5 provide the same method at different scales.

Power loss

: Split launch-power loss from coupling, connector, MUX, fiber, monitor, and receiver-plane errors (§10.1).

BER increase

: Separate a shifted waterfall from a BER floor, then check power, eye quality, noise, timing, and spectrum (§10.2, §10.3).

Eye closure or low ER

: Split bandwidth, drive, bias, reflection, dispersion, and resonance alignment (§10.7, §10.4).

Lane imbalance

: Split source, modulator or ring, filter or MUX, fiber attach, driver, and receiver (§10.5).

Temperature sensitivity

: Track power, wavelength, lock error, TEC or heater headroom, receiver margin, and package stress (§10.13).

Wavelength drift

: Split source movement from filter, ring, TEC, and control-loop movement (§10.6).

Intermittent bursts

: Preserve counters before reseating. Check connector contamination, ORL, supply noise, lock state, and weak attach (§10.9).

Yield drop

: Clear the tester, then split lot, site, process step, assembly, firmware, and calibration (§10.11).

The cases below provide the detailed measurements and corrective actions. Use the failure and debug callouts in Chapters 3--9 as shorter versions of the same method. Earlier chapters own the mechanism physics. This chapter owns the order of operations.

## Power loss

##### Observed behavior.

Received power or OMA falls at one or more lanes. BER may remain stable at first, then rise as receiver margin is consumed. The module monitor and an external power meter may disagree.

##### Likely hypotheses.

Launch power can fall because the laser is disabled, thermally rolled over, or aged. Power can disappear after the source through modulator loss, coupling shift, MUX loss, fiber bend, connector contamination, or a wrong reference-plane calibration. A drifting monitor photodiode can report loss that does not exist.

##### Measurements and root-cause isolation.

1.  Compare CMIS Tx and Rx power, external power at the faceplate, bias current, and case temperature. Disagreement identifies the first suspect plane.

2.  Walk optical power plane by plane with a known source and calibrated meter. Do not change bias or equalization while locating the loss.

3.  Rerun LIV at the failing temperature. Moved LIV points toward the source; stable LIV points toward the optical path or monitor.

4.  Inspect and clean connectors, then measure insertion loss and ORL. Use a golden fiber and module swap to separate field plant from module.

5.  For a weak lane, compare sibling lanes and per-lane coupling. Lot or lane clustering points toward assembly or MUX variation.

##### Corrective action and recurrence control.

Repair the first plane where power diverges. Correct calibration or monitor coefficients before changing source bias. Add a power check at the earliest production plane that can catch the signature and retain golden-path baselines for fleet comparison.

## BER increase: waterfall shift or floor

##### Observed behavior.

Pre-FEC BER rises, but the first task is to determine whether the whole BER waterfall moved to higher received power or whether it stopped improving at a horizontal floor.

##### Likely hypotheses.

A shifted waterfall points toward lost power, receiver sensitivity, eye closure, timing, or dispersion. A floor points toward signal-proportional noise, reflection, crosstalk, or burst errors. The distinction prevents a power fix from being applied to a noise-limited link.

##### Measurements and root-cause isolation.

1.  Sweep received power and plot BER rather than recording one operating point.

2.  If the waterfall shifted, compare received OMA, TDECQ, receiver sensitivity, equalizer taps, wavelength, and temperature with the golden baseline.

3.  If the curve floors, follow §10.3 and split intrinsic RIN, electrical noise, ORL, MPI, and crosstalk.

4.  Use FEC error timing and lane correlation to separate random noise from bursts and shared disturbances.

##### Corrective action and recurrence control.

Restore the margin ledger that moved, then repeat the full BER sweep at loaded corners. Store waterfall shape, not only pass/fail BER, so later fleet changes can be classified without guessing.

## BER floor

##### Observed behavior.

Pre-FEC BER improves as you increase transmit power, then stops improving and flattens at a constant floor regardless of how much more power you add.

##### Likely hypotheses.

A BER floor means a noise source that grows with signal power dominates the link. The classic cause is *relative intensity noise* (RIN): because $\sigma_\mathrm{RIN} \propto I$, once RIN dominates the noise budget, signal and noise grow together and $Q$ saturates at $Q_\mathrm{max} = 1/\sqrt{\mathrm{RIN}_\mathrm{lin} \cdot \mathrm{BW}}$ (§4.3). Other causes: multipath interference (MPI) from dirty connectors or high back-reflection, or broadband noise on the laser bias rail that converts to equivalent RIN (§5.8).

##### Measurements and root-cause isolation.

1.  Confirm the floor exists: sweep received power (or Tx OMA) and plot BER vs. power. A healthy link has a steep waterfall; a floor appears as a horizontal asymptote.

2.  **Bisect optical vs. electrical RIN.** Measure RIN with a quiet SMU powering the laser (intrinsic RIN). Then repeat with the product bias board connected. If the floor moves, the electrical path is injecting noise (§5.8).

3.  **Sweep ORL.** Add a controlled reflector. If BER floor worsens with lower ORL, the laser is feedback-sensitive. Check isolator, connector, and fiber-attach cleanliness.

4.  **Check for MPI.** Look at the ESA (electrical spectrum analyzer) for discrete spurs at frequencies corresponding to round-trip delays of reflective interfaces. MPI creates bursty errors; the FEC histogram shows clustered symbol errors rather than random ones.

5.  **Confirm RIN spec.** Compare measured $\mathrm{RIN}_x\mathrm{OMA}$ at the stated ORL against the PMD or ATP limit (e.g. $-136$ dB/Hz at 17.1 dB ORL for DR-class links ). If the part exceeds spec, reject.

##### Corrective action and recurrence control.

If intrinsic RIN is the limiter, the laser is marginal or aged; replace or derate. If electrical RIN, fix the bias supply (better PSRR, star ground, local decoupling). If ORL-driven, clean or replace connectors and verify isolator function. If MPI from multiple reflections, reduce the number of mated interfaces or improve their ORL.

## Low extinction ratio

##### Observed behavior.

Transmitter OMA looks low on the DCA even though average power is in range. TDECQ may or may not fail depending on how the reference equalizer compensates.

##### Likely hypotheses.

Extinction ratio $\mathrm{ER} = P_1/P_0$ sets how far apart the one and zero optical levels are for a given average power. Low ER means the zero level is too high (the modulator does not fully extinguish) or the one level is too low. In an EML, ER is set by the EAM reverse bias: insufficient bias leaves residual transmission in the off-state. In a DML, ER depends on modulation depth relative to threshold. The OMA penalty for finite ER is $\mathrm{PP} = (\mathrm{ER}+1)/(\mathrm{ER}-1)$: at 10 dB ER the penalty is $\sim$`<!-- -->`{=html}0.87 dB; at 6 dB ER it rises to $\sim$`<!-- -->`{=html}2.2 dB (§4.4).

##### Measurements and root-cause isolation.

1.  Measure ER on the DCA (outer OMA / average power, or directly from the histogram levels). Compare against the PMD limit.

2.  **EML:** Sweep EAM bias. ER should peak at the optimal bias point; if the curve has shifted (aged EAM), the operating point needs recalibration. Check EAM bias DAC code vs. datasheet.

3.  **DML:** Check bias current vs. LIV. If bias is close to threshold, modulation depth is limited. Increase bias (but watch thermal rollover and RIN).

4.  **MZM:** Check quadrature bias. If the MZM has drifted off quadrature ($V_\pi/2$ point), extinction degrades. Log the bias-control loop error signal; a saturated loop indicates drift beyond correction range.

5.  **Ring:** Check resonance alignment. If the ring is detuned from the laser wavelength, extinction drops. Monitor the thermal tuner current and wavelength-lock error.

##### Corrective action and recurrence control.

Recalibrate the modulator operating point. For EML aging, update the EAM bias setpoint in firmware or flag the module for replacement if the absorption curve has shifted beyond the correctable range. For MZM drift, verify the bias controller and its monitor PD. For rings, retune or check for neighbor thermal crosstalk (§6.5).

## Lane imbalance

##### Observed behavior.

In a multi-lane module (DR4, FR4, DR8), one or more lanes show significantly different OMA, TDECQ, or pre-FEC BER compared with siblings in the same module. The weak lane may be marginal or failing while others are healthy.

##### Likely hypotheses.

Multi-lane modules share a substrate, laser array (or CW-WDM source), and thermal environment. Lane-to-lane variation comes from: (1) die-level non-uniformity in the laser or modulator array (threshold, slope, $V_\pi$, coupling), (2) packaging variation in fiber-array alignment (one channel of the FAU slightly misaligned), (3) driver or TIA channel mismatch on the electronic IC, or (4) thermal gradient across the die (edge lanes hotter or cooler than center lanes).

##### Measurements and root-cause isolation.

1.  Measure all lanes: OMA, ER, TDECQ, RIN, wavelength. Identify the outlier.

2.  **Is it optical or electrical?** Swap the electrical lane assignment (if the host supports lane remapping) or test the suspect optical lane with a known-good driver channel. If the problem follows the optical path, it is laser/modulator/fiber-attach. If it follows the electrical channel, it is driver/TIA.

3.  **Check coupling.** Measure per-lane fiber-coupled power with an integrating sphere or power meter array. A single weak lane with normal LIV suggests FAU misalignment.

4.  **Thermal map.** Use an IR camera or CMIS per-lane monitors (if available) to check for hot spots. Edge lanes near the package wall or near a TEC boundary may run hotter.

5.  **Laser array aging.** If the imbalance grows over time (HTOL or field life), one laser in the array is aging faster (threshold rise, slope drop). Compare LIV curves at $t_0$ and now.

##### Corrective action and recurrence control.

FAU misalignment is a manufacturing escape; tighten incoming inspection or first-article coupling specs. Thermal gradient: redesign TEC zoning or derate the hot lane. Laser aging: flag the lot and check burn-in screening effectiveness. Driver mismatch: work with the IC supplier on channel-to-channel gain flatness.

## Wavelength drift

##### Observed behavior.

In a WDM system, one or more channels walk off the ITU grid or the ring/filter passband. BER degrades as the channel moves off the receiver filter or MUX/DEMUX passband. In ring-modulator CPO, this manifests as sudden unlock of the wavelength control loop.

##### Likely hypotheses.

Laser wavelength moves with temperature and bias current. If the TEC or wavelength-locker servo cannot track, the channel walks off its assigned slot. In microring systems, resonance also moves strongly with temperature, and neighbor heaters create thermal crosstalk that pushes adjacent channels (§6.4, §6.5).

##### Measurements and root-cause isolation.

1.  Measure wavelength on an OSA or wavemeter. Compare to the target grid.

2.  **Laser-side:** Check TEC current. If saturated (at max or min drive), the thermal load exceeds TEC capacity. Check case temperature and airflow.

3.  **Locker-side:** Read the wavelength-locker error signal. A healthy loop holds near zero; drift means the servo is losing lock. Check locker etalon alignment and PD balance.

4.  **Ring CPO:** Check the ring thermal tuner DAC code. If it has railed (max heater power), the ring cannot reach the target wavelength. Check for neighbor heating (all adjacent lanes at full traffic and max case $T$).

5.  **Aging:** If drift is progressive over weeks/months, suspect laser mode hop or gradual TEC degradation (reduced $\Delta T$ capacity).

##### Corrective action and recurrence control.

TEC saturation: reduce case temperature (improve airflow or liquid cooling) or derate the laser operating current. Ring unlock: increase heater headroom in the design, reduce thermal crosstalk with layout changes, or shift the CW-WDM source grid to re-center the ring tuning range. Aging: schedule preventive replacement (ELSFP hot-swap, §5.14).

## Eye closure (high TDECQ)

##### Observed behavior.

TDECQ exceeds the PMD limit even though average power and ER look acceptable. The DCA eye appears compressed or distorted after the reference equalizer is applied.

##### Likely hypotheses.

TDECQ measures how much noise the transmitter can tolerate before BER exceeds the FEC threshold, relative to an ideal transmitter (§7.4). High TDECQ means the equalized eye is poor. Common causes: (1) insufficient EO bandwidth (modulator or driver roll-off), (2) poor level linearity (RLM $<$ 0.95; driver or modulator compression), (3) pattern-dependent effects (ISI from bandwidth limit, reflections, or impedance mismatch), (4) chromatic dispersion on FR-class fiber eating into the margin.

##### Measurements and root-cause isolation.

1.  Inspect the raw (unequalized) eye on the DCA. Is it bandwidth-limited (rounded transitions), compressed (uneven levels), or noisy (RIN/jitter)?

2.  **Bandwidth:** Measure EO $S_{21}$ of the modulator (if accessible) or the combined Tx path. Compare to the Nyquist frequency. If 3-dB BW is below Nyquist, bandwidth is the limiter.

3.  **RLM:** Compute relative level mismatch from the DCA histogram. If $\mathrm{RLM} < 0.95$, the PAM4 levels are unevenly spaced. Check driver linearity (swept DAC code) and modulator transfer function (bias sweep).

4.  **Reflections:** Check $S_{11}$ of the RF path (driver to modulator) and the optical return loss. Reflections cause post-cursor ISI the FFE cannot fully cancel.

5.  **Dispersion:** Measure TDECQ with and without the test fiber (TECQ vs. TDECQ). If TDECQ is significantly worse than TECQ, dispersion is the marginal contributor. Check Tx wavelength and chirp against the fiber length and dispersion coefficient.

##### Corrective action and recurrence control.

Bandwidth: upgrade driver or modulator (higher-BW die or peaking network). RLM: tune driver pre-emphasis (DAC levels for each PAM4 symbol). Reflections: fix wirebond, impedance discontinuity, or connector. Dispersion: tighten wavelength tolerance or shorten the fiber (re-route).

## Thermal runaway

##### Observed behavior.

Module temperature rises continuously until shutdown (CMIS over-temperature alarm) or until the laser degrades catastrophically. May start subtly: BER creeps up as case $T$ rises during traffic ramp or with neighbor-lane loading.

##### Likely hypotheses.

In a faceplate pluggable, double-digit-watt module power must leave through the cage and heatsink . If airflow is blocked, the cage is overloaded, or the TEC inside the module is fighting a losing battle against junction temperature, the thermal loop runs away. In CPO, the optical engine sits on the switch substrate beside the ASIC; cooling-path faults concentrate heat on the source and ring controls . Both sources are vendor or research orientation, so the product thermal model remains authoritative.

##### Measurements and root-cause isolation.

1.  Read CMIS module temperature and compare to the module's rated case $T$ range. If case $T$ exceeds the max, the system cooling is inadequate.

2.  **Check TEC current.** A TEC at max drive current is saturated; it cannot pump more heat. The junction temperature is higher than the case $T$ suggests.

3.  **Measure LIV at temperature.** If threshold rises and slope drops steeply with $T$, the laser is near thermal rollover (§5.13). The operating point may be marginal.

4.  **Neighbor loading.** Bring all lanes and neighbor modules to full traffic simultaneously. If the problem only appears under full-cage load, the thermal design margin is insufficient.

5.  **Airflow audit.** Inspect the faceplate for blocked vents, incorrect fan speed, or missing blanking panels (bypass airflow). For liquid-cooled systems (CPO, XPO), check coolant flow rate and inlet temperature.

##### Corrective action and recurrence control.

System-level: improve airflow, lower ambient, or reduce module count per cage. Module-level: derate the laser (lower bias current reduces self-heating) or switch to a lower-power module style (LPO instead of retimed, §9.5.1). CPO: ensure the cold-plate thermal interface material (TIM) is intact and the liquid loop meets flow-rate spec. Long-term: specify a tighter thermal class in the laser requirements (§5.6).

## Intermittent failures

##### Observed behavior.

Links flap, lose lock, or show bursts of FEC errors while average power and a short bench BER test look normal. The symptom may clear after reseating, cooling, or restarting firmware.

##### Likely hypotheses.

Intermittent faults come from contacts, reflections, weak optical or electrical attach, supply noise, wavelength-lock loss, firmware state, or environmental stress. Reseating can remove the evidence by cleaning a contact, changing fiber stress, or resetting a state machine.

##### Measurements and root-cause isolation.

1.  Freeze CMIS state, FEC error timing, LOS or LOL history, temperatures, rails, lock error, and neighbor activity before touching hardware.

2.  Scope the pattern across lane, module, tray, rack, lot, and firmware revision. Shared timing points toward power, cooling, firmware, or a shared source.

3.  Correlate bursts with Rx power, ORL, supply and clock spurs, lock-loop state, vibration, and temperature. Use trigger capture rather than averages.

4.  Run controlled disturbance tests one at a time: connector motion, thermal ramp, neighbor load, rail load, and firmware state transition.

5.  Repeat on a golden unit and fixture. If the fault follows the unit, inspect fiber attach, solder, contacts, and control logs before destructive analysis.

##### Corrective action and recurrence control.

Fix the confirmed contact, attach, supply, lock, or firmware cause. Add event-triggered telemetry and a production stress that reproduces the fault. Keep intermittent and no-fault-found RMA codes separate from laser wear-out.

## Connector contamination

##### Observed behavior.

Intermittent link failures, burst errors, or elevated BER that clears after reseating or cleaning a connector. Rx power may fluctuate or show sudden drops. Often affects one direction of a duplex link.

##### Likely hypotheses.

A particle of dust on an MT, LC, or MPO ferrule endface scatters and absorbs light, raising insertion loss and back-reflection (lowering ORL). Debris in the core zone can cause large loss even when most of the ferrule looks clean. Elevated ORL feeds back into the laser and raises RIN, causing burst errors even when average power looks acceptable. In high-power CW-WDM and ELSFP systems, trapped particles can burn onto the fiber endface and cause permanent damage.

##### Measurements and root-cause isolation.

1.  **Inspect first.** Use a fiber-endface inspection scope (200--400$\times$) on every mated connector before any other debug. Look for particles in the core zone, scratches, pits, and residue.

2.  **Clean and re-inspect.** Use a dry-click cleaner or lint-free wipe with IPA. Re-inspect. If the endface still fails IEC 61300-3-35 zone criteria, replace the jumper .

3.  **Measure IL and ORL.** After cleaning, measure insertion loss and ORL across the mated pair. Compare to the link-budget allocation (§7.7).

4.  **Correlate with BER.** If BER clears after cleaning, the contamination was the root cause. Log the connector location and date code for trend analysis.

5.  **Repeat offenders.** If the same location re-contaminates quickly, check for airborne particulates (raised-floor debris, construction dust) or improper cap/cover discipline during service events.

##### Corrective action and recurrence control.

Immediate: clean and verify. Preventive: install dust caps on every unused port, enforce "inspect before connect" policy in the service runbook, use sealed cassettes or connectorized trunk cables that minimize open-ferrule exposure. For high-power paths (ELSFP, CW-WDM), any connector that shows burn damage must be replaced, not re-cleaned. Track contamination-related RMAs as a distinct failure code (not "laser failure") so FIT accounting stays honest (§7.12).

## Yield drop

##### Observed behavior.

First-pass yield falls below its stable baseline. The loss may cluster on one ATP row, lane, tester, shift, supplier lot, assembly site, or firmware revision.

##### Likely hypotheses.

Process drift, incoming material variation, fiber-array alignment, die-attach or solder change, tester or fixture drift, stale calibration, a software limit change, or a guardband that no longer matches measurement spread.

##### Measurements and root-cause isolation.

1.  Contain suspect work in process and freeze tester software, limits, fixtures, and calibration records.

2.  Build a Pareto by ATP row, lot, date code, site, tester, and shift. Do not average away a one-lane or one-station signature.

3.  Run a golden unit across stations and the same failed unit on the reference bench. This clears the measurement system before supplier action begins.

4.  Compare upstream wafer, die, assembly, and incoming data at the first point where good and bad populations separate.

5.  Select failure analysis that distinguishes the remaining mechanisms, then verify the correction on a controlled lot and watch the field code.

##### Corrective action and recurrence control.

Restore the changed process or measurement input, add a statistical control at the first observable point, revise ATP only with correlation data, and require a new first-article check before releasing volume (§8.10).

## Aging, thermal response, and margin erosion

Use time scale and recovery to route the incident. A reversible shift during a temperature or neighbor-load sweep is a thermal operating-point problem. A baseline that moves over stress hours or field months is aging. A sudden permanent step after a cycle points toward damage or an assembly defect, not ordinary thermal response.

1.  Return the unit to its starting temperature and operating point. Record whether power, wavelength, bias, TDECQ, and BER recover.

2.  Compare with ship and pre-stress data. Permanent LIV, spectrum, or bias-curve movement supports aging or damage.

3.  Repeat the temperature sweep with source, wavelength-selective element, receiver, and neighbors isolated in turn.

4.  Update the power, noise, timing, and spectral ledgers (§5.19). Several small shifts can explain a BER failure even when each component remains inside its stand-alone limit.

5.  Route reversible thermal loss to cooling, control, calibration, or derating. Route cumulative change to HTOL and life-model review. Route lot-clustered permanent steps to manufacturing failure analysis.

The corrective action must restore margin at combined corners. A room-temperature retest does not close a high-temperature incident, and one clean HTOL readout does not explain a reversible lock failure.

## Temperature sensitivity

##### Observed behavior.

BER, TDECQ, optical power, or lock stability degrades during a case-temperature ramp or under loaded-neighbor conditions. The unit may recover when cooled.

##### Likely hypotheses.

Laser threshold and slope drift, wavelength movement, ring-resonance drift, TEC or heater saturation, EAM or MZM bias error, receiver-noise rise, package stress, or a thermal gradient that affects one lane.

##### Measurements and root-cause isolation.

1.  Record case temperature, external optical power, wavelength, bias, TEC or heater current, lock error, OMA, ER, TDECQ, and pre-FEC BER on one time axis.

2.  Repeat with neighbors off and on. A shared shift points toward thermal or supply coupling; a lone lane points toward its local path.

3.  Hold the source fixed and move the wavelength-selective element, then reverse the test. This splits laser drift from ring or filter drift.

4.  Rerun LIV and receiver sensitivity hot and cold. Separate lost launch power from lost receiver margin.

5.  Inspect package and cooling interfaces if optical and electrical blocks pass alone but fail in the assembled system.

##### Corrective action and recurrence control.

Restore thermal headroom, correct calibration and control limits, reduce coupling, or derate the operating point. Add the loaded-neighbor temperature ramp to the ATP or design-validation plan that missed it.

## Failure-analysis checklist

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Step            Question                                                                       Required record
  --------------- ------------------------------------------------------------------------------ ----------------------------------------------------------------------------
  Preserve        What evidence will a reseat, reboot, clean, or retest destroy?                 CMIS, BER and FEC history, rails, temperature, firmware, fixture, and time

  Scope           One unit, lane, lot, vendor, site, or fleet?                                   Population and correlation plot

  Classify        Sudden or gradual, constant or intermittent, thermal or cumulative?            Timeline and recovery test

  Locate margin   Did power, noise, timing, or spectrum move first?                              Golden comparison and margin ledger

  Falsify         Which measurement best separates the leading hypotheses?                       Expected result for each hypothesis before the test

  Confirm         Does the fault follow the suspected block under a controlled swap or stress?   Repeated failure and passing control

  Correct         Does the fix restore the original failing condition with margin?               Before and after data at loaded corners

  Prevent         Where can production or fleet monitoring catch recurrence earliest?            ATP change, control limit, alarm, owner, and due date
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 10.1.** Failure-analysis checklist. The incident is not closed until the cause is reproduced, corrected, and covered by a recurrence control.

## Interview and design review questions

##### Scoping and evidence.

- BER rose on one rack after a software rollout. What data do you preserve before reseating modules?

- How would you decide whether a symptom belongs to one unit, one lot, one vendor, one site, or the fleet?

##### Root-cause isolation.

- Received power is unchanged but BER worsened. Which measurement do you make next, and which hypotheses does it separate?

- How do you distinguish a BER waterfall shift from a BER floor?

- BER degrades after thermal cycling. How do you separate reversible thermal response, calibration error, assembly damage, and long-term aging?

##### Production and fleet action.

- A golden unit fails only on one production station. What must be cleared before opening supplier failure analysis?

- Which recurrence control belongs in ATP, and which belongs in fleet telemetry?

- When is a no-fault-found return evidence of weak triage rather than a good unit?

**Key idea.** A useful failure analysis starts with a symptom and ends with a new control. Preserve the failing state, split shared from local behavior, clear the measurement system, and choose one measurement that can disprove the leading hypothesis. The corrective action is incomplete until production or fleet data show that the same signature no longer escapes.


<div class="nav-links">
  <a href="ch9-ai-datacenter-networking">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-abbreviations">Next &rarr;</a>
</div>
