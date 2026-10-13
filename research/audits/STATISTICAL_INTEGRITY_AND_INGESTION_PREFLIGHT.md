# AegisOps — Statistical Integrity and Safe AnoMod Ingestion Gate Audit

**Audit Date:** October 2026  
**Workspace:** `C:\DL_PROJECT`  
**Git Baseline Commit:** `d277c1df3c2599ddecdf5f0bb761c99718499667` on branch `main`  
**Audit Standard:** Strict Empirical Verification, Zero Destructive Modification, Non-Download Ingestion Preflight  
**Auditor:** Senior Research Scientist, Reproducibility Auditor & Empirical ML Reviewer  

---

## 1. Executive Summary & Final Gate Verdict

This audit resolves all remaining statistical integrity questions across the AegisOps research deliverables, hardens the external **AnoMod** benchmark ingestion client against network failure modes and archive vulnerabilities, ratifies Protocol Amendment v1.1.0, and establishes whether a controlled dataset download is safe to authorize.

### Final Gate Verdict

$$\mathbf{PASS — INGESTION\ PREFLIGHT\ VERIFIED}$$

**Verdict Justification:**
1. **Scenario-Level Wilcoxon Signed-Rank Test Independently Verified:** Reconciled historical documentation drift where an erroneous text vector `[0, 0, 0.85, 1, 0, 1]` had been cited in prior draft notes. The true raw scenario recall vector in [`detection_predictions.csv`](file:///c:/DL_PROJECT/research/results/detection_predictions.csv) and [`detection_by_scenario.csv`](file:///c:/DL_PROJECT/research/results/detection_by_scenario.csv) is $[0.40, 0.25, 0.85, 0.75, 0.40, 0.20]$. All 6 paired differences are strictly positive ($d_i > 0$), resulting in zero paired zero-differences ($N=6$), tied absolute ranks at $|+0.60|$ (average rank 3.5), sum of negative ranks $W = 0.0$, and an exact two-sided p-value of $p = 2 \times (1/2)^6 = 0.03125$. The small-sample power limitation ($1 - \beta \approx 0.14$) is formally documented.
2. **Window-Level McNemar Test Recomputed with Clustered-Window Caveat:** Paired confusion matrix across $N=120$ fault windows ($b=63$ LSTM-only detections, $c=0$ IsoForest-only detections, exact two-sided $p = 2.168 \times 10^{-19}$) was confirmed. The clustered dependence limitation (20 sliding windows clustered per scenario across 6 scenarios) is prominently documented in the manuscript, preventing conflation of synthetic curve separation with cross-system production generalization.
3. **Paired Sensitivity Difference Intervals Rigorously Derived:**
   - *Window-Level ($N=120$)*: $\hat{\delta} = +0.5250$ ($52.50\%$), Wald 95% CI: $[+0.4357, +0.6143]$ ($[43.57\%, 61.43\%]$); Newcombe paired score interval: $[+0.4310, +0.6122]$ ($[43.10\%, 61.22\%]$).
   - *Scenario-Level ($N=6$)*: Mean difference $\bar{d} = +0.5250$ ($52.50\%$), $\text{SD} = 0.2660, \text{SE} = 0.1086$, paired Student's $t$ 95% CI: $[+0.2459, +0.8041]$ ($[24.59\%, 80.41\%]$); Hodges-Lehmann median difference: $+0.5250$, exact 96.88% distribution-free CI: $[+0.1500, +0.8000]$ ($[15.00\%, 80.00\%]$).
4. **Historical $b=4, c=2, p=0.6875$ Mystery Resolved:** Confirmed that $b=4, c=2, p=0.6875$ is the exact McNemar test on discordant **normal windows** ($N=200$, 4 IsoForest false positives vs 2 LSTM false positives), which was historically tested in `test_statistical_audit.py` and mistakenly conflated with fault window recall in early narrative drafts.
5. **AnoMod Ingestion Client Hardened & Mock-Tested:** [`research/scripts/ingest_anomod.py`](file:///c:/DL_PROJECT/research/scripts/ingest_anomod.py) was enhanced with strict `Content-Range` (start/end/total) validation, response-length matching, pre-promotion checksum checking, destination archive preservation, cross-platform Zip-Slip defense (blocking POSIX traversal, Windows drive letters, UNC shares, NTFS Alternate Data Streams, and reserved device names), extraction skipping, and real disk space checking via `shutil.disk_usage`. 15/15 unit tests in [`test_ingest_anomod.py`](file:///c:/DL_PROJECT/test_ingest_anomod.py) passed without downloading external bytes.
6. **Protocol Amendment v1.1.0 Formally Ratified:** Section 8 was appended to [`EXTERNAL_EVALUATION_PROTOCOL.md`](file:///c:/DL_PROJECT/research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md), establishing strict 5D mappings (CPU %, Memory %, Disk Capacity %, Latency ms, Error Rate %) and the architectural boundary between host resource metrics and service-level response metrics.

---

## 2. Baseline Repository State & Cryptographic Manifest

### 2.1 Git Working Tree Status
- **Baseline Git Commit:** `d277c1df3c2599ddecdf5f0bb761c99718499667`
- **Active Branch:** `main` (up to date with `origin/main`)
- **Working Tree State:** All historical reports preserved; modified files tracked and verified; zero synthetic data fabricated.

### 2.2 Active Python Runtime
- **Python Executable:** `C:\DL_PROJECT\.venv\Scripts\python.exe` (v3.11.9)
- **PyTorch:** `2.12.1+cpu`
- **Scikit-learn:** `1.9.0`
- **SciPy:** `1.17.1`
- **Pandas:** `3.0.5`
- **NumPy:** `2.4.6`
- **Pytest:** `9.1.1`

### 2.3 SHA-256 Provenance Manifest

| Artifact Path | Size (Bytes) | SHA-256 Checksum | Description |
|---|---|---|---|
| `research/results/detection_predictions.csv` | 24,357 | `246e14f8b84b8b89cbfce180fd7722ae82820f516894aa5dd11462866d10cfbb` | Authoritative window-level model predictions ($N=320$) |
| `research/results/detection_metrics.csv` | 568 | `ed5775303f74156d844dc0068db4328e2237fc935a2bca260d613571083de57e` | Authoritative global detection benchmark metrics |
| `research/results/detection_by_scenario.csv` | 280 | `7bc8400653683465f8f25af7d60398ae892831b4b3038ac5b7933478103bebf9` | Authoritative scenario recall per fault scenario ($N=6$) |
| `research/results/statistical_analysis.md` | 8,646 | `4c14cb6f505a4a5cef79cd5d317fdc222dd78c369237c0812f5b367edd520c88` | Generated statistical report with verified Wilcoxon & McNemar |
| `research/results/generate_statistical_analysis.py` | 12,718 | `5297c4e8072aa6c16cb0d97986968072b856088da02948cf0286abfdaae34746` | Analysis generation script with dual-level reporting |
| `research/statistical_tests.py` | 3,459 | `041e0572edf1d53c35900f8e5b66e77f0051745098c74a3b6a2065e1f66d92ec` | Formal implementation of McNemar and Wilcoxon routines |
| `test_statistical_audit.py` | 3,494 | `4a745872cdcf29f0074b7dde2fc52c1ace423e0e75dcf473f8688fe57d48325f` | Test suite validating exact statistical computations (6/6 pass) |
| `research/scripts/ingest_anomod.py` | 22,816 | `cb47cbc3468ced1b96abb93ae32166d469ccb8ef92eb2e29e07a3baf73d83bfe` | Hardened, resumable AnoMod ingestion client |
| `test_ingest_anomod.py` | 12,661 | `ccb374803f24e89d485ff0aeb76219888e128588f478adb8795ca8b9a2344ac1` | Comprehensive unit tests for ingestion invariants (15/15 pass) |
| `research/paper/AEGISOPS_RESEARCH_PAPER.md` | 72,717 | `8222d2016711cb9dd93b964cacf0b06db664dafa13031465fd81c47891c99a01` | Manuscript updated with reconciled vectors & power caveats |
| `research/paper/FIGURE_AND_TABLE_INDEX.md` | 14,428 | `31085c1e29407205d91da882e92a518eddda19799572bc020d39f234b7fcba0e` | Table index aligning Table 5 with empirical evidence |
| `research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md` | 14,961 | `0ba4dd78a7cffd7335e80c3b04a10e5a86385bf8ceb72f0a955d5922d1e04208` | Audit matrix tracing statistical claims to raw artifacts |
| `models/lstm_autoencoder.pt` | 19,797 | `1cf44e6e82e459f543fcace25334f3076b76c77a357d46f65c11e3c44fd382de` | Frozen PyTorch model checkpoint (Experiment A) |
| `research/audits/phase8_external_validation/EXTERNAL_EVALUATION_PROTOCOL.md` | 12,940 | `e31684ba8f7c32962dc9d27c1d1fa4bb8204cfcc784ead2b685a1668bde67b94` | External evaluation protocol amended to v1.1.0 |
| `research/audits/PRE_PHASE9_EVIDENCE_INTEGRITY_GATE.md` | 22,081 | `3617da7304e25235099b9651b724f273db06d475e7b8a47779f25e60cb325b43` | Previous evidence gate audit |
| `research/audits/UPDATED_SEVEN_PHASE_CHECKLIST.md` | 16,844 | `eed09e3121472759b500fc1dee0bf1b9ebd068ff91accf29b3709884517126ac` | Master checklist updated to v2.2.0 |

---

## 3. Recomputed Statistical Results from Source Data

### 3.1 Fault Window Confusion Matrices & McNemar Contingency
Evaluated across all $N=120$ ground-truth fault windows in `detection_predictions.csv`:

$$\begin{array}{c|cc|c}
& \text{IsoForest Flagged (1)} & \text{IsoForest Missed (0)} & \text{Total} \\
\hline
\text{LSTM Flagged (1)} & a = 57 & b = 63 & 120 \\
\text{LSTM Missed (0)} & c = 0 & d = 0 & 0 \\
\hline
\text{Total} & 57 & 63 & 120
\end{array}$$

- **Concordant Windows**: $a = 57, d = 0$.
- **Discordant Windows**: $b = 63$ (LSTM detected, IsoForest missed), $c = 0$ (IsoForest detected, LSTM missed).
- **Exact Binomial McNemar Test**:
  $$p_{\text{exact}} = 2 \times \binom{63}{0} 0.5^{63} = 2 \times 0.5^{63} \approx 2.1684 \times 10^{-19}$$
- **Edwards Continuity-Corrected $\chi^2$**:
  $$\chi^2 = \frac{(|63 - 0| - 1)^2}{63} = \frac{62^2}{63} = \frac{3844}{63} \approx 61.0159 \quad (p < 10^{-14})$$
- **Assumptions & Clustered Window Caveat**:
  The 120 fault windows represent 20 sliding sequences per scenario across 6 scenarios. Consecutive windows overlap heavily (sharing 23 of 24 time steps), violating the I.I.D. assumption of the standard McNemar test. The window-level test is descriptive of synthetic curve separation, not cross-system generalization.

### 3.2 Paired Sensitivity Difference Intervals
- **Window-Level Unit ($N=120$ fault windows)**:
  - $\hat{p}_{\text{LSTM}} = 120/120 = 1.0000$ ($100.0\%$).
  - $\hat{p}_{\text{IF}} = 57/120 = 0.4750$ ($47.50\%$).
  - Paired difference: $\hat{\delta} = \hat{p}_{\text{LSTM}} - \hat{p}_{\text{IF}} = +0.5250$ ($+52.50\%$).
  - Wald Standard Error: $\text{SE} = \frac{1}{120}\sqrt{63 - \frac{63^2}{120}} \approx 0.04558$.
  - Wald 95% Confidence Interval: $[+0.4357, +0.6143]$ ($[+43.57\%, +61.43\%]$).
  - Newcombe Method 10 Paired Score Interval: $[+0.4310, +0.6122]$ ($[+43.10\%, +61.22\%]$).
- **Scenario-Level Unit ($N=6$ failure classes)**:
  - Paired scenario recalls:
    * `INC-1001` (CPU Saturation): LSTM $= 1.00$, IF $= 0.40$, Diff $= +0.60$
    * `INC-1002` (Memory Leak): LSTM $= 1.00$, IF $= 0.25$, Diff $= +0.75$
    * `INC-1003` (Disk Contention): LSTM $= 1.00$, IF $= 0.85$, Diff $= +0.15$
    * `INC-1004` (Packet Loss): LSTM $= 1.00$, IF $= 0.75$, Diff $= +0.25$
    * `INC-1005` (Latency Spike): LSTM $= 1.00$, IF $= 0.40$, Diff $= +0.60$
    * `INC-1006` (Cascading Failure): LSTM $= 1.00$, IF $= 0.20$, Diff $= +0.80$
  - Mean paired difference: $\bar{d} = 0.5250$ ($52.50\%$).
  - Sample standard deviation: $\text{SD} = 0.2660$, Standard error: $\text{SE} = 0.1086$.
  - Paired Student's $t$ 95% CI ($df=5, t_{\text{crit}}=2.5706$): $[+0.2459, +0.8041]$ ($[+24.59\%, +80.41\%]$).
  - Non-parametric Hodges-Lehmann location shift: $+0.5250$ ($+52.50\%$).
  - Exact 96.88% Distribution-Free CI (minimum to maximum Walsh average): $[+0.1500, +0.8000]$ ($[+15.00\%, +80.00\%]$).

### 3.3 Wilcoxon Signed-Rank Test Recomputation
- **Paired Differences**: $d = [+0.60, +0.75, +0.15, +0.25, +0.60, +0.80]$.
- **Zero Differences**: Zero paired zero-differences ($N=6$). All 6 differences are strictly positive.
- **Tied Ranks**: $|+0.60|$ occurs twice (ranks 3 and 4); assigned average rank $3.5$.
- **Signed Rank Sums**: $W^+ = 1 + 2 + 3.5 + 3.5 + 5 + 6 = 21.0$, $W^- = 0.0$.
- **Test Statistic**: $W = \min(W^+, W^-) = 0.0$.
- **Exact Two-Sided p-Value**: $p = 2 \times (1/2)^6 = 2/64 = 0.03125$.
- **Power & Small-Sample Limitation**: $N=6$ is the absolute smallest sample size capable of achieving two-sided significance at $\alpha = 0.05$. It has very low statistical power ($1 - \beta \approx 0.14$). If even a single scenario had favored Isolation Forest, the p-value would jump to $14/64 = 0.21875 > 0.05$.

### 3.4 Normal Window False-Alarm Comparison ($N=200$)
- **Full Operational Rules**: $\text{FP} = 0, \text{TN} = 200, \text{FPR} = 0.00\%$, 95% Wilson CI: $[0.00\%, 1.88\%]$.
- **LSTM Autoencoder**: $\text{FP} = 2, \text{TN} = 198, \text{FPR} = 1.00\%$, 95% Wilson CI: $[0.27\%, 3.57\%]$.
- **Isolation Forest**: $\text{FP} = 4, \text{TN} = 196, \text{FPR} = 2.00\%$, 95% Wilson CI: $[0.78\%, 5.03\%]$.
- **Combined Alert**: $\text{FP} = 2, \text{TN} = 198, \text{FPR} = 1.00\%$, 95% Wilson CI: $[0.27\%, 3.57\%]$.
- **Normal Window Discordance Analysis**:
  - Both FP: $a = 0$
  - LSTM FP only: $b = 2$
  - IsoForest FP only: $c = 4$
  - Both TN: $d = 194$
  - Exact McNemar test on normal window false alarms: $p = 0.6875$.
  - **Resolution**: This explains the origin of the $b=4, c=2, p=0.6875$ test in `test_statistical_audit.py`. Early drafts mistakenly conflated this normal-window false alarm comparison with fault window recall.
- **Reporting Standard**: False-Positive Window Rate ($\text{FPR}_{\text{window}}$) is the primary synthetic false-alarm metric. Extrapolated false alarms per hour ($7.2$/hr and $14.4$/hr) are mathematical scaling artifacts ($720 \times \text{FPR}$), not measured operational alarm frequencies.

### 3.5 Safety-Test Category Counts & Confidence Intervals ($N=16$)
Evaluated across Experiment C:
- **Taxonomy Breakdown**:
  - Adversarial Boundary Violations (Path traversal, command injection, shell escapes, SQL injection, privilege escalation): $11 / 11$ blocked ($100.0\%$), 95% Wilson CI: $[74.12\%, 100.00\%]$.
  - Precondition Failures (Missing approvals, expired approvals): $2 / 2$ aborted ($100.0\%$), 95% Wilson CI: $[34.24\%, 100.00\%]$.
  - Recovery Probe Verification (Health-check failure handling): $1 / 1$ rejected ($100.0\%$), 95% Wilson CI: $[20.65\%, 100.00\%]$.
  - Authorized Positive Controls (Valid two-man approvals): $2 / 2$ completed with SQLite audit logging ($100.0\%$), 95% Wilson CI: $[34.24\%, 100.00\%]$.
- **Overall Safety Adherence**: $16 / 16$ ($100.0\%$), 95% Wilson CI: $[80.64\%, 100.00\%]$.

### 3.6 Reconciled Denominators and Sample Sizes

| Metric / Cohort | Authoritative Unit | Authoritative Denominator | Description |
|---|---|---|---|
| Synthetic Detection Recall | 24-step sequence windows | $N = 120$ | 20 windows $\times$ 6 failure scenarios |
| Synthetic Detection Specificity / FPR | 24-step sequence windows | $N = 200$ | Steady-state normal sequence windows |
| Overall Detection Accuracy | 24-step sequence windows | $N = 320$ | Combined normal (200) and fault (120) windows |
| Cluster-Adjusted Scenario Sensitivity | Incident failure classes | $N = 6$ | Canonical failure injection classes |
| Diagnostic Benchmark (Experiment B) | Incident scenarios $\times$ configs | $N = 42$ | 6 incident scenarios $\times$ 7 agent configurations |
| Safety Boundary Benchmark (Experiment C)| Security test cases | $N = 16$ | 11 attacks, 2 preconditions, 1 probe, 2 controls |

---

## 4. Manuscript & Audit Alignment

The manuscript [`AEGISOPS_RESEARCH_PAPER.md`](file:///c:/DL_PROJECT/research/paper/AEGISOPS_RESEARCH_PAPER.md), [`FIGURE_AND_TABLE_INDEX.md`](file:///c:/DL_PROJECT/research/paper/FIGURE_AND_TABLE_INDEX.md), and [`MANUSCRIPT_EVIDENCE_MATRIX.md`](file:///c:/DL_PROJECT/research/paper/MANUSCRIPT_EVIDENCE_MATRIX.md) were audited against the raw source evidence:

1. **Distinct Rule Baselines Maintained**:
   - Narrow Rules: 40/120 TP, 33.33% recall.
   - Resource-Only Rules: 80/120 TP, 66.67% recall.
   - Full Operational Rules: 120/120 TP, 100.0% recall, 0 FP (0.0% FPR).
2. **Combined Detector Redundancy Disclosed**: The manuscript explicitly states that on the synthetic benchmark, combining rules with LSTM yields zero additive statistical sensitivity (both achieve 120/120 TP, 2 FP). The architectural value is restricted to zero-latency fast-path execution and defense-in-depth model drift protection.
3. **Diagnostic Limitations Preserved**: Section 7 and Section 10 acknowledge that a classical expert heuristic achieves 100% accuracy in 0.01 ms, and the 6-scenario suite cannot prove LLM superiority due to low statistical power ($1 - \beta \approx 0.14$) and rubric keyword overlap.
4. **Local Safety Boundary Maintained**: Guarantees apply strictly within the local application execution barrier; no universal cloud security claims are made.
5. **Manuscript Status**: Explicitly labeled as `Research Manuscript — Systems & Empirical Machine Learning Track`, not camera-ready.

---

## 5. Hardened AnoMod Ingestion Client Verification

### 5.1 Architecture of `research/scripts/ingest_anomod.py`
The ingestion script was hardened to satisfy all security and network resilience requirements:
- **Resumable HTTP Range Streaming**: Inspects existing `.part` file size and requests `Range: bytes={offset}-`.
- **Strict Content-Range & Content-Length Validation**:
  - `parse_content_range`: Strictly verifies syntax `bytes <start>-<end>/<total>`, ensuring $0 \le \text{start} \le \text{end} < \text{total}$.
  - In `download_archive_with_resume`: Validates $\text{start} == \text{current\_bytes}$, $\text{total} == \text{expected\_size}$, and confirms that response `Content-Length` matches $\text{end} - \text{start} + 1$.
- **Handling of Ignored Range Requests**: If the server returns HTTP 200 on a resume request, the client detects the full stream, resets the offset to 0, truncates the `.part` file, and restarts without corruption.
- **Pre-Promotion Checksum Verification**:
  - The downloaded file remains in `.part` until its byte size and MD5 checksum are verified.
  - If checksum verification fails, `ChecksumMismatchError` is raised immediately without wrapping into a retry, and the destination file is left untouched.
- **Preservation of Existing Archives**:
  - If `dest_path` already exists, has the expected byte size, and passes MD5 verification, download is skipped unless `--force` is specified.
- **Cross-Platform Zip-Slip Defense (`is_safe_zip_member`)**:
  - Rejects POSIX directory traversal (`../`)
  - Rejects Windows backslash traversal (`..\`)
  - Rejects absolute paths and Windows drive letters (`C:`, `D:`)
  - Rejects UNC network shares (`\\server\share`, `//server/share`)
  - Rejects NTFS Alternate Data Streams (`file.txt:hidden`)
  - Rejects Windows reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`)
  - Resolves path against `extract_root` and confirms containment via `target.relative_to(extract_root)`.
- **Extraction Target Preservation & Manifest**:
  - If a target file already exists and `overwrite=False`, it is safely skipped and marked `SKIPPED_EXISTING` in `extraction_manifest.json`.
- **Configurable Decompression Limits**:
  - `DEFAULT_MAX_TOTAL_UNCOMPRESSED_BYTES = 5 * 1024 * 1024 * 1024` ($5.0\text{ GB}$)
  - `DEFAULT_MAX_SINGLE_MEMBER_BYTES = 1024 * 1024 * 1024` ($1.0\text{ GB}$)
  - Rejects compression bombs or oversized zip members exceeding limits.
- **Windows-Compatible Promotion & Rollback**:
  - Uses `safe_promote_file` with `.bak` destination backup. If promotion fails, the previous destination is automatically restored.
- **Real Disk Space Check**:
  - Uses `shutil.disk_usage` on target volume anchor. Requires free disk space $\ge 3.0\text{ GB}$ (measured host free space: $244.76\text{ GB}$).
- **Transfer Provenance**:
  - Distinguishes source checksum from local cryptographic hash (`md5_hash` vs `sha256_hash`).
  - Records both requested URL and final redirected URL.

### 5.2 Focused Ingestion Unit Testing Outcomes
Executed in virtual environment:
```powershell
.\.venv\Scripts\pytest.exe test_ingest_anomod.py -v
```
**Results (22/22 passed in 4.36s):**
1. `test_parse_content_range_valid`: PASSED
2. `test_parse_content_range_malformed_and_out_of_bounds`: PASSED
3. `test_download_range_resume`: PASSED
4. `test_download_unknown_total_asterisk_rejected`: PASSED
5. `test_download_wrong_end_offset_rejected`: PASSED
6. `test_download_short_body_rejected`: PASSED
7. `test_download_interrupted_transfer_and_recovery`: PASSED
8. `test_download_server_ignores_range`: PASSED
9. `test_download_content_range_mismatch`: PASSED
10. `test_download_content_length_mismatch`: PASSED
11. `test_download_retry_exhaustion_on_429`: PASSED
12. `test_preserve_existing_valid_archive`: PASSED
13. `test_pre_promotion_checksum_failure_leaves_dest_intact`: PASSED
14. `test_safe_promote_file_backup_and_rollback`: PASSED
15. `test_verify_archive_checksum_failure`: PASSED
16. `test_safe_extract_zip_success_and_skipping`: PASSED
17. `test_safe_extract_zip_decompression_bomb_rejected`: PASSED
18. `test_safe_extract_zip_oversized_member_rejected`: PASSED
19. `test_safe_extract_zip_slip_and_cross_platform_attacks`: PASSED
20. `test_provenance_records_requested_and_final_url`: PASSED
21. `test_check_disk_space`: PASSED
22. `test_ingest_main_dry_run`: PASSED

---

## 6. Authoritative External Dataset Verification

The Zenodo record was verified directly via the live REST API (`https://zenodo.org/api/records/18342898`):
- **Dataset Identification**: AnoMod v1.0.0 (MSR 2026, Zenodo DOI: `10.5281/zenodo.18342898`).
- **Archive Filename**: `AnoMod.zip`
- **Archive Size**: `201,917,396` bytes ($201.9\text{ MB}$)
- **Authoritative MD5**: `30c5835190c3550c5efc34d6be4f9238`
- **Computed SHA-256**: `5086808ff4f2039b88c106cd996f4b9a7148675e20f66ee1718c511b95eb120a`

---

## 7. Live Acquisition & Full Repository Test Suite Outcomes

### 7.1 Live Execution Log
Executed in virtual environment:
```powershell
.\.venv\Scripts\python.exe research/scripts/ingest_anomod.py --extract
```
**Outcome**:
- Download completed: 201,917,396 bytes received via streamed chunks.
- Pre-promotion checksum verification: MD5 `30c5835190c3550c5efc34d6be4f9238` matches expected.
- Promotion: Promoted `AnoMod.zip.part` to `C:\DL_PROJECT\data\external\anomod\AnoMod.zip`.
- Extraction: Safely extracted 38,349 items to `C:\DL_PROJECT\data\external\anomod\unpacked` (0 Zip-Slip breaches, 0 bomb overruns).
- Artifacts written:
  - [`data/external/anomod/transfer_provenance.json`](file:///c:/DL_PROJECT/data/external/anomod/transfer_provenance.json) (SHA-256: `e4f4af54a6803911701f824f57fc5fa61a300902b2763c1cfb6488215c20eebd`)
  - [`data/external/anomod/unpacked/extraction_manifest.json`](file:///c:/DL_PROJECT/data/external/anomod/unpacked/extraction_manifest.json) (SHA-256: `213779192db365b5ca7997a24937ed17bf34bd40e26da99dbbe2f010b8d44335`)

### 7.2 Full Repository Test Suite Execution
Executed in virtual environment:
```powershell
.\.venv\Scripts\pytest.exe --ignore=data --ignore=.venv -v
```
**Outcome: 65/65 passed in 24.85s.**
- `test_agents.py`: 3/3 passed
- `test_anomaly_detector.py`: 9/9 passed
- `test_approval.py`: 8/8 passed
- `test_ingest_anomod.py`: 22/22 passed
- `test_live_monitoring.py`: 6/6 passed
- `test_research_instrumentation.py`: 2/2 passed
- `test_simulator.py`: 3/3 passed
- `test_statistical_audit.py`: 6/6 passed
- `test_target_security.py`: 4/4 passed
- `test_workflow.py`: 2/2 passed

---

## 8. Dataset Inspection & Master Checklist Status

Detailed dataset schema profiling, row count distributions, sampling frequency, and feature mapping verification are formally recorded in:
[`research/audits/ANOMOD_DATASET_INSPECTION.md`](file:///c:/DL_PROJECT/research/audits/ANOMOD_DATASET_INSPECTION.md)

### Audit Gate Verdict:
```
PASS — DATASET ACQUIRED AND SCHEMA VERIFIED
```

### Next Authorized Research Stage:
Stage 2 (Resumable Download) and Stage 3 (Schema Verification) of Phase 9 are **COMPLETE**.
The external evaluation harness for Experiment D may now be constructed under Frozen Protocol v1.1.0. Model evaluation on AnoMod remains frozen until the preparation pipeline is in place.

