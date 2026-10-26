# Reference Verification Audit

**Audit date:** 2026-10-16 (Asia/Kolkata)  
**Method:** Reviewed the Phase 5 detailed bibliography audit and its authoritative URLs, then rechecked representative primary records for Isolation Forest, Malhotra et al., MicroRCA, CloudRCA, Eadro, and AnoMod. The active manuscript contains only the 16 references below. A verified identity supports only the stated related-work claim, never an AegisOps result.

| Ref. | Record | Verification status | Appropriate manuscript use |
| ---:| --- | --- | --- |
| 1 | Audibert et al. (2020), USAD, DOI 10.1145/3394486.3403392 | Verified metadata; ACM access limitation retained | Related multivariate unsupervised method only |
| 2 | Edwards (1948), DOI 10.1007/BF02289261 | Verified | Continuity-correction provenance only |
| 3 | Hong et al. (2024), MetaGPT, arXiv:2308.00352 | Verified authoritative record | Generic role-based multi-agent context only |
| 4 | Kim et al. (2022), DOI 10.1609/aaai.v36i7.20680 | Verified | Evaluation-protocol caution only |
| 5 | Lee et al. (2023), Eadro, DOI 10.1109/ICSE48619.2023.00150 | Verified author record | Multi-source troubleshooting context only |
| 6 | Liu, Ting, and Zhou (2008), DOI 10.1109/ICDM.2008.17 | Rechecked IEEE record | Isolation Forest baseline concept only |
| 7 | McNemar (1947), DOI 10.1007/BF02295996 | Verified | Matched-pair test provenance only |
| 8 | Ping et al. (2026), AnoMod, arXiv:2601.22881 | Rechecked arXiv primary record; publisher DOI/venue remains pending | Dataset context and archive provenance only |
| 9 | Su et al. (2019), DOI 10.1145/3292500.3330672 | Verified; title is singular “Network” | Related method only |
| 10 | Wilson (1927), DOI 10.1080/01621459.1927.10502953 | Verified metadata; publisher fetch limitation retained | Interval provenance only |
| 11 | Wu et al. (2020), MicroRCA, DOI 10.1109/NOMS47738.2020.9110353 | Rechecked IEEE record | Attributed-graph RCA context only |
| 12 | Wu and Keogh (2021), DOI 10.1109/TKDE.2021.3112126 | Verified | Benchmark-quality caution only |
| 13 | Zhang et al. (2021), CloudRCA, DOI 10.1145/3459637.3481903 | Rechecked author record | Multi-source KHBN RCA context only |
| 14 | NIST SP 800-53 Rev. 5, DOI 10.6028/NIST.SP.800-53r5 | Verified standard | Governance vocabulary only; not compliance |
| 15 | Malhotra et al. (2016), arXiv:1607.00148 | Rechecked arXiv record | LSTM encoder-decoder precedent only |
| 16 | Wu et al. (2023), AutoGen, arXiv:2308.08155 | Verified authoritative record | Generic LLM-agent framework only |

## Unresolved or limited items

1. AnoMod’s primary arXiv title is **“Microservice Systems”** (plural). The reported ACM DOI/venue needs publisher-page confirmation before external release; no external AegisOps result is claimed.
2. Publisher-page access restrictions documented in Phase 5 remain a verification limitation for USAD and Wilson. They are retained rather than silently removed.
3. No cited source supports AegisOps LSTM novelty, live-LSTM effectiveness, LLM diagnostic superiority, authenticated dual authorization, NIST compliance, production security, or external generalization. The manuscript explicitly avoids those claims.

The detailed URLs, access dates, author lists, venues, and metadata notes remain in `research/exports/phase5/PHASE5_BIBLIOGRAPHY_AUDIT.csv`.
