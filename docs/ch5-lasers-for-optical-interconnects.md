---
layout: default
title: "Ch 5: Lasers for optical interconnects"
---

# Lasers for optical interconnects

Every optical link begins with a light source, and at fleet scale that source is usually the reliability bottleneck as well as the first item on the link budget. Datacenter interconnects have spent two decades climbing from coarse multimode optics toward dense single-mode WDM and co-packaged engines; each step changed which laser family won and which measurements decided pass/fail. This chapter follows that arc: the device families in use today, how a roadmap choice becomes a measurable requirements slice, the LIV/SMSR/RIN suite, how bias drivers enter the intensity-noise budget, aging and derating, and the external laser modules (ELSFP, CW-WDM) that make co-packaged optics serviceable.

## Device families

The short-reach market does not use one laser. It uses a small set of families, each tuned to a reach, a fiber type, and a packaging style. Broadly, the industry moved from multimode VCSEL arrays inside the rack, to single-mode DFB/EML pluggables for DR/FR, to external CW sources feeding silicon or TFLN modulators for CPO and 400G/lane. The list below is the vocabulary you will meet on datasheets and in supplier meetings; later sections explain how to measure and qualify each one.

DFB (distributed feedback)

: a grating along the active region gives single-mode output; the workhorse continuous-wave (CW) or directly modulated source for CWDM and LAN-WDM (§ `sec:dfb-eml`).

DBR (distributed Bragg reflector)

: the grating sits outside the gain region; enables tunable variants.

DML (directly modulated laser)

: modulate the bias current directly: cheap and low-power, but chirp-limited over dispersive fiber (§ `sec:dml-vcsel`).

EML (externally modulated laser)

: *EML*: a DFB integrated with an *EAM*. Low chirp and high bandwidth make it the dominant 100--200G/lane transmitter for single-mode links at DR (500 m) and shorter (§ `sec:dfb-eml,sec:eml-eam`).

CW laser + TFLN MZM

: an external CW source feeds a thin-film lithium niobate Mach--Zehnder modulator on a separate chip. Very low chirp and $\gtrsim$`<!-- -->`{=html}100 GHz EO bandwidth make this the leading path to 400G/lane pluggables and high-baud FR links; see § `sec:tfln-mzm,tab:tx-modulator`.

CW laser + Si MZM

: an external CW source feeds a silicon Mach--Zehnder modulator on the same PIC (§ `sec:simzm`). Low chirp, flat passband, and CMOS fab integration make this the default for 100--200G/lane DR/FR SiPh modules; 400G/lane demos appeared in 2026.

CW laser + Si ring

: same laser architecture, but a microring or microdisk modulator on the PIC (§ `sec:siring`). Smaller footprint and strong WDM/CPO fit; wavelength lock and thermal crosstalk dominate validation (§ `ch:wdm`).

CW-WDM / multi-wavelength sources

: high-power, multi-wavelength CW lasers (per the CW-WDM MSA) that feed comb-like WDM architectures (§ `sec:cwwdm-laser,sec:cwwdm`).

VCSEL

: 850--940 nm multimode sources for short-reach links over multimode fiber; cheap but reach-limited and less relevant at 200G/lane.

External laser source (ELS/ELSFP)

: a pluggable laser module supplying CW light to a co-packaged switch, so a failed laser is field-replaceable (§ `sec:elsfp`).

## Directly modulated lasers and VCSELs

Before EMLs and silicon photonics took over single-mode datacenter ports, most volume optics were either a cheap *DML* on single-mode fiber or a *VCSEL* array into multimode fiber. Both still matter at the low-cost, short-reach edge of the market, and both show why chirp, modal bandwidth, and temperature push AI fabrics toward externally modulated single-mode sources.

A DML modulates laser bias current directly. The transmitter is simple and efficient, but the same carrier dynamics that make modulation easy also produce chirp: intensity changes drag the optical frequency along (§ `sec:chirp-dispersion`). Over multimode or very short single-mode runs that is often acceptable. Over dispersive single-mode fiber at tens of GBd, the chirp turns into inter-symbol interference and closes the eye. Validation therefore focuses on extinction ratio, pattern-dependent chirp, and RIN, not just average power.

VCSELs took a different path. They emit from a vertical cavity at 850--940 nm straight into multimode fiber, so parallel arrays are easy to assemble and cheap to ship. That combination made VCSEL SR optics the default for early 40G/100G Ethernet inside the rack (100G-SR4 and its cousins): short ribbons of MMF, high lane count, low dollars per gigabit. The same physics that made them attractive also capped their future. Multimode fiber has modal bandwidth and modal noise limits; VCSEL bandwidth and reliability both degrade with temperature; and as lane rates climb toward 100 G and 200 G, those limits arrive sooner. The industry response has been incremental (better OM4/OM5 fiber, tighter specs, sometimes PAM4 on MMF) rather than a clean leap to 400G/lane SMF DR. In practice, MMF reach and modal dispersion keep VCSEL links in the SR box (§ `sec:pmd-reach`), while hyperscale AI fabrics standardize on single-mode DR/FR and CPO.

Neither family is the path to 400G/lane SMF DR. EMLs and external modulators (§ `sec:dfb-eml,sec:simzm,tab:tx-modulator`) own that space. Pattern-aware chirp linearization can stretch a DML a little farther, but it does not change the physics at FR distances: if you need low chirp and high EO bandwidth at fleet scale, you leave direct modulation behind.

## DFB and EML: the workhorse transmitters

Once single-mode DR/FR became the hyperscale default, most short-reach ports started with an InP laser chip. Two configurations still dominate production: the CW or directly modulated DFB, and the EML that adds an electro-absorption modulator on the same die.

##### DFB.

A distributed-feedback laser has a grating along the active region that selects one longitudinal mode. Spec-sheet metrics that matter in bring-up are threshold current, slope efficiency, SMSR (typically many tens of dB on a clean part), RIN, and wavelength vs. temperature/current. Used as a CW source for SiPh or TFLN modulators, or as a DML when chirp is acceptable (§ `sec:dml-vcsel`). Uncooled datacom DFBs ride case temperature with a known $d\lambda/dT$; cooled parts add a TEC and lock to a grid.

##### EML.

An electro-absorption modulated laser integrates a DFB with an *EAM* on one chip (§ `sec:eml-eam`). Reverse bias on the EAM sets absorption and extinction; chirp stays far below a DML. That combination, not marketing, is why EMLs became the volume answer for 100G/lane and then 200G/lane DR/FR pluggables: one chip, low chirp, mature supply chain. Validation adds EAM bias sweeps, aging of the absorption curve, and driver-match checks on top of the DFB LIV/SMSR/RIN suite (§ `sec:laser-params,sec:laser-aging`).

##### When to pick which.

Through 200G/lane DR, EML usually wins on cost and integration. A CW DFB (or ELSFP/CW-WDM bank) plus Si MZM, ring, or TFLN wins when the modulator must sit on silicon or needs $\gtrsim$`<!-- -->`{=html}100 GHz EO bandwidth (§ `tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm`). At CPO scale the laser often leaves the optical engine entirely so it can be replaced without pulling the ASIC package (§ `sec:elsfp`). Looking forward, 400G/lane pluggables are pushing harder toward external CW plus TFLN or high-BW silicon modulators, while EMLs remain the workhorse of the installed 100--200G base.

[]

  -------------------------------------------------------------------------------------------
  Source          Typical use                  Top risks
  --------------- ---------------------------- ----------------------------------------------
  DML             short reach, cost-driven     chirp/dispersion, extinction ratio

  EML             $\le$DR, 100--200G/lane      EAM bias/aging, thermal

  CW + TFLN MZM   400G/lane FR/DR, NPO         MZM bias drift, fiber attach, driver match

  CW + Si MZM     DR/FR SiPh, 100--400G/lane   driver match, bias drift, fiber coupling

  CW + Si ring    CPO, WDM transceivers        wavelength lock, thermal crosstalk, coupling

  VCSEL           SR over MMF                  modal noise, reach, temperature

  ELS / ELSFP     co-packaged optics           connectorization, fleet serviceability
  -------------------------------------------------------------------------------------------

**Table .** When each source is used, and its top validation risks.

## Silicon photonics platforms

The previous sections covered laser sources. This one treats the *modulator platforms* built in silicon that those sources feed. Silicon photonics (*SiPh*) integrates waveguides, phase shifters, modulators, detectors, and couplers on a single silicon-on-insulator (*SOI*) die in a CMOS-compatible fab flow. Two modulator topologies dominate short-reach IM/DD: the Mach--Zehnder modulator (MZM) and the microring modulator (MRM). Both encode data by converting an electrical signal into optical intensity via a refractive-index change in a PN junction phase shifter. This section covers the device physics common to both, then the trade-offs that decide which one fits a given link.

### PN junction phase shifters

Every silicon modulator starts with a phase shifter: a waveguide whose effective index $n_\mathrm{eff}$ changes with an applied voltage. In silicon, which has no useful Pockels effect, the dominant mechanism is the *plasma dispersion effect*: changing free-carrier concentration $\Delta N_e$, $\Delta N_h$ shifts $n_\mathrm{eff}$ and introduces absorption $\Delta\alpha$. Two drive modes exploit this effect:

Carrier depletion

: a reverse-biased PN junction sweeps carriers out of the waveguide core under voltage. Fast (RC-limited to tens of GHz with optimized doping profiles), low loss, and the default for high-speed datacom. Phase-shift efficiency is modest: typical $V_\pi L \approx 1.5$--$2.5$ V$\cdot$cm on production platforms.

Carrier injection

: a forward-biased PIN structure floods carriers into the intrinsic region. Large $\Delta n$ (low $V_\pi L$, often $<0.5$ V$\cdot$cm) but slow: carrier recombination limits bandwidth to a few GHz without pre-emphasis. Used in low-speed tuning (ring heater replacement) and variable optical attenuators, not for PAM4 data modulation at 100G+/lane.

The key figure of merit is *$V_\pi L$*: the product of the half-wave voltage $V_\pi$ (the voltage that produces a $\pi$ phase shift) and the phase-shifter length $L$. Lower $V_\pi L$ means either a shorter device (less loss, smaller footprint) or a lower drive voltage (easier on the driver). Carrier-depletion silicon sits at $V_\pi L \approx 1.5$--$2.5$ V$\cdot$cm; thin-film lithium niobate (§ `sec:tfln-mzm`) reaches $\approx 1$ V$\cdot$cm via the Pockels effect.

### Electro-optic bandwidth

*EO bandwidth* is the frequency at which the modulator's optical response ($S_{21}$, measured as the ratio of detected optical modulation to applied RF voltage) falls by 3 dB from its low-frequency value. It is the primary speed metric and depends on:

- **Junction RC.** Depletion capacitance $C_j$ and series resistance $R_s$ set an intrinsic roll-off $f_{3\mathrm{dB}} \approx 1/(2\pi R_s C_j)$. Thinner junctions (lower $C_j$) raise BW but reduce overlap with the optical mode (higher $V_\pi L$). Typical design targets: $C_j \approx 0.2$--$0.4$ pF/mm, $R_s \approx 5$--$15$ $\Omega\cdot$mm.

- **Velocity mismatch (MZM).** In a traveling-wave electrode (TWE) design, microwave and optical group indices must match or the modulation signal walks off the optical pulse. Si MZMs typically use slow-wave or loaded-line electrodes to equalize indices.

- **Photon lifetime (ring).** A high-$Q$ ring stores photons longer, narrowing the optical passband and creating an EO bandwidth ceiling at $f_{3\mathrm{dB}} \approx f_\mathrm{res}/(2Q)$ where $f_\mathrm{res}$ is the resonance frequency. Inductive peaking (T-coils) extends EO BW beyond the intrinsic cavity limit.

Production Si MZMs quote 70--100+ GHz; peaked ring modulators reach 90--110+ GHz in conference demos (§ `sec:siring`).

### Insertion loss

*Insertion loss* (IL) is the optical power lost traversing the modulator in its on-state. It subtracts directly from the link budget (§ `sec:link-budget`). Sources:

- **Waveguide propagation loss:** $\sim$`<!-- -->`{=html}1--3 dB/cm in production 220 nm SOI rib waveguides (doping-dependent; heavier doping for lower $V_\pi L$ raises free-carrier absorption).

- **Coupling loss:** fiber-to-chip (grating coupler $\sim$`<!-- -->`{=html}2--4 dB; edge coupler $\sim$`<!-- -->`{=html}1--2 dB) and splitter/combiner ($<$`<!-- -->`{=html}0.5 dB for a 3-dB MMI).

- **Phase-shifter excess loss:** doped silicon absorbs; carrier-depletion adds $\sim$`<!-- -->`{=html}3--8 dB/cm depending on doping concentration. Shorter phase shifters (lower $V_\pi L$) trade this against $V_\pi$.

Total on-chip IL for a Si MZM (including splitters) lands at $\sim$`<!-- -->`{=html}2--5 dB; a single ring modulator typically adds $\sim$`<!-- -->`{=html}1--3 dB at the through port on resonance. Every dB of IL is a dB off the transmitter OMA and must be recovered by higher launch power or tighter receiver sensitivity (§ `sec:sensitivity`).

### Mach--Zehnder modulators in silicon

A silicon MZM splits light into two arms, applies opposite phase shifts (push-pull), and recombines at a coupler. Intensity modulation arises from constructive/destructive interference. Advantages over resonant devices:

- **Broadband:** flat passband, no wavelength lock needed. Channel assignment is set by the laser, not the modulator.

- **Linear transfer:** the sine-squared MZM transfer function is well-characterized for PAM4 linearity budgets.

- **Temperature-insensitive:** no resonance to drift with thermal transients (contrast with rings, § `sec:siring`).

Trade-offs: mm-scale device length (large footprint), higher IL than a ring, and the need for a matched traveling-wave electrode (TWE) with velocity-matched microwave and optical group indices. At 224 GBd the 112 GHz Nyquist pushes against the velocity-match and RC limits of current production processes; peaking and advanced electrode co-design are active research areas (§ `sec:simzm`).

### Ring modulators in silicon

A microring modulator couples a bus waveguide to a closed-loop resonator via evanescent fields. On resonance, light drops into the ring and is strongly attenuated at the through port; off resonance, light passes. Data modulation shifts the resonance wavelength via carrier depletion in the ring's PN junction.

Advantages:

- **Compact:** ring radius 5--20 $\mu$m; hundreds fit on a die for dense WDM (§ `ch:wdm`).

- **Low drive voltage:** resonance enhancement means small $\Delta n$ produces large extinction; effective $V_\pi L$ is much lower than an MZM.

- **WDM-native:** each ring modulates one $\lambda$; add rings to add channels without extra MUX stages.

Trade-offs:

- **Wavelength lock:** resonance drifts $\sim$`<!-- -->`{=html}10 GHz/$^\circ$C in silicon. Each ring needs active thermal tuning or laser-to-ring feedback (§ `sec:locking-techniques`).

- **Photon-lifetime BW limit:** high $Q$ improves efficiency but caps EO BW. Inductive peaking extends usable BW to 90--110+ GHz in demos (§ `sec:siring`).

- **Thermal crosstalk:** adjacent-ring heaters shift neighbors in dense arrays (§ `sec:thermal-xtalk`).

### Choosing MZM versus ring

  Attribute                 Si MZM                                   Si ring
  ------------------------- ---------------------------------------- ---------------------------------------------------------
  Footprint                 mm-scale                                 $\mu$m-scale
  $V_\pi L$ (effective)     1.5--2.5 V$\cdot$cm                      $<$`<!-- -->`{=html}0.1 V$\cdot$cm (resonance-enhanced)
  EO BW (production)        70--100+ GHz                             50--90 GHz (peaked: 110+ GHz)
  Wavelength lock           not needed                               required
  WDM scaling               one per $\lambda$ + MUX                  inherently WDM-native
  On-chip IL                2--5 dB                                  1--3 dB
  Temperature sensitivity   low                                      high ($\sim$`<!-- -->`{=html}10 GHz/$^\circ$C)
  Best fit                  single-$\lambda$ DR/FR, broad-passband   CPO, dense WDM, scale-up optical I/O

  : Si MZM vs. ring modulator trade-offs.

Use an MZM when the link is single-wavelength DR/FR and you want a flat passband that avoids control loops. Use a ring when many $\lambda$ must fit on one PIC and modulator area dominates, as in CPO WDM engines and scale-up optical I/O (§ `sec:siring,sec:cpo-status`). Use TFLN when native 224 GBd bandwidth is needed and silicon cannot close the 112 GHz Nyquist without heavy peaking (§ `sec:tfln-mzm`).

**Key idea.** Silicon photonics modulates light by changing free-carrier density in a PN junction (plasma dispersion). Carrier depletion is fast but weak ($V_\pi L \approx
1.5$--$2.5$ V$\cdot$cm); carrier injection is strong but slow. MZMs are broadband and temperature-insensitive but large; rings are compact and WDM-native but need wavelength lock and have a photon-lifetime BW ceiling. Both share the same SOI fab flow, so the choice is architectural, not process-limited.

## Laser requirements: from roadmap to specs

Laser requirements only work when they are numbers a supplier can fail and a link budget can close. Start from the interconnect roadmap choice, then fill a short requirements slice; the ATP in § `sec:supplier-exec` is how that slice is enforced on every lot.

##### Roadmap forks that set the laser.

Each architecture decision forces a different requirements set (§ `tab:laser-req-fork`):

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
  Roadmap choice                      Laser implication                           Specs you must freeze early
  ----------------------------------- ------------------------------------------- -------------------------------------------------------------------------------
  Pluggable EML vs CW+Si/TFLN         Integrated EAM vs external CW + modulator   EAM bias/aging and TDECQ vs CW power class, RIN, and modulator $V_\pi$ match

  On-package laser vs ELSFP/CW-WDM    Field replace vs FIT inside the package     Connector/ORL/mate cycles and hot-swap CMIS vs COD/aging inside ASIC thermal

  Isolator vs isolator-free (CPO)     Feedback tolerance vs quiet RIN only        Stressed $\mathrm{RIN}_x\mathrm{OMA}$ at stated ORL; monitor PD / lock policy

  Single-$\lambda$ vs CW-WDM / comb   One line vs $N$ lines into rings/filters    Per-line power flatness, SMSR, grid, crosstalk (§ `sec:cwwdm-laser`)

  Retimed vs LPO                      Module DSP hides Tx vs host sees raw eye    Laser+modulator TDECQ/RLM floor vs host COM budget (§ `sec:com,sec:drivers`)

  Derate policy                       Operating $I$, $T$, power below abs-max     Bias window, thermal class, FIT/$E_a$ assumptions (§ `sec:laser-aging`)
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Architecture forks and the laser specs each one forces. Freeze these before DVT samples are built (§ `sec:supplier-exec`).

##### One-page requirements slice.

§ `tab:laser-prd` is the PRD-sized list. Fill every row with a number (or an explicit "N/A for this architecture") before you negotiate ATP limits. Do not leave RIN without an ORL, or power without a case-temperature class.

[]

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Parameter                How to set the number                                               Measure / ATP              Reject if                            Derate / ops note
  ------------------------ ------------------------------------------------------------------- -------------------------- ------------------------------------ --------------------------------------------------
  Launch power / class     Link budget + connector loss + aging margin (§ `sec:link-budget`)   Power meter; ELSFP class   Below min at rated $T$               Cap max power for COD

  Wavelength / grid        PMD or ring FSR plan; $d\lambda/dT$ headroom (§ `ch:wdm`)           OSA / wavemeter            Off-grid at case $T$                 TEC setpoints

  SMSR floor               Datasheet + modal-noise budget                                      OSA                        Below floor at $T$                   Watch aging

  RIN (quiet + stressed)   BER floor vs BW (§ `sec:rin`); ORL from plant                       PD+ESA; stated ORL         Above limit at ORL                   Bias-driver noise budget (§ `sec:laser-drivers`)

  Bias window              LIV kink-free range at max case $T$                                 LIV                        Kink in window                       Run below abs-max $I$

  EAM / MZM (if any)       ER, RLM, TDECQ at baud (§ `sec:tdecq`)                              DCA + bias sweep           TDECQ/RLM fail                       Bias aging policy

  ORL / isolator           Architecture: isolator-free needs tighter RIN                       ORL meter; mate cycles     ORL out of range                     Cleaning / ELS mate life

  CMIS monitors            What fleet triage will read (§ `sec:fleet-triage`)                  CMIS dump                  Missing alarms / bad state machine   Enable sequence (§ `sec:bringup`)

  FIT / life               Fleet failures/day target (§ `sec:fit-example`)                     GR-468 + $E_a$             Screen escape                        Burn-in depth; ELS replace
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Laser requirements one-pager. Every cell needs a program number; this table is the structure, not the limits.

##### How to fill numbers (method, not invention).

Work backward from the link, not forward from a marketing slide. The four steps below turn an architecture choice into ATP limits:

1.  Close the optical ledger at target pre-FEC BER (§ `sec:link-budget,sec:kp4`). That sets minimum launch OMA/power and maximum allowed penalties (transmitter and dispersion eye closure quaternary, TDECQ; ORL/RIN).

2.  From receiver BW and the RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ (§ `sec:rin`), set a stressed RIN limit with margin under the plant ORL you will actually see (not only a quiet bench).

3.  From case-temperature and derating policy, set the LIV bias window and thermal class so the laser never sits on a kink or at abs-max in the fleet (§ `sec:laser-aging,sec:prod-corners`).

4.  From service model, choose ELSFP mate-cycle / hot-swap requirements or accept on-package FIT and write COD/aging screens accordingly (§ `sec:elsfp`).

Hand the filled slice to the supplier with the ATP checklist (§ `tab:atp-laser`). If a roadmap slide cannot point to a row in § `tab:laser-prd`, the requirement is not real yet.

**Key idea.** Laser leadership is a requirements sheet: architecture forks force specific specs (power, grid, RIN@ORL, SMSR, bias window, CMIS, FIT). Fill § `tab:laser-prd` from the link budget and fleet model, then enforce it with the ATP (§ `sec:supplier-exec`).

## LIV, SMSR, and RIN: the measurement playbook

These three measurements decide whether a laser chip or module is usable. The instruments are standard; the skill is knowing which failure each one catches.

##### LIV (light--current--voltage).

The LIV curve plots optical power and forward voltage versus bias current. Read off threshold $I_\mathrm{th}$, slope efficiency (mW/mA above threshold), kink-free operating range, and thermal rollover at high current or high case temperature. § `fig:liv-sketch` is a labeled schematic (not measured data).

High-temp LIV failures look like: $I_\mathrm{th}$ rise, slope collapse, early rollover, or a kink that moves into the bias window. Those map to aging, TEC saturation, or package thermal resistance (§ `sec:laser-aging`).

::::
![](figures/fig_liv_sketch.pdf){width="85%"}

::: caption
Schematic LIV curve with threshold, slope, kink, and thermal rollover labeled. Idealized for teaching; use measured LIV for pass/fail. []
:::
::::

##### SMSR (side-mode suppression ratio).

SMSR is the power difference (dB) between the lasing mode and the strongest side mode on an optical spectrum analyzer (OSA). Datacom single-mode parts require high SMSR so side modes do not steal power or seed modal noise. Spec-sheet floors are part-specific; treat the datasheet or ATP limit as authoritative. SMSR collapse under temperature or aging is a reject: the laser is leaving single-mode operation.

##### RIN (relative intensity noise).

Measure RIN with a calibrated photodetector and RF spectrum analyzer (or a dedicated RIN analyzer), under a controlled optical return loss. Distinguish *intrinsic* RIN (quiet bench, high ORL) from stressed $\mathrm{RIN}_x\mathrm{OMA}$ used in Ethernet/MSA specs. IEEE 802.3 / 100G Lambda class links cap $\mathrm{RIN}_{17.1}\mathrm{OMA}$ at $-136$ dB/Hz with 17.1 dB ORL . Quiet datacom DFB/EML parts typically sit well below that when feedback is controlled; CPO ELS designs care as much about feedback tolerance as about the quiet number (§ `sec:rin-values,sec:rin`).

[]

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Parameter           Instrument                               Pass/fail intent                                                  Failure signature
  ------------------- ---------------------------------------- ----------------------------------------------------------------- ---------------------------------------------
  LIV                 SMU + power meter / integrating sphere   $I_\mathrm{th}$, slope, kink-free bias window                     high-temp rollover; kink in bias range

  SMSR                OSA                                      single-mode purity vs. datasheet/ATP                              side modes rise with $T$ or age

  RIN                 PD + ESA / RIN analyzer                  intrinsic and stressed $\mathrm{RIN}_x\mathrm{OMA}$               RIN rises with ORL; BER floor (§ `sec:rin`)

  Bias-driver noise   SMU vs. product bias board               $\mathrm{RIN}_{\mathrm{eq}}$ from $i_n$ (§ `sec:laser-drivers`)   RIN rises with rails on, flat vs. ORL

  Wavelength          OSA / wavemeter                          grid placement, $d\lambda/dT$, $d\lambda/dI$                      walk off ring or MSA grid

  EAM bias (EML)      bias sweep + DCA/TDECQ                   extinction, chirp, RLM                                            aging shifts absorption curve
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Laser measurement playbook: what to measure, with what, and what failure looks like.

## Laser drivers and the RIN budget

Modulator RF drivers (§ `sec:drivers`) deliver swing and bandwidth into an EAM or MZM. Laser *bias* drivers are a different circuit: they set a quiet constant current into the diode. Current noise on that path becomes optical intensity noise and adds in the RIN budget of § `sec:rin`. Confusing the two is a common debug miss: a great SiGe PAM4 driver can still ruin a CW laser if its supply or ground couples into the bias rail.

##### From current noise to equivalent RIN.

Above threshold, optical power tracks bias approximately as $P\propto(I-I_\mathrm{th})$. Relative intensity fluctuations then track relative current fluctuations: $$\mathrm{RIN}_{\mathrm{eq,lin}}
\;\approx\;
\left(\frac{i_n}{I-I_\mathrm{th}}\right)^{\!2},
\qquad
\mathrm{RIN}_{\mathrm{eq}}[\mathrm{dB/Hz}]
\;=\;
20\log_{10}\!\left(\frac{i_n}{I-I_\mathrm{th}}\right),$$ where $i_n$ is the one-sided current-noise density in A$/\sqrt{\mathrm{Hz}}$ at the laser terminals (driver plus board pickup). The approximation assumes linear slope efficiency and ignores intrinsic laser dynamics; it is a budget tool, not a device model.

Worked numbers at $I-I_\mathrm{th}=50$ mA (typical CW DFB window): $i_n=500$ pA$/\sqrt{\mathrm{Hz}}$ maps to $\mathrm{RIN}_{\mathrm{eq}}\approx-160$ dB/Hz; $270$ pA$/\sqrt{\mathrm{Hz}}$ maps to about $-165$ dB/Hz. Commercial low-noise laser drivers quote roughly $50$--$500$ pA$/\sqrt{\mathrm{Hz}}$ at 1 kHz depending on current range (§ `tab:laser-driver-noise`); the Koheron DRV200 family is a concrete example . Against a good datacom intrinsic RIN of $-145$ to $-155$ dB/Hz (§ `sec:rin-values`), those 1 kHz densities look comfortable. The budget tightens when $(I-I_\mathrm{th})$ is small (near threshold, derated CW, or low-current VCSELs), when you integrate broadband switching noise rather than a 1 kHz spot, or when SerDes/DSP rails dump discrete tones onto the bias network.

[]

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Driver class (example)             $i_n$ @ 1 kHz                                                   $\mathrm{RIN}_{\mathrm{eq}}$ @ 50 mA   What it means
  ---------------------------------- --------------------------------------------------------------- -------------------------------------- ------------------------------
  Ultra-low-noise CW (DRV200-A-40)   55 pA$/\sqrt{\mathrm{Hz}}$                                      $\approx-179$ dB/Hz                    Bench / metrology floor

  Low-noise CW (DRV200-A-200)        270 pA$/\sqrt{\mathrm{Hz}}$                                     $\approx-165$ dB/Hz                    Typical quiet CW source

  Higher-current CW (DRV200-A-400)   480 pA$/\sqrt{\mathrm{Hz}}$                                     $\approx-160$ dB/Hz                    Still below $-155$ intrinsic

  Shared digital LDO, poor PSRR      often $\gg$`<!-- -->`{=html}1 nA$/\sqrt{\mathrm{Hz}}$ + tones   can exceed $-145$                      False "RIN" on ESA
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Bias-driver current noise converted to equivalent RIN at $I-I_\mathrm{th}=50$ mA using $\mathrm{RIN}_{\mathrm{eq}}=20\log_{10}(i_n/(I-I_\mathrm{th}))$. Densities for the DRV200 rows are from the Koheron datasheet at 1 kHz; the last row is qualitative (board-dependent).

##### CW / ELSFP / CW-WDM paths.

For external CW sources feeding Si or TFLN modulators, design the bias path as a low-noise current source with high supply rejection, local decoupling at the diode, and a star ground that does not share return with SerDes switching currents. Automatic power control () loops that close through a monitor PD suppress slow drift; keep the loop bandwidth well below the RIN measurement band and quiet enough that the loop itself does not inject intensity noise. ELSFP and CW-WDM modules hide this circuitry inside the pluggable (§ `sec:elsfp,sec:cwwdm-laser`); acceptance still needs module-level RIN with the host bias and management rails connected, not only a quiet SMU on the bare die.

##### DML and EML.

A *DML* shares one diode for bias and RF: a bias tee (or on-chip bias network) combines a quiet DC source with the RF driver. Excess RF driver broadband noise, poor tee isolation, or supply ripple on the bias arm all raise measured RIN and chirp-related penalties. An *EML* splits the problem: keep the DFB bias as quiet as a CW source, and treat the EAM RF driver under § `sec:drivers`. EAM drive amplitude sets extinction and chirp; DFB bias noise still lands in optical intensity before the modulator.

##### What to measure on the bench.

Bisect electrical vs. optical RIN:

1.  Measure intrinsic RIN with a quiet SMU or known low-noise driver and high ORL (§ `sec:laser-params`).

2.  Repeat with the product bias board / module rails connected. Any rise is driver or supply contribution, not laser physics.

3.  Sweep ORL. Rise with reflection is feedback-driven laser RIN (§ `sec:rin-values`); rise independent of ORL points at the electrical path.

4.  Look for discrete spurs on the ESA (switching frequencies, CMIS clocks). Spurs fail stressed $\mathrm{RIN}_x\mathrm{OMA}$ even when the broadband floor looks fine (§ `sec:rin-values`).

**Key idea.** Treat laser bias noise as a RIN term: $\mathrm{RIN}_{\mathrm{eq}}\approx(i_n/(I-I_\mathrm{th}))^2$. Quiet CW drivers at tens to hundreds of pA$/\sqrt{\mathrm{Hz}}$ usually sit under a $-145$ dB/Hz intrinsic floor at 50 mA; digital supply pickup, near-threshold bias, and DML bias-tee leakage are what actually burn the budget.

## How lasers fail

Six mechanisms account for most laser field returns. Each has a distinct telemetry signature, so classify before you open FA.

Threshold current increase

: $I_\mathrm{th}$ rises from its ship value at fixed temperature, usually with slope efficiency dropping in step. Points to active-region or facet degradation (§ `sec:laser-aging`).

Slope efficiency degradation

: Output power per unit bias current falls even when $I_\mathrm{th}$ is stable. A separate wear-out track from threshold rise; both show up on the same LIV sweep.

Wavelength drift

: The lasing line walks off its grid slot or ring resonance. Distinguish laser drift from TEC or ring drift by holding one actuator fixed and moving the other (§ `sec:locking-techniques,ch:wdm`).

Aging (SMSR collapse, mode hopping)

: Side modes grow relative to the main mode, or the laser hops between modes under temperature or current. An OSA trend over time is the tell.

Thermal runaway

: A positive feedback loop where rising junction temperature raises leakage current, which raises self-heating further, until the diode overheats and fails catastrophically. Triggered by a failed or saturated TEC, a blocked heat path, or operation above the rated thermal class. Distinct from ordinary wear-out because it is fast (minutes, not months) once it starts; the failure-analysis handbook has the full symptom-to-cause breakdown (§ `sec:fm-thermal-runaway`).

Monitor photodiode failure

: The control loop's own sensor drifts or fails, so the laser looks unstable when the real fault is in the feedback path, not the gain medium (§ `sec:lasers-how-fails`).

## How lasers are qualified

Qualification projects these six mechanisms forward from a short bench test to years of field life. Three stress classes do the work:

HTOL (high-temperature operating life)

: Run a sample lot at elevated temperature and bias for a fixed duration (often 1000 hours) and track LIV, SMSR, and wavelength drift. HTOL is the primary input to the Arrhenius life projection below.

Burn-in

: A shorter, sometimes 100%-screen stress that removes infant-mortality units before ship, rather than projecting life. Burn-in trades test time for escape rate (§ `sec:hvm-test`).

Accelerated aging (temperature cycling, damp heat)

: Telcordia GR-468-CORE stresses beyond HTOL that catch packaging and mechanical failure modes thermal soak alone misses (§ `sec:gr468`).

Together with the Arrhenius acceleration factor, these three stresses turn a qualification lot into a defensible FIT number.

##### Observable aging signatures.

Watch LIV and spectrum over HTOL or field life:

- threshold rise and slope drop (active-region / facet degradation);

- SMSR collapse (mode competition);

- EAM bias creep on EMLs (absorption curve shift $\to$ TDECQ/RLM drift);

- RIN rise under feedback (ORL or isolator failure);

- COD (catastrophic optical damage) at the facet under overstress.

Each signature should appear in the ATP and in field telemetry triage (§ `sec:fleet-triage,sec:gr468`).

## Aging curves, derating, and fleet FIT

Lasers wear out. At fleet scale that is not a footnote; it sets architecture (ELSFP vs. integrated laser) and operating policy (derating, burn-in).

##### Arrhenius life projection.

Telcordia GR-468-CORE qualifies optoelectronic parts with accelerated stress (HTOL, temperature cycle, damp heat) and projects field life with Arrhenius acceleration : $$\mathrm{AF}
= \exp\!\left[\frac{E_a}{k_B}\left(\frac{1}{T_\mathrm{use}}-\frac{1}{T_\mathrm{stress}}\right)\right],$$ where $E_a$ is the activation energy for the wear-out mechanism under test, $k_B$ is Boltzmann's constant, and temperatures are absolute. Document $E_a$, sample size, and confidence bounds when converting a 1000-hour HTOL lot into field-year FIT. Activation energies are mechanism-specific; use the value justified in the qual plan, not a generic number copied from another product.

##### Derating.

Run below absolute-max current, case temperature, and optical power. Derating extends wear-out life and reduces COD risk. Uncooled datacom parts already sit near thermal limits at high case temperature; cooled or faceplate ELSFP modules (§ `sec:elsfp`) buy headroom by moving heat off the ASIC package.

##### Worked FIT example (assumptions labeled).

FIT is failures per $10^9$ device-hours. For illustration only, assume 50 FIT per laser (confirm against your supplier qual; do not treat 50 as a measured claim) and a fabric with $5\times10^5$ lasers (order-of-magnitude for a large AI cluster with several optical links per accelerator). Expected failures per day: $$\frac{5\times10^5 \times 50 \times 24}{10^9}
\approx 0.6\ \text{laser failures/day}.$$ That is why field-replaceable ELSFP modules, burn-in screens, and derating are design inputs, not afterthoughts (§ `ch:reliability`).

## ELS and ELSFP: architecture, pinout, qual

*ELSFP* (External Laser Small Form-Factor Pluggable) is the OIF form factor for faceplate-pluggable CW laser modules that feed co-packaged optical engines . The lasers sit at the coolest part of the system (front panel), hot-swap when they fail, and keep thermal load off the ASIC and photonic engine.

##### Mechanical and optical.

The module uses a card-edge electrical interface and a blind-mate multi-fiber optical connector at the rear (MT-class ferrules), which improves eye safety for high CW power by keeping live fiber inside the chassis . One ELSFP can feed more than one optical engine. OIF defines optical power classes, thermal classes, and wavelength assignments (e.g. DR-type 1311 nm and FR-type CWDM4 grids) so hosts and modules interoperate.

##### Management and hot-swap.

ELSFP uses CMIS and the CMIS module state machine over TWI. On plug-in the module resets, initializes management, and stays in low-power mode with lasers *off* until the host transitions it to ModuleReady and explicitly enables lasers . `ModPrsL` and `IntL` support presence detect and asynchronous alarms for safe hot-swap.

##### Electrical pinout (OIF-ELSFP-02.0 Table 7).

Twenty-four contacts: multiple 3.3 V VCC and GND pins, module reset (`ResetL`), low-power mode (`LPModeL`), two-wire serial management (`SCL`/`SDA`), presence (`ModPrsL`), and interrupt (`IntL`), plus reserved pins for future power/ground . § `tab:elsfp-pins` summarizes the published map.

[]

  -----------------------------------------------------------------------------------------------------------------------
  Pin      Function    Requirements               Notes
  -------- ----------- -------------------------- -----------------------------------------------------------------------
  1--3     VCC         1.5 A, 3.3 V               with noise filtering

  4        TBD         reserved                   future power

  5        ResetL      pull-up 10 k$\Omega$       reset module, LVTTL

  6        LPModeL     MMC on only                low-power mode (low), LVTTL

  7        TBD         reserved                   future ground

  8--10    GND         1.5 A, 3.3 V               with noise filtering

  11       TBD         reserved                   ---

  12       SCL         TWI clock                  host 4.7 k$\Omega$ pull-up; module $\ge$`<!-- -->`{=html}10 k$\Omega$

  13       SDA         TWI data                   same pull-ups as SCL

  14       TBD         reserved                   ---

  15--17   GND         1.5 A, 3.3 V               with noise filtering

  18       TBD         reserved                   future ground

  19       ModPrsL     shorted to GND in module   presence (low), LVTTL

  20       IntL        pull-up 10 k$\Omega$       interrupt, LVTTL

  21       TBD         reserved                   future power

  22--24   VCC         1.5 A, 3.3 V               with noise filtering
  -----------------------------------------------------------------------------------------------------------------------

**Table .** ELSFP electrical pinout (adapted from OIF-ELSFP-02.0 Table 7). Lasers power only in ModuleReady after host command; default on plug-in is lasers off .

##### Qual hooks for suppliers.

Acceptance test plans should cover the checklist in § `tab:atp-laser,sec:supplier-exec`: laser LIV/SMSR/RIN inside the module; optical power-class compliance; connector mating cycles and contamination/ORL; burn-in before ship; CMIS register sanity; and thermal class at rated case temperature. Module bring-up must also prove the CMIS enable sequence and ModuleReady laser policy (§ `sec:bringup`). Field returns split between laser wear-out and connector/fiber-attach faults; keep both in the triage tree (§ `sec:fleet-triage`).

## Optical safety and laser classes

### Hazard and laser classes

Laser safety for interconnects is governed by IEC 60825-1 (laser product classification) and IEC 60825-2 (optical-fiber communication systems, OFCS) . Classes run from Class 1 (safe under normal use) through Class 1M (safe unless the beam is collected by optics), Class 3R/3B, and Class 4. At 1310 nm and 1550 nm the beam is invisible, which raises the operational risk: technicians cannot see exposure. The retinal-hazard band ends near 1400 nm, but corneal and skin hazards remain, and single-mode power confined to a $\sim$`<!-- -->`{=html}9 μm core is high radiance even at modest milliwatt levels.

Short-reach datacom modules are usually engineered so each fiber port stays Class 1 or Class 1M under rated launch power. That is a design constraint on EML/DFB bias and on how much power each lane launches, not a label you add after the fact.

### Hazard level = aggregate, not per-lane

The safety case scales with *total* launched power at an accessible location, not with a single DFB data sheet. CW-WDM and ELS banks concentrate many lines on one MT or MPO ferrule (§ `sec:elsfp`). A connector that breaks out eight or sixteen fibers can exceed a per-lane Class 1 budget even when each lane is modest. IEC 60825-2 assigns hazard levels (1 through 4) to each accessible port in the OFCS based on the radiant power that could escape during service . That is why ELS architecture and fiber count drive classification, not the laser chip alone.

### Open-fiber protection: APR and ALS

When fiber continuity is lost, open connectors and broken fiber can expose hazardous power. *APR* (automatic power reduction) holds output at or below Hazard Level 1M and probes for re-mate with safe low-power pulses. *ALS* (automatic laser shutdown) cuts power entirely and was common on older SDH links; for modern high-power systems APR with automatic restart is the preferred pattern because restart probes stay within the hazard limit . ITU-T G.664 requires power reduction to Hazard Level 1M within about 3 s of a continuity break, a restart inhibit window, and restart only at safe power.

These mechanisms tie directly to CMIS and bring-up policy: lasers enable only when the host commands ModuleReady (§ `sec:bringup,sec:cmis`). APR/ALS is what makes a live ELSFP hot-swap survivable in a running rack (§ `sec:prod-corners`).

### What validation and ops owe

Optical safety is a validation deliverable, not a compliance sticker. ATP should verify APR/ALS trip threshold and timing on representative open-fiber faults; label modules and cages with the rated class; document max launched power per port and per MPO breakout; and write service procedures for multi-fiber connectors. At fleet scale, a hot-swap runbook that assumes ALS works but was never tested in ATP is a real hazard. Fold the APR/ALS check into the ELS hot-swap corner in § `sec:prod-corners` alongside mate-cycle and ORL tests.

## CW-WDM source validation

Multi-wavelength CW sources (CW-WDM MSA) feed dense ring or filter banks on a PIC (§ `sec:cwwdm,ch:wdm`). Validation is per-channel plus cross-channel:

- power flatness across $\lambda$ (uneven OMA after the modulator bank);

- per-channel SMSR and wavelength grid placement;

- channel crosstalk and residual ASE between lines;

- lock to microring resonances under temperature and neighbor heating (§ `sec:locking-techniques,sec:thermal-xtalk,sec:siring`);

- RIN and ORL sensitivity for each line (§ `sec:laser-params,sec:rin-values`).

Examples: Ayar Labs SuperNova (CW-WDM MSA-compliant, feeds TeraPHY)  ; Broadcom ELSFP banks on Tomahawk CPO (§ `sec:cpo-status,sec:elsfp`); quantum-dot comb lasers (Ranovus, Quintessent) aimed at many $\lambda$ from one chip. Source tests live here; locking and on-chip MUX live in § `ch:wdm`.

## The light-source supplier landscape

Who actually builds these lasers matters, because the light source is often the hardest and highest-value part of an optical link. The suppliers split along a strategic fork: put the laser *outside* the package as a serviceable module, or integrate it *into* the photonic chip.

Merchant laser chips (DFB / EML / high-power CW)

: the III-V chips inside most modules and sources: Lumentum (notably supplying lasers for NVIDIA Spectrum-X photonics), Coherent (collaborating with NVIDIA on silicon photonics), and the Japanese EML/CW specialists Sumitomo Electric, Mitsubishi Electric, Furukawa, and Fujitsu; also MACOM and Source Photonics.

External light-source modules (CW-WDM / ELSFP)

: the SuperNova peers: Ayar Labs (SuperNova, § `sec:cwwdm`), Broadcom's in-house ELSFP for its CPO switches, and POET Technologies' interposer-based light source.

Quantum-dot comb lasers

: a single chip emitting many wavelengths at once: Ranovus (Odin) and Quintessent, both aimed squarely at CW-WDM.

Lasers integrated on silicon

: III-V gain bonded into the PIC: Intel (hybrid silicon lasers, and an 8-wavelength integrated source for its optical compute interconnect), OpenLight with Tower Semiconductor, and startups such as Scintil, Nexus Photonics, and Aeluma.

[]

  -----------------------------------------------------------------------------------
  Approach                          Representative suppliers
  --------------------------------- -------------------------------------------------
  Merchant DFB/EML/CW chips         Lumentum, Coherent, Sumitomo, Mitsubishi, MACOM

  External CW-WDM / ELSFP modules   Ayar Labs, Broadcom, POET

  Quantum-dot comb lasers           Ranovus, Quintessent

  Lasers integrated on silicon      Intel, OpenLight/Tower, Scintil, Nexus, Aeluma
  -----------------------------------------------------------------------------------

**Table .** Light-source approaches and representative suppliers.

[^15]

## Why lasers are the reliability bottleneck

At the scale of a large optical fleet the laser is usually the reliability-limiting component. It is an active device with wear-out physics that passive optics and even photodiodes largely lack:

- *Catastrophic optical damage* (COD) at the facet.

- Gradual facet and active-region degradation (accelerated by temperature, following Arrhenius kinetics; § `sec:laser-aging`).

- EAM aging in EMLs; coupling and solder drift in packaged assemblies.

Because failures scale with the number of lasers, a fleet of $100{,}000$+ links turns a modest per-laser FIT rate into a steady stream of field failures (§ `sec:fit-example,sec:gr468`). The mitigations shape architecture: field-replaceable external laser sources (ELSFP, CW-WDM), redundancy, burn-in screening to weed out infant mortality, and derating (running lasers below their maximum to extend life).

## Engineering lens

### How it works

A laser is an active device with wear-out physics, which makes it both the first line of the link budget and the fleet's reliability bottleneck. The chapter's device families and LIV/SMSR/RIN measurements all serve one question: will this source stay in spec for years at temperature?

### How it is measured

Qualify the laser as a set of curves, not a room-temperature data-sheet point. Measure light-current-voltage (LIV), threshold current, slope efficiency, and rollover with a source-measure unit and power meter. Use an optical spectrum analyzer (OSA) for wavelength and side-mode suppression ratio (SMSR), a calibrated photodiode and spectrum analyzer for RIN, and a DCA for EML extinction, RLM, and TDECQ. Repeat across case temperature, bias, optical return loss, and aging time. The measurement details and ATP mapping are in § `sec:laser-params,tab:laser-meas,tab:atp-laser`; qualification uses the mechanism-based stress plan in § `sec:laser-aging,sec:gr468` .

### How it fails

Separate sudden death from gradual drift. Sudden dark output can be catastrophic optical damage, an open interconnect, electrostatic damage, or a failed bias path. Gradual failures include threshold rise, slope loss, SMSR collapse, mode hopping, wavelength drift, and EAM bias creep. Monitor-photodiode and thermoelectric-cooler failures can make a healthy laser look unstable because the control loop is using bad feedback or has run out of thermal range. Manufacturing adds die, wafer, lot, and assembly spread in every one of these terms.

\> \*\*Failure mode: Monitor photodiode drift\*\* \> \> \*\*Symptoms.\*\* Reported power falls or the bias loop moves, but an external power meter does not show the same change. \> \> \*\*Likely causes.\*\* Monitor-PD responsivity drift, transimpedance gain error, contamination in the monitor path, or a bad calibration coefficient. \> \> \*\*Measurements.\*\* External power meter, monitor current, bias current, LIV, and loop error versus temperature. \> \> \*\*Mitigations.\*\* Repair the monitor path or calibration, add disagreement alarms, and do not raise laser bias to compensate for a false reading.

### How it is debugged

For power degradation, compare external optical power, monitor current, bias, and case temperature before changing the setpoint. Rerun LIV at the failing temperature and compare it with ship data. If LIV moved, inspect SMSR, wavelength, and RIN to classify active-region, facet, or modal change. If LIV is stable, move to coupling, connector, monitor-PD, and control-loop checks. For a wavelength excursion, inspect OSA data and TEC current together. For a bias anomaly, replace the product driver with a quiet source before blaming the diode.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* BER worsened after thermal cycling while average optical power stayed in range. \> \> \*\*Investigation.\*\* The DCA showed that extinction ratio had collapsed. LIV and SMSR were unchanged, and an EAM bias sweep restored the eye. \> \> \*\*Finding.\*\* The light source was healthy, but its modulator operating point was wrong. \> \> \*\*Root cause.\*\* A calibration table used the wrong temperature segment after the cycle. \> \> \*\*Resolution.\*\* The table and screening limits were fixed, and EAM bias sweep data became part of the thermal-cycle readout.

## Interview and design review questions

##### Concept.

- Why is the laser typically the reliability-limiting component in an optical link?

- What physical mechanism causes a DFB laser's threshold current to rise with age?

- Why does an isolator-free design tighten the RIN requirement?

##### Design.

- Which aging model and activation energy match the observed failure mechanism?

- What are the distributions of threshold, slope, wavelength, SMSR, and RIN across wafer, lot, assembly site, and temperature?

- Which screens remove infant mortality, and what good units do those screens consume?

- Does the architecture make the laser field-replaceable, and what failure rate justifies that choice?

##### Debug.

- Optical power fell but the monitor photodiode reports no change. What do you check?

- BER worsened after thermal cycling while average power stayed in range. What is the most likely root cause?

- Which telemetry distinguishes laser wear from monitor, TEC, connector, and bias-driver faults in the fleet?

##### Manufacturing and operations.

- What are the process control limits and the supplier's reaction plan when a trend crosses them?

- How many HTOL hours at what temperature project 10 years of field life at your operating conditions?

- What lot-level data must the supplier provide at each NPI gate?

- What is the expected laser replacement rate for this fleet size and FIT?

**Key idea.** Measure LIV, SMSR, wavelength, and RIN as distributions across temperature, lot, and age. Tie each requirement to an ATP row, each life claim to a physical mechanism, and each field alarm to a measurement that separates the laser from its driver, monitor, cooler, and optical path.


<div class="nav-links">
  <a href="ch4-quantitative-models-noise-rin-and-ber">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch6-wdm-and-wavelength-locked-lasers">Next &rarr;</a>
</div>
