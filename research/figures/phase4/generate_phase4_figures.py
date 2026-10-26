#!/usr/bin/env python3
"""Generate the AegisOps Phase 4 evidence-bounded figure set.

This script reads only the frozen/reconciled local evidence.  It performs no
model inference, experiment execution, network access, or mutation outside
its own ``research/figures/phase4`` output directory.  SVG is generated using
the standard library; PNG and PDF companion files are rendered with Pillow,
which is already present in the project environment.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
FORMATS = ("png", "pdf", "svg")
W, H, DPI = 1800, 1125, 300
COL = {
    "ink": "#172033", "muted": "#526071", "blue": "#2B6CB0", "green": "#198754",
    "orange": "#C77800", "red": "#B63B3B", "gray": "#7A8594", "light": "#F3F6F9",
    "line": "#B9C3CF", "white": "#FFFFFF", "purple": "#6F4EA3",
}
REQUIRED = [
    "research/exports/PHASE1_EVIDENCE_FREEZE_AUDIT.md",
    "research/exports/PHASE2_METRIC_RECONCILIATION.md",
    "research/exports/PHASE2_METRIC_SOURCE_MAP.csv",
    "research/exports/PHASE2_STATISTICAL_VERIFICATION.md",
    "research/exports/PHASE3_IMPLEMENTATION_ARCHITECTURE_AUDIT.md",
    "research/exports/PHASE3_COMPONENT_SOURCE_TRACEABILITY.csv",
    "research/exports/PHASE3_DIAGRAM_SPECIFICATION.md",
    "research/exports/PHASE3_UNSUPPORTED_ARCHITECTURE_CLAIMS.md",
    "research/paper/CANONICAL_METRIC_RECONCILIATION.md",
]


def font(size: int, bold: bool = False):
    candidates = (["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/DejaVuSans-Bold.ttf"]
                  if bold else ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/DejaVuSans.ttf"])
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


# Phase 4.1 remediation: preserve a generous margin and use a column-legible
# type scale.  The previous scale made long evidence-boundary text clip.
F8, F10, F12, F14, F16, F20, F26, F34 = [font(n) for n in (16, 20, 24, 28, 32, 38, 46, 54)]
B12, B16, B20, B26, B34 = [font(n, True) for n in (24, 28, 34, 40, 54)]


def new_canvas(title: str, subtitle: str, margin: int = 70):
    im = Image.new("RGB", (W, H), COL["white"])
    d = ImageDraw.Draw(im)
    d.text((margin, 38), title, fill=COL["ink"], font=B34)
    d.text((margin + 2, 112), subtitle, fill=COL["muted"], font=F16)
    d.line((margin, 165, W - margin, 165), fill=COL["line"], width=3)
    return im, d


def multiline(d, xy, text, f=F14, fill=None, spacing=7, anchor=None):
    d.multiline_text(xy, text, font=f, fill=fill or COL["ink"], spacing=spacing, anchor=anchor)


def wrap(text: str, n: int = 29) -> str:
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if len(candidate) > n and line:
            lines.append(line); line = word
        else:
            line = candidate
    if line: lines.append(line)
    return "\n".join(lines)


def box(d, rect, title, body="", color="blue", state=None):
    x1, y1, x2, y2 = rect
    d.rounded_rectangle(rect, radius=16, fill=COL["light"], outline=COL[color], width=4)
    d.rounded_rectangle((x1, y1, x2, y1 + 42), radius=16, fill=COL[color])
    d.rectangle((x1, y1 + 24, x2, y1 + 42), fill=COL[color])
    d.text((x1 + 14, y1 + 7), title, font=B16, fill=COL["white"])
    multiline(d, (x1 + 14, y1 + 55), wrap(body, 20), F12, COL["ink"], spacing=5)
    if state:
        d.text((x1 + 14, y2 - 28), state, font=F10, fill=COL[color])


def arrow(d, start, end, color="ink", dashed=False):
    if dashed:
        x1, y1 = start; x2, y2 = end; dx, dy = x2-x1, y2-y1; dist = max(1, math.hypot(dx, dy))
        for k in range(0, int(dist), 20):
            a, b = k / dist, min(k + 12, dist) / dist
            d.line((x1 + dx*a, y1 + dy*a, x1 + dx*b, y1 + dy*b), fill=COL[color], width=3)
    else:
        d.line((*start, *end), fill=COL[color], width=4)
    d.polygon([(end[0], end[1]), (end[0]-14, end[1]-8), (end[0]-14, end[1]+8)], fill=COL[color])


def footer(d, source: str, note: str, margin: int = 70):
    d.line((margin, H - 135, W - margin, H - 135), fill=COL["line"], width=2)
    d.text((margin, H - 112), "Source: " + source, font=F10, fill=COL["muted"])
    d.text((margin, H - 72), "Boundary: " + note, font=F10, fill=COL["muted"])


def xml_text(x, y, s, size=18, fill="#172033", weight="normal", anchor="start"):
    safe = escape(s)
    lines = safe.split("\n")
    body = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else int(size*1.25)}">{line}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{body}</text>'


def svg_box(x, y, w, h, title, body, color="#2B6CB0", state=None):
    bits = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#F3F6F9" stroke="{color}" stroke-width="2"/>',
            f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="12" fill="{color}"/>',
            f'<rect x="{x}" y="{y+20}" width="{w}" height="18" fill="{color}"/>',
            xml_text(x+12, y+25, title, 15, "#fff", "bold")]
    for i, line in enumerate(wrap(body, 30).split("\n")):
        bits.append(xml_text(x+12, y+62 + i*19, line, 13))
    if state: bits.append(xml_text(x+12, y+h-14, state, 11, color, "bold"))
    return "".join(bits)


def svg_arrow(x1, y1, x2, y2, color="#172033", dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"{dash} marker-end="url(#arrow)"/>'


def export(name: str, im: Image.Image, svg_body: str, title: str, source: str, boundary: str, overwrite: bool):
    paths = [OUT / f"{name}.{ext}" for ext in FORMATS]
    existing = [p for p in paths if p.exists()]
    if existing and not overwrite:
        raise FileExistsError("Refusing to overwrite: " + ", ".join(str(p.name) for p in existing))
    if "png" in FORMATS:
        im.save(OUT / f"{name}.png", "PNG", dpi=(DPI, DPI))
    if "pdf" in FORMATS:
        im.save(OUT / f"{name}.pdf", "PDF", resolution=DPI)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1125" viewBox="0 0 1800 1125">
<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#172033"/></marker></defs>
<rect width="1800" height="1125" fill="#fff"/>
{xml_text(70, 110, title, 34, "#172033", "bold")}
{xml_text(72, 155, source, 16, "#526071")}
<line x1="70" y1="205" x2="1730" y2="205" stroke="#B9C3CF" stroke-width="2"/>
{svg_body}
<line x1="70" y1="990" x2="1730" y2="990" stroke="#B9C3CF" stroke-width="2"/>
{xml_text(70, 1025, "Source: " + source, 12, "#526071")}
{xml_text(70, 1060, "Boundary: " + boundary, 12, "#526071")}
</svg>'''
    if "svg" in FORMATS:
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def preflight():
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing: raise FileNotFoundError("Missing required Phase 4 input(s): " + "; ".join(missing))


def load_data():
    def rows(p):
        with (ROOT / p).open(newline="", encoding="utf-8") as f: return list(csv.DictReader(f))
    a, b, c, live = (rows("research/raw/detection_predictions.csv"), rows("research/raw/diagnosis_predictions.csv"),
                     rows("research/raw/safety_test_results.csv"), rows("research/exports/telemetry.csv"))
    metadata = json.loads((ROOT / "models/lstm_autoencoder.json").read_text(encoding="utf-8"))
    if len(a) != 320 or len(b) != 42 or len(c) != 16 or len(live) != 200:
        raise ValueError("Controlling raw counts do not match Phase 2 reconciliation (320/42/16/200).")
    return a, b, c, live, metadata


def architecture(overwrite):
    im, d = new_canvas("Figure A. Audited application architecture and trust boundaries", "Solid paths are implemented; green marks observed in the audited session; dashed gray marks optional/unobserved.")
    boxes = [
        (70, 270, 335, 500, "Streamlit UI", "Monitoring view, incident panel, approval input", "blue", "IMPLEMENTED"),
        (415, 270, 700, 500, "Collector", "Host CPU/memory/disk + configured-target HTTP probe", "green", "OBSERVED"),
        (780, 270, 1065, 500, "SQLite store", "telemetry_samples and incident_events", "blue", "IMPLEMENTED"),
        (1145, 270, 1430, 500, "Bootstrap rules", "Observed decision path in audited live session", "green", "OBSERVED"),
        (1145, 590, 1430, 820, "Live LSTM", "Optional separate checkpoint; unavailable/not observed", "gray", "OPTIONAL / BLOCKED"),
        (70, 650, 335, 890, "Incident workflow", "Manager → investigation → diagnosis → resolution", "blue", "IMPLEMENTED"),
        (415, 650, 700, 890, "Approval ticket", "Unauthenticated audit label; request / approve / consume", "orange", "WORKFLOW GUARD"),
        (780, 650, 1065, 890, "Local demo recovery", "clear_demo_service_fault only; no remote remediation", "orange", "LOCAL DEMO ONLY"),
        (1500, 430, 1730, 670, "Independent check", "Health + HTTP probe verification, then persistence", "blue", "IMPLEMENTED"),
    ]
    for x1,y1,x2,y2,t,b,c,s in boxes: box(d,(x1,y1,x2,y2),t,b,c,s)
    for a,b in [((335,385),(415,385)),((700,385),(780,385)),((1065,385),(1145,385)),((1430,385),(1500,510)),((335,770),(415,770)),((700,770),(780,770)),((1065,770),(1500,590)),((1065,385),(780,770))]: arrow(d,a,b)
    arrow(d,(1285,500),(1285,590),"gray",True)
    d.text((72, 555), "Trust boundary: collector-host metrics are distinct from configured-target HTTP probe; remote targets are monitor-only.", font=F12, fill=COL["red"])
    footer(d, "Phase 3 architecture audit and diagram specification.", "No authenticated dual control, production authorization, or remote remediation claim.")
    svg = "".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in boxes)
    for a,b in [((335,385),(415,385)),((700,385),(780,385)),((1065,385),(1145,385)),((1430,385),(1500,510)),((335,770),(415,770)),((700,770),(780,770)),((1065,770),(1500,590)),((1065,385),(780,770))]: svg += svg_arrow(*a,*b)
    svg += svg_arrow(1285,500,1285,590,"#7A8594",True) + xml_text(72,555,"Trust boundary: collector-host metrics are distinct from configured-target HTTP probe; remote targets are monitor-only.",14,"#B63B3B")
    export("FIG_A_ARCHITECTURE", im, svg, "Figure A. Audited application architecture and trust boundaries", "Phase 3 architecture audit and diagram specification.", "No authenticated dual control, production authorization, or remote remediation claim.", overwrite)


def model(metadata, overwrite):
    im,d = new_canvas("Figure B. Frozen synthetic-benchmark LSTM autoencoder contract", "Frozen model architecture and threshold contract; the separate intended live-training checkpoint is not present.")
    nodes = [
        (65, 350, 300, 640, "Input window", "(24, 5)\ncpu_pct\nmemory_pct\nlatency_ms\nerror_rate_pct\ndisk_pct", "blue", "FROZEN CONTRACT"),
        (355, 350, 565, 640, "Normalize", "Frozen per-feature mean / std", "blue", "FROZEN"),
        (620, 350, 825, 640, "Encoder LSTM", "5 → 16\nfinal hidden state h∈R¹⁶", "blue", "IMPLEMENTED"),
        (880, 350, 1085, 640, "Repeat", "Repeat h across 24 steps", "blue", "IMPLEMENTED"),
        (1140, 350, 1345, 640, "Decoder LSTM", "16 → 16", "blue", "IMPLEMENTED"),
        (1400, 350, 1730, 640, "Projection + score", "Linear 16 → 5\nreconstruction; global MSE\nstrict score > %.16f" % metadata["threshold"], "green", "SYNTHETIC BENCHMARK"),
    ]
    for x,y,x2,y2,t,b,c,s in nodes: box(d,(x,y,x2,y2),t,b,c,s)
    for i in range(len(nodes)-1): arrow(d,(nodes[i][2],495),(nodes[i+1][0],495))
    d.rounded_rectangle((230,740,1570,890),radius=20,fill="#FFF8E7",outline=COL["orange"],width=3)
    multiline(d,(260,770),"Per-feature reconstruction-error comparisons are available beside the global MSE decision.\nThe 16-dimensional hidden state is not a validated causal representation.\nIntended live checkpoint: separate artifact, unavailable in the audited session.",F16,COL["ink"])
    footer(d, "models/lstm_autoencoder.json; Phase 3 implementation audit.", "Architecture and threshold are frozen synthetic-benchmark evidence, not live validation.")
    svg = "".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in nodes)
    for i in range(len(nodes)-1): svg += svg_arrow(nodes[i][2],495,nodes[i+1][0],495)
    svg += '<rect x="230" y="740" width="1340" height="150" rx="20" fill="#FFF8E7" stroke="#C77800" stroke-width="2"/>' + xml_text(260,790,"Per-feature reconstruction-error comparisons are available beside the global MSE decision.",17) + xml_text(260,825,"The 16-dimensional hidden state is not a validated causal representation.",17) + xml_text(260,860,"Intended live checkpoint: separate artifact, unavailable in the audited session.",17)
    export("FIG_B_FROZEN_LSTM", im, svg, "Figure B. Frozen synthetic-benchmark LSTM autoencoder contract", "models/lstm_autoencoder.json; Phase 3 implementation audit.", "Frozen synthetic-benchmark contract; it does not establish live inference performance.", overwrite)


def telemetry_flow(overwrite):
    im,d = new_canvas("Figure C. Telemetry-to-alert flow and audited live-session boundary", "Observed session path is shown in green; optional model inference is gray and was not observed.")
    nodes=[(70,330,300,570,"Collection","Host metrics + target HTTP probe\n5 s intended cadence, not uniform","green","OBSERVED"),(370,330,600,570,"Rolling error rate","Current sample + preceding records","blue","IMPLEMENTED"),(670,330,900,570,"Persist","SQLite telemetry row","green","OBSERVED"),(970,330,1200,570,"Last-24 window","Insertion order; no timestamp-continuity validation","blue","IMPLEMENTED"),(1270,330,1500,570,"Optional inference","Live LSTM if checkpoint loads","gray","NOT OBSERVED"),(1270,660,1500,860,"Rule guard","Bootstrap rules / model fusion guard","green","OBSERVED"),(1570,480,1740,720,"Annotate + event","Alert-state event persistence","green","OBSERVED")]
    for x,y,x2,y2,t,b,c,s in nodes: box(d,(x,y,x2,y2),t,b,c,s)
    for a,b in [((300,450),(370,450)),((600,450),(670,450)),((900,450),(970,450)),((1200,450),(1270,450)),((1385,570),(1385,660)),((1500,760),(1570,600)),((1200,450),(1270,760))]: arrow(d,a,b, "gray" if a==(1200,450) else "ink", a==(1200,450))
    d.rounded_rectangle((130,720,1120,880),radius=20,fill="#EAF7EF",outline=COL["green"],width=4)
    multiline(d,(170,758),"AUDITED SESSION\n200 stored rows • bootstrap rules only • 200 null LSTM scores",B20,COL["green"])
    footer(d,"research/exports/telemetry.csv; Phase 2 reconciliation; Phase 3 architecture audit.","The stored records do not support live ROC, PR, accuracy, specificity, FPR, or alarms/hour.")
    svg="".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in nodes)
    for a,b in [((300,450),(370,450)),((600,450),(670,450)),((900,450),(970,450)),((1200,450),(1270,450)),((1385,570),(1385,660)),((1500,760),(1570,600)),((1200,450),(1270,760))]: svg+=svg_arrow(*a,*b,"#7A8594" if a==(1200,450) else "#172033",a==(1200,450))
    svg+='<rect x="130" y="720" width="990" height="160" rx="20" fill="#EAF7EF" stroke="#198754" stroke-width="3"/>'+xml_text(170,780,"AUDITED SESSION",21,"#198754","bold")+xml_text(170,820,"200 stored rows • bootstrap rules only • 200 null LSTM scores",22,"#198754","bold")
    export("FIG_C_TELEMETRY_FLOW",im,svg,"Figure C. Telemetry-to-alert flow and audited live-session boundary","research/exports/telemetry.csv; Phase 2 reconciliation; Phase 3 architecture audit.","No live classification-performance claim.",overwrite)


def workflow(overwrite):
    im,d=new_canvas("Figure D. Diagnosis, approval, and local-demo recovery workflow","Workflow components are implemented paths; configuration-level evaluation and live observation are separate evidence scopes.")
    steps=[("Manager","Incident construction","blue"),("Investigation","Evidence collection","blue"),("Diagnosis","Offline deterministic\nor Groq-backed API","purple"),("Resolution","Action selection","blue"),("Human approval","Ticket request / consume\nunauthenticated audit label","orange"),("Local demo recovery","clear_demo_service_fault","orange"),("Independent check","Health + probe","blue"),("Verification","Event persistence","blue")]
    x=55
    for i,(t,b,c) in enumerate(steps):
        box(d,(x,390,x+190,650),t,b,c,"IMPLEMENTED" if c!="purple" else "API BOUNDARY")
        if i: arrow(d,(x-20,520),(x,520))
        x+=215
    d.rounded_rectangle((280,740,1520,880),radius=20,fill="#FFF8E7",outline=COL["orange"],width=3)
    multiline(d,(320,775),"Groq/API boundary: source-visible live path has no explicit retry, timeout, or rate-limit handling.\nDo not infer that every component ran in every Experiment B configuration or in the audited live session.",F16,COL["ink"])
    footer(d,"Phase 3 implementation audit; Phase 2 Experiment B reconciliation.","Approval is a workflow guard, not proof of authenticated dual control or production authorization.")
    svg=""; x=55
    for i,(t,b,c) in enumerate(steps):
        svg+=svg_box(x,390,190,260,t,b,COL[c],"IMPLEMENTED" if c!="purple" else "API BOUNDARY")
        if i: svg+=svg_arrow(x-20,520,x,520)
        x+=215
    svg+='<rect x="280" y="740" width="1240" height="140" rx="20" fill="#FFF8E7" stroke="#C77800" stroke-width="2"/>'+xml_text(320,790,"Groq/API boundary: source-visible live path has no explicit retry, timeout, or rate-limit handling.",17)+xml_text(320,830,"Do not infer that every component ran in every Experiment B configuration or in the audited live session.",17)
    export("FIG_D_DIAGNOSIS_APPROVAL",im,svg,"Figure D. Diagnosis, approval, and local-demo recovery workflow","Phase 3 implementation audit; Phase 2 Experiment B reconciliation.","No claim that all workflow components executed in all evaluated configurations or live session.",overwrite)


def chart_axes(d, rect, ylabels, ymin, ymax, ylabel, title=None):
    x1,y1,x2,y2=rect
    d.line((x1,y1,x1,y2),fill=COL["ink"],width=3);d.line((x1,y2,x2,y2),fill=COL["ink"],width=3)
    for value in ylabels:
        y=y2-(value-ymin)/(ymax-ymin)*(y2-y1)
        d.line((x1,y,x2,y),fill="#E3E9EF",width=2)
        d.text((x1-18,y-12),f"{value:g}",font=F10,fill=COL["muted"],anchor="ra")
    d.text((x1-55,(y1+y2)//2),ylabel,font=F10,fill=COL["muted"],anchor="mm")
    return lambda v: y2-(v-ymin)/(ymax-ymin)*(y2-y1)


def detection(a,overwrite,emit=True):
    methods=[("Rules","rule_flag"),("Isolation Forest","iso_flag"),("LSTM","lstm_flag"),("Combined","combined_flag")]
    summary=[]
    for name,key in methods:
        tp=sum(r["ground_truth"]=="1" and r[key]=="1" for r in a); fp=sum(r["ground_truth"]=="0" and r[key]=="1" for r in a); tn=sum(r["ground_truth"]=="0" and r[key]=="0" for r in a); fn=sum(r["ground_truth"]=="1" and r[key]=="0" for r in a)
        p=tp/(tp+fp) if tp+fp else 0; rec=tp/(tp+fn); f1=2*p*rec/(p+rec) if p+rec else 0; fpr=fp/(fp+tn)
        summary.append((name,tp,fp,tn,fn,p,rec,f1,fpr))
    im,d=new_canvas("Figure E1. Experiment A synthetic detection comparison","Confusion-matrix-derived rates across 320 synthetic windows (200 nominal; 120 fault windows across six scenarios).")
    scale=chart_axes(d,(165,300,1680,800),[0,.2,.4,.6,.8,1],0,1,"rate")
    metrics=[("Precision",5),("Recall",6),("F1",7),("False-positive rate",8)]; colors=[COL["blue"],COL["green"],COL["purple"],COL["orange"]]
    width=68
    for i,row in enumerate(summary):
        base=260+i*350
        for j,(_,idx) in enumerate(metrics):
            val=row[idx]; x=base+j*(width+8); y=scale(val); d.rectangle((x,y,x+width,800),fill=colors[j]); d.text((x+width/2,y-32),f"{val:.3f}",font=F10,fill=COL["ink"],anchor="ma")
        d.text((base+140,830),row[0],font=B12,fill=COL["ink"],anchor="ma")
    for j,(label,_) in enumerate(metrics): d.rectangle((250+j*310,235,275+j*310,260),fill=colors[j]);d.text((285+j*310,237),label,font=F10,fill=COL["ink"])
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic windows may be dependent; no operational false alarms/hour is inferred.")
    svg='<line x1="165" y1="300" x2="165" y2="800" stroke="#172033" stroke-width="2"/><line x1="165" y1="800" x2="1680" y2="800" stroke="#172033" stroke-width="2"/>'
    for value in [0,.2,.4,.6,.8,1]:
        y=800-value*500;svg+=f'<line x1="165" y1="{y}" x2="1680" y2="{y}" stroke="#E3E9EF"/><text x="145" y="{y+5}" font-size="13" text-anchor="end">{value:g}</text>'
    for i,row in enumerate(summary):
        base=260+i*350
        for j,(_,idx) in enumerate(metrics):
            val=row[idx]; x=base+j*(width+8); y=800-val*500;svg+=f'<rect x="{x}" y="{y}" width="{width}" height="{800-y}" fill="{colors[j]}"/><text x="{x+width/2}" y="{y-10}" font-size="13" text-anchor="middle">{val:.3f}</text>'
        svg+=xml_text(base+140,840,row[0],15,"#172033","bold","middle")
    for j,(label,_) in enumerate(metrics): svg+=f'<rect x="{250+j*310}" y="235" width="25" height="25" fill="{colors[j]}"/>'+xml_text(285+j*310,255,label,13)
    export("FIG_E1_DETECTION_COMPARISON",im,svg,"Figure E1. Experiment A synthetic detection comparison","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic windows may be dependent; no operational false alarms/hour inference.",overwrite)
    return summary


def confusion(summary,overwrite):
    im,d=new_canvas("Figure E2. Experiment A confusion matrices","Positive class = fault window. Rows: observed ground truth; columns: detector prediction.")
    coords=[(160,290),(980,290),(160,630),(980,630)]
    svg=""
    for (name,tp,fp,tn,fn,*_), (x,y) in zip(summary,coords):
        d.text((x+210,y-28),name,font=B16,fill=COL["ink"],anchor="ma")
        d.text((x+210,y),"Predicted: nominal                         fault",font=F10,fill=COL["muted"],anchor="ma")
        d.text((x-22,y+125),"True: nominal",font=F10,fill=COL["muted"],anchor="ra")
        d.text((x-22,y+225),"True: fault",font=F10,fill=COL["muted"],anchor="ra")
        values=[(tn,"TN"),(fp,"FP"),(fn,"FN"),(tp,"TP")]
        for k,(val,lab) in enumerate(values):
            xx=x+(k%2)*210; yy=y+35+(k//2)*100; intensity=230-int(120*val/max(200,120)); fill=(220,intensity,220) if lab in ("TN","TP") else (255,225,210)
            d.rectangle((xx,yy,xx+190,yy+80),fill=fill,outline=COL["line"],width=2);d.text((xx+95,yy+20),lab,font=B12,fill=COL["ink"],anchor="ma");d.text((xx+95,yy+50),str(val),font=B16,fill=COL["ink"],anchor="ma")
        svg+=xml_text(x+210,y-28,name,18,"#172033","bold","middle")+xml_text(x+210,y,"Predicted: nominal                         fault",12,"#526071","normal","middle")
        for k,(val,lab) in enumerate(values):
            xx=x+(k%2)*210; yy=y+35+(k//2)*100; fill="#DCEADC" if lab in ("TN","TP") else "#FFE1D2";svg+=f'<rect x="{xx}" y="{yy}" width="190" height="80" fill="{fill}" stroke="#B9C3CF"/>'+xml_text(xx+95,yy+30,lab,16,"#172033","bold","middle")+xml_text(xx+95,yy+60,str(val),18,"#172033","normal","middle")
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Counts are synthetic benchmark results, not independent live observations.")
    export("FIG_E2_CONFUSION_MATRICES",im,svg,"Figure E2. Experiment A confusion matrices","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic benchmark counts; positive class is fault window.",overwrite)


def scenario(a,overwrite):
    scenarios=sorted({r["scenario"] for r in a if r["scenario"]!="NORMAL"})
    methods=[("Isolation Forest","iso_flag",COL["orange"]),("LSTM","lstm_flag",COL["green"]),("Combined","combined_flag",COL["blue"])]
    im,d=new_canvas("Figure E3. Experiment A scenario-level recall","Six fault scenarios, 20 synthetic fault windows each; scenario-cluster analysis is exploratory.")
    scale=chart_axes(d,(150,300,1680,800),[0,.2,.4,.6,.8,1],0,1,"recall")
    svg='<line x1="150" y1="800" x2="1680" y2="800" stroke="#172033" stroke-width="2"/>'
    for si,s in enumerate(scenarios):
        base=190+si*245
        for j,(name,key,color) in enumerate(methods):
            subset=[r for r in a if r["scenario"]==s]; v=sum(r[key]=="1" for r in subset)/len(subset); x=base+j*52;y=scale(v);d.rectangle((x,y,x+44,800),fill=color);d.text((x+22,y-30),f"{v:.2f}",font=F8,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{x}" y="{800-v*500}" width="44" height="{v*500}" fill="{color}"/><text x="{x+22}" y="{770-v*500}" text-anchor="middle" font-size="12">{v:.2f}</text>'
        d.text((base+68,830),wrap(s.replace("_"," "),14),font=F8,fill=COL["ink"],anchor="ma",spacing=2);svg+=xml_text(base+68,830,wrap(s.replace("_"," "),14),12,"#172033","normal","middle")
    for j,(name,_,color) in enumerate(methods):d.rectangle((250+j*340,235,275+j*340,260),fill=color);d.text((285+j*340,237),name,font=F10,fill=COL["ink"]);svg+=f'<rect x="{250+j*340}" y="235" width="25" height="25" fill="{color}"/>'+xml_text(285+j*340,255,name,13)
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Six scenario clusters only: descriptive/exploratory, not an operational generalization claim.")
    export("FIG_E3_SCENARIO_RECALL",im,svg,"Figure E3. Experiment A scenario-level recall","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Six scenario clusters; analysis is exploratory.",overwrite)


def diagnosis(b,overwrite):
    configs=[]
    for name in dict.fromkeys(r["configuration"] for r in b):
        rs=[r for r in b if r["configuration"]==name]; strict=sum(r["top1_strict"]=="1" for r in rs); assess=sum(r["rubric_verdict"]!="UNASSESSABLE" for r in rs); completed=sum(r["top1_strict"]=="1" and r["rubric_verdict"]!="UNASSESSABLE" for r in rs); mode=rs[0]["execution_mode"];configs.append((name,strict,len(rs),completed,assess,mode,len(rs)-assess))
    im,d=new_canvas("Figure E4. Experiment B diagnosis pilot: strict intent-to-treat and completed case","Strict outcomes retain UNASSESSABLE API omissions in denominator; completed-case denominator excludes them.")
    yscale=chart_axes(d,(175,300,1700,800),[0,.2,.4,.6,.8,1],0,1,"strict top-1 proportion")
    svg='<line x1="175" y1="800" x2="1700" y2="800" stroke="#172033" stroke-width="2"/>'
    for i,(name,st,n,co,ass,mode,omit) in enumerate(configs):
        x=230+i*205; values=[st/n,co/ass if ass else 0]; colors=[COL["purple"] if "groq" in mode else COL["blue"],COL["green"]]
        for j,v in enumerate(values):
            xx=x+j*65;y=yscale(v);label=f"{st}/{n}" if j==0 else f"{co}/{ass}";d.rectangle((xx,y,xx+52,800),fill=colors[j]);d.text((xx+26,y-27),label,font=F8,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{xx}" y="{800-v*500}" width="52" height="{v*500}" fill="{colors[j]}"/><text x="{xx+26}" y="{770-v*500}" text-anchor="middle" font-size="11">{label}</text>'
        d.text((x+52,835),f"C{i+1}",font=B12,fill=COL["ink"],anchor="ma");d.text((x+52,865),"Groq" if "groq" in mode else "offline",font=F8,fill=COL["purple"] if "groq" in mode else COL["blue"],anchor="ma");svg+=xml_text(x+52,835,f"C{i+1}",14,"#172033","bold","middle")+xml_text(x+52,865,"Groq" if "groq" in mode else "offline",12,"#6F4EA3" if "groq" in mode else "#2B6CB0","normal","middle")
        if omit: d.text((x+52,890),f"{omit} UNASSESSABLE",font=F8,fill=COL["red"],anchor="ma");svg+=xml_text(x+52,890,f"{omit} UNASSESSABLE",11,"#B63B3B","normal","middle")
    d.rectangle((260,235,285,260),fill=COL["blue"]);d.text((295,237),"strict ITT (offline) / strict ITT (Groq = purple)",font=F10,fill=COL["ink"]);d.rectangle((800,235,825,260),fill=COL["green"]);d.text((835,237),"strict completed case",font=F10,fill=COL["ink"])
    footer(d,"research/raw/diagnosis_predictions.csv; Phase 2 reconciliation.","Pilot result: no superiority, cost, token, or rate-limit-remediation claim.")
    svg+=f'<rect x="260" y="235" width="25" height="25" fill="#2B6CB0"/>'+xml_text(295,255,"strict ITT (offline) / strict ITT (Groq = purple)",13)+f'<rect x="800" y="235" width="25" height="25" fill="#198754"/>'+xml_text(835,255,"strict completed case",13)
    export("FIG_E4_DIAGNOSIS_PILOT",im,svg,"Figure E4. Experiment B diagnosis pilot: strict intent-to-treat and completed case","research/raw/diagnosis_predictions.csv; Phase 2 reconciliation.","UNASSESSABLE omissions visible; no superiority/cost claim.",overwrite)


def safety(c,overwrite):
    cases=Counter(r["case_type"] for r in c); attack=[r for r in c if r["case_type"]=="ATTACK_CASE"]; audit=sum(r["audit_trail_verified"]=="1" for r in c); contained=sum(r["verdict"]=="PASS" for r in attack)
    def wilson(x,n):
        z=1.959963984540054; p=x/n; den=1+z*z/n; cen=(p+z*z/(2*n))/den; rad=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return cen-rad,cen+rad
    ci_a,ci_u=wilson(contained,len(attack)),wilson(audit,len(c))
    im,d=new_canvas("Figure E5. Experiment C bounded local safety harness","Attack containment and audit-trail completeness, with reproducible Wilson 95% intervals.")
    bars=[("Attack containment",contained,len(attack),ci_a,COL["green"]),("Audit-trail completeness",audit,len(c),ci_u,COL["blue"])]
    for i,(label,x,n,ci,color) in enumerate(bars):
        y=345+i*180;d.text((190,y),label,font=B20,fill=COL["ink"]);d.rounded_rectangle((650,y,1510,y+70),radius=12,fill="#E7EDF3");d.rounded_rectangle((650,y,650+860*x/n,y+70),radius=12,fill=color);d.text((1535,y+15),f"{x}/{n} = {x/n:.3f}",font=B16,fill=COL["ink"]);d.text((650,y+92),f"Wilson 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]",font=F12,fill=COL["muted"])
    y=760;d.text((180,y),"Local-harness case taxonomy (n=16):",font=B16,fill=COL["ink"]);x=550
    for name,count in sorted(cases.items()):d.rounded_rectangle((x,y-20,x+190,y+35),radius=10,fill=COL["light"],outline=COL["line"]);d.text((x+95,y-8),f"{name}: {count}",font=F10,fill=COL["ink"],anchor="ma");x+=215
    footer(d,"research/raw/safety_test_results.csv; Phase 2 reconciliation.","Bounded local harness, not production-security certification; attack and audit denominators differ.")
    svg=""
    for i,(label,x,n,ci,color) in enumerate(bars):
        y=345+i*180;svg+=xml_text(190,y+30,label,21,"#172033","bold")+f'<rect x="650" y="{y}" width="860" height="70" rx="12" fill="#E7EDF3"/><rect x="650" y="{y}" width="{860*x/n}" height="70" rx="12" fill="{color}"/>'+xml_text(1535,y+42,f"{x}/{n} = {x/n:.3f}",18)+xml_text(650,y+112,f"Wilson 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]",14,"#526071")
    svg+=xml_text(180,760,"Local-harness case taxonomy (n=16):",18,"#172033","bold");x=550
    for name,count in sorted(cases.items()): svg+=f'<rect x="{x}" y="740" width="190" height="55" rx="10" fill="#F3F6F9" stroke="#B9C3CF"/>'+xml_text(x+95,773,f"{name}: {count}",12,"#172033","normal","middle");x+=215
    export("FIG_E5_SAFETY_HARNESS",im,svg,"Figure E5. Experiment C bounded local safety harness","research/raw/safety_test_results.csv; Phase 2 reconciliation.","Local-harness only; denominators differ between containment and audit completeness.",overwrite)


def live_summary(live,overwrite):
    modes=Counter(r["detector_mode"] for r in live); null=sum(not r["anomaly_score"].strip() for r in live); faults=Counter(r["fault_mode"] for r in live); sources=Counter(r["data_source"] for r in live)
    im,d=new_canvas("Figure E6. Live telemetry evidence summary", "Stored workflow-associated records and detector-mode facts; no independent ground-truth performance labels.")
    cards=[("Stored rows",str(len(live)),COL["green"]),("Bootstrap-rules rows",str(modes.get("bootstrap_rules",0)),COL["green"]),("Null LSTM scores",str(null),COL["gray"]),("Live-LSTM scored rows",str(len(live)-null),COL["red"])]
    for i,(t,v,c) in enumerate(cards):
        x=110+i*420;d.rounded_rectangle((x,300,x+350,520),radius=20,fill=COL["light"],outline=c,width=4);d.text((x+175,340),t,font=B12,fill=COL["ink"],anchor="ma");d.text((x+175,410),v,font=B34,fill=c,anchor="ma");d.text((x+175,470),"stored evidence",font=F10,fill=COL["muted"],anchor="ma")
    d.text((110,610),"Fault-mode field (stored workflow-associated observations; not independent labels)",font=B16,fill=COL["ink"])
    total=sum(faults.values());x=110
    palette=[COL["blue"],COL["orange"],COL["purple"],COL["green"]]
    for i,(name,count) in enumerate(sorted(faults.items())):
        width=1450*count/total;d.rectangle((x,665,x+width,745),fill=palette[i%len(palette)]);d.text((x+width/2,690),f"{name}: {count}",font=B12,fill=COL["white"],anchor="ma");x+=width
    d.text((110,805),"Data-source values: "+"; ".join(f"{k}={v}" for k,v in sorted(sources.items())),font=F10,fill=COL["muted"])
    footer(d,"research/exports/telemetry.csv; Phase 2 reconciliation.","No live ROC, PR, accuracy, specificity, FPR, or alarms-per-hour metric is plotted.")
    svg=""
    for i,(t,v,c) in enumerate(cards):
        x=110+i*420;svg+=f'<rect x="{x}" y="300" width="350" height="220" rx="20" fill="#F3F6F9" stroke="{c}" stroke-width="3"/>'+xml_text(x+175,350,t,15,"#172033","bold","middle")+xml_text(x+175,445,v,36,c,"bold","middle")+xml_text(x+175,480,"stored evidence",12,"#526071","normal","middle")
    svg+=xml_text(110,630,"Fault-mode field (stored workflow-associated observations; not independent labels)",18,"#172033","bold");x=110
    for i,(name,count) in enumerate(sorted(faults.items())):
        width=1450*count/total;svg+=f'<rect x="{x}" y="665" width="{width}" height="80" fill="{palette[i%len(palette)]}"/>'+xml_text(x+width/2,715,f"{name}: {count}",14,"#fff","bold","middle");x+=width
    svg+=xml_text(110,805,"Data-source values: "+"; ".join(f"{k}={v}" for k,v in sorted(sources.items())),12,"#526071")
    export("FIG_E6_LIVE_EVIDENCE",im,svg,"Figure E6. Live telemetry evidence summary","research/exports/telemetry.csv; Phase 2 reconciliation.","No live classification-performance claim.",overwrite)


def readiness(overwrite):
    im,d=new_canvas("Figure F. Experiment D external-validation readiness (not a performance result)","AnoMod input/archive provenance is present; required production evaluation evidence is unavailable.")
    items=[("Archive + provenance","present","green"),("Extraction manifest","present","green"),("24-step nominal-window compatibility","blocked","red"),("Calibration / evaluation separation","blocked","red"),("Production predictions + metrics","absent","gray"),("Ratification record","absent","gray")]
    for i,(t,state,c) in enumerate(items):
        x=110+(i%3)*550;y=310+(i//3)*280;box(d,(x,y,x+450,y+190),t,state,c,state.upper())
    d.text((900,900),"External performance results are unavailable.",font=B20,fill=COL["red"],anchor="ma")
    footer(d,"Phase 1 evidence freeze; Phase 2 reconciliation; Phase 3 architecture audit.","Readiness/provenance panel only: it is not an AnoMod performance chart or confusion matrix.")
    svg=""
    for i,(t,state,c) in enumerate(items):
        x=110+(i%3)*550;y=310+(i//3)*280;svg+=svg_box(x,y,450,190,t,state,COL[c],state.upper())
    svg+=xml_text(900,900,"External performance results are unavailable.",22,"#B63B3B","bold","middle")
    export("FIG_F_EXPERIMENT_D_READINESS",im,svg,"Figure F. Experiment D external-validation readiness (not a performance result)","Phase 1 evidence freeze; Phase 2 reconciliation; Phase 3 architecture audit.","Readiness/provenance only; no AnoMod performance result exists.",overwrite)


# ---------------------------------------------------------------------------
# Phase 4.1 visual remediation overrides.  These definitions intentionally
# replace the Phase 4 layouts while retaining the data loading and arithmetic
# above.  Each title/body is shortened only for layout; the full evidence
# boundary remains in the caption and source note.

def architecture(overwrite):
    im,d=new_canvas("Figure A. Audited architecture", "Implemented flow, observed bootstrap path, and restricted local-demo boundary.")
    top=[(70,230,330,450,"Streamlit UI","Monitor view and approval input","blue","IMPLEMENTED"),(390,230,670,450,"Collector","Host metrics + target HTTP probe","green","OBSERVED"),(730,230,990,450,"SQLite","Telemetry + incident events","blue","IMPLEMENTED"),(1050,230,1310,450,"Bootstrap rules","Observed decision path","green","OBSERVED"),(1370,230,1730,450,"Event + verification","Persist event; health + probe check","blue","IMPLEMENTED")]
    bottom=[(70,610,350,825,"Incident workflow","Manager → investigation → diagnosis","blue","IMPLEMENTED"),(420,610,700,825,"Approval ticket","Unauthenticated audit label","orange","WORKFLOW GUARD"),(770,610,1060,825,"Demo recovery","clear_demo_service_fault only","orange","LOCAL DEMO ONLY"),(1130,610,1410,825,"Live LSTM","Separate checkpoint unavailable","gray","OPTIONAL / BLOCKED")]
    for x,y,x2,y2,t,b,c,s in top+bottom: box(d,(x,y,x2,y2),t,b,c,s)
    for a,b in [((330,340),(390,340)),((670,340),(730,340)),((990,340),(1050,340)),((1310,340),(1370,340)),((350,715),(420,715)),((700,715),(770,715))]: arrow(d,a,b)
    arrow(d,(1060,715),(1370,450),"gray",True)
    d.rounded_rectangle((1460,610,1730,825),radius=16,fill="#FFF8E7",outline=COL["orange"],width=3)
    multiline(d,(1480,642),"Trust boundary\nCollector-host metrics\nremain distinct from\ntarget HTTP probe.\nRemote targets:\nmonitor-only.",F12,COL["ink"],spacing=5)
    footer(d,"Phase 3 architecture audit and diagram specification.","No remote remediation, authenticated dual control, or production authorization claim.")
    svg="".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in top+bottom)
    for a,b in [((330,340),(390,340)),((670,340),(730,340)),((990,340),(1050,340)),((1310,340),(1370,340)),((350,715),(420,715)),((700,715),(770,715))]: svg+=svg_arrow(*a,*b)
    svg+=svg_arrow(1060,715,1370,450,"#7A8594",True)+'<rect x="1460" y="610" width="270" height="215" rx="16" fill="#FFF8E7" stroke="#C77800" stroke-width="2"/>'+xml_text(1480,660,"Trust boundary",15,"#172033","bold")+xml_text(1480,690,"Collector-host metrics",13)+xml_text(1480,712,"remain distinct from",13)+xml_text(1480,734,"target HTTP probe.",13)+xml_text(1480,766,"Remote targets: monitor-only.",13)
    export("FIG_A_ARCHITECTURE",im,svg,"Figure A. Audited architecture","Phase 3 architecture audit and diagram specification.","No remote remediation, authenticated dual control, or production authorization claim.",overwrite)


def model(metadata,overwrite):
    im,d=new_canvas("Figure B. Frozen LSTM contract", "Frozen synthetic-benchmark model; intended live checkpoint is separate and unavailable.", margin=120)
    nodes=[(55,285,295,535,"Input","24 × 5 window\ncpu, memory, latency\nerror rate, disk","blue","FROZEN"),(335,285,575,535,"Normalize","Frozen mean / std","blue","FROZEN"),(615,285,855,535,"Encoder LSTM","5 → 16\nfinal h (16)","blue","IMPLEMENTED"),(895,285,1135,535,"Repeat","Repeat h over 24 steps","blue","IMPLEMENTED"),(1175,285,1415,535,"Decoder LSTM","16 → 16","blue","IMPLEMENTED"),(1455,285,1745,535,"Score","Linear 16 → 5\nreconstruction MSE\nscore > 0.7093990445137024","green","SYNTHETIC")]
    for x,y,x2,y2,t,b,c,s in nodes: box(d,(x,y,x2,y2),t,b,c,s)
    for left,right in zip(nodes,nodes[1:]): arrow(d,(left[2],410),(right[0],410))
    d.rounded_rectangle((150,670,1650,830),radius=18,fill="#FFF8E7",outline=COL["orange"],width=3)
    multiline(d,(190,704),"Per-feature reconstruction-error comparisons accompany the global MSE decision.\nThe 16-dimensional hidden state is not a validated causal representation.\nNo live-training checkpoint or live-inference result is represented here.",F14,COL["ink"],spacing=8)
    footer(d,"models/lstm_autoencoder.json; Phase 3 implementation audit.","Frozen synthetic-benchmark contract only; it does not establish live inference performance.", margin=120)
    svg="".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in nodes)
    for left,right in zip(nodes,nodes[1:]): svg+=svg_arrow(left[2],410,right[0],410)
    svg+='<rect x="150" y="670" width="1500" height="160" rx="18" fill="#FFF8E7" stroke="#C77800" stroke-width="2"/>'+xml_text(190,720,"Per-feature reconstruction-error comparisons accompany the global MSE decision.",16)+xml_text(190,760,"The 16-dimensional hidden state is not a validated causal representation.",16)+xml_text(190,800,"No live-training checkpoint or live-inference result is represented here.",16)
    export("FIG_B_FROZEN_LSTM",im,svg,"Figure B. Frozen LSTM contract","models/lstm_autoencoder.json; Phase 3 implementation audit.","Frozen synthetic-benchmark contract only; it does not establish live inference performance.",overwrite)


def telemetry_flow(overwrite):
    im,d=new_canvas("Figure C. Telemetry-to-alert flow", "Observed bootstrap-only session is distinct from optional, unobserved model inference.")
    top=[(55,250,315,470,"Collection","Host metrics + target probe\n5 s intended; not uniform","green","OBSERVED"),(370,250,630,470,"Rolling error rate","Current + prior records","blue","IMPLEMENTED"),(685,250,945,470,"Persist","SQLite telemetry row","green","OBSERVED"),(1000,250,1260,470,"Last-24 window","Insertion order; no\ntimestamp continuity check","blue","IMPLEMENTED"),(1315,250,1575,470,"Optional inference","Live LSTM if checkpoint loads","gray","NOT OBSERVED")]
    for x,y,x2,y2,t,b,c,s in top:box(d,(x,y,x2,y2),t,b,c,s)
    for left,right in zip(top,top[1:]):arrow(d,(left[2],360),(right[0],360),"gray" if left[4]=="Last-24 window" else "ink",left[4]=="Last-24 window")
    box(d,(1260,580,1520,790),"Rule guard","Bootstrap rules / model guard","green","OBSERVED")
    box(d,(1570,580,1740,790),"Event","Annotate + persist","green","OBSERVED")
    arrow(d,(1520,685),(1570,685));arrow(d,(1130,470),(1390,580),"ink");arrow(d,(1445,470),(1445,580),"gray",True)
    d.rounded_rectangle((100,850,1700,935),radius=16,fill="#EAF7EF",outline=COL["green"],width=3)
    d.text((130,868),"AUDITED SESSION",font=B16,fill=COL["green"])
    d.text((130,905),"200 stored rows  |  bootstrap rules only  |  200 null LSTM scores",font=B16,fill=COL["green"])
    footer(d,"research/exports/telemetry.csv; Phase 2 reconciliation; Phase 3 architecture audit.","No live ROC, PR, accuracy, specificity, FPR, or alarms/hour interpretation.")
    svg="".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in top)+svg_box(1260,580,260,210,"Rule guard","Bootstrap rules / model guard",COL["green"],"OBSERVED")+svg_box(1570,580,170,210,"Event","Annotate + persist",COL["green"],"OBSERVED")
    for left,right in zip(top,top[1:]):svg+=svg_arrow(left[2],360,right[0],360,"#7A8594" if left[4]=="Last-24 window" else "#172033",left[4]=="Last-24 window")
    svg+=svg_arrow(1520,685,1570,685)+svg_arrow(1130,470,1390,580)+svg_arrow(1445,470,1445,580,"#7A8594",True)+'<rect x="100" y="850" width="1600" height="85" rx="16" fill="#EAF7EF" stroke="#198754" stroke-width="2"/>'+xml_text(130,883,"AUDITED SESSION",16,"#198754","bold")+xml_text(130,918,"200 stored rows  |  bootstrap rules only  |  200 null LSTM scores",17,"#198754","bold")
    export("FIG_C_TELEMETRY_FLOW",im,svg,"Figure C. Telemetry-to-alert flow","research/exports/telemetry.csv; Phase 2 reconciliation; Phase 3 architecture audit.","No live classification-performance claim.",overwrite)


def workflow(overwrite):
    im,d=new_canvas("Figure D. Diagnosis and approval workflow", "Implemented components and local-demo restrictions; configuration-level execution is separate evidence.", margin=120)
    upper=[(90,250,410,455,"Manager","Incident construction","blue","IMPLEMENTED"),(500,250,820,455,"Investigation","Evidence collection","blue","IMPLEMENTED"),(910,250,1230,455,"Diagnosis","Offline deterministic\nor Groq API","purple","API BOUNDARY"),(1320,250,1640,455,"Resolution","Action selection","blue","IMPLEMENTED")]
    lower=[(90,605,410,810,"Human approval","Ticket request / consume\nunauthenticated audit label","orange","WORKFLOW GUARD"),(500,605,820,810,"Local-demo recovery","clear_demo_service_fault","orange","LOCAL DEMO ONLY"),(910,605,1230,810,"Independent check","Health + HTTP probe","blue","IMPLEMENTED"),(1320,605,1640,810,"Verification","Event persistence","blue","IMPLEMENTED")]
    for x,y,x2,y2,t,b,c,s in upper+lower:box(d,(x,y,x2,y2),t,b,c,s)
    for group,y in [(upper,352),(lower,707)]:
        for left,right in zip(group,group[1:]):arrow(d,(left[2],y),(right[0],y))
    arrow(d,(1480,455),(250,605),"ink")
    d.rounded_rectangle((210,865,1590,940),radius=16,fill="#FFF8E7",outline=COL["orange"],width=3)
    d.text((240,880),"Groq/API boundary: no source-visible explicit retry, timeout, or rate-limit handling.",font=F12,fill=COL["ink"])
    d.text((240,910),"Approval is a workflow guard, not authenticated dual control or production authorization.",font=F12,fill=COL["ink"])
    footer(d,"Phase 3 implementation audit; Phase 2 Experiment B reconciliation.","No claim that every component ran in every evaluated configuration or audited live session.", margin=120)
    svg="".join(svg_box(x,y,x2-x,y2-y,t,b,COL[c],s) for x,y,x2,y2,t,b,c,s in upper+lower)
    for group,y in [(upper,352),(lower,707)]:
        for left,right in zip(group,group[1:]):svg+=svg_arrow(left[2],y,right[0],y)
    svg+=svg_arrow(1480,455,250,605)+'<rect x="210" y="865" width="1380" height="75" rx="16" fill="#FFF8E7" stroke="#C77800" stroke-width="2"/>'+xml_text(240,895,"Groq/API boundary: no source-visible explicit retry, timeout, or rate-limit handling.",14)+xml_text(240,925,"Approval is a workflow guard, not authenticated dual control or production authorization.",14)
    export("FIG_D_DIAGNOSIS_APPROVAL",im,svg,"Figure D. Diagnosis and approval workflow","Phase 3 implementation audit; Phase 2 Experiment B reconciliation.","No claim that every component ran in every evaluated configuration or audited live session.",overwrite)


def detection(a,overwrite,emit=True):
    methods=[("Rules","rule_flag"),("Isolation Forest","iso_flag"),("LSTM","lstm_flag"),("Combined","combined_flag")]; summary=[]
    for name,key in methods:
        tp=sum(r["ground_truth"]=="1" and r[key]=="1" for r in a);fp=sum(r["ground_truth"]=="0" and r[key]=="1" for r in a);tn=sum(r["ground_truth"]=="0" and r[key]=="0" for r in a);fn=sum(r["ground_truth"]=="1" and r[key]=="0" for r in a);p=tp/(tp+fp);rec=tp/(tp+fn);f1=2*p*rec/(p+rec);summary.append((name,tp,fp,tn,fn,p,rec,f1,fp/(fp+tn)))
    im,d=new_canvas("Figure E1. Synthetic detection comparison","320 windows: 200 nominal and 120 fault windows across six synthetic scenarios.")
    scale=chart_axes(d,(160,310,1680,785),[0,.2,.4,.6,.8,1],0,1,"rate"); metrics=[("Precision",5,COL["blue"]),("Recall",6,COL["green"]),("F1",7,COL["purple"]),("FPR",8,COL["orange"])]
    for j,(label,_,color) in enumerate(metrics):d.rectangle((250+j*300,225,272+j*300,247),fill=color);d.text((282+j*300,224),label,font=F10,fill=COL["ink"])
    for i,row in enumerate(summary):
        base=260+i*360
        for j,(_,idx,color) in enumerate(metrics):
            v=row[idx];x=base+j*70;y=scale(v);d.rectangle((x,y,x+58,785),fill=color);d.text((x+29,max(270,y-25)),f"{v:.3f}",font=F10,fill=COL["ink"],anchor="ma")
        d.text((base+125,820),row[0],font=B16,fill=COL["ink"],anchor="ma")
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic windows may be dependent; no operational false-alarms-per-hour inference.")
    svg='<line x1="160" y1="310" x2="160" y2="785" stroke="#172033" stroke-width="2"/><line x1="160" y1="785" x2="1680" y2="785" stroke="#172033" stroke-width="2"/>'
    for value in [0,.2,.4,.6,.8,1]:y=785-value*475;svg+=f'<line x1="160" y1="{y}" x2="1680" y2="{y}" stroke="#E3E9EF"/><text x="140" y="{y+4}" font-size="12" text-anchor="end">{value:g}</text>'
    for j,(label,_,color) in enumerate(metrics):svg+=f'<rect x="{250+j*300}" y="225" width="22" height="22" fill="{color}"/>'+xml_text(282+j*300,243,label,12)
    for i,row in enumerate(summary):
        base=260+i*360
        for j,(_,idx,color) in enumerate(metrics):v=row[idx];x=base+j*70;y=785-v*475;svg+=f'<rect x="{x}" y="{y}" width="58" height="{785-y}" fill="{color}"/>'+xml_text(x+29,max(270,y-12),f"{v:.3f}",12,"#172033","normal","middle")
        svg+=xml_text(base+125,820,row[0],14,"#172033","bold","middle")
    if emit:
        export("FIG_E1_DETECTION_COMPARISON",im,svg,"Figure E1. Synthetic detection comparison","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic windows may be dependent; no operational false-alarms-per-hour inference.",overwrite)
    return summary


def confusion(summary,overwrite):
    im,d=new_canvas("Figure E2. Confusion matrices", "Positive class: fault window. In each panel: rows are ground truth and columns are prediction.", margin=120)
    coords=[(140,260),(970,260),(140,590),(970,590)];svg=""
    for (name,tp,fp,tn,fn,*_),(x,y) in zip(summary,coords):
        d.text((x+300,y-25),name,font=B16,fill=COL["ink"],anchor="ma");d.text((x+300,y+10),"Prediction: nominal                 fault",font=F10,fill=COL["muted"],anchor="ma");d.text((x,y+95),"True\nnominal",font=F10,fill=COL["muted"],anchor="ra");d.text((x,y+190),"True\nfault",font=F10,fill=COL["muted"],anchor="ra")
        for k,(v,label) in enumerate([(tn,"TN"),(fp,"FP"),(fn,"FN"),(tp,"TP")]):
            xx=x+45+(k%2)*250;yy=y+32+(k//2)*100;fill="#DCEADC" if label in ("TN","TP") else "#FFE1D2";d.rectangle((xx,yy,xx+220,yy+75),fill=fill,outline=COL["line"],width=2);d.text((xx+110,yy+12),label,font=B12,fill=COL["ink"],anchor="ma");d.text((xx+110,yy+43),str(v),font=B16,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{xx}" y="{yy}" width="220" height="75" fill="{fill}" stroke="#B9C3CF"/>'+xml_text(xx+110,yy+28,label,15,"#172033","bold","middle")+xml_text(xx+110,yy+58,str(v),18,"#172033","bold","middle")
        svg+=xml_text(x+300,y-25,name,17,"#172033","bold","middle")+xml_text(x+300,y+10,"Prediction: nominal                 fault",12,"#526071","normal","middle")
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic benchmark counts, not independent live observations.", margin=120)
    export("FIG_E2_CONFUSION_MATRICES",im,svg,"Figure E2. Confusion matrices","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Synthetic benchmark counts; positive class is fault window.",overwrite)


def scenario(a,overwrite):
    scenarios=sorted({r["scenario"] for r in a if r["scenario"]!="NORMAL"});methods=[("Isolation Forest","iso_flag",COL["orange"]),("LSTM","lstm_flag",COL["green"]),("Combined","combined_flag",COL["blue"])]
    im,d=new_canvas("Figure E3. Scenario-level recall", "Six synthetic fault scenarios; 20 fault windows per scenario. Analysis is exploratory.")
    scale=chart_axes(d,(150,310,1680,785),[0,.2,.4,.6,.8,1],0,1,"recall");svg='<line x1="150" y1="785" x2="1680" y2="785" stroke="#172033" stroke-width="2"/>'
    for j,(label,_,color) in enumerate(methods):d.rectangle((260+j*340,225,282+j*340,247),fill=color);d.text((292+j*340,224),label,font=F10,fill=COL["ink"]);svg+=f'<rect x="{260+j*340}" y="225" width="22" height="22" fill="{color}"/>'+xml_text(292+j*340,243,label,12)
    for i,s in enumerate(scenarios):
        base=205+i*245
        for j,(_,key,color) in enumerate(methods):v=sum(r[key]=="1" for r in a if r["scenario"]==s)/20;x=base+j*58;y=scale(v);d.rectangle((x,y,x+48,785),fill=color);d.text((x+24,max(270,y-23)),f"{v:.2f}",font=F8,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{x}" y="{785-v*475}" width="48" height="{v*475}" fill="{color}"/>'+xml_text(x+24,max(270,785-v*475-10),f"{v:.2f}",11,"#172033","normal","middle")
        d.text((base+80,820),s,font=F10,fill=COL["ink"],anchor="ma");svg+=xml_text(base+80,820,s,12,"#172033","normal","middle")
    footer(d,"research/raw/detection_predictions.csv; Phase 2 reconciliation.","Six scenario clusters only: descriptive/exploratory, not operational generalization.")
    export("FIG_E3_SCENARIO_RECALL",im,svg,"Figure E3. Scenario-level recall","research/raw/detection_predictions.csv; Phase 2 reconciliation.","Six scenario clusters; analysis is exploratory.",overwrite)


def diagnosis(b,overwrite):
    configs=[]
    for name in dict.fromkeys(r["configuration"] for r in b):
        rs=[r for r in b if r["configuration"]==name];st=sum(r["top1_strict"]=="1" for r in rs);ass=sum(r["rubric_verdict"]!="UNASSESSABLE" for r in rs);co=sum(r["top1_strict"]=="1" and r["rubric_verdict"]!="UNASSESSABLE" for r in rs);configs.append((st,co,ass,"groq" in rs[0]["execution_mode"].lower(),len(rs)-ass))
    im,d=new_canvas("Figure E4. Diagnosis pilot outcomes", "Strict intent-to-treat retains API omissions; completed-case excludes only UNASSESSABLE omissions.", margin=120)
    scale=chart_axes(d,(175,325,1670,765),[0,.2,.4,.6,.8,1],0,1,"strict top-1 proportion");d.rectangle((250,235,272,257),fill=COL["blue"]);d.text((282,234),"strict ITT (offline; Groq in purple)",font=F10,fill=COL["ink"]);d.rectangle((790,235,812,257),fill=COL["green"]);d.text((822,234),"strict completed case",font=F10,fill=COL["ink"]);svg='<line x1="175" y1="765" x2="1670" y2="765" stroke="#172033" stroke-width="2"/>'+f'<rect x="250" y="235" width="22" height="22" fill="{COL["blue"]}"/>'+xml_text(282,253,"strict ITT (offline; Groq in purple)",12)+f'<rect x="790" y="235" width="22" height="22" fill="{COL["green"]}"/>'+xml_text(822,253,"strict completed case",12)
    for i,(st,co,ass,is_groq,omit) in enumerate(configs):
        x=230+i*205;v1=st/6;v2=co/ass;first=COL["purple"] if is_groq else COL["blue"]
        for j,(v,c,label) in enumerate([(v1,first,f"{st}/6"),(v2,COL["green"],f"{co}/{ass}")]):
            xx=x+j*72;y=scale(v);d.rectangle((xx,y,xx+58,765),fill=c);d.text((xx+29,max(285,y-24)),label,font=F10,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{xx}" y="{765-v*440}" width="58" height="{v*440}" fill="{c}"/>'+xml_text(xx+29,max(285,765-v*440-10),label,11,"#172033","normal","middle")
        d.text((x+65,800),f"C{i+1}",font=B12,fill=COL["ink"],anchor="ma");d.text((x+65,828),"Groq" if is_groq else "offline",font=F8,fill=first,anchor="ma");svg+=xml_text(x+65,800,f"C{i+1}",14,"#172033","bold","middle")+xml_text(x+65,827,"Groq" if is_groq else "offline",11,first,"normal","middle")
        if omit:d.text((x+65,852),"1 UNASSESSABLE",font=F8,fill=COL["red"],anchor="ma");svg+=xml_text(x+65,852,"1 UNASSESSABLE",10,"#B63B3B","normal","middle")
    d.text((220,885),"C1 Rule baseline   C2 Single offline   C3 Full offline   C4 No-DL offline   C5 Single Groq   C6 Full Groq   C7 No-DL Groq",font=F8,fill=COL["muted"])
    footer(d,"research/raw/diagnosis_predictions.csv; Phase 2 reconciliation.","No superiority, cost, token, or rate-limit-remediation claim.", margin=120)
    svg+=xml_text(220,885,"C1 Rule baseline | C2 Single offline | C3 Full offline | C4 No-DL offline | C5 Single Groq | C6 Full Groq | C7 No-DL Groq",11,"#526071")
    export("FIG_E4_DIAGNOSIS_PILOT",im,svg,"Figure E4. Diagnosis pilot outcomes","research/raw/diagnosis_predictions.csv; Phase 2 reconciliation.","UNASSESSABLE omissions visible; no superiority/cost claim.",overwrite)


def safety(c,overwrite):
    cases=Counter(r["case_type"] for r in c);attack=[r for r in c if r["case_type"]=="ATTACK_CASE"];audit=sum(r["audit_trail_verified"]=="1" for r in c);contained=sum(r["verdict"]=="PASS" for r in attack)
    def wilson(x,n):z=1.959963984540054;p=x/n;den=1+z*z/n;cen=(p+z*z/(2*n))/den;rad=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return cen-rad,cen+rad
    bars=[("Attack containment",contained,11,wilson(contained,11),COL["green"]),("Audit-trail completeness",audit,16,wilson(audit,16),COL["blue"])]
    im,d=new_canvas("Figure E5. Local safety harness", "Bounded local-harness outcomes with Wilson 95% intervals and separate denominators.")
    svg=""
    for i,(label,x,n,ci,color) in enumerate(bars):
        y=310+i*190;d.text((145,y+15),label,font=B20,fill=COL["ink"]);d.rounded_rectangle((650,y,1450,y+62),radius=10,fill="#E7EDF3");d.rounded_rectangle((650,y,650+800*x/n,y+62),radius=10,fill=color);d.text((1490,y+12),f"{x}/{n} = {x/n:.3f}",font=B16,fill=COL["ink"]);d.text((650,y+88),f"Wilson 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]",font=F12,fill=COL["muted"]);svg+=xml_text(145,y+28,label,20,"#172033","bold")+f'<rect x="650" y="{y}" width="800" height="62" rx="10" fill="#E7EDF3"/><rect x="650" y="{y}" width="{800*x/n}" height="62" rx="10" fill="{color}"/>'+xml_text(1490,y+38,f"{x}/{n} = {x/n:.3f}",18)+xml_text(650,y+88,f"Wilson 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]",14,"#526071")
    d.text((145,735),"Case taxonomy (n=16)",font=B16,fill=COL["ink"]);svg+=xml_text(145,735,"Case taxonomy (n=16)",18,"#172033","bold")
    labels=[("Attack cases",11),("Precondition checks",2),("Positive controls",2),("Verification probe",1)]
    for i,(name,count) in enumerate(labels):
        x=145+i*400;d.rounded_rectangle((x,770,x+350,842),radius=10,fill=COL["light"],outline=COL["line"]);d.text((x+175,792),name,font=B12,fill=COL["ink"],anchor="ma");d.text((x+175,820),str(count),font=B16,fill=COL["ink"],anchor="ma");svg+=f'<rect x="{x}" y="770" width="350" height="72" rx="10" fill="#F3F6F9" stroke="#B9C3CF"/>'+xml_text(x+175,795,name,14,"#172033","bold","middle")+xml_text(x+175,824,str(count),18,"#172033","bold","middle")
    footer(d,"research/raw/safety_test_results.csv; Phase 2 reconciliation.","Bounded local harness, not production-security certification; denominators differ.")
    export("FIG_E5_SAFETY_HARNESS",im,svg,"Figure E5. Local safety harness","research/raw/safety_test_results.csv; Phase 2 reconciliation.","Bounded local harness; attack and audit denominators differ.",overwrite)


def live_summary(live,overwrite):
    modes=Counter(r["detector_mode"] for r in live);null=sum(not r["anomaly_score"].strip() for r in live);faults=Counter(r["fault_mode"] for r in live)
    im,d=new_canvas("Figure E6. Live telemetry evidence", "Stored workflow-associated records; no independent ground-truth performance labels.", margin=120)
    cards=[("Stored rows",len(live),COL["green"]),("Bootstrap-rules rows",modes["bootstrap_rules"],COL["green"]),("Null LSTM scores",null,COL["gray"]),("Live-LSTM scored rows",len(live)-null,COL["red"])]
    svg=""
    for i,(label,value,color) in enumerate(cards):
        x=90+i*430;d.rounded_rectangle((x,270,x+370,515),radius=18,fill=COL["light"],outline=color,width=4);d.text((x+185,320),label,font=B16,fill=COL["ink"],anchor="ma");d.text((x+185,390),str(value),font=B34,fill=color,anchor="ma");d.text((x+185,455),"stored evidence",font=F10,fill=COL["muted"],anchor="ma");svg+=f'<rect x="{x}" y="270" width="370" height="245" rx="18" fill="#F3F6F9" stroke="{color}" stroke-width="3"/>'+xml_text(x+185,330,label,16,"#172033","bold","middle")+xml_text(x+185,420,str(value),34,color,"bold","middle")+xml_text(x+185,460,"stored evidence",12,"#526071","normal","middle")
    d.text((90,600),"Stored fault-mode field (workflow-associated observations; not independent labels)",font=B16,fill=COL["ink"]);svg+=xml_text(90,600,"Stored fault-mode field (workflow-associated observations; not independent labels)",18,"#172033","bold")
    total=sum(faults.values());x=90;palette=[COL["blue"],COL["orange"],COL["purple"],COL["green"]]
    for i,(name,count) in enumerate(sorted(faults.items())):
        width=1620*count/total;d.rectangle((x,650,x+width,730),fill=palette[i]);
        if width >= 150: d.text((x+width/2,675),f"{name}: {count}",font=B12,fill=COL["white"],anchor="ma")
        svg+=f'<rect x="{x}" y="650" width="{width}" height="80" fill="{palette[i]}"/>'
        if width >= 150: svg+=xml_text(x+width/2,700,f"{name}: {count}",15,"#fff","bold","middle")
        x+=width
    d.text((90,780),"Fault-mode counts: error = 168  |  latency = 1  |  normal = 31",font=F10,fill=COL["muted"]);d.text((90,815),"Data source: live_local_host_and_http_probe = 200",font=F10,fill=COL["muted"]);svg+=xml_text(90,780,"Fault-mode counts: error = 168  |  latency = 1  |  normal = 31",13,"#526071")+xml_text(90,815,"Data source: live_local_host_and_http_probe = 200",13,"#526071")
    footer(d,"research/exports/telemetry.csv; Phase 2 reconciliation.","No live ROC, PR, accuracy, specificity, FPR, or alarms-per-hour figure.", margin=120)
    export("FIG_E6_LIVE_EVIDENCE",im,svg,"Figure E6. Live telemetry evidence","research/exports/telemetry.csv; Phase 2 reconciliation.","No live classification-performance claim.",overwrite)


def readiness(overwrite):
    im,d=new_canvas("Figure F. Experiment D readiness", "Readiness and provenance only. External performance results are unavailable.")
    items=[("Archive + provenance","PRESENT","green"),("Extraction manifest","PRESENT","green"),("24-step compatibility","BLOCKED","red"),("Calibration separation","BLOCKED","red"),("Predictions + metrics","ABSENT","gray"),("Ratification record","ABSENT","gray")]
    svg=""
    for i,(title,state,color) in enumerate(items):
        x=130+(i%3)*540;y=290+(i//3)*260;box(d,(x,y,x+460,y+180),title,state.lower(),color,state);svg+=svg_box(x,y,460,180,title,state.lower(),COL[color],state)
    d.text((900,860),"External performance results are unavailable.",font=B20,fill=COL["red"],anchor="ma");svg+=xml_text(900,860,"External performance results are unavailable.",23,"#B63B3B","bold","middle")
    footer(d,"Phase 1 evidence freeze; Phase 2 reconciliation; Phase 3 architecture audit.","Readiness/provenance panel only; not an AnoMod performance chart or confusion matrix.")
    export("FIG_F_EXPERIMENT_D_READINESS",im,svg,"Figure F. Experiment D readiness","Phase 1 evidence freeze; Phase 2 reconciliation; Phase 3 architecture audit.","Readiness/provenance only; no AnoMod performance result exists.",overwrite)


def manifest():
    files=[]
    for path in sorted(OUT.iterdir()):
        if path.is_file() and path.name != "PHASE4_SHA256_MANIFEST.json":
            files.append({"path": path.name, "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT / "PHASE4_SHA256_MANIFEST.json").write_text(json.dumps({"schema":"phase4-figure-manifest-v1","files":files},indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--overwrite",action="store_true",help="overwrite only selected generated renderings")
    parser.add_argument("--output-dir",type=Path,help="stage renderings outside the controlled figure directory")
    parser.add_argument("--targets",help="comma-separated figure stems; defaults to the complete controlled set")
    parser.add_argument("--formats",default="png,pdf,svg",help="comma-separated output formats: png,pdf,svg")
    parser.add_argument("--no-manifest",action="store_true",help="do not write a manifest (for partial staged renders)")
    args=parser.parse_args()
    global OUT, FORMATS
    if args.output_dir:
        OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
    FORMATS=tuple(x.strip().lower() for x in args.formats.split(",") if x.strip())
    if not FORMATS or any(x not in {"png","pdf","svg"} for x in FORMATS):
        raise ValueError("--formats must contain only png,pdf,svg")
    all_targets={"FIG_A_ARCHITECTURE","FIG_B_FROZEN_LSTM","FIG_C_TELEMETRY_FLOW","FIG_D_DIAGNOSIS_APPROVAL","FIG_E1_DETECTION_COMPARISON","FIG_E2_CONFUSION_MATRICES","FIG_E3_SCENARIO_RECALL","FIG_E4_DIAGNOSIS_PILOT","FIG_E5_SAFETY_HARNESS","FIG_E6_LIVE_EVIDENCE","FIG_F_EXPERIMENT_D_READINESS"}
    targets=set(x.strip() for x in args.targets.split(",")) if args.targets else all_targets
    unknown=targets-all_targets
    if unknown: raise ValueError("Unknown target(s): " + ", ".join(sorted(unknown)))
    preflight();a,b,c,live,metadata=load_data()
    if "FIG_A_ARCHITECTURE" in targets: architecture(args.overwrite)
    if "FIG_B_FROZEN_LSTM" in targets: model(metadata,args.overwrite)
    if "FIG_C_TELEMETRY_FLOW" in targets: telemetry_flow(args.overwrite)
    if "FIG_D_DIAGNOSIS_APPROVAL" in targets: workflow(args.overwrite)
    summary=detection(a,args.overwrite,emit="FIG_E1_DETECTION_COMPARISON" in targets) if {"FIG_E1_DETECTION_COMPARISON","FIG_E2_CONFUSION_MATRICES"}&targets else None
    if "FIG_E2_CONFUSION_MATRICES" in targets: confusion(summary,args.overwrite)
    if "FIG_E3_SCENARIO_RECALL" in targets: scenario(a,args.overwrite)
    if "FIG_E4_DIAGNOSIS_PILOT" in targets: diagnosis(b,args.overwrite)
    if "FIG_E5_SAFETY_HARNESS" in targets: safety(c,args.overwrite)
    if "FIG_E6_LIVE_EVIDENCE" in targets: live_summary(live,args.overwrite)
    if "FIG_F_EXPERIMENT_D_READINESS" in targets: readiness(args.overwrite)
    if not args.no_manifest: manifest()
    print(f"Generated {len(targets)} selected figure(s) in {OUT}; formats={','.join(FORMATS)}")


if __name__ == "__main__": main()
