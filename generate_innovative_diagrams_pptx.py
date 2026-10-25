"""
AICTE FDR Portal - Presentation Diagrams Generator (Judge-Friendly Edition)
Theme: Inspired by the 5 reference styles (Clean visual flows, 3-pillar problem-solution-impact,
closed-loop architecture, and impact scorecards).
Language: Clear, punchy, judge-friendly (no obscure AI math jargon; focuses on real-world impact).
Deliverable: AICTE_Innovative_Ideas_Diagrams_Editable.pptx (100% Native Editable PPT Shapes)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# FRESH COLOR PALETTE (Clean, Modern, Approachable)
# ==============================================================================
CANVAS_BG       = RGBColor(0xFA, 0xFB, 0xFC)
WHITE           = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT       = RGBColor(0x0F, 0x17, 0x2A) # Slate 900
BODY_TEXT       = RGBColor(0x33, 0x41, 0x55) # Slate 700
MUTED_TEXT      = RGBColor(0x64, 0x74, 0x8B) # Slate 500
BORDER_LIGHT    = RGBColor(0xE2, 0xE8, 0xF0) # Slate 200

# Theme Accents
SKY_BG          = RGBColor(0xF0, 0xF9, 0xFF) # Light Sky
SKY_BORDER      = RGBColor(0xBA, 0xE6, 0xFD)
SKY_ACCENT      = RGBColor(0x02, 0x84, 0xC7)

LILAC_BG        = RGBColor(0xEE, 0xF2, 0xFF) # Soft Indigo / Lilac
LILAC_BORDER    = RGBColor(0xC7, 0xD2, 0xFE)
LILAC_ACCENT    = RGBColor(0x4F, 0x46, 0xE5)

MINT_BG         = RGBColor(0xEC, 0xFD, 0xF5) # Soft Emerald
MINT_BORDER     = RGBColor(0xA7, 0xF3, 0xD0)
MINT_ACCENT     = RGBColor(0x05, 0x96, 0x69)

PEACH_BG        = RGBColor(0xFF, 0xF1, 0xF2) # Soft Rose / Coral
PEACH_BORDER    = RGBColor(0xFE, 0xCD, 0xD3)
PEACH_ACCENT    = RGBColor(0xE1, 0x1D, 0x48)

AMBER_BG        = RGBColor(0xFF, 0xFB, 0xEB) # Warm Amber
AMBER_BORDER    = RGBColor(0xFD, 0xE6, 0x8A)
AMBER_ACCENT    = RGBColor(0xD9, 0x77, 0x06)

PURPLE_BG       = RGBColor(0xF5, 0xF3, 0xFF) # Violet
PURPLE_BORDER   = RGBColor(0xDD, 0xD6, 0xFE)
PURPLE_ACCENT   = RGBColor(0x7C, 0x3A, 0xED)

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

def add_header(slide, title_text, super_title, subtitle_text):
    # Super Title (Small uppercase badge)
    tb_sup = slide.shapes.add_textbox(Inches(0.7), Inches(0.28), Inches(10), Inches(0.25))
    tf_sup = tb_sup.text_frame
    p_sup = tf_sup.paragraphs[0]
    r_sup = p_sup.add_run()
    r_sup.text = super_title.upper()
    r_sup.font.name = "Calibri"
    r_sup.font.size = Pt(9.5)
    r_sup.font.bold = True
    r_sup.font.color.rgb = LILAC_ACCENT

    # Main Title
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(0.52), Inches(10), Inches(0.48))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title_text
    r.font.name = "Calibri"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = DARK_TEXT

    # Subtitle
    tb_sub = slide.shapes.add_textbox(Inches(0.7), Inches(1.02), Inches(11.9), Inches(0.32))
    tf_sub = tb_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = subtitle_text
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = MUTED_TEXT

    # Thin Divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.36), Inches(11.933), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_LIGHT
    line.line.fill.background()

# ==============================================================================
# SLIDE 1: 5-STEP VISUAL TECHNICAL APPROACH (Inspired by Reference 5)
# Snake / Horizontal Workflow with Icons, Simple English, and Side Hardware/Spec Card
# ==============================================================================
def build_slide_technical_approach(prs):
    slide = create_slide(prs)
    add_header(slide,
               "How It Works: End-to-End Automated FDR Lifecycle",
               "Technical Approach & Architecture",
               "A streamlined 5-step journey replacing paper couriers and manual almirahs with instant digital verification.")

    # 5 Sequential Process Cards in a dynamic clean flow
    step_y = Inches(1.6)
    card_w = Inches(2.2)
    card_h = Inches(3.6)
    gap = Inches(0.24)

    steps = [
        ("1. Digital Intake", "📱", LILAC_BG, LILAC_BORDER, LILAC_ACCENT,
         "Institution Uploads",
         [("College logs in", True), (" and enters basic FDR details.", False),
          ("\n• Uploads photo/scan", False), (" of FDR receipt.", False),
          ("\n• ", False), ("Smart Auto-Crop", True), (" cleans up yellowed paper or shadows instantly.", False)]),

        ("2. AI Scrutiny", "🤖", SKY_BG, SKY_BORDER, SKY_ACCENT,
         "Dual-AI Scrutiny",
         [("Dual-AI Engine", True), (" extracts FDR No., Amount, Bank Name & Dates in 2 seconds.", False),
          ("\n• Spots ", False), ("Photoshop / Canva edits", True), (" automatically.", False),
          ("\n• Mismatches flagged for ", False), ("1-click review", True), (".", False)]),

        ("3. Bank Check", "🏦", AMBER_BG, AMBER_BORDER, AMBER_ACCENT,
         "Tri-Modal Gateway",
         [("Checks directly with bank", True), (" without waiting for paper post.", False),
          ("\n• Big Banks (SBI/HDFC): ", False), ("Direct API", True), (" check.", False),
          ("\n• Rural Banks: ", False), ("Secure 1-tap OTP link", True), (" sent to Branch Manager.", False)]),

        ("4. Anti-Lapse", "⏰", PEACH_BG, PEACH_BORDER, PEACH_ACCENT,
         "Automated Follow-ups",
         [("Autonomous Bot", True), (" tracks FDR maturity dates daily.", False),
          ("\n• Alerts Principal on ", False), ("WhatsApp & Email", True), (" at 180, 90 & 30 days.", False),
          ("\n• Stalled files ", False), ("auto-escalate", True), (" to Director desk.", False)]),

        ("5. Secure Release", "📜", MINT_BG, MINT_BORDER, MINT_ACCENT,
         "1-Click Discharge",
         [("Once lock-in finishes, ", False), ("AICTE Bureau e-Signs", True), (" legal NOC.", False),
          ("\n• Embeds ", False), ("Encrypted QR Code", True), (" on release letter.", False),
          ("\n• Bank scans QR to ", False), ("safely unfreeze deposit", True), (".", False)])
    ]

    for idx, (title, icon, bg_col, border_col, accent_col, role, bullets) in enumerate(steps):
        left_x = Inches(0.7) + idx * (card_w + gap)

        # Card container with retro clean border
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, step_y, card_w, card_h)
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = border_col
        box.line.width = Pt(1.8)
        box.adjustments[0] = 0.06

        # Icon Circle
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_x + Inches(0.15), step_y + Inches(0.15), Inches(0.48), Inches(0.48))
        circ.fill.solid()
        circ.fill.fore_color.rgb = WHITE
        circ.line.color.rgb = border_col
        circ.line.width = Pt(1.2)
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = p_c.add_run()
        r_c.text = icon
        r_c.font.size = Pt(13)

        # Step Title
        tb_t = slide.shapes.add_textbox(left_x + Inches(0.7), step_y + Inches(0.16), card_w - Inches(0.8), Inches(0.45))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = accent_col

        # Role Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.15), step_y + Inches(0.75), card_w - Inches(0.3), Inches(0.24))
        pill.fill.solid()
        pill.fill.fore_color.rgb = WHITE
        pill.line.color.rgb = border_col
        pill.line.width = Pt(1)
        pill.adjustments[0] = 0.3
        tf_p = pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        r_p = p_p.add_run()
        r_p.text = role.upper()
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(7.5)
        r_p.font.bold = True
        r_p.font.color.rgb = accent_col

        # Bullet text inside card
        tb_b = slide.shapes.add_textbox(left_x + Inches(0.12), step_y + Inches(1.1), card_w - Inches(0.24), card_h - Inches(1.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        for text_part, is_bold in bullets:
            r_b = p_b.add_run()
            r_b.text = text_part
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(9)
            r_b.font.bold = is_bold
            r_b.font.color.rgb = DARK_TEXT if is_bold else BODY_TEXT

        # Arrow connector to next step
        if idx < 4:
            arrow_left = left_x + card_w + Inches(0.04)
            arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_left, step_y + Inches(1.65), Inches(0.16), Inches(0.22))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = MUTED_TEXT
            arrow.line.fill.background()

    # Bottom Spanning Card: Technology Stack & Key Guarantee (Inspired by Reference 5)
    bar_y = Inches(5.45)
    bar_h = Inches(1.5)
    stack_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), bar_y, Inches(11.933), bar_h)
    stack_box.fill.solid()
    stack_box.fill.fore_color.rgb = WHITE
    stack_box.line.color.rgb = BORDER_LIGHT
    stack_box.line.width = Pt(1.5)
    stack_box.adjustments[0] = 0.04

    # Left side: Key Guarantee
    tb_g = slide.shapes.add_textbox(Inches(0.9), bar_y + Inches(0.15), Inches(5.5), Inches(1.2))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    p_g1 = tf_g.paragraphs[0]
    r_g1 = p_g1.add_run()
    r_g1.text = "🎯 Core Benefit to AICTE & Colleges:"
    r_g1.font.name = "Calibri"
    r_g1.font.size = Pt(11)
    r_g1.font.bold = True
    r_g1.font.color.rgb = DARK_TEXT

    p_g2 = tf_g.add_paragraph()
    p_g2.space_before = Pt(3)
    r_g2 = p_g2.add_run()
    r_g2.text = "Replaces 6 months of postal delay with under 7 working days turnaround. Eliminates duplicate or photoshopped receipts with zero manual data entry burden on officers."
    r_g2.font.name = "Calibri"
    r_g2.font.size = Pt(9.5)
    r_g2.font.color.rgb = BODY_TEXT

    # Right side: Simple Tech Stack chips
    tb_st = slide.shapes.add_textbox(Inches(6.8), bar_y + Inches(0.15), Inches(5.5), Inches(0.3))
    tf_st = tb_st.text_frame
    p_st = tf_st.paragraphs[0]
    r_st = p_st.add_run()
    r_st.text = "Built With Production-Grade Open Technologies:"
    r_st.font.name = "Calibri"
    r_st.font.size = Pt(10)
    r_st.font.bold = True
    r_st.font.color.rgb = MUTED_TEXT

    chips = ["Python / FastAPI", "PaddleOCR AI", "PostgreSQL 16", "Redis 7 Queues", "React 18 Dashboard", "Aadhaar e-Sign"]
    for c_idx, chip_text in enumerate(chips):
        row = c_idx // 3
        col = c_idx % 3
        c_x = Inches(6.8) + col * Inches(1.85)
        c_y = bar_y + Inches(0.5) + row * Inches(0.42)
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, Inches(1.75), Inches(0.35))
        chip.fill.solid()
        chip.fill.fore_color.rgb = CANVAS_BG
        chip.line.color.rgb = BORDER_LIGHT
        chip.line.width = Pt(1)
        chip.adjustments[0] = 0.3
        tf_chip = chip.text_frame
        p_chip = tf_chip.paragraphs[0]
        p_chip.alignment = PP_ALIGN.CENTER
        r_chip = p_chip.add_run()
        r_chip.text = chip_text
        r_chip.font.name = "Calibri"
        r_chip.font.size = Pt(8.5)
        r_chip.font.bold = True
        r_chip.font.color.rgb = DARK_TEXT


# ==============================================================================
# SLIDE 2: 3-PILLAR PROBLEM vs SOLUTION vs GAME-CHANGER (Inspired by Reference 4)
# Friendly Lilac, Sky Blue, and Mint pillars with corner icons and bold punchlines
# ==============================================================================
def build_slide_problem_solution_gamechanger(prs):
    slide = create_slide(prs)
    add_header(slide,
               "Challenges, Smart Solution & The Game-Changer",
               "Strategic Value Proposition",
               "How our software transforms a 30-year paper bottleneck into automated, transparent national governance.")

    pillar_w = Inches(3.7)
    pillar_h = Inches(5.4)
    pillar_y = Inches(1.6)

    # 1. Pillar 1: Challenges in Traditional FDR Management (Lilac)
    p1_left = Inches(0.7)
    box1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p1_left, pillar_y, pillar_w, pillar_h)
    box1.fill.solid()
    box1.fill.fore_color.rgb = LILAC_BG
    box1.line.color.rgb = LILAC_BORDER
    box1.line.width = Pt(2)
    box1.adjustments[0] = 0.05

    # Top pill
    pill1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p1_left + Inches(0.2), pillar_y + Inches(0.25), Inches(2.6), Inches(0.55))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = WHITE
    pill1.line.color.rgb = LILAC_BORDER
    pill1.line.width = Pt(1.5)
    pill1.adjustments[0] = 0.3
    tf_p1 = pill1.text_frame
    p_p1 = tf_p1.paragraphs[0]
    p_p1.alignment = PP_ALIGN.CENTER
    r_p1 = p_p1.add_run()
    r_p1.text = "Challenges in\nOld Paper Process"
    r_p1.font.name = "Calibri"
    r_p1.font.size = Pt(11)
    r_p1.font.bold = True
    r_p1.font.color.rgb = DARK_TEXT

    # Icon circle
    circ1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, p1_left + pillar_w - Inches(0.85), pillar_y + Inches(0.25), Inches(0.6), Inches(0.6))
    circ1.fill.solid()
    circ1.fill.fore_color.rgb = WHITE
    circ1.line.color.rgb = LILAC_BORDER
    circ1.line.width = Pt(1.5)
    tf_c1 = circ1.text_frame
    p_c1 = tf_c1.paragraphs[0]
    p_c1.alignment = PP_ALIGN.CENTER
    r_c1 = p_c1.add_run()
    r_c1.text = "⚠️"
    r_c1.font.size = Pt(14)

    # Bullets for Pillar 1
    tb_b1 = slide.shapes.add_textbox(p1_left + Inches(0.2), pillar_y + Inches(1.1), pillar_w - Inches(0.4), Inches(4.0))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True

    b1_items = [
        ("Physical Paper Silos:", True, " Lakhs of old physical receipts locked in almirahs across 10 Regional Offices. Searching one receipt takes months."),
        ("Photoshop & Fake Receipts:", True, " Colleges can easily edit amounts or deposit dates on computer printouts without human officers noticing."),
        ("Silent Expiry Rollover:", True, " FDRs mature unnoticed and get rolled over by banks into zero-interest accounts, risking college security deposits."),
        ("180-Day Refund Delay:", True, " Genuine colleges wait 6+ months for physical verification letters to travel back and forth by courier.")
    ]
    for i, (b_title, is_b, b_desc) in enumerate(b1_items):
        p = tf_b1.paragraphs[0] if i == 0 else tf_b1.add_paragraph()
        p.space_after = Pt(10)
        r_dot = p.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Calibri"
        r_dot.font.bold = True
        r_dot.font.color.rgb = LILAC_ACCENT
        r_head = p.add_run()
        r_head.text = b_title
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(10)
        r_head.font.bold = True
        r_head.font.color.rgb = DARK_TEXT
        r_tail = p.add_run()
        r_tail.text = b_desc
        r_tail.font.name = "Calibri"
        r_tail.font.size = Pt(9.5)
        r_tail.font.color.rgb = BODY_TEXT

    # Arrow 1 to 2
    arrow1 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, p1_left + pillar_w + Inches(0.08), pillar_y + Inches(2.5), Inches(0.24), Inches(0.35))
    arrow1.fill.solid()
    arrow1.fill.fore_color.rgb = DARK_TEXT
    arrow1.line.fill.background()

    # 2. Pillar 2: Our Smart Digital Solution (Sky Blue)
    p2_left = Inches(4.8)
    box2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p2_left, pillar_y, pillar_w, pillar_h)
    box2.fill.solid()
    box2.fill.fore_color.rgb = SKY_BG
    box2.line.color.rgb = SKY_BORDER
    box2.line.width = Pt(2)
    box2.adjustments[0] = 0.05

    pill2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p2_left + Inches(0.2), pillar_y + Inches(0.25), Inches(2.6), Inches(0.55))
    pill2.fill.solid()
    pill2.fill.fore_color.rgb = WHITE
    pill2.line.color.rgb = SKY_BORDER
    pill2.line.width = Pt(1.5)
    pill2.adjustments[0] = 0.3
    tf_p2 = pill2.text_frame
    p_p2 = tf_p2.paragraphs[0]
    p_p2.alignment = PP_ALIGN.CENTER
    r_p2 = p_p2.add_run()
    r_p2.text = "Our Smart\nAICTE Solution"
    r_p2.font.name = "Calibri"
    r_p2.font.size = Pt(11)
    r_p2.font.bold = True
    r_p2.font.color.rgb = DARK_TEXT

    circ2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, p2_left + pillar_w - Inches(0.85), pillar_y + Inches(0.25), Inches(0.6), Inches(0.6))
    circ2.fill.solid()
    circ2.fill.fore_color.rgb = WHITE
    circ2.line.color.rgb = SKY_BORDER
    circ2.line.width = Pt(1.5)
    tf_c2 = circ2.text_frame
    p_c2 = tf_c2.paragraphs[0]
    p_c2.alignment = PP_ALIGN.CENTER
    r_c2 = p_c2.add_run()
    r_c2.text = "💡"
    r_c2.font.size = Pt(14)

    tb_b2 = slide.shapes.add_textbox(p2_left + Inches(0.2), pillar_y + Inches(1.1), pillar_w - Inches(0.4), Inches(4.0))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True

    b2_items = [
        ("AI Key-Value Reading:", True, " PaddleOCR reads FDR Number, Principal Amount, IFSC & Expiry in 2 seconds without manual typing."),
        ("Photoshop & Tamper Shield:", True, " Error Level Analysis (ELA) detects edited fonts, modified numbers, or Canva fake receipts instantly."),
        ("Tri-Modal Bank Gateway:", True, " Works for ALL banks: Direct CBS API for Tier-1 banks, and a simple 2FA OTP Magic Link for rural co-op branches."),
        ("Autonomous SLA Engine:", True, " Daily chronometer bot sends proactive alerts on WhatsApp & email so files never get stuck.")
    ]
    for i, (b_title, is_b, b_desc) in enumerate(b2_items):
        p = tf_b2.paragraphs[0] if i == 0 else tf_b2.add_paragraph()
        p.space_after = Pt(10)
        r_dot = p.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Calibri"
        r_dot.font.bold = True
        r_dot.font.color.rgb = SKY_ACCENT
        r_head = p.add_run()
        r_head.text = b_title
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(10)
        r_head.font.bold = True
        r_head.font.color.rgb = DARK_TEXT
        r_tail = p.add_run()
        r_tail.text = b_desc
        r_tail.font.name = "Calibri"
        r_tail.font.size = Pt(9.5)
        r_tail.font.color.rgb = BODY_TEXT

    # Arrow 2 to 3
    arrow2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, p2_left + pillar_w + Inches(0.08), pillar_y + Inches(2.5), Inches(0.24), Inches(0.35))
    arrow2.fill.solid()
    arrow2.fill.fore_color.rgb = DARK_TEXT
    arrow2.line.fill.background()

    # 3. Pillar 3: The Game-Changer Impact (Mint Green)
    p3_left = Inches(8.9)
    box3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p3_left, pillar_y, pillar_w, pillar_h)
    box3.fill.solid()
    box3.fill.fore_color.rgb = MINT_BG
    box3.line.color.rgb = MINT_BORDER
    box3.line.width = Pt(2)
    box3.adjustments[0] = 0.05

    pill3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p3_left + Inches(0.2), pillar_y + Inches(0.25), Inches(2.6), Inches(0.55))
    pill3.fill.solid()
    pill3.fill.fore_color.rgb = WHITE
    pill3.line.color.rgb = MINT_BORDER
    pill3.line.width = Pt(1.5)
    pill3.adjustments[0] = 0.3
    tf_p3 = pill3.text_frame
    p_p3 = tf_p3.paragraphs[0]
    p_p3.alignment = PP_ALIGN.CENTER
    r_p3 = p_p3.add_run()
    r_p3.text = "The Game-Changer\nImpact"
    r_p3.font.name = "Calibri"
    r_p3.font.size = Pt(11)
    r_p3.font.bold = True
    r_p3.font.color.rgb = DARK_TEXT

    circ3 = slide.shapes.add_shape(MSO_SHAPE.OVAL, p3_left + pillar_w - Inches(0.85), pillar_y + Inches(0.25), Inches(0.6), Inches(0.6))
    circ3.fill.solid()
    circ3.fill.fore_color.rgb = WHITE
    circ3.line.color.rgb = MINT_BORDER
    circ3.line.width = Pt(1.5)
    tf_c3 = circ3.text_frame
    p_c3 = tf_c3.paragraphs[0]
    p_c3.alignment = PP_ALIGN.CENTER
    r_c3 = p_c3.add_run()
    r_c3.text = "🚀"
    r_c3.font.size = Pt(14)

    tb_b3 = slide.shapes.add_textbox(p3_left + Inches(0.2), pillar_y + Inches(1.1), pillar_w - Inches(0.4), Inches(4.0))
    tf_b3 = tb_b3.text_frame
    tf_b3.word_wrap = True

    b3_items = [
        ("Zero Physical Couriers:", True, " Saves 50,000+ registered postal letters annually. 100% digital paperless audit trail."),
        ("Under 7-Day Refund SLA:", True, " Genuine institutions get deposits released quickly instead of waiting 6 months across bureaucracy."),
        ("Impossible to Tamper:", True, " Cryptographic hash ledger prevents even database admins from quietly editing records."),
        ("100% Nationwide Bank Reach:", True, " Nariman Point SBI branch ho ya rural Bihar Gramin bank, every branch manager can verify with 1 tap.")
    ]
    for i, (b_title, is_b, b_desc) in enumerate(b3_items):
        p = tf_b3.paragraphs[0] if i == 0 else tf_b3.add_paragraph()
        p.space_after = Pt(10)
        r_dot = p.add_run()
        r_dot.text = "• "
        r_dot.font.name = "Calibri"
        r_dot.font.bold = True
        r_dot.font.color.rgb = MINT_ACCENT
        r_head = p.add_run()
        r_head.text = b_title
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(10)
        r_head.font.bold = True
        r_head.font.color.rgb = DARK_TEXT
        r_tail = p.add_run()
        r_tail.text = b_desc
        r_tail.font.name = "Calibri"
        r_tail.font.size = Pt(9.5)
        r_tail.font.color.rgb = BODY_TEXT


# ==============================================================================
# SLIDE 3: POTENTIAL IMPACT vs SOLUTION BENEFIT (Inspired by Reference 2)
# Executive 2-Column Split: Who Benefits vs Measurable KPIs
# ==============================================================================
def build_slide_impact_vs_benefits(prs):
    slide = create_slide(prs)
    add_header(slide,
               "Potential Impact & Quantified Benefits of the Solution",
               "Executive Impact & Stakeholder Value",
               "Clear operational gains for AICTE Officers, Technical Colleges, and Banking Partners.")

    col_w = Inches(5.8)
    col_h = Inches(5.4)
    top_y = Inches(1.6)

    # Left Column: Potential Impact on Key Stakeholders
    c1_left = Inches(0.7)
    box_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c1_left, top_y, col_w, col_h)
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = WHITE
    box_l.line.color.rgb = BORDER_LIGHT
    box_l.line.width = Pt(1.5)
    box_l.adjustments[0] = 0.04

    # Header Left
    tb_lh = slide.shapes.add_textbox(c1_left + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.45))
    tf_lh = tb_lh.text_frame
    p_lh = tf_lh.paragraphs[0]
    r_lh = p_lh.add_run()
    r_lh.text = "Potential Impact on Stakeholders"
    r_lh.font.name = "Calibri"
    r_lh.font.size = Pt(16)
    r_lh.font.bold = True
    r_lh.font.color.rgb = DARK_TEXT

    # 3 Stakeholder groups with icons
    stakeholders = [
        ("🎓", "Technical Institutions & Colleges:",
         [("Eliminates courier tracking anxiety:", True), (" Real-time dashboard shows exact verification status 24/7.", False),
          ("\n• ", False), ("Proactive renewal alerts:", True), (" Stops unexpected deposit forfeiture before statutory deadlines.", False)]),

        ("👔", "AICTE Regional Officers & Scrutiny Clerks:",
         [("90% verification time reduction:", True), (" AI pre-fills 80% of data; officers only verify highlighted discrepancies.", False),
          ("\n• ", False), ("Zero physical file hunting:", True), (" Instant search across 30 years of digital records.", False)]),

        ("🏛️", "Regulation Bureau & Vigilance Directorate:",
         [("Zero Financial Fraud Risk:", True), (" Stops fake/photoshopped FDRs from receiving approvals.", False),
          ("\n• ", False), ("Strict Non-Repudiation:", True), (" Every action sealed with Aadhaar e-Sign & cryptographic hash ledger.", False)])
    ]

    s_y = top_y + Inches(0.85)
    for icon, s_title, s_bullets in stakeholders:
        # Icon
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, c1_left + Inches(0.3), s_y, Inches(0.55), Inches(0.55))
        circ.fill.solid()
        circ.fill.fore_color.rgb = LILAC_BG
        circ.line.color.rgb = LILAC_BORDER
        circ.line.width = Pt(1)
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = p_c.add_run()
        r_c.text = icon
        r_c.font.size = Pt(13)

        # Title & bullets
        tb_s = slide.shapes.add_textbox(c1_left + Inches(1.0), s_y - Inches(0.05), col_w - Inches(1.2), Inches(1.2))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_st = tf_s.paragraphs[0]
        r_st = p_st.add_run()
        r_st.text = s_title
        r_st.font.name = "Calibri"
        r_st.font.size = Pt(11)
        r_st.font.bold = True
        r_st.font.color.rgb = DARK_TEXT

        p_sb = tf_s.add_paragraph()
        p_sb.space_before = Pt(3)
        for part, is_b in s_bullets:
            r_sb = p_sb.add_run()
            r_sb.text = part
            r_sb.font.name = "Calibri"
            r_sb.font.size = Pt(9.5)
            r_sb.font.bold = is_b
            r_sb.font.color.rgb = DARK_TEXT if is_b else BODY_TEXT

        s_y += Inches(1.4)

    # Right Column: Benefits of the Solution
    c2_left = Inches(6.83)
    box_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c2_left, top_y, col_w, col_h)
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = WHITE
    box_r.line.color.rgb = BORDER_LIGHT
    box_r.line.width = Pt(1.5)
    box_r.adjustments[0] = 0.04

    tb_rh = slide.shapes.add_textbox(c2_left + Inches(0.3), top_y + Inches(0.25), col_w - Inches(0.6), Inches(0.45))
    tf_rh = tb_rh.text_frame
    p_rh = tf_rh.paragraphs[0]
    r_rh = p_rh.add_run()
    r_rh.text = "Measurable Benefits of the Solution"
    r_rh.font.name = "Calibri"
    r_rh.font.size = Pt(16)
    r_rh.font.bold = True
    r_rh.font.color.rgb = DARK_TEXT

    benefits = [
        ("⚡", "Speed & Efficiency Gains:",
         [("Refund cycle compressed", True), (" from 180 days down to under 7 working days.", False),
          ("\n• ", False), ("2-second AI reading", True), (" replaces 45 minutes of manual document typing.", False)]),

        ("🛡️", "Fraud Immunity & Security:",
         [("100% Tamper Detection:", True), (" Identifies photoshopped deposit receipts before human review.", False),
          ("\n• ", False), ("Dual-Truth Segregation:", True), (" Institutional claim is independently verified with the bank ledger.", False)]),

        ("📈", "Governance & Accountability:",
         [("Zero-Lapse SLA Ladder:", True), (" Stalled cases auto-escalate from clerk to Regional Director.", False),
          ("\n• ", False), ("DPDP Act & IT Act Compliant:", True), (" Legally binding Aadhaar e-Sign with encrypted QR codes.", False)])
    ]

    r_y = top_y + Inches(0.85)
    for icon, b_title, b_bullets in benefits:
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, c2_left + Inches(0.3), r_y, Inches(0.55), Inches(0.55))
        circ.fill.solid()
        circ.fill.fore_color.rgb = MINT_BG
        circ.line.color.rgb = MINT_BORDER
        circ.line.width = Pt(1)
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        r_c = p_c.add_run()
        r_c.text = icon
        r_c.font.size = Pt(13)

        tb_b = slide.shapes.add_textbox(c2_left + Inches(1.0), r_y - Inches(0.05), col_w - Inches(1.2), Inches(1.2))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_bt = tf_b.paragraphs[0]
        r_bt = p_bt.add_run()
        r_bt.text = b_title
        r_bt.font.name = "Calibri"
        r_bt.font.size = Pt(11)
        r_bt.font.bold = True
        r_bt.font.color.rgb = DARK_TEXT

        p_bb = tf_b.add_paragraph()
        p_bb.space_before = Pt(3)
        for part, is_b in b_bullets:
            r_bb = p_bb.add_run()
            r_bb.text = part
            r_bb.font.name = "Calibri"
            r_bb.font.size = Pt(9.5)
            r_bb.font.bold = is_b
            r_bb.font.color.rgb = DARK_TEXT if is_b else BODY_TEXT

        r_y += Inches(1.4)


def main():
    prs = new_deck()
    print("Generating Slide 1: 5-Step Visual Technical Approach (Inspired by Reference 5)...")
    build_slide_technical_approach(prs)

    print("Generating Slide 2: 3-Pillar Problem vs Solution vs Impact (Inspired by Reference 4)...")
    build_slide_problem_solution_gamechanger(prs)

    print("Generating Slide 3: Potential Impact vs Quantified Benefits (Inspired by Reference 2)...")
    build_slide_impact_vs_benefits(prs)

    output_path = "AICTE_Innovative_Ideas_Diagrams_Editable.pptx"
    prs.save(output_path)
    print(f"Successfully generated new PPT in: {output_path}")

if __name__ == "__main__":
    main()
