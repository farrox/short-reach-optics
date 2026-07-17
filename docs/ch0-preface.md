---
layout: default
title: "Ch 0: Preface"
---

# Preface

Artificial intelligence has become an infrastructure problem. Training and serving frontier models at scale is no longer limited only by the accelerator at the center of the rack, but by how many accelerators can be wired together efficiently, reliably, and within a fixed power envelope. That wiring is increasingly optical, and the optics (especially the lasers inside them) have become a first-order lever on the cost, power, and reliability of the whole system.

This book is a concise technical overview of that layer: the short-reach optical interconnects that stitch together AI datacenters, from in-package optical I/O out to intra-rack links, deliberately setting aside the 2--10 km campus links that belong to coherent optics (§ `sec:reach`). It concentrates on the subjects that decide whether these links work at scale: IM/DD physics and vocabulary; lasers and external light sources; WDM and wavelength locking; quantitative noise and sensitivity models; validation from bench to fleet; and reliability and manufacturing at volume. Two chapters bracket those fundamentals: why inference-scale computing puts the interconnect on the critical path (§ `ch:role`), and how AI datacenter networks are built where optics dominate cost and power (§ `ch:networking`).

**On sources.** The industry moves quickly. Where the text cites specific products or figures (co-packaged-optics programs, per-lane roadmaps, energy-per-bit trends) it draws on public disclosures current as of early 2026, cited in the references. Where a claim is an inference rather than an established fact, the text says so. History and trend notes are included where they help explain why today's defaults exist, not as a full chronology of the field.

**Key idea.** The through-line: at gigawatt, multi-generation scale, the optical interconnect and its lasers are a first-order lever on power, cost, and reliability. Everything here serves that argument.


<div class="nav-links">
  <span></span>
  <a href="./">Table of Contents</a>
  <a href="ch1-why-the-interconnect-matters">Next &rarr;</a>
</div>
