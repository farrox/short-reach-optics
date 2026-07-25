---
layout: default
title: "Ch 12: Thirty-second interview frameworks"
---

# Thirty-second interview frameworks

This appendix is the operating manual for answering under time pressure. The philosophy lives in §A; wall-chart trees live in §C. Each playbook is a reusable template: question, what is tested, thirty-second answer, decision tree, measurements, traps, and thirty-second close. Memorize the green boxes. Expand only where the interview asks.

## BER increased with stable power

**Interview question.** Pre-FEC BER rose while average received power held steady. How do you debug it?

**What the interviewer is testing.** Debugging discipline: scope before components, power-versus-quality fork, and ending on a decision with recurrence control.

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure (unit $\rightarrow$ lot $\rightarrow$ vendor $\rightarrow$ fleet). Apply the power-versus-quality fork: chase eye, bias, wavelength, noise, or receiver. Therefore I would isolate with a golden swap and a bias sweep, then decide contain, retune, or ATP change.

::: dectree
Elevated BER, power stable \| Scope analysis (how large?) \| Sudden or gradual? \| Signal-quality path \| Tx quality clean? \|-- NO --\> stay on Tx \|-- YES --\> channel / Rx / DSP \| Correlation analysis (which cohort?) \| Decision + recurrence control
:::

**Engineering reasoning.** Stable power rules out average launch and connector loss as the primary cause. Scope sets severity first; correlation after isolation unlocks contain or lot action (§C.4, §A.6.3).

**Measurements.** Power meter $\rightarrow$ power ledger intact? $\rightarrow$ optical path or SI.\
DCA / bias sweep $\rightarrow$ eye or setpoint? $\rightarrow$ retune vs device.\
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

**Thirty-second close.** Power held, so I leave the power ledger, scope the population, isolate Tx versus Rx, and close with the control that catches the next escape.

**Deep dive.** Full prose: §A.8.7, §10.2. Ledgers: §A.6.4.

## Received power decreased

**Interview question.** Received optical power dropped and the link is failing. How do you debug it?

**What the interviewer is testing.** Power-ledger triage: external reference planes, monitor honesty, and population-driven containment.

> **30-second answer (memorize).** Power moved, so stay on the power ledger. First scope the failure. Confirm with an external meter at a named plane, then bisect source enable, coupling, connectors, MUX loss, and monitor-PD / APC honesty. Therefore I would contain if lot-correlated, clean or replace the plant if local, and update ATP or hygiene rules so it does not recur.

::: dectree
Power down \| Scope \| External meter @ named plane \| Monitor vs external agree? \|-- NO --\> APC / monitor-PD / cal \|-- YES --\> source / coupling / connector / MUX \| Population? \|-- lot/vendor --\> contain + FA \|-- single --\> plant or unit repair \| Decision + control
:::

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

**Deep dive.** Power fork and instruments: §A.6.3. APC and calibration: §5.11.

## One weak lane

**Interview question.** A single lane in a four-lane transceiver has elevated BER while received power on that lane looks normal. How would you isolate it?

**What the interviewer is testing.** Lane isolation: sibling comparison, optical-versus-electrical bisect, and lot versus unit ownership.

> **30-second answer (memorize).** First scope: one lane, one unit, or a pattern across the lot? Compare sibling lanes, then optical-versus-electrical swap to split path from driver or TIA. Therefore I would fix assembly or the array element that owns the fault, and add the screen that would have caught it.

::: dectree
One weak lane \| Siblings OK? \|-- NO --\> shared supply / thermal / host \|-- YES --\> lane-local \| Opt vs elec swap \|-- optical --\> FAU / coupling / PIC lane \|-- electrical --\> driver / TIA / SerDes \| Lot pattern? \| Decision: rework / screen / supplier
:::

**Engineering reasoning.** Sibling comparison is the cheapest population cut inside one module. Optical-versus-electrical swap prevents weeks of laser FA on a TIA lane (§A.8.6).

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

**Deep dive.** Worked answer: §A.8.6. FAU and parallel optics appear throughout Chapter 10.

## High-temperature failures

**Interview question.** BER worsens at high temperature but average power is stable. What do you do?

**What the interviewer is testing.** Corner debugging: measure where it fails, separate reversible control/calibration from permanent damage.

> **30-second answer (memorize).** Power held, so leave the power ledger. First scope the failure and whether cool-down recovers. At the failing temperature, read eye, bias sweep, wavelength, and control headroom. Therefore I would fix the table or thermal design and put that loaded corner in the ATP.

::: dectree
Hot BER, power stable \| Scope + cool-down recovers? \|-- YES --\> operating point / table / control \|-- NO --\> aging / permanent damage \| At failing T: eye, bias sweep, OSA, TEC/heater codes \| Control ledger exhausted? \|-- YES --\> thermal design / tuning range \|-- NO --\> cal table / wavelength / Rx \| Decision: retune + ATP corner
:::

**Engineering reasoning.** Temperature failures are often control or calibration, not a dead laser. Measuring at room temperature misses the spent ledger (§A.8.3).

**Measurements.** Cool-down test $\rightarrow$ reversible? $\rightarrow$ thermal vs aging.\
Bias sweep at hot $\rightarrow$ optimum moved? $\rightarrow$ table.\
Actuator codes $\rightarrow$ control authority left? $\rightarrow$ thermal design.\
OSA $\rightarrow$ spectral alignment? $\rightarrow$ lock / filter.

**Typical follow-ups.**

- Why insist on measuring at the failing temperature?

- How do you say "TEC maxed" in product language?

**Common mistakes.**

- Debugging only at ambient.

- Saying TEC current hit max instead of control ledger exhausted.

**Thirty-second close.** I measure at the failing temperature, ask whether cool-down recovers, fix table or thermal design, and put that loaded corner in ATP.

**Deep dive.** §A.8.3, §10.13. Control ledger: §A.6.4.

## Laser aging versus calibration drift

**Interview question.** How do you distinguish laser aging from calibration drift?

**What the interviewer is testing.** Mechanism separation with external references and reversibility, not telemetry narrative alone.

> **30-second answer (memorize).** Aging changes the LIV. Drift changes the setpoint on a healthy LIV. External LIV plus recovery after recalibration separates them. Time behavior confirms: monotonic climb versus a step after a table or firmware change. Therefore I would route aging to life/derate/replace and drift to table control plus an ATP loaded-corner check.

::: dectree
Symptom (bias up / BER up) \| Black-box telemetry first \| Need mechanism split? \|-- YES --\> engineering access / external LIV \| External LIV vs ship data \|-- LIV moved --\> aging --\> life / derate / replace \|-- LIV OK ----\> drift path \| Table reload recovers? \|-- YES --\> calibration / firmware \|-- NO --\> deeper FA
:::

**Engineering reasoning.** Telemetry can look identical for aging and drift. Only an external reference and a recovery test pick the owner (§A.8.4).

**Measurements.** External LIV $\rightarrow$ device changed? $\rightarrow$ aging vs setpoint.\
Monitor vs meter $\rightarrow$ APC honesty? $\rightarrow$ monitor-PD.\
Table reload $\rightarrow$ recovers? $\rightarrow$ calibration owner.\
Stress-hours plot $\rightarrow$ monotonic or step? $\rightarrow$ confirms.

**Typical follow-ups.**

- What is the silent failure mode if the monitor lies?

- Who owns aging versus who owns the table?

**Common mistakes.**

- Recalibrating an aged device and calling it fixed.

- Sending a table bug to the reliability team.

**Thirty-second close.** External LIV separates aging from drift; I route aging to life actions and drift to table control plus a loaded-corner screen.

**Deep dive.** §A.8.4, §5.11, §5.10.

## Second-source qualification

**Interview question.** How would you qualify a second laser or PIC supplier?

**What the interviewer is testing.** Second-source judgment: customer-visible margin across the envelope, not datasheet cloning.

> **30-second answer (memorize).** Freeze the requirements slice, not the incumbent datasheet. Characterize distributions across lots and temperature from the customer view: OMA, RIN at ORL, wavelength, eye, and life with a named HTOL mechanism. Therefore I would gate open volume on FAIR, ATP correlation, and split RMA codes, not on a hero sample.

::: dectree
Second source \| Nominal function \| Margin + environment + interop \| Reliability + manufacturing variation \| ATP compatibility \| Black-box enough? \|-- YES --\> pilot / ship gate \|-- NO --\> Tx-only / Rx-only / breakout \| Ship / hold / reject
:::

**Engineering reasoning.** The objective is acceptable system behavior and remaining margin across the deployment envelope, not nominal equivalence to the incumbent (§C.10, §A.8.5).

**Measurements.** Multi-lot LIV/RIN/SMSR $\rightarrow$ process spread? $\rightarrow$ risk.\
HTOL $\rightarrow$ life hypothesis? $\rightarrow$ FIT / derate.\
ATP on both sources $\rightarrow$ escape risk? $\rightarrow$ ship gate.\
RMA split $\rightarrow$ field falsifies qual? $\rightarrow$ reopen.

**Typical follow-ups.**

- Why not just match the incumbent datasheet?

- What customer measurements matter if the part is a black box?

**Common mistakes.**

- Qualifying a hero sample.

- Merging supplier RMA codes.

**Thirty-second close.** I qualify distributions and remaining margin on the customer-visible surface, then gate volume on FAIR, ATP correlation, and split RMA.

**Deep dive.** §A.8.5, §8.10.

## Validation plan for a new transceiver

**Interview question.** How would you validate a new optical transmitter from bring-up through production?

**What the interviewer is testing.** Staged uncertainty reduction and margin budgeting from bring-up through fleet.

> **30-second answer (memorize).** Validation is staged uncertainty reduction. Walk bring-up, characterization, margin, interop, environment, reliability, production, and fleet. Each stage answers a question the previous could not. Therefore I would refuse any test that answers no new question and watch the ledgers margin budgeting says will be spent first.

::: dectree
New transceiver \| Bring-up -\> Characterization -\> Margin \| Interop -\> Environment -\> Reliability \| ATP / manufacturing -\> Pilot -\> Fleet \| Each stage: question? uncertainty? decision?
:::

**Engineering reasoning.** The ladder is Universal Tree 2. Margin budgeting says stresses consume margin; stages exist to measure remaining margin from the customer-visible surface first (§A.6.5, §A.6.6).

**Measurements.** Each ladder stage $\rightarrow$ named uncertainty removed $\rightarrow$ continue / redesign / tighten ATP / stop ship.\
Margin sweeps $\rightarrow$ which ledger dies first? $\rightarrow$ telemetry alarms.

**Typical follow-ups.**

- Which stage removes combination risk?

- How does margin budgeting change what you instrument in the fleet?

**Common mistakes.**

- Treating bring-up as population proof.

- Running HTOL without a named mechanism.

**Thirty-second close.** I walk the ladder as staged uncertainty reduction and refuse any test that answers no new question about remaining margin.

**Deep dive.** §A.8.2, Table 7.1, §A.6.7.

## Fleet issue

**Interview question.** Field telemetry shows rising pre-FEC BER on a subset of racks. How do you triage?

**What the interviewer is testing.** Fleet ownership: scope, trend, bucket, and contain-versus-monitor under incomplete evidence.

> **30-second answer (memorize).** First scope: unit, lot, vendor, rack, datacenter, or fleet? Ask trend and change history. Classify performance versus reliability versus manufacturability before pulling hardware. Therefore I would contain if growing and supplier-specific, or monitor-only if tiny, flat, and no customer impact, with an owner on the next control.

::: dectree
Fleet symptom \| Scope ladder \| Rate / trend / customer impact \|-- tiny, flat, no impact --\> monitor only \|-- growing / supplier --\> contain now \| Bucket: performance / reliability / manufacturability \| Decision + owner + telemetry control
:::

**Engineering reasoning.** Fleet economics and scope pick the owner before FA. Pulling units without a bucket wastes the only failing state you had (§A.4, §7.12).

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

**Deep dive.** §A.4, Table 7.6.

## Supplier escape

**Interview question.** A new date code from Supplier B fails the hot corner at about 3%. What do you do?

**What the interviewer is testing.** Staff judgment under uncertainty: contain today, keep FA open, own recurrence control.

> **30-second answer (memorize).** Evidence beats an unknown mechanism. Stop shipment of Supplier B affected lots, continue Supplier A, expand the ATP hot-corner screen, open FA with DPA on fails, and watch RMA daily. Therefore I would contain today and keep the FA path open rather than wait for SEM before acting.

::: dectree
Escape detected \| Contain lot / pause deploy \| Scope deployed population \| Compare failing vs healthy \| Supplier joint FA \| Corrective action \| ATP or process-control update \| Verify next lot \| Fleet monitoring
:::

**Engineering reasoning.** Containment, root cause, and prevention are three actions. The system owner keeps responsibility for evidence quality and verifying the fix (§C.8, §A.4).

**Measurements.** Lot genealogy $\rightarrow$ exposure? $\rightarrow$ quarantine list.\
ATP hot corner $\rightarrow$ escape path? $\rightarrow$ production gate.\
DPA sample $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- Why contain before FA completes?

- What residual risk do you name to leadership?

**Common mistakes.**

- Waiting for root cause before stop-ship.

- Blocking all vendors for one supplier's lot.

**Thirty-second close.** I contain Supplier B today, keep a healthy path shipping, open FA, expand ATP, and own verification of the next lot.

**Deep dive.** §A.4, Table A.1.

## BER floor

**Interview question.** Why can a link show a BER floor that more launch power does not fix?

**What the interviewer is testing.** Separating sensitivity shift from multiplicative-noise floor and choosing the fix that matches the shape.

> **30-second answer (memorize).** A floor means multiplicative noise: SNR stops improving as power rises. Prioritize RIN under ORL, MPI from reflections, weak PSRR, and crosstalk. Therefore I would confirm floor versus shift on a waterfall, then remove the noise source rather than raise OMA.

::: dectree
BER vs power \| Shape? \|-- parallel shift --\> sensitivity \|-- floor ---------\> multiplicative noise \| ORL / RIN / MPI / PSRR / crosstalk \| Fix noise source, not launch
:::

**Engineering reasoning.** More power cannot beat noise that scales with the signal. The waterfall shape is the fast cut between sensitivity and floor (§A.8.8, §A.6.9).

**Measurements.** Waterfall $\rightarrow$ shift or floor? $\rightarrow$ next hunt.\
Controlled ORL $\rightarrow$ reflection-driven RIN? $\rightarrow$ plant.\
Supply noise $\rightarrow$ PSRR path? $\rightarrow$ filter / layout.

**Typical follow-ups.**

- Why not just increase OMA?

- How do FEC histograms look for MPI bursts?

**Common mistakes.**

- Raising launch into a floor.

- Skipping ORL when RIN is blamed.

**Thirty-second close.** I confirm floor versus shift on a waterfall, then remove the multiplicative noise source rather than raise launch power.

**Deep dive.** §A.8.8, §10.3, §4.3.

## Intermittent failures

**Interview question.** The link fails intermittently and often passes when retested. How do you proceed?

**What the interviewer is testing.** Evidence preservation, reproduction strategy, and refusing premature NFF closure.

> **30-second answer (memorize).** Preserve the failing state and telemetry before you reseat, clean, or reboot. Scope time and change: dwell, temperature, vibration, firmware, connector. Prefer burst/FEC histograms and long dwell over a single golden retest. Therefore I would contain if lot-correlated, tighten dwell/ATP if escape, and refuse to close an NFF without a reproduction plan.

::: dectree
Intermittent \| Preserve state / telemetry \| Triggers: T, time, mate, vibration, FW \| Reproduce with dwell / stress \| Scope population \| Decision: contain / ATP dwell / monitor
:::

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

::: dectree
Escape \| Which uncertainty ATP missed? \| New measurement / corner / limit \| Guard band from repeatability \| Station correlation \| Reaction plan + owner \| Ship ATP change
:::

**Engineering reasoning.** Recurrence control is usually an ATP or telemetry change. A limit nobody can trace gets waived under ship pressure (§A.8.2).

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

**Deep dive.** Production readiness stage in §A.6.5.

## Telemetry design

**Interview question.** What would you put in fleet telemetry, and why?

**What the interviewer is testing.** Instrumenting ledgers that unlock triage decisions, not logging every register.

> **30-second answer (memorize).** Log what discriminates hypotheses: per-lane power, bias, pre-FEC BER and FEC histograms; module temperature and actuator drive; LOS/LOL and firmware with context. Alarm on trends and disagreements, not only hard thresholds. Therefore I would instrument the ledgers margin testing said die first.

::: dectree
Telemetry purpose: early margin erosion \| Per-lane: power, bias, pre-FEC BER \| Module: T, TEC/heater, rails, lock \| Events + lot/age/rack context \| Alarms: trends / disagreements
:::

**Engineering reasoning.** Telemetry exists to triage without pulling hardware and to catch dying units before dead ones (§A.8.13).

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

**Deep dive.** §A.8.13, §7.8.

## Qualification planning

**Interview question.** How do you plan qualification for a new IM/DD module?

**What the interviewer is testing.** Qualification as remaining-margin verification with named mechanisms and customer view.

> **30-second answer (memorize).** Start from customer-visible requirements and a margin budget: which stresses will spend which ledgers. Map stresses to mechanisms, run HTOL only with a named activation energy, and prove ATP can catch escapes at rate. Therefore I would gate ship on remaining margin after environment, interop, and life, not on a checklist of rituals.

::: dectree
Qual plan \| Customer requirements + margin budget \| Stress -\> mechanism -\> ledger spent \| HTOL with named Ea \| ATP catches escapes? \| Ship gate = remaining margin OK
:::

**Engineering reasoning.** Margin budgeting and customer view keep qual from becoming museum of tests. Stress consumes margin; qual measures what remains (§A.6.6, §A.6.7).

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

**Deep dive.** §A.6.5, §8.2, §5.13.

## Unknown failure

**Interview question.** You must make a ship decision this week, but the physical mechanism is still unknown. What do you do?

**What the interviewer is testing.** Deciding with today's evidence: contain, owner, control, and residual risk before mechanism certainty.

> **30-second answer (memorize).** State evidence, confidence weights, and residual risk. Decide with today's evidence: contain the scoped population, keep a healthy path shipping, open FA, and add the ATP or telemetry control that would catch the next escape. Therefore I would not wait for certainty before ownership actions.

::: dectree
Unknown mechanism \| Evidence + scope + rate/trend \| Priors: common modes first \| Decision today (contain / ship / derate) \| FA path + control + owner \| Update when mechanism closes
:::

**Engineering reasoning.** The job is the best decision with today's evidence. Unknown mechanism is Framework 15 of Staff judgment, not a reason to freeze (§A.4).

**Measurements.** Whatever removes the most uncertainty per hour toward the ship decision: scope query, golden swap, external power, hot-corner ATP sample.\
DPA later $\rightarrow$ mechanism class? $\rightarrow$ permanent fix.

**Typical follow-ups.**

- What do you tell leadership about residual risk?

- Which measurement is worth delaying the decision for?

**Common mistakes.**

- Freezing all action until SEM.

- Making a ship call with no control and no owner.

**Thirty-second close.** I decide with today's evidence, contain the scoped population, keep a healthy path shipping, and name the control and residual risk.

**Deep dive.** §A.4, §A.2, Table A.1.

**Key idea.** Open the matching framework, deliver the thirty-second box, walk the tree, end on the decision and the control. Philosophy is in §A; this appendix is how you speak it under pressure.


<div class="nav-links">
  <a href="ch11-one-week-optical-systems-interview-review">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch13-engineering-decision-trees">Next &rarr;</a>
</div>
