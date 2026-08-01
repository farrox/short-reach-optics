---
layout: default
title: "Ch 7: Choosing light sources and modulation"
---

# 7 Choosing light sources and modulation

*Read first:* architecture paths; DML vs EML vs external modulation; LIV/SMSR/RIN; thermal versus aging; calibration.

*Deep dive:* bias-driver noise math; ELSFP pinout; optical-safety classes; CW-WDM source survey.

*Reference:* source/modulation matrix, laser PRD, measurement playbook, supplier ownership table.

Do not choose a laser by comparing data sheets in isolation. Start with reach, lane rate, fiber plant, power, cost, lifetime, manufacturing volume, and service policy. Those requirements select an architecture. The architecture then limits the useful source, modulation, detector, packaging, and validation choices.

## System requirements and architecture paths

Freeze the system problem before asking a supplier for samples. Decision order:

<pre class="dectree" aria-label="Fiber plant and reach"><code>Fiber plant and reach
  |
Lane rate and waveform requirement
  |
Physics vetoes (modal BW, chirp, dispersion, EO BW, lock)
  |
Power and thermal budget
  |
Manufacturing and supplier capability
  |
Reliability and service model
  |
Validation and production evidence</code></pre>
Fiber plant and reach

: decide whether multimode loss and modal bandwidth are acceptable or whether the link needs single-mode fiber.

Lane rate and waveform

: decide whether direct modulation closes the eye or whether the link needs an EML, MZM, or ring.

Physics vetoes

: eliminate paths that cannot close modal bandwidth, chirp and dispersion, electro-optic bandwidth, or wavelength-lock range.

Power and thermal

: include laser wall-plug power, modulator loss, driver power, TEC power, and control overhead.

Manufacturing and supplier

: include fiber plant, assembly alignment, burn-in, test time, yield, and measurement capability, not only die price.

Reliability and service

: decide whether the source can stay inside the package or must be a replaceable ELSFP.

Validation and production evidence

: name characterization, qualification, ATP, sample audit, SPC, or fleet telemetry for each remaining risk (Chapter 9).

The choices are coupled. A cost-driven, short multimode link points toward an 850 nm VCSEL, multimode fiber, silicon photodiodes, and direct modulation. A longer single-mode path points toward a 1310 nm DFB or EML and germanium or III-V detection. Dense WDM and co-packaged optics often move the CW source away from the modulator, which adds wavelength control, fiber attach, and service requirements. §7.6, Table 7.3 turns these paths into supplier specifications.

## Light-source and modulation choices

Do not treat VCSEL, DML, EML, and silicon photonics as four equivalent laser families. VCSEL and DFB describe source structures. DML describes direct modulation of a laser. EML describes a laser integrated with an electro-absorption modulator. Silicon photonics describes a photonic integration platform that generally requires a CW source and a silicon modulator. Compare complete transmitter paths, not acronyms.

Source structures

: **VCSEL**: 850--940 nm multimode emitters for short MMF links; cheap, array-friendly, reach- and temperature-limited (§7.3). **DFB**: grating along the active region for single-mode CW or directly modulated output on SMF CWDM/LAN-WDM paths (§7.4). **DBR**: grating outside the gain region when tunability or separate gain/wavelength control is worth the control burden. **External-cavity laser**: narrow linewidth and tunability when spectral purity matters more than size and control simplicity; most short-reach IM/DD links do not need it .

Modulation / transmitter architectures

: **DML**: modulate laser bias current directly; few components, but chirp-limited over dispersive fiber (§7.3). **EML**: DFB integrated with an *EAM*; commonly used for 100--200G/lane single-mode DR and shorter reaches when bandwidth and chirp close (§7.4, §3.14.3). **CW + Si MZM**: external or heterogeneously integrated CW source into a silicon Mach--Zehnder on the PIC; low chirp and CMOS integration for many 100--200G/lane DR/FR SiPh modules (§3.14.3). **CW + Si ring**: same CW-source idea with a microring/microdisk modulator; dense and WDM/CPO-friendly, with lock and thermal crosstalk as the validation burden (§3.14.3, Chapter 8). **CW + TFLN MZM**: CW source into thin-film lithium niobate MZM; used where very low chirp and $\gtrsim$100 GHz EO bandwidth are needed (§3.14.3, Table 3.12).

Source placement

: **CW-WDM / multi-wavelength sources**: multi-line CW feed for comb-like WDM architectures (§7.16, §8.6). **ELS / ELSFP**: field-replaceable external CW module for co-packaged engines (§7.14).

<table class="book-table"><tr><th>Attribute</th><th>VCSEL direct</th><th>DFB direct</th><th>DFB + EAM</th><th>CW DFB/DBR + MZM</th><th>CW DFB/DBR + ring</th><th>External cavity + modulator</th></tr><tr><td>Wavelength / fiber</td><td>850--940 nm / MMF</td><td>1310 nm / SMF</td><td>1310 nm / SMF</td><td>1310 or 1550 nm / SMF</td><td>WDM grid / SMF</td><td>Tunable grid / SMF</td></tr><tr><td>Modulation fit</td><td>Direct only</td><td>Direct</td><td>Integrated EML</td><td>Si or TFLN MZM</td><td>Resonant Si ring</td><td>External MZM or ring</td></tr><tr><td>Bandwidth / reach</td><td>Short, modal limit</td><td>Chirp-limited</td><td>High BW, low chirp</td><td>High BW, broad passband</td><td>High BW, lock-limited</td><td>High BW, architecture-specific</td></tr><tr><td>RIN / linewidth</td><td>RIN and modal noise</td><td>RIN and chirp</td><td>RIN plus EAM bias</td><td>RIN; linewidth usually secondary</td><td>RIN plus spectral alignment</td><td>Low linewidth; verify feedback response</td></tr><tr><td>Power / efficiency</td><td>Low Tx complexity</td><td>Low Tx complexity</td><td>Driver and EAM loss</td><td>Laser, driver, and MZM loss</td><td>Laser, heater, and lock power</td><td>Laser plus control overhead</td></tr><tr><td>Reliability</td><td>Junction and temperature wear</td><td>Facet and active-region wear</td><td>Laser plus EAM aging</td><td>Source, attach, and bias drift</td><td>Source, heater, and lock faults</td><td>Cavity, package, and lock faults</td></tr><tr><td>Manufacturing</td><td>Array-friendly, MMF plant</td><td>Simple Tx, SMF attach</td><td>Mature integrated Tx</td><td>Multi-die attach and RF match</td><td>Dense PIC, tight thermal control</td><td>Tight optical assembly and control</td></tr><tr><td>Evidence burden</td><td>Modal, temperature, aging</td><td>Chirp, LIV, RIN</td><td>LIV, RIN, EAM sweep, TDECQ</td><td>Source plus bias and RF path</td><td>Source plus resonance and crosstalk</td><td>Spectrum, lock, feedback, environment</td></tr></table>
**Table 7.1.** Decision matrix for common source and modulation paths. "Evidence burden" mixes characterization/ATP with life qualification; keep those jobs separate (Table 9.2, Chapter 9). Program limits come from Table 7.4.

### Reading the source and modulation matrix

Table 7.1 is a decision map, not a datasheet. Architecture order is plant and reach first, then modulation class, then the burdens those choices create (RIN/linewidth, power split, life owner, factory skill, validation cost), and only then the specific source part. Freeze fiber and rate from the product; strike paths that fail bandwidth or plant class; score survivors on the remaining rows; treat the evidence-burden row as the characterization, qualification, ATP, and FA cost you must fund. Fill Table 7.4 from the winning path and keep a one-line reject reason for each alternative. Later sections teach each path; do not let technology enthusiasm override a row that already vetoes the architecture.

## Directly modulated lasers and VCSELs

Before EMLs and silicon photonics took over single-mode datacenter ports, most volume optics were either a cheap *DML* on single-mode fiber or a *VCSEL* array into multimode fiber. Both still matter at the low-cost, short-reach edge of the market, and both show why chirp, modal bandwidth, and temperature push AI fabrics toward externally modulated single-mode sources.

A DML modulates laser bias current directly. The transmitter is simple and efficient, but the same carrier dynamics that make modulation easy also produce chirp: intensity changes drag the optical frequency along (§3.11). Over multimode or very short single-mode runs that is often acceptable. Over dispersive single-mode fiber at tens of GBd, the chirp turns into inter-symbol interference and closes the eye. Validation therefore focuses on extinction ratio, pattern-dependent chirp, and RIN, not just average power.

VCSELs took a different path. They emit from a vertical cavity at 850--940 nm straight into multimode fiber, so parallel arrays are easy to assemble and cheap to ship. That combination made VCSEL SR optics the default for early 40G/100G Ethernet inside the rack (100G-SR4 and its cousins): short ribbons of MMF, high lane count, low dollars per gigabit. The same physics that made them attractive also capped their future. Multimode fiber has modal bandwidth and modal noise limits; VCSEL bandwidth and reliability both degrade with temperature; and as lane rates climb toward 100 G and 200 G, those limits arrive sooner. The industry response has been incremental (better OM4/OM5 fiber, tighter specs, sometimes PAM4 on MMF) rather than a clean leap to 400G/lane SMF DR. In practice, MMF reach and modal dispersion keep VCSEL links in the SR box (§3.13), while hyperscale AI fabrics standardize on single-mode DR/FR and CPO.

Neither family is the path to 400G/lane SMF DR. EMLs and external modulators (§7.4, §3.14.3, Table 3.12) own that space. Pattern-aware chirp linearization can stretch a DML a little farther, but it does not change the physics at FR distances: if you need low chirp and high EO bandwidth at fleet scale, you leave direct modulation behind.

## DFB and EML: the workhorse transmitters

Once single-mode DR/FR became the hyperscale default, most short-reach ports started with an InP laser chip. Two configurations still dominate production: the CW or directly modulated DFB, and the EML that adds an electro-absorption modulator on the same die.

##### DFB.

A distributed-feedback laser has a grating along the active region that selects one longitudinal mode. Spec-sheet metrics that matter in bring-up are threshold current, slope efficiency, SMSR (typically many tens of dB on a clean part), RIN, and wavelength vs. temperature/current. Used as a CW source for SiPh or TFLN modulators, or as a DML when chirp is acceptable (§7.3). Uncooled datacom DFBs ride case temperature with a known $d\lambda/dT$; cooled parts add a TEC and lock to a grid.

##### EML.

An electro-absorption modulated laser integrates a DFB with an *EAM* on one chip (§3.14.3). Reverse bias on the EAM sets absorption and extinction; chirp stays far below a DML. That combination, not marketing, is why EMLs became the volume answer for 100G/lane and then 200G/lane DR/FR pluggables: one chip, low chirp, mature supply chain. Validation adds EAM bias sweeps, aging of the absorption curve, and driver-match checks on top of the DFB LIV/SMSR/RIN suite (§7.7, §7.13).

##### When to pick which.

Through 200G/lane DR, EML usually wins on cost and integration. A CW DFB (or ELSFP/CW-WDM bank) plus Si MZM, ring, or TFLN wins when the modulator must sit on silicon or needs $\gtrsim$100 GHz EO bandwidth (Table 3.12, §3.14.3). At CPO scale the laser often leaves the optical engine entirely so it can be replaced without pulling the ASIC package (§7.14). Looking forward, 400G/lane pluggables are pushing harder toward external CW plus TFLN or high-BW silicon modulators, while EMLs remain the workhorse of the installed 100--200G base.

<table class="book-table"><tr><th>Source</th><th>Typical use</th><th>Top risks</th></tr><tr><td>DML</td><td>short reach, cost-driven</td><td>chirp/dispersion, extinction ratio</td></tr><tr><td>EML</td><td>, 100--200G/lane</td><td>EAM bias/aging, thermal</td></tr><tr><td>CW + TFLN MZM</td><td>400G/lane FR/DR, NPO</td><td>MZM bias drift, fiber attach, driver match</td></tr><tr><td>CW + Si MZM</td><td>DR/FR SiPh, 100--400G/lane</td><td>driver match, bias drift, fiber coupling</td></tr><tr><td>CW + Si ring</td><td>CPO, WDM transceivers</td><td>wavelength lock, thermal crosstalk, coupling</td></tr><tr><td>VCSEL</td><td>SR over MMF</td><td>modal noise, reach, temperature</td></tr><tr><td>ELS / ELSFP</td><td>co-packaged optics</td><td>connectorization, fleet serviceability</td></tr></table>
**Table 7.2.** When each source is used, and its top validation risks.

Use Table 7.2 as a short risk card once the path is roughly known. Use Table 7.1 when you still need to compare attribute rows across paths. Do not treat this card as a substitute for the full matrix or for Table 7.4.

## Choosing the modulation path

The source decision and modulation decision must close together. Direct modulation minimizes parts and power but carries laser chirp into the link. An EML adds an EAM on the laser die and is a mature low-chirp path for 100--200G/lane. A silicon MZM uses more area and drive but gives a broad optical passband. A ring is compact and fits dense WDM, but adds resonance control and thermal-crosstalk tests. TFLN offers high bandwidth and low chirp with a separate material platform and assembly flow.

Table 7.1 compares the system consequences. The device operation, bandwidth, insertion loss, and driver interfaces live in §3.14.3, Table 3.12. Keep that physics in one place. Here the decision is whether the link can carry the added power, control, assembly, and validation burden.

## Laser requirements: from roadmap to specs

Laser requirements only work when they are numbers a supplier can fail and a link budget can close. Start from the interconnect roadmap choice, then fill a short requirements slice; the ATP checklist in Table G.2, Appendix G is how that slice is enforced on every lot.

##### Roadmap forks that set the laser.

Each architecture decision forces a different requirements set (Table 7.3):

<table class="book-table"><tr><th>Roadmap choice</th><th>Laser implication</th><th>Specs you must freeze early</th></tr><tr><td>Pluggable EML vs CW+Si/TFLN</td><td>Integrated EAM vs external CW + modulator</td><td>EAM bias/aging and TDECQ vs CW power class, RIN, and modulator V_ match</td></tr><tr><td>On-package laser vs ELSFP/CW-WDM</td><td>Field replace vs FIT inside the package</td><td>Connector/ORL/mate cycles and hot-swap CMIS vs COD/aging inside ASIC thermal</td></tr><tr><td>Isolator vs isolator-free (CPO)</td><td>Feedback tolerance vs quiet RIN only</td><td>Stressed RIN_xOMA at stated ORL; monitor PD / lock policy</td></tr><tr><td>Single- vs CW-WDM / comb</td><td>One line vs N lines into rings/filters</td><td>Per-line power flatness, SMSR, grid, crosstalk (sec:cwwdm-laser)</td></tr><tr><td>Retimed vs LPO</td><td>Module DSP hides Tx vs host sees raw eye</td><td>Laser+modulator TDECQ/RLM floor vs host COM budget (sec:com,sec:drivers)</td></tr><tr><td>Derate policy</td><td>Operating I, T, power below abs-max</td><td>Bias window, thermal class, FIT/E_a assumptions (sec:laser-aging)</td></tr></table>
**Table 7.3.** Architecture forks and the laser specs each one forces. Freeze these before DVT samples are built (Appendix G.16).

Each "Specs you must freeze early" cell is the exit criterion for that fork. **Exit when** every active fork has numbers (or explicit N/A) before DVT samples are built.

> **Tradeoff.** On-package laser vs field-replaceable ELS
>
> *Improves:* Integration density and fewer optical connectors
>
> *Worsens:* Package FIT, service downtime, and thermal risk next to the ASIC
>
> *When acceptable:* When laser FIT times link count exceeds the service model
>
> *Experienced decision:* Choose replaceability when fleet repair time dominates; choose on-package when connectors and mate cycles dominate.

##### One-page requirements slice.

Table 7.4 is the PRD-sized list. Fill every row with a number (or an explicit "N/A for this architecture") and a named evidence source before you negotiate production controls. Every requirement needs an owner; evidence may be engineering characterization, supplier data, qualification, incoming inspection, ATP, sampled audit, SPC, or fleet telemetry (Chapter 9). Do not leave RIN without an ORL, or power without a case-temperature class.

<table class="book-table"><tr><th>Parameter</th><th>How to set the number</th><th>Evidence / production control</th><th>Reject if</th><th>Derate / ops note</th></tr><tr><td>Launch power / class</td><td>Link budget + connector loss + aging margin (sec:link-budget)</td><td>Power meter; ATP or sample; ELSFP class</td><td>Below min at rated T</td><td>Cap max power for COD</td></tr><tr><td>Wavelength / grid</td><td>PMD or ring FSR plan; d/dT headroom (ch:wdm)</td><td>OSA / wavemeter; ATP or sample</td><td>Off-grid at case T</td><td>TEC setpoints</td></tr><tr><td>SMSR floor</td><td>Datasheet + modal-noise budget</td><td>OSA at source/subasm or sample</td><td>Below floor at T</td><td>Watch aging</td></tr><tr><td>RIN (quiet + stressed)</td><td>BER floor vs BW (sec:rin); ORL from plant</td><td>PD+ESA; stated ORL; sample / supplier</td><td>Above limit at ORL</td><td>Bias-driver noise budget (sec:laser-drivers)</td></tr><tr><td>Bias window</td><td>LIV kink-free range at max case T</td><td>LIV at die/subasm; module proxy</td><td>Kink in window</td><td>Run below abs-max I</td></tr><tr><td>EAM / MZM (if any)</td><td>ER, RLM, TDECQ at baud (sec:tdecq)</td><td>DCA + bias sweep; ATP proxy</td><td>TDECQ/RLM fail</td><td>Bias aging policy</td></tr><tr><td>ORL / isolator</td><td>Architecture: isolator-free needs tighter RIN</td><td>ORL meter; mate cycles</td><td>ORL out of range</td><td>Cleaning / ELS mate life</td></tr><tr><td>CMIS monitors</td><td>What fleet triage will read (sec:fleet-triage)</td><td>CMIS dump; ATP state check</td><td>Missing alarms / bad state machine</td><td>Enable sequence (sec:bringup)</td></tr><tr><td>Life / degradation</td><td>Fleet life and availability target (sec:fit-example)</td><td>Qual: mechanism stress, lots, confidence (ch:reliability); not ATP</td><td>Claim unsupported</td><td>Derating; supplier ECO; sampled audit; bias/headroom telemetry; burn-in only if infant pop.\ justified</td></tr></table>
**Table 7.4.** Laser requirements one-pager. Every cell needs a program number and an evidence owner; this table is the structure, not the limits. Life claims belong in qualification; ATP is only one possible production control.

> **Tradeoff.** Higher optical power vs lifetime
>
> *Improves:* Link margin and reach under loss and aging
>
> *Worsens:* Thermal stress, COD risk, wall-plug efficiency, and cooling load
>
> *When acceptable:* When power is the only remaining debit and the life model still closes at the new setpoint
>
> *Experienced decision:* Do not solve every BER problem with more launch. Often noise, alignment, DSP, or coupling is the cheaper fix.

##### How to fill numbers (method, not invention).

Work backward from the link, not forward from a marketing slide. The four steps below turn an architecture choice into requirements and control owners:

1.  Close the optical ledger at target pre-FEC BER (Appendix E.5, §3.12). That sets minimum launch OMA/power and maximum allowed penalties (transmitter and dispersion eye closure quaternary, TDECQ; ORL/RIN).

2.  From receiver BW and the RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ (§6.3), set a stressed RIN limit with margin under the plant ORL you will actually see (not only a quiet bench).

3.  From case-temperature and derating policy, set the LIV bias window and thermal class so the laser never sits on a kink or at abs-max in the fleet (§7.13, §9.11).

4.  From service model, choose ELSFP mate-cycle / hot-swap requirements or accept on-package life risk and write COD/aging controls accordingly (§7.14).

Hand the filled slice to the supplier with the production-control checklist (Table G.2, Chapter 9). If a roadmap slide cannot point to a row in Table 7.4, the requirement is not real yet.

**Exit when** every cell in Table 7.4 is a program number or explicit N/A, with ORL stated wherever RIN appears and case-$T$ class stated wherever power or bias appears. **Decision unlocked:** negotiate evidence and production controls, or reopen the architecture fork that left a cell empty.

**Key idea.** Laser leadership is a requirements sheet: architecture forks force specific specs (power, grid, RIN@ORL, SMSR, bias window, CMIS, life). Fill Table 7.4 from the link budget and fleet model, then assign each row an evidence source. ATP is only one possible control (Chapter 9, Appendix G.16).

## LIV, SMSR, and RIN: the measurement playbook

Three questions decide whether a laser chip or module is usable. Can it make enough power in a kink-free bias window at the thermal class you claim (LIV)? Is it single-mode enough for the plant and WDM grid (SMSR)? Is intensity noise quiet enough at the ORL you will actually see (RIN)? The instruments are standard; the skill is knowing which failure each answer catches, and which access plane can still see that answer.

##### Access ladder.

Match the measurement to the plane you can open:

Die or source subassembly

: Direct LIV, threshold and slope, SMSR, monitor-PD current, detailed wavelength and RIN.

Engineering module

: Selected internal nodes, source and modulator bias sweeps, direct thermal sensors, laboratory control substitution.

Closed production module

: External launch power, wavelength or spectrum where accessible, OMA and waveform proxies, product current, telemetry, BER, calibrated control-headroom proxies. Finished modules do not expose LIV merely because LIV mattered during source development.

Fleet

: Exposed telemetry, alarms, FEC and BER trends, temperature, and bias or actuator headroom where implemented.

Bench order when access allows: LIV $\to$ SMSR $\to$ wavelength $\to$ RIN (quiet, then stressed ORL) $\to$ EAM or bias-driver checks as the path requires. Stop when distributions across temperature and units support the bias window, grid, and RIN policy in Table 7.4. If RIN fails, bisect electrical versus optical before you blame the diode: quiet SMU / high ORL first, then product bias rails, then an ORL sweep. Rise with reflection is laser feedback; rise independent of ORL points at the electrical path; discrete ESA spurs are supply or clock pickup (§7.8, §6.3.1).

##### LIV (light--current--voltage).

The LIV curve plots optical power and forward voltage versus bias current. Read off threshold $I_\mathrm{th}$, slope efficiency (mW/mA above threshold), kink-free operating range, and thermal rollover at high current or high case temperature. §7.1 is a labeled schematic (not measured data).

High-temp LIV failures look like: $I_\mathrm{th}$ rise, slope collapse, early rollover, or a kink that moves into the bias window. Those map to aging, TEC saturation, or package thermal resistance (§7.13).

<figure id="fig:liv-sketch" data-latex-placement="ht">
<embed src="figures/fig_liv_sketch.pdf" style="width:85.0%" />
<figcaption>Schematic LIV curve with threshold, slope, kink, and thermal rollover labeled. Idealized for teaching; use measured LIV for pass/fail. <span id="fig:liv-sketch" data-label="fig:liv-sketch"></span></figcaption>
</figure>

##### SMSR (side-mode suppression ratio).

SMSR is the power difference (dB) between the lasing mode and the strongest side mode on an optical spectrum analyzer (OSA). Datacom single-mode parts require high SMSR so side modes do not steal power or seed modal noise. Spec-sheet floors are part-specific; treat the datasheet or ATP limit as authoritative. SMSR collapse under temperature or aging is a reject: the laser is leaving single-mode operation.

##### RIN (relative intensity noise).

Measure RIN with a calibrated photodetector and RF spectrum analyzer (or a dedicated RIN analyzer), under a controlled optical return loss. Distinguish *intrinsic* RIN (quiet bench, high ORL) from stressed $\mathrm{RIN}_x\mathrm{OMA}$ used in Ethernet/MSA specs. IEEE 802.3 / 100G Lambda class links cap $\mathrm{RIN}_{17.1}\mathrm{OMA}$ at $-136$ dB/Hz with 17.1 dB ORL . Quiet datacom DFB/EML parts typically sit well below that when feedback is controlled; CPO ELS designs care as much about feedback tolerance as about the quiet number (§6.3.1, §6.3).

<table class="book-table"><tr><th>Parameter</th><th>Instrument</th><th>Pass/fail intent</th><th>Failure signature</th></tr><tr><td>LIV</td><td>SMU + power meter / integrating sphere</td><td>I_th, slope, kink-free bias window</td><td>high-temp rollover; kink in bias range</td></tr><tr><td>SMSR</td><td>OSA</td><td>single-mode purity vs.\ datasheet/ATP</td><td>side modes rise with T or age</td></tr><tr><td>RIN</td><td>PD + ESA / RIN analyzer</td><td>intrinsic and stressed RIN_xOMA</td><td>RIN rises with ORL; BER floor (sec:rin)</td></tr><tr><td>Bias-driver noise</td><td>SMU vs.\ product bias board</td><td>RIN_eq from i_n (sec:laser-drivers)</td><td>RIN rises with rails on, flat vs.\ ORL</td></tr><tr><td>Wavelength</td><td>OSA / wavemeter</td><td>grid placement, d/dT, d/dI</td><td>walk off ring or MSA grid</td></tr><tr><td>EAM bias (EML)</td><td>bias sweep + DCA/TDECQ</td><td>extinction, chirp, RLM</td><td>aging shifts absorption curve</td></tr></table>
**Table 7.5.** Laser measurement playbook: what to measure, with what, and what failure looks like.

See also Table 7.10. Do not keep measuring for its own sake once those exits close.

##### Transmitter-quality metrics (what each does not prove).

Average power and RIN sit upstream of the modulated-signal metrics. Use Table 7.6 when average power passes but the eye or BER fails: each row localizes a different question, and none is a unique root cause.

<table class="book-table"><tr><th>Metric</th><th>What it describes</th><th>What it does not establish</th></tr><tr><td>Average power</td><td>Mean optical energy</td><td>Modulation quality or receiver margin</td></tr><tr><td>OMA</td><td>Optical modulation amplitude</td><td>Level linearity, jitter, or complete eye quality</td></tr><tr><td>Extinction ratio</td><td>Relative high and low optical levels</td><td>PAM level spacing or full waveform quality</td></tr><tr><td>RLM</td><td>PAM level linearity</td><td>Complete transmitter penalty</td></tr><tr><td>TDECQ (or Tx-quality metric)</td><td>Composite transmitter quality vs.\ a reference receiver</td><td>Unique physical root cause</td></tr><tr><td>BER waterfall</td><td>End-to-end margin behavior</td><td>Component ownership without isolation</td></tr></table>
**Table 7.6.** Transmitter-quality metrics: what each describes versus what it does not prove. TDECQ and RIN localize composite quality or noise, not a single mechanism.

## Laser drivers and the RIN budget

Modulator RF drivers (§3.14.3) deliver swing and bandwidth into an EAM or MZM. Laser *bias* drivers are a different circuit: they set a quiet constant current into the diode. Current noise on that path becomes optical intensity noise and adds in the RIN budget of §6.3. Confusing the two is a common debug miss: a great SiGe PAM4 driver can still ruin a CW laser if its supply or ground couples into the bias rail. The electrical-versus-optical bisection is in §7.7; use it before redesigning the diode.

*Reference: bias-driver noise numerics.* The conversion and table below are budget tools for quiet-CW sizing. Skip to path notes if you already have a measured product-board RIN.

##### From current noise to equivalent RIN.

Above threshold, optical power tracks bias approximately as $P\propto(I-I_\mathrm{th})$. Relative intensity fluctuations then track relative current fluctuations: $$\mathrm{RIN}_{\mathrm{eq,lin}}
\;\approx\;
\left(\frac{i_n}{I-I_\mathrm{th}}\right)^{\!2},
\qquad
\mathrm{RIN}_{\mathrm{eq}}[\mathrm{dB/Hz}]
\;=\;
20\log_{10}\!\left(\frac{i_n}{I-I_\mathrm{th}}\right),$$ where $i_n$ is the one-sided current-noise density in A$/\sqrt{\mathrm{Hz}}$ at the laser terminals (driver plus board pickup). The approximation assumes linear slope efficiency and ignores intrinsic laser dynamics; it is a budget tool, not a device model.

Worked numbers at $I-I_\mathrm{th}=50$ mA (typical CW DFB window): $i_n=500$ pA$/\sqrt{\mathrm{Hz}}$ maps to $\mathrm{RIN}_{\mathrm{eq}}\approx-160$ dB/Hz; $270$ pA$/\sqrt{\mathrm{Hz}}$ maps to about $-165$ dB/Hz. Commercial low-noise laser drivers quote roughly $50$--$500$ pA$/\sqrt{\mathrm{Hz}}$ at 1 kHz depending on current range (Table 7.7); the Koheron DRV200 family is a concrete example . Against a good datacom intrinsic RIN of $-145$ to $-155$ dB/Hz (§6.3.1), those 1 kHz densities look comfortable. The budget tightens when $(I-I_\mathrm{th})$ is small (near threshold, derated CW, or low-current VCSELs), when you integrate broadband switching noise rather than a 1 kHz spot, or when SerDes/DSP rails dump discrete tones onto the bias network.

<table class="book-table"><tr><th>Driver class (example)</th><th>i_n @ 1 kHz</th><th>RIN_eq @ 50 mA</th><th>What it means</th></tr><tr><td>Ultra-low-noise CW (DRV200-A-40)</td><td>55 pA/Hz</td><td>-179 dB/Hz</td><td>Bench / metrology floor</td></tr><tr><td>Low-noise CW (DRV200-A-200)</td><td>270 pA/Hz</td><td>-165 dB/Hz</td><td>Typical quiet CW source</td></tr><tr><td>Higher-current CW (DRV200-A-400)</td><td>480 pA/Hz</td><td>-160 dB/Hz</td><td>Still below -155 intrinsic</td></tr><tr><td>Shared digital LDO, poor PSRR</td><td>often 1 nA/Hz + tones</td><td>can exceed -145</td><td>False ``RIN'' on ESA</td></tr></table>
**Table 7.7.** Bias-driver current noise converted to equivalent RIN at $I-I_\mathrm{th}=50$ mA using $\mathrm{RIN}_{\mathrm{eq}}=20\log_{10}(i_n/(I-I_\mathrm{th}))$. Densities for the DRV200 rows are from the Koheron datasheet at 1 kHz; the last row is qualitative (board-dependent).

##### CW / ELSFP / CW-WDM paths.

For external CW sources feeding Si or TFLN modulators, design the bias path as a low-noise current source with high supply rejection, local decoupling at the diode, and a star ground that does not share return with SerDes switching currents. Automatic power control () loops that close through a monitor PD suppress slow drift; keep the loop bandwidth well below the RIN measurement band and quiet enough that the loop itself does not inject intensity noise. ELSFP and CW-WDM modules hide this circuitry inside the pluggable (§7.14, §7.16); acceptance still needs module-level RIN with the host bias and management rails connected, not only a quiet SMU on the bare die.

##### DML and EML.

A *DML* shares one diode for bias and RF: a bias tee (or on-chip bias network) combines a quiet DC source with the RF driver. Excess RF driver broadband noise, poor tee isolation, or supply ripple on the bias arm all raise measured RIN and chirp-related penalties. An *EML* splits the problem: keep the DFB bias as quiet as a CW source, and treat the EAM RF driver under §3.14.3. EAM drive amplitude sets extinction and chirp; DFB bias noise still lands in optical intensity before the modulator.

**Key idea.** Treat laser bias noise as a RIN term: $\mathrm{RIN}_{\mathrm{eq}}\approx(i_n/(I-I_\mathrm{th}))^2$. Quiet CW drivers at tens to hundreds of pA$/\sqrt{\mathrm{Hz}}$ usually sit under a $-145$ dB/Hz intrinsic floor at 50 mA; digital supply pickup, near-threshold bias, and DML bias-tee leakage are what actually burn the budget. A low current-noise density at one frequency (for example 1 kHz in Table 7.7) is not proof of a clean bias path across the receiver bandwidth; integrate broadband noise and check discrete tones. The table is illustrative, not a supplier recommendation.

## How lasers fail

Six mechanisms account for most laser field returns. Each has a distinct telemetry signature, so classify before you open FA.

Threshold current increase

: $I_\mathrm{th}$ rises from its ship value at fixed temperature, usually with slope efficiency dropping in step. Points to active-region or facet degradation (§7.13).

Slope efficiency degradation

: Output power per unit bias current falls even when $I_\mathrm{th}$ is stable. A separate wear-out track from threshold rise; both show up on the same LIV sweep.

Wavelength drift

: The lasing line walks off its grid slot or ring resonance. Distinguish laser drift from TEC or ring drift by holding one actuator fixed and moving the other (§8.4, Chapter 8).

Aging (SMSR collapse, mode hopping)

: Side modes grow relative to the main mode, or the laser hops between modes under temperature or current. An OSA trend over time is the tell.

Thermal runaway

: A positive feedback loop where higher junction temperature raises threshold current and cuts slope efficiency, so more drive power turns to heat for the same optical output, raising temperature further until the TEC saturates and the laser rolls over. Triggered by a failed or saturated TEC, a blocked heat path, or operation above the rated thermal class. Distinct from ordinary wear-out because it is fast (minutes, not months) once it starts; the failure-analysis handbook has the full symptom-to-cause breakdown (Appendix I.7).

Monitor photodiode failure

: The control loop's own sensor drifts or fails, so the laser looks unstable when the real fault is in the feedback path, not the gain medium (§7.20.3).

## Separate thermal behavior from long-term aging

Thermal response is reversible on the time scale of a temperature sweep or cycle. It changes threshold current, slope efficiency, wavelength, EAM bias, TEC current, and ring alignment. Measure it with controlled case-temperature sweeps, loaded thermal corners, heater sweeps, and thermal cycling. Repeat the measurement after returning to the starting temperature. Recovery points toward an operating-point or control problem.

Long-term aging is cumulative. Threshold current rises, slope efficiency falls, contacts degrade, defects grow, and an absorption or spectral curve can move permanently. Measure those changes with HTOL, accelerated life testing, and periodic LIV, spectrum, and modulation readouts. A temperature cycle can expose a weak attach or calibration error, but it does not by itself establish a lifetime acceleration model.

Do not merge the data sets. A high-temperature BER failure that clears at room temperature needs thermal-margin work. A room-temperature baseline that keeps moving after each stress interval needs an aging or damage hypothesis.

## Calibration: what drifts and what triggers retuning

Calibration corrects predictable unit-to-unit and temperature variation by storing operating points. It does not repair exhausted margin. A railed TEC, heater, or bias DAC, a permanently walked LIV or absorption curve, or a loop error that no longer converges is a design, life, or FA problem, not a "retune the table" task.

Calibration exists because no transmitter runs at a datasheet point. Every unit has its own threshold, slope, absorption curve, quadrature point, and resonance, and each of those moves with temperature and age. The operating points a product actually stores are:

Laser bias / APC target

: the bias current or monitor-PD power setpoint that holds launch power. Drifts as threshold rises and slope falls with age (§7.13); a drifting monitor PD corrupts it silently (§7.20.3).

EAM bias (EML)

: the reverse-bias point that sets extinction and chirp. Moves with case temperature and with absorption-curve aging, so production parts store bias versus temperature, not one number.

MZM quadrature

: the phase bias that holds the modulator at its linear point. Drifts with temperature, stress, and age; a bias-control loop tracks it, and a railed loop is a telemetry alarm, not a retune request.

Ring heater / lock point

: the tuner power that aligns resonance to the laser line. Consumes headroom as ambient rises and neighbors heat; a railed DAC means the tuning range is exhausted (§8.4, §8.5).

Tables are usually segmented by temperature. Segment boundaries are a real failure mode: the debug story in §7.20.4 is a healthy laser reading the wrong temperature segment after thermal cycling. Keep calibration tables under change control and record the table version with every test result, or failures cannot be replayed.

Recalibration should be triggered by evidence, not habit: a control-loop error residual that no longer converges, an actuator (TEC, heater, bias DAC) that approaches its rail, telemetry that disagrees with an external reference, a temperature excursion beyond the table range, or a repair, rework, or firmware change that invalidates stored coefficients. Repeated recalibration can mask physical drift: if coefficients keep walking, treat that as an aging, attach, monitor, or control problem, not a permanent fix. ATP must verify calibration at the temperature corners the fleet will see, not only at the station ambient (§9.11, Chapter 9).

## How lasers are qualified

Qualification supports a bounded life or degradation claim when the stress accelerates a credible field mechanism, the sample population is representative, observables and failure criteria are predefined, and the acceleration model and uncertainty are justified (Chapter 9, Appendix F.1.1). Three stress classes do most of the work:

HTOL (high-temperature operating life)

: Biased high-temperature exposure on representative samples; track LIV, SMSR, and wavelength drift for selected powered degradation mechanisms. Use Arrhenius only when the mechanism is temperature-activated in the assumed regime.

Burn-in

: An optional production screen for a demonstrated infant-mortality population. Burn-in trades test time for escape rate; it does not replace life qualification (Appendix G.14, Chapter 9).

Environmental stress

: Temperature cycling, damp heat, vibration, and shock catch packaging, attach, moisture, and mechanical risks that HTOL does not. They qualify different mechanisms and are not substitutes for powered-aging evidence (Appendix F.1.1).

Do not treat HTOL hours plus an Arrhenius factor as an automatic FIT proof. State the supported claim, sample-hours, lot diversity, and remaining risk.

##### Observable aging signatures.

Watch LIV and spectrum over HTOL or field life:

- threshold rise and slope drop (active-region / facet degradation);

- SMSR collapse (mode competition);

- EAM bias creep on EMLs (absorption curve shift $\to$ TDECQ/RLM drift);

- RIN rise under feedback (ORL or isolator failure);

- COD (catastrophic optical damage) at the facet under overstress.

Each signature needs an evidence owner in qualification, production control, or fleet telemetry (§10.10, Appendix F.1.1, Chapter 9).

## Aging curves, derating, and fleet FIT

Lasers wear out. At fleet scale that is not a footnote; it sets architecture (ELSFP vs. integrated laser) and operating policy (derating, burn-in).

> **Tradeoff.** FIT claim vs sample humility
>
> *Improves:* A crisp fleet failure-rate story for planning
>
> *Worsens:* Overconfidence when sample-hours, lots, and sites are thin
>
> *When acceptable:* When the bound, observation time, and population are stated with the claim
>
> *Experienced decision:* Publish an upper bound with assumptions, or do not claim a FIT number.

##### Arrhenius life projection.

Telcordia GR-468-CORE qualifies optoelectronic parts with accelerated stress (HTOL, temperature cycle, damp heat) and projects field life with Arrhenius acceleration : $$\mathrm{AF}
= \exp\!\left[\frac{E_a}{k_B}\left(\frac{1}{T_\mathrm{use}}-\frac{1}{T_\mathrm{stress}}\right)\right],$$ where $E_a$ is the activation energy for the wear-out mechanism under test, $k_B$ is Boltzmann's constant, and temperatures are absolute. Document $E_a$, sample size, and confidence bounds when converting a 1000-hour HTOL lot into field-year FIT. Activation energies are mechanism-specific; use the value justified in the qual plan, not a generic number copied from another product.

<figure id="fig:accelerated-aging" data-latex-placement="ht">
<embed src="figures/fig_accelerated_aging.pdf" style="width:92.0%" />
<figcaption>Schematic accelerated aging for gradual laser wear-out. A degradation parameter (for example optical power at fixed bias, or threshold current rise mapped to a falling health metric) is tracked versus time at several stress temperatures <span class="math inline"><em>T</em><sub>1</sub> &lt; <em>T</em><sub>2</sub> &lt; <em>T</em><sub>3</sub> &lt; <em>T</em><sub>4</sub></span>. Higher temperature reaches the failure threshold sooner. The dashed curve on the threshold plane is the time-to-failure trend that Arrhenius acceleration turns into a use-condition life estimate. Not measured data. Valid only for one thermally activated mechanism with junction temperature as the stress variable; sudden modes such as COD or ESD do not draw this surface. <span id="fig:accelerated-aging" data-label="fig:accelerated-aging"></span></figcaption>
</figure>

§7.2 is the mental model behind HTOL: same starting health, faster drift at higher temperature, a defined end-of-life threshold, and shorter time-to-failure as stress rises. For lasers the vertical axis is usually tied to LIV or power at constant current; the temperature axis must be junction temperature, not only chamber set point.

##### When the projection is valid.

Acceleration assumes the stress speeds up the *same* physical mechanism the fleet will see. The projection fails in two ways: the stress activates a mechanism the field never sees (solder creep or moisture ingress at a stress temperature the product never reaches), or the field sees a mechanism the stress never exercises (connector wear, bias-rail transients, thermal cycling from traffic load). So a qual number is a hypothesis, not a fact: compare field-return Pareto and failure signatures against the qual projection, and treat divergence as evidence that $E_a$ or the mechanism model is wrong, not that the fleet is unlucky (§10.10). Sudden fails (COD, ESD, cracked fiber attach) sit outside §7.2; classify those separately before you fit Arrhenius parameters.

##### Derating.

Run below absolute-max current, case temperature, and optical power. Derating extends wear-out life and reduces COD risk. Uncooled datacom parts already sit near thermal limits at high case temperature; cooled or faceplate ELSFP modules (§7.14) buy headroom by moving heat off the ASIC package.

##### Worked FIT example (assumptions labeled).

FIT is failures per $10^9$ device-hours. For illustration only, assume 50 FIT per laser (confirm against your supplier qual; do not treat 50 as a measured claim) and a fabric with $5\times10^5$ lasers (order-of-magnitude for a large AI cluster with several optical links per accelerator). Expected failures per day: $$\frac{5\times10^5 \times 50 \times 24}{10^9}
\approx 0.6\ \text{laser failures/day}.$$ That is why field-replaceable ELSFP modules, burn-in screens, and derating are design inputs, not afterthoughts (Chapter 9).

## ELS and ELSFP: architecture, pinout, qual

*ELSFP* (External Laser Small Form-Factor Pluggable) is the OIF form factor for faceplate-pluggable CW laser modules that feed co-packaged optical engines . The lasers sit at the coolest part of the system (front panel), hot-swap when they fail, and keep thermal load off the ASIC and photonic engine.

##### Mechanical and optical.

The module uses a card-edge electrical interface and a blind-mate multi-fiber optical connector at the rear (MT-class ferrules), which improves eye safety for high CW power by keeping live fiber inside the chassis . One ELSFP can feed more than one optical engine. OIF defines optical power classes, thermal classes, and wavelength assignments (e.g. DR-type 1311 nm and FR-type CWDM4 grids) so hosts and modules interoperate.

##### Management and hot-swap.

ELSFP uses CMIS and the CMIS module state machine over TWI. On plug-in the module resets, initializes management, and stays in low-power mode with lasers *off* until the host transitions it to ModuleReady and explicitly enables lasers . `ModPrsL` and `IntL` support presence detect and asynchronous alarms for safe hot-swap.

##### Reference: electrical pinout (OIF-ELSFP-02.0 Table 7).

extitDeep dive / pin map. Skip unless you are wiring the host connector. Twenty-four contacts: multiple 3.3 V VCC and GND pins, module reset (`ResetL`), low-power mode (`LPModeL`), two-wire serial management (`SCL`/`SDA`), presence (`ModPrsL`), and interrupt (`IntL`), plus reserved pins for future power/ground . Table 7.8 summarizes the published map.

<table class="book-table"><tr><th>Pin</th><th>Function</th><th>Requirements</th><th>Notes</th></tr><tr><td>1--3</td><td>VCC</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>4</td><td>TBD</td><td>reserved</td><td>future power</td></tr><tr><td>5</td><td>ResetL</td><td>pull-up 10 k</td><td>reset module, LVTTL</td></tr><tr><td>6</td><td>LPModeL</td><td>MMC on only</td><td>low-power mode (low), LVTTL</td></tr><tr><td>7</td><td>TBD</td><td>reserved</td><td>future ground</td></tr><tr><td>8--10</td><td>GND</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>11</td><td>TBD</td><td>reserved</td><td>(reserved)</td></tr><tr><td>12</td><td>SCL</td><td>TWI clock</td><td>host 4.7 k pull-up; module 10 k</td></tr><tr><td>13</td><td>SDA</td><td>TWI data</td><td>same pull-ups as SCL</td></tr><tr><td>14</td><td>TBD</td><td>reserved</td><td>(reserved)</td></tr><tr><td>15--17</td><td>GND</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>18</td><td>TBD</td><td>reserved</td><td>future ground</td></tr><tr><td>19</td><td>ModPrsL</td><td>shorted to GND in module</td><td>presence (low), LVTTL</td></tr><tr><td>20</td><td>IntL</td><td>pull-up 10 k</td><td>interrupt, LVTTL</td></tr><tr><td>21</td><td>TBD</td><td>reserved</td><td>future power</td></tr><tr><td>22--24</td><td>VCC</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr></table>
**Table 7.8.** ELSFP electrical pinout (adapted from OIF-ELSFP-02.0 Table 7). Lasers power only in ModuleReady after host command; default on plug-in is lasers off .

##### Qual hooks for suppliers.

Acceptance test plans should cover the checklist in Table G.2, Appendix G: laser LIV/SMSR/RIN inside the module; optical power-class compliance; connector mating cycles and contamination/ORL; burn-in before ship; CMIS register sanity; and thermal class at rated case temperature. Module bring-up must also prove the CMIS enable sequence and ModuleReady laser policy (§9.11). Field returns split between laser wear-out and connector/fiber-attach faults; keep both in the triage tree (§10.10).

## Optical safety and laser classes

*Reference / compliance deep dive.* Read when you own APR/ALS ATP or multi-fiber hazard classification. Architecture chapters only need the rule that aggregate port power, not per-lane datasheet power, sets the class.

### Hazard and laser classes

Laser safety for interconnects is governed by IEC 60825-1 (laser product classification) and IEC 60825-2 (optical-fiber communication systems, OFCS) . Classes run from Class 1 (safe under normal use) through Class 1M (safe unless the beam is collected by optics), Class 3R/3B, and Class 4. At 1310 nm and 1550 nm the beam is invisible, which raises the operational risk: technicians cannot see exposure. The retinal-hazard band ends near 1400 nm, but corneal and skin hazards remain, and single-mode power confined to a $\sim$9 μm core is high radiance even at modest milliwatt levels.

Short-reach datacom modules are usually engineered so each fiber port stays Class 1 or Class 1M under rated launch power. That is a design constraint on EML/DFB bias and on how much power each lane launches, not a label you add after the fact.

### Hazard level = aggregate, not per-lane

The safety case scales with *total* launched power at an accessible location, not with a single DFB data sheet. CW-WDM and ELS banks concentrate many lines on one MT or MPO ferrule (§7.14). A connector that breaks out eight or sixteen fibers can exceed a per-lane Class 1 budget even when each lane is modest. IEC 60825-2 assigns hazard levels (1 through 4) to each accessible port in the OFCS based on the radiant power that could escape during service . That is why ELS architecture and fiber count drive classification, not the laser chip alone.

### Open-fiber protection: APR and ALS

When fiber continuity is lost, open connectors and broken fiber can expose hazardous power. *APR* (automatic power reduction) holds output at or below Hazard Level 1M and probes for re-mate with safe low-power pulses. *ALS* (automatic laser shutdown) cuts power entirely and was common on older SDH links; for modern high-power systems APR with automatic restart is the preferred pattern because restart probes stay within the hazard limit . ITU-T G.664 requires power reduction to Hazard Level 1M within about 3 s of a continuity break, a restart inhibit window, and restart only at safe power.

These mechanisms tie directly to CMIS and bring-up policy: lasers enable only when the host commands ModuleReady (§9.11, Appendix E.7). APR/ALS is what makes a live ELSFP hot-swap survivable in a running rack (§9.11).

### What validation and ops owe

Optical safety is a validation deliverable, not a compliance sticker. ATP should verify APR/ALS trip threshold and timing on representative open-fiber faults; label modules and cages with the rated class; document max launched power per port and per MPO breakout; and write service procedures for multi-fiber connectors. At fleet scale, a hot-swap runbook that assumes ALS works but was never tested in ATP is a real hazard. Fold the APR/ALS check into the ELS hot-swap corner in §9.11 alongside mate-cycle and ORL tests.

## CW-WDM source validation

*Reference: multi-wavelength source survey.* Architecture contract for CW-WDM locking lives in Chapter 8; this section lists per-channel acceptance checks and example products.

Multi-wavelength CW sources (CW-WDM MSA) feed dense ring or filter banks on a PIC (§8.6, Chapter 8). Validation is per-channel plus cross-channel:

- power flatness across $\lambda$ (uneven OMA after the modulator bank);

- per-channel SMSR and wavelength grid placement;

- channel crosstalk and residual ASE between lines;

- lock to microring resonances under temperature and neighbor heating (§8.4, §8.5, §3.14.3);

- RIN and ORL sensitivity for each line (§7.7, §6.3.1).

Examples: Ayar Labs SuperNova (CW-WDM MSA-compliant, feeds TeraPHY)  ; Broadcom ELSFP banks on Tomahawk CPO (Appendix H.10, §7.14); quantum-dot comb lasers (Ranovus, Quintessent) aimed at many $\lambda$ from one chip. Source tests live here; locking and on-chip MUX live in Chapter 8.

## Light-source supply strategy

The sourcing decision follows the same architecture fork as the optical design: buy a merchant source, buy a serviceable external module, or bind the source to the photonic package. Evaluate each path by qualification ownership, second-source portability, lot traceability, test access, field replacement, and change-control rights. A vendor list ages quickly and does not answer those questions.

Merchant DFB, EML, or CW die

: preserve module-level design freedom and can support a second source, but the integrator owns attach, driver match, screening, and package reliability.

External CW-WDM or ELSFP module

: moves source qualification and management into a replaceable unit. The system still owns connector, ORL, hot-swap, and host interoperability (§7.14, §7.16).

Multi-wavelength source

: reduces source count and can simplify WDM fan-out, but couples channel yield, power flatness, control, and replacement into one unit (§7.16).

Source integrated with the PIC

: reduces optical interfaces and can improve density, but makes laser yield and wear-out part of package yield and service life.

<table class="book-table"><tr><th>Approach</th><th>Qualification ownership and risk</th></tr><tr><td>Merchant DFB/EML/CW die</td><td>Integrator owns attach, driver match, screen, and module qual</td></tr><tr><td>External CW-WDM / ELSFP module</td><td>Supplier owns source module; system owns interface and service qual</td></tr><tr><td>Multi-wavelength source</td><td>Shared yield, power-flatness, and replacement risk across channels</td></tr><tr><td>Source integrated with PIC</td><td>Highest density; laser yield and life become package risks</td></tr></table>
**Table 7.9.** Light-source sourcing paths and the qualification ownership each one creates.

### Reading the supplier ownership matrix

Table 7.9 is a qualification-ownership map. Choose the service model before you freeze optics. A merchant die leaves attach, driver match, screen, and package life with the integrator. An ELS or CW-WDM module moves source life into a replaceable unit while mate, ORL, hot-swap, and host interop stay system-owned. A multi-wavelength source couples channel yield, flatness, and replacement. An integrated PIC source makes laser yield and wear-out part of package life. Approve a path only when both ownership packs exist; do not treat a die cert as module qual, or a laser-module ATP as an optical-interface qual.

### Why ownership order matters

Choose the service and ownership model before you freeze the optical architecture. Qualify the architecture you will service, not only the laser die.

## Why lasers can be a reliability bottleneck

The laser can be an important reliability-limiting component because it is an active optical device with temperature- and bias-dependent degradation. The dominant fleet mechanism remains architecture-specific: connectors, electronics, packaging, cooling, control loops, and software may dominate another design (Chapter 9, Chapter 10).

Laser-specific mechanisms that still need a plan include:

- *Catastrophic optical damage* (COD) at the facet.

- Gradual facet and active-region degradation (accelerated by temperature when Arrhenius applies; §7.13).

- EAM aging in EMLs; coupling and solder drift in packaged assemblies.

Because failures scale with the number of lasers, a fleet of $100{,}000$+ links can turn a modest per-laser FIT rate into a steady stream of field failures (§7.13, Appendix F.1.1). Mitigations shape architecture: field-replaceable external laser sources (ELSFP, CW-WDM), redundancy, burn-in when a demonstrated infant-mortality population justifies it, and derating.

## Margin erosion over temperature, lot, and life

A link rarely loses all margin in one event. The source can lose launch power as slope efficiency falls. Connector loss and ORL can rise after service. EAM or MZM bias can move. A ring can consume spectral headroom as its heater approaches range. Driver noise can raise the BER floor while none of these changes violates its stand-alone limit.

Track five ownership ledgers. They are tools for deciding which measurement to run next, not five additive dB terms that always sum to a scalar budget:

Power margin

: launch power, coupling, connector and MUX loss, receiver sensitivity, and aging reserve.

Noise margin

: intrinsic and feedback-driven RIN, bias-rail noise, receiver noise, and crosstalk.

Timing margin

: source and modulator bandwidth, dispersion, driver and host jitter, and equalization reserve.

Spectral margin

: laser wavelength, SMSR, filter or ring passband, thermal drift, and lock range.

Control margin

: headroom in APC, TEC, heaters, ring lock, bias DACs, and calibration tables. A railed loop can fail the link while the diode is still healthy. Calibration corrects predictable variation; it does not restore exhausted physical or control margin (§7.11).

Recompute the link at combined production corners. A nominal part at nominal temperature says little about whether a slow loss in two ledgers will push a tail unit across the pre-FEC BER limit. A composite external measurement (TDECQ, BER waterfall) may already include several internal penalties; do not subtract the same impairment again in the system budget (Appendix E.5). §9.11, Table I.1 carry the same ledgers into validation and fleet triage. The interview review compresses this checklist in Appendix A.8.4. The wall-chart form is Appendix D.10.

> **Why experienced engineers track five ledgers instead of one margin number?**
>
> Because links usually fail when several small spends add up. One room-temperature pass/fail hides which ledger is nearly empty.

> **Engineering heuristic.** A railed heater, TEC, or bias DAC is often the failure before the diode is. Check control margin before you write a wear-out FIT story.

> **Tradeoff.** More optical margin vs cost and power
>
> *Improves:* Reach, temperature tolerance, aging headroom, and contamination tolerance
>
> *Worsens:* Laser power, thermal load, wall-plug efficiency, and sometimes component lifetime
>
> *When acceptable:* When a named uncertainty (aging, ORL, lot spread) still dominates the remaining risk
>
> *Experienced decision:* Do not maximize margin. Allocate margin where uncertainty is highest. A predictable 1 dB connector loss often needs less attention than an unknown aging mechanism.

<pre class="dectree" aria-label="Nominal system margin"><code>Nominal system margin
  |
Temperature debit
  |
Voltage / power-quality debit
  |
Channel / connector debit
  |
Manufacturing variation
  |
Aging / wear
  |
Interoperability variation
  |
Remaining margin
  |
Above deployment requirement?
  |-- YES --&gt; proceed
  |-- NO  --&gt; redesign / restrict / recalibrate / reject</code></pre>
Not every debit is naturally in decibels. Depending on the subsystem, remaining margin may be optical power, sensitivity, BER or FEC headroom, eye or TDECQ, jitter, control range, lifetime, or yield. Validation often measures the net externally visible result; do not double-count internal penalties the test cannot separate (Appendix E.5).

## Engineering lens

### How it works

A laser is an active device with wear-out physics, so it is both the first line of the link budget and often an important reliability risk. The dominant fleet mechanism remains architecture-specific (§7.9, Chapter 9). The chapter's transmitter paths and LIV/SMSR/RIN measurements all serve one question: will this source stay in spec for years at temperature?

### How it is measured

Qualify the laser as a set of curves across temperature, bias, ORL, and age, not a room-temperature data-sheet point. The measurement playbook (LIV, SMSR, RIN, wavelength, and EAM checks with their instruments and pass/fail intent) is in §7.7, Table 7.5; the stress classes that project field life are in §7.12, §7.13, Appendix F.1.1 .

### How it fails

The six field-return mechanisms are catalogued in §7.9: threshold rise, slope droop, wavelength drift, aging (SMSR collapse and mode hopping), thermal runaway, and monitor-photodiode failure. Manufacturing adds die, wafer, lot, and assembly spread to every one. The mechanism that most often misleads triage is a healthy laser behind a bad feedback sensor, so it gets the worked callout below.

\> \*\*Failure mode: Monitor photodiode drift\*\* \> \> \*\*Symptoms.\*\* Reported power falls or the bias loop moves, but an external power meter does not show the same change. \> \> \*\*Likely causes.\*\* Monitor-PD responsivity drift, transimpedance gain error, contamination in the monitor path, or a bad calibration coefficient. \> \> \*\*Measurements.\*\* External power meter, monitor current, bias current, LIV, and loop error versus temperature. \> \> \*\*Mitigations.\*\* Repair the monitor path or calibration, add disagreement alarms, and do not raise laser bias to compensate for a false reading.

### How it is debugged

For power degradation, compare external optical power, monitor current, bias, and case temperature before changing the setpoint. Rerun LIV at the failing temperature and compare it with ship data. If LIV moved, inspect SMSR, wavelength, and RIN to classify active-region, facet, or modal change. If LIV is stable, move to coupling, connector, monitor-PD, and control-loop checks. For a wavelength excursion, inspect OSA data and TEC current together. For a bias anomaly, replace the product driver with a quiet source before blaming the diode.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* BER worsened after thermal cycling while average optical power stayed in range. \> \> \*\*Investigation.\*\* The DCA showed that extinction ratio had collapsed. LIV and SMSR were unchanged, and an EAM bias sweep restored the eye. \> \> \*\*Finding.\*\* The light source was healthy, but its modulator operating point was wrong. \> \> \*\*Root cause.\*\* A calibration table used the wrong temperature segment after the cycle. \> \> \*\*Resolution.\*\* The table and screening limits were fixed, and EAM bias sweep data became part of the thermal-cycle readout.

## Engineering checklist

<table class="book-table"><tr><th>Decision or test</th><th>Question it answers</th><th>Evidence to retain</th><th></th></tr><tr><td>Architecture</td><td>Does the source and modulation path close reach, rate, power, cost, and service?</td><td>Requirement allocation and rejected alternatives</td><td></td></tr><tr><td>LIV</td><td>Is the operating window clear of threshold, kinks, and rollover?</td><td>Curves by unit, lot, temperature, and age</td><td></td></tr><tr><td>Spectrum</td><td>Does wavelength and SMSR stay inside the assigned grid and filter passband?</td><td>OSA or wavemeter data across corners</td><td></td></tr><tr><td>RIN and ORL</td><td>Does noise margin survive the reflection environment?</td><td>Quiet and stressed RIN with stated ORL and bandwidth</td><td></td></tr><tr><td>Modulation</td><td>Does bias, drive, chirp, and bandwidth close the eye?</td><td>Bias sweeps, TDECQ or equivalent, and driver conditions</td><td></td></tr><tr><td>Thermal behavior</td><td>Are reversible shifts within control and actuator range?</td><td>Temperature and heater sweeps, TEC current, recovery data</td><td></td></tr><tr><td>Long-term aging</td><td>Which parameters drift permanently, and at what rate?</td><td>HTOL intervals, LIV, spectrum, and modulation trends</td><td></td></tr><tr><td>Manufacturing</td><td>Can the ATP catch bad units and lot drift at useful test cost?</td><td>Limits, guard bands, GR\</td><td>R, yield, and reaction plan</td></tr><tr><td>Fleet operation</td><td>Which monitors distinguish source, modulator, cooler, and optical path?</td><td>Telemetry map, alarm thresholds, and golden baselines</td><td></td></tr></table>
**Table 7.10.** Source and modulation engineering checklist. Each row ties a decision to evidence, not only a test name.

### Reading the laser engineering checklist

Table 7.10 is the decision sequence for a laser program. Measurement methods for LIV, SMSR, RIN, and aging are taught earlier in this chapter; the notes below focus on what each row unlocks and when you may leave it.

##### Architecture.

**Purpose.** Does the source and modulation path close reach, rate, power, cost, and service?

**Uncertainty removed.** Component enthusiasm does not allocate requirements. After architecture you have a chosen path, rejected alternatives, and owners for lock, attach, and life (Table 7.1, Table 7.9).

**Exit criteria.** **Exit when** requirement allocation and rejected alternatives are written and reviewed.

**Decision unlocked.** Freeze the path into Table 7.4, or reopen the matrix.

**Risk if skipped.** You validate a hero topology that cannot be serviced or powered in the rack.

##### LIV.

**Purpose.** Is the operating window clear of threshold, kinks, and rollover across unit, lot, temperature, and age (§7.7)?

**Exit criteria.** **Exit when** kink-free bias windows and distributions support the bias policy.

**Decision unlocked.** Set bias and derate, or reject lots / redesign the window.

**Risk if skipped.** Soft BER and sudden dark fails appear without a ship baseline to compare.

##### Spectrum.

**Purpose.** Do wavelength and SMSR stay inside the assigned grid and filter passband?

**Exit criteria.** **Exit when** OSA or wavemeter data across corners meet grid and SMSR floors.

**Decision unlocked.** Approve channel assignment, tighten temperature policy, or reject modal risk.

**Risk if skipped.** WDM unlock and modal noise show up as "random" BER.

##### RIN and ORL.

**Purpose.** Does noise margin survive the reflection environment the plant will present (§6.3.1)?

**Exit criteria.** **Exit when** quiet and stressed RIN at stated ORL and bandwidth meet the BER-floor budget.

**Decision unlocked.** Approve isolator-free or isolator-required design; set plant cleaning rules.

**Risk if skipped.** Lab RIN looks fine; field ORL raises the floor.

##### Modulation.

**Purpose.** Do bias, drive, chirp, and bandwidth close the eye at baud?

**Exit criteria.** **Exit when** bias sweeps and TDECQ (or equivalent) at named driver conditions meet Tx quality limits (Appendix E.3).

**Decision unlocked.** Freeze EAM/MZM/ring bias policy, or reject the modulator class for this rate.

**Risk if skipped.** Average power passes while the eye fails under temperature.

##### Thermal behavior.

**Purpose.** Are reversible shifts within control and actuator range?

**Exit criteria.** **Exit when** temperature and heater sweeps, TEC current, and recovery data show control headroom at loaded corners.

**Decision unlocked.** Approve thermal envelope, add heaters/TEC margin, or derate case $T$.

**Risk if skipped.** Lock and calibration faults are misread as permanent aging.

##### Long-term aging.

**Purpose.** Which parameters drift permanently, and at what rate (§7.13)?

**Exit criteria.** **Exit when** HTOL intervals with LIV, spectrum, and modulation trends support the life claim or force derate.

**Decision unlocked.** Accept FIT/replacement plan, or hold ship for life risk.

**Risk if skipped.** Useful-life planning uses hope instead of a mechanism.

##### Manufacturing.

**Purpose.** Can the ATP catch bad units and lot drift at useful test cost (Table G.2)?

**Exit criteria.** **Exit when** limits, guardbands, GR&R, yield, and a reaction plan exist for the ship screens.

**Decision unlocked.** Open volume screens, or hold for process control.

**Risk if skipped.** Qualified engineering lots diverge from production without a catch point.

##### Fleet operation.

**Purpose.** Which monitors distinguish source, modulator, cooler, and optical path (§10.10)?

**Exit criteria.** **Exit when** telemetry map, alarm thresholds, and golden baselines are named and owned.

**Decision unlocked.** Arm fleet triage; feed escapes back into ATP.

**Risk if skipped.** Field tickets cannot separate laser wear from connector or TEC faults.

### Why the checklist order matters

Architecture first, or you characterize the wrong path. LIV and spectrum establish semiconductor and channel health before RIN and modulation argue about floors and eyes. Thermal separates reversible control from permanent drift before aging claims. Manufacturing and fleet close the loop so life and screens stay honest after ship. Later rows must not compensate for a missing architecture or ship baseline.

## Interview takeaway

**Key idea.** Measure LIV, SMSR, wavelength, and RIN as distributions across temperature, lot, and age. Tie each requirement to a named evidence source (characterization, supplier data, qualification, ATP, sample audit, SPC, or fleet telemetry), each life claim to a physical mechanism, and each field alarm to a measurement that separates the laser from its driver, monitor, cooler, and optical path. Not every requirement is an every-unit ATP line (Table 7.4, Chapter 9).

Junior mistake: declare wear-out from monitor telemetry alone, or raise launch power before naming which ledger spent (§7.19, Chapter 8, Chapter 9).

### Interview Q&A: Choosing Light Sources and Modulation

Practice speaking these answers aloud. Prefer first-person reasoning over definitions. Detail lives earlier in this chapter (§7.1, Table 7.1, §7.7, §7.19). Score your answer using the chapter-end spoken-answer rubric (Appendix A.12.1).

##### Question 1. How do you choose a light source and modulation architecture for a new optical link?

*Tests:* requirement flow-down and architecture selection.

*Spoken answer.* "I would start with the system rather than the laser datasheet. I need the lane rate, modulation format, reach, fiber plant, wavelength plan, link-loss and reflection environment, power budget, thermal class, cost, manufacturing volume, lifetime, and service model. Those requirements eliminate paths that cannot close the physics, for example modal bandwidth, chirp and dispersion, electro-optic bandwidth, or wavelength-lock range. I would then compare the surviving paths on wall-plug power, driver burden, coupling, control complexity, manufacturing capability, qualification, and field replacement. The output is a selected architecture with rejected alternatives and the measurements needed to close its highest-risk assumptions."

*Pressure follow-up.* "The customer says to use the lowest-cost laser. What do you do?"\
*Answer pivot.* "I would translate lowest cost into total product and fleet cost. A cheaper source can require more DSP, tighter fiber limits, greater cooling, lower manufacturing yield, or more field replacements."

*Trap:* comparing output power, bandwidth, and price across datasheets and choosing the best part.

##### Question 2. Compare VCSEL, DML, EML, and silicon photonics.

*Tests:* correct taxonomy and system-level comparison.

*Spoken answer.* "I would first correct the taxonomy. A VCSEL is a laser family commonly used with direct modulation and multimode fiber. DML describes direct modulation of a laser, often a DFB, so it is partly an operating architecture rather than one unique device structure. An EML integrates a laser, normally a DFB, with an electro-absorption modulator. Silicon photonics is not itself a laser family; it is a photonic integration platform that commonly uses a separate continuous-wave III-V source feeding a silicon MZM or ring modulator. I compare the complete transmitter paths on fiber type, reach, chirp, bandwidth, coupling, thermal control, power, manufacturing, reliability, and serviceability" (Table 7.1).

*Pressure follow-up.* "Is an EML a silicon-photonics transmitter?"\
*Answer pivot.* "A conventional datacom EML is usually a III-V laser and EAM integrated together. A silicon-photonics module normally uses a separate or heterogeneously integrated source with a silicon modulator, so the ownership and control architecture are different."

*Trap:* calling VCSEL, DML, EML, and silicon photonics four competing laser technologies.

##### Question 3. When would you use direct modulation rather than an EML, MZM, or ring?

*Tests:* chirp, bandwidth, reach, power, and complexity tradeoffs.

*Spoken answer.* "Direct modulation is attractive when the required rate and reach close with its bandwidth and chirp because it minimizes components, optical insertion loss, and control loops. The limitation is that changing carrier density changes both intensity and optical frequency, so chirp interacts with fiber dispersion and can close the eye. An EML separates most modulation from laser generation while retaining an integrated transmitter. An MZM offers a broad optical passband and low-chirp operation but adds driver swing, optical loss, area, and bias control. A ring is compact and WDM-friendly but adds resonance alignment and thermal crosstalk. I would change architectures when the direct path no longer closes the required eye and margin across fiber, temperature, lot, and age" (Chapter 8).

*Pressure follow-up.* "A DML passes back-to-back but fails after the specified fiber. What is your leading hypothesis?"\
*Answer pivot.* "Chirp interacting with dispersion becomes a leading hypothesis, but I would verify it through fiber-length, wavelength, and bias sweeps and compare the eye or BER behavior, not simply declare the DML unsuitable."

*Trap:* preferring direct modulation whenever it is cheaper and consumes less laser power.

##### Question 4. What does an LIV curve tell you, and how would you choose the laser operating window?

*Tests:* threshold, slope efficiency, rollover, kinks, and derating.

*Spoken answer.* "An LIV measurement gives optical power and voltage versus current. From it I extract threshold current, slope efficiency, electrical behavior, kink-free range, and thermal rollover. I measure distributions across units, lots, temperature, and relevant aging intervals rather than choosing one room-temperature curve. The operating window must remain far enough above threshold for modulation and noise performance, but below kinks, rollover, absolute maximum stress, and any lifetime or thermal limit. I also preserve control headroom because an APC loop can maintain launch power by increasing bias while the underlying threshold or slope is degrading" (§7.7, §7.11).

*Pressure follow-up.* "Launch power remains constant, but laser bias rises steadily. What can you conclude?"\
*Answer pivot.* "The control loop is consuming headroom, but the mechanism is not yet known. I would compare external power, monitor-photodiode response, threshold, slope efficiency, coupling, temperature, and calibration before calling it laser aging."

*Trap:* setting the laser at the current that produces the highest optical power without exceeding the absolute maximum.

##### Question 5. Average optical power passes, but BER or TDECQ fails. How do you debug it?

*Tests:* power versus modulated-signal quality.

*Spoken answer.* "Average power only tells me average launched energy. I would also inspect OMA, extinction ratio, level linearity, waveform quality, bandwidth, jitter, overshoot, and the applicable transmitter-quality metric such as TDECQ. For an EML I would sweep EAM bias and drive. For an MZM I would inspect quadrature bias and RF drive. For a ring I would inspect resonance alignment and control headroom. I would also check source RIN, reflections, and receiver behavior. A bad TDECQ localizes the problem toward composite transmitter quality, but it does not by itself identify whether the cause is laser noise, modulator bias, driver bandwidth, reflections, or calibration" (Table 7.6).

*Pressure follow-up.* "Would increasing launch power solve the problem?"\
*Answer pivot.* "Only if receiver power margin is the actual limiting ledger. More launch power does not repair distorted levels, bandwidth loss, chirp, jitter, a BER floor, or an incorrect modulator operating point."

*Trap:* increasing laser bias until BER clears when average power already passes.

##### Question 6. Explain how RIN, optical return loss, and laser-driver noise can produce a BER floor.

*Tests:* signal-dependent noise and measurement conditions.

*Spoken answer.* "RIN is relative optical-intensity noise, so its electrical noise contribution grows with received optical power and receiver bandwidth. Reflections can feed light back into the laser and change its effective noise or spectral behavior, which is why a quiet-bench RIN number may not represent the deployed fiber plant. Laser-bias current noise can also appear as optical intensity noise and may be mistaken for intrinsic laser RIN. I would measure quiet and reflection-stressed RIN under a stated bias, optical return loss, and bandwidth, inspect the BER waterfall, and substitute a quiet bias source or controlled optical path to separate the laser, driver, and reflection hypotheses" (§7.8, §6.3).

*Pressure follow-up.* "The laser has excellent RIN on the supplier bench but produces a field BER floor. What do you check?"\
*Answer pivot.* "I would reproduce the deployed ORL, connector plant, bias board, rail activity, and receiver bandwidth. The supplier's quiet number does not clear feedback sensitivity or product-level current noise."

*Trap:* claiming datasheet RIN below the limit means RIN cannot explain the field failure.

##### Question 7. How do you separate reversible thermal behavior from long-term aging?

*Tests:* recovery, control headroom, and permanent drift.

*Spoken answer.* "I measure the same parameters at the same reference condition before and after the thermal exposure. Reversible movement in threshold, slope, wavelength, EAM bias, MZM bias, ring heater code, TEC current, or BER that recovers after returning to the starting condition points toward operating-point or control-margin behavior. A baseline that remains shifted suggests aging, damage, or a calibration change. I also inspect whether an actuator is approaching its rail, because the control system can fail before the laser itself. A high-temperature failure is not automatically evidence of wear-out; it may simply show that the supported thermal envelope does not close" (§7.11, §7.12).

*Pressure follow-up.* "The unit fully recovers at room temperature but fails at its specified maximum case temperature. Does it pass?"\
*Answer pivot.* "No. The result may be reversible, but it is still a validation failure if that temperature is inside the required operating envelope."

*Trap:* treating any high-temperature degradation as accelerated laser aging.

##### Question 8. One optical lane degrades while its sibling lanes remain healthy. What does that tell you?

*Tests:* local versus shared mechanisms.

*Spoken answer.* "One weak lane raises local hypotheses such as its source or modulator, driver or TIA channel, fiber-array alignment, one MUX path, local thermal gradient, or lane-specific calibration. I would compare per-lane launch power, OMA, wavelength, TDECQ, BER, FEC timing, bias and control headroom, and temperature. I would then remap an electrical lane or use controlled channel swaps where supported to see whether the symptom follows the electrical channel or optical path. If all lanes move together, shared rails, a common thermal environment, firmware, cooling, or a shared source become more likely, but lane correlation is evidence, not mechanism confirmation."

*Pressure follow-up.* "The failure follows the module after a host-port swap. Is the laser confirmed bad?"\
*Answer pivot.* "No. The swap localizes the problem toward the module, but the module still contains the source, modulation, coupling, filtering, controls, firmware, and optical interfaces."

*Trap:* one weak lane proves that one laser die is defective.

##### Question 9. How do you evaluate source health when the laser is inaccessible inside a closed module?

*Tests:* access-aware observables and proxy limits.

*Spoken answer.* "On an engineering-access source or subassembly I may directly measure LIV, monitor-photodiode current, spectrum, SMSR, wavelength, RIN, and modulator-bias sweeps. In a closed module I may have only launch power, OMA, wavelength telemetry, module current, temperature, bias or control headroom, BER, transmitter-quality metrics, and supplier characterization. I would use the strongest validated proxies and narrow the conclusion accordingly. I would not claim active-region degradation solely from module power telemetry. Where possible, I correlate closed-module proxies with direct source measurements during development so fleet telemetry has an interpretable baseline" (§7.7).

*Pressure follow-up.* "CMIS reports falling power, but a calibrated external meter is stable. Which measurement do you trust?"\
*Answer pivot.* "For delivered optical power at the named external reference plane, the calibrated external meter is the stronger evidence. The disagreement raises a monitor-photodiode, telemetry, gain, or calibration hypothesis."

*Trap:* treating the module's internal monitor as always the most accurate measurement because it is closest to the laser.

##### Question 10. How would you choose between an integrated laser and a field-replaceable external laser source?

*Tests:* density, serviceability, ownership, and system reliability.

*Spoken answer.* "An integrated source reduces optical interfaces and can improve density, coupling, and packaging simplicity, but its yield, thermal exposure, and wear-out become part of the optical-engine or switch-package life. A field-replaceable external source can reduce replacement blast radius and improve serviceability, but it adds connectors, return-loss exposure, mate-cycle limits, fiber routing, hot-swap control, safety behavior, and another interoperability boundary. I would compare component failure rates together with population size, detection, redundancy, replacement time, connector reliability, thermal environment, and operational access. The correct decision comes from system availability and service policy, not source FIT alone" (§7.14, Chapter 9).

*Pressure follow-up.* "Does moving the laser into an ELS automatically improve reliability?"\
*Answer pivot.* "It can improve serviceability and isolate source replacement, but it introduces interface and operational risks. The architecture must qualify both the source module and the optical, management, hot-swap, and safety interfaces."

*Trap:* claiming an external laser is always more reliable because it operates farther from the hot ASIC.

##### Question 11. How would you qualify a second laser or transmitter supplier?

*Tests:* equivalence, distributions, mechanisms, and production control.

*Spoken answer.* "I would begin with the system requirements rather than asking the second source to copy the first supplier's nominal values. I would compare representative lots and sites across LIV distributions, wavelength and SMSR, quiet and stressed RIN, modulation behavior where applicable, thermal response, control headroom, aging evidence, package interaction, and closed-module performance. I would verify measurement correlation between supplier, engineering, and production stations and evaluate whether ATP or upstream controls detect the relevant variation. I also need supplier change control and genealogy. Meeting a datasheet does not establish identical tails, failure mechanisms, calibration behavior, or system margin" (Table 7.4, Chapter 9, Appendix G.16).

*Pressure follow-up.* "The replacement supplier meets every written laser specification. Is that sufficient?"\
*Answer pivot.* "Only if the written requirements capture the system-relevant conditions and the supplier's distributions and package interactions remain inside the allocated margin. Nominal specification compliance alone is not an interoperability or life argument."

*Trap:* approving the source after a few room-temperature parts match averages.

##### Question 12. Give me a 60-second source-and-modulation recommendation for a new high-speed short-reach link.

*Tests:* complete architecture answer under time pressure.

*Spoken answer.* "I would first freeze lane rate, reach, fiber type, wavelength plan, loss and ORL environment, power, thermal class, volume, lifetime, and service model. Then I would eliminate paths that fail the physics: VCSEL and multimode paths if modal reach is insufficient, direct modulation if chirp and bandwidth do not close, and resonant or multi-die paths if the available thermal control or manufacturing cannot support them. Among the survivors I would compare an integrated EML with continuous-wave source plus MZM or ring on total power, transmitter quality, coupling, calibration, reliability, production yield, and serviceability. I would close the choice with temperature and lot distributions, BER waterfalls, waveform quality, stressed RIN, control headroom, and life evidence."

*Pressure follow-up.* "What would make you change the architecture late in development?"\
*Answer pivot.* "A physics or margin failure that cannot be economically controlled, such as dispersion-limited direct modulation, exhausted thermal-lock range, unacceptable reflection sensitivity, weak manufacturing capability, or a service model that cannot tolerate the source placement."

*Trap:* picking the newest high-bandwidth source technology and validating it over the required reach.

Score each response using the shared chapter-interview rubric in Appendix A.12.1. Repeat any answer that does not state the system requirement, compare viable architecture paths, identify the dominant impairment, and name the evidence that changes the decision.


<div class="nav-links">
  <a href="ch6-quantitative-models-noise-rin-and-ber">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch8-wdm-and-wavelength-locked-lasers">Next &rarr;</a>
</div>
