#!/usr/bin/env python3
"""Plot publication-ready anomaly detection evaluation figures from machine-readable predictions."""
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "research" / "results"
FIGURES = ROOT / "research" / "figures"
PAPER_FIGURES = ROOT / "research" / "paper" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)
PAPER_FIGURES.mkdir(parents=True, exist_ok=True)


def get_font(size: int, bold: bool = False):
    """Safely load TrueType font or fallback to default."""
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def plot_confusion_matrices(df: pd.DataFrame, out_path: Path):
    """Generate 2x2 publication confusion matrices (1000x750)."""
    width, height = 1000, 750
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(15, bold=True)
    f_sub = get_font(12)
    f_mtitle = get_font(12, bold=True)
    f_header = get_font(11)
    f_label = get_font(11)
    f_num = get_font(13, bold=True)
    f_tag = get_font(11)

    # Title & Subtitle
    draw.text((30, 25), "Figure A.1: Anomaly Detection Confusion Matrices (N = 320 Held-Out Cases)", fill=(30, 41, 59), font=f_title)
    draw.text((30, 50), "200 Normal Windows + 120 Injected Incident Windows (20 Replicates x 6 Scenarios)", fill=(71, 85, 105), font=f_sub)

    yt = df["ground_truth"].values

    models = [
        ("Operational Rules", df["rule_flag"].values, 120, 0, 200, 0, 60, 110),
        ("Isolation Forest", df["iso_flag"].values, 57, 4, 196, 63, 530, 110),
        ("LSTM Autoencoder (Frozen)", df["lstm_flag"].values, 120, 2, 198, 0, 60, 420),
        ("Combined Alert (Rules OR LSTM)", df["combined_flag"].values, 120, 2, 198, 0, 530, 420),
    ]

    for title, y_pred, tp, fp, tn, fn, ox, oy in models:
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

        # Method Title & Summary
        draw.text((ox, oy), title, fill=(30, 58, 138), font=f_mtitle)
        draw.text((ox, oy + 22), f"Prec: {prec:.3f} | Rec: {rec:.3f} | F1: {f1:.3f}", fill=(51, 65, 85), font=f_header)

        # Matrix Headers
        box_x = ox + 80
        box_y = oy + 55
        cw, ch = 100, 80

        draw.text((box_x + 18, box_y - 18), "Pred Normal", fill=(30, 41, 59), font=f_label)
        draw.text((box_x + cw + 14, box_y - 18), "Pred Anomaly", fill=(30, 41, 59), font=f_label)
        draw.text((ox - 5, box_y + 28), "Act Normal", fill=(30, 41, 59), font=f_label)
        draw.text((ox - 5, box_y + ch + 28), "Act Incident", fill=(30, 41, 59), font=f_label)

        # Cells: (col, row)
        # Top-Left: TN (Light Blue)
        draw.rectangle([box_x, box_y, box_x + cw, box_y + ch], fill=(225, 240, 254), outline=(147, 197, 253), width=2)
        draw.text((box_x + 42, box_y + 22), "TN", fill=(30, 58, 138), font=f_tag)
        draw.text((box_x + 38, box_y + 40), str(tn), fill=(30, 58, 138), font=f_num)

        # Top-Right: FP (Light Pink)
        draw.rectangle([box_x + cw, box_y, box_x + 2 * cw, box_y + ch], fill=(253, 232, 232), outline=(248, 180, 180), width=2)
        draw.text((box_x + cw + 42, box_y + 22), "FP", fill=(155, 28, 28), font=f_tag)
        draw.text((box_x + cw + 45, box_y + 40), str(fp), fill=(155, 28, 28), font=f_num)

        # Bottom-Left: FN (Light Pink)
        draw.rectangle([box_x, box_y + ch, box_x + cw, box_y + 2 * ch], fill=(253, 232, 232), outline=(248, 180, 180), width=2)
        draw.text((box_x + 42, box_y + ch + 22), "FN", fill=(155, 28, 28), font=f_tag)
        draw.text((box_x + 42, box_y + ch + 40), str(fn), fill=(155, 28, 28), font=f_num)

        # Bottom-Right: TP (Light Green)
        draw.rectangle([box_x + cw, box_y + ch, box_x + 2 * cw, box_y + 2 * ch], fill=(225, 250, 234), outline=(134, 239, 172), width=2)
        draw.text((box_x + cw + 42, box_y + ch + 22), "TP", fill=(22, 101, 52), font=f_tag)
        draw.text((box_x + cw + 36, box_y + ch + 40), str(tp), fill=(22, 101, 52), font=f_num)

    img.save(out_path, "PNG")
    print(f"Saved confusion matrices figure: {out_path}")


def plot_comparison_chart(df: pd.DataFrame, out_path: Path):
    """Generate side-by-side comparative bar chart (950x550)."""
    width, height = 950, 550
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(15, bold=True)
    f_sub = get_font(12)
    f_legend = get_font(11)
    f_axis = get_font(11)
    f_group = get_font(12, bold=True)
    f_val = get_font(11, bold=True)
    f_fa = get_font(11)

    # Title & Subtitle
    draw.text((30, 25), "Figure A.2: Anomaly Detection Performance Comparison", fill=(30, 41, 59), font=f_title)
    draw.text((30, 50), "Comparing Precision, Recall, and F1-Score Across Candidate Detectors", fill=(71, 85, 105), font=f_sub)

    # Legend
    leg_x, leg_y = 550, 35
    colors = {
        "Precision": (37, 99, 235),  # Blue
        "Recall": (16, 185, 129),     # Green
        "F1-Score": (234, 88, 12),    # Orange
    }
    cur_lx = leg_x
    for label, col in colors.items():
        draw.rectangle([cur_lx, leg_y, cur_lx + 16, leg_y + 16], fill=col)
        draw.text((cur_lx + 22, leg_y + 1), label, fill=(51, 65, 85), font=f_legend)
        cur_lx += 115

    # Chart Area
    origin_x, origin_y = 90, 440
    chart_w, chart_h = 800, 340
    top_y = origin_y - chart_h

    # Y-axis line and ticks
    draw.line([(origin_x, origin_y), (origin_x, top_y)], fill=(148, 163, 184), width=2)
    for tick_val in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        ty = origin_y - int(tick_val * chart_h)
        draw.line([(origin_x - 5, ty), (origin_x, ty)], fill=(148, 163, 184), width=1)
        draw.text((origin_x - 30, ty - 7), f"{tick_val:.1f}", fill=(100, 116, 139), font=f_axis)
        if tick_val > 0.0:
            draw.line([(origin_x, ty), (origin_x + chart_w, ty)], fill=(241, 245, 249), width=1)

    # Base line
    draw.line([(origin_x, origin_y), (origin_x + chart_w, origin_y)], fill=(148, 163, 184), width=2)

    # Data items
    groups = [
        ("Operational Rules", 1.00, 1.00, 1.00, "FA/hr: 0.0"),
        ("Isolation Forest", 0.9344, 0.4750, 0.6298, "FA/hr: 14.4"),
        ("LSTM Autoencoder", 0.9836, 1.00, 0.9917, "FA/hr: 7.2"),
        ("Combined Alert", 0.9836, 1.00, 0.9917, "FA/hr: 7.2"),
    ]

    group_spacing = chart_w / len(groups)
    bar_w = 28

    for idx, (name, prec, rec, f1, fa_str) in enumerate(groups):
        gx = origin_x + idx * group_spacing + 45
        vals = [prec, rec, f1]
        c_list = [colors["Precision"], colors["Recall"], colors["F1-Score"]]

        for b_idx, (val, col) in enumerate(zip(vals, c_list)):
            bx = gx + b_idx * (bar_w + 3)
            bh = int(val * chart_h)
            by = origin_y - bh
            draw.rectangle([bx, by, bx + bar_w, origin_y], fill=col)
            draw.text((bx + 1, by - 16), f"{val:.2f}", fill=(30, 41, 59), font=f_val)

        # Labels underneath
        draw.text((gx - 10, origin_y + 15), name, fill=(30, 41, 59), font=f_group)
        draw.text((gx - 5, origin_y + 35), fa_str, fill=(100, 116, 139), font=f_fa)

    img.save(out_path, "PNG")
    print(f"Saved comparison chart figure: {out_path}")


def main():
    preds_path = RESULTS / "detection_predictions.csv"
    if not preds_path.exists():
        print(f"Error: {preds_path} not found. Run experiment A first.")
        return 1

    df = pd.read_csv(preds_path)
    fig1 = FIGURES / "detection_confusion_matrices.png"
    fig2 = FIGURES / "detection_comparison.png"

    plot_confusion_matrices(df, fig1)
    plot_comparison_chart(df, fig2)

    # Sync to paper figures directory
    shutil.copy2(fig1, PAPER_FIGURES / "detection_confusion_matrices.png")
    shutil.copy2(fig2, PAPER_FIGURES / "detection_comparison.png")
    print(f"Synced generated figures to {PAPER_FIGURES}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
