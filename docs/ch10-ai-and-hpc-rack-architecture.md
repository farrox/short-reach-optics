---
layout: default
title: "Ch 10: AI and HPC Rack Architecture"
---

# 10 AI and HPC Rack Architecture

This chapter is the design judgment home for short-reach AI and HPC fabrics: how workload shapes topology, what fat-tree and Clos actually buy, how oversubscription and rails change optics count, and how to walk a rack design on a whiteboard. Protocol surveys, OCS programs, power tables, and module-style catalogs stay in Appendix H. Packaging of optical engines is in Chapter 9. Productization closes the fleet claim in Chapter 11.

*Read first:* fat-tree / Clos, bisection bandwidth, oversubscription, rails, and scale-up versus scale-out.

*Deep dive:* topology survey in Appendix H.2; collectives in Appendix H.7; OCS in Appendix H.9; energy and thermal envelopes in Appendix H.13, Appendix H.13.1.

**Key idea.** A fat tree buys path diversity and bisection bandwidth, but it costs switch radix, cables, optics, and power. The first fabric question is which collective pattern and failure domain you are designing for, not which topology name is fashionable.

## Workload characteristics

Before you draw a Clos, name the traffic.

All-reduce

: Every rank contributes; every rank needs the result. Bandwidth and synchronization both matter. Stragglers set job time.

All-to-all

: Dense exchange across ranks. Stresses bisection and wiring symmetry more than a single reduction tree.

Parameter / gradient exchange

: Often periodic and synchronized across a training step. Many links go busy at once.

Incast

: Many senders hit one receiver or one switch uplink. Creates congestion even when average utilization looks modest.

Burstiness

: Idle then full-rate. Average link load understates peak demand on optics and FEC.

Stragglers and tail latency

: The slowest hop or the slowest rail stalls the collective. Tail, not mean, sets iteration time.

Optical count follows from how many parallel planes you build to keep those patterns from colliding. Deeper optics-to-collective mapping is in Appendix H.7.

## Fat-tree and Clos

A *fat-tree* is a folded *Clos* network: leaf (or ToR) switches face accelerators or servers; spine switches interconnect the leaves; aggregate bandwidth grows toward the upper layers when the design is nonblocking.

Core ideas:

Leaf / ToR

: Edge switch with downlinks to compute and uplinks toward the fabric.

Spine

: Upper-tier switches that provide path diversity across leaves.

Equal-cost paths

: Multiple routes between endpoints; load can spread.

Path diversity

: A single leaf or spine failure need not partition the cluster if radix and wiring allow alternate paths.

Bisection bandwidth

: The worst-case cut capacity between two equal halves of the fabric. Collective-heavy jobs care about this number.

### A leaf-scale example

Suppose:

- 32 leaf switches;

- 32 accelerator-facing ports per leaf;

- 32 uplinks per leaf, at the same speed as the downlinks.

At each leaf the downstream offered bandwidth equals the upstream fabric bandwidth: a 1:1 leaf. Subject to spine connectivity, the fabric can approach nonblocking behavior for that leaf tier. The full fat tree still needs enough spine ports and enough cables to realize that promise across all leaves.

### Why a full fat tree gets expensive

Nonblocking Clos fabrics multiply:

- switch count and radix;

- cable and optical module count;

- power and cooling;

- management and failure domains.

In a classic $k$-ary fat-tree sketch, endpoints scale roughly as $O(k^2)$ while links scale faster (Appendix H.2). Optics multiply faster than GPUs. That is why oversubscription, rails, and dragonfly-style hierarchies appear as cost controls, not as fashion.

## Oversubscription

Define oversubscription as the ratio of offered downstream bandwidth to available upstream fabric bandwidth: $$\begin{equation}
\text{oversubscription}
=
\frac{\text{downstream offered bandwidth}}
{\text{upstream fabric bandwidth}}.
\label{eq:oversub}
\end{equation}$$

1:1

: Upstream matches downstream at the named tier. Expensive; kind to synchronized collectives.

2:1

: Upstream is half of downstream. Cheaper; can still work if traffic is not fully concurrent across all downlinks.

Traffic dependence

: A sparse pattern may never stress the cut. A synchronized all-reduce can.

Average utilization misleads

: Links that idle most of the time can still collide on the step boundary. Design for the collective peak you claim, not for the daily mean.

Interview line: "I state the tier and the traffic pattern before I call an oversubscription ratio acceptable."

<table class="book-table"><tr><th>Ratio</th><th>Often survivable when</th><th>Hostile when</th></tr><tr><td>1:1</td><td>Synchronized collectives claimed</td><td>Cost or radix cannot close</td></tr><tr><td>2:1</td><td>Traffic rarely fully concurrent</td><td>All-reduce across all downlinks</td></tr><tr><td>>2:1</td><td>Strong locality / scheduling</td><td>Job sold as nonblocking bisection</td></tr></table>
## Rail-optimized design

A *rail* is an independent network plane. Rail-optimized designs give each accelerator multiple NICs (or ports) and assign one port to each rail so that collectives can stripe or stay within a plane.

Why rails appear in AI fabrics:

- They reduce shared failure domains: one rail fault need not take every path.

- They support topology-aware collectives that keep heavy traffic inside a rail.

- They raise optical count: more parallel planes mean more modules, fibers, and lasers.

Rails are not free diversity. They are an explicit purchase of parallelism and isolation against more optics and more ToR radix.

## Scale-up versus scale-out

Scale-up

: Inside a node, tray, rack, or tightly coupled domain. Very high bandwidth, very low latency, stronger ordering or coherence needs, short reach. Copper still competes; CPO and short-reach optics are entering as lane rates rise (Appendix H.1, Chapter 9).

Scale-out

: Across racks or clusters. Routable fabric, more hops, fault tolerance and congestion control, optical dominance for reach beyond a meter-class copper wall.

Do not treat "the fabric" as one network. Many AI clusters run a scale-up plane and a scale-out plane with different optics, FEC, and failure models (Appendix H.1).

## Rack-level design exercise

Worked prompt (guide numbers):

> Design a rack with 64 accelerators, eight accelerators per tray, eight 800G network links per tray, and two independent network rails.

Walk the whiteboard in this order. Numbers below are a consistent sketch, not a vendor BOM.

### Inventory

- Accelerators: 64.

- Trays: $64/8 = 8$ trays.

- Network links per tray: 8 at 800G each $\Rightarrow$ 6.4 Tb/s of network attach per tray if all links are active.

- Rack network attach: $8\times 6.4 = 51.2$ Tb/s aggregate endpoint bandwidth before oversubscription toward spines.

- Rails: 2. A natural split is 4 links per tray per rail (still 8 links per tray total), so each rail carries half the tray attach if balanced.

### Switch radix and ToR placement

Questions to close:

- Are ToRs in-tray, mid-rack, or end-of-row?

- How many downlinks per ToR versus uplinks to spine?

- Does each rail have its own ToR set, or do ToRs fan into both rails?

Example sketch: one ToR per tray per rail (16 ToRs if fully separated), each seeing 4$\times$800G down from its tray half and a chosen uplink ratio to spine. A shared-ToR sketch uses fewer switches and couples the rails in the failure domain. Say which one you mean.

### Links, optics, and cables

Count:

- Endpoint-facing 800G ports: $8\text{ trays}\times 8 = 64$ ports (one per named network link in the prompt).

- Uplinks: set by oversubscription. At 1:1 from those 64 ports you need 64 same-speed fabric ports toward the next tier; at 2:1 you need 32.

- Optics versus copper: inside the rack, DAC/ACC may still close short tray-to-ToR runs; rack-to-spine and rack-to-rack are usually optical (Appendix H.3, Appendix H.5).

Module count is not optional arithmetic. It sets FIT, power, and sparing (Chapter 11, Appendix H).

### Power, cooling, fiber, serviceability

- Power: sum accelerator, ToR, optics, and fans or pumps. Optics power is small next to GPUs but large next to a naive "ignore modules" budget (Appendix H.13).

- Liquid cooling: cold plates and manifolds constrain ToR and fiber routing; do not place optics where service needs a dry teardown of the cooling loop.

- Fiber routing: trunk versus breakout, polarity, and which plane is which rail. Mis-patched rails look like fabric bugs.

- Serviceability: hot-swap pluggables versus CPO engines versus ELSFP laser banks (Chapter 9, §7.14). Match the replaceable unit to the FIT story.

### Tradeoffs, not a winner

Valid answers disagree on ToR count, oversubscription, and copper versus optics inside the rack. A strong answer states the binding constraint (collective bisection, cost, service, or power) and shows what was sacrificed. A weak answer crowns one vendor rack photo as universal.

## Fat tree versus dragonfly

<table class="book-table"><tr><th>Topic</th><th>Fat-tree / Clos</th><th>Dragonfly-class</th></tr><tr><td>Hop count</td><td>Often more hops at scale</td><td>Fewer global hops by design</td></tr><tr><td>Global links</td><td>Many equivalent uplinks</td><td>Fewer long global links</td></tr><tr><td>Wiring</td><td>Regular, cable-heavy</td><td>Hierarchical, wiring-sensitive</td></tr><tr><td>Routing</td><td>ECMP-friendly</td><td>Needs careful global routing</td></tr><tr><td>Congestion</td><td>Localize with enough bisection</td><td>Global links can hotspot</td></tr><tr><td>Failure domains</td><td>Path diversity if provisioned</td><td>Global-link loss hurts more</td></tr><tr><td>Scalability</td><td>Radix and cost limited</td><td>Grows with hierarchy</td></tr><tr><td>Collectives</td><td>Strong when bisection is real</td><td>Pattern-dependent</td></tr></table>
Use dragonfly when long-global-link cost dominates and the routing stack is ready. Use fat-tree when you want regular ECMP behavior and will pay for bisection. Survey context: Appendix H.2.

## Optical switches in the fabric

Optical circuit switches sit at Layer 1: they rearrange connectivity without O-E-O packet processing (Appendix H.9). On a whiteboard:

- They help topology and failure reroute on millisecond-class timescales.

- They do not replace a packet switch for fine-grained congestion control.

- They change the transceiver plant (reach, power, connectors) more than they change SerDes EQ theory.

Say whether the OCS is a spine substitute, a patch-panel replacement, or a maintenance plane before you claim power savings.

## Whiteboard debug vignette

Prompt: "Jobs stall on all-reduce. Average link utilization is 25%. The fabric team says the Clos is fine. Walk the debug."

1.  Name the plane: scale-up or scale-out, which rail, which tier.

2.  Compare collective-period peaks to averages; look for incast and synchronized steps.

3.  Check bisection and oversubscription at the leaf-to-spine cut, not only at the NIC.

4.  Ask whether rails are truly independent or share ToRs and trunks.

5.  Separate optics/FEC faults from topology thinness (Chapter 12, Appendix H.7).

6.  Only then propose more spines, less oversubscription, or collective schedule changes.

Weak answers blame "optics" or "buy a bigger switch" without naming the cut. Strong answers rename the bottleneck before changing hardware.

## Interview takeaway

**Key idea.** I start from the collective and the failure domain. I size bisection and oversubscription at a named tier, decide how many rails I am buying, split scale-up from scale-out, then close a rack sketch with port count, optics count, power, and serviceability. Topology names come after those numbers.

## Interview Q&A

Practice aloud. Prefer first-person reasoning. Score with Appendix A.12.1.

##### Question 1. Explain a fat tree.

*Tests:* Clos structure and why it exists.

*Spoken answer.* "A fat tree is a folded Clos: leaves face compute, spines interconnect leaves, and aggregate bandwidth grows upward when the design is nonblocking. You buy path diversity and bisection bandwidth. You pay switch radix, cables, optics, and power."

*Pressure follow-up.* "Is every Clos a fat tree?"\
*Answer pivot.* "Fat tree usually means the folded Clos form used in datacenters. Clos is the broader switching idea."

*Trap:* "Fat tree means every link is optical."

##### Question 2. What is bisection bandwidth?

*Tests:* worst-case cut capacity.

*Spoken answer.* "Bisection bandwidth is the capacity across the worst cut that splits the fabric into two equal halves. Collective-heavy jobs care because many patterns push traffic across that cut. Average link utilization can look fine while bisection is the bottleneck."

*Pressure follow-up.* "How do you increase it?"\
*Answer pivot.* "More spine bandwidth, less oversubscription, or a topology that places heavy flows on richer cuts. All cost optics and switches."

*Trap:* "Bisection is the sum of all link speeds in the cluster."

##### Question 3. When is oversubscription acceptable?

*Tests:* pattern dependence.

*Spoken answer.* "Oversubscription is acceptable when the claimed traffic cannot fully load the downstream tier at once, or when the job can tolerate congestion and retries. Synchronized all-reduce across all downlinks is the hostile case. I name the tier and the pattern before I accept 2:1."

*Pressure follow-up.* "Our monitoring shows 20% average utilization."\
*Answer pivot.* "Averages miss step-boundary bursts. I ask for collective-period peaks and incast events."

*Trap:* "Any oversubscription is fine if mean utilization is low."

##### Question 4. Walk a 64-accelerator rack design.

*Tests:* structured rack arithmetic.

*Spoken answer.* "Sixty-four accelerators, eight per tray, gives eight trays. Eight 800G links per tray is 64 endpoint network ports and 51.2 Tb/s of attach if all run. With two rails I split planes and failure domains. Then I choose ToR count, uplink oversubscription, copper versus optics inside the rack, power, fiber routing, and what is field-replaceable."

*Pressure follow-up.* "What is the first number you refuse to guess?"\
*Answer pivot.* "Whether the eight links are scale-up, scale-out, or mixed, and whether rails are fully independent ToR planes."

*Trap:* "Just copy a public 64-GPU reference rack."

##### Question 5. How do you choose switch radix?

*Tests:* ports, tiers, and cost.

*Spoken answer.* "Radix sets how many downlinks and uplinks a switch can land. Higher radix can flatten the fabric and cut hops, but the ASIC, optics, and power get harder. I choose radix from endpoint count, target tiers, and the oversubscription I can afford, not from the largest switch on a slide."

*Pressure follow-up.* "Why not one giant switch for the rack?"\
*Answer pivot.* "Radix, blast radius, and serviceability. One chassis failure takes more of the rack."

*Trap:* "Always pick the highest-radix switch available."

##### Question 6. Optical versus copper inside a rack?

*Tests:* reach wall and service.

*Spoken answer.* "Inside a rack, short tray-to-ToR runs may still close on DAC or ACC. Past about a meter-class copper wall at high lane rates, or when density and cable bulk hurt, optics win. Rack-to-rack is usually optical. I check reach, SI, power, and whether hot-swap pluggables matter (Appendix H.5, Appendix H.3)."

*Pressure follow-up.* "Copper is always cheaper."\
*Answer pivot.* "Per meter maybe. Per delivered rack bandwidth after reach fails, optics can be cheaper and smaller."

*Trap:* "AI racks are all-optical everywhere."

##### Question 7. Why multiple rails?

*Tests:* isolation and collective striping.

*Spoken answer.* "Rails buy independent planes so collectives can stripe and so one fault does not share every path. The cost is more NICs, more ToR ports, and more optics. I only buy rails I can wire, name, and monitor."

*Pressure follow-up.* "Are two rails enough?"\
*Answer pivot.* "Enough for the failure model and collective schedule you claim. More rails help until optics count and radix dominate."

*Trap:* "More rails always improve job time."

##### Question 8. How do you design failure domains?

*Tests:* blast radius thinking.

*Spoken answer.* "I ask what one failed ToR, spine, rail, optical engine, or fiber trunk takes down. Then I align redundancy: dual rails, dual uplinks, spare optics, and repair procedures. Packaging choices change the replaceable unit (Chapter 9)."

*Pressure follow-up.* "We have ECMP, so we are fine."\
*Answer pivot.* "ECMP needs surviving alternate capacity. A shared-risk link group can still take both paths."

*Trap:* "Fat tree automatically means no single points of failure."

##### Question 9. How does topology interact with all-reduce?

*Tests:* bisection and synchronization.

*Spoken answer.* "All-reduce wants enough bisection and predictable latency across ranks. Oversubscription and hot spines create stragglers. Rail-aware collectives can keep traffic inside a plane. I design topology and collective library together, not as separate teams' afterthoughts (Appendix H.7)."

*Pressure follow-up.* "Can software fix a thin bisection?"\
*Answer pivot.* "Software can schedule and compress. It cannot create missing cut bandwidth."

*Trap:* "Collectives are a software problem; topology only sets hop count."

##### Question 10. Where do optical circuit switches fit?

*Tests:* OCS role versus packet switching.

*Spoken answer.* "OCS rearranges Layer 1 connectivity. It can cut O-E-O hops for topology or failure reroute on millisecond scales. It is not a packet switch for per-flow congestion. I place it only when the control plane and transceiver plant match that job (Appendix H.9)."

*Pressure follow-up.* "Does OCS replace CPO?"\
*Answer pivot.* "No. CPO shortens the electrical path at the package. OCS changes how packages interconnect. They can coexist."

*Trap:* "OCS means we can use dumb optics and no FEC."

##### Question 11. Scale-up versus scale-out?

*Tests:* two networks, two optics stories.

*Spoken answer.* "Scale-up is the short, high-bandwidth, low-latency domain inside a node or rack. Scale-out is the routable cluster fabric across racks. They differ in reach, protocol, FEC, and optics. I never answer a rack question until I know which plane the links belong to (Appendix H.1)."

*Pressure follow-up.* "Can one 800G port do both?"\
*Answer pivot.* "Sometimes in product marketing. In design I still budget them as different jobs if latency and reach targets differ."

*Trap:* "Scale-up and scale-out are just marketing synonyms."

##### Question 12. What power and thermal constraints matter?

*Tests:* rack envelope realism.

*Spoken answer.* "Accelerators dominate watts, but switches and optics still move the rack envelope and the service model. Liquid cooling constrains where ToRs and fiber can sit. On-package optics add local hotspots near ASICs (Appendix H.13, Appendix H.13.1, Chapter 9). I close power and cooling before I freeze port count."

*Pressure follow-up.* "Optics are only a few percent of rack power."\
*Answer pivot.* "True at fleet scale sometimes, but optics still set shoreline density, repair load, and whether the copper reach closes."

*Trap:* "If the GPUs fit the PDU, the network fits too."

##### Question 13. Give a 60-second fabric plan.

*Tests:* end-to-end judgment order.

*Spoken answer.* "I start from the collective and the failure domain. I split scale-up from scale-out. I size bisection and oversubscription at each tier, decide rail count, sketch the rack with port and optics counts, choose copper versus optics by reach, and I state power, cooling, and replaceable units. Topology names come after those numbers."

*Pressure follow-up.* "Schedule is cut. What do you protect?"\
*Answer pivot.* "Claimed collective bisection, rail independence if we sold it, and a serviceable optics story. Cosmetic oversubscription savings come last."

*Trap:* "Pick fat tree, buy the biggest switch, and tune later."


<div class="nav-links">
  <a href="ch9-advanced-packaging-for-optical-engines">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-productization-from-requirements-to-controlled-ramp">Next &rarr;</a>
</div>
