---
layout: default
title: "Ch 10: Optical Links in Operation: From Physical Margin to Workload Impact"
---

# 10 Optical Links in Operation: From Physical Margin to Workload Impact

An optical link does not fail only when it goes dark. It can remain logically up while consuming FEC margin, producing bursts, retraining intermittently, or delaying synchronized workloads.

Operating the fleet therefore requires more than monitoring average BER or link state. The engineering task is to connect physical margin, error behavior, recovery, topology, and workload consequence.

This chapter develops that chain. It explains how to interpret FEC and link-health signals, validate recovery behavior, analyze cohorts, translate component events into system availability, and use controlled deployment evidence to bound operational risk. Fabric context (scale-up/out, topologies, module styles, CPO/XPO/OCS, power and cost) lives in Appendix H. BER and noise models live in Chapter 4. Product readiness and pilot sequencing live in Chapter 7. Detailed failure analysis lives in Chapter 11.

The dominant model is:

> Physical impairment $\rightarrow$ margin or error change $\rightarrow$ FEC and link-health response $\rightarrow$ state transition or recovery $\rightarrow$ network consequence $\rightarrow$ workload consequence $\rightarrow$ fleet decision.

## What the system sees

Keep four layers distinct. A physical impairment is not a link-health indicator. A protocol event is not a workload failure. Mixing them hides the decision.

Every major example in this chapter maps onto one chain. For example:

> Reflection increase $\rightarrow$ waveform penalty and burst errors $\rightarrow$ corrected-error rise $\rightarrow$ uncorrectable block and retrain $\rightarrow$ temporary path loss $\rightarrow$ collective slowdown $\rightarrow$ hold or cohort containment.

Start observation at the layer where impact appears, then descend only far enough to isolate the next decision. A workload stall does not by itself prove an optical mechanism, and a rising laser current does not by itself prove a job impact.

<table class="book-table"><tr><th>Layer</th><th>Example observation</th></tr><tr><td>Optical or electrical</td><td>Power loss, reflection sensitivity, wavelength drift, receiver-margin loss</td></tr><tr><td>Link health</td><td>Rising corrected errors, burst errors, lane skew, degraded eye margin</td></tr><tr><td>Link state</td><td>Retrain, lane reset, link flap, loss of lock</td></tr><tr><td>Network behavior</td><td>Packet loss, reroute, congestion, reduced path diversity</td></tr><tr><td>Workload behavior</td><td>Straggler, collective delay, checkpoint/restart, reduced cluster efficiency</td></tr></table>
**Table 10.1.** Physical impairment becomes operational consequence only after it crosses these layers. Fabric topology context: Appendix H.

<table class="book-table"><tr><th>Concept</th><th>Question answered</th></tr><tr><td>Physical margin</td><td>How far is the link from a failure boundary?</td></tr><tr><td>Link health</td><td>How much impairment is present over time?</td></tr><tr><td>Link state</td><td>Is the lane or link currently operational?</td></tr><tr><td>Recovery</td><td>How is service restored after a detected event?</td></tr><tr><td>Availability</td><td>How often and how long is required service unavailable?</td></tr><tr><td>Workload impact</td><td>What does the event do to useful AI-compute progress?</td></tr></table>
**Table 10.2.** Use these questions instead of repeating informal definitions of "up," "healthy," and "available."

## Why link-up is not enough

Link-up is a state. Link health is a distribution over time.

A link can remain logically up while becoming operationally unhealthy. It may consume FEC margin through rising corrected-error activity, produce short bursts that the long-term average hides, retrain intermittently, or create workload stalls without a sustained down event. Steady-state pass at one operating point does not prove transition or recovery behavior.

Corrected-error growth is often the first useful warning. Service can remain error-free while the physical margin shrinks. Average BER over a long window can look excellent while millisecond bursts still approach the decoder limit. A link that passes under constant load can still fail during thermal slew, fan step, firmware transition, or fiber movement.

### Event vocabulary

Use a common event vocabulary and keep the order in time:

Correctable FEC event

: The decoder repairs errors; the link may remain logically usable while margin is consumed.

Uncorrectable FEC event

: The error pattern exceeds correction capability and may produce packet loss, a lane failure, or a link-state event.

Retrain

: The PHY repeats equalization, CDR, lane alignment, or another link-training function. Traffic may interrupt without a full MAC-level down.

Link flap

: The operational link transitions down and later returns up, usually with a larger control-plane or topology reaction.

Workload stall

: An application-visible delay, potentially caused by one or several lower-layer events.

> **Engineering heuristic.** Do not close an investigation because the link is up and post-FEC traffic looks clean. Ask what the corrected-error distribution, burst timing, retrain count, recovery duration, and workload tail say over the same window.

## BER, FEC, and error distributions

Interpret counters as system evidence, not as interchangeable BER synonyms. Detailed BER and coding models live in Chapter 4, §3.12.

Pre-FEC error activity

: indicates physical-link burden before correction. The counter may record bits, symbols, codewords, or implementation-specific events, so its definition and accumulation window must be stated.

Corrected errors

: indicate FEC activity and consumed margin. Rising correction demand can reveal shrinking physical margin even while delivered traffic remains error-free. It is an early-warning signal, not by itself proof of an imminent outage.

Uncorrectable events

: exceed correction capability and create service impact: packet loss, lane failure, or a link-state event.

Post-FEC residuals

: describe what remains after correction. Zero observed residuals do not prove unlimited margin.

Average BER can hide burstiness. Threshold crossing and temporal clustering matter. FEC counters must be interpreted with lane rate, time window, code, and counter semantics.

> **FEC counter semantics**\
> FEC counters are implementation-specific evidence. Their meaning depends on the code, lane rate, counter definition, accumulation window, reset behavior, and whether the counter records corrected bits, symbols, codewords, or threshold events.

An FEC symbol-error histogram is not a DCA eye histogram. Sparse, Poisson-like distributions fit steady noise. Bursty clumps fit time-local events: MPI, connector intermittents, unlock, supply or clock glitches. Shape prioritizes hypotheses; confirm with ORL, timing, swaps, and plant disturbance (§11.2, Chapter 11).

Do not claim that corrected errors mean the link is failing, that "below threshold" means safe, or that FEC hides the problem. Corrected activity indicates consumed margin. Uncorrectable events and recovery events indicate service impact.

## Bursts, transitions, and dynamic corners

Long averages can look excellent while brief bursts still trigger FEC failure, retrain, lane reset, or workload interruption. Dynamic corners that create this gap include:

- thermal transitions;

- fan-speed or airflow changes;

- neighboring-port loading;

- power-supply disturbances;

- wavelength-control events;

- host reset or firmware transitions;

- fiber movement and reflection changes;

- startup and low-power transitions.

> **Average versus burst errors**\
> Average BER compresses time. Two links can have the same average while behaving very differently. One may produce sparse independent errors that FEC handles easily; another may produce concentrated bursts during thermal, control, or power transitions. The second link may create uncorrectable events or retrains even when the long-term average appears acceptable.

Ask three questions for every suspect burst: How large is it? How long does it last? What operational event does it trigger?

*Illustrative example.* A link with an average BER of $10^{-10}$ may still experience millisecond bursts during thermal transitions that exceed the FEC correction capability and trigger a retrain. Do not treat any one burst threshold as universal; tie the claim to the named code, window, and recovery behavior.

## Recovery is part of the product

Recovery is engineered behavior, not an afterthought. For each path, name the trigger, owning layer, duration, evidence preservation, return configuration, oscillation risk, and workload interruption. A retrain is one recovery procedure that re-establishes timing, alignment, equalization, or protocol state.

Canonical sequence:

> Impairment $\rightarrow$ detection $\rightarrow$ local containment $\rightarrow$ retrain or reset $\rightarrow$ restoration $\rightarrow$ verification $\rightarrow$ recurrence monitoring.

<table class="book-table"><tr><th>Event</th><th>Detection</th><th>Expected response</th><th>Evidence to preserve</th></tr><tr><td>Loss of signal</td><td>Optical or PCS indication</td><td>Lane or link recovery sequence</td><td>Power, alarms, state history, time to restore</td></tr><tr><td>Loss of lock</td><td>CDR or PCS state</td><td>Retrain or reset</td><td>Error counters, lock state, host conditions</td></tr><tr><td>Thermal alarm</td><td>Module or host telemetry</td><td>Throttle, disable, or recover after cooling</td><td>Temperature history, workload, control demand</td></tr><tr><td>Power transient</td><td>Voltage or reset monitor</td><td>Controlled restart</td><td>Rail history, reset cause, firmware state</td></tr><tr><td>Firmware fault</td><td>Watchdog or management timeout</td><td>Local reset or host intervention</td><td>Logs, firmware identity, command history</td></tr></table>
**Table 10.3.** Recovery paths are product requirements. Validate detection, restoration time, evidence retention, and recurrence behavior before fleet exposure.

Ask for each recovery path:

- What triggers it?

- Which layer owns it?

- How long does it take?

- Does it preserve useful evidence?

- Does it return to the same configuration?

- Can it oscillate?

- What workload interruption does it create?

Repeated recovery loops are a product defect even when each loop eventually succeeds. Preserve state and counters across recovery when possible; a reset that erases the failing evidence forces guesswork. Escalate to host reset or human intervention only when the local path is exhausted or oscillating (§10.11, Chapter 11).

Align timestamps across optics, switch, and workload before arguing causality. Without a common clock story, every flap looks like every stall.

<table class="book-table"><tr><th>Architecture</th><th>Host owns</th><th>Module / engine owns</th><th>Main operational ambiguity</th></tr><tr><td>Fully retimed</td><td>Host channel to module input; system FEC</td><td>Module CDR/DSP and optical conversion</td><td>DSP may hide where impairment began</td></tr><tr><td>LPO</td><td>EQ, CDR, FEC, much of end-to-end margin</td><td>Analog optical conversion and linearity</td><td>Host and module behavior strongly coupled</td></tr><tr><td>LRO</td><td>Direction-dependent shared ownership</td><td>Retimed direction plus analog direction</td><td>Failure ownership changes by direction</td></tr><tr><td>CPO</td><td>Switch package, electrical XSR, system FEC</td><td>Co-packaged optical engine and external laser path</td><td>Larger thermal/service failure domain</td></tr></table>
**Table 10.4.** Operational ownership by architecture when assigning recovery and debug responsibility (Appendix H.3.1, Appendix H.10).

## Telemetry that supports decisions

A telemetry signal is valuable when it separates hypotheses, bounds a population, predicts degradation, or triggers an action. Organize evidence by purpose, not by register address. Register-level CMIS detail belongs in Appendix E.7, Appendix E.

### Four evidence groups

Identity and configuration

: Module serial, hardware revision, firmware, host, peer, port, fiber path, and deployment cohort.

Physical state

: Temperature, voltage and current, optical power, wavelength or control demand, laser current, and alarms.

Link-health state

: Pre-FEC or corrected-error counters, uncorrectable events, retrains, lane state transitions, loss-of-lock events, and recovery duration.

Operational consequence

: Packet loss, reroute, congestion, path withdrawal, workload slowdown, and job failure or restart.

### Decision-oriented signal matrix

<table class="book-table"><tr><th>Signal</th><th>Possible value</th><th>Limitation</th></tr><tr><td>Optical power</td><td>Detect gross loss or drift</td><td>Cannot isolate source, coupling, or path loss alone</td></tr><tr><td>Laser current or control demand</td><td>Reveal increasing control effort</td><td>May remain normal for path-loss failures</td></tr><tr><td>Temperature</td><td>Correlate events with thermal state</td><td>Internal sensor may not equal junction temperature</td></tr><tr><td>Corrected-error counters</td><td>Reveal consumed FEC margin</td><td>Counter semantics and accumulation window matter</td></tr><tr><td>Retrain count</td><td>Quantify recovery events</td><td>Does not identify physical cause</td></tr><tr><td>Alarm history</td><td>Reconstruct state transitions</td><td>Firmware definitions and latching behavior matter</td></tr><tr><td>Genealogy</td><td>Bound affected populations</td><td>Correlation does not prove mechanism</td></tr></table>
**Table 10.5.** Prefer signals that change a decision over exhaustive register inventories.

Management state must be trustworthy. Counters need semantic definitions. Polling cadence affects observability. Reset behavior can erase evidence. Alarm latching and clearing must be understood before you trust a "cleared" state.

## Operational severity

The same physical impairment can create different consequences. Assign severity from operational consequence, not only from the optical symptom.

1.  **Invisible correction:** FEC corrects the event with no service impact.

2.  **Degraded margin:** corrected-error rate rises but service continues.

3.  **Local recovery:** lane retrains or resets automatically.

4.  **Path impact:** link or path is temporarily removed.

5.  **Workload impact:** traffic stalls, congestion spreads, or a collective slows.

6.  **Job impact:** restart, checkpoint recovery, or job failure occurs.

## Cohorts and fleet interpretation

A cohort is a defined population sharing one or more attributes: module lot, laser lot, assembly site, supplier, hardware revision, firmware, host platform, switch type, rack or thermal zone, fiber plant, installation date, or workload profile.

One failure is an incident. A correlated cohort may be a systemic problem. Unaffected cohorts are as important as affected cohorts. Correlation raises a hypothesis but does not prove cause. Denominators and observation windows must be explicit.

*Example.* If retrains rise only on one host revision but across several module lots, the host or host--module interaction becomes more plausible than a single optical-component lot issue.

## From component reliability to system availability

Component FIT is not system availability. Link-event frequency scales with population. Availability depends on detection, redundancy, topology, reroute, repair time, and workload consequence. Synchronized AI workloads may amplify a single weak link: a straggler can delay an entire collective (Appendix H.7). A low individual failure rate can still create frequent fleet events at large scale.

### From component FIT to fabric availability

Component FIT arithmetic sizes RMA and sparing (§5.13, §8.4.1). It does not by itself state service impact.

*Illustrative example.* Consider a fleet of 500,000 optical links. If the observed event rate is two retrains per million link-hours, the expected fleet frequency is approximately one retrain every hour. That does not mean one hour of fleet downtime. The effect depends on retrain duration, topology, redundancy, traffic movement, and whether the workload is sensitive to the affected path. State the assumptions: population, event definition, observation window, and independence. This is a reasoning aid, not a universal availability model.

A second population-scale view uses hard failures rather than retrains. The FIT arithmetic in §5.13 gives about $0.6$ laser failures per day for a fleet of $5\times10^5$ lasers at 50 FIT. That number sizes the RMA pipeline and the ELS spares bin (§5.14). It still does not say what a failure costs a running job. Meta's published Llama 3 run is a useful public anchor: 16,384 H100 GPUs over 54 days logged 466 interruptions (419 unexpected), roughly one every three hours, while holding about 90% effective training time . Network switch and cable faults were a minority of hard stops, but at that cadence they still contribute tens of network events per run. Treat the split as orientation, not as a universal budget for every fabric.

Keep five quantities separate when translating events to availability:

Event rate

: How often the named event occurs per link-hour or fleet-hour.

Duration

: How long recovery or path loss lasts.

Affected scope

: Lane, link, path, rack, or collective.

Recurrence

: Isolated event versus oscillating recovery.

Workload consequence

: Silent correction, stall, restart, or job failure.

Architectural mitigations change duration and scope; they do not erase the need for component reliability or production controls:

Redundancy and rails.

: Parallel planes can degrade bandwidth instead of dropping an endpoint (Appendix H.2). More resilience is also more parts that can fail.

Detection and reroute.

: FEC, link-level retry, and adaptive routing can keep many transient optical faults below the hard-stop bucket (§3.12).

Topology reconfiguration.

: Optical circuit switching can re-wire around a dead link or rack when the architecture supports it (Appendix H.9).

Sparing and field service.

: Hot spares and field-replaceable external lasers change repair time and failure domain (§5.14).

The two multipliers are the failure rate and the cost of each failure that slips through. Qualification, manufacturing screens, and ATP lower the rate (Chapter 8, Chapter 9); resilient detection and recovery lower the cost.

## Pilot and controlled ramp as operational evidence

Chapter 7 owns the readiness lifecycle and pilot sequencing (Chapter 7, §7.4.8). Here the pilot is a bounded field experiment with:

- identifiable serials and genealogy;

- production-representative hardware and firmware;

- controlled topology and exposure;

- enhanced telemetry against the four evidence groups;

- expected distributions for corrected errors, retrains, and recovery time;

- hold, rollback, and expansion criteria;

- explicit ownership for containment decisions.

A small shipment is not automatically a pilot. A pilot has a hypothesis, bounded exposure, observability, exit criteria, and reversibility.

Expansion requires metrics consistent with the release model, no unexplained cohort, adequate telemetry, bounded residual risk, and reversible containment. If corrected-error or retrain distributions diverge without a named residual risk acceptance, pause before the next volume step.

## Operational investigation workflow

Stay at system-triage level. Mechanism confirmation belongs to Chapter 11, §11.16.

Canonical sequence:

> Verify the signal $\rightarrow$ bound the population $\rightarrow$ compare affected and unaffected cohorts $\rightarrow$ preserve state and genealogy $\rightarrow$ use reversible swaps or controlled comparisons $\rightarrow$ contain exposure $\rightarrow$ hand mechanism confirmation to failure analysis.

Operational evidence should preserve the failing state, genealogy, timing, and configuration before swaps or resets destroy information.

Useful reversible comparisons include module swap, host-port swap, fiber swap, firmware comparison, thermal or power comparison, and peer comparison. A module swap that moves the symptom raises a module or module--path hypothesis; it does not by itself establish root cause or supplier responsibility.

### Worked example: intermittent retrains in a loaded rack

*Observation.* Retrains rise in one rack during high-compute workloads.

*Verify.* Confirm counter semantics, time synchronization, and event duration.

*Scope.* Compare by module lot, host revision, firmware, port, thermal zone, fiber path, workload, and installation date.

*Physical-to-system hypotheses.* Thermal receiver-margin loss; host equalization interaction; reflection-sensitive fiber path; power-rail disturbance; firmware recovery defect.

*Reversible experiments.* Swap module while preserving port and fiber; swap fiber while preserving module and host; compare host firmware; reproduce under controlled thermal loading; correlate with corrected-error and power telemetry.

*Containment.* Hold expansion of the affected cohort and preserve failing units.

*Decision.* Module containment, host-firmware correction, fiber remediation, added telemetry, restricted operating envelope, or Chapter 11 failure analysis.

## Interview takeaway

**Key idea.** Staff-level optical systems leadership means connecting a physical impairment to the system event it creates and the workload consequence that follows. I do not stop at link-up, average BER, or a component FIT value. I ask how the impairment appears in FEC and state telemetry, how the system detects and recovers, how the event scales across the fleet, and what containment or release decision the evidence supports.

The most useful operational signal is not necessarily the most detailed one. It is the signal that separates hypotheses or changes the decision.

Junior mistake: treat a link as healthy whenever it is up and post-FEC traffic appears clean. Better practice: examine corrected-error distributions, bursts, retrains, recovery time, physical telemetry, and workload impact across deployment cohorts (§10.2, §10.8, Chapter 11).

### Interview Q&A: Optical Links in Operation

Practice speaking these answers aloud. Prefer first-person operational reasoning. Detail lives in §10.1, §10.3, §10.5, §10.6, §10.9.1, §10.11, §11.16.

##### Question 1. What does it mean for an optical link to be operationally healthy?

*Tests:* link-up versus health; margin and temporal behavior.

*Spoken answer.* "Link-up is necessary but not sufficient. I treat health as a distribution over time: corrected-error activity, burstiness, retrains, recovery duration, physical telemetry, and workload impact on the intended topology. A link that stays up while consuming FEC margin or stalling collectives is not healthy" (§10.2).

*Pressure follow-up.* "The link has been up for a week with no post-FEC errors. Is it healthy?"\
*Answer pivot.* "Not without the corrected-error and retrain history over that week, plus behavior under thermal and workload transitions."

*Trap:* "Up plus clean post-FEC means healthy."

##### Question 2. How do pre-FEC errors, corrected errors, uncorrectable events, and retrains differ?

*Tests:* layered error interpretation.

*Spoken answer.* "Pre-FEC activity measures physical-link burden before correction. Corrected errors show FEC consuming margin while service may still look clean. Uncorrectable events exceed the code and create service impact. Retrain is a recovery state transition, not an error counter. I never treat these as synonyms, and I always state counter semantics and window" (§10.3).

*Pressure follow-up.* "Corrected errors are rising. Is the link failing?"\
*Answer pivot.* "It indicates shrinking margin. I then check bursts, uncorrectables, recovery events, and workload consequence before assigning severity."

*Trap:* "Corrected errors mean the link is failing."

##### Question 3. Why can average BER be misleading?

*Tests:* bursts and temporal clustering.

*Spoken answer.* "Average BER compresses time. Two links can share the same average while one has sparse independent errors and the other has millisecond bursts during thermal or power transitions that exceed FEC and trigger retrain. I ask burst size, duration, and operational event" (§10.4).

*Pressure follow-up.* "Our average is $10^{-12}$. Are we safe?"\
*Answer pivot.* "Only if the burst distribution, code, and recovery behavior under dynamic corners also support that claim."

*Trap:* "A good long-term average proves transition safety."

##### Question 4. How do you validate recovery behavior?

*Tests:* detection, restoration, timing, and recurrence.

*Spoken answer.* "I treat recovery as a product requirement. For each path I name the trigger, owner, expected response, time to restore, evidence preserved across the event, return configuration, oscillation risk, and workload interruption. Then I inject or observe the trigger and measure those quantities, including repeated recovery loops" (§10.5).

*Pressure follow-up.* "The link always comes back. Is recovery good enough?"\
*Answer pivot.* "Not if recurrence is high, evidence is erased, or collectives stall every time."

*Trap:* "Successful restore equals validated recovery."

##### Question 5. What telemetry is most useful for optical fleet operation?

*Tests:* actionable telemetry rather than register inventory.

*Spoken answer.* "I collect identity, physical state, link-health state, and operational consequence. The best signal separates hypotheses, bounds a population, predicts degradation, or triggers action. Optical power, control demand, corrected-error counters, retrain count, alarms, and genealogy matter when I know their semantics and limitations" (§10.6).

*Pressure follow-up.* "Should we log every CMIS register?"\
*Answer pivot.* "No. I define the decision-oriented set and keep register maps in the management reference (Appendix E.7)."

*Trap:* "More registers always mean better operations."

##### Question 6. How do you investigate a rising retrain rate?

*Tests:* signal verification, scoping, cohorts, reversible experiments.

*Spoken answer.* "I verify counter semantics and timing, bound the population, compare affected and unaffected cohorts, preserve state, run reversible swaps, contain exposure, and hand mechanism confirmation to failure analysis. I do not jump from retrain count to optical root cause" (§10.11, §10.11.1).

*Pressure follow-up.* "Retrains rose after a firmware update. Blame firmware?"\
*Answer pivot.* "It raises a firmware hypothesis. I still compare cohorts and preserve units before concluding."

*Trap:* "A retrain proves an optical problem."

##### Question 7. How do you distinguish module, host, fiber, firmware, and environmental hypotheses?

*Tests:* controlled comparison and what-follows-the-symptom reasoning.

*Spoken answer.* "I use reversible comparisons: module swap, fiber swap, host-port swap, firmware comparison, and thermal or power correlation. What the symptom follows bounds ownership. Architecture ownership tables tell me which layer is ambiguous (Table 10.4). Correlation alone does not prove mechanism" (§10.8, Chapter 11).

*Pressure follow-up.* "A module swap fixed it. Is the module the root cause?"\
*Answer pivot.* "It supports a module or module--path hypothesis. I still need genealogy, peer comparison, and, if needed, Chapter 11 FA."

*Trap:* "Swap recovery proves supplier root cause."

##### Question 8. How does component FIT translate into system availability?

*Tests:* population, topology, redundancy, duration, workload.

*Spoken answer.* "Component FIT is a part rate. System availability also depends on detection, redundancy, reroute, repair time, and workload consequence. At fleet scale, a low per-link event rate can still produce frequent fleet events. I separate event rate, duration, scope, recurrence, and workload impact" (§10.9.1).

*Pressure follow-up.* "Low FIT means high availability, right?"\
*Answer pivot.* "Not by itself. A short retrain on a synchronized collective can matter more than a rare hard failure with fast failover."

*Trap:* "FIT equals availability."

##### Question 9. Why can a rare optical event matter in AI compute?

*Tests:* synchronization, stragglers, and correlated impact.

*Spoken answer.* "Synchronized collectives wait for the slowest member. A short link event can create a straggler that delays many accelerators. Severity comes from workload consequence, not only from how rare the optical symptom looks in isolation" (§10.7, Appendix H.7).

*Pressure follow-up.* "Redundancy eliminates the impact, correct?"\
*Answer pivot.* "Redundancy can reduce path impact. It does not automatically eliminate stalls if recovery is slow or many paths are correlated."

*Trap:* "Rare events can be ignored in AI fabrics."

##### Question 10. What makes a pilot an operational experiment rather than a small shipment?

*Tests:* bounded exposure, telemetry, exit criteria, rollback.

*Spoken answer.* "A pilot has a hypothesis, identifiable production-representative units, controlled exposure, enhanced telemetry, expected distributions, exit criteria, and reversibility. A small shipment without those controls is just early volume" (§10.10, §7.4.8).

*Pressure follow-up.* "We shipped 200 units. Is that a pilot?"\
*Answer pivot.* "Only if the experiment design and rollback path exist."

*Trap:* "Any small deployment is a pilot."

##### Question 11. When do you pause or roll back a deployment?

*Tests:* unexplained cohorts, containment, observability, workload consequence.

*Spoken answer.* "I pause or roll back when metrics diverge from the release model, an unexplained cohort appears, telemetry cannot bound risk, recovery or workload impact is unacceptable, or containment is not reversible. I do not wait for hard job failures if early-warning signals already justify hold" (§10.10, §10.8).

*Pressure follow-up.* "Corrected errors rose but jobs still finish. Continue?"\
*Answer pivot.* "I treat that as degraded margin. Expansion needs a named residual-risk decision, not silence."

*Trap:* "Only job failures justify rollback."

##### Question 12. Give a 60-second plan for operating and monitoring a new optical module in the fleet.

*Tests:* end-to-end systems reasoning.

*Spoken answer.* "I start from the physical-to-system chain. Freeze identity and genealogy, define the decision-oriented telemetry set, validate recovery paths, set severity and containment rules, run a bounded pilot with exit criteria, watch cohorts against the release model, and escalate mechanism confirmation to failure analysis when needed. Link-up and average BER are inputs, not the decision" (§10.1, §10.5, §10.10).

*Pressure follow-up.* "Where do you start if collectives slow after expansion?"\
*Answer pivot.* "Verify the signal, bound the cohort, compare affected and unaffected populations, preserve failing state, then run reversible swaps before destructive FA."

*Trap:* "Start by redesigning the topology."


<div class="nav-links">
  <a href="ch9-manufacturing-validation-reproducing-and-controlling-the-design">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch11-failure-analysis-handbook">Next &rarr;</a>
</div>
