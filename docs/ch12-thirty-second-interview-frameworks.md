---
layout: default
title: "Appendix B: Thirty-second interview frameworks"
---

# Appendix B: Thirty-second interview frameworks

This appendix is the operating manual for answering under time pressure. The philosophy lives in Appendix A; wall-chart trees live in Appendix C. Each playbook is a reusable template: question, what is tested, thirty-second answer, decision tree, measurements, traps, and thirty-second close. Memorize the green boxes. Expand only where the interview asks.

## BER increased with stable power

**Interview question.** Pre-FEC BER rose while average received power held steady. How do you debug it?

**What the interviewer is testing.** Debugging discipline: scope before components, power-versus-quality fork, and ending on a decision with recurrence control.

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure (unit $\rightarrow$ lot $\rightarrow$ vendor $\rightarrow$ fleet). On the black-box surface, chase BER/FEC, sensitivity, injected loss, telemetry, and retrains. With engineering access, add Tx-only/Rx-only, breakout, PRBS, loopback, and external optical eye. Therefore I would isolate with a golden swap and a bias sweep, then decide contain, retune, or ATP change.

<pre class="dectree" aria-label="Decision tree"><code>Elevated BER, power stable
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
**Engineering reasoning.** Stable power rules out average launch and connector loss as the primary cause. Scope sets severity first; correlation after isolation unlocks contain or lot action. Optical eye is external unless an internal eye-monitor is named (Appendix C.4, Appendix A.6.3, Appendix C.10).

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

- Naming the laser first.

- Calling "bad eye" a root cause.

- Listing instruments without a decision.

- Stopping before recurrence control.

**Thirty-second close.** Power held, so I leave the power ledger, scope the population, chase signal quality on the black-box surface first, isolate Tx versus Rx, then close with the control that catches the next escape.

**Deep dive.** Full prose: Appendix A.8.7, §10.2. Ledgers: Appendix A.6.4.

## Received power decreased

**Interview question.** Received optical power dropped and the link is failing. How do you debug it?

**What the interviewer is testing.** Power-ledger triage: external reference planes, monitor honesty, and population-driven containment.

> **30-second answer (memorize).** Power moved, so stay on the power ledger. First scope the failure. Confirm with an external meter at a named plane, then bisect source enable, coupling, connectors, MUX loss, and monitor-PD / APC honesty. Therefore I would contain if lot-correlated, clean or replace the plant if local, and update ATP or hygiene rules so it does not recur.

<pre class="dectree" aria-label="Decision tree"><code>Power down
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
**Engineering reasoning.** A power drop is not automatically a dying laser. Monitor corruption and dirty plant fake laser failure. The external meter is the cut that protects you from trusting a lying APC loop.

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

**Deep dive.** Power fork and instruments: Appendix A.6.3. APC and calibration: §5.11.

## One weak lane

**Interview question.** A single lane in a four-lane transceiver has elevated BER while received power on that lane looks normal. How would you isolate it?

**What the interviewer is testing.** Lane isolation: sibling comparison, optical-versus-electrical bisect, and lot versus unit ownership.

> **30-second answer (memorize).** First scope: one lane, one unit, or a pattern across the lot? Compare sibling lanes, then optical-versus-electrical swap to split path from driver or TIA. Therefore I would fix assembly or the array element that owns the fault, and add the screen that would have caught it.

<pre class="dectree" aria-label="Decision tree"><code>One weak lane
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
**Engineering reasoning.** Sibling comparison is the cheapest population cut inside one module. Optical-versus-electrical swap prevents weeks of laser FA on a TIA lane (Appendix A.8.6).

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

**Deep dive.** Worked answer: Appendix A.8.6. FAU and parallel optics appear throughout Chapter 10.

## High-temperature failures

**Interview question.** BER worsens at high temperature but average power is stable. What do you do?

**What the interviewer is testing.** Corner debugging: measure where it fails, separate reversible control/calibration from permanent damage.

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure and whether cool-down recovers. At the failing temperature, read externally visible remaining margin: BER/FEC, telemetry, retrains, and control headroom. With engineering access, add bias sweep, OSA, and external optical eye. Therefore I would fix the table or thermal design and put that loaded corner in the ATP.

<pre class="dectree" aria-label="Decision tree"><code>Hot BER, power stable
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
**Engineering reasoning.** Temperature failures are often control or calibration, not a dead laser. The decision uses externally visible remaining margin; internal physics is optional (Appendix A.8.3, Appendix C.10).

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

**Deep dive.** Appendix A.8.3, §10.13. Control ledger: Appendix A.6.4.

## Laser aging versus calibration drift

**Interview question.** How do you distinguish laser aging from calibration drift?

**What the interviewer is testing.** Mechanism separation with external references and reversibility, not telemetry narrative alone.

> **30-second answer (memorize).** Physical aging often changes a baseline: LIV, power, spectrum, RIN, sensitivity, or drive. Calibration drift changes the operating point while the device remains substantially healthy. Start black-box: BER/FEC, telemetry, and whether recalibration recovers. Recalibration recovery updates probability; it is not proof. With engineering access, compare external LIV and other physical baselines to ship data. Therefore I would route aging to life/derate/replace and drift to table control plus an ATP loaded-corner check.

<pre class="dectree" aria-label="Decision tree"><code>Symptom (bias up / BER up)
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
**Engineering reasoning.** Telemetry can look identical for aging and drift. Recalibration recovery updates belief; external baselines confirm the owner (Appendix A.8.4, Appendix C.10).

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

**Deep dive.** Appendix A.8.4, §5.11, §5.10.

## Second-source qualification

**Interview question.** How would you qualify a second laser or PIC supplier?

**What the interviewer is testing.** Second-source judgment: customer-visible margin across the envelope, not datasheet cloning.

> **30-second answer (memorize).** Freeze the requirements slice, not the incumbent datasheet. Walk the canonical lifecycle on the customer-visible surface: bring-up, nominal and margin characterization, interoperability, environmental and reliability qualification, manufacturing and ATP readiness, controlled pilot, then fleet monitoring. Request engineering access only when black-box evidence is insufficient. Therefore I would gate open volume on FAIR, ATP correlation, and split RMA codes, not on a hero sample.

<pre class="dectree" aria-label="Decision tree"><code>Second source
  |
Requirements freeze
  |
Bring-up + nominal + margin
  |
Interop + env/reliability
  |
Manufacturing + ATP readiness
  |
Black-box enough?
  |-- YES --&gt; controlled pilot
  |-- NO  --&gt; Tx-only / Rx-only / breakout / external eye
  |
Fleet deployment + monitoring
  |
Ship / hold / reject</code></pre>
**Engineering reasoning.** The objective is acceptable system behavior and remaining margin across the deployment envelope, not nominal equivalence to the incumbent (Appendix C.10, Appendix A.8.5, Appendix A.6.5).

**Measurements.** Multi-lot black-box margin $\rightarrow$ process spread? $\rightarrow$ risk.\
HTOL $\rightarrow$ life hypothesis? $\rightarrow$ FIT / derate.\
ATP on both sources $\rightarrow$ escape risk? $\rightarrow$ ship gate.\
RMA split $\rightarrow$ field falsifies qual? $\rightarrow$ reopen.

**Typical follow-ups.**

- Why not just match the incumbent datasheet?

- What customer measurements matter if the part is a black box?

**Common mistakes.**

- Qualifying a hero sample.

- Merging supplier RMA codes.

**Thirty-second close.** I walk the canonical lifecycle on the customer-visible surface, request engineering access only when needed, then gate volume on FAIR, ATP correlation, controlled pilot, and split RMA.

**Deep dive.** Appendix A.8.5, §8.10.

## Validation plan for a new transceiver

**Interview question.** How would you validate a new optical transmitter from bring-up through production?

**What the interviewer is testing.** Staged uncertainty reduction and margin budgeting from bring-up through fleet.

> **30-second answer (memorize).** Validation is staged uncertainty reduction. Walk requirements, bring-up, nominal characterization, margin characterization, interop, environmental and reliability qualification, manufacturing and ATP readiness, controlled pilot, then fleet monitoring. Each stage answers a question the previous could not. Therefore I would refuse any test that answers no new question and watch the ledgers margin budgeting says will be spent first.

<pre class="dectree" aria-label="Decision tree"><code>Requirements
  |
Bring-up -&gt; Nominal characterization
  |
Margin characterization -&gt; Interoperability
  |
Env + reliability qual
  |
Manufacturing / ATP -&gt; Controlled pilot
  |
Fleet monitoring
  |
Ship / restrict / reject</code></pre>
**Engineering reasoning.** The ladder is the canonical qualification tree. Margin budgeting says stresses consume margin; stages exist to measure remaining margin from the customer-visible surface first (Appendix A.6.5, Appendix C.2).

**Measurements.** Each ladder stage $\rightarrow$ named uncertainty removed $\rightarrow$ continue / redesign / tighten ATP / stop ship.\
Margin sweeps $\rightarrow$ which ledger dies first? $\rightarrow$ telemetry alarms.

**Typical follow-ups.**

- Which stage removes combination risk?

- How does margin budgeting change what you instrument in the fleet?

**Common mistakes.**

- Treating bring-up as population proof.

- Running HTOL without a named mechanism.

**Thirty-second close.** I walk the ladder as staged uncertainty reduction and refuse any test that answers no new question about remaining margin.

**Deep dive.** Appendix A.8.2, Table 7.1, Appendix A.6.7.

## Fleet issue

**Interview question.** Field telemetry shows rising pre-FEC BER on a subset of racks. How do you triage?

**What the interviewer is testing.** Fleet ownership: scope, trend, bucket, and contain-versus-monitor under incomplete evidence.

> **30-second answer (memorize).** First scope: unit, lot, vendor, rack, datacenter, or fleet? Ask trend and change history. Classify performance versus reliability versus manufacturability before pulling hardware. Therefore I would contain if growing and supplier-specific, or monitor-only if tiny, flat, and no customer impact, with an owner on the next control.

<pre class="dectree" aria-label="Decision tree"><code>Fleet symptom
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
**Engineering reasoning.** Fleet economics and scope pick the owner before FA. Pulling units without a bucket wastes the only failing state you had (Appendix A.4, §7.12).

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

**Deep dive.** Appendix A.4, Table 7.6.

## Supplier escape

**Interview question.** A new date code from Supplier B fails the hot corner at about 3%. What do you do?

**What the interviewer is testing.** Staff judgment under uncertainty: contain today, keep FA open, own recurrence control.

> **30-second answer (memorize).** Contain first, then own the loop. Stop shipment of Supplier B affected lots, scope the deployed population, compare failing versus healthy units, open joint FA with the supplier, drive corrective action, expand ATP or process control, verify the next lot, and keep fleet monitoring. The customer keeps ownership of evidence quality and the ship decision. Therefore I would contain today rather than wait for SEM before acting.

<pre class="dectree" aria-label="Decision tree"><code>Escape detected
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
**Engineering reasoning.** Containment, suspected mechanism, confirmed mechanism class, and recurrence control are separate steps. The system owner keeps responsibility for evidence quality and verifying the fix (Appendix C.8, Appendix A.4).

**Measurements.** Lot genealogy $\rightarrow$ exposure? $\rightarrow$ quarantine list.\
ATP hot corner $\rightarrow$ escape path? $\rightarrow$ production gate.\
DPA sample $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- Why contain before FA completes?

- What residual risk do you name to leadership?

**Common mistakes.**

- Waiting for root cause before stop-ship.

- Blocking all vendors for one supplier's lot.

**Thirty-second close.** I contain Supplier B today, scope exposure, open joint FA, expand ATP, verify the next lot, keep fleet monitoring, and keep ownership of the ship gate.

**Deep dive.** Appendix A.4, Table A.1.

## BER floor

**Interview question.** Why can a link show a BER floor that more launch power does not fix?

**What the interviewer is testing.** Separating waterfall shift from floor, then choosing measurements for the leading non-power-limited impairment.

> **30-second answer (memorize).** A floor means additional received power no longer removes the dominant impairment. Confirm floor versus shift on a waterfall, then test for signal-dependent noise, reflections or MPI, pattern dependence, crosstalk, timing or CDR limits, and DSP or equalization limits. Therefore I would fix the limiting mechanism rather than raise OMA.

<pre class="dectree" aria-label="Decision tree"><code>BER stops improving with power
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
**Engineering reasoning.** A floor is a diagnostic pattern, not a single mechanism. The waterfall shape is the fast cut between sensitivity shift and a non-power-limited impairment (Appendix A.8.8, Appendix A.6.9).

**Measurements.** Waterfall $\rightarrow$ shift or floor? $\rightarrow$ next hunt.\
Controlled ORL $\rightarrow$ reflection-driven path? $\rightarrow$ plant.\
Supply noise / FEC histogram $\rightarrow$ PSRR or burst? $\rightarrow$ owner.

**Typical follow-ups.**

- Why not just increase OMA?

- How do FEC histograms look for MPI bursts?

**Common mistakes.**

- Raising launch into a floor.

- Equating every floor with RIN before bisecting.

**Thirty-second close.** I confirm floor versus shift on a waterfall, then remove the non-power-limited impairment rather than raise launch power.

**Deep dive.** Appendix A.8.8, §10.3, §4.3.

## Intermittent failures

**Interview question.** The link fails intermittently and often passes when retested. How do you proceed?

**What the interviewer is testing.** Evidence preservation, reproduction strategy, and refusing premature NFF closure.

> **30-second answer (memorize).** Preserve the failing state and telemetry before you reseat, clean, or reboot. Scope time and change: dwell, temperature, vibration, firmware, connector. Prefer burst/FEC histograms and long dwell over a single golden retest. Therefore I would contain if lot-correlated, tighten dwell/ATP if escape, and refuse to close an NFF without a reproduction plan.

<pre class="dectree" aria-label="Decision tree"><code>Intermittent
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
**Engineering reasoning.** Intermittents die when the evidence is destroyed. NFF is often a triage failure, not a healthy part (§7.12).

**Measurements.** FEC histogram $\rightarrow$ burst vs Gaussian? $\rightarrow$ MPI / intermittent.\
Dwell BER $\rightarrow$ reproduces? $\rightarrow$ ATP change.\
Mate/demate $\rightarrow$ connector? $\rightarrow$ hygiene / replace.

**Typical follow-ups.**

- What do you refuse to do on first touch?

- How does high NFF change your answer?

**Common mistakes.**

- Reseating before capture.

- Closing NFF without a reproduction plan.

**Thirty-second close.** I preserve state before reseating, reproduce with dwell, and refuse NFF without a reproduction and control plan.

**Deep dive.** §7.12, Table 10.1.

## Production ATP update

**Interview question.** A failure escaped to the field that ATP did not catch. How do you update production test?

**What the interviewer is testing.** Recurrence control as an ATP change with guardband, correlation, and a reaction plan.

> **30-second answer (memorize).** Name the escape path and the measurement that would have caught it at a named plane and corner. Size the new limit from characterization and repeatability, correlate stations, and set a reaction plan. Therefore I would ship the ATP change with an owner and a metric, not a hope that operators will be careful.

<pre class="dectree" aria-label="Decision tree"><code>Escape
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
**Engineering reasoning.** Recurrence control is usually an ATP or telemetry change. A limit nobody can trace gets waived under ship pressure (Appendix A.8.2).

**Measurements.** Escape unit replay $\rightarrow$ missed corner? $\rightarrow$ new test.\
Gage R&R $\rightarrow$ repeatability? $\rightarrow$ guard band.\
Golden units across stations $\rightarrow$ correlation? $\rightarrow$ ship.

**Typical follow-ups.**

- How do you set the guard band?

- What is the reaction plan when the new limit fails?

**Common mistakes.**

- Adding a test with no reaction plan.

- Limits from one hero unit.

**Thirty-second close.** I name the missed uncertainty, size the limit from repeatability, correlate stations, and ship the ATP change with an owner.

**Deep dive.** Production readiness stage in Appendix A.6.5.

## Telemetry design

**Interview question.** What would you put in fleet telemetry, and why?

**What the interviewer is testing.** Instrumenting ledgers that unlock triage decisions, not logging every register.

> **30-second answer (memorize).** Log what discriminates hypotheses: per-lane power, bias, pre-FEC BER and FEC histograms; module temperature and actuator drive; LOS/LOL and firmware with context. Alarm on trends and disagreements, not only hard thresholds. Therefore I would instrument the ledgers margin testing said die first.

<pre class="dectree" aria-label="Decision tree"><code>Telemetry purpose: early margin erosion
  |
Per-lane: power, bias, pre-FEC BER
  |
Module: T, TEC/heater, rails, lock
  |
Events + lot/age/rack context
  |
Alarms: trends / disagreements</code></pre>
**Engineering reasoning.** Telemetry exists to triage without pulling hardware and to catch dying units before dead ones (Appendix A.8.13).

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

**Deep dive.** Appendix A.8.13, §7.8.

## Qualification planning

**Interview question.** How do you plan qualification for a new IM/DD module?

**What the interviewer is testing.** Qualification as remaining-margin verification with named mechanisms and customer view.

> **30-second answer (memorize).** Start from customer-visible requirements and a margin budget: which stresses will spend which ledgers. Walk nominal function, remaining margin, environment and interop, reliability and manufacturing, ATP readiness, then a controlled pilot. Therefore I would gate ship on remaining margin after those stresses, not on a checklist of rituals.

<pre class="dectree" aria-label="Decision tree"><code>Requirements + margin budget
  |
Nominal function
  |
Remaining margin
  |
Environment + interop
  |
Reliability + manufacturing / ATP
  |
Controlled pilot
  |
Ship / restrict / reject</code></pre>
**Engineering reasoning.** Margin budgeting and customer view keep qual from becoming museum of tests. Stress consumes margin; qual measures what remains (Appendix A.6.6, Appendix A.6.7).

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

**Deep dive.** Appendix A.6.5, §8.2, §5.13.

## Unknown failure

**Interview question.** You must make a ship decision this week, but the physical mechanism is still unknown. What do you do?

**What the interviewer is testing.** Deciding with today's evidence: contain, owner, control, and residual risk before mechanism certainty.

> **30-second answer (memorize).** State evidence, confidence weights, and residual risk. Decide with today's evidence: contain the scoped population, keep a healthy path shipping, open FA, and add the ATP or telemetry control that would catch the next escape. Therefore I would not wait for certainty before ownership actions.

<pre class="dectree" aria-label="Decision tree"><code>Unknown mechanism
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
**Engineering reasoning.** The job is the best decision with today's evidence. Unknown mechanism is Framework 15 of Staff judgment, not a reason to freeze (Appendix A.4).

**Measurements.** Whatever removes the most uncertainty per hour toward the ship decision: scope query, golden swap, external power, hot-corner ATP sample.\
DPA later $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- What do you tell leadership about residual risk?

- Which measurement is worth delaying the decision for?

**Common mistakes.**

- Freezing all action until SEM.

- Making a ship call with no control and no owner.

**Thirty-second close.** I decide with today's evidence, contain the scoped population, keep a healthy path shipping, and name the control and residual risk.

**Deep dive.** Appendix A.4, Appendix A.2, Table A.1.

**Key idea.** Open the matching framework, deliver the thirty-second box, walk the tree, end on the decision and the control. Philosophy is in Appendix A; this appendix is how you speak it under pressure.


<div class="nav-links">
  <a href="ch11-one-week-optical-systems-interview-review">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch13-engineering-decision-trees">Next &rarr;</a>
</div>
