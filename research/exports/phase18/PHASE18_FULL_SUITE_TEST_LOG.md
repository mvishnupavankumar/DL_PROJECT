# Phase 18 Full Repository Test Log

**Date:** 2026-10-18 (Asia/Kolkata)
**Repository:** `C:\DL_PROJECT`
**Branch / HEAD:** `publish/research-without-external-dataset` / `a32713c30a8ddca1425d44b1afbaf6d55a64c276`

## Safety review before execution

The root test inventory was inspected before execution. `test_ingest_anomod.py` uses injected mock openers and `tmp_path` fixtures rather than downloading a dataset. Live-monitoring tests monkeypatch host/probe dependencies and use temporary SQLite stores. Experiment D tests exercise synthetic fixtures, temporary outputs, dry-run/test-pipeline paths, and fail-closed authorization checks; no production Experiment D command was issued.

## Environment

| Item | Value |
| --- | --- |
| Python executable | `C:\DL_PROJECT\.venv\Scripts\python.exe` |
| Python | 3.11.9 |
| pytest | 9.1.1 |
| Temporary root | `C:\DL_PROJECT\.pytest_tmp_phase18_full_verified` |

## Command

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_tmp_phase18_full_verified
```

## Complete standard output

```text
........................................................................ [ 62%]
............................................                             [100%]
116 passed in 65.70s (0:01:05)
```

## Standard error

```text
(empty)
```

## Result

| Field | Value |
| --- | --- |
| Exit code | 0 |
| Passed | 116 |
| Failed | 0 |
| Errors | 0 |
| Skipped | 0 reported |
| Duration | 65.70 seconds |

The test-only temporary directory and transient runner logs were removed after this output was recorded. No production experiment, live collection, target access, database mutation, model change, or external dataset access occurred.
