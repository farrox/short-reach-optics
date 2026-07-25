---
layout: default
title: "Ch 0: Preface"
---

# 0 Preface

Artificial intelligence has become an infrastructure problem. Training and serving frontier models at scale is no longer limited only by the accelerator at the center of the rack, but by how many accelerators can be wired together efficiently, reliably, and within a fixed power envelope. That wiring is increasingly optical, and the optics (especially the lasers inside them) have become a first-order lever on the cost, power, and reliability of the whole system.

This book is a concise technical overview of that layer: the short-reach optical interconnects that stitch together AI datacenters, from in-package optical I/O out to intra-rack links, deliberately setting aside the 2--10 km campus links that belong to coherent optics (§3.3). It concentrates on the subjects that decide whether these links work at scale: IM/DD physics and vocabulary; lasers and external light sources; WDM and wavelength locking; quantitative noise and sensitivity models; validation from bench to fleet; and reliability and manufacturing at volume. Two chapters bracket those fundamentals: why inference-scale computing puts the interconnect on the critical path (Chapter 1), and how AI datacenter networks are built where optics dominate cost and power (Chapter 9).

**How to use this handbook.** Start from the requirement, not the component. Move downward from system requirements to architecture, subsystem, component, and only then to the physics needed to make or test the decision. A choice at one layer constrains the next. A VCSEL points toward 850 nm, multimode fiber, and direct modulation. A DFB at 1310 nm points toward single-mode fiber and leaves a choice among direct modulation, an EML, or an external modulator. Neither path is best in isolation. Each closes a different reach, power, cost, manufacturing, and service model.

Every major chapter asks four questions: How does it work? How is it measured, and what uncertainty does the measurement remove? How does it fail? How is it debugged? The aim is operational judgment. The purpose of engineering is not to find certainty. It is to reduce uncertainty enough to make the next decision. Validation, measurement, debugging, qualification, supplier choices, and production are all that same work under different names. Debugging asks which margin was exhausted. Qualification asks how much margin remains after stress. Both end on a decision and a recurrence control. ASCII trees and checklists throughout the chapters, plus the wall chart in Appendix C, are there so you can recover that method in minutes. Interview drill lives in Appendix A, Appendix B.

**On sources.** The industry moves quickly. Where the text cites specific products or figures (co-packaged-optics programs, per-lane roadmaps, energy-per-bit trends) it draws on public disclosures current as of early 2026, cited in the references. Where a claim is an inference rather than an established fact, the text says so. History and trend notes are included where they help explain why today's defaults exist, not as a full chronology of the field.

**Key idea.** The goal of an optical systems engineer is not to know every component. It is to make good engineering decisions under uncertainty using measurements, physics, and evidence. At gigawatt, multi-generation scale, the optical interconnect and its lasers are a first-order lever on power, cost, and reliability. Everything here serves that argument.


<div class="nav-links">
  <span></span>
  <a href="./">Table of Contents</a>
  <a href="ch1-why-the-interconnect-matters">Next &rarr;</a>
</div>
