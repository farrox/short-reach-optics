---
layout: default
title: "Ch 7: Optical validation"
---

# 7 Optical validation

A datasheet that closes on a quiet bench is not a product. *Validation* reduces uncertainty about whether a link meets its requirements across the temperatures, hosts, connectors, production spread, and lifetime the fleet will actually see. Passing tests is an output, not the purpose. This chapter walks the ladder from a single device to a deployed fleet, the engineering question at each stage, module and system bring-up under production-like corners, and the hypothesis-driven debug method the work demands.

Debugging asks which margin ledger was exhausted. Qualification asks how much margin remains after the expected stresses. Both are uncertainty reduction that ends in a decision (Appendix C).

## The validation ladder

Optical programs fail in the same places again and again: a part that looks good in characterization but cannot bring up on a production host, or a module that passes acceptance test plan (*ATP*) and then unlocks under neighbor heat. The ladder below is a decision framework, not a test menu. Each stage answers one question the previous stage could not answer. Skipping a rung does not save time. It moves the escape into a later, more expensive stage.

Requirements sit above the first gate: reach, lane rate, hosts, BER/FEC target, power and thermal envelope, lifetime, and production volume. Without those constraints, later measurements have no pass criterion (Appendix A.6.5).

  -----------------------------------------------------------------------------------------------------------------------------------------------------------
      Stage                  Main question                                  Evidence required                                  Decision unlocked
  --- ---------------------- ---------------------------------------------- -------------------------------------------------- ------------------------------
  1   Bring-up               Does it operate on a known-good host?          Power, management ready, light, lock, usable BER   Continue / debug integration

      Characterization       How does it behave across corners and units?   Mapped response vs $T$, $V$, ORL, age, lane        Derate / redesign / proceed

      Margin and interop     Does margin survive realistic use?             Loaded corners + target hosts/modules              Fleet corner OK / restrict

      Stress qualification   Will it survive intended life?                 Named mechanism + justified life evidence          Accept life risk / hold

      Production readiness   Can it be built and screened at volume?        Multi-lot yield, ATP, SPC, FAIR                    Open volume / hold

      Pilot and fleet        Were the assumptions correct in deployment?    Exit criteria + telemetry owners                   Ship / restrict / reject
  -----------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.1.** Validation ladder as a decision map. Instrument lists and stage detail follow below. The same order appears in expanded form in Appendix A.6.5, Appendix C.2.

  ---------------------------------------------------------------------------------------------------------------------------------
  Stage                  Entry uncertainty            Exit criteria                                  Decision unlocked
  ---------------------- ---------------------------- ---------------------------------------------- ------------------------------
  Bring-up               Part present; host unknown   Ready state, light, lock, BER on golden host   Continue / debug integration

  Characterization       Links at one corner          Mapped response vs $T$, $V$, ORL, age          Derate / redesign / proceed

  Margin and interop     Nominal map known            Loaded corners and target hosts close          Fleet corner OK / restrict

  Stress qualification   Mechanisms named             Life / env evidence with sample plan           Life risk accepted / hold

  Production readiness   Qual evidence in hand        Multi-lot yield, ATP, SPC, FAIR                Open volume / hold

  Pilot and fleet        Volume candidate             Exit criteria + telemetry owners               Ship / restrict / reject
  ---------------------------------------------------------------------------------------------------------------------------------

**Table 7.2.** Ladder gates for rapid retrieval. Do not treat an earlier exit as evidence for a later gate (Appendix C.2).

These tables are a grouped view of one canonical lifecycle, not a competing sequence. Stage 2 is nominal characterization. Stage 3 groups margin characterization with interoperability. Stage 4 is environmental and reliability qualification (stress / life). Stage 5 is manufacturing and ATP readiness. Stage 6 groups controlled pilot with fleet monitoring. The expanded stage names in Appendix A.6.5 map onto these six grouped stages in the same order.

<pre class="dectree" aria-label="Decision tree"><code>Requirement
  |
Budget (power / noise / timing / spectrum / control)
  |
Allocation to stages
  |
Verification on the ladder
  |
Production readiness
  |
Fleet feedback</code></pre>
### Stage 1: Bring-up

##### Purpose.

Does the product operate at all on a known-good host? Bring-up is not qualification. It asks whether power, management, light, timing recovery, and a usable error rate exist before anyone argues about margin.

##### Uncertainty removed.

Before bring-up you do not know whether a failure is integration (seat, cable, firmware, host) or product physics. After bring-up you know the unit can emit, receive, and pass data under controlled conditions.

##### Activities.

Power the module or engine. Confirm management presence and state progression through the Common Management Interface Specification (*CMIS*) state machine to a ready state. Enable transmit only when commanded. Verify first light and received power. Confirm clock and data recovery (*CDR*) lock, so later BER work is not dominated by a basic timing-recovery fail. Measure pre-FEC bit error ratio (*pre-FEC BER*) on a golden host. Details and fail branches live in §7.9, Table 7.4.

##### Measurements and evidence.

CMIS presence and ready state confirm the management path before you blame optics. CDR lock confirms the receiver can recover timing from the incoming stream; without stable lock, later BER work may only restate an integration fault. Pre-FEC BER is the first system health number: it is the error rate before FEC cleans the link, so it still reveals optical and electrical margin.

##### Exit criteria.

**Exit when** the unit reaches ready state, emits and receives light in class, holds CDR lock, and shows a usable pre-FEC BER on the golden host with named reference planes.

##### Decision unlocked.

Continue into characterization, or stop and debug integration (seat, power, firmware, fiber, host).

##### Risk if skipped.

You may spend weeks optimizing TDECQ or life models on a part that never reliably links in a real chassis.

### Stage 2: Characterization

##### Purpose.

How does the product behave across temperature, voltage, optical return loss (*ORL*), aging proxies, lanes, and units? Characterization maps the response surface. It does not yet prove fleet survival.

##### Uncertainty removed.

Before characterization you know one corner works. After it you know how distributions move with stress variables and which ledgers (power, noise, timing, spectral, control) are thin.

##### Activities.

Sweep case or junction temperature and supply. Stress ORL where reflections matter. Compare units and lots. On the transmitter path, measure transmitter and dispersion eye closure quaternary (*TDECQ*), outer optical modulation amplitude, extinction ratio, and level linearity. On components with access, measure light--current--voltage (*LIV*), relative intensity noise (*RIN*), and side-mode suppression ratio (*SMSR*). Close a signed link-budget ledger (§7.4, §7.7, §5.7).

##### Measurements and evidence.

TDECQ scores transmitter quality after a reference equalizer; a rise with stable average power points at bandwidth, linearity, or bias, not simple loss. Changes in the LIV baseline can support a physical-aging hypothesis, while a substantially healthy LIV combined with recovery after recalibration supports setpoint or control drift. LIV alone does not always perform a definitive separation. RIN under controlled ORL reveals feedback-sensitive floors. SMSR checks single-mode purity as temperature or age changes. Sensitivity and BER-versus-power waterfalls show whether the receiver path shifts or floors (Appendix A.6.9).

##### Exit criteria.

**Exit when** you have mapped population behavior versus the required corners, named the thin ledgers, and decided whether the design needs derate or redesign before loaded-fleet work.

##### Decision unlocked.

Proceed to margin and interoperability, derate the envelope, or redesign.

##### Risk if skipped.

A hero sample that worked at 25 $^\circ$C becomes the silent assumption for life and volume. Corner failures then appear as "surprises" in DVT.

### Stage 3: Margin and interoperability

##### Purpose.

Does remaining margin survive realistic system variation: chassis thermal load, live host supplies, dirty fiber, neighbor traffic, cable plant, and the target host or peer module?

##### Uncertainty removed.

Characterization maps the part. This stage asks whether that map still holds when the surrounding system is hostile in production-like ways (§7.9, §5.19).

##### Activities.

Run production-representative corners: module in target sled airflow, host rails with SerDes traffic, controlled contamination or ORL stress, production fiber length and bend radius, ELS hot-swap if the architecture promises it, adjacent modules at full load, and at least one non-golden host or second- source peer when multi-source is claimed.

##### Measurements and evidence.

Compare pre-FEC BER, telemetry, retrain count, and control headroom at the failing corner against the characterization baseline. An optical eye, when used, is measured externally unless an internal eye-monitor is explicitly named (Appendix C.10). Interop failures often land in CMIS, media type, or electrical eye rather than laser physics.

##### Exit criteria.

**Exit when** loaded corners and target hosts close with acceptable remaining margin, or when a documented restriction defines where the product may ship.

##### Decision unlocked.

Approve the fleet corner, restrict deployment, or send the design back.

##### Risk if skipped.

Quiet-bench margin evaporates in the first rack. Field tickets then look like random laser failures when the real escape was an untested corner.

### Stage 4: Stress qualification

##### Purpose.

Will the product survive its intended life under a named wear-out or environmental mechanism, not merely pass a short burn-in?

##### Uncertainty removed.

Functional and margin stages do not answer lifetime. Environmental sweeps ask how performance changes under a condition; reliability qualification asks whether exposure creates unacceptable permanent degradation over the intended life. Stress qualification covers both, and separates infant mortality and wear-out risk from operating-point mistakes (§8.2, §8.3).

##### Activities.

Run high-temperature operating life (*HTOL*), temperature cycling, humidity where claimed, electrostatic discharge (*ESD*) robustness, and connector mating cycles as required by the product class (often GR-468 / GR-1221 for optics and JESD47-class thinking for ICs). Name the failure class each stress is meant to expose, and justify activation energy $E_a$ when you project FIT.

##### Measurements and evidence.

Track the same customer-visible margins (power, BER/FEC, lock, wavelength) before and after stress. Compare LIV, SMSR, spectrum, and other physical baselines on returns: a permanent baseline shift supports physical aging, while a healthy baseline with recovery after recalibration supports setpoint or control drift. LIV is one useful baseline, not a universal aging detector. A life claim without a mechanism is a narrative, not evidence.

##### Exit criteria.

**Exit when** the sample plan, mechanism, and projected life support the requirements slice, or when you explicitly hold ship for life risk.

##### Decision unlocked.

Accept life risk for the envelope, derate life or use conditions, or hold.

##### Risk if skipped.

Early life failures concentrate by date code after volume ramp. Containment then costs more than the omitted HTOL matrix.

### Stage 5: Production readiness

##### Purpose.

Can the supplier reproduce the qualified result at volume, with screens that catch the escapes you care about?

##### Uncertainty removed.

A few carefully built engineering samples cannot establish volume readiness. Production readiness asks whether yield, process control, and ATP coverage survive lot-to-lot variation (§8.9, §8.10). Design Validation Test (*DVT*) asks whether the design meets requirements; Production Validation Test (*PVT*) asks whether the manufacturing line can build that design repeatedly at the intended scale.

##### Activities.

Review multi-lot yield and statistical process control (*SPC*). Correlate automated test equipment (*ATE*) to bench truth. Freeze ATP limits that catch the known escape paths. Complete first-article / FAIR gates and DVT / PVT exits that match the requirements slice.

##### Measurements and evidence.

Lot distributions for the same metrics used in characterization, guardbands between ATP and field fail, and evidence that the ATP would have caught prior escapes. Split supplier RMA codes so one vendor cannot hide inside a merged bucket.

##### Exit criteria.

**Exit when** multi-lot yield, ATP coverage, SPC stability, and FAIR evidence support opening volume, or when you hold for process control.

##### Decision unlocked.

Open volume, hold shipment, or demand corrective action before ramp.

##### Risk if skipped.

A qualified hero process ships an uncontrolled second lot. Fleet triage then becomes your de facto ATP.

### Stage 6: Controlled pilot and fleet monitoring

##### Purpose.

Were the qualification assumptions correct after real deployment, install practice, and traffic mix?

##### Uncertainty removed.

Lab corners never reproduce every rack. Pilot and fleet monitoring ask whether remaining margin, escape rate, and cohort signatures match the model (§7.12).

##### Activities.

Run a limited population with enhanced telemetry and clear exit criteria. Watch BER/FEC, retrains, power, temperature, lane behavior, and lot or site cohorts. Preserve CMIS dumps before reseat. Feed signatures back into ATP and design rules.

##### Measurements and evidence.

Cohort rates, not single tickets. Time behavior (sudden versus creep). Cool-down recovery versus permanent shift. Owner assignment uses the fleet triage map in Table 7.6.

##### Exit criteria.

**Exit when** pilot exit criteria are met and named owners watch the fleet metrics that would falsify the qual assumptions, or when you restrict or reject based on observed risk.

##### Decision unlocked.

Ship broadly, restrict, pause a supplier or lot, or reopen an earlier ladder stage.

##### Risk if skipped.

You learn the real escape mechanism from customer outage instead of from a controlled pilot.

### Why the stages occur in this order

Bring-up confirms that the system can produce interpretable data. Characterization establishes normal behavior. Margin testing identifies distance from failure; interoperability tests whether that margin survives realistic system variation (grouped as Stage 3). Stress qualification tests whether behavior survives time and named stress. Production readiness determines whether performance can be reproduced at volume. Controlled pilot and fleet monitoring check laboratory assumptions in the field, then at scale (grouped as Stage 6).

Later stages must not compensate for incomplete earlier stages. A large interoperability matrix cannot fix unstable bring-up. Reliability testing cannot establish manufacturing consistency from one engineering lot. An HTOL pass does not prove bring-up on the target host. Treat each exit as evidence only for its own question (Table 7.2, Appendix C.2).

### Learning summary

Bring-up

: Does it operate?

Characterization

: How does it behave?

Margin and interoperability

: How close is it to failure, and does that margin survive real system variation?

Stress qualification

: Will it survive its intended life?

Production readiness

: Can it be built and screened repeatedly at volume?

Pilot and fleet

: Do laboratory assumptions hold in a controlled cohort, and remain valid at scale?

> **Before qualification**
>
> Bring-up $\cdot$ characterization $\cdot$ margin/interop $\cdot$ stress/life $\cdot$ manufacturing/ATP $\cdot$ pilot/fleet feedback (Appendix C.15, Table 7.1).

For every metric at every stage, name the instrument, the reference plane (§3.9), the pass criterion, and the failure signature. A number without a plane and a method is not a measurement.

## The core IM/DD measurements

Once the ladder is clear, the measurement list is organized around isolation: transmitter, channel, and receiver. That split is older than PAM4. Long before TDECQ, field engineers learned that a dark link can be a dead laser, a dirty connector, or a dead TIA, and that guessing which one burns hours. Bisecting those three domains is still how you keep debug from turning into simultaneous retunes of everything.

### Transmitter

Start with the light leaving the faceplate or the CPO fiber array. For PAM4, the headline metric is *TDECQ* (transmitter and dispersion eye closure quaternary): a reference equalizer is applied to the captured eye and the residual penalty is reported in dB (§7.4). Alongside it you read *OMA* (outer), extinction ratio, and *RLM* (level linearity), plus wavelength, spectral width, and RIN with a bias-driver versus feedback bisect (§5.7, §5.8, §4.3.1).

What else you add depends on the transmitter style. Laser-bearing modules need LIV, threshold, slope, SMSR, and chirp checks for DMLs (§5.7, §5.4). External MZMs (TFLN or silicon) need EO $S_{21}$, $V_\pi$, quadrature bias versus temperature, and driver-path eye symmetry at baud (§3.14.3, §7.4). Microring banks need resonance alignment, thermal tuning, neighbor crosstalk, and peaking-network EO $S_{21}$ (§3.14.3, Chapter 6). The point of the list is not completeness for its own sake: it is knowing which instrument answers which hypothesis when the eye closes.

### Channel

If the transmitter looks clean into a golden receiver and the link still fails, the channel is next. Insertion loss from fiber, connectors, MUX/de-MUX (§6.3), and on-chip coupling (§3.14.3) is the first ledger line; plan about 1--3 dB per fiber interface. Chromatic dispersion (§3.11) matters more on FR-class SMF sweeps than on short DR links. Optical return loss (ORL) is the quiet killer: reflections back into the laser raise RIN and seed burst errors, which is why many DR/FR modules still carry isolators while some CPO engines rely on design margin and monitor photodiodes instead (§4.3.1, Chapter 5). Fiber attach (MPO/MTP, FAU, grating couplers) shows up as both yield and reliability (§8.8).

### Receiver

Receiver work asks whether the front-end can still decide bits at the OMA that survives the channel. Measure sensitivity (minimum OMA for the target BER) and stressed-receiver sensitivity with a calibrated stressor for margin (§7.5), plus overload before the TIA saturates. Underneath those system numbers sit the photodiode/TIA pair: responsivity, bandwidth, and input-referred noise (§4.5, Chapter 4).

### Link level

Only after Tx, channel, and Rx each look sane do you trust a full-link verdict: pre-FEC BER against the KP4 threshold (§3.12), post-FEC BER, FEC symbol-error histograms, and a signed link-budget ledger from transmitter OMA to receiver sensitivity with penalties and remaining margin. That ledger is the document you argue from in DVT; the BER alone is not.

## Measurement mapping

The metrics above are scattered across Tx, channel, Rx, and link level because that is how you debug them. Table 7.3 collects the same metrics into one reference: what is measured, the instrument, why it matters, and the failure signature that points back to it. Use the chapter subsections for the debug logic; use this table to look up an instrument fast.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Metric                        Instrument                          Why it matters                                                                          Failure signature
  ----------------------------- ----------------------------------- --------------------------------------------------------------------------------------- --------------------------------------------------------------------------------
  OMA / TDECQ                   DCA + reference equalizer           Scores transmitter quality against an ideal source; governs PAM4 acceptance (§7.4)      TDECQ rises with no average-power change; points to bandwidth, RLM, or bias

  Extinction ratio / RLM        DCA level histograms                Sets OMA at fixed average power (§4.4); poor RLM inflates TDECQ                         Compressed inner eyes with passing average power

  Wavelength / SMSR             OSA or wavemeter                    Confirms grid placement and single-mode purity (§5.7)                                   Side modes rise with $T$ or age; line walks off grid

  RIN                           PD + electrical spectrum analyzer   Sets the BER floor $Q_\mathrm{max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ (§4.3)        BER improves with power then flattens (a floor)

  Insertion loss / ORL          Power meter + ORL meter             First ledger line; reflections raise RIN and seed bursts (§7.2.2)                       Burst errors with stable average power; RIN rises with ORL

  Receiver sensitivity          BERT + calibrated attenuator        Minimum OMA at target BER, the budget's bottom line (§4.4, §7.5)                        Waterfall shifts uniformly right without flooring

  Pre-FEC BER / FEC histogram   BERT + FEC counters                 The single number every other metric feeds; histogram shape reveals mechanism (§3.12)   Clustered errors point to bursts; sparse errors point to Gaussian noise margin

  CMIS state / DDM              Host or CMIS tool                   Confirms management layer before blaming optics (§7.8)                                  Module never reaches ModuleReady; DDM disagrees with bench truth
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.3.** Measurement mapping: metric, instrument, rationale, and failure signature in one reference. Row explanations follow; chapter subsections give the full treatment of each metric.

### Reading the measurement map

Use the table for lookup. Use the notes below when a metric is new, or when you need the decision the measurement unlocks.

##### OMA / TDECQ.

TDECQ asks how much worse this transmitter is than an ideal source after a reference equalizer. Outer OMA is the optical swing the receiver actually uses. Together they answer whether the Tx path still has signal-quality margin. **Exit when** TDECQ and OMA meet the PMD/ATP at the named pattern and temperature. **Decision:** continue, retune bias/equalization, or reject the transmitter path. **Risk if skipped:** you chase receiver noise while the eye was already out of budget.

##### Extinction ratio / RLM.

Extinction ratio and level separation mismatch (RLM) set how much OMA you get at fixed average power and how linear the PAM4 levels are. Poor RLM inflates TDECQ even when average power looks fine. **Exit when** ER/RLM meet the mask at the failing corner. **Decision:** retune modulator bias or driver, or accept a derate. **Risk if skipped:** average-power APC hides a collapsing outer eye.

##### Wavelength / SMSR.

Wavelength placement and side-mode suppression ask whether the spectral ledger still closes: on-grid for filters or rings, single-mode under temperature and age. **Exit when** the line sits in the allowed window with SMSR in spec. **Decision:** retune lock/thermal control, derate temperature, or replace the laser. **Risk if skipped:** BER failures get blamed on RIN when the line walked onto a filter edge.

##### RIN.

Relative intensity noise sets how far $Q$ can rise with power. Measure with a quiet bias path and under controlled ORL so you separate intrinsic laser noise from feedback. **Exit when** RIN at the stated ORL meets the budget. **Decision:** fix reflections/supply, replace the laser, or stop raising launch into a floor. **Risk if skipped:** you keep adding photons to a non-power-limited impairment (Appendix A.6.9).

##### Insertion loss / ORL.

Insertion loss is the first power-ledger line. ORL asks whether reflections are seeding RIN or bursts. **Exit when** loss and ORL are inside the plant assumptions used in the link budget. **Decision:** clean/replace connectors, add isolation, or reopen the budget. **Risk if skipped:** burst tickets look like random laser death.

##### Receiver sensitivity.

Sensitivity is the minimum OMA for the target BER, the budget's bottom line. A parallel waterfall shift with no floor usually means the Rx path or channel loss changed. **Exit when** sensitivity meets the ledger with stated pattern and stress. **Decision:** golden-swap ownership, derate reach, or redesign Rx. **Risk if skipped:** Tx FA on an Rx-limited link.

##### Pre-FEC BER / FEC histogram.

Pre-FEC BER is the system score every other metric feeds. The FEC histogram shape separates sparse Gaussian-like errors from clustered bursts (MPI, intermittents, unlocked intervals). **Exit when** BER and histogram support the claimed mechanism class. **Decision:** contain, clean, retune, or open FA. **Risk if skipped:** average BER hides a bursty escape that ATP never stressed.

##### CMIS state / DDM.

Management state and digital diagnostics confirm the control and monitor path before you blame photons. Disagreement between digital diagnostics monitoring (DDM) and an external meter is itself a finding (monitor-PD or calibration). **Exit when** state progression and DDM match bench truth at the named plane. **Decision:** fix firmware/seat/power, or proceed to optics. **Risk if skipped:** weeks of optical FA on a module that never reached ready.

### Why this map is ordered by isolation

Transmitter metrics come before channel and receiver metrics because a bad Tx eye contaminates every downstream number. Channel loss and ORL come before Rx sensitivity arguments for the same reason. Link-level BER is last: it is the verdict, not the first bisect. If you start at BER alone, you still need this map to choose the next instrument.

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

<pre class="dectree" aria-label="Decision tree"><code>Transmitter output (OMA)
  |
Coupling loss
  |
Connector loss
  |
Fiber / waveguide loss
  |
Additional penalties (TDECQ / dispersion / ORL)
  |
Receiver input
  |
Sensitivity requirement
  |
Remaining margin</code></pre>
Keep power budget, signal-quality penalties, timing, thermal, and control authority as separate ledgers when the impairment is not a pure optical-power number (§5.19, Appendix C.9).

##### Design allocation versus validation measurement.

Distinguish margin allocation in design from margin verification in test. During design, engineers allocate transmitter output, receiver sensitivity, insertion loss, temperature degradation, aging, jitter, and manufacturing variation. During customer or system qualification, the integrator often validates the net behavior across the operating envelope.

<pre class="dectree" aria-label="Decision tree"><code>Design: allocate line items
  |
Build / integrate
  |
Test: measure net at named plane
  |
Room-T sensitivity margin
  |
Temperature / stress sweep
  |
Observed margin loss
  |
Remaining headroom
  |
Deployment decision</code></pre>
##### Typical ledger (single-mode DR class).

Start from Tx OMA on the DCA (or from average power and ER). Subtract connector/coupling loss (1--3 dB per mated pair; fiber attach in CPO), fiber loss ($\sim$`<!-- -->`{=html}0.3--0.4 dB/km at 1310 nm; often negligible at 500 m), and MUX/de-MUX if WDM (2--5 dB per stage, §6.3). Add penalties for TDECQ (already in the OMA spec for many PMDs), dispersion (§3.11), and ORL/RIN reflection (§7.2.2, §4.3.1). Compare the remainder to stressed sensitivity at pre-FEC BER $2.4\times10^{-4}$, and keep 1--3 dB+ of production margin (more for fleet corners). Numbers here are examples for a DR-class sketch, not universal limits. Electrical budgets parallel this for the host-to-module path: COM and pre-FEC BER (§9.5.2, §3.6). LPO requires *both* ledgers to close without module DSP help.

## Module management: CMIS

### What CMIS is, and why an optical engineer cares

*CMIS* (Common Management Interface Specification) is the vendor-neutral management layer between a host (switch ASIC, NIC, or test fixture) and a pluggable or on-board optical module. The host talks to the module over a two-wire bus (TWI, I2C-like) through a paged register map: identity, power mode, alarms, per-lane monitors, and (at 224G/448G) link-training and host signal- integrity tuning extensions . CMIS covers QSFP-DD, OSFP, COBO, ELSFP, and CPO engines that expose the same management contract.

You touch CMIS on every bring-up and every field triage. It is how the host learns what module is seated, when lasers may turn on, what Tx/Rx power and temperature look like, and whether a link failed at the management layer or the optical layer. A module that passes BER on a bench with lasers forced on but cannot reach ModuleReady on a production host will fail in the fleet (§7.9).

### The module state machine

CMIS defines a module state machine the host drives. After presence detect and power application, the module stays in low power until the host releases `LPModeL` (or the CMIS 5.x `LowPwr` equivalent). The host reads identifier pages, clears sticky interrupts, and steps the module toward ModuleReady. Only then should Tx lanes or ELS lasers enable. ELSFP modules that emit before ModuleReady are a reject: the host did not authorize light (§5.14).

Data paths have their own state machines in CMIS 5.x (data path states, and network path states for media-side links). For bring-up, map the sequence in §7.9 onto these transitions: presence and Vcc, CMIS init and ModuleReady, enable light, optical path check, electrical lock, traffic, snapshot. Skipping step 2 and jumping to BER is how interop failures hide until production.

### The memory map: pages, monitors, control

The lower memory map holds module identity, status, interrupt flags, and alarm thresholds. Upper pages hold application descriptors, lane controls, tunable-laser support, versatile diagnostics (VDM), and command-data-block (CDB) firmware messaging . Hosts select an application (lane count, host interface, media type) before bringing up traffic.

*DDM* (digital diagnostic monitoring) is the telemetry layer you read at scale: per-lane Tx and Rx optical power, laser bias current when exposed, module temperature, supply voltage, LOS/LOL flags, and alarm/warning bits. On WDM parts you also get wavelength or channel ID. This is exactly what §7.12 reads before anyone reaches for a DCA. On bring-up, dump the register map you will use in the field and treat that dump as the golden reference for later RMA comparisons.

### CMIS as a validation deliverable

CMIS correctness is part of production readiness, not a firmware afterthought. ATP should prove the state machine reaches ModuleReady across voltage and thermal corners; DDM monitors track bench truth (CMIS Tx power versus DCA, module temperature versus case $T$); alarms fire at the right thresholds; and firmware revision is ECO-controlled like laser die revision (§8.10). Multi-source interop failures are often CMIS, media-type, or firmware mismatches, not marginal TDECQ (§7.9). At fleet scale the register map is the only eyes you have on a module in the rack. If CMIS is wrong, triage starts blind.

## Module and system bring-up

Characterization proves a sample can meet metrics on a quiet bench. Bring-up proves a module (then a system) can be powered, managed, and linked the way production and the fleet will actually run it. Lab-to-production programs fail in the gap between those two if you only ever test golden hosts, clean fiber, and room-temperature faceplates.

##### Module bring-up sequence.

Run this order on every new module (pluggable, ELSFP, or CPO engine with CMIS). Do not skip ahead to BER: a link that "works" with lasers forced on and CMIS ignored will fail the first host that enforces the state machine (§5.14).

1.  **Presence and power.** Detect module (`ModPrsL` or equivalent). Apply rails in the host power sequence. Confirm Vcc and module temperature in CMIS. Stay in low power (`LPModeL` asserted or ModuleLowPwr) until management is sane.

2.  **CMIS init.** Read identifier, vendor, firmware rev, supported media. Clear sticky interrupts. Confirm the state machine can reach ModuleReady (or the pluggable equivalent) under host command. Dump the register map you will use in the field; that dump is your bring-up golden reference.

3.  **Enable light.** Exit low power; enable Tx lanes / ELS lasers only after ModuleReady. Confirm Tx optical power and laser bias (if exposed) against the power class. Lasers that come up before the host asks are a reject for ELSFP (§5.14).

4.  **Optical path.** Mate fiber (clean first). Check Rx power and LOS. Optical loopback first if the host path is unproven.

5.  **Electrical lock.** Bring host SerDes / module CDR. Confirm LOL clear, equalizer taps not pegged (§3.6). For LPO, this is the host eye and COM path (§9.5.2, §3.14.3).

6.  **Traffic.** PRBS or live FEC traffic. Pre-FEC BER vs. KP4 threshold (§3.12); glance at FEC symbol-error histogram shape.

7.  **Quality snapshot.** On a Tx-capable path: OMA/RLM/TDECQ or module diagnostics that proxy them (§7.4). Record CMIS + BER + case $T$ together so later triage has a baseline (§7.12).

Table 7.4 is the short form you can put on a lab wall.

  -------------------------------------------------------------------------------------------------------------------
  Step   Action                  Pass signal                                        Fail $\to$ first look
  ------ ----------------------- -------------------------------------------------- ---------------------------------
  1      Presence / Vcc / temp   CMIS alive, rails in range                         cable, seat, PSU

         CMIS state machine      ModuleReady (or equiv.)                            firmware, TWI, LPMode

         Enable Tx / ELS         Tx power in class; lasers on only when commanded   bias driver, enable pin, APC

         Fiber / Rx power        Rx power up; LOS clear                             dirty MT, polarity, break

         CDR / SerDes lock       LOL clear; taps not saturated                      host SI, LPO COM, retimer

         Pre-FEC BER             below KP4 target with margin                       Tx quality, ORL, Rx sensitivity

         Snapshot                CMIS dump + BER + $T$ logged                       (needed for RMA later)
  -------------------------------------------------------------------------------------------------------------------

**Table 7.4.** Module bring-up checklist. LOS = loss of signal; LOL = loss of lock. Limits come from the ATP and PMD, not from this table.

##### Production-representative corners.

Bench corners ($T$, $V$) are necessary and not sufficient. Before you call DVT or PVT done, run the corners that match how the fleet will abuse the link. Table 7.5 is the minimum set for IM/DD + laser programs.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Corner              What to run                                                                                         Why it catches                                                Points to
  ------------------- --------------------------------------------------------------------------------------------------- ------------------------------------------------------------- -------------------------------
  Chassis thermal     Module in target rack/sled at airflow and power load; not only a quiet chamber on a bench fixture   Faceplate $T$ and TEC load differ from chamber setpoints      derate, TEC, ring unlock

  Host rails live     Bias / CMIS powered from host supplies with SerDes traffic on                                       Switching noise into laser bias looks like RIN (§5.8)         PSRR, ground, APC

  Dirty fiber / ORL   Controlled contamination or ORL stress on MT/FAU; clean vs dirty BER                                Field installs are not lab-clean; ORL raises RIN and bursts   connector, isolator, feedback

  Cable plant         Production fiber length, MPO count, and bend radius                                                 Extra loss and reflections eat margin the ledger assumed      link budget (§7.7)

  ELS hot-swap        Pull/replace ELSFP under traffic (or under controlled traffic stop per CMIS)                        Service action the architecture promised (§5.14)              state machine, mate cycles

  Neighbor load       Adjacent modules/lanes at full traffic and max case $T$                                             Crosstalk, shared supply droop, thermal crosstalk on rings    WDM lock, SI, PSU

  LPO / linear path   Host COM and pre-FEC BER without module DSP crutch                                                  LPO fails here first (§3.14.2, §9.5.2, §3.14.3)               host FIR, module linearity

  Voltage corners     Host Vcc min/max with traffic                                                                       Brown-out and CMIS glitches                                   power design, ATP
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.5.** Production-representative corners. A quiet BERT at 25 $^\circ$C with pristine fiber is characterization, not production readiness.

### Reading the production-corner map

Bench temperature and voltage sweeps answer how the part behaves. The corners in Table 7.5 answer whether that behavior survives the rack, host, plant, and service actions the fleet will actually apply. Run them before you call DVT or PVT done.

##### Chassis thermal.

**Purpose.** Does the module hold lock, power, and BER when faceplate temperature and TEC load match a powered sled, not only a quiet chamber setpoint?

**Uncertainty removed.** Chamber case-$T$ does not prove airflow, neighbor heat, or faceplate gradient. After chassis thermal you know whether derate, TEC, or ring unlock risk is real under load.

**Activities.** Install in the target rack or sled. Apply production airflow and power load. Log case $T$, TEC current, lock, and pre-FEC BER versus the chamber baseline.

**Exit criteria.** **Exit when** loaded sled thermal either closes with margin or names a derate / TEC / unlock restriction.

**Decision unlocked.** Approve the thermal envelope, restrict deployment, or redesign cooling / lock.

**Risk if skipped.** Quiet-chamber passes unlock or floor in the first dense tray.

##### Host rails live.

**Purpose.** Does laser bias and CMIS stay clean when host supplies switch under SerDes traffic?

**Uncertainty removed.** A lab PSU hides switching noise into bias that looks like RIN (§5.8). After live rails you know whether PSRR, ground, or APC owns the floor.

**Activities.** Power bias and CMIS from the target host with traffic on. Compare BER and bias telemetry to a quiet supply.

**Exit criteria.** **Exit when** host-rail corners meet BER and telemetry limits, or a named supply / grounding fix is required.

**Decision unlocked.** Approve host pairing, demand PSRR/ground work, or hold LPO / linear paths that cannot tolerate the noise.

**Risk if skipped.** You chase optical RIN while the host injects the noise.

##### Dirty fiber / ORL.

**Purpose.** Does the link survive controlled contamination or ORL stress the way field installs will?

**Uncertainty removed.** Pristine MT fiber hides reflection-driven RIN and burst errors. After clean versus dirty BER you know whether connector, isolator, or feedback limits the plant.

**Activities.** Apply controlled ORL or contamination on MT/FAU. Compare BER, RIN proxies, and recovery after clean.

**Exit criteria.** **Exit when** stressed-ORL BER either meets the plant budget or forces isolator / connector / service rules.

**Decision unlocked.** Approve plant practice, tighten cleaning / mate rules, or require better isolation.

**Risk if skipped.** Lab heroes fail the first dirty install and look like random laser RMAs.

##### Cable plant.

**Purpose.** Does the link budget survive production fiber length, MPO count, and bend radius?

**Uncertainty removed.** A short golden patchcord does not prove the ledger. After production plant you know whether extra loss and reflections eat the assumed margin (§7.7).

**Activities.** Run the production cable set. Measure loss, ORL, and BER against the signed budget.

**Exit criteria.** **Exit when** production plant closes the budget with remaining margin, or the ledger is revised.

**Decision unlocked.** Approve plant design, cut reach or connectors, or raise launch / Rx requirements.

**Risk if skipped.** Budget fiction becomes field brownouts on long MPO chains.

##### ELS hot-swap.

**Purpose.** Can the external laser source be pulled and replaced under the service model the architecture promised (§5.14)?

**Uncertainty removed.** Static bring-up does not prove CMIS state machines, mate wear, or traffic recovery under swap. After hot-swap (or controlled stop per CMIS) you know whether service is real.

**Activities.** Pull/replace ELSFP under traffic or under the documented traffic stop. Log state machine, mate cycles, and recovery BER.

**Exit criteria.** **Exit when** swap recovers to ready state and BER without undefined hangs, or service is restricted.

**Decision unlocked.** Approve field-replaceable ELS service, or forbid hot-swap and rewrite ops.

**Risk if skipped.** The replaceable-laser story fails the first maintenance window.

##### Neighbor load.

**Purpose.** Do crosstalk, shared supply droop, and thermal crosstalk stay inside margin when adjacent modules and lanes run full traffic at max case $T$?

**Uncertainty removed.** A lone hero module hides tray-level coupling. After neighbor load you know whether WDM lock, SI, or PSU owns the fail.

**Activities.** Light neighbors at full traffic and temperature. Watch lock, BER, supply droop, and lane coupling.

**Exit criteria.** **Exit when** loaded-neighbor corners close, or a spacing / power / lock restriction is named.

**Decision unlocked.** Approve dense packing, derate neighbor density, or redesign supply / lock.

**Risk if skipped.** Single-module DVT passes; tray bring-up fails.

##### LPO / linear path.

**Purpose.** Does host channel operating margin (COM) and pre-FEC BER close without a module DSP crutch (§3.14.2, §9.5.2, §3.14.3)?

**Uncertainty removed.** Retimed modules hide host FIR and module linearity faults. After the linear path corner you know whether LPO is shippable on the target host.

**Activities.** Run host COM and pre-FEC BER on the linear electrical path. Sweep host equalization as needed.

**Exit criteria.** **Exit when** LPO/linear BER and COM meet targets on the production host, or LPO is rejected for that host class.

**Decision unlocked.** Approve LPO deployment, force retimed optics, or redesign host FIR / module linearity.

**Risk if skipped.** LPO ships on hope and fails first on the production ASIC SerDes.

##### Voltage corners.

**Purpose.** Do brown-out and CMIS glitches stay clear at host Vcc min/max under traffic?

**Uncertainty removed.** Nominal Vcc hides state-machine and bias glitches at rail edges. After voltage corners you know whether power design and ATP cover the envelope.

**Activities.** Sweep host Vcc with traffic. Log CMIS state, alarms, and BER.

**Exit criteria.** **Exit when** min/max Vcc corners pass with stable management and BER, or power design changes.

**Decision unlocked.** Approve voltage envelope, tighten ATP voltage screens, or redesign power.

**Risk if skipped.** Field brown-outs look like firmware or optics bugs.

### Why these corners come after quiet characterization

Quiet $T$/$V$ characterization maps the part. Production corners ask whether that map survives chassis heat, live host noise, dirty plant, service swaps, neighbors, linear hosts, and rail edges. Later fleet monitoring must not be asked to invent coverage that these corners never ran. Chassis thermal, host rails, and ORL are the minimum before you call bring-up or DVT done on a representative unit; the full set in Table 7.5 belongs before PVT exit.

### Learning summary

Chassis thermal

: Does sled airflow and faceplate $T$ match the claim?

Host rails / voltage

: Does live supply noise and rail edge stay clean?

Dirty fiber / cable plant

: Does the real plant leave margin?

ELS hot-swap / neighbors

: Does service and dense packing survive?

LPO / linear path

: Does the host close without module DSP?

##### System bring-up.

A module that passes on a golden host can still fail in a real chassis:

- **Host path:** run the same sequence on the target NIC/switch ASIC SerDes, not only the lab BERT. LPO and half-retimed modules expose host FIR/CTLE mistakes that a retimed module hid (§9.5.1, §9.3).

- **Multi-lane / multi-module:** bring all lanes on a port, then neighbors in the same cage or tray. Watch thermal rise, supply droop, and CMIS temp alarms when the tray is loaded.

- **Golden swap:** known-good module in the suspect host slot, then suspect module in a known-good slot. That single swap splits host vs. module before you open FA (§7.12).

- **Interop:** at least one other vendor host or module if the program claims multi-source. Interop failures are usually CMIS, media type, or electrical eye, not laser physics.

- **ELS / CPO:** external laser modules add a second bring-up: ELSFP state machine and optical mate to the engine, then engine bring-up with light present (§5.14, §9.10). A dark engine with a healthy ELS is an optical connector or FAU problem until proven otherwise.

##### Exit criteria before "bring-up done."

Call module bring-up done only when: CMIS state machine and enable sequence are correct; pre-FEC BER meets target on the *target* host with margin; a CMIS+BER+$T$ snapshot is filed; and at least the chassis-thermal, host-rails, and ORL corners in Table 7.5 have been run on a representative unit. Call system bring-up done when golden-swap has split host vs. module issues and multi-lane / neighbor load has not opened a new failure mode. Everything after that is characterization depth, supplier gates (§8.10), or fleet triage (§7.12).

**Key idea.** Bring-up is a sequence (presence $\to$ CMIS $\to$ light $\to$ lock $\to$ BER $\to$ snapshot), then a system proof on the real host, then production-representative corners (chassis thermal, host-rail noise, ORL, ELS hot-swap, neighbor load). A quiet bench pass is not DVT.

## The debug mindset

Debug at this level is data-driven, not opinion-driven. The method is disciplined bisection: change one domain at a time, and let the measurement tell you whether the transmitter, the channel, or the receiver moved.

1.  Isolate transmitter versus channel versus receiver, using loopbacks.

2.  Sweep temperature and voltage to expose corner-dependent failures.

3.  Correlate failures to DSP equalizer tap values (§3.6) and FEC symbol-error statistics (§3.12); these tell you *how* the link fails.

The third step is where modern PAM4 links differ from older eye-mask work. Tap saturation and FEC histograms often reveal the failure mode before a single waveform screenshot does. Treat those as primary evidence, not as afterthoughts logged once BER already fails.

[^17]

## The debugging fork in validation

Apply the debugging fork (§4.8) before sweeping parameters or changing firmware: check the power meter or CMIS Rx power monitor first. If power moved, the fault is in the optical path (laser, coupling, connector, fiber, MUX); if power held but BER or TDECQ worsened, it is signal quality (bandwidth, noise, jitter, bias, equalization, reflection). This one check prevents the most common validation mistake: retuning an equalizer or laser bias when the real cause is a dirty connector. Then check which margin ledger moved (§5.19) before descending to component physics.

<pre class="dectree" aria-label="Decision tree"><code>Observation
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
> Scope $\cdot$ time behavior $\cdot$ population $\cdot$ power or quality $\cdot$ highest-value measurement $\cdot$ decision $\cdot$ recurrence control (Appendix C.15).

## Fleet and field triage

Lab debug asks: *what is broken on this unit?* Fleet triage asks: *which bucket does this failure belong in, and who owns the fix?* Optical programs at fleet scale own that split across performance, reliability, and manufacturability. Wrong bucket wastes weeks (sending a contaminated connector to laser FA, or rewriting a SerDes FIR when the laser is rolling over).

##### Three buckets.

Classify every field issue before deep root-cause work:

Performance

: the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (§7.4, §9.5.2, §3.14.3).

Reliability

: the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (§8.4, §5.13, §8.2, §5.14).

Manufacturability

: a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (§8.10, §8.8).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label. Chapter 10 expands the same method into symptom-led bench and fleet procedures.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; §5.14).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (§3.12), equalizer tap saturation (§3.6).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $\to$ bucket).

Table 7.6 is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

<pre class="dectree" aria-label="Decision tree"><code>Fleet symptom
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
Scope sets severity and priors. Correlation after isolation unlocks contain, pause, replace, or supplier escalate (Appendix C.4).

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Symptom                               First telemetry check                                  Bucket                           Confirm on bench / FA                                                  Typical fix owner
  ------------------------------------- ------------------------------------------------------ -------------------------------- ---------------------------------------------------------------------- ---------------------------------------------
  Link never comes up (fresh install)   CMIS presence, Vcc, Tx power flatline, LOS             Mfg or install                   Visual fiber/connector; golden module swap; CMIS dump                  Ops install; supplier ATP if lot-correlated

  Intermittent LOS / burst errors       Rx power dropouts; FEC bursts; ORL events              Perf (ORL) or mfg (contam.)      Clean/inspect MT; ORL meter; RIN vs ORL (§5.8, §4.3.1)                 Ops cleaning; packaging if repeat RMA

  Pre-FEC BER high, power OK            Tap saturation; RLM/TDECQ if logged; case $T$          Perf                             DCA TDECQ/RLM; host COM; LPO vs retimed path (§7.4, §9.5.2)            Host SI / module Tx design

  BER rises only at high case $T$       Module temp alarm; Tx power drop; $\lambda$ walk       Perf or reliability              LIV at $T$; OSA grid; TEC current; EAM bias (§5.13)                    Derate / TEC / laser supplier

  Slow BER creep over weeks/months      Bias current up for same Tx power; SMSR if monitored   Reliability                      LIV/SMSR vs ship ATP; Arrhenius lot history                            Laser wear-out; ELS replace

  Sudden hard fail, was healthy         Last good CMIS snapshot; neighbor links OK             Reliability (COD) or mfg (ESD)   Dark LIV; DPA on facet/solder; date-code cluster?                      FA + supplier 8D

  One date code / site fails early      Lot Pareto; burn-in escape rate                        Mfg                              Incoming SPC vs ATP; FA on sample of lot                               Supplier CAPA; hold shipment

  WDM / ring unlock, power OK           Channel ID; thermal of neighbors; lock-loop status     Perf                             Resonance tune; crosstalk; CW-WDM line power (§6.7, §6.5, §5.16)       Lock firmware / thermal design

  ELSFP swap restores link              Old module CMIS vs new; connector cycles               Reliability or mfg (connector)   Inspect MT; mating-cycle count; laser LIV in returned module (§5.14)   Laser vs connector split in FA
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table 7.6.** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $=$ performance (design/operating point); reliability $=$ time-dependent wear; mfg $=$ lot/process/install excursion. Row notes follow.

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

Ask whether the external laser, the connector, or the engine owned the fail. Compare old versus new CMIS and connector cycles. Confirm MT inspect and LIV on the returned module. **Decision:** split RMA codes for laser versus connector. **Risk if skipped:** FIT burns down the wrong wear-out mode (§5.14).

### Why triage order matters

Scope before mechanism. Telemetry before destructive FA. Bucket before owner. Confirm before CAPA. Closing the loop into ATP is part of the incident, not optional paperwork. Reversing that order produces NFF piles and merged RMA codes that make life models dishonest.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $T$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with Table 7.6. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (§5.13).

    - Manufacturability: quarantine lot, incoming hold, supplier 8D with DPA photos and ATP deltas (§8.10).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Worked paths (three common tickets).

*"High temp only."* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate). A permanent LIV or spectrum shift at temperature that matches an aged lot raises $P(\mathrm{aging})$ and justifies moving the ticket toward reliability; cool-down recovery without baseline shift keeps it in performance. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (§3.14.3, Chapter 6).

*"Random burst errors, average power fine."* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, it is performance/architecture (feedback). If ORL is fine and bursts track a date code, it is mfg (intermittent fiber attach). If bursts grow over months at fixed ORL, suspect laser or driver aging (§5.8, §5.13).

*"ELSFP replace fixed it; returned module looks alive on the bench."* Alive LIV with high ORL sensitivity or dirty MT face means connector/ORL (mfg/ops), not laser death. Dead or kinked LIV means reliability. Split those RMA codes explicitly or your FIT math will blame the wrong wear-out mode (§5.14, §8.8).

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

## Engineering lens

### How it works

Validation is a chain of evidence, not a single pass: a number means nothing without its reference plane, its corner, and its method. The chapter's ladder, instruments, and triage tree are that evidence chain from bench to fleet.

### How it is measured

Use the least complex instrument that can falsify the current hypothesis. Table 7.3 maps every key metric to its instrument, rationale, and failure signature in one lookup; the bring-up sequence (§7.9) orders those instruments into a workflow.

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
