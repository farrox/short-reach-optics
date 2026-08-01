---
layout: default
title: "Ch 22: Optical Systems Staff Engineer Interview Questions"
---

# 22 Optical Systems Staff Engineer Interview Questions

Index only. Each item is one speakable question plus a pointer to the worked answer, playbook, or chapter home. Do not invent new topics here; expand in those homes. Architecture and PHY judgment come first. Validation, qualification, manufacturing, and supplier drills live in the productization Q&As, App M secondary flashcards, and their appendix homes.

## PAM4 / PAM8 and quantitative link

1.  When is PAM8 preferable to higher-baud PAM4? Chapter 4

2.  At fixed bit rate, how do NRZ, PAM4, and PAM8 baud and SNR trade? Chapter 4, Chapter 6

3.  Outer OMA looks fine but the link fails. What do you check next? Chapter 4, Appendix A.10.7

4.  Walk a short-reach link budget from launch to pre-FEC BER. Chapter 3, Appendix E.5, Chapter 6

## Equalization

5.  When do you use FFE versus DFE, and what can each correct? Chapter 5

6.  TX FFE versus RX FFE: who owns what, and why? Chapter 5, §3.7

7.  What does CTLE buy, and where does it fail? Chapter 5

8.  How does equalization change for PAM8 versus PAM4? Chapter 5, Chapter 4

## Laser / source / modulator

9.  When would you choose an EML, silicon MZM, or ring modulator? Appendix A.10.11, Chapter 3, Chapter 7

10. How would you set laser requirements for a new IM/DD link? Appendix A.10.1, Table 7.4

11. Why can a link show a BER floor that more launch power does not fix? Appendix C.11, Appendix A.10.8

12. How do you distinguish laser aging from calibration drift? Appendix C.5, Appendix A.10.4

## Packaging / CPO

13. Compare 2.5D, 3D, and CPO without treating them as synonyms. Chapter 9

14. When do you choose pluggable, LPO, or CPO? Chapter 9, Table H.4, Appendix H.5.1

15. Where should the lasers live for a CPO engine, and why? Chapter 9, §7.14, Chapter 7

16. How does packaging change the field-replaceable unit and FIT story? Chapter 9, Chapter 11

## HPC / rack / fabric

17. Walk a 64-accelerator, two-rail rack design. Chapter 10, §10.6

18. How does topology determine optical module, laser, power, and failure exposure? Chapter 10, §10.7

19. When is oversubscription acceptable in a collective-heavy fabric? Chapter 10, §10.13

20. Scale-up versus scale-out: what changes for optics? Chapter 10, Appendix H.1

## Debugging

21. Pre-FEC BER rose while average received power held steady. How do you debug it? Appendix C.1, Appendix A.10.7

22. A single lane is weak in a multi-lane module. How do you isolate it? Appendix C.3, Appendix A.10.6

23. BER worsens at high temperature but average power is stable. What next? Appendix C.4, Appendix A.10.3, Appendix B.7

## Productization

24. How would you validate a new optical transmitter from bring-up through margin? Appendix C.8, Appendix A.10.2, Table 11.2

25. How do you decide whether a field issue is performance, reliability, or manufacturability? Appendix A.10.12, Table G.3

**Key idea.** Lead with architecture and PHY judgment: signaling, equalization, sources, packaging, and fabric. Speak the question home first, then open the matching playbook only if the interviewer asks for depth. Readiness and supplier detail stay secondary unless the role is explicitly lifecycle-led.


<div class="nav-links">
  <a href="ch21-failure-analysis-reference">&larr; Previous</a>
  <a href="./">Table of Contents</a>
  <a href="ch23-how-staff-engineers-think">Next &rarr;</a>
</div>
