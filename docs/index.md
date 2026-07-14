---
layout: default
title: "Short-Reach Optics for AI Compute"
---

<div class="center">

**Short-Reach Optics for AI Compute**\
*From First Principles to the State of the Art*\
©  Ed (Ehsan) Shah Hosseini.

<div class="minipage">

A concise technical overview of the optics that wire together large-scale AI systems. Compiled from public sources (IEEE, OIF, MSA specifications, vendor disclosures, and industry literature). Figures and third-party announcements are cited to their sources; any errors are the author’s own.

</div>

</div>

# Preface

Artificial intelligence has become an infrastructure problem. Training and serving frontier models at scale is no longer limited only by the accelerator at the center of the rack, but by how many accelerators can be wired together efficiently, reliably, and within a fixed power envelope. That wiring is increasingly optical, and the optics (especially the lasers inside them) have become a first-order lever on the cost, power, and reliability of the whole system.

This book is a concise technical overview of that layer: the short-reach optical interconnects that stitch together AI datacenters, from in-package optical I/O out to intra-rack links, deliberately setting aside the 2–10 km campus links that belong to coherent optics (<a href="#sec:reach" data-reference-type="ref+Label" data-reference="sec:reach">3.3</a>). It concentrates on the subjects that decide whether these links work at scale: IM/DD physics and vocabulary; lasers and external light sources; WDM and wavelength locking; quantitative noise and sensitivity models; validation from bench to fleet; and reliability and manufacturing at volume. Two chapters bracket those fundamentals: why inference-scale computing puts the interconnect on the critical path (<a href="#ch:role" data-reference-type="ref+Label" data-reference="ch:role">1</a>), and how AI datacenter networks are built where optics dominate cost and power (<a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>).

**On sources.** The industry moves quickly. Where the text cites specific products or figures (co-packaged-optics programs, per-lane roadmaps, energy-per-bit trends) it draws on public disclosures current as of early 2026, cited in the references. Where a claim is an inference rather than an established fact, the text says so. History and trend notes are included where they help explain why today’s defaults exist, not as a full chronology of the field.

**Key idea.** The through-line: at gigawatt, multi-generation scale, the optical interconnect and its lasers are a first-order lever on power, cost, and reliability. Everything here serves that argument.

# Why the interconnect matters

## The two themes of this book

Large AI systems fail or succeed as much on wiring as on FLOPs. The short-reach optics that connect accelerators, switches, and memory sit on the critical path for latency, power, and uptime, and two parts of that layer decide whether the system scales: the *lasers* that generate the light, and the discipline of *IM/DD validation*[^1] that proves those links work from the first bench eye through production and fleet life. This book keeps returning to those two themes. Modulation formats, WDM, reliability, and network architecture matter because they serve them.

**Key idea.** Two things dominate short-reach optics at scale: *lasers* and *IM/DD validation*. Everything else orbits those two.

## The context: purpose-built inference silicon

The pressure on the interconnect is not abstract. It comes from a shift in how large AI systems are built: vertically integrated, purpose-built silicon deployed at gigawatt scale, with networking named as a first-order design axis beside compute and memory. A representative example is *Jalapeño*, a purpose-built LLM *inference* accelerator Broadcom and a hyperscaler partner announced in 2026 as a blank-slate design, the first chip in a multi-generation compute platform.[^2] Its public features are typical of the class:

- **Partners and integration.** Broadcom provides silicon implementation and networking (including *Tomahawk* switch silicon); Celestica provides board, rack, and system integration.

- **Cadence.** A roughly nine-month design-to-tape-out cycle, with the designers’ own models used to accelerate parts of the flow.

- **Scale.** Deployment at gigawatt scale, over multiple generations, beginning in late 2026.

- **Design thesis.** “Reduce data movement and balance compute, memory, and *networking* resources” to reach realized utilization close to theoretical peak.

That last point is the hook for this book. Purpose-built inference silicon does not treat networking as a commodity NIC bolted on after the die is done; it budgets interconnect power and latency alongside FLOPs and HBM. Partners and cadence matter because they set who owns the switch ASIC and how fast generations turn: Broadcom for silicon and networking (including Tomahawk), Celestica for board and rack, a roughly nine-month design-to-tape-out cycle, and gigawatt-scale deployment planned across multiple generations from late 2026. Once networking sits on that line, the optical interconnect is how the system scales past a single package to a gigawatt cluster, and laser quality plus IM/DD validation become infrastructure problems rather than module afterthoughts.

## Why inference makes the interconnect matter

Inference is not training. Once a model is trained, serving it is dominated by two phases with very different bottlenecks (developed fully in <a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>):

Prefill  
processing the prompt: highly parallel and compute-bound, much like training.

Decode  
generating tokens one at a time: autoregressive and *memory-bandwidth-bound*, because every token streams the model weights through the compute units again.

Frontier models do not fit on one chip. They are sharded across many accelerators, so every generated token triggers *collective communication* across the fabric: all-reduce for tensor parallelism, all-to-all for mixture-of-experts routing, point-to-point for pipeline stages. The interconnect therefore sits on the *latency critical path* of inference, not merely the plumbing between training runs.

**Key idea.** Reliable, low-power IM/DD links directly set how large and how dependable an inference fabric can be. That is why the optical layer has become central to AI system design.

## How to read this book

The chapters build from physics to fleet scale:

1.  <a href="#ch:firstprinciples,ch:imdd" data-reference-type="ref+Label" data-reference="ch:firstprinciples,ch:imdd">[ch:firstprinciples,ch:imdd]</a>: energy, IM/DD vocabulary, modulators, FEC, equalization.

2.  <a href="#ch:models" data-reference-type="ref+Label" data-reference="ch:models">4</a>: quantitative noise, RIN, sensitivity (use with <a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>).

3.  <a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>: light sources (DFB/EML, LIV/SMSR/RIN, aging, ELSFP/CW-WDM).

4.  <a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>: wavelength locking, thermal crosstalk, CW-WDM, on-chip MUX.

5.  <a href="#ch:validation,ch:reliability" data-reference-type="ref+Label" data-reference="ch:validation,ch:reliability">[ch:validation,ch:reliability]</a>: measurement ladder, link budgets, qual, packaging.

6.  <a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>: scale-up/out, pluggables, CPO/XPO, inference collectives.

To use the book as a design drill, pick one link style (retimed 800G DR, LPO, or CPO WDM) and trace it end to end through <a href="#sec:txrx-chain,sec:pluggables,sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:txrx-chain,sec:pluggables,sec:cpo-status">[sec:txrx-chain,sec:pluggables,sec:cpo-status]</a>.

# First principles: the energy of moving a bit

Before any device, modulation format, or standard, one quantity governs short-reach interconnect design: the energy required to move a bit from one place to another. David Miller’s work on optical interconnects to silicon lays out the clearest first-principles framework for this,[^3] and although the specific numbers are years old, the scaling arguments are what matter, and they still decide where the optics go.

## The electrical baseline: charging a wire

To send a bit down an electrical line you charge and discharge its capacitance through a voltage swing. To order of magnitude,
``` math
E_{\text{elec}} \approx \tfrac{1}{2}\,C\,V^{2},
```
and the line capacitance grows with length, $`C \approx c'\,L`$ (with $`c'`$ on the order of a hundred-odd femtofarads per millimeter, depending on the medium). [^4] So the energy to move a bit electrically *rises with distance*, and the resistive-capacitive delay and the equalization needed to fight it rise with both distance and data rate.

## The optical alternative: energy at the ends

An optical link spends its energy differently. The dominant costs are the *conversions at the two ends* (driving the laser or modulator, and the receiver that turns light back into charge) plus the wall-plug inefficiency of the laser. Over short reaches, waveguide and fiber loss are small, so the energy per bit is, to first order, *independent of distance*.

**Key idea.** Electrical energy per bit grows with length; optical energy per bit is set at the endpoints and is roughly flat with length. That single contrast is the seed of everything else.

## The break-even distance, and why optics moves toward the chip

Put the two together and there is a cross-over length: below it, electrical wins; above it, optical wins. The decisive observation is what happens as data rates climb: the electrical cost at a given length rises (more charging events per second, worse loss at higher frequency, more equalization), so the *break-even distance shrinks*.

That is the whole history of the field in one sentence. As rates went from gigabits to hundreds of gigabits per lane, the cross-over marched inward: campus, then rack, then board, then package, and now die-to-die. It is the first-principles reason co-packaged optics and in-package optical I/O exist (<a href="#sec:cpo-status,sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cpo-status,sec:cwwdm">[sec:cpo-status,sec:cwwdm]</a>), and the reason the scope of this book is the *shortest* links (<a href="#sec:reach" data-reference-type="ref+Label" data-reference="sec:reach">3.3</a>).

## The receiver, capacitance, and attojoule targets

Miller’s sharpest point concerns the receiver. To register a bit, the photocurrent must develop a detectable voltage on the receiver’s input node, so the detection energy again looks like a $`C V^{2}`$ on that node’s capacitance. Minimize the photodetector and input capacitance (by integrating the detector tightly with the first transistor, eliminating parasitic pads and wires) and you can detect a bit with *fewer photons and less energy*. This is the argument for close electronic–photonic integration, and it is what makes sub-100 fJ/bit (and, in principle, attojoule-class) devices conceivable.

[^5]

## The floors: photons per bit and noise

Two physical floors bound how far this can go. A real receiver needs enough photons per bit for adequate signal-to-noise: today hundreds, with ideal detection in the handful-of-photons range. That sets a floor on received optical power, and hence on laser energy. Separately, the $`kT/C`$ noise on the receiver node (not the Landauer $`kT\ln 2`$ limit of logic, which is far smaller) is the practical noise floor for communication, and it too rewards small capacitance.

Miller is careful to separate the energy of *logic* from the energy of *communication*; short-reach interconnect is overwhelmingly a communication- energy problem, dominated by the endpoints described above.

## Recent progress toward the limits

Miller’s numbers are years old, but the framework has aged well: the last few years have been a steady march of experiments toward the floors it predicts, and they validate rather than overturn it. Three threads are worth knowing.

First, **low-capacitance 3D integration is delivering the receiver energy Miller argued for**. A 2025 demonstration integrated an 80-channel transceiver in three dimensions, stacking the photonics directly on the CMOS to minimize the receiver-node capacitance, and reported roughly 120 fJ/bit.[^6] Tellingly, it reaches that number not by pushing per-lane rate but by using *many slow channels* (about 10 Gb/s each) so each receiver stays in its most sensitive, lowest-energy regime, with WDM providing the aggregate bandwidth. That is Miller’s prescription almost verbatim.

Second, **the capacitance argument is directly measurable**. A co-designed 12 nm-FinFET-on-silicon-photonics transceiver using direct-bond interconnect cut input parasitic capacitance by about 75 %, which bought $`\sim\!\SI{6}{dB}`$ of receiver sensitivity and pushed link energy to a few hundred fJ/bit.[^7] The $`C V^{2}`$ story is not a metaphor; you can watch the sensitivity move as the capacitance drops.

Third, **WDM receivers with near-zero-power wavelength control are approaching sub-pJ/bit at terabit scale**: a single-chip 32-channel WDM PAM4 receiver reached 1.024 Tb/s on one fiber at under 0.38 pJ/bit with no DSP or equalization.[^8] And on the device side, alternative emitters are being pushed into the same regime, a 2025 microLED link demonstrated 200 fJ/bit transmitter energy at $`\text{BER} < 10^{-12}`$ with no FEC,[^9] exactly the LED branch of Miller’s device-by-device comparison.

**Key idea.** The 2009/2017 framework has not been superseded; it has been confirmed in hardware. The winning recipe in every recent result (low-capacitance co-/3D-integration plus many WDM channels at modest per-lane rate) is precisely what Miller’s energy accounting recommends. What has changed is only the vertical axis: from theoretical attojoule targets toward demonstrated hundreds-of-fJ/bit links.

## Why this framework anchors the book

Everything that follows is an effort to approach these floors at the required data rate and reliability. Laser wall-plug efficiency (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>) sets how much optical power you can afford. Modulation and FEC (<a href="#ch:imdd,sec:kp4,sec:equalization" data-reference-type="ref+Label" data-reference="ch:imdd,sec:kp4,sec:equalization">[ch:imdd,sec:kp4,sec:equalization]</a>) trade SNR for reach and rate. WDM (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>) amortizes one laser source across many wavelengths. Receiver noise and sensitivity (<a href="#ch:models,sec:worked-budget,sec:link-budget" data-reference-type="ref+Label" data-reference="ch:models,sec:worked-budget,sec:link-budget">[ch:models,sec:worked-budget,sec:link-budget]</a>) decide whether that power is enough. Co-packaging and energy-per-bit trends (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>) show the same first principle playing out as copper reach collapses and optics move onto the interposer.

**Key idea.** Short-reach optics is, at bottom, an energy-per-bit optimization. Optical energy is spent at the endpoints and is flat with distance; electrical energy grows with distance and rate; so rising data rates push optics ever closer to the chip. Miller’s framework is the lens the rest of this book looks through.

# Intensity modulation, direct detection

## What IM/DD means

Almost every short-reach datacenter link still uses the same basic deal with physics: put data on optical *power*, and recover it with a photodiode. That is *IM/DD*: *intensity modulation, direct detection*. The transmitter encodes bits as changes in optical intensity; the receiver is a photodiode plus a transimpedance amplifier (TIA) that turns photocurrent back into voltage. There is no local oscillator and no coherent mixing.[^10] Detection is square-law (photocurrent proportional to optical power), so phase is discarded. That limitation is acceptable inside the rack and across a few hundred meters of fiber, where cost, power, and latency matter more than spectral efficiency. It is why IM/DD, not coherent, wires AI compute fabrics today.

## The IM/DD transceiver chain

Every pluggable module and every co-packaged engine is a rearrangement of the same chain. Once you can name the blocks, you can place equalization, FEC, and validation measurements without getting lost in form-factor jargon.

Transmit  
laser or CW source $`\to`$ modulator (EML, MZM, ring) $`\to`$ driver $`\to`$ fiber coupling (<a href="#ch:lasers,sec:eml-eam,sec:simzm,sec:siring" data-reference-type="ref+Label" data-reference="ch:lasers,sec:eml-eam,sec:simzm,sec:siring">[ch:lasers,sec:eml-eam,sec:simzm,sec:siring]</a>).

Channel  
fiber, connectors, MUX (<a href="#sec:optical-channel,sec:wdm-hardware" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:wdm-hardware">[sec:optical-channel,sec:wdm-hardware]</a>).

Receive  
photodiode $`\to`$ TIA (optional CTLE) $`\to`$ SerDes/CDR or linear ADC to host (<a href="#sec:pd-tia,sec:equalization" data-reference-type="ref+Label" data-reference="sec:pd-tia,sec:equalization">[sec:pd-tia,sec:equalization]</a>).

Digital  
KP4 FEC in host or retimer (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>); module DSP optional (<a href="#sec:pluggables,sec:conditioning,tab:placement" data-reference-type="ref+Label" data-reference="sec:pluggables,sec:conditioning,tab:placement">[sec:pluggables,sec:conditioning,tab:placement]</a>).

The rest of this chapter fills in modulation physics, equalization, FEC, and the modulator platforms. Noise math and measurement practice live in <a href="#ch:models,ch:validation" data-reference-type="ref+Label" data-reference="ch:models,ch:validation">[ch:models,ch:validation]</a>.

### A pluggable link, end to end

The block list above is one module. A working rack-to-rack link chains two of them back to back across a fiber, and it helps to trace a single bit through the whole path once. <a href="#fig:link-chain" data-reference-type="ref+Label" data-reference="fig:link-chain">3.1</a> follows that path as a folded loop: the transmit side runs left to right across the top, the fiber turns the corner on the right, and the receive side runs back along the bottom into the far switch.

Start at the switch ASIC in rack A. It builds Ethernet frames, runs the reconciliation and coding sublayers, and encodes KP4 FEC (<a href="#sec:phy-stack,sec:kp4" data-reference-type="ref+Label" data-reference="sec:phy-stack,sec:kp4">[sec:phy-stack,sec:kp4]</a>), then hands parallel bit streams to the host *SerDes*. The SerDes serializes each stream to a 112 GBd PAM4 lane, applies transmit FFE, and drives the host PCB and the module cage connector. That electrical hop, host to module, is the AUI (an OIF VSR-class channel; <a href="#sec:reach,sec:224g" data-reference-type="ref+Label" data-reference="sec:reach,sec:224g">[sec:reach,sec:224g]</a>). Inside the module, an optional DSP or retimer reshapes the lane, or for a linear pluggable (LPO) nothing does and the host SerDes owns the whole electrical budget (<a href="#sec:equalization,sec:224g-deploy" data-reference-type="ref+Label" data-reference="sec:equalization,sec:224g-deploy">[sec:equalization,sec:224g-deploy]</a>). The driver then swings a modulator, an EML, Mach-Zehnder, or ring (<a href="#sec:eml-eam,sec:simzm,sec:siring" data-reference-type="ref+Label" data-reference="sec:eml-eam,sec:simzm,sec:siring">[sec:eml-eam,sec:simzm,sec:siring]</a>), and electrons become photons. That is the first domain crossing, marked E$`\to`$O in the figure.

The fiber plant is the quiet middle: duplex or parallel single-mode fiber, connectors, and patch panels carrying the light a few meters to a few hundred meters (<a href="#sec:optical-channel,sec:reach" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:reach">[sec:optical-channel,sec:reach]</a>). At the far module the light hits a photodiode and TIA and becomes current again (O$`\to`$E, the second crossing; <a href="#sec:pd-tia" data-reference-type="ref+Label" data-reference="sec:pd-tia">4.5.0.0.1</a>). An optional module DSP cleans it up, and the rack B host SerDes recovers timing, equalizes the lane, and decodes KP4. The switch ASIC reassembles frames and forwards them into the fabric, out a NIC, and over the in-node link (PCIe or an NVLink-class fabric) into the destination GPU or CPU. Every pluggable link is this shape; form factors and CPO only rearrange where the boundaries fall.

<figure id="fig:link-chain" data-latex-placement="ht">
<embed src="figures/fig_link_chain.pdf" />
<figcaption>A pluggable rack-to-rack link, drawn as a folded loop. Transmit runs left to right (switch ASIC <span class="math inline">→</span> host SerDes <span class="math inline">→</span> cage/AUI <span class="math inline">→</span> module DSP <span class="math inline">→</span> driver and optics), the fiber turns the corner, and receive runs back into the far switch, then on to the NIC and GPU. Colors mark the domain of each block; the two E<span class="math inline">↔︎</span>O crossings sit at the optics.<span id="fig:link-chain" data-label="fig:link-chain"></span></figcaption>
</figure>

This is the *scale-out* path, the rack-to-rack Ethernet fabric where optics already dominate. The *scale-up* fabric that ties GPUs together (NVLink- or UALink-class; <a href="#sec:scale-up-out" data-reference-type="ref+Label" data-reference="sec:scale-up-out">9.1</a>) is a different link. Its reach is much shorter, so most of it is still copper: direct-attach cable or backplane under roughly a meter, with no optics in the path at all. Optics only appears once rack densification pushes those links past the copper wall, and even then it borrows the same IM/DD building blocks over a different link and protocol layer. So the chain in <a href="#fig:link-chain" data-reference-type="ref+Label" data-reference="fig:link-chain">3.1</a> is the one that carries the optical volume today; scale-up is where optics is arriving next.

## Reach regimes, and the scope of this book

“Optical interconnect” is a wide phrase. A die-to-die link of a few millimeters and a 10 km campus span both move bits on light, but they solve different problems with different physics. AI compute fabrics live at the short end of that spectrum, where lasers, IM/DD, and validation dominate cost, power, and reliability. This book stays there and largely sets aside the 2–10 km campus and data-center-interconnect links that have moved toward coherent optics.

<span id="tab:reach" data-label="tab:reach"></span>

| Regime | Distance | Notes |
|:---|:---|:---|
| In-package / die-to-die | mm–cm | optical I/O chiplets (e.g. <a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a>) |
| Chip-to-chip / co-packaged | cm | CPO engines on the switch/XPU substrate |
| Scale-up (rack scale) | $`\sim`$<!-- -->1–10 m | XPU-to-XPU; copper below $`\sim`$<!-- -->1–2 m, optics beyond |
| Intra-rack / intra-row | up to $`\sim`$<!-- -->100–500 m | SR over MMF; DR single-mode |
| Campus / DCI *(out of scope)* | 2 km (FR), 10 km (LR), and beyond | increasingly coherent, not IM/DD |

**Table .** Reach regimes. This book focuses on the top four.

The dividing line is roughly where a link leaves the compute fabric. Inside that boundary, from millimeters in-package out to a few hundred meters, IM/DD is the workhorse and the laser is the component that gates scale. That is the territory this book treats.

## Where coherent takes over

### The two detection schemes, in one paragraph

*IM/DD* encodes bits as changes in optical intensity and recovers them with a square-law photodiode. Phase and polarization are discarded at detection. Coherent detection mixes the received field against a narrow-linewidth local-oscillator (LO) laser on a balanced photodiode pair, recovering amplitude and phase on both polarizations. The receiver digitizes in-phase and quadrature samples and runs heavy DSP: carrier recovery, polarization demux, chromatic dispersion compensation, and soft-decision FEC. The coherent transmitter typically needs an I/Q modulator (or equivalent) under the same linewidth discipline. That stack buys spectral efficiency and reach tolerance. It costs extra photonic parts, ADC/DSP die area, power, and latency.

### Why short reach stays IM/DD

Inside the compute fabric, from millimeters in-package out to a few hundred meters of single-mode fiber, loss and dispersion are modest: standard G.652.D fiber runs about 0.2 dB/km at 1550 nm with a zero-dispersion wavelength near 1310 nm, so a few hundred meters costs well under a decibel . A PAM4 IM/DD link with equalization, FEC, and a reasonable laser closes without coherent mixing. The energy argument from <a href="#ch:firstprinciples" data-reference-type="ref+Label" data-reference="ch:firstprinciples">2</a> applies directly: IM/DD keeps the expensive digital work at the electrical ends where process scaling helps, and the optical path is passive fiber. Rack and row runs also lean on bend-insensitive G.657 fiber in patch panels and shelves, and the SR/DR reach classes below map onto the OM4/OM5 multimode and OS1/OS2 single-mode cabling classes that ISO/IEC 11801 and TIA-492 define for the datacenter plant . Retimed 800G pluggables run roughly 14–18 W; LPO trims to roughly 7–9 W by deleting module DSP . A 400ZR-class coherent pluggable is built around a coherent DSP that alone draws roughly 5–8 W inside a 15 W module budget , landing near 45 pJ/bit at 400 Gb/s. Over a 100 m rack link that extra DSP power does not buy enough margin to justify the BOM and service complexity (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>).

### What coherent buys, and its price

Coherent wins where the channel is harder: kilometers of fiber, amplified DWDM, and dispersion that would crush a directly modulated PAM4 eye. Polarization multiplexing and higher-order QAM raise bits per symbol. Electronic dispersion compensation removes the need for tight wavelength and chirp control on the transmit laser. LO mixing gives a sensitivity boost that IM/DD only matches with more launched power. The price is upfront: linewidth requirements on both the transmit laser and the LO (often well below 100 kHz for long reach), I/Q modulators or integrated coherent PICs, high-speed ADCs, and a DSP that dominates module power. OIF standardized 400ZR coherent pluggables with a 15 W module budget for DCI spans to roughly 120 km . ZR+ variants push reach further at similar or higher power. That trade is right for campus and metro DCI. It is not the default inside an AI rack.

### The crossover, and where it is moving

Today the practical line sits near 2 km: intra-datacenter DR and shorter hops stay IM/DD (<a href="#sec:reach,tab:ieee-lane" data-reference-type="ref+Label" data-reference="sec:reach,tab:ieee-lane">[sec:reach,tab:ieee-lane]</a>); campus FR/LR and DCI have moved to coherent 400ZR/ZR+ (<a href="#tab:reach" data-reference-type="ref+Label" data-reference="tab:reach">3.1</a>). Pressure pushes coherent inward on per-lane rates: at 224G and especially 448G the IM/DD SNR and TDECQ margin tighten, and some proposals explore coherent-lite or coherent receivers for the longest scale-out hops . Pressure keeps IM/DD dominant for AI compute: LPO and CPO attack the power wall (<a href="#sec:power,sec:224g-deploy" data-reference-type="ref+Label" data-reference="sec:power,sec:224g-deploy">[sec:power,sec:224g-deploy]</a>) by stripping module DSP and shortening electrical reach, not by adding an LO and ADC chain. For inference fabrics at in-package to a few hundred meters, IM/DD remains the workhorse through the 224G generation. The open question is 448G and beyond: whether the last scale-out meters stay PAM4/PAM6 IM/DD or whether a stripped coherent option appears for links that already run retimed modules today (<a href="#sec:448g" data-reference-type="ref+Label" data-reference="sec:448g">3.14.3</a>).

## PAM4: more bits per symbol

Through the 10G and early 25G eras, most short-reach optics used two-level NRZ: one eye, one decision threshold, simple receivers. As per-lane rates climbed past about 50 Gb/s, keeping NRZ would have demanded more electrical bandwidth than connectors and SerDes could afford. The industry answer was *PAM4*: four amplitude levels carrying two bits per symbol. Line rates below are in gigabaud (*GBd*); host I/O is built in *SerDes* blocks.

| Per-lane rate | Symbol rate                           | Context                |
|:--------------|:--------------------------------------|:-----------------------|
| 100G/lane     | $`\approx`$<!-- -->53.1 GBd           | 400G/800G today        |
| 200G/lane     | $`\approx`$<!-- -->106–112 GBd        | 800G/1.6T ramp         |
| 224G/lane     | $`\approx`$<!-- -->112 GBd (CEI-224G) | next SerDes generation |

Per-lane rates and symbol rates (PAM4). {#tab:pam4-rates}

PAM4 halves the required bandwidth versus NRZ for a given bit rate, but it costs about 9.5 dB of SNR (three eyes instead of one, spaced one-third as far apart). That SNR hit is why modern links assume equalization, DSP, and forward error correction as part of the architecture rather than as optional polish (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>). Looking ahead, the 448G debate is partly about whether to stay on PAM4 at still higher baud or move to PAM6/PAM8 to ease the electrical channel (<a href="#sec:448g" data-reference-type="ref+Label" data-reference="sec:448g">3.14.3</a>).

## Equalization and clock recovery

Once PAM4 became the default, the electrical channel stopped looking like a wire and started looking like a filter. PCB traces, connectors, and cables low-pass the signal; the receiver must undo that inter-symbol interference (ISI) before slicing. Three equalizer classes appear in every short-reach link, plus clock recovery when the bit clock is rebuilt.

CTLE (continuous-time linear equalizer)  
provides analog high-frequency boost, often a zero-pole pair in the SerDes front-end, the TIA, or a redriver chip. CTLE is cheap and low latency but fixed: it cannot adapt tap-by-tap to an arbitrary channel.

FFE (feed-forward equalizer)  
is a finite-impulse-response filter with pre- and post-cursor taps. Host SerDes and module DSPs use FFE (often with CTLE ahead of it) to open the eye. Transmitter and dispersion eye closure quaternary (TDECQ) applies a *bounded* reference FFE when scoring transmitters (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>).

DFE (decision-feedback equalizer)  
cancels post-cursor ISI using past symbol decisions. CEI electrical eye budgets reference an 8-tap DFE at the slicer (<a href="#sec:eye-budget" data-reference-type="ref+Label" data-reference="sec:eye-budget">9.5.2</a>). DFE adds latency and error propagation but recovers more ISI than FFE alone at high loss.

CDR (clock-data recovery)  
extracts bit timing from the data stream and re-samples the eye. A *retimer* includes CDR plus equalization and regenerates a clean output; a *redriver* has CTLE/VGA but no CDR (<a href="#sec:conditioning" data-reference-type="ref+Label" data-reference="sec:conditioning">9.5.1</a>).

Where these blocks sit depends on the module style (<a href="#sec:pluggables,ch:networking" data-reference-type="ref+Label" data-reference="sec:pluggables,ch:networking">[sec:pluggables,ch:networking]</a>):

- **Fully retimed pluggable:** host SerDes $`\to`$ connector $`\to`$ module DSP (FFE/DFE/CDR) $`\to`$ optical engine. The module cleans a bad electrical channel.

- **Redriver / ACC:** CTLE (+ VGA) in the cable or mid-channel; host SerDes still owns CDR and heavy EQ.

- **LPO:** no module DSP/CDR. Host SerDes EQ and FEC must survive the full path; module may add only CTLE in the TIA and a linear driver (<a href="#sec:conditioning" data-reference-type="ref+Label" data-reference="sec:conditioning">9.5.1</a>). Optical TDECQ and electrical margin both tighten.

<a href="#fig:eq-chains" data-reference-type="ref+Label" data-reference="fig:eq-chains">3.2</a> shows the correct SerDes equalizer order, then where those blocks live in a retimed module versus LPO.

<figure id="fig:eq-chains" data-latex-placement="ht">
<embed src="figures/fig_eq_chains.pdf" />
<figcaption>Equalization chains. (A) Correct order on one electrical lane: Tx FFE, channel, CTLE, Rx FFE, DFE, then slicer/CDR. (B) Fully retimed pluggable: module DSP owns FFE/DFE/CDR on both sides of the optics. (C) LPO: no module DSP; the host SerDes must close the full EQ and FEC path.<span id="fig:eq-chains" data-label="fig:eq-chains"></span></figcaption>
</figure>

**Key idea.** CTLE boosts analog bandwidth; FFE/DFE cancel ISI digitally; CDR rebuilds timing in retimers. LPO deletes the module-side safety net, so host equalization and KP4 margin (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>) become the whole electrical story.

## SerDes and DSP: who does the work

The equalizers above have to run somewhere, and “SerDes” and “DSP” get used loosely for that somewhere. They are not the same thing, and at 112 GBd the line between them has mostly dissolved. Pinning down the vocabulary makes the retimed versus LPO versus CPO argument (<a href="#sec:conditioning,ch:networking" data-reference-type="ref+Label" data-reference="sec:conditioning,ch:networking">[sec:conditioning,ch:networking]</a>) concrete instead of a wall of acronyms.

### What the SerDes is

*SerDes* is the high-speed electrical I/O macro on an ASIC: switch silicon, a NIC, an accelerator, or a module chip. On transmit it serializes wide, slow parallel data from the MAC/PCS into one PAM4 lane on the wire; on receive it deserializes the sampled lane back to parallel words. That is the literal serializer/deserializer job. Everything else the SerDes does is in service of getting a clean symbol stream across a lossy channel.

### Analog SerDes versus DSP-based SerDes

How the SerDes conditions the signal splits into two design styles. An *analog* (mixed-signal) SerDes equalizes in the analog domain (CTLE, a few analog FFE/DFE taps) and slices directly. It is low power and low latency but limited in how much loss it can undo and how flexibly it adapts. A *DSP-based* SerDes puts a high-speed ADC on the receive lane, digitizes the eye, and does FFE, DFE, and timing recovery numerically, with a DAC and digital pre-distortion on transmit. It burns more power and adds latency, but it closes far more channel loss and adapts tap-by-tap. Above roughly 50 GBd the DSP-based architecture won: 112 GBd (224G) host SerDes and module retimers are ADC/DSP designs. So the “DSP” that cancels ISI at 224G usually lives *inside* the SerDes, not in a separate chip.

### Two things people call “the DSP”

That is the first meaning of DSP: the digital equalization and clock recovery inside a modern SerDes. The second meaning is *the module DSP*, a distinct retimer chip in a pluggable that has its own ADC/DSP SerDes on the host side, an FFE/DFE/CDR core, a gearbox (<a href="#sec:gearbox" data-reference-type="ref+Label" data-reference="sec:gearbox">3.14.3.0.15</a>), and often the FEC engine, then drives the optics. When the book says a retimed module “has a DSP” and LPO “deletes the DSP” (<a href="#sec:conditioning" data-reference-type="ref+Label" data-reference="sec:conditioning">9.5.1</a>), it means this second chip. Deleting it does not delete DSP from the link; it moves the equalization burden back onto the *host* SerDes DSP and onto FEC.

### Where FEC sits

FEC is a third block, and it is usually not part of the SerDes proper. KP4 encode and decode live in the PCS/FEC layer on the host (or in the module DSP when one is present), operating on the recovered symbol stream (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>). This is why a link can have a healthy SerDes eye and still fail on FEC, or ride an ugly eye that KP4 cleans: the SerDes recovers symbols, FEC fixes what is left. Validation reads pre-FEC BER exactly at that SerDes-to-FEC boundary.

### Mapping it back to module styles

<a href="#tab:serdes-dsp" data-reference-type="ref+Label" data-reference="tab:serdes-dsp">3.3</a> sorts the blocks by where they physically run for the three module styles. <a href="#fig:eq-chains" data-reference-type="ref+Label" data-reference="fig:eq-chains">3.2</a> shows the same split as signal chains. Read the LPO column as the design point that matters most for AI power budgets: the host SerDes DSP and host FEC carry the entire electrical channel, because the module has no retimer to hide behind (<a href="#sec:224g-deploy" data-reference-type="ref+Label" data-reference="sec:224g-deploy">3.14.2</a>).

| Block            | Retimed          | LPO             | CPO (XSR)         |
|:-----------------|:-----------------|:----------------|:------------------|
| Serialize / PAM4 | Host SerDes      | Host SerDes     | Host SerDes       |
| Rx EQ (FFE/DFE)  | Module DSP       | Host SerDes DSP | Host SerDes DSP   |
| CDR / retiming   | Module DSP       | Host SerDes     | Host SerDes       |
| KP4 FEC          | Host (or module) | Host            | Host              |
| Optical drive    | Module DSP out   | Linear driver   | On-package engine |

Where each block runs, by module style. {#tab:serdes-dsp}

**Key idea.** The SerDes is the ASIC’s electrical PHY; at 224G its equalization and clock recovery are done in DSP inside the SerDes. “The module DSP” is a separate retimer chip. LPO removes that retimer, so the host SerDes DSP plus KP4 FEC (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>) own the whole electrical channel. Optics begin only after that handoff.

## The Ethernet PHY stack: where optics attaches

The SerDes, the FEC, and the optics are not loose parts. IEEE 802.3 stacks them into named sublayers, and knowing the stack tells you exactly where the optical transceiver plugs in and which block owns each impairment. Ethernet lives at the bottom two OSI layers: the *MAC* (data link) builds frames and carries the addressing, and the *PHY* (physical) turns those frames into signals on the wire. Everything in this book sits inside the PHY.

### The sublayers, top to bottom

The PHY is itself a stack. <a href="#tab:phy-stack" data-reference-type="ref+Label" data-reference="tab:phy-stack">3.4</a> lists the sublayers a 400G/800G port walks through on transmit (receive runs in reverse).

| Sublayer | Function | Domain |
|:---|:---|:---|
| MAC | Frame, address, CRC | Digital, host |
| RS | Reconciliation: adapt MAC to the PHY across the xMII | Digital, host |
| PCS | 64B/66B, 256B/257B transcode, scramble, RS-FEC | Digital |
| PMA | Serialize, lane mux, clock recovery (SerDes) | Mixed-signal |
| PMD | Modulate/detect light: laser, driver, PD, TIA | Optical |

IEEE 802.3 PHY sublayers, transmit order. {#tab:phy-stack}

Two interface names sit between these blocks and cause most of the confusion. The *xMII* (for example 400GMII) is a wide parallel bus inside the chip between MAC and PCS. The *AUI* (for example 400GAUI-4) is the electrical serial lane set that leaves the host and crosses the faceplate connector to the module. The AUI is the CEI electrical channel your SerDes has to survive (<a href="#sec:serdes-dsp,ch:networking" data-reference-type="ref+Label" data-reference="sec:serdes-dsp,ch:networking">[sec:serdes-dsp,ch:networking]</a>); the *PMD* is the optical transceiver on the far side of it.

### Where the optics attaches

Optics is the PMD, and only the PMD. Everything above it is electrical or logical and is medium-independent: the same MAC, RS, PCS, and PMA feed a copper DAC, a multimode SR module, or a single-mode DR module. That is the whole point of the layering. When IEEE names `400GBASE-DR4` or `800GBASE-DR8`, it is naming a PMD (<a href="#sec:pmd-reach" data-reference-type="ref+Label" data-reference="sec:pmd-reach">3.13</a>); the digital stack above is shared. It is also why the retimed-versus-LPO-versus-CPO argument is really about *where the PMA and PCS/FEC physically sit* relative to the AUI, not about changing the optics (<a href="#sec:serdes-dsp" data-reference-type="ref+Label" data-reference="sec:serdes-dsp">3.7</a>).

### Line-rate accounting

The layering is where the MAC-rate-versus-line-rate gap (<a href="#tab:rate-stack" data-reference-type="ref+Label" data-reference="tab:rate-stack">3.6</a>) actually comes from. Take one 400G port. The MAC delivers 400 Gb/s of payload. The PCS transcodes it (256B/257B adds about 0.4%) and then RS(544,514) FEC adds 30 parity symbols per 514 data symbols, a $`544/514`$ expansion of roughly 5.8% relative to payload (equivalently 5.5% of the coded line, <a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>). The two multiply out to $`257/256 \times 544/514 = 1.0625`$, so the line carries $`400 \times 1.0625 =
425`$ Gb/s, split as four AUI lanes at 106.25 Gb/s (53.125 GBd PAM4). The optical PMD carries that same 425 Gb/s. So “400G Ethernet” is a 400 Gb/s MAC rate riding a 425 Gb/s line, and the extra 25 Gb/s is transcode plus FEC, not wasted bandwidth.

### What the PCS actually does

Inside the PCS, the MAC’s 64-bit words are first wrapped in 64B/66B blocks: a 2-bit sync header (`01` for data, `10` for control) lets the receiver find block boundaries in the serial stream. Four 66-bit blocks are then transcoded into one 257-bit block, which compresses the four 2-bit sync headers to a single bit and, crucially, produces a 256-bit payload that aligns cleanly with 10-bit RS-FEC symbols ($`\mathrm{lcm}(256,10)=1280`$, so five blocks make exactly 128 symbols with no remainder). The RS(544,514) encoder then adds parity (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>), and the PMA distributes the coded symbols across logical lanes, bit-multiplexes them down to the physical AUI lanes, and serializes each to PAM4. The payload bits themselves are never altered by transcoding; only the framing overhead is squeezed.

Where these blocks physically live is an implementation choice, not a layer rule. The PCS/FEC can sit in the host switch ASIC or in a module retimer DSP; LPO deletes the module DSP and forces the host to own PCS/FEC and all of the PMA equalization (<a href="#sec:serdes-dsp,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:serdes-dsp,sec:conditioning">[sec:serdes-dsp,sec:conditioning]</a>). The layer names stay the same regardless of which chip runs them.

**Key idea.** Ethernet is MAC (frames) plus PHY, and the PHY is RS, PCS, PMA, PMD. Optics is only the PMD; everything above is medium-independent, which is why one digital stack feeds copper, multimode, or single-mode. The MAC-to-line-rate gap is transcode ($`257/256`$) times FEC ($`544/514`$), giving 425 Gb/s on a 400G port. The module-style debate is about which side of the AUI runs the PMA and PCS/FEC.

## Test points: where the link is measured

Every metric in this book is taken *somewhere*. A datasheet line like “TDECQ $`\le`$ 3.4 dB” or “stressed sensitivity $`-3.1`$ dBm” means nothing until you name the reference plane it was measured at. The standards name those planes TP0 through TP5, plus the host-referenced pair TP1a and TP4a, and they run in order from the transmit silicon to the receive silicon. Learning them turns a scattered pile of numbers into a map: each spec belongs to exactly one plane, and each plane is owned by one document. <a href="#fig:test-points" data-reference-type="ref+Label" data-reference="fig:test-points">3.3</a> walks the chain; <a href="#tab:test-points" data-reference-type="ref+Label" data-reference="tab:test-points">3.5</a> is the lookup card.

The mistake to avoid is treating TP2 and TP3 as electrical points just past a connector. They are *optical* planes at the fiber. TP2 is the light launched into the fiber, measured after the module’s electrical-to-optical conversion (driver plus laser or modulator). TP3 is the light arriving at the far module, before its optical-to-electrical conversion (photodiode plus TIA). The electrical planes are the ones on either side of those two crossings.

<figure id="fig:test-points" data-latex-placement="ht">
<embed src="figures/fig_test_points.pdf" />
<figcaption>Test points on a one-way IM/DD link. Green marks the host and die-pad electrical planes (TP0, TP1a, TP4a, TP5); blue the module’s electrical connector (TP1, TP4); red the optical planes at the fiber <em>MDI</em> (TP2, TP3). The two domain crossings, E<span class="math inline">→</span>O in the module transmitter and O<span class="math inline">→</span>E in the module receiver, sit between the electrical and optical planes.<span id="fig:test-points" data-label="fig:test-points"></span></figcaption>
</figure>

**Read the chain in order.** At the transmit end, **TP0** is the transmit SerDes output at the die pad, the silicon designer’s reference. **TP1a** is the same host signal referenced at the module cage, the *AUI* the module must accept; its electrical eye quality is *EECQ*, the electrical analog of TDECQ. **TP1** is the module’s electrical input on the far side of the mated connector. The module then converts electrical to optical, and **TP2** is the optical launch at the transmitter *MDI*, where TDECQ, TECQ, OMA$`_{\mathrm{outer}}`$, ER, and RIN are specified (<a href="#ch:validation,sec:tdecq" data-reference-type="ref+Label" data-reference="ch:validation,sec:tdecq">[ch:validation,sec:tdecq]</a>). After the fiber, **TP3** is the optical input at the receiver MDI, where stressed receiver sensitivity (SECQ) is specified. The module converts back to electrical at **TP4** (its electrical output), **TP4a** is the host-referenced input near the receive SerDes under worst-case module output, and **TP5** is the receive die pad.

<span id="tab:test-points" data-label="tab:test-points"></span>

| Point | Domain | Location | Principal measurement | Owning spec |
|:---|:---|:---|:---|:---|
| TP0 | Electrical | Tx ASIC/SerDes die pad (host) | Silicon Tx quality; design reference, hard to probe once packaged | OIF CEI C2M |
| TP1a | Electrical | Host output at the cage, host-referenced (SerDes output via a host compliance board) | Host Tx eye, EECQ; the AUI the module must accept | OIF CEI C2M; LPO MSA |
| TP1 | Electrical | Module electrical input (module side of the mated connector) | Module input stressor calibration | IEEE 802.3 AUI; OIF CEI |
| TP2 | Optical | Transmitter MDI, fiber launch (after E$`\to`$O) | TDECQ, TECQ, OMA$`_{\mathrm{outer}}`$, ER, RIN$`_x`$OMA | IEEE 802.3 PMD; LPO MSA |
| TP3 | Optical | Receiver MDI, fiber input (before O$`\to`$E) | Stressed receiver sensitivity, SECQ | IEEE 802.3 PMD; LPO MSA |
| TP4 | Electrical | Module electrical output (module side of the connector) | Module Rx electrical output, EECQ | IEEE 802.3 AUI; OIF CEI |
| TP4a | Electrical | Stressed host input, host-referenced (near the Rx SerDes) | Host Rx under worst-case module output | OIF CEI C2M; LPO MSA |
| TP5 | Electrical | Rx ASIC/SerDes die pad (host) | Silicon Rx recovery; design reference, hard to probe | OIF CEI C2M |

**Table .** Test-point reference planes on a short-reach IM/DD link, transmit to receive. The optical planes TP2 and TP3 carry the transmitter- and receiver-quality specs; the electrical planes carry the host and module eye specs. See <a href="#tab:lpo-tp" data-reference-type="ref+Label" data-reference="tab:lpo-tp">9.3</a> for the concrete LPO MSA assignments.

**Who owns which plane.** The split is not arbitrary. IEEE 802.3 optical PMD clauses define the transceiver planes: the optical TP2 and TP3, and the module’s electrical PMD input and output at TP1 and TP4 . The OIF Common Electrical I/O chip-to-module work owns the electrical planes deeper into the host: the die pads TP0 and TP5, and the host-referenced compliance points TP1a and TP4a, which are measured through host and module compliance boards to de-embed the fixture . The LPO MSA then binds both sides into a single product contract for a DSP-less module, with the six-point ladder (TP1a, TP1, TP2, TP3, TP4, TP4a) tabulated in <a href="#tab:lpo-tp" data-reference-type="ref+Label" data-reference="tab:lpo-tp">9.3</a> .

The numbering is a family of conventions, not one universal set. IEEE optical PMD clauses commonly define only TP1 through TP4, with the optical measurements at TP2 and TP3; the die pads TP0/TP5 and the host-referenced TP1a/TP4a come from the chip-to-module electrical world. Fibre Channel historically used its own reference points. Match the labels to the document you are reading rather than assuming a shared TP0-to-TP5 spine.

**Where compliance testing concentrates.** Optical transmitter compliance lives at TP2 (TDECQ, OMA, ER); optical receiver compliance lives at TP3 (stressed sensitivity). Electrical host and module compliance concentrate at TP1a and TP4a, which is why a module that passes optical TDECQ at TP2 can still fail interop if it misses EECQ at TP1a. TP0 and TP5 sit inside the package and are informative for silicon design but hard to probe in a finished system. A retimed module recovers the signal before TP4; a linear (LPO) module does not, so at 224G its host EQ and FEC carry the whole electrical channel (<a href="#sec:conditioning,sec:pmd-reach" data-reference-type="ref+Label" data-reference="sec:conditioning,sec:pmd-reach">[sec:conditioning,sec:pmd-reach]</a>).

**Key idea.** The plane makes the number. TP2 and TP3 are optical, at the fiber MDI, and carry transmitter and receiver quality (TDECQ, stressed sensitivity). TP1 and TP4 are the module’s electrical connector; TP1a and TP4a are host-referenced near the SerDes; TP0 and TP5 are the die pads. IEEE 802.3 owns the optical planes, OIF CEI owns the die and host-referenced electrical planes, and the LPO MSA binds all of them into one DSP-less product contract (<a href="#tab:lpo-tp" data-reference-type="ref+Label" data-reference="tab:lpo-tp">9.3</a>).

## The link-budget vocabulary

These terms are the language of both datasheets and debug. Learn them as a ledger, not as a glossary quiz: when a link fails, you are almost always arguing about one of them.

OMA (optical modulation amplitude)  
$`P_1 - P_0`$: the real signal swing. For PAM4 the “outer OMA” spans the outermost levels.

Extinction ratio (ER)  
$`P_1/P_0`$, in dB. Trades against insertion loss and against *TDECQ* (<a href="#ch:validation" data-reference-type="ref+Label" data-reference="ch:validation">7</a>).

RIN (relative intensity noise)  
the laser’s own amplitude noise; sets a noise floor that matters more as OMA shrinks.

Chirp  
the unwanted frequency modulation that accompanies intensity modulation. Large in directly modulated lasers; small and controllable in externally modulated lasers. See <a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>.

Chromatic dispersion penalty  
dispersion $`\times`$ chirp $`\times`$ distance produces inter-symbol interference. This drives the wavelength plan and the choice between directly and externally modulated lasers (<a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>).

Receiver sensitivity  
the minimum OMA needed to hit a target bit-error ratio; “stressed” sensitivity adds a calibrated impairment for margin.

[^11]

## Chirp, dispersion, and the IM/DD penalty

IM/DD detects power, not phase, but phase still matters on the fiber. Intensity modulation couples to frequency through the laser or modulator *chirp* parameter $`\alpha`$: a change in output power shifts the instantaneous optical frequency. Single-mode fiber then converts that frequency wander into intensity distortion via chromatic dispersion (different $`\lambda`$ travel at slightly different speeds).

The penalty grows with chirp $`\times`$ dispersion $`\times`$ distance. At O-band ($`\sim`$<!-- -->1310 nm) dispersion is near zero ($`|D|\lesssim 3`$ ps/(nm$`\cdot`$km)), which is why silicon photonics and many datacenter SMF links use 1310 nm class wavelengths. At C-band ($`\sim`$<!-- -->1550 nm) dispersion is larger; chirpy sources pay more per kilometer.

Source choice sets chirp (<a href="#ch:lasers,tab:tx-modulator,sec:eml-eam" data-reference-type="ref+Label" data-reference="ch:lasers,tab:tx-modulator,sec:eml-eam">[ch:lasers,tab:tx-modulator,sec:eml-eam]</a>):

- **DML:** large $`\alpha`$; fine for tens of meters of MMF or uncooled SR, poor for FR-class SMF unless rate and reach stay short.

- **EML / external MZM / ring:** low chirp; default for DR/FR and CPO.

- **Reflections:** light reflected back into the laser raises effective chirp and RIN; optical return loss (ORL) specs exist for this reason (<a href="#sec:optical-channel" data-reference-type="ref+Label" data-reference="sec:optical-channel">7.2.2</a>).

For the distances this book treats (in-package through a few hundred meters), dispersion is often secondary to TDECQ, connector loss, and receiver noise. It becomes decisive when a low-chirp assumption fails (aging EAM bias, DML on SMF, or FR edge cases). TDECQ embeds dispersion in its name because the reference receiver includes a dispersion penalty model for the standardized test channel.

## Forward error correction

Modern PAM4 links do not meet raw bit-error-ratio targets on their own; they lean on *FEC*. The datacenter workhorse is *KP4*, a Reed–Solomon code RS(544,514) operating on 10-bit symbols. The name comes from `100GBASE-KP4` in IEEE 802.3bj: K for backplane, P for PAM4, 4 for four lanes . Today “KP4” means that FEC code on any PAM4 Ethernet link (optical DR, 224G SerDes, and backplane), not only the original backplane PHY. The link is specified to a *pre-FEC* BER threshold, on the order of $`2.4\times10^{-4}`$, which FEC then drives down to an effectively error-free *post-FEC* BER.

Two consequences matter in practice:

1.  Validation targets are stated in pre-FEC BER, and FEC symbol-error histograms are a rich debug signal (they reveal *how* a link is failing, not just that it is).

2.  Emerging *linear-drive* optics (*LPO*/*LRO*, <a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>) remove the DSP/retimer to save power, which tightens the link budget and leans even harder on FEC and on transmitter quality (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>).

##### KP4 in practice.

*KP4* maps to Reed–Solomon RS(544,514) on 10-bit symbols: 514 payload symbols, 30 parity, up to 15 correctable symbol errors per codeword. Coding overhead is $`30/544\approx5.5\%`$, so the *line rate* on the wire exceeds the MAC/info rate (for example, 802.3dj delivers $`\approx`$<!-- -->211 Gb/s payload on a 224 Gb/s PAM4 lane). <a href="#tab:rate-stack" data-reference-type="ref+Label" data-reference="tab:rate-stack">3.6</a> is the decoder for the three rate names you will see in 802.3dj and CEI-224G docs (example: one 200G Ethernet lane).

| Term | Meaning | Example |
|:---|:---|:---|
| MAC rate | User Ethernet throughput at MAC | 200 Gb/s per lane |
| Line rate | Bits on wire incl. FEC overhead | $`\sim`$<!-- -->211–224 Gb/s (context-dependent) |
| Symbol rate | Baud on the electrical/optical lane | $`\sim`$<!-- -->112 GBd PAM4 |

Three rate names on one 802.3dj lane (200G Ethernet). {#tab:rate-stack}

The optical PHY is qualified to a *pre-FEC* BER threshold, typically $`2.4\times10^{-4}`$ for KP4-class links. That corresponds to $`Q\approx3.5`$ on the Gaussian model of <a href="#sec:qber" data-reference-type="ref+Label" data-reference="sec:qber">4.1</a>. Post-FEC the target is effectively error-free ($`10^{-12}`$ to $`10^{-15}`$ class). Validation always reports pre-FEC BER during bring-up; post-FEC confirms the decoder is working.

FEC symbol-error *histograms* are a debug tool: clustered errors point to burst impairments (reflections, power droop); sparse errors point to Gaussian noise margin. At 448G/lane, CEI notes that KP4 at $`10^{-4}`$ pre-FEC may not close on 40 dB-class channels without stronger codes (<a href="#tab:448-fec" data-reference-type="ref+Label" data-reference="tab:448-fec">3.10</a>): MLC plus higher overhead RS, or hard-decision FEC in demos (<a href="#sec:448g" data-reference-type="ref+Label" data-reference="sec:448g">3.14.3</a>).

## Ethernet optical PMDs and reach classes

IEEE 802.3 names the optical transceiver (*PMD*) separately from the MAC rate. Short-reach IM/DD classes that matter for AI fabrics:

SR (short reach)  
multimode fiber, VCSEL at 850 nm or evolving MMF solutions; rack and row distances; modal noise and bandwidth limit legacy SR.

DR (datacenter reach)  
single-mode, typically 500 m class at 1310 nm; PAM4, KP4, TDECQ limits; the mainstream 400G/800G/1.6T module reach.

FR (far reach)  
single-mode, 2 km class; same optics family as DR with tighter transmitter specs; chirp and dispersion matter more at the margin.

Naming examples: 400G-DR4 (four lanes), 800G-DR8, 800G-FR8 (eight $`\lambda`$, 2 km). 802.3dj adds 200G/lane Ethernet; the 400G/lane study group targets the next generation (<a href="#tab:ieee-lane,sec:448g" data-reference-type="ref+Label" data-reference="tab:ieee-lane,sec:448g">[tab:ieee-lane,sec:448g]</a>). Campus LR and coherent DCI sit beyond this book’s scope (<a href="#tab:reach" data-reference-type="ref+Label" data-reference="tab:reach">3.1</a>).

## The per-lane roadmap: 224G and beyond

Per-lane rate is the axis the whole industry advances along, because doubling it roughly doubles switch and module capacity for the same lane count. The electrical I/O roadmap is set by the OIF’s Common Electrical I/O (CEI) projects, and optics tracks it closely.

| Generation | Per lane | Modulation                        | Ethernet rates     |
|:-----------|:---------|:----------------------------------|:-------------------|
| CEI-112G   | 112 Gb/s | PAM4                              | 100/200/400G       |
| CEI-224G   | 224 Gb/s | PAM4 ($`\approx`$<!-- -->112 GBd) | 200/400/800/1600G  |
| CEI-448G   | 448 Gb/s | TBD (PAM4/6/8)                    | 400/800/1600/3200G |

The CEI per-lane roadmap. {#tab:cei-roadmap}

<a href="#fig:cei-rate-year" data-reference-type="ref+Label" data-reference="fig:cei-rate-year">3.4</a> puts that ladder on a longer clock: OIF CEI has roughly doubled the rate per differential pair every four to five years since the early 2000s. Open markers for 224G and 448G follow the demo deck’s “202X” placement; 224G is shipping now, 448G is still pathfinding .

<figure id="fig:cei-rate-year" data-latex-placement="ht">
<embed src="figures/fig_cei_rate_vs_year.pdf" style="width:92.0%" />
<figcaption>OIF CEI rate per differential pair versus year (log scale). Data from the OFC 2025 CEI interoperability demo genealogy; 224G/448G years are provisional placements for the deck’s 202X entries, and 448G’s rate is the naming target (PAM order still open).<span id="fig:cei-rate-year" data-label="fig:cei-rate-year"></span></figcaption>
</figure>

### 224G is settled; the frontier is deployment

*CEI-224G* kicked off in 2022 as the electrical follow-on to CEI-112G. It kept PAM4 and roughly doubled the baud, to about 112 GBd per lane, with reach projects from XSR through LR now maturing. That choice is no longer the open debate; it is the shipping baseline. Eight 224G lanes make a 1.6 Tb/s port, and the same SerDes generation feeds 102.4 Tb/s-class switch silicon (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>). Copper reach has collapsed to about a meter, DSP-based SerDes are assumed, and a *CEI-224G-Linear* variant defines linear operation without a DSP/retimer in the optical module: the electrical foundation for LPO (<a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>). The remaining work is deployment: closing LPO margins, qualifying ELSFP banks for CPO, and holding yield at volume, not inventing a new modulation alphabet.

<a href="#fig:cei-reach-map" data-reference-type="ref+Label" data-reference="fig:cei-reach-map">3.5</a> is the reach map those projects sit on: *XSR*/XSR+ inside the package (die-to-die and die-to-optical-engine), *VSR* from ASIC to a faceplate pluggable, *MR* chip-to-chip on the board (PCB or twinax), and *LR* for backplane and longer copper cables . The media labels (host PCB traces, twinax, optical fiber, optical module) are where the loss budget actually lives; the CEI class name is the electrical recipe for that hop. <a href="#tab:cei224-reach" data-reference-type="ref+Label" data-reference="tab:cei224-reach">3.8</a> is the matching lookup card from the CEI-224G project map (OFC 2025 demo framing) .

<figure id="fig:cei-reach-map" data-latex-placement="ht">
<embed src="figures/fig_cei_reach_map.pdf" />
<figcaption>CEI reach map on a host PCB (redrawn). Backplane applications sit above the board; faceplate cages and modules sit below. XSR/XSR+ are in-package; VSR is chip-to-module; MR is chip-to-chip; LR covers backplane and active/passive copper.<span id="fig:cei-reach-map" data-label="fig:cei-reach-map"></span></figcaption>
</figure>

<span id="tab:cei224-reach" data-label="tab:cei224-reach"></span>

| Class | Hop | Nominal reach / channel | Notes |
|:---|:---|:---|:---|
| XSR | Die-to-die or die-to-OE | $`\lesssim`$<!-- -->50 mm package substrate | CPO / chiplet optics; light EQ |
| VSR | Chip-to-pluggable module | $`\sim`$<!-- -->200 mm host + $`\sim`$<!-- -->20 mm module, 1 connector | Classic faceplate retimed path |
| MR | Chip-to-chip / midplane | $`\sim`$<!-- -->500 mm, 1 connector | Board-scale copper |
| LR | Backplane or copper cable | $`\sim`$<!-- -->1000 mm host+daughter, 2 connectors | DAC/ACC/AEC territory |
| Linear | Chip-to-linear module | Same cages as VSR-class ports; no module DSP | LPO foundation; host EQ + FEC |

**Table .** CEI-224G electrical classes (project map). BER target on the reach classes is $`10^{-15}`$ or better with FEC allowed. Draft LR/MR IAs were member-review as of OFC 2025; Linear is the separate full-linear module track.

One SerDes core may not cover XSR through LR efficiently: short reaches want simple, low-power equalization, while LR burns DSP to close tens of dB of loss. That is why Linear is its own project rather than “VSR with the DSP deleted,” and why CPO (XSR) and LPO (Linear) show up as different power/serviceability bets (<a href="#sec:224g-deploy,sec:pluggables,sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:pluggables,sec:cpo-status">[sec:224g-deploy,sec:pluggables,sec:cpo-status]</a>).

### Deploying 224G: LPO, COM, and TDECQ corners

At 224G the alphabet is settled (PAM4 + KP4). What fails in the field is the *margin stack*: electrical channel operating margin (COM) on the host side, transmitter and dispersion eye closure quaternary (TDECQ) on the optical side, and the production corners that couple them (<a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a>). Retimed modules still dominate 1.6T faceplate ports because their DSP absorbs host-channel sin. LPO and LRO exist to delete that DSP for power and latency; they only ship when both ledgers close without it .

##### The two ledgers that must close together.

A retimed module can hide a bad host PCB behind module EQ. An LPO module cannot. You therefore run two go/no-go tests as one program:

Electrical COM  
After the CEI reference TX, channel, and Rx (CTLE + 8-tap DFE), COM $`\ge3`$ dB is the usual pass line at the slicer (<a href="#sec:com,sec:eye-budget" data-reference-type="ref+Label" data-reference="sec:com,sec:eye-budget">[sec:com,sec:eye-budget]</a>). At 112 GBd the residual eye after that equalizer is only a few millivolts tall; KP4 then cleans pre-FEC BER near $`2.4\times10^{-4}`$ down to $`10^{-15}`$ class (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>).

Optical TDECQ / TECQ  
Outer OMA, RLM, and TDECQ (or *TECQ* without the test fiber) score the transmitter after a bounded reference FFE (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>). LPO MSA language for 100G/lane DR already couples OMA to max(TECQ, TDECQ) and caps TDECQ near 3.4 dB; 224G-class linear modules inherit the same philosophy even while CEI-224G-Linear and IEEE 802.3dj freeze the exact limits .

CEI-224G-Linear defines the host/module electrical test points (TP1/TP1a, TP4/TP4a) so a linear module can sit between a DSP host SerDes and the fiber without its own CDR . Commercial 224G driver/TIA families advertise that interface explicitly (tunable swing, on-chip CTLE, CEI-224G-Linear host EQ) [Semtech 224G](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era). If either ledger is soft, prefer retimed or LRO until the host PCB and module linearity improve; do not “fix” LPO with more FEC alone.

##### Where 224G LPO programs actually break.

The failure modes are familiar once you stop treating LPO as a cheaper OSFP:

- **Host FIR / CTLE mistuned.** Taps pegged or CTLE boost too aggressive raises COM loss and looks like a bad module. Golden-swap the module first (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>).

- **Connector and package return loss.** VSR/MR channels already sit near the edge at 112 GBd; a resonant stub or long bondwire eats the few mV of slicer margin (<a href="#sec:trace-loss,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:trace-loss,sec:conditioning">[sec:trace-loss,sec:conditioning]</a>).

- **Module nonlinearity.** Driver or TIA compression wrecks RLM; TDECQ climbs even when average power looks fine. Linear-optics parts exist because retimed DSP no longer hides this (<a href="#sec:drivers,sec:pd-tia" data-reference-type="ref+Label" data-reference="sec:drivers,sec:pd-tia">[sec:drivers,sec:pd-tia]</a>).

- **ORL / RIN feedback.** Dirty fiber or a bad isolator raises effective RIN and floors pre-FEC BER while LIV still looks healthy (<a href="#sec:rin,sec:optical-channel" data-reference-type="ref+Label" data-reference="sec:rin,sec:optical-channel">[sec:rin,sec:optical-channel]</a>).

- **Chassis thermal + neighbor load.** Faceplate case temperature and adjacent lanes move bias, TEC, and (for rings) lock; TDECQ and unlock show up together (<a href="#tab:prod-corners,sec:thermal-xtalk" data-reference-type="ref+Label" data-reference="tab:prod-corners,sec:thermal-xtalk">[tab:prod-corners,sec:thermal-xtalk]</a>).

##### Half-retimed LRO as the pragmatic middle.

When full LPO will not close on the target host, *LRO*/*TRO* (retimed TX, linear RX) keeps roughly half the DSP power and still relaxes the Tx eye into the fiber . Many AI clusters take that path first: spend watts on the harder electrical$`\to`$optical direction, keep the receive path linear into the host. The validation split is the same: COM and stressed host input on the linear side, TDECQ on the retimed Tx side (<a href="#sec:pluggables,sec:secq" data-reference-type="ref+Label" data-reference="sec:pluggables,sec:secq">[sec:pluggables,sec:secq]</a>).

##### CPO at the same SerDes generation.

Co-packaged engines shipping in 2025–26 typically run *200 Gb/s per optical channel* on 100G/200G SerDes into microring banks with external lasers (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>): same CEI-224G-class shoreline as faceplate 224G, but the lossy pluggable connector is gone and the laser service model moves to ELSFP (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>). Deployment corners shift from cage thermals to FAU mate, lock hold under neighbor heaters, and ELS hot-swap (<a href="#tab:prod-corners,ch:wdm" data-reference-type="ref+Label" data-reference="tab:prod-corners,ch:wdm">[tab:prod-corners,ch:wdm]</a>). The electrical alphabet is still 224G PAM4; the hard part is packaging and wavelength control.

**Key idea.** 224G deployment is a margin problem, not a modulation problem. Close COM and TDECQ together under production-representative corners; use LRO when full LPO will not; treat CPO as the same SerDes generation with a shorter electrical path and a harder laser/lock service model.

### 448G is where the modulation debate lives

The next step, *CEI-448G* (framework published in late 2025, targeting 3.2 Tb/s systems from 2026 onward), is where the long PAM4 consensus finally comes under pressure . A full CEI-448G glossary of terms is in <a href="#ch:abbrev" data-reference-type="ref+Label" data-reference="ch:abbrev">10</a>. The debate is not whether 448 Gb/s *per lane* is useful (eight lanes make a 3.2 Tb/s OSFP-class port), but what *symbol rate* and *modulation order* each part of the link must run at to get there.

##### Line rate, symbol rate, and where each applies.

*448G/lane* in CEI means roughly 448 Gb/s of payload on one differential electrical pair between host and module (or between dies in a package). Ethernet maps the same lane count to aggregate rates (400G, 800G, 1.6T, 3.2T). FEC and coding overhead sit on top of the 448 Gb/s target, as they did at 112G and 224G.

For PAM-$`M`$, the relationship is
``` math
R_{\mathrm{line}} \approx \log_2(M)\,R_{\mathrm{sym}},
```
with $`R_{\mathrm{sym}}`$ the baud rate and the Nyquist frequency $`f_N\approx
R_{\mathrm{sym}}/2`$. At 448 Gb/s the OIF framework tabulates the options in <a href="#tab:448-mod" data-reference-type="ref+Label" data-reference="tab:448-mod">3.9</a> . PAM4 needs 224 GBd and $`f_N\approx112`$ GHz. PAM6 drops to 173 GBd and $`f_N\approx87`$ GHz. PAM8 drops further to 149 GBd and $`f_N\approx75`$ GHz. Each step down in baud buys channel bandwidth at the cost of finer amplitude levels, lower SNR margin, and heavier FEC/DSP.

The critical split is *where* on the board those numbers apply:

- **In-package (*XSR*/XSR+, die-to-die, die-to-OE):** trace lengths of millimeters to a few centimeters. Package bandwidth can reach $`\gtrsim`$<!-- -->115 GHz with $`\le`$<!-- -->0.5 mm BGA pitch and skip-layer routing. 448G-PAM4 at 224 GBd is the working assumption here, including linear drive from host SerDes straight into a co-packaged optical engine .

- **Host PCB plus pluggable connector (*VSR*/*MR*/*LR*):** meters of PCB, a module connector, and often a cable. Measured end-to-end channel bandwidth is limited to about 90 GHz today, mostly by connector pin stubs and resonance notches above that frequency . At 90 GHz, PAM4 at 112 GHz Nyquist does not close; PAM6 or PAM8 is the fallback unless connector technology moves the roll-off past 112 GHz.

- **Optical lane (fiber):** IM/DD at 448 Gb/s still targets PAM4 at $`\approx`$<!-- -->224 GBd per wavelength. The fiber channel is not connector-limited in the same way; TDECQ, chirp, dispersion, and receiver bandwidth dominate instead of copper insertion loss .

<a href="#fig:oif-448g-package" data-reference-type="ref+Label" data-reference="fig:oif-448g-package">3.6</a> is the packaging map behind that split: co-packaged copper (*CPC*), co-packaged optics (CPO), and faceplate pluggables (retimed, LPO/LRO, AEC/DAC) all leave the host IC at different places, which is why connector bandwidth and host EQ budgets change together .

<figure id="fig:oif-448g-package" data-latex-placement="ht">
<embed src="figures/fig_oif_448g_package.pdf" />
<figcaption>CEI-448G packaging map (redrawn). CPC brings copper to the package edge; CPO puts an optical engine in the package; faceplate cages take retimed optics, LPO/LRO, or AEC/DAC. Same host IC, different SerDes reach and EQ burden. <span id="fig:oif-448g-package" data-label="fig:oif-448g-package"></span></figcaption>
</figure>

##### What ships today on that map (224G / 200G Ethernet).

Before the 448G fork, every branch of <a href="#fig:oif-448g-package" data-reference-type="ref+Label" data-reference="fig:oif-448g-package">3.6</a> already has a shipping answer at the CEI-224G / IEEE 802.3dj lane rate. Faceplate ports run eight 224 Gb/s PAM4 lanes into 1.6 Tb/s OSFP-class modules (retimed DSP modules still dominant; LPO and LRO gaining share where host COM and TDECQ close, <a href="#sec:224g-deploy" data-reference-type="ref+Label" data-reference="sec:224g-deploy">3.14.2</a>). Copper inside the rack uses DAC, ACC, and AEC at the same SerDes generation. CPO engines shipping with Tomahawk 6 and Quantum-X class switches are typically *200 Gb/s per optical channel* on 100G/200G SerDes into microring banks with external lasers (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>): same packaging map, one generation behind the 448G electrical debate. KP4 FEC, CEI-224G-Linear for LPO, and KP4 pre-FEC BER near $`2.4\times10^{-4}`$ are the settled electrical/optical contract (<a href="#sec:224g,sec:eye-budget,sec:kp4" data-reference-type="ref+Label" data-reference="sec:224g,sec:eye-budget,sec:kp4">[sec:224g,sec:eye-budget,sec:kp4]</a>). The rest of this section is about what breaks when you try to double that lane rate on the same shoreline.

So the “448G debate” is really two linked questions: can the *electrical* shoreline run PAM4 at 224 GBd, and can the *optical* *PMD* modulate and detect at the same symbol rate? <a href="#fig:448g-paths" data-reference-type="ref+Label" data-reference="fig:448g-paths">3.7</a> maps the three dominant architectures and the baud rate at each hop.

<figure id="fig:448g-paths" data-latex-placement="ht">
<embed src="figures/fig_448g_paths.pdf" />
<figcaption>448G/lane signal paths: aligned pluggable PAM4 (connector-limited), PAM6 electrical with module gearbox (LPO incompatible), and CPO or gearboxed 224G transition.<span id="fig:448g-paths" data-label="fig:448g-paths"></span></figcaption>
</figure>

| Scheme | Symbol rate | $`f_N`$ |     UI |      SNR penalty vs. PAM4 |
|:-------|------------:|--------:|-------:|--------------------------:|
| PAM4   |     224 GBd | 112 GHz | 4.5 ps |                      0 dB |
| PAM6   |     173 GBd |  87 GHz | 5.8 ps |   $`\approx`$<!-- -->2 dB |
| PAM8   |     149 GBd |  75 GHz | 6.7 ps | $`\approx`$<!-- -->4–5 dB |

PAM-$`M`$ options at 448 Gb/s/lane (OIF CEI-448G framework, pre-FEC line-rate target). {#tab:448-mod}

##### FEC overhead and the SNR budget.

At 224G, IEEE and CEI both lean on *KP4* FEC: Reed–Solomon RS(544,514) from 802.3 Clause 91, with coding overhead $`30/544\approx5.5\%`$ and a pre-FEC BER target near $`2.4\times10^{-4}`$ for optical PHYs . Post-FEC the corrected BER target is $`10^{-15}`$ class. The line rate on the wire is higher than the MAC/info rate: a 200 Gb/s Ethernet lane (802.3dj) runs PAM4 at 112 GBd ($`224`$ Gb/s raw) and delivers $`\approx`$<!-- -->211 Gb/s of payload after KP4, rounded to 200 Gb/s at the MAC.

448G pushes FEC harder. CEI-448G lists pre-FEC BER $`10^{-4}`$ as the working target (same as prior CEI generations) but notes that $`10^{-4}`$ at $`\ge`$<!-- -->40 dB channel loss may not close without a *stronger* code than KP4 . PAM6 adds $`\sim`$<!-- -->2 dB SNR penalty on top, so workshop assumptions often pair PAM6 with *MLC* and higher-overhead FEC ($`\sim`$<!-- -->12%) for a fair comparison to PAM4 with KP4 . <a href="#tab:448-fec" data-reference-type="ref+Label" data-reference="tab:448-fec">3.10</a> summarizes the landscape (OH = coding overhead); 448G codes are not finalized (see caption for sources).

<span id="tab:448-fec" data-label="tab:448-fec"></span>

| Context | FEC | OH | Role at 448G/lane |
|:---|:---|:---|:---|
| 802.3dj / 224G | KP4 RS(544,514) | 5.5% | Baseline; pre-FEC BER near 2.4e-4. |
| CEI-448G, PAM4 elec. | KP4 or stronger | 5.5%+ | Target pre-FEC 1e-4; KP4 may fail on 40 dB-class channels. |
| CEI-448G, PAM6 elec. | MLC + strong RS | 12% | Offsets PAM6 SNR penalty; adds latency (workshop assumption). |
| 448G optical demos | HD-FEC / product | 10–15% | 3.2T TFLN demo threshold; not necessarily host FEC. |
| FEC architecture | end-to-end vs. terminated | n/a | 448G may need dedicated electrical inner code. |

**Table .** FEC at 448G/lane (448G codes provisional).

Sources: 802.3dj/KP4 baseline ; CEI-448G electrical targets  ; PAM6 FEC assumption ; optical demo .

Higher FEC overhead feeds back into the modulation debate: every extra parity bit raises the line rate and Nyquist frequency, which hurts a bandwidth-limited copper channel. That is one reason PAM6 (lower baud) and stronger FEC get paired, and why CPO (shorter electrical path) keeps PAM4 attractive.

##### Electrical SerDes: feasible, but the channel is the gate.

448G SerDes themselves are widely treated as feasible on advanced CMOS ($`\le`$N3/N2): ADC/DAC DSP transmitters and receivers demonstrated at 224 Gb/s are the template, and coherent-optics SerDes with $`\sim`$<!-- -->100 GHz class AFE at 200 GBd is cited as encouraging precedent for doubling to 448G-PAM4 . Synopsys and others have published channel simulations showing margin for both PAM4 and PAM6 on 224G-class channels when equalization and FEC scale with the modulation order . Power targets cluster around 0.5–2.5 pJ/bit at 448G, similar in spirit to 224G scaling.

The blocker is not the PLL or the DAC; it is the *passive channel*. Connector bandwidth near 90 GHz forces a fork:

1.  **Fix the channel for PAM4:** new high-density connectors, shorter reach, skip-layer PCBs, cabled-host internal twinax. Simulations show passive CPC reach up to $`\sim`$<!-- -->1.2 m at 448G-PAM4 under optimistic connector assumptions . This path preserves electrical/optical format alignment and keeps LPO/LRO architectures viable (<a href="#ch:networking" data-reference-type="ref+Label" data-reference="ch:networking">9</a>).

2.  **Keep the channel, change modulation:** PAM6 at 173 GBd fits a 90 GHz channel but adds $`\sim`$<!-- -->2 dB SNR penalty and pushes the host toward stronger FEC than KP4. PAM8 relaxes bandwidth further at $`\sim`$<!-- -->4–5 dB penalty .

3.  **Bypass the bad channel:** co-packaged optics with millimeter-scale die-to-OE links. Host 448G-PAM4 SerDes drives the optical engine directly; the pluggable connector never sees 224 GBd .

If electrical PAM6 wins on the PCB but optics stay at PAM4, the module needs a *gearbox* (rate/format conversion) in the retimed path. That adds power, latency, and silicon area, and it breaks linear pluggable optics: LPO requires the host electrical waveform to match what the optical modulator expects . First 448G optical modules may therefore ship with gearboxed 224G SerDes (two 224G lanes per 448G optical lane) before native 448G electrical I/O is ready .

##### Optical modulation at 224 GBd: hard, but no longer hypothetical.

On the optics side, the industry assumption is still IM/DD PAM4 at $`\approx`$<!-- -->224 GBd for 448 Gb/s per $`\lambda`$ . That requires roughly 112 GHz class electro-optic bandwidth in the modulator (and comparable photodiode/TIA bandwidth in the receiver), plus a driver with enough linear swing and RF BW. By 2025–26 that stack exists in demos and, increasingly, in announced commercial parts: silicon rings and MZMs with peaking, TFLN MZMs past 100 GHz EO bandwidth, EMLs still owning volume at 200G/lane, and SiGe drivers / Ge receivers catching up. The snapshot below is the state of play; device sections later unpack each family.

- **Silicon microring modulators:** resonant, compact modulators for dense WDM and CPO (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>). OFC 2026 demos reach 224–416 Gb/s PAM4 with inductive peaking .

- **Silicon Mach–Zehnder modulators:** the broadband, non-resonant counterpart to microrings (<a href="#sec:simzm" data-reference-type="ref+Label" data-reference="sec:simzm">3.14.3.0.7</a>). OFC 2026 demos reach 400G/lane PAM4 with SiGe drivers .

- **EML:** integrated DFB + EAM remains the default through 200G/lane for DR/FR pluggables: one chip, low chirp, mature supply chain.

- **TFLN MZM:** thin-film lithium niobate Mach–Zehnder modulators with CW lasers exceed 100 GHz EO bandwidth and are the leading path to native 224 GBd IM/DD (<a href="#sec:tfln-mzm" data-reference-type="ref+Label" data-reference="sec:tfln-mzm">3.14.3.0.8</a>). A 3.2 Tb/s system (eight $`\times`$<!-- -->225 GBd PAM4 lanes) with 3 nm CMOS SerDes and TFLN modulators over 2 km *FR8*/*DR8* was reported in 2025 .

- **Drivers:** commercial modulator drivers with $`>`$<!-- -->120 GHz RF BW for 400G PAM4 EML/MZM/TFLN platforms appeared in 2026 .

- **Receivers:** Ge/Si PIN and APD photodiodes above 100 GHz and 224G TIAs exist (<a href="#sec:pd-tia,sec:rxtech" data-reference-type="ref+Label" data-reference="sec:pd-tia,sec:rxtech">[sec:pd-tia,sec:rxtech]</a>); the receive side is not the long pole relative to modulator/driver bandwidth at 448G.

##### Silicon microring and microdisk modulators.

A microring modulator (MRM) wraps a phase-shifter waveguide into a closed loop coupled to a straight *bus* waveguide. A *microdisk* is the same idea in disk form: a pillar cavity evanescently coupled to the bus, often with a wider free spectral range (FSR) in a smaller footprint. Both are resonant filters as well as modulators: when the input wavelength sits on resonance, drop-port power is high; off resonance it is rejected. Data modulation shifts the resonance (carrier depletion or injection in an embedded pn junction) or detunes the laser relative to a fixed ring, mapping voltage to intensity at the through or drop port.

The central design trade is *photon lifetime versus bandwidth*. A high-$`Q`$ ring stores photons longer, which improves modulator efficiency ($`V_\pi`$) but narrows the optical passband and creates an electrical bandwidth ceiling through the RC-limited junction. Coupling strength, ring radius, and whether the device operates in under-coupled or over-coupled regime set $`Q`$, extinction, and the electro-optic (EO) roll-off. That trade does not appear in broadband Mach–Zehnder modulators (<a href="#sec:simzm" data-reference-type="ref+Label" data-reference="sec:simzm">3.14.3.0.7</a>).

Three constraints dominate ring modulator design at 100–400G per $`\lambda`$. First, EO bandwidth: the junction RC roll-off is often below the target Nyquist frequency, so inductive peaking (T-coils on the drive path), optimized detuning from resonance, and compact RLC co-design extend EO BW without widening the ring so much that $`Q`$ collapses . Production CPO rings target 50–90 GHz; conference demos report 90–110+ GHz with aggressive peaking . Second, wavelength alignment: ring resonance drifts roughly 10 GHz/°C in silicon, so each $`\lambda`$ in a WDM bank needs the laser or the ring tuned onto the modulator resonance (<a href="#ch:wdm,sec:locking-techniques" data-reference-type="ref+Label" data-reference="ch:wdm,sec:locking-techniques">[ch:wdm,sec:locking-techniques]</a>). Thermal crosstalk from neighbors shifts resonances in dense arrays, which is why fleet validation must include corner temperature and adjacent-channel heating (<a href="#sec:thermal-xtalk,ch:validation" data-reference-type="ref+Label" data-reference="sec:thermal-xtalk,ch:validation">[sec:thermal-xtalk,ch:validation]</a>). Third, optical loss and FSR: ring radius sets FSR ($`\Delta\lambda`$ between adjacent resonances). Microdisk and *Euler* ring layouts widen FSR so more channels fit under one free spectral range without collisions , while residual coupling loss and on-resonance insertion loss (often 1–3 dB class per modulator) eat link budget.

Integration is where rings win. A single SOI die can pack dozens of ring modulators and filters for CW-WDM (<a href="#ch:wdm,sec:cwwdm" data-reference-type="ref+Label" data-reference="ch:wdm,sec:cwwdm">[ch:wdm,sec:cwwdm]</a>), each fed by one wavelength from an external comb or multi-wavelength ELS (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>). The photonic engine co-packaged with a switch ASIC (Broadcom Bailly/Davisson, NVIDIA Quantum-X/Spectrum-X, <a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>) uses microring modulators at 200 Gb/s per channel today. Fiber count stays low because many $`\lambda`$ share one waveguide; area and modulator count scale with WDM order rather than with faceplate port count.

State of the art in 2025–26 shows how far that peaking path has been pushed. Inductive and wavelength tuning carried silicon MRMs to 224 Gb/s PAM4 at 90 GHz EO BW . T-coil-peaked designs report 416 Gb/s PAM4 ($`\approx`$<!-- -->208 GBd) with $`>`$<!-- -->110 GHz 1-dB EO BW and TDECQ 2.88 dB at 1 Vpp . Euler microdisk rings show 256 Gb/s PAM4 with $`>`$<!-- -->67 GHz EO BW and 3 THz FSR in O-band . These are lab and conference results, but they match the 200G/lane CPO shipping point and probe 448G-class lane rates when paired with sufficient electrical drive.

The platform choice is a packaging and control decision as much as a bandwidth one. Prefer rings when many $`\lambda`$ must fit on one PIC and modulator area dominates: CPO WDM engines, scale-up optical I/O, and any architecture that already budgets for wavelength locking (<a href="#ch:wdm,ch:networking" data-reference-type="ref+Label" data-reference="ch:wdm,ch:networking">[ch:wdm,ch:networking]</a>). Prefer a silicon MZM for single-$`\lambda`$ DR/FR where a flat passband avoids lock loops (<a href="#sec:simzm" data-reference-type="ref+Label" data-reference="sec:simzm">3.14.3.0.7</a>). Prefer TFLN when you need native 224 GBd in a pluggable and ring thermal control at fleet scale looks harder than hybrid assembly (<a href="#sec:tfln-mzm" data-reference-type="ref+Label" data-reference="sec:tfln-mzm">3.14.3.0.8</a>).

##### Silicon Mach–Zehnder modulators.

Silicon photonics builds the Mach–Zehnder modulator (MZM) as a push-pull interferometer on a silicon-on-insulator (SOI) rib or strip waveguide. Phase shifters in each arm use *carrier depletion* in an embedded pn junction: reverse bias pulls carriers out of the waveguide core, lowering refractive index and shifting optical phase. Intensity modulation comes from recombining the arms at a 3-dB coupler, so chirp stays low compared with directly modulated lasers (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>).

Three constraints mirror every high-speed MZM, but silicon’s weak electro-optic coefficient ($`\Delta n`$ per volt is far smaller than lithium niobate) sets the numbers. The optical $`S_{21}`$ response must span the Nyquist frequency ($`\approx`$<!-- -->56 GHz at 112 GBd, 112 GHz at 224 GBd); junction capacitance, series resistance, and traveling-wave electrode (TWE) microwave loss set the roll-off. Production Si MZMs for 100–200G/lane modules typically quote 70–100+ GHz 3-dB BW; differential-drive layouts and compact 300-mm platforms report 80–95 GHz class results . $`V_\pi L`$ for carrier-depletion Si is often $`\approx`$<!-- -->1.5–2.5 V$`\cdot`$cm, so millimeter-scale devices need 2–4 V peak-to-peak drive at the target baud inside the linear range of a SiGe or BiCMOS modulator driver (448G-class drivers exceed 120 GHz RF BW) . Unlike resonant rings, an MZM is broadband, so WDM channels do not fight thermal lock (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>); the cost is length: mm-scale shifters and splitters add 2–4 dB on chip, and the device is far larger than a ring, which matters in dense CPO tiles.

Integration is the main reason Si MZM survives competition from EML and TFLN. The modulator shares a die with Ge photodiodes, fiber grating couplers or edge couplers, monitors, and (in WDM products) MUX/de-MUX filters, all in a CMOS foundry-compatible flow. An external CW DFB or ELS (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>) couples in through a spot-size converter; the RF driver is usually a separate die wire-bonded or 2.5D packaged next to the PIC, the same assembly style as TFLN modules but without bonding a second optical material stack.

State of the art in 2025–26: Si MZMs are the default modulator in 100G/lane and 200G/lane DR/FR silicon-photonics transceivers. Pushing to 400G/lane IM/DD was open until OFC 2026, when Coherent reported 400 Gb/s PAM4 per lane with a Si MZM and commercial SiGe driver (2.5 V swing) . The same conference cycle showed a 500 $`\mu`$m compact MZM on a 300-mm platform with 94.7 GHz median EO BW and 2.4 dB on-chip insertion loss , and a differential-drive MZM with 81.8 GHz 3-dB BW with eyes to 100 GBd PAM8 . These are lab and conference demos, not shipping modules, but they close the headline lane-rate gap with ring modulators while keeping a flat passband that rings only match with tight wavelength control (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>).

##### Thin-film lithium niobate Mach–Zehnder modulators.

*TFLN* refers to a sub-micrometer slice of lithium niobate bonded to a silicon or silica handle wafer. Compared with bulk LN, the tight optical mode confinement shrinks electrode gap and interaction length, which cuts the half-wave voltage–length product $`V_\pi L`$ while keeping a wide *electro-optic* (EO) bandwidth. The modulator is a Mach–Zehnder interferometer (MZM): a *Pockels* phase shifter in each arm, driven in push-pull, converts RF voltage on a *traveling-wave electrode* (TWE) into intensity at the output coupler.

Three design constraints set whether a TFLN MZM can run at 224 GBd PAM4 ($`f_N\approx112`$ GHz). EO bandwidth, measured as the $`S_{21}`$ roll-off of optical response versus RF drive, must clear that Nyquist: production-class devices quote $`\gtrsim`$<!-- -->110 GHz 3-dB BW, and research devices with low-$`k`$ underfill or advanced TWE layouts extrapolate toward 200+ GHz . $`V_\pi L\approx1`$–2 V$`\cdot`$cm is typical, so a 5–7 mm device gives $`V_\pi\approx1.5`$–2 V that must fit inside the linear swing of a SiGe or InP driver at 112 GHz class . Along the TWE, microwave and optical group indices must match or bandwidth collapses; low-loss underfill, narrow-gap CPW or co-planar layouts, and transparent conductive oxide (TCO) electrodes trade insertion loss against efficiency .

Demonstrated IM/DD results on TFLN MZMs include 224 Gb/s PAM4 at 108 GHz EO BW (O-band, $`V_\pi L=1.02`$ V$`\cdot`$cm)  and 390 Gb/s PAM8 on the same dual-band chip (extrapolated 220 GHz BW, sub-fJ/bit in lab) . System-level proof came with eight $`\times`$<!-- -->225 GBd PAM4 lanes over 2 km using 3 nm SerDes and packaged TFLN modulators . Commercial suppliers (HyperLight, Lumiphase, and foundry lines on 200-mm silicon) now ship 110 GHz-class packaged MZMs aimed at 200–240 GBd signaling .

Integration looks unlike monolithic silicon photonics. A CW DFB or ELS feeds the TFLN chip through a Si/SiN coupler; the RF driver sits on a separate die, wire-bonded or flip-chip mounted with matched 50 $`\Omega`$ lines. Hybrid Si–LN platforms (silicon waveguides, LN overlay) were demonstrated early for 100G/lane and remain a template for co-packaged assemblies . The laser is not on the TFLN chip, so alignment, fiber attach, and thermal bias of the MZM quadrature point become validation items (<a href="#ch:validation" data-reference-type="ref+Label" data-reference="ch:validation">7</a>).

##### EML and the electro-absorption modulator.

An *EML* integrates a DFB laser with an *EAM* (electro-absorption modulator) on one InP chip. The EAM is a reverse-biased absorption region: voltage shifts the band edge (Franz-Keldysh or quantum-confined Stark effect), attenuating light with far less chirp than direct current modulation (<a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>).

EMLs dominate 100G/lane and 200G/lane DR/FR pluggables because they are single-chip, mature in supply chain, and match $`\sim`$<!-- -->70–100 GHz class EO bandwidth (<a href="#tab:tx-modulator" data-reference-type="ref+Label" data-reference="tab:tx-modulator">3.12</a>). The design limits that show up in validation are EAM bias and aging (bias sets extinction and chirp; aging drifts the curve and shows up as TDECQ/RLM creep, <a href="#ch:validation,ch:reliability" data-reference-type="ref+Label" data-reference="ch:validation,ch:reliability">[ch:validation,ch:reliability]</a>), driver swing (a few volts inside the linear absorption region; 448G-class EML drivers appeared alongside MZM drivers in 2026 ), and thermal headroom (uncooled datacom is standard; slope efficiency and bias must stay in range across case temperature).

EML wins on cost and integration through 200G/lane. Above that, external modulators (Si MZM, TFLN, rings with CW laser) chase bandwidth and chirp headroom (<a href="#sec:simzm,sec:tfln-mzm,sec:siring" data-reference-type="ref+Label" data-reference="sec:simzm,sec:tfln-mzm,sec:siring">[sec:simzm,sec:tfln-mzm,sec:siring]</a>).

##### Modulator drivers: requirements, records, outlook.

Every external modulator (Si MZM, TFLN, ring, EAM) needs an RF path that delivers enough *linear* swing at the target baud. That path is either a dedicated SiGe/BiCMOS *modulator driver* die, or (for LPO) the host SerDes itself. Laser *bias* drivers are a different circuit and a different noise budget (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>). Do not share the modulator driver’s switching returns with the CW bias rail.

##### What the driver must deliver.

At 224 GBd PAM4 the symbol Nyquist frequency is 112 GHz, so a usable driver is not just “fast enough on paper.” It needs RF bandwidth roughly $`\gtrsim`$<!-- -->100–120 GHz (3 dB) with flat gain and low group-delay ripple, output swing matched to $`V_\pi`$ or EAM drive (often $`\sim`$<!-- -->1.5–3 V peak-to-peak, differential or single-ended, part- and modulator-dependent), linearity good enough that RLM and TDECQ stay inside the PMD budget when the optical path adds its own compression (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>), and return loss / matching into 50 $`\Omega`$ (or the designed modulator impedance) so bondwire and package reflections do not eat the bandwidth you paid for on the die. Distributed (traveling-wave) SiGe drivers dominate the high-BW niche: many cascoded gain cells along an artificial transmission line. Lumped drivers win on area and power at lower baud. Flip-chip bumped die and short wirebonds matter as much as $`f_T`$: a 120 GHz die behind a long bond loop is a 70 GHz module.

##### Record and commercial snapshot (2025–26).

<a href="#tab:driver-records" data-reference-type="ref+Label" data-reference="tab:driver-records">3.11</a> separates research demos (often with offline DSP) from shipping or announced commercial parts aimed at 1.6T/3.2T modules. Commercial anchors: MACOM’s MAOM-025408 MZM and MAOM-022404 EML drivers ($`>`$<!-- -->120 GHz RF BW, OFC 2026) ; Semtech’s GN1877/GN1887 224G quad/octal family for LPO/LRO/CPO across SiPh, InP, and TFLN . Research anchors: a 130 nm SiGe distributed driver at 105.7 GHz BW and 2.25 V swing running 232 GBd PAM4 into TFLN (offline DSP) ; OFC 2026 co-designed engines at 210 GBd / 420 Gb/s PAM4 (TFLN TOSA) , 180 GBd PAM4 (InP MZM + EML-class driver) , and differential SiGe+TFLN at 140 GBd PAM8 / 1.4 pJ/bit ; plus the Si MZM postdeadline with a commercial SiGe driver at 400 Gb/s/lane and 2.5 V swing .

<span id="tab:driver-records" data-label="tab:driver-records"></span>

| Part / paper | Process | RF BW | Rate / swing | Note |
|:---|:---|:---|:---|:---|
| MACOM MAOM-025408 (MZM) | SiGe | $`>`$<!-- -->120 GHz | 448G-class PAM4 | Commercial; SiPh MZM |
| MACOM MAOM-022404 (EML) | SiGe | $`>`$<!-- -->120 GHz | 448G-class PAM4 | Commercial; EML / TFLN |
| Semtech GN1877 / GN1887 | — | 224G-class | 224 Gb/s/lane | Quad/octal; LPO path |
| RFIC 2026 distributed drv | 130 nm SiGe | 105.7 GHz | 232 GBd; 2.25 V | Research; TFLN; offline DSP |
| OFC 2026 Si MZM + SiGe | commercial SiGe | (drv-limited) | 400 Gb/s/lane; 2.5 V | Postdeadline Th4A.4 |
| OFC 2026 TFLN TOSA | co-designed | — | 210 GBd / 420 Gb/s | Driver+TFLN engine |
| OFC 2026 InP MZM + EML drv | InP + SiGe-class | 76 GHz MZM | 180 GBd PAM4 | Co-packaged engine |
| Nokia/Bell Labs hybrid | SiGe + TFLN | — | 140 GBd PAM8; 1.4 pJ/bit | Diff. drive; low $`V_\pi L`$ |

**Table .** Modulator-driver snapshot (c. 2026). Commercial rows are vendor announcements (bandwidth/swing as published); research rows often use offline DSP and short RF interconnects. “448G-class” means aimed at $`\sim`$<!-- -->400–448 Gb/s/lane PAM4 modules, not a CEI compliance claim. Sources cited in the paragraph above.

##### LPO and the host-as-driver path.

For *LPO*, the host SerDes (or a linear driver in the module with no retimer) is the modulator driver. Waveform fidelity is end to end: host FFE, connector ISI, driver/modulator nonlinearity, and TIA all land in TDECQ and pre-FEC BER (<a href="#sec:equalization,sec:tdecq,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:equalization,sec:tdecq,sec:conditioning">[sec:equalization,sec:tdecq,sec:conditioning]</a>). That is why linear-optics driver families (e.g. Semtech’s 224G set) advertise CEI-224G-Linear host EQ and tunable swing: the module cannot clean up what the host launches [Semtech 224G](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era). Retimed modules hide some of this behind DSP; they also burn the watts LPO was meant to save.

##### Outlook.

Driver roadmaps are no longer waiting on papers alone. Commercial 448G-class parts are shipping as dies: MACOM’s $`>`$<!-- -->120 GHz MZM and EML drivers (OFC 2026) are the clearest public 400G/lane announcement [MACOM](https://www.macom.com/updates/news/2026/macom-announces-two-new-448g-per-lane-drivers-for-3-2t-data-cent), while research benches already run past 200 GBd on short RF paths. Expect a short period where optics and drivers lead host SerDes, so gearboxed 224G electrical into 448G optical remains common (<a href="#sec:gearbox,sec:448g" data-reference-type="ref+Label" data-reference="sec:gearbox,sec:448g">[sec:gearbox,sec:448g]</a>). The hard problems are packaging (bondwire, FAU, faceplate connectors), co-design of peaking with modulator $`S_{21}`$, and LPO cases where driver linearity and host COM sit beside TDECQ as first-order validation items (<a href="#sec:com,sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:com,sec:prod-corners">[sec:com,sec:prod-corners]</a>). After the driver, the next ceilings are modulator EO bandwidth and the PD/TIA noise stack (<a href="#sec:simzm,sec:tfln-mzm,sec:siring,sec:pd-tia,sec:rxtech" data-reference-type="ref+Label" data-reference="sec:simzm,sec:tfln-mzm,sec:siring,sec:pd-tia,sec:rxtech">[sec:simzm,sec:tfln-mzm,sec:siring,sec:pd-tia,sec:rxtech]</a>).

**Key idea.** A 448G-class modulator driver is a $`>`$<!-- -->100 GHz linear SiGe amp with swing matched to $`V_\pi`$, not a SerDes pin. Commercial dies now claim $`>`$<!-- -->120 GHz for MZM/EML/TFLN; research shows $`\sim`$<!-- -->230 GBd on co-designed benches. Package and modulator match set the real ceiling; LPO makes the host the driver.

##### Gearboxes: when electrical and optical rates diverge.

A *gearbox* converts lane rate or modulation format between electrical and optical domains. The 448G transition often uses *two* 224G electrical lanes into one 448G optical lane (<a href="#fig:448g-paths,sec:448g" data-reference-type="ref+Label" data-reference="fig:448g-paths,sec:448g">[fig:448g-paths,sec:448g]</a>) when host SerDes or connectors lag optics.

Gearboxes add power, latency, and silicon area. They also break strict LPO: the host waveform no longer matches what the optical lane carries, so a retimed or half-retimed module is required . Expect gearboxed 3.2T modules before native 448G electrical I/O and matched VSR connectors land in volume.

Putting the platforms side by side, <a href="#tab:tx-modulator" data-reference-type="ref+Label" data-reference="tab:tx-modulator">3.12</a> summarizes the trade space at 100–400G per $`\lambda`$; <a href="#sec:siring,sec:simzm,sec:tfln-mzm,sec:eml-eam" data-reference-type="ref+Label" data-reference="sec:siring,sec:simzm,sec:tfln-mzm,sec:eml-eam">[sec:siring,sec:simzm,sec:tfln-mzm,sec:eml-eam]</a> expand each path. Through 200G/lane DR, EML still leads on cost and single-chip integration. Silicon rings and MZMs lead in CPO where area and CMOS fab matter, with Si MZM preferred for flat single-$`\lambda`$ DR/FR and rings preferred for dense WDM. TFLN leads when you need $`\gtrsim`$<!-- -->100 GHz EO BW with low chirp for native 224 GBd PAM4 in a pluggable or NPO module and silicon cannot close the 112 GHz Nyquist without heavy peaking.

<span id="tab:tx-modulator" data-label="tab:tx-modulator"></span>

| Platform | EO BW | Per-$`\lambda`$ demo | Chirp | Integration | Typical use |
|:---|:---|:---|:---|:---|:---|
| Si microring | 90–110 GHz | 224–416 Gb/s PAM4 | low | monolithic SiPh | CPO, WDM |
| Si MZM | 70–100+ GHz | 400 Gb/s PAM4 | low | monolithic SiPh | DR/FR, CPO |
| TFLN MZM | 108–110+ GHz | 224–390 Gb/s PAM4/8 | very low | hybrid + driver die | 400G/lane pluggable, FR |
| EML | 70–100 GHz | 200 Gb/s PAM4 | low | single InP chip | DR/FR to 200G/lane |

**Table .** IM/DD transmitter platforms at 100–400G per $`\lambda`$ (2026 snapshot).

The honest summary: *modulating* at 224 GBd PAM4 is demonstrated in multiple material systems when the electrical drive path is short and the driver is dedicated (not a lossy meter of PCB plus OSFP connector). *Modulating* at that rate from a switch ASIC through a pluggable module is the harder system problem. Silicon photonics rings without peaking still sit below the 112 GHz Nyquist needed for 448G-PAM4; TFLN, EML, and peaked Si rings are the near-term paths. WDM (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>) and CPO remain the architectural escape hatches: more aggregate bits without forcing every electrical lane to 224 GBd on a lossy shoreline.

##### Where the standards conversation stands.

Electrical and Ethernet standards are climbing the same ladder on slightly different clocks. OIF CEI owns the electrical I/O recipe; IEEE 802.3 owns how Ethernet names the lane and the optical PMD. Neither has locked 448G modulation yet.

##### OIF CEI (electrical I/O).

No modulation order is locked yet in CEI-448G. PAM4 remains attractive if connectors reach $`\gtrsim`$<!-- -->112 GHz and if optics stay on PAM4 (alignment for LPO, lower FEC overhead, backward compatibility with 224G gear). PAM6 is the leading compromise for bandwidth-starved host channels if connector progress stalls . Electrical IAs target a 2026–28 window .

##### IEEE 802.3 (Ethernet PHY/MAC).

Ethernet standards trail CEI slightly but follow the same lane-doubling cadence. <a href="#tab:ieee-lane" data-reference-type="ref+Label" data-reference="tab:ieee-lane">3.13</a> is the map as of mid-2026.

| Project            | Status         | Eth. lane | PHY line                     |
|:-------------------|:---------------|:----------|:-----------------------------|
| 802.3df            | Feb 2024       | 100 Gb/s  | $`\approx`$<!-- -->112G PAM4 |
| 802.3dj            | SA ballot 2026 | 200 Gb/s  | $`\approx`$<!-- -->224G PAM4 |
| 802.3 400G/lane SG | Mar 2026       | 400 Gb/s  | $`\approx`$<!-- -->448G      |

IEEE 802.3 lane-rate generations. {#tab:ieee-lane}

**802.3df** (approved February 2024) defined 200/400/800 Gb/s Ethernet using **100 Gb/s lanes** (112 GBd PAM4 class). **802.3dj** is the active 200 Gb/s-lane amendment: 200/400/800/1600 Gb/s Ethernet with PAM4 at 112 GBd, KP4 FEC, and a large PHY portfolio (copper and IM/DD optics). The draft cleared 802.3 working-group recirculation ballot in February 2026 and entered IEEE Standards Association ballot; approval is expected around late 2026 .

**400 Gb/s per lane** is the next Ethernet milestone. The *Ethernet for AI* (E4AI) ad hoc incubated demand for 3.2 Tb/s ports and 400G/lane signaling . A call for interest in March 2026 led to an IEEE 802.3 **400 Gb/s/lane Signaling Study Group** (chartered 13 March 2026) to draft a PAR for electrical interconnects and single-mode fiber reaches up to 500 m . The proposed scope has two tracks: a fast track for 400/800/1600 Gb/s on 400G/lane copper and IM/DD optics (scale-up, intra/inter-rack), and a follow-on phase for **3.2 Tb/s** and additional PHYs . That aligns with OIF CEI-448G and industry 3.2T module work, with one naming difference: IEEE quotes **400 Gb/s per lane** (MAC/info rate); CEI quotes **448 Gb/s** (line rate including FEC overhead). They refer to the same generation.

Until native 448G host SerDes and matched connectors land, expect a transition generation that gearboxes 224G electrical lanes into 448G optical lanes (<a href="#fig:448g-paths" data-reference-type="ref+Label" data-reference="fig:448g-paths">3.7</a>), then a consolidation generation with 400G/lane Ethernet PHYs where electrical and optical both run PAM4 at 224 GBd end to end.

**Key idea.** IM/DD is intensity in, power out, with FEC and DSP closing the gap that PAM4’s SNR penalty opens. Master OMA, ER, chirp/dispersion, and pre-FEC BER and you can reason about any short-reach link.

# Quantitative models: noise, RIN, and BER

The previous chapters argued mostly in architecture and measurement vocabulary. This one puts numbers behind the two questions every link engineer eventually asks: *what bit-error ratio (BER) will this receiver deliver?* and *what is the minimum signal it needs?* The answers follow a short chain of physics that has been stable for decades of IM/DD design: Gaussian statistics at the decision circuit, a handful of noise sources, and the way relative intensity noise (RIN) turns into an error floor. Understanding that chain is what lets you read a sensitivity number or a RIN floor without treating the datasheet as magic.

Everything here is backed by short, reproducible Python (in `sims/`), so the figures are computed curves rather than sketches. The models follow the treatment in Säckinger’s *Analysis and Design of Transimpedance Amplifiers for Optical Receivers*,[^12] and the sanity checks in the code reproduce that book’s worked numbers.

## The decision: from $`Q`$ to BER

A binary receiver samples a noisy voltage and compares it to a threshold. If the noise is Gaussian and the threshold is optimally placed, the BER depends on a single quality factor $`Q`$, the separation between the one and zero levels measured in units of their combined noise:
``` math
Q = \frac{I_1 - I_0}{\sigma_1 + \sigma_0},
  \qquad
  \mathrm{BER} = \tfrac{1}{2}\,\mathrm{erfc}\!\left(\frac{Q}{\sqrt{2}}\right).
```
This is the workhorse relation of link design. Its power is that it needs no assumption about pulse shape or spectrum, only that the sampled noise is Gaussian.[^13] Two reference points anchor everything that follows: the classic uncoded target $`\mathrm{BER}=10^{-12}`$ needs $`Q=7.03`$, while the *KP4* Reed–Solomon FEC (<a href="#ch:imdd" data-reference-type="ref+Label" data-reference="ch:imdd">3</a>) corrects a pre-FEC $`\mathrm{BER}\approx2.4\times10^{-4}`$, needing only $`Q\approx3.5`$.

    from scipy.special import erfc, erfcinv
    import numpy as np

    def q_to_ber(q):
        return 0.5 * erfc(q / np.sqrt(2))

    def ber_to_q(ber):
        return np.sqrt(2) * erfcinv(2 * ber)

<figure id="fig:berq" data-latex-placement="ht">
<embed src="figures/fig_ber_vs_q.pdf" />
<figcaption>The Gaussian decision curve. Every dB of <span class="math inline"><em>Q</em></span> buys orders of magnitude of BER near the knee, which is why FEC (trading a modest <span class="math inline"><em>Q</em></span> for a huge BER improvement) is decisive.<span id="fig:berq" data-label="fig:berq"></span></figcaption>
</figure>

<a href="#fig:berq" data-reference-type="ref+Label" data-reference="fig:berq">4.1</a> shows why the curve is so steep near the operating point: a small change in $`Q`$ (equivalently, in received power) moves the BER by orders of magnitude. This steepness is exactly what FEC exploits: nudging the required $`Q`$ from 7.03 down to 3.5 relaxes the optical power budget by several dB.

## The receiver noise budget

$`Q`$ is only as good as our estimate of $`\sigma`$. Three noise sources dominate a short-reach IM/DD receiver, and they add in quadrature (they are independent):

Thermal / circuit noise  
the input-referred noise of the TIA and following stages, roughly white, so its variance scales with the noise bandwidth: $`\sigma_{\text{th}}^2 = i_n'^2\,\mathrm{BW}`$, where $`i_n'`$ is a noise-current density (A/$`\sqrt{\text{Hz}}`$). *Signal-independent.*

Shot noise  
from the discreteness of photocurrent, $`\sigma_{\text{shot}}^2 = 2q\,I\,\mathrm{BW}`$. *Grows with signal*, so it is larger on the ones than the zeros.

RIN (relative intensity noise)  
the laser’s own intensity fluctuations, $`\sigma_{\text{RIN}}^2 = \mathrm{RIN}_{\text{lin}}\,I^2\,\mathrm{BW}`$, with $`\mathrm{RIN}_{\text{lin}} = 10^{\mathrm{RIN[dB/Hz]}/10}`$. *Grows with the square of signal*, the key fact of the next section.

Because shot and RIN noise are signal dependent, we evaluate $`\sigma_1`$ and $`\sigma_0`$ separately and form $`Q`$ with their sum. The core of the model is just this:

    def nrz_q(p_avg_w, responsivity, i_thermal_rms, bw,
              er_db=np.inf, rin_db_hz=-np.inf):
        p1, p0 = er_levels(p_avg_w, er_db)      # one / zero optical powers
        i1, i0 = responsivity * p1, responsivity * p0
        var1 = i_thermal_rms**2 + 2*Q_E*i1*bw   # thermal + shot
        var0 = i_thermal_rms**2 + 2*Q_E*i0*bw
        if np.isfinite(rin_db_hz):
            rin = 10**(rin_db_hz / 10)
            var1 += rin * i1**2 * bw            # RIN grows as I^2
            var0 += rin * i0**2 * bw
        return (i1 - i0) / (np.sqrt(var1) + np.sqrt(var0))

## RIN and the BER floor

Here is the consequence that makes RIN worth its own section. Thermal noise is fixed, so pouring on more optical power raises $`I_1-I_0`$ while $`\sigma_{\text{th}}`$ stays put, so $`Q`$ improves without limit. But RIN noise scales *with the signal itself*: $`\sigma_{\text{RIN}} \propto I`$. Once RIN dominates, the signal and its noise grow together and $`Q`$ stops improving. Taking the high-power, high-extinction limit (thermal and shot negligible, $`I_0\to0`$):
``` math
Q_{\max} \;=\; \frac{I_1}{\sigma_{\text{RIN},1}}
           \;=\; \frac{1}{\sqrt{\mathrm{RIN}_{\text{lin}}\,\mathrm{BW}}}.
```
This is a hard ceiling: no amount of transmit power or receiver sensitivity can push $`Q`$ past it, so there is a BER floor set entirely by the laser and the bandwidth. Equivalently, the power penalty to hold a target $`Q`$ is
``` math
\mathrm{PP} = \frac{1}{\sqrt{1 - Q^2\,\mathrm{RIN}_{\text{lin}}\,\mathrm{BW}}},
```
which diverges as $`Q\to Q_{\max}`$.

<figure id="fig:berpower" data-latex-placement="ht">
<embed src="figures/fig_ber_vs_power_rin.pdf" />
<figcaption>With RIN present, the BER stops falling no matter how much power is added. The thermal/shot-only curve dives; each RIN level flattens into a floor. (RIN values here are deliberately high to make the floor visible in-frame; good DFBs at <span class="math inline"> &lt; −150</span> dB/Hz have no floor at these rates; see text.)<span id="fig:berpower" data-label="fig:berpower"></span></figcaption>
</figure>

<figure id="fig:rinfloor" data-latex-placement="ht">
<embed src="figures/fig_rin_floor.pdf" />
<figcaption>The RIN ceiling <span class="math inline">$Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$</span>. Wider receiver bandwidth (higher lane rate) integrates more RIN, lowering the ceiling. Where a curve dips below the dotted anchors, that link can no longer reach the corresponding BER.<span id="fig:rinfloor" data-label="fig:rinfloor"></span></figcaption>
</figure>

<a href="#fig:berpower" data-reference-type="ref+Label" data-reference="fig:berpower">4.2</a> shows the floor directly; <a href="#fig:rinfloor" data-reference-type="ref+Label" data-reference="fig:rinfloor">4.3</a> plots the ceiling versus RIN for three lane rates. The bandwidth dependence matters: doubling the lane rate doubles the noise bandwidth and drops $`Q_{\max}`$ by $`\sqrt{2}`$ ($`\approx1.5`$ dB of margin), so RIN that is harmless at 25G can bite at 200G. This is the quantitative reason the laser chapter (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>) lists RIN among the parameters that decide pass/fail.

### Typical RIN values (2026)

How much RIN headroom do real sources have? <a href="#tab:rin-values" data-reference-type="ref+Label" data-reference="tab:rin-values">4.1</a> collects representative figures. Two cautions on reading them. First, standards quote *$`\mathrm{RIN}_x\mathrm{OMA}`$*, RIN referenced to the OMA and measured under a specified optical return loss (ORL) $`x`$, because back-reflections into the laser raise its noise, so a spec limit is a stressed, worst-case number, not the device’s quiet intrinsic RIN.[^14] Second, RIN degrades with optical feedback, so isolator-free and co-packaged designs care as much about *feedback tolerance* as about the isolated number, one reason quantum-dot lasers (near-zero linewidth-enhancement factor) are attractive for CPO .

A RIN number in dB/Hz is, by itself, incomplete: because RIN is *relative*, it only becomes an absolute noise current once the photocurrent $`I=\mathcal{R}P`$ is fixed. The intensity-noise current density is
``` math
i_{\text{RIN}} = \sqrt{\mathrm{RIN}_{\text{lin}}}\;I \quad[\text{A}/\sqrt{\text{Hz}}],
  \qquad
  S_{\text{RIN}} = \mathrm{RIN}_{\text{lin}}\,I^2 \quad[\text{A}^2/\text{Hz}],
```
so it scales linearly with received power. <a href="#tab:rin-values" data-reference-type="ref+Label" data-reference="tab:rin-values">4.1</a> therefore lists both the RIN and the current density it produces at a common reference operating point ($`\mathcal{R}=0.8`$ A/W, $`P_{\text{rx}}=0`$ dBm, i.e. $`I=0.8`$ mA), the units a receiver designer actually compares against.

<span id="tab:rin-values" data-label="tab:rin-values"></span>

| Source | RIN (dB/Hz) | $`i_{\text{RIN}}`$ @ 0 dBm (pA/$`\sqrt{\text{Hz}}`$) | Note |
|:---|:---|:---|:---|
| Standards spec limit (400G-FR4, 100GBASE-BR) | $`\le -136`$ | $`\ge 127`$ | stressed, w/ ORL |
| Datacom VCSEL, 850 nm (MMF) | $`-135`$ to $`-145`$ | $`45`$ to $`142`$ | quiet parts $`\le\!-145`$ |
| Good datacom DFB / EML | $`-145`$ to $`-155`$ | $`14`$ to $`45`$ | CPO ELS targets $`\le\!-145`$ |
| Quantum-dot laser on Si | $`-140`$ to $`-150`$ | $`25`$ to $`80`$ | temp-stable, isolator-free |
| Heterogeneous / self-injection-locked Si laser | $`-155`$ to $`-165`$ | $`4.5`$ to $`14`$ | high-$`Q`$ feedback |
| Lab record (QD, quiet pump + injection lock) | down to $`\sim\!-168`$ | $`\sim 3.2`$ | research |

**Table .** Representative RIN by source type (c. 2026) and the intensity-noise *current* it produces at a reference operating point: $`\mathcal{R}=0.8`$ A/W, $`P_{\text{rx}}=0`$ dBm, so $`I=0.8`$ mA. The density is $`i_{\text{RIN}}=\sqrt{\mathrm{RIN}_{\text{lin}}}\,I`$; the PSD in A$`^2`$/Hz is its square. Spec limits are stressed $`\mathrm{RIN}_x\mathrm{OMA}`$ values; the rest are typical intrinsic RIN.

For scale, at that same $`0.8`$ mA the *shot*-noise density is $`\sqrt{2qI}=16`$ pA/$`\sqrt{\text{Hz}}`$ ($`S=2.6\times10^{-22}`$ A$`^2`$/Hz) and a good high-speed TIA adds roughly $`25`$ pA/$`\sqrt{\text{Hz}}`$ of thermal noise. So a VCSEL at $`-140`$ dB/Hz ($`80`$ pA/$`\sqrt{\text{Hz}}`$) already dominates both, while a heterogeneous source at $`-160`$ dB/Hz ($`8`$ pA/$`\sqrt{\text{Hz}}`$) is a minor term. The key asymmetry: thermal noise is fixed and shot grows only as $`\sqrt{I}`$, but RIN grows as $`I`$, so at low received power thermal wins and RIN is irrelevant, and only above a break-in power (<a href="#fig:noisedensity" data-reference-type="ref+Label" data-reference="fig:noisedensity">4.4</a>) does RIN take over. That is why quoting a RIN figure without an operating power says little.

<figure id="fig:noisedensity" data-latex-placement="ht">
<embed src="figures/fig_noise_density_vs_power.pdf" />
<figcaption>Noise current densities versus received power. Thermal is flat, shot <span class="math inline">$\propto\!\sqrt{I}$</span>, RIN <span class="math inline">∝ <em>I</em></span>; the RIN curves cross the fixed thermal floor only above a break-in power, which is why RIN only “makes sense” once the optical power (hence <span class="math inline"><em>I</em> = ℛ<em>P</em></span>) is stated.<span id="fig:noisedensity" data-label="fig:noisedensity"></span></figcaption>
</figure>

Put these against the ceiling. At 200G-PAM4 bandwidths ($`\mathrm{BW}\approx75`$ GHz), even the worst spec-compliant number ($`-136`$ dB/Hz) gives $`Q_{\max}\approx23`$ (far above the $`Q=7`$ needed for $`10^{-12}`$), so for well-behaved sources RIN is *not* the limiter; thermal noise is. RIN becomes the story only when feedback, aging, or a marginal source pushes the effective figure toward $`-125`$ dB/Hz, where $`Q_{\max}`$ falls through the uncoded target. That is why the practical spec is written against a stressed ORL, and why feedback-tolerant sources matter for dense, isolator-free integration. A third path to excess intensity noise is electrical: laser bias-driver current noise converts to equivalent RIN (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>) and must be budgeted separately from intrinsic laser RIN.

**Key idea.** Thermal noise is beaten by power; RIN is not. Because $`\sigma_{\text{RIN}}\propto I`$, intensity noise imposes a floor $`Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}`$ that no link budget can climb past, and it worsens as lane rates (and thus bandwidths) rise. Good 2026 sources ($`-145`$ to $`-165`$ dB/Hz) sit comfortably below that floor; feedback and aging are what erode the margin.

## Sensitivity and OMA

Turning the question around (*what is the least power that meets a target BER?*) gives the sensitivity. Referring the receiver’s input noise current $`i_n`$ back to the optical input through the responsivity $`\mathcal{R}`$:
``` math
P_{\text{sens}} = \frac{Q\,i_n}{\mathcal{R}}
  \qquad\text{(average power)},\qquad
  P_{\text{sens}}^{\text{OMA}} = \frac{2\,Q\,i_n}{\mathcal{R}}.
```
Modern short-reach standards specify the *OMA* (optical modulation amplitude, $`P_1-P_0`$) rather than average power, because it decouples the sensitivity spec from the transmitter’s extinction ratio. As a check, the textbook example ($`i_n = 1~\mu`$A, $`\mathcal{R}=0.8`$ A/W, $`\mathrm{BER}=10^{-12}`$) gives $`P_{\text{sens}}=7.03\times1~\mu\text{A}/0.8 = 8.8~\mu`$W, or $`-20.6`$ dBm, which the code reproduces. A finite extinction ratio costs a further $`\mathrm{PP}=(\mathrm{ER}+1)/(\mathrm{ER}-1)`$: $`0.87`$ dB at 10 dB ER, $`2.2`$ dB at 6 dB ER. These penalties feed directly into the link budgets of <a href="#ch:imdd" data-reference-type="ref+Label" data-reference="ch:imdd">3</a> and the transmitter and dispersion eye closure quaternary (TDECQ) discussion of <a href="#ch:validation" data-reference-type="ref+Label" data-reference="ch:validation">7</a>.

##### Worked example: DR4-class budget check.

Take a 200G/lane DR link with Ge-on-Si PIN ($`\mathcal{R}=0.9`$ A/W), TIA $`i_n=13`$ pA/$`\sqrt{\text{Hz}}`$, bandwidth $`\approx60`$ GHz, target pre-FEC BER $`2.4\times10^{-4}`$ ($`Q\approx3.5`$, <a href="#sec:qber,sec:kp4" data-reference-type="ref+Label" data-reference="sec:qber,sec:kp4">[sec:qber,sec:kp4]</a>).

Integrated noise: $`i_n \sqrt{\mathrm{BW}} \approx 13\times10^{-12}\times\sqrt{60\times10^9}
\approx 3.2~\mu`$A rms. Required OMA:
``` math
P_{\text{OMA,sens}} = \frac{2 Q i_n \sqrt{\mathrm{BW}}}{\mathcal{R}}
\approx \frac{2\times3.5\times3.2~\mu\text{A}}{0.9} \approx 25~\mu\text{W}
\approx -16~\text{dBm}.
```
Add $`\sim`$<!-- -->3 dB TDECQ penalty, $`\sim`$<!-- -->2 dB connector/fiber, $`\sim`$<!-- -->2 dB system margin: need Tx OMA $`\approx -16 + 7 \approx -9`$ dBm class at the receiver input, i.e. roughly $`-6`$ to $`-4`$ dBm launched depending on reach. If measured sensitivity is worse, bisect RIN, reflections, and ER (<a href="#sec:link-budget,sec:optical-channel" data-reference-type="ref+Label" data-reference="sec:link-budget,sec:optical-channel">[sec:link-budget,sec:optical-channel]</a>).

## Receiver technologies and their noise (2026)

The sensitivity formula $`P_{\text{sens}}=Q\,i_n/\mathcal{R}`$ has exactly two device inputs: the photodiode responsivity $`\mathcal{R}`$ and the amplifier’s input-referred noise current $`i_n`$. So “receiver noise performance” is really a statement about the detector–TIA pair, and the winning short-reach recipe is the one the question anticipates: a *waveguide germanium-on-silicon PIN* feeding a *tightly integrated CMOS or SiGe-BiCMOS TIA*. The reasons are all in the two parameters above plus a parasitic (<a href="#sec:pd-tia" data-reference-type="ref+Label" data-reference="sec:pd-tia">4.5.0.0.1</a> details the TIA side).

##### Photodiodes and transimpedance amplifiers.

The photodiode converts photons to photocurrent; the *TIA* (transimpedance amplifier) converts current to voltage with low input-referred noise. For PAM4 at 100–224G/lane:

- **PIN (Ge-on-Si):** no internal gain; lowest excess noise; mainstream (<a href="#tab:rxtech" data-reference-type="ref+Label" data-reference="tab:rxtech">4.4</a>). Capacitance at the TIA input dominates $`i_n`$.

- **APD**: internal multiplication gives 5–9 dB sensitivity gain at the cost of excess noise factor and bias voltage; Ge/Si APDs now reach $`>\!100`$ GHz class .

- **UTC/MUTC:** electron-only transport for $`>\!200`$ GHz BW and high saturation; used when linearity and speed beat raw sensitivity .

The TIA often embeds *CTLE* for LPO (<a href="#sec:equalization,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:equalization,sec:conditioning">[sec:equalization,sec:conditioning]</a>): a fixed high-frequency boost before the host SerDes ADC. Co-packaging PD and TIA (sub-mm interconnect) is the noise win repeated throughout this book (<a href="#ch:firstprinciples" data-reference-type="ref+Label" data-reference="ch:firstprinciples">2</a>).

##### Why Ge-on-Si wins the mainstream.

Germanium grown on silicon absorbs the O- and C-bands, is fully CMOS-process-compatible, and is built *on the same PIC* as the modulators and couplers. Modern devices reach $`\mathcal{R}\approx0.8`$–$`1.0`$ A/W with dark currents of single-digit to tens of nA and, in 2025 research, $`-3`$ dB bandwidths beyond 100 GHz (e.g. a recessed Ge/Si PIN at 106 GHz, $`0.93`$ A/W, $`<10`$ nA; SiN-coupled lateral Ge $`>110`$ GHz at 1 mA) . Crucially, monolithic or 3D/flip-chip co-integration keeps the PD-to-TIA interconnect sub-millimetre, so the input node capacitance stays tens of fF, and since a TIA’s input-referred noise rises with that capacitance ($`i_n \!\propto\! C\,f^{3/2}`$ in the front-end limit), *short is quiet*. This is the same capacitance argument that drives co-packaging in <a href="#ch:firstprinciples" data-reference-type="ref+Label" data-reference="ch:firstprinciples">2</a> (Miller’s receiver point), now cashed out as noise current.

##### What the TIA must deliver.

The TIA is the receive twin of the modulator driver (<a href="#sec:drivers" data-reference-type="ref+Label" data-reference="sec:drivers">3.14.3.0.10</a>). At 224 GBd PAM4 you need bandwidth $`\gtrsim`$<!-- -->50–70 GHz for a 112 GBd Nyquist-class front-end (often less than the Tx driver BW because the optical channel and reference receiver already band-limit; LPO pushes for flatter, more linear TIAs), input-referred noise in the low teens of pA$`/\sqrt{\mathrm{Hz}}`$ once co-packaged with a low-$`C`$ PD, linearity / overload so large OMA and reflections do not crush PAM4 levels (RLM) or trip AGC into a bad corner, and optional CTLE for LPO/LRO so the host SerDes sees a usable eye without module DSP (<a href="#sec:equalization,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:equalization,sec:conditioning">[sec:equalization,sec:conditioning]</a>). Noise scales with input capacitance: $`i_n \propto C\,f^{3/2}`$ in the front-end limit. That is why co-packaging (or monolithic PD+TIA) is not optional at 200G+: every millimetre of bondwire is noise and BW you cannot recover with FEC.

##### Noise levels you actually budget.

<a href="#tab:tia-noise" data-reference-type="ref+Label" data-reference="tab:tia-noise">4.2</a> puts the model numbers next to published front-ends. Shot noise at 0 dBm into $`\mathcal{R}=0.8`$ A/W is $`\sqrt{2qI}\approx16`$ pA$`/\sqrt{\mathrm{Hz}}`$; a good TIA sits near that floor. Worse $`i_n`$ or higher $`C`$ burns sensitivity linearly via $`P_{\mathrm{sens}}=Q\,i_n/\mathcal{R}`$ (<a href="#sec:sensitivity" data-reference-type="ref+Label" data-reference="sec:sensitivity">4.4</a>).

<span id="tab:tia-noise" data-label="tab:tia-noise"></span>

| Front-end | $`i_n`$ (pA$`/\sqrt{\mathrm{Hz}}`$) | BW / rate | Sensitivity note |
|:---|:---|:---|:---|
| Typical “good” short-reach TIA (book model) | $`\sim`$<!-- -->25 | — | older rule-of-thumb floor |
| 16-nm CMOS + co-pkg PD | 16.9 | 32 GHz / 112G PAM4 | $`-8.2`$ dBm class |
| 55-nm SiGe $`4\times`$<!-- -->112 GBd linear TIA | 13.2 | 65 GHz / 224G | $`\sim`$<!-- -->1.2 pJ/bit |
| Shot noise @ 0 dBm, $`\mathcal{R}=0.8`$ A/W | $`\approx`$<!-- -->16 | — | physics floor at that power |

**Table .** Input-referred TIA noise densities used in link budgets (c. 2023–26 published front-ends). Integrate $`i_n\sqrt{\mathrm{BW}}`$ for rms noise before applying $`Q`$ (<a href="#sec:sensitivity" data-reference-type="ref+Label" data-reference="sec:sensitivity">4.4</a>). Sources in text.

2026 linear PAM4 front-ends land around $`10`$–$`17`$ pA$`/\sqrt{\text{Hz}}`$: e.g. $`16.9`$ pA$`/\sqrt{\text{Hz}}`$ at 112G in 16-nm CMOS ($`-8.2`$ dBm sensitivity)  and $`13.2`$ pA$`/\sqrt{\text{Hz}}`$ at 224G in 55-nm SiGe BiCMOS (65 GHz BW, 1.2 pJ/bit) . Put these in the model: $`i_n\approx13`$ pA$`/\sqrt{\text{Hz}}`$ integrated over $`\sim\!60`$ GHz is $`\approx3.2~\mu`$A rms, giving an NRZ average sensitivity near $`-15`$ dBm; the PAM4 level penalty lands OMA sensitivities in the $`-8`$ to $`-10`$ dBm range these front-ends report.

##### Record and commercial snapshot (2025–26).

<a href="#tab:rx-records" data-reference-type="ref+Label" data-reference="tab:rx-records">4.3</a> pairs detectors and TIAs. Commercial linear-optics TIAs (Semtech GN1834L/DL, GN1838DL) target LPO/LRO/CPO at 224G/lane with on-chip EQ; Semtech has also shown 448G-class PMD ICs (TN14740 TIA) at OFC 2026 demos (vendor demonstration; not a volume datasheet claim) . On the detector side, recessed Ge/Si PINs at 106 GHz / 0.93 A/W , Ge/Si UMC-APDs at 105 GHz with $`\sim`$<!-- -->9 dB sensitivity gain over PIN at 224/260G PAM4 , waveguide Ge/Si APDs toward 100 GHz at 2 A/W , and OFC 2026 Ge-on-Si APDs at 180 GBd PAM4  mark the research edge. UTC/MUTC PDs remain the high-saturation / $`>\!200`$ GHz niche .

<span id="tab:rx-records" data-label="tab:rx-records"></span>

| Part / paper | Type | BW / $`i_n`$ or $`\mathcal{R}`$ | Rate / sens. | Note |
|:---|:---|:---|:---|:---|
| Semtech GN1834L/DL / GN1838DL | TIA | 224G-class; linear+EQ | 224 Gb/s/lane | Commercial LPO/CPO family |
| Semtech TN14740 (demo) | TIA | 448G-class | 448G/lane demo | OFC 2026 booth; provisional |
| SiGe $`4\times`$<!-- -->112 GBd TIA | TIA | 65 GHz; 13.2 pA$`/\sqrt{\mathrm{Hz}}`$ | 224G PAM4 | Research / product-class paper |
| 16-nm CMOS + co-pkg PD | TIA+PD | 16.9 pA$`/\sqrt{\mathrm{Hz}}`$ | 112G; $`-8.2`$ dBm | Co-packaged win |
| Recessed Ge/Si PIN | PD | 106 GHz; 0.93 A/W | 200 GBd-class | $`<`$<!-- -->10 nA dark |
| Ge/Si UMC-APD | APD | 105 GHz @ $`M\!\approx\!7`$ | 224/260G; $`-10.9`$/$`-10.1`$ dBm | $`\sim`$<!-- -->9 dB over PIN |
| Ge/Si WG APD (300 mm) | APD | $`>`$<!-- -->100 GHz; 2 A/W @ 70 GHz | 400G/lane target | 7 V bias class |
| OFC 2026 Ge-on-Si APD | APD | 70–100 GHz; 1.5–2 A/W | 180 GBd PAM4 | O- and C-band |
| UTC / MUTC-PD | PD | $`>\!110`$–200 GHz | high $`I_{\mathrm{sat}}`$ | Linear / LPO niche |

**Table .** Receiver snapshot (c. 2025–26). Commercial TIA rows are vendor announcements; APD/PIN rows mix production-intent SiPh with research demos. Sensitivities are as published (FEC threshold varies).

##### Reasonable alternatives to Ge PIN + quiet TIA.

<a href="#tab:rxtech" data-reference-type="ref+Label" data-reference="tab:rxtech">4.4</a> lays the detector menu out. III-V InGaAs PINs (flip-chipped) trade monolithic integration for higher power handling and remain common in discrete modules. Avalanche photodiodes add internal gain for $`\sim\!5`$–$`9`$ dB of sensitivity (attractive for power-starved or high-split links) at the cost of excess noise, bias complexity, and, historically, bandwidth; that bandwidth excuse is fading fast above 100 GHz . Uni-traveling-carrier (UTC/MUTC) PDs use electron-only transport for very high saturation current, linearity, and bandwidth ($`>\!200`$ GHz) but modest responsivity, a fit for linear/LPO and $`>\!200`$ GBd analog optics more than for raw sensitivity . SOA-preamplified receivers bolt optical gain ahead of the PD for large effective responsivity and reach, but pay in ASE noise figure, power, and complexity.

<span id="tab:rxtech" data-label="tab:rxtech"></span>

| Detector | $`\mathcal{R}`$ (A/W) | $`-3`$ dB BW | Integration | Where it fits |
|:---|:---|:---|:---|:---|
| Ge-on-Si waveguide PIN | $`0.8`$–$`1.0`$ | $`60`$–$`>\!100`$ GHz | monolithic on SiPh | mainstream short-reach / CPO |
| III-V InGaAs PIN (flip-chip) | $`0.6`$–$`0.9`$ | $`60`$–$`>\!100`$ GHz | hybrid / flip-chip | discrete modules, high power |
| APD (Ge/Si, InP, UMC) | effective $`\uparrow`$ (gain) | up to $`\sim\!100`$ GHz+ | hybrid / emerging | power-starved links; $`+5`$–$`9`$ dB sens. |
| UTC / MUTC-PD | $`0.1`$–$`0.8`$ | $`>\!110`$–$`200`$ GHz | III-V | linear/LPO, $`>\!200`$ GBd, high saturation |
| SOA-preamplified PD | effective $`\gg\!1`$ | $`\sim\!50`$ GHz | III-V PIC | tight power budgets; adds ASE noise |

**Table .** Short-reach receiver detector options, c. 2026. Ranges span production to recent research; APD/UTC/SOA figures are effective (with gain) or device-record.

##### Outlook.

Volume short-reach receive stays on PIN + SiGe/CMOS TIA: noise in the low teens of pA$`/\sqrt{\mathrm{Hz}}`$ with $`>\!100`$ GHz Ge PINs is enough for DR/FR PAM4 when co-packaged, so the fight is capacitance and yield, not a new detector physics. Linear optics raises the bar: LPO/LRO need high linearity, on-chip EQ, and multi-lane density (Semtech’s 224G family is the public commercial marker; 448G TIA demos are still provisional, <a href="#sec:drivers" data-reference-type="ref+Label" data-reference="sec:drivers">3.14.3.0.10</a>). APDs are back in the 200G conversation when several dB of sensitivity gain changes a power-limited plant; UTC/MUTC matter when the impairment is saturation or $`>\!200`$ GBd analog fidelity rather than photons per bit. Bondwire and FAU still set $`C`$ and BW, which is why CPO/NPO win on noise for the same reason they win on energy (<a href="#ch:firstprinciples" data-reference-type="ref+Label" data-reference="ch:firstprinciples">2</a>).

**Key idea.** Receiver performance is $`\mathcal{R}`$ and $`i_n`$, with $`i_n`$ set by PD+TIA capacitance. Budget $`10`$–$`17`$ pA$`/\sqrt{\mathrm{Hz}}`$ co-packaged TIAs and $`>\!100`$ GHz Ge PIN/APD detectors; use APD gain or UTC saturation when the link demands it. LPO makes TIA linearity as important as raw noise.

## NRZ versus PAM4, at equal bit rate

The 224G-per-lane roadmap (<a href="#ch:imdd" data-reference-type="ref+Label" data-reference="ch:imdd">3</a>) rides on PAM4, so it is worth seeing the trade quantitatively. PAM4 sends two bits per symbol using four levels, so at a fixed bit rate its symbol rate (and thus noise bandwidth) is halved, collecting less noise. But its three eyes each span only a third of the OMA, costing roughly $`20\log_{10}3 \approx 9.5`$ dB of vertical separation. <a href="#fig:pam4" data-reference-type="ref+Label" data-reference="fig:pam4">4.5</a> pits the two at a common 100 Gb/s: PAM4’s narrower bandwidth partly offsets its level penalty, but it still needs several dB more received power for the same BER, repaid by halving the electrical bandwidth the SerDes and optics must support. That balance is exactly why 100G/lane went NRZ and 200G/lane went PAM4.

<figure id="fig:pam4" data-latex-placement="ht">
<embed src="figures/fig_nrz_vs_pam4.pdf" />
<figcaption>NRZ (100 GBaud) versus PAM4 (50 GBaud) at the same 100 Gb/s. PAM4 pays a level penalty but relaxes bandwidth; the crossover with the KP4 pre-FEC threshold sets the required operating power.<span id="fig:pam4" data-label="fig:pam4"></span></figcaption>
</figure>

**Key idea.** Four relations carry most of short-reach link design: the Gaussian $`\mathrm{BER}(Q)`$, the quadrature noise budget (thermal + shot + RIN), the RIN floor $`Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}`$, and the sensitivity $`P_{\text{sens}}=Q\,i_n/\mathcal{R}`$. With these (and a few dozen lines of Python) you can predict, budget, and debug a link before touching a bench.

# Lasers for optical interconnects

Every optical link begins with a light source, and at fleet scale that source is usually the reliability bottleneck as well as the first item on the link budget. Datacenter interconnects have spent two decades climbing from coarse multimode optics toward dense single-mode WDM and co-packaged engines; each step changed which laser family won and which measurements decided pass/fail. This chapter follows that arc: the device families in use today, how a roadmap choice becomes a measurable requirements slice, the LIV/SMSR/RIN suite, how bias drivers enter the intensity-noise budget, aging and derating, and the external laser modules (ELSFP, CW-WDM) that make co-packaged optics serviceable.

## Device families

The short-reach market does not use one laser. It uses a small set of families, each tuned to a reach, a fiber type, and a packaging style. Broadly, the industry moved from multimode VCSEL arrays inside the rack, to single-mode DFB/EML pluggables for DR/FR, to external CW sources feeding silicon or TFLN modulators for CPO and 400G/lane. The list below is the vocabulary you will meet on datasheets and in supplier meetings; later sections explain how to measure and qualify each one.

DFB (distributed feedback)  
a grating along the active region gives single-mode output; the workhorse continuous-wave (CW) or directly modulated source for CWDM and LAN-WDM (<a href="#sec:dfb-eml" data-reference-type="ref+Label" data-reference="sec:dfb-eml">5.3</a>).

DBR (distributed Bragg reflector)  
the grating sits outside the gain region; enables tunable variants.

DML (directly modulated laser)  
modulate the bias current directly: cheap and low-power, but chirp-limited over dispersive fiber (<a href="#sec:dml-vcsel" data-reference-type="ref+Label" data-reference="sec:dml-vcsel">5.2</a>).

EML (externally modulated laser)  
*EML*: a DFB integrated with an *EAM*. Low chirp and high bandwidth make it the dominant 100–200G/lane transmitter for single-mode links at DR (500 m) and shorter (<a href="#sec:dfb-eml,sec:eml-eam" data-reference-type="ref+Label" data-reference="sec:dfb-eml,sec:eml-eam">[sec:dfb-eml,sec:eml-eam]</a>).

CW laser + TFLN MZM  
an external CW source feeds a thin-film lithium niobate Mach–Zehnder modulator on a separate chip. Very low chirp and $`\gtrsim`$<!-- -->100 GHz EO bandwidth make this the leading path to 400G/lane pluggables and high-baud FR links; see <a href="#sec:tfln-mzm,tab:tx-modulator" data-reference-type="ref+Label" data-reference="sec:tfln-mzm,tab:tx-modulator">[sec:tfln-mzm,tab:tx-modulator]</a>.

CW laser + Si MZM  
an external CW source feeds a silicon Mach–Zehnder modulator on the same PIC (<a href="#sec:simzm" data-reference-type="ref+Label" data-reference="sec:simzm">3.14.3.0.7</a>). Low chirp, flat passband, and CMOS fab integration make this the default for 100–200G/lane DR/FR SiPh modules; 400G/lane demos appeared in 2026.

CW laser + Si ring  
same laser architecture, but a microring or microdisk modulator on the PIC (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>). Smaller footprint and strong WDM/CPO fit; wavelength lock and thermal crosstalk dominate validation (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>).

CW-WDM / multi-wavelength sources  
high-power, multi-wavelength CW lasers (per the CW-WDM MSA) that feed comb-like WDM architectures (<a href="#sec:cwwdm-laser,sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser,sec:cwwdm">[sec:cwwdm-laser,sec:cwwdm]</a>).

VCSEL  
850–940 nm multimode sources for short-reach links over multimode fiber; cheap but reach-limited and less relevant at 200G/lane.

External laser source (ELS/ELSFP)  
a pluggable laser module supplying CW light to a co-packaged switch, so a failed laser is field-replaceable (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

## Directly modulated lasers and VCSELs

Before EMLs and silicon photonics took over single-mode datacenter ports, most volume optics were either a cheap *DML* on single-mode fiber or a *VCSEL* array into multimode fiber. Both still matter at the low-cost, short-reach edge of the market, and both show why chirp, modal bandwidth, and temperature push AI fabrics toward externally modulated single-mode sources.

A DML modulates laser bias current directly. The transmitter is simple and efficient, but the same carrier dynamics that make modulation easy also produce chirp: intensity changes drag the optical frequency along (<a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>). Over multimode or very short single-mode runs that is often acceptable. Over dispersive single-mode fiber at tens of GBd, the chirp turns into inter-symbol interference and closes the eye. Validation therefore focuses on extinction ratio, pattern-dependent chirp, and RIN, not just average power.

VCSELs took a different path. They emit from a vertical cavity at 850–940 nm straight into multimode fiber, so parallel arrays are easy to assemble and cheap to ship. That combination made VCSEL SR optics the default for early 40G/100G Ethernet inside the rack (100G-SR4 and its cousins): short ribbons of MMF, high lane count, low dollars per gigabit. The same physics that made them attractive also capped their future. Multimode fiber has modal bandwidth and modal noise limits; VCSEL bandwidth and reliability both degrade with temperature; and as lane rates climb toward 100 G and 200 G, those limits arrive sooner. The industry response has been incremental (better OM4/OM5 fiber, tighter specs, sometimes PAM4 on MMF) rather than a clean leap to 400G/lane SMF DR. In practice, MMF reach and modal dispersion keep VCSEL links in the SR box (<a href="#sec:pmd-reach" data-reference-type="ref+Label" data-reference="sec:pmd-reach">3.13</a>), while hyperscale AI fabrics standardize on single-mode DR/FR and CPO.

Neither family is the path to 400G/lane SMF DR. EMLs and external modulators (<a href="#sec:dfb-eml,sec:simzm,tab:tx-modulator" data-reference-type="ref+Label" data-reference="sec:dfb-eml,sec:simzm,tab:tx-modulator">[sec:dfb-eml,sec:simzm,tab:tx-modulator]</a>) own that space. Pattern-aware chirp linearization can stretch a DML a little farther, but it does not change the physics at FR distances: if you need low chirp and high EO bandwidth at fleet scale, you leave direct modulation behind.

## DFB and EML: the workhorse transmitters

Once single-mode DR/FR became the hyperscale default, most short-reach ports started with an InP laser chip. Two configurations still dominate production: the CW or directly modulated DFB, and the EML that adds an electro-absorption modulator on the same die.

##### DFB.

A distributed-feedback laser has a grating along the active region that selects one longitudinal mode. Spec-sheet metrics that matter in bring-up are threshold current, slope efficiency, SMSR (typically many tens of dB on a clean part), RIN, and wavelength vs. temperature/current. Used as a CW source for SiPh or TFLN modulators, or as a DML when chirp is acceptable (<a href="#sec:dml-vcsel" data-reference-type="ref+Label" data-reference="sec:dml-vcsel">5.2</a>). Uncooled datacom DFBs ride case temperature with a known $`d\lambda/dT`$; cooled parts add a TEC and lock to a grid.

##### EML.

An electro-absorption modulated laser integrates a DFB with an *EAM* on one chip (<a href="#sec:eml-eam" data-reference-type="ref+Label" data-reference="sec:eml-eam">3.14.3.0.9</a>). Reverse bias on the EAM sets absorption and extinction; chirp stays far below a DML. That combination, not marketing, is why EMLs became the volume answer for 100G/lane and then 200G/lane DR/FR pluggables: one chip, low chirp, mature supply chain. Validation adds EAM bias sweeps, aging of the absorption curve, and driver-match checks on top of the DFB LIV/SMSR/RIN suite (<a href="#sec:laser-params,sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-params,sec:laser-aging">[sec:laser-params,sec:laser-aging]</a>).

##### When to pick which.

Through 200G/lane DR, EML usually wins on cost and integration. A CW DFB (or ELSFP/CW-WDM bank) plus Si MZM, ring, or TFLN wins when the modulator must sit on silicon or needs $`\gtrsim`$<!-- -->100 GHz EO bandwidth (<a href="#tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm" data-reference-type="ref+Label" data-reference="tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm">[tab:tx-modulator,sec:simzm,sec:siring,sec:tfln-mzm]</a>). At CPO scale the laser often leaves the optical engine entirely so it can be replaced without pulling the ASIC package (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>). Looking forward, 400G/lane pluggables are pushing harder toward external CW plus TFLN or high-BW silicon modulators, while EMLs remain the workhorse of the installed 100–200G base.

<span id="tab:laser-choice" data-label="tab:laser-choice"></span>

| Source | Typical use | Top risks |
|:---|:---|:---|
| DML | short reach, cost-driven | chirp/dispersion, extinction ratio |
| EML | $`\le`$DR, 100–200G/lane | EAM bias/aging, thermal |
| CW + TFLN MZM | 400G/lane FR/DR, NPO | MZM bias drift, fiber attach, driver match |
| CW + Si MZM | DR/FR SiPh, 100–400G/lane | driver match, bias drift, fiber coupling |
| CW + Si ring | CPO, WDM transceivers | wavelength lock, thermal crosstalk, coupling |
| VCSEL | SR over MMF | modal noise, reach, temperature |
| ELS / ELSFP | co-packaged optics | connectorization, fleet serviceability |

**Table .** When each source is used, and its top validation risks.

## Laser requirements: from roadmap to specs

Laser requirements only work when they are numbers a supplier can fail and a link budget can close. Start from the interconnect roadmap choice, then fill a short requirements slice; the ATP in <a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a> is how that slice is enforced on every lot.

##### Roadmap forks that set the laser.

Each architecture decision forces a different requirements set (<a href="#tab:laser-req-fork" data-reference-type="ref+Label" data-reference="tab:laser-req-fork">5.2</a>):

<span id="tab:laser-req-fork" data-label="tab:laser-req-fork"></span>

| Roadmap choice | Laser implication | Specs you must freeze early |
|:---|:---|:---|
| Pluggable EML vs CW+Si/TFLN | Integrated EAM vs external CW + modulator | EAM bias/aging and TDECQ vs CW power class, RIN, and modulator $`V_\pi`$ match |
| On-package laser vs ELSFP/CW-WDM | Field replace vs FIT inside the package | Connector/ORL/mate cycles and hot-swap CMIS vs COD/aging inside ASIC thermal |
| Isolator vs isolator-free (CPO) | Feedback tolerance vs quiet RIN only | Stressed $`\mathrm{RIN}_x\mathrm{OMA}`$ at stated ORL; monitor PD / lock policy |
| Single-$`\lambda`$ vs CW-WDM / comb | One line vs $`N`$ lines into rings/filters | Per-line power flatness, SMSR, grid, crosstalk (<a href="#sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser">5.10</a>) |
| Retimed vs LPO | Module DSP hides Tx vs host sees raw eye | Laser+modulator TDECQ/RLM floor vs host COM budget (<a href="#sec:com,sec:drivers" data-reference-type="ref+Label" data-reference="sec:com,sec:drivers">[sec:com,sec:drivers]</a>) |
| Derate policy | Operating $`I`$, $`T`$, power below abs-max | Bias window, thermal class, FIT/$`E_a`$ assumptions (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>) |

**Table .** Architecture forks and the laser specs each one forces. Freeze these before DVT samples are built (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>).

##### One-page requirements slice.

<a href="#tab:laser-prd" data-reference-type="ref+Label" data-reference="tab:laser-prd">5.3</a> is the PRD-sized list. Fill every row with a number (or an explicit “N/A for this architecture”) before you negotiate ATP limits. Do not leave RIN without an ORL, or power without a case-temperature class.

<span id="tab:laser-prd" data-label="tab:laser-prd"></span>

| Parameter | How to set the number | Measure / ATP | Reject if | Derate / ops note |
|:---|:---|:---|:---|:---|
| Launch power / class | Link budget + connector loss + aging margin (<a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>) | Power meter; ELSFP class | Below min at rated $`T`$ | Cap max power for COD |
| Wavelength / grid | PMD or ring FSR plan; $`d\lambda/dT`$ headroom (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>) | OSA / wavemeter | Off-grid at case $`T`$ | TEC setpoints |
| SMSR floor | Datasheet + modal-noise budget | OSA | Below floor at $`T`$ | Watch aging |
| RIN (quiet + stressed) | BER floor vs BW (<a href="#sec:rin" data-reference-type="ref+Label" data-reference="sec:rin">4.3</a>); ORL from plant | PD+ESA; stated ORL | Above limit at ORL | Bias-driver noise budget (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>) |
| Bias window | LIV kink-free range at max case $`T`$ | LIV | Kink in window | Run below abs-max $`I`$ |
| EAM / MZM (if any) | ER, RLM, TDECQ at baud (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>) | DCA + bias sweep | TDECQ/RLM fail | Bias aging policy |
| ORL / isolator | Architecture: isolator-free needs tighter RIN | ORL meter; mate cycles | ORL out of range | Cleaning / ELS mate life |
| CMIS monitors | What fleet triage will read (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>) | CMIS dump | Missing alarms / bad state machine | Enable sequence (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>) |
| FIT / life | Fleet failures/day target (<a href="#sec:fit-example" data-reference-type="ref+Label" data-reference="sec:fit-example">5.7.0.0.4</a>) | GR-468 + $`E_a`$ | Screen escape | Burn-in depth; ELS replace |

**Table .** Laser requirements one-pager. Every cell needs a program number; this table is the structure, not the limits.

##### How to fill numbers (method, not invention).

Work backward from the link, not forward from a marketing slide. The four steps below turn an architecture choice into ATP limits:

1.  Close the optical ledger at target pre-FEC BER (<a href="#sec:link-budget,sec:kp4" data-reference-type="ref+Label" data-reference="sec:link-budget,sec:kp4">[sec:link-budget,sec:kp4]</a>). That sets minimum launch OMA/power and maximum allowed penalties (transmitter and dispersion eye closure quaternary, TDECQ; ORL/RIN).

2.  From receiver BW and the RIN ceiling $`Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}`$ (<a href="#sec:rin" data-reference-type="ref+Label" data-reference="sec:rin">4.3</a>), set a stressed RIN limit with margin under the plant ORL you will actually see (not only a quiet bench).

3.  From case-temperature and derating policy, set the LIV bias window and thermal class so the laser never sits on a kink or at abs-max in the fleet (<a href="#sec:laser-aging,sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:laser-aging,sec:prod-corners">[sec:laser-aging,sec:prod-corners]</a>).

4.  From service model, choose ELSFP mate-cycle / hot-swap requirements or accept on-package FIT and write COD/aging screens accordingly (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

Hand the filled slice to the supplier with the ATP checklist (<a href="#tab:atp-laser" data-reference-type="ref+Label" data-reference="tab:atp-laser">8.3</a>). If a roadmap slide cannot point to a row in <a href="#tab:laser-prd" data-reference-type="ref+Label" data-reference="tab:laser-prd">5.3</a>, the requirement is not real yet.

**Key idea.** Laser leadership is a requirements sheet: architecture forks force specific specs (power, grid, RIN@ORL, SMSR, bias window, CMIS, FIT). Fill <a href="#tab:laser-prd" data-reference-type="ref+Label" data-reference="tab:laser-prd">5.3</a> from the link budget and fleet model, then enforce it with the ATP (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>).

## LIV, SMSR, and RIN: the measurement playbook

These three measurements decide whether a laser chip or module is usable. The instruments are standard; the skill is knowing which failure each one catches.

##### LIV (light–current–voltage).

The LIV curve plots optical power and forward voltage versus bias current. Read off threshold $`I_\mathrm{th}`$, slope efficiency (mW/mA above threshold), kink-free operating range, and thermal rollover at high current or high case temperature. <a href="#fig:liv-sketch" data-reference-type="ref+Label" data-reference="fig:liv-sketch">5.1</a> is a labeled schematic (not measured data).

High-temp LIV failures look like: $`I_\mathrm{th}`$ rise, slope collapse, early rollover, or a kink that moves into the bias window. Those map to aging, TEC saturation, or package thermal resistance (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>).

<figure id="fig:liv-sketch" data-latex-placement="ht">
<embed src="figures/fig_liv_sketch.pdf" style="width:85.0%" />
<figcaption>Schematic LIV curve with threshold, slope, kink, and thermal rollover labeled. Idealized for teaching; use measured LIV for pass/fail. <span id="fig:liv-sketch" data-label="fig:liv-sketch"></span></figcaption>
</figure>

##### SMSR (side-mode suppression ratio).

SMSR is the power difference (dB) between the lasing mode and the strongest side mode on an optical spectrum analyzer (OSA). Datacom single-mode parts require high SMSR so side modes do not steal power or seed modal noise. Spec-sheet floors are part-specific; treat the datasheet or ATP limit as authoritative. SMSR collapse under temperature or aging is a reject: the laser is leaving single-mode operation.

##### RIN (relative intensity noise).

Measure RIN with a calibrated photodetector and RF spectrum analyzer (or a dedicated RIN analyzer), under a controlled optical return loss. Distinguish *intrinsic* RIN (quiet bench, high ORL) from stressed $`\mathrm{RIN}_x\mathrm{OMA}`$ used in Ethernet/MSA specs. IEEE 802.3 / 100G Lambda class links cap $`\mathrm{RIN}_{17.1}\mathrm{OMA}`$ at $`-136`$ dB/Hz with 17.1 dB ORL . Quiet datacom DFB/EML parts typically sit well below that when feedback is controlled; CPO ELS designs care as much about feedback tolerance as about the quiet number (<a href="#sec:rin-values,sec:rin" data-reference-type="ref+Label" data-reference="sec:rin-values,sec:rin">[sec:rin-values,sec:rin]</a>).

<span id="tab:laser-meas" data-label="tab:laser-meas"></span>

| Parameter | Instrument | Pass/fail intent | Failure signature |
|:---|:---|:---|:---|
| LIV | SMU + power meter / integrating sphere | $`I_\mathrm{th}`$, slope, kink-free bias window | high-temp rollover; kink in bias range |
| SMSR | OSA | single-mode purity vs. datasheet/ATP | side modes rise with $`T`$ or age |
| RIN | PD + ESA / RIN analyzer | intrinsic and stressed $`\mathrm{RIN}_x\mathrm{OMA}`$ | RIN rises with ORL; BER floor (<a href="#sec:rin" data-reference-type="ref+Label" data-reference="sec:rin">4.3</a>) |
| Bias-driver noise | SMU vs. product bias board | $`\mathrm{RIN}_{\mathrm{eq}}`$ from $`i_n`$ (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>) | RIN rises with rails on, flat vs. ORL |
| Wavelength | OSA / wavemeter | grid placement, $`d\lambda/dT`$, $`d\lambda/dI`$ | walk off ring or MSA grid |
| EAM bias (EML) | bias sweep + DCA/TDECQ | extinction, chirp, RLM | aging shifts absorption curve |

**Table .** Laser measurement playbook: what to measure, with what, and what failure looks like.

## Laser drivers and the RIN budget

Modulator RF drivers (<a href="#sec:drivers" data-reference-type="ref+Label" data-reference="sec:drivers">3.14.3.0.10</a>) deliver swing and bandwidth into an EAM or MZM. Laser *bias* drivers are a different circuit: they set a quiet constant current into the diode. Current noise on that path becomes optical intensity noise and adds in the RIN budget of <a href="#sec:rin" data-reference-type="ref+Label" data-reference="sec:rin">4.3</a>. Confusing the two is a common debug miss: a great SiGe PAM4 driver can still ruin a CW laser if its supply or ground couples into the bias rail.

##### From current noise to equivalent RIN.

Above threshold, optical power tracks bias approximately as $`P\propto(I-I_\mathrm{th})`$. Relative intensity fluctuations then track relative current fluctuations:
``` math
\mathrm{RIN}_{\mathrm{eq,lin}}
\;\approx\;
\left(\frac{i_n}{I-I_\mathrm{th}}\right)^{\!2},
\qquad
\mathrm{RIN}_{\mathrm{eq}}[\mathrm{dB/Hz}]
\;=\;
20\log_{10}\!\left(\frac{i_n}{I-I_\mathrm{th}}\right),
```
where $`i_n`$ is the one-sided current-noise density in A$`/\sqrt{\mathrm{Hz}}`$ at the laser terminals (driver plus board pickup). The approximation assumes linear slope efficiency and ignores intrinsic laser dynamics; it is a budget tool, not a device model.

Worked numbers at $`I-I_\mathrm{th}=50`$ mA (typical CW DFB window): $`i_n=500`$ pA$`/\sqrt{\mathrm{Hz}}`$ maps to $`\mathrm{RIN}_{\mathrm{eq}}\approx-160`$ dB/Hz; $`270`$ pA$`/\sqrt{\mathrm{Hz}}`$ maps to about $`-165`$ dB/Hz. Commercial low-noise laser drivers quote roughly $`50`$–$`500`$ pA$`/\sqrt{\mathrm{Hz}}`$ at 1 kHz depending on current range (<a href="#tab:laser-driver-noise" data-reference-type="ref+Label" data-reference="tab:laser-driver-noise">5.5</a>); the Koheron DRV200 family is a concrete example . Against a good datacom intrinsic RIN of $`-145`$ to $`-155`$ dB/Hz (<a href="#sec:rin-values" data-reference-type="ref+Label" data-reference="sec:rin-values">4.3.1</a>), those 1 kHz densities look comfortable. The budget tightens when $`(I-I_\mathrm{th})`$ is small (near threshold, derated CW, or low-current VCSELs), when you integrate broadband switching noise rather than a 1 kHz spot, or when SerDes/DSP rails dump discrete tones onto the bias network.

<span id="tab:laser-driver-noise" data-label="tab:laser-driver-noise"></span>

| Driver class (example) | $`i_n`$ @ 1 kHz | $`\mathrm{RIN}_{\mathrm{eq}}`$ @ 50 mA | What it means |
|:---|:---|:---|:---|
| Ultra-low-noise CW (DRV200-A-40) | 55 pA$`/\sqrt{\mathrm{Hz}}`$ | $`\approx-179`$ dB/Hz | Bench / metrology floor |
| Low-noise CW (DRV200-A-200) | 270 pA$`/\sqrt{\mathrm{Hz}}`$ | $`\approx-165`$ dB/Hz | Typical quiet CW source |
| Higher-current CW (DRV200-A-400) | 480 pA$`/\sqrt{\mathrm{Hz}}`$ | $`\approx-160`$ dB/Hz | Still below $`-155`$ intrinsic |
| Shared digital LDO, poor PSRR | often $`\gg`$<!-- -->1 nA$`/\sqrt{\mathrm{Hz}}`$ + tones | can exceed $`-145`$ | False “RIN” on ESA |

**Table .** Bias-driver current noise converted to equivalent RIN at $`I-I_\mathrm{th}=50`$ mA using $`\mathrm{RIN}_{\mathrm{eq}}=20\log_{10}(i_n/(I-I_\mathrm{th}))`$. Densities for the DRV200 rows are from the Koheron datasheet at 1 kHz; the last row is qualitative (board-dependent).

##### CW / ELSFP / CW-WDM paths.

For external CW sources feeding Si or TFLN modulators, design the bias path as a low-noise current source with high supply rejection, local decoupling at the diode, and a star ground that does not share return with SerDes switching currents. Automatic power control () loops that close through a monitor PD suppress slow drift; keep the loop bandwidth well below the RIN measurement band and quiet enough that the loop itself does not inject intensity noise. ELSFP and CW-WDM modules hide this circuitry inside the pluggable (<a href="#sec:elsfp,sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:elsfp,sec:cwwdm-laser">[sec:elsfp,sec:cwwdm-laser]</a>); acceptance still needs module-level RIN with the host bias and management rails connected, not only a quiet SMU on the bare die.

##### DML and EML.

A *DML* shares one diode for bias and RF: a bias tee (or on-chip bias network) combines a quiet DC source with the RF driver. Excess RF driver broadband noise, poor tee isolation, or supply ripple on the bias arm all raise measured RIN and chirp-related penalties. An *EML* splits the problem: keep the DFB bias as quiet as a CW source, and treat the EAM RF driver under <a href="#sec:drivers" data-reference-type="ref+Label" data-reference="sec:drivers">3.14.3.0.10</a>. EAM drive amplitude sets extinction and chirp; DFB bias noise still lands in optical intensity before the modulator.

##### What to measure on the bench.

Bisect electrical vs. optical RIN:

1.  Measure intrinsic RIN with a quiet SMU or known low-noise driver and high ORL (<a href="#sec:laser-params" data-reference-type="ref+Label" data-reference="sec:laser-params">5.5</a>).

2.  Repeat with the product bias board / module rails connected. Any rise is driver or supply contribution, not laser physics.

3.  Sweep ORL. Rise with reflection is feedback-driven laser RIN (<a href="#sec:rin-values" data-reference-type="ref+Label" data-reference="sec:rin-values">4.3.1</a>); rise independent of ORL points at the electrical path.

4.  Look for discrete spurs on the ESA (switching frequencies, CMIS clocks). Spurs fail stressed $`\mathrm{RIN}_x\mathrm{OMA}`$ even when the broadband floor looks fine (<a href="#sec:rin-values" data-reference-type="ref+Label" data-reference="sec:rin-values">4.3.1</a>).

**Key idea.** Treat laser bias noise as a RIN term: $`\mathrm{RIN}_{\mathrm{eq}}\approx(i_n/(I-I_\mathrm{th}))^2`$. Quiet CW drivers at tens to hundreds of pA$`/\sqrt{\mathrm{Hz}}`$ usually sit under a $`-145`$ dB/Hz intrinsic floor at 50 mA; digital supply pickup, near-threshold bias, and DML bias-tee leakage are what actually burn the budget.

## Aging curves, derating, and fleet FIT

Lasers wear out. At fleet scale that is not a footnote; it sets architecture (ELSFP vs. integrated laser) and operating policy (derating, burn-in).

##### Observable aging signatures.

Watch LIV and spectrum over HTOL or field life:

- threshold rise and slope drop (active-region / facet degradation);

- SMSR collapse (mode competition);

- EAM bias creep on EMLs (absorption curve shift $`\to`$ TDECQ/RLM drift);

- RIN rise under feedback (ORL or isolator failure);

- COD (catastrophic optical damage) at the facet under overstress.

Each signature should appear in the ATP and in field telemetry triage (<a href="#sec:fleet-triage,sec:gr468" data-reference-type="ref+Label" data-reference="sec:fleet-triage,sec:gr468">[sec:fleet-triage,sec:gr468]</a>).

##### Arrhenius life projection.

Telcordia GR-468-CORE qualifies optoelectronic parts with accelerated stress (HTOL, temperature cycle, damp heat) and projects field life with Arrhenius acceleration :
``` math
\mathrm{AF}
= \exp\!\left[\frac{E_a}{k_B}\left(\frac{1}{T_\mathrm{use}}-\frac{1}{T_\mathrm{stress}}\right)\right],
```
where $`E_a`$ is the activation energy for the wear-out mechanism under test, $`k_B`$ is Boltzmann’s constant, and temperatures are absolute. Document $`E_a`$, sample size, and confidence bounds when converting a 1000-hour HTOL lot into field-year FIT. Activation energies are mechanism-specific; use the value justified in the qual plan, not a generic number copied from another product.

##### Derating.

Run below absolute-max current, case temperature, and optical power. Derating extends wear-out life and reduces COD risk. Uncooled datacom parts already sit near thermal limits at high case temperature; cooled or faceplate ELSFP modules (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>) buy headroom by moving heat off the ASIC package.

##### Worked FIT example (assumptions labeled).

FIT is failures per $`10^9`$ device-hours. For illustration only, assume 50 FIT per laser (confirm against your supplier qual; do not treat 50 as a measured claim) and a fabric with $`5\times10^5`$ lasers (order-of-magnitude for a large AI cluster with several optical links per accelerator). Expected failures per day:
``` math
\frac{5\times10^5 \times 50 \times 24}{10^9}
\approx 0.6\ \text{laser failures/day}.
```
That is why field-replaceable ELSFP modules, burn-in screens, and derating are design inputs, not afterthoughts (<a href="#ch:reliability" data-reference-type="ref+Label" data-reference="ch:reliability">8</a>).

## ELS and ELSFP: architecture, pinout, qual

*ELSFP* (External Laser Small Form-Factor Pluggable) is the OIF form factor for faceplate-pluggable CW laser modules that feed co-packaged optical engines . The lasers sit at the coolest part of the system (front panel), hot-swap when they fail, and keep thermal load off the ASIC and photonic engine.

##### Mechanical and optical.

The module uses a card-edge electrical interface and a blind-mate multi-fiber optical connector at the rear (MT-class ferrules), which improves eye safety for high CW power by keeping live fiber inside the chassis . One ELSFP can feed more than one optical engine. OIF defines optical power classes, thermal classes, and wavelength assignments (e.g. DR-type 1311 nm and FR-type CWDM4 grids) so hosts and modules interoperate.

##### Management and hot-swap.

ELSFP uses CMIS and the CMIS module state machine over TWI. On plug-in the module resets, initializes management, and stays in low-power mode with lasers *off* until the host transitions it to ModuleReady and explicitly enables lasers . `ModPrsL` and `IntL` support presence detect and asynchronous alarms for safe hot-swap.

##### Electrical pinout (OIF-ELSFP-02.0 Table 7).

Twenty-four contacts: multiple 3.3 V VCC and GND pins, module reset (`ResetL`), low-power mode (`LPModeL`), two-wire serial management (`SCL`/`SDA`), presence (`ModPrsL`), and interrupt (`IntL`), plus reserved pins for future power/ground . <a href="#tab:elsfp-pins" data-reference-type="ref+Label" data-reference="tab:elsfp-pins">5.6</a> summarizes the published map.

<span id="tab:elsfp-pins" data-label="tab:elsfp-pins"></span>

| Pin | Function | Requirements | Notes |
|:---|:---|:---|:---|
| 1–3 | VCC | 1.5 A, 3.3 V | with noise filtering |
| 4 | TBD | reserved | future power |
| 5 | ResetL | pull-up 10 k$`\Omega`$ | reset module, LVTTL |
| 6 | LPModeL | MMC on only | low-power mode (low), LVTTL |
| 7 | TBD | reserved | future ground |
| 8–10 | GND | 1.5 A, 3.3 V | with noise filtering |
| 11 | TBD | reserved | — |
| 12 | SCL | TWI clock | host 4.7 k$`\Omega`$ pull-up; module $`\ge`$<!-- -->10 k$`\Omega`$ |
| 13 | SDA | TWI data | same pull-ups as SCL |
| 14 | TBD | reserved | — |
| 15–17 | GND | 1.5 A, 3.3 V | with noise filtering |
| 18 | TBD | reserved | future ground |
| 19 | ModPrsL | shorted to GND in module | presence (low), LVTTL |
| 20 | IntL | pull-up 10 k$`\Omega`$ | interrupt, LVTTL |
| 21 | TBD | reserved | future power |
| 22–24 | VCC | 1.5 A, 3.3 V | with noise filtering |

**Table .** ELSFP electrical pinout (adapted from OIF-ELSFP-02.0 Table 7). Lasers power only in ModuleReady after host command; default on plug-in is lasers off .

##### Qual hooks for suppliers.

Acceptance test plans should cover the checklist in <a href="#tab:atp-laser,sec:supplier-exec" data-reference-type="ref+Label" data-reference="tab:atp-laser,sec:supplier-exec">[tab:atp-laser,sec:supplier-exec]</a>: laser LIV/SMSR/RIN inside the module; optical power-class compliance; connector mating cycles and contamination/ORL; burn-in before ship; CMIS register sanity; and thermal class at rated case temperature. Module bring-up must also prove the CMIS enable sequence and ModuleReady laser policy (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>). Field returns split between laser wear-out and connector/fiber-attach faults; keep both in the triage tree (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

## Optical safety and laser classes

### Hazard and laser classes

Laser safety for interconnects is governed by IEC 60825-1 (laser product classification) and IEC 60825-2 (optical-fiber communication systems, OFCS) . Classes run from Class 1 (safe under normal use) through Class 1M (safe unless the beam is collected by optics), Class 3R/3B, and Class 4. At 1310 nm and 1550 nm the beam is invisible, which raises the operational risk: technicians cannot see exposure. The retinal-hazard band ends near 1400 nm, but corneal and skin hazards remain, and single-mode power confined to a $`\sim`$<!-- -->9 μm core is high radiance even at modest milliwatt levels.

Short-reach datacom modules are usually engineered so each fiber port stays Class 1 or Class 1M under rated launch power. That is a design constraint on EML/DFB bias and on how much power each lane launches, not a label you add after the fact.

### Hazard level = aggregate, not per-lane

The safety case scales with *total* launched power at an accessible location, not with a single DFB data sheet. CW-WDM and ELS banks concentrate many lines on one MT or MPO ferrule (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>). A connector that breaks out eight or sixteen fibers can exceed a per-lane Class 1 budget even when each lane is modest. IEC 60825-2 assigns hazard levels (1 through 4) to each accessible port in the OFCS based on the radiant power that could escape during service . That is why ELS architecture and fiber count drive classification, not the laser chip alone.

### Open-fiber protection: APR and ALS

When fiber continuity is lost, open connectors and broken fiber can expose hazardous power. *APR* (automatic power reduction) holds output at or below Hazard Level 1M and probes for re-mate with safe low-power pulses. *ALS* (automatic laser shutdown) cuts power entirely and was common on older SDH links; for modern high-power systems APR with automatic restart is the preferred pattern because restart probes stay within the hazard limit . ITU-T G.664 requires power reduction to Hazard Level 1M within about 3 s of a continuity break, a restart inhibit window, and restart only at safe power.

These mechanisms tie directly to CMIS and bring-up policy: lasers enable only when the host commands ModuleReady (<a href="#sec:bringup,sec:cmis" data-reference-type="ref+Label" data-reference="sec:bringup,sec:cmis">[sec:bringup,sec:cmis]</a>). APR/ALS is what makes a live ELSFP hot-swap survivable in a running rack (<a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a>).

### What validation and ops owe

Optical safety is a validation deliverable, not a compliance sticker. ATP should verify APR/ALS trip threshold and timing on representative open-fiber faults; label modules and cages with the rated class; document max launched power per port and per MPO breakout; and write service procedures for multi-fiber connectors. At fleet scale, a hot-swap runbook that assumes ALS works but was never tested in ATP is a real hazard. Fold the APR/ALS check into the ELS hot-swap corner in <a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a> alongside mate-cycle and ORL tests.

## CW-WDM source validation

Multi-wavelength CW sources (CW-WDM MSA) feed dense ring or filter banks on a PIC (<a href="#sec:cwwdm,ch:wdm" data-reference-type="ref+Label" data-reference="sec:cwwdm,ch:wdm">[sec:cwwdm,ch:wdm]</a>). Validation is per-channel plus cross-channel:

- power flatness across $`\lambda`$ (uneven OMA after the modulator bank);

- per-channel SMSR and wavelength grid placement;

- channel crosstalk and residual ASE between lines;

- lock to microring resonances under temperature and neighbor heating (<a href="#sec:locking-techniques,sec:thermal-xtalk,sec:siring" data-reference-type="ref+Label" data-reference="sec:locking-techniques,sec:thermal-xtalk,sec:siring">[sec:locking-techniques,sec:thermal-xtalk,sec:siring]</a>);

- RIN and ORL sensitivity for each line (<a href="#sec:laser-params,sec:rin-values" data-reference-type="ref+Label" data-reference="sec:laser-params,sec:rin-values">[sec:laser-params,sec:rin-values]</a>).

Examples: Ayar Labs SuperNova (CW-WDM MSA-compliant, feeds TeraPHY)  ; Broadcom ELSFP banks on Tomahawk CPO (<a href="#sec:cpo-status,sec:elsfp" data-reference-type="ref+Label" data-reference="sec:cpo-status,sec:elsfp">[sec:cpo-status,sec:elsfp]</a>); quantum-dot comb lasers (Ranovus, Quintessent) aimed at many $`\lambda`$ from one chip. Source tests live here; locking and on-chip MUX live in <a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>.

## The light-source supplier landscape

Who actually builds these lasers matters, because the light source is often the hardest and highest-value part of an optical link. The suppliers split along a strategic fork: put the laser *outside* the package as a serviceable module, or integrate it *into* the photonic chip.

Merchant laser chips (DFB / EML / high-power CW)  
the III-V chips inside most modules and sources: Lumentum (notably supplying lasers for NVIDIA Spectrum-X photonics), Coherent (collaborating with NVIDIA on silicon photonics), and the Japanese EML/CW specialists Sumitomo Electric, Mitsubishi Electric, Furukawa, and Fujitsu; also MACOM and Source Photonics.

External light-source modules (CW-WDM / ELSFP)  
the SuperNova peers: Ayar Labs (SuperNova, <a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a>), Broadcom’s in-house ELSFP for its CPO switches, and POET Technologies’ interposer-based light source.

Quantum-dot comb lasers  
a single chip emitting many wavelengths at once: Ranovus (Odin) and Quintessent, both aimed squarely at CW-WDM.

Lasers integrated on silicon  
III-V gain bonded into the PIC: Intel (hybrid silicon lasers, and an 8-wavelength integrated source for its optical compute interconnect), OpenLight with Tower Semiconductor, and startups such as Scintil, Nexus Photonics, and Aeluma.

<span id="tab:laser-suppliers" data-label="tab:laser-suppliers"></span>

| Approach | Representative suppliers |
|:---|:---|
| Merchant DFB/EML/CW chips | Lumentum, Coherent, Sumitomo, Mitsubishi, MACOM |
| External CW-WDM / ELSFP modules | Ayar Labs, Broadcom, POET |
| Quantum-dot comb lasers | Ranovus, Quintessent |
| Lasers integrated on silicon | Intel, OpenLight/Tower, Scintil, Nexus, Aeluma |

**Table .** Light-source approaches and representative suppliers.

[^15]

## Why lasers are the reliability bottleneck

At the scale of a large optical fleet the laser is usually the reliability-limiting component. It is an active device with wear-out physics that passive optics and even photodiodes largely lack:

- *Catastrophic optical damage* (COD) at the facet.

- Gradual facet and active-region degradation (accelerated by temperature, following Arrhenius kinetics; <a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>).

- EAM aging in EMLs; coupling and solder drift in packaged assemblies.

Because failures scale with the number of lasers, a fleet of $`100{,}000`$+ links turns a modest per-laser FIT rate into a steady stream of field failures (<a href="#sec:fit-example,sec:gr468" data-reference-type="ref+Label" data-reference="sec:fit-example,sec:gr468">[sec:fit-example,sec:gr468]</a>). The mitigations shape architecture: field-replaceable external laser sources (ELSFP, CW-WDM), redundancy, burn-in screening to weed out infant mortality, and derating (running lasers below their maximum to extend life).

**Key idea.** Measure LIV, SMSR, and RIN on every laser path; write the requirements slice in <a href="#sec:laser-reqs" data-reference-type="ref+Label" data-reference="sec:laser-reqs">5.4</a> before DVT; budget bias-driver noise against the same RIN floor (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>); project aging with Arrhenius and derate in the field; prefer ELSFP/CW-WDM when fleet FIT and hot-swap matter. At gigawatt scale the laser is still the part most likely to bring a link down.

# WDM and wavelength-locked lasers

Early datacenter optics mostly ran one wavelength per fiber. That worked while port counts were modest. At AI scale, fiber count itself becomes a first-order cost and cable-plant problem, so the industry packed more channels onto each strand. The price of that packing is control: once channel spacing tightens, or once the modulator is a wavelength-selective ring, someone must keep laser and filter locked together. Few phrases carry as much architectural information as “wavelength-locked laser,” because locking only appears under those interconnect choices. Ring and MZM device physics stay in <a href="#sec:siring,sec:simzm" data-reference-type="ref+Label" data-reference="sec:siring,sec:simzm">[sec:siring,sec:simzm]</a>; per-$`\lambda`$ laser ATP and aging stay in <a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>. This chapter covers grids, lock loops, thermal crosstalk, MUX budget, and CW-WDM architecture.

## Why multiplex wavelengths at all

At $`100{,}000`$+ accelerator scale, every extra fiber is another connector, another patch, and another failure mode. *Wavelength-division multiplexing* (WDM) puts many independent channels on a single fiber, each on its own wavelength, so bandwidth per fiber rises without adding fiber. Each wavelength can still be an ordinary IM/DD channel. WDM and IM/DD are orthogonal; you simply run IM/DD *per wavelength*.

Historically the industry climbed a ladder of spacing. Coarse CWDM4 used $`\approx`$<!-- -->20 nm slots and uncooled lasers. LAN-WDM tightened that for 2 km-class FR4. Dense grids and then CW-WDM O-band combs for CPO pushed spacing into the 100–800 GHz class and made active locking mandatory. Those spacings are standardized grids, not vendor choices: the 20 nm CWDM slots follow the ITU-T G.694.2 wavelength grid (18 channels, 1271–1611 nm), and the 50/100/200 GHz datacom DWDM spacings follow the ITU-T G.694.1 frequency grid anchored at 193.1 THz . CWDM4 uses the four O-band lines of that CWDM grid; the CW-WDM combs in <a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a> define their own O-band grids for dense integration. <a href="#tab:wdm-grids" data-reference-type="ref+Label" data-reference="tab:wdm-grids">6.1</a> is that ladder as you will meet it in short-reach AI optics today.

<span id="tab:wdm-grids" data-label="tab:wdm-grids"></span>

| Grid family | Spacing (class) | Channels / fiber | Cooling / lock | Typical short-reach use |
|:---|:---|:---|:---|:---|
| CWDM4 | $`\approx`$<!-- -->20 nm | 4 | Uncooled; loose control | FR-class pluggables; faceplate WDM |
| LAN-WDM | $`\approx`$<!-- -->800 GHz ($`\approx`$<!-- -->4–5 nm @ 1310 nm) | 4 | Cooled or tight open-loop | 2 km-class FR4 (edge of book scope) |
| Datacom DWDM | 200/100/50 GHz | many | Locked to grid | Discrete DFB/EML DWDM modules |
| CW-WDM / CPO O-band | 100–800 GHz class (MSA spans) | 8 / 16 / 32 | Locked; often ring-tuned | CPO engines, optical I/O chiplets |

**Table .** WDM grids for short-reach AI interconnects. CW-WDM MSA normative grids sit in O-band with 9/18/36 nm spans and 8/16/32-line sets (<a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a>); spacing is set by the chosen span and channel count, not by Ethernet CWDM4.

## Why “locked” is the operative word

WDM alone does not force active locking. CWDM4 packs four wavelengths with enough spacing that uncooled lasers can wander and still stay in their slots. Locking becomes the operative word only when either the channel spacing is tight or the modulator itself is wavelength-selective. Those two situations drive nearly every modern CPO and dense optical-I/O control loop.

### Tight DWDM grids

To pack channels at 50–200 GHz class spacing, each laser must sit on its grid slot or adjacent channels collide. Emphasizing “locking” therefore hints at spacing tighter than CWDM. You do not stress locking for coarse, uncooled CWDM4; you do as soon as the grid looks like LAN-WDM, datacom DWDM, or a CW-WDM comb.

### Microring modulators and WDM locking

Resonant ring and microdisk modulators are the dense-WDM workhorse (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>). Their resonance drifts by roughly $`10`$ GHz/°C in silicon, so even a stable laser is not enough: the laser and the ring must be wavelength-locked. Either lock the laser to the ring, or thermally tune the ring onto the laser with a feedback loop. That laser–ring co-locking is the central control problem in ring-based WDM links and in co-packaged optics, and it is why neighbor heat and case-temperature ramps belong in validation, not only in the thermal section of a datasheet.

## WDM filters, grids, and on-chip multiplexing

WDM is not only lasers and locking (<a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a>): the PIC needs wavelength selective routing. The MUX/demux stage is a first-class link-budget line item (<a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>), not a packaging footnote.

##### Hardware choices.

AWG / echelle gratings  
multiplex and demultiplex on silicon or glass. Insertion loss is often 2–5 dB per MUX stage; adjacent-channel crosstalk and passband ripple land in OMA and transmitter and dispersion eye closure quaternary (TDECQ).

Ring filter banks  
drop/port routing in microring banks sets how many $`\lambda`$ share a bus waveguide. Thermal tuning per ring is common (<a href="#sec:siring,sec:thermal-xtalk" data-reference-type="ref+Label" data-reference="sec:siring,sec:thermal-xtalk">[sec:siring,sec:thermal-xtalk]</a>).

Hybrid  
some engines use a coarse AWG plus fine ring filters; count every stage in the ledger.

**MZMs trade area for calm wavelength behavior.** When each lane carries its own laser (DR/FR SiPh modules), silicon Mach–Zehnder modulators sidestep ring locking (<a href="#sec:simzm" data-reference-type="ref+Label" data-reference="sec:simzm">3.14.3.0.7</a>). Rings remain the default when many $`\lambda`$ share one PIC and area dominates (<a href="#sec:siring,ch:networking" data-reference-type="ref+Label" data-reference="sec:siring,ch:networking">[sec:siring,ch:networking]</a>).

##### Where MUX defects land.

<a href="#tab:mux-budget" data-reference-type="ref+Label" data-reference="tab:mux-budget">6.2</a> maps common MUX faults to the measurement that catches them.

<span id="tab:mux-budget" data-label="tab:mux-budget"></span>

| Fault | Optical symptom | Hits | Catch with |
|:---|:---|:---|:---|
| Stage insertion loss | Lower launch OMA on all $`\lambda`$ | Link budget OMA | Power meter / OMA |
| Passband ripple / tilt | Uneven OMA across bank | Weakest $`\lambda`$ | Per-$`\lambda`$ OMA map |
| Adjacent-channel crosstalk | Closed eyes, RLM/TDECQ up | Tx quality / BER | Isolation sweep + DCA |
| MUX imbalance | One $`\lambda`$ weak, neighbors OK | Single-lane BER | Per-lane power + BER |
| Grid misalignment | Filter edge clipping | TDECQ, unlock risk | OSA + lock status |

**Table .** MUX/demux defects and where they appear in validation. Isolation and imbalance tests belong in ATP for any dense WDM engine (<a href="#sec:lock-validation,sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:lock-validation,sec:cwwdm-laser">[sec:lock-validation,sec:cwwdm-laser]</a>).

Validation adds channel isolation sweeps, grid alignment across temperature, and MUX imbalance (uneven OMA per $`\lambda`$). Treat the weakest channel as the budget-limiting lane, not the average.

## Lock-loop mechanics

Wavelength locking closes the loop between source and filter. Pick a technique based on whether the laser, the ring, or both must be steered (<a href="#sec:siring,ch:validation" data-reference-type="ref+Label" data-reference="sec:siring,ch:validation">[sec:siring,ch:validation]</a>).

##### Error-signal sources.

Etalon-based wavelength locker  
A fixed reference etalon plus a pair of photodiodes produces an error signal proportional to wavelength offset; feedback trims laser temperature or current onto the grid. Common on discrete DFB/EML modules.

Laser-to-ring thermal feedback  
Monitor the ring’s through/drop power (or a dither tone) and heat the ring, or trim laser current, to park the carrier on resonance. Default for dense microring WDM banks in CPO and optical I/O.

Injection / external-cavity locking  
Stabilize a laser’s wavelength and linewidth against an external reference cavity; higher performance, more parts. Rare in short-reach volume products.

Athermal design  
Engineer the device so its resonance barely moves with temperature, reducing the control burden. Athermal does not remove MUX grid alignment; it shrinks the loop authority you need.

Digital supervisory loop  
CMIS-exposed monitors and firmware on modern modules; link training at 224G/448G may iterate EQ and wavelength trim together (<a href="#sec:pluggables" data-reference-type="ref+Label" data-reference="sec:pluggables">9.3</a>).

##### What you trim.

Three actuators show up repeatedly, and the bring-up order usually starts with the slowest, highest-authority knob. Laser TEC / temperature moves the whole comb or a single DFB on the frequency axis. Laser bias current is the fine wavelength trim (and also changes power), so watch RIN and SMSR when you use it as a locker (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>). Ring heaters park each microring onto its assigned $`\lambda`$ and are the per-channel control in dense banks (<a href="#sec:thermal-xtalk" data-reference-type="ref+Label" data-reference="sec:thermal-xtalk">6.5</a>).

##### Capture versus hold.

*Capture* is acquiring lock from a cold or unlocked state: coarse scan of heater or TEC until the monitor error signal crosses zero, then close the loop. *Hold* is rejecting thermal drift and neighbor crosstalk once locked. Loop bandwidth must be fast enough to track case-temperature ramps and adjacent-heater steps, but slow enough not to fight the data path or inject RIN through bias modulation. Silicon rings at $`\sim`$<!-- -->10 GHz/°C set the disturbance scale: a 1 °C neighbor step is tens of GHz of resonance walk, which is a large fraction of a 100–200 GHz grid slot (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>).

##### Failure signatures.

Fleet failures often look like slow wavelength walk: drop monitor power falls, TDECQ rises on one $`\lambda`$, or one lane in a WDM bank drops out while neighbors stay up. Bisect laser versus ring by toggling TEC setpoint and ring heater independently (<a href="#sec:instruments,sec:fleet-triage,sec:lock-validation" data-reference-type="ref+Label" data-reference="sec:instruments,sec:fleet-triage,sec:lock-validation">[sec:instruments,sec:fleet-triage,sec:lock-validation]</a>).

## Thermal crosstalk and heater budget

Dense ring banks share a substrate. Heating one ring to stay on resonance shifts neighbors. That is , and it is why a single-lane lock test at room temperature is not a product test.

##### Where heat comes from.

Self-heating from the ring’s own heater (and absorbed optical power) shifts its resonance, so the lock loop must settle with the lane at operating optical power, not dark. Adjacent heaters on nearest-neighbor and next-nearest rings in a WDM bank are the next disturbance; the worst case is all neighbors at max heater power while you hold lock. Package and ASIC load add a common-mode walk: switch or XPU case-temperature ramps and local hotspots move the whole bank, and a shared TEC or cold plate sets how much of that walk the lock loop must reject (<a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a>).

##### Design and validation implications.

Budget heater range with headroom for crosstalk, not just for the coldest and hottest case alone. Layout (heater placement, thermal isolation trenches, ring pitch) is a reliability and yield problem as much as a control problem. In validation, simultaneous full-traffic on neighbors plus max case $`T`$ is a *lock* test: unlock, BER walk, or TDECQ rise on one $`\lambda`$ under neighbor load points at thermal design, not at a bad laser die (<a href="#sec:prod-corners,sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:prod-corners,sec:fleet-triage">[sec:prod-corners,sec:fleet-triage]</a>).

## External multi-wavelength sources (CW-WDM)

Dense WDM with ring modulators needs a source of many clean, stable wavelengths. The industry answer is a *disaggregated* external laser: a single multi-wavelength continuous-wave (CW) module supplies a comb of wavelengths over fiber to the photonic engine, where microrings imprint data onto each one. The *CW-WDM MSA* standardizes those sources for AI, HPC, and high-density optics . Source-side measurement detail (per-channel power, SMSR, RIN, lock under neighbor heat) is in <a href="#sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser">5.10</a>; this section is the architecture contract.

##### What the MSA specifies (and what it does not).

Rev 1.0 (June 2021) defines O-band wavelength grids, port configurations, and measurement methods. It does *not* standardize mechanical form factors, management pins, or full link parameters; those stay application-specific or move to form-factor MSAs such as ELSFP .

Core normative content:

- **Grid sets:** 8+1 and 16+1 lines in a 9 nm span; 8+1 / 16+1 / 32+1 in 18 nm and 36 nm spans (shortest line optional in each set).

- **Spacings (class):** for the 18 nm span, channel spacing is 400 / 200 / 100 GHz for 8 / 16 / 32-line sets; the 9 nm and 36 nm spans scale spacing with span width (100–800 GHz class). Normative MSA grids are denser than 5 nm; coarser CWDM-like spacings are informative only.

- **Two physical configs:** *modular* (each fiber carries one $`\lambda`$) and *integrated* (each fiber carries the full comb).

- **Power classes and AS parameters:** output power classes span low to high launch; SMSR, RIN, and linewidth floors are defined with measurement methods, with many limits marked application-specific (AS) in the normative tables.

Informative appendix examples (not universal product guarantees) often quote $`\approx`$<!-- -->30 dB SMSR, $`\approx-135`$ dB/Hz RIN, $`\approx`$<!-- -->20 MHz linewidth, $`\pm`$<!-- -->1 dB per-line power variation, and $`-20`$ dB ORL tolerance for 18 nm-span examples. Treat those as negotiation anchors; write the ATP to your link budget (<a href="#sec:cwwdm-laser,tab:laser-prd" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser,tab:laser-prd">[sec:cwwdm-laser,tab:laser-prd]</a>).

##### Why disaggregate the laser.

External CW-WDM / ELSFP sources are field-replaceable. Lasers dominate wear-out FIT (<a href="#ch:lasers,ch:reliability" data-reference-type="ref+Label" data-reference="ch:lasers,ch:reliability">[ch:lasers,ch:reliability]</a>); keeping them off the ASIC package turns a COD or facet failure into a hot-swap, not a board pull. The photonic engine still needs per-$`\lambda`$ lock to rings or filters.

##### Exemplar: SuperNova + TeraPHY.

Ayar Labs’ optical-I/O stack is aimed at *scale-up* (XPU-to-XPU) rather than switch fabric :

TeraPHY  
an optical-I/O chiplet co-packaged with the host XPU, carrying the microring modulators and receivers.

SuperNova  
the external CW light source, positioned as the first CW-WDM-MSA-compliant 16-wavelength source, delivering up to 16 wavelengths into each of 16 fibers. That is light for 256 data channels (vendor claim: about 16 Tb/s bidirectional), and roughly $`64\times`$ the wavelength count of CWDM4 pluggables.

Vendor performance claims versus pluggables plus electrical SerDes (5–10$`\times`$ bandwidth, 10$`\times`$ lower latency, 4–8$`\times`$ better power efficiency) are marketing numbers; use them as orientation, not as ATP limits.[^16]

##### System requirements the source must meet.

For the PIC to close every lane, the comb must deliver, across temperature and with all ports active, a small set of properties at once: per-line power flatness (else MUX + modulator bank makes uneven OMA), grid placement and SMSR per line, RIN under the specified ORL, and absolute wavelength stable enough that ring heaters stay in range (<a href="#sec:thermal-xtalk,sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:thermal-xtalk,sec:cwwdm-laser">[sec:thermal-xtalk,sec:cwwdm-laser]</a>). Miss any one and a single $`\lambda`$ will look like a modulator or lock-loop failure when the source is the real cause.

### Comb sources: one device, many lines

The SuperNova approach builds its comb from an array of discrete lasers, one distributed-feedback (DFB) die per wavelength, combined onto the output fiber. That is the shipping answer, and it scales cleanly to the 8 and 16 lines the MSA grids call for. Past a few dozen lines the die count, the combining loss, and the per-die wavelength trimming start to hurt, which is why a single device that emits a whole comb is attractive. Three device classes compete.

**Quantum-dot mode-locked lasers** (*QD-MLL*s) are the front-runner for a monolithic O-band comb. Mode locking in a single cavity produces evenly spaced lines at the cavity round-trip rate; quantum-dot gain adds low RIN, a near-zero linewidth-enhancement factor, and strong optical-feedback tolerance, the same properties that make quantum-dot lasers attractive for isolator-free co-packaging . Reported O-band demos carry 14$`\times`$<!-- -->100 Gb/s PAM4 over 10 km at $`\sim`$<!-- -->284 fJ/bit, and isolator-free variants target interconnect capacity beyond 3.2 Tb/s. These are research results, not qualified products, so treat the line counts and efficiencies as provisional.

**Kerr microcombs** take the opposite route: pump one high-$`Q`$ microresonator and let four-wave mixing fill in many evenly spaced lines on a chip . The line count and the spacing uniformity are excellent, and a 2025 demonstration added a monolithic demultiplexer that autonomously locks to and tracks the comb lines. The catch is power. Pump-to-comb conversion efficiency is modest, so each line leaves the chip weak and usually needs a booster or per-line amplifier before it reaches the modulator bank (<a href="#sec:soa-distribution" data-reference-type="ref+Label" data-reference="sec:soa-distribution">6.6.2</a>). Microcombs also need a clean pump laser and careful thermal control to hold the soliton state.

**Gain-switched and quantum-dash combs** sit between the two: a directly driven laser produces a flatter, lower-line-count comb with simple electronics. They have reached multi-terabit aggregate rates in the lab but see less datacom traction than QD-MLLs.

For any of them the contract from the MSA does not change: the source must hold per-line power flatness, SMSR, RIN, and grid placement across temperature with every port active (<a href="#sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser">5.10</a>). A comb that delivers 32 lines but drops 6 dB across the band, or whose edge lines miss the grid, buys nothing over an array of DFBs the PIC already knows how to drive.

### Gain and power distribution across the bank

Whatever generates the comb, the light still has to survive the trip to the modulators. One source feeds a multiplexer, a splitter tree, and per-line routing before it reaches a ring, and each stage takes its cut. When the source is a chip-scale comb with weak lines (<a href="#sec:comb-sources" data-reference-type="ref+Label" data-reference="sec:comb-sources">6.6.1</a>), or when the fan-out is large, a *semiconductor optical amplifier* (SOA) restores the budget.

**Where the gain sits.** A booster SOA placed right after the comb lifts every line before the split, so one device pays for the whole fan-out. A per-line SOA after the demultiplexer instead corrects line-to-line imbalance, at the cost of one amplifier per wavelength. The receiver-side SOA preamplifier (<a href="#tab:rxtech" data-reference-type="ref+Label" data-reference="tab:rxtech">4.4</a>) is a separate job: there the goal is sensitivity, here it is launch power.

**The noise-figure cost.** An SOA adds amplified spontaneous emission (*ASE*), and its noise figure sets how much. The quantum floor is 3 dB; commercial O-band SOAs land near 6–7 dB with roughly 15 dB of gain and about 1.5 dB polarization-dependent gain . Every dB of noise figure eats into the signal-to-noise ratio the receiver eventually sees, so an SOA that rescues launch power can cost link margin if it runs deep into saturation or amplifies an already-noisy comb. Quantum-dot SOAs grown on silicon are attractive for the same reason QD lasers are: low noise, wide O-band gain, and CMOS-compatible integration.

**Holding the bank flat.** Gain is not uniform across the comb span, and SOAs compress near saturation, so the line that starts strongest is not the line that ends strongest. Per-line power flatness is a system spec (<a href="#sec:cwwdm" data-reference-type="ref+Label" data-reference="sec:cwwdm">6.6</a>), held with some mix of source-side pre-emphasis, gain-tilt control, and per-line trimming. The alternative to any distribution-side gain is a higher-power source, which is why array-of-DFB designs that already meet the launch budget often skip the SOA entirely.

### Polarization on the CW distribution path

IM/DD is forgiving about polarization where it counts most. The photodiode is a square-law detector, so the received state of polarization does not affect the recovered bits (<a href="#sec:coherent-boundary" data-reference-type="ref+Label" data-reference="sec:coherent-boundary">3.4</a>). A standard single-mode drop to the receiver therefore needs no polarization control. The external-source and CW-WDM architectures move the sensitive part upstream, onto the path between the laser and the modulator.

**Where it matters.** Three elements on the CW feed care about the launched state. A *TFLN* Mach–Zehnder drives the electro-optic effect through TE-polarized light on one crystal axis (<a href="#sec:tfln-mzm" data-reference-type="ref+Label" data-reference="sec:tfln-mzm">3.14.3.0.8</a>); light on the wrong axis sees little modulation. Silicon grating couplers are polarization-selective by construction, so coupling loss swings with the input state, a *polarization-dependent loss* (PDL) that comes straight off the launch budget. And a booster or per-line SOA adds polarization-dependent gain (<a href="#sec:soa-distribution" data-reference-type="ref+Label" data-reference="sec:soa-distribution">6.6.2</a>), so a drifting state becomes a drifting per-line power. None of these sit after the photodiode, so none show up in a receiver-side budget: they act on light that has not yet been modulated.

**How it is held.** Keep the CW feed on *polarization-maintaining* (PM) fiber and PM connectors from the external laser (<a href="#ch:lasers" data-reference-type="ref+Label" data-reference="ch:lasers">5</a>) to the modulator input, launched on the coupler’s preferred axis. On-chip the light is already single-polarization once it is in a TE waveguide, so the discipline is really about the fiber run and the mate at the package. A co-packaged design with the laser on the same substrate shortens that run to millimeters and sidesteps most of the problem; an external-laser design pays for a PM path and its alignment tolerance instead.

## Lock validation playbook

Instruments and BER methods live in <a href="#ch:validation" data-reference-type="ref+Label" data-reference="ch:validation">7</a>. What is special to WDM is the order: you cannot trust a BER number on a ring bank until the comb is identified, the resonances are parked, and the lock loops hold under neighbor heat. The sequence below is the usual bring-up; skip a step and you will debug the wrong domain.

##### Bring-up order.

1.  **Grid ID:** confirm each CW line (or DFB) is on the assigned channel with an OSA / wavemeter (<a href="#sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:cwwdm-laser">5.10</a>).

2.  **Coarse align:** park rings near resonance with open-loop heater sweeps; check through/drop monitors.

3.  **Close lock:** enable the feedback loop; verify capture on every $`\lambda`$ at operating optical power.

4.  **Stress neighbors / temperature:** max case $`T`$, neighbor heaters and traffic on (<a href="#sec:thermal-xtalk,sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:thermal-xtalk,sec:prod-corners">[sec:thermal-xtalk,sec:prod-corners]</a>). Confirm hold, not just capture.

5.  **Close the link:** BER / TDECQ / sensitivity on the weakest lane first (<a href="#sec:tdecq,sec:link-budget" data-reference-type="ref+Label" data-reference="sec:tdecq,sec:link-budget">[sec:tdecq,sec:link-budget]</a>).

##### Bisect laser versus ring.

If one $`\lambda`$ unlocks or walks, change one actuator at a time:

- change laser TEC / current with ring heater fixed: if the error follows the laser, the source or its locker is wrong;

- change ring heater with laser fixed: if the error follows the heater, the ring, monitor PD, or thermal crosstalk is wrong;

- if both look fine but OMA is low, inspect MUX imbalance and connector/ORL (<a href="#tab:mux-budget,sec:optical-channel" data-reference-type="ref+Label" data-reference="tab:mux-budget,sec:optical-channel">[tab:mux-budget,sec:optical-channel]</a>).

##### Fleet telltales.

Slow BER creep with rising bias on one line is often laser wear-out (<a href="#sec:wearout-modes" data-reference-type="ref+Label" data-reference="sec:wearout-modes">8.4</a>). Sudden unlock under neighbor load with healthy LIV is thermal crosstalk or lock firmware. One dark lane with neighbors up is COD, FAU, or a single ring/heater fail; classify with <a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a> before you open an 8D on the wrong supplier.

## What wavelength locking implies about an architecture

Because locking is only worth its complexity under specific conditions, its presence narrows the design space considerably.

<span id="tab:wdm-read" data-label="tab:wdm-read"></span>

| Implication | Strength |
|:---|:---|
| Some form of WDM is in use | Near-certain: locking only matters with WDM. |
| Dense (D)WDM rather than coarse CWDM | Likely: locking implies tight spacing. |
| Microring-based silicon photonics with external multi-wavelength (CW-WDM) sources, often trending toward co-packaged optics | Common in modern AI interconnects (e.g. Broadcom and NVIDIA Quantum-X programs), driven by fiber-count pressure at scale. |
| Discrete DFB/EML DWDM (no rings) | Also possible; locking alone does not prove rings. |

**Table .** What a wavelength-locking requirement implies.

The solid conclusion is that **WDM is present and wavelength control is central**; whether the implementation is ring-based silicon photonics with external multi-wavelength sources or discrete DFB/EML DWDM depends on the specific system.

**Key idea.** Wavelength locking almost always implies WDM, and most often dense WDM with wavelength-selective (ring) modulators fed by external multi-wavelength sources. The hard problems are lock-loop capture and hold under thermal crosstalk, MUX loss and isolation in the link budget, and CW-WDM source flatness and grid stability at fleet scale.

# Optical validation

A datasheet that closes on a quiet bench is not a product. *Validation* is the work of proving a link meets spec and will keep meeting it across the temperatures, hosts, connectors, and aging the fleet will actually see. That discipline is the second theme of this book. This chapter walks the ladder from a single device to a deployed fleet, the metrics measured at each stage, module and system bring-up under production-like corners, and the data-driven debug mindset the work demands.

## The validation ladder

Optical programs fail in the same places again and again: a part that looks good in characterization but cannot bring up on a production host, or a module that passes ATP and then unlocks under neighbor heat. The practical way to avoid those gaps is a ladder of increasing scale. Each rung answers a sharper question.

<span id="tab:ladder" data-label="tab:ladder"></span>

| Stage | Question | Typical activity |
|:---|:---|:---|
| Component | In spec? | laser LIV, wavelength/RIN/SMSR; PD responsivity and bandwidth; modulator response |
| Module bring-up | Does it link? | power-on, CMIS, CDR/BER (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>) |
| Characterization | How much margin, across corners? | sweep temperature, voltage, aging; TDECQ, sensitivity, link budget |
| Interop / system | Works with the switch/NIC/ASIC? | chassis thermal, host SerDes, prod-rep corners (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>) |
| Production readiness | Can the supplier build it at yield? | ATP, SPC, DVT/PVT gates (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>) |
| Scaled deployment | Does the fleet stay up? | field telemetry, RMA, FIT tracking; triage tree (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>) |

**Table .** From bench to fleet.

## The core IM/DD measurements

Once the ladder is clear, the measurement list is organized around isolation: transmitter, channel, and receiver. That split is older than PAM4. Long before TDECQ, field engineers learned that a dark link can be a dead laser, a dirty connector, or a dead TIA, and that guessing which one burns hours. Bisecting those three domains is still how you keep debug from turning into simultaneous retunes of everything.

### Transmitter

Start with the light leaving the faceplate or the CPO fiber array. For PAM4, the headline metric is *TDECQ* (transmitter and dispersion eye closure quaternary): a reference equalizer is applied to the captured eye and the residual penalty is reported in dB (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>). Alongside it you read *OMA* (outer), extinction ratio, and *RLM* (level linearity), plus wavelength, spectral width, and RIN with a bias-driver versus feedback bisect (<a href="#sec:laser-params,sec:laser-drivers,sec:rin-values" data-reference-type="ref+Label" data-reference="sec:laser-params,sec:laser-drivers,sec:rin-values">[sec:laser-params,sec:laser-drivers,sec:rin-values]</a>).

What else you add depends on the transmitter style. Laser-bearing modules need LIV, threshold, slope, SMSR, and chirp checks for DMLs (<a href="#sec:laser-params,sec:dfb-eml" data-reference-type="ref+Label" data-reference="sec:laser-params,sec:dfb-eml">[sec:laser-params,sec:dfb-eml]</a>). External MZMs (TFLN or silicon) need EO $`S_{21}`$, $`V_\pi`$, quadrature bias versus temperature, and driver-path eye symmetry at baud (<a href="#sec:simzm,sec:tfln-mzm,sec:tdecq" data-reference-type="ref+Label" data-reference="sec:simzm,sec:tfln-mzm,sec:tdecq">[sec:simzm,sec:tfln-mzm,sec:tdecq]</a>). Microring banks need resonance alignment, thermal tuning, neighbor crosstalk, and peaking-network EO $`S_{21}`$ (<a href="#sec:siring,ch:wdm" data-reference-type="ref+Label" data-reference="sec:siring,ch:wdm">[sec:siring,ch:wdm]</a>). The point of the list is not completeness for its own sake: it is knowing which instrument answers which hypothesis when the eye closes.

### Channel

If the transmitter looks clean into a golden receiver and the link still fails, the channel is next. Insertion loss from fiber, connectors, MUX/de-MUX (<a href="#sec:wdm-hardware" data-reference-type="ref+Label" data-reference="sec:wdm-hardware">6.3</a>), and on-chip coupling (<a href="#sec:simzm,sec:siring" data-reference-type="ref+Label" data-reference="sec:simzm,sec:siring">[sec:simzm,sec:siring]</a>) is the first ledger line; plan about 1–3 dB per fiber interface. Chromatic dispersion (<a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>) matters more on FR-class SMF sweeps than on short DR links. Optical return loss (ORL) is the quiet killer: reflections back into the laser raise RIN and seed burst errors, which is why many DR/FR modules still carry isolators while some CPO engines rely on design margin and monitor photodiodes instead (<a href="#sec:rin-values,ch:lasers" data-reference-type="ref+Label" data-reference="sec:rin-values,ch:lasers">[sec:rin-values,ch:lasers]</a>). Fiber attach (MPO/MTP, FAU, grating couplers) shows up as both yield and reliability (<a href="#sec:photonic-packaging" data-reference-type="ref+Label" data-reference="sec:photonic-packaging">8.5</a>).

### Receiver

Receiver work asks whether the front-end can still decide bits at the OMA that survives the channel. Measure sensitivity (minimum OMA for the target BER) and stressed-receiver sensitivity with a calibrated stressor for margin (<a href="#sec:secq" data-reference-type="ref+Label" data-reference="sec:secq">7.4</a>), plus overload before the TIA saturates. Underneath those system numbers sit the photodiode/TIA pair: responsivity, bandwidth, and input-referred noise (<a href="#sec:pd-tia,ch:models" data-reference-type="ref+Label" data-reference="sec:pd-tia,ch:models">[sec:pd-tia,ch:models]</a>).

### Link level

Only after Tx, channel, and Rx each look sane do you trust a full-link verdict: pre-FEC BER against the KP4 threshold (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>), post-FEC BER, FEC symbol-error histograms, and a signed link-budget ledger from transmitter OMA to receiver sensitivity with penalties and remaining margin. That ledger is the document you argue from in DVT; the BER alone is not.

## Transmitter and dispersion eye closure quaternary (TDECQ)

*TDECQ* (transmitter and dispersion eye closure quaternary) deserves a closer look because it is the metric that governs PAM4 transmitter acceptance. It answers a specific question: *how much worse is this transmitter than an ideal one, after a realistic receiver has done what it can to clean up the signal?*

### How it is measured

1.  **Capture.** The optical waveform is acquired on a sampling oscilloscope (a DCA) through a standardized reference receiver (a fourth-order Bessel–Thomson filter at roughly half the baud rate) so every lab measures the same bandwidth.

2.  **Equalize.** A defined *reference equalizer*, a *feed-forward equalizer* (FFE) with a small, bounded number of taps (commonly up to five), is applied. This models the modest equalization a real receiver would perform, so the transmitter is not penalized for *ISI* the system can remove anyway.

3.  **Histogram.** Two narrow vertical histogram windows are placed inside the symbol (near 0.45 and 0.55 of the unit interval). The noise distribution is evaluated at the three PAM4 decision thresholds.

4.  **Compute.** The algorithm finds the RMS Gaussian noise $`\sigma`$ that, added to the equalized signal, would just reach a target symbol error ratio of $`4.8\times10^{-4}`$ (the SER consistent with the KP4 pre-FEC budget). TDECQ is the ratio, in dB, of the noise an *ideal* transmitter could tolerate to the noise *this* transmitter can tolerate:
    ``` math
    \mathrm{TDECQ} = 10\log_{10}\!\left(\frac{\sigma_{\text{ideal}}}
            {\sigma_{\text{measured}}}\right).
    ```

A worse transmitter tolerates less added noise before failing, so $`\sigma_{\text{measured}}`$ shrinks and TDECQ rises. Lower is better; typical 100–200G/lane specifications cap it in the low single-digit dB range.

### Related quantities and failure signatures

SECQ  
the stressed-eye counterpart used on the receiver side, adding a calibrated stressor to test margin rather than transmitter quality alone. See <a href="#sec:secq" data-reference-type="ref+Label" data-reference="sec:secq">7.4</a>.

RLM (relative level mismatch)  
measures how evenly the four PAM4 levels are spaced; poor RLM (uneven levels) inflates TDECQ.

Because TDECQ folds several impairments into one number, the way it fails is diagnostic: uneven levels point to modulator or driver linearity (RLM); residual eye closure the equalizer cannot fix points to excess ISI or limited bandwidth; a noise-limited result points to low OMA, RIN, or reflections. For external MZMs (TFLN or silicon), also check EO $`S_{21}`$ bandwidth, $`V_\pi`$ and bias quadrature drift with temperature, and RF return loss on the driver-to-modulator path (<a href="#sec:simzm,sec:tfln-mzm,sec:siring" data-reference-type="ref+Label" data-reference="sec:simzm,sec:tfln-mzm,sec:siring">[sec:simzm,sec:tfln-mzm,sec:siring]</a>). This is why *LPO*, which removes the module’s own DSP, raises the stakes on transmitter quality: there is less downstream equalization to hide behind, so TDECQ-class metrics become even more central.

## SECQ and stressed-receiver testing

*SECQ* (stressed eye closure quaternary) mirrors TDECQ on the *receiver*: instead of scoring transmitter quality with a reference equalizer, the test applies a calibrated optical stressor (attenuation, ISI template, optional RIN) and asks how much margin remains before the receiver hits the target pre-FEC BER.

Stressed-receiver sensitivity and overload tests (<a href="#sec:sensitivity" data-reference-type="ref+Label" data-reference="sec:sensitivity">4.4</a>) use the same philosophy: bracket the operating OMA range with impairments the link will see in the field. For LPO, where the module DSP is gone, SECQ-style margin on the host-side receiver (<a href="#sec:equalization,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:equalization,sec:conditioning">[sec:equalization,sec:conditioning]</a>) is as important as TDECQ on the transmitter.

## Instruments

A failing PAM4 link rarely announces which block is wrong. The bench is how you force the answer: each instrument isolates one failure mode, and the loopback topology tells you which side of the optical connector owns it.

DCA  
(digital communication analyzer): sampling scope for PAM4 eyes, TDECQ, OMA, RLM (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>). Needs a reference receiver filter matched to the PHY under test.

BERT  
bit-error ratio at pre- and post-FEC; FEC symbol histograms (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>).

OSA  
wavelength, SMSR, side modes, RIN estimates (<a href="#ch:lasers,sec:rin-values" data-reference-type="ref+Label" data-reference="ch:lasers,sec:rin-values">[ch:lasers,sec:rin-values]</a>).

VOA / stressor assembly  
calibrated attenuation and optional ISI for SECQ and sensitivity sweeps.

Power meter  
average power; pair with DCA for OMA.

Thermal chamber + TEC controller  
corner validation; essential for rings (<a href="#sec:siring,ch:wdm" data-reference-type="ref+Label" data-reference="sec:siring,ch:wdm">[sec:siring,ch:wdm]</a>) and laser grids.

Use electrical loopback (host SerDes), optical loopback (Tx$`\to`$Rx on module), and golden-host/golden-module interop to bisect faults (<a href="#sec:optical-channel" data-reference-type="ref+Label" data-reference="sec:optical-channel">7.2.2</a>). If the fault follows the module under golden-host swap, stop blaming the SerDes; if it stays with the host, stop opening laser FA.

## Building a link budget

A link budget is a signed dB (or power) ledger from transmitter to receiver. For IM/DD short reach, start from outer OMA at the Tx faceplate and subtract every loss and penalty until you compare against receiver sensitivity (with target BER and KP4 pre-FEC threshold, <a href="#sec:kp4,sec:sensitivity" data-reference-type="ref+Label" data-reference="sec:kp4,sec:sensitivity">[sec:kp4,sec:sensitivity]</a>).

##### Typical ledger (single-mode DR class).

Start from Tx OMA on the DCA (or from average power and ER). Subtract connector/coupling loss (1–3 dB per mated pair; fiber attach in CPO), fiber loss ($`\sim`$<!-- -->0.3–0.4 dB/km at 1310 nm; often negligible at 500 m), and MUX/de-MUX if WDM (2–5 dB per stage, <a href="#sec:wdm-hardware" data-reference-type="ref+Label" data-reference="sec:wdm-hardware">6.3</a>). Add penalties for TDECQ (already in the OMA spec for many PMDs), dispersion (<a href="#sec:chirp-dispersion" data-reference-type="ref+Label" data-reference="sec:chirp-dispersion">3.11</a>), and ORL/RIN reflection (<a href="#sec:optical-channel,sec:rin-values" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:rin-values">[sec:optical-channel,sec:rin-values]</a>). Compare the remainder to stressed sensitivity at pre-FEC BER $`2.4\times10^{-4}`$, and keep 1–3 dB+ of production margin (more for fleet corners). Electrical budgets parallel this for the host-to-module path: COM and pre-FEC BER (<a href="#sec:com,sec:eye-budget,sec:equalization" data-reference-type="ref+Label" data-reference="sec:com,sec:eye-budget,sec:equalization">[sec:com,sec:eye-budget,sec:equalization]</a>). LPO requires *both* ledgers to close without module DSP help.

## Module management: CMIS

### What CMIS is, and why an optical engineer cares

*CMIS* (Common Management Interface Specification) is the vendor-neutral management layer between a host (switch ASIC, NIC, or test fixture) and a pluggable or on-board optical module. The host talks to the module over a two-wire bus (TWI, I2C-like) through a paged register map: identity, power mode, alarms, per-lane monitors, and (at 224G/448G) link-training and host signal- integrity tuning extensions . CMIS covers QSFP-DD, OSFP, COBO, ELSFP, and CPO engines that expose the same management contract.

You touch CMIS on every bring-up and every field triage. It is how the host learns what module is seated, when lasers may turn on, what Tx/Rx power and temperature look like, and whether a link failed at the management layer or the optical layer. A module that passes BER on a bench with lasers forced on but cannot reach ModuleReady on a production host will fail in the fleet (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>).

### The module state machine

CMIS defines a module state machine the host drives. After presence detect and power application, the module stays in low power until the host releases `LPModeL` (or the CMIS 5.x `LowPwr` equivalent). The host reads identifier pages, clears sticky interrupts, and steps the module toward ModuleReady. Only then should Tx lanes or ELS lasers enable. ELSFP modules that emit before ModuleReady are a reject: the host did not authorize light (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

Data paths have their own state machines in CMIS 5.x (data path states, and network path states for media-side links). For bring-up, map the sequence in <a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a> onto these transitions: presence and Vcc, CMIS init and ModuleReady, enable light, optical path check, electrical lock, traffic, snapshot. Skipping step 2 and jumping to BER is how interop failures hide until production.

### The memory map: pages, monitors, control

The lower memory map holds module identity, status, interrupt flags, and alarm thresholds. Upper pages hold application descriptors, lane controls, tunable-laser support, versatile diagnostics (VDM), and command-data-block (CDB) firmware messaging . Hosts select an application (lane count, host interface, media type) before bringing up traffic.

*DDM* (digital diagnostic monitoring) is the telemetry layer you read at scale: per-lane Tx and Rx optical power, laser bias current when exposed, module temperature, supply voltage, LOS/LOL flags, and alarm/warning bits. On WDM parts you also get wavelength or channel ID. This is exactly what <a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a> reads before anyone reaches for a DCA. On bring-up, dump the register map you will use in the field and treat that dump as the golden reference for later RMA comparisons.

### CMIS as a validation deliverable

CMIS correctness is part of production readiness, not a firmware afterthought. ATP should prove the state machine reaches ModuleReady across voltage and thermal corners; DDM monitors track bench truth (CMIS Tx power versus DCA, module temperature versus case $`T`$); alarms fire at the right thresholds; and firmware revision is ECO-controlled like laser die revision (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>). Multi-source interop failures are often CMIS, media-type, or firmware mismatches, not marginal TDECQ (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>). At fleet scale the register map is the only eyes you have on a module in the rack. If CMIS is wrong, triage starts blind.

## Module and system bring-up

Characterization proves a sample can meet metrics on a quiet bench. Bring-up proves a module (then a system) can be powered, managed, and linked the way production and the fleet will actually run it. Lab-to-production programs fail in the gap between those two if you only ever test golden hosts, clean fiber, and room-temperature faceplates.

##### Module bring-up sequence.

Run this order on every new module (pluggable, ELSFP, or CPO engine with CMIS). Do not skip ahead to BER: a link that “works” with lasers forced on and CMIS ignored will fail the first host that enforces the state machine (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

1.  **Presence and power.** Detect module (`ModPrsL` or equivalent). Apply rails in the host power sequence. Confirm Vcc and module temperature in CMIS. Stay in low power (`LPModeL` asserted or ModuleLowPwr) until management is sane.

2.  **CMIS init.** Read identifier, vendor, firmware rev, supported media. Clear sticky interrupts. Confirm the state machine can reach ModuleReady (or the pluggable equivalent) under host command. Dump the register map you will use in the field; that dump is your bring-up golden reference.

3.  **Enable light.** Exit low power; enable Tx lanes / ELS lasers only after ModuleReady. Confirm Tx optical power and laser bias (if exposed) against the power class. Lasers that come up before the host asks are a reject for ELSFP (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

4.  **Optical path.** Mate fiber (clean first). Check Rx power and LOS. Optical loopback first if the host path is unproven.

5.  **Electrical lock.** Bring host SerDes / module CDR. Confirm LOL clear, equalizer taps not pegged (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>). For LPO, this is the host eye and COM path (<a href="#sec:com,sec:drivers" data-reference-type="ref+Label" data-reference="sec:com,sec:drivers">[sec:com,sec:drivers]</a>).

6.  **Traffic.** PRBS or live FEC traffic. Pre-FEC BER vs. KP4 threshold (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>); glance at FEC symbol-error histogram shape.

7.  **Quality snapshot.** On a Tx-capable path: OMA/RLM/TDECQ or module diagnostics that proxy them (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>). Record CMIS + BER + case $`T`$ together so later triage has a baseline (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

<a href="#tab:bringup-checklist" data-reference-type="ref+Label" data-reference="tab:bringup-checklist">7.2</a> is the short form you can put on a lab wall.

<span id="tab:bringup-checklist" data-label="tab:bringup-checklist"></span>

| Step | Action | Pass signal | Fail $`\to`$ first look |
|:---|:---|:---|:---|
| 1 | Presence / Vcc / temp | CMIS alive, rails in range | cable, seat, PSU |
| 2 | CMIS state machine | ModuleReady (or equiv.) | firmware, TWI, LPMode |
| 3 | Enable Tx / ELS | Tx power in class; lasers on only when commanded | bias driver, enable pin, APC |
| 4 | Fiber / Rx power | Rx power up; LOS clear | dirty MT, polarity, break |
| 5 | CDR / SerDes lock | LOL clear; taps not saturated | host SI, LPO COM, retimer |
| 6 | Pre-FEC BER | below KP4 target with margin | Tx quality, ORL, Rx sensitivity |
| 7 | Snapshot | CMIS dump + BER + $`T`$ logged | (needed for RMA later) |

**Table .** Module bring-up checklist. LOS = loss of signal; LOL = loss of lock. Limits come from the ATP and PMD, not from this table.

##### Production-representative corners.

Bench corners ($`T`$, $`V`$) are necessary and not sufficient. Before you call DVT or PVT done, run the corners that match how the fleet will abuse the link. <a href="#tab:prod-corners" data-reference-type="ref+Label" data-reference="tab:prod-corners">7.3</a> is the minimum set for IM/DD + laser programs.

<span id="tab:prod-corners" data-label="tab:prod-corners"></span>

| Corner | What to run | Why it catches | Points to |
|:---|:---|:---|:---|
| Chassis thermal | Module in target rack/sled at airflow and power load; not only a quiet chamber on a bench fixture | Faceplate $`T`$ and TEC load differ from chamber setpoints | derate, TEC, ring unlock |
| Host rails live | Bias / CMIS powered from host supplies with SerDes traffic on | Switching noise into laser bias looks like RIN (<a href="#sec:laser-drivers" data-reference-type="ref+Label" data-reference="sec:laser-drivers">5.6</a>) | PSRR, ground, APC |
| Dirty fiber / ORL | Controlled contamination or ORL stress on MT/FAU; clean vs dirty BER | Field installs are not lab-clean; ORL raises RIN and bursts | connector, isolator, feedback |
| Cable plant | Production fiber length, MPO count, and bend radius | Extra loss and reflections eat margin the ledger assumed | link budget (<a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>) |
| ELS hot-swap | Pull/replace ELSFP under traffic (or under controlled traffic stop per CMIS) | Service action the architecture promised (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>) | state machine, mate cycles |
| Neighbor load | Adjacent modules/lanes at full traffic and max case $`T`$ | Crosstalk, shared supply droop, thermal crosstalk on rings | WDM lock, SI, PSU |
| LPO / linear path | Host COM and pre-FEC BER without module DSP crutch | LPO fails here first (<a href="#sec:224g-deploy,sec:com,sec:drivers" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:com,sec:drivers">[sec:224g-deploy,sec:com,sec:drivers]</a>) | host FIR, module linearity |
| Voltage corners | Host Vcc min/max with traffic | Brown-out and CMIS glitches | power design, ATP |

**Table .** Production-representative corners. A quiet BERT at 25 $`^\circ`$C with pristine fiber is characterization, not production readiness.

##### System bring-up.

A module that passes on a golden host can still fail in a real chassis:

- **Host path:** run the same sequence on the target NIC/switch ASIC SerDes, not only the lab BERT. LPO and half-retimed modules expose host FIR/CTLE mistakes that a retimed module hid (<a href="#sec:conditioning,sec:pluggables" data-reference-type="ref+Label" data-reference="sec:conditioning,sec:pluggables">[sec:conditioning,sec:pluggables]</a>).

- **Multi-lane / multi-module:** bring all lanes on a port, then neighbors in the same cage or tray. Watch thermal rise, supply droop, and CMIS temp alarms when the tray is loaded.

- **Golden swap:** known-good module in the suspect host slot, then suspect module in a known-good slot. That single swap splits host vs. module before you open FA (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

- **Interop:** at least one other vendor host or module if the program claims multi-source. Interop failures are usually CMIS, media type, or electrical eye, not laser physics.

- **ELS / CPO:** external laser modules add a second bring-up: ELSFP state machine and optical mate to the engine, then engine bring-up with light present (<a href="#sec:elsfp,sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:elsfp,sec:cpo-status">[sec:elsfp,sec:cpo-status]</a>). A dark engine with a healthy ELS is an optical connector or FAU problem until proven otherwise.

##### Exit criteria before “bring-up done.”

Call module bring-up done only when: CMIS state machine and enable sequence are correct; pre-FEC BER meets target on the *target* host with margin; a CMIS+BER+$`T`$ snapshot is filed; and at least the chassis-thermal, host-rails, and ORL corners in <a href="#tab:prod-corners" data-reference-type="ref+Label" data-reference="tab:prod-corners">7.3</a> have been run on a representative unit. Call system bring-up done when golden-swap has split host vs. module issues and multi-lane / neighbor load has not opened a new failure mode. Everything after that is characterization depth, supplier gates (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>), or fleet triage (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

**Key idea.** Bring-up is a sequence (presence $`\to`$ CMIS $`\to`$ light $`\to`$ lock $`\to`$ BER $`\to`$ snapshot), then a system proof on the real host, then production-representative corners (chassis thermal, host-rail noise, ORL, ELS hot-swap, neighbor load). A quiet bench pass is not DVT.

## The debug mindset

Debug at this level is data-driven, not opinion-driven. The method is disciplined bisection: change one domain at a time, and let the measurement tell you whether the transmitter, the channel, or the receiver moved.

1.  Isolate transmitter versus channel versus receiver, using loopbacks.

2.  Sweep temperature and voltage to expose corner-dependent failures.

3.  Correlate failures to DSP equalizer tap values (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>) and FEC symbol-error statistics (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>); these tell you *how* the link fails.

The third step is where modern PAM4 links differ from older eye-mask work. Tap saturation and FEC histograms often reveal the failure mode before a single waveform screenshot does. Treat those as primary evidence, not as afterthoughts logged once BER already fails.

[^17]

## Fleet and field triage

Lab debug asks: *what is broken on this unit?* Fleet triage asks: *which bucket does this failure belong in, and who owns the fix?* Optical programs at fleet scale own that split across performance, reliability, and manufacturability. Wrong bucket wastes weeks (sending a contaminated connector to laser FA, or rewriting a SerDes FIR when the laser is rolling over).

##### Three buckets.

Classify every field issue before deep root-cause work:

Performance  
the design or operating point does not close the budget under the conditions seen in the fleet. Examples: TDECQ/RLM marginal at case temperature, host COM tight on LPO, ring unlock under thermal crosstalk, ORL-driven RIN that the architecture assumed away. Fix is usually retune, derate, firmware, or a design/spec change (<a href="#sec:tdecq,sec:com,sec:siring" data-reference-type="ref+Label" data-reference="sec:tdecq,sec:com,sec:siring">[sec:tdecq,sec:com,sec:siring]</a>).

Reliability  
the unit met spec at ship and later degraded. Examples: LIV threshold rise, SMSR collapse, EAM bias creep, COD, TEC wear, epoxy creep on fiber attach. Fix is Arrhenius-backed life projection, burn-in/screen, derating, or field-replaceable lasers (<a href="#sec:wearout-modes,sec:laser-aging,sec:gr468,sec:elsfp" data-reference-type="ref+Label" data-reference="sec:wearout-modes,sec:laser-aging,sec:gr468,sec:elsfp">[sec:wearout-modes,sec:laser-aging,sec:gr468,sec:elsfp]</a>).

Manufacturability  
a subpopulation fails early or never met the ATP; the issue tracks lot, date code, supplier site, or assembly step. Examples: FAU misalign yield cliff, solder void on a driver die attach, incoming DPPM spike, CMIS register map mismatch on one firmware rev. Fix is SPC, ATP tighten, first-article, DPA, and 8D/CAPA with the supplier (<a href="#sec:supplier-exec,sec:photonic-packaging" data-reference-type="ref+Label" data-reference="sec:supplier-exec,sec:photonic-packaging">[sec:supplier-exec,sec:photonic-packaging]</a>).

A single symptom can sit in more than one bucket until you bisect. The tree below forces the split with telemetry first, then a short bench confirm, then an RMA label.

##### Telemetry you actually read.

At scale you rarely start with a DCA. Start with what the host and module already report:

- *CMIS* monitors and alarms: module temperature, supply rails, Tx/Rx optical power, laser bias (when exposed), wavelength or channel ID on WDM parts, LOS/LOL flags, and interrupt history (`IntL` on ELSFP; <a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>).

- Host link state: CDR lock, pre-FEC BER, FEC symbol-error histogram shape (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>), equalizer tap saturation (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>).

- Fleet context: rack position, case temperature, time since install, date code / lot, neighbor-link correlation (one bad fiber vs whole tray).

##### Decision tree (symptom $`\to`$ bucket).

<a href="#tab:fleet-triage" data-reference-type="ref+Label" data-reference="tab:fleet-triage">7.4</a> is the working map. Read left to right: observe, check telemetry, pick a provisional bucket, then run the named confirm measurement before you open an RMA or change a design rule.

<span id="tab:fleet-triage" data-label="tab:fleet-triage"></span>

| Symptom | First telemetry check | Bucket | Confirm on bench / FA | Typical fix owner |
|:---|:---|:---|:---|:---|
| Link never comes up (fresh install) | CMIS presence, Vcc, Tx power flatline, LOS | Mfg or install | Visual fiber/connector; golden module swap; CMIS dump | Ops install; supplier ATP if lot-correlated |
| Intermittent LOS / burst errors | Rx power dropouts; FEC bursts; ORL events | Perf (ORL) or mfg (contam.) | Clean/inspect MT; ORL meter; RIN vs ORL (<a href="#sec:laser-drivers,sec:rin-values" data-reference-type="ref+Label" data-reference="sec:laser-drivers,sec:rin-values">[sec:laser-drivers,sec:rin-values]</a>) | Ops cleaning; packaging if repeat RMA |
| Pre-FEC BER high, power OK | Tap saturation; RLM/TDECQ if logged; case $`T`$ | Perf | DCA TDECQ/RLM; host COM; LPO vs retimed path (<a href="#sec:tdecq,sec:com" data-reference-type="ref+Label" data-reference="sec:tdecq,sec:com">[sec:tdecq,sec:com]</a>) | Host SI / module Tx design |
| BER rises only at high case $`T`$ | Module temp alarm; Tx power drop; $`\lambda`$ walk | Perf or reliability | LIV at $`T`$; OSA grid; TEC current; EAM bias (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>) | Derate / TEC / laser supplier |
| Slow BER creep over weeks/months | Bias current up for same Tx power; SMSR if monitored | Reliability | LIV/SMSR vs ship ATP; Arrhenius lot history | Laser wear-out; ELS replace |
| Sudden hard fail, was healthy | Last good CMIS snapshot; neighbor links OK | Reliability (COD) or mfg (ESD) | Dark LIV; DPA on facet/solder; date-code cluster? | FA + supplier 8D |
| One date code / site fails early | Lot Pareto; burn-in escape rate | Mfg | Incoming SPC vs ATP; FA on sample of lot | Supplier CAPA; hold shipment |
| WDM / ring unlock, power OK | Channel ID; thermal of neighbors; lock-loop status | Perf | Resonance tune; crosstalk; CW-WDM line power (<a href="#sec:lock-validation,sec:thermal-xtalk,sec:cwwdm-laser" data-reference-type="ref+Label" data-reference="sec:lock-validation,sec:thermal-xtalk,sec:cwwdm-laser">[sec:lock-validation,sec:thermal-xtalk,sec:cwwdm-laser]</a>) | Lock firmware / thermal design |
| ELSFP swap restores link | Old module CMIS vs new; connector cycles | Reliability or mfg (connector) | Inspect MT; mating-cycle count; laser LIV in returned module (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>) | Laser vs connector split in FA |

**Table .** Fleet triage map: symptom to provisional bucket to confirm measurement. Perf $`=`$ performance (design/operating point); reliability $`=`$ time-dependent wear; mfg $`=`$ lot/process/install excursion.

##### How to walk an incident (order of operations).

1.  **Stabilize and capture.** Freeze CMIS dump, host BER/FEC counters, rack $`T`$, and install age before anyone reseats the module. Reseating destroys connector evidence.

2.  **Localize.** One link vs tray vs rack. Tray-wide points at power, cooling, or a shared ELS. Single-link points at that module, fiber, or host lane.

3.  **Classify** with <a href="#tab:fleet-triage" data-reference-type="ref+Label" data-reference="tab:fleet-triage">7.4</a>. Write the bucket on the ticket before FA starts.

4.  **Confirm** with the smallest measurement that can falsify the bucket (golden swap, clean/inspect, LIV, TDECQ, ORL). Do not skip to DPA.

5.  **Act.**

    - Performance: change operating policy (derate, FIR, lock loop) or open a design/spec defect.

    - Reliability: replace (ELSFP hot-swap when available), update FIT burn-down, tighten burn-in or derate (<a href="#sec:laser-aging,sec:fit-example" data-reference-type="ref+Label" data-reference="sec:laser-aging,sec:fit-example">[sec:laser-aging,sec:fit-example]</a>).

    - Manufacturability: quarantine lot, incoming hold, supplier 8D with DPA photos and ATP deltas (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>).

6.  **Close the loop.** Feed the signature back into ATP and CMIS alarm thresholds so the next incident trips earlier.

##### Worked paths (three common tickets).

*“High temp only.”* CMIS shows module near thermal limit and Tx power sagging. Bucket starts as performance (thermal design / derate) until LIV at temperature shows threshold rise matching an aged lot, which flips it to reliability. Measure OSA wavelength before blaming the laser: a ring unlock is still performance (<a href="#sec:siring,ch:wdm" data-reference-type="ref+Label" data-reference="sec:siring,ch:wdm">[sec:siring,ch:wdm]</a>).

*“Random burst errors, average power fine.”* Check FEC histogram for clustered errors and CMIS for Rx power dropouts. Clean and measure ORL. If RIN rises with ORL, it is performance/architecture (feedback). If ORL is fine and bursts track a date code, it is mfg (intermittent fiber attach). If bursts grow over months at fixed ORL, suspect laser or driver aging (<a href="#sec:laser-drivers,sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-drivers,sec:laser-aging">[sec:laser-drivers,sec:laser-aging]</a>).

*“ELSFP replace fixed it; returned module looks alive on the bench.”* Alive LIV with high ORL sensitivity or dirty MT face means connector/ORL (mfg/ops), not laser death. Dead or kinked LIV means reliability. Split those RMA codes explicitly or your FIT math will blame the wrong wear-out mode (<a href="#sec:elsfp,sec:photonic-packaging" data-reference-type="ref+Label" data-reference="sec:elsfp,sec:photonic-packaging">[sec:elsfp,sec:photonic-packaging]</a>).

##### RMA labels that keep FIT honest.

RMA codes should be distinct, not a single “optics fail”:

- laser wear-out (LIV/SMSR/EAM aging confirmed);

- COD / sudden dark;

- connector / contamination / ORL;

- fiber attach / FAU;

- driver / bias electronics;

- host / SerDes / LPO eye (not module);

- NFF (no-fault-found; track these; high NFF means bad triage).

NFF rate and lot Pareto are as important as FIT. A rising NFF with clean LIV points at install practice or intermittent connectors, not Arrhenius.

**Key idea.** Fleet triage is bucket-first: performance (budget/design), reliability (time), or manufacturability (lot/process). Read CMIS and host FEC before you touch a DCA; confirm with one falsifying measurement; label RMAs so FIT, ATP, and supplier 8D point at the real owner (<a href="#tab:fleet-triage" data-reference-type="ref+Label" data-reference="tab:fleet-triage">7.4</a>).

# Reliability and manufacturing at scale

A link that closes in the lab can still fail the business case if lasers die in the field or suppliers cannot hold yield. At gigawatt, multi-generation scale, reliability and manufacturability stop being afterthoughts and become design constraints: they decide whether you put the laser on the ASIC package or in a replaceable module, how hard you derate, and what ATP language you freeze with partners. This chapter covers the vocabulary of failure at scale, the qualification flows that project field life, and the supplier-execution work these systems demand.

## The language of scale: FIT and DPPM

Fleet arguments need two different numbers. One is about life in the field; the other is about quality at the factory door.

FIT (failures in time)  
failures per $`10^{9}`$ device-hours. Multiply a per-laser FIT by the number of lasers in a fleet and by hours to estimate failures per day.

DPPM (defective parts per million)  
the manufacturing-quality counterpart, measured at incoming or outgoing inspection.

[^18]

## Qualification flows

Optoelectronics inherited a common qualification language from telecom: *Telcordia GR-468-CORE*. The core stress tests still show up on every laser and module program:

- HTOL (high-temperature operating life) and burn-in.

- Temperature cycling and damp heat.

- Electrostatic-discharge and mechanical stress.

*Arrhenius* acceleration underpins life projection: raising temperature accelerates wear-out by a factor set by the activation energy, so a bounded high-temperature test projects years of field life. Screening (burn-in) removes infant-mortality parts before deployment.

##### GR-468 in practice.

Telcordia GR-468-CORE is the common qualification language for optoelectronic modules and discrete lasers. For optical engineers the actionable pieces are test-plan alignment (map your ATP to GR-468 stress sequences such as HTOL, temperature cycle, damp heat, and ESD so supplier and customer agree on pass/fail), activation energy (FIT projections use Arrhenius acceleration; document $`E_a`$ and confidence bounds when converting 1000-hour HTOL to field years), sample-size humility (qualification lots are small; production SPC catches drift that qual missed, <a href="#tab:npi" data-reference-type="ref+Label" data-reference="tab:npi">8.2</a>), and boundary clarity: qualify the laser die, the hermetic package, and the module assembly separately when failures split across those boundaries (<a href="#sec:photonic-packaging,sec:laser-aging,sec:elsfp" data-reference-type="ref+Label" data-reference="sec:photonic-packaging,sec:laser-aging,sec:elsfp">[sec:photonic-packaging,sec:laser-aging,sec:elsfp]</a>).

##### GR-1221: the passive-component companion.

GR-468 covers active optoelectronics. Its companion, *Telcordia GR-1221-CORE* (Generic Reliability Assurance Requirements for Passive Optical Components), covers the parts GR-468 does not: connectors, fiber couplers, WDM filters and MUX/DEMUX, splitters, and isolators . It uses the same style of stress sequence (damp heat, temperature cycling, mechanical, and aging tests) but scores pass/fail on insertion loss and return loss rather than on LIV. A short-reach link that leans on an on-package or blind-mate MUX and on external multi-wavelength sources carries a passive reliability budget that lives in GR-1221, not GR-468 (<a href="#sec:connector-reliability,ch:wdm" data-reference-type="ref+Label" data-reference="sec:connector-reliability,ch:wdm">[sec:connector-reliability,ch:wdm]</a>). Split the qual the same way you split the FIT: active laser die under GR-468, silicon under JESD47, passive optics under GR-1221.

##### ATP sketch: EML module or ELSFP.

A short acceptance sketch lives with the qual hooks in <a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>; the full ATP-as-contract, SPC, and 8D workflow is in <a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>. Failures that pass qual but fail field usually sit in derating policy or connector contamination (<a href="#sec:laser-aging,sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:laser-aging,sec:fleet-triage">[sec:laser-aging,sec:fleet-triage]</a>).

## Electronics reliability: driver, TIA, and DSP silicon

GR-468 covers the optoelectronic parts of the link: the laser die, the photodiode, and the hermetic or non-hermetic package around them. The modulator driver, TIA, retimer, and DSP (<a href="#sec:drivers,sec:pd-tia" data-reference-type="ref+Label" data-reference="sec:drivers,sec:pd-tia">[sec:drivers,sec:pd-tia]</a>) are ordinary CMOS or SiGe BiCMOS ICs, and they wear out and fail by a different, better-documented set of mechanisms. Treat them with the semiconductor industry’s own qualification language, not with Arrhenius laser-aging math borrowed from <a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>.

##### JESD47: the silicon-side GR-468.

JEDEC JESD47 is the baseline stress-test-driven qualification flow for a new IC, a device family, or a process change: temperature cycling, HTOL, HTSL (high-temperature storage life), autoclave or HAST (highly accelerated stress test) for moisture, and mechanical shock and vibration . It plays the same role for driver and TIA silicon that GR-468 plays for the laser: a common list of stresses that a supplier runs once and a customer accepts instead of renegotiating a qual plan on every design win.

##### ESD and latch-up: failure modes GR-468 does not test.

Two mechanisms are specific to ICs and absent from the laser-side wear-out map in <a href="#tab:wearout-map" data-reference-type="ref+Label" data-reference="tab:wearout-map">8.1</a>:

ESD  
a discharge event during handling or assembly damages a gate oxide or junction. Component-level classification uses the human-body model (HBM) and charged-device model (CDM) test standards, *ANSI/ESDA/JEDEC JS-001* and *JS-002* . A driver or TIA datasheet HBM/CDM rating is the number that protects the part on the factory floor, at fiber-attach and wire-bond stations where a laser die is also exposed.

Latch-up  
a parasitic thyristor structure in CMOS turns on under an overvoltage or current-injection event and holds a low-impedance path until power is cycled. *JESD78* defines the overvoltage and $`\pm100`$ mA current-injection test that classifies susceptibility by supply and signal pin . A latched driver IC can look like a dead laser on the bench (no light, no LIV signature) until you check the supply current instead of the optical path.

Both mechanisms are 100%-screen or design-margin items, not something you project with an activation energy. If a driver fails ESD or latch-up in the field, that is a manufacturability or design-margin bucket item (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>), not a wear-out FIT argument.

##### AEC-Q100: a borrowed grade, not a requirement.

*AEC-Q100* is the automotive industry’s qualification standard for ICs, built on the same JEDEC JESD47/JESD22 stress methods with tighter ESD targets and named temperature grades from Grade 3 ($`-40`$ to $`85`$°C) up to Grade 0 ($`-40`$ to $`150`$°C) . Datacenter optics does not require Q100; the fleet lives in a controlled data hall, not an engine bay. It is still a useful signal: a driver, TIA, or retimer die that also ships in an automotive part number typically carries a published Q100 grade, and that grade is a fast proxy for the ESD/latch-up margin and temperature-cycle depth behind the datasheet, without re-running the qual plan yourself.

##### Where this lands in the ATP.

Fold IC-level qual into the same acceptance and SPC structure used for the laser (<a href="#tab:atp-laser,sec:supplier-exec" data-reference-type="ref+Label" data-reference="tab:atp-laser,sec:supplier-exec">[tab:atp-laser,sec:supplier-exec]</a>): require the supplier’s JESD47 qual report and HBM/CDM/latch-up ratings for driver and TIA die at DVT, add an ESD handling audit to the incoming-QC checklist alongside laser LIV/SMSR sampling, and treat a driver/TIA silicon revision the same way you treat a laser die revision or a CMIS firmware rev: an ECO that needs first-article requalification, not a silent BOM swap.

## Wear-out modes to know

Arrhenius math, derating, and the worked FIT example live in <a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>. This section is the mechanism catalog: how each failure shows up in ATP and telemetry, and which triage bucket owns it (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>). Do not run process CAPA on a wear-out part, and do not burn FIT math on a dirty connector.

##### Infant mortality versus wear-out versus packaging.

Field failures come in three clocks, and mixing them up wastes CAPA. Infant mortality is early fails from latent defects; burn-in and HTOL screens remove them before ship (<a href="#sec:gr468" data-reference-type="ref+Label" data-reference="sec:gr468">8.2.0.0.1</a>). Wear-out is gradual or sudden end-of-life in the laser or EAM under temperature, current, and optical power, projected with Arrhenius and derating (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>). Packaging and assembly faults (FAU align, epoxy creep, solder voids, connector wear) often dominate field returns once lasers are screened (<a href="#sec:photonic-packaging" data-reference-type="ref+Label" data-reference="sec:photonic-packaging">8.5</a>). Destructive physical analysis (facet cross-section, EDX, FAU section) is required when the signature is ambiguous or when you need evidence for supplier 8D (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>).

##### Mechanism map.

<a href="#tab:wearout-map" data-reference-type="ref+Label" data-reference="tab:wearout-map">8.1</a> is the working list for laser-bearing modules and CPO/ELS paths. Customize limits in the ATP; keep the classification discipline.

<span id="tab:wearout-map" data-label="tab:wearout-map"></span>

| Mechanism | Observable | ATP / telemetry | Triage bucket |
|:---|:---|:---|:---|
| COD (facet) | Sudden dark or hard fail; was healthy | Dark LIV; DPA facet; date-code cluster? | Reliability (COD) or mfg (ESD) |
| Gradual facet / active region | $`I_\mathrm{th}`$ up, slope down over life | LIV trend vs ship ATP; HTOL lot history | Reliability (wear-out) |
| SMSR collapse | Side modes rise; modal noise / BER | OSA SMSR vs floor at $`T`$ | Reliability; watch aging |
| EAM aging (EML) | TDECQ/RLM creep at fixed bias | EAM bias sweep + DCA; bias creep log | Reliability (EAM) |
| RIN rise | BER floor up; feedback sensitive | RIN @ ORL; isolator / connector check | Perf if ORL; reliability if isolator |
| TEC / thermal control | Unlock or $`\lambda`$ walk; LIV may look fine | TEC current, case $`T`$, lock status | Perf (lock) or reliability (TEC) |
| Coupling / FAU / solder | Loss step, intermittent LOS, shock-related | ORL, mate cycles, DPA FAU/solder | Manufacturability / packaging |
| Driver/TIA latch-up (ESD) | Sudden hard fail; no light, no LIV signature; supply current spikes | Supply current vs bias; JESD78 rating; date-code cluster? | Mfg (ESD) or design margin |
| Connector wear / contamination | ORL creep after repeated mate cycles; RIN floor rise | Mate-cycle count vs IEC 61300-2-2 rating; endface grade (IEC 61300-3-35) | Manufacturability / packaging |

**Table .** Wear-out and packaging mechanisms versus observables. Arrhenius projection and derating for the laser rows: <a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>. Electronics stress qualification: <a href="#sec:ic-reliability" data-reference-type="ref+Label" data-reference="sec:ic-reliability">8.3</a>. Connector reliability: <a href="#sec:connector-reliability" data-reference-type="ref+Label" data-reference="sec:connector-reliability">8.5.0.0.1</a>. Field classification workflow: <a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>.

*Catastrophic optical damage* (COD) is the sudden facet failure under optical or electrical overstress. Gradual facet and active-region degradation move threshold and slope on a slower clock. EAM aging shifts the absorption curve and shows up as transmitter and dispersion eye closure quaternary (TDECQ) or RLM drift before the DFB LIV looks dead. TEC and lock failures mimic optical wear-out until you bisect heater versus laser (<a href="#sec:lock-validation" data-reference-type="ref+Label" data-reference="sec:lock-validation">6.7</a>). Coupling and FAU faults belong with packaging, not with Arrhenius $`E_a`$ arguments.

## Photonic packaging and module-level failures

Fleet FIT is not only laser wear-out. Once lasers are screened and derated, module and packaging failures often dominate field returns: the part that shipped with a clean LIV still loses light after shock, humidity, or a thousand ELSFP mate cycles. Fiber attach and FAU alignment fail from shock, humidity ingress, and epoxy creep; CPO fiber-array units add assembly steps that wafer test cannot catch (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>). Hybrid stacks (TFLN-on-Si, InP laser on Si, flip-chip drivers) introduce solder voids, underfill cracks, and RF return-loss drift (<a href="#sec:tfln-mzm,sec:drivers" data-reference-type="ref+Label" data-reference="sec:tfln-mzm,sec:drivers">[sec:tfln-mzm,sec:drivers]</a>). Thermal paths matter too: uncooled datacom versus liquid-cooled XPO/CPO, and TEC failure that looks like wavelength drift off grid or off ring (<a href="#sec:siring,ch:wdm" data-reference-type="ref+Label" data-reference="sec:siring,ch:wdm">[sec:siring,ch:wdm]</a>).

##### Connector reliability: MPO, mating cycles, and endface quality.

Multi-fiber connectors are the highest-touch mechanical interface in the fleet: every ELSFP swap, every fiber-attach unit (FAU) rework, and every cable-plant install mates and unmates an MPO. The MPO/MT ferrule family (rectangular, 6.4 mm $`\times`$ 2.5 mm, guide-pin aligned, 8/12/16/24 fibers per row) is standardized in *IEC 61754-7*, split into one-fibre-row and two-fibre-row parts . That standard fixes geometry, not lifetime; lifetime comes from two companion test methods. *IEC 61300-2-2* specifies the mate/unmate cycling test connector datasheets are rated against, and *IEC 61300-3-35* grades endface scratches, pits, and debris into pass/fail zones on the fiber core and cladding . TIA-568.3 sets 500 cycles as the structured-cabling mating-durability floor; MPO/MTP-class connectors in practice are commonly rated well above 1000 cycles, but that headroom erodes fast with the wrong cleaning discipline (<a href="#sec:optical-channel" data-reference-type="ref+Label" data-reference="sec:optical-channel">7.2.2</a>).

Three practical consequences follow for an ELSFP or CPO fiber-attach program. First, ORL creep is a mating-cycle and cleaning problem before it is a laser problem: a rising RIN floor after repeated ELS swaps (<a href="#tab:wearout-map" data-reference-type="ref+Label" data-reference="tab:wearout-map">8.1</a>) is diagnosed with an IEC 61300-3-35-style endface inspection, not a laser FA request. Second, mate-cycle count belongs in the same telemetry you already read for CMIS and DDM (<a href="#sec:cmis" data-reference-type="ref+Label" data-reference="sec:cmis">7.7</a>); track it per connector, not per module, since a connector can outlive several module swaps or vice versa. Third, write the mating-cycle and endface-grade limits into the ATP explicitly (<a href="#tab:atp-laser" data-reference-type="ref+Label" data-reference="tab:atp-laser">8.3</a>) rather than inheriting a generic MPO datasheet number: an ELS bank that hot-swaps weekly reaches a 500-cycle floor in under ten years, and a CPO fiber array that is field-serviced more aggressively reaches it faster still.

ELSFP cycling adds connector wear and contamination that raise ORL (<a href="#sec:optical-channel,sec:elsfp" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:elsfp">[sec:optical-channel,sec:elsfp]</a>); the mating-cycle and endface-grade limits above are exactly the numbers that turn “the connector feels loose” into an ATP line item instead of a guess.

Destructive physical analysis (cross-section, EDX) and structured 8D/CAPA with suppliers close the loop from RMA to design rule (<a href="#sec:supplier-exec,sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:supplier-exec,sec:fleet-triage">[sec:supplier-exec,sec:fleet-triage]</a>). Without that loop, packaging FIT gets mis-attributed to laser Arrhenius models and the wrong part gets redesigned.

## Production test at volume

### Test time is a cost, coverage is a risk

Every second in the acceptance test plan (ATP) times millions of units is line capacity and real money. Every skipped measurement is escaped DPPM in the field (<a href="#sec:fit-dppm" data-reference-type="ref+Label" data-reference="sec:fit-dppm">8.1</a>). The core tension in high-volume manufacturing is not “test or don’t test” but how much coverage you buy per second. The expensive optical steps are thermal soak and corner runs, TDECQ on a sampling scope, BER dwell long enough to trust a low pre-FEC target, laser burn-in, and mate-cycle stress on ELSFP connectors. Some screens are statistical (sample burn-in from a lot, audit TDECQ on a subset). Others must be 100%: CMIS state machine sanity, basic LIV/SMSR pass, and any test that catches a safety or enable-sequence fault (<a href="#sec:cmis,sec:laser-safety" data-reference-type="ref+Label" data-reference="sec:cmis,sec:laser-safety">[sec:cmis,sec:laser-safety]</a>).

### Where the test happens: wafer, die, module, system

Push defect detection as far upstream as correlation allows. Wafer-level or PIC probe catches process shifts (waveguide loss, ring resonance drift, bad heaters) before fiber attach and packaging spend. Killing a bad die at probe is orders of magnitude cheaper than an RMA (<a href="#sec:photonic-packaging" data-reference-type="ref+Label" data-reference="sec:photonic-packaging">8.5</a>). Module ATP is the full functional test: optical power class, TDECQ or proxy, sensitivity spot-check, CMIS bring-up, and connector/ORL on ELS parts. System or golden-host bring-up catches interop: media type, firmware rev, equalizer defaults, and the corners in <a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a>. Wafer test cannot catch fiber attach, FAU alignment, epoxy creep, or connector wear. Those failures must survive to module ATP and, for some signatures, to fleet telemetry (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

### ATE-to-bench correlation

Production testers are built for speed and cost, not lab fidelity. The number that matters is correlation: does the ATE TDECQ, OMA, or sensitivity track the DCA/BERT reference within a known offset and spread? Set ATP limits with guardbands derived from that spread. A drifting tester or a stale golden unit shows up as a yield cliff or a DPPM escape. Keep a golden module (and golden laser subassembly for ELS), run gauge R&R across testers and shifts, and correlate CMIS monitors to bench instruments the same way you correlate TDECQ (<a href="#sec:cmis" data-reference-type="ref+Label" data-reference="sec:cmis">7.7</a>). If the ATE and the DCA disagree, fix the correlation before you argue with the supplier about spec.

### Screens, guardbanding, and SPC

Burn-in and HTOL screens trade infant-mortality escape rate against test time and cost (<a href="#sec:wearout-modes,sec:gr468" data-reference-type="ref+Label" data-reference="sec:wearout-modes,sec:gr468">[sec:wearout-modes,sec:gr468]</a>). Test limits are usually guardbanded tighter than the customer spec so field DPPM stays inside target under drift. SPC control charts on LIV, SMSR, RIN, TDECQ, and mate-cycle yield by lot, site, and date code catch a process shift before it becomes an 8D (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>). Production test is a yield, DPPM, and cost trade under a fixed reliability target. It is not a pass/fail checkbox after the optics already work on a golden bench.

## Supplier execution playbook

The supplier path is milestones, performance targets, quality, and manufacturability triage. That is not a soft skill. It is a concrete contract: requirements, gates, acceptance tests, process control, and corrective action when a lot goes wrong.

##### NPI gates and exit criteria.

<a href="#tab:npi" data-reference-type="ref+Label" data-reference="tab:npi">8.2</a> is the usual stage map. For lasers and IM/DD modules, write exit criteria that a supplier can fail clearly, not slogans.

<span id="tab:npi" data-label="tab:npi"></span>

| Gate | Question | Laser / optics exit criteria (examples) | Who signs |
|:---|:---|:---|:---|
| EVT | Does it work at all? | First light; CMIS bring-up sequence (<a href="#sec:bringup" data-reference-type="ref+Label" data-reference="sec:bringup">7.8</a>); LIV/SMSR/RIN on engineering samples; one link closes BER | Optical eng + supplier FAE |
| DVT | Spec across corners? | Full ATP at $`T`$/$`V`$ corners; prod-rep corners (<a href="#sec:prod-corners" data-reference-type="ref+Label" data-reference="sec:prod-corners">7.8.0.0.2</a>); TDECQ/OMA/sensitivity; GR-468 stress plan frozen; FIT model agreed | Optical eng + reliability |
| PVT | Buildable at yield? | Multi-lot yield vs ATP; SPC charts live; burn-in escape rate; FAIR on production tooling; bring-up on production host | Optical eng + SQE / mfg |
| MP | Sustained quality? | Steady DPPM; RMA Pareto owned; ECO control on CMIS/firmware and process | Program + supplier QM |

**Table .** NPI gates with laser-relevant exit criteria. EVT/DVT/PVT/MP are stage names, not a schedule; dates and sample sizes belong in the program plan with the supplier.

Hold a gate if the exit data are missing. Shipping PVT material without frozen ATP limits is how field NFF and FIT arguments start (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>).

##### Requirements and ATP are the contract.

ATP and the requirements doc are the contract. Write both and keep them versioned together:

1.  **Requirements / PRD slice for the laser path:** fill <a href="#tab:laser-prd,sec:laser-reqs" data-reference-type="ref+Label" data-reference="tab:laser-prd,sec:laser-reqs">[tab:laser-prd,sec:laser-reqs]</a> (power class, grid, RIN@ORL, SMSR, derating, CMIS, FIT). Version it with the ATP.

2.  **Acceptance test plan (ATP):** the measurable tests that prove those requirements on every ship lot (or on a defined sample). Map each ATP line to a GR-468 or design-validation stress where life is claimed (<a href="#sec:gr468" data-reference-type="ref+Label" data-reference="sec:gr468">8.2.0.0.1</a>).

<a href="#tab:atp-laser" data-reference-type="ref+Label" data-reference="tab:atp-laser">8.3</a> is a working ATP checklist for an EML pluggable or an ELSFP CW module. Customize limits from the datasheet and the link budget; do not invent numbers in the ATP itself.

<span id="tab:atp-laser" data-label="tab:atp-laser"></span>

| ATP item | Instrument / method | Pass intent | Ties to |
|:---|:---|:---|:---|
| LIV ($`I_\mathrm{th}`$, slope, kink) | SMU + power meter | kink-free bias window at rated $`T`$ | wear-out, derate (<a href="#sec:laser-params" data-reference-type="ref+Label" data-reference="sec:laser-params">5.5</a>) |
| SMSR | OSA | single-mode vs. spec floor | modal noise, aging |
| RIN (intrinsic + stressed ORL) | PD + ESA | $`\mathrm{RIN}_x\mathrm{OMA}`$ / quiet floor | BER floor (<a href="#sec:rin-values" data-reference-type="ref+Label" data-reference="sec:rin-values">4.3.1</a>) |
| Wavelength / grid | OSA / wavemeter | channel ID; $`d\lambda/dT`$ | WDM lock (<a href="#ch:wdm" data-reference-type="ref+Label" data-reference="ch:wdm">6</a>) |
| Optical power class | power meter | ELSFP / MSA class met | link budget |
| EAM bias / chirp (EML) | bias sweep + DCA | ER, RLM, TDECQ at baud | Tx quality (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>) |
| CMIS / TWI bring-up | host or CMIS tool | registers, alarms, state machine | field telemetry |
| Connector / ORL | mate cycles + ORL meter | cycles + endface grade vs IEC 61300 limits | packaging (<a href="#sec:connector-reliability,sec:elsfp" data-reference-type="ref+Label" data-reference="sec:connector-reliability,sec:elsfp">[sec:connector-reliability,sec:elsfp]</a>) |
| Burn-in screen | HTOL sample or 100% screen | infant mortality culled | GR-468 (<a href="#sec:gr468" data-reference-type="ref+Label" data-reference="sec:gr468">8.2.0.0.1</a>) |
| Driver/TIA ESD, latch-up | supplier JESD47/HBM/CDM report; sample audit | rating on file; no latch-up under current injection | IC reliability (<a href="#sec:ic-reliability" data-reference-type="ref+Label" data-reference="sec:ic-reliability">8.3</a>) |
| Thermal class | chamber at case $`T`$ | LIV/RIN/CMIS still pass | derate policy |

**Table .** Acceptance checklist for laser-bearing modules (EML or ELSFP). Limits are program-specific; the structure is what you negotiate with the supplier.

##### Incoming QC and SPC.

Qual lots are small. Production catches drift that qual missed.

- **Incoming:** sample or 100% screen against a subset of the ATP (at least power, CMIS, and a laser LIV/SMSR sample). Track DPPM by date code and site.

- **SPC**: control charts on $`I_\mathrm{th}`$, slope, SMSR, Tx power, and burn-in fallout. A process shift is a hold, not a hope.

- **First-article / FAIR:** when tooling, epi, or assembly site changes, rerun a defined FAIR package before open PO volume. Treat CMIS firmware revs the same way as process changes.

##### Excursions: 8D / CAPA.

When a lot fails ATP, incoming, or field triage lands in the manufacturability bucket (<a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a>), run structured corrective action:

1.  **Contain:** quarantine WIP and ship holds; identify suspect date codes in the fleet.

2.  **Evidence pack:** failing ATP rows, CMIS dumps, LIV/SMSR/RIN plots, DPA photos (facet, solder, FAU cross-section) compared to a golden unit.

3.  **8D / CAPA**: root cause with the supplier (process step, material lot, firmware), corrective action, and preventive control (ATP tighten, SPC limit, poke-yoke).

4.  **Verify:** re-run FAIR on the corrected process; watch field RMA codes for that date-code family for a defined burn-in window.

Do not close 8D on “operator error” without a control that would have caught it at ATP. If FA shows laser wear-out on a young unit, it may be a reliability screen gap, not a supplier process bug; reclassify with <a href="#sec:fleet-triage" data-reference-type="ref+Label" data-reference="sec:fleet-triage">7.10</a> before you argue FIT.

##### Milestone hygiene with partners.

Align the partner calendar to gates, not slideware:

- freeze requirements before DVT samples are built;

- freeze ATP limits before PVT yield is claimed;

- freeze FIT/$`E_a`$ assumptions before reliability marketing numbers ship;

- require ECO notice on laser die revision, TEC vendor, FAU epoxy, driver/TIA silicon revision (<a href="#sec:ic-reliability" data-reference-type="ref+Label" data-reference="sec:ic-reliability">8.3</a>), and CMIS firmware.

Your job in those meetings is to name the measurement that would kill the gate. If nobody can point to an ATP row or a corner, the milestone is not real.

**Key idea.** Reliability at scale is mechanism discipline plus supplier gates. Classify failures with the wear-out map (<a href="#tab:wearout-map" data-reference-type="ref+Label" data-reference="tab:wearout-map">8.1</a>) before you argue FIT or open 8D. Laser wear-out gets Arrhenius and GR-468; driver and TIA silicon gets JESD47, HBM/CDM ESD, and latch-up ratings (<a href="#sec:ic-reliability" data-reference-type="ref+Label" data-reference="sec:ic-reliability">8.3</a>); MPO connectors get mating-cycle and endface-grade limits (<a href="#sec:connector-reliability" data-reference-type="ref+Label" data-reference="sec:connector-reliability">8.5.0.0.1</a>). Supplier execution is a gated contract: requirements and ATP at DVT, multi-lot SPC and FAIR at PVT, then 8D with evidence when a lot or field Pareto says manufacturability. Do not run process CAPA on a wear-out failure, and do not burn FIT math on a dirty or worn connector.

## From component FIT to fabric availability

The FIT arithmetic in <a href="#sec:fit-example" data-reference-type="ref+Label" data-reference="sec:fit-example">5.7.0.0.4</a> gives a rate: about $`0.6`$ laser failures per day for a fleet of $`5\times10^5`$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>), but it does not say what a failure costs or how a running job survives one. Two facts turn a per-component rate into a fabric problem.

First, a training or large inference job is synchronous. A collective (<a href="#sec:collectives" data-reference-type="ref+Label" data-reference="sec:collectives">9.7</a>) waits for its slowest member, so a single dead or slow link stalls the whole group, not just one endpoint (<a href="#sec:inference-bottlenecks" data-reference-type="ref+Label" data-reference="sec:inference-bottlenecks">9.6</a>). A link that flaps for a second is a stall for every accelerator in that collective. The optical FIT the earlier chapters budget therefore matters out of proportion to its share of the parts count.

Second, at cluster scale failures are continuous, not rare. Meta’s published Llama 3 run is the clearest public data point: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . GPU and HBM3 faults dominated at close to half; network switch and cable faults were 35 events, 8.4% of the total. The optical link is a minority of hard job stops, but 8.4% of a failure every three hours is still tens of network events per run, and the ELS, module, and connector FIT this chapter budgets (<a href="#sec:fit-dppm,sec:connector-reliability" data-reference-type="ref+Label" data-reference="sec:fit-dppm,sec:connector-reliability">[sec:fit-dppm,sec:connector-reliability]</a>) lands in exactly that bucket.

So the design question shifts. It is no longer “how reliable is one link” but “how does a fabric of $`10^5`$ links keep a job running through a failure every few hours.” The answers are architectural, and the optical engineer feeds each one.

Redundancy and rails.  
Rail-optimized topologies (<a href="#sec:topologies" data-reference-type="ref+Label" data-reference="sec:topologies">9.2</a>) already give parallel planes; dual-plane and dual-ToR designs let a lost link degrade bandwidth instead of dropping an endpoint. Redundancy multiplies the link and laser count, which feeds straight back into the FIT budget: more resilience is more parts that can fail.

Detection and reroute.  
Transient faults stay below the job. KP4 FEC (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>) absorbs the error bursts a marginal link throws; link-level retry and sub-second link-flap detection plus adaptive routing steer traffic off a degraded link before the scheduler notices. Vendor fabrics (NVIDIA Spectrum-X and Quantum, Broadcom Tomahawk) advertise adaptive or “cognitive” routing and link-level retry for this. Treat the specifics as vendor orientation, but the mechanism is why transient optical faults rarely reach the hard-stop bucket above.

Topology reconfiguration.  
When a link or rack dies for good, an optical circuit switch re-wires the topology around it in milliseconds, so the scheduler routes around the dead node instead of stalling the pod (<a href="#sec:ocs" data-reference-type="ref+Label" data-reference="sec:ocs">9.9</a>) . Component FIT still applies; the fabric survives each failure by re-wiring optically.

Sparing and field service.  
Hot spare nodes and lanes cover the interval between failure and repair. Field-replaceable external lasers (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>) make a dead laser a faceplate swap rather than a fabric outage, which is the architectural reason ELS decouples laser FIT from switch FIT. The connector mating-cycle and endface budget (<a href="#sec:connector-reliability" data-reference-type="ref+Label" data-reference="sec:connector-reliability">8.5.0.0.1</a>) sets how many of those swaps the plant survives.

The cost of a failure closes the loop. A hard interruption is lost compute plus the time to detect, reroute or reschedule, and restart from the last checkpoint. Fast detection and reroute shrink that lost time, which is the fabric-level reason the module work in this chapter pays off: derating (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>), burn-in and screens (<a href="#sec:gr468" data-reference-type="ref+Label" data-reference="sec:gr468">8.2.0.0.1</a>), and a tight ATP (<a href="#sec:supplier-exec" data-reference-type="ref+Label" data-reference="sec:supplier-exec">8.7</a>) lower the failure rate, and a resilient fabric lowers the cost of each failure that slips through. The two multiply.

**Key idea.** Component FIT sets the failure *rate*; the fabric sets the failure *cost*. A synchronous collective makes one bad link everyone’s stall (<a href="#sec:collectives" data-reference-type="ref+Label" data-reference="sec:collectives">9.7</a>), and at cluster scale failures are continuous: Meta’s Llama 3 run saw a failure about every three hours, network faults 8.4% of them, at roughly 90% effective uptime . The fabric survives that with redundant rails, FEC and fast reroute, OCS topology reconfiguration (<a href="#sec:ocs" data-reference-type="ref+Label" data-reference="sec:ocs">9.9</a>), and field-replaceable lasers (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>). Lowering per-link FIT and lowering per-failure cost multiply, which is why link reliability sets how large a dependable fabric can grow.

# AI datacenter networking

Optics only make sense once you see the fabric they sit in. Training and inference clusters are not one network; they are several overlapping networks with different bandwidth, latency, and reach needs. This chapter places the devices and validation methods from earlier chapters into that system context: how AI clusters are wired, why the interconnect sits on the inference critical path, and where optics dominates cost and power.

## Scale-up versus scale-out

The industry borrowed two words from computer architecture and overloaded them for AI fabrics. Keeping them straight matters, because they buy different optics.

Scale-up  
tight coupling inside a node or rack: GPU-to-GPU over a memory-semantic fabric (for example NVLink). Very high bandwidth, very low latency. Increasingly optical as bandwidth outgrows copper reach.

Scale-out  
coupling across racks and pods over a switched network (Ethernet or InfiniBand). This is where pluggable and co-packaged optics have long lived.

<figure id="fig:scale-node" data-latex-placement="ht">
<embed src="figures/fig_scale_up_node.pdf" />
<figcaption>Schematic AI compute node (one tray in a larger cluster). <em>Accelerators</em> are the heavy compute engines (typically GPUs; the book also uses XPU for GPUs and custom ASICs). <strong>Scale-up</strong> links (red) tie accelerators through a high-bandwidth, low-latency switch fabric inside the node or rack (NVLink-class). <strong>Scale-out</strong> links (blue) leave via a dedicated NIC per accelerator into the datacenter Ethernet or InfiniBand fabric. The CPU and front-end NIC handle host, storage, and management traffic.<span id="fig:scale-node" data-label="fig:scale-node"></span></figcaption>
</figure>

### Three networks, two that set the optics budget

The OIF CEI-448G framework names *three* distinct networks in a large AI cluster . <a href="#fig:scale-node" data-reference-type="ref+Label" data-reference="fig:scale-node">9.1</a> shows two; the third is easy to overlook:

Scale-up  
accelerator-to-accelerator inside a pod or rack. Highest bandwidth per link, lowest latency, often lossless. Dominates compute time if under- provisioned.

Scale-out  
accelerator-to-accelerator (or node-to-node) across the cluster over a switched fabric (InfiniBand, *UEC*/Ethernet with RoCE or Ultra Ethernet Transport). Lower per-link bandwidth than scale-up, but must reach $`10^5`$+ endpoints.

Front-end  
CPU-attached traffic: management, control plane, checkpointing, storage, and training-data ingest. Analogous to a conventional cloud datacenter network; not the IM/DD bottleneck this book focuses on, but it shares the same rack power and cabling budget.

Scale-up carries the majority of *interconnect* bandwidth inside a training job; scale-out multiplies link count across the building. That is why both push 448G-class lane rates and why optics shows up first on scale-out, then on scale-up as copper reach shrinks .

### Scale-up versus scale-out at a glance

<a href="#tab:oif-scale" data-reference-type="ref+Label" data-reference="tab:oif-scale">9.1</a> condenses OIF Table 1 (CEI-448G framework, §2.2): order-of- magnitude targets for node count, physical extent, and media type . Numbers are industry snapshots, not hard limits, but they explain why “optics inside the rack” and “optics between racks” arrive on different timelines.

<span id="tab:oif-scale" data-label="tab:oif-scale"></span>

<table id="tab:oif-scale" style="width:90%;">
<colgroup>
<col style="width: 22%" />
<col style="width: 17%" />
<col style="width: 17%" />
<col style="width: 17%" />
<col style="width: 17%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"></th>
<th colspan="2" style="text-align: center;">Scale-up</th>
<th colspan="2" style="text-align: center;">Scale-out</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><span>2-3</span>(lr)<span>4-5</span> Metric</td>
<td style="text-align: left;">Today</td>
<td style="text-align: left;">Next gen</td>
<td style="text-align: left;">Today</td>
<td style="text-align: left;">Next gen</td>
</tr>
<tr>
<td style="text-align: left;">Accelerator nodes in domain</td>
<td style="text-align: left;"><span class="math inline">∼</span>100</td>
<td style="text-align: left;"><span class="math inline">∼</span>1 k</td>
<td style="text-align: left;">100 k+</td>
<td style="text-align: left;"><span class="math inline">≫</span>100 k</td>
</tr>
<tr>
<td style="text-align: left;">Physical extent</td>
<td style="text-align: left;">Rack</td>
<td style="text-align: left;">Rack to row</td>
<td style="text-align: left;">Datacenter</td>
<td style="text-align: left;">Datacenter</td>
</tr>
<tr>
<td style="text-align: left;">Network properties</td>
<td colspan="2" style="text-align: left;">Lossless, low latency</td>
<td colspan="2" style="text-align: left;">Large scale; multi-tier switching</td>
</tr>
<tr>
<td style="text-align: left;">Media within rack</td>
<td colspan="2" style="text-align: left;">Electrical: passive PCB / twinax backplane</td>
<td colspan="2" style="text-align: left;">Electrical: twinax backplane</td>
</tr>
<tr>
<td style="text-align: left;">Media between racks</td>
<td style="text-align: left;">AEC (adjacent racks)</td>
<td style="text-align: left;">Optical (within row)</td>
<td colspan="2" style="text-align: left;">Optical (pluggable or CPO on switch/NIC)</td>
</tr>
</tbody>
</table>

**Table .** Scale-up vs. scale-out snapshots (adapted from OIF CEI-448G framework Table 1, 2025). Scale-up stays on copper as long as rack densification keeps channels short; scale-out is already optical at datacenter scale.

### Standards bodies: who owns what

448G/lane signaling is not owned by one standards body, and that is by design. Electrical reach, Ethernet naming, connectors, and rack packaging evolved in different rooms; AI fabrics forced them to meet at the same lane rate. OIF’s CEI-448G framework (§2.3) lists the groups that must align . <a href="#tab:sdo-map" data-reference-type="ref+Label" data-reference="tab:sdo-map">9.2</a> maps each body to the layer an optical engineer actually touches. The short version: OIF sets the electrical baud and reach classes; IEEE names the Ethernet optical PMD; UALink and UEC own scale-up and scale-out protocol stacks; SNIA and OCP decide connectors and where the optics physically live. The *LPO MSA* is not a standards body, but it publishes the only open end-to-end spec that stitches CEI Linear electrical limits to IEEE optical PMD limits for DSP-less modules (<a href="#sec:lpo-msa" data-reference-type="ref+Label" data-reference="sec:lpo-msa">9.3.1</a>). Prose below expands each row, OIF and non-OIF.

<span id="tab:sdo-map" data-label="tab:sdo-map"></span>

| Body | Fabric | What matters for short-reach optics |
|:---|:---|:---|
| OIF CEI | All reaches | Electrical PHY: XSR/VSR/MR/LR, 448G PAM4/6/8, LPO/LRO; CMIS for module management |
| UALink | Scale-up | Open load/store pod fabric; 200G/lane today, $`\sim`$<!-- -->400G/lane next; drives XSR-class PHY needs |
| UEC | Scale-out | Ultra Ethernet Transport, congestion control; PHY group surveying 400G/lane enhancements |
| SNIA SFF | Host / backplane | Cables, connectors, PCIe/EDSFF form factors; SFF 448G COM for backplane (complements CEI front-panel work) |
| OCP | Rack / system | Open rack designs, CPO/XPO placement, optical circuit switching (OCS) for AI clusters |
| IEEE 802.3 | Scale-out (+ optics PMD) | Ethernet MAC rates (802.3dj, 400G/lane SG), KP4 FEC, IM/DD PMD clauses (DR/FR, TDECQ) |
| 100G Lambda MSA | Scale-out optics | Originated the 100G/$`\lambda`$ single-mode PMDs (100G-FR/LR, 400G-DR4/FR4/LR4) later folded into IEEE 802.3; RIN$`_x`$OMA transmitter method the DR/FR and LPO specs inherit |
| IBTA | Scale-out | InfiniBand Architecture; NDR 400G, XDR 800G/port at 200G/lane, 1.6T switch links; reuses QSFP/OSFP + MPO optics with Ethernet |
| IEEE 802.1 | All fabrics | Link-layer security: MACsec (802.1AE) line-rate encryption; 802.1X port access control |
| PCI-SIG / CXL | Scale-up, in-node | PCIe 7.0 (128 GT/s PAM4) and CXL 4.0 memory fabric; PCI-SIG Optical Workgroup for optical PCIe |
| DMTF / OpenConfig / SONiC | Management | Box and fleet telemetry and config (Redfish, OpenConfig, SONiC); complement OIF CMIS module management |

**Table .** SDO and consortium roles at 448G/lane. The top six rows follow OIF CEI-448G §2.3; the 100G Lambda MSA, IBTA, IEEE 802.1, PCI-SIG/CXL, and the management stack are added for coverage beyond OIF’s own list.

##### OIF.

Common Electrical I/O (*CEI*) Implementation Agreements are the modular electrical PHY recipes: die-to-die (*XSR*), chip-to-module (*VSR*), chip-to-chip (*MR*), and backplane (*LR*). CEI-448G is the current AI-driven push beyond 224G/lane . Related OIF tracks include energy-efficient interfaces (EEI), CMIS management extensions at 448G, and coherent DCI (out of scope for this book). For optics, CEI tells you the *baud and reach* the module or CPO engine must meet; IEEE 802.3 tells you how Ethernet names the optical PMD.

##### UALink Consortium.

*UALink* specifies an open *scale-up* stack (transaction, data link, and physical layers) optimized for direct accelerator memory access, not IP/Ethernet . UALink 1.0 targets 200G/lane and pods up to roughly 1 k accelerators; the physical-layer working group is gathering requirements for $`\sim`$<!-- -->400G/lane. Optical engineers care because higher lane rate reduces port count on the accelerator package, and because scale-up eventually hits the same copper reach wall as CEI XSR (<a href="#sec:trace-loss" data-reference-type="ref+Label" data-reference="sec:trace-loss">9.5</a>).

##### Ultra Ethernet Consortium.

*UEC* builds a complete Ethernet-based stack for AI/HPC *scale-out*: transport (UET), link layer, and PHY enhancements . UEC 1.0 (June 2025) targets cluster-scale congestion control and RDMA-class performance over standard Ethernet hardware, including NICs, switches, optics, and cables. The PHY working group is surveying 400G/lane improvements. This is the protocol layer above the transceiver; IM/DD module specs still come from IEEE and MSAs.

##### SNIA (SFF Technology Affiliate).

SNIA’s SFF working group defines connectors, cables, and form factors for storage and compute backplanes, not front-panel Ethernet . The SFF 448G project (SFF-TA-1043) parallels CEI-448G but focuses on backplane COM, package insertion loss, and PAM choice on copper channels inside the box. Pair OIF VSR (module connector) with SFF (host PCB and PCIe cable) when debugging a link budget.

##### Open Compute Project.

OCP publishes open rack, server, and networking designs for hyperscale . Relevant work includes Open Systems for AI, short-reach optical interconnect guidelines, and the Optical Circuit Switching (OCS) subproject (2025) for reconfigurable cluster fabrics. OCP rarely specifies baud rate; it specifies *where* the optical engine lives (faceplate pluggable vs. CPO vs. XPO) and how it is cooled and serviced.

##### IEEE 802.3.

Ethernet standards define MAC rates, FEC (KP4 in Clause 91), and interoperable optical PMDs . 802.3dj (200G/lane) and the 400G/lane study group name the product generations that consume 224G and 448G-class optics. One naming trap: IEEE quotes **400 Gb/s per lane** (MAC/info rate); CEI quotes **$`\sim`$<!-- -->448 Gb/s** (line rate with coding overhead). Same physics, different accounting (<a href="#ch:imdd,tab:rate-stack" data-reference-type="ref+Label" data-reference="ch:imdd,tab:rate-stack">[ch:imdd,tab:rate-stack]</a>).

##### 100G Lambda MSA.

The single-mode PMDs this book leans on did not start at IEEE. The *100G Lambda MSA*, formed in 2017 by a broad group of suppliers and hyperscalers, wrote the first interoperable optical specifications built on one wavelength carrying 100 Gb/s PAM4 ($`\approx`$<!-- -->53 GBd): 100G-FR and 100G-LR for single-wavelength 100 GbE, and 400G-DR4/FR4/LR4 for four-lane 400 GbE over duplex single-mode fiber . IEEE 802.3 then adopted the same 100 Gb/s-per-$`\lambda`$ approach into its DR/FR/LR PMD clauses, and the LPO MSA 100G-DR-LPO profile (<a href="#sec:lpo-msa" data-reference-type="ref+Label" data-reference="sec:lpo-msa">9.3.1</a>) inherits both that modulation and the RIN$`_x`$OMA transmitter method the MSA defined (<a href="#sec:rin" data-reference-type="ref+Label" data-reference="sec:rin">4.3</a>). For a short-reach engineer this is the body behind the reach-class names on almost every single-mode datasheet: when a module is called “DR4” or “FR4,” the per-wavelength recipe traces to this MSA even where the compliance point is now quoted against an IEEE clause.

##### InfiniBand Trade Association.

The *IBTA* maintains the InfiniBand Architecture Specification, the other dominant scale-out fabric for AI and HPC alongside Ethernet . Data rates follow the same per-lane SerDes ladder: NDR reaches 400 Gb/s per port over four 100 Gb/s lanes, and XDR reaches 800 Gb/s per port over four 200 Gb/s lanes, with switch-to-switch links at 1.6 Tb/s (XDR figures are from the 2023 spec announcement and remain provisional). For the optical engineer the physical layer is close to the Ethernet case: the same QSFP and OSFP form factors, the same MPO fiber, and DR/FR-class IM/DD optics at matching lane rates. InfiniBand changes the transport and congestion model (credit-based flow control, RDMA), not the transceiver. It is absent from the OIF §2.3 list because IBTA runs its own specification, but it occupies the same scale-out slot as UEC.

##### IEEE 802.1 (link-layer security).

Encryption is a link-layer function, and at 800G and 1.6T it has to run at line rate. *MACsec* (IEEE 802.1AE) provides connectionless confidentiality, frame integrity, and data origin authenticity at the MAC layer, transparent to the MAC client; IEEE 802.1X handles port access control and the key agreement that establishes MACsec associations . This lands on optics indirectly: line-rate MACsec costs latency and gate count in the switch ASIC or NIC, not in the transceiver, and an LPO or DSP-less module carries the ciphertext transparently. Encryption is therefore orthogonal to the optical PMD choice (<a href="#sec:lpo-msa" data-reference-type="ref+Label" data-reference="sec:lpo-msa">9.3.1</a>), but it belongs in the standards map because a fabric-security requirement can still gate a module program at qualification.

##### PCI-SIG and CXL.

Inside the node, the load-store fabric is PCI Express and *CXL*. PCI-SIG released PCIe 7.0 in 2025 at 128 GT/s per lane using PAM4 and flit encoding, and the CXL Consortium built CXL 4.0 on that same PCIe 7.0 electrical base for coherent memory pooling . Both are 2025 releases, so treat the exact rates and the optical-interface scope as provisional. Both are copper-first and short today, but PCI-SIG runs an Optical Workgroup defining a technology-agnostic optical PCIe interface, and CXL memory disaggregation across a rack is exactly the reach that pulls optics into a bus that was never optical before. For a short-reach optics team this is the emerging in-node and in-rack case to watch: PAM4 at PCIe rates over fiber, with the same modulator and detector problems as an Ethernet lane.

##### Management and telemetry.

Module management is OIF CMIS (<a href="#sec:cmis" data-reference-type="ref+Label" data-reference="sec:cmis">7.7</a>), but the box and fleet layers above it are not OIF. *DMTF Redfish* is the RESTful standard for server and switch management and telemetry; *OpenConfig* defines vendor-neutral data models and streaming telemetry (gNMI) for network devices; and *SONiC* is the open network operating system many hyperscalers run, with its own dataplane telemetry hooks . These are where per-module CMIS monitors surface as fleet signals: optical power, case temperature, FEC symbol-error counts, and pre-FEC BER aggregated across $`10^5`$ links (<a href="#ch:reliability,sec:fabric-availability" data-reference-type="ref+Label" data-reference="ch:reliability,sec:fabric-availability">[ch:reliability,sec:fabric-availability]</a>). A module program that ships without a telemetry contract into one of these systems is effectively invisible at fleet scale.

The frontier is optics entering the scale-up domain (optical NVLink-class links, co-packaged switches), because copper reach at 200G/lane is only about a meter.

## Topologies and why optics count explodes

Cluster topology is where optical count stops being “a few modules per server” and becomes a fleet problem. Large AI fabrics mostly use fat-tree / Clos, rail-optimized, or dragonfly layouts. In a classic $`k`$-ary fat-tree, link count scales as $`O(k^3)`$ while endpoints scale as $`O(k^2)`$: optics multiply faster than compute. Rail-optimized designs (one NIC rail per accelerator row, all-to-all within a rail) rose with collective-heavy training and inference because they cut oversubscription on all-reduce paths, at the price of more parallel optical planes. Dragonfly and other hierarchical topologies trade some global bisection bandwidth for fewer long links.

The optical engineer cares because every topology choice sets link count, which sets laser count, module count, and FIT budget (<a href="#ch:reliability" data-reference-type="ref+Label" data-reference="ch:reliability">8</a>); rail layouts drive fan-out from leaf to spine and push denser 800G/1.6T ports toward CPO/XPO (<a href="#sec:cpo-status,sec:xpo" data-reference-type="ref+Label" data-reference="sec:cpo-status,sec:xpo">[sec:cpo-status,sec:xpo]</a>); and scale-up inside the rack stays electrical longer while scale-out between racks is already optical (<a href="#tab:oif-scale" data-reference-type="ref+Label" data-reference="tab:oif-scale">9.1</a>). That explosion in link count is the economic reason a hyperscaler builds an in-house optical engineering team.

## Pluggable form factors and module styles

Faceplate modules differ in aggregate rate, lane count, electrical reach, and where the DSP lives. The form factor sets the passive channel the SerDes must survive, and the last decade of AI networking has mostly been a fight over that choice: keep a retimer in the module for interop, delete it for watts (LPO/LRO), or move the optics onto the package (CPO) and service the laser from the faceplate (ELSFP).

QSFP-DD / OSFP  
the incumbent datacom pluggables. QSFP-DD carries 800G/1.6T class products (eight lanes at 100G or 200G per lane). OSFP targets higher power and density (1.6T today, 3.2T roadmaps) with a larger cage and better thermal path. Both impose a VSR-class electrical channel from host PCB through the connector (<a href="#sec:trace-loss,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:trace-loss,sec:conditioning">[sec:trace-loss,sec:conditioning]</a>).

Retimed module  
DSP/CDR inside the module (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>). Default for interoperability; $`\sim`$<!-- -->15–20 W class at 800G/1.6T.

LPO / LRO  
linear or lightly retimed: delete or slim module DSP (<a href="#sec:conditioning,sec:drivers,fig:oif-448g-package,fig:eq-chains" data-reference-type="ref+Label" data-reference="sec:conditioning,sec:drivers,fig:oif-448g-package,fig:eq-chains">[sec:conditioning,sec:drivers,fig:oif-448g-package,fig:eq-chains]</a>). Power drops to $`\sim`$<!-- -->7–9 W but host EQ and transmitter and dispersion eye closure quaternary (TDECQ) margin tighten.

ELSFP / external laser  
field-replaceable CW source for CPO (<a href="#sec:cpo-status,ch:lasers" data-reference-type="ref+Label" data-reference="sec:cpo-status,ch:lasers">[sec:cpo-status,ch:lasers]</a>): decouples laser FIT from switch FIT.

XPO  
liquid-cooled mega-pluggable (<a href="#sec:xpo" data-reference-type="ref+Label" data-reference="sec:xpo">9.11</a>): 12.8 Tb/s per module, front-panel serviceability with CPO-class density.

*CMIS* (<a href="#sec:cmis" data-reference-type="ref+Label" data-reference="sec:cmis">7.7</a>) is the management layer for module identity, monitors, and (at 224G/448G) link-training and host-side signal-integrity tuning extensions. Optical engineers touch it when debugging lock, FEC, and equalizer settings across vendors.

##### Half-retimed and asymmetric modules.

Not every pluggable is fully retimed or fully linear. Common 2025–26 variants sit between those poles:

LPO  
linear drive and linear receive: no module DSP/CDR (<a href="#sec:equalization,sec:drivers" data-reference-type="ref+Label" data-reference="sec:equalization,sec:drivers">[sec:equalization,sec:drivers]</a>).

LRO / RTLR  
retimed transmit, linear receive (OIF RTLR): DSP on electrical $`\to`$ optical only; eases host TX while keeping a simpler RX path .

TRO / half-retimed  
symmetric opposite or partial retiming variants appear in vendor roadmaps; always check which direction carries the DSP.

Fully retimed  
DSP both directions; default for interoperability at 800G/1.6T.

Power scales with DSP content: retimed $`\sim`$<!-- -->15–20 W, LRO $`\sim`$<!-- -->9 W, LPO $`\sim`$<!-- -->7–9 W at 800G class (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>). The architecture choice is a trade between host margin (COM, TDECQ) and module watts.

### The LPO MSA: stitching IEEE optics to CEI Linear

OIF CEI tells you the electrical recipe at the module cage. IEEE 802.3 tells you how Ethernet names the optical PMD and its TDECQ/OMA limits. Neither document, by itself, is a complete product spec for a linear pluggable that deletes the module DSP. The *LPO MSA* (Linear Pluggable Optics Multi-Source Agreement) fills that gap: one open specification for both sides of the module, with normative test points and host responsibilities spelled out .

The first published revision, *100G-DR-LPO* (v1.0, March 2025), targets 100 Gb/s per lane at 53.125 GBd PAM4 on single-mode fiber from 0.5 m to 500 m. It is explicitly a data-center profile: low power, low latency, high port density, RS(544,514) FEC on the host, and form-factor agnostic (QSFP, QSFP-DD, OSFP are examples, not the spec). The naming pattern generalizes to `n00G-DRn-LPO` for $`n\in\{1,2,4,8\}`$ lanes. Optical reach and modulation track IEEE DR-class PMDs; the electrical interface tracks OIF CEI-112G-LINEAR-PAM4. That split is the template 224G linear modules follow: CEI-224G-Linear on the AUI, 802.3dj optical PMD limits on the fiber (<a href="#sec:224g-deploy,sec:pmd-reach" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:pmd-reach">[sec:224g-deploy,sec:pmd-reach]</a>).

##### Who owns which block.

In an LPO link the host is not a passive cable driver. It runs KP4 FEC (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>), full SerDes equalization (CTLE, FFE, DFE, CDR; <a href="#sec:equalization,sec:serdes-dsp" data-reference-type="ref+Label" data-reference="sec:equalization,sec:serdes-dsp">[sec:equalization,sec:serdes-dsp]</a>), and optional nonlinear compensation (NLC) and startup protocol functions. The module is analog: linear driver, modulator or laser, photodiode, TIA, and at most a fixed CTLE. No retiming, no FEC, no heavy DSP. CMIS (<a href="#sec:cmis" data-reference-type="ref+Label" data-reference="sec:cmis">7.7</a>) is the management contract. SFF hardware specs (QSFP-DD, OSFP cages) set the mechanical envelope. The MSA’s job is to define what must pass at each interface between those blocks so modules from different vendors close on the same host.

##### The test-point ladder.

LPO MSA normative compliance is organized around six electrical/optical test points (<a href="#tab:lpo-tp" data-reference-type="ref+Label" data-reference="tab:lpo-tp">9.3</a>), the concrete instance of the general TP0-to-TP5 planes in <a href="#sec:test-points" data-reference-type="ref+Label" data-reference="sec:test-points">3.9</a>. Think of them as the validation script: host TX at TP1a, module optical TX at TP2, stressed optical RX at TP3, module electrical RX at TP4, and stressed host RX at TP4a. Section 10 of the MSA adds a host-to-host end-to-end BER test with FEC-encoded traffic, which is how you prove interop after the point tests pass.

| Point | Location | Principal measurements |
|:---|:---|:---|
| TP1a | Host SerDes output | EECQ (electrical eye closure), host TX quality |
| TP1 | Module electrical input | Module input stressor calibration |
| TP2 | Optical TX (2–5 m patch cord) | TDECQ, TECQ, OMA$`_{\mathrm{outer}}`$, RIN$`_{x\mathrm{OMA}}`$, ER |
| TP3 | Optical RX input | Stressed receiver calibration (SECQ), sensitivity masks |
| TP4 | Module electrical output | Module RX linear output (EECQ) |
| TP4a | Stressed host input | Host RX under worst-case module output |

LPO MSA test points (100G-DR-LPO). {#tab:lpo-tp}

##### Optical limits that matter.

The MSA optical tables (<a href="#sec:tdecq,ch:validation" data-reference-type="ref+Label" data-reference="sec:tdecq,ch:validation">[sec:tdecq,ch:validation]</a>) inherit IEEE 802.3 measurement methods with LPO-specific reference equalizers. The numbers you will quote in a datasheet review:

- TDECQ and TECQ capped at 3.4 dB per lane, measured with a 9-tap T-spaced reference FFE and SER target $`4.0\times10^{-4}`$.

- OMA$`_{\mathrm{outer}}`$ coupled to transmitter quality: launch power in OMA rises with max(TECQ, TDECQ) along a piecewise mask (for example $`-3.2 + \mathrm{max}(\mathrm{TECQ},\mathrm{TDECQ})`$ dBm in the mid-TECQ region).

- RIN$`_{x\mathrm{OMA}} \le -138`$ dB/Hz at 17.2 dB ORL (the “$`x`$” subscript tracks return loss, same convention as IEEE DR PMDs).

- Illustrative link budget 6.7 dB total at 500 m (3 dB channel loss plus 0.3 dB MPI penalty plus 3.4 dB TDECQ allocation).

- Stressed receiver sensitivity $`-3.1`$ dBm OMA$`_{\mathrm{outer}}`$ at TP3 with SECQ = 3.4 dB and aggressor lanes at 4.2 dBm OMA.

TECQ is TDECQ without the dispersion test fiber. The MSA uses both because outer OMA limits are written against max(TECQ, TDECQ), and a module can be fiber-limited even when the electrical eye looks clean.

##### Electrical limits and host COM.

On the electrical side the MSA points to CEI-112G-LINEAR-PAM4 for the host-to-module interface and defines EECQ (electrical eye closure quaternary) at TP1a and TP4a. That is the electrical analogue of TDECQ: a host that passes optical TDECQ at TP2 but fails EECQ at TP1a still will not interoperate. Host PCB insertion loss, connector, and module input return loss sit in the channel reference model (Section 7). For 224G deployment, swap CEI-112G-LINEAR for CEI-224G-Linear and run the same two-ledger program (<a href="#sec:224g-deploy,sec:com" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:com">[sec:224g-deploy,sec:com]</a>).

##### What to read first.

For a bring-up engineer the reading order is: Section 5 (system overview and host FEC requirements), Section 7 (electrical TPs and channel model), Section 8 (optical TX/RX tables), Section 9 (parameter definitions, especially 9.5 TDECQ/TECQ and 9.10 stressed RX), then Section 10 (host-to-host FEC BER). Cross-check every optical definition against the cited IEEE 802.3 clause; the MSA adds reference equalizer taps and SER targets, not new physics.

**Key idea.** OIF owns the electrical baud at the cage. IEEE owns the optical PMD metrics on the fiber. The LPO MSA is the product contract that binds them for DSP-less modules: normative test points, host FEC/EQ duties, and TDECQ/OMA masks you can test without a module retimer safety net.

### The LPO supplier base and the adoption question

The MSA defines what a linear module must pass; it does not settle whether the market buys one. By 2025–26 the supplier base had formed around the analog parts that replace the DSP: high-linearity TIAs and linear drivers. Macom, Semtech, and Maxlinear are the named component proponents, and once the DSP is gone the TIA and driver become the make-or-break blocks .

The demonstrations track a fast rate climb. Eoptolink showed a 200G/$`\lambda`$ four-channel LPO link with no DSP or CDR at OFC 2024 and moved a second-generation 100G/lane 800G and 400G single-mode line into volume, claiming full TP2 compliance at the transmit interface . Macom exhibited its PURE DRIVE 200 Gb/s LPO parts at OFC 2024 and extended them toward 212 Gb/s/lane for a 1.6T module, with the TIA and driver as the headline . Marvell, a DSP house, announced a 200G/lane TIA and laser-driver chipset for 800G and 1.6T LPO aimed at scale-up XPU fabrics . Macom and Eoptolink are founding members of the LPO MSA (<a href="#sec:lpo-msa" data-reference-type="ref+Label" data-reference="sec:lpo-msa">9.3.1</a>).

**LPO reaches into PCIe scale-up.** Alphawave and Innolight demonstrated a 64 Gb/s/lane PCIe 6.0 subsystem (controller plus PHY) over Innolight’s LPO OSFP optics at OFC 2024, then a 128 Gb/s/lane platform pairing a PCIe 7.0-ready SerDes PHY with the same optics . The pull is the switch-fabric pull again: larger, faster AI nodes need more PCIe reach than copper gives, and the linear module skips the DSP latency and power a retimed module would add (<a href="#sec:scale-up-out,sec:latency-budget" data-reference-type="ref+Label" data-reference="sec:scale-up-out,sec:latency-budget">[sec:scale-up-out,sec:latency-budget]</a>).

**Whether LPO wins is a separate question.** Host support exists: Juniper’s Broadcom-based QFX switches take LPO optics without hardware changes, and Arista has shown Broadcom TH5 compatibility for over two years . The market read is still cautious. Cignal AI argues LPO stays a small share, at least at 800G, because the installed fabric was already designed around DSP-based modules; 100G/lane (800GbE) LPO looks late and likely to hold only a small slice long term . At 200G/lane and 1.6T the balance tips toward LRO: early 1.6T LPO parts draw more than 30 W, a thermal problem at faceplate density (<a href="#sec:thermal-envelope" data-reference-type="ref+Label" data-reference="sec:thermal-envelope">9.13.1</a>), while a transmit-DSP LRO design promises under 20 W with easier integration and interop . Cignal notes that every vendor showing 1.6T LPO at OFC also showed an LRO part . That matches the book’s technical read: LPO and LRO win where the host electrical channel and TDECQ close without the module DSP, and lose where they do not (<a href="#sec:224g-deploy,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:conditioning">[sec:224g-deploy,sec:conditioning]</a>).

## Emerging link styles

The form-factor list above is the present. The industry argument for 2025–26 is where the DSP and the laser should live next. Retimed pluggables remain the interop default: a module DSP cleans the electrical channel, at the cost of watts. LPO and LRO delete or slim that DSP so the host SerDes carries more of the EQ burden, which is attractive for AI power budgets and painful for margin and interop. CPO moves the optical engine onto the switch or XPU substrate to cut electrical reach, and usually keeps the laser external and field-replaceable (ELSFP/CW-WDM). XPO appeared in 2026 as a middle path: a much larger, liquid-cooled pluggable that keeps front-panel serviceability while pushing density toward CPO territory (<a href="#sec:xpo" data-reference-type="ref+Label" data-reference="sec:xpo">9.11</a>). The rest of this chapter treats electrical reach, eye budgets, and vendor CPO programs as consequences of that argument.

## The electrical link: reach, conditioning, and the eye budget

Every form factor above is really an answer to one physical question: *how far can the electrical signal travel before it is cheaper (in power and dB) to convert to light?* As the per-lane rate climbs, that distance collapses, and it is what pushes the optics from the faceplate toward the die.

**Trace loss scales with frequency.** A PCB stripline’s insertion loss grows roughly with $`\sqrt{f}`$ (skin effect) plus a dielectric term linear in $`f`$, so it is quoted per inch *at the Nyquist frequency*. Going from 112G to 224G PAM4 moves Nyquist from 28 GHz to 56 GHz, and the loss per inch roughly doubles. Recent 224G board studies measure $`\approx2.8`$ dB/inch for regular stripline and $`\approx1.9`$ dB/inch with skip-layer routing at 56 GHz, against a next-generation *target* of 1 dB/inch that demands ultra-low-loss dielectric, HVLP copper, and short via stubs . <a href="#fig:traceloss" data-reference-type="ref+Label" data-reference="fig:traceloss">9.2</a> shows the consequence: at a fixed PCB-trace budget, doubling the baud rate roughly halves the copper reach.

<figure id="fig:traceloss" data-latex-placement="ht">
<embed src="figures/fig_trace_loss.pdf" />
<figcaption>PCB trace insertion loss versus length at each rate’s Nyquist. The reach to a fixed budget shrinks from <span class="math inline">∼ 10</span> inches (112G) to a few inches (224G), which is why the optical conversion must move closer to the ASIC.<span id="fig:traceloss" data-label="fig:traceloss"></span></figcaption>
</figure>

**The CEI channel classes name the reaches.** OIF’s Common Electrical I/O project defines the electrical link budgets the whole industry designs to. <a href="#tab:cei224-reach" data-reference-type="ref+Label" data-reference="tab:cei224-reach">3.8</a> is the CEI-224G lookup card (XSR / VSR / MR / LR, plus Linear for DSP-less modules); the reach map is <a href="#fig:cei-reach-map" data-reference-type="ref+Label" data-reference="fig:cei-reach-map">3.5</a>. At 56 GHz Nyquist the same names mean much shorter copper than at 112G :

XSR  
*XSR*: die-to-die / die-to-engine: the shortest, lowest-power tier, the one CPO and chiplet optics live in ($`\lesssim`$<!-- -->50 mm package).

VSR  
*VSR*: chip-to-module: $`\approx`$<!-- -->200 mm of host plus 20 mm of module and one connector: the classic pluggable channel.

MR  
*MR*: chip-to-chip across a board: $`\approx`$<!-- -->500 mm, one connector, $`\sim`$<!-- -->32–34 dB die-to-die.

LR  
*LR*: backplane or copper cable: $`\approx`$<!-- -->1000 mm of host and daughter cards, two connectors, up to $`\sim`$<!-- -->40 dB die-to-die (including a 1 m cable).

Linear  
*CEI-224G-Linear*: same faceplate-class ports without a module DSP/CDR; the electrical foundation for LPO (<a href="#sec:224g-deploy,sec:pluggables" data-reference-type="ref+Label" data-reference="sec:224g-deploy,sec:pluggables">[sec:224g-deploy,sec:pluggables]</a>).

##### Active copper: ACC, AEC, and DAC.

Passive direct-attach copper (DAC) survives only where the reach is short: at 224G a passive DAC is good for roughly $`0.5`$–$`1`$ m (strong 224G PHYs have demonstrated 2 m). *ACC* adds redrivers (CTLE + VGA) in the cable; *AEC* adds retimers (EQ + CDR) and stretches twinax to $`\sim`$<!-- -->2.5 m at higher power (<a href="#sec:conditioning,sec:equalization" data-reference-type="ref+Label" data-reference="sec:conditioning,sec:equalization">[sec:conditioning,sec:equalization]</a>) . Beyond that, and increasingly *within* the rack for scale-up, the answer is optics (<a href="#tab:oif-scale" data-reference-type="ref+Label" data-reference="tab:oif-scale">9.1</a>).

##### Co-packaged and near-package copper: copper moves inward too.

Optics is not the only thing the reach wall pushes toward the package. *CPC* (co-packaged copper) mates a copper cable or connector directly onto the ASIC package substrate, and *NPC* (near-package copper) places that connector just outside the package on the socket. Both leave the host at the package edge and skip the lossy PCB run to the faceplate, where most of the trace budget in <a href="#fig:traceloss" data-reference-type="ref+Label" data-reference="fig:traceloss">9.2</a> is spent. The move mirrors CPO: shorten the electrical path until the channel closes, but keep the signal in copper instead of converting it to light.

On-substrate copper has been validated at 224G-PAM4 with a stated roadmap to 448G, and compression substrate connectors now target 224 Gb/s PAM4 and beyond . Inside its reach, copper keeps the properties that make it the default: a long-reach 224G SerDes into a CPC cable runs near 4 pJ/bit with no electro-optic conversion, adds less latency than a retimed optical hop, and costs less per lane. Passive co-packaged copper reaches about a meter at 448G-PAM4 under optimistic connector assumptions (<a href="#sec:448g" data-reference-type="ref+Label" data-reference="sec:448g">3.14.3</a>), enough to cover many scale-up links inside a rack or between adjacent racks.

Past that wall the conversion to light pays for itself. When the reach exceeds what a clean substrate channel can carry, or the port count makes copper bulk and cabling weight unmanageable, optics takes the link (<a href="#tab:oif-scale" data-reference-type="ref+Label" data-reference="tab:oif-scale">9.1</a>). CPC and NPC do not remove that crossover; they move it, buying copper one more rate generation before the optics win. Read the placement ladder in <a href="#tab:placement" data-reference-type="ref+Label" data-reference="tab:placement">9.4</a> from the copper side and this is the same trade seen in reverse.

**So the optics march inward.** Shortening the electrical path is exactly what trades power and reach for serviceability, the through-line of this chapter. <a href="#tab:placement" data-reference-type="ref+Label" data-reference="tab:placement">9.4</a> lays out the ladder from faceplate to interposer.

<span id="tab:placement" data-label="tab:placement"></span>

| Placement | Host electrical reach | Energy/bit | Serviceability |
|:---|:---|:---|:---|
| Pluggable (faceplate) | full VSR host run ($`\sim`$<!-- -->200 mm) + connector | highest ($`>`$<!-- -->30 pJ/bit w/ DSP; less for LPO) | hot-swap at faceplate (best) |
| On-board optics (OBO / COBO) | shorter mid-board trace | lower | board-level (solder/socket); largely bypassed for CPO |
| Near-packaged (NPO) | engine beside the ASIC on substrate | lower still | module on substrate; limited |
| Co-packaged (CPO) | mm-scale die-to-engine (XSR) | $`<`$<!-- -->5 pJ/bit | soldered; ELSFP lasers field-replaceable |
| Optical I/O on interposer | on-die / interposer | $`<`$<!-- -->2 pJ/bit | not field-serviceable (emerging) |

**Table .** The optics-placement ladder. Moving the electro-optic conversion inward cuts trace loss and energy per bit but erodes field serviceability, the central tension behind pluggables, OBO/NPO, CPO (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>), and the XPO middle ground (<a href="#sec:xpo" data-reference-type="ref+Label" data-reference="sec:xpo">9.11</a>). A mid-board fiber connector can shift breakage risk from the costly engine to a cheap jumper.

**On-board optics: the step the industry mostly skipped.** OBO (standardized by the *Consortium for On-Board Optics*, COBO) moves the optical engine off the faceplate and onto the main PCB, cutting the copper run without abandoning silicon photonics . It works, but it gives up hot-plug serviceability while only partly closing the power gap, so with CPO maturing, most hyperscalers are leapfrog­ping OBO/NPO straight to co-packaging, keeping serviceability via field-replaceable lasers (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>) and the XPO pluggable hedge (<a href="#sec:xpo" data-reference-type="ref+Label" data-reference="sec:xpo">9.11</a>).

**The die-to-die interface is a standard too.** At the innermost tier (<a href="#tab:placement" data-reference-type="ref+Label" data-reference="tab:placement">9.4</a>), the electrical hand-off between chiplets is increasingly set by *UCIe* (Universal Chiplet Interconnect Express), an open die-to-die interconnect whose 2.0 revision (August 2024) added 3D packaging and in-field manageability, with a 3.0 revision roughly doubling bandwidth in 2025 . UCIe is the parallel counterpart to CEI XSR: XSR is a serial die-to-OE link, while UCIe carries wide parallel lanes across a package or interposer. It reaches optics because co-packaged engines and optical-I/O chiplets attach to the compute die over a UCIe port, and optical-UCIe proposals aim to carry that traffic over fiber instead of a few millimeters of substrate. The chiplet-protocol and packaging detail sits outside this book’s scope; the point for short reach is that the die-to-die interface, copper or optical, sets the shortest reach an optical engine must beat.

### Reshaping, retiming, and where the DSP lives

To survive that lossy channel the signal is conditioned at several points (<a href="#sec:equalization" data-reference-type="ref+Label" data-reference="sec:equalization">3.6</a>), and it helps to keep two device classes distinct.[^19]

Redriver  
an analog *reshaper/amplifier*: a *CTLE* plus a VGA. It sharpens and boosts the eye but has *no* clock recovery, so it cannot reset accumulated jitter; it adds almost no latency. This is the active element in active copper cables (ACC) and on host boards used to stretch a marginal trace.

Retimer  
adaptive EQ *plus* a *CDR* that re-samples and regenerates the data. It breaks the channel into independent jitter/loss segments, at the cost of power and per-hop latency. Retimers sit in active electrical cables (AEC) and in fully retimed modules (Broadcom’s Agera is a host retimer).

Inside the optical module the traditional “cleanup” is a full DSP (retimer $`+`$ FEC engine). The retimed-to-linear spectrum trades exactly cleanup for power and latency:

Fully retimed  
DSPs in both directions: least sensitive to *ISI*/dispersion, but highest power ($`\sim`$<!-- -->14–18 W/module at 800G) and most latency ($`\sim`$<!-- -->8–10 ns/hop).

LPO (linear)  
*LPO*: *no* DSP or CDR in either direction: only a CTLE in the TIA and a linear driver, so the host SerDes must do all the *FFE*/CTLE equalization *and* carry the FEC. Lowest power ($`\sim`$<!-- -->7–9 W), lowest latency ($`<`$<!-- -->3 ns), but most ISI/dispersion-sensitive and shortest reach ($`<`$<!-- -->2 km) .

LRO / TRO (retimed TX, linear RX)  
DSP only on the electrical$`\to`$optical path, roughly half the power, sensitivity, and latency, with easier interop.

So yes: reshapers/amplifiers (redrivers) and retimers are routinely placed on the host path, and the module’s own DSP is the last line of cleanup. The entire LPO bet (<a href="#sec:power,sec:224g-deploy" data-reference-type="ref+Label" data-reference="sec:power,sec:224g-deploy">[sec:power,sec:224g-deploy]</a>) is to *delete* those active stages and let the host SerDes’ CTLE/FFE carry the channel, trading electrical margin for power and latency.

### The electrical eye: acceptable voltage and noise

What must the signal actually look like where it hands off to the module? The CEI-224G reference and draft numbers set the envelope . Differential swing sits roughly in the 0.36–1.05 V<sub>ppd</sub> band (reference TX near 1 V peak-to-peak differential; lossier channels use the larger swing). Transmitter *SNDR* ($`\mathrm{SNR_{TX}}`$) is about 33 dB: the transmitter’s own noise-plus-distortion ceiling. PAM4 level uniformity needs $`\mathrm{RLM}\ge0.95`$ (1.0 = perfectly even eyes). Jitter budgets are tight: random $`\approx`$<!-- -->0.01 *UI* rms and bounded/uncorrelated $`\approx`$<!-- -->0.02 UI pk. The go/no-go metric that folds those pieces together is *COM* (channel operating margin) $`\ge3`$ dB: a statistical SNR of the fully equalized link (<a href="#sec:com" data-reference-type="ref+Label" data-reference="sec:com">9.5.2.0.2</a>).

##### Jitter and level uniformity.

At 112 GBd, 1 UI $`\approx`$<!-- -->8.9 ps; 0.01 UI rms jitter is $`\sim`$<!-- -->90 fs rms. Random jitter adds vertical eye closure; deterministic jitter (ISI, crosstalk) shows up in bathtub curves and COM. *RLM* $`\ge0.95`$ keeps the three PAM4 eyes even; poor RLM wastes vertical margin the same way excess TDECQ does on the optical side (<a href="#sec:tdecq" data-reference-type="ref+Label" data-reference="sec:tdecq">7.3</a>).

Retimers reset jitter per segment; redrivers do not. That is why long ACC chains accumulate timing budget stress while AEC segments stay independent (<a href="#sec:active-cables,sec:conditioning" data-reference-type="ref+Label" data-reference="sec:active-cables,sec:conditioning">[sec:active-cables,sec:conditioning]</a>).

Here is the number that reframes “acceptable noise.” After the reference receiver’s equalizer (an 8-tap *DFE*), the eye at the slicer is only about $`4`$–$`10`$ mV tall and $`\sim`$<!-- -->0.06 UI wide, with $`\sim`$<!-- -->11–14 dB of vertical eye closure, at a *pre-FEC* error rate near $`10^{-4}`$. The channel is deliberately driven deep into ISI and closed nearly shut; *KP4* FEC (pre-FEC $`2.4\times
10^{-4}`$ to post-FEC $`10^{-15}`$, <a href="#ch:models" data-reference-type="ref+Label" data-reference="ch:models">4</a>) is what turns that into a working link. “Acceptable,” then, is not a clean open eye; it is whatever keeps COM $`\ge3`$ dB and the pre-FEC BER under the KP4 threshold. It is also why the optics must present a clean, highly linear interface, especially for LPO: with only a few mV of margin, any added noise or nonlinearity from the driver or TIA comes straight off COM.

##### Channel operating margin (COM) in one page.

*COM* is the electrical go/no-go statistic for CEI-class channels: after the reference transmitter, channel, and receiver (CTLE + 8-tap DFE) are applied, COM is the SNR margin at the slicer, in dB. COM $`\ge3`$ dB is the usual pass line (<a href="#sec:eye-budget,sec:equalization" data-reference-type="ref+Label" data-reference="sec:eye-budget,sec:equalization">[sec:eye-budget,sec:equalization]</a>).

COM connects directly to optics because the module is the last analog segment before FEC. A retimed module can absorb some host-channel sin; LPO cannot (<a href="#sec:pluggables,sec:drivers" data-reference-type="ref+Label" data-reference="sec:pluggables,sec:drivers">[sec:pluggables,sec:drivers]</a>). When COM is tight, debug in this order: host TX SNDR and RLM, connector return loss, equalizer tap saturation, then module input swing and TIA noise (<a href="#sec:pd-tia,ch:models" data-reference-type="ref+Label" data-reference="sec:pd-tia,ch:models">[sec:pd-tia,ch:models]</a>).

Optical-side analogs are not identical: TDECQ scores the transmitter with a reference equalizer; SECQ stresses the receiver (<a href="#sec:tdecq,sec:secq" data-reference-type="ref+Label" data-reference="sec:tdecq,sec:secq">[sec:tdecq,sec:secq]</a>). Think of COM as the *electrical* counterpart to those optical margin tests.

**Key idea.** Electrical reach is the hidden clock behind form factors. Trace loss per inch roughly doubles from 112G (28 GHz) to 224G (56 GHz), collapsing copper reach to a few inches on-board and $`\sim`$<!-- -->1 m in cable. Each step inward (pluggable, OBO, NPO, CPO, on-interposer optical I/O) buys power and reach and spends serviceability. The signal is held together by redrivers (reshape), retimers (reclock), and DSPs (both), which LPO deletes, inside a brutal budget: $`\sim`$<!-- -->1 V<sub>ppd</sub> in, 33 dB TX SNDR, COM $`\ge3`$ dB, and a post-equalizer eye of only a few mV rescued by FEC.

## The two phases of inference, revisited

<a href="#ch:role" data-reference-type="ref+Label" data-reference="ch:role">1</a> introduced prefill and decode; here is why they matter for the network.

Prefill  
compute-bound and highly parallel: crunches the whole prompt through every layer at once.

Decode  
memory-bandwidth-bound and autoregressive: one token at a time, streaming all weights each step. The *KV cache* (scaling with batch $`\times`$ context length) is a major and growing memory consumer.

**Why decode is memory-bandwidth-bound.** It comes down to *arithmetic intensity*, FLOPs performed per byte read from memory. Each weight matrix $`W\in\mathbb{R}^{d_\text{out}\times d_\text{in}}`$ costs $`d_\text{out}d_\text{in}`$ parameters to read. In decode you generate one token, so every layer is a matrix–*vector* product (GEMV): about $`2\,d_\text{out}
d_\text{in}`$ FLOPs against $`2\,d_\text{out}d_\text{in}`$ bytes of FP16 weights, i.e. each weight is used once and discarded:
``` math
\text{AI}_\text{decode}\;\approx\;
\frac{2\,d_\text{out}d_\text{in}}{2\,d_\text{out}d_\text{in}}
\;=\;1\ \text{FLOP/byte}.
```
Prefill instead pushes $`N`$ prompt tokens through the *same* weights at once, a matrix–matrix product (GEMM) that reuses each loaded weight $`N`$ times, so $`\text{AI}_\text{prefill}\approx N`$ FLOP/byte. On a roofline this is decisive: an H100 delivers $`\sim`$<!-- -->1000 TFLOP/s FP16 on $`\sim`$<!-- -->3.35 TB/s of HBM, so its balance point sits at
``` math
\frac{1000\times10^{12}}{3.35\times10^{12}}\;\approx\;300\ \text{FLOP/byte}.
```
Decode at $`\sim`$<!-- -->1 FLOP/byte runs $`\sim`$<!-- -->300$`\times`$ *below* that ridge (under 1% of peak FLOPs) so token rate is set by $`\text{HBM bandwidth}/\text{model bytes}`$, not by compute . Two effects compound it: the full weight set must be streamed from HBM *per token*, and attention re-reads the KV cache every step, with traffic that grows with context length.

**Batching couples latency and throughput.** Larger batches amortize the weight-streaming cost (better throughput and energy per token) but make each individual response wait (worse latency). Squeezing both at once is a central goal of an inference platform.

**Sharding puts the network on the critical path.** Because frontier models (especially mixture-of-experts) are sharded across many accelerators, each token triggers collectives: all-reduce for tensor parallelism, all-to-all for expert routing, point-to-point for pipeline stages. For MoE all-to-all in particular, interconnect bandwidth and tail latency can dominate. This is the concrete reason hyperscale inference platforms balance “compute, memory, and networking.”

| Phase       | Bottleneck       | Network role                          |
|:------------|:-----------------|:--------------------------------------|
| Prefill     | compute          | moderate (parallel)                   |
| Decode      | memory bandwidth | high for sharded models (collectives) |
| MoE routing | interconnect     | dominant (all-to-all)                 |

Where optics fits the inference bottlenecks. {#tab:inference}

## Collective communication and optics demand

Once a model is sharded across many accelerators, the network stops carrying only point-to-point streams. Training and large inference jobs spend a large fraction of wall time in *collective* patterns: all-reduce for tensor-parallel layers, all-to-all for MoE expert routing, and steadier point-to-point streams for pipeline stages. Those patterns set optical requirements even when the PHY still looks like ordinary Ethernet or InfiniBand.

All-reduce  
tensor-parallel layers sum partial results across a group; needs high bisection bandwidth and low latency; latency sensitive at small message sizes (decode).

All-to-all  
MoE expert routing sends tokens to remote experts; bandwidth dominates; tail latency spikes if any link in the pod is slow (<a href="#tab:inference" data-reference-type="ref+Label" data-reference="tab:inference">9.5</a>).

Point-to-point  
pipeline parallelism moves activations between stages; steady streams rather than global sync.

Optical engineering maps to these patterns indirectly. More rails and higher per-lane rate cut time spent in collectives; CPO/XPO raise faceplate bandwidth so fewer hops are needed (<a href="#sec:cpo-status,sec:xpo,sec:topologies" data-reference-type="ref+Label" data-reference="sec:cpo-status,sec:xpo,sec:topologies">[sec:cpo-status,sec:xpo,sec:topologies]</a>). Protocol choice (UEC vs IB) sets lossless delivery and congestion behavior (<a href="#sec:fabric-protocols" data-reference-type="ref+Label" data-reference="sec:fabric-protocols">9.8</a>), but the PHY job remains the same: deliver pre-FEC BER below KP4 at the lowest pJ/bit (<a href="#sec:power,sec:kp4" data-reference-type="ref+Label" data-reference="sec:power,sec:kp4">[sec:power,sec:kp4]</a>). The next section names the fabric stacks that carry those collectives; the sections after that show where the optics physically sit.

## Fabric options

InfiniBand, Ethernet, and the Ultra Ethernet Consortium’s AI-tuned Ethernet are the scale-out contenders. Momentum in 2025–26 favors open Ethernet for AI; large vertical AI stacks commonly use Broadcom Tomahawk switch silicon (<a href="#ch:role,sec:cpo-status" data-reference-type="ref+Label" data-reference="ch:role,sec:cpo-status">[ch:role,sec:cpo-status]</a>).

InfiniBand / NVLink fabric  
lossless, RDMA-native; NVIDIA Quantum switches; strong in closed NVIDIA stacks; CPO photonics on Quantum-X (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>).

RoCEv2 Ethernet  
RDMA over converged Ethernet; widely deployed; competes on congestion control and tail latency versus IB.

Ultra Ethernet (UEC)  
UET transport, enhanced PHY, congestion control aimed at AI collectives (<a href="#tab:sdo-map" data-reference-type="ref+Label" data-reference="tab:sdo-map">9.2</a>). PHY work tracks 400G/lane class electrical and optical I/O.

Collectives (all-reduce, all-to-all for MoE) sit on this fabric (<a href="#sec:inference-bottlenecks" data-reference-type="ref+Label" data-reference="sec:inference-bottlenecks">9.6</a>). The optical job is raw bandwidth and predictable latency at $`\sim`$<!-- -->200–400G per lane, not long-haul reach.

## Optical circuit switching

The fabric options above are all *packet* switches: every link terminates in a switch ASIC that turns light into electrons, reads the header, and turns it back into light for the next hop. That O-E-O conversion is where much of a fabric’s power and latency goes (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>), and at $`10^5`$-plus endpoints it repeats at every tier. An *optical circuit switch* does a different job. It is a Layer-1 switch that steers light from an input fiber to an output fiber with no O-E-O conversion, so it is transparent to bit rate, modulation format, and wavelength. The same switch that passes 200 Gb/s PAM4 today passes 448G or a full WDM comb tomorrow with no change (<a href="#ch:wdm,sec:224g" data-reference-type="ref+Label" data-reference="ch:wdm,sec:224g">[ch:wdm,sec:224g]</a>).

Transparency is the point, and also the limit. Because an OCS never looks at a packet, it cannot buffer, arbitrate, or route per packet. It sets up a *circuit*: a fixed light path held open as long as the topology needs it. The mirrors or waveguides that steer the light reconfigure in milliseconds, far slower than a packet time, so an OCS reshapes the *topology* between jobs or around failures, not the traffic inside a job. In return it deletes a whole tier of packet switches and their pluggable optics, along with the power, cost, and FIT that tier carried (<a href="#sec:topologies,ch:reliability" data-reference-type="ref+Label" data-reference="sec:topologies,ch:reliability">[sec:topologies,ch:reliability]</a>).

##### The device and its parameters.

Most production OCS today is free-space: a fiber-collimator array launches beams onto a two-axis MEMS mirror array, and each mirror tilts to aim its beam at the chosen output collimator. <a href="#tab:ocs-tech" data-reference-type="ref+Label" data-reference="tab:ocs-tech">9.6</a> lists the main technologies. For an optics engineer the parameters that matter are the ones that land in the link budget and the fleet model.

Insertion loss  
a hop through the switch costs roughly 2 dB, straight off the optical budget (<a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>). Higher launch power or better receiver sensitivity has to cover it (<a href="#ch:lasers,sec:sensitivity" data-reference-type="ref+Label" data-reference="ch:lasers,sec:sensitivity">[ch:lasers,sec:sensitivity]</a>).

Radix  
how many fibers the switch connects. Production MEMS OCS runs about $`136\times136`$; circulators reuse each port in both directions and so double the effective radix (below).

Reconfiguration time  
milliseconds for MEMS, which fixes OCS as a topology switch. Silicon-photonic and SOA switches reach nanoseconds, but at low radix and higher loss (<a href="#tab:ocs-tech" data-reference-type="ref+Label" data-reference="tab:ocs-tech">9.6</a>).

Crosstalk, return loss, polarization  
a mirror that leaks light into the wrong port is crosstalk; a reflective interface raises ORL and feeds laser RIN (<a href="#sec:optical-channel,sec:rin" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:rin">[sec:optical-channel,sec:rin]</a>). Free-space paths are largely polarization-insensitive, which suits IM/DD.

<span id="tab:ocs-tech" data-label="tab:ocs-tech"></span>

| Technology | Switching | Insertion loss | Radix | Where it fits |
|:---|:---|:---|:---|:---|
| MEMS mirror array (free-space) | ms | $`\sim`$<!-- -->1–3 dB | 100s ($`136\times136`$ shipping) | DC fabric and AI-pod topology reconfiguration |
| Piezoelectric beam steering | ms | low–moderate | 10s–100s | free-space alternative to MEMS |
| Liquid crystal (LCoS) | ms | moderate | wavelength-selective | wavelength add/drop, WSS roles |
| 3D robotic fiber | seconds–minutes | $`\sim`$<!-- -->0.5 dB | 1000s | automated patch and provisioning, not per-job |
| Silicon photonic (MZI / SOA) | ns–$`\mu`$s | higher (integrated) | 10s | fast, low-radix; research and niche |

**Table .** OCS technologies. Free-space MEMS switches dominate AI deployments today; robotic-fiber switches trade speed for radix and very low loss; integrated photonic switches trade radix and loss for nanosecond speed.

##### What it buys at fleet scale.

Google’s Jupiter datacenter fabric replaced a patch-panel Clos interconnect with a layer of MEMS OCS under software-defined control, and reported roughly 30% lower capex, 41% lower power, and 3x faster fabric reconfiguration while a direct-connect topology carried the same production traffic . The switch, Palomar, is a $`136\times136`$ MEMS OCS with about 2 dB insertion loss and millisecond switching, and circulators realize bidirectional links through it to double the effective radix . The same building block reshapes AI pods: a TPU v4 pod wires 4096 accelerators through 48 OCS into a 3D torus that reconfigures per job and routes around failed racks, so a dead node becomes a topology the scheduler works around instead of a pod-wide outage . That reconfiguration is the fabric-reliability lever <a href="#ch:reliability" data-reference-type="ref+Label" data-reference="ch:reliability">8</a> points at: component FIT still applies, but the fabric survives each failure by re-wiring optically rather than stalling the job.

##### What OCS asks of the transceivers.

An OCS layer changes the module spec in ways this book cares about. Because the switch adds a fixed loss and is wavelength-transparent, single-fiber duplex reaches (FR, one fiber each way) fit an OCS better than parallel-fiber reaches (DR, many fibers), so an OCS deployment pulls the plant toward FR optics and toward circulators for bidirectional operation on one fiber . The insertion loss argues for higher launch power and tighter ORL budgets, since every mated interface and mirror is a reflection the laser sees (<a href="#sec:optical-channel,sec:rin-values" data-reference-type="ref+Label" data-reference="sec:optical-channel,sec:rin-values">[sec:optical-channel,sec:rin-values]</a>). Wavelength transparency means a WDM link passes through the switch unchanged, so CW-WDM and ring-based engines (<a href="#ch:wdm,sec:cwwdm" data-reference-type="ref+Label" data-reference="ch:wdm,sec:cwwdm">[ch:wdm,sec:cwwdm]</a>) compose with an OCS without a translation layer. None of this is exotic optics; it is the same DR/FR PMD and laser work from earlier chapters (<a href="#sec:pmd-reach,ch:lasers" data-reference-type="ref+Label" data-reference="sec:pmd-reach,ch:lasers">[sec:pmd-reach,ch:lasers]</a>), specified against a channel that now includes a switch.

##### Status and where it sits next to CPO.

By 2025–26 OCS moved from a Google-specific technique to an industry theme, a headline topic at OFC 2026 with MEMS, piezoelectric, liquid-crystal, robotic-fiber, and silicon-photonic approaches competing on radix, loss, speed, and reliability . It complements co-packaged optics rather than competing with it: CPO shortens the electrical path at the switch package (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>), while OCS removes packet-switch hops between packages and racks. A fabric can use both, CPO optics feeding an OCS layer, and the reliability question for each is the one <a href="#ch:validation,ch:reliability" data-reference-type="ref+Label" data-reference="ch:validation,ch:reliability">[ch:validation,ch:reliability]</a> keeps returning to.

**Key idea.** An optical circuit switch reroutes light at Layer 1 with no O-E-O conversion, so it is transparent to rate, format, and wavelength and adds only insertion loss to the link budget. Millisecond MEMS switching makes it a topology and failure-reroute switch, not a packet switch. It buys fabric power, cost, and resilience (Google Jupiter and the TPU pods are the production proof), and it pulls the transceiver plant toward FR optics, circulators, and higher launch power. OCS and CPO are complementary bets on the same power and reliability problem.

## Co-packaged optics: 2025–26 status

By 2025–26, co-packaged optics crossed from demonstrations into shipping products, pushed by the power and reliability limits of pluggables in AI scale-out. The programs converge on a common recipe: a photonic engine co-packaged with the switch ASIC, 200 Gb/s per channel, microring modulators (<a href="#sec:siring" data-reference-type="ref+Label" data-reference="sec:siring">3.14.3.0.6</a>), *field-replaceable* lasers pulled out of the package, and TSMC COUPE packaging underneath.

### Broadcom Tomahawk and CPO

Broadcom entered CPO earlier than most switch vendors and treated it as a product line, not a one-off demo. The current flagship is *Tomahawk 6*, a 102.4 Tb/s single-chip Ethernet switch (shipping 2025) offered with either copper or co-packaged optics, on 100G/200G SerDes.[^20] The CPO variant, *TH6-Davisson*, began shipping in October 2025 as Broadcom’s *third-generation* CPO switch. The public numbers sketch the architecture:

- 102.4 Tb/s optically enabled, built from sixteen 6.4 Tb/s “Davisson DR” optical engines at 200 Gb/s per channel.

- Photonic engines fabricated with *TSMC COUPE*; 64 Condor 3 nm SerDes cores (eight 212.5 Gb/s PAM4 lanes each).

- About 70% lower optical-interconnect power than pluggables.

- *Field-replaceable ELSFP laser modules*: lasers, the highest-failure component, made serviceable in the field.

- Scale-up to 512 XPUs; 100,000+ XPUs in a two-tier fabric at 200 Gb/s/link.

The lineage matters: CPO shipped on Tomahawk 4 and the second-generation *TH5-Bailly* (51.2 Tb/s), which logged “millions of hours” of reliability testing before Davisson. A fourth generation at 400 Gb/s per channel is already in development.

### NVIDIA

NVIDIA’s CPO story is the scale-up and scale-out fabric vendor converging on the same TSMC COUPE + microring recipe as Broadcom, announced as product families at GTC 2025: *Quantum-X* (InfiniBand) and *Spectrum-X* (Ethernet) Photonics switches, 200G SerDes, 1.6 Tb/s ports. Headline marketing claims include 3.5$`\times`$ power efficiency, *4$`\times`$ fewer lasers*, and large resiliency gains versus pluggables; treat those as vendor orientation, and validate against your own FIT and power model.

- *Quantum-X InfiniBand*: 144 ports of 800G ($`\approx`$<!-- -->115 Tb/s), liquid-cooled; available late 2025. Each package integrates eighteen silicon-photonics engines fed by 36 laser inputs through six *detachable* optical sub-assemblies.

- *Spectrum-X Ethernet*: up to 409.6 Tb/s; available in 2H 2026.

- Ecosystem: lasers from Lumentum, silicon photonics with Coherent, packaging with TSMC.

### TSMC COUPE (the shared foundation)

*COUPE* (Compact Universal Photonic Engine) stacks an electronic IC on a photonic IC via SoIC-X hybrid bonding (a 6 nm EIC on a 65 nm SOI PIC), giving a low-impedance die-to-die interface. The roadmap: pluggable qualification in 2025, CoWoS-based CPO integration and *mass production in 2026*, with 800G/1.6T engines now and 3.2T/6.4T (toward 12.8 Tb/s on-package) to follow. TSMC cites the energy-per-bit trajectory from $`>`$<!-- -->30 pJ/bit for copper toward $`<`$<!-- -->5 pJ/bit for CPO on substrate and $`<`$<!-- -->2 pJ/bit once optical I/O moves onto the interposer (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>). The hard problems it names (wafer-level test, fiber-array-unit integration, and high-speed optical packaging assembly) are exactly the validation and manufacturing challenges of <a href="#ch:validation,ch:reliability" data-reference-type="ref+Label" data-reference="ch:validation,ch:reliability">[ch:validation,ch:reliability]</a>.

<span id="tab:cpo-programs" data-label="tab:cpo-programs"></span>

| Program | Technology | Status |
|:---|:---|:---|
| Broadcom TH6-Davisson | 102.4 Tb/s, 200G/ch, COUPE, ELSFP lasers | 3rd-gen CPO, shipping Oct 2025 |
| Broadcom TH5-Bailly | 51.2 Tb/s CPO | 2nd-gen, extensively field-tested |
| NVIDIA Quantum-X (IB) | 144$`\times`$<!-- -->800G, MRM, COUPE, detachable lasers | available late 2025 |
| NVIDIA Spectrum-X (Enet) | up to 409.6 Tb/s, MRM, COUPE | 2H 2026 |
| TSMC COUPE | SoIC-X EIC-on-PIC packaging | mass production 2026 |
| Samsung (foundry) | optical engines / turnkey CPO | OE 2027, CPO 2029 |
| Ayar Labs | TeraPHY optical I/O + SuperNova CW-WDM source | merchant scale-up optical I/O |

**Table .** CPO programs, 2025–26.

**Key idea.** The 2025–26 CPO wave shares one architecture: 200G/lane microring engines on TSMC COUPE, with field-replaceable lasers because lasers fail first. Tomahawk-class CPO at 200G/lane makes IM/DD validation and ELSFP laser reliability direct gates on how many accelerators a pod can wire together dependably.

## The serviceable-density middle ground: XPO (OFC 2026)

CPO buys density and power at a cost the operator feels: the optics are soldered to the switch, so a single failed engine can mean pulling the whole line card. That tension (pluggable serviceability versus co-packaged density) defined much of *OFC 2026*, where a third path drew the most attention.

Arista, with Coherent, Marvell, Lightmatter, and a broad partner list, launched the *XPO* (eXtra-dense Pluggable Optics) multi-source agreement. The bet is to keep the front-panel pluggable form factor (slide a module out, snap a new one in) while closing most of the density and power gap to CPO:

- **12.8 Tb/s per module**: 64 electrical lanes at 200 Gb/s PAM4 (with a roadmap to 400 Gb/s lanes for 25.6 Tb/s), roughly $`4\times`$ the density of a 1.6T-OSFP pluggable.

- **204.8 Tb/s per OCP rack unit**, from up to sixteen modules, front-panel density approaching co-packaged designs.

- **Integrated liquid-cooled cold plate** rated for 400 W+ per module, with blind-mate dripless quick-disconnects; this, not the connector, is what makes the high per-module power serviceable.

- **Universal reach and interface**: SR/DR/FR/LR plus ZR/ZR+, and fully-retimed, half-retimed, or linear (LPO/LRO) optics in one form factor.

<span id="tab:xpo-compare" data-label="tab:xpo-compare"></span>

| Attribute | Retimed / LPO pluggable | XPO | CPO |
|:---|:---|:---|:---|
| Capacity | 0.8–1.6 Tb/s/module | 12.8 Tb/s/module | 100+ Tb/s on-package |
| Density | baseline | $`\sim`$<!-- -->4$`\times`$ (204.8 Tb/s per RU) | highest |
| Power path | full electrical run to faceplate | short run to dense faceplate | shortest (on substrate) |
| Cooling | air (or LPO savings) | integrated cold plate, 400 W+ | switch-package liquid cooling |
| Serviceability | field-replaceable (best) | field-replaceable (slide-out) | soldered; ELSFP lasers replaceable |
| Energy/bit | highest | intermediate | lowest ($`<`$<!-- -->5, then $`<`$<!-- -->2 pJ/bit) |
| Maturity | shipping | MSA launched OFC 2026 | shipping (Broadcom, NVIDIA) |

**Table .** Where XPO sits between pluggables and co-packaged optics.

[^21]

**The broader OFC 2026 picture.** XPO landed inside a clear consensus: 1.6T transceivers went mainstream and 3.2T (400G/lane) previews appeared, with initial demos expected around 2027; CPO moved from demo to imminent, with new MSAs (Open CPX, “socketed CPO”) blurring the pluggable/co-packaged line; and hollow-core fiber (record loss now $`\sim`$<!-- -->0.091 dB/km) advanced toward low-latency intra-datacenter use (<a href="#sec:hcf" data-reference-type="ref+Label" data-reference="sec:hcf">9.12.1</a>). The through-line is the one this book opened with: rising per-lane rate forcing optics closer to the silicon and squeezing every last pJ/bit.

## The latency budget

The book has a link budget in dB (<a href="#sec:link-budget" data-reference-type="ref+Label" data-reference="sec:link-budget">7.6</a>) and, next, an energy budget in pJ/bit. It needs a third ledger. Inference puts the optical link on the critical path (<a href="#sec:inference-bottlenecks" data-reference-type="ref+Label" data-reference="sec:inference-bottlenecks">9.6</a>), so you should be able to add up a link’s latency the way you add up its loss and its power. The contributors fall into two groups: fixed digital costs that do not care about distance, and a propagation term that does.

| Contributor                    | Typical latency                         |
|:-------------------------------|:----------------------------------------|
| PCS framing / serialization    | a few ns                                |
| FEC encode $`+`$ decode (KP4)  | $`\sim`$<!-- -->20–100 ns each          |
| Module DSP / retimer (per hop) | $`\sim`$<!-- -->8–10 ns (fully retimed) |
| LPO (no DSP)                   | $`<`$<!-- -->3 ns                       |
| Driver, modulator, PD, TIA     | sub-ns                                  |
| Fiber propagation (silica)     | $`\sim`$<!-- -->4.9 ns/m                |
| hollow-core fiber              | $`\sim`$<!-- -->3.3 ns/m                |
| Switch hop (O-E-O)             | $`\sim`$<!-- -->100–560 ns              |

Approximate one-way latency contributors, 200G/lane class. {#tab:latency}

**The fixed digital cost dominates a short link.** FEC is the largest single term. KP4 RS(544,514) (<a href="#sec:kp4" data-reference-type="ref+Label" data-reference="sec:kp4">3.12</a>) costs roughly 20 to 100 ns to encode and again to decode, set by the codeword length and the implementation, not the fiber . The module DSP adds another 8 to 10 ns per hop when the link is fully retimed. The analog stages, driver, modulator, photodiode, and *TIA*, together contribute well under a nanosecond of group delay and are almost never the problem. On a 10 m in-rack link the fiber itself is about 50 ns, smaller than one pass through the FEC.

**Propagation dominates only once the fabric is large.** Light in standard single-mode fiber travels at roughly $`c/1.47`$, about $`4.9`$ ns/m, because the glass has a group index near 1.47. A 100 m row-scale run is then about 490 ns, comparable to a switch hop and larger than the digital terms. Each switched tier adds an O-E-O conversion: a cut-through Ethernet switch forwards in a few hundred nanoseconds ($`\sim`$<!-- -->560 ns for an 800GbE class device), while InfiniBand reaches under 100 ns per hop . Across a multi-tier scale-out fabric, the switch hops and their conversions, not the fiber, set the tail latency that stalls a collective (<a href="#sec:inference-bottlenecks" data-reference-type="ref+Label" data-reference="sec:inference-bottlenecks">9.6</a>). This is the latency argument for optical circuit switching (<a href="#sec:ocs" data-reference-type="ref+Label" data-reference="sec:ocs">9.9</a>) and for co-packaging: both remove conversions and electrical runs from the path.

**Latency is where the module architecture shows up again.** The retimed-to-linear choice you met in <a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a> for power repeats here. A fully retimed module spends $`\sim`$<!-- -->8–10 ns per hop; *LRO* roughly halves that; *LPO* deletes the module DSP and lands under 3 ns . On a link with a few hops, deleting the DSP saves more time than shortening the fiber does. Latency and energy point the same way, which is why LPO and CPO are attractive for the scale-up domain where both matter most.

### Hollow-core fiber

The one distance term you can attack is the group index. Hollow-core fiber (*HCF*) guides light mostly through air rather than glass, so its group index sits near 1.0 and light travels close to vacuum speed. A double nested antiresonant nodeless fiber (*DNANF*) design reported 0.091 dB/km at 1550 nm, below the $`\sim`$<!-- -->0.14 dB/km floor that silica has held since the 1980s, and about 0.2 dB/km across a 66 THz window . The latency payoff is the headline for short reach: propagation drops from $`\sim`$<!-- -->4.9 to $`\sim`$<!-- -->3.3 ns/m, roughly 45% faster or about a third lower latency, which on a 100 m run saves $`\sim`$<!-- -->150 ns, the size of a switch hop. Microsoft reports deploying cabled HCF in the Azure network.

For short-reach IM/DD the low nonlinearity and near-zero dispersion of air guiding matter less than they do for coherent long-haul; the draw here is purely latency and, secondarily, the wider low-loss window for more wavelengths. The open problems are practical: low-loss splicing and connectorization to solid-core plant, yield at volume, and cost. These figures are recent records, so treat them as provisional.

## Energy per bit and the power wall

Frontier AI is *power-limited*: a site’s usable megawatts, not just capital, caps how much compute it can host. Every watt spent moving bits is a watt not spent on compute, and interconnect energy multiplies across a fabric with millions of links, which is why energy per bit (*pJ/bit*) has become a headline design metric.

The trajectory that CPO is chasing, per TSMC’s COUPE disclosures:

| Link style                      | Energy per bit         |
|:--------------------------------|:-----------------------|
| Conventional copper / retimed   | $`>`$<!-- -->30 pJ/bit |
| Co-packaged optics on substrate | $`<`$<!-- -->5 pJ/bit  |
| Optical I/O on the interposer   | $`<`$<!-- -->2 pJ/bit  |

Approximate interconnect energy per bit. {#tab:pjbit}

This is the quantitative reason CPO exists: removing the power-hungry electrical run between a switch ASIC and a front-panel pluggable (and the module’s retiming DSP) is roughly a $`70\%`$ cut in optical-interconnect power in Broadcom’s Davisson (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>). *LPO/LRO* attacks the same target from the pluggable side by deleting the DSP; CPO attacks it by shortening the electrical path.

**Why it compounds.** Multiply even a few pJ/bit by aggregate fabric bandwidth and link count and interconnect becomes a meaningful slice of cluster power. At a fabric moving petabits per second, a 5 pJ/bit versus 30 pJ/bit choice is megawatts, directly setting how many accelerators fit under a fixed power envelope. Laser wall-plug efficiency feeds the same budget: fewer, more efficient lasers (NVIDIA claims 4$`\times`$ fewer) cut both power and failure count at once.

**The macro trend behind the metric.** The pJ/bit fight has grid-scale stakes. US data centers drew about 176 TWh in 2023, roughly 4.4% of national electricity, up from 58 TWh in 2014; the Lawrence Berkeley National Laboratory projects 325 to 580 TWh, or 6.7 to 12% of US electricity, by 2028 . Interconnect is a growing share of that draw as lane rates climb . Every pJ/bit an LPO or CPO link removes is multiplied across that base, so interconnect power reads as an infrastructure problem, not only a per-module one.

### The thermal envelope

Every watt from the budget above turns into heat that has to leave the box, so interconnect power is also a cooling problem, and cooling sets a second ceiling beside the power wall. On a faceplate switch the optics are a large part of that heat: a 32-port 800G switch dissipates on the order of a kilowatt, and the pluggable modules account for roughly half of it . Air cooling loses headroom as per-module power climbs past the mid-teens of watts, which is why dense high-rate switches are moving to liquid and immersion cooling, and why the LPO power cut (from $`\sim`$<!-- -->14–18 W to $`\sim`$<!-- -->8 W, <a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>) reads as a thermal cut as much as an electrical one .

**Co-packaging changes the shape of the problem.** Moving the optics onto the switch substrate (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>) puts heat-sensitive optical engines a few millimeters from a high-power ASIC. Absolute temperature still matters, but the steep on-package gradient becomes the performance-limiting term: rings drift off resonance and lock loops fight neighbor heaters (<a href="#sec:thermal-xtalk" data-reference-type="ref+Label" data-reference="sec:thermal-xtalk">6.5</a>), and the laser is the least tolerant part of all . This is the thermal half of the argument for external lasers (<a href="#sec:elsfp" data-reference-type="ref+Label" data-reference="sec:elsfp">5.8</a>): holding the laser off the hot interposer at a controlled temperature protects both its wavelength and its life.

**Cooling is a reliability lever, not only a power one.** Laser wear-out follows Arrhenius kinetics (<a href="#sec:laser-aging" data-reference-type="ref+Label" data-reference="sec:laser-aging">5.7</a>): the acceleration factor is exponential in inverse junction temperature, so a few degrees of cooling buys a measurable drop in FIT and, across $`10^5`$-plus lasers, fewer failures per day (<a href="#sec:fit-example" data-reference-type="ref+Label" data-reference="sec:fit-example">5.7.0.0.4</a>). Power, cooling, and reliability are one constraint seen three ways. The link that fits under a fixed power and cooling envelope, and stays cool enough to last, is the one that scales.

**Key idea.** Energy per bit is a first-order lever on cluster size under a fixed power budget. The industry path, retimed pluggable ($`>`$<!-- -->30 pJ/bit) to LPO to CPO ($`<`$<!-- -->5, then $`<`$<!-- -->2 pJ/bit), is why “balance compute, memory, and networking” (<a href="#ch:role" data-reference-type="ref+Label" data-reference="ch:role">1</a>) is a power statement as much as a performance one.

## A first-order cost model

The book quantifies two of its three themes. Power has a ledger in pJ/bit (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>); reliability has one in FIT (<a href="#sec:fit-example" data-reference-type="ref+Label" data-reference="sec:fit-example">5.7.0.0.4</a>). Cost is invoked everywhere but never counted. It deserves the same first-order treatment, kept deliberately relative and order-of-magnitude. What follows is an illustrative model, not a price sheet: absolute module prices move too fast and vary too much by volume to write down usefully, so the numbers here are assumptions you should replace with your own.

*Total cost of ownership* (TCO) for an optical link splits into three buckets. The first is acquisition, the *bill of materials* (BOM) and the yield of optical assembly and test: laser count, whether a DSP die is present, and the packaging and coupling steps that dominate transceiver cost. The second is lifetime energy, the module’s power drawn over years and multiplied by a cooling overhead. The third is service: the failures per day implied by the fleet FIT (<a href="#sec:fit-example" data-reference-type="ref+Label" data-reference="sec:fit-example">5.7.0.0.4</a>), each one costing a replacement part and a hands-on visit. Acquisition is capital; the other two are recurring.

**Energy is the bucket you can compute.** Take an 800G module drawing $`\sim`$<!-- -->15 W fully retimed against $`\sim`$<!-- -->8 W for LPO (<a href="#sec:power" data-reference-type="ref+Label" data-reference="sec:power">9.13</a>) . Over a five-year life at \$0.10/kWh, with a *power usage effectiveness* (PUE) of $`\sim`$<!-- -->1.3 to cover cooling, the retimed module burns about 850 kWh, near \$85 of electricity; the LPO module about 460 kWh, near \$46. The $`\sim`$\$40 gap per module is a meaningful fraction of what the module itself costs, and it recurs every life cycle. Scaled up, the number stops being small: a vendor estimate puts the LPO saving on a 500,000-accelerator cluster on the order of 100 MW and roughly \$100 million a year in electricity . Treat that figure as vendor orientation, but the order of magnitude is the point.

**Recurring cost is a large share of the total.** A gigawatt-class AI site has been quoted near \$38 billion of up-front capital and roughly \$0.9 billion a year to run . Over a multi-year life the running cost is a real fraction of the capital, and interconnect power is a growing slice of it, so a pJ/bit cut reads directly as dollars saved. That estimate is an analyst breakdown, provisional, but it sets the scale: power and cost are the same argument seen through two units.

**The architecture choice moves all three buckets at once.** Per delivered Gb/s, a fully retimed pluggable carries the highest BOM (a DSP die and its packaging) and the highest power. LPO and LRO delete or relax that DSP, cutting both the BOM and $`\sim`$<!-- -->40–50% of the power , and move the cost that remains into host validation risk rather than the module. CPO and XPO remove the faceplate connector and the long electrical run and push energy under 5 pJ/bit (<a href="#tab:pjbit" data-reference-type="ref+Label" data-reference="tab:pjbit">9.10</a>), but raise assembly and test cost and couple the optics to an expensive switch ASIC, which is why the lasers are field-replaceable: a laser failure must not scrap the package (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>). Co-packaged and near-package copper is cheaper still per Gb/s wherever it reaches, carrying only the connector and the host SerDes energy (<a href="#sec:cpc-npc" data-reference-type="ref+Label" data-reference="sec:cpc-npc">9.5.0.0.2</a>); the crossover to optics is set by the reach wall, not by cost. At the fabric level, optical circuit switching is itself a cost lever: replacing a tier of O-E-O packet switches with a MEMS OCS cut capex $`\sim`$<!-- -->30% and power $`\sim`$<!-- -->41% in Google’s Jupiter (<a href="#sec:ocs" data-reference-type="ref+Label" data-reference="sec:ocs">9.9</a>) .

**Key idea.** Cost tracks power and reliability, not against them. The cheapest link per Gb/s is the one you do not light (copper within reach), then the one with the fewest active stages (LPO, then CPO), weighed against the validation risk and the failure blast radius each one adds. A pJ/bit saved is dollars saved every year the fabric runs, which is why the energy budget and the cost model point the same way.

**Key idea.** Inference is memory-bandwidth-bound in decode and interconnect-bound for sharded and MoE models, so the optical link is on the latency critical path, not just plumbing. Reliable, low-power IM/DD (and WDM) links set how large and dependable an inference fabric can grow.

# Abbreviations

This glossary is adapted from the OIF *Next Generation CEI-448G Framework* glossary (pages 7–11, OIF-FD-CEI-448G-01.0, September 2025) . Some entries include material from public reference sources noted in the original.

ADC  
An analog-to-digital converter is a system that converts an analog signal into a digital signal.

AI  
Artificial intelligence.

ACC  
Active copper cable. ACCs are a type of active copper cable used in data centers. ACCs primarily use Redriver chips and Continuous Time Linear Equalization (CTLE) to amplify and equalize the signal and provide longer reach than DACs. ACCs generally are lower power and cost than AECs (another type of active copper cable), but provide shorter reach than AECs.

AEC  
Active electrical cable. AECs are a type of active copper cable used in data centers. AECs utilize Retimer chips with Clock and Data Recovery (CDR) to reshape and retransmit signals which generally offer longer reach and better signal integrity compared to ACCs, but at a higher cost.

Application spaces  
Portions of equipment or network architecture that could benefit from having a defined set of interconnection parameters.

ASIC  
An application-specific integrated circuit is an integrated circuit (IC) customized for a particular use, rather than intended for general-purpose use.

Backplane  
A group of electrical connections used as a backbone to connect several printed circuit boards together to make up a switch, computing or storage system.

BER  
Bit error ratio is a measure of the number of bit errors that occur during data transmission, expressed as a ratio of erroneous bits to the total number of bits transmitted.

BoW  
Bunch of wires is a die-to-die interface specification. It is part of the open compute project (OCP) and, like UCIe, is used to connect chiplets within a package.

Cabled host  
An implementation where twinaxial cable is used instead of PCB traces expressly for the insertion loss benefits or 3D architecture.

CDR  
Clock and data recovery, a component that re-establishes the timing of a signal that may have degraded due to impairments on a transmission line, the retimed signal is able to continue further to its destination.

CEI  
Common Electrical IO, an OIF Implementation Agreement containing clauses defining electrical interface specifications, each optimized for various reaches at minimal power.

Coded modulation  
Coded modulation is a technique in digital communication that combines error-control coding with modulation to enhance reliability and efficiency. Its main goal is to balance bandwidth efficiency, power efficiency, and error probability.

CMIS  
Common management information specification.

CMIS-LT  
CMIS-based link training provides a message set and exchange mechanism for out-of-band link training or tuning between a pluggable module and a host.

CMIS-VCS  
CMIS versatile control set extends the base CMIS standard to allow for more advanced and flexible signal integrity (SI) capabilities.

CPC  
Co-packaged copper is an emerging interconnect technology where copper cables are directly attached to the top of an Application-Specific Integrated Circuit (ASIC) or other high-speed integrated circuit within a single package. This design minimizes the length of high-speed electrical signals on the printed circuit board (PCB) and package, addressing the limitations of traditional copper traces at increasingly high data rates (e.g., 224G and above).

CPO  
Co-packaged optics. An electrical to optical device intended to be mounted on the host package.

CTLE  
Continuous time linear equalizer.

DAC  
Direct attach copper cable. A high-speed cable assembly made of copper twinaxial cable with fixed passive transceiver modules on each end. DAC cables enable direct, electrical connections between networking devices over short distances.

DER  
Detector error ratio.

DFE  
Decision feedback equalizer. An equalizer by adding a filtered version of previous symbol estimates to the original filter output.

DSP  
Digital signal processing.

ENOB  
Effective number of bits. A measure of the dynamic performance of an analog-to-digital converter (ADC).

Faceplate  
A plate, cover, or bezel on the front of a device which may contain I/O ports.

FEC  
Forward error correction gives a receiver the ability to correct errors without needing a reverse channel to request retransmission of data.

FFE  
Feed forward equalizer.

Gbps  
Gigabits per second. The throughput or data rate of a port or piece of equipment. Gbps is $`1\times10^{9}`$ bits per second.

GBd  
The baud rate is the number of electrical transitions per second, also called symbol rate. Giga Baud is $`1\times10^{9}`$ symbols per second.

Gearbox  
A component used for managing and manipulating data streams, primarily by converting multiple serial data streams at one rate to multiple streams at another rate,

Hamming codes  
A type of linear error-correcting code used in digital communication and data storage systems. It enhances data integrity by detecting and correcting single-bit errors that may occur during transmission or storage.

HPC  
High performance compute.

HPDC  
High-performance data center. A general term for data centers designed for high-compute workloads like AI/HPC.

IA  
Implementation Agreements, what the OIF names their defined interface specifications.

IC  
Integrated circuit.

IMDD  
Intensity modulation direct detection is a method where the intensity of a light source is modulated by an electrical signal. This modulated light then travels through an optical medium (like a fiber optic cable) and is directly detected by a photo detector at the receiving end. This is a common and relatively straightforward technique for transmitting information over optical links.

I/O  
Input Output, a common name for describing a port or ports on equipment.

ISI  
Intersymbol interference.

KP4 FEC  
A specific Reed-Solomon FEC (544,514) defined in IEEE 802.3 Clause 91, commonly used in Ethernet standards.

LDPC  
A low-density parity-check code is a linear error correcting code, a method of transmitting a message over a noisy transmission channel. An LDPC is constructed using a sparse Tanner graph. LDPC codes are capacity-approaching codes.

LR  
Long reach. CEI LR specifies backplane/midplane and copper cable electrical interfaces.

LPO  
Linear pluggable optic is a technology used in optical transceivers that simplifies the design of pluggable optical modules by removing the traditional Digital Signal Processor (DSP) and Clock Data Recovery (CDR) chips. Instead, LPO utilizes a direct-drive linear approach where the signal path is considered linear, relying on the capabilities of the Application Specific Integrated Circuit (ASIC) in the host system (like a switch or Network Interface Card) to perform signal conditioning and equalization.

MCM  
Multi chip module, a specialized electronic package where multiple integrated circuits (ICs), semiconductor dies or other discrete components are packaged onto a unifying substrate, facilitating their use as a single component (as though a larger IC).

Mid-board optics  
an optical transceiver that is mounted on a PCBA away from the PCBA edge, close to a switch ASIC to reduce the amount of PCBA trace loss between an ASIC and the optical transceiver. This is in contrast to the common practice today of locating optical transceivers at the PCBA edge.

Midplane  
Some backplanes are constructed with slots for connecting to devices on both sides and are referred to as midplanes.

MLSD  
Maximum likelihood sequence detection is a mathematical algorithm to extract useful data out of a noisy data stream.

MR  
Medium reach. CEI MR specifies chip-to-chip electrical interfaces.

NG  
Next generation.

NRZ (PAM2)  
Non return to zero, a binary code in which 1s are represented by one significant condition (usually a positive voltage) and 0s are represented by some other significant condition (usually a negative voltage), with no other neutral or rest condition.

NPC  
Near-package copper. NPC uses a copper cable to bring the front panel signal to a location close to the host silicon to minimize the host PCB losses. It reduces PCB losses by bringing the signals to a connector on the PCB close to the ASIC whereas CPC (Co-packaged copper) brings the signal to a connector on the ASIC package.

NPO  
Near-package optics. Similar to CPO (Co-packaged optics) and NPC (Near-package copper), NPO is an electrical to optical device intended to be mounted on the host PCB at a location adjacent to the host silicon to minimize host PCB traces to minimize electrical signaling requirements.

OE  
Optical engine.

O-to-E and E-to-O  
Optical to electrical interface and Electrical to optical interface, a component that converts an optical signal to an electrical signal or vice versa.

PAM  
Pulse amplitude modulation, a form of signal modulation where the message information is encoded in the amplitude of a series of signal pulses. For optical links it refers to intensity modulation.

PAM4  
Pulse amplitude modulation-4 is a two-bit modulation that takes two bits at a time and maps the signal amplitude to one of four possible levels.

PAM6  
A digital signal modulation scheme that encodes information by varying the amplitude of a pulse across six distinct voltage levels. Each of these six levels can represent approximately 2.5 bits of data.

PAM8  
A digital signal modulation scheme that encodes information by varying the amplitude of a pulse across eight distinct voltage levels. Each of these eight levels can represent 3 bits of data.

PCB/PCBA  
Printed circuit board (PCB) assembly, an assembly of electrical components built on a rigid glass-reinforced epoxy-based board.

Repeater  
A low-latency electronic device that receives a signal and retransmits it. Repeaters are used to extend transmissions so that the signal can cover a longer distance. Besides signal equalization, clock and data recovery (CDR) functions could be also added to remove jitter from received signals effectively.

RoCE  
RDMA over Converged Ethernet (CE) is a network protocol which allows remote direct memory access (RDMA) over an Ethernet network.

RS  
Reed Solomon FEC coding is a type of block code. Block codes work on fixed-size blocks (packets) of bits or symbols of predetermined size. It can detect and correct multiple random and burst errors.

RTLR  
(Retimed Transmit, Linear Receive) also generically referred to as Linear receive optic (LRO), is a type of optical transceiver technology used primarily in high-speed data center and networking applications, especially within AI clusters. The RTLR naming convention is within OIF. LRO is characterized by the presence of a Digital Signal Processor (DSP) solely on the transmit path, while the receive path operates with a linear, non-retimed architecture. This differs from fully retimed optical modules that utilize DSPs on both transmit and receive paths, and also from Linear Pluggable Optics (LPO) that eliminate DSPs entirely.

Scale out  
also known as horizontal scaling, refers to the process of increasing capacity and performance by adding more individual machines or nodes to a distributed system.

Scale up  
also known as vertical scaling, refers to the process of increasing the capacity or performance of a single server or system within an AI data center by adding more resources.

SDO  
standard development organizations.

SerDes  
A Serializer/Deserializer is a pair of functional blocks commonly used in high-speed communications to transfer data over a relatively low number of lanes.

SFP  
Small form-factor pluggable connector is a modular, hot-pluggable interface used in networking devices to connect to various types of fiber optic or copper cables. It uses a PCB card edge interface.

SI  
Signal integrity is a set of measures of the quality of an electrical signal.

SNDR  
Signal-to-noise-and-distortion ratio is a measurement of the purity of a signal.

SNR  
Signal-to-noise ratio.

TBD  
To be determined.

Tbps  
Terabits per second. The throughput or data rate of a port or piece of equipment. Tbps is $`1\times10^{12}`$ bits per second.

TCM  
Trellis coded modulation is a technique that combines convolutional coding and modulation to improve data transmission efficiency over bandwidth-limited channels, like telephone lines. It achieves this by intelligently integrating the encoding and modulation processes, increasing the distance between signal points in the constellation to enhance error correction without expanding bandwidth.

TME  
Test and measurement equipment.

Twinax copper cable  
A type of copper cable similar to coaxial cable, but with two inner conductors instead of one.

UCIe  
Universal chiplet interconnect express is an open industry standard that defines the interconnect between chiplets, or small component dies, within a single package.

VLC  
Vertical line card. A new line card design in which vertical I/O connectors and ASIC are mounted side by side, reducing the signal trace distance.

VSR  
Very short reach. CEI VSR specifies chip-to-module electrical interfaces.

XSR  
Extra short reach. CEI XSR specifies die-to-optical engine (D2OE) and die-to-die (D2D) electrical interfaces.

448G  
A generic name for an expected technology enabling data rates (including overhead) of approximately 448 Gbps per lane.

ALS  
Automatic laser shutdown. A safety mechanism that cuts laser output when fiber continuity is lost. Modern systems prefer APR with automatic restart over full shutdown.

APC  
Automatic power control. A feedback loop from a monitor photodiode that holds average optical output power constant against temperature drift and aging.

APD  
Avalanche photodiode. A photodiode with internal multiplication gain (5–9 dB sensitivity improvement over PIN) at the cost of excess noise factor and bias voltage.

APR  
Automatic power reduction. Holds laser output at or below Hazard Level 1M on fiber break and probes for re-mate with safe low-power pulses (ITU-T G.664).

ASE  
Amplified spontaneous emission. Broadband optical noise generated by optical amplifiers (SOA, EDFA); adds to the receiver noise floor.

AUI  
Attachment unit interface. The electrical serial lane set between a host ASIC and the module cage connector (e.g. 400GAUI-4).

BERT  
Bit-error-ratio tester. An instrument or ASIC function that generates PRBS patterns and counts bit errors for pre-FEC and post-FEC BER measurement.

BiCMOS  
A semiconductor process combining bipolar transistors (high $`f_T`$) with CMOS on one die; used for high-speed TIAs and modulator drivers.

BOM  
Bill of materials. The component and assembly cost of a module or system; DSP presence is a large BOM driver.

CMOS  
Complementary metal-oxide-semiconductor. The mainstream IC fabrication process; TIAs and SerDes are built at 16 nm to 3 nm nodes.

COBO  
Consortium for On-Board Optics. Standardized mid-board optical engine placement; largely leapfrogged by CPO in hyperscale deployments.

COD  
Catastrophic optical damage. A sudden, irreversible failure of a laser facet under thermal or optical overstress.

COM  
Channel operating margin. A statistical SNR metric for the fully equalized electrical link; CEI go/no-go is typically COM $`\ge`$ 3 dB.

COUPE  
Compact Universal Photonic Engine. TSMC’s SoIC-X hybrid-bonded EIC-on-PIC packaging platform for co-packaged optics; mass production in 2026.

CW  
Continuous wave. Unmodulated laser output; external modulators (MZM, ring, EAM) encode data onto a CW source.

CW-WDM  
Continuous-wave wavelength division multiplexing. A multi-source agreement for multi-wavelength CW laser sources feeding WDM photonic engines.

CXL  
Compute Express Link. A coherent memory interconnect protocol built on the PCIe PHY (CXL 4.0 on PCIe 7.0); potential optical-reach application.

DCA  
Digital communication analyzer. A sampling oscilloscope used for PAM4 eye diagrams, TDECQ, OMA, and RLM measurements.

DBR  
Distributed Bragg reflector. A laser architecture where the grating sits outside the gain region, enabling tunable single-mode output.

DDM  
Digital diagnostic monitoring. Per-lane telemetry in CMIS: Tx/Rx optical power, laser bias, module temperature, LOS/LOL flags.

DFB  
Distributed feedback laser. A laser with a grating along the active region that selects one longitudinal mode; the workhorse CW or directly modulated source.

DML  
Directly modulated laser. Modulates bias current to encode data; simple and efficient but chirp-limited over dispersive fiber.

DR  
Datacenter reach. An IEEE 802.3 single-mode fiber class, typically 500 m at 1310 nm; the default for AI scale-out optics.

DWDM  
Dense wavelength division multiplexing. WDM with channel spacing $`\le`$<!-- -->100 GHz; used in metro/long-haul and dense CPO architectures.

EAM  
Electro-absorption modulator. A voltage-controlled absorption region on InP; low chirp compared with direct modulation; paired with a DFB in an EML.

EECQ  
Electrical eye closure quaternary. The electrical analog of TDECQ, quoted at host-referenced test points TP1a and TP4a.

ELS  
External laser source. A CW laser module feeding a co-packaged optical engine; superset of ELSFP and CW-WDM module forms.

ELSFP  
External Laser Small Form-Factor Pluggable. An OIF-defined faceplate-pluggable CW laser module for CPO with a 24-pin card edge, CMIS management, and blind-mate MT optics.

EML  
Externally modulated laser. A DFB laser integrated with an EAM on one InP chip; the dominant 100–200G/lane pluggable transmitter.

EO  
Electro-optic. Conversion from voltage to optical phase or intensity; EO bandwidth is the primary speed metric for a modulator.

ER  
Extinction ratio. $`P_1/P_0`$ in dB; higher ER widens OMA for a given average power and trades against chirp and driver swing.

FAU  
Fiber array unit. A precision V-groove assembly that mates multiple fibers to a PIC edge or grating coupler array.

FIT  
Failures in time. Failures per $`10^9`$ device-hours; fleet FIT times link count sets expected failures per day.

FR  
Far reach. An IEEE 802.3 single-mode fiber class, typically 2 km; tighter chirp and dispersion budget than DR.

FSR  
Free spectral range. The wavelength or frequency span between adjacent resonances of a ring resonator or etalon.

HBM  
High-bandwidth memory. Stacked DRAM on an interposer beside the accelerator die; memory bandwidth sets the decode roofline.

HCF  
Hollow-core fiber. Guides light primarily in air ($`n\approx1`$), giving roughly 33% lower latency than solid silica SMF.

HTOL  
High-temperature operating life. An accelerated reliability stress test (GR-468); Arrhenius modeling projects field wear-out from HTOL results.

IBTA  
InfiniBand Trade Association. Maintains the InfiniBand Architecture spec (NDR 400G, XDR 800G/port); reuses QSFP/OSFP optics with Ethernet.

IEEE  
Institute of Electrical and Electronics Engineers. IEEE 802.3 owns Ethernet PHY/MAC rates, KP4 FEC, and IM/DD optical PMD clauses.

IL  
Insertion loss. Optical power lost traversing a component (connector, fiber, MUX); quoted in dB.

InP  
Indium phosphide. A III-V semiconductor material for lasers, EAMs, SOAs, and high-speed photodiodes in the 1310/1550 nm bands.

LIV  
Light–current–voltage. The fundamental laser characterization curve: plots optical power and voltage versus bias current to read threshold, slope, kinks, and rollover.

LOL  
Loss of lock. A CDR or SerDes flag indicating the clock recovery circuit has lost symbol timing.

LOS  
Loss of signal. A receiver or host flag indicating optical input power has fallen below the detect threshold.

LRO  
Linear receive optic (also called RTLR). A module with a retimer/DSP only on the transmit path; the receive path is linear into the host SerDes.

MAC  
Media access control. The Ethernet data-link sublayer that builds frames, handles addressing and CRC. MAC rate is payload throughput.

MACsec  
IEEE 802.1AE media access control security. Provides line-rate encryption, frame integrity, and data origin authentication at Layer 2; transparent to the optical PMD.

MDI  
Medium dependent interface. The optical connector where a module meets the fiber; test points TP2 (Tx launch) and TP3 (Rx input) sit at the MDI.

MEMS  
Micro-electro-mechanical systems. Tilting mirror arrays used in optical circuit switches; millisecond switching at $`\sim`$<!-- -->2 dB loss.

MLC  
Multi-level coding. Coded modulation paired with PAM6/PAM8; OIF 448G workshop models often add a strong outer RS code at $`\sim`$<!-- -->12% overhead.

MMF  
Multimode fiber. Fiber supporting many spatial modes (50/125 $`\mu`$m); used with VCSELs at 850–940 nm for SR links (OM3/OM4/OM5 grades).

MoE  
Mixture of experts. A transformer architecture that routes tokens to specialist sub-networks; drives all-to-all collective traffic on the fabric.

MPO  
Multi-fiber push-on. A standard multi-fiber connector for parallel optics (8, 12, 16, 24, or 32 fibers per ferrule).

MRM  
Microring modulator. A resonant silicon modulator; compact and WDM-native but requires wavelength lock. The CPO workhorse at 200G/channel.

MSA  
Multi-source agreement. An industry specification for interoperable products (e.g. LPO MSA, CW-WDM MSA, 100G Lambda MSA).

MZM  
Mach–Zehnder modulator. A push-pull interferometer; broadband, low chirp. Built in silicon, TFLN, or III-V platforms.

NFF  
No fault found. An RMA unit that passes all tests on return; high NFF rate points at triage or intermittent connector faults.

NIC  
Network interface card. A host adapter connecting an accelerator or CPU to the scale-out fabric (Ethernet or InfiniBand).

OBO  
On-board optics. Optical engines mounted mid-board on the host PCB (COBO standard); mostly bypassed for CPO in hyperscale.

OCS  
Optical circuit switch. A Layer-1 switch that steers light from input to output fiber with no O-E-O conversion; transparent to rate, format, and wavelength.

OMA  
Optical modulation amplitude. The outer PAM4 signal swing ($`P_1-P_0`$); the primary power metric for IM/DD transmitters.

ORL  
Optical return loss. The ratio of reflected to incident power at a fiber interface; low ORL raises laser RIN and can cause burst errors.

OSA  
Optical spectrum analyzer. An instrument that measures wavelength, SMSR, side-mode structure, and spectral width of a laser source.

OSFP  
Octal Small Form-factor Pluggable. A high-power faceplate module cage for 800G/1.6T/3.2T; larger thermal envelope than QSFP-DD.

PCS  
Physical coding sublayer. The IEEE 802.3 sublayer that performs 64B/66B line coding, 256B/257B transcoding, scrambling, and RS-FEC encoding.

PD  
Photodiode. A semiconductor device that converts photons to photocurrent (PIN, APD, or UTC variants).

PHY  
Physical layer. The combined PCS, PMA, and PMD that maps MAC frames to signals on the wire or fiber.

PIC  
Photonic integrated circuit. A chip integrating waveguides, modulators, detectors, and couplers (typically on SOI at 220 nm silicon).

PIN  
A p-intrinsic-n photodiode with no internal gain and the lowest excess noise; Ge-on-Si waveguide PIN is the mainstream short-reach detector.

PMA  
Physical medium attachment. The IEEE 802.3 sublayer that serializes, lane-multiplexes, and recovers clock. The SerDes lives here.

PMD  
Physical medium dependent. The IEEE 802.3 sublayer that modulates and detects light: the optical transceiver (laser, driver, PD, TIA).

PRBS  
Pseudo-random binary sequence. A deterministic test pattern that exercises all bit transitions; used for BER and eye measurements.

PSRR  
Power supply rejection ratio. A circuit’s ability to suppress supply-rail noise; critical for laser bias drivers to avoid injecting RIN.

PUE  
Power usage effectiveness. Total facility power divided by IT equipment power; typical hyperscale values 1.1–1.3.

QSFP-DD  
Quad Small Form-factor Pluggable Double Density. A faceplate module cage carrying eight electrical lanes for 400G/800G/1.6T.

RDMA  
Remote direct memory access. Zero-copy network transfer between accelerator memories; carried over RoCE (Ethernet) or native InfiniBand.

RIN  
Relative intensity noise. The laser’s own amplitude-noise spectral density (dB/Hz); sets a BER floor that power cannot overcome.

RLM  
Relative level mismatch. A measure of PAM4 level spacing uniformity (1.0 = perfectly even); CEI typically requires $`\ge`$<!-- -->0.95.

RMA  
Return merchandise authorization. A field-failed unit returned to the supplier for failure analysis. Distinct RMA codes keep FIT accounting honest.

SECQ  
Stressed eye closure quaternary. A receiver-side metric that applies calibrated optical stress and reports remaining margin before BER threshold.

SiGe  
Silicon-germanium BiCMOS. A high-$`f_T`$ semiconductor process for TIAs and modulator drivers operating at 100–200+ GHz bandwidth.

SiPh  
Silicon photonics. Waveguides and modulators on silicon-on-insulator; CMOS fab-compatible and the mainstream for DR/FR and CPO.

SMF  
Single-mode fiber. Fiber with a $`\sim`$<!-- -->9 $`\mu`$m core carrying one spatial mode; G.652.D (standard) and G.657 (bend-insensitive) for datacenter plant.

SMSR  
Side-mode suppression ratio. The power difference (dB) between the dominant lasing mode and the strongest side mode on an OSA.

SOA  
Semiconductor optical amplifier. A III-V inline optical gain block; adds ASE noise. Used as a receiver preamplifier for sensitivity.

SOI  
Silicon on insulator. A wafer substrate for silicon photonics: a thin ($`\sim`$<!-- -->220 nm) silicon layer on buried oxide confines the optical mode.

SR  
Short reach. An IEEE 802.3 multimode fiber class, typically $`\le`$<!-- -->100 m over OM4; VCSEL at 850 nm.

TCO  
Total cost of ownership. Acquisition (BOM, yield) plus lifetime energy plus service cost (FIT $`\times`$ replacement + labor).

TDECQ  
Transmitter and dispersion eye closure quaternary. The headline PAM4 transmitter-quality metric; measured after a reference receiver and bounded FFE, including a test fiber.

TEC  
Thermoelectric cooler. A Peltier device that holds a laser junction or ring at a controlled temperature against case thermal variations.

TECQ  
Transmitter eye closure quaternary. Same measurement as TDECQ without the test fiber; used alongside TDECQ in LPO MSA OMA tables.

TFLN  
Thin-film lithium niobate. A sub-micrometer LN layer on a silicon or silica handle; $`>`$<!-- -->110 GHz EO BW and the leading path to native 224 GBd PAM4.

TIA  
Transimpedance amplifier. Converts photodiode current to voltage with low input-referred noise; co-packaging with the PD minimizes capacitance and noise.

TP  
Test point. A defined reference plane where a link measurement is taken (TP0 through TP5, plus TP1a/TP4a).

TRO  
Transmit retimed optic. A module with DSP only on the transmit (electrical-to-optical) path; the receive path is linear.

TWE  
Traveling-wave electrode. An RF transmission line on a modulator that velocity-matches the electrical and optical group indices for high EO bandwidth.

TWI  
Two-wire interface. An I2C-like serial bus (SCL + SDA) used for CMIS module management communication.

UALink  
Ultra Accelerator Link. An open scale-up fabric specification for direct accelerator memory access (200G/lane class; $`\sim`$<!-- -->400G/lane next).

UEC  
Ultra Ethernet Consortium. Builds an open Ethernet-based stack (UET transport, PHY) optimized for AI/HPC scale-out with cluster-scale congestion control.

UI  
Unit interval. One symbol period ($`=1/R_\mathrm{sym}`$); jitter budgets and eye diagrams are referenced in UI.

UTC / MUTC  
Uni-traveling-carrier (modified UTC) photodiode. Uses electron-only transport for $`>`$<!-- -->200 GHz bandwidth and high saturation current; linear/LPO niche.

VOA  
Variable optical attenuator. A calibrated loss element used for sensitivity sweeps and stressed-receiver testing.

WDM  
Wavelength division multiplexing. Sending multiple wavelengths on one fiber; CWDM (20 nm spacing) or DWDM ($`\le`$<!-- -->100 GHz spacing).

XPO  
eXtra-dense Pluggable Optics. A liquid-cooled, 12.8 Tb/s faceplate pluggable module (Arista MSA, OFC 2026); front-panel serviceable at CPO-class density.

# References

## References

See the PDF version for the full bibliography.

[^1]: IM/DD = intensity modulation with direct detection: the short-reach datacenter transceiver style. See <a href="#ch:imdd" data-reference-type="ref+Label" data-reference="ch:imdd">3</a>.

[^2]: Source: [Broadcom and partner, “LLM-optimized inference chip,” 24 June 2026](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor).

[^3]: [D. A. B. Miller, “Device requirements for optical interconnects to silicon chips,” *Proc. IEEE*, 2009](https://doi.org/10.1109/JPROC.2009.2014298); and [“Attojoule optoelectronics for low-energy information processing and communications,” *JLT*, 2017](https://doi.org/10.1109/JLT.2017.2647779).

[^4]: The exact prefactor depends on the signaling scheme (voltage-mode, current-mode, terminated transmission line) but the *length dependence* is the first principle that matters here.

[^5]: This is why integration is not a packaging convenience but an energy strategy: shortening the electrical path between detector and amplifier lowers capacitance, which lowers both the energy and the optical power a link needs.

[^6]: [S. Daudlin *et al.*, “Three-dimensional photonic integration for ultra-low-energy, high-bandwidth interchip data links,” *Nature Photonics* 19:502–509, 2025](https://doi.org/10.1038/s41566-025-01633-0).

[^7]: [P.-H. Chang *et al.*, “A 3D integrated energy-efficient transceiver … co-designed 12 nm FinFET and silicon photonic ICs,” *JLT* 41(21):6741–6755, 2023](https://doi.org/10.1109/JLT.2023.3291704).

[^8]: [A. Pirmoradi *et al.*, “A single-chip 1.024 Tb/s silicon photonics PAM4 receiver,” arXiv:2507.12452, 2025](https://arxiv.org/abs/2507.12452).

[^9]: [Avicena, ECOC 2025 demonstration of the LightBundle microLED interconnect](https://www.avicena.tech/).

[^10]: Contrast with *coherent* detection, which mixes the signal against a local-oscillator laser to recover amplitude *and* phase. Coherent wins for long-haul spectral efficiency; IM/DD wins on cost and power for short reach.

[^11]: A clean mental model: start with transmitter OMA, subtract connector and fiber loss, subtract penalties (dispersion, TDECQ, reflection), and compare the result to receiver sensitivity (<a href="#sec:sensitivity,ch:models,sec:link-budget" data-reference-type="ref+Label" data-reference="sec:sensitivity,ch:models,sec:link-budget">[sec:sensitivity,ch:models,sec:link-budget]</a>). What remains is margin.

[^12]: [E. Säckinger, *Analysis and Design of Transimpedance Amplifiers for Optical Receivers*, Wiley, 2018, ch. 4](https://doi.org/10.1002/9781119264422).

[^13]: $`Q`$ here is the electrical decision quality, not to be confused with a laser-cavity or resonator $`Q`$.

[^14]: For example [IEEE 802.3 / 100G Lambda MSA short-reach PAM4 links](https://www.ieee802.org/3/bs/public/) cap $`\mathrm{RIN}_{17.1}\mathrm{OMA}`$ at $`-136`$ dB/Hz with 17.1 dB ORL .

[^15]: The fork is a reliability decision. *External* sources (Ayar, Broadcom ELSFP, POET) make the highest-failure component field-replaceable; *integrated* lasers (Intel, OpenLight, Scintil) win on density and cost but place that component permanently inside the package. The leading CPO programs have so far chosen external, for the GR-468 reasons of <a href="#ch:reliability,sec:elsfp" data-reference-type="ref+Label" data-reference="ch:reliability,sec:elsfp">[ch:reliability,sec:elsfp]</a>.

[^16]: Source: [Ayar Labs, SuperNova light source, ayarlabs.com](https://ayarlabs.com/supernova/). Positioning: Ayar targets scale-up optical I/O between accelerators; Broadcom and NVIDIA CPO (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>) put the same building blocks on the *switch*.

[^17]: Worked example. “The link fails only at high temperature.” Candidate causes: laser wavelength drift off the grid or off a ring resonance; TEC saturation; EAM bias shift; elevated receiver thermal noise; LIV rollover (<a href="#sec:laser-aging,sec:laser-params" data-reference-type="ref+Label" data-reference="sec:laser-aging,sec:laser-params">[sec:laser-aging,sec:laser-params]</a>). You bisect with measurements (spectrum for wavelength, LIV for the laser, receiver sensitivity at temperature) rather than guessing.

[^18]: An order-of-magnitude exercise: a $`100{,}000`$-GPU cluster with several optical links per GPU has on the order of $`10^{5}`$–$`10^{6}`$ lasers. Even a small per-laser FIT then implies a nontrivial number of link failures per day, which is exactly why field-replaceable external laser sources and redundancy are attractive.

[^19]: Rule of thumb: a redriver reshapes, a retimer rebuilds timing. Neither fixes reflections or a bad return path.

[^20]: Broadcom’s broader AI-Ethernet stack: Tomahawk and Jericho switches, Thor NICs, Agera retimers, Sian optical DSPs, and CPO. Large hyperscale inference fabrics draw on this family (<a href="#ch:role" data-reference-type="ref+Label" data-reference="ch:role">1</a>).

[^21]: XPO is best read as a hedge against CPO’s serviceability problem. If field-replaceable ELSFP lasers (<a href="#sec:cpo-status" data-reference-type="ref+Label" data-reference="sec:cpo-status">9.10</a>) prove insufficient and CPO repair economics stay painful, a liquid-cooled pluggable that reaches CPO-class density lets operators keep the failure model they already trust. The reliability and validation questions of <a href="#ch:validation,ch:reliability" data-reference-type="ref+Label" data-reference="ch:validation,ch:reliability">[ch:validation,ch:reliability]</a> are exactly what decides which path wins.
