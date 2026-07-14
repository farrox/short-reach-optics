---
layout: default
title: "Ch 2: First principles: the energy of moving a bit"
---

# First principles: the energy of moving a bit

Before any device, modulation format, or standard, one quantity governs short-reach interconnect design: the energy required to move a bit from one place to another. David Miller's work on optical interconnects to silicon lays out the clearest first-principles framework for this,[^3] and although the specific numbers are years old, the scaling arguments are what matter, and they still decide where the optics go.

## The electrical baseline: charging a wire

To send a bit down an electrical line you charge and discharge its capacitance through a voltage swing. To order of magnitude, $$E_{\text{elec}} \approx \tfrac{1}{2}\,C\,V^{2},$$ and the line capacitance grows with length, $C \approx c'\,L$ (with $c'$ on the order of a hundred-odd femtofarads per millimeter, depending on the medium). [^4] So the energy to move a bit electrically *rises with distance*, and the resistive-capacitive delay and the equalization needed to fight it rise with both distance and data rate.

## The optical alternative: energy at the ends

An optical link spends its energy differently. The dominant costs are the *conversions at the two ends* (driving the laser or modulator, and the receiver that turns light back into charge) plus the wall-plug inefficiency of the laser. Over short reaches, waveguide and fiber loss are small, so the energy per bit is, to first order, *independent of distance*.

**Key idea.** Electrical energy per bit grows with length; optical energy per bit is set at the endpoints and is roughly flat with length. That single contrast is the seed of everything else.

## The break-even distance, and why optics moves toward the chip

Put the two together and there is a cross-over length: below it, electrical wins; above it, optical wins. The decisive observation is what happens as data rates climb: the electrical cost at a given length rises (more charging events per second, worse loss at higher frequency, more equalization), so the *break-even distance shrinks*.

That is the whole history of the field in one sentence. As rates went from gigabits to hundreds of gigabits per lane, the cross-over marched inward: campus, then rack, then board, then package, and now die-to-die. It is the first-principles reason co-packaged optics and in-package optical I/O exist ([\[sec:cpo-status,sec:cwwdm\]](#sec:cpo-status,sec:cwwdm)), and the reason the scope of this book is the *shortest* links ([3.3](#sec:reach)).

## The receiver, capacitance, and attojoule targets

Miller's sharpest point concerns the receiver. To register a bit, the photocurrent must develop a detectable voltage on the receiver's input node, so the detection energy again looks like a $C V^{2}$ on that node's capacitance. Minimize the photodetector and input capacitance (by integrating the detector tightly with the first transistor, eliminating parasitic pads and wires) and you can detect a bit with *fewer photons and less energy*. This is the argument for close electronic--photonic integration, and it is what makes sub-100 fJ/bit (and, in principle, attojoule-class) devices conceivable.

[^5]

## The floors: photons per bit and noise

Two physical floors bound how far this can go. A real receiver needs enough photons per bit for adequate signal-to-noise: today hundreds, with ideal detection in the handful-of-photons range. That sets a floor on received optical power, and hence on laser energy. Separately, the $kT/C$ noise on the receiver node (not the Landauer $kT\ln 2$ limit of logic, which is far smaller) is the practical noise floor for communication, and it too rewards small capacitance.

Miller is careful to separate the energy of *logic* from the energy of *communication*; short-reach interconnect is overwhelmingly a communication- energy problem, dominated by the endpoints described above.

## Recent progress toward the limits

Miller's numbers are years old, but the framework has aged well: the last few years have been a steady march of experiments toward the floors it predicts, and they validate rather than overturn it. Three threads are worth knowing.

First, **low-capacitance 3D integration is delivering the receiver energy Miller argued for**. A 2025 demonstration integrated an 80-channel transceiver in three dimensions, stacking the photonics directly on the CMOS to minimize the receiver-node capacitance, and reported roughly 120 fJ/bit.[^6] Tellingly, it reaches that number not by pushing per-lane rate but by using *many slow channels* (about 10 Gb/s each) so each receiver stays in its most sensitive, lowest-energy regime, with WDM providing the aggregate bandwidth. That is Miller's prescription almost verbatim.

Second, **the capacitance argument is directly measurable**. A co-designed 12 nm-FinFET-on-silicon-photonics transceiver using direct-bond interconnect cut input parasitic capacitance by about 75 %, which bought $\sim\!\SI{6}{dB}$ of receiver sensitivity and pushed link energy to a few hundred fJ/bit.[^7] The $C V^{2}$ story is not a metaphor; you can watch the sensitivity move as the capacitance drops.

Third, **WDM receivers with near-zero-power wavelength control are approaching sub-pJ/bit at terabit scale**: a single-chip 32-channel WDM PAM4 receiver reached 1.024 Tb/s on one fiber at under 0.38 pJ/bit with no DSP or equalization.[^8] And on the device side, alternative emitters are being pushed into the same regime, a 2025 microLED link demonstrated 200 fJ/bit transmitter energy at $\text{BER} < 10^{-12}$ with no FEC,[^9] exactly the LED branch of Miller's device-by-device comparison.

**Key idea.** The 2009/2017 framework has not been superseded; it has been confirmed in hardware. The winning recipe in every recent result (low-capacitance co-/3D-integration plus many WDM channels at modest per-lane rate) is precisely what Miller's energy accounting recommends. What has changed is only the vertical axis: from theoretical attojoule targets toward demonstrated hundreds-of-fJ/bit links.

## Why this framework anchors the book

Everything that follows is an effort to approach these floors at the required data rate and reliability. Laser wall-plug efficiency ([5](#ch:lasers)) sets how much optical power you can afford. Modulation and FEC ([\[ch:imdd,sec:kp4,sec:equalization\]](#ch:imdd,sec:kp4,sec:equalization)) trade SNR for reach and rate. WDM ([6](#ch:wdm)) amortizes one laser source across many wavelengths. Receiver noise and sensitivity ([\[ch:models,sec:worked-budget,sec:link-budget\]](#ch:models,sec:worked-budget,sec:link-budget)) decide whether that power is enough. Co-packaging and energy-per-bit trends ([9.13](#sec:power)) show the same first principle playing out as copper reach collapses and optics move onto the interposer.

**Key idea.** Short-reach optics is, at bottom, an energy-per-bit optimization. Optical energy is spent at the endpoints and is flat with distance; electrical energy grows with distance and rate; so rising data rates push optics ever closer to the chip. Miller's framework is the lens the rest of this book looks through.


<div class="nav-links">
  <a href="ch1-why-the-interconnect-matters">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch3-intensity-modulation-direct-detection">Next &rarr;</a>
</div>
