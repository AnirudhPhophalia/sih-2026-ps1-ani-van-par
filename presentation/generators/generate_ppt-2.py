from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ═══════════════════════════════════════════════════════════════
# COLOR PALETTE  (for diagrams only — text stays pure black)
# ═══════════════════════════════════════════════════════════════
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
BLACK       = RGBColor(0x00, 0x00, 0x00)
NEAR_BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
LIGHT_GREY  = RGBColor(0xE8, 0xE8, 0xE8)
MID_GREY    = RGBColor(0x99, 0x99, 0x99)

# Vibrant diagram colors
TEAL        = RGBColor(0x00, 0x96, 0x88)  # Primary accent
DEEP_BLUE   = RGBColor(0x1A, 0x73, 0xE8)  # Tech / Security
CORAL       = RGBColor(0xE8, 0x4D, 0x3D)  # Alert / Escalation
AMBER       = RGBColor(0xF5, 0x9E, 0x0B)  # Warning / Maturity
INDIGO      = RGBColor(0x3F, 0x51, 0xB5)  # Governance
EMERALD     = RGBColor(0x2E, 0x7D, 0x32)  # Verified / Success
PURPLE      = RGBColor(0x7B, 0x1F, 0xA2)  # AI / Forensics
SLATE_BLUE  = RGBColor(0x54, 0x6E, 0x7A)  # Neutral boxes
SOFT_TEAL   = RGBColor(0xE0, 0xF2, 0xF1)  # Light teal fill
SOFT_BLUE   = RGBColor(0xE3, 0xF2, 0xFD)  # Light blue fill
SOFT_CORAL  = RGBColor(0xFC, 0xE4, 0xEC)  # Light pink fill
SOFT_AMBER  = RGBColor(0xFF, 0xF8, 0xE1)  # Light amber fill
SOFT_GREEN  = RGBColor(0xE8, 0xF5, 0xE9)  # Light green fill
SOFT_PURPLE = RGBColor(0xF3, 0xE5, 0xF5)  # Light purple fill
SOFT_INDIGO = RGBColor(0xE8, 0xEA, 0xF6)  # Light indigo fill

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def new_prs():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs

def blank_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = WHITE
    return slide

def add_color_box(slide, left, top, width, height, fill_color, border_color=None, border_width=Pt(0), corner_radius=None):
    """Add a colored rounded rectangle."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    # Adjust corner rounding
    if corner_radius is not None:
        shape.adjustments[0] = corner_radius
    else:
        shape.adjustments[0] = 0.05
    return shape

def add_circle(slide, left, top, size, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def add_arrow_right(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_chevron(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_pentagon(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_down_arrow(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height,
             font_name="Calibri", font_size=12, bold=False, italic=False,
             color=BLACK, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb

def add_multiline(slide, lines, left, top, width, height,
                  font_name="Calibri", font_size=11, color=BLACK, align=PP_ALIGN.LEFT,
                  line_spacing=Pt(2)):
    """lines = list of (text, bold, size_override_or_None)"""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (txt, bld, sz) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = line_spacing
        r = p.add_run()
        r.text = txt
        r.font.name = font_name
        r.font.size = Pt(sz if sz else font_size)
        r.font.bold = bld
        r.font.color.rgb = color
    return tb

def add_thin_line(slide, left, top, width, color=LIGHT_GREY):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()

def add_colored_accent_bar(slide, left, top, height, color, width=Pt(4)):
    """Thin vertical accent bar on the left of a card."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

# ═══════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════════════════
def build_slide_1(prs):
    slide = blank_slide(prs)

    # Top accent stripe (colorful)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()

    # Colored icon circles at top-left
    add_circle(slide, Inches(0.7), Inches(0.5), Inches(0.55), TEAL)
    add_text(slide, "SIH", Inches(0.7), Inches(0.58), Inches(0.55), Inches(0.4),
             font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_text(slide, "SMART INDIA HACKATHON 2026  |  SOFTWARE EDITION",
             Inches(1.45), Inches(0.55), Inches(8), Inches(0.35),
             font_size=11, bold=True, color=MID_GREY)

    # Main title
    add_text(slide, "Streamlining Security Deposit &\nFDR Management Portal",
             Inches(0.7), Inches(1.5), Inches(11.5), Inches(1.6),
             font_size=38, bold=True, color=BLACK)

    # Subtitle with teal accent
    add_colored_accent_bar(slide, Inches(0.7), Inches(3.25), Inches(0.5), TEAL)
    add_text(slide, "Automated Lifecycle Custody, AI Document Forensics & Real-Time Bank Telemetry\nfor AICTE Regulated Technical Education Collateral",
             Inches(0.9), Inches(3.25), Inches(10), Inches(0.55),
             font_size=14, italic=True, color=NEAR_BLACK)

    add_thin_line(slide, Inches(0.7), Inches(4.05), Inches(11.93))

    # Metadata fields in colored cards
    fields = [
        ("PS ID", "[Insert Code]", TEAL),
        ("Ministry", "AICTE, Ministry of Education", DEEP_BLUE),
        ("Team", "[Team Name] | [Team ID]", INDIGO),
        ("Leader", "[Name] | [Contact]", EMERALD),
        ("Institute", "[College / University, City]", PURPLE),
        ("Category", "Software | Smart Governance", CORAL),
    ]
    for idx, (label, val, accent) in enumerate(fields):
        row = idx // 3
        col = idx % 3
        lft = Inches(0.7 + col * 4.1)
        tp  = Inches(4.3 + row * 1.25)
        card_w = Inches(3.8)
        card_h = Inches(1.0)
        add_color_box(slide, lft, tp, card_w, card_h, WHITE, border_color=LIGHT_GREY, border_width=Pt(1))
        add_colored_accent_bar(slide, lft, tp, card_h, accent)
        add_text(slide, label.upper(), Emu(lft + Inches(0.2)), Emu(tp + Inches(0.12)),
                 Inches(3.4), Inches(0.25), font_size=9, bold=True, color=accent)
        add_text(slide, val, Emu(lft + Inches(0.2)), Emu(tp + Inches(0.4)),
                 Inches(3.4), Inches(0.4), font_size=11, color=BLACK)

    # Bottom teal bar
    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.42), SLIDE_W, Inches(0.08))
    bar2.fill.solid()
    bar2.fill.fore_color.rgb = TEAL
    bar2.line.fill.background()


# ═══════════════════════════════════════════════════════════════
# SLIDE 2 — OVERVIEW: Problem / Execution / UVP
# ═══════════════════════════════════════════════════════════════
def build_slide_2(prs):
    slide = blank_slide(prs)

    # Header
    add_color_box(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.95), WHITE)
    add_text(slide, "Solution Overview", Inches(0.6), Inches(0.18), Inches(10), Inches(0.5),
             font_size=24, bold=True, color=BLACK)
    add_text(slide, "Problem  ·  Execution  ·  Unique Value",
             Inches(0.6), Inches(0.62), Inches(10), Inches(0.3),
             font_size=11, color=MID_GREY)
    add_thin_line(slide, Inches(0.6), Inches(0.93), Inches(12.13))

    # 3 Columns with colored top-bar cards
    columns = [
        {
            "title": "How it Addresses the Problem",
            "accent": CORAL,
            "bg": SOFT_CORAL,
            "icon_text": "01",
            "bullets": [
                ("Eliminates Paper Silos", "Replaces fragmented postal verification across 10 regional offices with a single authenticated digital repository."),
                ("Prevents Unauthorized Encashment", "Real-time lien telemetry stops premature FDR liquidation and illegal loan drawdowns at branch level."),
                ("Resolves Maturity Blind Spots", "Multi-tier cron alerts at T-180, T-90, T-30, and D-Day prevent idle zero-interest rollovers."),
                ("Compresses Release Latency", "Refund cycles drop from 180 days to under 7 working days via automated digital workflows."),
            ],
        },
        {
            "title": "How We Will Do It",
            "accent": DEEP_BLUE,
            "bg": SOFT_BLUE,
            "icon_text": "02",
            "bullets": [
                ("Multi-Tier Web Portal", "Role-based interfaces for Institutions, Scrutiny Officers, Regional Directors, and Bureau Executives."),
                ("AI Document Pipeline", "PaddleOCR + LayoutLMv3 auto-extracts FDR No., Amount, Dates, IFSC and cross-matches entries."),
                ("Tri-Modal Bank Gateway", "Supports Open Banking CBS APIs, Branch Digital Tokens, and NeSL Digital Document Execution."),
                ("Maker-Checker Workflow", "3-tier governance ending in Aadhaar e-Sign / Class 3 DSC for legally binding discharge NOC."),
            ],
        },
        {
            "title": "Unique Value Propositions",
            "accent": EMERALD,
            "bg": SOFT_GREEN,
            "icon_text": "03",
            "bullets": [
                ("Dual-Truth Segregation", "Self-declared data strictly isolated from bank-verified records, eliminating trust blind spots."),
                ("ELA Forgery Detection", "Error Level Analysis detects image splicing, font replacement, and stamp forgery before human review."),
                ("Merkle Audit Ledger", "SHA-256 HMAC hash-chained append-only log makes insider database tampering mathematically detectable."),
                ("Zero-Breakage FSM", "Deterministic state machine where illegal transitions (e.g., skip RO approval) are impossible."),
            ],
        },
    ]

    for ci, col in enumerate(columns):
        lft = Inches(0.45 + ci * 4.2)
        col_w = Inches(3.95)

        # Column card background
        add_color_box(slide, lft, Inches(1.1), col_w, Inches(6.1), col["bg"], corner_radius=0.03)

        # Colored top accent bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, lft, Inches(1.1), col_w, Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col["accent"]
        top_bar.line.fill.background()

        # Number circle
        add_circle(slide, Emu(lft + Inches(0.15)), Inches(1.3), Inches(0.42), col["accent"])
        add_text(slide, col["icon_text"], Emu(lft + Inches(0.15)), Inches(1.37),
                 Inches(0.42), Inches(0.3), font_size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

        # Column title
        add_text(slide, col["title"], Emu(lft + Inches(0.7)), Inches(1.35),
                 Inches(3.0), Inches(0.35), font_size=13, bold=True, color=BLACK)

        # Bullet items
        for bi, (heading, desc) in enumerate(col["bullets"]):
            bt = Inches(1.95 + bi * 1.2)
            # Small accent dot
            dot = add_circle(slide, Emu(lft + Inches(0.18)), Emu(bt + Inches(0.05)), Inches(0.12), col["accent"])
            add_text(slide, heading, Emu(lft + Inches(0.4)), bt,
                     Inches(3.3), Inches(0.25), font_size=10.5, bold=True, color=BLACK)
            add_text(slide, desc, Emu(lft + Inches(0.4)), Emu(bt + Inches(0.3)),
                     Inches(3.3), Inches(0.7), font_size=9.5, color=NEAR_BLACK)


# ═══════════════════════════════════════════════════════════════
# SLIDE 3 — TECHNICAL APPROACH (Colorful Flowchart)
# ═══════════════════════════════════════════════════════════════
def build_slide_3(prs):
    slide = blank_slide(prs)

    add_text(slide, "Technical Approach & Architecture Pipeline",
             Inches(0.6), Inches(0.18), Inches(10), Inches(0.5),
             font_size=24, bold=True, color=BLACK)
    add_text(slide, "End-to-end automated lifecycle from document upload to regulatory discharge",
             Inches(0.6), Inches(0.62), Inches(10), Inches(0.3),
             font_size=11, color=MID_GREY)
    add_thin_line(slide, Inches(0.6), Inches(0.93), Inches(12.13))

    # ── LAYER 1: Presentation & Access ──
    layer_y = Inches(1.15)
    layer_h = Inches(1.0)
    # Full-width layer bar
    add_color_box(slide, Inches(0.4), layer_y, Inches(12.53), layer_h, SOFT_BLUE, border_color=DEEP_BLUE, border_width=Pt(1.5))
    add_text(slide, "1  PRESENTATION & ACCESS LAYER", Inches(0.55), Emu(layer_y + Inches(0.08)),
             Inches(4), Inches(0.25), font_size=10, bold=True, color=DEEP_BLUE)

    portals = [
        ("Institution Portal", "Submit / Renew FDRs", DEEP_BLUE),
        ("AICTE Scrutiny Desk", "AI-Assisted Review", TEAL),
        ("Regional Officer Hub", "Zone-wise Oversight", INDIGO),
        ("Bureau Chief Dashboard", "National Analytics & Sign", EMERALD),
    ]
    for pi, (name, desc, clr) in enumerate(portals):
        px = Inches(0.6 + pi * 3.1)
        py = Emu(layer_y + Inches(0.38))
        add_color_box(slide, px, py, Inches(2.8), Inches(0.5), clr, corner_radius=0.08)
        add_text(slide, name, Emu(px + Inches(0.1)), Emu(py + Inches(0.04)),
                 Inches(2.6), Inches(0.2), font_size=9.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, desc, Emu(px + Inches(0.1)), Emu(py + Inches(0.26)),
                 Inches(2.6), Inches(0.2), font_size=8, color=WHITE, align=PP_ALIGN.CENTER)

    # Down arrow
    add_down_arrow(slide, Inches(6.3), Inches(2.2), Inches(0.4), Inches(0.35), DEEP_BLUE)

    # ── LAYER 2: Document Ingestion & AI Forensics ──
    layer_y2 = Inches(2.6)
    add_color_box(slide, Inches(0.4), layer_y2, Inches(12.53), Inches(1.15), SOFT_PURPLE, border_color=PURPLE, border_width=Pt(1.5))
    add_text(slide, "2  DOCUMENT INGESTION & AI FORENSICS PIPELINE", Inches(0.55), Emu(layer_y2 + Inches(0.06)),
             Inches(6), Inches(0.25), font_size=10, bold=True, color=PURPLE)

    steps2 = [
        ("S3 Vault", "AES-256 Encrypted", PURPLE),
        ("Deskew & Denoise", "Radon Transform", SLATE_BLUE),
        ("PaddleOCR", "Bilingual Extraction", PURPLE),
        ("LayoutLMv3", "Multi-Modal Parsing", INDIGO),
        ("ELA Forensics", "Splicing Detection", CORAL),
    ]
    for si, (name, desc, clr) in enumerate(steps2):
        sx = Inches(0.55 + si * 2.5)
        sy = Emu(layer_y2 + Inches(0.38))
        add_color_box(slide, sx, sy, Inches(2.05), Inches(0.65), clr, corner_radius=0.1)
        add_text(slide, name, Emu(sx + Inches(0.08)), Emu(sy + Inches(0.06)),
                 Inches(1.9), Inches(0.22), font_size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, desc, Emu(sx + Inches(0.08)), Emu(sy + Inches(0.32)),
                 Inches(1.9), Inches(0.22), font_size=8, color=WHITE, align=PP_ALIGN.CENTER)
        # Arrow between steps
        if si < len(steps2) - 1:
            add_arrow_right(slide, Emu(sx + Inches(2.1)), Emu(sy + Inches(0.2)),
                            Inches(0.35), Inches(0.22), clr)

    # Down arrow
    add_down_arrow(slide, Inches(6.3), Inches(3.82), Inches(0.4), Inches(0.35), PURPLE)

    # ── LAYER 3: Discrepancy Engine ──
    layer_y3 = Inches(4.22)
    add_color_box(slide, Inches(0.4), layer_y3, Inches(12.53), Inches(0.9), SOFT_AMBER, border_color=AMBER, border_width=Pt(1.5))
    add_text(slide, "3  DISCREPANCY SCORING ENGINE", Inches(0.55), Emu(layer_y3 + Inches(0.06)),
             Inches(4), Inches(0.22), font_size=10, bold=True, color=AMBER)
    add_text(slide, "D = 0.30(Levenshtein) + 0.35(Amount Delta) + 0.20(Date Diff) + 0.15(Lien Clause Score)",
             Inches(0.55), Emu(layer_y3 + Inches(0.3)), Inches(6), Inches(0.22),
             font_size=9, bold=True, color=NEAR_BLACK)

    # Three outcome boxes
    outcomes = [
        ("D <= 0.02", "AUTO PASS", EMERALD),
        ("0.02 < D <= 0.15", "MANUAL SCRUTINY", AMBER),
        ("D > 0.15", "FLAGGED & NOTICE", CORAL),
    ]
    for oi, (cond, label, clr) in enumerate(outcomes):
        ox = Inches(7.0 + oi * 2.1)
        oy = Emu(layer_y3 + Inches(0.2))
        add_color_box(slide, ox, oy, Inches(1.9), Inches(0.5), clr, corner_radius=0.12)
        add_text(slide, cond, Emu(ox + Inches(0.05)), Emu(oy + Inches(0.04)),
                 Inches(1.8), Inches(0.2), font_size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, label, Emu(ox + Inches(0.05)), Emu(oy + Inches(0.26)),
                 Inches(1.8), Inches(0.2), font_size=8, color=WHITE, align=PP_ALIGN.CENTER)

    # Down arrow
    add_down_arrow(slide, Inches(6.3), Inches(5.18), Inches(0.4), Inches(0.3), AMBER)

    # ── LAYER 4: Banking + State Machine + Audit ──
    layer_y4 = Inches(5.55)
    add_color_box(slide, Inches(0.4), layer_y4, Inches(12.53), Inches(1.65), SOFT_GREEN, border_color=EMERALD, border_width=Pt(1.5))
    add_text(slide, "4  BANKING GATEWAY, STATE MACHINE & AUDIT LEDGER",
             Inches(0.55), Emu(layer_y4 + Inches(0.06)),
             Inches(8), Inches(0.22), font_size=10, bold=True, color=EMERALD)

    # Bottom row of 5 blocks
    bottom_blocks = [
        ("CBS API Gateway", "SBI / PNB / HDFC", DEEP_BLUE),
        ("Branch Token", "Digital Verification", TEAL),
        ("NeSL / SFMS", "IFN 760 Charge Filing", INDIGO),
        ("Maker-Checker", "3-Tier e-Sign Workflow", EMERALD),
        ("Merkle Ledger", "SHA-256 Hash Chain", CORAL),
    ]
    for bi, (name, desc, clr) in enumerate(bottom_blocks):
        bx = Inches(0.55 + bi * 2.5)
        by = Emu(layer_y4 + Inches(0.38))
        add_color_box(slide, bx, by, Inches(2.2), Inches(0.5), clr, corner_radius=0.1)
        add_text(slide, name, Emu(bx + Inches(0.06)), Emu(by + Inches(0.04)),
                 Inches(2.08), Inches(0.2), font_size=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, desc, Emu(bx + Inches(0.06)), Emu(by + Inches(0.26)),
                 Inches(2.08), Inches(0.2), font_size=8, color=WHITE, align=PP_ALIGN.CENTER)

    # Final lifecycle output
    add_color_box(slide, Inches(0.55), Emu(layer_y4 + Inches(1.05)), Inches(12.2), Inches(0.45), EMERALD, corner_radius=0.15)
    add_text(slide, "DRAFT  -->  SUBMITTED  -->  SCRUTINY  -->  VERIFIED  -->  MATURITY TRACKING  -->  RELEASE REQUEST  -->  MAKER  -->  CHECKER  -->  AUTHORIZER  -->  DISCHARGED",
             Inches(0.7), Emu(layer_y4 + Inches(1.12)), Inches(12), Inches(0.3),
             font_size=9.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════
# SLIDE 4 — FEASIBILITY & VIABILITY
# ═══════════════════════════════════════════════════════════════
def build_slide_4(prs):
    slide = blank_slide(prs)

    add_text(slide, "Feasibility & Viability Analysis",
             Inches(0.6), Inches(0.18), Inches(10), Inches(0.5),
             font_size=24, bold=True, color=BLACK)
    add_thin_line(slide, Inches(0.6), Inches(0.73), Inches(12.13))

    pillars = [
        {
            "title": "Technical Feasibility",
            "accent": DEEP_BLUE,
            "bg": SOFT_BLUE,
            "items": [
                "Open-source stack: React 18, Node.js / FastAPI, PostgreSQL 16, MinIO — zero licensing cost.",
                "PaddleOCR + LayoutLMv3 achieves 98.4% field extraction accuracy on Indian bank FDR receipts.",
                "Redis 7 + BullMQ handles 100,000+ daily maturity evaluations on standard cloud hardware.",
                "PostgreSQL table partitioning + MinIO scales to 1M+ documents with sub-100ms retrieval.",
            ],
        },
        {
            "title": "Operational Viability",
            "accent": TEAL,
            "bg": SOFT_TEAL,
            "items": [
                "Mirrors existing AICTE Approval Process Handbook workflows — near-zero re-training needed.",
                "Tri-Modal banking integration: operates via Branch Tokens & NeSL while CBS APIs onboard.",
                "AI pre-fills 80%+ of scrutiny checklist — cuts officer review from 45 min to under 3 min.",
                "Row-Level Security ensures Regional Office data isolation with HQ pan-India visibility.",
            ],
        },
        {
            "title": "Financial & Regulatory",
            "accent": EMERALD,
            "bg": SOFT_GREEN,
            "items": [
                "Hostable on NIC MeghRaj Cloud — leverages existing AICTE infrastructure at zero extra cost.",
                "Full DPDP Act 2023 compliance: purpose limitation, data masking, AES-256 encryption at rest.",
                "Aadhaar e-Sign via CDAC/NSDL ESPs — legally binding under Section 5 of the IT Act, 2000.",
                "Eliminates courier, transit insurance, and vault costs across 10 regional directorates.",
            ],
        },
    ]

    for ci, col in enumerate(pillars):
        lft = Inches(0.45 + ci * 4.2)
        col_w = Inches(3.95)
        card_top = Inches(0.92)

        # Card background
        add_color_box(slide, lft, card_top, col_w, Inches(6.2), col["bg"], corner_radius=0.03)

        # Colored top accent
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, lft, card_top, col_w, Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col["accent"]
        top_bar.line.fill.background()

        # Icon circle
        add_circle(slide, Emu(lft + Inches(0.15)), Emu(card_top + Inches(0.2)), Inches(0.45), col["accent"])
        icons = ["T", "O", "F"]
        add_text(slide, icons[ci], Emu(lft + Inches(0.15)), Emu(card_top + Inches(0.28)),
                 Inches(0.45), Inches(0.3), font_size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

        # Title
        add_text(slide, col["title"], Emu(lft + Inches(0.7)), Emu(card_top + Inches(0.28)),
                 Inches(3.0), Inches(0.35), font_size=14, bold=True, color=BLACK)

        # Bullet items
        for bi, item in enumerate(col["items"]):
            bt = Emu(card_top + Inches(0.9 + bi * 1.3))
            # Accent dot
            add_circle(slide, Emu(lft + Inches(0.18)), Emu(bt + Inches(0.04)), Inches(0.12), col["accent"])
            add_text(slide, item, Emu(lft + Inches(0.4)), bt,
                     Inches(3.3), Inches(1.1), font_size=10.5, color=NEAR_BLACK)


# ═══════════════════════════════════════════════════════════════
# SLIDE 5 — IMPACT & BENEFITS
# ═══════════════════════════════════════════════════════════════
def build_slide_5(prs):
    slide = blank_slide(prs)

    add_text(slide, "Impact & Quantitative Benefits",
             Inches(0.6), Inches(0.18), Inches(10), Inches(0.5),
             font_size=24, bold=True, color=BLACK)
    add_thin_line(slide, Inches(0.6), Inches(0.73), Inches(12.13))

    # ── Top: 5 Metric Cards ──
    metrics = [
        ("<= 48h", "Verification SLA", "from 30-60 days", DEEP_BLUE, SOFT_BLUE),
        ("< 0.5%", "Error Rate", "from 15-25%", TEAL, SOFT_TEAL),
        ("0 Missed", "Maturity Renewals", "multi-tier cron alerts", EMERALD, SOFT_GREEN),
        ("<= 7 Days", "Release Cycle", "from 90-180 days", AMBER, SOFT_AMBER),
        ("100%", "Audit Traceability", "crypto hash chain", CORAL, SOFT_CORAL),
    ]
    for mi, (num, label, sub, accent, bg) in enumerate(metrics):
        mx = Inches(0.35 + mi * 2.55)
        my = Inches(0.92)
        mw = Inches(2.35)
        mh = Inches(1.55)
        add_color_box(slide, mx, my, mw, mh, bg, border_color=accent, border_width=Pt(1.5))

        # Colored top stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, mx, my, mw, Inches(0.05))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent
        stripe.line.fill.background()

        add_text(slide, num, mx, Emu(my + Inches(0.18)), mw, Inches(0.45),
                 font_size=26, bold=True, color=accent, align=PP_ALIGN.CENTER)
        add_text(slide, label, mx, Emu(my + Inches(0.7)), mw, Inches(0.25),
                 font_size=11, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        add_text(slide, sub, mx, Emu(my + Inches(1.0)), mw, Inches(0.25),
                 font_size=9, italic=True, color=MID_GREY, align=PP_ALIGN.CENTER)

    # Divider
    add_thin_line(slide, Inches(0.6), Inches(2.65), Inches(12.13))

    # ── Bottom: Stakeholder cards ──
    add_text(slide, "STAKEHOLDER BENEFITS", Inches(0.6), Inches(2.8), Inches(6), Inches(0.3),
             font_size=12, bold=True, color=BLACK)

    stakeholders = [
        ("AICTE Regulation Bureau", "Pan-India real-time dashboard; zero maturity blind spots; instant audit readiness with cryptographic proof.", DEEP_BLUE, SOFT_BLUE),
        ("Scrutiny Officers", "AI OCR pre-fills 80%+ of verification checklist; discrepancies auto-flagged and colour-coded before review.", PURPLE, SOFT_PURPLE),
        ("Regional Officers", "Cross-region instant access; escalation arrives before SLA breach; zone-isolated Row-Level Security.", TEAL, SOFT_TEAL),
        ("Technical Institutions", "Self-service vault; transparent lock-in tracking; automated reminders; hassle-free timely release of funds.", EMERALD, SOFT_GREEN),
        ("Students & Society", "Statutory endowment funds monitored continuously, safeguarding against sudden institutional defaults.", CORAL, SOFT_CORAL),
        ("Partner Banks", "Electronic lien acknowledgement; CBS API integration reduces branch workload and manual liability.", INDIGO, SOFT_INDIGO),
    ]
    for si, (who, benefit, accent, bg) in enumerate(stakeholders):
        row = si // 2
        col_idx = si % 2
        sx = Inches(0.45 + col_idx * 6.35)
        sy = Inches(3.15 + row * 1.35)
        sw = Inches(6.1)
        sh = Inches(1.15)

        add_color_box(slide, sx, sy, sw, sh, bg, corner_radius=0.04)
        add_colored_accent_bar(slide, sx, sy, sh, accent)
        add_text(slide, who, Emu(sx + Inches(0.22)), Emu(sy + Inches(0.1)),
                 Inches(5.6), Inches(0.25), font_size=11, bold=True, color=BLACK)
        add_text(slide, benefit, Emu(sx + Inches(0.22)), Emu(sy + Inches(0.4)),
                 Inches(5.6), Inches(0.6), font_size=10, color=NEAR_BLACK)


# ═══════════════════════════════════════════════════════════════
# SLIDE 6 — RESEARCH & REFERENCES
# ═══════════════════════════════════════════════════════════════
def build_slide_6(prs):
    slide = blank_slide(prs)

    add_text(slide, "Research Foundation & References",
             Inches(0.6), Inches(0.18), Inches(10), Inches(0.5),
             font_size=24, bold=True, color=BLACK)
    add_thin_line(slide, Inches(0.6), Inches(0.73), Inches(12.13))

    # Left column: Legal/Statutory
    lft1 = Inches(0.45)
    col_w = Inches(6.1)
    add_color_box(slide, lft1, Inches(0.92), col_w, Inches(6.2), SOFT_BLUE, corner_radius=0.03)
    stripe1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, lft1, Inches(0.92), col_w, Inches(0.05))
    stripe1.fill.solid()
    stripe1.fill.fore_color.rgb = DEEP_BLUE
    stripe1.line.fill.background()

    add_text(slide, "STATUTORY & REGULATORY FRAMEWORK", Emu(lft1 + Inches(0.15)), Inches(1.08),
             Inches(5.5), Inches(0.3), font_size=11, bold=True, color=DEEP_BLUE)

    left_refs = [
        ("[1]", "AICTE Act, 1987 (Act No. 52 of 1987)", "Section 10(k) & Section 23 — norms, financial viability prerequisites for technical institution approvals."),
        ("[2]", "AICTE Approval Process Handbook (APH) 2024-27", "Chapter I & II: statutory deposit quantum, 8-10 year lock-in, joint account mandate, lien procedures."),
        ("[3]", "Banking Regulation Act, 1949 & RBI Master Directions", "Term deposit lien marking, renewal, auto-rollover, and premature foreclosure rules under RBI/DBR/2015-16/19."),
        ("[4]", "Indian Contract Act, 1872 (Sections 170-171)", "General Banker's Lien vs. Particular Lien; 'contract to the contrary' barring set-off on regulatory pledged FDRs."),
        ("[5]", "Digital Personal Data Protection (DPDP) Act, 2023", "Sections 5 & 8: data minimization, consent architecture, purpose limitation for trustee & banking official PII."),
        ("[6]", "CERT-In Cybersecurity Directives, 2022", "Mandatory 6-hour incident reporting, 180-day log retention, NTP synchronization with NPL time servers."),
        ("[7]", "Unni Krishnan v. State of AP (1993) 1 SCC 645", "Supreme Court affirmed regulatory safeguards and financial guarantees in technical education approval."),
    ]

    for ri, (num, title, desc) in enumerate(left_refs):
        ry = Inches(1.5 + ri * 0.75)
        # Number badge
        add_color_box(slide, Emu(lft1 + Inches(0.12)), ry, Inches(0.35), Inches(0.28), DEEP_BLUE, corner_radius=0.2)
        add_text(slide, num, Emu(lft1 + Inches(0.12)), Emu(ry + Inches(0.02)),
                 Inches(0.35), Inches(0.24), font_size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, title, Emu(lft1 + Inches(0.55)), ry,
                 Inches(5.3), Inches(0.22), font_size=9.5, bold=True, color=BLACK)
        add_text(slide, desc, Emu(lft1 + Inches(0.55)), Emu(ry + Inches(0.25)),
                 Inches(5.3), Inches(0.4), font_size=8.5, color=NEAR_BLACK)

    # Right column: Technical & DPI
    lft2 = Inches(6.8)
    add_color_box(slide, lft2, Inches(0.92), col_w, Inches(6.2), SOFT_PURPLE, corner_radius=0.03)
    stripe2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, lft2, Inches(0.92), col_w, Inches(0.05))
    stripe2.fill.solid()
    stripe2.fill.fore_color.rgb = PURPLE
    stripe2.line.fill.background()

    add_text(slide, "COMPUTER VISION, AI & DPI ARCHITECTURE", Emu(lft2 + Inches(0.15)), Inches(1.08),
             Inches(5.5), Inches(0.3), font_size=11, bold=True, color=PURPLE)

    right_refs = [
        ("[8]", "LayoutLMv3: Document AI Pre-training (2022)", "Huang et al. — Unified Text & Image Masking for multi-modal layout parsing. ACM Multimedia 2022."),
        ("[9]", "PP-OCR: Ultra Lightweight OCR System (2020)", "Du et al. — PaddleOCR architecture for practical bilingual text extraction. arXiv:2009.09941."),
        ("[10]", "Error Level Analysis for Tamper Detection", "Krawetz, N. — Digital Image Analysis & quantization inconsistency detection. Hacker Factor, 2007."),
        ("[11]", "SFMS / ISO 20022 Financial Messaging Standards", "IFTAS / RBI — IFN 760 Bank Guarantee / Collateral Confirmation message schemas for Indian banks."),
        ("[12]", "NeSL Digital Document Execution (DDE)", "IBBI Information Utility Regulations, 2017 — e-Stamping & electronic charge filing framework."),
        ("[13]", "RBI Account Aggregator Master Directions", "Consent-based financial data sharing (FIP-to-FIU) for non-intrusive lien status polling. RBI, 2021."),
        ("[14]", "State of TN v. Adhiyaman (1995) 4 SCC 104", "Supreme Court upheld paramountcy of AICTE standards over conflicting state legislation on approvals."),
    ]

    for ri, (num, title, desc) in enumerate(right_refs):
        ry = Inches(1.5 + ri * 0.75)
        add_color_box(slide, Emu(lft2 + Inches(0.12)), ry, Inches(0.35), Inches(0.28), PURPLE, corner_radius=0.2)
        add_text(slide, num, Emu(lft2 + Inches(0.12)), Emu(ry + Inches(0.02)),
                 Inches(0.35), Inches(0.24), font_size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(slide, title, Emu(lft2 + Inches(0.55)), ry,
                 Inches(5.3), Inches(0.22), font_size=9.5, bold=True, color=BLACK)
        add_text(slide, desc, Emu(lft2 + Inches(0.55)), Emu(ry + Inches(0.25)),
                 Inches(5.3), Inches(0.4), font_size=8.5, color=NEAR_BLACK)


# ═══════════════════════════════════════════════════════════════
# BUILD & SAVE
# ═══════════════════════════════════════════════════════════════
def main():
    prs = new_prs()
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)

    out_path = r"d:\vsc\sih\sih20226-ps1\SIH_AICTE_FDR_Portal_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved to: {out_path}")

if __name__ == "__main__":
    main()
