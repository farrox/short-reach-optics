---
layout: default
title: "Ch 6: WDM and wavelength-locked lasers"
---

# WDM and wavelength-locked lasers

Early datacenter optics mostly ran one wavelength per fiber. That worked while port counts were modest. At AI scale, fiber count itself becomes a first-order cost and cable-plant problem, so the industry packed more channels onto each strand. The price of that packing is control: once channel spacing tightens, or once the modulator is a wavelength-selective ring, someone must keep laser and filter locked together. Few phrases carry as much architectural information as "wavelength-locked laser," because locking only appears under those interconnect choices. Ring and MZM device physics stay in § `sec:siring,sec:simzm`; per-$\lambda$ laser ATP and aging stay in § `ch:lasers`. This chapter covers grids, lock loops, thermal crosstalk, MUX budget, and CW-WDM architecture.

## Why multiplex wavelengths at all

At $100{,}000$+ accelerator scale, every extra fiber is another connector, another patch, and another failure mode. *Wavelength-division multiplexing* (WDM) puts many independent channels on a single fiber, each on its own wavelength, so bandwidth per fiber rises without adding fiber. Each wavelength can still be an ordinary IM/DD channel. WDM and IM/DD are orthogonal; you simply run IM/DD *per wavelength*.

Historically the industry climbed a ladder of spacing. Coarse CWDM4 used $\approx$`<!-- -->`{=html}20 nm slots and uncooled lasers. LAN-WDM tightened that for 2 km-class FR4. Dense grids and then CW-WDM O-band combs for CPO pushed spacing into the 100--800 GHz class and made active locking mandatory. Those spacings are standardized grids, not vendor choices: the 20 nm CWDM slots follow the ITU-T G.694.2 wavelength grid (18 channels, 1271--1611 nm), and the 50/100/200 GHz datacom DWDM spacings follow the ITU-T G.694.1 frequency grid anchored at 193.1 THz . CWDM4 uses the four O-band lines of that CWDM grid; the CW-WDM combs in § `sec:cwwdm` define their own O-band grids for dense integration. § `tab:wdm-grids` is that ladder as you will meet it in short-reach AI optics today.

[]

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Grid family           Spacing (class)                                                                   Channels / fiber   Cooling / lock              Typical short-reach use
  --------------------- --------------------------------------------------------------------------------- ------------------ --------------------------- -------------------------------------
  CWDM4                 $\approx$`<!-- -->`{=html}20 nm                                                   4                  Uncooled; loose control     FR-class pluggables; faceplate WDM

  LAN-WDM               $\approx$`<!-- -->`{=html}800 GHz ($\approx$`<!-- -->`{=html}4--5 nm @ 1310 nm)   4                  Cooled or tight open-loop   2 km-class FR4 (edge of book scope)

  Datacom DWDM          200/100/50 GHz                                                                    many               Locked to grid              Discrete DFB/EML DWDM modules

  CW-WDM / CPO O-band   100--800 GHz class (MSA spans)                                                    8 / 16 / 32        Locked; often ring-tuned    CPO engines, optical I/O chiplets
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** WDM grids for short-reach AI interconnects. CW-WDM MSA normative grids sit in O-band with 9/18/36 nm spans and 8/16/32-line sets (§ `sec:cwwdm`); spacing is set by the chosen span and channel count, not by Ethernet CWDM4.

## Why "locked" is the operative word

WDM alone does not force active locking. CWDM4 packs four wavelengths with enough spacing that uncooled lasers can wander and still stay in their slots. Locking becomes the operative word only when either the channel spacing is tight or the modulator itself is wavelength-selective. Those two situations drive nearly every modern CPO and dense optical-I/O control loop.

### Tight DWDM grids

To pack channels at 50--200 GHz class spacing, each laser must sit on its grid slot or adjacent channels collide. Emphasizing "locking" therefore hints at spacing tighter than CWDM. You do not stress locking for coarse, uncooled CWDM4; you do as soon as the grid looks like LAN-WDM, datacom DWDM, or a CW-WDM comb.

### Microring modulators and WDM locking

Resonant ring and microdisk modulators are the dense-WDM workhorse (§ `sec:siring`). Their resonance drifts by roughly $10$ GHz/°C in silicon, so even a stable laser is not enough: the laser and the ring must be wavelength-locked. Either lock the laser to the ring, or thermally tune the ring onto the laser with a feedback loop. That laser--ring co-locking is the central control problem in ring-based WDM links and in co-packaged optics, and it is why neighbor heat and case-temperature ramps belong in validation, not only in the thermal section of a datasheet.

## WDM filters, grids, and on-chip multiplexing

WDM is not only lasers and locking (§ `sec:cwwdm`): the PIC needs wavelength selective routing. The MUX/demux stage is a first-class link-budget line item (§ `sec:link-budget`), not a packaging footnote.

##### Hardware choices.

AWG / echelle gratings

: multiplex and demultiplex on silicon or glass. Insertion loss is often 2--5 dB per MUX stage; adjacent-channel crosstalk and passband ripple land in OMA and transmitter and dispersion eye closure quaternary (TDECQ).

Ring filter banks

: drop/port routing in microring banks sets how many $\lambda$ share a bus waveguide. Thermal tuning per ring is common (§ `sec:siring,sec:thermal-xtalk`).

Hybrid

: some engines use a coarse AWG plus fine ring filters; count every stage in the ledger.

**MZMs trade area for calm wavelength behavior.** When each lane carries its own laser (DR/FR SiPh modules), silicon Mach--Zehnder modulators sidestep ring locking (§ `sec:simzm`). Rings remain the default when many $\lambda$ share one PIC and area dominates (§ `sec:siring,ch:networking`).

##### Where MUX defects land.

§ `tab:mux-budget` maps common MUX faults to the measurement that catches them.

[]

  -------------------------------------------------------------------------------------------------------------
  Fault                        Optical symptom                     Hits                 Catch with
  ---------------------------- ----------------------------------- -------------------- -----------------------
  Stage insertion loss         Lower launch OMA on all $\lambda$   Link budget OMA      Power meter / OMA

  Passband ripple / tilt       Uneven OMA across bank              Weakest $\lambda$    Per-$\lambda$ OMA map

  Adjacent-channel crosstalk   Closed eyes, RLM/TDECQ up           Tx quality / BER     Isolation sweep + DCA

  MUX imbalance                One $\lambda$ weak, neighbors OK    Single-lane BER      Per-lane power + BER

  Grid misalignment            Filter edge clipping                TDECQ, unlock risk   OSA + lock status
  -------------------------------------------------------------------------------------------------------------

**Table .** MUX/demux defects and where they appear in validation. Isolation and imbalance tests belong in ATP for any dense WDM engine (§ `sec:lock-validation,sec:cwwdm-laser`).

Validation adds channel isolation sweeps, grid alignment across temperature, and MUX imbalance (uneven OMA per $\lambda$). Treat the weakest channel as the budget-limiting lane, not the average.

## Lock-loop mechanics

Wavelength locking closes the loop between source and filter. Pick a technique based on whether the laser, the ring, or both must be steered (§ `sec:siring,ch:validation`).

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

: CMIS-exposed monitors and firmware on modern modules; link training at 224G/448G may iterate EQ and wavelength trim together (§ `sec:pluggables`).

##### What you trim.

Three actuators show up repeatedly, and the bring-up order usually starts with the slowest, highest-authority knob. Laser TEC / temperature moves the whole comb or a single DFB on the frequency axis. Laser bias current is the fine wavelength trim (and also changes power), so watch RIN and SMSR when you use it as a locker (§ `sec:laser-drivers`). Ring heaters park each microring onto its assigned $\lambda$ and are the per-channel control in dense banks (§ `sec:thermal-xtalk`).

##### Capture versus hold.

*Capture* is acquiring lock from a cold or unlocked state: coarse scan of heater or TEC until the monitor error signal crosses zero, then close the loop. *Hold* is rejecting thermal drift and neighbor crosstalk once locked. Loop bandwidth must be fast enough to track case-temperature ramps and adjacent-heater steps, but slow enough not to fight the data path or inject RIN through bias modulation. Silicon rings at $\sim$`<!-- -->`{=html}10 GHz/°C set the disturbance scale: a 1 °C neighbor step is tens of GHz of resonance walk, which is a large fraction of a 100--200 GHz grid slot (§ `sec:siring`).

##### Failure signatures.

Fleet failures often look like slow wavelength walk: drop monitor power falls, TDECQ rises on one $\lambda$, or one lane in a WDM bank drops out while neighbors stay up. Bisect laser versus ring by toggling TEC setpoint and ring heater independently (§ `sec:instruments,sec:fleet-triage,sec:lock-validation`).

## Thermal crosstalk and heater budget

Dense ring banks share a substrate. Heating one ring to stay on resonance shifts neighbors. That is , and it is why a single-lane lock test at room temperature is not a product test.

##### Where heat comes from.

Self-heating from the ring's own heater (and absorbed optical power) shifts its resonance, so the lock loop must settle with the lane at operating optical power, not dark. Adjacent heaters on nearest-neighbor and next-nearest rings in a WDM bank are the next disturbance; the worst case is all neighbors at max heater power while you hold lock. Package and ASIC load add a common-mode walk: switch or XPU case-temperature ramps and local hotspots move the whole bank, and a shared TEC or cold plate sets how much of that walk the lock loop must reject (§ `sec:prod-corners`).

##### Design and validation implications.

Budget heater range with headroom for crosstalk, not just for the coldest and hottest case alone. Layout (heater placement, thermal isolation trenches, ring pitch) is a reliability and yield problem as much as a control problem. In validation, simultaneous full-traffic on neighbors plus max case $T$ is a *lock* test: unlock, BER walk, or TDECQ rise on one $\lambda$ under neighbor load points at thermal design, not at a bad laser die (§ `sec:prod-corners,sec:fleet-triage`).

## External multi-wavelength sources (CW-WDM)

Dense WDM with ring modulators needs a source of many clean, stable wavelengths. The industry answer is a *disaggregated* external laser: a single multi-wavelength continuous-wave (CW) module supplies a comb of wavelengths over fiber to the photonic engine, where microrings imprint data onto each one. The *CW-WDM MSA* standardizes those sources for AI, HPC, and high-density optics . Source-side measurement detail (per-channel power, SMSR, RIN, lock under neighbor heat) is in § `sec:cwwdm-laser`; this section is the architecture contract.

##### What the MSA specifies (and what it does not).

Rev 1.0 (June 2021) defines O-band wavelength grids, port configurations, and measurement methods. It does *not* standardize mechanical form factors, management pins, or full link parameters; those stay application-specific or move to form-factor MSAs such as ELSFP .

Core normative content:

- **Grid sets:** 8+1 and 16+1 lines in a 9 nm span; 8+1 / 16+1 / 32+1 in 18 nm and 36 nm spans (shortest line optional in each set).

- **Spacings (class):** for the 18 nm span, channel spacing is 400 / 200 / 100 GHz for 8 / 16 / 32-line sets; the 9 nm and 36 nm spans scale spacing with span width (100--800 GHz class). Normative MSA grids are denser than 5 nm; coarser CWDM-like spacings are informative only.

- **Two physical configs:** *modular* (each fiber carries one $\lambda$) and *integrated* (each fiber carries the full comb).

- **Power classes and AS parameters:** output power classes span low to high launch; SMSR, RIN, and linewidth floors are defined with measurement methods, with many limits marked application-specific (AS) in the normative tables.

Informative appendix examples (not universal product guarantees) often quote $\approx$`<!-- -->`{=html}30 dB SMSR, $\approx-135$ dB/Hz RIN, $\approx$`<!-- -->`{=html}20 MHz linewidth, $\pm$`<!-- -->`{=html}1 dB per-line power variation, and $-20$ dB ORL tolerance for 18 nm-span examples. Treat those as negotiation anchors; write the ATP to your link budget (§ `sec:cwwdm-laser,tab:laser-prd`).

##### Why disaggregate the laser.

External CW-WDM / ELSFP sources are field-replaceable. Lasers dominate wear-out FIT (§ `ch:lasers,ch:reliability`); keeping them off the ASIC package turns a COD or facet failure into a hot-swap, not a board pull. The photonic engine still needs per-$\lambda$ lock to rings or filters.

##### Exemplar: SuperNova + TeraPHY.

Ayar Labs' optical-I/O stack is aimed at *scale-up* (XPU-to-XPU) rather than switch fabric :

TeraPHY

: an optical-I/O chiplet co-packaged with the host XPU, carrying the microring modulators and receivers.

SuperNova

: the external CW light source, positioned as the first CW-WDM-MSA-compliant 16-wavelength source, delivering up to 16 wavelengths into each of 16 fibers. That is light for 256 data channels (vendor claim: about 16 Tb/s bidirectional), and roughly $64\times$ the wavelength count of CWDM4 pluggables.

Vendor performance claims versus pluggables plus electrical SerDes (5--10$\times$ bandwidth, 10$\times$ lower latency, 4--8$\times$ better power efficiency) are marketing numbers; use them as orientation, not as ATP limits.[^16]

##### System requirements the source must meet.

For the PIC to close every lane, the comb must deliver, across temperature and with all ports active, a small set of properties at once: per-line power flatness (else MUX + modulator bank makes uneven OMA), grid placement and SMSR per line, RIN under the specified ORL, and absolute wavelength stable enough that ring heaters stay in range (§ `sec:thermal-xtalk,sec:cwwdm-laser`). Miss any one and a single $\lambda$ will look like a modulator or lock-loop failure when the source is the real cause.

### Comb sources: one device, many lines

The SuperNova approach builds its comb from an array of discrete lasers, one distributed-feedback (DFB) die per wavelength, combined onto the output fiber. That is the shipping answer, and it scales cleanly to the 8 and 16 lines the MSA grids call for. Past a few dozen lines the die count, the combining loss, and the per-die wavelength trimming start to hurt, which is why a single device that emits a whole comb is attractive. Three device classes compete.

**Quantum-dot mode-locked lasers** (*QD-MLL*s) are the front-runner for a monolithic O-band comb. Mode locking in a single cavity produces evenly spaced lines at the cavity round-trip rate; quantum-dot gain adds low RIN, a near-zero linewidth-enhancement factor, and strong optical-feedback tolerance, the same properties that make quantum-dot lasers attractive for isolator-free co-packaging . Reported O-band demos carry 14$\times$`<!-- -->`{=html}100 Gb/s PAM4 over 10 km at $\sim$`<!-- -->`{=html}284 fJ/bit, and isolator-free variants target interconnect capacity beyond 3.2 Tb/s. These are research results, not qualified products, so treat the line counts and efficiencies as provisional.

**Kerr microcombs** take the opposite route: pump one high-$Q$ microresonator and let four-wave mixing fill in many evenly spaced lines on a chip . The line count and the spacing uniformity are excellent, and a 2025 demonstration added a monolithic demultiplexer that autonomously locks to and tracks the comb lines. The catch is power. Pump-to-comb conversion efficiency is modest, so each line leaves the chip weak and usually needs a booster or per-line amplifier before it reaches the modulator bank (§ `sec:soa-distribution`). Microcombs also need a clean pump laser and careful thermal control to hold the soliton state.

**Gain-switched and quantum-dash combs** sit between the two: a directly driven laser produces a flatter, lower-line-count comb with simple electronics. They have reached multi-terabit aggregate rates in the lab but see less datacom traction than QD-MLLs.

For any of them the contract from the MSA does not change: the source must hold per-line power flatness, SMSR, RIN, and grid placement across temperature with every port active (§ `sec:cwwdm-laser`). A comb that delivers 32 lines but drops 6 dB across the band, or whose edge lines miss the grid, buys nothing over an array of DFBs the PIC already knows how to drive.

### Gain and power distribution across the bank

Whatever generates the comb, the light still has to survive the trip to the modulators. One source feeds a multiplexer, a splitter tree, and per-line routing before it reaches a ring, and each stage takes its cut. When the source is a chip-scale comb with weak lines (§ `sec:comb-sources`), or when the fan-out is large, a *semiconductor optical amplifier* (SOA) restores the budget.

**Where the gain sits.** A booster SOA placed right after the comb lifts every line before the split, so one device pays for the whole fan-out. A per-line SOA after the demultiplexer instead corrects line-to-line imbalance, at the cost of one amplifier per wavelength. The receiver-side SOA preamplifier (§ `tab:rxtech`) is a separate job: there the goal is sensitivity, here it is launch power.

**The noise-figure cost.** An SOA adds amplified spontaneous emission (*ASE*), and its noise figure sets how much. The quantum floor is 3 dB; commercial O-band SOAs land near 6--7 dB with roughly 15 dB of gain and about 1.5 dB polarization-dependent gain . Every dB of noise figure eats into the signal-to-noise ratio the receiver eventually sees, so an SOA that rescues launch power can cost link margin if it runs deep into saturation or amplifies an already-noisy comb. Quantum-dot SOAs grown on silicon are attractive for the same reason QD lasers are: low noise, wide O-band gain, and CMOS-compatible integration.

**Holding the bank flat.** Gain is not uniform across the comb span, and SOAs compress near saturation, so the line that starts strongest is not the line that ends strongest. Per-line power flatness is a system spec (§ `sec:cwwdm`), held with some mix of source-side pre-emphasis, gain-tilt control, and per-line trimming. The alternative to any distribution-side gain is a higher-power source, which is why array-of-DFB designs that already meet the launch budget often skip the SOA entirely.

### Polarization on the CW distribution path

IM/DD is forgiving about polarization where it counts most. The photodiode is a square-law detector, so the received state of polarization does not affect the recovered bits (§ `sec:coherent-boundary`). A standard single-mode drop to the receiver therefore needs no polarization control. The external-source and CW-WDM architectures move the sensitive part upstream, onto the path between the laser and the modulator.

**Where it matters.** Three elements on the CW feed care about the launched state. A *TFLN* Mach--Zehnder drives the electro-optic effect through TE-polarized light on one crystal axis (§ `sec:tfln-mzm`); light on the wrong axis sees little modulation. Silicon grating couplers are polarization-selective by construction, so coupling loss swings with the input state, a *polarization-dependent loss* (PDL) that comes straight off the launch budget. And a booster or per-line SOA adds polarization-dependent gain (§ `sec:soa-distribution`), so a drifting state becomes a drifting per-line power. None of these sit after the photodiode, so none show up in a receiver-side budget: they act on light that has not yet been modulated.

**How it is held.** Keep the CW feed on *polarization-maintaining* (PM) fiber and PM connectors from the external laser (§ `ch:lasers`) to the modulator input, launched on the coupler's preferred axis. On-chip the light is already single-polarization once it is in a TE waveguide, so the discipline is really about the fiber run and the mate at the package. A co-packaged design with the laser on the same substrate shortens that run to millimeters and sidesteps most of the problem; an external-laser design pays for a PM path and its alignment tolerance instead.

## Lock validation playbook

Instruments and BER methods live in § `ch:validation`. What is special to WDM is the order: you cannot trust a BER number on a ring bank until the comb is identified, the resonances are parked, and the lock loops hold under neighbor heat. The sequence below is the usual bring-up; skip a step and you will debug the wrong domain.

##### Bring-up order.

1.  **Grid ID:** confirm each CW line (or DFB) is on the assigned channel with an OSA / wavemeter (§ `sec:cwwdm-laser`).

2.  **Coarse align:** park rings near resonance with open-loop heater sweeps; check through/drop monitors.

3.  **Close lock:** enable the feedback loop; verify capture on every $\lambda$ at operating optical power.

4.  **Stress neighbors / temperature:** max case $T$, neighbor heaters and traffic on (§ `sec:thermal-xtalk,sec:prod-corners`). Confirm hold, not just capture.

5.  **Close the link:** BER / TDECQ / sensitivity on the weakest lane first (§ `sec:tdecq,sec:link-budget`).

##### Bisect laser versus ring.

If one $\lambda$ unlocks or walks, change one actuator at a time:

- change laser TEC / current with ring heater fixed: if the error follows the laser, the source or its locker is wrong;

- change ring heater with laser fixed: if the error follows the heater, the ring, monitor PD, or thermal crosstalk is wrong;

- if both look fine but OMA is low, inspect MUX imbalance and connector/ORL (§ `tab:mux-budget,sec:optical-channel`).

##### Fleet telltales.

Slow BER creep with rising bias on one line is often laser wear-out (§ `sec:wearout-modes`). Sudden unlock under neighbor load with healthy LIV is thermal crosstalk or lock firmware. One dark lane with neighbors up is COD, FAU, or a single ring/heater fail; classify with § `sec:fleet-triage` before you open an 8D on the wrong supplier.

## What wavelength locking implies about an architecture

Because locking is only worth its complexity under specific conditions, its presence narrows the design space considerably.

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Implication                                                                                                                   Strength
  ----------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------
  Some form of WDM is in use                                                                                                    Near-certain: locking only matters with WDM.

  Dense (D)WDM rather than coarse CWDM                                                                                          Likely: locking implies tight spacing.

  Microring-based silicon photonics with external multi-wavelength (CW-WDM) sources, often trending toward co-packaged optics   Common in modern AI interconnects (e.g. Broadcom and NVIDIA Quantum-X programs), driven by fiber-count pressure at scale.

  Discrete DFB/EML DWDM (no rings)                                                                                              Also possible; locking alone does not prove rings.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** What a wavelength-locking requirement implies.

The solid conclusion is that **WDM is present and wavelength control is central**; whether the implementation is ring-based silicon photonics with external multi-wavelength sources or discrete DFB/EML DWDM depends on the specific system.

## Engineering lens

### How it works

WDM buys fiber count back by stacking wavelengths, and the price is control: once the grid is tight or the modulator is resonant, laser and filter must stay locked. The chapter's lock loops, thermal budgets, and source specs all exist to hold that lock across temperature and neighbor load.

### How it is measured

Start with an OSA or wavemeter to identify every source line, then sweep each ring or filter while recording through-port, drop-port, heater current, monitor-PD signal, and lock error. Measure insertion loss and adjacent-channel leakage per lane. Close the loop and repeat BER, OMA, and TDECQ under case-temperature ramps, neighbor heater activity, source-power spread, and restart. Capture range and hold range are different acceptance tests; § `sec:lock-validation` gives the order, and the source measurements follow the CW-WDM MSA methods .

### How it fails

One degraded lane points toward its laser line, ring, filter channel, heater, monitor, or local fiber attach. All lanes moving together points toward the shared CW source, thermal controller, supply, polarization path, or common MUX. Capture failures occur during startup or a large temperature step. Hold failures occur after lock, often under neighbor heat, power droop, or control-loop interaction. Treat those as separate signatures.

##### One lane fails.

Possible causes, roughly in order of how often each shows up in the field:

- **Wavelength locker failure:** the etalon-based error signal drifts or the locker photodiodes degrade, so the loop steers the laser to the wrong setpoint even though the laser itself is healthy (§ `sec:locking-techniques`).

- **Ring drift:** the microring's own resonance walks off the assigned $\lambda$ under local heating or process aging, independent of the laser (§ `sec:siring`).

- **AWG issues:** an arrayed-waveguide grating channel shifts passband center or picks up excess adjacent-channel crosstalk, clipping one lane at the filter edge while neighboring channels stay clean (§ `sec:wdm-hardware,tab:mux-budget`). Distinguish from a laser or ring fault by sweeping the source across the passband and watching for a grid-alignment signature rather than a lock-error signature.

- **Thermal crosstalk:** an adjacent heater's disturbance exceeds this lane's hold-range budget while its own actuators read nominal (§ `sec:thermal-xtalk`).

##### Intermittent failure.

Failures that appear and clear on their own point to control-loop dynamics rather than a broken part:

- **Lock acquisition issues:** the loop fails to capture reliably from a cold or power-cycled state, so failures correlate with restarts or ELS hot-swaps rather than with steady-state operation (§ `sec:lock-validation`).

- **Heater control instability:** the thermal feedback loop oscillates or overshoots, often triggered by a control-loop bandwidth that fights the data path or a gain that was tuned for a different neighbor-load condition. Shows up as a heater current that hunts rather than settles.

- **Temperature excursions:** a transient case-temperature ramp (fan failure, load step, HVAC event) pushes the loop past its hold range momentarily; the lane recovers once the transient passes, which is the distinguishing signature versus a genuine hardware fault.

\> \*\*Failure mode: Wavelength drift\*\* \> \> \*\*Symptoms.\*\* BER rises with temperature, one WDM lane moves, and lock error or heater demand grows. \> \> \*\*Likely causes.\*\* Laser wavelength drift, ring resonance drift, thermal coupling, a saturated TEC or heater, or a weak monitor signal. \> \> \*\*Measurements.\*\* OSA or wavemeter, heater and TEC current, lock error, neighbor activity, and per-lane BER. \> \> \*\*Mitigations.\*\* Restore thermal headroom, widen capture only after noise is checked, improve calibration, and reduce shared thermal or supply coupling.

### How it is debugged

First decide whether the fault affects one lane or all lanes. Freeze heater and laser actuators long enough to measure the open-loop spectrum. Move the source while holding the ring fixed, then move the ring while holding the source fixed. If neither follows the failing BER, inspect MUX loss, polarization, connector ORL, and the electrical lane. For intermittent unlock, align lock-error, heater, temperature, supply, and neighbor-traffic traces on one time axis. A control loop cannot be debugged from final register values alone.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* One lane failed only after adjacent lanes began traffic. \> \> \*\*Investigation.\*\* The source line stayed on grid, while the suspect ring heater railed and lock error grew with neighbor temperature. \> \> \*\*Finding.\*\* The optical source and receiver passed; the resonance was being pushed out of hold range. \> \> \*\*Root cause.\*\* Thermal coupling from the adjacent heater exceeded the control-loop budget. \> \> \*\*Resolution.\*\* The heater map and feed-forward terms were corrected, and neighbor-load hold testing became an ATP corner.

## Interview and design review questions

##### Concept.

- Why is WDM preferable to adding fibers at scale?

- Why does a microring modulator require wavelength locking while a Mach--Zehnder does not?

- What happens if laser wavelength drifts by 2 nm in a 200 GHz-spaced WDM system?

##### Design.

- What are capture and hold ranges across process, voltage, temperature, and source-power spread?

- Which resource is shared across lanes, and what does its failure signature look like?

- How much heater and TEC headroom remains at the worst thermal corner?

- Can telemetry distinguish laser drift, ring drift, MUX loss, and monitor-PD error without opening the package?

##### Debug.

- One WDM lane fails while neighbors are healthy. How do you determine whether the cause is the laser, ring, filter, heater, or connector?

- All lanes unlock after a temperature step. What shared resource do you check first?

- Which calibration or startup error can escape production and fail only after a field restart?

##### Manufacturing and operations.

- What production test proves lock hold under worst-case neighbor heat?

- How do you qualify a new CW-WDM source lot against the ATP?

- What field telemetry distinguishes a source failure from a ring-bank failure?

**Key idea.** Wavelength locking is a control-system problem wrapped around an optical link. Measure the grid, capture, hold, shared thermal paths, and per-lane margin. Then use one-lane versus all-lane behavior to split the source, ring bank, MUX, thermal controller, and common supplies.


<div class="nav-links">
  <a href="ch5-lasers-for-optical-interconnects">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch7-optical-validation">Next &rarr;</a>
</div>
