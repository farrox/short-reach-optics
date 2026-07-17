---
layout: default
title: "Ch 7: Optical validation"
---

# Optical validation

A datasheet that closes on a quiet bench is not a product. *Validation* is the work of proving a link meets spec and will keep meeting it across the temperatures, hosts, connectors, and aging the fleet will actually see. That discipline is the second theme of this book. This chapter walks the ladder from a single device to a deployed fleet, the metrics measured at each stage, module and system bring-up under production-like corners, and the data-driven debug mindset the work demands.

## The validation ladder

Optical programs fail in the same places again and again: a part that looks good in characterization but cannot bring up on a production host, or a module that passes ATP and then unlocks under neighbor heat. The practical way to avoid those gaps is a ladder of five stages, each answering a sharper question than the last. Skipping one creates escapes that surface later at higher cost.

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Stage                  Question                               Activity and instruments
  --- ---------------------- -------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------
  1   Bring-up               Does it link?                          Power-on, CMIS state machine, first light, CDR lock, pre-FEC BER on golden host (§7.9)

  2   Characterization       How much margin, across corners?       Sweep $T$, $V$, ORL, aging; TDECQ, sensitivity, link budget; component LIV/RIN/SMSR (§7.4, §7.7)

  3   Margin and interop     Does margin survive the fleet?         Production-representative corners: chassis thermal, host rails, neighbor load, dirty fiber, ELS hot-swap, target host/NIC/ASIC (§7.9)

  4   Stress qualification   Does it survive its projected life?    HTOL, temperature cycle, humidity, ESD, mating cycles per GR-468, GR-1221, JESD47 (§8.2, §8.3)

  5   Production readiness   Can the supplier build it at volume?   Multi-lot yield, SPC stability, ATP coverage, ATE correlation, first-article, DVT/PVT gates (§8.9, §8.10)
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.1.** The validation ladder: five stages from bench to fleet. A sixth concern, scaled deployment and fleet triage, runs continuously once material ships (§7.12). Field telemetry, RMA tracking, and FIT burn-down feed back into stages 3--5.

For every metric at every stage, name the instrument, the reference plane (§3.9), the pass criterion, and the failure signature. A number without a plane and a method is not a measurement.

## The core IM/DD measurements

Once the ladder is clear, the measurement list is organized around isolation: transmitter, channel, and receiver. That split is older than PAM4. Long before TDECQ, field engineers learned that a dark link can be a dead laser, a dirty connector, or a dead TIA, and that guessing which one burns hours. Bisecting those three domains is still how you keep debug from turning into simultaneous retunes of everything.

### Transmitter

Start with the light leaving the faceplate or the CPO fiber array. For PAM4, the headline metric is *TDECQ* (transmitter and dispersion eye closure quaternary): a reference equalizer is applied to the captured eye and the residual penalty is reported in dB (§7.4). Alongside it you read *OMA* (outer), extinction ratio, and *RLM* (level linearity), plus wavelength, spectral width, and RIN with a bias-driver versus feedback bisect (§5.6, §5.7, §4.3.1).

What else you add depends on the transmitter style. Laser-bearing modules need LIV, threshold, slope, SMSR, and chirp checks for DMLs (§5.6, §5.3). External MZMs (TFLN or silicon) need EO $S_{21}$, $V_\pi$, quadrature bias versus temperature, and driver-path eye symmetry at baud (§3.14.3, §7.4). Microring banks need resonance alignment, thermal tuning, neighbor crosstalk, and peaking-network EO $S_{21}$ (§3.14.3, Chapter 6). The point of the list is not completeness for its own sake: it is knowing which instrument answers which hypothesis when the eye closes.

### Channel

If the transmitter looks clean into a golden receiver and the link still fails, the channel is next. Insertion loss from fiber, connectors, MUX/de-MUX (§6.3), and on-chip coupling (§3.14.3) is the first ledger line; plan about 1--3 dB per fiber interface. Chromatic dispersion (§3.11) matters more on FR-class SMF sweeps than on short DR links. Optical return loss (ORL) is the quiet killer: reflections back into the laser raise RIN and seed burst errors, which is why many DR/FR modules still carry isolators while some CPO engines rely on design margin and monitor photodiodes instead (§4.3.1, Chapter 5). Fiber attach (MPO/MTP, FAU, grating couplers) shows up as both yield and reliability (§8.8).

### Receiver

Receiver work asks whether the front-end can still decide bits at the OMA that survives the channel. Measure sensitivity (minimum OMA for the target BER) and stressed-receiver sensitivity with a calibrated stressor for margin (§7.5), plus overload before the TIA saturates. Underneath those system numbers sit the photodiode/TIA pair: responsivity, bandwidth, and input-referred noise (§4.5, Chapter 4).

### Link level

Only after Tx, channel, and Rx each look sane do you trust a full-link verdict: pre-FEC BER against the KP4 threshold (§3.12), post-FEC BER, FEC symbol-error histograms, and a signed link-budget ledger from transmitter OMA to receiver sensitivity with penalties and remaining margin. That ledger is the document you argue from in DVT; the BER alone is not.

## Measurement mapping

The metrics above are scattered across Tx, channel, Rx, and link level because that is how you debug them. Table 7.2 collects the same metrics into one reference: what is measured, the instrument, why it matters, and the failure signature that points back to it. Use the chapter subsections for the debug logic; use this table to look up an instrument fast.

[]

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Metric                        Instrument                          Why it matters                                                                          Failure signature
  ----------------------------- ----------------------------------- --------------------------------------------------------------------------------------- --------------------------------------------------------------------------------
  OMA / TDECQ                   DCA + reference equalizer           Scores transmitter quality against an ideal source; governs PAM4 acceptance (§7.4)      TDECQ rises with no average-power change; points to bandwidth, RLM, or bias

  Extinction ratio / RLM        DCA level histograms                Sets OMA at fixed average power (§4.4); poor RLM inflates TDECQ                         Compressed inner eyes with passing average power

  Wavelength / SMSR             OSA or wavemeter                    Confirms grid placement and single-mode purity (§5.6)                                   Side modes rise with $T$ or age; line walks off grid

  RIN                           PD + electrical spectrum analyzer   Sets the BER floor $Q_\mathrm{max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ (§4.3)        BER improves with power then flattens (a floor)

  Insertion loss / ORL          Power meter + ORL meter             First ledger line; reflections raise RIN and seed bursts (§7.2.2)                       Burst errors with stable average power; RIN rises with ORL

  Receiver sensitivity          BERT + calibrated attenuator        Minimum OMA at target BER, the budget's bottom line (§4.4, §7.5)                        Waterfall shifts uniformly right without flooring

  Pre-FEC BER / FEC histogram   BERT + FEC counters                 The single number every other metric feeds; histogram shape reveals mechanism (§3.12)   Clustered errors point to bursts; sparse errors point to Gaussian noise margin

  CMIS state / DDM              Host or CMIS tool                   Confirms management layer before blaming optics (§7.8)                                  Module never reaches ModuleReady; DDM disagrees with bench truth
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.2.** Measurement mapping: metric, instrument, rationale, and failure signature in one reference. Cross-references point to the full treatment of each metric elsewhere in this chapter.

## Transmitter and dispersion eye closure quaternary (TDECQ)

*TDECQ* (transmitter and dispersion eye closure quaternary) deserves a closer look because it is the metric that governs PAM4 transmitter acceptance. It answers a specific question: *how much worse is this transmitter than an ideal one, after a realistic receiver has done what it can to clean up the signal?*

### How it is measured

1.  **Capture.** The optical waveform is acquired on a sampling oscilloscope (a DCA) through a standardized reference receiver (a fourth-order Bessel--Thomson filter at roughly half the baud rate) so every lab measures the same bandwidth.

2.  **Equalize.** A defined *reference equalizer*, a *feed-forward equalizer* (FFE) with a small, bounded number of taps (commonly up to five), is applied. This models the modest equalization a real receiver would perform, so the transmitter is not penalized for *ISI* the system can remove anyway.

3.  **Histogram.** Two narrow vertical histogram windows are placed inside the symbol (near 0.45 and 0.55 of the unit interval). The noise distribution is evaluated at the three PAM4 decision thresholds.

4.  **Compute.** The algorithm finds the RMS Gaussian noise $\sigma$ that, added to the equalized signal, would just reach a target symbol error ratio of $4.8\times10^{-4}$ (the SER consistent with the KP4 pre-FEC budget). TDECQ is the ratio, in dB, of the noise an *ideal* transmitter could tolerate to the noise *this* transmitter can tolerate: $$\mathrm{TDECQ} = 10\log_{10}\!\left(\frac{\sigma_{\text{ideal}}}
            {\sigma_{\text{measured}}}\right).$$

A worse transmitter tolerates less added noise before failing, so $\sigma_{\text{measured}}$ shrinks and TDECQ rises. Lower is better; typical 100--200G/lane specifications cap it in the low single-digit dB range.

### Related quantities and failure signatures

SECQ

: the stressed-eye counterpart used on the receiver side, adding a calibrated stressor to test margin rather than transmitter quality alone. See §7.5.

RLM (relative level mismatch)

: measures how evenly the four PAM4 levels are spaced; poor RLM (uneven levels) inflates TDECQ.

Because TDECQ folds several impairments into one number, the way it fails is diagnostic: uneven levels point to modulator or driver linearity (RLM); residual eye closure the equalizer cannot fix points to excess ISI or limited bandwidth; a noise-limited result points to low OMA, RIN, or reflections. For external MZMs (TFLN or silicon), also check EO $S_{21}$ bandwidth, $V_\pi$ and bias quadrature drift with temperature, and RF return loss on the driver-to-modulator path (§3.14.3). This is why *LPO*, which removes the module's own DSP, raises the stakes on transmitter quality: there is less downstream equalization to hide behind, so TDECQ-class metrics become even more central.

## SECQ and stressed-receiver testing

*SECQ* (stressed eye closure quaternary) mirrors TDECQ on the *receiver*: instead of scoring transmitter quality with a reference equalizer, the test applies a calibrated optical stressor (attenuation, ISI template, optional RIN) and asks how much margin remains before the receiver hits the target pre-FEC BER.

Stressed-receiver sensitivity and overload tests (§4.4) use the same philosophy: bracket the operating OMA range with impairments the link will see in the field. For LPO, where the module DSP is gone, SECQ-style margin on the host-side receiver (§3.6, §9.5.1) is as important as TDECQ on the transmitter.

## Instruments

A failing PAM4 link rarely announces which block is wrong. The bench is how you force the answer: each instrument isolates one failure mode, and the loopback topology tells you which side of the optical connector owns it.

DCA

: (digital communication analyzer): sampling scope for PAM4 eyes, TDECQ, OMA, RLM (§7.4). Needs a reference receiver filter matched to the PHY under test.

BERT

: bit-error ratio at pre- and post-FEC; FEC symbol histograms (§3.12).

OSA

: wavelength, SMSR, side modes, RIN estimates (Chapter 5, §4.3.1).

VOA / stressor assembly

: calibrated attenuation and optional ISI for SECQ and sensitivity sweeps.

Power meter

: average power; pair with DCA for OMA.

Thermal chamber + TEC controller

: corner validation; essential for rings (§3.14.3, Chapter 6) and laser grids.

Use electrical loopback (host SerDes), optical loopback (Tx$\to$Rx on module), and golden-host/golden-module interop to bisect faults (§7.2.2). If the fault follows the module under golden-host swap, stop blaming the SerDes; if it stays with the host, stop opening laser FA.

## Building a link budget

A link budget is a signed dB (or power) ledger from transmitter to receiver. For IM/DD short reach, start from outer OMA at the Tx faceplate and subtract every loss and penalty until you compare against receiver sensitivity (with target BER and KP4 pre-FEC threshold, §3.12, §4.4).

##### Typical ledger (single-mode DR class).

Start from Tx OMA on the DCA (or from average power and ER). Subtract connector/coupling loss (1--3 dB per mated pair; fiber attach in CPO), fiber loss ($\sim$`<!-- -->`{=html}0.3--0.4 dB/km at 1310 nm; often negligible at 500 m), and MUX/de-MUX if WDM (2--5 dB per stage, §6.3). Add penalties for TDECQ (already in the OMA spec for many PMDs), dispersion (§3.11), and ORL/RIN reflection (§7.2.2, §4.3.1). Compare the remainder to stressed sensitivity at pre-FEC BER $2.4\times10^{-4}$, and keep 1--3 dB+ of production margin (more for fleet corners). Electrical budgets parallel this for the host-to-module path: COM and pre-FEC BER (§9.5.2, §3.6). LPO requires *both* ledgers to close without module DSP help.

## Module management: CMIS

### What CMIS is, and why an optical engineer cares

*CMIS* (Common Management Interface Specification) is the vendor-neutral management layer between a host (switch ASIC, NIC, or test fixture) and a pluggable or on-board optical module. The host talks to the module over a two-wire bus (TWI, I2C-like) through a paged register map: identity, power mode, alarms, per-lane monitors, and (at 224G/448G) link-training and host signal- integrity tuning extensions . CMIS covers QSFP-DD, OSFP, COBO, ELSFP, and CPO engines that expose the same management contract.

You touch CMIS on every bring-up and every field triage. It is how the host learns what module is seated, when lasers may turn on, what Tx/Rx power and temperature look like, and whether a link failed at the management layer or the optical layer. A module that passes BER on a bench with lasers forced on but cannot reach ModuleReady on a production host will fail in the fleet (§7.9).

### The module state machine

CMIS defines a module state machine the host drives. After presence detect and power application, the module stays in low power until the host releases `LPModeL` (or the CMIS 5.x `LowPwr` equivalent). The host reads identifier pages, clears sticky interrupts, and steps the module toward ModuleReady. Only then should Tx lanes or ELS lasers enable. ELSFP modules that emit before ModuleReady are a reject: the host did not authorize light (§5.11).

Data paths have their own state machines in CMIS 5.x (data path states, and network path states for media-side links). For bring-up, map the sequence in §7.9 onto these transitions: presence and Vcc, CMIS init and ModuleReady, enable light, optical path check, electrical lock, traffic, snapshot. Skipping step 2 and jumping to BER is how interop failures hide until production.

### The memory map: pages, monitors, control

The lower memory map holds module identity, status, interrupt flags, and alarm thresholds. Upper pages hold application descriptors, lane controls, tunable-laser support, versatile diagnostics (VDM), and command-data-block (CDB) firmware messaging . Hosts select an application (lane count, host interface, media type) before bringing up traffic.

*DDM* (digital diagnostic monitoring) is the telemetry layer you read at scale: per-lane Tx and Rx optical power, laser bias current when exposed, module temperature, supply voltage, LOS/LOL flags, and alarm/warning bits. On WDM parts you also get wavelength or channel ID. This is exactly what §7.12 reads before anyone reaches for a DCA. On bring-up, dump the register map you will use in the field and treat that dump as the golden reference for later RMA comparisons.

### CMIS as a validation deliverable

CMIS correctness is part of production readiness, not a firmware afterthought. ATP should prove the state machine reaches ModuleReady across voltage and thermal corners; DDM monitors track bench truth (CMIS Tx power versus DCA, module temperature versus case $T$); alarms fire at the right thresholds; and firmware revision is ECO-controlled like laser die revision (§8.10). Multi-source interop failures are often CMIS, media-type, or firmware mismatches, not marginal TDECQ (§7.9). At fleet scale the register map is the only eyes you have on a module in the rack. If CMIS is wrong, triage starts blind.

## Module and system bring-up

Characterization proves a sample can meet metrics on a quiet bench. Bring-up proves a module (then a system) can be powered, managed, and linked the way production and the fleet will actually run it. Lab-to-production programs fail in the gap between those two if you only ever test golden hosts, clean fiber, and room-temperature faceplates.

##### Module bring-up sequence.

Run this order on every new module (pluggable, ELSFP, or CPO engine with CMIS). Do not skip ahead to BER: a link that "works" with lasers forced on and CMIS ignored will fail the first host that enforces the state machine (§5.11).

1.  **Presence and power.** Detect module (`ModPrsL` or equivalent). Apply rails in the host power sequence. Confirm Vcc and module temperature in CMIS. Stay in low power (`LPModeL` asserted or ModuleLowPwr) until management is sane.

2.  **CMIS init.** Read identifier, vendor, firmware rev, supported media. Clear sticky interrupts. Confirm the state machine can reach ModuleReady (or the pluggable equivalent) under host command. Dump the register map you will use in the field; that dump is your bring-up golden reference.

3.  **Enable light.** Exit low power; enable Tx lanes / ELS lasers only after ModuleReady. Confirm Tx optical power and laser bias (if exposed) against the power class. Lasers that come up before the host asks are a reject for ELSFP (§5.11).

4.  **Optical path.** Mate fiber (clean first). Check Rx power and LOS. Optical loopback first if the host path is unproven.

5.  **Electrical lock.** Bring host SerDes / module CDR. Confirm LOL clear, equalizer taps not pegged (§3.6). For LPO, this is the host eye and COM path (§9.5.2, §3.14.3).

6.  **Traffic.** PRBS or live FEC traffic. Pre-FEC BER vs. KP4 threshold (§3.12); glance at FEC symbol-error histogram shape.

7.  **Quality snapshot.** On a Tx-capable path: OMA/RLM/TDECQ or module diagnostics that proxy them (§7.4). Record CMIS + BER + case $T$ together so later triage has a baseline (§7.12).

Table 7.3 is the short form you can put on a lab wall.

[]

  -------------------------------------------------------------------------------------------------------------------
  Step   Action                  Pass signal                                        Fail $\to$ first look
  ------ ----------------------- -------------------------------------------------- ---------------------------------
  1      Presence / Vcc / temp   CMIS alive, rails in range                         cable, seat, PSU

  2      CMIS state machine      ModuleReady (or equiv.)                            firmware, TWI, LPMode

  3      Enable Tx / ELS         Tx power in class; lasers on only when commanded   bias driver, enable pin, APC

  4      Fiber / Rx power        Rx power up; LOS clear                             dirty MT, polarity, break

  5      CDR / SerDes lock       LOL clear; taps not saturated                      host SI, LPO COM, retimer

  6      Pre-FEC BER             below KP4 target with margin                       Tx quality, ORL, Rx sensitivity

  7      Snapshot                CMIS dump + BER + $T$ logged                       (needed for RMA later)
  -------------------------------------------------------------------------------------------------------------------

**Table 7.3.** Module bring-up checklist. LOS = loss of signal; LOL = loss of lock. Limits come from the ATP and PMD, not from this table.

##### Production-representative corners.

Bench corners ($T$, $V$) are necessary and not sufficient. Before you call DVT or PVT done, run the corners that match how the fleet will abuse the link. Table 7.4 is the minimum set for IM/DD + laser programs.

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Corner              What to run                                                                                         Why it catches                                                Points to
  ------------------- --------------------------------------------------------------------------------------------------- ------------------------------------------------------------- -------------------------------
  Chassis thermal     Module in target rack/sled at airflow and power load; not only a quiet chamber on a bench fixture   Faceplate $T$ and TEC load differ from chamber setpoints      derate, TEC, ring unlock

  Host rails live     Bias / CMIS powered from host supplies with SerDes traffic on                                       Switching noise into laser bias looks like RIN (§5.7)         PSRR, ground, APC

  Dirty fiber / ORL   Controlled contamination or ORL stress on MT/FAU; clean vs dirty BER                                Field installs are not lab-clean; ORL raises RIN and bursts   connector, isolator, feedback

  Cable plant         Production fiber length, MPO count, and bend radius                                                 Extra loss and reflections eat margin the ledger assumed      link budget (§7.7)

  ELS hot-swap        Pull/replace ELSFP under traffic (or under controlled traffic stop per CMIS)                        Service action the architecture promised (§5.11)              state machine, mate cycles

  Neighbor load       Adjacent modules/lanes at full traffic and max case $T$                                             Crosstalk, shared supply droop, thermal crosstalk on rings    WDM lock, SI, PSU

  LPO / linear path   Host COM and pre-FEC BER without module DSP crutch                                                  LPO fails here first (§3.14.2, §9.5.2, §3.14.3)               host FIR, module linearity

  Voltage corners     Host Vcc min/max with traffic                                                                       Brown-out and CMIS glitches                                   power design, ATP
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.4.** Production-representative corners. A quiet BERT at 25 $^\circ$C with pristine fiber is characterization, not production readiness.

##### System bring-up.

A module that passes on a golden host can still fail in a real chassis:

- **Host path:** run the same sequence on the target NIC/switch ASIC SerDes, not only the lab BERT. LPO and half-retimed modules expose host FIR/CTLE mistakes that a retimed module hid (§9.5.1, §9.3).

- **Multi-lane / multi-module:** bring all lanes on a port, then neighbors in the same cage or tray. Watch thermal rise, supply droop, and CMIS temp alarms when the tray is loaded.

- **Golden swap:** known-good module in the suspect host slot, then suspect module in a known-good slot. That single swap splits host vs. module before you open FA (§7.12).

- **Interop:** at least one other vendor host or module if the program claims multi-source. Interop failures are usually CMIS, media type, or electrical eye, not laser physics.

- **ELS / CPO:** external laser modules add a second bring-up: ELSFP state machine and optical mate to the engine, then engine bring-up with light present (§5.11, §9.10). A dark engine with a healthy ELS is an optical connector or FAU problem until proven otherwise.

##### Exit criteria before "bring-up done."

Call module bring-up done only when: CMIS state machine and enable sequence are correct; pre-FEC BER meets target on the *target* host with margin; a CMIS+BER+$T$ snapshot is filed; and at least the chassis-thermal, host-rails, and ORL corners in Table 7.4 have been run on a representative unit. Call system bring-up done when golden-swap has split host vs. module issues and multi-lane / neighbor load has not opened a new failure mode. Everything after that is characterization depth, supplier gates (§8.10), or fleet triage (§7.12).

**Key idea.** Bring-up is a sequence (presence $\to$ CMIS $\to$ light $\to$ lock $\to$ BER $\to$ snapshot), then a system proof on the real host, then production-representative corners (chassis thermal, host-rail noise, ORL, ELS hot-swap, neighbor load). A quiet bench pass is not DVT.

## The debug mindset

Debug at this level is data-driven, not opinion-driven. The method is disciplined bisection: change one domain at a time, and let the measurement tell you whether the transmitter, the channel, or the receiver moved.

1.  Isolate transmitter versus channel versus receiver, using loopbacks.

2.  Sweep temperature and voltage to expose corner-dependent failures.

3.  Correlate failures to DSP equalizer tap values (§3.6) and FEC symbol-error statistics (§3.12); these tell you *how* the link fails.

The third step is where modern PAM4 links differ from older eye-mask work. Tap saturation and FEC histograms often reveal the failure mode before a single waveform screenshot does. Treat those as primary evidence, not as afterthoughts logged once BER already fails.

[^17]

## The debugging fork in validation

Apply the debugging fork (§4.8) before sweeping parameters or changing firmware: check the power meter or CMIS Rx power monitor first. If power moved, the fault is in the optical path (laser, coupling, connector, fiber, MUX); if power held but BER or TDECQ worsened, it is signal quality (bandwidth, noise, jitter, bias, equalization, reflection). This one check prevents the most common validation mistake: retuning an equalizer or laser bias when the real cause is a dirty connector.

## Fleet and field triage

Lab debug asks: *what is broken on this unit?* Fleet triage asks: *which bucket does this failure belong in, and who owns the fix?* Optical programs at fleet scale own that split across performance, reliability, and manufacturability. Wrong bucket wastes weeks (sending a contaminated connector to laser FA, or rewriting a SerDes FIR when the laser is rolling over).

##### Three buckets.

Classify every field issue before deep root-cause work:

Performance

: the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (§7.4, §9.5.2, §3.14.3).

Reliability

: the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (§8.4, §5.10, §8.2, §5.11).

Manufacturability

: a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (§8.10, §8.8).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; §5.11).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (§3.12), equalizer tap saturation (§3.6).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $\to$ bucket).

Table 7.5 is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

[]

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Symptom                               First telemetry check                                  Bucket                           Confirm on bench / FA                                                  Typical fix owner
  ------------------------------------- ------------------------------------------------------ -------------------------------- ---------------------------------------------------------------------- ---------------------------------------------
  Link never comes up (fresh install)   CMIS presence, Vcc, Tx power flatline, LOS             Mfg or install                   Visual fiber/connector; golden module swap; CMIS dump                  Ops install; supplier ATP if lot-correlated

  Intermittent LOS / burst errors       Rx power dropouts; FEC bursts; ORL events              Perf (ORL) or mfg (contam.)      Clean/inspect MT; ORL meter; RIN vs ORL (§5.7, §4.3.1)                 Ops cleaning; packaging if repeat RMA

  Pre-FEC BER high, power OK            Tap saturation; RLM/TDECQ if logged; case $T$          Perf                             DCA TDECQ/RLM; host COM; LPO vs retimed path (§7.4, §9.5.2)            Host SI / module Tx design

  BER rises only at high case $T$       Module temp alarm; Tx power drop; $\lambda$ walk       Perf or reliability              LIV at $T$; OSA grid; TEC current; EAM bias (§5.10)                    Derate / TEC / laser supplier

  Slow BER creep over weeks/months      Bias current up for same Tx power; SMSR if monitored   Reliability                      LIV/SMSR vs ship ATP; Arrhenius lot history                            Laser wear-out; ELS replace

  Sudden hard fail, was healthy         Last good CMIS snapshot; neighbor links OK             Reliability (COD) or mfg (ESD)   Dark LIV; DPA on facet/solder; date-code cluster?                      FA + supplier 8D

  One date code / site fails early      Lot Pareto; burn-in escape rate                        Mfg                              Incoming SPC vs ATP; FA on sample of lot                               Supplier CAPA; hold shipment

  WDM / ring unlock, power OK           Channel ID; thermal of neighbors; lock-loop status     Perf                             Resonance tune; crosstalk; CW-WDM line power (§6.7, §6.5, §5.13)       Lock firmware / thermal design

  ELSFP swap restores link              Old module CMIS vs new; connector cycles               Reliability or mfg (connector)   Inspect MT; mating-cycle count; laser LIV in returned module (§5.11)   Laser vs connector split in FA
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.5.** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $=$ performance (design/operating point); reliability $=$ time-dependent wear; mfg $=$ lot/process/install excursion.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $T$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with Table 7.5. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (§5.10).

    - Manufacturability: quarantine lot, incoming hold, supplier 8D with DPA photos and ATP deltas (§8.10).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Worked paths (three common tickets).

*"High temp only."* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate) until LIV at temperature shows threshold rise matching an aged lot, which flips it to reliability. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (§3.14.3, Chapter 6).

*"Random burst errors, average power fine."* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, it is performance/architecture (feedback). If ORL is fine and bursts track a date code, it is mfg (intermittent fiber attach). If bursts grow over months at fixed ORL, suspect laser or driver aging (§5.7, §5.10).

*"ELSFP replace fixed it; returned module looks alive on the bench."* Alive LIV with high ORL sensitivity or dirty MT face means connector/ORL (mfg/ops), not laser death. Dead or kinked LIV means reliability. Split those RMA codes explicitly or your FIT math will blame the wrong wear-out mode (§5.11, §8.8).

##### RMA labels that keep FIT honest.

RMA codes should be distinct, not a single "optics fail":

- laser wear-out (LIV/SMSR/EAM aging confirmed);

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

Use the least complex instrument that can falsify the current hypothesis. Table 7.2 maps every key metric to its instrument, rationale, and failure signature in one lookup; the bring-up sequence (§7.9) orders those instruments into a workflow.

### How it fails

Validation fails when the setup, sample, or acceptance rule does not match the product. Common misses are a stale calibration, the wrong reference plane, a golden host that hides interop risk, pristine fiber that hides ORL sensitivity, short BER dwell, one lane tested without neighbors, and chamber temperature used as a substitute for measured case temperature. These are test escapes even when the device physics is sound.

\> \*\*Failure mode: Low optical power\*\* \> \> \*\*Symptoms.\*\* A lane is dark or below its launch-power limit. \> \> \*\*Likely causes.\*\* A laser or enable fault, coupling loss, connector contamination, fiber polarity, calibration error, or a power-meter setup mistake. \> \> \*\*Measurements.\*\* Known source and meter, inspection scope, CMIS state and bias, power at successive planes, and a golden fiber or module. \> \> \*\*Mitigations.\*\* Correct the setup first, then repair the failing source, attach, connector, or control path. Add the signature at the earliest production test that can catch it.

### How it is debugged

Preserve the failing state and record software, firmware, calibration, fixture, cables, temperature, and supply. Verify the meter with a known source. Walk from power to spectrum to waveform to BER, moving one reference plane at a time. Use a golden swap to split host, module, and fiber. Only then stress temperature, voltage, ORL, and neighbors. Every corrective action needs a repeated failing test, a repeated passing test, and a guard against recurrence in ATP or telemetry.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* A new module lot showed low optical power on one station. \> \> \*\*Investigation.\*\* The same units passed on a second station. A known source exposed an offset in the first power-meter path. \> \> \*\*Finding.\*\* The lot was good, and the station was reading low. \> \> \*\*Root cause.\*\* A reference jumper had been replaced without updating the path-loss calibration. \> \> \*\*Resolution.\*\* The station was recalibrated, jumper identity was placed under change control, and a start-of- shift source check was added.

## Interview and design review questions

##### Concept.

- Why is a passing BER on a golden bench not sufficient for production readiness?

- What is the difference between characterization and validation?

- Why does LPO raise the stakes on transmitter TDECQ?

##### Design.

- What requirement does each test prove, at which plane, and with which uncertainty and guardband?

- Which corner is represented only by a lab fixture rather than the target host or chassis?

- What is the fastest measurement that can falsify each top risk?

- Which setup error can make a bad unit pass or a good unit fail?

##### Debug.

- A new module passes on the bench but fails on the production host. What is your first measurement?

- BER is high but optical power looks fine. Apply the debugging fork (§7.11): what do you check next?

- A module works on host A but fails on host B. How do you determine ownership?

- Are raw data, calibration state, firmware, and sample identity stored well enough to replay a failure months later?

##### Manufacturing and operations.

- What is the minimum set of corners that proves production readiness?

- How do you detect tester drift before it becomes a yield cliff or a field escape?

- What exit criteria distinguish DVT from PVT?

**Key idea.** Validation is a chain of evidence. Start with calibrated power and management state, move through spectrum and waveform, then trust BER only after the blocks and reference planes are known. Run the target host, chassis, fiber, and neighbor corners before calling the product ready.


<div class="nav-links">
  <a href="ch6-wdm-and-wavelength-locked-lasers">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch8-reliability-and-manufacturing-at-scale">Next &rarr;</a>
</div>
