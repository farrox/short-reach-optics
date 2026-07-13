# Content gaps and coverage backlog

A working list of topics that are missing or thin relative to the book's stated
scope: short-reach optical interconnects for AI compute, from in-package optical
I/O out to a few hundred meters, IM/DD not coherent (see the preface and
`sec:reach`). Coherent, campus, and DCI links stay out of scope on purpose.

We work these one at a time. Each entry says what is missing, why it fits the
scope, where it would live, a suggested treatment, and what to verify before it
enters the book. Priority is a judgment call on reader value, not difficulty.

Facts in the "verify" notes move fast (vendor programs, fiber loss records, comb
products). Confirm against primary sources before writing, and mark anything from
a preprint or vendor announcement as provisional, per the book-authoring rules.

## Priority backlog

| # | Gap | Chapter home | Priority | Status |
|---|-----|--------------|----------|--------|
| 1 | Optical circuit switching (OCS) | ch07 networking | High | done |
| 2 | Fabric-level reliability, redundancy, and availability | ch06 -> ch07 bridge | High | done |
| 3 | Consolidated latency budget | ch07 (or ch02) | High | done |
| 4 | Hollow-core fiber for intra-datacenter latency | ch02 channel / ch07 | Medium | done |
| 5 | Integrated comb and multi-wavelength source alternatives | ch03 lasers / ch04 WDM | Medium | done |
| 6 | Co-packaged / near-package copper (CPC/NPC) as the copper counter-move | ch07 electrical link | Medium | done |
| 7 | Polarization management (PM fiber, PDL, grating-coupler sensitivity) | ch02 channel / ch03 | Medium | done |
| 8 | SOA gain and WDM power distribution/equalization | ch03 / ch04 | Low-Med | done |
| 9 | Cost and TCO model across module styles | ch07 power (adjacent) | Low-Med | done |
| 10 | Line-rate security (MACsec) and fleet observability | ch05 or ch07 | Low | done |
| 11 | Thermal envelope and cooling (the physical flip side of the power wall) | ch07 power (adjacent) | Medium | done |

## Gap detail

### 1. Optical circuit switching (OCS) [DONE]
- **Resolved:** added `\section{Optical circuit switching}` (`sec:ocs`) in ch07,
  after fabric options and before the CPO status section. Covers Layer-1
  transparency, the device/parameter set, a `table*` comparing switch
  technologies (MEMS/piezo/LCoS/robotic/silicon-photonic), fleet-scale benefits,
  transceiver implications, CPO comparison, and a closing `\keyidea`.
- **Sources wired up:** Google Jupiter (Palomar 136x136 MEMS OCS, ~2 dB insertion
  loss, ms switching, circulators double radix, ~30% capex / ~41% power / 3x
  reconfiguration gains), TPU v4 (4096 accelerators through 48 OCS, reconfigurable
  3D torus, route-around-failure), and a 2025 market survey (FR-over-DR,
  circulators, higher-power optics). New bibitems `jupiterocs`, `tpuv4ocs`,
  `ocsmarket` with matching citeurls and citesnips; new `OCS` termsnip.
- **Verified:** compiles clean, no undefined refs, all three bibkeys resolve in
  `main.aux`; section is 9.9 on p.121, table on p.122, no new overfull hboxes.
  Pages 121-123 rendered and visually checked, wide table sits within the margins.

### 2. Fabric-level reliability, redundancy, and availability [DONE]
- **Resolved:** ch06 has `\section{From component FIT to fabric availability}`
  (`sec:fabric-availability`) bridging component FIT to fabric uptime: redundant
  rails, sparing, link-flap detection and adaptive reroute, OCS reconfiguration
  around dead links (`\Cref{sec:ocs}`), and the cost of a failure to a collective
  (checkpoint/restart). Uses the Meta Llama 3 fleet numbers (`metallama3`: failure
  ~every 3 h, network faults 8.4\%, ~90\% uptime) and closes with a keyidea.
- **Now (historical):** ch06 covers component FIT, DPPM, wear-out, and connects FIT to
  "laser failures per day" (`sec:fit-example`). The step from component FIT to
  fabric uptime is missing.
- **Why in scope:** the book's thesis is that link reliability sets how large a
  dependable fabric can grow. Component FIT alone does not answer that. A
  0.6-failures/day fleet needs a story for how the fabric survives each one.
- **Treatment:** a bridge section (end of ch06 or start of ch07) on redundant
  rails, sparing strategy, link-flap detection and reroute, OCS reconfiguration
  around a dead link (ties to #1), and the cost of a failure to a collective
  (tail latency, all-reduce stalls, checkpoint/restart). Keep it quantitative:
  connect FIT to expected concurrent failures and to mean time between fabric
  events.
- **Verify:** any public availability targets or reroute-time figures; keep
  vendor resiliency claims (NVIDIA, Broadcom) marked as vendor orientation.

### 3. Consolidated latency budget [DONE]
- **Resolved:** added `\section{The latency budget}` (`sec:latency-budget`) in
  ch07 before `sec:power`, mirroring the dB link budget and the pJ/bit energy
  budget. Sums serialization, FEC encode/decode (KP4 RS(544,514) ~20--100~ns,
  `feclatency`), per-hop DSP (~8--10~ns retimed), sub-ns analog group delay, fiber
  propagation, and switch-hop latency (~560~ns 800GbE vs sub-100~ns InfiniBand,
  `switchlat`). Contrasts retimed/LRO/LPO/CPO. Includes `tab:latency`.
- **Now (historical):** latency appears in pieces: inference critical path (ch01, ch07),
  retimer/DSP nanoseconds per hop, LPO under 3 ns, HCF propagation. There is no
  single latency ledger the way there is a link budget (`sec:link-budget`) and an
  energy budget (`sec:power`).
- **Why in scope:** the book puts optics on the latency critical path. A reader
  should be able to add up a link's latency the way they add up its dB and its
  pJ/bit.
- **Treatment:** a short section that sums the contributors: serialization,
  FEC encode/decode, DSP or retimer hops, modulator/driver and PD/TIA group delay,
  fiber propagation (and the HCF delta, ties to #4), and switch-hop latency across
  a topology. Contrast retimed vs LRO vs LPO vs CPO on latency, mirroring the
  existing power contrast.
- **Verify:** typical FEC decode latency for KP4; per-hop DSP latency numbers
  already cited in ch07 (reuse, do not restate differently).

### 4. Hollow-core fiber for intra-datacenter latency [DONE]
- **Resolved:** added `\subsection{Hollow-core fiber}` (`sec:hcf`) in ch07 under
  the latency budget. Covers the group-index attack on propagation delay
  (~4.9 -> ~3.3~ns/m, ~45% faster), the loss trajectory (DNANF record 0.091~dB/km
  at 1550~nm, ~0.2~dB/km over 66~THz, `hcf2025`, marked record/provisional), low
  nonlinearity relevance, and the open problems (splicing, connectorization, cost).
  Also fixed the stale ~0.04~dB/km figure in the OFC-picture paragraph.
- **Now (historical):** one sentence at the end of ch07 (loss near 0.04 dB/km,
  low-latency intra-datacenter use).
- **Why in scope:** HCF's roughly 1.5x lower propagation delay than solid glass is
  a short-reach, latency-driven story, and loss and manufacturing maturity have
  moved fast. It reinforces the latency-budget work in #3.
- **Treatment:** a short subsection in `sec:optical-channel` (ch02) or ch07.
  Cover the latency advantage (near vacuum speed of light), the loss trajectory,
  low nonlinearity and its relevance (or not) to IM/DD short reach, and the open
  problems (splicing, connectorization, cost, availability).
- **Verify:** latest published HCF loss and any intra-datacenter deployment.
  Treat records as provisional; cite primary sources (vendor/standards/papers).

### 5. Integrated comb and multi-wavelength source alternatives [DONE]
- **Resolved:** added `\subsection{Comb sources: one device, many lines}`
  (`sec:comb-sources`) in ch04 `sec:cwwdm`, after the source-requirements
  paragraph. Compares DFB arrays (baseline), QD-MLLs (front-runner: 14x100G PAM4
  over 10 km at ~284 fJ/bit, isolator-free >3.2 Tb/s, `qdcomb`/`qdrin`, marked
  provisional), Kerr microcombs (low per-line power motivates SOAs, cross-refs
  `sec:soa-distribution`, `microcomb`, provisional), and gain-switched/quantum-dash
  combs. Closes back to the MSA contract (`\Cref{sec:cwwdm-laser}`).
- **Sources wired up:** `qdcomb`, `microcomb` bibitems with matching citeurls and
  citesnips; QD-MLL term. Compiles clean, bibkeys resolve, page 81 visually checked.

### 6. Co-packaged / near-package copper (CPC/NPC) as the copper counter-move [DONE]
- **Resolved:** added `\paragraph{Co-packaged and near-package copper: copper moves
  inward too.}` (`sec:cpc-npc`) in ch07 `sec:trace-loss`, after the active-copper
  (ACC/AEC/DAC) paragraph and before "the optics march inward". Defines CPC
  (connector onto the ASIC substrate) and NPC (connector on the socket just outside
  the package), frames both as copper's answer to the same reach wall that drives
  CPO, and marks the crossover: within ~1 m at 448G-PAM4 (`\Cref{sec:448g}`) copper
  keeps the SerDes-only energy (~4 pJ/bit), lower latency, and lower cost; past that
  wall optics wins (`\Cref{tab:oif-scale}`). Cross-refs the placement ladder
  (`\Cref{tab:placement}`) and trace-loss figure (`\Cref{fig:traceloss}`).
- **Sources wired up:** new bibitem `cpc` (Molex on-substrate CPC validated at
  224G-PAM4, roadmap to 448G, Impress compression connector; Marvell 224G LR SerDes
  ~4 pJ/bit; Lintes shared NPC/NPO socket), marked vendor/provisional, with citeurl
  and citesnip. Compiles clean (152 pp), bibkey resolves, page 121 visually checked.

### 7. Polarization management [DONE]
- **Resolved:** added `\subsection{Polarization on the CW distribution path}`
  (`sec:polarization`) in ch04 `sec:cwwdm`, after the SOA subsection and before the
  lock-validation playbook. States where polarization matters, source-to-modulator
  through TFLN (`\Cref{sec:tfln-mzm}`), grating-coupler PDL, and SOA PDG
  (`\Cref{sec:soa-distribution}`), and where it does not, post-PD in IM/DD
  (`\Cref{sec:coherent-boundary}`). Covers how it is held: PM fiber and PM
  connectors from the external laser (`\Cref{ch:lasers}`), with co-packaging
  shortening the run. Uses `\term{}` for TFLN, PDL, and PM; no new citations needed.
- **Verified:** compiles clean, no undefined refs; subsection 6.6.3 on p.82,
  rendered and visually checked (within margins).

### 8. SOA gain and WDM power distribution/equalization [DONE]
- **Resolved:** added `\subsection{Gain and power distribution across the bank}`
  (`sec:soa-distribution`) in ch04 `sec:cwwdm`, right after the comb subsection
  (comb low per-line power motivates the SOA discussion). Covers booster vs
  per-line SOA placement, the receiver-side preamp cross-ref (`\Cref{tab:rxtech}`),
  the ASE noise-figure cost (quantum floor 3 dB; commercial O-band ~6--7 dB NF,
  ~15 dB gain, ~1.5 dB PDG, `soa`), QD-SOA on Si, and holding per-line flatness.
- **Sources wired up:** `soa` bibitem (Anritsu datasheet + ACS Photonics 2019
  QD-SOA on Si) with citeurl and citesnip; ASE term. Compiles clean, bibkey
  resolves, page 82 visually checked.

### 9. Cost and TCO model across module styles [DONE]
- **Resolved:** added `\section{A first-order cost model}` (`sec:cost-model`) in
  ch07 after `sec:power` (the energy budget), before the chapter-closing keyidea.
  Kept explicitly order-of-magnitude and illustrative, not a price sheet. Splits TCO
  into acquisition (BOM/yield), lifetime energy, and service (from FIT,
  `\Cref{sec:fit-example}`). Works a labeled illustrative opex example (retimed
  $\sim$15~W vs LPO $\sim$8~W over five years at \$0.10/kWh, PUE $\sim$1.3, giving a
  $\sim$\$40/module gap), then scales it. Contrasts retimed/LPO/LRO/CPO/XPO/CPC
  per delivered Gb/s and closes with a keyidea tying cost to the energy budget.
- **Sources wired up:** reused `lpo`, `jupiterocs` (OCS $\sim$30\% capex,
  `\Cref{sec:ocs}`), and `tab:pjbit`. Added two bibitems, `lpocost` (Semtech: LPO
  $\sim$50--60\% power saving, $\sim$100~MW / $\sim$\$100M/year at 500k GPUs) and
  `dctco` (Epoch AI: 1~GW site $\sim$\$38B capex, $\sim$\$0.9B/year opex), both
  marked vendor/analyst provisional, with matching citeurls and citesnips.
- **Verified:** compiles clean (152 pp), no undefined refs, both bibkeys resolve in
  `main.aux`; section 9.14 on p.135, rendered and visually checked (within margins).

### 10. Line-rate security and fleet observability [DONE]
- **Resolved:** ch07 now covers IEEE 802.1AE MACsec (line-rate L2 encryption, its
  PHY latency/power cost, placement relative to the PMD) and the fleet
  observability stack above CMIS (DMTF Redfish, OpenConfig/gNMI, SONiC). Bibkeys
  `ieee8021ae` and `netmgmt` wired up with citeurls and citesnips.
- **Now (historical):** CMIS DDM telemetry is covered for triage. Link-layer
  encryption and broader observability are not.
- **Why in scope:** MACsec at 800G/1.6T has real PHY latency and power
  implications; fleet observability beyond DDM affects triage at scale. May be
  judged out of scope; flag the decision rather than assume.
- **Treatment:** if kept, a short note in ch05 or ch07 on where encryption sits
  relative to the PMD and its power/latency cost. Otherwise, an explicit
  scope-exclusion line.
- **Verify:** MACsec overhead and placement at these rates.

### 11. Thermal envelope and cooling [DONE]
- **Resolved:** added `\subsection{The thermal envelope}` (`sec:thermal-envelope`)
  in ch07 within the power section, framing cooling as the second ceiling beside
  the power wall. Covers faceplate-switch heat load (32-port 800G switch $>$1~kW,
  optics $\sim$half, `switchthermal`), the air-cooling headroom limit past the
  mid-teens of watts and the move to liquid/immersion, LPO's power cut read as a
  thermal cut (`\Cref{sec:power}`, `lpo`), co-packaging turning the on-package
  gradient into the limiting term (rings/lock loops `\Cref{sec:thermal-xtalk}`,
  laser least tolerant, `cpocooling`), the thermal case for external lasers
  (`\Cref{sec:elsfp}`), and cooling as an Arrhenius reliability lever
  (`\Cref{sec:laser-aging}`, `\Cref{sec:fit-example}`).
- **Sources wired up:** `switchthermal` (FiberMall, vendor/provisional) and
  `cpocooling` (Cao et al., Front. Optoelectron. 2025) bibitems with matching
  citeurls and citesnips.
- **Verified:** compiles clean (154 pp), no undefined refs/citations, both bibkeys
  resolve; no large overfull hboxes on the affected pages (134--135).

## Considered and already well covered (not gaps)

Listed so we do not re-raise them:

- Energy per bit and the Miller framework (ch_firstprinciples), including recent
  hardware confirmation.
- Modulators: silicon microring, silicon MZM, TFLN MZM, EML/EAM, plus drivers and
  gearbox (all in ch02: `sec:siring`, `sec:simzm`, `sec:tfln-mzm`, `sec:eml-eam`,
  `sec:drivers`, `sec:gearbox`).
- Noise, RIN, BER, sensitivity, PD/TIA and detector menu (ch_models).
- Lasers, bias-driver RIN budget, aging/derating/FIT, ELSFP pinout and qual,
  optical safety with APR/ALS, CW-WDM source validation, supplier landscape (ch03).
- WDM grids (incl. ITU-T G.694), lock-loop mechanics, thermal crosstalk, MUX
  budget, CW-WDM architecture (ch04).
- Validation ladder, TDECQ/TECQ, SECQ, instruments, link budget, CMIS, bring-up,
  production corners, debug, fleet triage (ch05).
- Reliability: FIT/DPPM, GR-468 qual, IC reliability (JEDEC/AEC-Q100), connector
  reliability (IEC 61754-7/61300), wear-out map, packaging, HVM test, supplier
  execution (ch06).
- Networking: scale-up vs scale-out, three-network model, SDO map, topologies,
  pluggable form factors, LPO MSA, CEI reach classes, conditioning, electrical eye
  and COM, CPO programs (Broadcom/NVIDIA/TSMC COUPE), XPO, power wall, inference
  collectives, fabric options (ch07).
- Standards coverage is tracked separately in the README non-OIF section. As of
  the latest pass there are no open non-OIF standards gaps: IBTA/InfiniBand,
  IEEE 802.1AE MACsec, PCI-SIG/CXL, Telcordia GR-1221, and the
  DMTF/OpenConfig/SONiC management stack are all now covered in the book.
