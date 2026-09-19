import os
import sys
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

base_dir = os.path.dirname(os.path.abspath(__file__))
cv_pdf_path = os.path.join(base_dir, 'CV_AI_ProductManage_EN.pdf')
report_temp_path = os.path.join(base_dir, 'report_body_temp.pdf')
final_pdf_path = os.path.join(base_dir, 'mystorage_intern_assignment.pdf')

doc = SimpleDocTemplate(
    report_temp_path,
    pagesize=letter,
    rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom Palette (MyStorage Brand: Blue #0275BC, Dark #0F172A, Accent #0369A1, Light #F8FAFC)
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor('#0275BC'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#0275BC'),
    spaceBefore=12,
    spaceAfter=6
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor('#0369A1'),
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#1E293B'),
    spaceAfter=5
)

bullet_style = ParagraphStyle(
    'BulletDark',
    parent=body_style,
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=3
)

code_style = ParagraphStyle(
    'CodeBlock',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#0F172A'),
    backColor=colors.HexColor('#F1F5F9'),
    borderColor=colors.HexColor('#CBD5E1'),
    borderWidth=1,
    borderPadding=5,
    spaceAfter=6
)

story = []

# Header Banner
story.append(Paragraph("MYSTORAGE PRODUCT ENGINEERING INTERN ASSIGNMENT", title_style))
story.append(Paragraph("Candidate Audit Report, STOW 2.0 Prototype Guide & AI Tool Reflection", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0275BC'), spaceAfter=10))

# Candidate Profile Summary Box
candidate_meta = [
    [
        Paragraph("<b>Applicant Name:</b> NGUYỄN NHƯ KHẢI", body_style),
        Paragraph("<b>Target Role:</b> Product Engineering Intern (AI-Native)", body_style)
    ],
    [
        Paragraph("<b>Email:</b> <a href='mailto:khai0335814880@gmail.com'><u>khai0335814880@gmail.com</u></a>", body_style),
        Paragraph("<b>Phone / WhatsApp:</b> 0335814880", body_style)
    ],
    [
        Paragraph("<b>LinkedIn:</b> <a href='https://www.linkedin.com/in/kh%E1%BA%A3i-nguy%E1%BB%85n-nh%C6%B0'><u>linkedin.com/in/khải-nguyễn-như</u></a>", body_style),
        Paragraph("<b>GitHub Profile:</b> <a href='https://github.com/khai0335814880-create'><u>github.com/khai0335814880-create</u></a>", body_style)
    ],
    [
        Paragraph("<b>Personal Portfolio:</b> <a href='https://figma-portfolio-drab.vercel.app/'><u>figma-portfolio-drab.vercel.app</u></a>", body_style),
        Paragraph("<b>Prototype Repository:</b> <a href='https://github.com/khai0335814880-create/mystorage-intern-challenge'><u>GitHub Source Code</u></a>", body_style)
    ],
    [
        Paragraph("<b>Live Prototype URL:</b> <a href='https://mystorage-intern-challenge-e507g80yp.vercel.app/'><u>mystorage-intern-challenge-e507g80yp.vercel.app</u></a>", body_style),
        Paragraph("<b>Canonical Spec:</b> <a href='https://mystorage.vn/llms.txt'><u>https://mystorage.vn/llms.txt</u></a>", body_style)
    ]
]

t_meta = Table(candidate_meta, colWidths=[270, 270])
t_meta.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story.append(t_meta)
story.append(Spacer(1, 10))

# SECTION 1: SYSTEM AUDIT REPORT
story.append(Paragraph("1. System Audit Report (stow.mystorage.vn)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=6))

# Finding 1
story.append(Paragraph("Finding 1 [HIGH SEVERITY]: AI Prompt Knowledge Desynchronization vs Canonical llms.txt Ground Truth", h2_style))
story.append(Paragraph("<b>What Happened:</b> When querying stow.mystorage.vn for starting unit prices or basic insurance coverage limits, the AI assistant generates inconsistent quotes (e.g. 500,000 VND/month or 600,000 VND/month) and fails to state the exact Basic Protection limit (500,000 VND/CBM up to max 10,000,000 VND).", body_style))
story.append(Paragraph("<b>Steps to Reproduce:</b>", body_style))
story.append(Paragraph("1. Open <a href='https://stow.mystorage.vn/'><u>stow.mystorage.vn</u></a> and start a new chat conversation.", bullet_style))
story.append(Paragraph("2. Ask: 'Kho máy lạnh nhỏ nhất giá bao nhiêu 1 tháng và chính sách bảo hiểm tối đa bao nhiêu?'", bullet_style))
story.append(Paragraph("3. Compare generated response against canonical <a href='https://mystorage.vn/llms.txt'><u>llms.txt</u></a> (Air-conditioned/furniture from 559,000 VND/mo, Basic Protection free up to 10M VND).", bullet_style))
story.append(Paragraph("<b>Impact to Customer & Business:</b> Price discrepancies create checkout friction on booking.mystorage.vn, harming customer trust and lead conversion.", body_style))
story.append(Paragraph("<b>Proposed Fix:</b> Dynamic server-side context injection of llms.txt into STOW's system prompt and enforcing tool-based fact verification.", body_style))
story.append(Spacer(1, 4))

# Finding 2
story.append(Paragraph("Finding 2 [MEDIUM SEVERITY]: Unhandled UX Breakdown & Exception for Oversized Items (> 2.0m Height)", h2_style))
story.append(Paragraph("<b>What Happened:</b> Adding items exceeding 2000mm in height (e.g. 2.4m wardrobes) in Item Manager triggers a 'CannotStoreMaxHeight' warning that blocks bin recommendations without offering a fallback route.", body_style))
story.append(Paragraph("<b>Steps to Reproduce:</b>", body_style))
story.append(Paragraph("1. In stow.mystorage.vn, add a custom item 'Custom Wardrobe' (W: 1200mm, D: 600mm, H: 2400mm).", bullet_style))
story.append(Paragraph("2. Click 'Estimate Storage Solution'. Observe system error modal / infinite calculation state.", bullet_style))
story.append(Paragraph("<b>Impact to Customer & Business:</b> High-value customers storing large furniture are turned away instead of being redirected to Full Service Storage.", body_style))
story.append(Paragraph("<b>Proposed Fix:</b> Implement automatic fallback routing to MyStorage's Nhon Trach 3 (Dong Nai) Full-Service Shelf-Space Warehouse with pickup transport.", body_style))
story.append(Spacer(1, 4))

# Finding 3
story.append(Paragraph("Finding 3 [MEDIUM SEVERITY]: Locale Context Disconnect Across Chat, Voice Mode, and Item Tray", h2_style))
story.append(Paragraph("<b>What Happened:</b> Switching language from Vietnamese to English updates static labels but leaves active chat session instructions and item tray summary strings in the previous locale.", body_style))
story.append(Paragraph("<b>Steps to Reproduce:</b> Switch header language to English mid-session; observe item tray headers ('Đã lưu 0 đồ vật') and Live Voice responses remain in Vietnamese.", body_style))
story.append(Paragraph("<b>Impact to Customer & Business:</b> Confusing UX for international expat customers in Ho Chi Minh City.", body_style))
story.append(Paragraph("<b>Proposed Fix:</b> Bind i18n dictionary reactively across session parameters and item list state.", body_style))
story.append(Spacer(1, 10))

# SECTION 2: PROTOTYPE ACCESS & TESTING GUIDE
story.append(Paragraph("2. STOW 2.0 Prototype Solution & How to Review / Test", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=6))

story.append(Paragraph("To address Findings 1, 2, and 3, a working Angular prototype **STOW 2.0 AI Sales Assistant & Size Estimator** was engineered in <b>src/app/stow-assistant/</b>.", body_style))
story.append(Paragraph("<b>How Reviewers Can Access & Test the Prototype:</b>", h2_style))
story.append(Paragraph("• <b>Option A (Live Deployed Web Application):</b> Visit <a href='https://mystorage-intern-challenge-e507g80yp.vercel.app/'><u>https://mystorage-intern-challenge-e507g80yp.vercel.app/</u></a> on any browser or mobile device.", bullet_style))
story.append(Paragraph("• <b>Option B (Source Code Repository):</b> Inspect full source code on GitHub: <a href='https://github.com/khai0335814880-create/mystorage-intern-challenge'><u>khai0335814880-create/mystorage-intern-challenge</u></a>.", bullet_style))
story.append(Paragraph("• <b>Option C (Local Execution Steps):</b>", bullet_style))
story.append(Paragraph("git clone https://github.com/khai0335814880-create/mystorage-intern-challenge.git\ncd mystorage-intern-challenge\nnpm install\nnpm start\n# Open http://localhost:4200/ in your browser", code_style))

story.append(Spacer(1, 4))
story.append(Paragraph("<b>Key Features Demonstrated in Prototype:</b>", body_style))
story.append(Paragraph("1. <b>Ground Truth Sync (Fix 1):</b> Accurately quotes starting price 559,000 VND/mo & free insurance limits (500k/CBM max 10M VND).", bullet_style))
story.append(Paragraph("2. <b>Automatic Oversized Fallback (Fix 2):</b> Detects items > 2.0m height and automatically routes customers to Dong Nai Shelf-Space Warehouse.", bullet_style))
story.append(Paragraph("3. <b>Seamless i18n Locale Sync (Fix 3):</b> Instant Vietnamese/English toggle across chat history, item tray, and system prompts.", bullet_style))

story.append(Spacer(1, 10))

# SECTION 3: AI CODE REFLECTION
story.append(Paragraph("3. AI Code Reflection (Claude Code / Antigravity Review)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=6))

story.append(Paragraph("<b>What the AI Model Generated:</b> Initial scaffolding provided clean UI layouts, but generated legacy Angular template syntax, raw array mutations (`this.items().push()`), and unhandled state exceptions.", body_style))
story.append(Paragraph("<b>What Was Rejected / Rewritten & Why:</b>", body_style))
story.append(Paragraph("• <i>Signal State Immutability:</i> Rewrote raw mutations to `this.items.update(list => [...list, newItem])` for Angular 19 reactive signals.", bullet_style))
story.append(Paragraph("• <i>Oversized Fallback Logic:</i> Replaced silent warning banners with explicit computed signal evaluation (`hasOversizedItems`).", bullet_style))
story.append(Paragraph("• <i>Ground Truth Enforcement:</i> Overrode default LLM price estimates with exact rules derived from mystorage.vn/llms.txt.", bullet_style))

story.append(Spacer(1, 10))

# SECTION 4: NOTE ON AI TOOL USE (REQUIRED < 300 WORDS)
story.append(Paragraph("4. Brief Note on AI Tool Usage (< 300 words)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=6))
story.append(Paragraph("<i>Question: What's the last thing you built with an AI coding tool, and what did you have to fix yourself?</i>", ParagraphStyle('ItalicHead', parent=body_style, fontName='Helvetica-Oblique', textColor=colors.HexColor('#475569'))))
story.append(Paragraph("The last project I built with an AI coding tool (Antigravity AI) was my interactive Developer Portfolio and the STOW 2.0 AI Assistant prototype for MyStorage. While the AI rapidly scaffolded UI components and PDF generation scripts, I had to fix several critical issues myself: refactoring legacy Angular template syntax, fixing signal array mutation bugs (`this.items().push` vs `.update()`), resolving i18n locale state desync across chat and voice modes, and engineering a custom Python PDF merger script to combine my CV with clickable assignment links into a single PDF under the 4MB limit.", body_style))

# Build temporary report PDF
doc.build(story)
print(f"Generated temporary report PDF: {report_temp_path}")

# Merge CV (Page 1) + Report Body (Page 2+) into final PDF
writer = pypdf.PdfWriter()

# 1. Append CV PDF
if os.path.exists(cv_pdf_path):
    print(f"Appending CV PDF: {cv_pdf_path}")
    writer.append(cv_pdf_path)
else:
    print(f"WARNING: CV PDF not found at {cv_pdf_path}")

# 2. Append Generated Report PDF
if os.path.exists(report_temp_path):
    print(f"Appending Report Body PDF: {report_temp_path}")
    writer.append(report_temp_path)

# Write final single PDF file
with open(final_pdf_path, 'wb') as f_out:
    writer.write(f_out)

# Clean up temp file
if os.path.exists(report_temp_path):
    os.remove(report_temp_path)

final_size = os.path.getsize(final_pdf_path)
final_size_mb = final_size / (1024 * 1024)

print(f"\n==========================================")
print(f"SUCCESSFULLY MERGED FINAL PDF REPORT:")
print(f"File Path: {final_pdf_path}")
print(f"File Size: {final_size} bytes ({final_size_mb:.4f} MB)")
print(f"==========================================\n")
