---
layout: default
title: "Ch 1: Why the interconnect matters"
---

# Why the interconnect matters

## The two themes of this book

Large AI systems fail or succeed as much on wiring as on FLOPs. The short-reach optics that connect accelerators, switches, and memory sit on the critical path for latency, power, and uptime, and two parts of that layer decide whether the system scales: the *lasers* that generate the light, and the discipline of *IM/DD validation*[^1] that proves those links work from the first bench eye through production and fleet life. This book keeps returning to those two themes. Modulation formats, WDM, reliability, and network architecture matter because they serve them.

**Key idea.** Two things dominate short-reach optics at scale: *lasers* and *IM/DD validation*. Everything else orbits those two.

## The context: purpose-built inference silicon

The pressure on the interconnect is not abstract. It comes from a shift in how large AI systems are built: vertically integrated, purpose-built silicon deployed at gigawatt scale, with networking named as a first-order design axis beside compute and memory. A representative example is *Jalapeño*, a purpose-built LLM *inference* accelerator Broadcom and a hyperscaler partner announced in 2026 as a blank-slate design, the first chip in a multi-generation compute platform.[^2] Its public features are typical of the class:

- **Partners and integration.** Broadcom provides silicon implementation and networking (including *Tomahawk* switch silicon); Celestica provides board, rack, and system integration.

- **Cadence.** A roughly nine-month design-to-tape-out cycle, with the designers' own models used to accelerate parts of the flow.

- **Scale.** Deployment at gigawatt scale, over multiple generations, beginning in late 2026.

- **Design thesis.** "Reduce data movement and balance compute, memory, and *networking* resources" to reach realized utilization close to theoretical peak.

That last point is the hook for this book. Purpose-built inference silicon does not treat networking as a commodity NIC bolted on after the die is done; it budgets interconnect power and latency alongside FLOPs and HBM. Partners and cadence matter because they set who owns the switch ASIC and how fast generations turn: Broadcom for silicon and networking (including Tomahawk), Celestica for board and rack, a roughly nine-month design-to-tape-out cycle, and gigawatt-scale deployment planned across multiple generations from late 2026. Once networking sits on that line, the optical interconnect is how the system scales past a single package to a gigawatt cluster, and laser quality plus IM/DD validation become infrastructure problems rather than module afterthoughts.

## Why inference makes the interconnect matter

Inference is not training. Once a model is trained, serving it is dominated by two phases with very different bottlenecks (developed fully in [9](#ch:networking)):

Prefill

: processing the prompt: highly parallel and compute-bound, much like training.

Decode

: generating tokens one at a time: autoregressive and *memory-bandwidth-bound*, because every token streams the model weights through the compute units again.

Frontier models do not fit on one chip. They are sharded across many accelerators, so every generated token triggers *collective communication* across the fabric: all-reduce for tensor parallelism, all-to-all for mixture-of-experts routing, point-to-point for pipeline stages. The interconnect therefore sits on the *latency critical path* of inference, not merely the plumbing between training runs.

**Key idea.** Reliable, low-power IM/DD links directly set how large and how dependable an inference fabric can be. That is why the optical layer has become central to AI system design.

## How to read this book

The chapters build from physics to fleet scale:

1.  [\[ch:firstprinciples,ch:imdd\]](#ch:firstprinciples,ch:imdd): energy, IM/DD vocabulary, modulators, FEC, equalization.

2.  [4](#ch:models): quantitative noise, RIN, sensitivity (use with [7.6](#sec:link-budget)).

3.  [5](#ch:lasers): light sources (DFB/EML, LIV/SMSR/RIN, aging, ELSFP/CW-WDM).

4.  [6](#ch:wdm): wavelength locking, thermal crosstalk, CW-WDM, on-chip MUX.

5.  [\[ch:validation,ch:reliability\]](#ch:validation,ch:reliability): measurement ladder, link budgets, qual, packaging.

6.  [9](#ch:networking): scale-up/out, pluggables, CPO/XPO, inference collectives.

To use the book as a design drill, pick one link style (retimed 800G DR, LPO, or CPO WDM) and trace it end to end through [\[sec:txrx-chain,sec:pluggables,sec:cpo-status\]](#sec:txrx-chain,sec:pluggables,sec:cpo-status).


<div class="nav-links">
  <a href="ch0-preface">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch2-first-principles-the-energy-of-moving-a-bit">Next &rarr;</a>
</div>
