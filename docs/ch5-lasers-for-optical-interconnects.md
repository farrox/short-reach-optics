---
layout: default
title: "Ch 5: Lasers for optical interconnects"
---

# Lasers for optical interconnects

Every optical link begins with a light source, and at fleet scale that source is usually the reliability bottleneck as well as the first item on the link budget. Datacenter interconnects have spent two decades climbing from coarse multimode optics toward dense single-mode WDM and co-packaged engines; each step changed which laser family won and which measurements decided pass/fail. This chapter follows that arc: the device families in use today, how a roadmap choice becomes a measurable requirements slice, the LIV/SMSR/RIN suite, how bias drivers enter the intensity-noise budget, aging and derating, and the external laser modules (ELSFP, CW-WDM) that make co-packaged optics serviceable.

## Device families

The short-reach market does not use one laser. It uses a small set of families, each tuned to a reach, a fiber type, and a packaging style. Broadly, the industry moved from multimode VCSEL arrays inside the rack, to single-mode DFB/EML pluggables for DR/FR, to external CW sources feeding silicon or TFLN modulators for CPO and 400G/lane. The list below is the vocabulary you will meet on datasheets and in supplier meetings; later sections explain how to measure and qualify each one.

DFB (distributed feedback)

: a grating along the active region gives single-mode output; the workhorse continuous-wave (CW) or directly modulated source for CWDM and LAN-WDM ([5.3](#sec:dfb-eml)).

DBR (distributed Bragg reflector)

: the grating sits outside the gain region; enables tunable variants.

DML (directly modulated laser)

: modulate the bias current directly: cheap and low-power, but chirp-limited over dispersive fiber ([5.2](#sec:dml-vcsel)).

EML (externally modulated laser)

: *EML*: a DFB integrated with an *EAM*. Low chirp and high bandwidth make it the dominant 100--200G/lane transmitter for single-mode links at DR (500 m) and shorter ([\[sec:dfb-eml,sec:eml-eam\]](#sec:dfb-eml,sec:eml-eam)).

CW laser + TFLN MZM

: an external CW source feeds a thin-film lithium niobate Mach--Zehnder modulator on a separate chip. Very low chirp and $\gtrsim$`<!-- -->`{=html}100 GHz EO bandwidth make this the leading path to 400G/lane pluggables and high-baud FR links; see [\[sec:tfln-mzm,tab:tx-modulator\]](#sec:tfln-mzm,tab:tx-modulator).

CW laser + Si MZM

: an external CW source feeds a silicon Mach--Zehnder modulator on the same PIC ([3.14.3.0.7](#sec:simzm)). Low chirp, flat passband, and CMOS fab integration make this the default for 100--200G/lane DR/FR SiPh modules; 400G/lane demos appeared in 2026.

CW laser + Si ring

: same laser architecture, but a microring or microdisk modulator on the PIC ([3.14.3.0.6](#sec:siring)). Smaller footprint and strong WDM/CPO fit; wavelength lock and thermal crosstalk dominate validation ([6](#ch:wdm)).

CW-WDM / multi-wavelength sources

: high-power, multi-wavelength CW lasers (per the CW-WDM MSA) that feed comb-like WDM architectures ([\[sec:cwwdm-laser,sec:cwwdm\]](#sec:cwwdm-laser,sec:cwwdm)).

VCSEL

: 850--940 nm multimode sources for short-reach links over multimode fiber; cheap but reach-limited and less relevant at 200G/lane.

External laser source (ELS/ELSFP)

: a pluggable laser module supplying CW light to a co-packaged switch, so a failed laser is field-replaceable ([5.8](#sec:elsfp)).

## Directly modulated lasers and VCSELs

Before EMLs and silicon photonics took over single-mode datacenter ports, most volume optics were either a cheap *DML* on single-mode fiber or a *VCSEL* array into multimode fiber. Both still matter at the low-cost, short-reach edge of the market, and both show why chirp, modal bandwidth, and temperature push AI fabrics toward externally modulated single-mode sources.

A DML modulates laser bias current directly. The transmitter is simple and efficient, but the same carrier dynamics that make modulation easy also produce chirp: intensity changes drag the optical frequency along ([3.11](#sec:chirp-dispersion)). Over multimode or very short single-mode runs that is often acceptable. Over dispersive single-mode fiber at tens of GBd, the chirp turns into inter-symbol interference and closes the eye. Validation therefore focuses on extinction ratio, pattern-dependent chirp, and RIN, not just average power.

VCSELs took a different path. They emit from a vertical cavity at 850--940 nm straight into multimode fiber, so parallel arrays are easy to assemble and cheap to ship. That combination made VCSEL SR optics the default for early 40G/100G Ethernet inside the rack (100G-SR4 and its cousins): short ribbons of MMF, high lane count, low dollars per gigabit. The same physics that made them attractive also capped their future. Multimode fiber has modal bandwidth and modal noise limits; VCSEL bandwidth and reliability both degrade with temperature; and as lane rates climb toward 100 G and 200 G, those limits arrive sooner. The industry response has been incremental (better OM4/OM5 fiber, tighter specs, sometimes PAM4 on MMF) rather than a clean leap to 400G/lane SMF DR. In practice, MMF reach and modal dispersion keep VCSEL links in the SR box ([3.13](#sec:pmd-reach)), while hyperscale AI fabrics standardize on single-mode DR/FR and CPO.

Neither family is the path to 400G/lane SMF DR. EMLs and external modulators ([\[sec:dfb-eml,sec:simzm,tab:tx-modulator\]](#sec:dfb-eml,sec:simzm,tab:tx-modulator)) own that space. Pattern-aware chirp linearization can stretch a DML a little farther, but it does not change the physics at FR distances: if you need low chirp and high EO bandwidth at fleet scale, you leave direct modulation behind.

## DFB and EML: the workhorse transmitters

Once single-mode DR/FR became the hyperscale default, most short-reach ports started with an InP laser chip. Two configurations still dominate production: the CW or directly modulated DFB, and the EML that adds an electro-absorption modulator on the same die.

##### DFB.

A distributed-feedback laser has a grating along the active region that selects one longitudinal mode. Spec-sheet metrics that matter in bring-up are threshold current, slope efficiency, SMSR (typically many tens of dB on a clean part), RIN, and wavelength vs. temperature/current. Used as a CW source for SiPh or TFLN modulators, or as a DML when chirp is acceptable ([5.2](#sec:dml-vcsel)). Uncooled datacom DFBs ride case temperature with a known $d\lambda/dT$; cooled parts add a TEC and lock to a grid.

##### EML.

An electro-absorption modulated laser integrates a DFB with an *EAM* on one chip ([3.14.3.0.9](#sec:eml-eam)). Reverse bias on the EAM sets absorption and extinction; chirp stays far below a DML. That combination, not marketing, is why EMLs became the volume answer for 100G/lane and then 200G/lane DR/FR pluggables: one chip, low chirp, mature supply chain. Validation adds EAM bias sweeps, aging of the absorption curve, and driver-match checks on top of the DFB LIV/SMSR/RIN suite ([\[sec:laser-params,sec:laser-aging\]](#sec:laser-params,sec:laser-aging)).

##### When to pick which.

Through 200G/lane DR, EML usually wins on cost and integration. A CW DFB (or ELSFP/CW-WDM bank) plus Si MZM, ring, or TFLN wins when the modulator must sit on silicon or needs $\gtrsim$`<!-- -->`{=html}100 GHz EO bandwidth ([\[tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm\]](#tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm)). At CPO scale the laser often leaves the optical engine entirely so it can be replaced without pulling the ASIC package ([5.8](#sec:elsfp)). Looking forward, 400G/lane pluggables are pushing harder toward external CW plus TFLN or high-BW silicon modulators, while EMLs remain the workhorse of the installed 100--200G base.

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

## Laser requirements: from roadmap to specs

Laser requirements only work when they are numbers a supplier can fail and a link budget can close. Start from the interconnect roadmap choice, then fill a short requirements slice; the ATP in [8.7](#sec:supplier-exec) is how that slice is enforced on every lot.

##### Roadmap forks that set the laser.

Each architecture decision forces a different requirements set ([5.2](#tab:laser-req-fork)):

[]

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Roadmap choice                      Laser implication                           Specs you must freeze early
  ----------------------------------- ------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Pluggable EML vs CW+Si/TFLN         Integrated EAM vs external CW + modulator   EAM bias/aging and TDECQ vs CW power class, RIN, and modulator $V_\pi$ match

  On-package laser vs ELSFP/CW-WDM    Field replace vs FIT inside the package     Connector/ORL/mate cycles and hot-swap CMIS vs COD/aging inside ASIC thermal

  Isolator vs isolator-free (CPO)     Feedback tolerance vs quiet RIN only        Stressed $\mathrm{RIN}_x\mathrm{OMA}$ at stated ORL; monitor PD / lock policy

  Single-$\lambda$ vs CW-WDM / comb   One line vs $N$ lines into rings/filters    Per-line power flatness, SMSR, grid, crosstalk ([5.10](#sec:cwwdm-laser))

  Retimed vs LPO                      Module DSP hides Tx vs host sees raw eye    Laser+modulator TDECQ/RLM floor vs host COM budget ([\[sec:com,sec:drivers\]](#sec:com,sec:drivers))

  Derate policy                       Operating $I$, $T$, power below abs-max     Bias window, thermal class, FIT/$E_a$ assumptions ([5.7](#sec:laser-aging))
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Architecture forks and the laser specs each one forces. Freeze these before DVT samples are built ([8.7](#sec:supplier-exec)).

##### One-page requirements slice.

[5.3](#tab:laser-prd) is the PRD-sized list. Fill every row with a number (or an explicit "N/A for this architecture") before you negotiate ATP limits. Do not leave RIN without an ORL, or power without a case-temperature class.

[]

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Parameter                How to set the number                                                                                                           Measure / ATP              Reject if                            Derate / ops note
  ------------------------ ------------------------------------------------------------------------------------------------------------------------------- -------------------------- ------------------------------------ ----------------------------------------------------------------------------------------------------------------
  Launch power / class     Link budget + connector loss + aging margin ([7.6](#sec:link-budget))   Power meter; ELSFP class   Below min at rated $T$               Cap max power for COD

  Wavelength / grid        PMD or ring FSR plan; $d\lambda/dT$ headroom ([6](#ch:wdm))                      OSA / wavemeter            Off-grid at case $T$                 TEC setpoints

  SMSR floor               Datasheet + modal-noise budget                                                                                                  OSA                        Below floor at $T$                   Watch aging

  RIN (quiet + stressed)   BER floor vs BW ([4.3](#sec:rin)); ORL from plant                               PD+ESA; stated ORL         Above limit at ORL                   Bias-driver noise budget ([5.6](#sec:laser-drivers))

  Bias window              LIV kink-free range at max case $T$                                                                                             LIV                        Kink in window                       Run below abs-max $I$

  EAM / MZM (if any)       ER, RLM, TDECQ at baud ([7.3](#sec:tdecq))                                    DCA + bias sweep           TDECQ/RLM fail                       Bias aging policy

  ORL / isolator           Architecture: isolator-free needs tighter RIN                                                                                   ORL meter; mate cycles     ORL out of range                     Cleaning / ELS mate life

  CMIS monitors            What fleet triage will read ([7.10](#sec:fleet-triage))                CMIS dump                  Missing alarms / bad state machine   Enable sequence ([7.8](#sec:bringup))

  FIT / life               Fleet failures/day target ([5.7.0.0.4](#sec:fit-example))               GR-468 + $E_a$             Screen escape                        Burn-in depth; ELS replace
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Laser requirements one-pager. Every cell needs a program number; this table is the structure, not the limits.

##### How to fill numbers (method, not invention).

Work backward from the link, not forward from a marketing slide. The four steps below turn an architecture choice into ATP limits:

1.  Close the optical ledger at target pre-FEC BER ([\[sec:link-budget,sec:kp4\]](#sec:link-budget,sec:kp4)). That sets minimum launch OMA/power and maximum allowed penalties (transmitter and dispersion eye closure quaternary, TDECQ; ORL/RIN).

2.  From receiver BW and the RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$ ([4.3](#sec:rin)), set a stressed RIN limit with margin under the plant ORL you will actually see (not only a quiet bench).

3.  From case-temperature and derating policy, set the LIV bias window and thermal class so the laser never sits on a kink or at abs-max in the fleet ([\[sec:laser-aging,sec:prod-corners\]](#sec:laser-aging,sec:prod-corners)).

4.  From service model, choose ELSFP mate-cycle / hot-swap requirements or accept on-package FIT and write COD/aging screens accordingly ([5.8](#sec:elsfp)).

Hand the filled slice to the supplier with the ATP checklist ([8.3](#tab:atp-laser)). If a roadmap slide cannot point to a row in [5.3](#tab:laser-prd), the requirement is not real yet.

**Key idea.** Laser leadership is a requirements sheet: architecture forks force specific specs (power, grid, RIN@ORL, SMSR, bias window, CMIS, FIT). Fill [5.3](#tab:laser-prd) from the link budget and fleet model, then enforce it with the ATP ([8.7](#sec:supplier-exec)).

## LIV, SMSR, and RIN: the measurement playbook

These three measurements decide whether a laser chip or module is usable. The instruments are standard; the skill is knowing which failure each one catches.

##### LIV (light--current--voltage).

The LIV curve plots optical power and forward voltage versus bias current. Read off threshold $I_\mathrm{th}$, slope efficiency (mW/mA above threshold), kink-free operating range, and thermal rollover at high current or high case temperature. [5.1](#fig:liv-sketch) is a labeled schematic (not measured data).

High-temp LIV failures look like: $I_\mathrm{th}$ rise, slope collapse, early rollover, or a kink that moves into the bias window. Those map to aging, TEC saturation, or package thermal resistance ([5.7](#sec:laser-aging)).

::::
![](figures/fig_liv_sketch.pdf){width="85%"}

::: caption
Schematic LIV curve with threshold, slope, kink, and thermal rollover labeled. Idealized for teaching; use measured LIV for pass/fail. []
:::
::::

##### SMSR (side-mode suppression ratio).

SMSR is the power difference (dB) between the lasing mode and the strongest side mode on an optical spectrum analyzer (OSA). Datacom single-mode parts require high SMSR so side modes do not steal power or seed modal noise. Spec-sheet floors are part-specific; treat the datasheet or ATP limit as authoritative. SMSR collapse under temperature or aging is a reject: the laser is leaving single-mode operation.

##### RIN (relative intensity noise).

Measure RIN with a calibrated photodetector and RF spectrum analyzer (or a dedicated RIN analyzer), under a controlled optical return loss. Distinguish *intrinsic* RIN (quiet bench, high ORL) from stressed $\mathrm{RIN}_x\mathrm{OMA}$ used in Ethernet/MSA specs. IEEE 802.3 / 100G Lambda class links cap $\mathrm{RIN}_{17.1}\mathrm{OMA}$ at $-136$ dB/Hz with 17.1 dB ORL . Quiet datacom DFB/EML parts typically sit well below that when feedback is controlled; CPO ELS designs care as much about feedback tolerance as about the quiet number ([\[sec:rin-values,sec:rin\]](#sec:rin-values,sec:rin)).

[]

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Parameter           Instrument                               Pass/fail intent                                                                                                                Failure signature
  ------------------- ---------------------------------------- ------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------
  LIV                 SMU + power meter / integrating sphere   $I_\mathrm{th}$, slope, kink-free bias window                                                                                   high-temp rollover; kink in bias range

  SMSR                OSA                                      single-mode purity vs. datasheet/ATP                                                                                            side modes rise with $T$ or age

  RIN                 PD + ESA / RIN analyzer                  intrinsic and stressed $\mathrm{RIN}_x\mathrm{OMA}$                                                                             RIN rises with ORL; BER floor ([4.3](#sec:rin))

  Bias-driver noise   SMU vs. product bias board               $\mathrm{RIN}_{\mathrm{eq}}$ from $i_n$ ([5.6](#sec:laser-drivers))   RIN rises with rails on, flat vs. ORL

  Wavelength          OSA / wavemeter                          grid placement, $d\lambda/dT$, $d\lambda/dI$                                                                                    walk off ring or MSA grid

  EAM bias (EML)      bias sweep + DCA/TDECQ                   extinction, chirp, RLM                                                                                                          aging shifts absorption curve
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Table .** Laser measurement playbook: what to measure, with what, and what failure looks like.

## Laser drivers and the RIN budget

Modulator RF drivers ([3.14.3.0.10](#sec:drivers)) deliver swing and bandwidth into an EAM or MZM. Laser *bias* drivers are a different circuit: they set a quiet constant current into the diode. Current noise on that path becomes optical intensity noise and adds in the RIN budget of [4.3](#sec:rin). Confusing the two is a common debug miss: a great SiGe PAM4 driver can still ruin a CW laser if its supply or ground couples into the bias rail.

##### From current noise to equivalent RIN.

Above threshold, optical power tracks bias approximately as $P\propto(I-I_\mathrm{th})$. Relative intensity fluctuations then track relative current fluctuations: $$\mathrm{RIN}_{\mathrm{eq,lin}}
\;\approx\;
\left(\frac{i_n}{I-I_\mathrm{th}}\right)^{\!2},
\qquad
\mathrm{RIN}_{\mathrm{eq}}[\mathrm{dB/Hz}]
\;=\;
20\log_{10}\!\left(\frac{i_n}{I-I_\mathrm{th}}\right),$$ where $i_n$ is the one-sided current-noise density in A$/\sqrt{\mathrm{Hz}}$ at the laser terminals (driver plus board pickup). The approximation assumes linear slope efficiency and ignores intrinsic laser dynamics; it is a budget tool, not a device model.

Worked numbers at $I-I_\mathrm{th}=50$ mA (typical CW DFB window): $i_n=500$ pA$/\sqrt{\mathrm{Hz}}$ maps to $\mathrm{RIN}_{\mathrm{eq}}\approx-160$ dB/Hz; $270$ pA$/\sqrt{\mathrm{Hz}}$ maps to about $-165$ dB/Hz. Commercial low-noise laser drivers quote roughly $50$--$500$ pA$/\sqrt{\mathrm{Hz}}$ at 1 kHz depending on current range ([5.5](#tab:laser-driver-noise)); the Koheron DRV200 family is a concrete example . Against a good datacom intrinsic RIN of $-145$ to $-155$ dB/Hz ([4.3.1](#sec:rin-values)), those 1 kHz densities look comfortable. The budget tightens when $(I-I_\mathrm{th})$ is small (near threshold, derated CW, or low-current VCSELs), when you integrate broadband switching noise rather than a 1 kHz spot, or when SerDes/DSP rails dump discrete tones onto the bias network.

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

For external CW sources feeding Si or TFLN modulators, design the bias path as a low-noise current source with high supply rejection, local decoupling at the diode, and a star ground that does not share return with SerDes switching currents. Automatic power control () loops that close through a monitor PD suppress slow drift; keep the loop bandwidth well below the RIN measurement band and quiet enough that the loop itself does not inject intensity noise. ELSFP and CW-WDM modules hide this circuitry inside the pluggable ([\[sec:elsfp,sec:cwwdm-laser\]](#sec:elsfp,sec:cwwdm-laser)); acceptance still needs module-level RIN with the host bias and management rails connected, not only a quiet SMU on the bare die.

##### DML and EML.

A *DML* shares one diode for bias and RF: a bias tee (or on-chip bias network) combines a quiet DC source with the RF driver. Excess RF driver broadband noise, poor tee isolation, or supply ripple on the bias arm all raise measured RIN and chirp-related penalties. An *EML* splits the problem: keep the DFB bias as quiet as a CW source, and treat the EAM RF driver under [3.14.3.0.10](#sec:drivers). EAM drive amplitude sets extinction and chirp; DFB bias noise still lands in optical intensity before the modulator.

##### What to measure on the bench.

Bisect electrical vs. optical RIN:

1.  Measure intrinsic RIN with a quiet SMU or known low-noise driver and high ORL ([5.5](#sec:laser-params)).

2.  Repeat with the product bias board / module rails connected. Any rise is driver or supply contribution, not laser physics.

3.  Sweep ORL. Rise with reflection is feedback-driven laser RIN ([4.3.1](#sec:rin-values)); rise independent of ORL points at the electrical path.

4.  Look for discrete spurs on the ESA (switching frequencies, CMIS clocks). Spurs fail stressed $\mathrm{RIN}_x\mathrm{OMA}$ even when the broadband floor looks fine ([4.3.1](#sec:rin-values)).

**Key idea.** Treat laser bias noise as a RIN term: $\mathrm{RIN}_{\mathrm{eq}}\approx(i_n/(I-I_\mathrm{th}))^2$. Quiet CW drivers at tens to hundreds of pA$/\sqrt{\mathrm{Hz}}$ usually sit under a $-145$ dB/Hz intrinsic floor at 50 mA; digital supply pickup, near-threshold bias, and DML bias-tee leakage are what actually burn the budget.

## Aging curves, derating, and fleet FIT

Lasers wear out. At fleet scale that is not a footnote; it sets architecture (ELSFP vs. integrated laser) and operating policy (derating, burn-in).

##### Observable aging signatures.

Watch LIV and spectrum over HTOL or field life:

- threshold rise and slope drop (active-region / facet degradation);

- SMSR collapse (mode competition);

- EAM bias creep on EMLs (absorption curve shift $\to$ TDECQ/RLM drift);

- RIN rise under feedback (ORL or isolator failure);

- COD (catastrophic optical damage) at the facet under overstress.

Each signature should appear in the ATP and in field telemetry triage ([\[sec:fleet-triage,sec:gr468\]](#sec:fleet-triage,sec:gr468)).

##### Arrhenius life projection.

Telcordia GR-468-CORE qualifies optoelectronic parts with accelerated stress (HTOL, temperature cycle, damp heat) and projects field life with Arrhenius acceleration : $$\mathrm{AF}
= \exp\!\left[\frac{E_a}{k_B}\left(\frac{1}{T_\mathrm{use}}-\frac{1}{T_\mathrm{stress}}\right)\right],$$ where $E_a$ is the activation energy for the wear-out mechanism under test, $k_B$ is Boltzmann's constant, and temperatures are absolute. Document $E_a$, sample size, and confidence bounds when converting a 1000-hour HTOL lot into field-year FIT. Activation energies are mechanism-specific; use the value justified in the qual plan, not a generic number copied from another product.

##### Derating.

Run below absolute-max current, case temperature, and optical power. Derating extends wear-out life and reduces COD risk. Uncooled datacom parts already sit near thermal limits at high case temperature; cooled or faceplate ELSFP modules ([5.8](#sec:elsfp)) buy headroom by moving heat off the ASIC package.

##### Worked FIT example (assumptions labeled).

FIT is failures per $10^9$ device-hours. For illustration only, assume 50 FIT per laser (confirm against your supplier qual; do not treat 50 as a measured claim) and a fabric with $5\times10^5$ lasers (order-of-magnitude for a large AI cluster with several optical links per accelerator). Expected failures per day: $$\frac{5\times10^5 \times 50 \times 24}{10^9}
\approx 0.6\ \text{laser failures/day}.$$ That is why field-replaceable ELSFP modules, burn-in screens, and derating are design inputs, not afterthoughts ([8](#ch:reliability)).

## ELS and ELSFP: architecture, pinout, qual

*ELSFP* (External Laser Small Form-Factor Pluggable) is the OIF form factor for faceplate-pluggable CW laser modules that feed co-packaged optical engines . The lasers sit at the coolest part of the system (front panel), hot-swap when they fail, and keep thermal load off the ASIC and photonic engine.

##### Mechanical and optical.

The module uses a card-edge electrical interface and a blind-mate multi-fiber optical connector at the rear (MT-class ferrules), which improves eye safety for high CW power by keeping live fiber inside the chassis . One ELSFP can feed more than one optical engine. OIF defines optical power classes, thermal classes, and wavelength assignments (e.g. DR-type 1311 nm and FR-type CWDM4 grids) so hosts and modules interoperate.

##### Management and hot-swap.

ELSFP uses CMIS and the CMIS module state machine over TWI. On plug-in the module resets, initializes management, and stays in low-power mode with lasers *off* until the host transitions it to ModuleReady and explicitly enables lasers . `ModPrsL` and `IntL` support presence detect and asynchronous alarms for safe hot-swap.

##### Electrical pinout (OIF-ELSFP-02.0 Table 7).

Twenty-four contacts: multiple 3.3 V VCC and GND pins, module reset (`ResetL`), low-power mode (`LPModeL`), two-wire serial management (`SCL`/`SDA`), presence (`ModPrsL`), and interrupt (`IntL`), plus reserved pins for future power/ground . [5.6](#tab:elsfp-pins) summarizes the published map.

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

Acceptance test plans should cover the checklist in [\[tab:atp-laser,sec:supplier-exec\]](#tab:atp-laser,sec:supplier-exec): laser LIV/SMSR/RIN inside the module; optical power-class compliance; connector mating cycles and contamination/ORL; burn-in before ship; CMIS register sanity; and thermal class at rated case temperature. Module bring-up must also prove the CMIS enable sequence and ModuleReady laser policy ([7.8](#sec:bringup)). Field returns split between laser wear-out and connector/fiber-attach faults; keep both in the triage tree ([7.10](#sec:fleet-triage)).

## Optical safety and laser classes

### Hazard and laser classes

Laser safety for interconnects is governed by IEC 60825-1 (laser product classification) and IEC 60825-2 (optical-fiber communication systems, OFCS) . Classes run from Class 1 (safe under normal use) through Class 1M (safe unless the beam is collected by optics), Class 3R/3B, and Class 4. At 1310 nm and 1550 nm the beam is invisible, which raises the operational risk: technicians cannot see exposure. The retinal-hazard band ends near 1400 nm, but corneal and skin hazards remain, and single-mode power confined to a $\sim$`<!-- -->`{=html}9 μm core is high radiance even at modest milliwatt levels.

Short-reach datacom modules are usually engineered so each fiber port stays Class 1 or Class 1M under rated launch power. That is a design constraint on EML/DFB bias and on how much power each lane launches, not a label you add after the fact.

### Hazard level = aggregate, not per-lane

The safety case scales with *total* launched power at an accessible location, not with a single DFB data sheet. CW-WDM and ELS banks concentrate many lines on one MT or MPO ferrule ([5.8](#sec:elsfp)). A connector that breaks out eight or sixteen fibers can exceed a per-lane Class 1 budget even when each lane is modest. IEC 60825-2 assigns hazard levels (1 through 4) to each accessible port in the OFCS based on the radiant power that could escape during service . That is why ELS architecture and fiber count drive classification, not the laser chip alone.

### Open-fiber protection: APR and ALS

When fiber continuity is lost, open connectors and broken fiber can expose hazardous power. *APR* (automatic power reduction) holds output at or below Hazard Level 1M and probes for re-mate with safe low-power pulses. *ALS* (automatic laser shutdown) cuts power entirely and was common on older SDH links; for modern high-power systems APR with automatic restart is the preferred pattern because restart probes stay within the hazard limit . ITU-T G.664 requires power reduction to Hazard Level 1M within about 3 s of a continuity break, a restart inhibit window, and restart only at safe power.

These mechanisms tie directly to CMIS and bring-up policy: lasers enable only when the host commands ModuleReady ([\[sec:bringup,sec:cmis\]](#sec:bringup,sec:cmis)). APR/ALS is what makes a live ELSFP hot-swap survivable in a running rack ([7.8.0.0.2](#sec:prod-corners)).

### What validation and ops owe

Optical safety is a validation deliverable, not a compliance sticker. ATP should verify APR/ALS trip threshold and timing on representative open-fiber faults; label modules and cages with the rated class; document max launched power per port and per MPO breakout; and write service procedures for multi-fiber connectors. At fleet scale, a hot-swap runbook that assumes ALS works but was never tested in ATP is a real hazard. Fold the APR/ALS check into the ELS hot-swap corner in [7.8.0.0.2](#sec:prod-corners) alongside mate-cycle and ORL tests.

## CW-WDM source validation

Multi-wavelength CW sources (CW-WDM MSA) feed dense ring or filter banks on a PIC ([\[sec:cwwdm,ch:wdm\]](#sec:cwwdm,ch:wdm)). Validation is per-channel plus cross-channel:

- power flatness across $\lambda$ (uneven OMA after the modulator bank);

- per-channel SMSR and wavelength grid placement;

- channel crosstalk and residual ASE between lines;

- lock to microring resonances under temperature and neighbor heating ([\[sec:locking-techniques,sec:thermal-xtalk,sec:siring\]](#sec:locking-techniques,sec:thermal-xtalk,sec:siring));

- RIN and ORL sensitivity for each line ([\[sec:laser-params,sec:rin-values\]](#sec:laser-params,sec:rin-values)).

Examples: Ayar Labs SuperNova (CW-WDM MSA-compliant, feeds TeraPHY)  ; Broadcom ELSFP banks on Tomahawk CPO ([\[sec:cpo-status,sec:elsfp\]](#sec:cpo-status,sec:elsfp)); quantum-dot comb lasers (Ranovus, Quintessent) aimed at many $\lambda$ from one chip. Source tests live here; locking and on-chip MUX live in [6](#ch:wdm).

## The light-source supplier landscape

Who actually builds these lasers matters, because the light source is often the hardest and highest-value part of an optical link. The suppliers split along a strategic fork: put the laser *outside* the package as a serviceable module, or integrate it *into* the photonic chip.

Merchant laser chips (DFB / EML / high-power CW)

: the III-V chips inside most modules and sources: Lumentum (notably supplying lasers for NVIDIA Spectrum-X photonics), Coherent (collaborating with NVIDIA on silicon photonics), and the Japanese EML/CW specialists Sumitomo Electric, Mitsubishi Electric, Furukawa, and Fujitsu; also MACOM and Source Photonics.

External light-source modules (CW-WDM / ELSFP)

: the SuperNova peers: Ayar Labs (SuperNova, [6.6](#sec:cwwdm)), Broadcom's in-house ELSFP for its CPO switches, and POET Technologies' interposer-based light source.

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

- Gradual facet and active-region degradation (accelerated by temperature, following Arrhenius kinetics; [5.7](#sec:laser-aging)).

- EAM aging in EMLs; coupling and solder drift in packaged assemblies.

Because failures scale with the number of lasers, a fleet of $100{,}000$+ links turns a modest per-laser FIT rate into a steady stream of field failures ([\[sec:fit-example,sec:gr468\]](#sec:fit-example,sec:gr468)). The mitigations shape architecture: field-replaceable external laser sources (ELSFP, CW-WDM), redundancy, burn-in screening to weed out infant mortality, and derating (running lasers below their maximum to extend life).

**Key idea.** Measure LIV, SMSR, and RIN on every laser path; write the requirements slice in [5.4](#sec:laser-reqs) before DVT; budget bias-driver noise against the same RIN floor ([5.6](#sec:laser-drivers)); project aging with Arrhenius and derate in the field; prefer ELSFP/CW-WDM when fleet FIT and hot-swap matter. At gigawatt scale the laser is still the part most likely to bring a link down.


<div class="nav-links">
  <a href="ch4-quantitative-models-noise-rin-and-ber">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch6-wdm-and-wavelength-locked-lasers">Next &rarr;</a>
</div>
