---
layout: default
title: "Ch 5: Choosing light sources and modulation"
---

# 5 Choosing light sources and modulation

Do not choose a laser by comparing data sheets in isolation. Start with reach, lane rate, fiber plant, power, cost, lifetime, manufacturing volume, and service policy. Those requirements select an architecture. The architecture then limits the useful source, modulation, detector, packaging, and validation choices.

## System requirements and architecture paths

Freeze the system problem before asking a supplier for samples:

<pre class="dectree" aria-label="Reach / fiber plant"><code>Reach / fiber plant
  |
Lane rate / bandwidth
  |
Laser choice
  |
Modulator path
  |
Receiver / detector
  |
Validation / qual burden (ATP, lock, thermal, life)</code></pre>
Reach and fiber

: decide whether multimode loss and modal bandwidth are acceptable or whether the link needs single-mode fiber.

Lane rate and bandwidth

: decide whether direct modulation closes the eye or whether the link needs an EML, MZM, or ring.

Power and cooling

: include laser wall-plug power, modulator loss, driver power, TEC power, and control overhead.

Cost and volume

: include fiber plant, assembly alignment, burn-in, test time, yield, and field replacement, not only die price.

Reliability and service

: decide whether the source can stay inside the package or must be a replaceable ELSFP.

The choices are coupled. A cost-driven, short multimode link points toward an 850 nm VCSEL, multimode fiber, silicon photodiodes, and direct modulation. A longer single-mode path points toward a 1310 nm DFB or EML and germanium or III-V detection. Dense WDM and co-packaged optics often move the CW source away from the modulator, which adds wavelength control, fiber attach, and service requirements. laser-reqs, Table laser-req-fork turns these paths into supplier specifications.

## Light-source and modulation choices

The short-reach market uses a small set of source families. Each fits a different constraint set:

DFB (distributed feedback)

: a grating along the active region gives single-mode output; the workhorse continuous-wave (CW) or directly modulated source for CWDM and LAN-WDM (dfb-eml).

DBR (distributed Bragg reflector)

: the grating sits outside the gain region. Choose it when tunability or separate control of gain and wavelength is worth added control and qualification work.

External-cavity laser

: a gain element and an external wavelength-selective cavity provide narrow linewidth and tunability. Choose it when spectral purity or lock range matters more than package size, cost, and control-loop simplicity. Most short-reach IM/DD links do not need it ; the cited product is vendor orientation, not a datacenter source recommendation.

DML (directly modulated laser)

: modulate the bias current directly: cheap and low-power, but chirp-limited over dispersive fiber (dml-vcsel).

EML (externally modulated laser)

: *EML*: a DFB integrated with an *EAM*. Low chirp and high bandwidth make it the dominant 100--200G/lane transmitter for single-mode links at DR (500 m) and shorter (dfb-eml, eml-eam).

CW laser + TFLN MZM

: an external CW source feeds a thin-film lithium niobate Mach--Zehnder modulator on a separate chip. Very low chirp and $\gtrsim$100 GHz EO bandwidth make this the leading path to 400G/lane pluggables and high-baud FR links; see tfln-mzm, Table tx-modulator.

CW laser + Si MZM

: an external CW source feeds a silicon Mach--Zehnder modulator on the same PIC (simzm). Low chirp, flat passband, and CMOS fab integration make this the default for 100--200G/lane DR/FR SiPh modules; 400G/lane demos appeared in 2026.

CW laser + Si ring

: same laser architecture, but a microring or microdisk modulator on the PIC (siring). Smaller footprint and strong WDM/CPO fit; wavelength lock and thermal crosstalk dominate validation (Ch. wdm).

CW-WDM / multi-wavelength sources

: high-power, multi-wavelength CW lasers (per the CW-WDM MSA) that feed comb-like WDM architectures (cwwdm-laser, cwwdm).

VCSEL

: 850--940 nm multimode sources for short-reach links over multimode fiber; cheap but reach-limited and less relevant at 200G/lane.

External laser source (ELS/ELSFP)

: a pluggable laser module supplying CW light to a co-packaged switch, so a failed laser is field-replaceable (elsfp).

<table class="book-table"><tr><th>Attribute</th><th>VCSEL direct</th><th>DFB direct</th><th>DFB + EAM</th><th>CW DFB/DBR + MZM</th><th>CW DFB/DBR + ring</th><th>External cavity + modulator</th></tr><tr><td>Wavelength / fiber</td><td>850--940 nm / MMF</td><td>1310 nm / SMF</td><td>1310 nm / SMF</td><td>1310 or 1550 nm / SMF</td><td>WDM grid / SMF</td><td>Tunable grid / SMF</td></tr><tr><td>Modulation fit</td><td>Direct only</td><td>Direct</td><td>Integrated EML</td><td>Si or TFLN MZM</td><td>Resonant Si ring</td><td>External MZM or ring</td></tr><tr><td>Bandwidth / reach</td><td>Short, modal limit</td><td>Chirp-limited</td><td>High BW, low chirp</td><td>High BW, broad passband</td><td>High BW, lock-limited</td><td>High BW, architecture-specific</td></tr><tr><td>RIN / linewidth</td><td>RIN and modal noise</td><td>RIN and chirp</td><td>RIN plus EAM bias</td><td>RIN; linewidth usually secondary</td><td>RIN plus spectral alignment</td><td>Low linewidth; verify feedback response</td></tr><tr><td>Power / efficiency</td><td>Low Tx complexity</td><td>Low Tx complexity</td><td>Driver and EAM loss</td><td>Laser, driver, and MZM loss</td><td>Laser, heater, and lock power</td><td>Laser plus control overhead</td></tr><tr><td>Reliability</td><td>Junction and temperature wear</td><td>Facet and active-region wear</td><td>Laser plus EAM aging</td><td>Source, attach, and bias drift</td><td>Source, heater, and lock faults</td><td>Cavity, package, and lock faults</td></tr><tr><td>Manufacturing</td><td>Array-friendly, MMF plant</td><td>Simple Tx, SMF attach</td><td>Mature integrated Tx</td><td>Multi-die attach and RF match</td><td>Dense PIC, tight thermal control</td><td>Tight optical assembly and control</td></tr><tr><td>Evidence burden</td><td>Modal, temperature, aging</td><td>Chirp, LIV, RIN</td><td>LIV, RIN, EAM sweep, TDECQ</td><td>Source plus bias and RF path</td><td>Source plus resonance and crosstalk</td><td>Spectrum, lock, feedback, environment</td></tr></table>
**Table ?.** Decision matrix for common source and modulation paths. "Evidence burden" mixes characterization/ATP with life qualification; keep those jobs separate (Table ladder, Ch. reliability). Program limits come from Table laser-prd.

### Reading the source and modulation matrix

Table source-mod-matrix is a decision map across paths, not a datasheet. Read it by *attribute row*: each row asks one engineering question that every path must answer. Family detail for VCSEL, DML, EML, MZM, and rings follows in later sections; use this matrix to see which questions become hard before you commit.

##### Wavelength / fiber.

**Purpose.** Which wavelength band and fiber type does the path assume?

**Uncertainty removed.** Reach, plant, and WDM grid are not free variables after this choice. MMF at 850--940 nm and SMF at 1310/1550 nm pull different connectors, modal limits, and lock burdens.

**Decision unlocked.** Accept the plant class, or reject a path that cannot meet the fiber and grid requirement.

**Risk if skipped.** You pick a modulator before you know whether the link is MMF short-reach or SMF WDM.

##### Modulation fit.

**Purpose.** Is the path direct modulation, integrated EAM, external MZM, or resonant ring?

**Uncertainty removed.** Driver, chirp, and lock problems change with the modulator class. Direct paths buy simplicity and pay chirp or modal limits; external paths buy bandwidth and pay attach and control.

**Decision unlocked.** Allocate driver, bias, and control ownership for the chosen modulator class.

##### Bandwidth / reach.

**Purpose.** Can the path close the baud and reach without a physics veto?

**Uncertainty removed.** Modal bandwidth, chirp, or lock range may kill a path before cost discussions matter.

**Decision unlocked.** Keep the path, derate reach/rate, or move to a higher-BW class (for example EML or MZM over DML).

##### RIN / linewidth.

**Purpose.** Which noise and spectral purity limits dominate the BER floor and WDM fit?

**Uncertainty removed.** Isolator-free and reflection-rich plants harden RIN. Rings and WDM harden spectral alignment. External cavities often win linewidth but still need feedback checks.

**Decision unlocked.** Set RIN@ORL and SMSR/linewidth requirements in Table laser-prd.

##### Power / efficiency.

**Purpose.** Where does wall-plug and optical power go: laser only, or laser plus driver, EAM/MZM loss, heaters, and lock?

**Uncertainty removed.** "Efficient laser" claims fail if heater and lock power dominate the module budget.

**Decision unlocked.** Accept the power split, or reject a dense path that breaks the rack power envelope.

##### Reliability.

**Purpose.** Which wear-out and fault classes own life: junction, facet, EAM, attach, heater, or lock?

**Uncertainty removed.** Life models and FA paths differ by class (wearout-modes). An integrated source makes laser yield a package risk; an ELS makes the optical interface a service risk.

**Decision unlocked.** Name the life owner and the screens (HTOL, EAM age, mate cycles) before NPI.

##### Manufacturing.

**Purpose.** What assembly and plant skills does the path demand?

**Uncertainty removed.** Array MMF plants, SMF attach, multi-die RF match, and dense PIC thermal control are different factories. Path choice is also a supplier-capability choice.

**Decision unlocked.** Pick a path the supply chain can screen, or fund the missing process.

##### Validation burden.

**Purpose.** Which measurements become mandatory because of the path?

**Uncertainty removed.** VCSEL needs modal and temperature work. EML needs LIV, RIN, EAM sweep, and TDECQ. Rings need resonance, crosstalk, and lock. External cavities need spectrum, lock, and feedback.

**Decision unlocked.** Size the ATP and DVT matrix to the path; do not copy another product's checklist blindly.

### How to use the matrix

1.  Freeze wavelength/fiber and reach/rate from the product requirements.

2.  Strike paths that fail bandwidth/reach or plant class.

3.  Among survivors, score RIN/linewidth, power, reliability, and manufacturing against your constraints.

4.  Read the validation-burden row as a cost: every hard cell is an ATP and FA investment you must fund.

5.  Fill Table laser-prd from the winning path; reject alternatives with a one-line reason retained for review.

Later sections teach each family. Do not let family enthusiasm override a row that already vetoes the path.

### Learning summary

Wavelength / fiber

: Plant and grid first.

Modulation / BW

: Physics veto before cost.

RIN / power / reliability

: The ledgers that usually decide.

Manufacturing / validation

: Can you build and screen it repeatedly?

## Directly modulated lasers and VCSELs

Before EMLs and silicon photonics took over single-mode datacenter ports, most volume optics were either a cheap *DML* on single-mode fiber or a *VCSEL* array into multimode fiber. Both still matter at the low-cost, short-reach edge of the market, and both show why chirp, modal bandwidth, and temperature push AI fabrics toward externally modulated single-mode sources.

A DML modulates laser bias current directly. The transmitter is simple and efficient, but the same carrier dynamics that make modulation easy also produce chirp: intensity changes drag the optical frequency along (chirp-dispersion). Over multimode or very short single-mode runs that is often acceptable. Over dispersive single-mode fiber at tens of GBd, the chirp turns into inter-symbol interference and closes the eye. Validation therefore focuses on extinction ratio, pattern-dependent chirp, and RIN, not just average power.

VCSELs took a different path. They emit from a vertical cavity at 850--940 nm straight into multimode fiber, so parallel arrays are easy to assemble and cheap to ship. That combination made VCSEL SR optics the default for early 40G/100G Ethernet inside the rack (100G-SR4 and its cousins): short ribbons of MMF, high lane count, low dollars per gigabit. The same physics that made them attractive also capped their future. Multimode fiber has modal bandwidth and modal noise limits; VCSEL bandwidth and reliability both degrade with temperature; and as lane rates climb toward 100 G and 200 G, those limits arrive sooner. The industry response has been incremental (better OM4/OM5 fiber, tighter specs, sometimes PAM4 on MMF) rather than a clean leap to 400G/lane SMF DR. In practice, MMF reach and modal dispersion keep VCSEL links in the SR box (pmd-reach), while hyperscale AI fabrics standardize on single-mode DR/FR and CPO.

Neither family is the path to 400G/lane SMF DR. EMLs and external modulators (dfb-eml, simzm, Table tx-modulator) own that space. Pattern-aware chirp linearization can stretch a DML a little farther, but it does not change the physics at FR distances: if you need low chirp and high EO bandwidth at fleet scale, you leave direct modulation behind.

## DFB and EML: the workhorse transmitters

Once single-mode DR/FR became the hyperscale default, most short-reach ports started with an InP laser chip. Two configurations still dominate production: the CW or directly modulated DFB, and the EML that adds an electro-absorption modulator on the same die.

##### DFB.

A distributed-feedback laser has a grating along the active region that selects one longitudinal mode. Spec-sheet metrics that matter in bring-up are threshold current, slope efficiency, SMSR (typically many tens of dB on a clean part), RIN, and wavelength vs. temperature/current. Used as a CW source for SiPh or TFLN modulators, or as a DML when chirp is acceptable (dml-vcsel). Uncooled datacom DFBs ride case temperature with a known $d\lambda/dT$; cooled parts add a TEC and lock to a grid.

##### EML.

An electro-absorption modulated laser integrates a DFB with an *EAM* on one chip (eml-eam). Reverse bias on the EAM sets absorption and extinction; chirp stays far below a DML. That combination, not marketing, is why EMLs became the volume answer for 100G/lane and then 200G/lane DR/FR pluggables: one chip, low chirp, mature supply chain. Validation adds EAM bias sweeps, aging of the absorption curve, and driver-match checks on top of the DFB LIV/SMSR/RIN suite (laser-params, laser-aging).

##### When to pick which.

Through 200G/lane DR, EML usually wins on cost and integration. A CW DFB (or ELSFP/CW-WDM bank) plus Si MZM, ring, or TFLN wins when the modulator must sit on silicon or needs $\gtrsim$100 GHz EO bandwidth (Table tx-modulator, simzm, siring, tfln-mzm). At CPO scale the laser often leaves the optical engine entirely so it can be replaced without pulling the ASIC package (elsfp). Looking forward, 400G/lane pluggables are pushing harder toward external CW plus TFLN or high-BW silicon modulators, while EMLs remain the workhorse of the installed 100--200G base.

<table class="book-table"><tr><th>Source</th><th>Typical use</th><th>Top risks</th></tr><tr><td>DML</td><td>short reach, cost-driven</td><td>chirp/dispersion, extinction ratio</td></tr><tr><td>EML</td><td>, 100--200G/lane</td><td>EAM bias/aging, thermal</td></tr><tr><td>CW + TFLN MZM</td><td>400G/lane FR/DR, NPO</td><td>MZM bias drift, fiber attach, driver match</td></tr><tr><td>CW + Si MZM</td><td>DR/FR SiPh, 100--400G/lane</td><td>driver match, bias drift, fiber coupling</td></tr><tr><td>CW + Si ring</td><td>CPO, WDM transceivers</td><td>wavelength lock, thermal crosstalk, coupling</td></tr><tr><td>VCSEL</td><td>SR over MMF</td><td>modal noise, reach, temperature</td></tr><tr><td>ELS / ELSFP</td><td>co-packaged optics</td><td>connectorization, fleet serviceability</td></tr></table>
**Table ?.** When each source is used, and its top validation risks.

Use Table laser-choice as a short risk card once the path is roughly known. Use Table source-mod-matrix when you still need to compare attribute rows across paths. Do not treat this card as a substitute for the full matrix or for Table laser-prd.

## Choosing the modulation path

The source decision and modulation decision must close together. Direct modulation minimizes parts and power but carries laser chirp into the link. An EML adds an EAM on the laser die and is a mature low-chirp path for 100--200G/lane. A silicon MZM uses more area and drive but gives a broad optical passband. A ring is compact and fits dense WDM, but adds resonance control and thermal-crosstalk tests. TFLN offers high bandwidth and low chirp with a separate material platform and assembly flow.

Table source-mod-matrix compares the system consequences. The device operation, bandwidth, insertion loss, and driver interfaces live in eml-eam, simzm, siring, tfln-mzm, Table tx-modulator. Keep that physics in one place. Here the decision is whether the link can carry the added power, control, assembly, and validation burden.

## Laser requirements: from roadmap to specs

Laser requirements only work when they are numbers a supplier can fail and a link budget can close. Start from the interconnect roadmap choice, then fill a short requirements slice; the ATP in supplier-exec is how that slice is enforced on every lot.

##### Roadmap forks that set the laser.

Each architecture decision forces a different requirements set (Table laser-req-fork):

<table class="book-table"><tr><th>Roadmap choice</th><th>Laser implication</th><th>Specs you must freeze early</th></tr><tr><td>Pluggable EML vs CW+Si/TFLN</td><td>Integrated EAM vs external CW + modulator</td><td>EAM bias/aging and TDECQ vs CW power class, RIN, and modulator V_ match</td></tr><tr><td>On-package laser vs ELSFP/CW-WDM</td><td>Field replace vs FIT inside the package</td><td>Connector/ORL/mate cycles and hot-swap CMIS vs COD/aging inside ASIC thermal</td></tr><tr><td>Isolator vs isolator-free (CPO)</td><td>Feedback tolerance vs quiet RIN only</td><td>Stressed RIN_xOMA at stated ORL; monitor PD / lock policy</td></tr><tr><td>Single- vs CW-WDM / comb</td><td>One line vs N lines into rings/filters</td><td>Per-line power flatness, SMSR, grid, crosstalk (sec:cwwdm-laser)</td></tr><tr><td>Retimed vs LPO</td><td>Module DSP hides Tx vs host sees raw eye</td><td>Laser+modulator TDECQ/RLM floor vs host COM budget (sec:com,sec:drivers)</td></tr><tr><td>Derate policy</td><td>Operating I, T, power below abs-max</td><td>Bias window, thermal class, FIT/E_a assumptions (sec:laser-aging)</td></tr></table>
**Table ?.** Architecture forks and the laser specs each one forces. Freeze these before DVT samples are built (supplier-exec).

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

Table laser-prd is the PRD-sized list. Fill every row with a number (or an explicit "N/A for this architecture") before you negotiate ATP limits. Do not leave RIN without an ORL, or power without a case-temperature class.

<table class="book-table"><tr><th>Parameter</th><th>How to set the number</th><th>Measure / ATP</th><th>Reject if</th><th>Derate / ops note</th></tr><tr><td>Launch power / class</td><td>Link budget + connector loss + aging margin (sec:link-budget)</td><td>Power meter; ELSFP class</td><td>Below min at rated T</td><td>Cap max power for COD</td></tr><tr><td>Wavelength / grid</td><td>PMD or ring FSR plan; d/dT headroom (ch:wdm)</td><td>OSA / wavemeter</td><td>Off-grid at case T</td><td>TEC setpoints</td></tr><tr><td>SMSR floor</td><td>Datasheet + modal-noise budget</td><td>OSA</td><td>Below floor at T</td><td>Watch aging</td></tr><tr><td>RIN (quiet + stressed)</td><td>BER floor vs BW (sec:rin); ORL from plant</td><td>PD+ESA; stated ORL</td><td>Above limit at ORL</td><td>Bias-driver noise budget (sec:laser-drivers)</td></tr><tr><td>Bias window</td><td>LIV kink-free range at max case T</td><td>LIV</td><td>Kink in window</td><td>Run below abs-max I</td></tr><tr><td>EAM / MZM (if any)</td><td>ER, RLM, TDECQ at baud (sec:tdecq)</td><td>DCA + bias sweep</td><td>TDECQ/RLM fail</td><td>Bias aging policy</td></tr><tr><td>ORL / isolator</td><td>Architecture: isolator-free needs tighter RIN</td><td>ORL meter; mate cycles</td><td>ORL out of range</td><td>Cleaning / ELS mate life</td></tr><tr><td>CMIS monitors</td><td>What fleet triage will read (sec:fleet-triage)</td><td>CMIS dump</td><td>Missing alarms / bad state machine</td><td>Enable sequence (sec:bringup)</td></tr><tr><td>FIT / life</td><td>Fleet failures/day target (sec:fit-example)</td><td>GR-468 + E_a</td><td>Screen escape</td><td>Burn-in depth; ELS replace</td></tr></table>
**Table ?.** Laser requirements one-pager. Every cell needs a program number; this table is the structure, not the limits.

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

Work backward from the link, not forward from a marketing slide. The four steps below turn an architecture choice into ATP limits:

1.  Close the optical ledger at target pre-FEC BER (link-budget, kp4). That sets minimum launch OMA/power and maximum allowed penalties (transmitter and dispersion eye closure quaternary, TDECQ; ORL/RIN).

2.  From receiver BW and the RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ (rin), set a stressed RIN limit with margin under the plant ORL you will actually see (not only a quiet bench).

3.  From case-temperature and derating policy, set the LIV bias window and thermal class so the laser never sits on a kink or at abs-max in the fleet (laser-aging, prod-corners).

4.  From service model, choose ELSFP mate-cycle / hot-swap requirements or accept on-package FIT and write COD/aging screens accordingly (elsfp).

Hand the filled slice to the supplier with the ATP checklist (Table atp-laser). If a roadmap slide cannot point to a row in Table laser-prd, the requirement is not real yet.

**Exit when** every cell in Table laser-prd is a program number or explicit N/A, with ORL stated wherever RIN appears and case-$T$ class stated wherever power or bias appears. **Decision unlocked:** negotiate ATP limits, or reopen the architecture fork that left a cell empty.

**Key idea.** Laser leadership is a requirements sheet: architecture forks force specific specs (power, grid, RIN@ORL, SMSR, bias window, CMIS, FIT). Fill Table laser-prd from the link budget and fleet model, then enforce it with the ATP (supplier-exec).

## LIV, SMSR, and RIN: the measurement playbook

These three measurements decide whether a laser chip or module is usable. The instruments are standard; the skill is knowing which failure each one catches.

##### LIV (light--current--voltage).

The LIV curve plots optical power and forward voltage versus bias current. Read off threshold $I_\mathrm{th}$, slope efficiency (mW/mA above threshold), kink-free operating range, and thermal rollover at high current or high case temperature. Fig. liv-sketch is a labeled schematic (not measured data).

High-temp LIV failures look like: $I_\mathrm{th}$ rise, slope collapse, early rollover, or a kink that moves into the bias window. Those map to aging, TEC saturation, or package thermal resistance (laser-aging).

<figure id="fig:liv-sketch" data-latex-placement="ht">
<embed src="figures/fig_liv_sketch.pdf" style="width:85.0%" />
<figcaption>Schematic LIV curve with threshold, slope, kink, and thermal rollover labeled. Idealized for teaching; use measured LIV for pass/fail. <span id="fig:liv-sketch" data-label="fig:liv-sketch"></span></figcaption>
</figure>

##### SMSR (side-mode suppression ratio).

SMSR is the power difference (dB) between the lasing mode and the strongest side mode on an optical spectrum analyzer (OSA). Datacom single-mode parts require high SMSR so side modes do not steal power or seed modal noise. Spec-sheet floors are part-specific; treat the datasheet or ATP limit as authoritative. SMSR collapse under temperature or aging is a reject: the laser is leaving single-mode operation.

##### RIN (relative intensity noise).

Measure RIN with a calibrated photodetector and RF spectrum analyzer (or a dedicated RIN analyzer), under a controlled optical return loss. Distinguish *intrinsic* RIN (quiet bench, high ORL) from stressed $\mathrm{RIN}_x\mathrm{OMA}$ used in Ethernet/MSA specs. IEEE 802.3 / 100G Lambda class links cap $\mathrm{RIN}_{17.1}\mathrm{OMA}$ at $-136$ dB/Hz with 17.1 dB ORL . Quiet datacom DFB/EML parts typically sit well below that when feedback is controlled; CPO ELS designs care as much about feedback tolerance as about the quiet number (rin-values, rin).

<table class="book-table"><tr><th>Parameter</th><th>Instrument</th><th>Pass/fail intent</th><th>Failure signature</th></tr><tr><td>LIV</td><td>SMU + power meter / integrating sphere</td><td>I_th, slope, kink-free bias window</td><td>high-temp rollover; kink in bias range</td></tr><tr><td>SMSR</td><td>OSA</td><td>single-mode purity vs.\ datasheet/ATP</td><td>side modes rise with T or age</td></tr><tr><td>RIN</td><td>PD + ESA / RIN analyzer</td><td>intrinsic and stressed RIN_xOMA</td><td>RIN rises with ORL; BER floor (sec:rin)</td></tr><tr><td>Bias-driver noise</td><td>SMU vs.\ product bias board</td><td>RIN_eq from i_n (sec:laser-drivers)</td><td>RIN rises with rails on, flat vs.\ ORL</td></tr><tr><td>Wavelength</td><td>OSA / wavemeter</td><td>grid placement, d/dT, d/dI</td><td>walk off ring or MSA grid</td></tr><tr><td>EAM bias (EML)</td><td>bias sweep + DCA/TDECQ</td><td>extinction, chirp, RLM</td><td>aging shifts absorption curve</td></tr></table>
**Table ?.** Laser measurement playbook: what to measure, with what, and what failure looks like.

Measure in order: LIV $\to$ SMSR $\to$ wavelength $\to$ RIN (quiet then stressed ORL) $\to$ EAM or bias-driver checks as the path requires. Stop when distributions across temperature and units support the bias window, grid, and RIN policy in Table laser-prd (see also Table laser-engineering-checklist). Do not keep measuring for its own sake once those exits close.

## Laser drivers and the RIN budget

Modulator RF drivers (drivers) deliver swing and bandwidth into an EAM or MZM. Laser *bias* drivers are a different circuit: they set a quiet constant current into the diode. Current noise on that path becomes optical intensity noise and adds in the RIN budget of rin. Confusing the two is a common debug miss: a great SiGe PAM4 driver can still ruin a CW laser if its supply or ground couples into the bias rail.

##### From current noise to equivalent RIN.

Above threshold, optical power tracks bias approximately as $P\propto(I-I_\mathrm{th})$. Relative intensity fluctuations then track relative current fluctuations: $$\mathrm{RIN}_{\mathrm{eq,lin}}
\;\approx\;
\left(\frac{i_n}{I-I_\mathrm{th}}\right)^{\!2},
\qquad
\mathrm{RIN}_{\mathrm{eq}}[\mathrm{dB/Hz}]
\;=\;
20\log_{10}\!\left(\frac{i_n}{I-I_\mathrm{th}}\right),$$ where $i_n$ is the one-sided current-noise density in A$/\sqrt{\mathrm{Hz}}$ at the laser terminals (driver plus board pickup). The approximation assumes linear slope efficiency and ignores intrinsic laser dynamics; it is a budget tool, not a device model.

Worked numbers at $I-I_\mathrm{th}=50$ mA (typical CW DFB window): $i_n=500$ pA$/\sqrt{\mathrm{Hz}}$ maps to $\mathrm{RIN}_{\mathrm{eq}}\approx-160$ dB/Hz; $270$ pA$/\sqrt{\mathrm{Hz}}$ maps to about $-165$ dB/Hz. Commercial low-noise laser drivers quote roughly $50$--$500$ pA$/\sqrt{\mathrm{Hz}}$ at 1 kHz depending on current range (Table laser-driver-noise); the Koheron DRV200 family is a concrete example . Against a good datacom intrinsic RIN of $-145$ to $-155$ dB/Hz (rin-values), those 1 kHz densities look comfortable. The budget tightens when $(I-I_\mathrm{th})$ is small (near threshold, derated CW, or low-current VCSELs), when you integrate broadband switching noise rather than a 1 kHz spot, or when SerDes/DSP rails dump discrete tones onto the bias network.

<table class="book-table"><tr><th>Driver class (example)</th><th>i_n @ 1 kHz</th><th>RIN_eq @ 50 mA</th><th>What it means</th></tr><tr><td>Ultra-low-noise CW (DRV200-A-40)</td><td>55 pA/Hz</td><td>-179 dB/Hz</td><td>Bench / metrology floor</td></tr><tr><td>Low-noise CW (DRV200-A-200)</td><td>270 pA/Hz</td><td>-165 dB/Hz</td><td>Typical quiet CW source</td></tr><tr><td>Higher-current CW (DRV200-A-400)</td><td>480 pA/Hz</td><td>-160 dB/Hz</td><td>Still below -155 intrinsic</td></tr><tr><td>Shared digital LDO, poor PSRR</td><td>often 1 nA/Hz + tones</td><td>can exceed -145</td><td>False ``RIN'' on ESA</td></tr></table>
**Table ?.** Bias-driver current noise converted to equivalent RIN at $I-I_\mathrm{th}=50$ mA using $\mathrm{RIN}_{\mathrm{eq}}=20\log_{10}(i_n/(I-I_\mathrm{th}))$. Densities for the DRV200 rows are from the Koheron datasheet at 1 kHz; the last row is qualitative (board-dependent).

##### CW / ELSFP / CW-WDM paths.

For external CW sources feeding Si or TFLN modulators, design the bias path as a low-noise current source with high supply rejection, local decoupling at the diode, and a star ground that does not share return with SerDes switching currents. Automatic power control () loops that close through a monitor PD suppress slow drift; keep the loop bandwidth well below the RIN measurement band and quiet enough that the loop itself does not inject intensity noise. ELSFP and CW-WDM modules hide this circuitry inside the pluggable (elsfp, cwwdm-laser); acceptance still needs module-level RIN with the host bias and management rails connected, not only a quiet SMU on the bare die.

##### DML and EML.

A *DML* shares one diode for bias and RF: a bias tee (or on-chip bias network) combines a quiet DC source with the RF driver. Excess RF driver broadband noise, poor tee isolation, or supply ripple on the bias arm all raise measured RIN and chirp-related penalties. An *EML* splits the problem: keep the DFB bias as quiet as a CW source, and treat the EAM RF driver under drivers. EAM drive amplitude sets extinction and chirp; DFB bias noise still lands in optical intensity before the modulator.

##### What to measure on the bench.

Bisect electrical vs. optical RIN:

1.  Measure intrinsic RIN with a quiet SMU or known low-noise driver and high ORL (laser-params).

2.  Repeat with the product bias board / module rails connected. Any rise is driver or supply contribution, not laser physics.

3.  Sweep ORL. Rise with reflection is feedback-driven laser RIN (rin-values); rise independent of ORL points at the electrical path.

4.  Look for discrete spurs on the ESA (switching frequencies, CMIS clocks). Spurs fail stressed $\mathrm{RIN}_x\mathrm{OMA}$ even when the broadband floor looks fine (rin-values).

**Key idea.** Treat laser bias noise as a RIN term: $\mathrm{RIN}_{\mathrm{eq}}\approx(i_n/(I-I_\mathrm{th}))^2$. Quiet CW drivers at tens to hundreds of pA$/\sqrt{\mathrm{Hz}}$ usually sit under a $-145$ dB/Hz intrinsic floor at 50 mA; digital supply pickup, near-threshold bias, and DML bias-tee leakage are what actually burn the budget.

## How lasers fail

Six mechanisms account for most laser field returns. Each has a distinct telemetry signature, so classify before you open FA.

Threshold current increase

: $I_\mathrm{th}$ rises from its ship value at fixed temperature, usually with slope efficiency dropping in step. Points to active-region or facet degradation (laser-aging).

Slope efficiency degradation

: Output power per unit bias current falls even when $I_\mathrm{th}$ is stable. A separate wear-out track from threshold rise; both show up on the same LIV sweep.

Wavelength drift

: The lasing line walks off its grid slot or ring resonance. Distinguish laser drift from TEC or ring drift by holding one actuator fixed and moving the other (locking-techniques, Ch. wdm).

Aging (SMSR collapse, mode hopping)

: Side modes grow relative to the main mode, or the laser hops between modes under temperature or current. An OSA trend over time is the tell.

Thermal runaway

: A positive feedback loop where higher junction temperature raises threshold current and cuts slope efficiency, so more drive power turns to heat for the same optical output, raising temperature further until the TEC saturates and the laser rolls over. Triggered by a failed or saturated TEC, a blocked heat path, or operation above the rated thermal class. Distinct from ordinary wear-out because it is fast (minutes, not months) once it starts; the failure-analysis handbook has the full symptom-to-cause breakdown (fm-thermal-runaway).

Monitor photodiode failure

: The control loop's own sensor drifts or fails, so the laser looks unstable when the real fault is in the feedback path, not the gain medium (lasers-how-fails).

## Separate thermal behavior from long-term aging

Thermal response is reversible on the time scale of a temperature sweep or cycle. It changes threshold current, slope efficiency, wavelength, EAM bias, TEC current, and ring alignment. Measure it with controlled case-temperature sweeps, loaded thermal corners, heater sweeps, and thermal cycling. Repeat the measurement after returning to the starting temperature. Recovery points toward an operating-point or control problem.

Long-term aging is cumulative. Threshold current rises, slope efficiency falls, contacts degrade, defects grow, and an absorption or spectral curve can move permanently. Measure those changes with HTOL, accelerated life testing, and periodic LIV, spectrum, and modulation readouts. A temperature cycle can expose a weak attach or calibration error, but it does not by itself establish a lifetime acceleration model.

Do not merge the data sets. A high-temperature BER failure that clears at room temperature needs thermal-margin work. A room-temperature baseline that keeps moving after each stress interval needs an aging or damage hypothesis.

## Calibration: what drifts and what triggers retuning

Calibration exists because no transmitter runs at a datasheet point. Every unit has its own threshold, slope, absorption curve, quadrature point, and resonance, and each of those moves with temperature and age. The operating points a product actually stores are:

Laser bias / APC target

: the bias current or monitor-PD power setpoint that holds launch power. Drifts as threshold rises and slope falls with age (laser-aging); a drifting monitor PD corrupts it silently (lasers-how-fails).

EAM bias (EML)

: the reverse-bias point that sets extinction and chirp. Moves with case temperature and with absorption-curve aging, so production parts store bias versus temperature, not one number.

MZM quadrature

: the phase bias that holds the modulator at its linear point. Drifts with temperature, stress, and age; a bias-control loop tracks it, and a railed loop is a telemetry alarm, not a retune request.

Ring heater / lock point

: the tuner power that aligns resonance to the laser line. Consumes headroom as ambient rises and neighbors heat; a railed DAC means the tuning range is exhausted (locking-techniques, thermal-xtalk).

Tables are usually segmented by temperature. Segment boundaries are a real failure mode: the debug story in lasers-how-debugged is a healthy laser reading the wrong temperature segment after thermal cycling. Keep calibration tables under change control and record the table version with every test result, or failures cannot be replayed.

Recalibration should be triggered by evidence, not habit: a control-loop error residual that no longer converges, an actuator (TEC, heater, bias DAC) that approaches its rail, telemetry that disagrees with an external reference, a temperature excursion beyond the table range, or a repair, rework, or firmware change that invalidates stored coefficients. ATP must verify calibration at the temperature corners the fleet will see, not only at the station ambient (prod-corners).

## How lasers are qualified

Qualification projects the failure mechanisms of how-lasers-fail forward from a short bench test to years of field life. Three stress classes do the work:

HTOL (high-temperature operating life)

: Run a sample lot at elevated temperature and bias for a fixed duration (often 1000 hours) and track LIV, SMSR, and wavelength drift. HTOL is the primary input to the Arrhenius life projection below.

Burn-in

: A shorter, sometimes 100%-screen stress that removes infant-mortality units before ship, rather than projecting life. Burn-in trades test time for escape rate (hvm-test).

Environmental stress

: Temperature cycling, damp heat, vibration, and shock catch packaging, attach, and mechanical failure modes that HTOL does not. They qualify different risks and should not be treated as substitutes for long-term aging data (gr468).

Together with the Arrhenius acceleration factor, these three stresses turn a qualification lot into a defensible FIT number.

##### Observable aging signatures.

Watch LIV and spectrum over HTOL or field life:

- threshold rise and slope drop (active-region / facet degradation);

- SMSR collapse (mode competition);

- EAM bias creep on EMLs (absorption curve shift $\to$ TDECQ/RLM drift);

- RIN rise under feedback (ORL or isolator failure);

- COD (catastrophic optical damage) at the facet under overstress.

Each signature should appear in the ATP and in field telemetry triage (fleet-triage, gr468).

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

Fig. accelerated-aging is the mental model behind HTOL: same starting health, faster drift at higher temperature, a defined end-of-life threshold, and shorter time-to-failure as stress rises. For lasers the vertical axis is usually tied to LIV or power at constant current; the temperature axis must be junction temperature, not only chamber set point.

##### When the projection is valid.

Acceleration assumes the stress speeds up the *same* physical mechanism the fleet will see. The projection fails in two ways: the stress activates a mechanism the field never sees (solder creep or moisture ingress at a stress temperature the product never reaches), or the field sees a mechanism the stress never exercises (connector wear, bias-rail transients, thermal cycling from traffic load). So a qual number is a hypothesis, not a fact: compare field-return Pareto and failure signatures against the qual projection, and treat divergence as evidence that $E_a$ or the mechanism model is wrong, not that the fleet is unlucky (fleet-triage). Sudden fails (COD, ESD, cracked fiber attach) sit outside Fig. accelerated-aging; classify those separately before you fit Arrhenius parameters.

##### Derating.

Run below absolute-max current, case temperature, and optical power. Derating extends wear-out life and reduces COD risk. Uncooled datacom parts already sit near thermal limits at high case temperature; cooled or faceplate ELSFP modules (elsfp) buy headroom by moving heat off the ASIC package.

##### Worked FIT example (assumptions labeled).

FIT is failures per $10^9$ device-hours. For illustration only, assume 50 FIT per laser (confirm against your supplier qual; do not treat 50 as a measured claim) and a fabric with $5\times10^5$ lasers (order-of-magnitude for a large AI cluster with several optical links per accelerator). Expected failures per day: $$\frac{5\times10^5 \times 50 \times 24}{10^9}
\approx 0.6\ \text{laser failures/day}.$$ That is why field-replaceable ELSFP modules, burn-in screens, and derating are design inputs, not afterthoughts (Ch. reliability).

## ELS and ELSFP: architecture, pinout, qual

*ELSFP* (External Laser Small Form-Factor Pluggable) is the OIF form factor for faceplate-pluggable CW laser modules that feed co-packaged optical engines . The lasers sit at the coolest part of the system (front panel), hot-swap when they fail, and keep thermal load off the ASIC and photonic engine.

##### Mechanical and optical.

The module uses a card-edge electrical interface and a blind-mate multi-fiber optical connector at the rear (MT-class ferrules), which improves eye safety for high CW power by keeping live fiber inside the chassis . One ELSFP can feed more than one optical engine. OIF defines optical power classes, thermal classes, and wavelength assignments (e.g. DR-type 1311 nm and FR-type CWDM4 grids) so hosts and modules interoperate.

##### Management and hot-swap.

ELSFP uses CMIS and the CMIS module state machine over TWI. On plug-in the module resets, initializes management, and stays in low-power mode with lasers *off* until the host transitions it to ModuleReady and explicitly enables lasers . `ModPrsL` and `IntL` support presence detect and asynchronous alarms for safe hot-swap.

##### Electrical pinout (OIF-ELSFP-02.0 Table 7).

Twenty-four contacts: multiple 3.3 V VCC and GND pins, module reset (`ResetL`), low-power mode (`LPModeL`), two-wire serial management (`SCL`/`SDA`), presence (`ModPrsL`), and interrupt (`IntL`), plus reserved pins for future power/ground . Table elsfp-pins summarizes the published map.

<table class="book-table"><tr><th>Pin</th><th>Function</th><th>Requirements</th><th>Notes</th></tr><tr><td>1--3</td><td>VCC</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>4</td><td>TBD</td><td>reserved</td><td>future power</td></tr><tr><td>5</td><td>ResetL</td><td>pull-up 10 k</td><td>reset module, LVTTL</td></tr><tr><td>6</td><td>LPModeL</td><td>MMC on only</td><td>low-power mode (low), LVTTL</td></tr><tr><td>7</td><td>TBD</td><td>reserved</td><td>future ground</td></tr><tr><td>8--10</td><td>GND</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>11</td><td>TBD</td><td>reserved</td><td>---</td></tr><tr><td>12</td><td>SCL</td><td>TWI clock</td><td>host 4.7 k pull-up; module 10 k</td></tr><tr><td>13</td><td>SDA</td><td>TWI data</td><td>same pull-ups as SCL</td></tr><tr><td>14</td><td>TBD</td><td>reserved</td><td>---</td></tr><tr><td>15--17</td><td>GND</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr><tr><td>18</td><td>TBD</td><td>reserved</td><td>future ground</td></tr><tr><td>19</td><td>ModPrsL</td><td>shorted to GND in module</td><td>presence (low), LVTTL</td></tr><tr><td>20</td><td>IntL</td><td>pull-up 10 k</td><td>interrupt, LVTTL</td></tr><tr><td>21</td><td>TBD</td><td>reserved</td><td>future power</td></tr><tr><td>22--24</td><td>VCC</td><td>1.5 A, 3.3 V</td><td>with noise filtering</td></tr></table>
**Table ?.** ELSFP electrical pinout (adapted from OIF-ELSFP-02.0 Table 7). Lasers power only in ModuleReady after host command; default on plug-in is lasers off .

##### Qual hooks for suppliers.

Acceptance test plans should cover the checklist in Table atp-laser, supplier-exec: laser LIV/SMSR/RIN inside the module; optical power-class compliance; connector mating cycles and contamination/ORL; burn-in before ship; CMIS register sanity; and thermal class at rated case temperature. Module bring-up must also prove the CMIS enable sequence and ModuleReady laser policy (bringup). Field returns split between laser wear-out and connector/fiber-attach faults; keep both in the triage tree (fleet-triage).

## Optical safety and laser classes

### Hazard and laser classes

Laser safety for interconnects is governed by IEC 60825-1 (laser product classification) and IEC 60825-2 (optical-fiber communication systems, OFCS) . Classes run from Class 1 (safe under normal use) through Class 1M (safe unless the beam is collected by optics), Class 3R/3B, and Class 4. At 1310 nm and 1550 nm the beam is invisible, which raises the operational risk: technicians cannot see exposure. The retinal-hazard band ends near 1400 nm, but corneal and skin hazards remain, and single-mode power confined to a $\sim$9 μm core is high radiance even at modest milliwatt levels.

Short-reach datacom modules are usually engineered so each fiber port stays Class 1 or Class 1M under rated launch power. That is a design constraint on EML/DFB bias and on how much power each lane launches, not a label you add after the fact.

### Hazard level = aggregate, not per-lane

The safety case scales with *total* launched power at an accessible location, not with a single DFB data sheet. CW-WDM and ELS banks concentrate many lines on one MT or MPO ferrule (elsfp). A connector that breaks out eight or sixteen fibers can exceed a per-lane Class 1 budget even when each lane is modest. IEC 60825-2 assigns hazard levels (1 through 4) to each accessible port in the OFCS based on the radiant power that could escape during service . That is why ELS architecture and fiber count drive classification, not the laser chip alone.

### Open-fiber protection: APR and ALS

When fiber continuity is lost, open connectors and broken fiber can expose hazardous power. *APR* (automatic power reduction) holds output at or below Hazard Level 1M and probes for re-mate with safe low-power pulses. *ALS* (automatic laser shutdown) cuts power entirely and was common on older SDH links; for modern high-power systems APR with automatic restart is the preferred pattern because restart probes stay within the hazard limit . ITU-T G.664 requires power reduction to Hazard Level 1M within about 3 s of a continuity break, a restart inhibit window, and restart only at safe power.

These mechanisms tie directly to CMIS and bring-up policy: lasers enable only when the host commands ModuleReady (bringup, cmis). APR/ALS is what makes a live ELSFP hot-swap survivable in a running rack (prod-corners).

### What validation and ops owe

Optical safety is a validation deliverable, not a compliance sticker. ATP should verify APR/ALS trip threshold and timing on representative open-fiber faults; label modules and cages with the rated class; document max launched power per port and per MPO breakout; and write service procedures for multi-fiber connectors. At fleet scale, a hot-swap runbook that assumes ALS works but was never tested in ATP is a real hazard. Fold the APR/ALS check into the ELS hot-swap corner in prod-corners alongside mate-cycle and ORL tests.

## CW-WDM source validation

Multi-wavelength CW sources (CW-WDM MSA) feed dense ring or filter banks on a PIC (cwwdm, Ch. wdm). Validation is per-channel plus cross-channel:

- power flatness across $\lambda$ (uneven OMA after the modulator bank);

- per-channel SMSR and wavelength grid placement;

- channel crosstalk and residual ASE between lines;

- lock to microring resonances under temperature and neighbor heating (locking-techniques, thermal-xtalk, siring);

- RIN and ORL sensitivity for each line (laser-params, rin-values).

Examples: Ayar Labs SuperNova (CW-WDM MSA-compliant, feeds TeraPHY)  ; Broadcom ELSFP banks on Tomahawk CPO (cpo-status, elsfp); quantum-dot comb lasers (Ranovus, Quintessent) aimed at many $\lambda$ from one chip. Source tests live here; locking and on-chip MUX live in Ch. wdm.

## Light-source supply strategy

The sourcing decision follows the same architecture fork as the optical design: buy a merchant source, buy a serviceable external module, or bind the source to the photonic package. Evaluate each path by qualification ownership, second-source portability, lot traceability, test access, field replacement, and change-control rights. A vendor list ages quickly and does not answer those questions.

Merchant DFB, EML, or CW die

: preserve module-level design freedom and can support a second source, but the integrator owns attach, driver match, screening, and package reliability.

External CW-WDM or ELSFP module

: moves source qualification and management into a replaceable unit. The system still owns connector, ORL, hot-swap, and host interoperability (elsfp, cwwdm-laser).

Multi-wavelength source

: reduces source count and can simplify WDM fan-out, but couples channel yield, power flatness, control, and replacement into one unit (cwwdm-laser).

Source integrated with the PIC

: reduces optical interfaces and can improve density, but makes laser yield and wear-out part of package yield and service life.

<table class="book-table"><tr><th>Approach</th><th>Qualification ownership and risk</th></tr><tr><td>Merchant DFB/EML/CW die</td><td>Integrator owns attach, driver match, screen, and module qual</td></tr><tr><td>External CW-WDM / ELSFP module</td><td>Supplier owns source module; system owns interface and service qual</td></tr><tr><td>Multi-wavelength source</td><td>Shared yield, power-flatness, and replacement risk across channels</td></tr><tr><td>Source integrated with PIC</td><td>Highest density; laser yield and life become package risks</td></tr></table>
**Table ?.** Light-source sourcing paths and the qualification ownership each one creates.

### Reading the supplier ownership matrix

Table laser-suppliers is a qualification-ownership map. The fork decides who owns life data, screens, and field service, not only who ships a die.

##### Merchant DFB / EML / CW die.

**Purpose.** Who owns attach, driver match, module screen, and package reliability when the source is a merchant die?

**Uncertainty removed.** Die datasheets do not qualify the module. After ownership is explicit, the integrator knows which FAIR, ATP, and HTOL packages stay in-house.

**Evidence the other party still owes.** Die-level LIV, SMSR, RIN, and life sample data from the merchant; change control on epi and process.

**Decision unlocked.** Accept integrator-owned module qual, or reject the path if attach and screen capability are missing.

**Risk if ownership is assumed wrong.** You treat a die cert as module qual and discover attach or driver match in the fleet.

##### External CW-WDM / ELSFP module.

**Purpose.** What does the source supplier own versus what the system still must qualify?

**Uncertainty removed.** A replaceable ELS moves source life into a field unit, but connector, ORL, hot-swap, and host interop remain system-owned (elsfp).

**Evidence the other party still owes.** Supplier: source-module ATP, CMIS, life, and mate ratings. System: optical mate, ORL plant, service sequence, and engine bring-up with light present.

**Decision unlocked.** Approve ELS architecture only when both ownership packs exist.

**Risk if ownership is assumed wrong.** You qualify the laser module and skip the optical interface that fails first in service.

##### Multi-wavelength source.

**Purpose.** How do channel yield, power flatness, and replacement couple across the comb?

**Uncertainty removed.** One weak channel can scrap or derate the whole source. Shared control means shared field risk (cwwdm-laser).

**Evidence required.** Per-channel power and wavelength distributions, flatness over temperature, and a replacement/service policy when one channel fails.

**Decision unlocked.** Accept coupled yield, require channel redundancy, or split into multiple sources.

**Risk if ownership is assumed wrong.** You buy "one laser" economics and inherit N-channel fail modes without N-channel screens.

##### Source integrated with PIC.

**Purpose.** When laser yield and wear-out become package risks, who owns life and service?

**Uncertainty removed.** Density gains remove a replaceable optical interface. Failures then pull the engine or package, not a pluggable source.

**Evidence required.** Package-level life, known-good attach, and a service model that matches non-replaceable sources.

**Decision unlocked.** Accept integrated risk for density, or keep ELS/merchant die for field replaceability.

**Risk if ownership is assumed wrong.** You qualify the die physics and underfund package yield and fleet replacement cost.

### Why ownership order matters

Choose the service and ownership model before you freeze the optical architecture. An external source is replaceable and adds a managed interface. An integrated source removes that interface and places source yield inside the package. Qualify the architecture you will service, not only the laser die.

### Learning summary

Merchant die

: Integrator owns module qual; merchant owns die life data.

ELS / CW-WDM module

: Supplier owns source; system owns mate, ORL, swap.

Multi-wavelength

: Channels share yield and replacement risk.

Integrated PIC

: Laser life is package life; plan service accordingly.

[^15]

## Why lasers are the reliability bottleneck

At the scale of a large optical fleet the laser is usually the reliability-limiting component. It is an active device with wear-out physics that passive optics and even photodiodes largely lack:

- *Catastrophic optical damage* (COD) at the facet.

- Gradual facet and active-region degradation (accelerated by temperature, following Arrhenius kinetics; laser-aging).

- EAM aging in EMLs; coupling and solder drift in packaged assemblies.

Because failures scale with the number of lasers, a fleet of $100{,}000$+ links turns a modest per-laser FIT rate into a steady stream of field failures (fit-example, gr468). The mitigations shape architecture: field-replaceable external laser sources (ELSFP, CW-WDM), redundancy, burn-in screening to weed out infant mortality, and derating (running lasers below their maximum to extend life).

## Margin erosion over temperature, lot, and life

A link rarely loses all margin in one event. The source can lose launch power as slope efficiency falls. Connector loss and ORL can rise after service. EAM or MZM bias can move. A ring can consume spectral headroom as its heater approaches range. Driver noise can raise the BER floor while none of these changes violates its stand-alone limit.

Track five ledgers:

Power margin

: launch power, coupling, connector and MUX loss, receiver sensitivity, and aging reserve.

Noise margin

: intrinsic and feedback-driven RIN, bias-rail noise, receiver noise, and crosstalk.

Timing margin

: source and modulator bandwidth, dispersion, driver and host jitter, and equalization reserve.

Spectral margin

: laser wavelength, SMSR, filter or ring passband, thermal drift, and lock range.

Control margin

: headroom in APC, TEC, heaters, ring lock, bias DACs, and calibration tables. A railed loop can fail the link while the diode is still healthy.

Recompute the link at combined production corners. A nominal part at nominal temperature says little about whether a slow loss in two ledgers will push a tail unit across the pre-FEC BER limit. prod-corners, Table fleet-triage carry the same ledgers into validation and fleet triage. The interview review compresses this checklist in interview-margin-ledgers. The wall-chart form is tree-margin-budget.

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
Not every debit is naturally in decibels. Depending on the subsystem, remaining margin may be optical power, sensitivity, BER or FEC headroom, eye or TDECQ, jitter, control range, lifetime, or yield. Validation often measures the net externally visible result; do not double-count internal penalties the test cannot separate (link-budget).

## Engineering lens

### How it works

A laser is an active device with wear-out physics, which makes it both the first line of the link budget and the fleet's reliability bottleneck. The chapter's device families and LIV/SMSR/RIN measurements all serve one question: will this source stay in spec for years at temperature?

### How it is measured

Qualify the laser as a set of curves across temperature, bias, ORL, and age, not a room-temperature data-sheet point. The measurement playbook (LIV, SMSR, RIN, wavelength, and EAM checks with their instruments and pass/fail intent) is in laser-params, Table laser-meas; the stress classes that project field life are in how-lasers-qualified, laser-aging, gr468 .

### How it fails

The six field-return mechanisms are catalogued in how-lasers-fail: threshold rise, slope droop, wavelength drift, aging (SMSR collapse and mode hopping), thermal runaway, and monitor-photodiode failure. Manufacturing adds die, wafer, lot, and assembly spread to every one. The mechanism that most often misleads triage is a healthy laser behind a bad feedback sensor, so it gets the worked callout below.

\> \*\*Failure mode: Monitor photodiode drift\*\* \> \> \*\*Symptoms.\*\* Reported power falls or the bias loop moves, but an external power meter does not show the same change. \> \> \*\*Likely causes.\*\* Monitor-PD responsivity drift, transimpedance gain error, contamination in the monitor path, or a bad calibration coefficient. \> \> \*\*Measurements.\*\* External power meter, monitor current, bias current, LIV, and loop error versus temperature. \> \> \*\*Mitigations.\*\* Repair the monitor path or calibration, add disagreement alarms, and do not raise laser bias to compensate for a false reading.

### How it is debugged

For power degradation, compare external optical power, monitor current, bias, and case temperature before changing the setpoint. Rerun LIV at the failing temperature and compare it with ship data. If LIV moved, inspect SMSR, wavelength, and RIN to classify active-region, facet, or modal change. If LIV is stable, move to coupling, connector, monitor-PD, and control-loop checks. For a wavelength excursion, inspect OSA data and TEC current together. For a bias anomaly, replace the product driver with a quiet source before blaming the diode.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* BER worsened after thermal cycling while average optical power stayed in range. \> \> \*\*Investigation.\*\* The DCA showed that extinction ratio had collapsed. LIV and SMSR were unchanged, and an EAM bias sweep restored the eye. \> \> \*\*Finding.\*\* The light source was healthy, but its modulator operating point was wrong. \> \> \*\*Root cause.\*\* A calibration table used the wrong temperature segment after the cycle. \> \> \*\*Resolution.\*\* The table and screening limits were fixed, and EAM bias sweep data became part of the thermal-cycle readout.

## Engineering checklist

<table class="book-table"><tr><th>Decision or test</th><th>Question it answers</th><th>Evidence to retain</th><th></th></tr><tr><td>Architecture</td><td>Does the source and modulation path close reach, rate, power, cost, and service?</td><td>Requirement allocation and rejected alternatives</td><td></td></tr><tr><td>LIV</td><td>Is the operating window clear of threshold, kinks, and rollover?</td><td>Curves by unit, lot, temperature, and age</td><td></td></tr><tr><td>Spectrum</td><td>Does wavelength and SMSR stay inside the assigned grid and filter passband?</td><td>OSA or wavemeter data across corners</td><td></td></tr><tr><td>RIN and ORL</td><td>Does noise margin survive the reflection environment?</td><td>Quiet and stressed RIN with stated ORL and bandwidth</td><td></td></tr><tr><td>Modulation</td><td>Does bias, drive, chirp, and bandwidth close the eye?</td><td>Bias sweeps, TDECQ or equivalent, and driver conditions</td><td></td></tr><tr><td>Thermal behavior</td><td>Are reversible shifts within control and actuator range?</td><td>Temperature and heater sweeps, TEC current, recovery data</td><td></td></tr><tr><td>Long-term aging</td><td>Which parameters drift permanently, and at what rate?</td><td>HTOL intervals, LIV, spectrum, and modulation trends</td><td></td></tr><tr><td>Manufacturing</td><td>Can the ATP catch bad units and lot drift at useful test cost?</td><td>Limits, guard bands, GR\</td><td>R, yield, and reaction plan</td></tr><tr><td>Fleet operation</td><td>Which monitors distinguish source, modulator, cooler, and optical path?</td><td>Telemetry map, alarm thresholds, and golden baselines</td><td></td></tr></table>
**Table ?.** Source and modulation engineering checklist. Each row ties a decision to evidence, not only a test name.

### Reading the laser engineering checklist

Table laser-engineering-checklist is the decision sequence for a laser program. Measurement methods for LIV, SMSR, RIN, and aging are taught earlier in this chapter; the notes below focus on what each row unlocks and when you may leave it.

##### Architecture.

**Purpose.** Does the source and modulation path close reach, rate, power, cost, and service?

**Uncertainty removed.** Component enthusiasm does not allocate requirements. After architecture you have a chosen path, rejected alternatives, and owners for lock, attach, and life (Table source-mod-matrix, Table laser-suppliers).

**Exit criteria.** **Exit when** requirement allocation and rejected alternatives are written and reviewed.

**Decision unlocked.** Freeze the path into Table laser-prd, or reopen the matrix.

**Risk if skipped.** You validate a hero topology that cannot be serviced or powered in the rack.

##### LIV.

**Purpose.** Is the operating window clear of threshold, kinks, and rollover across unit, lot, temperature, and age (laser-params)?

**Exit criteria.** **Exit when** kink-free bias windows and distributions support the bias policy.

**Decision unlocked.** Set bias and derate, or reject lots / redesign the window.

**Risk if skipped.** Soft BER and sudden dark fails appear without a ship baseline to compare.

##### Spectrum.

**Purpose.** Do wavelength and SMSR stay inside the assigned grid and filter passband?

**Exit criteria.** **Exit when** OSA or wavemeter data across corners meet grid and SMSR floors.

**Decision unlocked.** Approve channel assignment, tighten temperature policy, or reject modal risk.

**Risk if skipped.** WDM unlock and modal noise show up as "random" BER.

##### RIN and ORL.

**Purpose.** Does noise margin survive the reflection environment the plant will present (rin-values)?

**Exit criteria.** **Exit when** quiet and stressed RIN at stated ORL and bandwidth meet the BER-floor budget.

**Decision unlocked.** Approve isolator-free or isolator-required design; set plant cleaning rules.

**Risk if skipped.** Lab RIN looks fine; field ORL raises the floor.

##### Modulation.

**Purpose.** Do bias, drive, chirp, and bandwidth close the eye at baud?

**Exit criteria.** **Exit when** bias sweeps and TDECQ (or equivalent) at named driver conditions meet Tx quality limits (tdecq).

**Decision unlocked.** Freeze EAM/MZM/ring bias policy, or reject the modulator class for this rate.

**Risk if skipped.** Average power passes while the eye fails under temperature.

##### Thermal behavior.

**Purpose.** Are reversible shifts within control and actuator range?

**Exit criteria.** **Exit when** temperature and heater sweeps, TEC current, and recovery data show control headroom at loaded corners.

**Decision unlocked.** Approve thermal envelope, add heaters/TEC margin, or derate case $T$.

**Risk if skipped.** Lock and calibration faults are misread as permanent aging.

##### Long-term aging.

**Purpose.** Which parameters drift permanently, and at what rate (laser-aging)?

**Exit criteria.** **Exit when** HTOL intervals with LIV, spectrum, and modulation trends support the life claim or force derate.

**Decision unlocked.** Accept FIT/replacement plan, or hold ship for life risk.

**Risk if skipped.** Useful-life planning uses hope instead of a mechanism.

##### Manufacturing.

**Purpose.** Can the ATP catch bad units and lot drift at useful test cost (Table atp-laser)?

**Exit criteria.** **Exit when** limits, guardbands, GR&R, yield, and a reaction plan exist for the ship screens.

**Decision unlocked.** Open volume screens, or hold for process control.

**Risk if skipped.** Qualified engineering lots diverge from production without a catch point.

##### Fleet operation.

**Purpose.** Which monitors distinguish source, modulator, cooler, and optical path (fleet-triage)?

**Exit criteria.** **Exit when** telemetry map, alarm thresholds, and golden baselines are named and owned.

**Decision unlocked.** Arm fleet triage; feed escapes back into ATP.

**Risk if skipped.** Field tickets cannot separate laser wear from connector or TEC faults.

### Why the checklist order matters

Architecture first, or you characterize the wrong path. LIV and spectrum establish semiconductor and channel health before RIN and modulation argue about floors and eyes. Thermal separates reversible control from permanent drift before aging claims. Manufacturing and fleet close the loop so life and screens stay honest after ship. Later rows must not compensate for a missing architecture or ship baseline.

### Learning summary

Architecture

: Does the path close the product?

LIV / spectrum / RIN

: Is the source healthy in its plant?

Modulation / thermal

: Does the eye and control survive corners?

Aging

: What drifts permanently, and how fast?

Manufacturing / fleet

: Can you screen it and triage it at volume?

## Interview takeaway

**Key idea.** Measure LIV, SMSR, wavelength, and RIN as distributions across temperature, lot, and age. Tie each requirement to an ATP row, each life claim to a physical mechanism, and each field alarm to a measurement that separates the laser from its driver, monitor, cooler, and optical path.

Junior mistake: declare wear-out from monitor telemetry alone, or raise launch power before naming which ledger spent (laser-margin-erosion, Ch. wdm, Ch. reliability).

##### Three questions to test yourself.

1.  Why is the laser typically the reliability-limiting component in an optical link?

2.  Optical power fell but the monitor photodiode reports no change. What do you check?

3.  How would you qualify a second laser supplier without assuming the first supplier's failure distribution?


<div class="nav-links">
  <a href="ch4-quantitative-models-noise-rin-and-ber">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch6-wdm-and-wavelength-locked-lasers">Next &rarr;</a>
</div>
