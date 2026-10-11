#!/usr/bin/env python3
"""AegisOps research automation: readiness audit, tests, controlled trials, and metrics.

Safe-by-default: only loopback service URLs are accepted; recovery is NEVER executed
by this script. After each fault, the operator must use the existing approval UI and
this script independently verifies the service returned to normal before continuing.
"""
from __future__ import annotations
import argparse, csv, json, math, os, sqlite3, subprocess, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

FIELDS = [
 "trial_id","trial_type","fault_mode","replicate","run_date_utc","baseline_start_utc",
 "fault_injection_utc","first_model_alert_utc","first_rule_alert_utc","first_combined_alert_utc",
 "fault_reset_utc","verification_utc","verification_passed","raw_model_prediction","rule_prediction",
 "combined_prediction","diagnosis_baseline","diagnosis_agent","diagnosis_baseline_correct",
 "diagnosis_agent_correct","recovery_approved","recovery_attempted","recovery_success",
 "http_status_after_recovery","fault_mode_after_recovery","latency_ms_after_recovery","notes"
]
ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT / "research" / "controlled_experiment"
TRIALS = RESEARCH / "trial_log.csv"
DB_DEFAULT = ROOT / "data" / "aegisops_live.sqlite3"
SERVICE_DEFAULT = "http://127.0.0.1:8765"

def now(): return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
def parse_dt(s):
    if not s: return None
    try: return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception: return None

def request_json(url, method="GET", payload=None, timeout=4):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode(errors="replace")
        try: body = json.loads(raw)
        except Exception: body = {"raw": raw}
        return r.status, body

def loopback_only(url):
    p = urlparse(url)
    return p.scheme == "http" and p.hostname in {"127.0.0.1", "localhost", "::1"} and p.port is not None

def db_connect(path):
    con = sqlite3.connect(str(path), timeout=5); con.row_factory = sqlite3.Row; return con

def print_result(ok, msg): print(("[PASS] " if ok else "[BLOCK] ") + msg)

def cmd_preflight(a):
    print("AegisOps research readiness audit")
    print("Project:", ROOT)
    print_result((ROOT/".venv"/"Scripts"/"python.exe").exists() or sys.platform != "win32", "Python environment located (use project venv for tests)")
    db = Path(a.db)
    print_result(db.exists(), f"Telemetry database exists: {db}")
    if db.exists():
        try:
            with db_connect(db) as c:
                tables={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                print_result("telemetry_samples" in tables, "telemetry_samples table present")
                print_result("incident_events" in tables, "incident_events table present")
                if "telemetry_samples" in tables:
                    cols={r[1] for r in c.execute("PRAGMA table_info(telemetry_samples)")}
                    n=c.execute("SELECT COUNT(*) FROM telemetry_samples").fetchone()[0]
                    print(f"  telemetry rows: {n}; columns: {', '.join(sorted(cols))}")
                    for col in ("timestamp","fault_mode","status_code","anomaly_score","is_anomaly","detector_mode"):
                        print_result(col in cols, f"telemetry column: {col}")
                if "incident_events" in tables:
                    n=c.execute("SELECT COUNT(*) FROM incident_events").fetchone()[0]
                    print(f"  incident events: {n}")
        except Exception as e: print_result(False, f"Database read failed: {e}")
    model=ROOT/"models"/"lstm_autoencoder.json"
    live_model=ROOT/"models"/"live_lstm_autoencoder.json"
    print_result(model.exists() or live_model.exists(), "Model metadata file exists")
    if model.exists() or live_model.exists():
        for p in (model,live_model):
            if p.exists():
                try:
                    d=json.loads(p.read_text(encoding="utf-8")); print(f"  model metadata {p.name}: threshold={d.get('threshold','unknown')}, sequence_length={d.get('sequence_length','unknown')}")
                except Exception as e: print_result(False, f"Could not parse {p.name}: {e}")
    protocol=RESEARCH/"experiment_protocol.txt"
    print_result(protocol.exists(), f"Experiment protocol exists: {protocol}")
    print_result(TRIALS.exists(), f"Trial log exists: {TRIALS}")
    if TRIALS.exists():
        try:
            with TRIALS.open(newline='',encoding='utf-8-sig') as f:
                r=csv.DictReader(f); rows=list(r); missing=[x for x in FIELDS if x not in (r.fieldnames or [])]
            print_result(not missing, "Trial log schema matches expected fields" if not missing else "Trial log missing fields: "+", ".join(missing))
            print(f"  logged trial rows: {len(rows)}")
        except Exception as e: print_result(False, f"Trial log read failed: {e}")
    if not loopback_only(a.service):
        print_result(False, "Service URL must be HTTP loopback with explicit port; no LAN/public targets accepted")
    else:
        try:
            code, body=request_json(a.service+"/health")
            ok=code==200 and body.get("status")=="ok" and body.get("fault_mode") in {"normal","latency","error"}
            print_result(ok, f"Local service health: HTTP {code}, fault_mode={body.get('fault_mode')}")
        except Exception as e: print_result(False, f"Local service not reachable at {a.service}: {e}")
    print("\nImportant: a passing software test suite is not research evidence. Formal trials must only start after the model/rules and trial procedure are frozen, and after the baseline alert issue has been documented.")

def cmd_tests(a):
    py=Path(a.python) if a.python else (ROOT/".venv"/"Scripts"/"python.exe")
    if not py.exists(): py=Path(sys.executable)
    print(f"Running pytest with: {py}")
    p=subprocess.run([str(py),"-m","pytest","-q"],cwd=ROOT)
    return p.returncode

def ensure_trial_log():
    RESEARCH.mkdir(parents=True,exist_ok=True)
    if not TRIALS.exists():
        with TRIALS.open("w",newline="",encoding="utf-8") as f: csv.DictWriter(f,fieldnames=FIELDS).writeheader()
    else:
        with TRIALS.open(newline="",encoding="utf-8-sig") as f:
            rd=csv.DictReader(f)
            if rd.fieldnames != FIELDS: raise RuntimeError("Existing trial_log.csv headers do not exactly match expected protocol schema; no changes made.")

def get_latest_id(db):
    with db_connect(db) as c: return c.execute("SELECT COALESCE(MAX(id),0) FROM telemetry_samples").fetchone()[0]

def rows_since(db, sample_id):
    with db_connect(db) as c:
        return [dict(r) for r in c.execute("SELECT * FROM telemetry_samples WHERE id>? ORDER BY id",(sample_id,)).fetchall()]

def first_alert(rows, key):
    for r in rows:
        if r.get(key) in (1, True, "1"):
            return r.get("timestamp")
    return ""

def trial_row(trial_id, trial_type, mode, replicate):
    d={k:"" for k in FIELDS}; d.update(trial_id=trial_id,trial_type=trial_type,fault_mode=mode,replicate=replicate,run_date_utc=now(),baseline_start_utc=now()); return d

def cmd_run(a):
    if not loopback_only(a.service): raise SystemExit("Refusing to run: service must be local loopback HTTP only.")
    if not Path(a.db).exists(): raise SystemExit(f"Database not found: {a.db}")
    try:
        code, health=request_json(a.service+"/health")
    except Exception as e: raise SystemExit(f"Local service health check failed: {e}")
    if code!=200 or health.get("fault_mode")!="normal": raise SystemExit(f"Service must be healthy and in normal mode before starting; got {health}")
    ensure_trial_log()
    completed=0
    with TRIALS.open(newline="",encoding="utf-8-sig") as f: existing=list(csv.DictReader(f))
    existing_ids={r.get("trial_id") for r in existing}
    print("This runner will inject faults only into the local demo service. It will NOT execute recovery or bypass the approval UI.")
    print("Keep exactly one telemetry collector active. Stop dashboard auto-collection before continuing.")
    input("Press Enter only when the collector is running and the dashboard is not collecting telemetry; Ctrl+C cancels. ")
    plan=[]
    for i in range(1,11): plan.append((f"HC{i:02d}","healthy_control","normal",i))
    for mode,prefix in (("latency","L"),("error","E")):
        for i in range(1,21): plan.append((f"{prefix}{i:02d}","fault",mode,i))
    for tid,ttype,mode,rep in plan:
        if tid in existing_ids:
            print(f"Skipping already logged trial {tid}"); continue
        # Controls run only in normal mode for 60 sec.
        rec=trial_row(tid,ttype,mode,rep)
        start_id=get_latest_id(a.db); rec["baseline_start_utc"]=now()
        if ttype=="healthy_control":
            print(f"\n{tid}: healthy control, 60 seconds. Do not inject a fault.")
            time.sleep(60)
            samples=rows_since(a.db,start_id)
            rec["fault_injection_utc"]=""; rec["fault_reset_utc"]=""; rec["verification_passed"]="not_applicable"
            rec["combined_prediction"]=str(int(any(int(x.get("is_anomaly") or 0)==1 for x in samples)))
            rule_values=[x.get("rule_anomaly") for x in samples if x.get("rule_anomaly") is not None]
            rec["rule_prediction"]=str(int(any(int(v or 0)==1 for v in rule_values))) if rule_values else str(int(any(float(x.get("latency_ms") or 0)>=1000 or int(x.get("status_code") or 0)!=200 or float(x.get("error_rate_pct") or 0)>0 for x in samples)))
            model_values=[x.get("model_anomaly") for x in samples if x.get("model_anomaly") is not None]
            rec["raw_model_prediction"]=str(int(any(int(v or 0)==1 for v in model_values))) if model_values else "unavailable_no_raw_model_outputs"
            rec["first_model_alert_utc"]=first_alert(samples,"model_anomaly")
            rec["first_rule_alert_utc"]=first_alert(samples,"rule_anomaly")
            rec["first_combined_alert_utc"]=first_alert(samples,"is_anomaly")
            rec["notes"]=f"control_samples={len(samples)}; db_ids={start_id+1}..{get_latest_id(a.db)}"
        else:
            print(f"\n{tid}: injecting {mode}; observing for 30 seconds.")
            try:
                _, before=request_json(a.service+"/health")
                if before.get("fault_mode")!="normal": raise RuntimeError(f"Service not normal before trial: {before}")
                _, injected=request_json(a.service+"/admin/fault","POST",{"mode":mode,"delay_ms":1200})
                rec["fault_injection_utc"]=now()
                if injected.get("fault_mode")!=mode: raise RuntimeError(f"Fault injection response mismatch: {injected}")
                time.sleep(30)
                samples=rows_since(a.db,start_id)
                rec["first_model_alert_utc"]=first_alert(samples,"model_anomaly")
                rec["first_rule_alert_utc"]=first_alert(samples,"rule_anomaly")
                rec["first_combined_alert_utc"]=first_alert(samples,"is_anomaly")
                rule_values=[x.get("rule_anomaly") for x in samples if x.get("rule_anomaly") is not None]
                rec["rule_prediction"]=str(int(any(int(v or 0)==1 for v in rule_values))) if rule_values else str(int(any(float(x.get("latency_ms") or 0)>=1000 or int(x.get("status_code") or 0)!=200 or float(x.get("error_rate_pct") or 0)>0 for x in samples)))
                rec["combined_prediction"]=str(int(any(int(x.get("is_anomaly") or 0)==1 for x in samples)))
                model_values=[x.get("model_anomaly") for x in samples if x.get("model_anomaly") is not None]
                rec["raw_model_prediction"]=str(int(any(int(v or 0)==1 for v in model_values))) if model_values else "unavailable_no_raw_model_outputs"
                rec["notes"]=f"fault_samples={len(samples)}; db_ids={start_id+1}..{get_latest_id(a.db)}"
            except Exception as e:
                rec["notes"]="RUNNER_ERROR: "+str(e)
                print("Trial error:",e)
                # If trial setup failed, restore the local demo service to normal as a safety cleanup.
                try:
                    request_json(a.service+"/admin/fault","POST",{"mode":"normal","delay_ms":1200})
                    rec["fault_reset_utc"]=now()
                except Exception as reset_error:
                    rec["notes"] += f"; SAFETY_RESET_ERROR: {reset_error}"
                with TRIALS.open("a",newline="",encoding="utf-8") as f: csv.DictWriter(f,fieldnames=FIELDS).writerow(rec)
                raise SystemExit(2)
            print("\nRECOVERY CHECKPOINT: the injected fault is intentionally still active. Use the existing AegisOps approval UI to request, approve, and execute recovery. This runner will not approve or execute recovery for you.")
            input("After the approved recovery workflow has completed, press Enter so I can independently verify service health. ")
            try:
                status, after=request_json(a.service+"/health")
                _, probe=request_json(a.service+"/probe")
                rec["verification_utc"]=now(); rec["fault_reset_utc"]=rec["verification_utc"]; rec["http_status_after_recovery"]=status
                rec["fault_mode_after_recovery"]=after.get("fault_mode","unknown")
                rec["latency_ms_after_recovery"]=probe.get("server_processing_ms","")
                ok=status==200 and after.get("status")=="ok" and after.get("fault_mode")=="normal" and float(probe.get("server_processing_ms",999999))<1000
                rec["verification_passed"]=str(bool(ok)).lower(); rec["recovery_approved"]="operator_confirmed_in_existing_ui"; rec["recovery_attempted"]="operator_confirmed_in_existing_ui"; rec["recovery_success"]=str(bool(ok)).lower()
                if not ok: print("[BLOCK] Recovery verification failed. Stop and investigate before continuing.")
            except Exception as e:
                rec["verification_utc"]=now(); rec["verification_passed"]="false"; rec["recovery_success"]="false"; rec["notes"] += f"; VERIFY_ERROR: {e}"
                print("[BLOCK] Could not verify recovery:",e)
            # Collect labels from human/agent workflow; never fabricate diagnosis labels.
            print(f"Ground-truth root cause for {tid}: {mode}")
            rec["diagnosis_baseline"]=input("Baseline workflow diagnosis (latency/error/normal/unknown): ").strip()
            rec["diagnosis_agent"]=input("Agent workflow diagnosis (latency/error/normal/unknown): ").strip()
            rec["diagnosis_baseline_correct"]=str(rec["diagnosis_baseline"].lower()==mode).lower()
            rec["diagnosis_agent_correct"]=str(rec["diagnosis_agent"].lower()==mode).lower()
            if rec["verification_passed"]!="true":
                print("Stopping experiment because recovery verification failed. Trial record will be saved.")
                with TRIALS.open("a",newline="",encoding="utf-8") as f: csv.DictWriter(f,fieldnames=FIELDS).writerow(rec)
                raise SystemExit(2)
        with TRIALS.open("a",newline="",encoding="utf-8") as f: csv.DictWriter(f,fieldnames=FIELDS).writerow(rec)
        completed+=1
        print(f"Saved {tid}: samples recorded; trial row appended.")
    print(f"Runner finished. Newly completed rows: {completed}. Trial log: {TRIALS}")
    print("NOTE: raw model prediction is not separately persisted in telemetry_samples in this code snapshot; do not report LSTM-only metrics until raw predictions are instrumented or recovered from per-sample event logs.")

def cmd_analyze(a):
    if not TRIALS.exists(): raise SystemExit(f"Trial log not found: {TRIALS}")
    with TRIALS.open(newline="",encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
    def boolval(x): return str(x).strip().lower() in {"true","1","yes"}
    out={"generated_utc":now(),"trial_log":str(TRIALS),"rows_total":len(rows),"trial_counts":{},"detection":{},"diagnosis":{},"recovery":{},"limitations":[]}
    for r in rows: out["trial_counts"][r.get("trial_type","unknown")]=out["trial_counts"].get(r.get("trial_type","unknown"),0)+1
    for col in ("rule_prediction","combined_prediction"):
        tp=fp=tn=fn=0; evaluable=0
        for r in rows:
            typ=r.get("trial_type"); pred=r.get(col)
            if typ not in {"fault","healthy_control"} or pred not in {"0","1"}: continue
            truth=typ=="fault"; p=pred=="1"; evaluable+=1
            if truth and p: tp+=1
            elif truth and not p: fn+=1
            elif not truth and p: fp+=1
            else: tn+=1
        out["detection"][col]={"n":evaluable,"tp":tp,"fp":fp,"tn":tn,"fn":fn,"precision":tp/(tp+fp) if tp+fp else None,"recall":tp/(tp+fn) if tp+fn else None,"specificity":tn/(tn+fp) if tn+fp else None,"f1":2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}
    for col in ("diagnosis_baseline_correct","diagnosis_agent_correct"):
        vals=[boolval(r[col]) for r in rows if r.get("trial_type")=="fault" and r.get(col) not in {"",None}]
        out["diagnosis"][col]={"n":len(vals),"correct":sum(vals),"accuracy":sum(vals)/len(vals) if vals else None}
    fault_rows=[r for r in rows if r.get("trial_type")=="fault"]
    verified=[r for r in fault_rows if r.get("verification_passed")=="true"]
    out["recovery"]={"fault_trials":len(fault_rows),"verified_successes":len(verified),"verified_success_rate":len(verified)/len(fault_rows) if fault_rows else None}
    out["limitations"].append("This summary includes only rows in the trial log; it does not infer missing outcomes.")
    out["limitations"].append("Combined detector flags are not raw LSTM predictions; raw-model metrics are not estimable unless raw per-sample predictions were logged.")
    out["limitations"].append("Rows from overlapping time windows are not independent samples; the experimental unit is the trial/episode.")
    RESEARCH.mkdir(parents=True,exist_ok=True)
    dest=RESEARCH/"metrics_summary.json"; dest.write_text(json.dumps(out,indent=2),encoding="utf-8")
    md=RESEARCH/"metrics_summary.md"
    lines=["# AegisOps controlled experiment metrics",f"Generated (UTC): {out['generated_utc']}",f"Trial rows: {len(rows)}","", "## Detection metrics", "| Method | n | TP | FP | TN | FN | Precision | Recall | Specificity | F1 |","|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name,m in out["detection"].items():
        fmt=lambda x: "NA" if x is None else f"{x:.3f}"
        lines.append(f"| {name} | {m['n']} | {m['tp']} | {m['fp']} | {m['tn']} | {m['fn']} | {fmt(m['precision'])} | {fmt(m['recall'])} | {fmt(m['specificity'])} | {fmt(m['f1'])} |")
    lines += ["", "## Diagnosis", "```json",json.dumps(out["diagnosis"],indent=2),"```","", "## Recovery", "```json",json.dumps(out["recovery"],indent=2),"```","", "## Limitations"]+["- "+x for x in out["limitations"]]
    md.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Wrote {dest}\nWrote {md}")
    print(json.dumps({"rows_total":out["rows_total"],"trial_counts":out["trial_counts"],"detection":out["detection"],"diagnosis":out["diagnosis"],"recovery":out["recovery"]},indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest="cmd",required=True)
    q=sub.add_parser("preflight"); q.add_argument("--db",default=str(DB_DEFAULT)); q.add_argument("--service",default=SERVICE_DEFAULT); q.set_defaults(func=cmd_preflight)
    q=sub.add_parser("tests"); q.add_argument("--python",default=None); q.set_defaults(func=cmd_tests)
    q=sub.add_parser("run"); q.add_argument("--db",default=str(DB_DEFAULT)); q.add_argument("--service",default=SERVICE_DEFAULT); q.set_defaults(func=cmd_run)
    q=sub.add_parser("analyze"); q.set_defaults(func=cmd_analyze)
    a=p.parse_args(); ret=a.func(a); sys.exit(ret if isinstance(ret,int) else 0)
if __name__=="__main__": main()
