---
layout: default
title: "Appendix M: Interview Cheat Sheets"
---

# Appendix M: Interview Cheat Sheets

Printable one-pagers for fast review before an interview. Each page is a memory trigger, not a substitute for the chapter. Read the goal, walk the checklist, say the answer out loud, then use the pressure pivot.

## Book overview

*Universal rule.* State the decision, name the evidence, explain the tradeoff, and say what you would do next.

##### Lifecycle spine.

Model the link $\rightarrow$ choose the architecture $\rightarrow$ control wavelength and margins $\rightarrow$ establish readiness $\rightarrow$ qualify life $\rightarrow$ validate manufacturing $\rightarrow$ operate the fleet $\rightarrow$ investigate failures.

<table class="book-table"><tr><th>Ch</th><th>Main question</th></tr><tr><td>4</td><td>What sets BER and margin?</td></tr><tr><td>5</td><td>How do the source and modulator behave?</td></tr><tr><td>6</td><td>How do wavelength and WDM stay controlled?</td></tr><tr><td>7</td><td>What evidence is needed before release?</td></tr><tr><td>8</td><td>Will time and exposure cause permanent degradation?</td></tr><tr><td>9</td><td>Can the factory build and control it repeatedly?</td></tr><tr><td>10</td><td>How does optical behavior affect the system and workload?</td></tr><tr><td>11</td><td>How do I find and prevent the real cause of a failure?</td></tr></table>
##### How to use these sheets.

Spend about 2--3 minutes per page. Chapters 7--11 first if time is short. Drill the rapid-fire flashcards at the end of this appendix in one-breath answers. Full depth: Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11.

## Chapter 4: Quantitative link behavior

*Goal.* Explain what sets bit-error rate (BER) and margin without hiding behind a single number.

##### Mental checklist.

Define planes $\rightarrow$ Build budget $\rightarrow$ Add noise $\rightarrow$ Find boundary $\rightarrow$ Measure margin $\rightarrow$ Check assumptions

##### What I need to know.

- BER is an outcome of signal, noise, bandwidth, distortion, and decision behavior.

- Average power alone does not define receiver performance.

- A waterfall shows how performance changes as margin is removed.

- A floor suggests that adding more power may not solve the problem.

- Always state the reference plane and forward-error correction (FEC) condition.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Average optical power</td><td>Receiver sensitivity at a named BER</td></tr><tr><td>Waterfall shift</td><td>Error floor</td></tr><tr><td>Pre-FEC activity</td><td>Post-FEC residual</td></tr></table>
##### Numbers worth remembering.

Margin is the distance from the operating point to the measured failure boundary.

##### Trap.

Trap: Quoting BER without plane, pattern, or FEC condition.\
Better: Name the plane and the BER or FEC objective first.

##### 60-second answer.

"I start by naming the reference plane and the BER or FEC condition. Then I build a simple budget for signal and the main noise or impairment terms, find the failure boundary, and measure how much margin remains. If the waterfall shifts, more power may help. If I see a floor, I look for noise, reflection, or decision limits instead of chasing average power."

##### Pressure.

Pressure: "Our average Rx power looks fine. Why is BER bad?"\
Pivot: "Stable average power rules out gross loss, not timing, noise, or distortion. I would pull a waterfall and check for a floor."

Depth: Chapter 4.

## Chapter 5: Sources and modulation

*Goal.* Choose and operate a source so the modulated link closes the system budget, not just a lab power target.

##### Mental checklist.

Choose source $\rightarrow$ Set operating point $\rightarrow$ Modulate $\rightarrow$ Control temperature $\rightarrow$ Check quality $\rightarrow$ Reserve headroom

##### What I need to know.

- Laser output power is not the same as useful modulated signal.

- Bias, temperature, slope efficiency, extinction, chirp, and bandwidth interact.

- The control loop needs room to respond over temperature and aging.

- The best source closes system, reliability, and manufacturing budgets, not only the best nominal lab result.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>CW launch power</td><td>Modulated OMA / usable signal</td></tr><tr><td>Nominal lab result</td><td>Worst-corner closed budget</td></tr><tr><td>Bias setting</td><td>Remaining control headroom</td></tr></table>
##### Trap.

Trap: Picking the laser with the highest room-temperature power.\
Better: Ask which source still closes margin, reliability, and factory control at the claimed corners.

##### 60-second answer.

"I choose the source from the system budget: reach, modulation, temperature, reliability, and manufacturability. I set bias and temperature with headroom for aging, then check modulated quality, not only CW power. If the loop is already at the stop at one corner, the design is not ready."

##### Pressure.

Pressure: "Why not just raise bias for more power?"\
Pivot: "Bias also moves extinction, chirp, reliability, and headroom. I would show the net margin, not one power number."

Depth: Chapter 5.

## Chapter 6: WDM and wavelength control

*Goal.* Keep channels on the grid across temperature, process, and aging with enough control authority left.

##### Mental checklist.

Set grid $\rightarrow$ Model drift $\rightarrow$ Sense error $\rightarrow$ Correct wavelength $\rightarrow$ Check authority $\rightarrow$ Handle failure

##### What I need to know.

- Wavelength is a control problem, not only a nominal setting.

- Temperature, process, aging, and neighboring channels move the operating point.

- Heater or TEC authority must remain at the worst corner.

- Passing at room temperature does not prove control across life.

- Monitor both wavelength and how hard the loop is working.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Locked flag</td><td>Remaining control headroom</td></tr><tr><td>Room-temp pass</td><td>Life and corner control</td></tr><tr><td>Source drift</td><td>Filter or ring drift</td></tr></table>
##### Trap.

Trap: Treating "locked" as proof of margin.\
Better: Check lock error and actuator demand at the worst claimed corner.

##### 60-second answer.

"I treat wavelength as a closed-loop problem. I name the grid, the drift sources, and the sense/correct path. Then I ask whether the actuator still has room at the hot and aged corners. A lock bit without headroom is not a passing control design."

##### Pressure.

Pressure: "It locks on the bench. Ship it?"\
Pivot: "Not until I see authority and wavelength error across temperature and aging, not only a room-temp lock."

Depth: Chapter 6.

## Chapter 7: Product readiness

*Goal.* Know what evidence is required before release, and which question each stage answers.

##### Mental checklist.

Define $\rightarrow$ Review $\rightarrow$ Bring up $\rightarrow$ Characterize $\rightarrow$ Verify/validate $\rightarrow$ Qualify $\rightarrow$ Validate factory $\rightarrow$ Pilot $\rightarrow$ Ramp $\rightarrow$ Monitor $\rightarrow$ Learn

##### What I need to know.

- Product readiness is the umbrella lifecycle.

- Characterization maps behavior; verification checks frozen requirements.

- System validation proves intended use.

- Reliability qualification and manufacturing validation answer different questions.

- Later evidence cannot replace missing earlier evidence.

- Program labels such as EVT, DVT, and PVT do not define what the evidence proves.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Characterization</td><td>Verification</td></tr><tr><td>System validation</td><td>Reliability qualification</td></tr><tr><td>Manufacturing validation</td><td>Qualification life claim</td></tr><tr><td>Phase label (EVT/DVT/PVT)</td><td>Evidence content</td></tr></table>
##### Trap.

Trap: Using a phase name as proof of readiness.\
Better: Translate the phase into hardware, evidence, open risks, and the exit decision.

##### 60-second answer.

"I start from the claim and the decision gate. Characterization maps the behavior. Verification checks frozen requirements. System validation proves intended use. Qualification and manufacturing validation answer life and factory questions separately. I will not use a later pass to paper over a missing earlier step."

##### Pressure.

Pressure: "We are in PVT. Are we done?"\
Pivot: "PVT is a program label. I ask what evidence exists for the remaining risks and what decision it supports."

Depth: Chapter 7, Table 7.3.

## Chapter 8: Reliability qualification

*Goal.* Build a life or environment claim from mechanism and evidence, not from a copied test list.

##### Mental checklist.

Claim $\rightarrow$ Mechanism $\rightarrow$ Stress $\rightarrow$ Observable $\rightarrow$ Acceptance $\rightarrow$ Samples $\rightarrow$ Confidence $\rightarrow$ Decision $\rightarrow$ Handoff

##### What I need to know.

- Start with the claim and failure mechanism, not a test list.

- The stress must accelerate the field mechanism without creating a different one.

- Separate reversible hot behavior from permanent degradation.

- Zero failures do not mean zero failure rate.

- HTOL is qualification evidence; burn-in is an optional production screen.

- Standards provide methods, not the complete argument.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>HTOL / qual stress</td><td>Production burn-in screen</td></tr><tr><td>Reversible thermal behavior</td><td>Permanent wear-out</td></tr><tr><td>Component FIT</td><td>System availability</td></tr></table>
##### Numbers worth remembering.

One FIT $=1$ failure per $10^9$ device-hours. Zero observed fails still leaves a one-sided upper bound on rate.

##### Trap.

Trap: Saying "we passed GR-468" as the whole reliability argument.\
Better: State the claim, mechanism, stress relevance, sample basis, and residual risk.

##### 60-second answer.

"I start from the life claim and the mechanism. I choose a stress that accelerates that mechanism, define the observable and acceptance rule, then size samples for the confidence I need. Zero fails still leave an upper bound. I handoff production screens only when the screen separates real escapes."

##### Pressure.

Pressure: "Can we skip HTOL if burn-in looks clean?"\
Pivot: "Burn-in is a screen. It does not replace the qualification claim unless the argument explicitly says so."

Depth: Chapter 8.

## Chapter 9: Manufacturing validation

*Goal.* Prove the factory can repeatedly build, measure, and control the released design.

##### Mental checklist.

Freeze $\rightarrow$ Represent $\rightarrow$ Trace $\rightarrow$ Trust measurement $\rightarrow$ Read yield $\rightarrow$ Check stability $\rightarrow$ Measure capability $\rightarrow$ Control $\rightarrow$ FAIR $\rightarrow$ React $\rightarrow$ Ramp

##### What I need to know.

- Freeze the production reference; changes need approval.

- Validate the measurement system before believing yield.

- First-pass yield shows process health; final yield may hide rework.

- Look at the distribution before using capability numbers.

- Stable process first, then $C_p$ and $C_{pk}$.

- FAIR is the controlled first-article evidence package that gates open volume after a relevant tooling, site, material, silicon, assembly, test, or firmware change; evidence depth follows the affected risk.

- Every control needs a trigger, owner, action, and restart rule.

- Passing good units does not prove a screen catches bad ones.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Control limits</td><td>Specification limits</td></tr><tr><td>ATP / acceptance limits</td><td>Specification limits</td></tr><tr><td>First-pass yield</td><td>Final yield</td></tr><tr><td>C_p (spread)</td><td>C_pk (spread and offset)</td></tr></table>
##### Numbers worth remembering.

$C_p$ asks whether the process spread could fit the specification if centered. $C_{pk}$ includes the actual process offset.

##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab / learning build</td><td>Learn and separate variables</td></tr><tr><td>Pilot lot</td><td>Protect lot integrity; collect representative evidence</td></tr><tr><td>Production</td><td>Protect shipments; execute the reaction plan</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Using final yield to hide heavy rework.\
Better: Separate first-pass yield, retest, rework, scrap, and final yield.

##### 60-second answer.

"I freeze the production reference, build a representative population, and clear the measurement system before I trust yield. I look at first-pass yield and the distribution, establish stability, then interpret $C_p$ or $C_{pk}$. Controls need owners and reaction plans. I ramp only when evidence supports the next volume."

##### Pressure.

Pressure: "Final yield is 99%. Ship?"\
Pivot: "Not until I know first-pass yield and what the recovery path is costing and hiding."

Depth: Chapter 9, Table 9.3, Appendix G.5.

## Chapter 10: Optical links in operation

*Goal.* Connect physical margin to FEC, recovery, workload impact, and fleet decisions.

##### Mental checklist.

Observe $\rightarrow$ Read FEC $\rightarrow$ Find bursts $\rightarrow$ Check recovery $\rightarrow$ Use telemetry $\rightarrow$ Compare cohorts $\rightarrow$ Judge impact $\rightarrow$ Contain

##### What I need to know.

- Link-up is not the same as link health.

- Corrected errors can reveal shrinking margin before traffic fails.

- Average BER can hide short bursts.

- Recovery time and repeated retrains matter.

- Telemetry is useful when it separates a cause or changes an action.

- Component failure rate is not system availability.

- At fleet scale, a rare per-link event may happen frequently.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Link-up</td><td>Link health over time</td></tr><tr><td>Corrected-error rise</td><td>Service already failing</td></tr><tr><td>Component FIT</td><td>Fleet event rate and availability</td></tr></table>
##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab</td><td>Learn and reproduce</td></tr><tr><td>Pilot</td><td>Bound exposure; keep observability</td></tr><tr><td>Production fleet</td><td>Protect the workload; contain first</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Treating a link as healthy because it is up.\
Better: Check corrected errors, bursts, retrains, and recovery time.

##### 60-second answer.

"Link-up is a state; health is a distribution over time. I read FEC activity for consumed margin, look for bursts, and check recovery duration and repeats. I use telemetry that separates hypotheses, compare affected and unaffected groups, and judge severity from workload impact. Component FIT alone is not availability."

##### Pressure.

Pressure: "Post-FEC looks clean. Why worry?"\
Pivot: "Clean post-FEC can still hide rising corrected-error demand and short bursts. I would inspect those distributions before calling the link healthy."

Depth: Chapter 10.

## Chapter 11: Failure analysis

*Goal.* Find the real cause without destroying the evidence, then stop it from happening again.

##### Mental checklist.

Protect $\rightarrow$ Preserve $\rightarrow$ Scope $\rightarrow$ Classify $\rightarrow$ Hypothesize $\rightarrow$ Test $\rightarrow$ Prove $\rightarrow$ Fix $\rightarrow$ Prevent $\rightarrow$ Verify

##### What I need to know.

- Do not reset, clean, or swap before preserving evidence.

- A symptom is not a cause.

- Timing helps: sudden, gradual, or intermittent.

- Shared failures suggest a shared dependency.

- Use reversible tests first.

- A swap can isolate ownership without proving the physical mechanism.

- It is acceptable to say the mechanism is not yet confirmed.

- The case is not closed until recurrence control works on fresh data.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Failure mode / symptom</td><td>Failure mechanism</td></tr><tr><td>Correction</td><td>Recurrence control</td></tr><tr><td>Ownership from a swap</td><td>Microscopic proof</td></tr></table>
##### Context.

<table class="book-table"><tr><th>Context</th><th>First priority</th></tr><tr><td>Lab</td><td>Learn quickly and reproduce</td></tr><tr><td>Vetting or pilot lot</td><td>Protect lot integrity; collect representative evidence</td></tr><tr><td>Production fleet</td><td>Protect the workload; avoid disruptive tests until safe</td></tr></table>
Same flow, different first priority.

##### Trap.

Trap: Reseating first, or closing when the unit recovers.\
Better: Preserve state, then close only after a recurrence control works on fresh data.

##### 60-second answer.

"I start by protecting the workload and preserving the failing state. Then I scope the issue by lane, module, host, lot, firmware, and site. I build a short list of likely causes and use the smallest safe test, often a controlled swap, to see what the problem follows. I do not call root cause from one correlation. Once the cause is supported, I fix the immediate issue, put in a control to prevent recurrence, and verify it on fresh data."

##### Pressure.

Pressure: "What if it is in production and you cannot swap anything?"\
Pivot: "I protect the workload and collect non-disruptive evidence first. I schedule intrusive tests only after traffic is drained or risk is contained."

Depth: Chapter 11, Appendix I.

## Cross-chapter interview habits

##### How to answer technical questions.

1.  Start with the decision or distinction.

2.  State what you would check first.

3.  Explain why that check is high value.

4.  Name the main tradeoff.

5.  Say what result would change your direction.

6.  Avoid claiming more than the evidence supports.

7.  End with the action or release decision.

##### Useful phrases.

- "The first thing I would separate is..."

- "I would not interpret that result until..."

- "That raises a hypothesis, but it does not prove the cause."

- "I would choose the cheapest safe test that separates the leading causes."

- "The same measurement can support several claims, but the decision is different."

- "I would protect the workload first, then preserve enough evidence to investigate."

- "I would not call the case closed until the fix works on fresh data."

##### Universal traps.

- Jumping from correlation to cause.

- Quoting a number without plane or condition.

- Treating pass/fail as margin.

- Treating a standard as the complete engineering argument.

- Assuming a passing sample represents the whole population.

- Treating link-up as health.

- Treating final yield as process health.

- Fixing the failed unit without preventing recurrence.

*Design rule.* One page, one mental model, one spoken answer.

## Chapters 7--11: 100 rapid-fire interview flashcards

Use these as short memory prompts. Say the answer in one breath, then expand only if asked. Depth: Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11.

### Chapter 7: Product readiness

1.  **Q:** What is product readiness?\
    **A:** The full path from requirements to fleet learning.

2.  **Q:** What is the first step?\
    **A:** Define measurable requirements and the release decision.

3.  **Q:** Why review architecture early?\
    **A:** Catch thin margins before hardware makes changes expensive.

4.  **Q:** What does bring-up prove?\
    **A:** The hardware, firmware, states, and basic link work reproducibly.

5.  **Q:** What does characterization do?\
    **A:** Maps nominal behavior, spread, sensitivities, and failure edges.

6.  **Q:** What does verification do?\
    **A:** Checks frozen requirements at named planes and conditions.

7.  **Q:** What does system validation do?\
    **A:** Proves the product works in the intended system and workload.

8.  **Q:** What does reliability qualification do?\
    **A:** Supports life and environmental claims.

9.  **Q:** What does manufacturing validation do?\
    **A:** Proves the factory can build and control the design repeatedly.

10. **Q:** What is a pilot?\
    **A:** A bounded field experiment with telemetry, exit rules, and rollback.

11. **Q:** What justifies pilot expansion?\
    **A:** Metrics match the release model and no unexplained cohort appears.

12. **Q:** What makes a later test insufficient?\
    **A:** It cannot replace missing earlier evidence.

13. **Q:** What do EVT, DVT, and PVT mean?\
    **A:** Program phases, not universal proof categories.

14. **Q:** How do you interpret a phase gate?\
    **A:** Ask which build, which evidence, which risks, and which decision.

15. **Q:** Why not validate only on a reference host?\
    **A:** Production hosts can move the real failure edge.

16. **Q:** What must accompany every measurement?\
    **A:** Plane, metric, conditions, population, uncertainty, and decision.

17. **Q:** How do you choose the next test?\
    **A:** Pick the cheapest safe test that separates the leading causes.

18. **Q:** When is destructive analysis justified?\
    **A:** When non-destructive evidence cannot unblock a major decision.

19. **Q:** What do you protect when schedule is cut?\
    **A:** Requirements, measurement integrity, thin margins, and reversible pilot.

20. **Q:** Best one-line readiness summary?\
    **A:** Define, prove, qualify, control, pilot, ramp, monitor, learn.

### Chapter 8: Reliability qualification

21. **Q:** What is reliability qualification?\
    **A:** A bounded confidence argument for life and environmental exposure.

22. **Q:** What is the first step in a qual plan?\
    **A:** Start with the claim, not the test list.

23. **Q:** What comes after the claim?\
    **A:** Identify the mechanism that could break it.

24. **Q:** What makes an accelerated stress useful?\
    **A:** It speeds up the same mechanism expected in the field.

25. **Q:** What makes a stress invalid?\
    **A:** It creates different failure physics.

26. **Q:** Why define observables before stress?\
    **A:** So acceptance is not invented after seeing the data.

27. **Q:** Why use representative samples?\
    **A:** One convenient lot does not represent the released population.

28. **Q:** What does zero failures prove?\
    **A:** A confidence bound, not a zero failure rate.

29. **Q:** What is FIT?\
    **A:** One failure per billion device-hours.

30. **Q:** What must accompany a FIT claim?\
    **A:** Population, exposure, failure definition, model, and confidence.

31. **Q:** What is DPPM?\
    **A:** Defective parts per million at a named quality boundary.

32. **Q:** FIT versus DPPM?\
    **A:** FIT uses time exposure; DPPM uses units inspected.

33. **Q:** HTOL versus burn-in?\
    **A:** HTOL supports life claims; burn-in is an optional production screen.

34. **Q:** Can burn-in replace qualification?\
    **A:** No.

35. **Q:** Can qualification replace screening?\
    **A:** No.

36. **Q:** What is a failure mode?\
    **A:** What you observe.

37. **Q:** What is a failure mechanism?\
    **A:** The physical or electrical cause.

38. **Q:** Why does failure timing matter?\
    **A:** Early, random, and late failures point to different risks.

39. **Q:** What is the role of standards like GR-468?\
    **A:** Common methods and language, not the whole engineering argument.

40. **Q:** Best one-line qual summary?\
    **A:** Claim, mechanism, stress, observable, sample, confidence, decision.

### Chapter 9: Manufacturing validation

41. **Q:** What does manufacturing validation prove?\
    **A:** The factory can build, measure, trace, and control the design.

42. **Q:** What do you freeze first?\
    **A:** Design, BOM, process, firmware, test software, and approved suppliers.

43. **Q:** Why freeze the production reference?\
    **A:** So changes are visible and traceable.

44. **Q:** What is FAIR?\
    **A:** First Article Inspection Report.

45. **Q:** What does FAIR prove?\
    **A:** The first production-intent units match the released design and process.

46. **Q:** What is MSA?\
    **A:** Measurement System Analysis.

47. **Q:** What is GR&R?\
    **A:** Gauge repeatability and reproducibility.

48. **Q:** What does GR&R ask?\
    **A:** Is the variation from the parts or from the measurement?

49. **Q:** What comes before yield interpretation?\
    **A:** Trust the measurement system.

50. **Q:** What is first-pass yield?\
    **A:** Units passing without retest or rework.

51. **Q:** Why is first-pass yield important?\
    **A:** It shows true process health.

52. **Q:** What is final yield?\
    **A:** Units eventually accepted after allowed rework and retest.

53. **Q:** Why can final yield mislead?\
    **A:** It can hide heavy rework and unstable process behavior.

54. **Q:** What is a Pareto chart?\
    **A:** A ranked view of the few causes driving most loss.

55. **Q:** Distribution versus capability?\
    **A:** Distribution is the raw shape; capability compares it with specs.

56. **Q:** What is process stability?\
    **A:** The process behaves predictably over time.

57. **Q:** Why must stability come before $C_{pk}$?\
    **A:** An unstable process makes capability numbers unreliable.

58. **Q:** $C_p$ versus $C_{pk}$?\
    **A:** $C_p$ is potential spread; $C_{pk}$ includes how off-center the process is.

59. **Q:** Control limit versus spec limit?\
    **A:** Control limits describe process behavior; specs define product acceptance.

60. **Q:** What is ATP?\
    **A:** The production acceptance test used to ship, hold, or reject units.

61. **Q:** How do you validate an ATP test?\
    **A:** Show it catches known bad cases, not just good units.

62. **Q:** What is a false accept?\
    **A:** A bad unit passes.

63. **Q:** What is a false reject?\
    **A:** A good unit fails.

64. **Q:** How do you set a production threshold?\
    **A:** Balance escapes, false rejects, cost, and customer risk.

65. **Q:** What is SPC?\
    **A:** Statistical Process Control for detecting drift over time.

66. **Q:** What must every reaction plan include?\
    **A:** Trigger, owner, containment, evidence, restart rule, and follow-up.

67. **Q:** Where should a defect be caught?\
    **A:** At the earliest reliable and economical point.

68. **Q:** How do you choose builds?\
    **A:** Cover real sources of variation and keep genealogy.

69. **Q:** Representation versus sample size?\
    **A:** First sample the right populations, then collect enough data.

70. **Q:** Best one-line manufacturing summary?\
    **A:** Freeze, trace, trust measurement, read yield, control, react, ramp.

### Chapter 10: Optical links in operation

71. **Q:** What is the chapter's main message?\
    **A:** Link-up is not the same as link health.

72. **Q:** What does pre-FEC error activity show?\
    **A:** The burden on the physical link before correction.

73. **Q:** What do corrected errors show?\
    **A:** FEC is working and margin may be shrinking.

74. **Q:** What do uncorrectable events show?\
    **A:** FEC could not recover the data.

75. **Q:** What is a retrain?\
    **A:** A recovery action that rebuilds link or lane state.

76. **Q:** Why can average BER mislead?\
    **A:** It can hide short, dangerous bursts.

77. **Q:** What should you ask about an error burst?\
    **A:** How big, how long, and what event it triggered.

78. **Q:** What is operational severity based on?\
    **A:** Workload consequence, not just optical symptoms.

79. **Q:** What does good recovery look like?\
    **A:** Fast, predictable, evidence-preserving, and not repetitive.

80. **Q:** Why is recovery part of product behavior?\
    **A:** A link will eventually hit faults and must return safely.

81. **Q:** What makes telemetry useful?\
    **A:** It separates causes, bounds a population, or triggers action.

82. **Q:** What is a cohort?\
    **A:** A group sharing lot, host, firmware, site, or another attribute.

83. **Q:** Why compare affected and unaffected cohorts?\
    **A:** To narrow the shared cause.

84. **Q:** Does correlation prove root cause?\
    **A:** No.

85. **Q:** Why can a rare event matter at fleet scale?\
    **A:** Large populations turn rare per-link events into frequent fleet events.

86. **Q:** Why is FIT not availability?\
    **A:** Availability also depends on duration, redundancy, reroute, and repair.

87. **Q:** What makes a pilot real?\
    **A:** Bounded exposure, telemetry, exit rules, and rollback.

88. **Q:** When do you pause deployment?\
    **A:** When risk is widening, unexplained, or hard to contain.

89. **Q:** What is the T1-to-T5 memory hook?\
    **A:** Trust measurement, know product, find edge, connect lab to system, monitor fleet.

90. **Q:** Best one-line operations summary?\
    **A:** Watch margin, FEC, bursts, recovery, cohorts, and workload impact.

### Chapter 11: Failure analysis

91. **Q:** What is the first priority in production?\
    **A:** Protect the workload, then preserve evidence.

92. **Q:** What is the failure-analysis spine?\
    **A:** Protect, preserve, scope, classify, test, prove, fix, prevent, verify.

93. **Q:** Why preserve before resetting?\
    **A:** Resets can erase the clues.

94. **Q:** What does scoping mean?\
    **A:** Find who is affected and what they share.

95. **Q:** What timing patterns matter?\
    **A:** Sudden, gradual, or intermittent.

96. **Q:** What is a hypothesis tree?\
    **A:** A short list of plausible causes and how to separate them.

97. **Q:** Why use reversible swaps first?\
    **A:** They localize ownership with low risk.

98. **Q:** If the fault follows the module, is root cause proven?\
    **A:** No. Ownership is localized; mechanism still needs proof.

99. **Q:** Correlation versus root cause?\
    **A:** Correlation moves together; root cause is reproducible and stoppable.

100. **Q:** When is the case closed?\
     **A:** When the fix works on fresh data and recurrence is controlled.

### Five universal fallback lines

- "I would start by clarifying the decision."

- "I would not interpret that number without the plane and conditions."

- "That raises a hypothesis, but it does not prove the cause."

- "I would pick the smallest safe test that separates the leading causes."

- "Based on the evidence, here is my call and next step."


<div class="nav-links">
  <a href="ch23-abbreviations-and-terminology">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch25-references">Next &rarr;</a>
</div>
