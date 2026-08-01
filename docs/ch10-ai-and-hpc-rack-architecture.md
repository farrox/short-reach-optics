---
layout: default
title: "Ch 10: AI and HPC Rack Architecture"
---

# 10 AI and HPC Rack Architecture

This chapter is the design judgment home for short-reach AI and HPC fabrics: how workload shapes topology, what fat-tree and Clos actually buy, how oversubscription and rails change optics count, and how to walk a rack design on a whiteboard. Protocol surveys, OCS programs, power tables, and module-style catalogs stay in Appendix H. Packaging of optical engines is in Chapter 9. Productization closes the fleet claim in Chapter 11.

*Read first:* fat-tree / Clos, bisection bandwidth, oversubscription, network rails, and scale-up versus scale-out.

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

: Idle then full-rate. Burstiness stresses buffers, congestion control, and collective completion time. It does not raise the instantaneous line rate on an already-active fixed-rate optical PHY, but it can expose traffic-dependent PHY weaknesses: simultaneous-switching noise, thermal excursions, marginal adaptation, or clustered FEC errors.

Stragglers and tail latency

: The slowest hop or the slowest network rail stalls the collective. Tail, not mean, sets iteration time.

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

In a conventional $k$-ary three-stage fat tree, both host count and physical link count scale as $O(k^3)$. The usual construction has hosts $k^3/4$, edge-to-host links $k^3/4$, edge-to-aggregation links $k^3/4$, and aggregation-to-core links $k^3/4$. The economic pressure is not a different asymptotic exponent. It is the large number of switch ports, cable ends, and optical endpoints required per host.

Concrete sketch for $k=32$: about $32^3/4 = 8192$ hosts and about $3\times 8192 = 24576$ bidirectional network link attachments across the three tiers (plus the host-edge tier). That is tens of thousands of cable ends and optical endpoints before oversubscription or multi-rail multiplication (Appendix H.2). Oversubscription, network rails, and dragonfly-style hierarchies appear as cost controls on that constant-factor burden, not as fashion.

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

A *network rail* is a topology-aligned path group, commonly formed from corresponding NIC ports across nodes. Rails may be physically independent, or they may share switches, trunks, control planes, power, or software. The designer must state the actual shared-risk boundaries. (Do not confuse a network rail with an electrical supply rail.)

Rail-optimized designs give each accelerator multiple NICs (or ports) and assign one port to each network rail so collectives can stripe or stay within a plane.

Why network rails appear in AI fabrics:

- They can reduce shared failure domains when the planes do not share risk.

- They support topology-aware collectives that keep heavy traffic inside a rail.

- They raise optical count: more parallel planes mean more modules, fibers, and lasers.

Network rails are not free diversity. They are an explicit purchase of parallelism and (claimed) isolation against more optics and more ToR radix. If ToRs or trunks are shared, say so.

## Scale-up versus scale-out

Scale-up

: Inside a node, tray, rack, or tightly coupled domain. Very high bandwidth, very low latency, short reach. It may impose stronger ordering, memory-semantic, or coherence requirements depending on the interconnect. Copper still competes; CPO and short-reach optics are entering as lane rates rise (Appendix H.1, Chapter 9).

Scale-out

: Across racks or clusters. Routable fabric, more hops, fault tolerance and congestion control, optical dominance for reach beyond a meter-class copper wall.

Do not treat "the fabric" as one network. Many AI clusters run a scale-up plane and a scale-out plane with different optics, FEC, and failure models (Appendix H.1).

## Rack-level design exercise

Worked prompt (guide numbers):

> Design a rack with 64 accelerators, eight accelerators per tray, eight 800G network links per tray, and two network rails (state shared-risk boundaries).

Walk the whiteboard in this order. Numbers below are a consistent sketch, not a vendor BOM.

### Inventory

- Accelerators: 64.

- Trays: $64/8 = 8$ trays.

- Network links per tray: 8 at 800G each $\Rightarrow$ 6.4 Tb/s of network attach per tray if all links are active.

- Rack network attach: $8\times 6.4 = 51.2$ Tb/s aggregate endpoint bandwidth before oversubscription toward spines.

- Network rails: 2. A natural split is 4 links per tray per rail (still 8 links per tray total), so each rail carries half the tray attach if balanced. State whether the rails share ToRs or trunks.

## From rack bandwidth to an optical architecture

The inventory above stops at attach bandwidth. The optical-engineering decision starts here. Keep one consistent sketch; change an assumption only if you rename it.

##### 1. Collective and bisection target.

Assume the rack must support synchronized all-reduce across both network rails without intentional leaf-to-spine oversubscription on the claimed plane. That sets a 1:1 starting point; a cost cut to 2:1 is a named sacrifice, not a silent default.

##### 2. Endpoint ports and uplinks.

Sixty-four 800G endpoint-facing ports give 51.2 Tb/s of attach. At 1:1 you need 64 same-speed uplink ports toward the next tier; at 2:1 you need 32. State which tier owns that ratio.

##### 3. Optical link endpoints, not merely ports.

If tray-to-ToR and ToR-to-spine are both discrete optical links, 64 downlink links imply about 128 optical endpoints, and 64 uplink links imply another about 128. Copper DAC on the short side deletes endpoints there. CPO on the switch side can fold an endpoint into an engine. The lesson is to count terminations, not only ASIC port stickers (§10.8.2).

##### 4. Lanes and wavelengths per 800G.

A common short-reach sketch is $8\times100$G PAM4 lanes (electrical) into an 800G DR8-class or similar optical PMD, or $4\times200$G PAM4 as lane rates rise. Parallel SMF (DR) multiplies fibers; WDM (FR) multiplies wavelengths on fewer fibers (Chapter 8, Appendix H.3). Pick one and keep fiber and laser counts consistent.

##### 5. PAM format and baud.

For this sketch stay on PAM4 unless a named reach or SerDes generation forces a baud cut that PAM8 might buy (Chapter 4). PAM8 is preferable only when the saved baud closes electrical or optical bandwidth that PAM4 cannot, and when SNR, linearity, and calibration still close. Do not choose PAM8 to sound denser.

##### 6. Reach class and EQ ownership.

Tray-to-ToR may be copper or short optics. ToR-to-spine and rack-to-rack set VSR/MR versus longer optics. Retimed pluggables keep heavy EQ in the module; LPO pushes EQ and FEC onto the host SerDes; CPO shortens to XSR at the package (Chapter 5, §3.7, Appendix H.5.1). Name who owns CTLE, FFE, DFE, and KP4 for each hop.

##### 7. Pluggable, LPO, or CPO.

Use pluggables when faceplate serviceability dominates. Use LPO when module DSP power is the binding constraint and host EQ/FEC are proven. Use CPO when shoreline density and SerDes energy dominate and package yield/thermal/service stories are closed (Chapter 9, Table H.4). A mixed rack (copper inside, optics out) is a valid answer if the reaches match.

##### 8. Lasers, fibers, watts, replaceable units.

From the lane/wavelength choice, count lasers or CW lines, FAU or MPO fibers, and module or engine watts (Appendix H.13, Chapter 7). Prefer ELSFP-class external lasers when CPO engines are soldered and laser FIT still dominates (§7.14). State the field-replaceable unit: pluggable, laser bank, fiber jumper, or whole package.

##### 9. Fleet event rate and degraded-rack behavior.

Module and laser count set FIT exposure and sparing. Ask what one failed rail, ToR, or trunk does to job completion, and whether the rack runs degraded or drains (Chapter 11, Chapter 12). Topology that looks cheap per port can be expensive per fleet event.

Worked memory: collective $\rightarrow$ ports $\rightarrow$ endpoints $\rightarrow$ lanes/$\lambda$ $\rightarrow$ PAM/baud $\rightarrow$ EQ owner $\rightarrow$ placement $\rightarrow$ lasers/watts $\rightarrow$ replaceables and degraded behavior.

## Finishing the rack sketch

Return to the same 64-accelerator sketch. Close switch placement, optics count, power, and the tradeoffs you will defend.

### Switch radix and ToR placement

Questions to close:

- Are ToRs in-tray, mid-rack, or end-of-row?

- How many downlinks per ToR versus uplinks to spine?

- Does each rail have its own ToR set, or do ToRs fan into both rails?

Example sketch: one ToR per tray per rail (16 ToRs if fully separated), each seeing 4$\times$800G down from its tray half and a chosen uplink ratio to spine. A shared-ToR sketch uses fewer switches and couples the rails in the failure domain. Say which one you mean.

### Links, optics, and cables

Keep the counting vocabulary separate:

Switch ports

: Faces on a ToR or NIC ASIC. The prompt names 64 endpoint-facing 800G ports ($8\text{ trays}\times 8$).

Link pairs

: Complete connections between two ports. Sixty-four complete optical links normally imply 128 optical endpoints unless one side is integrated into an engine or package.

Optical endpoints

: Module or engine faces that terminate light.

Pluggable modules / optical engines

: Field-replaceable or soldered units that may host one or more endpoints.

Lanes / wavelengths

: Electrical or optical channels inside an 800G port.

Fiber count

: Physical strands after breakout and polarity.

Uplinks: set by oversubscription. At 1:1 from those 64 ports you need 64 same-speed fabric ports toward the next tier (another 64 links and, if both ends are discrete optics, another 128 optical endpoints). At 2:1 you need 32 uplink ports. Inside the rack, DAC/ACC may still close short tray-to-ToR runs; rack-to-spine and rack-to-rack are usually optical (Appendix H.3, Appendix H.5).

Module and endpoint count is not optional arithmetic. It sets FIT, power, and sparing (Chapter 11, Appendix H). Carry the same sketch into §10.7.

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

- They operate on circuit-reconfiguration timescales, not packet timescales. The useful transition can range from fast protection switching to scheduled topology changes, depending on the device and on the surrounding control plane and link-recovery path.

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

##### Question 7. Why multiple network rails?

*Tests:* isolation and collective striping.

*Spoken answer.* "Network rails are topology-aligned path groups, often matching NIC ports. They can buy striping and failure isolation, but only if I state what they share: switches, trunks, control, power, or software. The cost is more NICs, ToR ports, and optics. I only buy rails I can wire, name, and monitor."

*Pressure follow-up.* "Are two rails enough?"\
*Answer pivot.* "Enough for the failure model and collective schedule you claim. More rails help until optics count and radix dominate."

*Trap:* "More rails always improve job time," or treating a rail as automatically an independent physical plane.

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

*Spoken answer.* "OCS rearranges Layer 1 connectivity. It can cut O-E-O hops for topology change or protection, but the reconfiguration timescale depends on the switch device, control plane, and link recovery, from fast protection to scheduled topology change. It is not a packet switch for per-flow congestion. I place it only when the control plane and transceiver plant match that job (Appendix H.9)."

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

##### Question 13. From 64$\times$800G attach to an optical architecture?

*Tests:* rack-to-PHY bridge.

*Spoken answer.* "I start from the collective and bisection target, then count endpoint ports and 1:1 versus 2:1 uplinks. I convert ports to optical link endpoints, pick lanes and wavelengths per 800G, decide PAM4 versus PAM8 and baud, name EQ ownership by hop, choose pluggable, LPO, or CPO, then close lasers, fibers, watts, replaceable units, and degraded-rack behavior (§10.7)."

*Pressure follow-up.* "Why not stop at port count?"\
*Answer pivot.* "Ports are stickers. Endpoints, lasers, and replaceables set FIT, power, and service."

*Trap:* "64 ports means 64 optical modules."

##### Question 14. Give a 60-second fabric plan.

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
