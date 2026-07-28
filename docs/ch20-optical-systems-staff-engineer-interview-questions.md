---
layout: default
title: "Ch 20: Optical Systems Staff Engineer Interview Questions"
---

# 20 Optical Systems Staff Engineer Interview Questions

Index only. Each item is one speakable question plus a pointer to the worked answer, playbook, or chapter home. Do not invent new topics here; expand in those homes.

## Debugging

1.  Pre-FEC BER rose while average received power held steady. How do you debug it? Appendix C.1, Appendix A.10.7

2.  Received power decreased. What do you check first? Appendix C.2, Appendix D.4

3.  A single lane is weak in a multi-lane module. How do you isolate it? Appendix C.3, Appendix A.10.6

4.  BER worsens at high temperature but average power is stable. What next? Appendix C.4, Appendix A.10.3, Appendix B.7

5.  The failure is intermittent. How do you scope and trap it? Appendix C.12, Appendix D.6

## Validation

6.  How would you validate a new optical transmitter from bring-up through margin? Appendix C.8, Appendix A.10.2, Table 7.3

7.  How would you set laser requirements for a new IM/DD link? Appendix A.10.1, Table 5.4

8.  Received power is unchanged but required receiver power increased. Why? Appendix A.10.7, Appendix A.8.9

9.  Why can a link show a BER floor that more launch power does not fix? Appendix C.11, Appendix A.10.8

10. Which measurement do you choose next when access is limited? Appendix A.2, Appendix B.1

## Qualification

11. How would you qualify reliability? Chapter 8, Appendix C.15, Appendix D.3

12. How do you build a qualification plan that maps mechanisms to stress? Appendix C.15, Appendix D.3, Appendix F.4

13. What makes an HTOL projection credible? Appendix A.10.9, Chapter 8

14. How do you distinguish laser aging from calibration drift? Appendix C.5, Appendix A.10.4

15. What evidence closes a qualification decision? Appendix D.3, Appendix D.16

## Manufacturing

16. How would you validate manufacturing? Chapter 9, Table 9.1, Table G.1

17. How would you respond to a yield drop? Chapter 9, §9.12, Chapter 11

18. When would you update ATP after a field or lab escape? Appendix C.13, Appendix D.13, §9.11

19. Which data must an automated test save so a failure can be replayed? Appendix A.10.10, Chapter 9

20. How do you decide whether a field issue is performance, reliability, or manufacturability? Appendix A.10.12, Table 9.1

## Supplier

21. How would you qualify a second laser or PIC supplier? Appendix C.6, Appendix A.10.5, Chapter 9, Chapter 8

22. How would you qualify a second transceiver or cable-assembly supplier? Appendix C.7, Appendix D.8, Chapter 9

23. A supplier lot looks correlated with a fleet cohort. What do you do? Appendix C.9, Appendix B.5, Appendix D.5

## Architecture

24. When would you choose an EML, silicon MZM, or ring modulator? Appendix A.10.11, Chapter 3

25. How do optics choices constrain AI datacenter networking cost and power? Chapter 10, Chapter 1

**Key idea.** Speak the question home first: scope, ledger, measurement, decision, control. Then open the matching playbook only if the interviewer asks for depth.


<div class="nav-links">
  <a href="ch19-ai-fabric-context">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch21-how-staff-engineers-think">Next &rarr;</a>
</div>
