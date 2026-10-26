# Phase 14 Data Collection Protocol

**Status:** Proposed procedure only. It does not authorize collection or modify runtime configuration.

## 1. Purpose and boundaries

Collect a provenance-recorded stream suitable for later model development and independently labelled evaluation. The stream must not be described as performance evidence until the approved label protocol, partition plan, and analysis plan have been completed.

The system's five model features retain their existing ordered contract:

`cpu_pct`, `memory_pct`, `latency_ms`, `error_rate_pct`, `disk_pct`

Their units are percent, percent, milliseconds, percent, and percent. CPU, memory, and disk describe the collector host in the current implementation; latency, status, availability, and rolling error rate describe the configured HTTP probe target. This distinction must appear in the collection record and any analysis.

## 2. Required record content

Each sample record must contain the existing raw fields plus the following provenance context in the study export or companion immutable run manifest.

| Record class | Required fields |
| --- | --- |
| Sample identity and time | stable sample ID; UTC ISO-8601 timestamp with timezone; collector clock source; collection-run ID; ordered sequence position |
| Feature contract | the five raw feature values in the fixed order and units; finite-value status; no imputed/replaced value indicator |
| Probe/availability context | service_available; status_code; latency_ms; error_message class without secrets; rolling-error calculation definition; probe endpoint identifier without credentials |
| Source/topology | collector-host identifier; target identifier; environment; service/probe owner; deployment version; configured cadence; timezone/time synchronization declaration |
| Operational condition | `fault_mode` only when supplied; declared condition class; injected-event ID when applicable; collector/probe interruption ID when applicable |
| Inference provenance | detector_mode; inference_reason; anomaly_score; model_anomaly; rule_anomaly; combined_anomaly; checkpoint_provenance; checkpoint_identity; model metadata hash/version |
| Protocol provenance | protocol version; configuration digest excluding secrets; consent/authorization record where applicable; export hash and extraction timestamp |

Do not place bearer tokens, raw secrets, personal data, credentials, or unbounded exception strings in telemetry or labels.

## 3. Timestamp, cadence, and window policy

1. Use one UTC, timezone-aware timestamp format for collector samples and separate source timestamps where available.
2. Record both configured cadence and observed consecutive gap. Do not infer cadence from a dashboard refresh alone.
3. Before scoring, require 24 insertion-order samples with finite values, strictly increasing timestamps, and all gaps at or below the owner-approved `AEGISOPS_LSTM_MAX_INTER_SAMPLE_GAP_S`.
4. When a timestamp is malformed/non-monotonic or the gap is excessive, classify the window as unusable for model scoring; persist the bounded reason, preserve the raw record, and begin accumulating a new candidate window only from subsequent eligible samples.
5. Do not resample, interpolate, forward-fill, backward-fill, reorder by a repaired timestamp, or bridge an interruption. Such operations would be a separate, preapproved research method rather than a collection convenience.

The owner must approve the numeric gap limit after observing a non-evaluative pilot at the intended collection cadence. The Phase 13 six-second smoke-test setting is not operational evidence and is not a proposed default.

## 4. Topology and condition classification

At run start, create an immutable run sheet that names the collector, target, endpoint role, network path, environment, service owner, time source, expected cadence, checkpoint selection mode, and whether the run is eligible for training, calibration, evaluation, or quality-only use.

Use mutually exclusive condition classes:

| Class | Definition and handling |
| --- | --- |
| Normal operation | No declared test event or confirmed incident; may become candidate normal exposure only after independent review. |
| Genuine incident | Operational event confirmed through an independent incident process; record incident ID, onset/offset evidence, affected target, and adjudicator status. |
| Injected test event | Preplanned fault/test action with injection ID and schedule; retain for engineering checks or separately reported scenario analysis, not silently merge with genuine incidents. |
| Collector failure | Missing host metric, collector crash/restart, clock fault, local resource exhaustion, or agent/exporter failure; preserve gap and interruption record. |
| Probe/target failure | Probe transport/HTTP failure, target outage, endpoint deployment change, or target-side telemetry outage; distinguish it from collector failure. |
| Missing/invalid data | Absent, nonfinite, malformed, out-of-contract, or non-monotonic fields; preserve reason and exclude the affected window from model scoring. |
| Unknown/ambiguous | Evidence is insufficient to assign another class; exclude from normal and anomalous truth sets until adjudicated. |

## 5. Quality controls and interruption procedure

Run quality checks at collection start, periodically, and at run close:

- Verify schema/feature names/order, units, finite values, monotonic UTC timestamps, and sample-ID uniqueness.
- Calculate observed gaps and enumerate timestamp resets, duplicate times, missing fields, clock offsets, collector restarts, probe failures, and configuration/checkpoint changes.
- Confirm that the target remains the declared target and that collector-host metrics are not relabelled as target metrics.
- Confirm a configured checkpoint's metadata contract before using scores, and retain checkpoint identity/provenance on every scored or fallback-analyzed row.
- Export raw telemetry, interruption log, configuration digest, and a quality summary with cryptographic hashes before downstream labeling or analysis.

For every interruption, open an interruption record containing start/end UTC times, discoverer, component, known cause, raw-data extent, configuration/checkpoint state, and recovery action. Mark all windows crossing that interval invalid for LSTM scoring. A restart does not permit score backfill.

## 6. Collection stages

1. **Quality-only pilot:** observe cadence, topology, and interruption behavior. It is not used to choose an unrecorded threshold or report performance.
2. **Prospective development collection:** after protocol approval, collect candidate healthy data and separately logged incidents. Freeze run manifests before any model fitting.
3. **Held-out evaluation collection:** declare it before labels/model results are reviewed. Do not use it for scaler fitting, threshold selection, epoch selection, or protocol tuning.

No minimum duration, event count, sample count, or acceptance threshold is prescribed here. Those require owner approval with pilot evidence and the intended estimand.
