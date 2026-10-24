import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.app.config import DOCS_DIR, NOC_DIR

def generate_fdr_sample_image(
    filename: str,
    fdr_number: str,
    bank_name: str,
    branch_name: str,
    ifsc_code: str,
    institution_name: str,
    deposit_amount: float,
    issue_date: str,
    maturity_date: str,
    is_lien_marked: bool = True
) -> str:
    """
    Generates a realistic graphical Fixed Deposit Receipt (FDR) image.
    Saved to disk for instant viewing, OCR extraction, and visual vault inspection.
    """
    filepath = DOCS_DIR / filename
    width, height = 1000, 650

    img = Image.new("RGB", (width, height), color=(253, 252, 248))
    draw = ImageDraw.Draw(img)

    # Decorative Border
    draw.rectangle([15, 15, width - 15, height - 15], outline=(15, 44, 89), width=4)
    draw.rectangle([22, 22, width - 22, height - 22], outline=(180, 150, 90), width=1)

    # Bank Header Bar
    draw.rectangle([25, 25, width - 25, 110], fill=(15, 44, 89))
    draw.text((45, 40), bank_name.upper(), fill=(255, 255, 255))
    draw.text((45, 75), f"Branch: {branch_name} | IFSC: {ifsc_code}", fill=(200, 220, 245))
    draw.text((width - 320, 55), "FIXED DEPOSIT RECEIPT", fill=(240, 200, 100))

    # Watermark / Background faint crest
    draw.text((320, 260), "AICTE JOINT COLLATERAL", fill=(245, 240, 235))

    # Instrument Metadata Grid
    y_pos = 140
    line_h = 36

    items = [
        ("FDR Receipt No:", fdr_number, "Deposit Date:", issue_date),
        ("Depositor Name:", institution_name, "Maturity Date:", maturity_date),
        ("Principal Sum:", f"INR {deposit_amount:,.2f}", "Interest Rate:", "7.25% p.a. (Cumulative)"),
        ("Joint Account With:", "Member Secretary, AICTE, New Delhi", "Tenure:", "8 Years (96 Months)"),
    ]

    for label1, val1, label2, val2 in items:
        # Col 1
        draw.text((50, y_pos), label1, fill=(80, 80, 80))
        draw.text((220, y_pos), val1, fill=(10, 20, 40))

        # Col 2
        draw.text((550, y_pos), label2, fill=(80, 80, 80))
        draw.text((700, y_pos), val2, fill=(10, 20, 40))

        # Divider line
        draw.line([50, y_pos + line_h - 6, width - 50, y_pos + line_h - 6], fill=(230, 230, 230), width=1)
        y_pos += line_h

    # Statutory Lien Endorsement Stamp (Red ink box)
    if is_lien_marked:
        stamp_box = [60, 310, 520, 410]
        draw.rectangle(stamp_box, outline=(190, 30, 30), width=3)
        draw.text((75, 320), "OFFICIALLY LIEN MARKED", fill=(190, 30, 30))
        draw.text((75, 345), "In favour of: MEMBER SECRETARY, AICTE, NEW DELHI", fill=(180, 20, 20))
        draw.text((75, 370), "No premature withdrawal or loan allowed without AICTE NOC.", fill=(150, 20, 20))
        draw.text((75, 390), f"Lien Ref: AICTE/REG/FDR-LIEN/{fdr_number[-6:]}", fill=(100, 20, 20))
    else:
        stamp_box = [60, 310, 520, 410]
        draw.rectangle(stamp_box, outline=(100, 100, 100), width=1)
        draw.text((75, 345), "STANDARD FIXED DEPOSIT (NO REGULATORY LIEN NOTED)", fill=(120, 120, 120))

    # Bank Seal and Signatures
    draw.rectangle([600, 310, 930, 410], outline=(180, 180, 180), width=1)
    draw.text((620, 320), f"FOR {bank_name.upper()}", fill=(60, 60, 60))
    draw.text((620, 380), "Authorized Branch Signatory", fill=(100, 100, 100))
    draw.text((790, 380), "Branch Manager Seal", fill=(100, 100, 100))

    # Security Footnote
    draw.rectangle([25, height - 70, width - 25, height - 25], fill=(240, 244, 250))
    draw.text((45, height - 58), "SECURE REGULATORY REPOSITORY RECORD • VERIFIABLE ON AICTE FDR LIFECYCLE PORTAL", fill=(70, 90, 120))
    draw.text((width - 320, height - 58), f"SHA-256 PINNED INSTRUMENT", fill=(100, 120, 140))

    img.save(filepath, "PNG")
    return str(filepath)

def generate_release_noc_pdf(
    release_req_id: str,
    fdr_number: str,
    institution_name: str,
    institution_pid: str,
    bank_name: str,
    amount: float,
    authorized_by: str,
    digital_signature_hash: str
) -> str:
    """
    Generates an official AICTE No Objection Certificate (NOC) and Discharge Letter (PDF).
    """
    pdf_filename = f"AICTE_NOC_RELEASE_{fdr_number}.pdf"
    filepath = NOC_DIR / pdf_filename

    doc = SimpleDocTemplate(str(filepath), pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=1, # Center
        textColor=colors.HexColor('#0F2C59')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#4A5568')
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=16,
        textColor=colors.HexColor('#1A202C')
    )
    sig_style = ParagraphStyle(
        'DocSig',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2D3748')
    )

    elements = []

    elements.append(Paragraph("<b>ALL INDIA COUNCIL FOR TECHNICAL EDUCATION</b>", title_style))
    elements.append(Paragraph("A Statutory Body Under Ministry of Education, Govt. of India<br/>Nelson Mandela Marg, Vasant Kunj, New Delhi - 110070", subtitle_style))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("<b>REGULATION BUREAU & FINANCIAL SECURITY DEPOSIT DIVISION</b>", subtitle_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Ref No:</b> AICTE/REG/FDR-REL/{fdr_number}/2026<br/><b>Date:</b> {str(Path.cwd())[:0]}2026-10-24", body_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b><u>SUBJECT: DISCHARGE OF LIEN & NO OBJECTION CERTIFICATE (NOC) FOR RELEASE OF FIXED DEPOSIT RECEIPT</u></b>", title_style))
    elements.append(Spacer(1, 15))

    p1 = (f"To,<br/><b>The Branch Manager,</b><br/>{bank_name}<br/><br/>"
          f"Sir/Madam,<br/><br/>"
          f"With reference to the statutory security deposit maintained under joint name / lien in favor of the "
          f"Member Secretary, AICTE by <b>{institution_name}</b> (AICTE PID: <b>{institution_pid}</b>), it is hereby "
          f"certified that the Competent Authority has scrutinized and approved the formal discharge of regulatory lien.")
    elements.append(Paragraph(p1, body_style))
    elements.append(Spacer(1, 12))

    # Table of particulars
    data = [
        ["AICTE Permanent Institute ID", institution_pid],
        ["Institution Name", institution_name],
        ["FDR Receipt Number", fdr_number],
        ["Issuing Bank & Branch", bank_name],
        ["Principal Deposit Amount", f"INR {amount:,.2f}"],
        ["Status of Statutory Tenure", "COMPLETED (8-10 Academic Years Solvency Norms Fulfilled)"],
        ["Scrutiny Recommendation", "Approved by Regulation Bureau Desk"],
        ["Regional Office Clearance", "Recommended by Regional Director"]
    ]
    t = Table(data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2D3748')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    p2 = ("The bank is hereby authorized to release and credit the proceeds of the aforementioned Fixed Deposit "
          "along with accrued interest to the sole operating bank account of the institution, without further reference to AICTE.")
    elements.append(Paragraph(p2, body_style))
    elements.append(Spacer(1, 20))

    sig_block = (f"<b>Digitally Signed & Sealed:</b><br/>"
                 f"<b>{authorized_by}</b><br/>"
                 f"Member Secretary / Bureau Head, AICTE<br/>"
                 f"<b>Cryptographic DSC Signature Hash:</b><br/>"
                 f"<font color='#0F2C59' face='Courier'>{digital_signature_hash}</font><br/>"
                 f"<b>Verification URI:</b> https://fdr.aicte-india.org/verify/noc/{fdr_number}")
    elements.append(Paragraph(sig_block, sig_style))

    doc.build(elements)
    return str(filepath)
