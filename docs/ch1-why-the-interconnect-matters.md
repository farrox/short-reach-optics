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

Inference is not training. Once a model is trained, serving it is dominated by two phases with very different bottlenecks (developed fully in Chapter 9):

Prefill

: processing the prompt: highly parallel and compute-bound, much like training.

Decode

: generating tokens one at a time: autoregressive and *memory-bandwidth-bound*, because every token streams the model weights through the compute units again.

Frontier models do not fit on one chip. They are sharded across many accelerators, so every generated token triggers *collective communication* across the fabric: all-reduce for tensor parallelism, all-to-all for mixture-of-experts routing, point-to-point for pipeline stages. The interconnect therefore sits on the *latency critical path* of inference, not merely the plumbing between training runs.

**Key idea.** Reliable, low-power IM/DD links directly set how large and how dependable an inference fabric can be. That is why the optical layer has become central to AI system design.

## The shifting bottleneck

Each generation of AI infrastructure has been limited by a different resource. The progression explains why optics moved from a commodity NIC accessory to a first-order design axis:

Compute-limited

: Early deep learning (pre-2016). GPUs were scarce and slow; models fit on one card; the network barely mattered.

Memory-limited

: Larger models and larger batches (2016--2020). HBM bandwidth set training throughput; the network carried gradients but was rarely the gate.

Network-limited

: Sharded frontier models (2020--present). Tensor, pipeline, and expert parallelism put collectives on the critical path; fabric bandwidth and tail latency now limit realized compute use (§9.7, §9.6).

Power-limited

: Gigawatt-class deployments (emerging). Site megawatts cap total capacity; every pJ/bit the interconnect saves is a watt returned to compute (§9.13).

The bottleneck did not replace the previous one; it stacked on top. A modern cluster is simultaneously memory-bandwidth-bound in decode, network-bound in collectives, and power-bound at the site. The interconnect sits at the intersection of the last two, which is why this book treats optics as infrastructure rather than as a module datasheet exercise.

## AI clusters are communication machines

An accelerator does useful work only while its operands arrive on time. Model parallelism spreads weights, activations, and expert routing across many devices, so the fabric repeatedly moves partial results between otherwise fast compute engines. Three traffic patterns set the pressure:

All-reduce

: combines partial results across a group and returns the result to every member. The slowest path can hold the whole group at the synchronization point (§9.7).

All-to-all

: moves different payloads between every pair, as in mixture-of-experts routing. It tests bisection bandwidth, queueing, and path balance rather than one peak link rate.

Point-to-point

: carries pipeline stages and storage or memory traffic. Tail latency and retries can matter more than average throughput.

More compute increases the amount of traffic the system can inject. It does not increase fabric capacity. Once links or switches saturate, accelerators wait at collectives and realized compute use falls. Public large-model training data show why this is also an availability problem: network faults are only one failure bucket, but a synchronous job pays for every interruption across the whole allocation . Compute scales faster than communication unless the network, optics, and software are designed as one system.

## The systems engineering loop

Work from the system downward:

::: center
[Requirements]{.smallcaps}\
$\downarrow$\
[Architecture]{.smallcaps}\
$\downarrow$\
[Subsystem]{.smallcaps}\
$\downarrow$\
[Component]{.smallcaps}\
$\downarrow$\
[Needed physics]{.smallcaps}
:::

A component choice is never isolated. A VCSEL usually commits the link to an 850 nm multimode path, direct modulation, and a short reach. A 1310 nm DFB points toward single-mode fiber and can feed a DML, EML, Mach--Zehnder modulator, or ring. Those paths then set detector material, fiber plant, thermal control, test coverage, and service policy. Start with reach, lane rate, power, cost, lifetime, and manufacturing volume. Choose the component only after those constraints rule out the other paths.

##### Validation reduces uncertainty.

Characterization asks what the design does across its operating range. Margin testing asks how close it is to a limit. Environmental and life testing ask which mechanisms move with temperature, stress, and time. Production testing asks whether process variation and assembly escapes can be caught at useful test cost. A passing result is useful only when the test answers one of those questions (Chapter 7, Chapter 8).

##### Margin erodes before the link fails.

Power, noise, timing, and spectral margins usually move a little at a time. A connector adds loss, a laser loses slope efficiency, a bias point drifts, and a ring moves toward the edge of its lock range. No single change must be large. Their sum pushes normal unit and temperature variation across the BER threshold. Track margin as a ledger over temperature, lot, age, and workload rather than as one room-temperature pass/fail point.

##### Debug by eliminating hypotheses.

First scope the failure: one unit, one lot, one vendor, one site, or the fleet. Then classify its pattern: sudden or gradual, constant or temperature-dependent, power-related or signal-quality-related. Choose the next measurement for its ability to separate competing causes. The debugging pyramid below gives the order; the failure-analysis handbook in Chapter 10 gives the symptom-led procedures.

## Engineering lens

### How it works

The interconnect carries partial results between accelerators, and collectives make the slowest link set the pace for the whole job. At AI scale the optical layer is the dominant medium between racks, so its bandwidth, latency, and uptime become the cluster's bandwidth, latency, and uptime.

### How it is measured

At the system level: step time, collective latency, accelerator idle fraction, and tail behavior. At the link level: pre-FEC BER, FEC error distribution, optical power, module temperature, and flap count. At the architecture level: delivered bandwidth per watt, link count, and FIT-weighted availability (§7.12, §5.13).

### How it fails

Fabric capacity can fall behind injected traffic. A single marginal link can stall a synchronous collective. Connector contamination, laser aging, thermal excursions, and firmware mismatches all reduce margin invisibly until the workload crosses the cliff. Service errors during expansion (polarity, cleaning, fiber routing) are a common source of day-one failures.

### How it is debugged

Use the debugging pyramid: start at the system symptom, narrow to signal quality, walk the link budget, bisect the subsystem, then identify the physical root cause. Do not skip layers.

## The debugging pyramid

When a link fails, work from the top down. Each layer narrows the search before you open a connector or reseat a module. This framework reappears in every chapter.

Layer 1: System

: What is failing at the workload level? BER, throughput, latency, training instability, collective stall. Start here because the symptom often rules out entire subsystems.

Layer 2: Signal quality

: What changed in the signal? Eye opening, jitter, noise, equalization margin, FEC error distribution. These are what the host and module already report (§7.8, §7.12).

Layer 3: Link budget

: Where did margin disappear? Optical power, receiver sensitivity, insertion loss, extinction ratio, ORL. Walk the ledger from transmitter to receiver (§7.7).

Layer 4: Subsystem

: Which block is responsible? Laser, modulator, driver, photodiode, TIA, DSP, connector, fiber, or host SerDes. Bisect with loopbacks and golden swaps (§7.10, §7.9).

Layer 5: Physical root cause

: What mechanism explains the failure? Aging, contamination, thermal stress, process variation, assembly defect, calibration error, firmware bug. This is where you open FA or 8D (§8.10).

Do not skip layers. A direct jump to root cause without first confirming the system symptom and localizing the subsystem wastes weeks on the wrong part. The pyramid is a discipline, not a checklist: each layer produces a measurement that either confirms or falsifies the hypothesis before you descend.

## Interview and design review questions

##### Concept.

- Why does optics become favorable over copper at higher data rates?

- What distinguishes a communication-limited system from a compute-limited one?

- Why does a synchronous collective amplify single-link failures?

##### Design.

- What traffic pattern sets the requirement: all-reduce, all-to-all, or a latency-sensitive point-to-point path?

- What is the measured bottleneck: SerDes reach, switch radix, fiber count, module power, cooling, or collective efficiency?

- Why does passive copper, a direct-attach cable, or an active electrical cable not close the required reach and rate?

- Does a pluggable, linear pluggable, or co-packaged engine move risk into a domain the team can test and service?

##### Debug.

- Training throughput dropped after scaling. Where in the debugging pyramid (§1.8) do you start?

- How do you distinguish a network bottleneck from a compute or memory bottleneck using only host-visible telemetry?

- What data would show that added optical bandwidth does not improve job time?

##### Manufacturing and operations.

- What failure rate per link is acceptable given the total link count and the target job uptime?

- How does the service model (hot-swap vs board pull) change the architecture?

- What is the fleet cost of a wrong triage classification?

## How to read this book

The chapters build from requirements to fleet operation:

1.  Chapter 2, Chapter 3: energy, IM/DD vocabulary, architecture, modulators, FEC, and equalization.

2.  Chapter 4: quantitative noise, RIN, sensitivity (use with §7.7).

3.  Chapter 5: requirements-led source and modulation decisions, measurement, aging, and service architecture.

4.  Chapter 6: wavelength locking, thermal crosstalk, CW-WDM, on-chip MUX.

5.  Chapter 7, Chapter 8: measurement ladder, link budgets, qual, packaging.

6.  Chapter 9: scale-up/out, pluggables, CPO/XPO, inference collectives.

7.  Chapter 10: symptom-led root-cause isolation and corrective action.

To use the book as a design drill, pick one link style (retimed 800G DR, LPO, or CPO WDM) and trace it end to end through §3.2, §9.3, §9.10.

**Key idea.** Start from the system requirement and work downward. Validate to reduce uncertainty, track how several small losses consume margin, and debug by choosing measurements that eliminate hypotheses.


<div class="nav-links">
  <a href="ch0-preface">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch2-first-principles-the-energy-of-moving-a-bit">Next &rarr;</a>
</div>
