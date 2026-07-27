---
layout: default
title: "Appendix B: Thirty-second interview frameworks"
---

# Appendix B: Thirty-second interview frameworks

This appendix is the interview quick-reference. Deep technical explanations live in the body chapters and Appendix A. Each playbook uses one format: question, assumptions, 30-second answer, key concepts, common mistakes, and deep-dive reference. Memorize the callouts labeled "30-second answer." Expand only where the interview asks. Name access level (Appendix A.2) and use Appendix D.16 for claim, population, plane, and decision.

## BER increased with stable power

**Interview question.** Pre-FEC BER rose while average received power held steady. How do you debug it?

**What the interviewer is testing.** Debugging discipline: scope before components, power-versus-quality fork, and ending on a decision with recurrence control.

**Assumptions to state.** Average received-power telemetry is trusted; the issue reproduces; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm scope, time behavior, and that average-power telemetry is trusted at a named plane.

> **30-second answer (memorize).** Stable average power reduces the likelihood of gross optical-loss problems, so I move into signal quality. I first scope the population and timing behavior, then separate transmitter, channel, receiver, and DSP hypotheses using the highest-value measurement available at the lowest access level. If engineering access exists I add deeper measurements such as eyes or bias behavior. The final action depends on whether the issue requires containment, repair, supplier correction, or qualification updates.

<pre class="dectree" aria-label="Elevated BER, power stable"><code>Elevated BER, power stable
  |
Scope analysis (how large?)
  |
Sudden or gradual?
  |
Signal-quality path (black-box first)
  |
Tx quality clean?
  |-- NO --&gt; stay on Tx
  |-- YES --&gt; channel / Rx / DSP
  |
Correlation analysis (which cohort?)
  |
Decision + recurrence control</code></pre>
**Key concepts.** Stable average power deprioritizes gross insertion loss but does not eliminate fast fluctuation, intermittent contact, monitor averaging, or reflection-dependent effects. Scope sets severity first; correlation after isolation unlocks contain or lot action. A bias sweep requires engineering access and is not universally first (Appendix D.1, Appendix D.11).

**Measurements.** Power meter $\rightarrow$ power ledger intact? $\rightarrow$ optical path or SI.\
Black-box BER/FEC $\rightarrow$ quality path? $\rightarrow$ next isolate.\
External optical eye / bias (if access) $\rightarrow$ setpoint? $\rightarrow$ retune.\
Golden swap $\rightarrow$ Tx or Rx? $\rightarrow$ owner.\
BER waterfall $\rightarrow$ shift or floor? $\rightarrow$ sensitivity vs noise.

**Typical follow-ups.**

- Why measure power before the DCA?

- Why not start with RIN?

- What if cool-down recovers the BER?

**Common mistakes.**

- "The receiver is bad because optical power is fine." Power does not represent noise, timing, distortion, or control behavior.

- Naming the laser first.

- Calling "bad eye" a confirmed mechanism.

- Listing instruments without a decision or recurrence control.

**Thirty-second close.** Average power is stable, so I deprioritize gross loss, scope the population, chase signal quality on the black-box surface first, isolate Tx / channel / Rx / DSP, then close with the control that catches the next escape.

**Deep dive.** Full prose: Appendix A.10.7, §11.2. Ledgers: Appendix A.8.4. Pattern: Appendix A.1.

## Received power decreased

**Interview question.** Received optical power dropped and the link is failing. How do you debug it?

**What the interviewer is testing.** Power-ledger triage: external reference planes, monitor honesty, and population-driven containment.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm the power drop with an external meter at a named plane before trusting module monitors.

> **30-second answer (memorize).** Power moved, so stay on the power ledger. First scope the failure. Confirm with an external meter at a named plane, then bisect source enable, coupling, connectors, MUX loss, and monitor-PD / APC honesty. Therefore I would contain if lot-correlated, clean or replace the plant if local, and update ATP or hygiene rules so it does not recur.

<pre class="dectree" aria-label="Power down"><code>Power down
  |
Scope
  |
External meter @ named plane
  |
Monitor vs external agree?
  |-- NO --&gt; APC / monitor-PD / cal
  |-- YES --&gt; source / coupling / connector / MUX
  |
Population?
  |-- lot/vendor --&gt; contain + FA
  |-- single --&gt; plant or unit repair
  |
Decision + control</code></pre>
**Key concepts.** A power drop is not automatically a dying laser. Monitor corruption and dirty plant fake laser failure. The external meter is the cut that protects you from trusting a lying APC loop.

**Measurements.** External power meter $\rightarrow$ true power? $\rightarrow$ optical path.\
Inspect / ORL $\rightarrow$ plant dirty or reflective? $\rightarrow$ clean / replace.\
LIV $\rightarrow$ device changed? $\rightarrow$ replace vs setpoint.\
Lot query $\rightarrow$ population? $\rightarrow$ contain vs unit fix.

**Typical follow-ups.**

- Why not trust the module's reported Tx power?

- When do you stop ship versus clean the connector?

**Common mistakes.**

- Trusting monitor-PD without an external meter.

- Treating one dirty connector as a fleet laser problem.

**Thirty-second close.** I confirm power at a named plane with an external meter, bisect the optical path, contain if lot-correlated, and update the screen that missed it.

**Deep dive.** Power fork and instruments: Appendix A.8.3. APC and calibration: §5.11.

## One weak lane

**Interview question.** A single lane in a four-lane transceiver has elevated BER while received power on that lane looks normal. How would you isolate it?

**What the interviewer is testing.** Lane isolation: sibling comparison, optical-versus-electrical bisect, and lot versus unit ownership.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm whether one lane is an outlier versus a multi-lane gradient or pattern.

> **30-second answer (memorize).** First scope: one lane, one unit, or a pattern across the lot? Compare sibling lanes, then optical-versus-electrical swap to split path from driver or TIA. Therefore I would fix assembly or the array element that owns the fault, and add the screen that would have caught it.

<pre class="dectree" aria-label="One weak lane"><code>One weak lane
  |
Siblings OK?
  |-- NO --&gt; shared supply / thermal / host
  |-- YES --&gt; lane-local
        |
   Opt vs elec swap
        |-- optical --&gt; FAU / coupling / PIC lane
        |-- electrical --&gt; driver / TIA / SerDes
        |
   Lot pattern?
        |
   Decision: rework / screen / supplier</code></pre>
**Key concepts.** Sibling comparison is the cheapest population cut inside one module. Optical-versus-electrical swap prevents weeks of laser FA on a TIA lane (Appendix A.10.6).

**Measurements.** Sibling BER/power $\rightarrow$ shared or local? $\rightarrow$ scope.\
Lane swap $\rightarrow$ optical or electrical? $\rightarrow$ owner.\
LIV on weak lane $\rightarrow$ device or coupling? $\rightarrow$ FAU vs die.

**Typical follow-ups.**

- Why compare siblings before opening the module?

- What lot pattern would make you call the supplier today?

**Common mistakes.**

- Rewriting the module spec for one assembly escape.

- Skipping the electrical path when power looks fine.

**Thirty-second close.** I compare siblings, swap optical versus electrical, then own the assembly or array element and the ATP row that would have caught it.

**Deep dive.** Worked answer: Appendix A.10.6. FAU and parallel optics appear throughout Chapter 11.

## High-temperature failures

**Interview question.** BER worsens at high temperature but average power is stable. What do you do?

**What the interviewer is testing.** Corner debugging: measure where it fails, separate reversible control/calibration from permanent damage.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm scope and whether cool-down recovers before blaming the laser.

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure and whether cool-down recovers. At the failing temperature, read externally visible remaining margin: BER/FEC, telemetry, retrains, and control headroom. With engineering access, add bias sweep, OSA, and external optical eye. Therefore I would fix the table or thermal design and put that loaded corner in the ATP.

<pre class="dectree" aria-label="Hot BER, power stable"><code>Hot BER, power stable
  |
Scope + cool-down recovers?
  |-- YES --&gt; operating point / table / control
  |-- NO  --&gt; aging / permanent damage
  |
At failing T: black-box margin first
  |-- access --&gt; external eye / bias / OSA
  |
Control ledger exhausted?
  |-- YES --&gt; thermal design / tuning range
  |-- NO  --&gt; cal table / wavelength / Rx
  |
Decision: retune + ATP corner</code></pre>
**Key concepts.** Temperature failures are often control or calibration, not a dead laser. The decision uses externally visible remaining margin; internal physics is optional (Appendix A.10.3, Appendix D.11).

**Measurements.** Cool-down test $\rightarrow$ reversible? $\rightarrow$ thermal vs aging.\
Black-box BER/FEC at hot $\rightarrow$ remaining margin? $\rightarrow$ gate.\
Bias sweep at hot (if access) $\rightarrow$ optimum moved? $\rightarrow$ table.\
Actuator codes $\rightarrow$ control authority left? $\rightarrow$ thermal design.\
OSA $\rightarrow$ spectral alignment? $\rightarrow$ lock / filter.

**Typical follow-ups.**

- Why insist on measuring at the failing temperature?

- How do you say "TEC maxed" in product language?

**Common mistakes.**

- Debugging only at ambient.

- Saying TEC current hit max instead of control ledger exhausted.

**Thirty-second close.** I measure externally visible remaining margin at the failing temperature, ask whether cool-down recovers, fix table or thermal design, and put that loaded corner in ATP.

**Deep dive.** Appendix A.10.3, §11.12. Control ledger: Appendix A.8.4.

## Laser aging versus calibration drift

**Interview question.** How do you distinguish laser aging from calibration drift?

**What the interviewer is testing.** Mechanism separation with external references and reversibility, not telemetry narrative alone.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm whether recalibration recovers the symptom (black-box) before opening LIV.

> **30-second answer (memorize).** Physical aging often changes a baseline: LIV, power, spectrum, RIN, sensitivity, or drive. Calibration drift changes the operating point while the device remains substantially healthy. Start black-box: BER/FEC, telemetry, and whether recalibration recovers. Recalibration recovery updates probability; it is not proof. With engineering access, compare external LIV and other physical baselines to ship data. Therefore I would route aging to life/derate/replace and drift to table control plus an ATP loaded-corner check.

<pre class="dectree" aria-label="Symptom (bias up / BER up)"><code>Symptom (bias up / BER up)
  |
Black-box telemetry first
  |
Degraded?
  |
Recal recovers?
  |-- YES --&gt; raise P(calibration drift); not proof
  |-- NO  --&gt; raise P(physical aging / damage)
  |
Need mechanism split?
  |-- YES --&gt; engineering access / external baselines
  |
Physical baselines vs ship data
  |-- moved --&gt; aging --&gt; life / derate / replace
  |-- OK ----&gt; deeper FA or table owner</code></pre>
**Key concepts.** Telemetry can look identical for aging and drift. Recalibration recovery updates belief; external baselines confirm the owner (Appendix A.10.4, Appendix D.11).

**Measurements.** Recal trial $\rightarrow$ recovers? $\rightarrow$ updates P(drift).\
External LIV / power / spectrum (if access) $\rightarrow$ baseline moved?\
Monitor vs meter $\rightarrow$ APC honesty? $\rightarrow$ monitor-PD.\
Stress-hours plot $\rightarrow$ monotonic or step? $\rightarrow$ confirms.

**Typical follow-ups.**

- What is the silent failure mode if the monitor lies?

- Who owns aging versus who owns the table?

**Common mistakes.**

- Treating recalibration recovery as proof of healthy silicon.

- Sending a table bug to the reliability team.

**Thirty-second close.** I start black-box, treat recal recovery as evidence not proof, then compare physical baselines when access exists; aging goes to life actions and drift to table control plus a loaded-corner screen.

**Deep dive.** Appendix A.10.4, §5.11, §5.10.

## Second component source

**Interview question.** How would you qualify a second laser, photodiode, driver, TIA, or PIC supplier?

**What the interviewer is testing.** Component-boundary judgment: requirements at the component interface, wafer/lot distributions, integration compatibility, process-specific reliability, supplier ATP correlation, and module-level confirmation.

**Assumptions to state.** The component boundary and ownership are defined; module confirmation is still required before open volume; engineering access to source samples may be available.

**First thing I would check.** Freeze the component-boundary requirements slice, not the incumbent datasheet.

> **30-second answer (memorize).** Freeze requirements at the component boundary, not the incumbent datasheet. Characterize multi-lot distributions for LIV, SMSR, RIN, wavelength, and process corners. Demonstrate integration compatibility in the host module, run mechanism-appropriate reliability, correlate supplier ATP to your proxy, then confirm on module samples. Therefore I would gate open volume on FAIR, ATP correlation, and split RMA codes, not on a hero die.

<pre class="dectree" aria-label="Second component source"><code>Second component source
  |
Component requirements freeze
  |
Multi-lot distributions
  |
Integration in host module
  |
Mechanism-appropriate reliability
  |
Supplier ATP correlation
  |
Module confirmation + split RMA</code></pre>
**Key concepts.** Component and complete-product second sources have different access, interop burden, and owners (Appendix D.8, §9.2, Appendix D.16).

**Measurements.** Wafer/lot distributions $\rightarrow$ process spread? $\rightarrow$ risk.\
Module confirmation $\rightarrow$ integration OK? $\rightarrow$ continue.\
Supplier ATP vs your proxy $\rightarrow$ escape risk? $\rightarrow$ ship gate.

**Typical follow-ups.**

- What is measured at the component boundary versus the module connector?

- What changes if the second source is only a laser die?

**Common mistakes.**

- Treating a hero sample as a distribution.

- Skipping module confirmation after die-level pass.

**Thirty-second close.** I qualify at the component boundary with multi-lot distributions, then confirm in-module with FAIR, ATP correlation, and split RMA.

**Deep dive.** Appendix A.10.5, §9.2.

## Second module or cable source

**Interview question.** How would you qualify a second transceiver, AOC, or cable-assembly supplier?

**What the interviewer is testing.** Complete-product second source: black-box nominal behavior, margin, host/peer interop, environmental and reliability evidence, manufacturing readiness, controlled pilot, and fleet RMA separation.

**Assumptions to state.** The product is bookended unless engineering samples are contracted; customer-visible metrics dominate; open volume waits on pilot exit.

**First thing I would check.** Define what equivalence means for the customer-visible product before measuring a golden sample.

> **30-second answer (memorize).** Freeze the customer-visible requirements slice. Walk architecture feasibility, bring-up, characterization, margin, interoperability, reliability qualification, manufacturing validation, controlled pilot, mass production readiness, then fleet monitoring with feedback. Request engineering access only when black-box evidence is insufficient. Therefore I would gate open volume on FAIR, ATP correlation, pilot exit, and split RMA codes.

<pre class="dectree" aria-label="Second module / cable source"><code>Second module / cable source
  |
Requirements freeze
  |
Bring-up + nominal + margin
  |
Interop + env/reliability
  |
Manufacturing + ATP readiness
  |
Controlled pilot
  |
Fleet monitoring + split RMA</code></pre>
**Key concepts.** Module second-source burden is interop and black-box margin across the envelope, not die physics first (Appendix D.11, Appendix A.8.5).

**Measurements.** Multi-lot black-box margin $\rightarrow$ process spread? $\rightarrow$ risk.\
Host/peer matrix $\rightarrow$ interop cliffs? $\rightarrow$ restrict.\
Pilot cohort $\rightarrow$ assumptions hold? $\rightarrow$ open MP.

**Typical follow-ups.**

- Why not clone the incumbent datasheet?

- What changes between a pluggable and an AOC second source?

**Common mistakes.**

- Qualifying a hero module.

- Merging supplier RMA codes.

**Thirty-second close.** I walk the product lifecycle on the customer-visible surface, then gate volume on FAIR, ATP correlation, pilot exit, and split RMA.

**Deep dive.** Appendix A.10.5, §9.2.

## Product-readiness plan for a new transceiver

**Interview question.** How would you establish readiness for a new optical transmitter from bring-up through production?

**What the interviewer is testing.** Product-readiness judgment: sequencing, ownership, stage gates, dependencies, exit criteria, schedule and resource judgment.

**Assumptions to state.** Requirements and owners exist; stage exits are binary enough to fail; engineering access is requested only when a gate cannot decide.

**First thing I would check.** Freeze the requirements slice and named risks before listing instruments.

> **30-second answer (memorize).** I start by defining the system requirements and failure risks. Then I build the product-readiness plan around reducing uncertainty: architecture demonstrates the budgets can close, bring-up demonstrates basic operation, characterization builds the behavioral model, requirement verification and system validation close specs and intended use, reliability qualification demonstrates life and environmental confidence, manufacturing validation demonstrates repeatability, and controlled deployment plus telemetry confirms field assumptions. Every stage has an exit criterion tied to a decision.

<pre class="dectree" aria-label="Requirements definition"><code>Requirements definition
  |
Architecture review
  |
Bring-up -&gt; Characterization
  |
Verify requirements -&gt; Validate system use
  |
Reliability qualification
  |
Manufacturing validation
  |
Controlled pilot -&gt; Mass production
  |
Fleet monitoring -&gt; Feedback</code></pre>
**Key concepts.** This answer is about program sequencing and ownership. Qualification *evidence* construction lives in Appendix C.15, Appendix D.3. The product-readiness stages are the gates (Appendix A.8.5, Appendix D.2).

**Measurements.** Each readiness stage $\rightarrow$ named uncertainty removed $\rightarrow$ continue / redesign / tighten ATP / stop ship.\
Margin sweeps $\rightarrow$ which ledger dies first? $\rightarrow$ telemetry alarms.

**Typical follow-ups.**

- Which stage removes combination risk?

- How does margin budgeting change what you instrument in the fleet?

**Common mistakes.**

- Treating bring-up as population proof.

- Running HTOL without a named mechanism.

**Thirty-second close.** I walk the ladder as staged uncertainty reduction and refuse any measurement that answers no new question about remaining margin.

**Deep dive.** Appendix A.10.2, Table 7.3, Appendix A.8.7.

## Fleet issue

**Interview question.** Field telemetry shows rising pre-FEC BER on a subset of racks. How do you triage?

**What the interviewer is testing.** Fleet ownership: scope, trend, bucket, and contain-versus-monitor under incomplete evidence.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Scope population and trend (unit / lot / vendor / rack / fleet) before pulling hardware.

> **30-second answer (memorize).** First scope: unit, lot, vendor, rack, datacenter, or fleet? Ask trend and change history. Classify performance versus reliability versus manufacturability before pulling hardware. Therefore I would contain if growing and supplier-specific, or monitor-only if tiny, flat, and no customer impact, with an owner on the next control.

> **Engineering heuristic.** Contain a growing lot-scoped escape before you finish the physics story. The next day of ship can cost more than the next day of FA.

<pre class="dectree" aria-label="Fleet symptom"><code>Fleet symptom
  |
Scope ladder
  |
Rate / trend / customer impact
  |-- tiny, flat, no impact --&gt; monitor only
  |-- growing / supplier --&gt; contain now
  |
Bucket: performance / reliability / manufacturability
  |
Decision + owner + telemetry control</code></pre>
**Key concepts.** Fleet economics and scope pick the owner before FA. Pulling units without a bucket wastes the only failing state you had (Appendix A.6, §11.16).

**Measurements.** Telemetry query $\rightarrow$ scope and trend? $\rightarrow$ contain vs monitor.\
Lot/date correlation $\rightarrow$ manufacturability? $\rightarrow$ supplier.\
Golden host in rack $\rightarrow$ environment vs module? $\rightarrow$ owner.

**Typical follow-ups.**

- When is monitor-only the correct Staff answer?

- What do you do before the mechanism is known?

**Common mistakes.**

- Treating one rack as the fleet.

- Waiting for DPA before containing a growing lot.

**Thirty-second close.** I scope first, pick the bucket, contain if growing and supplier-specific, and name the owner of the next control.

**Deep dive.** Appendix A.6, Table 11.2.

## Supplier escape

**Interview question.** A new date code from Supplier B fails the hot corner at about 3%. What do you do?

**What the interviewer is testing.** Staff judgment under uncertainty: contain today, keep FA open, own recurrence control.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Provisionally contain the growing population, then refine scope.

> **30-second answer (memorize).** Contain first, then own the loop. Stop shipment of Supplier B affected lots, scope the deployed population, compare failing versus healthy units, open joint FA with the supplier, drive corrective action, expand ATP or process control, verify the next lot, and keep fleet monitoring. The customer keeps ownership of evidence quality and the ship decision. Therefore I would contain today rather than wait for SEM before acting.

<pre class="dectree" aria-label="Escape detected"><code>Escape detected
  |
Contain lot / pause deploy
  |
Scope deployed population
  |
Compare failing vs healthy
  |
Joint FA with supplier
  |
Corrective action
  |
ATP / process-control update
  |
Verify next lot
  |
Fleet monitoring (customer owns ship gate)</code></pre>
**Key concepts.** Containment, suspected mechanism, confirmed mechanism class, and recurrence control are separate steps. The system owner keeps responsibility for evidence quality and verifying the fix (Appendix D.9, Appendix A.6).

**Measurements.** Lot genealogy $\rightarrow$ exposure? $\rightarrow$ quarantine list.\
ATP hot corner $\rightarrow$ escape path? $\rightarrow$ production gate.\
DPA sample $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- Why contain before FA completes?

- What residual risk do you name to leadership?

**Common mistakes.**

- Waiting for a confirmed mechanism before stop-ship.

- Blocking all vendors for one supplier's lot.

**Thirty-second close.** I contain Supplier B today, scope exposure, open joint FA, expand ATP, verify the next lot, keep fleet monitoring, and keep ownership of the ship gate.

**Deep dive.** Appendix A.6, Table A.1.

## BER floor

**Interview question.** Why can a link show a BER floor that more launch power does not fix?

**What the interviewer is testing.** Separating waterfall shift from floor, then choosing measurements for the leading non-power-limited impairment.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Confirm floor versus waterfall shift with a VOA sweep at a named plane.

> **30-second answer (memorize).** A floor means additional received power no longer removes the dominant impairment. Confirm floor versus shift on a waterfall, then test for signal-dependent noise, reflections or MPI, pattern dependence, crosstalk, timing or CDR limits, and DSP or equalization limits. Therefore I would fix the limiting mechanism rather than raise OMA.

<pre class="dectree" aria-label="BER stops improving with power"><code>BER stops improving with power
  |
Power no longer limiting
  |
Test for:
  |-- signal-dependent noise (RIN)
  |-- reflections / MPI
  |-- deterministic / pattern distortion
  |-- crosstalk / timing / CDR / DSP-EQ
  |
Choose measurement from leading hypothesis
  |
Fix mechanism, not launch</code></pre>
**Key concepts.** A floor is a diagnostic pattern, not a single mechanism. The waterfall shape is the fast cut between sensitivity shift and a non-power-limited impairment (Appendix A.10.8, Appendix A.8.9).

**Measurements.** Waterfall $\rightarrow$ shift or floor? $\rightarrow$ next hunt.\
Controlled ORL $\rightarrow$ reflection-driven path? $\rightarrow$ plant.\
Supply noise / FEC histogram $\rightarrow$ PSRR or burst? $\rightarrow$ owner.

**Typical follow-ups.**

- Why not increase OMA alone?

- How do FEC histograms look for MPI bursts?

**Common mistakes.**

- Raising launch into a floor.

- Equating every floor with RIN before bisecting.

**Thirty-second close.** I confirm floor versus shift on a waterfall, then remove the non-power-limited impairment rather than raise launch power.

**Deep dive.** Appendix A.10.8, §11.2.1, §4.3.

## Intermittent failures

**Interview question.** The link fails intermittently and often passes when retested. How do you proceed?

**What the interviewer is testing.** Evidence preservation, reproduction strategy, and refusing premature NFF closure.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** Preserve the failing state and telemetry before reseat, clean, or reboot.

> **30-second answer (memorize).** Preserve the failing state and telemetry before you reseat, clean, or reboot. Scope time and change: dwell, temperature, vibration, firmware, connector. Prefer burst/FEC histograms and long dwell over a single golden retest. Therefore I would contain if lot-correlated, tighten dwell/ATP if escape, and refuse to close an NFF without a reproduction plan.

<pre class="dectree" aria-label="Intermittent"><code>Intermittent
  |
Preserve state / telemetry
  |
Triggers: T, time, mate, vibration, FW
  |
Reproduce with dwell / stress
  |
Scope population
  |
Decision: contain / ATP dwell / monitor</code></pre>
**Key concepts.** Intermittents die when the evidence is destroyed. NFF is often a triage failure, not a healthy part (§11.16).

**Measurements.** FEC histogram $\rightarrow$ burst vs Gaussian? $\rightarrow$ MPI / intermittent.\
Time sync + event capture $\rightarrow$ state preserved? $\rightarrow$ FA.\
Fixture / firmware identity $\rightarrow$ shared cause? $\rightarrow$ scope.\
Dwell BER $\rightarrow$ reproduces? $\rightarrow$ control choice.\
Mate/demate $\rightarrow$ connector? $\rightarrow$ hygiene / replace.

**Typical follow-ups.**

- What do you refuse to do on first touch?

- How does high NFF change your answer?

**Common mistakes.**

- Reseating before capture.

- Closing NFF without a reproduction plan.

**Thirty-second close.** I preserve state before reseating, reproduce with dwell, and refuse NFF without a reproduction and control plan.

**Deep dive.** §11.16, Table 11.1.

## Production recurrence-control update

**Interview question.** A failure escaped to the field that production controls did not catch. How do you update recurrence control?

**What the interviewer is testing.** Choosing among ATP, sampling, SPC, supplier process, design, firmware, and telemetry controls; not assuming a new 100% screen.

**Assumptions to state.** The escape path can be named; a failing unit or equivalent can be replayed; measurement capability is known.

**First thing I would check.** Name the escape path and the measurement that would have caught it.

> **30-second answer (memorize).** Name the escape path and the measurement that would have caught it at a named plane and corner. Choose the most economical control: new ATP item, tighter limit, sampled audit, SPC variable, supplier process correction, design or firmware guard, or telemetry alarm. Only select a 100% screen when separation, cycle time, measurement capability, and cost justify it. Therefore I would ship the chosen control with an owner and a metric.

<pre class="dectree" aria-label="Escape"><code>Escape
  |
Which uncertainty ATP missed?
  |
New measurement / corner / limit
  |
Guard band from repeatability
  |
Station correlation
  |
Reaction plan + owner
  |
Ship ATP change</code></pre>
**Key concepts.** Recurrence control is not always an ATP change. A limit nobody can trace gets waived under ship pressure (Appendix A.10.2, Appendix D.9).

**Measurements.** Escape unit replay $\rightarrow$ missed corner? $\rightarrow$ new test.\
Gage R&R $\rightarrow$ repeatability? $\rightarrow$ guard band.\
Golden units across stations $\rightarrow$ correlation? $\rightarrow$ ship.

**Typical follow-ups.**

- How do you set the guard band?

- What is the reaction plan when the new limit fails?

**Common mistakes.**

- Adding a test with no reaction plan.

- Limits from one hero unit.

**Thirty-second close.** I name the missed uncertainty, choose ATP / sample / SPC / supplier / design / firmware / telemetry, demonstrate separation, and ship the control with an owner.

**Deep dive.** Production readiness stage in Appendix A.8.5.

## Telemetry design

**Interview question.** What would you put in fleet telemetry, and why?

**What the interviewer is testing.** Instrumenting ledgers that unlock triage decisions, not logging every register.

**Assumptions to state.** Schema and firmware versions are known; retention and owners exist; missing-data behavior is defined; alarms have a decision owner.

**First thing I would check.** Name the decision each telemetry field must unlock before adding registers.

> **30-second answer (memorize).** Log what discriminates hypotheses: per-lane power, bias, pre-FEC BER and FEC histograms; module temperature and actuator drive; LOS/LOL with context. Require timestamp accuracy, sampling cadence, aggregation window, units, calibration/scaling, missing-data behavior, firmware/schema version, serial/lot/platform, event trigger, retention, and a decision owner. Alarm on trends and disagreements, not only hard thresholds. Therefore I would instrument the ledgers margin testing said die first.

Add a register only if it changes contain, derate, RMA, or FA ownership. Full tradeoff: §11.16.

<pre class="dectree" aria-label="Telemetry purpose: early margin erosion"><code>Telemetry purpose: early margin erosion
  |
Per-lane: power, bias, pre-FEC BER
  |
Module: T, TEC/heater, rails, lock
  |
Events + lot/age/rack context
  |
Alarms: trends / disagreements</code></pre>
**Key concepts.** Telemetry exists to triage without pulling hardware and to catch dying units before dead ones (Appendix A.10.13).

**Measurements.** Bias at constant power $\rightarrow$ aging? $\rightarrow$ reliability bucket.\
Power at constant bias $\rightarrow$ optical path? $\rightarrow$ plant.\
Actuator near rail $\rightarrow$ control margin? $\rightarrow$ thermal design.

**Typical follow-ups.**

- Why alarm on actuator headroom?

- What context fields make lot queries possible?

**Common mistakes.**

- Logging every register with no hypothesis.

- Hard thresholds only, no trends.

**Thirty-second close.** I instrument the ledgers that discriminate hypotheses and alarm on trends and disagreements that unlock triage.

**Deep dive.** Appendix A.10.13, Appendix E.7.

## Qualification planning

**Interview question.** How do you plan qualification for a new IM/DD module?

**What the interviewer is testing.** Qualification-evidence judgment: mechanism coverage, stress selection, sample strategy, acceptance criteria, confidence, production correlation, release evidence. This playbook is a scoped evidence path, not a second full lifecycle; use Appendix C.8, Appendix D.2 for the stage order.

**Assumptions to state.** Requirements name mechanisms; sample strategy and confidence are stated; production proxies are cheaper than full GR-468 replay; release is a ship / restrict / reject decision.

**First thing I would check.** Freeze the requirements slice and named mechanisms before listing stresses.

> **30-second answer (memorize).** I qualify from requirements to mechanisms, not from a ritual list. What does the system require? What can fail? How do we accelerate those mechanisms? What observable changes? What defines pass/fail? How much evidence is enough? How does production control maintain quality? Therefore I would gate ship on remaining margin after named stresses with a stated sample strategy and confidence, plus a production proxy (Appendix D.3, Appendix F.4).

<pre class="dectree" aria-label="Qualification interview framework"><code>Qualification interview framework
  |
Requirements: what does the system require?
  |
Failure mechanisms: what can fail?
  |
Acceleration: how do we stress those mechanisms?
  |
Measurement: what observable changes?
  |
Acceptance: what defines pass/fail?
  |
Confidence: how much evidence is enough?
  |
Production control: how do we maintain quality?</code></pre>
**Key concepts.** This is a scoped evidence path inside the lifecycle, not a second lifecycle (Appendix C.8, Appendix D.2). Stress consumes margin; qual measures what remains (Appendix A.8.6, Appendix A.8.7). Sample strategy depends on failure-rate target, confidence, cost, and population variation, not a fixed "we test 20 units."

**Measurements.** Margin sweeps $\rightarrow$ cliff distance? $\rightarrow$ derate or redesign.\
HTOL $\rightarrow$ wear-out hypothesis? $\rightarrow$ FIT.\
ATP correlation $\rightarrow$ factory control? $\rightarrow$ volume.

**Typical follow-ups.**

- What does "remaining margin" mean in one sentence?

- When do you ask for Tx-only or Rx-only samples?

**Common mistakes.**

- HTOL without mechanism or $E_a$.

- Qualifying internals the customer never observes.

**Thirty-second close.** I budget which stresses spend which ledgers, run HTOL only with a named mechanism, and gate ship on remaining margin.

**Deep dive.** Appendix A.8.5, Appendix F.1.1, §5.13.

## Unknown failure

**Interview question.** You must make a ship decision this week, but the physical mechanism is still unknown. What do you do?

**What the interviewer is testing.** Deciding with today's evidence: contain, owner, control, and residual risk before mechanism certainty.

**Assumptions to state.** The failure reproduces; telemetry is calibrated unless challenged; the product is bookended; engineering access is unavailable unless requested.

**First thing I would check.** State evidence, scope, and residual risk before waiting for a physical mechanism.

> **30-second answer (memorize).** State evidence, confidence weights, and residual risk. Decide with today's evidence: contain the scoped population, keep a healthy path shipping, open FA, and add the ATP or telemetry control that would catch the next escape. Therefore I would not wait for certainty before ownership actions.

<pre class="dectree" aria-label="Unknown mechanism"><code>Unknown mechanism
  |
Evidence + scope + rate/trend
  |
Priors: common modes first
  |
Decision today (contain / ship / derate)
  |
FA path + control + owner
  |
Update when mechanism closes</code></pre>
**Key concepts.** The job is the best decision with today's evidence. Unknown mechanism is Framework 15 of Staff judgment, not a reason to freeze (Appendix A.6).

**Measurements.** Whatever removes the most uncertainty per hour toward the ship decision: scope query, golden swap, external power, hot-corner ATP sample.\
DPA later $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- What do you tell leadership about residual risk?

- Which measurement is worth delaying the decision for?

**Common mistakes.**

- Freezing all action until SEM.

- Making a ship call with no control and no owner.

**Thirty-second close.** I decide with today's evidence, contain the scoped population, keep a healthy path shipping, and name the control and residual risk.

**Deep dive.** Appendix A.6, Appendix A.4, Table A.1.

## Tradeoff interview questions

Staff follow-ups often stop asking "what test?" and start asking "given constraints, what do you choose?" Answer each with benefit, downside, and decision criteria. Point at the matching tradeoff homes; do not invent a new framework.

##### Would you choose more margin or lower power?

*Benefit of margin:* reach, temperature, aging, contamination tolerance.\
*Downside:* laser power, heat, efficiency, sometimes lifetime.\
*Criteria:* allocate margin where uncertainty is highest; do not maximize every ledger (§5.19, Chapter 7).

##### Would you add more telemetry?

*Benefit:* faster fleet triage and earlier margin erosion detection.\
*Downside:* firmware, storage, alarm fatigue.\
*Criteria:* each field needs a decision owner and a reaction plan (Appendix C.14, §11.16).

##### Would you run more qualification?

*Benefit:* confidence and fewer late escapes.\
*Downside:* schedule, cost, delayed learning.\
*Criteria:* prioritize by risk $\times$ uncertainty $\times$ impact; stop when remaining risk has a production control (§8.4).

##### Would you add a second supplier?

*Benefit:* supply resilience and pricing leverage.\
*Downside:* validation, interop, and manufacturing differences.\
*Criteria:* qualify on concentration risk and evidence, not ideology (§9.2, Appendix C.7).

##### Would you increase ATP coverage?

*Benefit:* escape detection earlier in the flow.\
*Downside:* cycle time, cost, false rejects.\
*Criteria:* cheapest control that reliably detects the named mechanism: 100%, sample, SPC, or supplier process (§9.5).

**Key idea.** Open the matching framework, deliver the thirty-second box, walk the tree, end on the decision and the control. When the interviewer asks a tradeoff question, name benefit, downside, and criteria. Philosophy is in Appendix A; this appendix is how you speak it under pressure.


<div class="nav-links">
  <a href="ch13-engineering-case-studies">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch15-engineering-decision-trees">Next &rarr;</a>
</div>
