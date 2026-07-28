---
layout: default
title: "Ch 4: Quantitative models: noise, RIN, and BER"
---

# 4 Quantitative models: noise, RIN, and BER

The previous chapters argued mostly in architecture and measurement vocabulary. This one puts numbers behind the two questions every link engineer eventually asks: *what bit-error ratio (BER) will this receiver deliver?* and *what is the minimum signal it needs?* The answers follow a short chain of physics that has been stable for decades of IM/DD design: Gaussian statistics at the decision circuit, a handful of noise sources, and the way relative intensity noise (RIN) turns into an error floor. Understanding that chain is what lets you read a sensitivity number or a RIN floor without treating the datasheet as magic.

Everything here is backed by short, reproducible Python (in `sims/`), so the figures are computed curves rather than sketches. The models follow the treatment in Säckinger's *Analysis and Design of Transimpedance Amplifiers for Optical Receivers*,[^11] and the sanity checks in the code reproduce that book's worked numbers.

##### Model-fidelity ladder.

Use the simplest model that answers the decision. Do not force a simple model to explain evidence outside its assumptions. This is a model-fidelity ladder, not a product lifecycle.

Level 1. Scalar link budget

: Tx OMA or power, path loss, receiver sensitivity, allocated penalties and margin. Answers: does the first-order budget close?

Level 2. Equivalent-$Q$ noise model

: Optical levels, responsivity, thermal/shot/RIN, effective noise bandwidth. Answers: does stochastic vertical noise explain the required BER?

Level 3. Waveform and channel model

: Finite bandwidth, dispersion, jitter, ISI, nonlinear levels, reflections, equalization, compression. Answers: how does the real waveform behave?

Level 4. Measured statistical behavior

: BER waterfalls, error histograms, time-correlated bursts, temperature and lane distributions. Answers: does the product population match the model?

## The decision: from $Q$ to BER

A binary receiver samples a noisy voltage and compares it to a threshold. If the noise is Gaussian and the threshold is optimally placed, the BER depends on a single quality factor $Q$, the separation between the one and zero levels measured in units of their combined noise: $$Q = \frac{I_1 - I_0}{\sigma_1 + \sigma_0},
  \qquad
  \mathrm{BER} = \tfrac{1}{2}\,\mathrm{erfc}\!\left(\frac{Q}{\sqrt{2}}\right).$$ The mathematical $Q$-to-BER mapping depends on the sampled level distributions rather than directly on the optical pulse shape. Pulse shape, bandwidth, dispersion, jitter, and equalization still determine those distributions and therefore cannot be ignored when predicting $Q$ from a physical link. This binary $Q$-to-BER equation is an *equivalent-quality* approximation used throughout link budgeting. A full PAM4 treatment evaluates three decision boundaries, unequal level noise, nonlinearity, equalization, and Gray mapping; do not treat the binary formula as a complete PAM4 model. When applying the approximation to a PAM4-class example, call it a *binary-equivalent* $Q$. [^12] Two reference points anchor the binary curve: the classic uncoded target $\mathrm{BER}=10^{-12}$ needs $Q=7.03$. For a named KP4-class optical PMD under its random-error assumption, a pre-FEC objective near $2.4\times10^{-4}$ corresponds to $Q\approx3.5$ on this binary map (Chapter 3). That number is not a universal Reed--Solomon threshold; state the FEC architecture, error model, target PMD, and post-FEC metric.

##### BER and FEC terminology.

Pre-FEC BER or symbol-error behavior describes the decoder input. Post-FEC behavior describes residual errors after decoding. Corrected-codeword counts can reveal declining margin before post-FEC failure. FEC thresholds depend on code, interleaving, PMD, error distribution, and implementation. Burst errors can be more harmful than an equal average random BER. A quoted FEC threshold is not a universal analog receiver specification (Chapter 10, Chapter 3).

    from scipy.special import erfc, erfcinv
    import numpy as np

    def q_to_ber(q):
        return 0.5 * erfc(q / np.sqrt(2))

    def ber_to_q(ber):
        return np.sqrt(2) * erfcinv(2 * ber)

<figure id="fig:berq" data-latex-placement="ht">
<embed src="figures/fig_ber_vs_q.pdf" />
<figcaption>The Gaussian decision curve. Every dB of <span class="math inline"><em>Q</em></span> buys orders of magnitude of BER near the knee, which is why FEC (trading a modest <span class="math inline"><em>Q</em></span> for a huge BER improvement) is decisive.<span id="fig:berq" data-label="fig:berq"></span></figcaption>
</figure>

§4.1 shows why the curve is so steep near the operating point: a small change in $Q$ (equivalently, in received power) moves the BER by orders of magnitude. This steepness is exactly what FEC exploits: nudging the required $Q$ from 7.03 down to 3.5 relaxes the optical power budget by several dB.

## The receiver noise budget

$Q$ is only as good as our estimate of $\sigma$. Three noise sources dominate a short-reach IM/DD receiver. Independent noise sources add in variance (equivalently, rms amplitudes add in quadrature):

Thermal / circuit noise

: the input-referred noise of the TIA and following stages, roughly white, so its variance scales with the noise bandwidth: $\sigma_{\text{th}}^2 = i_n'^2\,\mathrm{BW}$, where $i_n'$ is a noise-current density (A/$\sqrt{\text{Hz}}$). *Signal-independent.*

Shot noise

: from the discreteness of photocurrent, $\sigma_{\text{shot}}^2 = 2q\,I\,\mathrm{BW}$. *Grows with signal*, so it is larger on the ones than the zeros.

RIN (relative intensity noise)

: the laser's own intensity fluctuations, $\sigma_{\text{RIN}}^2 = \mathrm{RIN}_{\text{lin}}\,I^2\,\mathrm{BW}$, with $\mathrm{RIN}_{\text{lin}} = 10^{\mathrm{RIN[dB/Hz]}/10}$. *Grows with the square of signal*, the key fact of the next section.

##### Noise bandwidth.

Noise bandwidth is the integral of the squared magnitude of the applicable noise transfer function, expressed as an equivalent rectangular bandwidth. It is not automatically equal to baud rate, bit rate, or the receiver's quoted $-3$ dB bandwidth. A first-order estimate must name where the noise density is referred, which filter response is assumed, and whether equalization changes the integrated noise.

##### Limits of variance addition.

Correlated sources need covariance terms. Discrete spurs should not be treated automatically as white noise. Data-dependent jitter and ISI are not necessarily stochastic noise. RIN altered by reflections may be frequency-dependent and nonstationary. Receiver adaptation can change the effective noise transfer function. Do not add thermal, shot, and RIN *currents* as if they were amplitudes on one line.

Because shot and RIN noise are signal dependent, we evaluate $\sigma_1$ and $\sigma_0$ separately and form $Q$ with their sum. The core of the model is just this:

    def nrz_q(p_avg_w, responsivity, i_thermal_rms, bw,
              er_db=np.inf, rin_db_hz=-np.inf):
        p1, p0 = er_levels(p_avg_w, er_db)      # one / zero optical powers
        i1, i0 = responsivity * p1, responsivity * p0
        var1 = i_thermal_rms**2 + 2*Q_E*i1*bw   # thermal + shot
        var0 = i_thermal_rms**2 + 2*Q_E*i0*bw
        if np.isfinite(rin_db_hz):
            rin = 10**(rin_db_hz / 10)
            var1 += rin * i1**2 * bw            # RIN grows as I^2
            var0 += rin * i0**2 * bw
        return (i1 - i0) / (np.sqrt(var1) + np.sqrt(var0))

## RIN and the BER floor

Here is the consequence that makes RIN worth its own section. Thermal noise is fixed, so pouring on more optical power raises $I_1-I_0$ while $\sigma_{\text{th}}$ stays put, so $Q$ improves without limit. But RIN noise scales *with the signal itself*: $\sigma_{\text{RIN}} \propto I$. Once RIN dominates, the signal and its noise grow together and $Q$ stops improving. Taking the high-power, high-extinction limit (thermal and shot negligible, $I_0\to0$): $$Q_{\max} \;=\; \frac{I_1}{\sigma_{\text{RIN},1}}
           \;=\; \frac{1}{\sqrt{\mathrm{RIN}_{\text{lin}}\,\mathrm{BW}}}.$$ This is a *simplified dominant-RIN ceiling*, not a universal hard limit for every PAM4 product. It assumes dominant RIN, a defined effective bandwidth, approximately Gaussian stationary noise, adequate extinction, binary or idealized level structure, no receiver overload, and no stronger jitter, ISI, reflection, or nonlinear limitation. Under those assumptions, no amount of transmit power or receiver sensitivity can push $Q$ past $Q_{\max}$, so a BER floor appears. Equivalently, the power penalty to hold a target $Q$ is $$\mathrm{PP} = \frac{1}{\sqrt{1 - Q^2\,\mathrm{RIN}_{\text{lin}}\,\mathrm{BW}}},$$ which diverges as $Q\to Q_{\max}$.

> **Engineering heuristic.** If the waterfall floors, stop raising launch power as the primary fix. You are buying photons against a non-power-limited impairment.

<figure id="fig:berpower" data-latex-placement="ht">
<embed src="figures/fig_ber_vs_power_rin.pdf" />
<figcaption>With RIN present, the BER stops falling no matter how much power is added. The thermal/shot-only curve dives; each RIN level flattens into a floor. (RIN values here are deliberately high to make the floor visible in-frame; good DFBs at <span class="math inline"> &lt; −150</span> dB/Hz have no floor at these rates; see text.)<span id="fig:berpower" data-label="fig:berpower"></span></figcaption>
</figure>

<figure id="fig:rinfloor" data-latex-placement="ht">
<embed src="figures/fig_rin_floor.pdf" />
<figcaption>The RIN ceiling <span class="math inline">$Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$</span>. Wider receiver bandwidth (higher lane rate) integrates more RIN, lowering the ceiling. Where a curve dips below the dotted anchors, that link can no longer reach the corresponding BER.<span id="fig:rinfloor" data-label="fig:rinfloor"></span></figcaption>
</figure>

§4.2 shows the floor directly; §4.3 plots the ceiling versus RIN for three lane rates. The bandwidth dependence matters: doubling the lane rate doubles the noise bandwidth and drops $Q_{\max}$ by $\sqrt{2}$ ($\approx1.5$ dB of margin), so RIN that is harmless at 25G can bite at 200G. This is the quantitative reason the laser chapter (Chapter 5) lists RIN among the parameters that decide pass/fail.

### Typical RIN values (2026)

How much RIN headroom do real sources have? Table 4.1 collects representative figures. Two cautions on reading them. First, standards quote *$\mathrm{RIN}_x\mathrm{OMA}$*, RIN referenced to the OMA and measured under a specified optical return loss (ORL) $x$, because back-reflections into the laser raise its noise, so a spec limit is a stressed, worst-case number, not the device's quiet intrinsic RIN.[^13] Second, RIN degrades with optical feedback, so isolator-free and co-packaged designs care as much about *feedback tolerance* as about the isolated number, one reason quantum-dot lasers (near-zero linewidth-enhancement factor) are attractive for CPO .

A RIN number in dB/Hz is, by itself, incomplete: because RIN is *relative*, it only becomes an absolute noise current once the photocurrent $I=\mathcal{R}P$ is fixed. The intensity-noise current density is $$i_{\text{RIN}} = \sqrt{\mathrm{RIN}_{\text{lin}}}\;I \quad[\text{A}/\sqrt{\text{Hz}}],
  \qquad
  S_{\text{RIN}} = \mathrm{RIN}_{\text{lin}}\,I^2 \quad[\text{A}^2/\text{Hz}],$$ so it scales linearly with received power. Table 4.1 therefore lists both the RIN and the current density it produces at a common reference operating point ($\mathcal{R}=0.8$ A/W, $P_{\text{rx}}=0$ dBm, i.e. $I=0.8$ mA), the units a receiver designer actually compares against.

<table class="book-table"><tr><th>Source</th><th>RIN (dB/Hz)</th><th>i_RIN @ 0 dBm</th><th>Metric</th><th>Note</th></tr><tr><td>400G-FR4 / 100G Lambda class limit</td><td>-136</td><td>127</td><td>stressed RIN_xOMA</td><td>named ORL (e.g.\ 17.1 dB)</td></tr><tr><td>Datacom VCSEL, 850 nm (MMF)</td><td>-135 to -145</td><td>45 to 142</td><td>intrinsic</td><td>quiet parts \!-145</td></tr><tr><td>Good datacom DFB / EML</td><td>-145 to -155</td><td>14 to 45</td><td>intrinsic</td><td>CPO ELS often target \!-145</td></tr><tr><td>Quantum-dot laser on Si</td><td>-140 to -150</td><td>25 to 80</td><td>intrinsic</td><td>feedback-tolerant class</td></tr><tr><td>Heterogeneous / injection-locked Si</td><td>-155 to -165</td><td>4.5 to 14</td><td>intrinsic</td><td>high-Q feedback</td></tr><tr><td>Lab record (QD + injection lock)</td><td>\!-168</td><td>3.2</td><td>intrinsic</td><td>research</td></tr></table>
**Table 4.1.** Representative RIN by source (c. 2026) at $\mathcal{R}=0.8$ A/W, $P_{\text{rx}}=0$ dBm ($I=0.8$ mA). Intrinsic RIN and stressed $\mathrm{RIN}_x\mathrm{OMA}$ are different metrics; do not convert them through one equation unless the definitions align. Density $i_{\text{RIN}}=\sqrt{\mathrm{RIN}_{\text{lin}}}\,I$.

For scale, at that same $0.8$ mA the *shot*-noise density is $\sqrt{2qI}=16$ pA/$\sqrt{\text{Hz}}$ ($S=2.6\times10^{-22}$ A$^2$/Hz) and a good high-speed TIA adds roughly $25$ pA/$\sqrt{\text{Hz}}$ of thermal noise. So a VCSEL at $-140$ dB/Hz ($80$ pA/$\sqrt{\text{Hz}}$) already dominates both, while a heterogeneous source at $-160$ dB/Hz ($8$ pA/$\sqrt{\text{Hz}}$) is a minor term. The key asymmetry: thermal noise is fixed and shot grows only as $\sqrt{I}$, but RIN grows as $I$, so at low received power thermal wins and RIN is irrelevant, and only above a break-in power (Table 4.4) does RIN take over. That is why quoting a RIN figure without an operating power says little.

<figure id="fig:noisedensity" data-latex-placement="ht">
<embed src="figures/fig_noise_density_vs_power.pdf" />
<figcaption>Noise current densities versus received power. Thermal is flat, shot <span class="math inline">$\propto\!\sqrt{I}$</span>, RIN <span class="math inline">∝ <em>I</em></span>; the RIN curves cross the fixed thermal floor only above a break-in power, which is why RIN only “makes sense” once the optical power (hence <span class="math inline"><em>I</em> = ℛ<em>P</em></span>) is stated.<span id="fig:noisedensity" data-label="fig:noisedensity"></span></figcaption>
</figure>

Put these against the simplified dominant-RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$. Assumptions: RIN dominates, noise bandwidth is defined, level structure is idealized, no stronger deterministic impairment is present, and the receiver is not compressed. At 200G-PAM4 bandwidths ($\mathrm{BW}\approx75$ GHz), plugging the stressed $-136$ dB/Hz $\mathrm{RIN}_x\mathrm{OMA}$ number into that intrinsic-style formula is illustrative only; the definitions do not automatically align. Even under that optimistic plug-in, $Q_{\max}\approx23$ is far above $Q=7$ for $10^{-12}$, so for well-behaved sources RIN is often not the limiter; thermal noise is. RIN becomes the story when feedback, aging, or a marginal source pushes the *effective* intensity noise toward $-125$ dB/Hz class. A third path is electrical: laser bias-driver current noise converts to equivalent RIN (§5.8) and must be budgeted separately from intrinsic laser RIN.

<table class="book-table"><tr><th>Quantity</th><th>Meaning</th></tr><tr><td>Intrinsic RIN</td><td>Relative intensity-noise spectrum under stated source conditions</td></tr><tr><td>Stressed RIN_xOMA</td><td>Standard-defined Tx metric under a named ORL and normalization</td></tr><tr><td>Equivalent bias-board RIN</td><td>Optical intensity noise from electrical current-noise coupling</td></tr><tr><td>Absolute RIN current density</td><td>Current-noise density at a stated photocurrent</td></tr></table>
**Table 4.2.** RIN-related quantities. Similar units do not guarantee identical definitions (§5.8, Chapter 5).

**Key idea.** Thermal noise is beaten by power; dominant RIN is not. Under a simplified model, $\sigma_{\text{RIN}}\propto I$ imposes $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$. Keep intrinsic RIN and stressed $\mathrm{RIN}_x\mathrm{OMA}$ separate. Feedback, aging, and bias-board noise erode the margin that quiet intrinsic sources appear to have.

## Sensitivity and OMA

### Common misconception: sensitivity does not guarantee a working link

Received power exceeding the datasheet sensitivity number does not guarantee low BER. Sensitivity is measured under specific, controlled assumptions: a clean transmitter, known extinction ratio, specified ORL, and a particular equalization state. In the field, BER depends on all of these simultaneously:

- received optical power;

- extinction ratio and OMA (not just average power);

- RIN under the actual ORL;

- jitter (random and deterministic);

- ISI from bandwidth limits and dispersion;

- receiver thermal noise and any TIA compression;

- equalization state and FEC margin.

Sensitivity is therefore a shorthand for receiver noise performance under reference conditions, not a complete description of whether the link closes. A link that "has enough power" can still fail if ER is poor, RIN is elevated, or the equalizer is saturated. Always close the full link budget (Appendix E.5), not just the power line.

<table class="book-table"><tr><th>Quantity</th><th>Required condition</th></tr><tr><td>Transmit average power</td><td>Named output plane and operating state</td></tr><tr><td>Transmit OMA</td><td>Named output plane, modulation definition, calibration method</td></tr><tr><td>Received power</td><td>Receiver optical-input plane</td></tr><tr><td>Receiver sensitivity</td><td>Average power or OMA; BER/FEC target; Tx condition; wavelength; temperature</td></tr><tr><td>RIN</td><td>Intrinsic or stressed definition; optical power or OMA; ORL; frequency range</td></tr><tr><td>TIA noise</td><td>Density or integrated rms; input reference; bandwidth and loading</td></tr><tr><td>BER</td><td>Pre- or post-FEC; interval; pattern or traffic; lane and direction</td></tr></table>
**Table 4.3.** Metric and reference-plane checklist. A number without its metric definition and reference plane cannot be entered safely into the model.

> **Tradeoff.** Better receiver sensitivity vs receiver complexity
>
> *Improves:* APD gain, stronger DSP, deeper equalization, or quieter optics can close a tight budget
>
> *Worsens:* Power, latency, calibration burden, and reliability of the more complex path
>
> *When acceptable:* When the sensitivity line is the true limiting ledger after Tx and plant are sound
>
> *Experienced decision:* Improve the weakest link, not the most visible datasheet metric.

### OMA versus average power

Two links may have identical average optical power but different BER. The reason is OMA and extinction ratio. At fixed average power $P_\mathrm{avg}$, the OMA depends on ER through $$\frac{\mathrm{OMA}}{P_\mathrm{avg}}
  = \frac{2(\mathrm{ER}-1)}{\mathrm{ER}+1},$$ where ER is the linear extinction ratio $P_1/P_0$. A link with 10 dB ER ($\mathrm{ER}_\mathrm{lin}=10$) delivers $\mathrm{OMA}/P_\mathrm{avg} = 18/11 \approx 1.636$, while 6 dB ER ($\mathrm{ER}_\mathrm{lin}\approx 4$) delivers $6/5 = 1.200$. The difference is about 1.36 dB of OMA at the same average power. Whether that 1.36 dB matters depends on where the receiver sits on its BER waterfall: near the sensitivity cliff a 1 dB OMA change moves BER by orders of magnitude (§4.1, §4.2), while well above sensitivity the same change is invisible. The impact also depends on RIN, bandwidth, equalization state, and TDECQ; ER alone does not set BER.

For PAM4, the relevant quantity is the outer OMA ($P_3 - P_0$), and level spacing (RLM) matters independently. A transmitter that launches adequate average power but has compressed inner eyes (poor RLM) will fail TDECQ even though a power meter reads in-spec. This is why TDECQ, OMA, and RLM are specified together, not average power alone (Appendix E.3).

### The sensitivity formula

Turning the question around (*what is the least power that meets a target BER?*) gives the sensitivity. Referring the receiver's input noise current $i_n$ (already integrated rms, not a density) back to the optical input through the responsivity $\mathcal{R}$: $$P_{\text{sens}} = \frac{Q\,i_n}{\mathcal{R}}
  \qquad\text{(average power)},\qquad
  P_{\text{sens}}^{\text{OMA}} = \frac{2\,Q\,i_n}{\mathcal{R}}.$$ These simple expressions assume binary signaling, a stated relation between average power and OMA, high or explicitly handled extinction ratio, signal-independent effective rms noise for the simplified form, a linear detector and TIA, no substantial ISI, jitter, compression, or RIN floor, and an optimal or defined decision threshold. For PAM4, treat the calculation as a *first-order binary-equivalent estimate*, not a standards-compliance receiver calculation. A noise density in A/$\sqrt{\mathrm{Hz}}$ must be integrated through the effective noise bandwidth before it enters these equations.

Modern short-reach standards specify *OMA* rather than average power. For binary NRZ, $\mathrm{OMA}=P_1-P_0$; for PAM4, outer OMA is $P_3-P_0$. OMA decouples the sensitivity spec from extinction ratio. As a check, the textbook example ($i_n = 1~\mu$A, $\mathcal{R}=0.8$ A/W, $\mathrm{BER}=10^{-12}$) gives $P_{\text{sens}}=7.03\times1~\mu\text{A}/0.8 = 8.8~\mu$W, or $-20.6$ dBm, which the code reproduces. A finite extinction ratio costs an idealized further $\mathrm{PP}_\mathrm{dB}=10\log_{10}[(\mathrm{ER}_\mathrm{lin}+1)/(\mathrm{ER}_\mathrm{lin}-1)]$: $0.87$ dB at 10 dB ER, $2.2$ dB at 6 dB ER. These penalties feed link budgets (Chapter 3) and TDECQ discussion (Chapter 7); do not double-count TDECQ as an independent penalty if the compliance method already includes it. Do not convert every impairment into arbitrary dB, mix average-power sensitivity with OMA penalties, or combine nominal values from one plane with worst-case values from another as if they were independent.

##### Worked example: DR4-class budget check.

Take a 200G/lane DR-class estimate with Ge-on-Si PIN ($\mathcal{R}=0.9$ A/W), TIA $i_n=13$ pA/$\sqrt{\text{Hz}}$, noise bandwidth $\approx60$ GHz, and a KP4-class pre-FEC objective $2.4\times10^{-4}$ mapped to binary $Q\approx3.5$ (§4.1, §3.12). Reference plane: receiver optical input. Assume Gaussian noise, equalized eye, no compression, and RIN not yet dominant.

Integrated thermal-class noise: $i_n \sqrt{\mathrm{BW}} \approx
13\times10^{-12}\times\sqrt{60\times10^9} \approx 3.2~\mu$A rms. Required OMA under the binary sensitivity formula: $$P_{\text{OMA,sens}} = \frac{2 Q i_n \sqrt{\mathrm{BW}}}{\mathcal{R}}
\approx \frac{2\times3.5\times3.2~\mu\text{A}}{0.9} \approx 25~\mu\text{W}
\approx -16~\text{dBm}.$$ Illustrative allocations (not a normative budget): $\sim$3 dB TDECQ-class Tx impairment *or* remaining margin after a TDECQ-based OMA method (not both), $\sim$2 dB connector/fiber at stated planes, $\sim$2 dB system margin. That lands near $-9$ dBm class OMA at the receiver input, or roughly $-6$ to $-4$ dBm launched depending on reach. Parameter sensitivity: $\pm$1 dB in $i_n$ or $\mathcal{R}$ moves the estimate about 1 dB; a RIN floor or MPI can invalidate the waterfall entirely.

Where the model stops: unequal PAM4 levels, level-dependent noise, strong ISI, compressed TIA, correlated RIN, or a different FEC/error model. If measured sensitivity is worse, bisect RIN, reflections, and ER (Appendix E.5, Appendix E.2).

##### Model-validity checklist.

Before applying $Q$, $Q_{\max}$, or $P_{\mathrm{sens}}$, ask:

- Is the noise approximately Gaussian at the decision point?

- Is the noise bandwidth defined for this measurement?

- Are PAM4 levels equally spaced (or is RLM budgeted)?

- Is noise level-dependent (shot/RIN) accounted for?

- Is the receiver compressed or overloaded?

- Is residual ISI deterministic rather than noise-like?

- Is RIN intrinsic, stressed $\mathrm{RIN}_x\mathrm{OMA}$, or bias-board noise?

- Is the FEC threshold appropriate for this PMD and error model?

- Is the input metric average power or OMA, and at which reference plane?

<!-- -->

<pre class="dectree" aria-label="Measured BER behavior"><code>Measured BER behavior
  |
Gaussian stationary waterfall?
  |-- YES --&gt; equivalent-Q model may be adequate
  |-- NO  --&gt; inspect PAM4 levels, ISI, jitter,
              bursts, reflections, compression,
              adaptation, and non-Gaussian tails</code></pre>
##### Correlating the model with the bench.

A model is validated by prediction across changed conditions, not by fitting one curve after the fact. Recommended order:

1.  Verify attenuator and power-meter calibration.

2.  Establish the optical reference plane.

3.  Measure transmitter average power, OMA, ER or RLM, and quality metric.

4.  Measure receiver noise or infer an effective value from trusted characterization.

5.  Sweep received OMA and record BER with sufficient error count or dwell.

6.  Fit only physically meaningful parameters.

7.  Compare curve crossing, slope, floor, and overload behavior.

8.  Repeat across lanes and temperature.

9.  Record model uncertainty and measurement uncertainty separately.

## Receiver technologies and their noise (2026)

The sensitivity formula $P_{\text{sens}}=Q\,i_n/\mathcal{R}$ has exactly two device inputs: the photodiode responsivity $\mathcal{R}$ and the amplifier's input-referred noise current $i_n$. So "receiver noise performance" is really a statement about the detector--TIA pair. Ge-on-silicon PIN plus a closely integrated CMOS or SiGe TIA is a common short-reach path because it offers useful responsivity, bandwidth, and integration. Alternative detectors become attractive when gain, saturation, wavelength, linearity, or packaging requirements change (§4.5).

##### Photodiodes and transimpedance amplifiers.

The photodiode converts photons to photocurrent; the *TIA* (transimpedance amplifier) converts current to voltage with low input-referred noise. For PAM4 at 100--224G/lane:

- **PIN (Ge-on-Si):** no internal gain; lowest excess noise; common short-reach choice (Table 4.6). Capacitance at the TIA input dominates $i_n$.

- **APD**: internal multiplication. Any sensitivity benefit versus PIN depends on gain, excess-noise factor, bandwidth, receiver design, and BER target; published Ge/Si APD results often cite roughly 5--9 dB under specific conditions, not as a universal gain .

- **UTC/MUTC:** electron-only transport for $>\!200$ GHz BW and high saturation; used when linearity and speed beat raw sensitivity .

The TIA often embeds *CTLE* for LPO (§3.6, Appendix H.5.1): a fixed high-frequency boost before the host SerDes ADC. Co-packaging PD and TIA (sub-mm interconnect) is the noise win repeated throughout this book (Chapter 2).

##### Why Ge-on-Si is a common mainstream path.

Germanium grown on silicon absorbs the O- and C-bands, is CMOS-process-compatible, and can be built on the same PIC as the modulators and couplers. Modern devices reach $\mathcal{R}\approx0.8$--$1.0$ A/W with dark currents of single-digit to tens of nA and, in mid-2020s research, $-3$ dB bandwidths beyond 100 GHz (e.g. a recessed Ge/Si PIN at 106 GHz, $0.93$ A/W, $<10$ nA; SiN-coupled lateral Ge $>110$ GHz at 1 mA) . Monolithic or 3D/flip-chip co-integration keeps the PD-to-TIA interconnect short, so the input node capacitance stays low. In common front-end-limited approximations, input-referred noise rises strongly with input capacitance and required bandwidth; some simplified architectures produce an approximate $i_n \!\propto\! C\,f^{3/2}$ scaling. Actual scaling depends on TIA topology, transistor technology, feedback network, detector impedance, equalization, power, and stability. Short interconnects remain quiet when those terms cooperate (Chapter 2).

##### What the TIA must deliver.

The TIA is the receive twin of the modulator driver (§3.14.3). At 224 GBd PAM4 you need bandwidth $\gtrsim$50--70 GHz for a 112 GBd Nyquist-class front-end (often less than the Tx driver BW because the optical channel and reference receiver already band-limit; LPO pushes for flatter, more linear TIAs), input-referred noise in the low teens of pA$/\sqrt{\mathrm{Hz}}$ once co-packaged with a low-$C$ PD, linearity / overload so large OMA and reflections do not crush PAM4 levels (RLM) or trip AGC into a bad corner, and optional CTLE for LPO/LRO so the host SerDes sees a usable eye without module DSP (§3.6, Appendix H.5.1). In common front-end-limited approximations, noise rises strongly with input capacitance and bandwidth (sometimes near $i_n \propto C\,f^{3/2}$). That is why close detector--TIA integration is valuable at 200G+: every millimetre of bondwire spends noise and bandwidth that FEC cannot recover. Integration is an engineering trade against repairability and yield, not a universal mandate.

##### Noise levels you actually budget.

Table 4.4 puts the model numbers next to published front-ends. Shot noise at 0 dBm into $\mathcal{R}=0.8$ A/W is $\sqrt{2qI}\approx16$ pA$/\sqrt{\mathrm{Hz}}$; a good TIA sits near that floor. Worse $i_n$ or higher $C$ burns sensitivity linearly via $P_{\mathrm{sens}}=Q\,i_n/\mathcal{R}$ (§4.4).

<table class="book-table"><tr><th>Front-end</th><th>i_n (pA/Hz)</th><th>BW / rate</th><th>Sensitivity note</th></tr><tr><td>Typical ``good'' short-reach TIA (book model)</td><td>25</td><td>---</td><td>older rule-of-thumb floor</td></tr><tr><td>16-nm CMOS + co-pkg PD</td><td>16.9</td><td>32 GHz / 112G PAM4</td><td>-8.2 dBm class</td></tr><tr><td>55-nm SiGe 4112 GBd linear TIA</td><td>13.2</td><td>65 GHz / 224G</td><td>1.2 pJ/bit</td></tr><tr><td>Shot noise @ 0 dBm, R=0.8 A/W</td><td>16</td><td>---</td><td>physics floor at that power</td></tr></table>
**Table 4.4.** Input-referred TIA noise densities used in link budgets (c. 2023--26 published front-ends). Integrate $i_n\sqrt{\mathrm{BW}}$ for rms noise before applying $Q$ (§4.4). Sources in text.

2026 linear PAM4 front-ends land around $10$--$17$ pA$/\sqrt{\text{Hz}}$: e.g. $16.9$ pA$/\sqrt{\text{Hz}}$ at 112G in 16-nm CMOS ($-8.2$ dBm sensitivity)  and $13.2$ pA$/\sqrt{\text{Hz}}$ at 224G in 55-nm SiGe BiCMOS (65 GHz BW, 1.2 pJ/bit) . Put these in the model: $i_n\approx13$ pA$/\sqrt{\text{Hz}}$ integrated over $\sim\!60$ GHz is $\approx3.2~\mu$A rms, giving an NRZ average sensitivity near $-15$ dBm; the PAM4 level penalty lands OMA sensitivities in the $-8$ to $-10$ dBm range these front-ends report.

##### Industry snapshot --- mid-2026 (receivers).

Table 4.5 pairs detectors and TIAs with maturity labels. Commercial linear-optics TIAs (Semtech GN1834L/DL, GN1838DL) target LPO/LRO/CPO at 224G/lane with on-chip EQ (production / sampling class). Semtech has also shown 448G-class PMD ICs (TN14740 TIA) at OFC 2026 demos (vendor demonstration; not a volume datasheet claim) . On the detector side, recessed Ge/Si PINs at 106 GHz / 0.93 A/W , Ge/Si UMC-APDs at 105 GHz with a published $\sim$9 dB sensitivity gain over PIN at 224/260G PAM4 under that paper's conditions , waveguide Ge/Si APDs toward 100 GHz at 2 A/W , and OFC 2026 Ge-on-Si APDs at 180 GBd PAM4  mark the research edge. UTC/MUTC PDs remain the high-saturation / $>\!200$ GHz niche .

<table class="book-table"><tr><th>Part / paper</th><th>Type</th><th>BW / i_n or R</th><th>Rate / sens.</th><th>Note</th></tr><tr><td>Semtech GN1834L/DL / GN1838DL</td><td>TIA</td><td>224G-class; linear+EQ</td><td>224 Gb/s/lane</td><td>Commercial LPO/CPO family</td></tr><tr><td>Semtech TN14740 (demo)</td><td>TIA</td><td>448G-class</td><td>448G/lane demo</td><td>OFC 2026 booth; provisional</td></tr><tr><td>SiGe 4112 GBd TIA</td><td>TIA</td><td>65 GHz; 13.2 pA/Hz</td><td>224G PAM4</td><td>Research / product-class paper</td></tr><tr><td>16-nm CMOS + co-pkg PD</td><td>TIA+PD</td><td>16.9 pA/Hz</td><td>112G; -8.2 dBm</td><td>Co-packaged win</td></tr><tr><td>Recessed Ge/Si PIN</td><td>PD</td><td>106 GHz; 0.93 A/W</td><td>200 GBd-class</td><td><10 nA dark</td></tr><tr><td>Ge/Si UMC-APD</td><td>APD</td><td>105 GHz @ M\!\!7</td><td>224/260G; -10.9/-10.1 dBm</td><td>9 dB over PIN (paper conditions)</td></tr><tr><td>Ge/Si WG APD (300 mm)</td><td>APD</td><td>>100 GHz; 2 A/W @ 70 GHz</td><td>400G/lane target</td><td>7 V bias class</td></tr><tr><td>OFC 2026 Ge-on-Si APD</td><td>APD</td><td>70--100 GHz; 1.5--2 A/W</td><td>180 GBd PAM4</td><td>O- and C-band</td></tr><tr><td>UTC / MUTC-PD</td><td>PD</td><td>>\!110--200 GHz</td><td>high I_sat</td><td>Linear / LPO niche</td></tr></table>
**Table 4.5.** Receiver snapshot (c. 2025--26). Commercial TIA rows are vendor announcements; APD/PIN rows mix production-intent SiPh with research demos. Sensitivities are as published (FEC threshold varies).

##### Reasonable alternatives to Ge PIN + quiet TIA.

Table 4.6 lays the detector menu out. III-V InGaAs PINs (flip-chipped) trade monolithic integration for higher power handling and remain common in discrete modules. Avalanche photodiodes add internal gain that can improve sensitivity when gain, excess noise, bandwidth, and BER target cooperate (published short-reach results often land near 5--9 dB under specific conditions) at the cost of bias complexity and excess noise; device bandwidth above 100 GHz is no longer rare in research . Uni-traveling-carrier (UTC/MUTC) PDs use electron-only transport for very high saturation current, linearity, and bandwidth ($>\!200$ GHz) but modest responsivity, a fit for linear/LPO and $>\!200$ GBd analog optics more than for raw sensitivity . SOA-preamplified receivers bolt optical gain ahead of the PD for large effective responsivity and reach, but pay in ASE noise figure, power, and complexity.

<table class="book-table"><tr><th>Detector</th><th>R (A/W)</th><th>-3 dB BW</th><th>Integration</th><th>Where it fits</th></tr><tr><td>Ge-on-Si waveguide PIN</td><td>0.8--1.0</td><td>60-->\!100 GHz</td><td>monolithic on SiPh</td><td>mainstream short-reach / CPO</td></tr><tr><td>III-V InGaAs PIN (flip-chip)</td><td>0.6--0.9</td><td>60-->\!100 GHz</td><td>hybrid / flip-chip</td><td>discrete modules, high power</td></tr><tr><td>APD (Ge/Si, InP, UMC)</td><td>effective (gain)</td><td>up to \!100 GHz+</td><td>hybrid / emerging</td><td>power-starved links; gain benefit condition-dependent</td></tr><tr><td>UTC / MUTC-PD</td><td>0.1--0.8</td><td>>\!110--200 GHz</td><td>III-V</td><td>linear/LPO, >\!200 GBd, high saturation</td></tr><tr><td>SOA-preamplified PD</td><td>effective \!1</td><td>\!50 GHz</td><td>III-V PIC</td><td>tight power budgets; adds ASE noise</td></tr></table>
**Table 4.6.** Short-reach receiver detector options, c. 2026. Ranges span production to recent research; APD/UTC/SOA figures are effective (with gain) or device-record.

##### Outlook.

Volume short-reach receive commonly stays on PIN + SiGe/CMOS TIA: noise in the low teens of pA$/\sqrt{\mathrm{Hz}}$ with $>\!100$ GHz Ge PINs is often enough for DR/FR PAM4 when closely integrated, so the fight is capacitance and yield as much as detector physics. Linear optics raises the bar: LPO/LRO need high linearity, on-chip EQ, and multi-lane density (Semtech's 224G family is the public commercial marker; 448G TIA demos are still provisional, §3.14.3). APDs are back in the 200G conversation when several dB of sensitivity gain changes a power-limited plant; UTC/MUTC matter when the impairment is saturation or $>\!200$ GBd analog fidelity rather than photons per bit. Bondwire and FAU still set $C$ and BW, which is why CPO/NPO win on noise for the same reason they win on energy (Chapter 2).

**Key idea.** Receiver performance is $\mathcal{R}$ and $i_n$, with $i_n$ set by PD+TIA capacitance. Budget $10$--$17$ pA$/\sqrt{\mathrm{Hz}}$ co-packaged TIAs and $>\!100$ GHz Ge PIN/APD detectors; use APD gain or UTC saturation when the link demands it. LPO makes TIA linearity as important as raw noise.

## NRZ versus PAM4, at equal bit rate

The 224G-per-lane roadmap (Chapter 3) rides on PAM4, so it is worth seeing the trade quantitatively. At equal bit rate, PAM4 halves the ideal symbol rate relative to NRZ but divides the available outer modulation span among three eyes. The resulting link penalty depends on bandwidth, transmitter linearity, level spacing, level-dependent noise, equalization, coding, and FEC. The figure $20\log_{10}3 \approx 9.5$ dB is an *ideal vertical level-separation comparison* before bandwidth and implementation effects. §4.5 pits the two at a common 100 Gb/s: PAM4's narrower bandwidth partly offsets its level penalty, but it still often needs several dB more received power for the same BER, repaid by relaxing the electrical bandwidth the SerDes and optics must support. That balance is why many 100G/lane products used NRZ and 200G/lane products used PAM4.

<figure id="fig:pam4" data-latex-placement="ht">
<embed src="figures/fig_nrz_vs_pam4.pdf" />
<figcaption>NRZ (100 GBaud) versus PAM4 (50 GBaud) at the same 100 Gb/s. PAM4 pays a level penalty but relaxes bandwidth; the crossover with the KP4 pre-FEC threshold sets the required operating power.<span id="fig:pam4" data-label="fig:pam4"></span></figcaption>
</figure>

## Engineering lens

### How it works

Binary link models often collapse receiver performance to a quality factor $Q$: signal separation divided by combined noise. That is a useful equivalent-quality map, not a complete PAM4 theory. Thermal noise yields to more power; dominant RIN does not, which is why a BER floor can exist. The rest of this chapter computes, measures, and defends $Q$ under stated assumptions.

### How it is measured

A BER model earns trust only when every term has a bench measurement. Use a BERT and calibrated optical attenuator for BER versus received OMA. Measure receiver input-referred noise with the photodiode dark and illuminated. Use a DCA for OMA, ER, and eye quality, and a photodiode plus electrical spectrum analyzer for relative intensity noise (RIN). Repeat power sweeps at temperature and per lane. Acceptance is a curve, not one point: the required waterfall must cross the program's pre-FEC threshold with margin and without a floor (§4.1, §4.2, §4.3, §4.4).

### How it fails

Thermal noise dominates at low optical power, shot noise grows with photocurrent, and RIN grows with signal power. Reflections, crosstalk, jitter, and compression break a simple Gaussian fit. Curve shape chooses the next experiment; it is not a root-cause label (Table 4.7).

<table class="book-table"><tr><th>Measured behavior</th><th>Raises these hypotheses</th><th>Does not prove</th></tr><tr><td>Uniform waterfall shift</td><td>Lost OMA, loss, greater Rx noise, calibration offset</td><td>Which component caused it</td></tr><tr><td>High-power floor</td><td>RIN, reflections, crosstalk, jitter, bursts, distortion</td><td>Intrinsic laser RIN</td></tr><tr><td>High-power degradation</td><td>TIA/PD overload, compression, AGC/adaptation corner</td><td>Excess launch alone</td></tr><tr><td>Temperature-dependent shift</td><td>Responsivity, noise, OMA, loss, wavelength, EQ</td><td>Aging</td></tr><tr><td>One-lane-only movement</td><td>Lane-local optical or electrical path</td><td>Defective laser</td></tr><tr><td>Correlated lane movement</td><td>Shared rail, source, clock, thermal or control</td><td>Common source failure</td></tr></table>
**Table 4.7.** BER-waterfall signatures: hypothesis routing, not mechanism confirmation (Chapter 11).

\> \*\*Failure mode: BER floor\*\* \> \> \*\*Symptoms.\*\* BER improves with received power, then stops improving. \> \> \*\*Likely causes.\*\* RIN, reflection-driven multipath interference, laser-bias noise, crosstalk, or periodic jitter. \> \> \*\*Measurements.\*\* BER versus OMA, RF RIN spectrum (PD+ESA or RIN analyzer, not OSA), ORL sweep, FEC error distribution, and a quiet laser-bias source. \> \> \*\*Mitigations.\*\* Remove the correlated noise source, improve ORL, or isolate supplies. The recurrence control may be source qualification, stressed-RIN screening, supplier process control, bias-board validation, ORL control, sampled audit, ATP proxy, or fleet monitoring, depending on where the mechanism can be detected reliably (Chapter 5, Chapter 8, Chapter 9).

### How it is debugged

When pre-FEC BER moves from well below the named FEC threshold into a $10^{-6}$-class regime, save the failing condition and work in this order: received OMA, transmitter OMA and ER, receiver noise, RIN and ORL, electrical jitter, and lane crosstalk. Sweep power before changing settings. If the curve recovers with power, quantify the sensitivity shift. If it floors, split intrinsic laser noise from board noise and reflection feedback. If only temperature moves it, repeat the same terms hot and cold instead of assigning the change to "thermal margin."

\> \*\*Debug story\*\* \> \> \*\*Observed.\*\* One lane developed a BER floor after the product board replaced the bench supply. \> \> \*\*Investigation.\*\* The optical power sweep flattened. Intrinsic RIN on the quiet source passed, but discrete tones appeared with the product rails active. \> \> \*\*Finding.\*\* The laser was not the noisy element. \> \> \*\*Root cause.\*\* A switching regulator coupled into the laser bias path. \> \> \*\*Resolution.\*\* The bias filter and return path were changed, and a powered-board RIN check was added to validation.

## The debugging fork: did received power change?

When BER degrades, ask one question first:

<pre class="dectree" aria-label="BER degraded"><code>BER degraded
  |
Stable average received power?
  |-- NO  --&gt; Power ledger / optical-path investigation
  |           laser / coupling / connector / fiber / MUX / monitor
  |-- YES --&gt; Signal-quality path
              Tx / channel / Rx / DSP
              noise / timing / spectral / control
  |
Highest-value measurement
  |
Decision + recurrence control</code></pre>
Stable average received power deprioritizes gross optical loss but does not clear fast fluctuations, reflections, clipping, wavelength filtering, or monitor-calibration error. The fork chooses an investigation route; it does not establish mechanism ownership (Chapter 11).

##### Did average received optical power change?

If yes, investigate the power path:

- laser degradation (threshold rise, slope loss, COD);

- connector contamination or damage;

- coupling loss (fiber attach, FAU drift);

- fiber break or bend loss;

- MUX/de-MUX imbalance or grid misalignment.

##### Or did signal quality degrade at stable average power?

If average received power is stable but BER worsened, isolate transmitter, channel, receiver, and DSP quality:

- noise: RIN (intrinsic, feedback-driven, or bias-driver), Rx noise, crosstalk, MPI;

- timing: jitter, CDR, skew, adaptation timing;

- spectral: wavelength, filtering, alignment;

- control: bias, APC, TEC/heaters, calibration, EQ authority.

This fork often narrows an investigation in minutes. Power-path failures show up on a meter; signal-quality failures need FEC timing, DCA, BERT, or spectrum analysis, depending on access. Apply it before opening the package, changing settings, or blaming a supplier (§11.16, Chapter 11, Chapter 7).

> **Why experienced engineers separate power from quality?**
>
> Because average optical power is easy to measure but tells very little about timing, noise, distortion, or adaptation. One meter reading prunes an entire branch of the tree.

> **What this usually means.** Stable average power with rising BER
>
> *Usually:* noise, timing, spectral alignment, control or calibration, intermittent contact
>
> *Not:* gross attenuation as the primary story

## Interview takeaway

**Key idea.** Name the metric and reference plane, state the model assumptions, and close only what the model can defend: Gaussian $\mathrm{BER}(Q)$, the variance noise budget (thermal + shot + RIN), the simplified dominant-RIN ceiling $Q_{\max}=1/\sqrt{\mathrm{RIN}\cdot\mathrm{BW}}$, and $P_{\text{sens}}=Q\,i_n/\mathcal{R}$ with integrated rms noise. Verify with a measured BER waterfall. Let disagreement reveal missing physics (Table 4.3, §4.4.3, Table 4.7).

Junior mistake: raise launch power into a BER floor, or quote sensitivity without the measurement conditions (§4.3, §4.8, Chapter 5, Chapter 7).

### Interview Q&A: Quantitative Models, Noise, RIN, and BER

Practice speaking these answers aloud. Prefer physical meaning and assumptions over equation recitation. Detail lives earlier in this chapter (§4.1, §4.2, §4.3, §4.4, §4.8). Score your answer using the chapter-end spoken-answer rubric (Appendix A.12.1).

##### Question 1. What is the $Q$ factor, and when is the $Q$-to-BER relationship useful?

*Tests:* physical interpretation, Gaussian assumption, and model scope.

*Spoken answer.* "In the simple binary receiver model, $Q$ is the separation between the sampled one and zero levels divided by the sum of their rms noise widths. Under approximately Gaussian sampled distributions and an appropriate decision threshold, $Q$ maps to BER through the complementary error function. I use it to convert measured or modeled signal and noise into an expected error rate and to understand sensitivity trends. I would not treat it as a complete waveform model. ISI, non-Gaussian tails, burst errors, unequal PAM4 eyes, clipping, and adaptation can make the equivalent-$Q$ interpretation incomplete."

*Pressure follow-up.* "Can you use the same $Q$ formula directly for PAM4?"\
*Answer pivot.* "Not as a complete PAM4 model. I can use binary-equivalent-$Q$ approximations for intuition or a stated reference model, but real PAM4 has three eyes, potentially unequal level spacing, level-dependent noise, and an FEC-specific error distribution."

*Trap:* claiming $Q$ completely describes any optical link as long as the BER is known.

##### Question 2. Walk me through the receiver noise budget.

*Tests:* thermal, shot, and RIN scaling.

*Spoken answer.* "I convert optical levels to photocurrent using detector responsivity, then calculate the noise at each sampled level. Thermal and circuit noise are approximately signal-independent and integrate with noise bandwidth. Shot-noise variance grows linearly with photocurrent. RIN variance grows with the square of photocurrent. For independent terms, I add variances, not rms amplitudes, and I calculate the one-level and zero-level noise separately when the noise is signal-dependent. The resulting level separation and noise widths determine the equivalent $Q$ and expected BER."

*Pressure follow-up.* "Why are $\sigma_1$ and $\sigma_0$ different?"\
*Answer pivot.* "Shot noise and RIN depend on photocurrent, so the high optical level normally has more noise than the low level. Assuming one common noise value can misplace the optimal threshold and misestimate BER."

*Trap:* adding thermal, shot, and RIN current amplitudes directly.

##### Question 3. Why can RIN create a BER floor?

*Tests:* signal-proportional noise and asymptotic behavior.

*Spoken answer.* "Thermal noise stays roughly fixed while the signal grows, so more received power improves signal-to-noise ratio in a thermal-noise-limited link. RIN noise grows in proportion to the optical signal amplitude, so once RIN dominates, increasing power increases the signal and its noise together. $Q$ then approaches a simplified dominant-RIN ceiling and BER stops improving. That ceiling assumes dominant, approximately white Gaussian RIN, a defined bandwidth, no receiver compression, and no stronger deterministic impairment."

*Pressure follow-up.* "Does a flat BER curve prove intrinsic laser RIN?"\
*Answer pivot.* "No. A floor can also come from optical feedback, MPI, electrical bias noise, periodic jitter, crosstalk, burst errors, or receiver limitations. The curve identifies a signal-quality class, not a unique mechanism."

*Trap:* treating a BER floor as proof that the receiver needs more optical power.

##### Question 4. What can the shape of a BER waterfall tell you?

*Tests:* shift, floor, shoulder, cliff, and curve interpretation.

*Spoken answer.* "I compare the complete BER-versus-received-OMA curve rather than one operating point. A roughly horizontal shift can indicate lost OMA or increased receiver noise. A high-power floor suggests a signal-proportional, periodic, bursty, or deterministic impairment. A shoulder or multiple slopes can indicate a change in dominant mechanism, adaptation behavior, pattern dependence, or mixed populations. A sharp unexpected cliff may indicate overload, compression, control saturation, or lock loss. I compare the curve across lanes, temperature, host, and controlled disturbances before assigning ownership" (Table 4.7).

*Pressure follow-up.* "Two links have the same sensitivity at the threshold but different waterfall shapes. Are they equivalent?"\
*Answer pivot.* "No. One may have greater margin above the threshold while the other approaches a floor or cliff. A single crossing point hides the remaining operating envelope."

*Trap:* treating the power where BER crosses the FEC threshold as the only important waterfall result.

##### Question 5. What must accompany a receiver-sensitivity number?

*Tests:* reference planes, conditions, and specification interpretation.

*Spoken answer.* "I need the optical reference plane, whether the metric is average power or OMA, the modulation format and lane rate, wavelength, transmitter-quality condition, extinction ratio or level structure, ORL condition, equalization state, temperature, pattern or traffic condition, FEC and BER criterion, dwell or error count, and measurement uncertainty. Sensitivity is a receiver result under defined conditions. It does not independently guarantee that a real transmitter, fiber plant, and host combination will close" (Table 4.3).

*Pressure follow-up.* "A supplier says sensitivity is $-10$ dBm. What is your first question?"\
*Answer pivot.* "I would ask whether that is average power or OMA and at which reference plane and BER or FEC condition. Without those details, the number is not comparable."

*Trap:* assuming that if receive power is above the sensitivity number, the link should work.

##### Question 6. Explain average optical power, OMA, extinction ratio, RLM, and TDECQ.

*Tests:* metric ownership and avoiding composite-metric misuse.

*Spoken answer.* "Average power measures mean optical energy. OMA measures the modulated optical separation: one minus zero for NRZ and outer OMA for PAM4. Extinction ratio describes the ratio of high and low optical levels. RLM describes PAM4 level-spacing linearity. TDECQ is a composite transmitter-quality metric relative to a defined reference receiver. These metrics answer different questions. Two transmitters can have the same average power but different OMA or level quality and therefore very different BER. TDECQ can identify a transmitter-quality penalty, but it does not identify the physical mechanism."

*Pressure follow-up.* "Can you add a TDECQ penalty to a budget that already uses a TDECQ-based transmitter OMA requirement?"\
*Answer pivot.* "Not automatically. That can count the same transmitter impairment twice. I would first identify exactly what the compliance method and budget term already include."

*Trap:* treating OMA, extinction ratio, and TDECQ as different ways of expressing transmitter power.

##### Question 7. How do you estimate receiver sensitivity from noise and responsivity?

*Tests:* sensitivity model, units, and assumptions.

*Spoken answer.* "For a simplified binary, thermal-noise-dominated receiver, I integrate the input-referred noise-current density over the applicable noise bandwidth to obtain rms current noise. I divide the required signal current by detector responsivity to refer it to optical power. The required signal separation depends on the target equivalent $Q$. Before trusting the estimate, I verify whether the noise value is a density or already integrated, whether the metric is average power or OMA, whether extinction ratio is finite, and whether shot noise, RIN, ISI, or compression are important."

*Pressure follow-up.* "Why can't you multiply a TIA noise density directly by $Q$ and divide by responsivity?"\
*Answer pivot.* "Because the density has units per square-root hertz. It must be integrated through the effective noise transfer function, often approximated as density times the square root of noise bandwidth, before it becomes rms current."

*Trap:* using datasheet noise in pA/$\sqrt{\mathrm{Hz}}$ directly in the optical-sensitivity equation.

##### Question 8. How do bandwidth and detector--TIA capacitance affect receiver sensitivity?

*Tests:* noise-bandwidth tradeoff and integration architecture.

*Spoken answer.* "Wider electrical bandwidth admits more noise and usually requires a faster front end with lower impedance or more gain-bandwidth burden. Detector capacitance, pad capacitance, bond wires, and interconnect parasitics load the TIA input and make it harder to achieve both low noise and high bandwidth. That is why close detector--TIA integration is valuable. I would not apply one universal capacitance-to-noise power law to every topology, but the direction is clear: excess input capacitance consumes bandwidth, noise, power, or all three."

*Pressure follow-up.* "Why not simply narrow the receiver bandwidth to improve sensitivity?"\
*Answer pivot.* "Because insufficient bandwidth creates deterministic ISI and closes the eye. The optimum bandwidth balances integrated noise against waveform distortion and equalizer capability."

*Trap:* claiming maximum receiver bandwidth always provides the best BER.

##### Question 9. Compare PIN, APD, and high-saturation detector approaches.

*Tests:* detector choice and complete receiver tradeoffs.

*Spoken answer.* "A PIN detector provides no internal gain and is attractive for low excess noise, simple biasing, and close integration with a TIA. An APD provides internal multiplication that can improve sensitivity when the gain exceeds the combined excess-noise and bandwidth penalties, but it adds high-voltage bias, temperature dependence, gain control, and qualification burden. UTC or MUTC-style detectors emphasize bandwidth, saturation, and linearity rather than maximum responsivity. I would choose from the complete detector--TIA requirement: sensitivity, bandwidth, linearity, overload, power, process integration, yield, and operating environment."

*Pressure follow-up.* "An APD paper reports 8 dB better sensitivity than a PIN. Does your product receive 8 dB?"\
*Answer pivot.* "Not automatically. I would compare modulation, rate, BER target, gain, bandwidth, noise, reference receiver, temperature, and integration conditions. Published improvement is conditional, not a universal device credit."

*Trap:* claiming an APD is always preferable when the link budget is tight because it adds optical gain.

##### Question 10. How do NRZ and PAM4 trade bandwidth against vertical margin?

*Tests:* symbol rate, level spacing, and model limitations.

*Spoken answer.* "At the same bit rate, PAM4 carries two bits per symbol, so its symbol rate is half that of NRZ and the required channel bandwidth can be lower. The cost is four amplitude levels and three eyes, so the ideal level spacing is about one third of the outer OMA before accounting for unequal spacing, level-dependent noise, and transmitter distortion. That creates a significant vertical-margin penalty, partly offset by the lower bandwidth and by FEC. I would compare them using the actual transmitter, channel, receiver, equalization, and FEC model rather than one universal dB penalty."

*Pressure follow-up.* "Why not say PAM4 has exactly a 9.54 dB penalty?"\
*Answer pivot.* "That is the ideal amplitude-separation comparison for one-third eye spacing. The practical power penalty also depends on noise bandwidth, coding, level statistics, transmitter quality, and receiver implementation."

*Trap:* claiming PAM4 is always more power-efficient because it uses half the baud rate.

##### Question 11. The measured BER curve is worse than your model. How do you reconcile it?

*Tests:* model correlation and disciplined hypothesis testing.

*Spoken answer.* "I first verify units, reference planes, OMA calibration, attenuation, responsivity, noise bandwidth, target BER, and FEC assumptions. Then I compare the predicted and measured curve shape. A uniform shift may point to calibration, loss, responsivity, or receiver noise. A floor points toward RIN, reflections, crosstalk, timing, or bursts. A high-power degradation suggests compression or overload. I then add one omitted mechanism at a time or run a measurement that separates the hypotheses. I do not tune several free parameters until the model matches, because that produces fit without understanding" (§4.4.3).

*Pressure follow-up.* "Can you use measured BER to back-calculate receiver noise?"\
*Answer pivot.* "Yes, as an effective parameter under the model assumptions, but it may absorb transmitter distortion, ISI, and other unmodeled penalties. I would label it effective noise rather than claim it is the intrinsic TIA noise."

*Trap:* adjusting assumed receiver noise until the simulated BER matches the measurement.

##### Question 12. Give me a 60-second quantitative link-analysis plan.

*Tests:* complete Staff-level modeling and measurement answer.

*Spoken answer.* "I begin by defining the reference planes, modulation format, lane rate, target BER and FEC, temperature, fiber plant, and required margin. I convert transmitter levels into received OMA and photocurrent, then build the receiver noise budget using measured responsivity, input-referred noise, bandwidth, shot noise, and RIN under the relevant reflection condition. I use an equivalent-$Q$ model only within its assumptions and treat PAM4, ISI, jitter, compression, and burst behavior separately where needed. I predict the BER waterfall, then measure it with a calibrated attenuator and compare its crossing, slope, floor, and temperature movement. The result drives the design margin, architecture choice, or next discriminating measurement."

*Pressure follow-up.* "What evidence would make you reject the simplified model?"\
*Answer pivot.* "Non-Gaussian tails, unequal PAM4 eyes, strong pattern dependence, a floor unexplained by the included noise, compression, adaptation discontinuities, or disagreement that cannot be resolved through measurement uncertainty. At that point I use a waveform, statistical-eye, or measured-distribution model."

*Trap:* calculating the link budget, comparing receive power with sensitivity, and adding a standard margin.

Score each response using the shared chapter-interview rubric in Appendix A.12.1. Repeat any answer that does not define the metric and reference plane, state the model assumptions, connect the model to a measured curve, and explain what decision the result enables.


<div class="nav-links">
  <a href="ch3-intensity-modulation-direct-detection">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch5-choosing-light-sources-and-modulation">Next &rarr;</a>
</div>
