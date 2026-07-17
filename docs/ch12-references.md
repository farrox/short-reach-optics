---
layout: default
title: "Ch 12: References"
---

# References

## References

See the PDF version for the full bibliography.

[^1]: IM/DD = intensity modulation with direct detection: the short-reach datacenter transceiver style. See Chapter 3.

[^2]: Source: [Broadcom and partner, "LLM-optimized inference chip," 24 June 2026](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor).

[^3]: [D. A. B. Miller, "Device requirements for optical interconnects to silicon chips," *Proc. IEEE*, 2009](https://doi.org/10.1109/JPROC.2009.2014298); and ["Attojoule optoelectronics for low-energy information processing and communications," *JLT*, 2017](https://doi.org/10.1109/JLT.2017.2647779).

[^4]: The exact prefactor depends on the signaling scheme (voltage-mode, current-mode, terminated transmission line) but the *length dependence* is the first principle that matters here.

[^5]: This is why integration is not a packaging convenience but an energy strategy: shortening the electrical path between detector and amplifier lowers capacitance, which lowers both the energy and the optical power a link needs.

[^6]: [S. Daudlin *et al.*, "Three-dimensional photonic integration for ultra-low-energy, high-bandwidth interchip data links," *Nature Photonics* 19:502--509, 2025](https://doi.org/10.1038/s41566-025-01633-0).

[^7]: [P.-H. Chang *et al.*, "A 3D integrated energy-efficient transceiver ... co-designed 12 nm FinFET and silicon photonic ICs," *JLT* 41(21):6741--6755, 2023](https://doi.org/10.1109/JLT.2023.3291704).

[^8]: [A. Pirmoradi *et al.*, "A single-chip 1.024 Tb/s silicon photonics PAM4 receiver," arXiv:2507.12452, 2025](https://arxiv.org/abs/2507.12452).

[^9]: [Avicena, ECOC 2025 demonstration of the LightBundle microLED interconnect](https://www.avicena.tech/).

[^10]: Contrast with *coherent* detection, which mixes the signal against a local-oscillator laser to recover amplitude *and* phase. Coherent wins for long-haul spectral efficiency; IM/DD wins on cost and power for short reach.

[^11]: A clean mental model: start with transmitter OMA, subtract connector and fiber loss, subtract penalties (dispersion, TDECQ, reflection), and compare the result to receiver sensitivity (§4.4, Chapter 4, §7.7). What remains is margin.

[^12]: [E. Säckinger, *Analysis and Design of Transimpedance Amplifiers for Optical Receivers*, Wiley, 2018, ch. 4](https://doi.org/10.1002/9781119264422).

[^13]: $Q$ here is the electrical decision quality, not to be confused with a laser-cavity or resonator $Q$.

[^14]: For example [IEEE 802.3 / 100G Lambda MSA short-reach PAM4 links](https://www.ieee802.org/3/bs/public/) cap $\mathrm{RIN}_{17.1}\mathrm{OMA}$ at $-136$ dB/Hz with 17.1 dB ORL .

[^15]: The fork is a reliability decision. *External* sources (Ayar, Broadcom ELSFP, POET) make the highest-failure component field-replaceable; *integrated* lasers (Intel, OpenLight, Scintil) win on density and cost but place that component permanently inside the package. The leading CPO programs have so far chosen external, for the GR-468 reasons of Chapter 8, §5.11.

[^16]: Source: [Ayar Labs, SuperNova light source, ayarlabs.com](https://ayarlabs.com/supernova/). Positioning: Ayar targets scale-up optical I/O between accelerators; Broadcom and NVIDIA CPO (§9.10) put the same building blocks on the *switch*.

[^17]: Worked example. "The link fails only at high temperature." Candidate causes: laser wavelength drift off the grid or off a ring resonance; TEC saturation; EAM bias shift; elevated receiver thermal noise; LIV rollover (§5.10, §5.6). You bisect with measurements (spectrum for wavelength, LIV for the laser, receiver sensitivity at temperature) rather than guessing.

[^18]: An order-of-magnitude exercise: a $100{,}000$-GPU cluster with several optical links per GPU has on the order of $10^{5}$--$10^{6}$ lasers. Even a small per-laser FIT then implies a nontrivial number of link failures per day, which is exactly why field-replaceable external laser sources and redundancy are attractive.

[^19]: Rule of thumb: a redriver reshapes, a retimer rebuilds timing. Neither fixes reflections or a bad return path.

[^20]: Broadcom's broader AI-Ethernet stack: Tomahawk and Jericho switches, Thor NICs, Agera retimers, Sian optical DSPs, and CPO. Large hyperscale inference fabrics draw on this family (Chapter 1).

[^21]: XPO is best read as a hedge against CPO's serviceability problem. If field-replaceable ELSFP lasers (§9.10) prove insufficient and CPO repair economics stay painful, a liquid-cooled pluggable that reaches CPO-class density lets operators keep the failure model they already trust. The reliability and validation questions of Chapter 7, Chapter 8 are exactly what decides which path wins.


<div class="nav-links">
  <a href="ch11-abbreviations">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <span></span>
</div>
