---
layout: default
title: "Ch 10: Abbreviations"
---

# Abbreviations

This glossary is adapted from the OIF *Next Generation CEI-448G Framework* glossary (pages 7--11, OIF-FD-CEI-448G-01.0, September 2025) . Some entries include material from public reference sources noted in the original.

ADC

: An analog-to-digital converter is a system that converts an analog signal into a digital signal.

AI

: Artificial intelligence.

ACC

: Active copper cable. ACCs are a type of active copper cable used in data centers. ACCs primarily use Redriver chips and Continuous Time Linear Equalization (CTLE) to amplify and equalize the signal and provide longer reach than DACs. ACCs generally are lower power and cost than AECs (another type of active copper cable), but provide shorter reach than AECs.

AEC

: Active electrical cable. AECs are a type of active copper cable used in data centers. AECs utilize Retimer chips with Clock and Data Recovery (CDR) to reshape and retransmit signals which generally offer longer reach and better signal integrity compared to ACCs, but at a higher cost.

Application spaces

: Portions of equipment or network architecture that could benefit from having a defined set of interconnection parameters.

ASIC

: An application-specific integrated circuit is an integrated circuit (IC) customized for a particular use, rather than intended for general-purpose use.

Backplane

: A group of electrical connections used as a backbone to connect several printed circuit boards together to make up a switch, computing or storage system.

BER

: Bit error ratio is a measure of the number of bit errors that occur during data transmission, expressed as a ratio of erroneous bits to the total number of bits transmitted.

BoW

: Bunch of wires is a die-to-die interface specification. It is part of the open compute project (OCP) and, like UCIe, is used to connect chiplets within a package.

Cabled host

: An implementation where twinaxial cable is used instead of PCB traces expressly for the insertion loss benefits or 3D architecture.

CDR

: Clock and data recovery, a component that re-establishes the timing of a signal that may have degraded due to impairments on a transmission line, the retimed signal is able to continue further to its destination.

CEI

: Common Electrical IO, an OIF Implementation Agreement containing clauses defining electrical interface specifications, each optimized for various reaches at minimal power.

Coded modulation

: Coded modulation is a technique in digital communication that combines error-control coding with modulation to enhance reliability and efficiency. Its main goal is to balance bandwidth efficiency, power efficiency, and error probability.

CMIS

: Common management information specification.

CMIS-LT

: CMIS-based link training provides a message set and exchange mechanism for out-of-band link training or tuning between a pluggable module and a host.

CMIS-VCS

: CMIS versatile control set extends the base CMIS standard to allow for more advanced and flexible signal integrity (SI) capabilities.

CPC

: Co-packaged copper is an emerging interconnect technology where copper cables are directly attached to the top of an Application-Specific Integrated Circuit (ASIC) or other high-speed integrated circuit within a single package. This design minimizes the length of high-speed electrical signals on the printed circuit board (PCB) and package, addressing the limitations of traditional copper traces at increasingly high data rates (e.g., 224G and above).

CPO

: Co-packaged optics. An electrical to optical device intended to be mounted on the host package.

CTLE

: Continuous time linear equalizer.

DAC

: Direct attach copper cable. A high-speed cable assembly made of copper twinaxial cable with fixed passive transceiver modules on each end. DAC cables enable direct, electrical connections between networking devices over short distances.

DER

: Detector error ratio.

DFE

: Decision feedback equalizer. An equalizer by adding a filtered version of previous symbol estimates to the original filter output.

DSP

: Digital signal processing.

ENOB

: Effective number of bits. A measure of the dynamic performance of an analog-to-digital converter (ADC).

Faceplate

: A plate, cover, or bezel on the front of a device which may contain I/O ports.

FEC

: Forward error correction gives a receiver the ability to correct errors without needing a reverse channel to request retransmission of data.

FFE

: Feed forward equalizer.

Gbps

: Gigabits per second. The throughput or data rate of a port or piece of equipment. Gbps is $1\times10^{9}$ bits per second.

GBd

: The baud rate is the number of electrical transitions per second, also called symbol rate. Giga Baud is $1\times10^{9}$ symbols per second.

Gearbox

: A component used for managing and manipulating data streams, primarily by converting multiple serial data streams at one rate to multiple streams at another rate,

Hamming codes

: A type of linear error-correcting code used in digital communication and data storage systems. It enhances data integrity by detecting and correcting single-bit errors that may occur during transmission or storage.

HPC

: High performance compute.

HPDC

: High-performance data center. A general term for data centers designed for high-compute workloads like AI/HPC.

IA

: Implementation Agreements, what the OIF names their defined interface specifications.

IC

: Integrated circuit.

IMDD

: Intensity modulation direct detection is a method where the intensity of a light source is modulated by an electrical signal. This modulated light then travels through an optical medium (like a fiber optic cable) and is directly detected by a photo detector at the receiving end. This is a common and relatively straightforward technique for transmitting information over optical links.

I/O

: Input Output, a common name for describing a port or ports on equipment.

ISI

: Intersymbol interference.

KP4 FEC

: A specific Reed-Solomon FEC (544,514) defined in IEEE 802.3 Clause 91, commonly used in Ethernet standards.

LDPC

: A low-density parity-check code is a linear error correcting code, a method of transmitting a message over a noisy transmission channel. An LDPC is constructed using a sparse Tanner graph. LDPC codes are capacity-approaching codes.

LR

: Long reach. CEI LR specifies backplane/midplane and copper cable electrical interfaces.

LPO

: Linear pluggable optic is a technology used in optical transceivers that simplifies the design of pluggable optical modules by removing the traditional Digital Signal Processor (DSP) and Clock Data Recovery (CDR) chips. Instead, LPO utilizes a direct-drive linear approach where the signal path is considered linear, relying on the capabilities of the Application Specific Integrated Circuit (ASIC) in the host system (like a switch or Network Interface Card) to perform signal conditioning and equalization.

MCM

: Multi chip module, a specialized electronic package where multiple integrated circuits (ICs), semiconductor dies or other discrete components are packaged onto a unifying substrate, facilitating their use as a single component (as though a larger IC).

Mid-board optics

: an optical transceiver that is mounted on a PCBA away from the PCBA edge, close to a switch ASIC to reduce the amount of PCBA trace loss between an ASIC and the optical transceiver. This is in contrast to the common practice today of locating optical transceivers at the PCBA edge.

Midplane

: Some backplanes are constructed with slots for connecting to devices on both sides and are referred to as midplanes.

MLSD

: Maximum likelihood sequence detection is a mathematical algorithm to extract useful data out of a noisy data stream.

MR

: Medium reach. CEI MR specifies chip-to-chip electrical interfaces.

NG

: Next generation.

NRZ (PAM2)

: Non return to zero, a binary code in which 1s are represented by one significant condition (usually a positive voltage) and 0s are represented by some other significant condition (usually a negative voltage), with no other neutral or rest condition.

NPC

: Near-package copper. NPC uses a copper cable to bring the front panel signal to a location close to the host silicon to minimize the host PCB losses. It reduces PCB losses by bringing the signals to a connector on the PCB close to the ASIC whereas CPC (Co-packaged copper) brings the signal to a connector on the ASIC package.

NPO

: Near-package optics. Similar to CPO (Co-packaged optics) and NPC (Near-package copper), NPO is an electrical to optical device intended to be mounted on the host PCB at a location adjacent to the host silicon to minimize host PCB traces to minimize electrical signaling requirements.

OE

: Optical engine.

O-to-E and E-to-O

: Optical to electrical interface and Electrical to optical interface, a component that converts an optical signal to an electrical signal or vice versa.

PAM

: Pulse amplitude modulation, a form of signal modulation where the message information is encoded in the amplitude of a series of signal pulses. For optical links it refers to intensity modulation.

PAM4

: Pulse amplitude modulation-4 is a two-bit modulation that takes two bits at a time and maps the signal amplitude to one of four possible levels.

PAM6

: A digital signal modulation scheme that encodes information by varying the amplitude of a pulse across six distinct voltage levels. Each of these six levels can represent approximately 2.5 bits of data.

PAM8

: A digital signal modulation scheme that encodes information by varying the amplitude of a pulse across eight distinct voltage levels. Each of these eight levels can represent 3 bits of data.

PCB/PCBA

: Printed circuit board (PCB) assembly, an assembly of electrical components built on a rigid glass-reinforced epoxy-based board.

Repeater

: A low-latency electronic device that receives a signal and retransmits it. Repeaters are used to extend transmissions so that the signal can cover a longer distance. Besides signal equalization, clock and data recovery (CDR) functions could be also added to remove jitter from received signals effectively.

RoCE

: RDMA over Converged Ethernet (CE) is a network protocol which allows remote direct memory access (RDMA) over an Ethernet network.

RS

: Reed Solomon FEC coding is a type of block code. Block codes work on fixed-size blocks (packets) of bits or symbols of predetermined size. It can detect and correct multiple random and burst errors.

RTLR

: (Retimed Transmit, Linear Receive) also generically referred to as Linear receive optic (LRO), is a type of optical transceiver technology used primarily in high-speed data center and networking applications, especially within AI clusters. The RTLR naming convention is within OIF. LRO is characterized by the presence of a Digital Signal Processor (DSP) solely on the transmit path, while the receive path operates with a linear, non-retimed architecture. This differs from fully retimed optical modules that utilize DSPs on both transmit and receive paths, and also from Linear Pluggable Optics (LPO) that eliminate DSPs entirely.

Scale out

: also known as horizontal scaling, refers to the process of increasing capacity and performance by adding more individual machines or nodes to a distributed system.

Scale up

: also known as vertical scaling, refers to the process of increasing the capacity or performance of a single server or system within an AI data center by adding more resources.

SDO

: standard development organizations.

SerDes

: A Serializer/Deserializer is a pair of functional blocks commonly used in high-speed communications to transfer data over a relatively low number of lanes.

SFP

: Small form-factor pluggable connector is a modular, hot-pluggable interface used in networking devices to connect to various types of fiber optic or copper cables. It uses a PCB card edge interface.

SI

: Signal integrity is a set of measures of the quality of an electrical signal.

SNDR

: Signal-to-noise-and-distortion ratio is a measurement of the purity of a signal.

SNR

: Signal-to-noise ratio.

TBD

: To be determined.

Tbps

: Terabits per second. The throughput or data rate of a port or piece of equipment. Tbps is $1\times10^{12}$ bits per second.

TCM

: Trellis coded modulation is a technique that combines convolutional coding and modulation to improve data transmission efficiency over bandwidth-limited channels, like telephone lines. It achieves this by intelligently integrating the encoding and modulation processes, increasing the distance between signal points in the constellation to enhance error correction without expanding bandwidth.

TME

: Test and measurement equipment.

Twinax copper cable

: A type of copper cable similar to coaxial cable, but with two inner conductors instead of one.

UCIe

: Universal chiplet interconnect express is an open industry standard that defines the interconnect between chiplets, or small component dies, within a single package.

VLC

: Vertical line card. A new line card design in which vertical I/O connectors and ASIC are mounted side by side, reducing the signal trace distance.

VSR

: Very short reach. CEI VSR specifies chip-to-module electrical interfaces.

XSR

: Extra short reach. CEI XSR specifies die-to-optical engine (D2OE) and die-to-die (D2D) electrical interfaces.

448G

: A generic name for an expected technology enabling data rates (including overhead) of approximately 448 Gbps per lane.

ALS

: Automatic laser shutdown. A safety mechanism that cuts laser output when fiber continuity is lost. Modern systems prefer APR with automatic restart over full shutdown.

APC

: Automatic power control. A feedback loop from a monitor photodiode that holds average optical output power constant against temperature drift and aging.

APD

: Avalanche photodiode. A photodiode with internal multiplication gain (5--9 dB sensitivity improvement over PIN) at the cost of excess noise factor and bias voltage.

APR

: Automatic power reduction. Holds laser output at or below Hazard Level 1M on fiber break and probes for re-mate with safe low-power pulses (ITU-T G.664).

ASE

: Amplified spontaneous emission. Broadband optical noise generated by optical amplifiers (SOA, EDFA); adds to the receiver noise floor.

AUI

: Attachment unit interface. The electrical serial lane set between a host ASIC and the module cage connector (e.g. 400GAUI-4).

BERT

: Bit-error-ratio tester. An instrument or ASIC function that generates PRBS patterns and counts bit errors for pre-FEC and post-FEC BER measurement.

BiCMOS

: A semiconductor process combining bipolar transistors (high $f_T$) with CMOS on one die; used for high-speed TIAs and modulator drivers.

BOM

: Bill of materials. The component and assembly cost of a module or system; DSP presence is a large BOM driver.

CMOS

: Complementary metal-oxide-semiconductor. The mainstream IC fabrication process; TIAs and SerDes are built at 16 nm to 3 nm nodes.

COBO

: Consortium for On-Board Optics. Standardized mid-board optical engine placement; largely leapfrogged by CPO in hyperscale deployments.

COD

: Catastrophic optical damage. A sudden, irreversible failure of a laser facet under thermal or optical overstress.

COM

: Channel operating margin. A statistical SNR metric for the fully equalized electrical link; CEI go/no-go is typically COM $\ge$ 3 dB.

COUPE

: Compact Universal Photonic Engine. TSMC's SoIC-X hybrid-bonded EIC-on-PIC packaging platform for co-packaged optics; mass production in 2026.

CW

: Continuous wave. Unmodulated laser output; external modulators (MZM, ring, EAM) encode data onto a CW source.

CW-WDM

: Continuous-wave wavelength division multiplexing. A multi-source agreement for multi-wavelength CW laser sources feeding WDM photonic engines.

CXL

: Compute Express Link. A coherent memory interconnect protocol built on the PCIe PHY (CXL 4.0 on PCIe 7.0); potential optical-reach application.

DCA

: Digital communication analyzer. A sampling oscilloscope used for PAM4 eye diagrams, TDECQ, OMA, and RLM measurements.

DBR

: Distributed Bragg reflector. A laser architecture where the grating sits outside the gain region, enabling tunable single-mode output.

DDM

: Digital diagnostic monitoring. Per-lane telemetry in CMIS: Tx/Rx optical power, laser bias, module temperature, LOS/LOL flags.

DFB

: Distributed feedback laser. A laser with a grating along the active region that selects one longitudinal mode; the workhorse CW or directly modulated source.

DML

: Directly modulated laser. Modulates bias current to encode data; simple and efficient but chirp-limited over dispersive fiber.

DR

: Datacenter reach. An IEEE 802.3 single-mode fiber class, typically 500 m at 1310 nm; the default for AI scale-out optics.

DWDM

: Dense wavelength division multiplexing. WDM with channel spacing $\le$`<!-- -->`{=html}100 GHz; used in metro/long-haul and dense CPO architectures.

EAM

: Electro-absorption modulator. A voltage-controlled absorption region on InP; low chirp compared with direct modulation; paired with a DFB in an EML.

EECQ

: Electrical eye closure quaternary. The electrical analog of TDECQ, quoted at host-referenced test points TP1a and TP4a.

ELS

: External laser source. A CW laser module feeding a co-packaged optical engine; superset of ELSFP and CW-WDM module forms.

ELSFP

: External Laser Small Form-Factor Pluggable. An OIF-defined faceplate-pluggable CW laser module for CPO with a 24-pin card edge, CMIS management, and blind-mate MT optics.

EML

: Externally modulated laser. A DFB laser integrated with an EAM on one InP chip; the dominant 100--200G/lane pluggable transmitter.

EO

: Electro-optic. Conversion from voltage to optical phase or intensity; EO bandwidth is the primary speed metric for a modulator.

ER

: Extinction ratio. $P_1/P_0$ in dB; higher ER widens OMA for a given average power and trades against chirp and driver swing.

FAU

: Fiber array unit. A precision V-groove assembly that mates multiple fibers to a PIC edge or grating coupler array.

FIT

: Failures in time. Failures per $10^9$ device-hours; fleet FIT times link count sets expected failures per day.

FR

: Far reach. An IEEE 802.3 single-mode fiber class, typically 2 km; tighter chirp and dispersion budget than DR.

FSR

: Free spectral range. The wavelength or frequency span between adjacent resonances of a ring resonator or etalon.

HBM

: High-bandwidth memory. Stacked DRAM on an interposer beside the accelerator die; memory bandwidth sets the decode roofline.

HCF

: Hollow-core fiber. Guides light primarily in air ($n\approx1$), giving roughly 33% lower latency than solid silica SMF.

HTOL

: High-temperature operating life. An accelerated reliability stress test (GR-468); Arrhenius modeling projects field wear-out from HTOL results.

IBTA

: InfiniBand Trade Association. Maintains the InfiniBand Architecture spec (NDR 400G, XDR 800G/port); reuses QSFP/OSFP optics with Ethernet.

IEEE

: Institute of Electrical and Electronics Engineers. IEEE 802.3 owns Ethernet PHY/MAC rates, KP4 FEC, and IM/DD optical PMD clauses.

IL

: Insertion loss. Optical power lost traversing a component (connector, fiber, MUX); quoted in dB.

InP

: Indium phosphide. A III-V semiconductor material for lasers, EAMs, SOAs, and high-speed photodiodes in the 1310/1550 nm bands.

LIV

: Light--current--voltage. The fundamental laser characterization curve: plots optical power and voltage versus bias current to read threshold, slope, kinks, and rollover.

LOL

: Loss of lock. A CDR or SerDes flag indicating the clock recovery circuit has lost symbol timing.

LOS

: Loss of signal. A receiver or host flag indicating optical input power has fallen below the detect threshold.

LRO

: Linear receive optic (also called RTLR). A module with a retimer/DSP only on the transmit path; the receive path is linear into the host SerDes.

MAC

: Media access control. The Ethernet data-link sublayer that builds frames, handles addressing and CRC. MAC rate is payload throughput.

MACsec

: IEEE 802.1AE media access control security. Provides line-rate encryption, frame integrity, and data origin authentication at Layer 2; transparent to the optical PMD.

MDI

: Medium dependent interface. The optical connector where a module meets the fiber; test points TP2 (Tx launch) and TP3 (Rx input) sit at the MDI.

MEMS

: Micro-electro-mechanical systems. Tilting mirror arrays used in optical circuit switches; millisecond switching at $\sim$`<!-- -->`{=html}2 dB loss.

MLC

: Multi-level coding. Coded modulation paired with PAM6/PAM8; OIF 448G workshop models often add a strong outer RS code at $\sim$`<!-- -->`{=html}12% overhead.

MMF

: Multimode fiber. Fiber supporting many spatial modes (50/125 $\mu$m); used with VCSELs at 850--940 nm for SR links (OM3/OM4/OM5 grades).

MoE

: Mixture of experts. A transformer architecture that routes tokens to specialist sub-networks; drives all-to-all collective traffic on the fabric.

MPO

: Multi-fiber push-on. A standard multi-fiber connector for parallel optics (8, 12, 16, 24, or 32 fibers per ferrule).

MRM

: Microring modulator. A resonant silicon modulator; compact and WDM-native but requires wavelength lock. The CPO workhorse at 200G/channel.

MSA

: Multi-source agreement. An industry specification for interoperable products (e.g. LPO MSA, CW-WDM MSA, 100G Lambda MSA).

MZM

: Mach--Zehnder modulator. A push-pull interferometer; broadband, low chirp. Built in silicon, TFLN, or III-V platforms.

NFF

: No fault found. An RMA unit that passes all tests on return; high NFF rate points at triage or intermittent connector faults.

NIC

: Network interface card. A host adapter connecting an accelerator or CPU to the scale-out fabric (Ethernet or InfiniBand).

OBO

: On-board optics. Optical engines mounted mid-board on the host PCB (COBO standard); mostly bypassed for CPO in hyperscale.

OCS

: Optical circuit switch. A Layer-1 switch that steers light from input to output fiber with no O-E-O conversion; transparent to rate, format, and wavelength.

OMA

: Optical modulation amplitude. The outer PAM4 signal swing ($P_1-P_0$); the primary power metric for IM/DD transmitters.

ORL

: Optical return loss. The ratio of reflected to incident power at a fiber interface; low ORL raises laser RIN and can cause burst errors.

OSA

: Optical spectrum analyzer. An instrument that measures wavelength, SMSR, side-mode structure, and spectral width of a laser source.

OSFP

: Octal Small Form-factor Pluggable. A high-power faceplate module cage for 800G/1.6T/3.2T; larger thermal envelope than QSFP-DD.

PCS

: Physical coding sublayer. The IEEE 802.3 sublayer that performs 64B/66B line coding, 256B/257B transcoding, scrambling, and RS-FEC encoding.

PD

: Photodiode. A semiconductor device that converts photons to photocurrent (PIN, APD, or UTC variants).

PHY

: Physical layer. The combined PCS, PMA, and PMD that maps MAC frames to signals on the wire or fiber.

PIC

: Photonic integrated circuit. A chip integrating waveguides, modulators, detectors, and couplers (typically on SOI at 220 nm silicon).

PIN

: A p-intrinsic-n photodiode with no internal gain and the lowest excess noise; Ge-on-Si waveguide PIN is the mainstream short-reach detector.

PMA

: Physical medium attachment. The IEEE 802.3 sublayer that serializes, lane-multiplexes, and recovers clock. The SerDes lives here.

PMD

: Physical medium dependent. The IEEE 802.3 sublayer that modulates and detects light: the optical transceiver (laser, driver, PD, TIA).

PRBS

: Pseudo-random binary sequence. A deterministic test pattern that exercises all bit transitions; used for BER and eye measurements.

PSRR

: Power supply rejection ratio. A circuit's ability to suppress supply-rail noise; critical for laser bias drivers to avoid injecting RIN.

PUE

: Power usage effectiveness. Total facility power divided by IT equipment power; typical hyperscale values 1.1--1.3.

QSFP-DD

: Quad Small Form-factor Pluggable Double Density. A faceplate module cage carrying eight electrical lanes for 400G/800G/1.6T.

RDMA

: Remote direct memory access. Zero-copy network transfer between accelerator memories; carried over RoCE (Ethernet) or native InfiniBand.

RIN

: Relative intensity noise. The laser's own amplitude-noise spectral density (dB/Hz); sets a BER floor that power cannot overcome.

RLM

: Relative level mismatch. A measure of PAM4 level spacing uniformity (1.0 = perfectly even); CEI typically requires $\ge$`<!-- -->`{=html}0.95.

RMA

: Return merchandise authorization. A field-failed unit returned to the supplier for failure analysis. Distinct RMA codes keep FIT accounting honest.

SECQ

: Stressed eye closure quaternary. A receiver-side metric that applies calibrated optical stress and reports remaining margin before BER threshold.

SiGe

: Silicon-germanium BiCMOS. A high-$f_T$ semiconductor process for TIAs and modulator drivers operating at 100--200+ GHz bandwidth.

SiPh

: Silicon photonics. Waveguides and modulators on silicon-on-insulator; CMOS fab-compatible and the mainstream for DR/FR and CPO.

SMF

: Single-mode fiber. Fiber with a $\sim$`<!-- -->`{=html}9 $\mu$m core carrying one spatial mode; G.652.D (standard) and G.657 (bend-insensitive) for datacenter plant.

SMSR

: Side-mode suppression ratio. The power difference (dB) between the dominant lasing mode and the strongest side mode on an OSA.

SOA

: Semiconductor optical amplifier. A III-V inline optical gain block; adds ASE noise. Used as a receiver preamplifier for sensitivity.

SOI

: Silicon on insulator. A wafer substrate for silicon photonics: a thin ($\sim$`<!-- -->`{=html}220 nm) silicon layer on buried oxide confines the optical mode.

SR

: Short reach. An IEEE 802.3 multimode fiber class, typically $\le$`<!-- -->`{=html}100 m over OM4; VCSEL at 850 nm.

TCO

: Total cost of ownership. Acquisition (BOM, yield) plus lifetime energy plus service cost (FIT $\times$ replacement + labor).

TDECQ

: Transmitter and dispersion eye closure quaternary. The headline PAM4 transmitter-quality metric; measured after a reference receiver and bounded FFE, including a test fiber.

TEC

: Thermoelectric cooler. A Peltier device that holds a laser junction or ring at a controlled temperature against case thermal variations.

TECQ

: Transmitter eye closure quaternary. Same measurement as TDECQ without the test fiber; used alongside TDECQ in LPO MSA OMA tables.

TFLN

: Thin-film lithium niobate. A sub-micrometer LN layer on a silicon or silica handle; $>$`<!-- -->`{=html}110 GHz EO BW and the leading path to native 224 GBd PAM4.

TIA

: Transimpedance amplifier. Converts photodiode current to voltage with low input-referred noise; co-packaging with the PD minimizes capacitance and noise.

TP

: Test point. A defined reference plane where a link measurement is taken (TP0 through TP5, plus TP1a/TP4a).

TRO

: Transmit retimed optic. A module with DSP only on the transmit (electrical-to-optical) path; the receive path is linear.

TWE

: Traveling-wave electrode. An RF transmission line on a modulator that velocity-matches the electrical and optical group indices for high EO bandwidth.

TWI

: Two-wire interface. An I2C-like serial bus (SCL + SDA) used for CMIS module management communication.

UALink

: Ultra Accelerator Link. An open scale-up fabric specification for direct accelerator memory access (200G/lane class; $\sim$`<!-- -->`{=html}400G/lane next).

UEC

: Ultra Ethernet Consortium. Builds an open Ethernet-based stack (UET transport, PHY) optimized for AI/HPC scale-out with cluster-scale congestion control.

UI

: Unit interval. One symbol period ($=1/R_\mathrm{sym}$); jitter budgets and eye diagrams are referenced in UI.

UTC / MUTC

: Uni-traveling-carrier (modified UTC) photodiode. Uses electron-only transport for $>$`<!-- -->`{=html}200 GHz bandwidth and high saturation current; linear/LPO niche.

VOA

: Variable optical attenuator. A calibrated loss element used for sensitivity sweeps and stressed-receiver testing.

WDM

: Wavelength division multiplexing. Sending multiple wavelengths on one fiber; CWDM (20 nm spacing) or DWDM ($\le$`<!-- -->`{=html}100 GHz spacing).

XPO

: eXtra-dense Pluggable Optics. A liquid-cooled, 12.8 Tb/s faceplate pluggable module (Arista MSA, OFC 2026); front-panel serviceable at CPO-class density.


<div class="nav-links">
  <a href="ch9-ai-datacenter-networking">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-references">Next &rarr;</a>
</div>
