---
layout: default
title: "Ch 9: Advanced Packaging for Optical Engines"
---

# 9 Advanced Packaging for Optical Engines

This chapter is the design judgment home for short-reach optical packaging: what 2.5D and 3D actually mean, why co-packaged optics is a placement choice rather than a stack recipe, and how thermal partitioning, known-good die, yield, fiber attach, and serviceability decide whether the engine ships. Program status, shipping CPO products, and XPO hedges stay in Appendix H, Appendix H.10, Appendix H.11. External laser modules live in §7.14. SerDes reach classes and module styles are in §3.7, Appendix H.5.1, Appendix H.3.

*Read first:* 2.5D versus 3D, CPO is not automatically 3D, thermal partitioning, and known-good-die / yield.

*Deep dive:* placement ladder energy and serviceability in Table H.4; ELSFP architecture in §7.14; COUPE and vendor programs in Appendix H.10.

**Key idea.** CPO means the optical engine sits in or next to the ASIC package. It may use 2.5D, 3D, substrate-mounted engines, or an interposer. Do not equate CPO with vertical stacking. The first packaging question is which impairment you are buying: electrical reach, thermal access, yield, or field service.

## Define the terms carefully

### 2.5D integration

*2.5D* integration places multiple dies side by side on a shared platform: a silicon interposer, an organic interposer, a bridge die, or a redistribution layer. Communication is primarily lateral through dense interconnect. Chiplets, HBM stacks beside logic, and photonics sitting next to a switch ASIC are common 2.5D patterns. Electrical reaches are short compared with a faceplate VSR run, but the dies still sit in one plane for heat extraction and often for separate test before attach.

### 3D integration

*3D* integration stacks dies vertically using hybrid bonding, microbumps, through-silicon vias, or face-to-face / face-to-back bonds. Communication is vertical and very dense. Bandwidth density rises; thermal access and test access get harder. Stack yield can multiply die yields, so known-good-die strategy becomes critical. Optical I/O through a tall stack is not automatic. Fiber exit, laser placement, and heat paths must be designed into the stack, not assumed.

### Co-packaged optics

*Co-packaged optics* places optical engines in the same package as the switch or accelerator ASIC, or close enough that the electrical hop is XSR-class millimeters rather than VSR-class host traces (Table H.4, §3.14). CPO may use:

- 2.5D integration (engine beside the ASIC on an interposer or substrate);

- 3D integration (electronics bonded onto photonics, or the reverse);

- substrate-mounted optical engines without a full interposer;

- interposer-attached photonic I/O;

- external laser sources feeding the package (§7.14).

The interview trap is "CPO means 3D hybrid bonding." That is one recipe, not the definition. Ask what electrical reach, thermal budget, and serviceability the design actually bought.

## 2.5D versus 3D

<table class="book-table"><tr><th>Topic</th><th>2.5D</th><th>3D</th></tr><tr><td>Electrical reach</td><td>Short lateral links</td><td>Very short vertical links</td></tr><tr><td>Bandwidth density</td><td>High</td><td>Extremely high</td></tr><tr><td>Thermal access</td><td>Easier</td><td>Harder</td></tr><tr><td>Test access</td><td>Better</td><td>More difficult</td></tr><tr><td>Known-good-die strategy</td><td>More manageable</td><td>Critical and harder</td></tr><tr><td>Yield interaction</td><td>Dies can be screened separately</td><td>Stack yield can multiply</td></tr><tr><td>Repairability</td><td>Better</td><td>Poor</td></tr><tr><td>Optical access</td><td>Often easier</td><td>Depends strongly on stack</td></tr><tr><td>Package complexity</td><td>High</td><td>Very high</td></tr><tr><td>Best use</td><td>Chiplets, HBM, adjacent photonics</td><td>Dense logic/memory or bonded electronics-photonics</td></tr></table>
Interview memory: 2.5D is side-by-side with lateral wiring. 3D is stacked with vertical wiring. CPO can use either. Thermal and KGD often decide before bandwidth density does.

## Optical-engine packaging issues

Once the stack style is named, the engine still has to close a list of hard physical problems.

Fiber attach / FAU

: Fiber-array units set coupling loss, polarization alignment, and lane-to-lane uniformity. A one-channel FAU miss looks like a dark lane after the package is sealed.

Optical I/O orientation

: Edge coupling, grating coupling, and vertical fiber exits fight different keep-out zones, lid designs, and board clearances.

Thermal isolation

: Lasers hate the ASIC hotspot. Rings and filters drift with local heaters and neighbor channels (Chapter 8, Chapter 7). Partition heat deliberately.

Modulator temperature

: Resonant modulators transfer package thermal gradient into wavelength and OMA control burden.

PD/TIA proximity

: Co-packaging the detector with the TIA cuts capacitance and noise (Chapter 6). Bondwire length is a noise budget line, not a drawing convenience.

Bump pitch and RF loss

: Dense electrical interfaces buy bandwidth and spend SI margin. Package discontinuities show up as EQ and COM problems (Chapter 5).

Power delivery

: Optical engines and SerDes share rails and return paths with a multi-hundred-watt ASIC. Supply noise becomes optical margin.

Warpage

: Large packages warp over reflow and temperature. Alignment and bump reliability move with the warp.

Known-good die

: Screen dies before you stack or co-package them when you can. A bad photonic engine bonded to a good switch scrapes both.

Assembly yield

: Optical attach, underfill, lid, and fiber steps often dominate module cost more than the PIC wafer.

Test strategy

: Define what you measure before lid attach, after fiber attach, and at system bring-up. Late discovery is expensive.

Serviceability

: Decide what fails in the field and what you can replace: laser module, fiber jumper, whole package, or nothing.

## Co-packaging tradeoffs

Moving optics onto the package buys and spends at the same time.

##### What you buy.

- Shorter SerDes reach (XSR-class) and lower electrical energy per bit (Table H.4, Appendix H.13).

- Higher shoreline bandwidth density than a faceplate cage farm.

- Less host-board SI pain for the optical hop.

##### What you spend.

- Thermal coupling to a large ASIC: rings walk, lasers age faster if left on-package, lock loops fight neighbors.

- Package and assembly yield: one bad optical attach can scrap an expensive switch package.

- Fiber management at the package edge instead of at a pluggable cage.

- Harder test access after final assembly.

- Field replacement: soldered engines are not hot-swappable; that is why many CPO recipes pull lasers into ELSFP banks (§7.14).

XPO and pluggable hedges exist because some fleets still want faceplate serviceability while they close CPO yield and thermal stories (Appendix H.11, Appendix H.3). Productization then has to prove the factory can reproduce the package claim (Chapter 10).

### External versus integrated lasers

Three common laser placements:

On-engine / on-PIC

: Shortest optical path; hottest and least serviceable. Attractive when reliability and thermal headroom are proven.

On-package but separated

: Laser die near the engine with some thermal isolation. Compromise on coupling length versus heat.

External (ELS / ELSFP)

: Lasers at the cool faceplate, fiber or waveguide into the package. Best serviceability and laser ambient; adds coupling, connectors, and shared-source failure domains (§7.14).

Interview line: "I choose laser placement from thermal life and field replaceability first, then from coupling loss. Power per bit alone does not pick the architecture."

## Placement ladder

Read the optics-placement ladder once as a design menu, not as a chronology you must climb:

<table class="book-table"><tr><th>Step</th><th>Design question</th></tr><tr><td>Pluggable</td><td>Can faceplate serviceability and VSR SI still close?</td></tr><tr><td>OBO / COBO</td><td>Is mid-board optics worth losing hot-swap?</td></tr><tr><td>NPO</td><td>Engine beside ASIC on substrate: enough reach cut?</td></tr><tr><td>CPO</td><td>XSR die-to-engine worth package yield and thermal risk?</td></tr><tr><td>Interposer optical I/O</td><td>On-package photonics with almost no copper left?</td></tr></table>
Table H.4 carries energy-per-bit and serviceability numbers. Appendix H.10 carries who is shipping what. This chapter asks whether your constraints match the step you named.

Copper counter-moves (CPC / NPC) push the crossover outward for one more rate generation (Appendix H). They do not erase the packaging trade when reach or port count forces optics inward.

## Thermal and power design for optical engines

Package thermal design is not a heatsink footnote.

- Map ASIC hotspot, optical-engine location, and laser location on one sketch.

- Budget junction temperature for lasers separately from case temperature for the module (Chapter 7).

- Treat microring heaters as both actuators and heat sources (Chapter 8).

- Liquid cooling at the rack does not automatically cool a laser buried under a lid next to a switch die.

- Power delivery noise and simultaneous switching can look like optical BER if supplies are shared carelessly.

Appendix H.13.1, Appendix H.13 expand fabric-level envelopes. Here the rule is local: if the optical engine sees the ASIC thermal gradient, wavelength and life margins shrink even when the room looks fine.

## Known-good die, yield, and test before assembly

A whiteboard packaging answer that skips test is incomplete.

1.  Screen ASICs and optical engines as far as probe, known-good-die, and partial assembly allow.

2.  Define optical attach metrics before lid seal: coupling loss, dark lanes, polarization, monitor PD continuity.

3.  Keep a rework path where the business case allows it. Pure 3D stacks often do not.

4.  Plan system-level bring-up that can still localize package versus host versus fiber plant (Chapter 10, Chapter 11).

Package yield is multiplicative when you stack. Separate screening is why many CPO engines stay 2.5D-adjacent rather than fully bonded until the optical test story matures.

## Whiteboard vignette

Prompt: "Design the packaging for a 102.4 Tb/s switch optical shoreline. Do we go CPO? 2.5D or 3D? Where do the lasers live?"

A strong answer stays ordered:

1.  Name the binding constraint: SerDes energy, faceplate density, or serviceability.

2.  If CPO is required, pick 2.5D-adjacent engines unless a bonded 3D electronics-photonics stack has a proven KGD and thermal path.

3.  Put lasers in ELSFP-class banks unless on-package laser life is already proven at the ASIC hotspot.

4.  Define FAU attach screens and dark-lane reject before lid seal.

5.  Co-design XSR, power rails, and heatsink keep-outs with the ASIC team.

6.  State the field replaceables explicitly for the reliability model.

Weak answers jump to "use COUPE 3D" without naming yield and service. Strong answers treat vendor process names as options inside a constraint set.

## Interview takeaway

**Key idea.** I name the placement first: pluggable, NPO, or CPO. Then I name the integration style: 2.5D or 3D. I do not treat those as synonyms. I partition laser heat from the ASIC, insist on a known-good-die and fiber-attach story, and I only accept soldered engines when field replacement of the laser bank or a clear non-serviceable cost model closes.

## Interview Q&A

Practice aloud. Prefer first-person reasoning. Score with Appendix A.12.1.

##### Question 1. What is the difference between 2.5D and 3D?

*Tests:* lateral versus vertical integration.

*Spoken answer.* "2.5D puts dies side by side on an interposer, bridge, or RDL, so the dense wiring is lateral. 3D stacks dies with hybrid bonds, microbumps, or TSVs, so the dense wiring is vertical. 3D wins bandwidth density and pays in thermal access, test access, and stack yield."

*Pressure follow-up.* "Is CPO the same as 3D?"\
*Answer pivot.* "No. CPO is where the optical engine sits relative to the ASIC. It can be 2.5D, 3D, or substrate-mounted."

*Trap:* "CPO means hybrid-bonded 3D photonics."

##### Question 2. Why choose CPO?

*Tests:* electrical reach and energy density.

*Spoken answer.* "I choose CPO when faceplate VSR copper and pluggable power stop closing the port-count or energy budget. Shortening to XSR cuts SerDes energy and board SI pain, and it raises shoreline density. I still have to close thermal, yield, fiber, and serviceability."

*Pressure follow-up.* "Why not just use LPO pluggables?"\
*Answer pivot.* "LPO deletes module DSP but keeps the long host electrical run and cage. CPO attacks the copper reach itself."

*Trap:* "CPO is always lower power, so always choose it."

##### Question 3. Why might you refuse CPO?

*Tests:* yield, thermal, serviceability judgment.

*Spoken answer.* "I refuse CPO when package yield is unproven, when the laser cannot be kept off the ASIC hotspot, when fiber attach scrap risk is unacceptable, or when the fleet requires faceplate hot-swap of the whole optical path. XPO or pluggables can be the rational hold."

*Pressure follow-up.* "Management says competitors shipped CPO."\
*Answer pivot.* "Shipping proves a recipe can work. It does not prove our thermal partition, FAU yield, or service model are ready."

*Trap:* "Never do CPO until every vendor program looks perfect."

##### Question 4. External versus integrated laser?

*Tests:* thermal life versus coupling and failure domain.

*Spoken answer.* "An integrated laser shortens the optical path but sits near the heat and is hard to replace. An ELSFP-class external laser keeps the source cool and field-replaceable, at the cost of coupling, connectors, and a shared-source failure domain. I pick from life and service first, then from coupling loss (§7.14)."

*Pressure follow-up.* "Does external laser make CPO unnecessary?"\
*Answer pivot.* "No. It often enables CPO by removing the least reliable part from the hot package."

*Trap:* "External lasers are only for discrete pluggables."

##### Question 5. How do you partition thermally?

*Tests:* hotspot map and wavelength/life coupling.

*Spoken answer.* "I sketch ASIC hotspot, engine, laser, and fiber exit. I keep lasers off the hottest region when life matters, treat ring heaters as heat sources, and I budget junction temperature separately from case temperature. Rack liquid cooling does not automatically fix an on-die thermal gradient."

*Pressure follow-up.* "The case temperature meets spec. Why are rings walking?"\
*Answer pivot.* "Local gradient and neighbor heaters can move resonances even when case average looks fine."

*Trap:* "If the heatsink is sized for ASIC watts, optics are covered."

##### Question 6. What is known-good die in this context?

*Tests:* screen before irreversible attach.

*Spoken answer.* "Known-good die means I screen the ASIC and the optical engine as far as probe and partial assembly allow before I commit to a stack or sealed co-package. A bad PIC bonded to a good switch wastes both. 3D makes this harder because stack yield multiplies."

*Pressure follow-up.* "Can you fully optically test at wafer probe?"\
*Answer pivot.* "Often not completely. I define which optical metrics are probeable, which need partial assembly, and which wait for FAU attach."

*Trap:* "Wafer sort of the ASIC is enough; optics will be caught in system test."

##### Question 7. How does package yield change the architecture?

*Tests:* multiplicative yield and cost of scrap.

*Spoken answer.* "If optical attach or fiber alignment yield is soft, I avoid architectures that scrap a whole switch package on every miss. That pushes toward separable engines, reworkable attach, or keeping lasers in replaceable modules. Yield is an architecture input, not only a factory metric."

*Pressure follow-up.* "Yield is a manufacturing problem."\
*Answer pivot.* "Manufacturing executes it. Architecture chooses whether a fail scraps \$X or \$100X."

*Trap:* "Ship the densest stack and let the factory climb the yield curve."

##### Question 8. What matters for optical I/O in the package?

*Tests:* coupling style and keep-outs.

*Spoken answer.* "I name edge versus grating coupling, fiber exit direction, polarization control, and lid or socket keep-outs. Optical I/O has to coexist with the heatsink, power planes, and board clearance. A beautiful electrical 3D stack that cannot exit fiber cleanly is not a product."

*Pressure follow-up.* "Can we always use grating couplers for easier vertical fiber?"\
*Answer pivot.* "Sometimes. They trade efficiency, polarization, and wavelength dependence. Edge coupling may win on loss if the mechanical design allows it."

*Trap:* "Optical I/O is just a FAU drawing detail after electrical floorplanning."

##### Question 9. Why is fiber attach a first-class risk?

*Tests:* coupling, dark lanes, sealed-package discovery.

*Spoken answer.* "FAU attach sets insertion loss, lane balance, and often polarization. A single misaligned channel looks like a dead laser or bad PIC after the lid is on. I want attach metrics and dark-lane screens before irreversible seal, and I track FAU variation in FA when one lane is weak (Appendix F.11.4)."

*Pressure follow-up.* "Average coupling looks fine."\
*Answer pivot.* "I still check the weakest lane. Averages hide the channel that fails the link."

*Trap:* "If total power out of the FAU is in family, attach is good."

##### Question 10. How do you think about repairability?

*Tests:* field replaceable elements versus soldered engines.

*Spoken answer.* "I list what can fail and what a tech can replace: ELSFP laser bank, fiber jumper, pluggable module, or nothing because the engine is soldered. CPO often keeps the engine soldered and makes the laser replaceable. I state that explicitly so reliability and ops models match the hardware."

*Pressure follow-up.* "Is a soldered engine always a bad idea?"\
*Answer pivot.* "No, if the dominant fails are elsewhere and the cost model accepts package replacement. It is a bad idea if laser FIT still dominates and lasers are trapped on the hot die."

*Trap:* "CPO cannot be serviced, so it cannot ship."

##### Question 11. What does switch-ASIC co-design mean here?

*Tests:* shoreline, SerDes, power, and thermal co-ownership.

*Spoken answer.* "The optical engine and the switch SerDes share shoreline, bump map, power delivery, and thermal path. I co-design lane count, XSR budget, retimer or DSP placement, and heatsinking. A perfect PIC that the ASIC cannot drive cleanly, or that cooks the rings, is not an engine."

*Pressure follow-up.* "Who owns the XSR budget?"\
*Answer pivot.* "Both sides. Package SI and SerDes EQ share it (Chapter 5, §3.7)."

*Trap:* "The optics team owns optics; the ASIC team owns silicon; package is NPI's problem."

##### Question 12. How do you test an optical engine before final assembly?

*Tests:* staged test plan.

*Spoken answer.* "I stage tests: die or engine probe where possible, electrical continuity and basic photonic metrics after attach, optical power and dark-lane screens after FAU, then full link metrics after lid and at system bring-up. Each stage needs pass/fail that prevents carrying a known-bad unit into a more expensive assembly step."

*Pressure follow-up.* "System BER is the only test that matters."\
*Answer pivot.* "System BER is necessary, but it is a late, expensive screen. Earlier stages protect yield."

*Trap:* "Build the full package, then characterize everything at the host."

##### Question 13. Give a 60-second packaging plan for a CPO engine.

*Tests:* end-to-end judgment order.

*Spoken answer.* "I start from reach and port density to decide if CPO is needed. I choose 2.5D versus 3D from thermal access, KGD, and optical I/O, not from buzzwords. I place lasers for life and service, often external. I define FAU attach and dark-lane screens before seal, co-design XSR and power with the ASIC, and I only freeze the package when yield, thermal corners, and field replacement match the fleet model."

*Pressure follow-up.* "Schedule is cut. What do you protect?"\
*Answer pivot.* "Laser thermal partition, FAU yield evidence, and a service story for the highest-FIT part. Density slides after those."

*Trap:* "Pick the densest COUPE-like stack and qualify later."


<div class="nav-links">
  <a href="ch8-wdm-and-wavelength-locked-lasers">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch10-productization-from-requirements-to-controlled-ramp">Next &rarr;</a>
</div>
