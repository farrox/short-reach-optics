---
layout: default
title: "Ch 21: How Staff Engineers Think"
---

# 21 How Staff Engineers Think

This appendix is judgment, not physics. The machinery lives elsewhere: validation, qualification, and manufacturing (Chapter 9), networking constraints (Chapter 9), the failure handbook (Chapter 10), the Staff loop and access levels (Appendix A.1, Appendix A.2), cases and tradeoff drills (Appendix B, Appendix C.17), and the wall-chart trees (Appendix D). Read this when you need the habits that turn that machinery into decisions under pressure.

## Engineering under uncertainty

You rarely get a confirmed mechanism before a ship, hold, or contain call. Uncertainty is the normal state. The job is to decide with today's evidence, name residual risk, and keep the FA path open (Appendix A.6).

Do not confuse "I do not know the confirmed mechanism" with "I cannot act." Scope, population, trend, and a reversible control are often enough for today's call. Waiting for SEM photos while a bad lot keeps shipping is a process failure, not scientific humility.

*Principle:* Decide with the evidence you have; name what you still do not know.

## Reversible decisions

Prefer actions you can undo cheaply: lot holds, derates, monitor-only watches, temporary ATP tightenings, firmware guards. Irreversible moves (public recall, permanent architecture change, destructive FA on the last failing unit) need stronger evidence and a named owner.

Ask: What is the cost of being wrong either way? If a hold costs a week of schedule and a miss costs a customer outage, hold. If a hold strands a healthy supply line and the rate is flat and tiny, monitor with a tripwire (Table A.1).

*Principle:* Buy reversibility when uncertainty is high; spend irreversibility only when evidence demands it.

## Choosing measurements

Pick the next measurement by information value per cost and access level, not by instrument prestige (Appendix A.2, Appendix B.1). Climb Level 0--2 until they stop reordering beliefs. Name the decision the measurement unlocks before you request Level 3--4 access.

A good next measurement separates the largest useful hypothesis set. A bad next measurement confirms what you already believe or spends the sample before you know the question.

*Principle:* Measure to unlock an action, not to collect comfort.

## Owning risk

Every product call has an owner, a residual risk statement, and a control. "We are still looking" is not ownership. Containment, correction, and recurrence control are three different jobs; name who holds each one (Appendix A.1, Appendix C.16).

Risk ownership includes saying when monitor-only is correct. Tiny, flat rates with no customer impact can stay on a watch list if the tripwire and review cadence are real. Hope without a tripwire is not a plan.

*Principle:* No decision without an owner, a residual risk line, and a control.

## Evidence vs confidence

Separate observation, correlation, hypothesis, and confirmation. Strong confidence on weak evidence is a junior failure mode; weak confidence on strong evidence is how fleets ship escapes.

Hero samples do not answer ship. Population data, versioned ATP, and a life model do. One failing unit can open FA; it cannot by itself justify a fleet-wide architecture rewrite (Appendix A.2.1, Table 9.2).

*Principle:* Match the strength of the claim to the strength of the evidence.

## Communicating bad news

Bad news travels upward in a fixed frame: problem, impact, evidence, confidence, containment, next decision (Appendix B.3). Lead with the decision leaders must make. Put mechanism depth behind the frame, not in front of it.

Do not soften numbers to protect feelings. Do not bury the hold recommendation in a paragraph of physics. If shipment should stop, say so in the first two sentences, then show the evidence.

*Principle:* Clarity beats comfort. Name the call, then the proof.

## Supplier interactions

Treat supplier conversations like debug with a second party across the table (Appendix B.4, Appendix G.16, Appendix C.10). Scope first: lot, site, date code, plane, condition. Ask for evidence that would change your ship call. Offer the measurements you will accept as closure.

Second sources are not ideology. Qualify them when concentration risk exceeds fleet tolerance, and only on evidence you would trust for the first source (Appendix C.7, Appendix C.17).

*Principle:* Same loop for suppliers as for silicon: scope, evidence, decision, control.

## Fleet thinking

One unit is a story. A lot, rack, vendor, or time trend is a decision. Scope before you generalize (§10.10, Appendix C.9). Telemetry earns its keep only when each field has a decision owner and a reaction plan (Appendix C.14).

Ask what fraction of the population is affected, whether the rate is rising, and whether healthy paths can keep shipping while the bad population is held. Fleet judgment is population math plus reversible containment, not a louder lab story.

*Principle:* Decide on populations and trends, not on anecdotes.

## Avoiding confirmation bias

State the leading hypothesis, then name the observation that would kill it. If you cannot name a falsifier, you are defending a narrative, not running a debug (Appendix A.7, Appendix D).

Prefer measurements that can reorder belief over measurements that decorate the current story. When two mechanisms predict the same symptom, design the cheapest test that splits them. Do not collect three confirming eyes when one power-plane split would end the debate.

*Principle:* Hunt for disproof as hard as you hunt for support.

## Learning from escapes

An escape that passed qual is a process miss, not only a part miss (Appendix C.10, Appendix D.9). Classify it: wrong stress, wrong sample, wrong limit, wrong screen, or wrong assumption about use. Close with a versioned control in ATP, SPC, telemetry, or supplier process so the same path cannot ship tomorrow.

Learning is incomplete until the factory or fleet can catch the mechanism without heroics. FA closure without a production catch is a report, not a fix.

*Principle:* Every escape ends in a named control that would have caught it.

**Key idea.** Junior questions ask what test to run. Senior questions ask what uncertainty remains. Staff questions ask what decision is due and what minimum evidence unlocks it. Use the Staff loop (Appendix A.1), climb access levels on purpose (Appendix A.2), and end every call with owner, residual risk, and control.


<div class="nav-links">
  <a href="ch20-optical-systems-staff-engineer-interview-questions">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch22-abbreviations-and-terminology">Next &rarr;</a>
</div>
