# Manuscript QA Report

**Draft checked:** `AEGISOPS_RESEARCH_PAPER.md`  
**Date:** 2026-10-16 (Asia/Kolkata)

## Completed checks

| Check | Result |
| --- | --- |
| Required manuscript, figure register, claim map, reference audit, QA report, and readiness report exist | Pass |
| Main-paper figure paths A, B, C, D, E1, E2, E4, E5, E6, and F exist | Pass |
| Figure E3 is identified as supplementary and its path exists | Pass |
| Table 1 counts match current raw A predictions | Pass: Rules 120/0/200/0; IF 57/4/196/63; LSTM and Combined 120/2/198/0 |
| A population and statistical qualification | Pass: 320 windows, six scenarios, b=63, c=0, exact p approximately 2.1684e-19, exploratory six-scenario result |
| B denominators and omissions | Pass: 42 records, seven configurations × six cases, C5 and C7 ITT omissions retained |
| C counts and intervals | Pass: 11/11 attack containment [0.7412, 1.0000]; 16/16 audit completeness [0.8064, 1.0000] |
| Live boundary | Pass: 200 rows, all bootstrap rules, all scores null, zero live-LSTM-scored rows |
| Experiment D boundary | Pass: provenance only; no predictions, metrics, ratification, or external result claimed |
| Citation keys and bibliography | Pass: numeric citations 1–16 are represented once in References; related-work claim scope checked against Phase 5 audit |
| Unsupported claims | Pass: no affirmative live-LSTM, external-generalization, LLM-superiority, authenticated-dual-control, NIST-compliance, production-security, or autonomous-recovery claim retained |

## Known limitations not resolved by writing

- Author, affiliation, and venue metadata are placeholders.
- AnoMod publisher-page metadata requires a final publisher confirmation; the arXiv primary record is cited with that limitation.
- The repository worktree remains dirty and historical integrity material is stale; this manuscript update does not establish a release snapshot.
- Live LSTM and Experiment D remain evidence gaps, not manuscript defects that can be repaired by editing.
- Markdown source was checked for paths and consistency. A full rendered PDF/DOCX proofing pass remains required before external circulation.

## QA disposition

The source manuscript is internally consistent with the stated authoritative records and is suitable for substantive supervisor review only. It is not publication-ready.
