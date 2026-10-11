#!/usr/bin/env python3
"""
JTBD Hypothesis Canvas PDF Generator
------------------------------------
Reads a YAML instance that conforms to jtbd_hypothesis_canvas.linkml.yaml
and renders it into the official visual layout (V3) defined by the JTBD Toolkit.

Usage:
    python generate_canvas_pdf.py <canvas.yaml> [-o output.pdf]

Dependencies: PyYAML, reportlab
"""

import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import simpleSplit

# ---------------------------------------------------------------------------
# Visual constants (matched to official V3 canvas)
# ---------------------------------------------------------------------------
BG         = HexColor("#F0F0F0")
WHITE      = white
BLACK      = HexColor("#111111")
DARK       = HexColor("#222222")
MED        = HexColor("#555555")
LIGHT_LINE = HexColor("#CCCCCC")
STAGE_GRAY = HexColor("#B0B0B0")


def wrap(c, text, font, size, max_width):
    if not text:
        return []
    return simpleSplit(str(text).strip(), font, size, max_width)


def clean(text):
    """Collapse whitespace for clean rendering."""
    if text is None:
        return ""
    return " ".join(str(text).split())


def load_canvas(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a mapping")
    return data


def render(canvas_data: dict, output_path: Path):
    c = pdfcanvas.Canvas(str(output_path), pagesize=letter)
    W, H = letter

    # Background
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    margin_x = 28
    canvas_left = margin_x + 18
    canvas_right = W - margin_x
    canvas_width = canvas_right - canvas_left

    # ----- Playing Field -----
    pf_w, pf_h = 130, 18
    pf_x = (W - pf_w) / 2
    pf_y = H - 36
    c.setFillColor(WHITE)
    c.setStrokeColor(LIGHT_LINE)
    c.setLineWidth(0.7)
    c.roundRect(pf_x, pf_y - pf_h, pf_w, pf_h, 2, fill=1, stroke=1)
    c.setFillColor(STAGE_GRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, pf_y - pf_h + 5, "Playing Field")

    pf_text = clean(canvas_data.get("playing_field", ""))
    c.setFillColor(DARK)
    c.setFont("Helvetica", 6.5)
    # Single line, truncated if needed
    if c.stringWidth(pf_text, "Helvetica", 6.5) > canvas_width - 20:
        while c.stringWidth(pf_text + "…", "Helvetica", 6.5) > canvas_width - 20 and len(pf_text) > 10:
            pf_text = pf_text[:-1]
        pf_text += "…"
    c.drawCentredString(W / 2, pf_y - pf_h - 11, pf_text)

    # ----- Vertical label -----
    c.saveState()
    c.setFillColor(DARK)
    c.translate(18, H / 2 + 30)
    c.rotate(90)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(0, 0, "JTBD CANVAS")
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(0, -10, "HYPOTHESIS")
    c.restoreState()

    top_of_main = pf_y - pf_h - 22
    left_col_w = 145
    right_col_w = 145
    center_w = canvas_width - left_col_w - right_col_w
    top_row_h = 105

    # ----- Job Performer -----
    jp_x = canvas_left
    jp_y = top_of_main - top_row_h
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.3)
    c.rect(jp_x, jp_y, left_col_w, top_row_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(jp_x + 6, top_of_main - 13, "Job Performer")

    jp_body = clean(canvas_data.get("job_performer", ""))
    lines = wrap(c, jp_body, "Helvetica", 6.5, left_col_w - 12)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(DARK)
    ty = top_of_main - 26
    for line in lines[:9]:
        c.drawString(jp_x + 6, ty, line)
        ty -= 8.5

    # ----- Related Jobs -----
    rj_x = canvas_left + left_col_w + center_w
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.3)
    c.rect(rj_x, jp_y, right_col_w, top_row_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(rj_x + 6, top_of_main - 13, "Related Jobs")

    related = canvas_data.get("related_jobs") or []
    c.setFont("Helvetica", 6.5)
    c.setFillColor(DARK)
    ty = top_of_main - 26
    for item in related[:7]:
        txt = "• " + clean(item)
        # truncate
        if c.stringWidth(txt, "Helvetica", 6.5) > right_col_w - 12:
            while c.stringWidth(txt + "…", "Helvetica", 6.5) > right_col_w - 12:
                txt = txt[:-1]
            txt += "…"
        c.drawString(rj_x + 6, ty, txt)
        ty -= 9.5

    # ----- Aspirations (center top) -----
    cen_x = canvas_left + left_col_w
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.3)
    c.rect(cen_x, jp_y, center_w, top_row_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(cen_x + center_w / 2, top_of_main - 13, "Aspirations")

    aspirations = canvas_data.get("aspirations") or []
    asp_text = " ".join(clean(a) for a in aspirations)
    lines = wrap(c, asp_text, "Helvetica", 6.5, center_w - 16)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(DARK)
    ty = top_of_main - 26
    for line in lines[:7]:
        c.drawString(cen_x + 8, ty, line)
        ty -= 8.5

    # ----- Focus Job Arch -----
    # Place the arch so its flat base sits on the bottom edge of the top row.
    # Content inside the arch must stay above that base → no overlap with Aspirations text.
    arch_cx = cen_x + center_w / 2
    arch_base_y = jp_y
    arch_radius = min(center_w / 2 - 6, 78)

    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(2.4)
    p = c.beginPath()
    p.moveTo(arch_cx - arch_radius, arch_base_y)
    p.arcTo(arch_cx - arch_radius, arch_base_y - arch_radius,
            arch_cx + arch_radius, arch_base_y + arch_radius, 0, 180)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(arch_cx, arch_base_y + 38, "Focus Job")

    focus = clean(canvas_data.get("focus_job", ""))
    # Break into up to 3 centered lines
    focus_lines = wrap(c, focus, "Helvetica-Bold", 7, arch_radius * 1.7)
    c.setFont("Helvetica-Bold", 7)
    fy = arch_base_y + 22
    for line in focus_lines[:3]:
        c.drawCentredString(arch_cx, fy, line)
        fy -= 9.5

    # ----- Job Steps -----
    js_top = arch_base_y
    js_h = 155
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.6)
    c.rect(canvas_left, js_top - js_h, canvas_width, js_h, fill=1, stroke=1)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(canvas_left + 6, js_top - 13, "Job Steps")

    # Stages
    steps_data = canvas_data.get("job_steps") or {}
    if isinstance(steps_data, dict):
        stages = steps_data.get("stages") or ["PLAN", "PREPARE", "EXECUTE", "MONITOR", "MODIFY", "CONCLUDE"]
    else:
        stages = ["PLAN", "PREPARE", "EXECUTE", "MONITOR", "MODIFY", "CONCLUDE"]
    stage_area_w = canvas_width - 70
    sw = stage_area_w / max(len(stages), 1)
    c.setFont("Helvetica", 6)
    c.setFillColor(STAGE_GRAY)
    for i, s in enumerate(stages):
        c.drawCentredString(canvas_left + 55 + i * sw + sw / 2, js_top - 13, str(s).upper())

    # Step content
    c.setFillColor(DARK)
    y = js_top - 28
    if isinstance(steps_data, dict):
        for label, key in [("Beginning:", "beginning"), ("Middle:", "middle"), ("End:", "end")]:
            body = clean(steps_data.get(key, ""))
            if not body:
                continue
            c.setFont("Helvetica-Bold", 6.5)
            c.drawString(canvas_left + 6, y, label)
            body_lines = wrap(c, body, "Helvetica", 6.3, canvas_width - 14)
            c.setFont("Helvetica", 6.3)
            y -= 9
            for line in body_lines:
                if y < js_top - js_h + 8:
                    break
                c.drawString(canvas_left + 6, y, line)
                y -= 8.2
            y -= 4
    else:
        notes = clean(steps_data)
        for line in wrap(c, notes, "Helvetica", 6.3, canvas_width - 14):
            c.drawString(canvas_left + 6, y, line)
            y -= 8.2

    # ----- Success Criteria -----
    sc_top = js_top - js_h
    sc_h = 118
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.6)
    c.rect(canvas_left, sc_top - sc_h, canvas_width, sc_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(canvas_left + 6, sc_top - 13, "Success Criteria")

    sc_list = canvas_data.get("success_criteria") or []
    c.setFont("Helvetica", 6.4)
    c.setFillColor(DARK)
    y = sc_top - 26
    for item in sc_list[:9]:
        txt = "• " + clean(item)
        c.drawString(canvas_left + 6, y, txt[:110])
        y -= 9.5

    # ----- Emotions | Circumstances -----
    bot_top = sc_top - sc_h
    bot_h = 115
    half = canvas_width / 2

    # Emotions
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.6)
    c.rect(canvas_left, bot_top - bot_h, half, bot_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(canvas_left + 6, bot_top - 13, "Emotions")

    emo_list = canvas_data.get("emotions") or []
    c.setFont("Helvetica", 6.4)
    c.setFillColor(DARK)
    y = bot_top - 26
    for item in emo_list[:7]:
        c.drawString(canvas_left + 6, y, "• " + clean(item)[:55])
        y -= 10

    # Circumstances
    c.setFillColor(WHITE)
    c.setStrokeColor(BLACK)
    c.rect(canvas_left + half, bot_top - bot_h, half, bot_h, fill=1, stroke=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(canvas_left + half + 6, bot_top - 13, "Circumstances")

    circ_list = canvas_data.get("circumstances") or []
    c.setFont("Helvetica", 6.2)
    c.setFillColor(DARK)
    y = bot_top - 26
    for item in circ_list[:8]:
        c.drawString(canvas_left + half + 6, y, "• " + clean(item)[:55])
        y -= 9.5

    # ----- Footer -----
    meta = canvas_data.get("meta") or {}
    c.setFont("Helvetica", 6)
    c.setFillColor(MED)
    c.drawString(canvas_left, 18, "V3")
    c.drawCentredString(W / 2, 18, "DETAILS: jtbd.tk/canvas")
    title = meta.get("title") or "JTBD Hypothesis Canvas"
    c.drawRightString(canvas_right, 18, f"{title}  |  CC BY-NC-ND 4.0")

    c.save()
    print(f"Generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate official-layout JTBD Hypothesis Canvas PDF from YAML")
    parser.add_argument("yaml_file", type=Path, help="Path to canvas YAML instance")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output PDF path")
    args = parser.parse_args()

    if not args.yaml_file.exists():
        sys.exit(f"File not found: {args.yaml_file}")

    data = load_canvas(args.yaml_file)

    out = args.output
    if out is None:
        out = args.yaml_file.with_suffix(".pdf")
    render(data, out)


if __name__ == "__main__":
    main()
