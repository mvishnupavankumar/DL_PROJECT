# AegisOps — Multi-Agent System & Root-Cause Analysis Audit

**Audit Phase**: Phase 6  
**Auditor**: Senior Python Engineer / ML Researcher / SRE / Security Reviewer  
**Scope**: Agent Coordination, Prompts, LLM Provider Integration, Offline Fallback Heuristics, and RCA Reliability

---

## 1. Multi-Agent Architecture & Coordination Model

AegisOps implements a sequential pipeline of 5 specialized agents coordinated by `IncidentAgents` (`agents.py:208`).

```text
Incident Data + Live Evidence
             │
             ▼
    [Manager Agent]
     Classifies category, defines priority and investigation tasks
             │
             ▼
  [Investigation Agent]
     Synthesizes logs + LSTM autoencoder reconstruction evidence
             │
             ▼
    [Diagnosis Agent]
     Identifies most likely root cause and reasoning summary
             │
             ▼
   [Resolution Agent]
     Selects single remediation action_id from catalog
             │
             ▼
  [Action Execution] (Approvals + Local Reset)
             │
             ▼
  [Verification Agent]
     Evaluates post-action health probe and declares PASS/FAIL
```

---

## 2. Dual Execution Modes: LLM vs Offline Deterministic Logic

The agent system operates in two distinct modes depending on the presence of `GROQ_API_KEY`:

### A. Mode 1: LLM-Backed (`GroqAgent.run` via Groq API)
- **Model / Provider**: Groq Cloud API, configured via `GROQ_MODEL` (default: `"openai/gpt-oss-20b"`).
- **Inference Configuration**: Temperature `0.1`, max tokens `1,200`, `response_format={"type": "json_object"}`.
- **Prompt Architecture**: Single-turn prompt with system role instruction and JSON-encoded user payload.
- **Agent Interactivity**: No multi-agent debate, autonomous tool execution, or dynamic feedback loops. The pipeline is a linear, feed-forward sequence of prompt-response calls.

### B. Mode 2: Offline Deterministic Fallback (`GroqAgent._run_local`)
- **Activation**: Triggers automatically when `GROQ_API_KEY` is empty, unset, or set to placeholder strings (`config.py:7-9`).
- **Internal Mechanism**: **Pure hardcoded string heuristics and regex matching**:
  - `_local_root_cause(text)` (`agents.py:20-37`) scans concatenated logs and incident descriptions for hardcoded keywords:
    - `"pool exhausted"` / `"connection pool"` $\to$ `"Database connection pool exhausted..."`
    - `"customer-db"` / `"connection refused"` $\to$ `"The database service is stopped..."`
    - `"http 500"` / `"probe latency"` $\to$ `"The monitored local service is returning errors..."`
    - `"cpu"` / `"worker process"` $\to$ `"Worker processes are saturating CPU capacity."`
    - `"disk"` / `"/var usage"` $\to$ `"The server disk volume is nearly full..."`
    - `"oauth"` / `"auth-service"` $\to$ `"The OAuth configuration is inconsistent..."`
    - `"timeout"` / `"service-b"` $\to$ `"The service-to-service network path is causing timeouts."`
  - `_preferred_actions(root_cause)` (`agents.py:39-53`) matches substrings to static lists of candidate action IDs.
  - Confidence is completely hardcoded: returns `0.82` if anomaly flagged, else `0.66` (`agents.py:119`).

---

## 3. Information Passing, Hallucination Risk & Evidence Citation

| Agent | Input Context Received | Output Produced | Risk of Hallucination / Unsupported Claims |
| :--- | :--- | :--- | :--- |
| **Manager Agent** | `description`, `category`, `environment` | `incident_category`, `priority`, `investigation_tasks`, `objective` | Low. Output is high-level task framing. |
| **Investigation Agent** | `description`, `logs`, `environment`, `manager_plan`, `deep_learning_analysis` | `evidence`, `signals`, `candidate_causes`, `confidence` | **Moderate to High in LLM mode**. Prompts instruct the model to "treat model output as evidence, not ground truth", but provide no citation anchor; LLM can extrapolate phantom log lines or dependencies. |
| **Diagnosis Agent** | `description`, `logs`, `investigation`, `deep_learning_analysis` | `root_cause`, `evidence_used`, `confidence`, `reasoning_summary` | **High in LLM mode**. In offline mode, locked to 7 predefined scenarios. In LLM mode, the model can assert an unsupported root cause (e.g. "DNS cache poison") with high confidence without verifiable telemetry evidence. |
| **Resolution Agent** | `description`, `root_cause`, `action_catalog`, `actions_already_tried` | `action_id`, `rationale`, `expected_result` | **Constrained**. Offline mode strictly checks `if a in catalog_ids`. In live execution, `live_monitoring.py:514` forces `action_id = "clear_demo_service_fault"`. |
| **Verification Agent** | `description`, `root_cause`, `verification_condition`, `selected_action`, `simulated_action_result` | `verified`, `verification_status`, `evidence`, `next_step` | **Low**. Primarily mirrors `bool(action_result['success'])`. |

---

## 4. Resilience, Error Handling & API Safety Audit

### Defect 1: Unhandled Groq API Network Exceptions & Outages
- **Location**: `agents.py:65` (`GroqAgent.run`).
- **Evidence**:
  ```python
  response = self.client.chat.completions.create(
      model=GROQ_MODEL,
      messages=[...],
      ...
  )
  ```
- **Finding**: There is **no `try ... except` block** wrapping the Groq API client call. If the API returns HTTP 429 (Rate Limit Exceeded), HTTP 503 (Overloaded), or experiences a socket timeout, an uncaught `groq.APIConnectionError` or `groq.RateLimitError` propagates to the UI, crashing the Streamlit run without graceful degradation to offline mode.

### Defect 2: Dead Configuration Parameter `MAX_RETRIES`
- **Location**: `config.py:11` vs `agents.py:11`.
- **Evidence**: `config.py` defines `MAX_RETRIES = max(0, int(os.getenv("MAX_RETRIES", "2")))`.
- **Finding**: `MAX_RETRIES` is **never imported, referenced, or used** in `agents.py` or anywhere else in the repository. No retry loop with exponential backoff exists.

### Defect 3: Regex JSON Extraction Fallback
- **Location**: `agents.py:78-82`.
- **Evidence**:
  ```python
  except json.JSONDecodeError:
      match = re.search(r"\{.*\}", content, re.S)
      if not match:
          raise ValueError(f"{self.name} returned invalid JSON: {content}")
      return json.loads(match.group(0))
  ```
- **Finding**: A greedy regex `\{.*\}` will extract everything from the first `{` to the last `}`. If the model emits explanatory text before or after multiple JSON blocks, this regex can produce invalid JSON or mismatched structures.

---

## 5. Proposed Root-Cause Analysis (RCA) Evaluation Metrics

To provide a rigorous scientific evaluation of the multi-agent system in a research paper, the following metrics should be implemented:

1. **Top-1 / Top-k Root Cause Diagnostic Accuracy**:
   $$\text{Accuracy} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(\hat{C}_i = C_i^*)$$
   Where $\hat{C}_i$ is the diagnosed root cause and $C_i^*$ is the ground-truth fault injected.
2. **Evidence Precision (Grounding Ratio)**:
   $$\text{Evidence Precision} = \frac{|\text{Evidence Cited by Agent} \cap \text{True Injected Anomaly Signals}|}{|\text{Total Evidence Cited by Agent}|}$$
   Measures whether the diagnosis references real logged errors and telemetry spikes or hallucinates unrelated system symptoms.
3. **Unsupported Diagnosis Rate (Hallucination Rate)**:
   Percentage of cases where the agent asserts a root cause with confidence $\ge 0.80$ while zero cited evidence items exist in the actual input logs.
4. **Remediation Action Precision**:
   Percentage of cases where the Resolution Agent selects the exact minimally invasive recovery action that successfully restores health on the first attempt without trial-and-error escalation.
5. **Agent Pipeline Latency & Cost**:
   End-to-end wall-clock latency (seconds) and token consumption (input/output prompt cost in USD) across all 5 agent steps per incident.
