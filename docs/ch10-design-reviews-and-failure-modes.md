---
layout: default
title: "Ch 10: Design reviews and failure modes"
---

# Design reviews and failure modes

This appendix collects worked failure-mode examples: the symptoms an engineer sees on the bench or in telemetry, the physics behind the failure, and the systematic debug steps that isolate root cause. Each case follows the same template: observe, hypothesize, measure, confirm. The discipline is bisection, not intuition: change one variable at a time and let the instrument decide.

These are the seven signatures you will encounter most often in a first optical hardware role. Master them and you can triage almost any short-reach link failure in the field or in DVT.

## BER floor

##### Symptom.

Pre-FEC BER improves as you increase transmit power, then stops improving and flattens at a constant floor regardless of how much more power you add.

##### Physics.

A BER floor means a noise source that grows with signal power dominates the link. The classic cause is *relative intensity noise* (RIN): because $\sigma_\mathrm{RIN} \propto I$, once RIN dominates the noise budget, signal and noise grow together and $Q$ saturates at $Q_\mathrm{max} = 1/\sqrt{\mathrm{RIN}_\mathrm{lin} \cdot \mathrm{BW}}$ ([4.3](#sec:rin)). Other causes: multipath interference (MPI) from dirty connectors or high back-reflection, or broadband noise on the laser bias rail that converts to equivalent RIN ([5.7](#sec:laser-drivers)).

##### Debug steps.

1.  Confirm the floor exists: sweep received power (or Tx OMA) and plot BER vs. power. A healthy link has a steep waterfall; a floor appears as a horizontal asymptote.

2.  **Bisect optical vs. electrical RIN.** Measure RIN with a quiet SMU powering the laser (intrinsic RIN). Then repeat with the product bias board connected. If the floor moves, the electrical path is injecting noise ([5.7](#sec:laser-drivers)).

3.  **Sweep ORL.** Add a controlled reflector. If BER floor worsens with lower ORL, the laser is feedback-sensitive. Check isolator, connector, and fiber-attach cleanliness.

4.  **Check for MPI.** Look at the ESA (electrical spectrum analyzer) for discrete spurs at frequencies corresponding to round-trip delays of reflective interfaces. MPI creates bursty errors; the FEC histogram shows clustered symbol errors rather than random ones.

5.  **Confirm RIN spec.** Compare measured $\mathrm{RIN}_x\mathrm{OMA}$ at the stated ORL against the PMD or ATP limit (e.g. $-136$ dB/Hz at 17.1 dB ORL for DR-class links). If the part exceeds spec, reject.

##### Resolution.

If intrinsic RIN is the limiter, the laser is marginal or aged; replace or derate. If electrical RIN, fix the bias supply (better PSRR, star ground, local decoupling). If ORL-driven, clean or replace connectors and verify isolator function. If MPI from multiple reflections, reduce the number of mated interfaces or improve their ORL.

## Low extinction ratio

##### Symptom.

Transmitter OMA looks low on the DCA even though average power is in range. TDECQ may or may not fail depending on how the reference equalizer compensates.

##### Physics.

Extinction ratio $\mathrm{ER} = P_1/P_0$ sets how far apart the one and zero optical levels are for a given average power. Low ER means the zero level is too high (the modulator does not fully extinguish) or the one level is too low. In an EML, ER is set by the EAM reverse bias: insufficient bias leaves residual transmission in the off-state. In a DML, ER depends on modulation depth relative to threshold. The OMA penalty for finite ER is $\mathrm{PP} = (\mathrm{ER}+1)/(\mathrm{ER}-1)$: at 10 dB ER the penalty is $\sim$`<!-- -->`{=html}0.87 dB; at 6 dB ER it rises to $\sim$`<!-- -->`{=html}2.2 dB ([4.4](#sec:sensitivity)).

##### Debug steps.

1.  Measure ER on the DCA (outer OMA / average power, or directly from the histogram levels). Compare against the PMD limit.

2.  **EML:** Sweep EAM bias. ER should peak at the optimal bias point; if the curve has shifted (aged EAM), the operating point needs recalibration. Check EAM bias DAC code vs. datasheet.

3.  **DML:** Check bias current vs. LIV. If bias is close to threshold, modulation depth is limited. Increase bias (but watch thermal rollover and RIN).

4.  **MZM:** Check quadrature bias. If the MZM has drifted off quadrature ($V_\pi/2$ point), extinction degrades. Log the bias-control loop error signal; a saturated loop indicates drift beyond correction range.

5.  **Ring:** Check resonance alignment. If the ring is detuned from the laser wavelength, extinction drops. Monitor the thermal tuner current and wavelength-lock error.

##### Resolution.

Recalibrate the modulator operating point. For EML aging, update the EAM bias setpoint in firmware or flag the module for replacement if the absorption curve has shifted beyond the correctable range. For MZM drift, verify the bias controller and its monitor PD. For rings, retune or check for neighbor thermal crosstalk ([6.5](#sec:thermal-xtalk)).

## Lane imbalance

##### Symptom.

In a multi-lane module (DR4, FR4, DR8), one or more lanes show significantly different OMA, TDECQ, or pre-FEC BER compared with siblings in the same module. The weak lane may be marginal or failing while others are healthy.

##### Physics.

Multi-lane modules share a substrate, laser array (or CW-WDM source), and thermal environment. Lane-to-lane variation comes from: (1) die-level non-uniformity in the laser or modulator array (threshold, slope, $V_\pi$, coupling), (2) packaging variation in fiber-array alignment (one channel of the FAU slightly misaligned), (3) driver or TIA channel mismatch on the electronic IC, or (4) thermal gradient across the die (edge lanes hotter or cooler than center lanes).

##### Debug steps.

1.  Measure all lanes: OMA, ER, TDECQ, RIN, wavelength. Identify the outlier.

2.  **Is it optical or electrical?** Swap the electrical lane assignment (if the host supports lane remapping) or test the suspect optical lane with a known-good driver channel. If the problem follows the optical path, it is laser/modulator/fiber-attach. If it follows the electrical channel, it is driver/TIA.

3.  **Check coupling.** Measure per-lane fiber-coupled power with an integrating sphere or power meter array. A single weak lane with normal LIV suggests FAU misalignment.

4.  **Thermal map.** Use an IR camera or CMIS per-lane monitors (if available) to check for hot spots. Edge lanes near the package wall or near a TEC boundary may run hotter.

5.  **Laser array aging.** If the imbalance grows over time (HTOL or field life), one laser in the array is aging faster (threshold rise, slope drop). Compare LIV curves at $t_0$ and now.

##### Resolution.

FAU misalignment is a manufacturing escape; tighten incoming inspection or first-article coupling specs. Thermal gradient: redesign TEC zoning or derate the hot lane. Laser aging: flag the lot and check burn-in screening effectiveness. Driver mismatch: work with the IC supplier on channel-to-channel gain flatness.

## Wavelength drift

##### Symptom.

In a WDM system, one or more channels walk off the ITU grid or the ring/filter passband. BER degrades as the channel moves off the receiver filter or MUX/DEMUX passband. In ring-modulator CPO, this manifests as sudden unlock of the wavelength control loop.

##### Physics.

Laser wavelength drifts with temperature ($d\lambda/dT \approx 0.1$ nm/$^\circ$C for InP DFB) and bias current ($d\lambda/dI \approx 0.01$ nm/mA). If the TEC or wavelength-locker servo cannot track, the channel walks off its assigned slot. In microring systems, the ring resonance drifts at $\sim$`<!-- -->`{=html}80 pm/$^\circ$C ($\sim$`<!-- -->`{=html}10 GHz/$^\circ$C in Si), and neighbor heaters create thermal crosstalk that pushes adjacent channels ([6.5](#sec:thermal-xtalk)).

##### Debug steps.

1.  Measure wavelength on an OSA or wavemeter. Compare to the target grid.

2.  **Laser-side:** Check TEC current. If saturated (at max or min drive), the thermal load exceeds TEC capacity. Check case temperature and airflow.

3.  **Locker-side:** Read the wavelength-locker error signal. A healthy loop holds near zero; drift means the servo is losing lock. Check locker etalon alignment and PD balance.

4.  **Ring CPO:** Check the ring thermal tuner DAC code. If it has railed (max heater power), the ring cannot reach the target wavelength. Check for neighbor heating (all adjacent lanes at full traffic and max case $T$).

5.  **Aging:** If drift is progressive over weeks/months, suspect laser mode hop or gradual TEC degradation (reduced $\Delta T$ capacity).

##### Resolution.

TEC saturation: reduce case temperature (improve airflow or liquid cooling) or derate the laser operating current. Ring unlock: increase heater headroom in the design, reduce thermal crosstalk with layout changes, or shift the CW-WDM source grid to re-center the ring tuning range. Aging: schedule preventive replacement (ELSFP hot-swap, [5.9](#sec:elsfp)).

## Eye closure (high TDECQ)

##### Symptom.

TDECQ exceeds the PMD limit even though average power and ER look acceptable. The DCA eye appears compressed or distorted after the reference equalizer is applied.

##### Physics.

TDECQ measures how much noise the transmitter can tolerate before BER exceeds the FEC threshold, relative to an ideal transmitter ([7.3](#sec:tdecq)). High TDECQ means the equalized eye is poor. Common causes: (1) insufficient EO bandwidth (modulator or driver roll-off), (2) poor level linearity (RLM $<$ 0.95; driver or modulator compression), (3) pattern-dependent effects (ISI from bandwidth limit, reflections, or impedance mismatch), (4) chromatic dispersion on FR-class fiber eating into the margin.

##### Debug steps.

1.  Inspect the raw (unequalized) eye on the DCA. Is it bandwidth-limited (rounded transitions), compressed (uneven levels), or noisy (RIN/jitter)?

2.  **Bandwidth:** Measure EO $S_{21}$ of the modulator (if accessible) or the combined Tx path. Compare to the Nyquist frequency. If 3-dB BW is below Nyquist, bandwidth is the limiter.

3.  **RLM:** Compute relative level mismatch from the DCA histogram. If $\mathrm{RLM} < 0.95$, the PAM4 levels are unevenly spaced. Check driver linearity (swept DAC code) and modulator transfer function (bias sweep).

4.  **Reflections:** Check $S_{11}$ of the RF path (driver to modulator) and the optical return loss. Reflections cause post-cursor ISI the FFE cannot fully cancel.

5.  **Dispersion:** Measure TDECQ with and without the test fiber (TECQ vs. TDECQ). If TDECQ is significantly worse than TECQ, dispersion is the marginal contributor. Check Tx wavelength and chirp against the fiber length and dispersion coefficient.

##### Resolution.

Bandwidth: upgrade driver or modulator (higher-BW die or peaking network). RLM: tune driver pre-emphasis (DAC levels for each PAM4 symbol). Reflections: fix wirebond, impedance discontinuity, or connector. Dispersion: tighten wavelength tolerance or shorten the fiber (re-route).

## Thermal runaway

##### Symptom.

Module temperature rises continuously until shutdown (CMIS over-temperature alarm) or until the laser degrades catastrophically. May start subtly: BER creeps up as case $T$ rises during traffic ramp or with neighbor-lane loading.

##### Physics.

In a faceplate pluggable, the module dissipates $\sim$`<!-- -->`{=html}8--20 W into the cage heatsink. If airflow is blocked, the cage is overloaded (too many high-power modules), or the TEC inside the module is fighting a losing battle against junction temperature, the thermal loop runs away. In CPO, the optical engine sits on the switch substrate next to a high-power ASIC ($>$`<!-- -->`{=html}500 W); even small failures in the cooling path concentrate heat on the laser or ring heaters.

##### Debug steps.

1.  Read CMIS module temperature and compare to the module's rated case $T$ range. If case $T$ exceeds the max, the system cooling is inadequate.

2.  **Check TEC current.** A TEC at max drive current is saturated; it cannot pump more heat. The junction temperature is higher than the case $T$ suggests.

3.  **Measure LIV at temperature.** If threshold rises and slope drops steeply with $T$, the laser is near thermal rollover ([5.8](#sec:laser-aging)). The operating point may be marginal.

4.  **Neighbor loading.** Bring all lanes and neighbor modules to full traffic simultaneously. If the problem only appears under full-cage load, the thermal design margin is insufficient.

5.  **Airflow audit.** Inspect the faceplate for blocked vents, incorrect fan speed, or missing blanking panels (bypass airflow). For liquid-cooled systems (CPO, XPO), check coolant flow rate and inlet temperature.

##### Resolution.

System-level: improve airflow, lower ambient, or reduce module count per cage. Module-level: derate the laser (lower bias current reduces self-heating) or switch to a lower-power module style (LPO instead of retimed, [9.5.1](#sec:conditioning)). CPO: ensure the cold-plate thermal interface material (TIM) is intact and the liquid loop meets flow-rate spec. Long-term: specify a tighter thermal class in the laser requirements ([5.5](#sec:laser-reqs)).

## Connector contamination

##### Symptom.

Intermittent link failures, burst errors, or elevated BER that clears after reseating or cleaning a connector. Rx power may fluctuate or show sudden drops. Often affects one direction of a duplex link.

##### Physics.

A particle of dust on an MT, LC, or MPO ferrule endface scatters and absorbs light, raising insertion loss and back-reflection (lowering ORL). Particles as small as 1 $\mu$m on a single-mode core (9 $\mu$m diameter) can cause $>$`<!-- -->`{=html}1 dB loss. Elevated ORL feeds back into the laser and raises RIN, causing burst errors even when average power looks acceptable. In high-power CW-WDM and ELSFP systems, trapped particles can burn onto the fiber endface and cause permanent damage.

##### Debug steps.

1.  **Inspect first.** Use a fiber-endface inspection scope (200--400$\times$) on every mated connector before any other debug. Look for particles in the core zone, scratches, pits, and residue.

2.  **Clean and re-inspect.** Use a dry-click cleaner or lint-free wipe with IPA. Re-inspect. If the endface still fails IEC 61300-3-35 zone criteria, replace the jumper.

3.  **Measure IL and ORL.** After cleaning, measure insertion loss and ORL across the mated pair. Compare to the link-budget allocation ([7.6](#sec:link-budget)).

4.  **Correlate with BER.** If BER clears after cleaning, the contamination was the root cause. Log the connector location and date code for trend analysis.

5.  **Repeat offenders.** If the same location re-contaminates quickly, check for airborne particulates (raised-floor debris, construction dust) or improper cap/cover discipline during service events.

##### Resolution.

Immediate: clean and verify. Preventive: install dust caps on every unused port, enforce "inspect before connect" policy in the service runbook, use sealed cassettes or connectorized trunk cables that minimize open-ferrule exposure. For high-power paths (ELSFP, CW-WDM), any connector that shows burn damage must be replaced, not re-cleaned. Track contamination-related RMAs as a distinct failure code (not "laser failure") so FIT accounting stays honest ([7.10](#sec:fleet-triage)).

**Key idea.** Optical link failures are not mysteries; they are physics. A BER floor is RIN or MPI. Low ER is a modulator bias problem. Lane imbalance is coupling or thermal gradient. Wavelength drift is a servo losing lock. Eye closure is bandwidth, linearity, or dispersion. Thermal runaway is watts exceeding the cooling budget. Connector contamination is dust. In every case: observe the symptom, form a hypothesis, measure one variable, confirm. Bisect, do not guess.


<div class="nav-links">
  <a href="ch9-ai-datacenter-networking">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-abbreviations">Next &rarr;</a>
</div>
