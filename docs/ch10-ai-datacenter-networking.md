---
layout: default
title: "Ch 10: AI datacenter networking"
---

# 10 AI datacenter networking

Optics only make sense once you see the fabric they sit in. Training and inference clusters are not one network; they are several overlapping networks with different bandwidth, latency, and reach needs. This chapter places the devices and validation methods from earlier chapters into that system context: how AI clusters are wired, why the interconnect sits on the inference critical path, and where optics dominates cost and power.

## Scale-up versus scale-out

The industry borrowed two words from computer architecture and overloaded them for AI fabrics. Keeping them straight matters, because they buy different optics.

Scale-up

: tight coupling inside a node or rack: GPU-to-GPU over a memory-semantic fabric (for example NVLink). Very high bandwidth, very low latency. Increasingly optical as bandwidth outgrows copper reach.

Scale-out

: coupling across racks and pods over a switched network (Ethernet or InfiniBand). This is where pluggable and co-packaged optics have long lived.

<figure id="fig:scale-node" data-latex-placement="ht">
<embed src="figures/fig_scale_up_node.pdf" />
<figcaption>Schematic AI compute node (one tray in a larger cluster). <em>Accelerators</em> are the heavy compute engines (typically GPUs; the book also uses XPU for GPUs and custom ASICs). <strong>Scale-up</strong> links (red) tie accelerators through a high-bandwidth, low-latency switch fabric inside the node or rack (NVLink-class). <strong>Scale-out</strong> links (blue) leave via a dedicated NIC per accelerator into the datacenter Ethernet or InfiniBand fabric. The CPU and front-end NIC handle host, storage, and management traffic.<span id="fig:scale-node" data-label="fig:scale-node"></span></figcaption>
</figure>

### Three networks, two that set the optics budget

The OIF CEI-448G framework names *three* distinct networks in a large AI cluster . §10.1 shows two; the third is easy to overlook:

Scale-up

: accelerator-to-accelerator inside a pod or rack. Highest bandwidth per link, lowest latency, often lossless. Dominates compute time if under- provisioned.

Scale-out

: accelerator-to-accelerator (or node-to-node) across the cluster over a switched fabric (InfiniBand, *UEC*/Ethernet with RoCE or Ultra Ethernet Transport). Lower per-link bandwidth than scale-up, but must reach $10^5$+ endpoints.

Front-end

: CPU-attached traffic: management, control plane, checkpointing, storage, and training-data ingest. Analogous to a conventional cloud datacenter network; not the IM/DD bottleneck this book focuses on, but it shares the same rack power and cabling budget.

Scale-up carries the majority of *interconnect* bandwidth inside a training job; scale-out multiplies link count across the building. That is why both push 448G-class lane rates and why optics shows up first on scale-out, then on scale-up as copper reach shrinks .

### Scale-up versus scale-out at a glance

Table 10.1 condenses OIF Table 1 (CEI-448G framework, §2.2): order-of- magnitude targets for node count, physical extent, and media type . Numbers are industry snapshots, not hard limits, but they explain why "optics inside the rack" and "optics between racks" arrive on different timelines.

<table class="book-table"><tr><th></th><th>2cScale-up</th><th>2cScale-out</th><th></th><th></th></tr><tr><td>(lr)2-3(lr)4-5 Metric</td><td>Today</td><td>Next gen</td><td>Today</td><td>Next gen</td></tr><tr><td>Accelerator nodes in domain</td><td>100</td><td>1\,k</td><td>100\,k+</td><td>100\,k</td></tr><tr><td>Physical extent</td><td>Rack</td><td>Rack to row</td><td>Datacenter</td><td>Datacenter</td></tr><tr><td>Network properties</td><td>2p0.34Lossless, low latency</td><td>2p0.34Large scale; multi-tier switching</td><td></td><td></td></tr><tr><td>Media within rack</td><td>2p0.34Electrical: passive PCB / twinax backplane</td><td>2p0.34Electrical: twinax backplane</td><td></td><td></td></tr><tr><td>Media between racks</td><td>AEC (adjacent racks)</td><td>Optical (within row)</td><td>2p0.34Optical (pluggable or CPO on switch/NIC)</td><td></td></tr></table>
**Table 10.1.** Scale-up vs. scale-out snapshots (adapted from OIF CEI-448G framework Table 1, 2025). Scale-up stays on copper as long as rack densification keeps channels short; scale-out is already optical at datacenter scale.

### Standards bodies: who owns what

448G/lane signaling is not owned by one standards body, and that is by design. Electrical reach, Ethernet naming, connectors, and rack packaging evolved in different rooms; AI fabrics forced them to meet at the same lane rate. OIF's CEI-448G framework (§2.3) lists the groups that must align . Table 10.2 maps each body to the layer an optical engineer actually touches. The short version: OIF sets the electrical baud and reach classes; IEEE names the Ethernet optical PMD; UALink and UEC own scale-up and scale-out protocol stacks; SNIA and OCP decide connectors and where the optics physically live. The *LPO MSA* is not a standards body, but it publishes the only open end-to-end spec that stitches CEI Linear electrical limits to IEEE optical PMD limits for DSP-less modules (§10.3.1). Prose below expands each row, OIF and non-OIF.

<table class="book-table"><tr><th>Body</th><th>Fabric</th><th>What matters for short-reach optics</th></tr><tr><td>OIF CEI</td><td>All reaches</td><td>Electrical PHY: XSR/VSR/MR/LR, 448G PAM4/6/8, LPO/LRO; CMIS for module management</td></tr><tr><td>UALink</td><td>Scale-up</td><td>Open load/store pod fabric; 200G/lane today, 400G/lane next; drives XSR-class PHY needs</td></tr><tr><td>UEC</td><td>Scale-out</td><td>Ultra Ethernet Transport, congestion control; PHY group surveying 400G/lane enhancements</td></tr><tr><td>SNIA SFF</td><td>Host / backplane</td><td>Cables, connectors, PCIe/EDSFF form factors; SFF 448G COM for backplane (complements CEI front-panel work)</td></tr><tr><td>OCP</td><td>Rack / system</td><td>Open rack designs, CPO/XPO placement, optical circuit switching (OCS) for AI clusters</td></tr><tr><td>IEEE 802.3</td><td>Scale-out (+ optics PMD)</td><td>Ethernet MAC rates (802.3dj, 400G/lane SG), KP4 FEC, IM/DD PMD clauses (DR/FR, TDECQ)</td></tr><tr><td>100G Lambda MSA</td><td>Scale-out optics</td><td>Originated the 100G/ single-mode PMDs (100G-FR/LR, 400G-DR4/FR4/LR4) later folded into IEEE 802.3; RIN_xOMA transmitter method the DR/FR and LPO specs inherit</td></tr><tr><td>IBTA</td><td>Scale-out</td><td>InfiniBand Architecture; NDR 400G, XDR 800G/port at 200G/lane, 1.6T switch links; reuses QSFP/OSFP + MPO optics with Ethernet</td></tr><tr><td>IEEE 802.1</td><td>All fabrics</td><td>Link-layer security: MACsec (802.1AE) line-rate encryption; 802.1X port access control</td></tr><tr><td>PCI-SIG / CXL</td><td>Scale-up, in-node</td><td>PCIe 7.0 (128 GT/s PAM4) and CXL 4.0 memory fabric; PCI-SIG Optical Workgroup for optical PCIe</td></tr><tr><td>DMTF / OpenConfig / SONiC</td><td>Management</td><td>Box and fleet telemetry and config (Redfish, OpenConfig, SONiC); complement OIF CMIS module management</td></tr></table>
**Table 10.2.** SDO and consortium roles at 448G/lane. The top six rows follow OIF CEI-448G §2.3; the 100G Lambda MSA, IBTA, IEEE 802.1, PCI-SIG/CXL, and the management stack are added for coverage beyond OIF's own list.

##### OIF.

Common Electrical I/O (*CEI*) Implementation Agreements are the modular electrical PHY recipes: die-to-die (*XSR*), chip-to-module (*VSR*), chip-to-chip (*MR*), and backplane (*LR*). CEI-448G is the current AI-driven push beyond 224G/lane . Related OIF tracks include energy-efficient interfaces (EEI), CMIS management extensions at 448G, and coherent DCI (out of scope for this book). For optics, CEI tells you the *baud and reach* the module or CPO engine must meet; IEEE 802.3 tells you how Ethernet names the optical PMD.

##### UALink Consortium.

*UALink* specifies an open *scale-up* stack (transaction, data link, and physical layers) optimized for direct accelerator memory access, not IP/Ethernet . UALink 1.0 targets 200G/lane and pods up to roughly 1 k accelerators; the physical-layer working group is gathering requirements for $\sim$400G/lane. Optical engineers care because higher lane rate reduces port count on the accelerator package, and because scale-up eventually hits the same copper reach wall as CEI XSR (§10.5).

##### Ultra Ethernet Consortium.

*UEC* builds a complete Ethernet-based stack for AI/HPC *scale-out*: transport (UET), link layer, and PHY enhancements . UEC 1.0 (June 2025) targets cluster-scale congestion control and RDMA-class performance over standard Ethernet hardware, including NICs, switches, optics, and cables. The PHY working group is surveying 400G/lane improvements. This is the protocol layer above the transceiver; IM/DD module specs still come from IEEE and MSAs.

##### SNIA (SFF Technology Affiliate).

SNIA's SFF working group defines connectors, cables, and form factors for storage and compute backplanes, not front-panel Ethernet . The SFF 448G project (SFF-TA-1043) parallels CEI-448G but focuses on backplane COM, package insertion loss, and PAM choice on copper channels inside the box. Pair OIF VSR (module connector) with SFF (host PCB and PCIe cable) when debugging a link budget.

##### Open Compute Project.

OCP publishes open rack, server, and networking designs for hyperscale . Relevant work includes Open Systems for AI, short-reach optical interconnect guidelines, and the Optical Circuit Switching (OCS) subproject (2025) for reconfigurable cluster fabrics. OCP rarely specifies baud rate; it specifies *where* the optical engine lives (faceplate pluggable vs. CPO vs. XPO) and how it is cooled and serviced.

##### IEEE 802.3.

Ethernet standards define MAC rates, FEC (KP4 in Clause 91), and interoperable optical PMDs . 802.3dj (200G/lane) and the 400G/lane study group name the product generations that consume 224G and 448G-class optics. One naming trap: IEEE quotes **400 Gb/s per lane** (MAC/info rate); CEI quotes **$\sim$448 Gb/s** (line rate with coding overhead). Same physics, different accounting (Chapter 3, §3.6).

##### 100G Lambda MSA.

The single-mode PMDs this book leans on did not start at IEEE. The *100G Lambda MSA*, formed in 2017 by a broad group of suppliers and hyperscalers, wrote the first interoperable optical specifications built on one wavelength carrying 100 Gb/s PAM4 ($\approx$53 GBd): 100G-FR and 100G-LR for single-wavelength 100 GbE, and 400G-DR4/FR4/LR4 for four-lane 400 GbE over duplex single-mode fiber . IEEE 802.3 then adopted the same 100 Gb/s-per-$\lambda$ approach into its DR/FR/LR PMD clauses, and the LPO MSA 100G-DR-LPO profile (§10.3.1) inherits both that modulation and the RIN$_x$OMA transmitter method the MSA defined (§4.3). For a short-reach engineer this is the body behind the reach-class names on almost every single-mode datasheet: when a module is called "DR4" or "FR4," the per-wavelength recipe traces to this MSA even where the compliance point is now quoted against an IEEE clause.

##### InfiniBand Trade Association.

The *IBTA* maintains the InfiniBand Architecture Specification, the other dominant scale-out fabric for AI and HPC alongside Ethernet . Data rates follow the same per-lane SerDes ladder: NDR reaches 400 Gb/s per port over four 100 Gb/s lanes, and XDR reaches 800 Gb/s per port over four 200 Gb/s lanes, with switch-to-switch links at 1.6 Tb/s (XDR figures are from the 2023 spec announcement and remain provisional). For the optical engineer the physical layer is close to the Ethernet case: the same QSFP and OSFP form factors, the same MPO fiber, and DR/FR-class IM/DD optics at matching lane rates. InfiniBand changes the transport and congestion model (credit-based flow control, RDMA), not the transceiver. It is absent from the OIF §2.3 list because IBTA runs its own specification, but it occupies the same scale-out slot as UEC.

##### IEEE 802.1 (link-layer security).

Encryption is a link-layer function, and at 800G and 1.6T it has to run at line rate. *MACsec* (IEEE 802.1AE) provides connectionless confidentiality, frame integrity, and data origin authenticity at the MAC layer, transparent to the MAC client; IEEE 802.1X handles port access control and the key agreement that establishes MACsec associations . This lands on optics indirectly: line-rate MACsec costs latency and gate count in the switch ASIC or NIC, not in the transceiver, and an LPO or DSP-less module carries the ciphertext transparently. Encryption is therefore orthogonal to the optical PMD choice (§10.3.1), but it belongs in the standards map because a fabric-security requirement can still gate a module program at qualification.

##### PCI-SIG and CXL.

Inside the node, the load-store fabric is PCI Express and *CXL*. PCI-SIG released PCIe 7.0 in 2025 at 128 GT/s per lane using PAM4 and flit encoding, and the CXL Consortium built CXL 4.0 on that same PCIe 7.0 electrical base for coherent memory pooling . Both are 2025 releases, so treat the exact rates and the optical-interface scope as provisional. Both are copper-first and short today, but PCI-SIG runs an Optical Workgroup defining a technology-agnostic optical PCIe interface, and CXL memory disaggregation across a rack is exactly the reach that pulls optics into a bus that was never optical before. For a short-reach optics team this is the emerging in-node and in-rack case to watch: PAM4 at PCIe rates over fiber, with the same modulator and detector problems as an Ethernet lane.

##### Management and telemetry.

Module management is OIF CMIS (Appendix E.7), but the box and fleet layers above it are not OIF. *DMTF Redfish* is the RESTful standard for server and switch management and telemetry; *OpenConfig* defines vendor-neutral data models and streaming telemetry (gNMI) for network devices; and *SONiC* is the open network operating system many hyperscalers run, with its own dataplane telemetry hooks . These are where per-module CMIS monitors surface as fleet signals: optical power, case temperature, FEC symbol-error counts, and pre-FEC BER aggregated across $10^5$ links (Chapter 8, §10.17.6). A module program that ships without a telemetry contract into one of these systems is effectively invisible at fleet scale.

The frontier is optics entering the scale-up domain (optical NVLink-class links, co-packaged switches), because copper reach at 200G/lane is only about a meter.

## Topologies and why optics count explodes

Cluster topology is where optical count stops being "a few modules per server" and becomes a fleet problem. Large AI fabrics mostly use fat-tree / Clos, rail-optimized, or dragonfly layouts. In a classic $k$-ary fat-tree, link count scales as $O(k^3)$ while endpoints scale as $O(k^2)$: optics multiply faster than compute. Rail-optimized designs (one NIC rail per accelerator row, all-to-all within a rail) rose with collective-heavy training and inference because they cut oversubscription on all-reduce paths, at the price of more parallel optical planes. Dragonfly and other hierarchical topologies trade some global bisection bandwidth for fewer long links.

The optical engineer cares because every topology choice sets link count, which sets laser count, module count, and FIT budget (Chapter 8); rail layouts drive fan-out from leaf to spine and push denser 800G/1.6T ports toward CPO/XPO (§10.10, §10.11); and scale-up inside the rack stays electrical longer while scale-out between racks is already optical (Table 10.1). That explosion in link count is the economic reason a hyperscaler builds an in-house optical engineering team.

## Pluggable form factors and module styles

Faceplate modules differ in aggregate rate, lane count, electrical reach, and where the DSP lives. The form factor sets the passive channel the SerDes must survive, and the last decade of AI networking has mostly been a fight over that choice: keep a retimer in the module for interop, delete it for watts (LPO/LRO), or move the optics onto the package (CPO) and service the laser from the faceplate (ELSFP).

QSFP-DD / OSFP

: the incumbent datacom pluggables. QSFP-DD carries 800G/1.6T class products (eight lanes at 100G or 200G per lane). OSFP targets higher power and density (1.6T today, 3.2T roadmaps) with a larger cage and better thermal path. Both impose a VSR-class electrical channel from host PCB through the connector (§10.5, §10.5.1).

Retimed module

: DSP/CDR inside the module (§3.6). Default for interoperability; $\sim$15--20 W class at 800G/1.6T.

LPO / LRO

: linear or lightly retimed: delete or slim module DSP (§10.5.1, §3.14.3, §3.6, §3.2). Power drops to $\sim$7--9 W but host EQ and transmitter and dispersion eye closure quaternary (TDECQ) margin tighten.

ELSFP / external laser

: field-replaceable CW source for CPO (§10.10, Chapter 5): decouples laser FIT from switch FIT.

XPO

: liquid-cooled mega-pluggable (§10.11): 12.8 Tb/s per module, front-panel serviceability with CPO-class density.

*CMIS* (Appendix E.7) is the management layer for module identity, monitors, and (at 224G/448G) link-training and host-side signal-integrity tuning extensions. Optical engineers touch it when debugging lock, FEC, and equalizer settings across vendors.

##### Half-retimed and asymmetric modules.

Not every pluggable is fully retimed or fully linear. Common 2025--26 variants sit between those poles:

LPO

: linear drive and linear receive: no module DSP/CDR (§3.6, §3.14.3).

LRO / RTLR

: retimed transmit, linear receive (OIF RTLR): DSP on electrical $\to$ optical only; eases host TX while keeping a simpler RX path .

TRO / half-retimed

: symmetric opposite or partial retiming variants appear in vendor roadmaps; always check which direction carries the DSP.

Fully retimed

: DSP both directions; default for interoperability at 800G/1.6T.

Power scales with DSP content: retimed $\sim$15--20 W, LRO $\sim$9 W, LPO $\sim$7--9 W at 800G class (§10.13). The architecture choice is a trade between host margin (COM, TDECQ) and module watts.

### The LPO MSA: stitching IEEE optics to CEI Linear

OIF CEI tells you the electrical recipe at the module cage. IEEE 802.3 tells you how Ethernet names the optical PMD and its TDECQ/OMA limits. Neither document, by itself, is a complete product spec for a linear pluggable that deletes the module DSP. The *LPO MSA* (Linear Pluggable Optics Multi-Source Agreement) fills that gap: one open specification for both sides of the module, with normative test points and host responsibilities spelled out .

The first published revision, *100G-DR-LPO* (v1.0, March 2025), targets 100 Gb/s per lane at 53.125 GBd PAM4 on single-mode fiber from 0.5 m to 500 m. It is explicitly a data-center profile: low power, low latency, high port density, RS(544,514) FEC on the host, and form-factor agnostic (QSFP, QSFP-DD, OSFP are examples, not the spec). The naming pattern generalizes to `n00G-DRn-LPO` for $n\in\{1,2,4,8\}$ lanes. Optical reach and modulation track IEEE DR-class PMDs; the electrical interface tracks OIF CEI-112G-LINEAR-PAM4. That split is the template 224G linear modules follow: CEI-224G-Linear on the AUI, 802.3dj optical PMD limits on the fiber (§3.14.2, §3.13).

##### Who owns which block.

In an LPO link the host is not a passive cable driver. It runs KP4 FEC (§3.12), full SerDes equalization (CTLE, FFE, DFE, CDR; §3.6, §3.7), and optional nonlinear compensation (NLC) and startup protocol functions. The module is analog: linear driver, modulator or laser, photodiode, TIA, and at most a fixed CTLE. No retiming, no FEC, no heavy DSP. CMIS (Appendix E.7) is the management contract. SFF hardware specs (QSFP-DD, OSFP cages) set the mechanical envelope. The MSA's job is to define what must pass at each interface between those blocks so modules from different vendors close on the same host.

> **Tradeoff.** Retimed module vs LPO host burden
>
> *Improves:* Module watts and faceplate density when DSP leaves the module
>
> *Worsens:* Host SerDes margin, equalization depth, and interop risk on every platform
>
> *When acceptable:* When host channels and thermal budgets are proven for the linear path
>
> *Experienced decision:* Pay for retimers when host margin is the scarce resource; delete them when watts dominate and the host can own EQ and FEC.

##### The test-point ladder.

LPO MSA normative compliance is organized around six electrical/optical test points (§10.3), the concrete instance of the general TP0-to-TP5 planes in §3.9. Think of them as the validation script: host TX at TP1a, module optical TX at TP2, stressed optical RX at TP3, module electrical RX at TP4, and stressed host RX at TP4a. Section 10 of the MSA adds a host-to-host end-to-end BER test with FEC-encoded traffic, which is how you prove interop after the point tests pass.

<table class="book-table"><tr><th>Point</th><th>Location</th><th>Principal measurements</th></tr><tr><td>TP1a</td><td>Host SerDes output</td><td>EECQ (electrical eye closure), host TX quality</td></tr><tr><td>TP1</td><td>Module electrical input</td><td>Module input stressor calibration</td></tr><tr><td>TP2</td><td>Optical TX (2--5 m patch cord)</td><td>TDECQ, TECQ, OMA_outer, RIN_xOMA, ER</td></tr><tr><td>TP3</td><td>Optical RX input</td><td>Stressed receiver calibration (SECQ), sensitivity masks</td></tr><tr><td>TP4</td><td>Module electrical output</td><td>Module RX linear output (EECQ)</td></tr><tr><td>TP4a</td><td>Stressed host input</td><td>Host RX under worst-case module output</td></tr></table>
##### Optical limits that matter.

The MSA optical tables (Appendix E.3, Chapter 7) inherit IEEE 802.3 measurement methods with LPO-specific reference equalizers. The numbers you will quote in a datasheet review:

- TDECQ and TECQ capped at 3.4 dB per lane, measured with a 9-tap T-spaced reference FFE and SER target $4.0\times10^{-4}$.

- OMA$_{\mathrm{outer}}$ coupled to transmitter quality: launch power in OMA rises with max(TECQ, TDECQ) along a piecewise mask (for example $-3.2 + \mathrm{max}(\mathrm{TECQ},\mathrm{TDECQ})$ dBm in the mid-TECQ region).

- RIN$_{x\mathrm{OMA}} \le -138$ dB/Hz at 17.2 dB ORL (the "$x$" subscript tracks return loss, same convention as IEEE DR PMDs).

- Illustrative link budget 6.7 dB total at 500 m (3 dB channel loss plus 0.3 dB MPI penalty plus 3.4 dB TDECQ allocation). Do not stack that TDECQ allocation on a SECQ-stressed sensitivity that already embeds Tx quality.

- Stressed receiver sensitivity $-3.1$ dBm OMA$_{\mathrm{outer}}$ at TP3 with SECQ = 3.4 dB and aggressor lanes at 4.2 dBm OMA.

TECQ is TDECQ without the dispersion test fiber. The MSA uses both because outer OMA limits are written against max(TECQ, TDECQ), and a module can be fiber-limited even when the electrical eye looks clean.

##### Electrical limits and host COM.

On the electrical side the MSA points to CEI-112G-LINEAR-PAM4 for the host-to-module interface and defines EECQ (electrical eye closure quaternary) at TP1a and TP4a. That is the electrical analogue of TDECQ: a host that passes optical TDECQ at TP2 but fails EECQ at TP1a still will not interoperate. Host PCB insertion loss, connector, and module input return loss sit in the channel reference model (Section 7). For 224G deployment, swap CEI-112G-LINEAR for CEI-224G-Linear and run the same two-ledger program (§3.14.2, §10.5.2).

##### What to read first.

For a bring-up engineer the reading order is: Section 5 (system overview and host FEC requirements), Section 7 (electrical TPs and channel model), Section 8 (optical TX/RX tables), Section 9 (parameter definitions, especially 9.5 TDECQ/TECQ and 9.10 stressed RX), then Section 10 (host-to-host FEC BER). Cross-check every optical definition against the cited IEEE 802.3 clause; the MSA adds reference equalizer taps and SER targets, not new physics.

**Key idea.** OIF owns the electrical baud at the cage. IEEE owns the optical PMD metrics on the fiber. The LPO MSA is the product contract that binds them for DSP-less modules: normative test points, host FEC/EQ duties, and TDECQ/OMA masks you can test without a module retimer safety net.

### The LPO supplier base and the adoption question

The MSA defines what a linear module must pass; it does not settle whether the market buys one. By 2025--26 the supplier base had formed around the analog parts that replace the DSP: high-linearity TIAs and linear drivers. Macom, Semtech, and Maxlinear are the named component proponents, and once the DSP is gone the TIA and driver become the make-or-break blocks .

The demonstrations track a fast rate climb. Eoptolink showed a 200G/$\lambda$ four-channel LPO link with no DSP or CDR at OFC 2024 and moved a second-generation 100G/lane 800G and 400G single-mode line into volume, claiming full TP2 compliance at the transmit interface . Macom exhibited its PURE DRIVE 200 Gb/s LPO parts at OFC 2024 and extended them toward 212 Gb/s/lane for a 1.6T module, with the TIA and driver as the headline . Marvell, a DSP house, announced a 200G/lane TIA and laser-driver chipset for 800G and 1.6T LPO aimed at scale-up XPU fabrics . Macom and Eoptolink are founding members of the LPO MSA (§10.3.1).

**LPO reaches into PCIe scale-up.** Alphawave and Innolight demonstrated a 64 Gb/s/lane PCIe 6.0 subsystem (controller plus PHY) over Innolight's LPO OSFP optics at OFC 2024, then a 128 Gb/s/lane platform pairing a PCIe 7.0-ready SerDes PHY with the same optics . The pull is the switch-fabric pull again: larger, faster AI nodes need more PCIe reach than copper gives, and the linear module skips the DSP latency and power a retimed module would add (§10.1, §10.12).

**Whether LPO wins is a separate question.** Host support exists: Juniper's Broadcom-based QFX switches take LPO optics without hardware changes, and Arista has shown Broadcom TH5 compatibility for over two years . The market read is still cautious. Cignal AI argues LPO stays a small share, at least at 800G, because the installed fabric was already designed around DSP-based modules; 100G/lane (800GbE) LPO looks late and likely to hold only a small slice long term . At 200G/lane and 1.6T the balance tips toward LRO: early 1.6T LPO parts draw more than 30 W, a thermal problem at faceplate density (§10.13.1), while a transmit-DSP LRO design promises under 20 W with easier integration and interop . Cignal notes that every vendor showing 1.6T LPO at OFC also showed an LRO part . That matches the book's technical read: LPO and LRO win where the host electrical channel and TDECQ close without the module DSP, and lose where they do not (§3.14.2, §10.5.1).

## Emerging link styles

The form-factor list above is the present. The industry argument for 2025--26 is where the DSP and the laser should live next. Retimed pluggables remain the interop default: a module DSP cleans the electrical channel, at the cost of watts. LPO and LRO delete or slim that DSP so the host SerDes carries more of the EQ burden, which is attractive for AI power budgets and painful for margin and interop. CPO moves the optical engine onto the switch or XPU substrate to cut electrical reach, and usually keeps the laser external and field-replaceable (ELSFP/CW-WDM). XPO appeared in 2026 as a middle path: a much larger, liquid-cooled pluggable that keeps front-panel serviceability while pushing density toward CPO territory (§10.11). The rest of this chapter treats electrical reach, eye budgets, and vendor CPO programs as consequences of that argument.

## The electrical link: reach, conditioning, and the eye budget

Every form factor above is really an answer to one physical question: *how far can the electrical signal travel before it is cheaper (in power and dB) to convert to light?* As the per-lane rate climbs, that distance collapses, and it is what pushes the optics from the faceplate toward the die.

**Trace loss scales with frequency.** A PCB stripline's insertion loss grows roughly with $\sqrt{f}$ (skin effect) plus a dielectric term linear in $f$, so it is quoted per inch *at the Nyquist frequency*. Going from 112G to 224G PAM4 moves Nyquist from 28 GHz to 56 GHz, and the loss per inch roughly doubles. Recent 224G board studies measure $\approx2.8$ dB/inch for regular stripline and $\approx1.9$ dB/inch with skip-layer routing at 56 GHz, against a next-generation *target* of 1 dB/inch that demands ultra-low-loss dielectric, HVLP copper, and short via stubs . §10.2 shows the consequence: at a fixed PCB-trace budget, doubling the baud rate roughly halves the copper reach.

<figure id="fig:traceloss" data-latex-placement="ht">
<embed src="figures/fig_trace_loss.pdf" />
<figcaption>PCB trace insertion loss versus length at each rate’s Nyquist. The reach to a fixed budget shrinks from <span class="math inline">∼ 10</span> inches (112G) to a few inches (224G), which is why the optical conversion must move closer to the ASIC.<span id="fig:traceloss" data-label="fig:traceloss"></span></figcaption>
</figure>

**The CEI channel classes name the reaches.** OIF's Common Electrical I/O project defines the electrical link budgets the whole industry designs to. Table 3.8 is the CEI-224G lookup card (XSR / VSR / MR / LR, plus Linear for DSP-less modules); the reach map is §3.5. At 56 GHz Nyquist the same names mean much shorter copper than at 112G :

XSR

: *XSR*: die-to-die / die-to-engine: the shortest, lowest-power tier, the one CPO and chiplet optics live in ($\lesssim$50 mm package).

VSR

: *VSR*: chip-to-module: $\approx$200 mm of host plus 20 mm of module and one connector: the classic pluggable channel.

MR

: *MR*: chip-to-chip across a board: $\approx$500 mm, one connector, $\sim$32--34 dB die-to-die.

LR

: *LR*: backplane or copper cable: $\approx$1000 mm of host and daughter cards, two connectors, up to $\sim$40 dB die-to-die (including a 1 m cable).

Linear

: *CEI-224G-Linear*: same faceplate-class ports without a module DSP/CDR; the electrical foundation for LPO (§3.14.2, §10.3).

##### Active copper: ACC, AEC, and DAC.

Passive direct-attach copper (DAC) survives only where the reach is short: at 224G a passive DAC is good for roughly $0.5$--$1$ m (strong 224G PHYs have demonstrated 2 m). *ACC* adds redrivers (CTLE + VGA) in the cable; *AEC* adds retimers (EQ + CDR) and stretches twinax to $\sim$2.5 m at higher power (§10.5.1, §3.6) . Beyond that, and increasingly *within* the rack for scale-up, the answer is optics (Table 10.1).

##### Co-packaged and near-package copper: copper moves inward too.

Optics is not the only thing the reach wall pushes toward the package. *CPC* (co-packaged copper) mates a copper cable or connector directly onto the ASIC package substrate, and *NPC* (near-package copper) places that connector just outside the package on the socket. Both leave the host at the package edge and skip the lossy PCB run to the faceplate, where most of the trace budget in §10.2 is spent. The move mirrors CPO: shorten the electrical path until the channel closes, but keep the signal in copper instead of converting it to light.

On-substrate copper has been validated at 224G-PAM4 with a stated roadmap to 448G, and compression substrate connectors now target 224 Gb/s PAM4 and beyond . Inside its reach, copper keeps the properties that make it the default: a long-reach 224G SerDes into a CPC cable runs near 4 pJ/bit with no electro-optic conversion, adds less latency than a retimed optical hop, and costs less per lane. Passive co-packaged copper reaches about a meter at 448G-PAM4 under optimistic connector assumptions (§3.14.3), enough to cover many scale-up links inside a rack or between adjacent racks.

Past that wall the conversion to light pays for itself. When the reach exceeds what a clean substrate channel can carry, or the port count makes copper bulk and cabling weight unmanageable, optics takes the link (Table 10.1). CPC and NPC do not remove that crossover; they move it, buying copper one more rate generation before the optics win. Read the placement ladder in Table 10.4 from the copper side and this is the same trade seen in reverse.

**So the optics march inward.** Shortening the electrical path is exactly what trades power and reach for serviceability, the through-line of this chapter. Table 10.4 lays out the ladder from faceplate to interposer.

<table class="book-table"><tr><th>Placement</th><th>Host electrical reach</th><th>Energy/bit</th><th>Serviceability</th></tr><tr><td>Pluggable (faceplate)</td><td>full VSR host run (200 mm) + connector</td><td>highest (>30 pJ/bit w/ DSP; less for LPO)</td><td>hot-swap at faceplate (best)</td></tr><tr><td>On-board optics (OBO / COBO)</td><td>shorter mid-board trace</td><td>lower</td><td>board-level (solder/socket); largely bypassed for CPO</td></tr><tr><td>Near-packaged (NPO)</td><td>engine beside the ASIC on substrate</td><td>lower still</td><td>module on substrate; limited</td></tr><tr><td>Co-packaged (CPO)</td><td>mm-scale die-to-engine (XSR)</td><td><5 pJ/bit</td><td>soldered; ELSFP lasers field-replaceable</td></tr><tr><td>Optical I/O on interposer</td><td>on-die / interposer</td><td><2 pJ/bit</td><td>not field-serviceable (emerging)</td></tr></table>
**Table 10.4.** The optics-placement ladder. Moving the electro-optic conversion inward cuts trace loss and energy per bit but erodes field serviceability, the central tension behind pluggables, OBO/NPO, CPO (§10.10), and the XPO middle ground (§10.11). A mid-board fiber connector can shift breakage risk from the costly engine to a cheap jumper.

**On-board optics: the step the industry mostly skipped.** OBO (standardized by the *Consortium for On-Board Optics*, COBO) moves the optical engine off the faceplate and onto the main PCB, cutting the copper run without abandoning silicon photonics . It works, but it gives up hot-plug serviceability while only partly closing the power gap, so with CPO maturing, most hyperscalers are leapfrog­ping OBO/NPO straight to co-packaging, keeping serviceability via field-replaceable lasers (§10.10) and the XPO pluggable hedge (§10.11).

**The die-to-die interface is a standard too.** At the innermost tier (Table 10.4), the electrical hand-off between chiplets is increasingly set by *UCIe* (Universal Chiplet Interconnect Express), an open die-to-die interconnect whose 2.0 revision (August 2024) added 3D packaging and in-field manageability, with a 3.0 revision roughly doubling bandwidth in 2025 . UCIe is the parallel counterpart to CEI XSR: XSR is a serial die-to-OE link, while UCIe carries wide parallel lanes across a package or interposer. It reaches optics because co-packaged engines and optical-I/O chiplets attach to the compute die over a UCIe port, and optical-UCIe proposals aim to carry that traffic over fiber instead of a few millimeters of substrate. The chiplet-protocol and packaging detail sits outside this book's scope; the point for short reach is that the die-to-die interface, copper or optical, sets the shortest reach an optical engine must beat.

### Reshaping, retiming, and where the DSP lives

To survive that lossy channel the signal is conditioned at several points (§3.6), and it helps to keep two device classes distinct.[^36]

Redriver

: an analog *reshaper/amplifier*: a *CTLE* plus a VGA. It sharpens and boosts the eye but has *no* clock recovery, so it cannot reset accumulated jitter; it adds almost no latency. This is the active element in active copper cables (ACC) and on host boards used to stretch a marginal trace.

Retimer

: adaptive EQ *plus* a *CDR* that re-samples and regenerates the data. It breaks the channel into independent jitter/loss segments, at the cost of power and per-hop latency. Retimers sit in active electrical cables (AEC) and in fully retimed modules (Broadcom's Agera is a host retimer).

Inside the optical module the traditional "cleanup" is a full DSP (retimer $+$ FEC engine). The retimed-to-linear spectrum trades exactly cleanup for power and latency:

Fully retimed

: DSPs in both directions: least sensitive to *ISI*/dispersion, but highest power ($\sim$14--18 W/module at 800G) and most latency ($\sim$8--10 ns/hop).

LPO (linear)

: *LPO*: *no* DSP or CDR in either direction: only a CTLE in the TIA and a linear driver, so the host SerDes must do all the *FFE*/CTLE equalization *and* carry the FEC. Lowest power ($\sim$7--9 W), lowest latency ($<$3 ns), but most ISI/dispersion-sensitive and shortest reach ($<$2 km) .

LRO / TRO (retimed TX, linear RX)

: DSP only on the electrical$\to$optical path, roughly half the power, sensitivity, and latency, with easier interop.

So yes: reshapers/amplifiers (redrivers) and retimers are routinely placed on the host path, and the module's own DSP is the last line of cleanup. The entire LPO bet (§10.13, §3.14.2) is to *delete* those active stages and let the host SerDes' CTLE/FFE carry the channel, trading electrical margin for power and latency.

### The electrical eye: acceptable voltage and noise

What must the signal actually look like where it hands off to the module? The CEI-224G reference and draft numbers set the envelope . Differential swing sits roughly in the 0.36--1.05 V~ppd~ band (reference TX near 1 V peak-to-peak differential; lossier channels use the larger swing). Transmitter *SNDR* ($\mathrm{SNR_{TX}}$) is about 33 dB: the transmitter's own noise-plus-distortion ceiling. PAM4 level uniformity needs $\mathrm{RLM}\ge0.95$ (1.0 = perfectly even eyes). Jitter budgets are tight: random $\approx$0.01 *UI* rms and bounded/uncorrelated $\approx$0.02 UI pk. The go/no-go metric that folds those pieces together is *COM* (channel operating margin) $\ge3$ dB: a statistical SNR of the fully equalized link (§10.5.2).

##### Jitter and level uniformity.

At 112 GBd, 1 UI $\approx$8.9 ps; 0.01 UI rms jitter is $\sim$90 fs rms. Random jitter adds vertical eye closure; deterministic jitter (ISI, crosstalk) shows up in bathtub curves and COM. *RLM* $\ge0.95$ keeps the three PAM4 eyes even; poor RLM wastes vertical margin the same way excess TDECQ does on the optical side (Appendix E.3).

Retimers reset jitter per segment; redrivers do not. That is why long ACC chains accumulate timing budget stress while AEC segments stay independent (§10.5, §10.5.1).

Here is the number that reframes "acceptable noise." After the reference receiver's equalizer (an 8-tap *DFE*), the eye at the slicer is only about $4$--$10$ mV tall and $\sim$0.06 UI wide, with $\sim$11--14 dB of vertical eye closure, at a *pre-FEC* error rate near $10^{-4}$. The channel is deliberately driven deep into ISI and closed nearly shut; *KP4* FEC (pre-FEC $2.4\times
10^{-4}$ to post-FEC $10^{-15}$, Chapter 4) is what turns that into a working link. "Acceptable," then, is not a clean open eye; it is whatever keeps COM $\ge3$ dB and the pre-FEC BER under the KP4 threshold. It is also why the optics must present a clean, highly linear interface, especially for LPO: with only a few mV of margin, any added noise or nonlinearity from the driver or TIA comes straight off COM.

##### Channel operating margin (COM) in one page.

*COM* is the electrical go/no-go statistic for CEI-class channels: after the reference transmitter, channel, and receiver (CTLE + 8-tap DFE) are applied, COM is the SNR margin at the slicer, in dB. COM $\ge3$ dB is the usual pass line (§10.5.2, §3.6).

COM connects directly to optics because the module is the last analog segment before FEC. A retimed module can absorb some host-channel sin; LPO cannot (§10.3, §3.14.3). When COM is tight, debug in this order: host TX SNDR and RLM, connector return loss, equalizer tap saturation, then module input swing and TIA noise (§4.5, Chapter 4).

Optical-side analogs are not identical: TDECQ scores the transmitter with a reference equalizer; SECQ stresses the receiver (Appendix E.3, Appendix E.4). Think of COM as the *electrical* counterpart to those optical margin tests.

**Key idea.** Electrical reach is the hidden clock behind form factors. Trace loss per inch roughly doubles from 112G (28 GHz) to 224G (56 GHz), collapsing copper reach to a few inches on-board and $\sim$1 m in cable. Each step inward (pluggable, OBO, NPO, CPO, on-interposer optical I/O) buys power and reach and spends serviceability. The signal is held together by redrivers (reshape), retimers (reclock), and DSPs (both), which LPO deletes, inside a brutal budget: $\sim$1 V~ppd~ in, 33 dB TX SNDR, COM $\ge3$ dB, and a post-equalizer eye of only a few mV rescued by FEC.

## The two phases of inference, revisited

Chapter 1 introduced prefill and decode; here is why they matter for the network.

Prefill

: compute-bound and highly parallel: crunches the whole prompt through every layer at once.

Decode

: memory-bandwidth-bound and autoregressive: one token at a time, streaming all weights each step. The *KV cache* (scaling with batch $\times$ context length) is a major and growing memory consumer.

**Why decode is memory-bandwidth-bound.** It comes down to *arithmetic intensity*, FLOPs performed per byte read from memory. Each weight matrix $W\in\mathbb{R}^{d_\text{out}\times d_\text{in}}$ costs $d_\text{out}d_\text{in}$ parameters to read. In decode you generate one token, so every layer is a matrix--*vector* product (GEMV): about $2\,d_\text{out}
d_\text{in}$ FLOPs against $2\,d_\text{out}d_\text{in}$ bytes of FP16 weights, i.e. each weight is used once and discarded: $$\text{AI}_\text{decode}\;\approx\;
\frac{2\,d_\text{out}d_\text{in}}{2\,d_\text{out}d_\text{in}}
\;=\;1\ \text{FLOP/byte}.$$ Prefill instead pushes $N$ prompt tokens through the *same* weights at once, a matrix--matrix product (GEMM) that reuses each loaded weight $N$ times, so $\text{AI}_\text{prefill}\approx N$ FLOP/byte. On a roofline this is decisive: an H100 delivers $\sim$1000 TFLOP/s FP16 on $\sim$3.35 TB/s of HBM, so its balance point sits at $$\frac{1000\times10^{12}}{3.35\times10^{12}}\;\approx\;300\ \text{FLOP/byte}.$$ Decode at $\sim$1 FLOP/byte runs $\sim$300$\times$ *below* that ridge (under 1% of peak FLOPs) so token rate is set by $\text{HBM bandwidth}/\text{model bytes}$, not by compute . Two effects compound it: the full weight set must be streamed from HBM *per token*, and attention re-reads the KV cache every step, with traffic that grows with context length.

**Batching couples latency and throughput.** Larger batches amortize the weight-streaming cost (better throughput and energy per token) but make each individual response wait (worse latency). Squeezing both at once is a central goal of an inference platform.

**Sharding puts the network on the critical path.** Because frontier models (especially mixture-of-experts) are sharded across many accelerators, each token triggers collectives: all-reduce for tensor parallelism, all-to-all for expert routing, point-to-point for pipeline stages. For MoE all-to-all in particular, interconnect bandwidth and tail latency can dominate. This is the concrete reason hyperscale inference platforms balance "compute, memory, and networking."

<table class="book-table"><tr><th>Phase</th><th>Bottleneck</th><th>Network role</th></tr><tr><td>Prefill</td><td>compute</td><td>moderate (parallel)</td></tr><tr><td>Decode</td><td>memory bandwidth</td><td>high for sharded models (collectives)</td></tr><tr><td>MoE routing</td><td>interconnect</td><td>dominant (all-to-all)</td></tr></table>
## Collective communication and optics demand

Once a model is sharded across many accelerators, the network stops carrying only point-to-point streams. Training and large inference jobs spend a large fraction of wall time in *collective* patterns: all-reduce for tensor-parallel layers, all-to-all for MoE expert routing, and steadier point-to-point streams for pipeline stages. Those patterns set optical requirements even when the PHY still looks like ordinary Ethernet or InfiniBand.

All-reduce

: tensor-parallel layers sum partial results across a group; needs high bisection bandwidth and low latency; latency sensitive at small message sizes (decode).

All-to-all

: MoE expert routing sends tokens to remote experts; bandwidth dominates; tail latency spikes if any link in the pod is slow (§10.5).

Point-to-point

: pipeline parallelism moves activations between stages; steady streams rather than global sync.

Optical engineering maps to these patterns indirectly. More rails and higher per-lane rate cut time spent in collectives; CPO/XPO raise faceplate bandwidth so fewer hops are needed (§10.10, §10.11, §10.2). Protocol choice (UEC vs IB) sets lossless delivery and congestion behavior (§10.8), but the PHY job remains the same: deliver pre-FEC BER below KP4 at the lowest pJ/bit (§10.13, §3.12). The next section names the fabric stacks that carry those collectives; the sections after that show where the optics physically sit.

> **Why experienced engineers chase one slow rail before rewriting the fabric?**
>
> Because synchronous collectives amplify a single straggler. Average utilization can look healthy while one optical lane sets the job tail.

> **Engineering heuristic.** Judge the fabric by delivered step time and collective tail, not by aggregate port rate on a clean bench.

Telemetry versus complexity: same decision criteria as §11.16, Appendix C.14. Instrument ledgers that unlock contain or repair; skip vanity counters.

## Fabric options

InfiniBand, Ethernet, and the Ultra Ethernet Consortium's AI-tuned Ethernet are the scale-out contenders. Momentum in 2025--26 favors open Ethernet for AI; large vertical AI stacks commonly use Broadcom Tomahawk switch silicon (Chapter 1, §10.10).

InfiniBand / NVLink fabric

: lossless, RDMA-native; NVIDIA Quantum switches; strong in closed NVIDIA stacks; CPO photonics on Quantum-X (§10.10).

RoCEv2 Ethernet

: RDMA over converged Ethernet; widely deployed; competes on congestion control and tail latency versus IB.

Ultra Ethernet (UEC)

: UET transport, enhanced PHY, congestion control aimed at AI collectives (Table 10.2). PHY work tracks 400G/lane class electrical and optical I/O.

Collectives (all-reduce, all-to-all for MoE) sit on this fabric (§10.6). The optical job is raw bandwidth and predictable latency at $\sim$200--400G per lane, not long-haul reach.

## Optical circuit switching

The fabric options above are all *packet* switches: every link terminates in a switch ASIC that turns light into electrons, reads the header, and turns it back into light for the next hop. That O-E-O conversion is where much of a fabric's power and latency goes (§10.13), and at $10^5$-plus endpoints it repeats at every tier. An *optical circuit switch* does a different job. It is a Layer-1 switch that steers light from an input fiber to an output fiber with no O-E-O conversion, so it is transparent to bit rate, modulation format, and wavelength. The same switch that passes 200 Gb/s PAM4 today passes 448G or a full WDM comb tomorrow with no change (Chapter 6, §3.14).

Transparency is the point, and also the limit. Because an OCS never looks at a packet, it cannot buffer, arbitrate, or route per packet. It sets up a *circuit*: a fixed light path held open as long as the topology needs it. The mirrors or waveguides that steer the light reconfigure in milliseconds, far slower than a packet time, so an OCS reshapes the *topology* between jobs or around failures, not the traffic inside a job. In return it deletes a whole tier of packet switches and their pluggable optics, along with the power, cost, and FIT that tier carried (§10.2, Chapter 8).

##### The device and its parameters.

Most production OCS today is free-space: a fiber-collimator array launches beams onto a two-axis MEMS mirror array, and each mirror tilts to aim its beam at the chosen output collimator. Table 10.6 lists the main technologies. For an optics engineer the parameters that matter are the ones that land in the link budget and the fleet model.

Insertion loss

: a hop through the switch costs roughly 2 dB, straight off the optical budget (Appendix E.5). Higher launch power or better receiver sensitivity has to cover it (Chapter 5, §4.4).

Radix

: how many fibers the switch connects. Production MEMS OCS runs about $136\times136$; circulators reuse each port in both directions and so double the effective radix (below).

Reconfiguration time

: milliseconds for MEMS, which fixes OCS as a topology switch. Silicon-photonic and SOA switches reach nanoseconds, but at low radix and higher loss (Table 10.6).

Crosstalk, return loss, polarization

: a mirror that leaks light into the wrong port is crosstalk; a reflective interface raises ORL and feeds laser RIN (Appendix E.2, §4.3). Free-space paths are largely polarization-insensitive, which suits IM/DD.

<table class="book-table"><tr><th>Technology</th><th>Switching</th><th>Insertion loss</th><th>Radix</th><th>Where it fits</th></tr><tr><td>MEMS mirror array (free-space)</td><td>ms</td><td>1--3 dB</td><td>100s (136136 shipping)</td><td>DC fabric and AI-pod topology reconfiguration</td></tr><tr><td>Piezoelectric beam steering</td><td>ms</td><td>low--moderate</td><td>10s--100s</td><td>free-space alternative to MEMS</td></tr><tr><td>Liquid crystal (LCoS)</td><td>ms</td><td>moderate</td><td>wavelength-selective</td><td>wavelength add/drop, WSS roles</td></tr><tr><td>3D robotic fiber</td><td>seconds--minutes</td><td>0.5 dB</td><td>1000s</td><td>automated patch and provisioning, not per-job</td></tr><tr><td>Silicon photonic (MZI / SOA)</td><td>ns--</td><td>higher (integrated)</td><td>10s</td><td>fast, low-radix; research and niche</td></tr></table>
**Table 10.6.** OCS technologies. Free-space MEMS switches dominate AI deployments today; robotic-fiber switches trade speed for radix and very low loss; integrated photonic switches trade radix and loss for nanosecond speed.

##### What it buys at fleet scale.

Google's Jupiter datacenter fabric replaced a patch-panel Clos interconnect with a layer of MEMS OCS under software-defined control, and reported roughly 30% lower capex, 41% lower power, and 3x faster fabric reconfiguration while a direct-connect topology carried the same production traffic . The switch, Palomar, is a $136\times136$ MEMS OCS with about 2 dB insertion loss and millisecond switching, and circulators realize bidirectional links through it to double the effective radix . The same building block reshapes AI pods: a TPU v4 pod wires 4096 accelerators through 48 OCS into a 3D torus that reconfigures per job and routes around failed racks, so a dead node becomes a topology the scheduler works around instead of a pod-wide outage . That reconfiguration is the fabric-reliability lever Chapter 8 points at: component FIT still applies, but the fabric survives each failure by re-wiring optically rather than stalling the job.

##### What OCS asks of the transceivers.

An OCS layer changes the module spec in ways this book cares about. Because the switch adds a fixed loss and is wavelength-transparent, single-fiber duplex reaches (FR, one fiber each way) fit an OCS better than parallel-fiber reaches (DR, many fibers), so an OCS deployment pulls the plant toward FR optics and toward circulators for bidirectional operation on one fiber . The insertion loss argues for higher launch power and tighter ORL budgets, since every mated interface and mirror is a reflection the laser sees (Appendix E.2, §4.3.1). Wavelength transparency means a WDM link passes through the switch unchanged, so CW-WDM and ring-based engines (Chapter 6, §6.6) compose with an OCS without a translation layer. None of this is exotic optics; it is the same DR/FR PMD and laser work from earlier chapters (§3.13, Chapter 5), specified against a channel that now includes a switch.

##### Status and where it sits next to CPO.

By 2025--26 OCS moved from a Google-specific technique to an industry theme, a headline topic at OFC 2026 with MEMS, piezoelectric, liquid-crystal, robotic-fiber, and silicon-photonic approaches competing on radix, loss, speed, and reliability . It complements co-packaged optics rather than competing with it: CPO shortens the electrical path at the switch package (§10.10), while OCS removes packet-switch hops between packages and racks. A fabric can use both, CPO optics feeding an OCS layer, and the reliability question for each is the one Chapter 7, Chapter 8 keeps returning to.

**Key idea.** An optical circuit switch reroutes light at Layer 1 with no O-E-O conversion, so it is transparent to rate, format, and wavelength and adds only insertion loss to the link budget. Millisecond MEMS switching makes it a topology and failure-reroute switch, not a packet switch. It buys fabric power, cost, and resilience (Google Jupiter and the TPU pods are the production proof), and it pulls the transceiver plant toward FR optics, circulators, and higher launch power. OCS and CPO are complementary bets on the same power and reliability problem.

## Co-packaged optics: 2025--26 status

By 2025--26, co-packaged optics crossed from demonstrations into shipping products, pushed by the power and reliability limits of pluggables in AI scale-out. The programs converge on a common recipe: a photonic engine co-packaged with the switch ASIC, 200 Gb/s per channel, microring modulators (§3.14.3), *field-replaceable* lasers pulled out of the package, and TSMC COUPE packaging underneath.

### Broadcom Tomahawk and CPO

Broadcom entered CPO earlier than most switch vendors and treated it as a product line, not a one-off demo. The current flagship is *Tomahawk 6*, a 102.4 Tb/s single-chip Ethernet switch (shipping 2025) offered with either copper or co-packaged optics, on 100G/200G SerDes.[^37] The CPO variant, *TH6-Davisson*, began shipping in October 2025 as Broadcom's *third-generation* CPO switch. The public numbers sketch the architecture:

- 102.4 Tb/s optically enabled, built from sixteen 6.4 Tb/s "Davisson DR" optical engines at 200 Gb/s per channel.

- Photonic engines fabricated with *TSMC COUPE*; 64 Condor 3 nm SerDes cores (eight 212.5 Gb/s PAM4 lanes each).

- About 70% lower optical-interconnect power than pluggables.

- *Field-replaceable ELSFP laser modules*: lasers, the highest-failure component, made serviceable in the field.

- Scale-up to 512 XPUs; 100,000+ XPUs in a two-tier fabric at 200 Gb/s/link.

The lineage matters: CPO shipped on Tomahawk 4 and the second-generation *TH5-Bailly* (51.2 Tb/s), which logged "millions of hours" of reliability testing before Davisson. A fourth generation at 400 Gb/s per channel is already in development.

### NVIDIA

NVIDIA's CPO story is the scale-up and scale-out fabric vendor converging on the same TSMC COUPE + microring recipe as Broadcom, announced as product families at GTC 2025: *Quantum-X* (InfiniBand) and *Spectrum-X* (Ethernet) Photonics switches, 200G SerDes, 1.6 Tb/s ports. Headline marketing claims include 3.5$\times$ power efficiency, *4$\times$ fewer lasers*, and large resiliency gains versus pluggables; treat those as vendor orientation, and validate against your own FIT and power model.

- *Quantum-X InfiniBand*: 144 ports of 800G ($\approx$115 Tb/s), liquid-cooled; available late 2025. Each package integrates eighteen silicon-photonics engines fed by 36 laser inputs through six *detachable* optical sub-assemblies.

- *Spectrum-X Ethernet*: up to 409.6 Tb/s; available in 2H 2026.

- Ecosystem: lasers from Lumentum, silicon photonics with Coherent, packaging with TSMC.

### TSMC COUPE (the shared foundation)

*COUPE* (Compact Universal Photonic Engine) stacks an electronic IC on a photonic IC via SoIC-X hybrid bonding (a 6 nm EIC on a 65 nm SOI PIC), giving a low-impedance die-to-die interface. The roadmap: pluggable qualification in 2025, CoWoS-based CPO integration and *mass production in 2026*, with 800G/1.6T engines now and 3.2T/6.4T (toward 12.8 Tb/s on-package) to follow. TSMC cites the energy-per-bit trajectory from $>$30 pJ/bit for copper toward $<$5 pJ/bit for CPO on substrate and $<$2 pJ/bit once optical I/O moves onto the interposer (§10.13). The hard problems it names (wafer-level test, fiber-array-unit integration, and high-speed optical packaging assembly) are exactly the validation and manufacturing challenges of Chapter 7, Chapter 8, Chapter 9.

<table class="book-table"><tr><th>Program</th><th>Technology</th><th>Status</th></tr><tr><td>Broadcom TH6-Davisson</td><td>102.4 Tb/s, 200G/ch, COUPE, ELSFP lasers</td><td>3rd-gen CPO, shipping Oct 2025</td></tr><tr><td>Broadcom TH5-Bailly</td><td>51.2 Tb/s CPO</td><td>2nd-gen, extensively field-tested</td></tr><tr><td>NVIDIA Quantum-X (IB)</td><td>144800G, MRM, COUPE, detachable lasers</td><td>available late 2025</td></tr><tr><td>NVIDIA Spectrum-X (Enet)</td><td>up to 409.6 Tb/s, MRM, COUPE</td><td>2H 2026</td></tr><tr><td>TSMC COUPE</td><td>SoIC-X EIC-on-PIC packaging</td><td>mass production 2026</td></tr><tr><td>Samsung (foundry)</td><td>optical engines / turnkey CPO</td><td>OE 2027, CPO 2029</td></tr><tr><td>Ayar Labs</td><td>TeraPHY optical I/O + SuperNova CW-WDM source</td><td>merchant scale-up optical I/O</td></tr></table>
**Table 10.7.** CPO programs, 2025--26.

**Key idea.** The 2025--26 CPO wave shares one architecture: 200G/lane microring engines on TSMC COUPE, with field-replaceable lasers because lasers fail first. Tomahawk-class CPO at 200G/lane makes IM/DD validation and ELSFP laser reliability direct gates on how many accelerators a pod can wire together dependably.

## The serviceable-density middle ground: XPO (OFC 2026)

CPO buys density and power at a cost the operator feels: the optics are soldered to the switch, so a single failed engine can mean pulling the whole line card. That tension (pluggable serviceability versus co-packaged density) defined much of *OFC 2026*, where a third path drew the most attention.

Arista, with Coherent, Marvell, Lightmatter, and a broad partner list, launched the *XPO* (eXtra-dense Pluggable Optics) multi-source agreement. The bet is to keep the front-panel pluggable form factor (slide a module out, snap a new one in) while closing most of the density and power gap to CPO:

- **12.8 Tb/s per module**: 64 electrical lanes at 200 Gb/s PAM4 (with a roadmap to 400 Gb/s lanes for 25.6 Tb/s), roughly $4\times$ the density of a 1.6T-OSFP pluggable.

- **204.8 Tb/s per OCP rack unit**, from up to sixteen modules, front-panel density approaching co-packaged designs.

- **Integrated liquid-cooled cold plate** rated for 400 W+ per module, with blind-mate dripless quick-disconnects; this, not the connector, is what makes the high per-module power serviceable.

- **Universal reach and interface**: SR/DR/FR/LR plus ZR/ZR+, and fully-retimed, half-retimed, or linear (LPO/LRO) optics in one form factor.

<table class="book-table"><tr><th>Attribute</th><th>Retimed / LPO pluggable</th><th>XPO</th><th>CPO</th></tr><tr><td>Capacity</td><td>0.8--1.6 Tb/s/module</td><td>12.8 Tb/s/module</td><td>100+ Tb/s on-package</td></tr><tr><td>Density</td><td>baseline</td><td>4 (204.8 Tb/s per RU)</td><td>highest</td></tr><tr><td>Power path</td><td>full electrical run to faceplate</td><td>short run to dense faceplate</td><td>shortest (on substrate)</td></tr><tr><td>Cooling</td><td>air (or LPO savings)</td><td>integrated cold plate, 400 W+</td><td>switch-package liquid cooling</td></tr><tr><td>Serviceability</td><td>field-replaceable (best)</td><td>field-replaceable (slide-out)</td><td>soldered; ELSFP lasers replaceable</td></tr><tr><td>Energy/bit</td><td>highest</td><td>intermediate</td><td>lowest (<5, then <2 pJ/bit)</td></tr><tr><td>Maturity</td><td>shipping</td><td>MSA launched OFC 2026</td><td>shipping (Broadcom, NVIDIA)</td></tr></table>
**Table 10.8.** Where XPO sits between pluggables and co-packaged optics.

[^38]

**The broader OFC 2026 picture.** XPO landed inside a clear consensus: 1.6T transceivers went mainstream and 3.2T (400G/lane) previews appeared, with initial demos expected around 2027; CPO moved from demo to imminent, with new MSAs (Open CPX, "socketed CPO") blurring the pluggable/co-packaged line; and hollow-core fiber (record loss now $\sim$0.091 dB/km) advanced toward low-latency intra-datacenter use (§10.12.1). The through-line is the one this book opened with: rising per-lane rate forcing optics closer to the silicon and squeezing every last pJ/bit.

## The latency budget

The book has a link budget in dB (Appendix E.5) and, next, an energy budget in pJ/bit. It needs a third ledger. Inference puts the optical link on the critical path (§10.6), so you should be able to add up a link's latency the way you add up its loss and its power. The contributors fall into two groups: fixed digital costs that do not care about distance, and a propagation term that does.

<table class="book-table"><tr><th>Contributor</th><th>Typical latency</th></tr><tr><td>PCS framing / serialization</td><td>a few ns</td></tr><tr><td>FEC encode + decode (KP4)</td><td>20--100 ns each</td></tr><tr><td>Module DSP / retimer (per hop)</td><td>8--10 ns (fully retimed)</td></tr><tr><td>LPO (no DSP)</td><td><3 ns</td></tr><tr><td>Driver, modulator, PD, TIA</td><td>sub-ns</td></tr><tr><td>Fiber propagation (silica)</td><td>4.9 ns/m</td></tr><tr><td>hollow-core fiber</td><td>3.3 ns/m</td></tr><tr><td>Switch hop (O-E-O)</td><td>100--560 ns</td></tr></table>
**The fixed digital cost dominates a short link.** FEC is the largest single term. KP4 RS(544,514) (§3.12) costs roughly 20 to 100 ns to encode and again to decode, set by the codeword length and the implementation, not the fiber . The module DSP adds another 8 to 10 ns per hop when the link is fully retimed. The analog stages, driver, modulator, photodiode, and *TIA*, together contribute well under a nanosecond of group delay and are almost never the problem. On a 10 m in-rack link the fiber itself is about 50 ns, smaller than one pass through the FEC.

**Propagation dominates only once the fabric is large.** Light in standard single-mode fiber travels at roughly $c/1.47$, about $4.9$ ns/m, because the glass has a group index near 1.47. A 100 m row-scale run is then about 490 ns, comparable to a switch hop and larger than the digital terms. Each switched tier adds an O-E-O conversion: a cut-through Ethernet switch forwards in a few hundred nanoseconds ($\sim$560 ns for an 800GbE class device), while InfiniBand reaches under 100 ns per hop . Across a multi-tier scale-out fabric, the switch hops and their conversions, not the fiber, set the tail latency that stalls a collective (§10.6). This is the latency argument for optical circuit switching (§10.9) and for co-packaging: both remove conversions and electrical runs from the path.

**Latency is where the module architecture shows up again.** The retimed-to-linear choice you met in §10.13 for power repeats here. A fully retimed module spends $\sim$8--10 ns per hop; *LRO* roughly halves that; *LPO* deletes the module DSP and lands under 3 ns . On a link with a few hops, deleting the DSP saves more time than shortening the fiber does. Latency and energy point the same way, which is why LPO and CPO are attractive for the scale-up domain where both matter most.

### Hollow-core fiber

The one distance term you can attack is the group index. Hollow-core fiber (*HCF*) guides light mostly through air rather than glass, so its group index sits near 1.0 and light travels close to vacuum speed. A double nested antiresonant nodeless fiber (*DNANF*) design reported 0.091 dB/km at 1550 nm, below the $\sim$0.14 dB/km floor that silica has held since the 1980s, and about 0.2 dB/km across a 66 THz window . The latency payoff is the headline for short reach: propagation drops from $\sim$4.9 to $\sim$3.3 ns/m, roughly 45% faster or about a third lower latency, which on a 100 m run saves $\sim$150 ns, the size of a switch hop. Microsoft reports deploying cabled HCF in the Azure network.

For short-reach IM/DD the low nonlinearity and near-zero dispersion of air guiding matter less than they do for coherent long-haul; the draw here is purely latency and, secondarily, the wider low-loss window for more wavelengths. The open problems are practical: low-loss splicing and connectorization to solid-core plant, yield at volume, and cost. These figures are recent records, so treat them as provisional.

## Energy per bit and the power wall

Frontier AI is *power-limited*: a site's usable megawatts, not just capital, caps how much compute it can host. Every watt spent moving bits is a watt not spent on compute, and interconnect energy multiplies across a fabric with millions of links, which is why energy per bit (*pJ/bit*) has become a headline design metric.

The trajectory that CPO is chasing, per TSMC's COUPE disclosures:

<table class="book-table"><tr><th>Link style</th><th>Energy per bit</th></tr><tr><td>Conventional copper / retimed</td><td>>30 pJ/bit</td></tr><tr><td>Co-packaged optics on substrate</td><td><5 pJ/bit</td></tr><tr><td>Optical I/O on the interposer</td><td><2 pJ/bit</td></tr></table>
This is the quantitative reason CPO exists: removing the power-hungry electrical run between a switch ASIC and a front-panel pluggable (and the module's retiming DSP) is roughly a $70\%$ cut in optical-interconnect power in Broadcom's Davisson (§10.10). *LPO/LRO* attacks the same target from the pluggable side by deleting the DSP; CPO attacks it by shortening the electrical path.

**Why it compounds.** Multiply even a few pJ/bit by aggregate fabric bandwidth and link count and interconnect becomes a meaningful slice of cluster power. At a fabric moving petabits per second, a 5 pJ/bit versus 30 pJ/bit choice is megawatts, directly setting how many accelerators fit under a fixed power envelope. Laser wall-plug efficiency feeds the same budget: fewer, more efficient lasers (NVIDIA claims 4$\times$ fewer) cut both power and failure count at once.

**The macro trend behind the metric.** The pJ/bit fight has grid-scale stakes. US data centers drew about 176 TWh in 2023, roughly 4.4% of national electricity, up from 58 TWh in 2014; the Lawrence Berkeley National Laboratory projects 325 to 580 TWh, or 6.7 to 12% of US electricity, by 2028 . Interconnect is a growing share of that draw as lane rates climb . Every pJ/bit an LPO or CPO link removes is multiplied across that base, so interconnect power reads as an infrastructure problem, not only a per-module one.

### The thermal envelope

Every watt from the budget above turns into heat that has to leave the box, so interconnect power is also a cooling problem, and cooling sets a second ceiling beside the power wall. On a faceplate switch the optics are a large part of that heat: a 32-port 800G switch dissipates on the order of a kilowatt, and the pluggable modules account for roughly half of it . Air cooling loses headroom as per-module power climbs past the mid-teens of watts, which is why dense high-rate switches are moving to liquid and immersion cooling, and why the LPO power cut (from $\sim$14--18 W to $\sim$8 W, §10.13) reads as a thermal cut as much as an electrical one .

**Co-packaging changes the shape of the problem.** Moving the optics onto the switch substrate (§10.10) puts heat-sensitive optical engines a few millimeters from a high-power ASIC. Absolute temperature still matters, but the steep on-package gradient becomes the performance-limiting term: rings drift off resonance and lock loops fight neighbor heaters (§6.5), and the laser is the least tolerant part of all . This is the thermal half of the argument for external lasers (§5.14): holding the laser off the hot interposer at a controlled temperature protects both its wavelength and its life.

**Cooling is a reliability lever, not only a power one.** Laser wear-out follows Arrhenius kinetics (§5.13): the acceleration factor is exponential in inverse junction temperature, so a few degrees of cooling buys a measurable drop in FIT and, across $10^5$-plus lasers, fewer failures per day (§5.13). Power, cooling, and reliability are one constraint seen three ways. The link that fits under a fixed power and cooling envelope, and stays cool enough to last, is the one that scales.

**Key idea.** Energy per bit is a first-order lever on cluster size under a fixed power budget. The industry path, retimed pluggable ($>$30 pJ/bit) to LPO to CPO ($<$5, then $<$2 pJ/bit), is why "balance compute, memory, and networking" (Chapter 1) is a power statement as much as a performance one.

## A first-order cost model

The book quantifies two of its three themes. Power has a ledger in pJ/bit (§10.13); reliability has one in FIT (§5.13). Cost is invoked everywhere but never counted. It deserves the same first-order treatment, kept deliberately relative and order-of-magnitude. What follows is an illustrative model, not a price sheet: absolute module prices move too fast and vary too much by volume to write down usefully, so the numbers here are assumptions you should replace with your own.

*Total cost of ownership* (TCO) for an optical link splits into three buckets. The first is acquisition, the *bill of materials* (BOM) and the yield of optical assembly and test: laser count, whether a DSP die is present, and the packaging and coupling steps that dominate transceiver cost. The second is lifetime energy, the module's power drawn over years and multiplied by a cooling overhead. The third is service: the failures per day implied by the fleet FIT (§5.13), each one costing a replacement part and a hands-on visit. Acquisition is capital; the other two are recurring.

**Energy is the bucket you can compute.** Take an 800G module drawing $\sim$15 W fully retimed against $\sim$8 W for LPO (§10.13) . Over a five-year life at \$0.10/kWh, with a *power usage effectiveness* (PUE) of $\sim$1.3 to cover cooling, the retimed module burns about 850 kWh, near \$85 of electricity; the LPO module about 460 kWh, near \$46. The $\sim$\$40 gap per module is a meaningful fraction of what the module itself costs, and it recurs every life cycle. Scaled up, the number stops being small: a vendor estimate puts the LPO saving on a 500,000-accelerator cluster on the order of 100 MW and roughly \$100 million a year in electricity . Treat that figure as vendor orientation, but the order of magnitude is the point.

**Recurring cost is a large share of the total.** A gigawatt-class AI site has been quoted near \$38 billion of up-front capital and roughly \$0.9 billion a year to run . Over a multi-year life the running cost is a real fraction of the capital, and interconnect power is a growing slice of it, so a pJ/bit cut reads directly as dollars saved. That estimate is an analyst breakdown, provisional, but it sets the scale: power and cost are the same argument seen through two units.

**The architecture choice moves all three buckets at once.** Per delivered Gb/s, a fully retimed pluggable carries the highest BOM (a DSP die and its packaging) and the highest power. LPO and LRO delete or relax that DSP, cutting both the BOM and $\sim$40--50% of the power , and move the cost that remains into host validation risk rather than the module. CPO and XPO remove the faceplate connector and the long electrical run and push energy under 5 pJ/bit (§10.10), but raise assembly and test cost and couple the optics to an expensive switch ASIC, which is why the lasers are field-replaceable: a laser failure must not scrap the package (§10.10). Co-packaged and near-package copper is cheaper still per Gb/s wherever it reaches, carrying only the connector and the host SerDes energy (§10.5); the crossover to optics is set by the reach wall, not by cost. At the fabric level, optical circuit switching is itself a cost lever: replacing a tier of O-E-O packet switches with a MEMS OCS cut capex $\sim$30% and power $\sim$41% in Google's Jupiter (§10.9) .

**Key idea.** Cost tracks power and reliability, not against them. The cheapest link per Gb/s is the one you do not light (copper within reach), then the one with the fewest active stages (LPO, then CPO), weighed against the validation risk and the failure blast radius each one adds. A pJ/bit saved is dollars saved every year the fabric runs, which is why the energy budget and the cost model point the same way.

## Synthesis: from workload to fleet

This chapter sits at the end of the book because it joins the decisions from every earlier chapter into one system. The path below is not a waterfall; teams iterate. But each step produces evidence that either advances the design or sends it back.

<pre class="dectree" aria-label="Workload / collectives"><code>Workload / collectives
  |
Reach / topology
  |
Placement (pluggable / LPO / CPO / CPC)
  |
Laser / modulator / WDM
  |
Budgets (optical / electrical / energy / thermal)
  |
Validation ladder
  |
Supplier / ATP / SPC
  |
Fleet telemetry + corrective action</code></pre>
1.  **Workload and collective requirements.** What traffic pattern, latency target, and tail tolerance does the job demand? (Chapter 1, §10.7, §10.6)

2.  **Reach and topology.** What physical extent, link count, and oversubscription does the cluster need? Does copper close, or does optics take the link? (§10.2, §10.5, Table 10.1)

3.  **Electrical versus optical placement.** Pluggable, LPO, CPO, XPO, or co-packaged copper? The answer follows from reach, power envelope, and serviceability. (Table 10.4, §10.10, §10.11, §10.5)

4.  **Laser, modulation, and WDM selection.** DFB, EML, CW+Si MZM, CW+ring, or CW+TFLN? Single-wavelength DR or dense WDM with locking? The choice sets the ATP, the supplier base, and the fleet FIT model. (Chapter 5, Chapter 6, Table 5.1, Table 3.12)

5.  **Link, power, and thermal budgets.** Close the optical ledger (OMA to sensitivity with penalties), the electrical ledger (COM), the energy ledger (pJ/bit), and the thermal envelope together. (Appendix E.5, §10.5.2, §10.13, §10.13.1)

6.  **Noise, sensitivity, and receiver design.** Match photodiode, TIA, and equalization to the power the laser and channel deliver. Budget RIN, shot, and thermal noise against the pre-FEC BER target. (Chapter 4, §4.4, §4.3, §4.5)

7.  **Product-readiness evidence.** Walk the lifecycle: bring-up, characterization, requirement verification and system validation, stress qualification, and manufacturing validation. Name the instrument and reference plane for every number. (Chapter 7, §7.3, §7.6)

8.  **Yield and supplier readiness.** Multi-lot yield, SPC, ATP coverage, NPI gates, first-article, and 8D discipline. Prove the part can be built at volume before committing the fleet. (Chapter 9, §9.5, §9.9)

9.  **Fleet telemetry and corrective action.** Pilot, ramp, and fleet monitoring are operational readiness and sustaining evidence. CMIS monitors, FEC histograms, triage buckets, RMA codes, and the feedback loop from field to ATP. The system is not done until the fleet can detect, classify, and correct a failure without the design team. (§11.16, §10.17.6, §7.4.8)

A design review should be able to point at evidence for every step. Where evidence is missing, the step is not done. Where two steps conflict (power budget versus serviceability, yield versus guardband), the trade must be stated and owned, not hidden behind a single-number spec.

## Engineering lens

### How it works

An AI fabric is judged by delivered workload time, not port rate, and the optical layer sits on that critical path. The chapter places every earlier device into scale-up and scale-out networks and shows where copper ends and optics wins the link.

### How it is measured

> **Observe at four layers**\
>
> Workload
>
> : Step time, collective latency, accelerator idle time, and tail behavior.
>
> Fabric
>
> : Routes, queues, congestion, retries, and failed links.
>
> Link
>
> : Pre-FEC error distribution, corrected and uncorrectable FEC, equalizer state, retrains, and flaps.
>
> Module
>
> : Power, temperature, wavelength or lock, alarms, firmware, and control state.
>
> Start at the layer where the impact is observed, then descend only far enough to isolate the cause.

A peak-rate test does not replace an all-reduce or all-to-all run on the intended topology (§10.7, §11.16, §10.17).

### How it fails

Scaling can fail through oversubscription, poor route balance, head-of-line blocking, a straggling link, excess retries, switch-radix limits, fiber-count and service errors, or a power and cooling ceiling. Architecture adds distinct escape paths: pluggables can run out of faceplate power, linear optics can expose host margin, and co-packaged optics can turn package thermals, lock control, or fiber service into the limiting risk. A working link can still be a bad system choice if it cannot be monitored, replaced, or operated at fleet scale.

\> \*\*Failure mode: Collective slowdown\*\* \> \> \*\*Symptoms.\*\* Accelerator count rises, but job throughput flattens or falls and tail step time grows. \> \> \*\*Likely causes.\*\* Fabric oversubscription, uneven routing, one degraded rail, retransmits, switch congestion, or synchronization amplifying a straggler. \> \> \*\*Measurements.\*\* Collective traces, route and queue telemetry, per-link FEC and retry counters, topology map, and a scale sweep. \> \> \*\*Mitigations.\*\* Repair weak links, rebalance routes, remove oversubscription, change the collective or topology, and gate the next scale point on delivered workload performance.

### How it is debugged

Start with the workload symptom and identify the slow collective, rail, or time window. Compare topology and route data with link counters. A single lane with rising FEC points to the optical path; many clean links with full queues point to fabric capacity or scheduling. On the optical path, use the power-versus-quality fork and five ledgers (§4.8, §5.19, Appendix D.4). Remove one rail, reroute one group, or replace one suspect module to test causality. Keep optics, switch, and workload timestamps aligned. Otherwise a link flap and a collective stall cannot be ordered reliably.

> **Engineering heuristic.** Align timestamps across optics, switch, and workload before arguing causality. Without a common clock story, every flap looks like every stall.

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* All-reduce tail latency rose after a rack expansion, while average link utilization looked normal. \> \> \*\*Investigation.\*\* Per-rail traces showed one path with FEC bursts and retries. A module swap moved the symptom with the module. \> \> \*\*Finding.\*\* The fabric had capacity, but one marginal optical lane set the collective tail. \> \> \*\*Root cause.\*\* A contaminated connector raised ORL and produced burst errors without a large average-power change. \> \> \*\*Resolution.\*\* The connector was replaced, inspection was added to the expansion runbook, and collective-tail alarms were tied to link-level error bursts.

## Operational events, telemetry, and availability

### Event vocabulary

These events are related but not interchangeable. Debugging requires their order in time.

Correctable FEC event

: The decoder successfully repairs errors; the link remains logically usable.

Uncorrectable FEC event

: The error pattern exceeds correction capability and may produce packet loss, a lane failure, or a link-state event.

Retrain

: The PHY repeats equalization, CDR, lane alignment, or another link-training function. Traffic may interrupt without a full MAC-level down.

Link flap

: The operational link transitions down and later returns up, usually with a larger control-plane or topology reaction.

Retry or retransmission

: A transport, link, or protocol response to failed delivery. It does not identify the underlying layer by itself.

Workload stall

: An application-visible delay or pause, potentially caused by one or several lower-layer events.

### FEC telemetry interpretation

Averages are insufficient. For every FEC metric preserve lane, direction, code type, measurement interval, corrected and uncorrectable counts, codeword or symbol distribution, burst duration, threshold assumptions, and firmware or counter semantics. Two links with the same average error rate may have different operational risk if one has stationary random errors and the other has short bursts that approach the decoder limit. Do not state one universal pre-FEC threshold; tie thresholds to the actual FEC and PMD.

An FEC *symbol-error histogram* is not a DCA eye histogram. For a named KP4-class Reed--Solomon code on fixed-size symbols (§3.12), host or decoder counters report wrong symbols per codeword or versus time. Sparse, Poisson-like distributions fit steady noise. Bursty clumps fit time-local events: MPI, connector intermittents, unlock, supply or clock glitches. A burst can exceed correction capability even when long-run average BER still looks acceptable. Shape prioritizes hypotheses; confirm with ORL, timing, swaps, and plant disturbance (§11.2, Chapter 11).

### Retrain, flap, and recovery counters

Extend the telemetry contract beyond optical power and temperature. Prefer actionable counters when the hardware exposes them: lane training, CDR loss and recovery, PCS alignment, FEC lock loss, link down/up, module reset, host reset, CMIS state change, firmware recovery, route reconvergence, packet retry or drop, and workload checkpoint or restart. Where a counter is missing, state the visibility gap rather than inferring the event from a distant proxy.

<pre class="dectree" aria-label="Workload tail rises"><code>Workload tail rises
  |
Packet retries increase
  |
Link retrains / flaps
  |
FEC burst begins
  |
Optical / thermal / host state changes</code></pre>
*Illustrative order only.* Align timestamps to determine the actual order. The same events in reverse order imply a different mechanism.

### Host and module ownership by architecture

<table class="book-table"><tr><th>Architecture</th><th>Host owns</th><th>Module / engine owns</th><th>Main operational ambiguity</th></tr><tr><td>Fully retimed</td><td>Host channel to module input; system FEC</td><td>Module CDR/DSP and optical conversion</td><td>DSP may hide where impairment began</td></tr><tr><td>LPO</td><td>EQ, CDR, FEC, much of end-to-end margin</td><td>Analog optical conversion and linearity</td><td>Host and module behavior strongly coupled</td></tr><tr><td>LRO</td><td>Direction-dependent shared ownership</td><td>Retimed direction plus analog direction</td><td>Failure ownership changes by direction</td></tr><tr><td>CPO</td><td>Switch package, electrical XSR, system FEC</td><td>Co-packaged optical engine and external laser path</td><td>Larger thermal/service failure domain</td></tr></table>
**Table 10.11.** Operational ownership reference by architecture. Not a new architecture framework; use it when assigning debug ownership (§10.3.1, §10.10).

### Component reliability versus system availability

Component reliability describes how often a part is expected to fail under stated assumptions. System availability also depends on detection, redundancy, failover, repair time, spares, service access, and whether one failure interrupts useful work. A simple steady-state starting point is

$$\begin{equation}
A \approx \frac{\mathrm{MTBF}}{\mathrm{MTBF}+\mathrm{MTTR}}
\end{equation}$$

AI-fabric availability also depends on correlated failures, routing, detection and failover latency, repair access, spares, service policy, checkpoint or job restart cost, and workload-level impact. Independent component FIT addition is not a complete system-availability model (§8.4.1). The rest of this section works that gap in detail.

### From component FIT to fabric availability

The FIT arithmetic in §5.13 gives a rate: about $0.6$ laser failures per day for a fleet of $5\times10^5$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin (§5.14), but it does not say what a failure costs or how a running job survives one. Two facts turn a per-component rate into a fabric problem.

First, a training or large inference job is synchronous. A collective (§10.7) waits for its slowest member, so a single dead or slow link stalls the whole group, not just one endpoint (§10.6). A link that flaps for a second is a stall for every accelerator in that collective. The optical FIT that Chapter 8 budgets therefore matters out of proportion to its share of the parts count.

Second, at cluster scale failures are continuous, not rare. Meta's published Llama 3 run is the clearest public data point: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . GPU and HBM3 faults dominated at close to half; network switch and cable faults were 35 events, 8.4% of the total. The optical link is a minority of hard job stops, but 8.4% of a failure every three hours is still tens of network events per run, and the ELS, module, and connector FIT budgeted in §8.4.1, Appendix F.5 lands in exactly that bucket.

So the design question shifts. It is no longer "how reliable is one link" but "how does a fabric of $10^5$ links keep a job running through a failure every few hours." The answers are architectural, and the optical engineer feeds each one.

Redundancy and rails.

: Rail-optimized topologies (§10.2) already give parallel planes; dual-plane and dual-ToR designs let a lost link degrade bandwidth instead of dropping an endpoint. Redundancy multiplies the link and laser count, which feeds straight back into the FIT budget: more resilience is more parts that can fail.

Detection and reroute.

: Transient faults stay below the job. KP4 FEC (§3.12) absorbs the error bursts a marginal link throws; link-level retry and sub-second link-flap detection plus adaptive routing steer traffic off a degraded link before the scheduler notices. Vendor fabrics (NVIDIA Spectrum-X and Quantum, Broadcom Tomahawk) advertise adaptive or "cognitive" routing and link-level retry for this. Treat the specifics as vendor orientation, but the mechanism is why transient optical faults rarely reach the hard-stop bucket above.

Topology reconfiguration.

: When a link or rack dies for good, an optical circuit switch re-wires the topology around it in milliseconds, so the scheduler routes around the dead node instead of stalling the pod (§10.9) . Component FIT still applies; the fabric survives each failure by re-wiring optically.

Sparing and field service.

: Hot spare nodes and lanes cover the interval between failure and repair. Field-replaceable external lasers (§5.14) make a dead laser a faceplate swap rather than a fabric outage, which is the architectural reason ELS decouples laser FIT from switch FIT. The connector mating-cycle and endface budget (Appendix F.5) sets how many of those swaps the plant survives.

The cost of a failure closes the loop. A hard interruption is lost compute plus the time to detect, reroute or reschedule, and restart from the last checkpoint. Fast detection and reroute shrink that lost time, which is the fabric-level reason the module work pays off: derating (§5.13), qualification and production screens (Chapter 8, Chapter 9), and a tight ATP (§9.9) lower the failure rate, and a resilient fabric lowers the cost of each failure that slips through. The two multiply.

## Interview takeaway

**Key idea.** An AI fabric is judged by delivered workload time, not aggregate port rate. Connect collective traces to queue, route, FEC, optical, thermal, and service data. Choose pluggables, linear optics, or co-packaging by the measured system constraint and by how the fleet detects, contains, and repairs each failure.

Junior mistake: rewrite the topology before scoping one weak rail, or ignore optics FA when collectives stall (§4.8, Chapter 11, Appendix D, Appendix I).

### Interview Q&A: Networking and System Operation

Practice speaking these answers aloud. Prefer first-person operational reasoning over topology slogans. Detail lives in §10.17, §10.17.1, §10.7, §11.16, Table 10.11.

##### Question 1. What is the difference between scale-up and scale-out, and why does the distinction matter to an optical engineer?

*Tests:* system architecture, reach, bandwidth, latency, and optical deployment.

*Spoken answer.* "Scale-up connects accelerators inside a tightly coupled node, rack, or pod. It usually has the highest bandwidth per endpoint and the strictest latency requirement, so copper remains attractive while the reach is short enough, but optics moves inward as lane rates and physical extent grow. Scale-out connects nodes and racks through a switched fabric across a much larger population. It already relies heavily on optics because of distance, routing, and link count. The distinction matters because scale-up prioritizes latency, power, and very short electrical reach, while scale-out adds topology, interoperability, serviceability, and fleet-scale availability" (§10.1).

*Pressure follow-up.* "Would you always choose lower-latency LPO for scale-up?"\
*Answer pivot.* "No. LPO reduces module power and retiming latency, but it transfers equalization, FEC, and channel-margin burden to the host. I would choose it only when the host electrical path and interop evidence close with adequate margin."

*Trap:* "Scale-up is copper and scale-out is optics."

##### Question 2. Explain pre-FEC errors, corrected errors, uncorrectable errors, and post-FEC behavior.

*Tests:* FEC interpretation and operational meaning.

*Spoken answer.* "Pre-FEC errors describe the raw impairment entering the decoder. Corrected symbol or codeword counts show how much work the FEC is doing while the link remains operational. Uncorrectable events occur when the error pattern exceeds the code's correction capability and may produce packet loss, lane failure, or a link-state event. Post-FEC BER is the residual error rate after decoding. I would never interpret one counter alone. I want the code type, measurement interval, lane distribution, burst shape, and trend relative to the specified threshold. Rising correctable errors can be an early warning even when post-FEC traffic is still clean" (§10.17.1).

*Pressure follow-up.* "The link has zero uncorrectable errors. Is it healthy?"\
*Answer pivot.* "Not necessarily. If correctable errors are rising, highly bursty, concentrated in one lane, or consuming most of the FEC margin, the link may be approaching a cliff. I would trend it and correlate it with temperature, power, equalizer state, and operational events."

*Trap:* "If FEC corrects the errors, there is no problem."

##### Question 3. A lane has rising FEC errors, but average receive power is stable. How do you respond?

*Tests:* power versus quality, layer isolation, and discriminating evidence.

*Spoken answer.* "Stable average power makes gross attenuation less likely, but it does not clear the optical path. I would first confirm which lane and direction are affected and inspect the time distribution of the errors. Then I would compare optical power, temperature, wavelength or lock state, equalizer taps, host SerDes counters, and FEC histograms. Possible mechanisms include RIN, reflections or MPI, transmitter distortion, wavelength drift, receiver noise, timing, crosstalk, or control behavior. A module or fiber swap can help isolate ownership, but I would preserve the original state before disturbing it" (§4.8).

*Pressure follow-up.* "What would make you suspect connector reflection rather than loss?"\
*Answer pivot.* "BER bursts or a floor with little average-power movement, sensitivity to remating or fiber routing, and degraded ORL would support a reflection hypothesis. I would still confirm it with controlled inspection, cleaning, ORL measurement, or a known-good path."

*Trap:* "Power is normal, so the problem must be the host receiver."

##### Question 4. Distinguish a retrain, a link flap, a packet retry, and a workload stall.

*Tests:* event hierarchy and causal ordering.

*Spoken answer.* "A retrain is a PHY or SerDes recovery event in which equalization, clock recovery, lane alignment, or another link-training function is repeated. It may interrupt traffic without always producing a full MAC-level down event. A link flap is an observable transition from link up to down and back, usually causing a larger control-plane or topology reaction. A packet retry or retransmission is a higher-layer response to loss or delivery failure and does not by itself identify the physical cause. A workload stall is the application-level symptom. I align timestamps across those layers before deciding which event caused which" (§10.17.1).

*Pressure follow-up.* "The collective stalled at the same minute as a link flap. Is causality established?"\
*Answer pivot.* "No. Minute-level coincidence is not enough. I need clocks aligned closely enough to order FEC bursts, retraining, link-state transitions, route changes, retries, and workload latency."

*Trap:* "A retrain and a link flap are the same event with different names."

##### Question 5. What telemetry contract would you require before deploying an optical module at scale?

*Tests:* observability, metadata, cadence, and actionability.

*Spoken answer.* "I would define telemetry around decisions rather than collecting every available field. At module level I want identity, serial and lot genealogy, firmware, case temperature, supply power, transmit and receive power, wavelength or lock state where applicable, alarms, and relevant control headroom. At link level I want lane-resolved pre-FEC errors, corrected and uncorrectable distributions, retrains, link-state events, and equalizer state where exposed. I also need host, switch, route, topology, workload, and maintenance timestamps. The schema, units, cadence, retention, clock source, and missing-data behavior must be defined before deployment" (§10.17, §11.16).

*Pressure follow-up.* "Why not collect every register once per second?"\
*Answer pivot.* "More data can create storage, firmware, and interpretation burden without improving decisions. Cadence should match the mechanism: a daily drift metric and a millisecond-scale burst event need different collection strategies."

*Trap:* "Optical power and module temperature are enough for fleet monitoring."

##### Question 6. How do you separate host, module, fiber-plant, peer, and switch ownership?

*Tests:* system-boundary reasoning and controlled isolation.

*Spoken answer.* "I begin by naming the failing direction and reference plane, because a bidirectional link has two transmitters, two receivers, and several electrical and optical boundaries. I compare lane-resolved counters at both ends, then use the least disruptive controlled change: fiber swap, endpoint swap, module swap, host-port swap, or loopback. If the symptom moves with the module, that strengthens module ownership; if it stays with the port, I investigate host channel, switch SerDes, configuration, or thermal environment. For LPO, I am especially careful because the host owns more equalization, CDR, and FEC behavior while the module remains analog" (Table 10.11).

*Pressure follow-up.* "A module swap fixes the link. Is the original module confirmed bad?"\
*Answer pivot.* "It is strong localization evidence, but not always mechanism confirmation. Reseating may also clean a connector, reset state, or alter thermal and mechanical conditions. I preserve and retest the original unit under controlled conditions."

*Trap:* "If the problem disappears after replacing the module, the module was the root cause."

##### Question 7. How does ownership change among a fully retimed module, LPO, LRO, and CPO?

*Tests:* architecture-specific operational boundaries.

*Spoken answer.* "A fully retimed module breaks the host and optical paths into more independent segments; its DSP and CDR absorb much of the host-channel impairment, which helps interoperability but costs power and latency. LPO removes that isolation, so the host owns most equalization, clock recovery, and FEC while the analog module must remain highly linear. LRO places retiming in only part of the path, so direction matters. CPO shortens the electrical path but couples optics more tightly to the switch package, thermals, fiber attach, and service model. I would never assign ownership without first identifying which architecture and direction I am debugging" (Table 10.11, §10.3.1, §10.10).

*Pressure follow-up.* "Why can two individually compliant LPO components still fail together?"\
*Answer pivot.* "Because the end-to-end margin depends on the combined host channel, equalizer behavior, module linearity, noise, and optical path. Point compliance reduces risk but does not replace host-to-host interoperability evidence."

*Trap:* "The module vendor owns optical errors, and the host vendor owns electrical errors."

##### Question 8. A large all-reduce operation slows down, but average fabric utilization looks normal. How do you debug it?

*Tests:* workload-to-link correlation, topology, and straggler amplification.

*Spoken answer.* "I would start with the workload trace and identify the affected collective, rail, rank group, and time window. Average utilization can hide a straggling path, so I would inspect tail latency, per-rail throughput, route balance, queue occupancy, retries, and lane-level FEC behavior. If one rail shows error bursts or flaps, I would reroute or remove that rail and see whether the collective tail improves. If links are clean but queues are persistently full, the problem is more likely congestion, oversubscription, or scheduling. I keep optics, switch, and workload timestamps aligned throughout" (§10.7, §10.16.4).

*Pressure follow-up.* "Why can one weak link affect thousands of accelerators?"\
*Answer pivot.* "Many collectives synchronize participants at each phase. The slowest path can set the completion time, so one marginal link becomes a system-level straggler rather than merely losing its own bandwidth."

*Trap:* "Normal average utilization proves the fabric has enough capacity."

##### Question 9. How does topology change optical count, failure impact, and debugging strategy?

*Tests:* Clos, rails, path diversity, and failure domains.

*Spoken answer.* "Topology determines how many optical links are deployed, which paths share failure domains, and whether traffic can be rerouted. A multi-tier Clos can provide path diversity but adds switch hops, optics, and more possible failure points. Rail-optimized fabrics reduce contention for collective traffic but make one degraded rail highly visible to a particular accelerator group. Hierarchical or dragonfly-style designs trade global bandwidth and long-link count differently. During debugging I need the physical topology and current routes, not just endpoint addresses, because the same workload symptom can result from one marginal link, route imbalance, or an oversubscribed tier" (§10.2).

*Pressure follow-up.* "Would you redesign the topology after seeing repeated collective stalls?"\
*Answer pivot.* "Not before determining whether the stalls come from capacity, routing, or a small set of weak links. A topology rewrite is expensive and may hide a correctable optical or operational problem."

*Trap:* "More path redundancy automatically gives higher availability."

##### Question 10. What is the difference between component reliability and system availability?

*Tests:* FIT, redundancy, repair time, and operational consequence.

*Spoken answer.* "Component reliability describes how often a component is expected to fail under stated assumptions. System availability depends not only on failure rate but also on detection, redundancy, failover behavior, repair time, spare strategy, service access, and whether one failure interrupts useful work. A module with a good FIT rate can still produce poor availability if replacement takes hours or if one failure stalls an entire collective. Conversely, a higher component failure rate may be tolerable when failures are detected quickly, isolated, rerouted, and repaired without workload impact" (§10.17.5, §10.17.6).

*Pressure follow-up.* "What matters more: MTBF or MTTR?"\
*Answer pivot.* "Neither alone. Availability depends on both and on the architecture's ability to mask or contain the failure. I would also include workload restart cost and correlated failure domains."

*Trap:* "A high MTBF means the network will have high availability."

##### Question 11. A link flaps intermittently in the fleet. Walk me through the operational response.

*Tests:* evidence preservation, containment, event ordering, and recurrence control.

*Spoken answer.* "I would preserve the pre-flap and post-flap telemetry before reseating or power cycling: FEC history, retrains, lane state, optical power, temperature, equalizer state, alarms, route changes, and workload impact. Then I would scope the population by module lot, host, port, peer, fiber path, firmware, site, and install age. Operationally, I may reroute, drain, or replace the affected link to protect the workload, but I preserve the original unit and path for controlled analysis. I then reproduce or isolate the mechanism and update the appropriate control: firmware, service procedure, connector inspection, ATP, supplier process, qualification, or telemetry" (§9.11, Chapter 11).

*Pressure follow-up.* "The flap disappears after power cycling. What can you conclude?"\
*Answer pivot.* "Only that state reset affected the symptom. It could be firmware, control, CDR, thermal state, an intermittent interface, or a marginal physical path. The reset may have erased the most valuable evidence."

*Trap:* "Power-cycle it, and replace the module if the flap returns."

##### Question 12. Give me a 60-second operational-debug plan for a degraded AI fabric.

*Tests:* complete workload-to-optics Staff-level answer.

*Spoken answer.* "I start with the workload symptom and identify the affected collective, topology region, and time window. I align clocks across workload, switch, host, link, and module telemetry, then determine whether the evidence points to congestion, route imbalance, packet loss, a link-state event, or gradual PHY-margin loss. For suspect links I inspect lane-level pre-FEC and FEC distributions, retrains, equalizer state, optical power, temperature, wavelength or lock state, and relevant alarms. I use a controlled reroute, fiber swap, module swap, or port swap to isolate ownership while preserving evidence. I contain workload risk first, confirm the mechanism second, and close the case only when a recurrence control and fleet monitor are in place."

*Pressure follow-up.* "What would make you stop deployment or drain a whole cohort?"\
*Answer pivot.* "I would escalate containment when the failure rate is growing, the mechanism can cause correlated loss, telemetry cannot bound the affected population, or the workload impact exceeds the available redundancy. The action should match exposure, confidence, and reversibility."

*Trap:* "I would identify the worst link counters, replace those modules, and monitor the network."

Score each response using the shared chapter-interview rubric in Appendix A.12.1. Repeat answers that do not connect the workload symptom, telemetry evidence, ownership decision, and operational action.


<div class="nav-links">
  <a href="ch9-manufacturing-validation-reproducing-and-controlling-the-design">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-failure-analysis-handbook">Next &rarr;</a>
</div>
