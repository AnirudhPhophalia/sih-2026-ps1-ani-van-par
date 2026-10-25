"""
AICTE FDR Portal - 7 Innovative Technical Pipelines (Professional Enterprise Edition)
Pure Professional English • Zero Hindi/Hinglish • Clean Architectural Impact (No Pitch Quotes)
Directly generated from: docs/05_INNOVATIVE_IDEAS_BRAINSTORMING.md
Contains:
1. Legacy Physical Records Digitization & Historical Data Ingestion Engine
2. Hierarchical Multi-Model Ensemble OCR with Intelligent Routing
3. AI Document Forensics & Tamper Detection Engine (ELA + EXIF + Kerning)
4. Military-Grade Cryptographic Ledger & Defense-in-Depth (Merkle Hash Chaining)
5. Tri-Modal Universal Bank Verification Gateway (CBS API + 2FA Magic Token + NeSL)
6. Autonomous Maturity Escalation & Anti-Lapse SLA Engine
7. Cross-Government DPI Entity Intelligence Engine (NITI NGO Darpan + MCA21 + PAN)

Format: 100% Native Vector PowerPoint Shapes & Fully Editable Text Frames
Output: presentation/decks/AICTE_Innovative_Ideas_Diagrams_Editable.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE (Clean, Modern, Approachable)
# ==============================================================================
CANVAS_BG       = RGBColor(0xFA, 0xFB, 0xFC)
WHITE           = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT       = RGBColor(0x0F, 0x17, 0x2A) # Slate 900
BODY_TEXT       = RGBColor(0x33, 0x41, 0x55) # Slate 700
MUTED_TEXT      = RGBColor(0x64, 0x74, 0x8B) # Slate 500
BORDER_LIGHT    = RGBColor(0xE2, 0xE8, 0xF0) # Slate 200

# Theme Accents
SKY_BG          = RGBColor(0xF0, 0xF9, 0xFF)
SKY_BORDER      = RGBColor(0xBA, 0xE6, 0xFD)
SKY_ACCENT      = RGBColor(0x02, 0x84, 0xC7)

LILAC_BG        = RGBColor(0xEE, 0xF2, 0xFF)
LILAC_BORDER    = RGBColor(0xC7, 0xD2, 0xFE)
LILAC_ACCENT    = RGBColor(0x4F, 0x46, 0xE5)

MINT_BG         = RGBColor(0xEC, 0xFD, 0xF5)
MINT_BORDER     = RGBColor(0xA7, 0xF3, 0xD0)
MINT_ACCENT     = RGBColor(0x05, 0x96, 0x69)

PEACH_BG        = RGBColor(0xFF, 0xF1, 0xF2)
PEACH_BORDER    = RGBColor(0xFE, 0xCD, 0xD3)
PEACH_ACCENT    = RGBColor(0xE1, 0x1D, 0x48)

AMBER_BG        = RGBColor(0xFF, 0xFB, 0xEB)
AMBER_BORDER    = RGBColor(0xFD, 0xE6, 0x8A)
AMBER_ACCENT    = RGBColor(0xD9, 0x77, 0x06)

PURPLE_BG       = RGBColor(0xFA, 0xF5, 0xFF)
PURPLE_BORDER   = RGBColor(0xE9, 0xD5, 0xFF)
PURPLE_ACCENT   = RGBColor(0x7E, 0x22, 0xCE)

DARK_FOOTER     = RGBColor(0x0F, 0x17, 0x2A)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

def new_deck():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs

def create_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = CANVAS_BG
    return slide

def add_slide_header(slide, super_title, title_text):
    tb_sup = slide.shapes.add_textbox(Inches(0.7), Inches(0.22), Inches(11.9), Inches(0.24))
    tf_sup = tb_sup.text_frame
    p_sup = tf_sup.paragraphs[0]
    r_sup = p_sup.add_run()
    r_sup.text = super_title.upper()
    r_sup.font.name = "Calibri"
    r_sup.font.size = Pt(9)
    r_sup.font.bold = True
    r_sup.font.color.rgb = LILAC_ACCENT

    tb_t = slide.shapes.add_textbox(Inches(0.7), Inches(0.44), Inches(11.9), Inches(0.48))
    tf_t = tb_t.text_frame
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title_text
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(20)
    r_t.font.bold = True
    r_t.font.color.rgb = DARK_TEXT

def add_mvp_strip(slide, problem_text, solution_text):
    strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(0.95), Inches(11.933), Inches(0.82))
    strip.fill.solid()
    strip.fill.fore_color.rgb = WHITE
    strip.line.color.rgb = BORDER_LIGHT
    strip.line.width = Pt(1.2)
    strip.adjustments[0] = 0.04

    # Problem Side (Left)
    tb_p = slide.shapes.add_textbox(Inches(0.85), Inches(0.98), Inches(5.2), Inches(0.74))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_p1 = tf_p.paragraphs[0]
    r_p1 = p_p1.add_run()
    r_p1.text = "CORE OPERATIONAL CHALLENGE:"
    r_p1.font.name = "Calibri"
    r_p1.font.size = Pt(7.5)
    r_p1.font.bold = True
    r_p1.font.color.rgb = PEACH_ACCENT

    p_p2 = tf_p.add_paragraph()
    p_p2.space_before = Pt(1)
    r_p2 = p_p2.add_run()
    r_p2.text = problem_text
    r_p2.font.name = "Calibri"
    r_p2.font.size = Pt(8.5)
    r_p2.font.color.rgb = BODY_TEXT

    # Vertical Divider Line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.25), Inches(1.05), Pt(1), Inches(0.62))
    div.fill.solid()
    div.fill.fore_color.rgb = BORDER_LIGHT
    div.line.fill.background()

    # Solution / MVP Side (Right)
    tb_s = slide.shapes.add_textbox(Inches(6.45), Inches(0.98), Inches(6.0), Inches(0.74))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    p_s1 = tf_s.paragraphs[0]
    r_s1 = p_s1.add_run()
    r_s1.text = "ENGINEERED ARCHITECTURE & MVP PIPELINE:"
    r_s1.font.name = "Calibri"
    r_s1.font.size = Pt(7.5)
    r_s1.font.bold = True
    r_s1.font.color.rgb = MINT_ACCENT

    p_s2 = tf_s.add_paragraph()
    p_s2.space_before = Pt(1)
    r_s2 = p_s2.add_run()
    r_s2.text = solution_text
    r_s2.font.name = "Calibri"
    r_s2.font.size = Pt(8.5)
    r_s2.font.color.rgb = BODY_TEXT

def draw_pillar(slide, left, top, width, height, title, subtitle, icon, bg_color, border_color, accent_color):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = bg_color
    box.line.color.rgb = border_color
    box.line.width = Pt(1.6)
    box.adjustments[0] = 0.05

    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.15), top + Inches(0.12), Inches(0.4), Inches(0.4))
    circ.fill.solid()
    circ.fill.fore_color.rgb = WHITE
    circ.line.color.rgb = border_color
    circ.line.width = Pt(1)
    tf_c = circ.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.alignment = PP_ALIGN.CENTER
    r_c = p_c.add_run()
    r_c.text = icon
    r_c.font.size = Pt(12)

    tb = slide.shapes.add_textbox(left + Inches(0.62), top + Inches(0.12), width - Inches(0.75), Inches(0.42))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = title.upper()
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    r1.font.color.rgb = DARK_TEXT

    p2 = tf.add_paragraph()
    p2.space_before = Pt(1)
    r2 = p2.add_run()
    r2.text = subtitle
    r2.font.name = "Calibri"
    r2.font.size = Pt(7.5)
    r2.font.color.rgb = MUTED_TEXT

    return box

def draw_sub_card(slide, left, top, width, height, title, desc_parts, pill_tag=None, pill_color=None, pill_bg=None, border_color=BORDER_LIGHT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    card.adjustments[0] = 0.06

    tb = slide.shapes.add_textbox(left + Inches(0.08), top + Inches(0.06), width - Inches(0.16), height - Inches(0.12))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r_t = p.add_run()
    r_t.text = title
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(9)
    r_t.font.bold = True
    r_t.font.color.rgb = DARK_TEXT

    if pill_tag:
        pill_w = Inches(0.95)
        pill_h = Inches(0.18)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + width - pill_w - Inches(0.06), top + Inches(0.06), pill_w, pill_h)
        pill.fill.solid()
        pill.fill.fore_color.rgb = pill_bg if pill_bg else LILAC_BG
        pill.line.fill.background()
        pill.adjustments[0] = 0.3
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        r_p = p_p.add_run()
        r_p.text = pill_tag.upper()
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(6)
        r_p.font.bold = True
        r_p.font.color.rgb = pill_color if pill_color else LILAC_ACCENT

    p_d = tf.add_paragraph()
    p_d.space_before = Pt(2)
    for part, is_bold in desc_parts:
        r_d = p_d.add_run()
        r_d.text = part
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(8)
        r_d.font.bold = is_bold
        r_d.font.color.rgb = DARK_TEXT if is_bold else BODY_TEXT

def draw_arrow(slide, left, center_y, color):
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, center_y - Inches(0.1), Inches(0.24), Inches(0.2))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = color
    arrow.line.fill.background()

def add_impact_bar(slide, impact_title, impact_text, stack_chips):
    bar_y = Inches(6.05)
    bar_h = Inches(1.15)
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), bar_y, Inches(11.933), bar_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_FOOTER
    bar.line.fill.background()
    bar.adjustments[0] = 0.06

    tb_q = slide.shapes.add_textbox(Inches(0.9), bar_y + Inches(0.1), Inches(7.5), Inches(0.95))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    p1 = tf_q.paragraphs[0]
    r1 = p1.add_run()
    r1.text = impact_title.upper()
    r1.font.name = "Calibri"
    r1.font.size = Pt(8)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    p2 = tf_q.add_paragraph()
    p2.space_before = Pt(2)
    r2 = p2.add_run()
    r2.text = impact_text
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = WHITE

    tb_s = slide.shapes.add_textbox(Inches(8.6), bar_y + Inches(0.1), Inches(3.8), Inches(0.25))
    tf_s = tb_s.text_frame
    p_s = tf_s.paragraphs[0]
    r_s = p_s.add_run()
    r_s.text = "PRODUCTION TECH STACK:"
    r_s.font.name = "Calibri"
    r_s.font.size = Pt(7.5)
    r_s.font.bold = True
    r_s.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    chip_x = Inches(8.6)
    chip_y = bar_y + Inches(0.4)
    for i, chip_name in enumerate(stack_chips):
        row = i // 2
        col = i % 2
        c_x = chip_x + col * Inches(1.85)
        c_y = chip_y + row * Inches(0.32)
        c_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, Inches(1.75), Inches(0.28))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        c_box.line.color.rgb = RGBColor(0x33, 0x41, 0x55)
        c_box.line.width = Pt(1)
        c_box.adjustments[0] = 0.2
        c_tf = c_box.text_frame
        c_p = c_tf.paragraphs[0]
        c_p.alignment = PP_ALIGN.CENTER
        c_r = c_p.add_run()
        c_r.text = chip_name
        c_r.font.name = "Calibri"
        c_r.font.size = Pt(7.5)
        c_r.font.bold = True
        c_r.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)


# ==============================================================================
# 1. LEGACY PHYSICAL RECORDS DIGITIZATION ENGINE
# ==============================================================================
def build_slide_1(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Legacy Modernization & Backlog Resolution",
                     "Legacy Physical Records Digitization & Historical Data Ingestion Engine")
    add_mvp_strip(slide,
                  "Over 50,000 legacy physical FDR files and letters are archived across 10 Regional Offices. Retrieving a single legacy deposit record manually takes up to 60 days.",
                  "High-throughput batch scanner, OpenCV contrast restoration, LayoutLMv3 table extraction, and RapidFuzz PID entity linkage with a split-screen 10-second review desk.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Batch Ingestion", "Image Normalization", "🗄️", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(0.95),
                  "High-Speed Batch Scanner", [("Ingests multi-page batch PDF/TIFF files of ", False), ("aged physical FDR receipts and correspondence", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(1.72), Inches(3.0), Inches(0.95),
                  "OpenCV CLAHE & Deskew", [("Adaptive histogram equalization and Otsu thresholding ", False), ("restores faded dot-matrix print and corrects skew", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.79), Inches(3.0), Inches(0.95),
                  "Stamp & Seal Anchoring", [("Automated region-of-interest cropping using ", False), ("AICTE regional inward stamps and bank seals", True), (" as geometric anchors.", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. AI Extraction & Entity Link", "RapidFuzz & Layout Parser", "⚡", PURPLE_BG, PURPLE_BORDER, PURPLE_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(1.4),
                  "LayoutLMv3 Spatial Table Parser",
                  [("Converts complex unstructured paper layouts into verified JSON data: ", False), ("FDR Number, Principal Amount, Bank Branch, and Maturity Date", True), (". Disambiguates irregular column baselines.", False)],
                  pill_tag="JSON Engine", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.15), Inches(4.3), Inches(1.55),
                  "RapidFuzz Levenshtein PID Linker",
                  [("Resolves historical institutional naming variations (e.g., ", False), ("'St. Xavier Engg' vs 'St. Xavier's College of Engineering'", True),
                   (") and maps records automatically to the ", False), ("AICTE Master Permanent Institute ID (PID)", True), (".", False)],
                  pill_tag="PID Matcher", pill_color=SKY_ACCENT, pill_bg=SKY_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), PURPLE_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Dual-Queue Output", "Verification & Seeding", "✅", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(1.4),
                  "Match Score >= 95%",
                  [("Directly committed into the PostgreSQL active FDR ledger. ", False), ("Physical records are certified and cleared for permanent archival or destruction", True), (".", False)],
                  pill_tag="Auto-Seed", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.15), Inches(2.83), Inches(1.55),
                  "Match Score < 95%",
                  [("Routed to split-screen Fast-Tagger UI: Scanned document on left, pre-populated AI fields on right. Scrutiny officers verify within ", False), ("10 seconds using keyboard shortcuts", True), (".", False)],
                  pill_tag="Fast Tagger", pill_color=AMBER_ACCENT, pill_bg=AMBER_BG, border_color=AMBER_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Eliminates 30 years of paper backlog across 10 Regional Offices. Converts physical archives into an instantly searchable, tamper-evident digital master database with over 90% manual effort reduction.",
                   ["OpenCV CLAHE", "PaddleOCR v4", "RapidFuzz C++", "PostgreSQL 16"])


# ==============================================================================
# 2. HIERARCHICAL MULTI-MODEL ENSEMBLE OCR
# ==============================================================================
def build_slide_2(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Computer Vision & Document Intelligence",
                     "Hierarchical Multi-Model Ensemble OCR with Intelligent Routing")
    add_mvp_strip(slide,
                  "Single rigid OCR engines fail on faded dot-matrix print, physical rubber stamps, and handwritten cursive branch manager endorsements.",
                  "Dynamic Neural Routing: Ingested scans are evaluated for image quality and routed across PaddleOCR (<300ms), LayoutLMv3 table segmentation, and Microsoft TrOCR handwriting extraction.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Pre-Flight Triage", "Quality Classification", "🔍", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(1.4),
                  "Laplacian Blur Evaluator",
                  [("Measures edge sharpness via ", False), ("cv2.Laplacian() variance", True), (". Scans below threshold undergo unsharp masking and binarization prior to optical recognition.", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.15), Inches(3.0), Inches(1.55),
                  "Geometry & Layout Classifier",
                  [("Automatically classifies incoming documents into: ", False), ("Standard Machine-Printed, Multi-Column Tabular Matrix, or Cursive Handwritten Endorsement", True), (".", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Multi-Model Routes", "Specialized Neural Engines", "🧠", AMBER_BG, AMBER_BORDER, AMBER_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "Route A: PaddleOCR PP-OCRv4",
                  [("Sub-300ms high-throughput inference", True), (" delivering 98.4% precision on numerical fields, FDR numbers, and IFSC codes.", False)],
                  pill_tag="High Speed", pill_color=MINT_ACCENT, pill_bg=MINT_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Route B: LayoutLMv3 Multi-Modal",
                  [("Integrates visual layout coordinates with linguistic tokens to ", False), ("disambiguate Principal vs Maturity columns", True), (" in complex banking deposit certificates.", False)],
                  pill_tag="Table Parser", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Route C: Microsoft TrOCR",
                  [("Transformer-based sequence recognition trained on ", False), ("cursive handwriting, branch manager lien endorsements, and rubber stamps", True), (".", False)],
                  pill_tag="Handwriting", pill_color=AMBER_ACCENT, pill_bg=AMBER_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), AMBER_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Ensemble Consensus", "Confidence Evaluation", "🗳️", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(1.4),
                  "Confidence Score >= 0.88",
                  [("Cross-model voting confirmation. ", False), ("Automatically populates database fields", True), (" and advances deposit instrument to bank telemetry validation without clerk overhead.", False)],
                  pill_tag="Auto-Pass", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.15), Inches(2.83), Inches(1.55),
                  "Confidence Score < 0.88",
                  [("Triggers side-by-side visual diff highlighting discrepancies in amber for ", False), ("one-click confirmation by Regional Scrutiny Officers", True), (".", False)],
                  pill_tag="Diff Review", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG, border_color=PEACH_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Replaces rigid single-engine OCR with an adaptive multi-model neural pipeline, elevating optical extraction accuracy from 74% to 99.2% across diverse banking receipts nationwide.",
                   ["PaddleOCR PP-OCRv4", "LayoutLMv3", "Microsoft TrOCR", "FastAPI"])


# ==============================================================================
# 3. AI DOCUMENT FORENSICS & ANTI-TAMPER ENGINE
# ==============================================================================
def build_slide_3(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Security & Anti-Fraud Inspection",
                     "AI Document Forensics & Tamper Detection Engine")
    add_mvp_strip(slide,
                  "Digital image manipulation tools enable fraudulent alteration of deposit amounts from 5 Lakhs to 50 Lakhs, which is undetectable to the human eye on scanned copies.",
                  "Zero-Trust Image Forensics: Error Level Analysis (ELA) isolates compression variance in modified JPEG pixels, combined with EXIF software provenance and font kerning analysis.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Ingestion & Sandbox", "Zero-Trust Perimeter", "🔒", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(1.4),
                  "MinIO S3 Vault Storage",
                  [("Uploaded deposit certificates are stored under ", False), ("server-side AES-256 encryption", True), (" with immediate SHA-256 cryptographic hash pinning.", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.15), Inches(3.0), Inches(1.55),
                  "Raw Signal Decomposition",
                  [("Decompresses raster data into an ", False), ("uncompressed RGB pixel matrix", True), (" to prevent re-compression artifacts from masking tampering.", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Tri-Vector Inspection", "Forensic Probe Pipelines", "🔬", PEACH_BG, PEACH_BORDER, PEACH_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "Probe 1: Error Level Analysis (ELA)",
                  [("Resaves file at fixed 95% JPEG quality. ", False), ("Digitally manipulated pixels exhibit pronounced error intensity deltas", True), (" against unchanged scan areas.", False)],
                  pill_tag="JPEG Splicing", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Probe 2: EXIF & Software Signatures",
                  [("Extracts metadata headers to detect signatures of ", False), ("Adobe Photoshop, Canva, GIMP, iLovePDF", True), (", or scrubbed scanner hardware tags.", False)],
                  pill_tag="Provenance", pill_color=AMBER_ACCENT, pill_bg=AMBER_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Probe 3: Font & Kerning Jitter",
                  [("Examines baseline collinearity across digits. ", False), ("Detects resolution mismatches, character blurring, and font over-typing", True), (".", False)],
                  pill_tag="Pixel Geometry", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), PEACH_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Policy Enforcer", "Automated Triage Gate", "⚖️", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(0.95),
                  "Score 0 - 30 : Clean Scan",
                  [("Authentic provenance confirmed. ", False), ("Auto-cleared", True), (" for Bank Verification Gateway.", False)],
                  pill_tag="Clean", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(1.72), Inches(2.83), Inches(0.95),
                  "Score 31 - 70 : Suspicious",
                  [("Moderate anomaly detected. Escalated to ", False), ("Forensic Scrutiny Queue", True), (" with ELA difference overlay.", False)],
                  pill_tag="Suspicious", pill_color=AMBER_ACCENT, pill_bg=AMBER_BG, border_color=AMBER_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.79), Inches(2.83), Inches(0.95),
                  "Score 71 - 100 : Fraud Alert",
                  [("Tampering verified. ", False), ("File frozen, hash blacklisted, and notification dispatched to Chief Vigilance Officer", True), (".", False)],
                  pill_tag="Fraud Block", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG, border_color=PEACH_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Prevents multi-crore financial collateral fraud by programmatically identifying synthetic, photoshopped, or digitally altered deposit receipts within 2 seconds of ingestion.",
                   ["Pillow & NumPy", "PyPDF2 / ExifRead", "MinIO S3", "OpenCV CLAHE"])


# ==============================================================================
# 4. MILITARY-GRADE CRYPTOGRAPHIC LEDGER
# ==============================================================================
def build_slide_4(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Cryptography & Immutable Governance",
                     "Military-Grade Cryptographic Ledger & Defense-in-Depth Security")
    add_mvp_strip(slide,
                  "Internal data manipulation risks: Rogue database administrators or compromised credentials could illicitly update deposit statuses to 'RELEASED' or alter monetary balances.",
                  "Merkle Hash Chaining: Each lifecycle event is cryptographically sealed using HMAC-SHA256. A 60-second sentinel daemon breaks instantly upon direct SQL manipulation.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Zero-Trust Ingress", "Perimeter Access Controls", "🛡️", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(0.95),
                  "Row-Level Security (RLS)", [("Enforces granular database partitioning: Regional Officers are strictly isolated to ", False), ("their assigned geographic jurisdiction", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(1.72), Inches(3.0), Inches(0.95),
                  "Four-Eyes Maker-Checker", [("Enforces dual-authorization: The officer submitting a deposit release request ", False), ("cannot approve or authorize the release", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.79), Inches(3.0), Inches(0.95),
                  "AES-256-GCM Field Vault", [("Sensitive fields (Account Numbers, IFSC, PAN) are ", False), ("encrypted at rest using hardware master HSM keys", True), (".", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Merkle Hash Chaining", "State Mutation Blocks", "⛓️", PURPLE_BG, PURPLE_BORDER, PURPLE_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "Block #1: Genesis State",
                  [("Hash_1 = SHA256(Payload + Seed_0). ", True), ("Permanently anchors institutional PID, deposit amount, IFSC, and intake timestamp.", False)],
                  pill_tag="Genesis Block", pill_color=SKY_ACCENT, pill_bg=SKY_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Block #2: Bank Lien Confirmed",
                  [("Hash_2 = HMAC(BankData + Hash_1, Key). ", True), ("Binds bank transaction tokens directly to Block #1.", False)],
                  pill_tag="Mutation Block", pill_color=MINT_ACCENT, pill_bg=MINT_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Block #3: Bureau Release NOC",
                  [("Hash_3 = HMAC(AadhaarSign + Hash_2, Key). ", True), ("Cryptographically locks final statutory discharge.", False)],
                  pill_tag="Release Block", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), PURPLE_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Verified NOC Output", "Statutory Certification", "📜", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(1.4),
                  "Aadhaar XML e-Sign",
                  [("Discharge certificates executed under ", False), ("Section 5 of the Information Technology Act, 2000", True), (", conferring full statutory validity across Indian courts.", False)],
                  pill_tag="IT Act Valid", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.15), Inches(2.83), Inches(1.55),
                  "Encrypted QR Verification",
                  [("Embeds an AICTE private-key signed token. ", False), ("Bank branch managers verify document authenticity via smartphone scan in 2 seconds", True), (".", False)],
                  pill_tag="Instant Verify", pill_color=SKY_ACCENT, pill_bg=SKY_BG, border_color=SKY_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Guarantees non-repudiation and insider threat immunity. Direct database modification breaks the cryptographic hash chain immediately, generating a critical security alert.",
                   ["HMAC-SHA256", "AES-256-GCM", "PostgreSQL RLS", "Aadhaar e-Sign"])


# ==============================================================================
# 5. TRI-MODAL BANK GATEWAY
# ==============================================================================
def build_slide_5(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Banking Telemetry & Interoperability",
                     "Tri-Modal Universal Bank Verification Gateway")
    add_mvp_strip(slide,
                  "Lack of standardized API infrastructure across 43 Regional Rural Banks and 1,500+ Urban Co-operative Banks creates a nationwide verification barrier.",
                  "A 3-Tier Adaptive Gateway: Integrates Core Banking System (CBS) APIs for Tier-1 banks, secure two-factor authenticated digital tokens for rural branches, and NeSL for statutory e-BG records.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Request Triage", "Capability Classifier", "🏛️", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(1.4),
                  "FDR Instrument Declaration",
                  [("Institution submits FDR Number, Principal Amount, Maturity Date, and IFSC. ", False), ("Joint Account Undertaking is verified and cryptographically pinned", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.15), Inches(3.0), Inches(1.55),
                  "RBI Capability Registry Router",
                  [("Resolves IFSC against the RBI Bank Infrastructure Master to automatically select ", False), ("Mode 1 (CBS API), Mode 2 (Token Link), or Mode 3 (NeSL)", True), (".", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Tri-Modal Execution", "Adaptive 3-Tier Gateway", "🏦", AMBER_BG, AMBER_BORDER, AMBER_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "Mode 1: CBS / SFMS Webhook",
                  [("Tier-1 Banks (SBI, PNB, Canara, HDFC). ", False), ("SFMS IFN 760 BG/Lien", True), (" automated JSON callback in under 1 second.", False)],
                  pill_tag="Tier-1 PSBs", pill_color=MINT_ACCENT, pill_bg=MINT_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Mode 2: Branch Manager Magic Token",
                  [("Co-operative and Rural Banks. ", False), ("Time-bound cryptographic link dispatched to official branch email; manager confirms lien via SMS OTP", True), (". Zero IT overhead.", False)],
                  pill_tag="Rural & Co-op", pill_color=SKY_ACCENT, pill_bg=SKY_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Mode 3: NeSL Statutory Utility",
                  [("Digital Document Execution (DDE) query directly verifies ", False), ("e-Bank Guarantee and electronic stamp charge registrations", True), (".", False)],
                  pill_tag="NeSL Utility", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), AMBER_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Lien Confirmed", "Dual-Truth Reconciliation", "🔒", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(1.4),
                  "Lien Marked & Freeze Confirmed",
                  [("Bank Core Banking logs an ", False), ("encashment restriction in favor of AICTE", True), (". Unauthorized pre-mature liquidation or loan drawdowns are blocked.", False)],
                  pill_tag="Lien Locked", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.15), Inches(2.83), Inches(1.55),
                  "Dual-Truth Ledger Binding",
                  [("Institution self-declarations are reconciled against ", False), ("independently authenticated Bank Truth", True), (". Maturity tracking initialized.", False)],
                  pill_tag="Dual-Truth", pill_color=SKY_ACCENT, pill_bg=SKY_BG, border_color=SKY_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Achieves 100% nationwide institutional coverage without mandating costly API overhauls on rural or co-operative banks, providing seamless lien verification across all banking tiers.",
                   ["Open Banking CBS", "SFMS IFN 760", "2FA JWT Magic Link", "NeSL DDE Platform"])


# ==============================================================================
# 6. AUTONOMOUS MATURITY ESCALATION & ANTI-LAPSE SLA ENGINE
# ==============================================================================
def build_slide_6(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Automation & Administrative Accountability",
                     "Autonomous Maturity Escalation & Anti-Lapse SLA Engine")
    add_mvp_strip(slide,
                  "Administrative lethargy and manual tracking cause deposits to mature unnoticed, resulting in unauthorized rollovers into non-interest-bearing holding accounts.",
                  "Autonomous Milestone Escalation: Automated chrono-workers monitor deposit horizons (T-180, T-90, T-30 days), dispatch multi-channel notifications, and escalate stalled files through a strict administrative ladder.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Midnight Cron", "Chrono Scan Worker", "⏰", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(1.4),
                  "Celery / Redis Chrono Bot",
                  [("Executes daily at 00:00 UTC across ", False), ("10,000+ active deposit instruments without requiring human initiation", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.15), Inches(3.0), Inches(1.55),
                  "Maturity Horizon Classifier",
                  [("Classifies portfolio exposure into strict statutory intervals: ", False), ("T-180 Days (Early Advisory), T-90 Days (Renewal Open), T-30 Days (Urgent Alert), and D-Day", True), (".", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Omni-Channel Dispatch", "Multi-Tier Alerts", "📢", AMBER_BG, AMBER_BORDER, AMBER_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "WhatsApp Nodal Bot",
                  [("Interactive quick-action buttons sent to Institution Heads: ", False), ("1-tap renewal document submission and live status verification", True), (".", False)],
                  pill_tag="Mobile First", pill_color=MINT_ACCENT, pill_bg=MINT_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Official Email & SMS Gateway",
                  [("Cryptographically signed notices dispatched to ", False), ("registered Trust domain emails and authorized trustees", True), (".", False)],
                  pill_tag="Statutory Dispatch", pill_color=SKY_ACCENT, pill_bg=SKY_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Bank Branch Telemetry Notice",
                  [("Formally instructs bank branch managers that ", False), ("liens remain enforceable pending official AICTE NOC execution", True), (".", False)],
                  pill_tag="Lien Safeguard", pill_color=PURPLE_ACCENT, pill_bg=PURPLE_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), AMBER_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. SLA Escalation", "Accountability Ladder", "🚨", PEACH_BG, PEACH_BORDER, PEACH_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(0.95),
                  "Day 0 - 7: Scrutiny Desk",
                  [("Assigned to Regional Scrutiny Clerk with ", False), ("pre-extracted AI verification checklists", True), (".", False)],
                  pill_tag="Level 0 Desk", pill_color=SKY_ACCENT, pill_bg=SKY_BG)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(1.72), Inches(2.83), Inches(0.95),
                  "Day 10: RO Director Alert",
                  [("Unreviewed past 7 days -> ", False), ("Automated escalation notice dispatched directly to Regional Director", True), (".", False)],
                  pill_tag="Level 1 RO", pill_color=AMBER_ACCENT, pill_bg=AMBER_BG, border_color=AMBER_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.79), Inches(2.83), Inches(0.95),
                  "Day 15: AICTE HQ Red Flag",
                  [("High-priority red flag activated on ", False), ("New Delhi Central Bureau Chief Dashboard", True), (". Enforces zero administrative latency.", False)],
                  pill_tag="Level 2 HQ", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG, border_color=PEACH_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Enforces complete bureaucratic accountability. Eliminates multi-month processing delays through automated escalations, ensuring 100% compliance with statutory lock-in timelines.",
                   ["Celery & Redis 7.2", "Meta Cloud API", "FastAPI Async", "PostgreSQL Triggers"])


# ==============================================================================
# 7. CROSS-GOVERNMENT DPI ENTITY INTELLIGENCE
# ==============================================================================
def build_slide_7(prs):
    slide = create_slide(prs)
    add_slide_header(slide, "System Architecture • Interoperability & Digital Public Infrastructure",
                     "Cross-Government DPI Entity Intelligence Engine")
    add_mvp_strip(slide,
                  "Shell societies and benami trusts exploit identity mismatches where deposit accounts, educational institutions, and trustee PANs do not legally correspond.",
                  "Real-time handshakes with NITI Aayog NGO Darpan, MCA21, and CBDT PAN verify trustee identity, corporate registration, and authorized signatories on Day 1.")

    top_y = Inches(1.9)
    p_h = Inches(4.0)

    draw_pillar(slide, Inches(0.7), top_y, Inches(3.3), p_h, "1. Statutory APIs", "Live Government Feeds", "🌐", SKY_BG, SKY_BORDER, SKY_ACCENT)
    draw_sub_card(slide, Inches(0.85), top_y + Inches(0.65), Inches(3.0), Inches(0.95),
                  "NITI Aayog NGO Darpan", [("Real-time Trust Unique ID lookup; ", False), ("extracts certified list of executive trustees", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(1.72), Inches(3.0), Inches(0.95),
                  "MCA21 Corporate Affairs", [("Validates Section-8 non-profit company ", False), ("CIN, director identity, and active legal status", True), (".", False)])
    draw_sub_card(slide, Inches(0.85), top_y + Inches(2.79), Inches(3.0), Inches(0.95),
                  "CBDT PAN & AISHE Linkage", [("Validates Trust PAN entity name and ", False), ("maps sanctioned student intake capacity", True), (".", False)])

    draw_arrow(slide, Inches(4.1), top_y + Inches(1.9), SKY_ACCENT)

    draw_pillar(slide, Inches(4.45), top_y, Inches(4.6), p_h, "2. Graph Matcher", "Entity Relationship Matrix", "🕸️", PURPLE_BG, PURPLE_BORDER, PURPLE_ACCENT)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(0.65), Inches(4.3), Inches(0.95),
                  "Trust Name Reconciliation",
                  [("Cross-examines ", False), ("FDR Account Holder against Registered Trust Name", True), (" in NGO Darpan registry.", False)],
                  pill_tag="Name Match", pill_color=SKY_ACCENT, pill_bg=SKY_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(1.72), Inches(4.3), Inches(0.95),
                  "Signatory Authorization",
                  [("Matches Authorized Signatory against ", False), ("MCA21 active trustees and directors registry", True), (".", False)],
                  pill_tag="Role Check", pill_color=MINT_ACCENT, pill_bg=MINT_BG)
    draw_sub_card(slide, Inches(4.6), top_y + Inches(2.79), Inches(4.3), Inches(0.95),
                  "Blacklist & Shell Sentinel",
                  [("Cross-references PANs and names against the ", False), ("AICTE debarred entity blacklist", True), (". Eliminates benami trusts prior to approval.", False)],
                  pill_tag="Benami Filter", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG)

    draw_arrow(slide, Inches(9.15), top_y + Inches(1.9), PURPLE_ACCENT)

    draw_pillar(slide, Inches(9.5), top_y, Inches(3.13), p_h, "3. Trust Clearance", "Regulatory Determination", "🛡️", MINT_BG, MINT_BORDER, MINT_ACCENT)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(0.65), Inches(2.83), Inches(1.4),
                  "100% Green Match : Cleared",
                  [("Zero identity discrepancies. ", False), ("Fast-tracks deposit directly to Bank Gateway without requiring manual notarized affidavits", True), (".", False)],
                  pill_tag="Approved", pill_color=MINT_ACCENT, pill_bg=MINT_BG, border_color=MINT_BORDER)
    draw_sub_card(slide, Inches(9.65), top_y + Inches(2.15), Inches(2.83), Inches(1.55),
                  "Discrepancy : Show-Cause",
                  [("Entity mismatch detected. ", False), ("Freezes approval workflows and generates automated show-cause notice", True), (".", False)],
                  pill_tag="Show-Cause", pill_color=PEACH_ACCENT, pill_bg=PEACH_BG, border_color=PEACH_BORDER)

    add_impact_bar(slide, "Architectural Impact & Operational Guarantee",
                   "Integrates directly with National Digital Public Infrastructure (DPI) to eliminate shell societies and benami trusts, saving hundreds of administrative scrutiny hours annually.",
                   ["NITI NGO Darpan API", "MCA21 REST API", "CBDT PAN Gateway", "AISHE Registry"])


# ==============================================================================
# MAIN DECK GENERATION
# ==============================================================================
def main():
    prs = new_deck()
    print("Generating Slide 1: Legacy Records Digitization Engine...")
    build_slide_1(prs)

    print("Generating Slide 2: Hierarchical Multi-Model OCR Routing...")
    build_slide_2(prs)

    print("Generating Slide 3: AI Document Forensics & Tamper Detection...")
    build_slide_3(prs)

    print("Generating Slide 4: Military-Grade Cryptographic Ledger...")
    build_slide_4(prs)

    print("Generating Slide 5: Tri-Modal Universal Bank Verification Gateway...")
    build_slide_5(prs)

    print("Generating Slide 6: Autonomous Maturity Escalation Engine...")
    build_slide_6(prs)

    print("Generating Slide 7: Cross-Government DPI Entity Intelligence...")
    build_slide_7(prs)

    decks_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "decks")
    os.makedirs(decks_dir, exist_ok=True)
    output_path = os.path.join(decks_dir, "AICTE_Innovative_Ideas_Diagrams_Editable.pptx")
    prs.save(output_path)
    print(f"Successfully generated 7 innovative pipeline slides in: {output_path}")

if __name__ == "__main__":
    main()
