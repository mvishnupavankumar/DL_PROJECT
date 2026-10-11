#!/usr/bin/env python3
"""One-command non-destructive AegisOps research audit and evidence inventory."""
from __future__ import annotations
import csv, json, os, re, sqlite3, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'research' / 'controlled_experiment'
DB = OUT.parent.parent / 'data' / 'aegisops_live.sqlite3'

def utc(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def run(cmd, cwd=ROOT):
    print('\n$ ' + ' '.join(map(str, cmd)))
    return subprocess.run(list(map(str, cmd)), cwd=cwd, text=True, capture_output=True)
def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--python', default=sys.executable)
    p.add_argument('--db', default=str(DB))
    args=p.parse_args()
    checks=[]; details=[]
    def check(name, ok, detail):
        checks.append({'name':name,'passed':bool(ok),'detail':str(detail)})
        print(f"[{'PASS' if ok else 'BLOCK'}] {name}: {detail}")
    print('AEGISOPS RESEARCH PIPELINE — NON-DESTRUCTIVE AUDIT')
    print('Project root:', ROOT)
    check('project_root', (ROOT/'app.py').exists(), 'app.py located in project root')
    check('pytest_available', True, f'Python executable: {args.python}')
    tests=run([args.python,'-m','pytest','-q'])
    print(tests.stdout, end=''); print(tests.stderr, end='')
    check('software_tests', tests.returncode==0, f'exit={tests.returncode}; output={tests.stdout.strip()[-1000:]}')
    protocol=OUT/'experiment_protocol.txt'; trial=OUT/'trial_log.csv'
    check('protocol_exists', protocol.exists(), str(protocol))
    check('trial_log_exists', trial.exists(), str(trial))
    if protocol.exists():
        txt=protocol.read_text(encoding='utf-8',errors='replace')
        for label, pattern in [('40 fault episodes',r'40|20.*latency.*20.*error'),('30-second observation',r'30.?second|30 seconds'),('10 healthy controls',r'10.*healthy|healthy.*10'),('approval-gated recovery',r'approval|approved')]:
            check('protocol_'+label, re.search(pattern,txt,re.I|re.S) is not None, 'protocol text checked')
    if trial.exists():
        with trial.open(newline='',encoding='utf-8-sig') as f:
            rd=csv.DictReader(f); rows=list(rd); fields=rd.fieldnames or []
        check('trial_log_headers', bool(fields) and 'trial_id' in fields and 'trial_type' in fields, f'{len(fields)} columns; {len(rows)} rows')
        ids=[r.get('trial_id','') for r in rows if r.get('trial_id')]
        check('trial_ids_unique', len(ids)==len(set(ids)), f'{len(ids)} nonempty IDs')
        details.append({'trial_rows':len(rows),'trial_ids':ids})
    db=Path(args.db)
    check('database_exists',db.exists(),str(db))
    if db.exists():
        try:
            with sqlite3.connect(str(db)) as c:
                tables={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                check('telemetry_table', 'telemetry_samples' in tables, ', '.join(sorted(tables)))
                if 'telemetry_samples' in tables:
                    cols={r[1] for r in c.execute('PRAGMA table_info(telemetry_samples)')}
                    n=c.execute('SELECT COUNT(*) FROM telemetry_samples').fetchone()[0]
                    check('telemetry_nonempty',n>0,f'{n} rows')
                    required={'timestamp','fault_mode','status_code','is_anomaly','detector_mode'}
                    check('telemetry_schema',required<=cols,f'missing={sorted(required-cols)}')
                    details.append({'telemetry_rows':n,'telemetry_columns':sorted(cols)})
                if 'incident_events' in tables:
                    n_events=c.execute('SELECT COUNT(*) FROM incident_events').fetchone()[0]
                    details.append({'incident_event_rows':n_events})
                    check('incident_events_table',True,f'{n_events} events')
                else: check('incident_events_table',False,'table missing')
        except Exception as e: check('database_readable',False,repr(e))
    # Static instrumentation checks. These flag research validity gaps, not necessarily software bugs.
    lm=ROOT/'live_monitoring.py'
    if lm.exists():
        src=lm.read_text(encoding='utf-8',errors='replace')
        check('raw_model_prediction_code_path','model_anomaly' in src,'raw model flag variable exists in source')
        
        # The schema audit below is authoritative for persisted per-sample model outputs; source text alone is not evidence.
        if db.exists():
            with sqlite3.connect(str(db)) as c:
                t={r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                cols={r[1] for r in c.execute('PRAGMA table_info(telemetry_samples)')} if 'telemetry_samples' in t else set()
            raw_cols={'model_anomaly','raw_model_prediction'} & cols
            check('per_sample_raw_prediction_persistence',bool(raw_cols),f'raw prediction columns found={sorted(raw_cols)}')
        else:
            check('per_sample_raw_prediction_persistence',False,'database unavailable for schema verification')
        check('recovery_verification_code_path','fault_mode' in src and ('verification' in src.lower() or 'verified' in src.lower()),'recovery/verification keywords present')
    else:
        check('live_monitoring_source',False,'live_monitoring.py missing from project root')
    # Existing checkpoint metadata discovery.
    metas=list((ROOT/'models').glob('*.json')) if (ROOT/'models').exists() else []
    check('model_metadata',bool(metas),', '.join(str(x.relative_to(ROOT)) for x in metas) or 'no JSON model metadata found')
    blockers=[c for c in checks if not c['passed']]
    report={'generated_utc':utc(),'project_root':str(ROOT),'database':str(db),'checks':checks,'details':details,'blocking_check_count':len(blockers),'status':'READY_FOR_REVIEW' if not blockers else 'BLOCKED'}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'research_readiness.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    lines=['# AegisOps research readiness report','',f"Generated (UTC): {report['generated_utc']}",f"Status: **{report['status']}**",f"Blocking checks: {len(blockers)}",'', '| Check | Result | Detail |','|---|---|---|']
    for c in checks: lines.append(f"| {c['name']} | {'PASS' if c['passed'] else 'BLOCK'} | {c['detail'].replace('|','/').replace('\n',' ')} |")
    lines += ['', '## Interpretation', '- This is a non-destructive audit. It does not inject faults or approve/execute recovery.', '- A software test pass does not establish detector accuracy or support research hypotheses.', '- Formal results require all planned trials, complete raw method outputs, ground-truth labels, and independently verified recovery outcomes.', '- If raw model outputs are not persisted per sample, do not report LSTM-only confusion-matrix metrics.', '']
    (OUT/'research_readiness.md').write_text('\n'.join(lines),encoding='utf-8')
    print('\nReport:',OUT/'research_readiness.md')
    print('JSON:',OUT/'research_readiness.json')
    return 0 if not blockers else 2
if __name__=='__main__': raise SystemExit(main())
