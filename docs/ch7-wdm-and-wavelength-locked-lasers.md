---
layout: default
title: "Ch 7: WDM and wavelength-locked lasers"
---

# 7 WDM and wavelength-locked lasers

*Read first:* why WDM; capture versus hold; thermal crosstalk; laser-versus-ring isolation; one-lane versus all-lane signatures.

*Deep dive:* SOA noise figure and gain placement; polarization on the CW path; comb-source device classes.

*Reference:* WDM grid table, MUX defect map, CW-WDM MSA grid details.

Early datacenter optics mostly ran one wavelength per fiber. That worked while port counts were modest. At AI scale, fiber count itself becomes a first-order cost and cable-plant problem, so the industry packed more channels onto each strand. The price of that packing is control: once channel spacing tightens, or once the modulator is a wavelength-selective ring, someone must keep laser and filter locked together. In the architectures covered here, an explicit wavelength-lock requirement strongly suggests a tight wavelength grid, a wavelength-selective modulator or filter, or both. It does not uniquely prove WDM or microring modulation; a single-channel resonant path can also need stabilization. Ring and MZM device physics stay in §3.14.3; per-$\lambda$ laser evidence and aging stay in Chapter 6. This chapter covers grids, lock loops, thermal crosstalk, MUX budget, and CW-WDM architecture.

> **Tradeoff.** Dense WDM vs lock complexity
>
> *Improves:* Fiber count, faceplate density, and bandwidth per strand
>
> *Worsens:* Heaters, TEC, lock firmware, thermal crosstalk, and unlock controls
>
> *When acceptable:* When fiber plant or connector count is the binding constraint
>
> *Experienced decision:* Pay for locking only when multiplexing is worth the control burden.

## Why multiplex wavelengths at all

At $100{,}000$+ accelerator scale, every extra fiber is another connector, another patch, and another failure mode. *Wavelength-division multiplexing* (WDM) puts many independent channels on a single fiber, each on its own wavelength, so bandwidth per fiber rises without adding fiber. Each wavelength can still be an ordinary IM/DD channel. WDM and IM/DD are orthogonal; you run IM/DD *per wavelength*.

Historically the industry climbed a ladder of spacing. Coarse CWDM4 used $\approx$20 nm slots and uncooled lasers. LAN-WDM tightened that for 2 km-class FR4. Dense grids and then CW-WDM O-band combs for CPO pushed spacing into the 100--800 GHz class and made active locking mandatory. Those spacings are standardized grids, not vendor choices: the 20 nm CWDM slots follow the ITU-T G.694.2 wavelength grid (18 channels, 1271--1611 nm), and the 50/100/200 GHz datacom DWDM spacings follow the ITU-T G.694.1 frequency grid anchored at 193.1 THz . CWDM4 uses the four O-band lines of that CWDM grid; the CW-WDM combs in §7.6 define their own O-band grids for dense integration. Table 7.1 is that ladder as you will meet it in short-reach AI optics today.

<table class="book-table"><tr><th>Grid family</th><th>Spacing (class)</th><th>Channels / fiber</th><th>Cooling / lock</th><th>Typical short-reach use</th></tr><tr><td>CWDM4</td><td>20 nm</td><td>4</td><td>Uncooled; loose control</td><td>FR-class pluggables; faceplate WDM</td></tr><tr><td>LAN-WDM</td><td>800 GHz (4--5 nm @ 1310 nm)</td><td>4</td><td>Cooled or tight open-loop</td><td>2 km-class FR4 (edge of book scope)</td></tr><tr><td>Datacom DWDM</td><td>200/100/50 GHz</td><td>many</td><td>Locked to grid</td><td>Discrete DFB/EML DWDM modules</td></tr><tr><td>CW-WDM / CPO O-band</td><td>100--800 GHz class (MSA spans)</td><td>8 / 16 / 32</td><td>Locked; often ring-tuned</td><td>CPO engines, optical I/O chiplets</td></tr></table>
**Table 7.1.** WDM grids for short-reach AI interconnects. CW-WDM MSA normative grids sit in O-band with 9/18/36 nm spans and 8/16/32-line sets (§7.6); spacing is set by the chosen span and channel count, not by Ethernet CWDM4.

**Exit when** fiber count, lock burden, and cooling class pick one grid family for the product. **Decision unlocked:** accept uncooled CWDM4, or fund locked denser grids (LAN-WDM, DWDM, CW-WDM) with the control page they require.

## Why "locked" is the operative word

WDM alone does not force active locking. CWDM4 packs four wavelengths with enough spacing that uncooled lasers can wander and still stay in their slots. Active locking becomes important when the channel spacing and filter guardband are tight, or when the modulator itself is resonant. Those two situations drive most modern CPO and dense optical-I/O control loops. Calculate total drift and manufacturing variation against the usable passband before choosing calibration, temperature control, or closed-loop locking.

### Tight DWDM grids

To pack channels at 50--200 GHz class spacing, each laser must sit on its grid slot or adjacent channels collide. Emphasizing "locking" therefore hints at spacing tighter than CWDM. You do not stress locking for coarse, uncooled CWDM4; you do as soon as the grid looks like LAN-WDM, datacom DWDM, or a CW-WDM comb.

### Microring modulators and WDM locking

Resonant ring and microdisk modulators are commonly used where density and capacitance matter (§3.14.3). Silicon microring resonance often shifts by order-of-magnitude several to roughly ten gigahertz per degree Celsius, depending on geometry, material stack, and operating point; prefer the measured product coefficient when building a lock budget. Even a stable laser is then not enough: the laser and the ring must stay aligned. Either lock the laser to the ring, or thermally tune the ring onto the laser with a feedback loop. That laser--ring co-locking is the central control problem in ring-based WDM links and in co-packaged optics, and it is why neighbor heat and case-temperature ramps belong in validation, not only in the thermal section of a datasheet.

A Mach--Zehnder is comparatively broadband, so it normally does not require the same carrier-to-modulator resonance lock, although its laser must still remain inside the WDM grid and MUX passband (§3.14.3).

## WDM filters, grids, and on-chip multiplexing

WDM is not only lasers and locking (§7.6): the PIC needs wavelength selective routing. The MUX/demux stage is a first-class link-budget line item (Appendix E.5), not a packaging footnote.

##### Signal journey through the MUX.

Follow one wavelength from laser (or comb line) through the modulator, into the MUX, across the plant, and out the demux to the receiver. Stage insertion loss lowers OMA on every lane. Passband ripple and MUX imbalance make the weakest $\lambda$ the budget limit even when the average looks fine. Adjacent-channel crosstalk closes eyes and raises TDECQ before average power looks dead. Grid misalignment clips the filter edge and can unlock a ring before the power meter alarms. Treat those signatures as plant and filter problems until per-$\lambda$ power and isolation prove otherwise.

##### Hardware choices.

AWG / echelle gratings

: multiplex and demultiplex on silicon or glass. Insertion loss is often 2--5 dB per MUX stage; adjacent-channel crosstalk and passband ripple land in OMA and transmitter and dispersion eye closure quaternary (TDECQ).

Ring filter banks

: drop/port routing in microring banks sets how many $\lambda$ share a bus waveguide. Thermal tuning per ring is common (§3.14.3, §7.5).

Hybrid

: some engines use a coarse AWG plus fine ring filters; count every stage in the ledger.

**MZMs trade area for calm wavelength behavior.** When each lane carries its own laser (DR/FR SiPh modules), silicon Mach--Zehnder modulators sidestep ring locking (§3.14.3). Rings remain the default when many $\lambda$ share one PIC and area dominates (§3.14.3, Chapter 8).

##### Where MUX defects land.

Table 7.2 maps common MUX faults to the measurement that catches them.

<table class="book-table"><tr><th>Fault</th><th>Optical symptom</th><th>Hits</th><th>Catch with</th></tr><tr><td>Stage insertion loss</td><td>Lower launch OMA on all</td><td>Link budget OMA</td><td>Power meter / OMA</td></tr><tr><td>Passband ripple / tilt</td><td>Uneven OMA across bank</td><td>Weakest</td><td>Per- OMA map</td></tr><tr><td>Adjacent-channel crosstalk</td><td>Closed eyes, RLM/TDECQ up</td><td>Tx quality / BER</td><td>Isolation sweep + DCA</td></tr><tr><td>MUX imbalance</td><td>One weak, neighbors OK</td><td>Single-lane BER</td><td>Per-lane power + BER</td></tr><tr><td>Grid misalignment</td><td>Filter edge clipping</td><td>TDECQ, unlock risk</td><td>OSA + lock status</td></tr></table>
**Table 7.2.** MUX/demux defects and where they appear in validation. Isolation and imbalance maps need a named evidence owner; they are not automatically every-unit ATP (§7.7, Chapter 8).

Validation adds channel isolation sweeps, grid alignment across temperature, and MUX imbalance (uneven OMA per $\lambda$). Treat the weakest channel as the budget-limiting lane, not the average. Every wavelength-control requirement needs a named evidence source: engineering characterization, qualification, supplier data, process monitoring, ATP, sampled audit, or fleet telemetry (Chapter 8). Dense passband, isolation, and neighbor-hold maps often stay sample or characterization; identity, basic power and wavelength proxies, capture status, actuator codes, alarms, and limited functional checks are more common every-unit controls.

##### How to read the MUX budget.

Table 7.2 is an FA map for the journey above. Approve the MUX when the weakest lane's OMA, isolation, and grid alignment close the budget with a named control plan; otherwise open packaging or PIC FA on the failing row.

## Lock-loop mechanics

Wavelength locking closes the loop between source and filter. Pick a technique based on whether the laser, the ring, or both must be steered (§3.14.3, Chapter 8).

##### Error-signal sources.

Etalon-based wavelength locker

: A fixed reference etalon plus a pair of photodiodes produces an error signal proportional to wavelength offset; feedback trims laser temperature or current onto the grid. Common on discrete DFB/EML modules.

Laser-to-ring thermal feedback

: Monitor the ring's through/drop power (or a dither tone) and heat the ring, or trim laser current, to park the carrier on resonance. Default for dense microring WDM banks in CPO and optical I/O.

Injection / external-cavity locking

: Stabilize a laser's wavelength and linewidth against an external reference cavity; higher performance, more parts. Rare in short-reach volume products.

Athermal design

: Engineer the device so its resonance barely moves with temperature, reducing the control burden. Athermal does not remove MUX grid alignment; it shrinks the loop authority you need.

Digital supervisory loop

: CMIS-exposed monitors and firmware on modern modules; link training at 224G/448G may iterate EQ and wavelength trim together (Appendix H.3).

##### Capture, hold, reacquisition, and headroom.

Decide the control job before you inventory actuators.

Capture

: Initial acquisition of the intended wavelength or resonance from an unlocked state (cold start, reset, hot-swap, or a large temperature change). The controller may coarse-scan heater, TEC, or wavelength before closing the loop.

Hold

: Rejection of expected dynamic disturbances after acquisition: case temperature, source power, neighboring channels, supplies, and traffic.

Reacquisition

: Recovery after a temporary unlock without requiring a full module or system restart.

Lock margin / control headroom

: Remaining wavelength, temperature, or actuator authority before the controlled state can no longer be maintained. A unit may report locked while sitting near a heater, TEC, current-trim, or calibration-map rail.

Capture and hold require separate tests. Successful cold capture is not proof of operational recovery or dynamic hold. Validate applicable states: cold and hot start, reset, source or engine restart, ELS hot-swap, transient unlock, and firmware recovery (§7.7).

<pre class="dectree" aria-label="Cold / unlocked state"><code>Cold / unlocked state
  |
Coarse scan
  |
Correct resonance identified
  |
Loop closes
  |
Captured state
  |
Temperature / neighbor / supply disturbance
  |
Held, reacquired, or unlocked</code></pre>
Loop bandwidth must be fast enough to track case-temperature ramps and adjacent-heater steps, but slow enough not to fight the data path or inject RIN through bias modulation. Illustrative silicon-ring shifts of several to $\sim$10 GHz/°C set the disturbance scale: a 1 °C neighbor step can be tens of GHz of resonance walk, a large fraction of a 100--200 GHz grid slot (§3.14.3). Prefer the measured product coefficient.

##### Open-loop calibration versus closed-loop locking.

*Open-loop calibration* applies a predicted actuator value from temperature, unit calibration, and operating condition. Strengths: lower sensor and firmware complexity, no continuous dither, potentially lower power. Limits: calibration error, process variation, aging, unmodeled neighbor interaction, and weak disturbance rejection. *Closed-loop locking* uses an error signal to update the actuator continuously or periodically. Strengths: rejects drift and exposes residual error and actuator demand. Limits: sensors, dither or monitor overhead, loop stability, firmware, noise injection, and channel interaction. A hybrid design may use open-loop feed-forward for coarse positioning and feedback for fine hold. Treat them as complementary tools, not exclusive product categories.

##### Loop stability (interview-relevant).

Watch sensor noise, loop gain, actuator range and resolution, loop delay, thermal time constants, dither amplitude and frequency, neighbor-loop interaction, startup sequencing, and saturation or anti-windup. Observable signatures include hunting, overshoot, long settling, repeated capture attempts, limit cycling, actuator railing, and correlated neighbor oscillation. A wider capture range or faster loop is not automatically better if it adds noise, power, crosstalk, or instability.

##### Wavelength guardband ledger.

Table 7.3 is a spectral ownership ledger, not a scalar dB sum. Do not treat every impairment as independent, and do not convert every spectral penalty into optical-power loss. Correlated source and filter movement may help or hurt depending on architecture.

<table class="book-table"><tr><th>Ledger term</th><th>What to name for the product</th></tr><tr><td>Assigned carrier center</td><td>Grid slot and absolute reference plane</td></tr><tr><td>Source initial tolerance</td><td>Ship and lot wavelength spread</td></tr><tr><td>Source thermal / aging drift</td><td>Case-T and life walk of the carrier</td></tr><tr><td>Filter or ring initial offset</td><td>Process and calibration park error</td></tr><tr><td>Filter thermal / crosstalk drift</td><td>Self-heat, neighbors, package walk</td></tr><tr><td>Aging / calibration uncertainty</td><td>Table error and monitor aging</td></tr><tr><td>Control residual</td><td>Steady-state lock error after close</td></tr><tr><td>Passband width / isolation</td><td>Usable filter width and adjacent-channel floor</td></tr><tr><td>Remaining spectral guardband</td><td>What is left for hold and life</td></tr></table>
**Table 7.3.** Wavelength and passband guardband ledger. Fill with program numbers; correlated drifts are not five independent additive penalties.

##### Cold-start narrative.

Power the module, identify each assigned $\lambda$, park the coarse TEC or heater until the error signal crosses zero, close the loop at operating optical power (not dark), then prove hold under neighbor heat and case-$T$ ramp before you call lock validated (§7.7). Capture without hold is a demo, not a product. Also prove reacquisition after a controlled unlock when the service model requires it.

##### What you trim.

Three actuators show up repeatedly, and the bring-up order usually starts with the slowest, highest-authority knob. Laser TEC / temperature moves the whole comb or a single DFB on the frequency axis. Laser bias current is the fine wavelength trim (and also changes power), so watch RIN and SMSR when you use it as a locker (§6.8). Ring heaters park each microring onto its assigned $\lambda$ and are the per-channel control in dense banks (§7.5).

##### Source versus ring isolation.

When a loop loses lock, bisect laser versus ring by holding one side fixed and moving the other (Appendix E.1, §9.10, §7.7):

<pre class="dectree" aria-label="Source wavelength actuator"><code>Source wavelength actuator
  |
Relative alignment --&gt; optical performance
  |
Ring / filter actuator</code></pre>
- Source moves while ring or filter is fixed: error that follows the source localizes toward the laser, TEC, or locker.

- Ring or filter moves while source is fixed: error that follows the heater localizes toward the ring, monitor path, calibration, or local thermal coupling.

Localization is not mechanism confirmation (Chapter 9). The one-lane and intermittent signatures this produces are catalogued in §7.9.3.

## Thermal crosstalk and heater budget

Dense ring banks share a substrate. Heating one ring to stay on resonance shifts neighbors. That is , and it is why a single-lane lock test at room temperature is not a product test.

##### Where heat comes from.

Self-heating from the ring's own heater (and absorbed optical power) shifts its resonance, so the lock loop must settle with the lane at operating optical power, not dark. Adjacent heaters on nearest-neighbor and next-nearest rings in a WDM bank are the next disturbance; the worst case is all neighbors at max heater power while you hold lock. Package and ASIC load add a common-mode walk: switch or XPU case-temperature ramps and local hotspots move the whole bank, and a shared TEC or cold plate sets how much of that walk the lock loop must reject (§8.11).

##### Design and validation implications.

Budget heater range with headroom for crosstalk, manufacturing offset, temperature, and aging, not just for the coldest and hottest case alone. Lock range is the total region where acquisition or control is possible; control headroom is the remaining distance from the present operating point to a heater rail, TEC limit, laser-current trim limit, safe temperature, or calibration-map boundary. A locked unit with near-zero headroom is already a reliability risk. Layout (heater placement, thermal isolation trenches, ring pitch) is a reliability and yield problem as much as a control problem. Characterize the thermal coupling matrix; do not validate channels only in isolation. In validation, simultaneous full-traffic on neighbors plus max case $T$ is a *lock* test: unlock, BER walk, or TDECQ rise on one $\lambda$ under neighbor load supports a thermal-coupling or control hypothesis, not a confirmed bad laser die (§8.11, §9.10, Chapter 9). Widening heater or TEC range without checking noise, crosstalk, power, and lifetime is not the first fix.

## External multi-wavelength sources (CW-WDM)

Dense WDM with ring modulators needs a source of many clean, stable wavelengths. The industry answer is a *disaggregated* external laser: a single multi-wavelength continuous-wave (CW) module supplies a comb of wavelengths over fiber to the photonic engine, where microrings imprint data onto each one. The *CW-WDM MSA* standardizes those sources for AI, HPC, and high-density optics . Source-side measurement detail (per-channel power, SMSR, RIN, lock under neighbor heat) is in §6.16; this section is the architecture contract.

##### Architecture contract.

Specify the source at the optical-engine input, not only at the laser output. For every line name power and flatness, absolute wavelength or grid error, spectral purity (SMSR), RIN under the relevant reflection environment, and stability across temperature, ports, aging, and operating states. Add polarization requirements when the engine input is polarization-sensitive, plus startup, hot-swap, alarm, safety, and management behavior (§7.6.3, §7.5, §6.16). Miss any one and a single $\lambda$ looks like a modulator or lock failure when the source is the cause. Total comb power does not replace per-line evidence. A shared source is a common failure domain: telemetry must distinguish one weak line from source-wide degradation. Moving the laser into a replaceable external source can reduce the service blast radius when the source is an important lifetime-limiting element. Whether availability improves depends on source reliability, optical interfaces, connector and polarization controls, detection, redundancy, and replacement time (Chapter 6, Chapter 8).

##### Reference: CW-WDM MSA grid and measurement detail.

*Reference.* Rev 1.0 (June 2021) defines O-band wavelength grids, port configurations, and measurement methods. It does *not* standardize mechanical form factors, management pins, or full link parameters; those stay application-specific or move to form-factor MSAs such as ELSFP .

Core normative content:

- **Grid sets:** 8+1 and 16+1 lines in a 9 nm span; 8+1 / 16+1 / 32+1 in 18 nm and 36 nm spans (shortest line optional in each set).

- **Spacings (class):** for the 18 nm span, channel spacing is 400 / 200 / 100 GHz for 8 / 16 / 32-line sets; the 9 nm and 36 nm spans scale spacing with span width (100--800 GHz class). Normative MSA grids are denser than 5 nm; coarser CWDM-like spacings are informative only.

- **Two physical configs:** *modular* (each fiber carries one $\lambda$) and *integrated* (each fiber carries the full comb).

- **Power classes and AS parameters:** output power classes span low to high launch; SMSR, RIN, and linewidth floors are defined with measurement methods, with many limits marked application-specific (AS) in the normative tables.

Informative appendix examples (not universal product guarantees) often quote $\approx$30 dB SMSR, $\approx-135$ dB/Hz RIN, $\approx$20 MHz linewidth, $\pm$1 dB per-line power variation, and $-20$ dB ORL tolerance for 18 nm-span examples. Treat those as negotiation anchors; write production and qualification controls to your link budget (§6.16, Table 6.4, Chapter 8).

##### Exemplar: SuperNova + TeraPHY.

Ayar Labs' optical-I/O stack is aimed at *scale-up* (XPU-to-XPU) rather than switch fabric :

TeraPHY

: an optical-I/O chiplet co-packaged with the host XPU, carrying the microring modulators and receivers.

SuperNova

: the external CW light source, positioned as the first CW-WDM-MSA-compliant 16-wavelength source, delivering up to 16 wavelengths into each of 16 fibers. That is light for 256 data channels (vendor claim: about 16 Tb/s bidirectional), and roughly $64\times$ the wavelength count of CWDM4 pluggables.

Vendor performance claims versus pluggables plus electrical SerDes (5--10$\times$ bandwidth, 10$\times$ lower latency, 4--8$\times$ better power efficiency) are marketing numbers; use them as orientation, not as ATP limits.[^14]

### Comb sources: one device, many lines

The SuperNova approach builds its comb from an array of discrete lasers, one distributed-feedback (DFB) die per wavelength, combined onto the output fiber. As of the CW-WDM MSA era, discrete DFB arrays are the commonly fielded path for the 8- and 16-line grids the MSA calls for . Past a few dozen lines the die count, the combining loss, and the per-die wavelength trimming start to hurt, which is why a single device that emits a whole comb is attractive. Three device classes compete on line count, per-line power, flatness, spacing stability, RIN, linewidth, pump or electrical power, amplification, control complexity, yield, and failure-domain coupling.

**Quantum-dot mode-locked lasers** (*QD-MLL*s) are a leading research path for a monolithic O-band comb (snapshot: published demos through the mid-2020s; not a deployment claim). Mode locking in a single cavity produces evenly spaced lines at the cavity round-trip rate; quantum-dot gain adds low RIN, a near-zero linewidth-enhancement factor, and strong optical-feedback tolerance, the same properties that make quantum-dot lasers attractive for isolator-free co-packaging . Reported O-band demos carry 14$\times$100 Gb/s PAM4 over 10 km at $\sim$284 fJ/bit, and isolator-free variants target interconnect capacity beyond 3.2 Tb/s. These are research results, not qualified products, so treat the line counts and efficiencies as provisional.

**Kerr microcombs** take the opposite route: pump one high-$Q$ microresonator and let four-wave mixing fill in many evenly spaced lines on a chip . The line count and the spacing uniformity are excellent, and a 2025 demonstration added a monolithic demultiplexer that autonomously locks to and tracks the comb lines. The catch is power. Pump-to-comb conversion efficiency is modest, so each line leaves the chip weak and usually needs a booster or per-line amplifier before it reaches the modulator bank (§7.6.2). Microcombs also need a clean pump laser and careful thermal control to hold the soliton state.

**Gain-switched and quantum-dash combs** sit between the two: a directly driven laser produces a flatter, lower-line-count comb with simple electronics. They have reached multi-terabit aggregate rates in the lab; as of the mid-2020s they have fewer published datacom product paths than QD-MLL demos, which is an ecosystem observation rather than a physics ranking.

For any of them the contract from the MSA does not change: the source must hold per-line power flatness, SMSR, RIN, and grid placement across temperature with every port active (§6.16). A comb that delivers 32 lines but drops 6 dB across the band, or whose edge lines miss the grid, buys nothing over an array of DFBs the PIC already knows how to drive.

### Gain and power distribution across the bank

##### Interview takeaway.

An SOA rescues launch power or line flatness and spends noise figure and polarization-dependent gain. Prefer a higher-power source that already meets the budget; if you add gain, name whether it is a comb booster, per-line trim, or receiver preamp, and keep per-line flatness as a named system evidence row.

Whatever generates the comb, the light still has to survive the trip to the modulators. One source feeds a multiplexer, a splitter tree, and per-line routing before it reaches a ring, and each stage takes its cut. When the source is a chip-scale comb with weak lines (§7.6.1), or when the fan-out is large, a *semiconductor optical amplifier* (SOA) restores the budget.

**Where the gain sits.** A booster SOA placed right after the comb lifts every line before the split, so one device pays for the whole fan-out. A per-line SOA after the demultiplexer instead corrects line-to-line imbalance, at the cost of one amplifier per wavelength. The receiver-side SOA preamplifier (Table 5.6) is a separate job: there the goal is sensitivity, here it is launch power.

**The noise-figure cost.** An SOA adds amplified spontaneous emission (*ASE*), and its noise figure sets how much. The quantum floor is 3 dB; commercial O-band SOAs land near 6--7 dB with roughly 15 dB of gain and about 1.5 dB polarization-dependent gain . Every dB of noise figure eats into the signal-to-noise ratio the receiver eventually sees, so an SOA that rescues launch power can cost link margin if it runs deep into saturation or amplifies an already-noisy comb. Quantum-dot SOAs grown on silicon are attractive for the same reason QD lasers are: low noise, wide O-band gain, and CMOS-compatible integration.

**Holding the bank flat.** Gain is not uniform across the comb span, and SOAs compress near saturation, so the line that starts strongest is not the line that ends strongest. Per-line power flatness is a system spec (§7.6), held with some mix of source-side pre-emphasis, gain-tilt control, and per-line trimming. The alternative to any distribution-side gain is a higher-power source, which is why array-of-DFB designs that already meet the launch budget often skip the SOA entirely.

### Polarization on the CW distribution path

##### Interview takeaway.

The photodiode's basic square-law response is not the only system consideration. Couplers, modulators, filters, amplifiers, and package interfaces on the CW feed may be polarization-sensitive. Hold that path on PM fiber to the preferred axis when the architecture needs it, or shorten the external path with co-packaging; neither choice is universal for every external CW design.

IM/DD is forgiving about polarization at the receiver: the photodiode is a square-law detector, so the received state of polarization does not by itself corrupt recovered bits (§3.4). A standard single-mode drop to the receiver therefore needs no polarization control. External-source and CW-WDM architectures move the sensitive part upstream, onto the path between the laser and the modulator.

**Where it matters.** Three elements on the CW feed care about the launched state. A *TFLN* Mach--Zehnder drives the electro-optic effect through TE-polarized light on one crystal axis (§3.14.3); light on the wrong axis sees little modulation. Silicon grating couplers are polarization-selective by construction, so coupling loss swings with the input state, a *polarization-dependent loss* (PDL) that comes straight off the launch budget. And a booster or per-line SOA adds polarization-dependent gain (§7.6.2), so a drifting state becomes a drifting per-line power. None of these sit after the photodiode, so none show up in a receiver-side budget: they act on light that has not yet been modulated.

**How it is held.** When the CW input is polarization-sensitive, keep the feed on *polarization-maintaining* (PM) fiber and PM connectors from the external laser (Chapter 6) to the modulator input, launched on the coupler's preferred axis. PM fiber reduces uncertainty but adds axis-alignment and connector requirements. On-chip the light is often single-polarization once it is in a TE waveguide, so the discipline is about the fiber run and the mate at the package. A co-packaged source shortens the external polarization-sensitive path but does not automatically eliminate all on-chip polarization considerations.

## Lock validation playbook

Instruments and BER methods live in Chapter 8. What is special to WDM is the order: you cannot trust a BER number on a ring bank until the comb is identified, the resonances are parked, and the lock loops hold under neighbor heat. The sequence below is the usual bring-up; skip a step and you will debug the wrong domain.

##### Bring-up order.

1.  **Grid ID:** confirm each CW line (or DFB) is on the assigned channel with an OSA / wavemeter (§6.16).

2.  **Coarse align:** park rings near resonance with open-loop heater sweeps; check through/drop monitors.

3.  **Close lock:** enable the feedback loop; verify capture on every $\lambda$ at operating optical power.

4.  **Stress neighbors / temperature:** max case $T$, neighbor heaters and traffic on (§7.5, §8.11). Confirm hold, not just capture.

5.  **Close the link:** BER / TDECQ / sensitivity on the weakest lane first (Appendix E.3, Appendix E.5).

**Exit when** every assigned $\lambda$ is grid-identified, captures at operating power, holds under neighbor heat and case $T$, and the weakest lane closes BER. **Decision unlocked:** proceed to loaded characterization, or stop and bisect laser versus ring before trusting any BER number.

Host-visible CMIS may report lock error, heater codes, or wavelength monitors; use those for fleet triage. Grid ID and absolute alignment still need an OSA or wavemeter when engineering access exists. Do not treat a "locked" flag alone as proof the comb is on the assigned grid. No single register or optical measurement closes the wavelength-control argument (Table 7.4).

<table class="book-table"><tr><th>Observable</th><th>What it can show</th><th>What it does not prove</th></tr><tr><td>Locked flag</td><td>Controller believes an internal criterion is satisfied</td><td>Correct absolute grid assignment or adequate optical margin</td></tr><tr><td>Lock error</td><td>Residual sensor error</td><td>Sensor accuracy or actuator headroom</td></tr><tr><td>Heater / TEC code</td><td>Actuator demand</td><td>Actual resonance or wavelength without calibration</td></tr><tr><td>Through / drop monitor</td><td>Relative alignment signal</td><td>Full transmitter or receiver performance</td></tr><tr><td>OSA / wavemeter</td><td>Absolute optical spectrum or wavelength</td><td>Closed-loop stability during fast events</td></tr><tr><td>BER / FEC</td><td>End-to-end consequence</td><td>Source, ring, MUX, or receiver ownership alone</td></tr></table>
**Table 7.4.** Wavelength-control evidence: what each observable can show versus what it does not establish.

##### Bisect laser versus ring.

If one $\lambda$ unlocks or walks, change one actuator at a time (§7.4):

- change laser TEC / current with ring heater fixed: if the error follows the laser, localize toward the source or its locker;

- change ring heater with laser fixed: if the error follows the heater, localize toward the ring, monitor PD, calibration, or thermal crosstalk;

- if both look fine but OMA is low, inspect MUX imbalance and connector/ORL (Table 7.2, Appendix E.2).

##### Fleet telltales.

Slow BER creep with rising bias on one line raises a laser-aging hypothesis (Appendix F.11, Chapter 9). Sudden unlock under neighbor load with healthy LIV supports a thermal-coupling or lock-firmware hypothesis. One dark lane with neighbors up localizes investigation toward COD, FAU, or a single ring/heater path; classify with §9.10 before you open an 8D on the wrong supplier.

> **What this usually means.** All lanes unlock after a temperature step
>
> *Usually:* shared TEC, supply, firmware, or thermal control
>
> *Not:* independent failures of every lane's laser in the same second

> **Engineering heuristic.** One-lane unlock raises local hypotheses; all-lane unlock raises shared hypotheses first. Lane correlation prioritizes ownership; it does not confirm the mechanism (Chapter 9).

Local one-lane hypotheses include that lane's source line, ring or filter, heater, monitor, MUX channel, calibration entry, attach, or electrical lane. Shared all-lane hypotheses include common source or TEC, supply, controller, firmware, package thermal event, shared MUX, polarization path, or telemetry.

## What wavelength locking implies about an architecture

Because locking is only worth its complexity under specific conditions, its presence narrows the design space considerably.

<pre class="dectree" aria-label="Locking present"><code>Locking present
  |
Tight grid and/or selective filter/modulator
  |
Thermal / heater / TEC control
  |
Evidence: capture, hold, headroom, crosstalk
  |
Fleet: unlock alarms, wavelength telemetry</code></pre>

<table class="book-table"><tr><th>Implication</th><th>Strength</th></tr><tr><td>Tight grid, selective filter/modulator, or both</td><td>Strongly suggested: lock is worth its complexity under those conditions; not unique proof of WDM.</td></tr><tr><td>Dense (D)WDM rather than coarse CWDM</td><td>Commonly indicated when spacing and guardband leave little open-loop room.</td></tr><tr><td>Microring-based silicon photonics with external multi-wavelength (CW-WDM) sources</td><td>Narrows the space; common in modern AI interconnects under fiber-count pressure, but not uniquely determined.</td></tr><tr><td>Discrete DFB/EML DWDM (no rings)</td><td>Also possible; locking alone does not prove rings or silicon photonics.</td></tr></table>
**Table 7.5.** What a wavelength-locking requirement can imply. Locking narrows architecture possibilities; it does not uniquely identify WDM, dense WDM, microrings, or silicon photonics.

The useful conclusion is that **wavelength control is central**; whether the implementation is ring-based silicon photonics with external multi-wavelength sources or discrete DFB/EML DWDM depends on the specific system.

## Engineering lens

### How it works

WDM buys fiber count back by stacking wavelengths, and the price is control: once the grid is tight or the modulator is resonant, laser and filter must stay locked. The chapter's lock loops, thermal budgets, and source specs all exist to hold that lock across temperature and neighbor load.

### How it is measured

Start with an OSA or wavemeter to identify every source line, then sweep each ring or filter while recording through-port, drop-port, heater current, monitor-PD signal, and lock error. Measure insertion loss and adjacent-channel leakage per lane. Close the loop and repeat BER, OMA, and TDECQ under case-temperature ramps, neighbor heater activity, source-power spread, and restart. Capture range and hold range are different acceptance tests; §7.7 gives the order, and the source measurements follow the CW-WDM MSA methods .

### How it fails

One degraded lane points toward its laser line, ring, filter channel, heater, monitor, or local fiber attach. All lanes moving together points toward the shared CW source, thermal controller, supply, polarization path, or common MUX. Capture failures occur during startup or a large temperature step. Hold failures occur after lock, often under neighbor heat, power droop, or control-loop interaction. Treat those as separate signatures.

##### One lane fails.

Possible causes, roughly in order of how often each shows up in the field:

- **Wavelength locker failure:** the etalon-based error signal drifts or the locker photodiodes degrade, so the loop steers the laser to the wrong setpoint even though the laser itself is healthy (§7.4).

- **Ring drift:** the microring's own resonance walks off the assigned $\lambda$ under local heating or process aging, independent of the laser (§3.14.3).

- **AWG issues:** an arrayed-waveguide grating channel shifts passband center or picks up excess adjacent-channel crosstalk, clipping one lane at the filter edge while neighboring channels stay clean (§7.3, Table 7.2). Distinguish from a laser or ring fault by sweeping the source across the passband and watching for a grid-alignment signature rather than a lock-error signature.

- **Thermal crosstalk:** an adjacent heater's disturbance exceeds this lane's hold-range budget while its own actuators read nominal (§7.5).

##### Intermittent failure.

Failures that appear and clear on their own point to control-loop dynamics rather than a broken part:

- **Lock acquisition issues:** the loop fails to capture reliably from a cold or power-cycled state, so failures correlate with restarts or ELS hot-swaps rather than with steady-state operation (§7.7).

- **Heater control instability:** the thermal feedback loop oscillates or overshoots, often triggered by a control-loop bandwidth that fights the data path or a gain that was tuned for a different neighbor-load condition. Shows up as a heater current that hunts rather than settles.

- **Temperature excursions:** a transient case-temperature ramp (fan failure, load step, HVAC event) pushes the loop past its hold range momentarily; the lane recovers once the transient passes, which is the distinguishing signature versus a genuine hardware fault.

\> \*\*Failure mode: Wavelength drift\*\* \> \> \*\*Symptoms.\*\* BER rises with temperature, one WDM lane moves, and lock error or heater demand grows. \> \> \*\*Likely causes.\*\* Laser wavelength drift, ring resonance drift, thermal coupling, a saturated TEC or heater, or a weak monitor signal. \> \> \*\*Measurements.\*\* OSA or wavemeter, heater and TEC current, lock error, neighbor activity, and per-lane BER. \> \> \*\*Mitigations.\*\* Restore thermal headroom, widen capture only after noise is checked, improve calibration, and reduce shared thermal or supply coupling.

### How it is debugged

First decide whether the fault affects one lane or all lanes. Apply the power-versus-quality fork, then ask which ledger moved: often spectral or control (§5.8, §6.19). Freeze heater and laser actuators long enough to measure the open-loop spectrum. Move the source while holding the ring fixed, then move the ring while holding the source fixed. If neither follows the failing BER, inspect MUX loss, polarization, connector ORL, and the electrical lane. For intermittent unlock, align lock-error, heater, temperature, supply, and neighbor-traffic traces on one time axis. A control loop cannot be debugged from final register values alone.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* One lane failed only after adjacent lanes began traffic. \> \> \*\*Investigation.\*\* The source line stayed on grid, while the suspect ring heater railed and lock error grew with neighbor temperature. \> \> \*\*Finding.\*\* The optical source and receiver passed; the resonance was being pushed out of hold range. \> \> \*\*Root cause.\*\* Thermal coupling from the adjacent heater exceeded the control-loop budget. \> \> \*\*Resolution.\*\* The heater map and feed-forward terms were corrected, and neighbor-load hold behavior became a required recurrence control. Depending on production access and test time, that control may be an engineering qualification corner, a sampled production audit, an ATP proxy based on heater headroom, or an SPC monitor tied to the affected process (Chapter 8).

## Interview takeaway

**Key idea.** Wavelength locking is a control-system problem wrapped around an optical link. Define the grid, identify everything that can move, prove capture and hold separately, stress shared thermal paths, and decide from the weakest channel with measured control headroom. A locked flag is not absolute grid or margin proof. One-lane versus all-lane behavior routes ownership hypotheses; it does not confirm mechanism (Table 7.4, Chapter 9).

Junior mistake: blame every unlock on the laser, or debug lock from final register values without neighbor-load and time-aligned traces (§5.8, Chapter 8, Chapter 9).

### Interview Q&A: WDM and Wavelength Control

Practice speaking these answers aloud. Prefer first-person reasoning over definitions. Detail lives earlier in this chapter (§7.1, §7.4, §7.5, §7.7). Score your answer using the chapter-end spoken-answer rubric (Appendix A.12.1).

##### Question 1. Why use WDM, and when is its control burden justified?

*Tests:* system motivation, fiber-count tradeoff, and architectural judgment.

*Spoken answer.* "WDM increases bandwidth per fiber by placing several independent channels on different wavelengths. I would use it when fiber count, connector density, cable routing, or faceplate bandwidth is a binding system constraint. The cost is added MUX loss, channel isolation requirements, wavelength control, thermal coupling, calibration, firmware, and more complex production and fleet observability. I would compare the saved fiber and connector burden against that complete control cost. WDM is not automatically the best answer merely because more wavelengths fit on one strand."

*Pressure follow-up.* "Would you use the densest grid available?"\
*Answer pivot.* "No. I would use the loosest grid that closes the fiber-density requirement. Tighter spacing buys channel count but consumes wavelength, filter, thermal, and control margin."

*Trap:* preferring WDM whenever the system needs more bandwidth.

##### Question 2. When does a WDM architecture require active wavelength locking?

*Tests:* coarse versus tight grids and resonant versus non-resonant modulation.

*Spoken answer.* "WDM alone does not automatically require active locking. A coarse grid may tolerate the source drift and filter passband across temperature using an uncooled or calibrated open-loop design. Active locking becomes important when the channel spacing and filter guardband are tight, or when the modulator itself is resonant, as with a microring. In that case both the source wavelength and the ring or filter resonance must remain aligned. I would calculate the total drift and manufacturing variation against the usable passband before deciding whether calibration, temperature control, or closed-loop locking is necessary."

*Pressure follow-up.* "Does a wavelength-lock requirement prove the design uses microrings?"\
*Answer pivot.* "No. It may be a ring-based silicon-photonics design, but a discrete DFB or EML on a tight DWDM grid can also require wavelength stabilization. Locking narrows the architecture possibilities; it does not uniquely identify one."

*Trap:* claiming active locking means the transmitter must use a silicon microring.

##### Question 3. Why is wavelength alignment more demanding for a microring than for a Mach--Zehnder modulator?

*Tests:* resonant and broadband modulator behavior.

*Spoken answer.* "A microring is resonant, so its transmission and modulation efficiency depend strongly on the offset between the optical carrier and the ring resonance. Both can move with temperature, process, age, and neighboring heater activity. A Mach--Zehnder is comparatively broadband, so it normally does not require the same carrier-to-modulator resonance lock, although its laser must still remain inside the WDM grid and MUX passband. Rings gain density and low capacitance, but they transfer burden into wavelength sensing, heaters, calibration, and feedback control" (§3.14.3).

*Pressure follow-up.* "Does that mean an MZM requires no wavelength control?"\
*Answer pivot.* "No. It removes the narrow modulator-resonance constraint, but the source must still satisfy the channel grid, MUX passband, receiver, and adjacent-channel isolation requirements."

*Trap:* calling an MZM wavelength-independent so the laser may drift anywhere inside the optical band.

##### Question 4. Explain capture range and hold range.

*Tests:* startup acquisition versus disturbance rejection.

*Spoken answer.* "Capture is the ability to acquire the correct operating point from an unlocked state, such as cold start, reset, hot-swap, or a large temperature change. The controller may perform a coarse TEC, wavelength, or heater scan before closing the loop. Hold is the ability to remain locked after acquisition while case temperature, source power, neighboring channels, supply conditions, and traffic change. They require separate tests. A system may capture successfully in a quiet room-temperature condition but lose lock under a fast thermal ramp or neighbor-heater step" (§7.4).

*Pressure follow-up.* "Which range should be larger?"\
*Answer pivot.* "The required ranges come from different disturbances. Capture must cover startup variation and uncertainty; hold must cover expected dynamic movement after lock. I would derive both from the product's actual thermal, process, aging, and restart conditions rather than assume one universal relationship."

*Trap:* treating cold-start capture as proof that wavelength control is validated.

##### Question 5. How would you validate capture and hold?

*Tests:* test ordering, operating corners, and acceptance criteria.

*Spoken answer.* "I would first identify every source line and filter or ring channel using an OSA, wavemeter, or trusted internal monitor. Then I would test capture from cold, hot, reset, power-cycle, and relevant source or engine restart states. After lock, I would test hold during case-temperature ramps, neighboring-channel activation, maximum traffic, source-power variation, supply movement, and actuator disturbances. I would record lock time, acquisition success rate, residual error, heater or TEC demand, overshoot, control headroom, unlock events, and the resulting OMA, transmitter quality, and BER. Acceptance must include repeatability and remaining actuator margin, not only a locked bit" (§7.7, Table 7.4).

*Pressure follow-up.* "The module reports locked on every restart. Is that enough?"\
*Answer pivot.* "No. I still need to verify absolute channel assignment, optical performance, lock time, and headroom. A controller can settle at the wrong resonance or report an internal success condition while the carrier is misaligned to the intended grid."

*Trap:* power-cycling the module several times and verifying only the lock-status flag.

##### Question 6. How do you separate laser drift from ring or filter drift?

*Tests:* controlled actuator isolation and ownership localization.

*Spoken answer.* "I would measure the open-loop source spectrum and the filter or ring response at the failing condition. Then I would hold one side fixed and move the other. With the ring heater fixed, I vary laser temperature or current and observe whether the error follows the source. With the source fixed, I sweep the ring or filter and observe its passband and monitor response. I correlate both with lock error, BER, OMA, temperature, and actuator state. If neither movement explains the symptom, I investigate the MUX, coupling, polarization, reflections, monitor path, or electrical lane."

*Pressure follow-up.* "The failure follows the heater setting. Is the ring confirmed defective?"\
*Answer pivot.* "It localizes the issue toward the ring-control path, but the mechanism could still be the ring, heater resistance, monitor photodiode, calibration map, local thermal coupling, or firmware."

*Trap:* blaming the ring whenever the laser sits on its nominal grid wavelength.

##### Question 7. How do thermal crosstalk and actuator headroom affect a dense ring bank?

*Tests:* neighbor interactions, common-mode movement, and control margin.

*Spoken answer.* "In a dense bank, each ring's heater affects its own resonance and also shifts neighboring resonances through the shared substrate. Package and ASIC temperature add common-mode movement. I would characterize the thermal coupling matrix rather than test channels only in isolation. The worst condition may involve maximum case temperature, active neighboring channels, high heater demand, and full optical power. I track heater or TEC range, residual lock error, settling behavior, and BER while neighbors change state. The controller needs enough headroom for manufacturing offset, temperature, aging, and crosstalk without operating continuously at an actuator rail" (§7.5).

*Pressure follow-up.* "Why not simply increase the maximum heater power?"\
*Answer pivot.* "More authority can increase power, local temperature, crosstalk, drift, and reliability stress. I would first determine whether the limitation is range, thermal design, calibration, loop behavior, or an incorrectly centered nominal operating point."

*Trap:* validating neighboring channels independently because each ring has its own heater.

##### Question 8. What WDM MUX or DEMUX impairments matter, and how do they appear?

*Tests:* insertion loss, ripple, isolation, grid alignment, and weakest-channel reasoning.

*Spoken answer.* "I would evaluate insertion loss, passband center and width, ripple or tilt, channel-to-channel imbalance, adjacent-channel isolation, polarization sensitivity where relevant, and movement over temperature. Common insertion loss lowers every channel's power or OMA. Ripple and imbalance create a weakest-channel problem. Crosstalk may degrade level linearity, transmitter-quality metrics, or BER without a dramatic average-power loss. Grid misalignment clips the channel near a filter edge and can look like a source or lock problem. I would measure per-channel distributions and use the weakest channel, not the bank average, for the system decision" (Table 7.2).

*Pressure follow-up.* "Average power across the bank is within specification. Can the MUX be approved?"\
*Answer pivot.* "Not from the average. One edge channel may have poor passband alignment, isolation, or OMA while the average remains healthy. The release criterion must close every supported channel or define an explicit yield and mapping strategy."

*Trap:* approving a MUX when its average insertion loss meets the link budget.

##### Question 9. One WDM channel unlocks while all neighboring channels remain healthy. How do you debug it?

*Tests:* lane-local hypotheses and controlled isolation.

*Spoken answer.* "One-channel behavior raises local hypotheses: its source line, ring or filter, heater, monitor path, calibration entry, MUX channel, local attach, or thermal hotspot. I compare wavelength, per-line power, SMSR or spectral quality where available, heater demand, lock error, OMA, BER, and neighbor activity. I then move one actuator or path at a time and, where the architecture permits, exchange source lines, ring assignments, monitor channels, or electrical lanes. The result can localize the failing block, but I do not jump directly from one-lane behavior to a defective laser."

*Pressure follow-up.* "The channel recovers after recalibration. Is the issue closed?"\
*Answer pivot.* "Only if recalibration restores the correct operating point with stable margin and the original drift is understood. Repeated recalibration may be hiding thermal, aging, sensor, or control-headroom loss."

*Trap:* concluding that one isolated channel failure means that wavelength's laser die is bad.

##### Question 10. All channels unlock after a temperature or power event. What do you check first?

*Tests:* shared-resource reasoning and causal ordering.

*Spoken answer.* "Simultaneous movement across the bank makes independent lane failures unlikely. I would check shared resources first: source TEC or comb control, common supply rails, clock or controller reset, firmware state, package or cold-plate temperature, shared MUX alignment, polarization path, and monitoring infrastructure. I align wavelength, lock error, heater demand, TEC current, rails, temperature, resets, and traffic on one time axis to identify which signal moved first. After restoring service, I reproduce the event with one controlled disturbance at a time."

*Pressure follow-up.* "All heater codes move at the same time. Does that prove a thermal event?"\
*Answer pivot.* "No. A firmware restart, common sensor error, supply disturbance, or source shift could command every heater to move. I need the event ordering and independent temperature or spectral evidence."

*Trap:* assuming that if all channels unlock, the shared laser source has failed.

##### Question 11. What is the system contract for an external multi-wavelength CW source?

*Tests:* per-line source requirements and shared failure domains.

*Spoken answer.* "I would specify the source at the optical-engine input rather than only at the laser output. For every line I need power and flatness, absolute wavelength or grid error, spectral purity such as SMSR, RIN under the relevant reflection environment, and stability across temperature, ports, aging, and operating states. I also need polarization requirements when the engine input is polarization-sensitive, plus startup, hot-swap, alarm, safety, and management behavior. A shared source creates a common failure domain, so telemetry and redundancy must distinguish one weak line from source-wide degradation" (§7.6).

*Pressure follow-up.* "A comb has many lines and sufficient total output power. What could still fail?"\
*Answer pivot.* "The edge lines may be weak, noisy, off grid, or poorly aligned to the engine. Total power can hide per-line flatness, spectral, and wavelength defects."

*Trap:* treating total launch power and channel count as the main requirements for a multi-wavelength source.

##### Question 12. Give me a 60-second WDM and wavelength-control validation plan.

*Tests:* complete Staff-level architecture and validation answer.

*Spoken answer.* "I begin with the fiber-count requirement, wavelength grid, channel spacing, and the source, modulator, MUX, and receiver passbands. I identify every element that can drift and define the sensors, actuators, capture range, hold range, and required control headroom. During bring-up I verify each source line and filter channel, perform coarse alignment, close the loops, and confirm that the correct grid assignment was acquired. I then stress cold and hot starts, temperature ramps, neighboring channels, full traffic, source-power spread, supplies, and restart behavior. I evaluate per-channel power, isolation, lock error, actuator demand, OMA, transmitter quality, and BER using the weakest channel. Finally, I define production controls and fleet telemetry for unlock, drift, and exhausted headroom."

*Pressure follow-up.* "What evidence would make you reject the ring-based path?"\
*Answer pivot.* "I would reconsider it if required capture or hold range cannot be achieved with acceptable power and reliability, thermal crosstalk cannot be controlled, weakest-channel yield is poor, or the production and fleet observability cannot bound the lock risk."

*Trap:* verifying the wavelength grid, enabling the lock loop, testing BER over temperature, and releasing if all channels pass.

Score each response using the shared chapter-interview rubric in Appendix A.12.1. Repeat any answer that does not define the wavelength requirement, distinguish capture from hold, identify the moving source or filter element, and name the evidence that supports the release or containment decision.


<div class="nav-links">
  <a href="ch6-choosing-light-sources-and-modulation">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch8-productization-from-requirements-to-controlled-ramp">Next &rarr;</a>
</div>
