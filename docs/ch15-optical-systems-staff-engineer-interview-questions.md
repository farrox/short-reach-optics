---
layout: default
title: "Ch 15: Optical Systems Staff Engineer Interview Questions"
---

# 15 Optical Systems Staff Engineer Interview Questions

Index only. Each item is one speakable question plus a pointer to the worked answer, playbook, or chapter home. Do not invent new topics here; expand in those homes.

## Debugging

1.  Pre-FEC BER rose while average received power held steady. How do you debug it? fw:ber-stable-power, interview-worked-sensitivity

2.  Received power decreased. What do you check first? fw:power-down, tree-power-fork

3.  A single lane is weak in a multi-lane module. How do you isolate it? fw:weak-lane, interview-worked-lane

4.  BER worsens at high temperature but average power is stable. What next? fw:hot-fail, interview-worked-hot-ber, case-hot-ber

5.  The failure is intermittent. How do you scope and trap it? fw:intermittent, tree-time-behavior

## Validation

6.  How would you validate a new optical transmitter from bring-up through margin? fw:validation-plan, interview-worked-validation, Table ladder

7.  How would you set laser requirements for a new IM/DD link? interview-worked-laser-reqs, Table laser-prd

8.  Received power is unchanged but required receiver power increased. Why? interview-worked-sensitivity, interview-waterfall

9.  Why can a link show a BER floor that more launch power does not fix? fw:ber-floor, interview-worked-ber-floor

10. Which measurement do you choose next when access is limited? interview-access-levels, case-info-value

## Qualification

11. How do you build a qualification plan that maps mechanisms to stress? fw:qual-plan, tree-qual-evidence, qual-planning-matrix

12. What makes an HTOL projection credible? interview-worked-htol, Ch. reliability

13. How do you distinguish laser aging from calibration drift? fw:aging-vs-cal, interview-worked-aging-vs-cal

14. A field escape passed qual. How do you classify the miss? fw:supplier-escape, tree-escape

15. What evidence closes a qualification decision? tree-qual-evidence, tree-decision-closure

## Manufacturing

16. When would you update ATP after a field or lab escape? fw:atp-update, tree-production-loop

17. Which data must an automated test save so a failure can be replayed? interview-worked-test-data

18. How do you decide whether a field issue is performance, reliability, or manufacturability? interview-worked-triage-class

19. What would you put in fleet telemetry, and why? fw:telemetry, interview-worked-telemetry, fw:fleet

20. You do not know the mechanism yet. What do you decide anyway? fw:unknown, tree-unknown

## Supplier

21. How would you qualify a second laser or PIC supplier? fw:second-component, interview-worked-second-source

22. How would you qualify a second transceiver or cable-assembly supplier? fw:second-module, tree-supplier

23. A supplier lot looks correlated with a fleet cohort. What do you do? fw:fleet, case-fleet-ber, tree-scope-population

## Architecture

24. When would you choose an EML, silicon MZM, or ring modulator? interview-worked-modulator, Chapter 3

25. How do optics choices constrain AI datacenter networking cost and power? Ch. networking, Chapter 1

**Key idea.** Speak the question home first: scope, ledger, measurement, decision, control. Then open the matching playbook only if the interviewer asks for depth.


<div class="nav-links">
  <a href="ch14-engineering-decision-trees">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch16-how-staff-engineers-think">Next &rarr;</a>
</div>
