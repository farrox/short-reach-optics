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

<table class="book-table"><tr><th>Ch</th><th>Main question</th></tr><tr><td>4</td><td>PAM4 versus PAM8: baud relief versus vertical cost?</td></tr><tr><td>5</td><td>FFE versus DFE: which impairment, which risk?</td></tr><tr><td>6</td><td>What sets BER and margin?</td></tr><tr><td>7</td><td>How do the source and modulator behave?</td></tr><tr><td>8</td><td>How do wavelength and WDM stay controlled?</td></tr><tr><td>9</td><td>2.5D versus 3D / CPO: which integration, which risk?</td></tr><tr><td>10</td><td>How does a sound design become a controlled product?</td></tr><tr><td>11</td><td>How do I find and prevent the real cause of a failure?</td></tr></table>
##### How to use these sheets.

Spend about 2--3 minutes per page. Prefer the PAM4 versus PAM8, FFE versus DFE, and 2.5D versus 3D/CPO sheets, then models through WDM, productization, and failure analysis. The productization flashcards at the end are a secondary reference bank, not the primary study set. Full depth: Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11.

## PAM4 versus PAM8

*Goal.* Explain why denser PAM lowers baud and raises SNR, linearity, and calibration burden.

##### Mental checklist.

Bits per symbol $\rightarrow$ Baud $\rightarrow$ Level spacing $\rightarrow$ Gray coding $\rightarrow$ Linearity $\rightarrow$ Where PAM is generated $\rightarrow$ FEC/EQ bill $\rightarrow$ Keep or reject PAM8

##### What I need to know.

- $R_s=R_b/\log_2 M$: PAM4 is 2 bits/symbol; PAM8 is 3.

- Same total swing: PAM4 spacing is $1/3$; PAM8 is $1/7$.

- Gray coding makes nearest-level mistakes one-bit errors; SER $\neq$ BER.

- Outer OMA is $P_3-P_0$ (PAM4) or $P_7-P_0$ (PAM8), not an inner eye.

- PAM8 needs seven thresholds and tighter DAC/driver/modulator linearity.

- Baud relief is worthless if linearity, FEC power, or calibration fails.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Bit rate</td><td>Baud (symbol rate)</td></tr><tr><td>Outer OMA</td><td>Inner-eye quality / RLM</td></tr><tr><td>Ideal spacing dB</td><td>Finished link sensitivity penalty</td></tr><tr><td>PAM8 roadmap slogan</td><td>Closed SNR and linearity budget</td></tr></table>
##### Trap.

Trap: "PAM8 is better because it is higher-order modulation."\
Better: "PAM8 buys baud relief and spends vertical margin, linearity, and calibration."

##### 60-second answer.

"At a fixed bit rate, PAM8 cuts baud to about one-third of the bit rate, so the channel bandwidth demand drops. The cost is seven eyes and one-seventh level spacing for the same outer swing, so SNR, linearity, threshold calibration, and often FEC get harder. I only choose PAM8 when that baud relief outweighs the bill."

##### Pressure.

Pressure: "Outer OMA looks fine. Why is PAM8 failing?"\
Pivot: "Outer OMA does not prove inner-eye spacing or modulator linearity. I would inspect level uniformity and compression next."

Depth: Chapter 4, §6.6, §3.9.

## FFE versus DFE

*Goal.* Pick equalization from the impairment, not from the acronym.

##### Mental checklist.

Channel response $\rightarrow$ Precursor vs postcursor $\rightarrow$ CTLE tilt $\rightarrow$ TX vs RX FFE $\rightarrow$ DFE only if postcursor remains $\rightarrow$ Noise / error propagation $\rightarrow$ FEC cost $\rightarrow$ Stop if nonlinear

##### What I need to know.

- FFE filters samples; DFE filters past decisions.

- Precursor needs FFE or TX pre-emphasis; DFE cannot fix precursor.

- FFE can enhance noise; DFE can propagate errors.

- TX FFE does not amplify RX noise; RX FFE can.

- Pegged taps mean the channel or optic is outside EQ authority.

- Open eye with bad BER: check adaptation, thresholds, and bursts.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>TX FFE</td><td>RX FFE</td></tr><tr><td>Precursor ISI</td><td>Postcursor ISI</td></tr><tr><td>Noise enhancement</td><td>Error propagation</td></tr><tr><td>Reference DFE in a standard</td><td>Your product DFE health</td></tr></table>
##### Trap.

Trap: "Max EQ on every lane."\
Better: "Tune until residual ISI falls without driving FEC demand up."

##### 60-second answer.

"I start from precursor and postcursor. CTLE fixes smooth tilt. FFE handles linear pre- and post-cursor ISI. DFE helps remaining postcursor if decisions are solid. I keep TX pre-emphasis separate from RX EQ, watch noise enhancement and error propagation, and stop when the problem is nonlinearity or noise, not ISI."

##### Pressure.

Pressure: "The eye is open. Why is BER bad?"\
Pivot: "I check sampling phase, thresholds, adaptation lock, and bursts. An open scope eye can still hide decision errors."

Depth: Chapter 5, §5.1, §3.7.

## Chapter 6: Quantitative link behavior

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

Depth: Chapter 6.

## Chapter 7: Sources and modulation

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

Depth: Chapter 7.

## Chapter 8: WDM and wavelength control

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

Depth: Chapter 8.

## 2.5D versus 3D / CPO

*Goal.* Pick packaging from reach, thermal, yield, and service, not from the densest stack acronym.

##### Mental checklist.

Placement (pluggable / NPO / CPO) $\rightarrow$ 2.5D vs 3D $\rightarrow$ Laser location $\rightarrow$ Thermal partition $\rightarrow$ FAU / optical I/O $\rightarrow$ KGD and yield $\rightarrow$ Field replaceables $\rightarrow$ Test stages

##### What I need to know.

- 2.5D is side-by-side; 3D is stacked.

- CPO is engine placement, not automatically 3D.

- External lasers often enable CPO by moving FIT and heat.

- FAU attach and dark lanes are first-class scrap risks.

- Stack yield multiplies; screen before irreversible attach.

- Serviceability must match the reliability model.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>CPO</td><td>3D hybrid bonding</td></tr><tr><td>2.5D</td><td>``Almost 3D''</td></tr><tr><td>Case temperature</td><td>Local hotspot / ring walk</td></tr><tr><td>Package density</td><td>Closed thermal and yield story</td></tr></table>
##### Trap.

Trap: "Ship the densest COUPE-like stack."\
Better: "Name placement, stack style, laser service, and FAU yield evidence."

##### 60-second answer.

"I decide if CPO is needed from reach and port density. I choose 2.5D or 3D from thermal access, KGD, and optical I/O. I place lasers for life and field replacement, often external. I screen attach before seal, co-design XSR with the ASIC, and I freeze only when yield and service match the fleet."

##### Pressure.

Pressure: "Competitors shipped CPO. Why wait?"\
Pivot: "Shipping proves a recipe can work. I still need our thermal partition, FAU yield, and replaceable-laser story."

Depth: Chapter 9, Table H.4, §7.14, Appendix H.10.

## Chapter 10: Productization and fleet readiness

   

*Goal.* Show that a technically sound architecture becomes a controlled product with named residual risk.

##### Mental checklist.

Define $\rightarrow$ Characterize $\rightarrow$ Validate $\rightarrow$ Qualify $\rightarrow$ Control factory $\rightarrow$ Pilot $\rightarrow$ Monitor

##### What I need to know.

- One lifecycle, not five separate subjects.

- Characterization maps behavior; system validation proves intended use.

- Qualification is claim, mechanism, stress, observable, confidence.

- Factory readiness needs measurement trust, first-pass yield, and controls.

- A pilot needs bounded exposure, telemetry, exit rules, and rollback.

- Link-up is not link health.

- Later evidence cannot replace missing earlier evidence.

##### Key distinctions.

<table class="book-table"><tr><th>Do not confuse</th><th>With</th></tr><tr><td>Characterization</td><td>System validation</td></tr><tr><td>HTOL / qual stress</td><td>Production burn-in</td></tr><tr><td>First-pass yield</td><td>Final yield</td></tr><tr><td>Phase label (EVT/DVT/PVT)</td><td>Evidence content</td></tr></table>
##### Trap.

Trap: Reciting readiness terminology instead of naming the decision and residual risk.\
Better: State the claim, the evidence, the thin margin, and the next gate.

##### 60-second answer.

"I define the claim and planes, close the architecture, characterize margins, verify requirements, validate intended use, qualify the dominant life mechanisms, prove the factory can measure and control the design, run a bounded pilot with rollback, then ramp while monitoring cohorts."

##### Pressure.

Pressure: "Schedule is cut. What do you protect?"\
Pivot: "Requirements and planes, measurement integrity, thin margins, dominant life mechanisms, factory controls, and a reversible pilot."

Depth: Chapter 10, Table 10.2, Appendix F, Appendix G.

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

## Secondary bank: productization rapid-fire flashcards

Secondary reference only. The primary productization interview set is the eight questions in §10.14. Use these cards if you need extra one-breath drills after the architecture chapters. Depth: Chapter 10, Chapter 11, Appendix F, Appendix G.

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
