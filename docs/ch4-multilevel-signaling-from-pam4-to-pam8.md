---
layout: default
title: "Ch 4: Multilevel Signaling: From PAM4 to PAM8"
---

# 4 Multilevel Signaling: From PAM4 to PAM8

This chapter is the design judgment home for multilevel intensity modulation: why more levels exist, what you pay in SNR and linearity, how Gray coding changes the bit-error story, and when PAM8 is or is not worth it. Roadmaps and per-lane rates live in Chapter 3. Noise and BER math live in Chapter 5. Equalizer classes live in §3.6.

*Read first:* baud versus bit rate, level spacing, Gray coding, and the PAM8 pressure list.

*Deep dive:* 448G alphabet options in §3.14.3, §3.9; NRZ/PAM4 quantitative comparison in §5.6.

**Key idea.** PAM8 lowers the baud rate for a given bit rate, but the level spacing becomes much tighter, so you pay more in SNR, linearity, calibration, and DSP. Lower baud is purchased with smaller vertical eyes and harder detection.

## Why multilevel signaling exists

A symbol carries information by choosing one of $M$ amplitudes. The number of bits per symbol is $\log_2 M$:

<table class="book-table"><tr><th>Format</th><th>Levels \(M\)</th><th>Bits per symbol</th></tr><tr><td>NRZ (PAM2)</td><td>2</td><td>1</td></tr><tr><td>PAM4</td><td>4</td><td>2</td></tr><tr><td>PAM8</td><td>8</td><td>3</td></tr></table>
At a fixed bit rate $R_b$, the symbol rate (baud) is $$\begin{equation}
R_s = \frac{R_b}{\log_2 M}.
\label{eq:baud-vs-bitrate}
\end{equation}$$

Higher $M$ lowers the baud for the same throughput. That relaxes the electrical and optical bandwidth the channel, connectors, driver, modulator, and receiver must support. The cost is smaller vertical openings between adjacent levels and stronger sensitivity to noise, distortion, and nonlinearity.

##### Worked example at 200 Gb/s.

Using Eq. 4.1 at $R_b=200$ Gb/s (ideal, before FEC overhead):

<table class="book-table"><tr><th>Format</th><th>Ideal symbol rate</th></tr><tr><td>NRZ</td><td>200 GBd</td></tr><tr><td>PAM4</td><td>100 GBd</td></tr><tr><td>PAM8</td><td>\(\)66.7 GBd</td></tr></table>
Real Ethernet and CEI lanes include FEC and coding overhead, so published baud numbers differ slightly from this ideal (§3.2, §3.14). The design point is unchanged: multilevel buys baud relief and spends vertical margin.

##### What baud relief buys.

Lower symbol rate moves the Nyquist frequency down. That can mean less channel loss at the frequency that matters, less connector bandwidth demand, and more headroom in the driver and modulator electro-optic response. It can also ease ADC sampling rate when the alphabet is recovered in DSP. None of those gains is automatic: if the optical path is linearity-limited rather than bandwidth-limited, denser PAM spends margin without unlocking the link.

## Level spacing and noise penalty

For equally spaced levels over the same total swing $A_{\mathrm{total}}$, the adjacent-level spacing is $$\begin{equation}
\Delta = \frac{A_{\mathrm{total}}}{M-1}.
\label{eq:level-spacing}
\end{equation}$$

NRZ has one eye. PAM4 has three eyes. PAM8 has seven eyes. With the same full-scale swing:

- PAM4 adjacent spacing is one-third of the total swing;

- PAM8 adjacent spacing is one-seventh of the total swing.

Relative to NRZ's full swing as one step, the ideal amplitude-separation comparisons are about $20\log_{10}3\approx9.5$ dB for PAM4 and $20\log_{10}7\approx16.9$ dB for PAM8 before bandwidth, coding, and implementation effects. Those are spacing comparisons, not automatic sensitivity penalties on a finished link (§5.6).

Tighter spacing raises the SNR needed to keep the same symbol-error rate. It also tightens linearity: compression that was tolerable on a two-level eye can crush the inner PAM8 eyes. Noise that was acceptable for NRZ can dominate the smallest PAM8 openings.

<table class="book-table"><tr><th>Format</th><th>Eyes</th><th>Adjacent spacing vs outer swing</th><th>Ideal vs NRZ step</th></tr><tr><td>NRZ</td><td>1</td><td>1</td><td>0 dB</td></tr><tr><td>PAM4</td><td>3</td><td>1/3</td><td>9.5 dB</td></tr><tr><td>PAM8</td><td>7</td><td>1/7</td><td>16.9 dB</td></tr></table>
Ideal amplitude-separation comparison for equal spacing and equal outer swing, before bandwidth, EQ, coding, and transmitter quality.

##### Noise is not the only enemy.

Additive noise sets one floor. Pattern-dependent ISI, reflections, and level-dependent noise set others. A format with seven eyes has seven places for those impairments to land. When you debug a multilevel failure, ask which eye closed first.

## Gray coding

Adjacent levels are normally Gray coded so that a nearest-level mistake flips one bit rather than several. That matters because detectors usually err to a neighbor, not to a random distant level.

Two consequences:

- Symbol error rate (SER) and bit error rate (BER) are not identical. With Gray coding, BER is often near $\mathrm{SER}/\log_2 M$ when most errors are adjacent-level mistakes.

- Without Gray coding, one symbol error can create multiple bit errors and waste FEC budget.

When you quote a pre-FEC BER target for PAM4 or PAM8, state whether the model assumes Gray mapping and adjacent-error dominance.

## PAM8 design pressure

Moving from PAM4 to PAM8 is not "one more bit for free." Design pressure stacks:

Decision thresholds

: Seven thresholds instead of three. Placement error and threshold drift hit more eyes.

Linearity

: DAC, driver, and modulator compression must stay small across the full swing. Inner eyes die first.

Level placement

: Absolute and relative level accuracy matter more. RLM thinking for PAM4 becomes an eight-level calibration problem.

ADC and DSP

: Higher resolution and more precise equalization; more power and latency if the alphabet lives in DSP.

Clock recovery

: Lower baud helps bandwidth, but multilevel edges and denser eyes make timing recovery less forgiving.

FEC dependence

: Stronger coding or higher overhead may be needed to buy back the SNR spent on spacing (§3.9).

Production calibration

: Thresholds, levels, and temperature corners need factory and field procedures that PAM4 already strains.

The interview sentence is simple: PAM8 lowers baud, but you pay in SNR, linearity, calibration, and DSP.

## Optical implementation

Multilevel light can be generated several ways. The architecture choice sets linearity, extinction, chirp, and calibration.

Directly modulated laser (DML)

: Simple, but chirp and nonlinear $L$--$I$ behavior fight dense eyes. Harder as $M$ grows (Chapter 6).

EML

: Better spectral control than a DML for many short-reach lanes; still needs linear drive for PAM8.

MZM

: Often the linearity workhorse when a CW laser feeds a Mach--Zehnder modulator. Bias and swing must stay in a linear region of the transfer curve.

Ring modulator

: Compact and WDM-friendly; resonance and thermal control complicate multilevel calibration.

Segmented or cascaded binary modulators

: Binary-weighted optical paths can synthesize multilevel amplitude by optical addition rather than one highly linear analog swing.

DAC-driven linear modulation

: Generate PAM8 electrically, then demand a linear optical transfer function from driver through modulator.

Ask where the multilevel alphabet is created:

1.  Electrically, before one modulator (DAC + linear optic);

2.  With segmented optical modulation;

3.  Through optical addition of binary-weighted paths;

4.  Or with DSP/DAC plus a carefully linearized optical response.

Each path moves the hard problem: DAC resolution, optical linearity, path matching, or thermal control. There is no free PAM8 modulator.

##### Short-reach shortlist.

For many DR/FR-class modules the credible PAM8 paths are a linear MZM or EML with a clean DAC/driver chain, or a segmented optical approach if the product team can match path delays and weights. Rings remain attractive for WDM density but need an explicit thermal and resonance-control story before they are a PAM8 default. DMLs are usually the last choice for eight-level eyes unless the reach and rate are modest.

## Metrics interviewers expect

##### Outer OMA.

For PAM4, outer OMA is $P_3-P_0$, not an inner-eye span. For PAM8, the outer span is $P_7-P_0$. Quoting "OMA" without saying outer versus per-eye invites a wrong budget (Chapter 5, Appendix E).

##### Per-eye thinking.

A passing outer eye does not prove the inner eyes are open. Level mismatch, compression, and ISI hit inner eyes first.

##### Extinction ratio.

ER compares high and low optical levels. It is necessary context, not a substitute for multilevel eye quality.

##### RLM and level mismatch.

Relative level mismatch (RLM) for PAM4 asks whether the three eyes are evenly spaced. PAM8 needs the same idea with more levels: unequal spacing burns SNR even when outer OMA looks fine.

##### TDECQ and stressed metrics.

Transmitter quality metrics after a reference equalizer belong in the measurement appendix (Appendix E.3). Use them to close a claim; do not treat a single composite number as a confirmed mechanism.

## When PAM8 is not worth it

Choose PAM8 only when the baud relief is worth the vertical and linearity cost.

Stay on PAM4 when:

- the electrical channel already closes at the PAM4 baud with acceptable power;

- the optical path cannot deliver the linearity PAM8 needs;

- FEC, DSP, or calibration power erases the system gain;

- production cannot place and hold eight levels across temperature and aging.

The 448G debate is exactly this trade: fix the channel for higher-baud PAM4, or accept denser alphabets and stronger coding (§3.14.3, §3.9). Do not treat PAM8 as the default upgrade path.

## Interview takeaway

**Key idea.** I explain multilevel formats as a baud-versus-vertical-margin trade. I name bits per symbol, level spacing, Gray coding, and where the alphabet is generated. I do not claim PAM8 is "more efficient" without stating the SNR, linearity, FEC, and calibration bill.

## Interview Q&A

Practice aloud. Prefer first-person reasoning. Score with Appendix A.12.1.

##### Question 1. Why use PAM8 instead of staying on PAM4?

*Tests:* baud relief versus vertical and linearity cost.

*Spoken answer.* "I use PAM8 when the bit rate forces a PAM4 baud that the channel, connector, or optics cannot support cleanly. Eight levels cut the ideal symbol rate to one-third of the bit rate, so Nyquist drops. I only take that deal if the SNR, linearity, FEC, and calibration budget still close."

*Pressure follow-up.* "Is PAM8 always the next step after PAM4?"\
*Answer pivot.* "No. If PAM4 already closes, PAM8 mostly buys complexity."

*Trap:* "PAM8 is better because it is higher order modulation."

##### Question 2. At the same bit rate, how do NRZ, PAM4, and PAM8 baud rates compare?

*Tests:* $R_s=R_b/\log_2 M$.

*Spoken answer.* "NRZ uses one bit per symbol, PAM4 two, PAM8 three. At 200 Gb/s ideal, that is 200 GBd, 100 GBd, and about 66.7 GBd. Real lanes add FEC overhead, but the ratio is the design point."

*Pressure follow-up.* "Why do datasheets show different baud numbers?"\
*Answer pivot.* "Coding and FEC overhead change the line rate. I still start from bits per symbol, then apply the standard's overhead."

*Trap:* treating bit rate and baud as interchangeable for PAM4/PAM8.

##### Question 3. What SNR penalty does denser PAM create?

*Tests:* level spacing $\Delta=A/(M-1)$.

*Spoken answer.* "For equal spacing over the same total swing, PAM4 adjacent spacing is one third of the outer swing and PAM8 is one seventh. Ideal amplitude-separation comparisons are about 9.5 dB and 17 dB versus a full NRZ step before bandwidth and implementation effects. The practical power penalty also depends on noise bandwidth, EQ, and FEC" (§5.6).

*Pressure follow-up.* "Can I quote 9.54 dB as the PAM4 link penalty?"\
*Answer pivot.* "Only as the ideal spacing comparison. I would not call it the finished sensitivity penalty."

*Trap:* "PAM8 has no SNR cost because baud is lower."

##### Question 4. Why does linearity matter more for PAM8?

*Tests:* compression and inner-eye collapse.

*Spoken answer.* "PAM8 has seven eyes. Driver or modulator compression that barely dents PAM4 can close the inner PAM8 eyes. I budget DAC, driver, and modulator linearity across the full swing, not only the outer levels."

*Pressure follow-up.* "Outer OMA looks fine. Why fail?"\
*Answer pivot.* "Outer OMA does not prove inner-eye spacing or linearity."

*Trap:* "If average power and outer OMA pass, PAM8 is fine."

##### Question 5. How does equalization change for denser PAM?

*Tests:* EQ handoff without claiming Pass 3 depth.

*Spoken answer.* "Lower baud can ease channel loss, but denser eyes leave less margin for residual ISI and noise enhancement. I still need to know whether the impairment is precursor or postcursor and whether FFE, DFE, or DSP is doing the work (§3.6). PAM8 makes tap precision and adaptation errors more expensive."

*Pressure follow-up.* "Does lower baud remove the need for EQ?"\
*Answer pivot.* "No. It can reduce the boost required, but multilevel links still live or die on residual ISI."

*Trap:* "PAM8 needs no equalization because baud is lower."

##### Question 6. How does FEC interact with PAM8?

*Tests:* coding as part of the alphabet trade.

*Spoken answer.* "Denser PAM often needs stronger FEC or higher overhead to buy back SNR spent on level spacing. I treat FEC as part of the architecture trade, not as a cleanup step after the alphabet is chosen" (§3.9).

*Pressure follow-up.* "Can FEC fix a nonlinear transmitter?"\
*Answer pivot.* "FEC helps random or coded errors within its capability. It does not repair a closed inner eye from compression."

*Trap:* "Pick PAM8 and let FEC handle the rest."

##### Question 7. How do you think about threshold calibration?

*Tests:* seven thresholds and drift.

*Spoken answer.* "PAM8 needs seven decision thresholds. I ask how they are set at production, how they track temperature and aging, and what telemetry shows threshold or level drift. A static room-temperature calibration is not a product argument."

*Pressure follow-up.* "Who owns threshold adaptation, optics or DSP?"\
*Answer pivot.* "Whoever closes the claim. I name the owner and the observable used to retune."

*Trap:* "Thresholds are set once in the lab."

##### Question 8. What is level mismatch, and why does it matter?

*Tests:* RLM / unequal eyes.

*Spoken answer.* "Level mismatch means the eyes are not equally spaced. Outer OMA can look acceptable while an inner eye is starved. For PAM4 we use RLM; for PAM8 I apply the same idea across eight levels. Unequal spacing burns SNR that the baud reduction was supposed to buy."

*Pressure follow-up.* "Is RLM a mechanism?"\
*Answer pivot.* "No. It is a symptom metric. I still find whether the cause is DAC, driver, modulator, or bias."

*Trap:* "RLM is only a PAM4 curiosities checkbox."

##### Question 9. What is outer OMA for PAM4 and PAM8?

*Tests:* outer span versus inner eyes.

*Spoken answer.* "Outer OMA is the span from the lowest to highest optical level: $P_3-P_0$ for PAM4 and $P_7-P_0$ for PAM8. I never use an inner-eye span as the general OMA definition in a budget."

*Pressure follow-up.* "Does outer OMA replace eye quality metrics?"\
*Answer pivot.* "No. It sets the outer swing. Eye quality and level uniformity still need their own evidence."

*Trap:* "OMA means the bottom eye height."

##### Question 10. How does extinction ratio fit multilevel links?

*Tests:* ER versus multilevel quality.

*Spoken answer.* "Extinction ratio compares high and low levels. It matters for average power, eye placement, and some noise terms, but it does not by itself prove PAM4 or PAM8 eye quality. I report ER with outer OMA and level-uniformity evidence."

*Pressure follow-up.* "High ER means better PAM8?"\
*Answer pivot.* "Not if linearity collapses the inner levels to get that ER."

*Trap:* "Raise ER until PAM8 passes."

##### Question 11. How do you choose the optical modulator for PAM8?

*Tests:* DML/EML/MZM/ring/segmented trade.

*Spoken answer.* "I ask where the alphabet is generated and which device can stay linear across eight levels. A DML is usually the hardest for dense PAM. An MZM or segmented optical approach is often more credible if the electrical DAC and bias control are solid. Rings need thermal and resonance control in the story (Chapter 6, §4.5)."

*Pressure follow-up.* "Can I reuse a PAM4 EML for PAM8?"\
*Answer pivot.* "Only if linearity, bandwidth, and calibration evidence support eight levels, not because the part shipped as PAM4."

*Trap:* "Any 224G PAM4 optic is automatically PAM8-capable."

##### Question 12. When is PAM8 not worth it?

*Tests:* stop criteria for denser alphabets.

*Spoken answer.* "If the channel already closes on PAM4, or if optical linearity, FEC power, or factory calibration cannot support eight levels, I stay on PAM4 or fix the channel. Baud relief that spends more power than it saves is a bad trade (§4.7, §3.14.3)."

*Pressure follow-up.* "Marketing wants PAM8 on the roadmap. What do you say?"\
*Answer pivot.* "I show the baud gain, the SNR and linearity bill, and the measurement plan. Without those, PAM8 is a slogan."

*Trap:* "Always move to the densest PAM the DAC supports."

##### Question 13. Give a 60-second multilevel-signaling plan.

*Tests:* end-to-end whiteboard answer.

*Spoken answer.* "I start from the bit rate and ask what baud each alphabet requires. I compare level spacing and the ideal vertical penalty, then ask whether the channel, connector, and optics can deliver the needed linearity. I choose where PAM is generated, electrical or optical, name FEC and EQ assumptions, and define outer OMA, level uniformity, and threshold calibration evidence. I pick PAM8 only when baud relief outweighs the SNR and calibration cost."

*Pressure follow-up.* "What do you measure first on a PAM8 prototype?"\
*Answer pivot.* "Outer levels, inner-eye openings or equivalent level histogram, RLM-class uniformity, and BER or FEC stress at temperature corners."

*Trap:* "Look only at average power and a single outer eye."


<div class="nav-links">
  <a href="ch3-intensity-modulation-direct-detection">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch5-quantitative-models-noise-rin-and-ber">Next &rarr;</a>
</div>
