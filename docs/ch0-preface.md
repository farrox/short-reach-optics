---
layout: default
title: "Ch 0: Preface"
---

# 0 Preface

Artificial intelligence has become an infrastructure problem. Training and serving frontier models at scale is no longer limited only by the accelerator at the center of the rack, but by how many accelerators can be wired together efficiently, reliably, and within a fixed power envelope. That wiring is increasingly optical, and the optics (especially the lasers inside them) have become a first-order lever on the cost, power, and reliability of the whole system.

This book is a concise technical overview of that layer: the short-reach optical interconnects that stitch together AI datacenters, from in-package optical I/O out to intra-rack links, deliberately setting aside the 2--10 km campus links that belong to coherent optics (§3.3). It concentrates on the subjects that decide whether these links work at scale: IM/DD physics and vocabulary; lasers and external light sources; WDM and wavelength locking; quantitative noise and sensitivity models; validation from bench to fleet; and reliability and manufacturing at volume. Two chapters bracket those fundamentals: why inference-scale computing puts the interconnect on the critical path (Chapter 1), and how AI datacenter networks are built where optics dominate cost and power (Chapter 9).

**How to use this handbook.** The book supports three modes. Pick one and stay in it until you switch deliberately.

Deep learning

: Read the body chapters from requirements downward (Chapter 1 through Chapter 9), then the failure-analysis handbook (Chapter 10). Every major chapter asks: How does it work? How is it measured, and what uncertainty does the measurement remove? How does it fail? How is it debugged?

Interview preparation

: Follow the one-week plan (Appendix A.13), practice cases (Appendix B), drill thirty-second answers and tradeoff questions (Appendix C), review the Top 25 index (Appendix E), and read how Staff judgment works (Appendix F).

Incident / problem solving

: Open the wall-chart trees (Appendix D), the failure handbook (Chapter 10), a matching case (Appendix B), and the Staff judgment appendix (Appendix F). Recover the method in minutes, not hours.

Start from the requirement, not the component. Move downward from system requirements to architecture, subsystem, component, and only then to the physics needed to make the decision. A choice at one layer constrains the next. The aim is operational judgment: reduce uncertainty enough to make the next decision, then name the control that prevents recurrence.

**On sources.** The industry moves quickly. Where the text cites specific products or figures (co-packaged-optics programs, per-lane roadmaps, energy-per-bit trends) it draws on public disclosures current as of early 2026, cited in the references. Where a claim is an inference rather than an established fact, the text says so. History and trend notes are included where they help explain why today's defaults exist, not as a full chronology of the field.

**Key idea.** The goal of an optical systems engineer is not to know every component. It is to make good engineering decisions under uncertainty using measurements, physics, and evidence. At gigawatt, multi-generation scale, the optical interconnect and its lasers are a first-order lever on power, cost, and reliability. Everything here serves that argument.

Content freeze: this handbook is frozen for expansion. Prefer cuts, cross-refs, and errata over new frameworks or chapters.


<div class="nav-links">
  <span></span>
  <a href="./">Table of Contents</a>
  <a href="ch1-why-the-interconnect-matters">Next &rarr;</a>
</div>
