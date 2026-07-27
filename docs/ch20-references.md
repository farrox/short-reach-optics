---
layout: default
title: "References"
---

# References

Complete bibliography for *Short-Reach Optics for AI Compute*.
Source of truth is `sections/references.tex` (same entries as the PDF).
Volatile web sources: access date **2026-07-25** unless a revision date is stated in the entry.

Source-type labels: **standard**, **draft**, **research**, **production datasheet**,
**demonstration**, **vendor announcement**, **roadmap**, **deployment disclosure**,
**editorial inference**.

Architectural arguments belong in the chapters; entries below are supporting sources.

## Standards and MSAs

<a id="ref-ituG694"></a>**ITU-T(2003--20)**

*Source type:* standard · *Date:* 2003--20

ITU-T. [Recommendation ITU-T G.694.1 (10/2020), Spectral grids for WDM applications: DWDM frequency grid](https://www.itu.int/rec/T-REC-G.694.1/en) and [ITU-T G.694.2 (12/2003), CWDM wavelength grid](https://www.itu.int/rec/T-REC-G.694.2/en). G.694.1 anchors the DWDM grid at 193.1 THz with 12.5/25/50/100 GHz spacings and integer multiples; G.694.2 defines the 20 nm CWDM grid, 18 channels from 1271 to 1611 nm. Datacom DWDM locks to G.694.1; CWDM4 uses four O-band lines of G.694.2.

<span class="bibkey">`ituG694`</span>

---

<a id="ref-g664"></a>**ITU-T(2012)**

*Source type:* standard · *Date:* 2012

ITU-T. [Recommendation ITU-T G.664 (02/2012)](https://www.itu.int/rec/T-REC-G.664-201202-I/en). Optical safety procedures; APR with automatic restart; reduce to Hazard Level 1M within 3 s of continuity loss.

<span class="bibkey">`g664`</span>

---

<a id="ref-ieee8023bj"></a>**IEEE 802.3bj(2014)**

*Source type:* standard · *Date:* 2014

IEEE Std 802.3bj-2014. [100 Gb/s Operation Over Backplanes and Copper Cables](https://standards.ieee.org/standard/802_3bj-2014.html). Introduced `100GBASE-KP4 (backplane, PAM4, four lanes) and mandatory RS(544,514) FEC (Clause 91); the ``KP4'' label for that code.

<span class="bibkey">`ieee8023bj`</span>

---

<a id="ref-netmgmt"></a>**Redfish/OpenConfig/SONiC(2015--25)**

*Source type:* standard · *Date:* 2015--25

DMTF, OpenConfig, and the SONiC community. [DMTF Redfish (DSP0266)](https://www.dmtf.org/standards/redfish), [OpenConfig models and gNMI](https://www.openconfig.net/), and [SONiC](https://sonicfoundation.dev/). Box- and fleet-level management and telemetry above OIF CMIS. Redfish: RESTful server/switch management API (v1.0, August 2015). OpenConfig: vendor-neutral YANG models and streaming telemetry. SONiC: open network OS with dataplane telemetry. Where per-module optical monitors surface at cluster scale.

<span class="bibkey">`netmgmt`</span>

---

<a id="ref-itufiber"></a>**ITU-T(2016--24)**

*Source type:* standard · *Date:* 2016--24

ITU-T. [Recommendation ITU-T G.652 (11/2016), Characteristics of a single-mode optical fibre and cable](https://www.itu.int/rec/T-REC-G.652/en) and [ITU-T G.657 (08/2024), Characteristics of a bending-loss insensitive single-mode optical fibre and cable](https://www.itu.int/rec/T-REC-G.657/en). G.652.D sets the standard single-mode fiber used in short-reach links: attenuation $0.2 dB/km at 1550 nm, $0.32 dB/km at 1310 nm, and zero-dispersion wavelength near 1310 nm. G.657 defines bend-insensitive fiber for tight-radius routing in patch panels and shelves; category A stays G.652-compatible, category B trades some standard-fiber interoperability for tighter bend radii.

<span class="bibkey">`itufiber`</span>

---

<a id="ref-lambdamsa"></a>**100G Lambda MSA(2017--20)**

*Source type:* standard · *Date:* 2017--20

100G Lambda MSA Group. *[100G Lambda MSA specifications](https://100glambda.com/) (100G-FR/LR, 400G-DR4/FR4/LR4). Formed 2017 (22 promoter members). Specifications built on 100 Gb/s per wavelength PAM4 ($53 GBd) over duplex single-mode fiber, 2--40 km reaches; defined the single- 100G approach IEEE 802.3 adopted into its DR/FR/LR PMD clauses and that the LPO MSA 100G-DR-LPO profile inherits, including the RIN_xOMA$ transmitter method.

<span class="bibkey">`lambdamsa`</span>

---

<a id="ref-ieee8021ae"></a>**IEEE 802.1(2018--20)**

*Source type:* standard · *Date:* 2018--20

IEEE. [IEEE Std 802.1AE-2018, MAC Security (MACsec)](https://standards.ieee.org/ieee/802.1AE/7154) and [IEEE Std 802.1X-2020, Port-Based Network Access Control](https://standards.ieee.org/ieee/802.1X/12247). MACsec: connectionless user-data confidentiality, frame integrity, and data origin authenticity at the MAC layer, transparent to the MAC client. 802.1X: port-based access control and key agreement that establishes MACsec associations. Line-rate encryption for 800G/1.6T links lives in the switch ASIC or NIC, not the transceiver.

<span class="bibkey">`ieee8021ae`</span>

---

<a id="ref-oif400zr"></a>**OIF(2020)**

*Source type:* standard · *Date:* 2020

Optical Internetworking Forum. [OIF Implementation Agreement for 400ZR](https://www.oiforum.com/technical-work/400zr/). 400 Gb/s coherent DWDM pluggable; 15 W module power budget; DCI reach to $$120 km; interoperable QSFP-DD/OSFP coherent optics.

<span class="bibkey">`oif400zr`</span>

---

<a id="ref-cwwdm"></a>**CW-WDM MSA(2021)**

*Source type:* standard · *Date:* 2021

CW-WDM MSA. *[Continuous-Wave WDM Multi-Source Agreement](https://cw-wdm.org/) Technical Specifications Rev 1.0 (4 June 2021). O-band grids: 8/16/32-line sets in 9/18/36 nm spans; modular (one $/fiber) and integrated (full comb/fiber) configs; measurement methods for power, RIN, SMSR, linewidth. Form factor and management left to suppliers / ELSFP. Informative 18 nm examples often cite 30 dB SMSR, -135 dB/Hz RIN, $20 MHz linewidth.

<span class="bibkey">`cwwdm`</span>

---

<a id="ref-traceloss"></a>**IEEE 802.3df 224G PCB(2022)**

*Source type:* standard · *Date:* 2022

M. Li et al., *[224G Package and PCB Investigations and COM Reference Model](https://www.ieee802.org/3/df/public/22_07/li_3df_01a_2207.pdf), IEEE 802.3df, 2022. M7N stripline loss at 56 GHz: $2.8 dB/inch (regular), $1.9 dB/inch (skip-layer); next-gen target 1 dB/inch at Nyquist.

<span class="bibkey">`traceloss`</span>

---

<a id="ref-tia112"></a>**Krishnamoorthy et al.(2022)**

*Source type:* standard · *Date:* 2022

A 112-Gb/s -8.2-dBm-sensitivity 4-PAM linear TIA in 16-nm CMOS with co-packaged photodiodes. *IEEE J. Solid-State Circuits 58(4), 2023 (32 GHz BW, 16.9 pA/Hz).

<span class="bibkey">`tia112`</span>

---

<a id="ref-ibta"></a>**IBTA(2023)**

*Source type:* standard · *Date:* 2023

InfiniBand Trade Association. [InfiniBand Architecture Specification](https://www.infinibandta.org/ibta-specification/) (Volumes 1 and 2). XDR release October 2023 (Vol. 1 R1.7, Vol. 2 R1.5): 200 Gb/s/lane SerDes, 800 Gb/s per four-lane port, 1.6 Tb/s switch-to-switch; NDR at 400 Gb/s per port. Scale-out fabric alongside Ethernet; reuses QSFP/OSFP form factors and MPO fiber. Dominant vendor NVIDIA (Mellanox). Provisional: XDR rates are from the 2023 spec announcement; confirm against the published specification.

<span class="bibkey">`ibta`</span>

---

<a id="ref-elsfp"></a>**OIF ELSFP(2023)**

*Source type:* standard · *Date:* 2023

Optical Internetworking Forum. [External Laser Small Form-Factor Pluggable (ELSFP) Implementation Agreement](https://www.oiforum.com/wp-content/uploads/OIF-ELSFP-02.0.pdf). OIF-ELSFP-02.0, 2023. 24-pin card-edge electrical interface; CMIS management; blind-mate MT optical connector; optical/thermal/electrical power classes.

<span class="bibkey">`elsfp`</span>

---

<a id="ref-cmis53"></a>**OIF CMIS(2024)**

*Source type:* standard · *Date:* 2024

Optical Internetworking Forum. [CMIS 5.3 Implementation Agreement](https://www.oiforum.com/wp-content/uploads/OIF-CMIS-05.3.pdf) (OIF-CMIS-05.3). Host-to-module management over two-wire bus; module and data-path state machines; DDM, VDM, CDB; link training; ELSFP and CPO extensions.

<span class="bibkey">`cmis53`</span>

---

<a id="ref-cei224"></a>**OIF CEI-224G(2024--25)**

*Source type:* standard · *Date:* 2024--25

Optical Internetworking Forum, [Common Electrical I/O (CEI-224G) framework and implementation agreements](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/); CEI interoperability demos, OFC/ECOC 2025. Reach classes: XSR (die-to-die), VSR (200 mm host + module), MR ($500 mm, 32--34 dB), LR (1 m, up to $40 dB die-to-die). CEI-224G-Linear extends the CEI-112G-Linear methodology to 224G full-linear modules (LPO/CPO/NPO): TP1/TP1a and TP4/TP4a electrical specs without module DSP/CDR.

<span class="bibkey">`cei224`</span>

---

<a id="ref-cignal448"></a>**Cignal AI(2025)**

*Source type:* standard · *Date:* 2025

Cignal AI. [OIF's 448G Workshop: The Need for Speed](https://cignal.ai/2025/04/oifs-448g-workshop-the-need-for-speed/). April 2025. Industry coalescing on PAM6 for electrical chip-to-module; PAM4 at 224 GBd for optics; OFC 2025 400G PAM4 optical demos.

<span class="bibkey">`cignal448`</span>

---

<a id="ref-lpomsa"></a>**LPO MSA(2025)**

*Source type:* standard · *Date:* 2025

LPO MSA, *[100G-DR-LPO Specification](https://www.lpo-msa.org/files/live/sites/lpomsa/files/specs/LPO_MSA_Specification_v1p01.pdf), rev. 1.0, 19 March 2025. 100 Gb/s/lane PAM4 SMF to 500 m; builds on IEEE 802.3 and OIF CEI-112G-LINEAR. TDECQ/TECQ $$3.4 dB; OMA coupled to max(TECQ,TDECQ); host RS(544,514) FEC. Template for linear-module optical limits; 224G linear modules follow CEI-224G-Linear electrically while optical PMDs track 802.3dj.

<span class="bibkey">`lpomsa`</span>

---

<a id="ref-lpo"></a>**LPO/LRO(2025)**

*Source type:* standard · *Date:* 2025

[Linear Pluggable Optics (LPO) and Linear-Receive Optics (LRO/TRO)](https://eps.ieee.org/wp-content/uploads/2026/03/Linear-Pluggable-Optics_V2-UPDATED.pdf): DSP-less and half-retimed module architectures. IEEE EPS overview (2026); OIF/MSA interop demos, OFC 2025. Typical 800G: DSP module $14--18 W, 8--10 ns/hop; LPO 7--9 W, <3 ns, <2 km; LRO 9 W. Redriver = CTLE+VGA (no CDR); retimer = EQ+$CDR. Names component proponents (Macom, Semtech, Maxlinear) and OFC 2024--25 demos from Eoptolink, Macom, Marvell, Alphawave, and Innolight.

<span class="bibkey">`lpo`</span>

---

<a id="ref-huawei448"></a>**OIF 448G Workshop(2025)**

*Source type:* standard · *Date:* 2025

OIF 448G AI Workshop (Lumentum/Huawei et al.). [448G/lane native modulation and gearbox transition](https://www.oiforum.com/wp-content/uploads/OIF-448G-AI-Workshop-Huawei-Kuschnerov_Matuz.pdf). 2025. First 448G optical modules may gear-box 224G SerDes; electrical/optical format alignment preferred for LPO and retimed architectures.

<span class="bibkey">`huawei448`</span>

---

<a id="ref-cei224demo"></a>**OIF CEI Demo OFC(2025)**

*Source type:* standard · *Date:* 2025

Optical Internetworking Forum, *[448G, 224G, 112G CEI Interoperability Demo](https://www.oiforum.com/wp-content/uploads/OIF_CEI_Demo_OFC2025.pdf), OFC 2025. Project map: CEI-224G-XSR ($50 mm), VSR (200+20 mm), MR (500 mm), LR (1000 mm), and CEI-224G-Linear (no module DSP); BER 10^-15$ with FEC allowed. Live Linear/RTLR/VSR/LR demos.

<span class="bibkey">`cei224demo`</span>

---

<a id="ref-cei448"></a>**OIF CEI-448G(2025)**

*Source type:* standard · *Date:* 2025

Optical Internetworking Forum. [Next Generation CEI-448G Framework](https://www.oiforum.com/wp-content/uploads/OIF-FD-CEI-448G-01.0.pdf) (OIF-FD-CEI-448G-01.0, 2025). 448 Gb/s/lane target; PAM4 at 224 GBd (f_N112 GHz), PAM6 at 173 GBd (f_N87 GHz), PAM8 at 149 GBd; connector-limited channels $90 GHz; package BW $115 GHz at 0.5 mm pitch; CPO die-to-OE as PAM4 bypass; SDO liaison map (2.3) and scale-up/out metrics (Table 1).

<span class="bibkey">`cei448`</span>

---

<a id="ref-oif224"></a>**OIF(2025)**

*Source type:* standard · *Date:* 2025

Optical Internetworking Forum. *[CEI-224G and CEI-448G](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/) Common Electrical I/O projects (OIF-FD-CEI-448G-01.0 framework, 2025).

<span class="bibkey">`oif224`</span>

---

<a id="ref-lpocost"></a>**Semtech(2025)**

*Source type:* standard · *Date:* 2025

Semtech. [Low-power 1.6T datacom transceivers and the path to 3.2T](https://blog.semtech.com/webinar-recap-low-power-1.6t-datacom-transceivers-and-the-path-to-3.2t). Webinar recap, 2025. Linear modules cited at $50--60% less power than fully retimed; a 500,000-GPU cluster estimated to save >100 MW and \100 million/year in electricity. Vendor orientation, provisional.

<span class="bibkey">`lpocost`</span>

---

<a id="ref-snia448"></a>**SNIA SFF(2025)**

*Source type:* standard · *Date:* 2025

SNIA SFF Technology Affiliate. [SFF 448G project overview](https://www.oiforum.com/wp-content/uploads/OIF_448G_AI_Workshop-SNIA-2025-03-31_v2_AConstantine.pdf) (OIF 448G AI Workshop). March 2025. Backplane/storage/compute focus; SFF-TA-1043; complements OIF front-panel CEI.

<span class="bibkey">`snia448`</span>

---

<a id="ref-ualink200"></a>**UALink(2025)**

*Source type:* standard · *Date:* 2025

Ultra Accelerator Link Consortium. [UALink 200G 1.0 Specification](https://ualinkconsortium.org/specifications/). April 2025. Open scale-up interconnect; 200G/lane; up to 1 024 accelerators per pod.

<span class="bibkey">`ualink200`</span>

---

<a id="ref-uec10"></a>**UEC(2025)**

*Source type:* standard · *Date:* 2025

Ultra Ethernet Consortium. [UEC Specification 1.0](https://ultraethernet.org/specification/). June 2025. Scale-out Ethernet stack for AI/HPC; Ultra Ethernet Transport (UET).

<span class="bibkey">`uec10`</span>

---

<a id="ref-e4ai448"></a>**IEEE E4AI(2025--26)**

*Source type:* standard · *Date:* 2025--26

IEEE 802.3 ``Ethernet for AI'' ad hoc. [E4AI assessment and 400G/lane CFI materials](https://www.ieee802.org/3/ad_hoc/E4AI/). 3.2 TbE port demand; fast-track 400/800/1600G on 400G/lane; follow-on 3.2T PHYs.

<span class="bibkey">`e4ai448`</span>

---

<a id="ref-tia224"></a>**224G SiGe TIA(2026)**

*Source type:* standard · *Date:* 2026

A 4112-GBaud linear PAM-4 TIA with 65-GHz bandwidth and 13.2-pA/Hz input noise for 1.6-T links. *IEEE Trans. Microw. Theory Tech., 2026 (55-nm SiGe BiCMOS, 224 Gb/s, 1.22 pJ/bit).

<span class="bibkey">`tia224`</span>

---

<a id="ref-xpo"></a>**Arista/XPO MSA(2026)**

*Source type:* standard · *Date:* 2026

Arista Networks (with Coherent, Marvell, Lightmatter, et al.). *XPO: eXtra-dense Pluggable Optics multi-source agreement (12.8 Tb/s liquid-cooled pluggable). Announced OFC 2026; arista.com white paper, March 2026.

<span class="bibkey">`xpo`</span>

---

<a id="ref-rfic460drv"></a>**Da Silva et al.(2026)**

*Source type:* standard · *Date:* 2026

L. Da Silva *et al. [A 460 Gb/s PAM-4 linear distributed driver with 105 GHz BW for TFLN modulators in 130 nm SiGe BiCMOS](https://rfic-ieee.org/paper_abstract/1148). RFIC 2026: 105.7 GHz BW, 2.25 V_pp, 232 GBd PAM4 with offline DSP (research).

<span class="bibkey">`rfic460drv`</span>

---

<a id="ref-ieee400gpl"></a>**IEEE 400G/lane SG(2026)**

*Source type:* standard · *Date:* 2026

IEEE 802.3 400 Gb/s/lane Signaling Study Group. [400 Gb/s per lane signaling for electrical and SMF reaches up to 500 m](https://www.ieee802.org/3/400GPL/); chartered 13 March 2026. PAR/CSD for scale-up copper and IM/DD optics; aligns with CEI-448G / 3.2T module roadmap.

<span class="bibkey">`ieee400gpl`</span>

---

<a id="ref-ieee8023dj"></a>**IEEE 802.3dj(2026)**

*Source type:* draft · *Date:* 2026 · *Accessed:* 2026-07-25

IEEE P802.3dj Task Force. [200 Gb/s, 400 Gb/s, 800 Gb/s, and 1.6 Tb/s Ethernet](https://www.ieee802.org/3/dj/). 200 Gb/s per lane Ethernet (typically $106.25 GBd PAM4 on the AUI/PMD; related OIF CEI-224G electrical class near 112 GBd); KP4 FEC RS(544,514); draft entered SA ballot February 2026; approval expected $late 2026.

<span class="bibkey">`ieee8023dj`</span>

---

<a id="ref-semtech224"></a>**Semtech(2026)**

*Source type:* standard · *Date:* 2026

Semtech Corporation. [224 Gb/s/lane MZM drivers (GN1877/GN1887) and TIA family for LPO/LRO/CPO](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era). March 2026 (OFC); CEI-224G-Linear / LPO-MSA positioning (vendor announcement).

<span class="bibkey">`semtech224`</span>

---

<a id="ref-rinspec"></a>**100G Lambda MSA / IEEE 802.3**

*Source type:* standard

100G Lambda MSA and IEEE 802.3. [*400G-FR4 and 100GBASE-BR technical specifications](https://www.ieee802.org/3/bs/public/) (RIN_17.1OMA-136 dB/Hz; RIN method per IEEE Std 802.3 clause 52.9.6).

<span class="bibkey">`rinspec`</span>

---

## Peer-reviewed papers

<a id="ref-he2019"></a>**He et al.(2019)**

*Source type:* research · *Date:* 2019

M. He *et al. [High-performance hybrid silicon and lithium niobate Mach--Zehnder modulators](https://doi.org/10.1038/s41566-019-0378-6). *Nature Photonics **13, 359--364 (2019). Hybrid Si--LN integration template for co-packaged assemblies.

<span class="bibkey">`he2019`</span>

---

<a id="ref-qdrin"></a>**QD-on-Si RIN(2020--2025)**

*Source type:* research · *Date:* 2020--2025

Intensity-noise studies of epitaxial/heterogeneous quantum-dot lasers on silicon. *Opt. Lett. 45(17):4887 (2020, p-doped QD RIN -150 dB/Hz); *J. Photonics (2024, quiet-pump/injection-locked RIN to -168 dB/Hz); *JLT 43(4):1855 (2025, feedback-tolerant QD on 300 mm Si).

<span class="bibkey">`qdrin`</span>

---

<a id="ref-iec60825"></a>**IEC(2021)**

*Source type:* research · *Date:* 2021

IEC. [IEC 60825-1:2014/AMD1:2021](https://webstore.iec.ch/en/publication/74712) and [IEC 60825-2:2021](https://webstore.iec.ch/en/publication/66912). Laser product classes (1, 1M, 3R, 3B, 4) and OFCS hazard levels at accessible fiber ports.

<span class="bibkey">`iec60825`</span>

---

<a id="ref-chang2023"></a>**Chang et al.(2023)**

*Source type:* research · *Date:* 2023

P.-H. Chang, A. Samanta, P. Yan, *et al. A 3D integrated energy-efficient transceiver realized by direct bond interconnect of co-designed 12 nm FinFET and silicon photonic integrated circuits. *Journal of Lightwave Technology 41(21):6741--6755, 2023. ([link](https://doi.org/10.1109/JLT.2023.3291704))

<span class="bibkey">`chang2023`</span>

---

<a id="ref-cignal"></a>**Cignal AI(2023)**

*Source type:* research · *Date:* 2023

Cignal AI, *[The Linear Drive Market Opportunity](https://cignal.ai/2023/08/linear-drive-market-opportunity/) (2023) and OFC 2025 show report. Market view: LPO stays a small share, especially at 800G, because the installed fabric is DSP-based; 100G/lane 800GbE LPO late to market; at 1.6T, LRO favored over LPO on power/thermal. Provisional (analyst reports).

<span class="bibkey">`cignal`</span>

---

<a id="ref-tpuv4ocs"></a>**Jouppi et al.(2023)**

*Source type:* research · *Date:* 2023

Jouppi, N. P., *et al. (Google). [TPU v4: An optically reconfigurable supercomputer for machine learning with hardware support for embeddings](https://arxiv.org/abs/2304.01433). Proc.\ ISCA, 2023. 4096 accelerators wired through 48 OCS into a reconfigurable 3D torus; per-job topology and route-around-failure for availability and utilization.

<span class="bibkey">`tpuv4ocs`</span>

---

<a id="ref-utc"></a>**UTC-PD(2023)**

*Source type:* research · *Date:* 2023

[Wideband uni-traveling-carrier photodiodes for near-300 Gbps communications](https://arxiv.org/abs/2501.02812). Type-II GaInAsSb/InP UTC-PD >\!110 GHz; InP MUTC-PD 206 GHz (arXiv:2501.02812, 2025).

<span class="bibkey">`utc`</span>

---

<a id="ref-macomlpo"></a>**Macom(2024)**

*Source type:* research · *Date:* 2024

Macom, *[Macom to showcase 200G-per-lane products at OFC](https://ir.macom.com/news-releases/news-release-details/macom-showcase-200g-lane-products-optical-fiber-communication), March 2024. PURE DRIVE 200 Gb/s LPO, extensible to 212 Gb/s/lane for 1.6T; linear TIA and driver as the key blocks. Vendor, provisional.

<span class="bibkey">`macomlpo`</span>

---

<a id="ref-metallama3"></a>**Meta Llama 3(2024)**

*Source type:* research · *Date:* 2024

Grattafiori, A., *et al. (Meta AI). [The Llama 3 herd of models](https://arxiv.org/abs/2407.21783). arXiv:2407.21783, 2024. Reliability snapshot (3.3.4): 16,384 H100 GPUs, 54-day pre-training run, 466 interruptions (419 unexpected, $one every 3 hours), 90% effective training time; 78% hardware, GPU/HBM3 $47%, network switch/cable 35 events (8.4%).

<span class="bibkey">`metallama3`</span>

---

<a id="ref-feclatency"></a>**RS-FEC latency(2024)**

*Source type:* research · *Date:* 2024

Concatenated RS-BCH coded modulation latency study (incl.\ KP4). [Performance-complexity-latency trade-offs of concatenated codes](https://arxiv.org/abs/2402.09364), arXiv:2402.09364, 2024; and vendor RS(544,514) implementation notes. KP4 RS(544,514) decode latency in practice $$20--100 ns depending on implementation and clock; encode is comparable. Academic/vendor figures, provisional.

<span class="bibkey">`feclatency`</span>

---

<a id="ref-daudlin2025"></a>**Daudlin et al.(2025)**

*Source type:* research · *Date:* 2025

S. Daudlin, A. Rizzo, S. Lee, *et al. Three-dimensional photonic integration for ultra-low-energy, high-bandwidth interchip data links. *Nature Photonics 19:502--509, 2025. ([link](https://doi.org/10.1038/s41566-025-01633-0))

<span class="bibkey">`daudlin2025`</span>

---

<a id="ref-gesipd"></a>**Ge/Si PD(2025)**

*Source type:* research · *Date:* 2025

Waveguide germanium-on-silicon photodiodes for 200 GBd and beyond. Shahin et al., *OECC/PSC (2025), recessed Ge/Si PIN: 106 GHz, 0.93 A/W, <\!10 nA dark; *ACS Photonics (2025), SiN-coupled lateral Ge PD >\!110 GHz at 1 mA (O-band).

<span class="bibkey">`gesipd`</span>

---

<a id="ref-tfln224"></a>**Liu et al.(2025)**

*Source type:* research · *Date:* 2025

Y. Liu *et al. [High-speed thin-film lithium niobate modulator with transparent conductive oxide electrodes](https://arxiv.org/abs/2311.05119). arXiv:2311.05119; OFC 2025, paper M3K.2. 108 GHz EO BW; 224 Gb/s PAM4 O-band; V_ L=1.02 V$$cm.

<span class="bibkey">`tfln224`</span>

---

<a id="ref-nvphotonics"></a>**NVIDIA(2025)**

*Source type:* research · *Date:* 2025

NVIDIA. *Spectrum-X and Quantum-X silicon photonics co-packaged-optics switches (GTC 2025; Hot Chips 2025, Shainer).

<span class="bibkey">`nvphotonics`</span>

---

<a id="ref-pirmoradi2025"></a>**Pirmoradi et al.(2025)**

*Source type:* research · *Date:* 2025

A. Pirmoradi, H. Hao, K. Omirzakhov, *et al. [A single-chip 1.024 Tb/s silicon photonics PAM4 receiver](https://arxiv.org/abs/2507.12452). arXiv:2507.12452, 2025.

<span class="bibkey">`pirmoradi2025`</span>

---

<a id="ref-tfmln32t"></a>**St-Arnault et al.(2025)**

*Source type:* research · *Date:* 2025

C. St-Arnault *et al. [Net 3.2 Tbps 225 Gbaud PAM4 O-band IM/DD 2 km transmission with CMOS 3 nm SerDes and TFLN modulators](https://arxiv.org/html/2503.24147). arXiv:2503.24147, 2025 (preprint). Eight $$225 GBd PAM4 lanes; FR8/DR8; HD-FEC threshold.

<span class="bibkey">`tfmln32t`</span>

---

<a id="ref-tflndiffdrv"></a>**Aimone et al.(2026)**

*Source type:* research · *Date:* 2026

A. Aimone *et al. [Truly-differential drive of TFLN TWE-MZM by linear SiGe driver in a codesigned hybrid integrated assembly](https://doi.org/10.1364/OFC.2026.M4D.4). OFC 2026, M4D.4: V_ L=1.1 V$$cm; 140 GBd PAM8; 1.4 pJ/bit.

<span class="bibkey">`tflndiffdrv`</span>

---

<a id="ref-simzm400"></a>**Dong et al.(2026)**

*Source type:* research · *Date:* 2026

P. Dong *et al. [400G/lane PAM4 modulation using silicon Mach--Zehnder modulators](https://doi.org/10.1364/OFC.2026.Th4A.4). OFC 2026 postdeadline, paper Th4A.4. Si MZM with commercial SiGe driver (2.5 V swing); 400 Gb/s/lane PAM4 IM/DD.

<span class="bibkey">`simzm400`</span>

---

<a id="ref-ring224"></a>**Lin et al.(2026)**

*Source type:* research · *Date:* 2026

M.-W. Lin *et al. [Record-high 90-GHz silicon microring modulator and 224-Gb/s PAM4 operation](https://doi.org/10.1364/OFC.2026.Th2A.14). OFC 2026, paper Th2A.14. Inductive and wavelength tuning; compact RLC model; 90-GHz EO BW; CPO target.

<span class="bibkey">`ring224`</span>

---

<a id="ref-macom448"></a>**MACOM(2026)**

*Source type:* research · *Date:* 2026

MACOM Technology Solutions. [448G per-lane PAM4 modulator drivers (MAOM-025408 MZM, MAOM-022404 EML)](https://www.macom.com/updates/news/2026/macom-announces-two-new-448g-per-lane-drivers-for-3-2t-data-cent). March 2026 (OFC). >120 GHz RF bandwidth; SiPh, EML, and TFLN platforms; wire-bond or bumped die.

<span class="bibkey">`macom448`</span>

---

<a id="ref-ring256"></a>**OFC M2A.1(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper M2A.1. [256 Gb/s silicon Euler microring modulator with 3 THz FSR and >67 GHz bandwidth](https://doi.org/10.1364/OFC.2026.M2A.1). O-band Euler ring; inductive peaking; 256 Gb/s PAM4.

<span class="bibkey">`ring256`</span>

---

<a id="ref-simzmcompact"></a>**OFC M2A.6(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper M2A.6. [Compact Mach--Zehnder modulator in 300-mm silicon photonic platform toward 400Gbps/lane](https://doi.org/10.1364/OFC.2026.M2A.6). 500 $$m MZM; 94.7 GHz median EO BW; 2.4 dB median IL at 1310 nm.

<span class="bibkey">`simzmcompact`</span>

---

<a id="ref-ofc360apd"></a>**OFC Th3F.2(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper Th3F.2. [360 Gbps Ge-on-Si avalanche photodiodes operating in the O- and C-band](https://doi.org/10.1364/OFC.2026.Th3F.2). Up to 180 GBd PAM4 below HD-FEC; 70/100 GHz BW; 2/1.5 A/W.

<span class="bibkey">`ofc360apd`</span>

---

<a id="ref-simzmdiff"></a>**OFC W3E.5(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper W3E.5. [Toward 400 G/lane silicon differential-drive Mach--Zehnder modulator with >80 GHz bandwidth](https://doi.org/10.1364/OFC.2026.W3E.5). Differential-drive Si MZM; 81.8 GHz 3-dB EO BW; 100 GBd PAM8 eyes (lab setup).

<span class="bibkey">`simzmdiff`</span>

---

<a id="ref-ofc180drv"></a>**OFC W3E.6(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper W3E.6. [180 GBaud PAM4 driver--modulator engine for IM/DD in the O-band](https://doi.org/10.1364/OFC.2026.W3E.6). Co-packaged 76 GHz InP MZM with 224 GBd-class linear differential EML driver.

<span class="bibkey">`ofc180drv`</span>

---

<a id="ref-ofc420tosa"></a>**OFC W4J.4(2026)**

*Source type:* research · *Date:* 2026

OFC 2026, paper W4J.4. [A 420 Gb/s/lane O-band PAM-4 TOSA based on thin-film lithium niobate](https://doi.org/10.1364/OFC.2026.W4J.4). Co-designed TFLN modulator + driver; 210 GBd / 420 Gb/s PAM4.

<span class="bibkey">`ofc420tosa`</span>

---

<a id="ref-ring400"></a>**Peng et al.(2026)**

*Source type:* research · *Date:* 2026

C.-W. Peng *et al. [Ultra-high bandwidth silicon microring modulator with T-coil peaking for >400 Gbps transmission](https://doi.org/10.1364/OFC.2026.M2A.2). OFC 2026, paper M2A.2. >110 GHz EO BW; 416 Gb/s PAM4, TDECQ 2.88 dB at 1 Vpp.

<span class="bibkey">`ring400`</span>

---

<a id="ref-gesiapd100"></a>**Shahin et al.(2026)**

*Source type:* research · *Date:* 2026

A. Shahin *et al. [Towards 100 GHz waveguide Ge/Si avalanche photodiodes for high-speed optical interconnects](https://doi.org/10.1109/JLT.2026.3670103). *JLT 2026: >100 GHz peak BW; 70 GHz at 2 A/W; $$7 V; 300 mm SOI.

<span class="bibkey">`gesiapd100`</span>

---

<a id="ref-tfln200mm"></a>**OFC 2026 W1A.3**

*Source type:* research

OFC 2026, paper W1A.3. [200-mm silicon-compatible TFLN platform](https://doi.org/10.1364/OFC.2026.W1A.3). 110 GHz EO modulators; V_ L=1.9 V$$cm; foundry-scale integration path.

<span class="bibkey">`tfln200mm`</span>

---

## Books and foundational references

<a id="ref-miller2009"></a>**Miller(2009)**

*Source type:* research · *Date:* 2009

D. A. B. Miller. Device requirements for optical interconnects to silicon chips. *Proceedings of the IEEE 97(7):1166--1185, 2009. ([link](https://doi.org/10.1109/JPROC.2009.2014298))

<span class="bibkey">`miller2009`</span>

---

<a id="ref-miller2017"></a>**Miller(2017)**

*Source type:* research · *Date:* 2017

D. A. B. Miller. Attojoule optoelectronics for low-energy information processing and communications. *Journal of Lightwave Technology 35(3):346--396, 2017. ([link](https://doi.org/10.1109/JLT.2017.2647779))

<span class="bibkey">`miller2017`</span>

---

<a id="ref-sackinger2018"></a>**Säckinger(2018)**

*Source type:* research · *Date:* 2018

E. Säckinger. *Analysis and Design of Transimpedance Amplifiers for Optical Receivers. Wiley, 2018 (Chapter 4: Receiver Fundamentals). ([link](https://doi.org/10.1002/9781119264422))

<span class="bibkey">`sackinger2018`</span>

---

## Reliability and manufacturing standards

<a id="ref-gr1221"></a>**Telcordia(1999)**

*Source type:* standard · *Date:* 1999

Telcordia. *GR-1221-CORE: Generic Reliability Assurance Requirements for Passive Optical Components, Issue 2 (January 1999). Passive-component companion to GR-468: connectors, couplers, WDM filters, splitters, and isolators. Same stress families (damp heat, temperature cycle, mechanical, aging) scored on insertion and return loss rather than LIV. ([link](https://telecom-info.njdepot.com/))

<span class="bibkey">`gr1221`</span>

---

<a id="ref-gr468"></a>**Telcordia(2004)**

*Source type:* standard · *Date:* 2004

Telcordia. *GR-468-CORE: Generic Reliability Assurance Requirements for Optoelectronic Devices. ([link](https://telecom-info.njdepot.com/))

<span class="bibkey">`gr468`</span>

---

<a id="ref-iec61300"></a>**IEC(2009--22)**

*Source type:* standard · *Date:* 2009--22

IEC. [IEC 61300-2-2:2009, Basic test and measurement procedures -- Mating durability](https://webstore.ansi.org/standards/iec/iec61300ed2009-1296572) and [IEC 61300-3-35:2022, Visual inspection of fibre optic connectors and fibre-stub transceivers](https://webstore.iec.ch/en/publication/64254). IEC 61300-2-2 defines the mate/unmate cycling test method that connector datasheets rate against; TIA-568.3 sets 500 cycles as the structured-cabling durability floor, and MPO/MTP-class connectors are commonly rated well above 1000. IEC 61300-3-35 grades endface scratches, pits, and debris against zones on the fiber core and cladding for pass/fail inspection.

<span class="bibkey">`iec61300`</span>

---

<a id="ref-jesd78"></a>**JEDEC(2023)**

*Source type:* standard · *Date:* 2023

JEDEC Solid State Technology Association. [JESD78F.02, IC Latch-Up Test](https://www.jedec.org/standards-documents/docs/jesd-78b). Published November 2023. Overvoltage and 100 mA current-injection test method for parasitic-thyristor latch-up susceptibility in CMOS, bipolar, and BiCMOS ICs; the failure mode COD is to a laser facet.

<span class="bibkey">`jesd78`</span>

---

<a id="ref-aecq100"></a>**AEC(2023--25)**

*Source type:* standard · *Date:* 2023--25

Automotive Electronics Council. [AEC-Q100 Rev-J, Failure Mechanism Based Stress Test Qualification for Integrated Circuits](http://aecouncil.com/). Automotive-grade IC qualification built on the JEDEC JESD47/JESD22 methods with tightened ESD targets and temperature grades (Grade 3: -40 to 85 C through Grade 0: -40 to 150 C). Not required for datacenter optics, but a useful borrow when a driver or TIA die also ships in an automotive part number and the datasheet cites a Q100 grade.

<span class="bibkey">`aecq100`</span>

---

<a id="ref-jsesd"></a>**JEDEC/ESDA(2024--25)**

*Source type:* standard · *Date:* 2024--25

JEDEC Solid State Technology Association and ESD Association. [ANSI/ESDA/JEDEC JS-001-2024, Human Body Model (HBM) ESD Sensitivity Testing](https://www.jedec.org/standards-documents/docs/js-001-2023) and [JS-002-2025, Charged Device Model (CDM) ESD Sensitivity Testing](https://www.jedec.org/standards-documents/docs/js002-2014). Component-level ESD classification for driver, TIA, and DSP silicon. Supersede the older JEDEC-only JESD22-A114 (HBM) and JESD22-C101 (CDM) test methods.

<span class="bibkey">`jsesd`</span>

---

<a id="ref-jesd47"></a>**JEDEC(2025)**

*Source type:* standard · *Date:* 2025

JEDEC Solid State Technology Association. [JESD47M, Stress-Test-Driven Qualification of Integrated Circuits](https://www.jedec.org/standards-documents/docs/jesd-47g). Published August 2025. Baseline acceptance-test flow (temperature cycle, HTOL/HTSL, autoclave/HAST, mechanical shock and vibration) for qualifying an IC as a new product, a product family, or after a process change. The silicon-side counterpart to Telcordia GR-468-CORE for optoelectronics.

<span class="bibkey">`jesd47`</span>

---

## Vendor datasheets

<a id="ref-soa"></a>**O-band SOA(2019--2023)**

*Source type:* production datasheet · *Date:* 2019--2023

Semiconductor optical amplifiers for datacom booster/distribution use. Commercial O-band SOA modules quote $15 dB gain, noise figure 7 dB, and $1.5 dB polarization-dependent gain ([Anritsu SOA datasheet](https://www.anritsu.com/en-US/sensing-devices/products/soa)); the quantum NF floor is 3 dB. [O-band quantum-dot SOAs grown on a CMOS-compatible silicon substrate](https://pubs.acs.org/doi/10.1021/acsphotonics.9b00903) (*ACS Photonics, 2019) give wide O-band gain with low noise for co-packaged integration. An SOA restores launch power after comb generation and fan-out, at the cost of added ASE. Vendor/academic figures.

<span class="bibkey">`soa`</span>

---

<a id="ref-switchlat"></a>**AI switch latency(2025--26)**

*Source type:* production datasheet · *Date:* 2025--26

Vendor switch datasheets (Ethernet and InfiniBand). [800GbE 51.2 Tb/s SONiC switch, $560 ns port-to-port](https://cloudswit.ch/product/800gbe-switch-512tbps-enterprise-sonic/); NVIDIA Quantum-X800 InfiniBand advertises sub-100 ns port-to-port with in-network compute. Per-hop O-E-O switch latency: a few hundred ns for cut-through Ethernet, under $100 ns for InfiniBand. Vendor orientation, provisional.

<span class="bibkey">`switchlat`</span>

---

<a id="ref-semtech448demo"></a>**Semtech OFC demos(2026)**

*Source type:* production datasheet · *Date:* 2026

Semtech Corporation. [OFC 2026: 224G optical demos and 448G/lane PMD ICs (TN622 driver, TN14740 TIA)](https://www.semiconductor-today.com/news_items/2026/mar/semtech-160326.shtml). Vendor demonstration; provisional until datasheet limits are published.

<span class="bibkey">`semtech448demo`</span>

---

<a id="ref-koherondrv200"></a>**Koheron DRV200**

*Source type:* production datasheet

Koheron. [*DRV200 low-noise laser diode driver datasheet](https://www.koheron.com/) (current noise density at 1 kHz: 55 / 270 / 480 pA/Hz for 40 / 200 / 400 mA variants).

<span class="bibkey">`koherondrv200`</span>

---

<a id="ref-eclplanex"></a>**RIO PLANEX**

*Source type:* production datasheet

RIO Lasers. [*PLANEX 1550 nm external-cavity laser datasheet](https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/rio-laser/orion-planex-external-cavity-laser.pdf). Planar gain-chip and Bragg-grating external cavity with narrow linewidth, low phase noise, and wavelength stability; sensing and metrology product rather than a short-reach IM/DD default. Vendor orientation, provisional.

<span class="bibkey">`eclplanex`</span>

---

## Vendor announcements and demonstrations

<a id="ref-qdcomb"></a>**QD comb(2022--2025)**

*Source type:* demonstration · *Date:* 2022--2025 · *Accessed:* 2026-07-25

Quantum-dot mode-locked laser (QD-MLL) frequency combs for datacom. [High-efficiency QD lasers as comb sources for DWDM](https://www.mdpi.com/2076-3417/12/4/1836), *Appl.\ Sci. 12(4):1836 (2022): among DFB arrays, nonlinear microcombs, and semiconductor MLLs, QD-MLLs currently offer the best efficiency, simplicity, and size for a single-device comb. O-band IM/DD demos: a 1.3 m InAs/InGaAs QD-MLL comb carrying 14$100 Gb/s PAM4 over 10 km SMF at $284 fJ/bit; and an isolator-free QD-MLL comb reported for interconnects beyond 3.2 Tb/s ([arXiv:2506.02402](https://arxiv.org/abs/2506.02402), 2025). Research demos, provisional.

<span class="bibkey">`qdcomb`</span>

---

<a id="ref-alphawavelpo"></a>**Alphawave/InnoLight(2024)**

*Source type:* demonstration · *Date:* 2024 · *Accessed:* 2026-07-25

Alphawave Semi and InnoLight, *[Low-latency LPO with a PCIe 6.0 subsystem for AI infrastructure](https://awavesemi.com/press-release/alphawave-semi-and-innolight-collaborate-to-demonstrate-low-latency-linear-pluggable-optics-with-pcie-6-0-subsystem-solution-for-high-performance-ai-infrastructure-at-ofc-2024/), March 2024. 64 Gb/s/lane PCIe 6.0 controller+PHY over InnoLight LPO OSFP optics (OFC 2024); later a 128 Gb/s/lane PCIe 7.0-ready platform. Vendor, provisional.

<span class="bibkey">`alphawavelpo`</span>

---

<a id="ref-eoptolinklpo"></a>**Eoptolink(2024)**

*Source type:* demonstration · *Date:* 2024 · *Accessed:* 2026-07-25

Eoptolink, *[Industry-first 200G-per-lane LPO; 100G/lane 800G LPO entering mass production](https://www.eoptolink.com/news/13-new-products/348-eoptolink-demonstrates-industry-1st-200g-lane-lpos-with-100g-lane-800g-lpos-entering-mass-production), March 2024. 200G/$$ four-channel LPO, no DSP/CDR; Gen2 100G/lane 800G and 400G SMF (OSFP, QSFP-DD, QSFP112), full TP2 compliance claimed. Vendor, provisional.

<span class="bibkey">`eoptolinklpo`</span>

---

<a id="ref-avicena2025"></a>**Avicena(2025)**

*Source type:* demonstration · *Date:* 2025 · *Accessed:* 2026-07-25

Avicena. *Ultra-low-power microLED link at 200 fJ/bit (LightBundle). ECOC 2025 demonstration. ([link](https://www.avicena.tech/))

<span class="bibkey">`avicena2025`</span>

---

<a id="ref-th6davisson"></a>**Broadcom(2025)**

*Source type:* vendor announcement · *Date:* 2025

Broadcom Inc. *Tomahawk 6 -- Davisson: 102.4 Tb/s co-packaged-optics Ethernet switch (press release and briefs). October 2025.

<span class="bibkey">`th6davisson`</span>

---

<a id="ref-tfln390"></a>**He et al.(2025)**

*Source type:* demonstration · *Date:* 2025 · *Accessed:* 2026-07-25

M. He *et al. [Dual-band thin-film lithium niobate modulators for 390 Gb/s PAM8 transmission](https://arxiv.org/abs/2411.15037). *Laser & Photonics Reviews, 2025; arXiv:2411.15037. Extrapolated 220 GHz EO BW; V_ L1.08--1.33 V$$cm; sub-fJ/bit lab demo.

<span class="bibkey">`tfln390`</span>

---

<a id="ref-hyperlight110"></a>**HyperLight(2025)**

*Source type:* vendor announcement · *Date:* 2025 · *Accessed:* 2026-07-25

HyperLight Corp. [110-GHz packaged TFLN IQ modulators for 240-GBaud-class signaling](https://www.hyperlightcorp.com/news/hyperlight-announces-110-ghz-modulators). September 2025 (vendor announcement; provisional).

<span class="bibkey">`hyperlight110`</span>

---

<a id="ref-microcomb"></a>**Kerr microcomb source(2025)**

*Source type:* demonstration · *Date:* 2025 · *Accessed:* 2026-07-25

Integrated Kerr/soliton microcomb multi-wavelength sources. [Integrated multi-port multi-wavelength coherent optical source](https://doi.org/10.1038/s41467-025-61288-x), *Nat.\ Commun. 16 (2025): a Kerr microcomb with a monolithically integrated demultiplexer that autonomously locks to and tracks the comb lines, aimed at beyond-Tb/s links. A microcomb turns one pump into hundreds of evenly spaced lines on a chip, but per-line power is low (pump-conversion efficiency is modest), so a booster or per-line SOA is usually required (sec:soa-distribution). Research demos, provisional.

<span class="bibkey">`microcomb`</span>

---

<a id="ref-jalapeno2026"></a>**Broadcom et al.(2026)**

*Source type:* vendor announcement · *Date:* 2026 · *Accessed:* 2026-07-25

Broadcom and hyperscaler partner. *[LLM-optimized inference processor announcement (Broadcom, June 2026)](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-unveil-llm-optimized-intelligence-processor).

<span class="bibkey">`jalapeno2026`</span>

---

## Public deployment disclosures

<a id="ref-hcf2025"></a>**Chen et al.(2025)**

*Source type:* deployment disclosure · *Date:* 2025 · *Accessed:* 2026-07-25

Y. Chen, M. N. Petrovich, E. Numkam Fokoua, *et al. (Southampton/Microsoft). [Record-low-loss hollow-core fibre](https://doi.org/10.1038/s41566-025-01633-0) (double nested antiresonant nodeless fibre, DNANF). *Nature Photonics, September 2025: 0.091 dB/km at 1550 nm (below the $0.14 dB/km silica floor), 0.2 dB/km over a 66 THz window; air guiding gives group index near 1.0, $45% faster propagation (about a third lower latency) than silica. Microsoft reports Azure network deployment. Record result, provisional.

<span class="bibkey">`hcf2025`</span>

---

## Research roadmaps

<a id="ref-roofline"></a>**Roofline(2009)**

*Source type:* roadmap · *Date:* 2009 · *Accessed:* 2026-07-25

S. Williams, A. Waterman, and D. Patterson. *[Roofline: An Insightful Visual Performance Model for Multicore Architectures](https://doi.org/10.1145/1498765.1498785). Communications of the ACM, 2009. Arithmetic intensity (FLOP/byte) vs.\ the compute/bandwidth balance point; the framework behind the decode memory-bound argument.

<span class="bibkey">`roofline`</span>

---

<a id="ref-cpc"></a>**CPC/NPC(2025--2026)**

*Source type:* roadmap · *Date:* 2025--2026 · *Accessed:* 2026-07-25

Co-packaged and near-package copper, copper's answer to the same reach wall that drives CPO. [Molex co-packaged copper (CPC)](https://www.molex.com/content/molex/molex-dot-com/language-masters/en/industries-applications/data-center-connector-solutions/near-asic/co-packaged-copper.html): on-substrate routing validated at 224 Gb/s PAM4 with a stated roadmap to 448G, aimed at short scale-up runs where power, latency, and cost favor copper over optics. The Impress compression substrate connector and mating cable support 224 Gb/s PAM4 and beyond. [Marvell 224G long-reach SerDes](https://www.marvell.com/blogs/224g-long-range-serdes-scale-up-scale-inside.html) reports $$4 pJ/bit and targets CPC cables, near-packaged optics, and CPO. Near-package copper (NPC) mates the connector near the ASIC rather than onto the package substrate; shared NPC/NPO sockets have been proposed. Vendor orientation, provisional.

<span class="bibkey">`cpc`</span>

---

## Other sources

<a id="ref-iec617547"></a>**IEC(2014--17)**

*Source type:* research · *Date:* 2014--17

IEC. [IEC 61754-7-1:2014, Fibre optic connector interfaces -- Type MPO connector family: one fibre row](https://webstore.ansi.org/standards/iec/iec61754eden2014) and [IEC 61754-7-2:2017, Type MPO connector family: two fibre rows](https://webstore.iec.ch/en/publication/30239). Mechanical interface standard for the MPO/MT connector family: 6.4 mm $$ 2.5 mm rectangular ferrule, guide-pin alignment, 8/12/16/24-fiber counts. Superseded the single-part IEC 61754-7:2008 to add active-device receptacles and up-angled plugs.

<span class="bibkey">`iec617547`</span>

---

<a id="ref-fibercabling"></a>**ISO/IEC and TIA(2017--24)**

*Source type:* research · *Date:* 2017--24

ISO/IEC and TIA. [ISO/IEC 11801:2017, Information technology: Generic cabling for customer premises](https://www.iso.org/standard/66763.html) and the [TIA-492 series, Detail Specifications for Optical Fibers](https://www.tiaonline.org/). ISO/IEC 11801 defines the cabled fiber performance classes used in datacenter patch plant: OM1--OM5 for multimode and OS1/OS2 for single-mode. TIA-492 gives the matching detailed fiber specifications (for example TIA-492AAAD corresponds to OM4); TIA-568 adopts the same OM/OS class names for structured cabling.

<span class="bibkey">`fibercabling`</span>

---

<a id="ref-jupiterocs"></a>**Google Jupiter(2022)**

*Source type:* research · *Date:* 2022

Poutievski, L., *et al. (Google). [Jupiter evolving: transforming Google's datacenter network via optical circuit switches and software-defined networking](https://doi.org/10.1145/3544216.3544265). Proc.\ ACM SIGCOMM, 2022. MEMS OCS under SDN control; Palomar 136136 OCS, $2 dB insertion loss, millisecond switching, circulators for bidirectional links; reported 30% capex, $41% power, and 3x reconfiguration gains on a direct-connect topology.

<span class="bibkey">`jupiterocs`</span>

---

<a id="ref-ucie"></a>**UCIe(2022--25)**

*Source type:* research · *Date:* 2022--25

UCIe Consortium. [Universal Chiplet Interconnect Express (UCIe) Specification](https://www.uciexpress.org/). Open die-to-die chiplet interconnect (physical layer, protocol stack, software model). 1.0 (March 2022); 2.0 (August 2024) adds 3D packaging and in-field manageability; 3.0 (2025) roughly doubles bandwidth. Parallel package/interposer counterpart to CEI XSR; relevant to co-packaged optical I/O and optical-UCIe work.

<span class="bibkey">`ucie`</span>

---

<a id="ref-lbnl2024"></a>**LBNL(2024)**

*Source type:* research · *Date:* 2024

A. Shehabi et al. *[2024 United States Data Center Energy Usage Report](https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf). Lawrence Berkeley National Laboratory, December 2024. US data centers: 58 TWh (2014) $ 176 TWh (2023, 4.4% of US electricity) $ projected 325--580 TWh (6.7--12%) by 2028.

<span class="bibkey">`lbnl2024`</span>

---

<a id="ref-marvelllpo"></a>**Marvell(2024)**

*Source type:* research · *Date:* 2024

Marvell, *[Marvell introduces 1.6 Tbps LPO chipset](https://www.marvell.com/company/newsroom/marvell-introduces-1-6-tbps-lpo-chipset.html), December 2024. 200G/lane TIA and laser-driver chipset for 800G and 1.6T LPO, targeting scale-up XPU compute fabrics. Vendor, provisional.

<span class="bibkey">`marvelllpo`</span>

---

<a id="ref-dac224"></a>**Synopsys 224G DAC(2024)**

*Source type:* research · *Date:* 2024

Reliable 2 m+ passive DAC connectivity for AI-scale networks with 224G PHY IP (BER $2 10^-9 at 2 m); passive DAC 0.5--1 m nominal, AEC to $2.5 m at 224G.

<span class="bibkey">`dac224`</span>

---

<a id="ref-cpocooling"></a>**Cao et al.(2025)**

*Source type:* research · *Date:* 2025

Cao, *et al. [Simulation and experimental investigation of liquid-cooling thermal management for high-bandwidth co-packaged optics](https://doi.org/10.1007/s12200-025-00156-4). Front.\ Optoelectron., 2025. Power density and on-package thermal crosstalk limit CPO reliability; liquid cooling investigated to hold optical-engine and laser temperature.

<span class="bibkey">`cpocooling`</span>

---

<a id="ref-ocsmarket"></a>**Cignal AI(2025)**

*Source type:* research · *Date:* 2025

Cignal AI. [The optical circuit switching market](https://cignal.ai/2025/12/the-optical-circuit-switching-market-4q25/). 2025. OCS technology survey (MEMS, liquid crystal, piezoelectric, robotic, silicon photonic) and transceiver impact: FR single-fiber over DR, circulators, higher-power optics. Analyst report; figures provisional.

<span class="bibkey">`ocsmarket`</span>

---

<a id="ref-cxl4"></a>**CXL(2025)**

*Source type:* research · *Date:* 2025

CXL Consortium. [Compute Express Link (CXL) 4.0 Specification](https://computeexpresslink.org/). Released 18 November 2025 on a PCIe 7.0 base (128 GT/s, PAM4); coherent CPU/accelerator/memory fabric with memory pooling and bundled ports. Relevant to in-rack memory disaggregation and optical CXL. Provisional: 2025 release; verify details against the final published specification.

<span class="bibkey">`cxl4`</span>

---

<a id="ref-dctco"></a>**Epoch AI(2025)**

*Source type:* research · *Date:* 2025

Epoch AI. [Total cost of ownership of a one-gigawatt AI data center](https://epoch.ai/data-insights/ai-datacenter-cost-breakdown). Data insight, 2025. A 1 GW AI site estimated near \38 billion up-front capex and \0.9 billion/year opex. Analyst breakdown, provisional. thebibliography

<span class="bibkey">`dctco`</span>

---

<a id="ref-ocpai"></a>**OCP(2025)**

*Source type:* research · *Date:* 2025

Open Compute Project. [Optical Circuit Switching subproject](https://www.opencompute.org/projects/optical-circuit-switching); Open Systems for AI. 2025. Open rack/cluster designs; OCS for AI fabric reconfiguration.

<span class="bibkey">`ocpai`</span>

---

<a id="ref-pcie7"></a>**PCI-SIG(2025)**

*Source type:* research · *Date:* 2025

PCI-SIG. [PCI Express 7.0 Specification](https://pcisig.com/) and Optical Workgroup interconnect revision. Released 11 June 2025: 128 GT/s per lane, PAM4, flit encoding ($$512 GB/s bidirectional on a x16 link). The PCI-SIG Optical Workgroup (2023) targets a technology-agnostic optical PCIe interface for reach beyond copper. Provisional: 2025 release; rates and optical-interface scope pending cross-check against the final published specification.

<span class="bibkey">`pcie7`</span>

---

<a id="ref-synopsys448"></a>**Synopsys 448G(2025)**

*Source type:* research · *Date:* 2025

Synopsys. [Designing for 448G: Modulation, DSP, and Channel Feasibility](https://www.synopsys.com/content/dam/synopsys/white-papers/designing-for-448g-modulation-dsp-wp.pdf). White paper, 2025. PAM4 (224 GBd, 112 GHz Nyquist) vs.\ PAM6 (179 GBd, 90 GHz); dual-mode 448G SerDes channel simulations on 224G-class links.

<span class="bibkey">`synopsys448`</span>

---

<a id="ref-apd"></a>**UMC-APD(2025)**

*Source type:* research · *Date:* 2025

[Ultrafast avalanche photodiode exceeding 100 GHz bandwidth](https://doi.org/10.1038/s41467-025-66047-6). *Nat.\ Commun. (2025): Ge/Si UMC-APD, 105 GHz at gain $7; GBP 4800 GHz; 224/260 Gb/s PAM4 at -10.9/-10.1 dBm ($9 dB over PIN).

<span class="bibkey">`apd`</span>

---

<a id="ref-ayar"></a>**Ayar Labs(2026)**

*Source type:* research · *Date:* 2026

Ayar Labs. *[SuperNova light source and TeraPHY optical I/O chiplet](https://ayarlabs.com/supernova/). ayarlabs.com.

<span class="bibkey">`ayar`</span>

---

<a id="ref-switchthermal"></a>**FiberMall(2026)**

*Source type:* research · *Date:* 2026

FiberMall. [OSFP thermal management: data center cooling guide](https://www.fibermall.com/blog/osfp-thermal-management-guide.htm). 2026. A 32-port 800G switch dissipates >1 kW, with optical modules $$50% of the thermal load; observed power runs 15--25% above rated. Vendor orientation, provisional.

<span class="bibkey">`switchthermal`</span>

---

<a id="ref-coupe"></a>**TSMC(2026)**

*Source type:* research · *Date:* 2026

TSMC. *Compact Universal Photonic Engine (COUPE): SoIC-X electronic/ photonic integration; mass-production milestone. 2026.

<span class="bibkey">`coupe`</span>

---

<a id="ref-cobo"></a>**COBO / OBO--NPO--CPO**

*Source type:* research

Consortium for On-Board Optics, *On-Board Optical Module Specification; and comparative analyses of pluggable, on-board (OBO), near-packaged (NPO), and co-packaged (CPO) optics architectures.

<span class="bibkey">`cobo`</span>

---

## Endnotes and worked clarifications

Chapter sidenotes and inline clarifications remain in the chapter HTML pages.
This page holds bibliographic sources only; interpretive arguments stay with the teaching text.
