import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

MEDIA_DIR = r"c:\Users\haren\OneDrive\Desktop\mwtfinalel\user_doc_media"
ROOT_DIR = r"c:\Users\haren\OneDrive\Desktop\mwtfinalel"

def get_media(fname):
    return os.path.join(MEDIA_DIR, fname)

def get_root(fname):
    return os.path.join(ROOT_DIR, fname)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_styled_paragraph(doc, text="", style='Normal', space_after=6, space_before=0, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.5)):
    p = doc.add_paragraph(text, style=style)
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = line_spacing
    if first_line_indent is not None:
        p.paragraph_format.first_line_indent = first_line_indent
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_point(doc, bold_prefix, text, left_indent=Inches(0.5)):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if left_indent is not None:
        p.paragraph_format.left_indent = left_indent
        p.paragraph_format.first_line_indent = Inches(-0.25)
    
    r1 = p.add_run(bold_prefix)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0, 0, 0)

    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_screenshot(doc, img_path, caption, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r = p_cap.add_run(caption)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.italic = True
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)

def format_schema_table(doc, title, headers, rows):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(3)
    p_title.paragraph_format.left_indent = Inches(0.5)
    r = p_title.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, "A0A0A0")

    for col_idx, h_text in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

    for row_idx, r_data in enumerate(rows):
        row = table.rows[row_idx + 1]
        bg_color = "F9F9F9" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=45, bottom=45, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx != 0 else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph()

def format_grid_table(doc, headers, rows):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, "A0A0A0")

    for col_idx, h_text in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

    for row_idx, r_data in enumerate(rows):
        row = table.rows[row_idx + 1]
        bg_color = "F9F9F9" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=45, bottom=45, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_paragraph()

def setup_page_number_footer(section, start_number=1):
    sectPr = section._sectPr
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), str(start_number))
    sectPr.append(pgNumType)

    footer = section.footer
    footer.is_linked_to_previous = False
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    run = f_p.add_run()
    run.font.name = 'Calibri'
    run.font.size = Pt(11)

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

print("Report generator core primitives defined.")

def generate_full_report():
    doc = Document()

    # Section 1: Title / Cover Page
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.different_first_page_header_footer = True

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(30)
    p_title.paragraph_format.space_after = Pt(14)
    r = p_title.add_run("MULTI-EXAM PREPARATION AND RESOURCE EXCHANGE PLATFORM")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(36)
    r = p_course.add_run("23CS54C – MODERN WEB TECHNOLOGIES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True
    r.font.bold = True

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(40)
    r = p_author.add_run("HARENI T                       2403957610422005")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_degree = doc.add_paragraph()
    p_degree.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_degree.paragraph_format.space_before = Pt(16)
    p_degree.paragraph_format.space_after = Pt(24)
    r = p_degree.add_run("In partial fulfillment for the award of the degree\nof\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True
    
    r_deg = p_degree.add_run("BACHELOR OF ENGINEERING\nin\nCOMPUTER SCIENCE AND ENGINEERING")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(12)
    r_deg.font.bold = True

    # Centered College Logo
    logo_path = get_media("image1.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(14)
        p_logo.paragraph_format.space_after = Pt(20)
        p_logo.add_run().add_picture(logo_path, height=Inches(1.5))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(16)
    p_inst.paragraph_format.space_after = Pt(20)
    
    r = p_inst.add_run("NATIONAL ENGINEERING COLLEGE\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    r2 = p_inst.add_run("(An Autonomous Institution affiliated to Anna University, Chennai)\nK.R.NAGAR, KOVILPATTI – 628503\n\nOCTOBER - 2026")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = True

    # -------------------------------------------------------------------------
    # SECTION 2: BONAFIDE CERTIFICATE (PAGE 1) & CONTINUING
    # -------------------------------------------------------------------------
    sec2 = doc.add_section()
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    setup_page_number_footer(sec2, start_number=1)

    # Bonafide Header with College Logo
    if os.path.exists(logo_path):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(10)
        p_logo2.paragraph_format.space_after = Pt(10)
        p_logo2.add_run().add_picture(logo_path, height=Inches(1.2))

    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(8)
    p_c1.paragraph_format.space_after = Pt(4)
    r = p_c1.add_run("NATIONAL ENGINEERING COLLEGE\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    r = p_c1.add_run("(An Autonomous Institution affiliated to Anna University, Chennai)\nK.R.NAGAR, KOVILPATTI – 628503")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    p_bona = doc.add_paragraph()
    p_bona.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bona.paragraph_format.space_before = Pt(32)
    p_bona.paragraph_format.space_after = Pt(24)
    r = p_bona.add_run("BONAFIDE CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.4
    p_cert.paragraph_format.first_line_indent = Inches(0.5)
    p_cert.paragraph_format.space_after = Pt(48)
    r = p_cert.add_run("This is to certify that this project report, “")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    
    r_bold = p_cert.add_run("Multi-Exam Preparation and Resource Exchange Platform")
    r_bold.font.name = 'Times New Roman'
    r_bold.font.size = Pt(12)
    r_bold.font.bold = True

    r_rem = p_cert.add_run("”, is the bonafide work of ")
    r_rem.font.name = 'Times New Roman'
    r_rem.font.size = Pt(12)

    r_stu = p_cert.add_run("HARENI T (2403957610422005)")
    r_stu.font.name = 'Times New Roman'
    r_stu.font.size = Pt(12)
    r_stu.font.bold = True

    r_end = p_cert.add_run(" who carried out the project work under my supervision.")
    r_end.font.name = 'Times New Roman'
    r_end.font.size = Pt(12)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.space_after = Pt(48)
    r = p_guide.add_run("Course Instructor/Guide")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_viva = doc.add_paragraph()
    p_viva.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_viva.paragraph_format.line_spacing = 1.2
    p_viva.paragraph_format.space_after = Pt(40)
    r = p_viva.add_run("Submitted to the 23CS54C – MODERN WEB TECHNOLOGIES Viva-Voce examination held at National Engineering College, K.R.Nagar, Kovilpatti on ___________________")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    t_exam = doc.add_table(rows=1, cols=2)
    t_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_exam, "FFFFFF")
    c_int, c_ext = t_exam.rows[0].cells
    c_int.width = Inches(3.0)
    c_ext.width = Inches(3.0)
    
    p = c_int.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("_____________________\nInternal Examiner")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p = c_ext.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("_____________________\nCo Examiner")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 2: TABLE OF CONTENTS
    # -------------------------------------------------------------------------
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(14)
    p_toc.paragraph_format.space_after = Pt(18)
    r = p_toc.add_run("TABLE OF CONTENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    toc_items = [
        ("1", "INTRODUCTION", "3"),
        ("2", "OBJECTIVES", "4"),
        ("3", "DESCRIPTION", "5"),
        ("4", "CLASS DIAGRAM", "6"),
        ("5", "TABLE STRUCTURES", "7"),
        ("6", "ER DIAGRAM", "13"),
        ("7", "TECH STACK", "14"),
        ("8", "MODULES", "15"),
        ("9", "CONCLUSION", "58"),
        ("10", "REFERENCE", "59"),
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_toc, "D0D0D0")
    
    h1, h2, h3 = t_toc.rows[0].cells
    h1.width = Inches(1.2)
    h2.width = Inches(4.2)
    h3.width = Inches(1.0)
    h1.text = "CH NO"
    h2.text = "TITLE"
    h3.text = "PAGE NO"
    for cell in [h1, h2, h3]:
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cell != h2 else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

    for idx, (ch, title, page) in enumerate(toc_items):
        c1, c2, c3 = t_toc.rows[idx + 1].cells
        c1.text = ch
        c2.text = title
        c3.text = page
        bg = "F9F9F9" if idx % 2 == 1 else "FFFFFF"
        for cell in [c1, c2, c3]:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=55, bottom=55, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cell != c2 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)
                run.font.bold = True if ch != "" else False
                run.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION (PAGE 3)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 1\nINTRODUCTION")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform (PrepCycle) is a full-stack, enterprise-grade web application developed to modernize and consolidate competitive examination preparation and peer-to-peer educational resource circulation. In the modern educational landscape, aspirants preparing for national-level competitive assessments—such as GATE CSE, UPSC Civil Services, JEE Advanced, NEET, and CAT—face fragmented study methodologies, unverified syllabus distributions, isolated preparation routines, and expensive physical reference materials. PrepCycle eliminates these operational bottlenecks by providing an integrated digital ecosystem connecting students, academic mentors, delivery personnel, and institutional administrators onto a unified platform."
    )

    add_styled_paragraph(
        doc,
        "The system incorporates role-specific workspaces tailored to the operational requirements of each stakeholder: Student, Academic Mentor, Delivery Partner, and System Administrator. Students can enroll in official national exam catalogs, explore weightage-ranked syllabus roadmaps (High, Medium, and Low priority tiers) while retaining complete syllabus coverage, mark granular topic completion states, track daily study streaks and calendar activity heatmaps, attempt timed computer-based mock tests, generate dynamic quizzes, and revise with interactive flashcards. Concurrently, the platform fosters an affordable circular economy through a peer-to-peer textbook marketplace, enabling students to purchase pre-owned verified reference books, list surplus study materials for resale, or donate physical textbooks to junior aspirants."
    )

    add_styled_paragraph(
        doc,
        "To ensure continuous academic supervision and student accountability, the application features an automated mentorship monitoring subsystem. Whenever an enrolled student completes a computer-based mock test, logs in for daily revision, or finishes an entire subject syllabus, automated alerts are dispatched directly to the assigned mentor's WhatsApp, SMS, and email channels without requiring administrative mediation. Mentors evaluate longitudinal progress curves and performance trends, identifying lagging students and providing timely personalized motivation. Doorstep deliveries and donation pickups are managed through a dedicated logistics partner console featuring 10-second real-time tracking updates and mandatory 4-digit OTP verification."
    )

    add_styled_paragraph(
        doc,
        "The application is engineered using modern web technologies: a React.js single-page frontend bundled with Vite, an Express.js and Node.js REST API service layer, and a scalable MongoDB NoSQL database managed via Mongoose ODM. Secure authentication is enforced through JSON Web Tokens (JWT) and Google OAuth 2.0 single sign-on. Universal accessibility settings—including full color palette customization, light/dark modes, font scaling, and multi-language support (English, Tamil, Hindi)—ensure an inclusive experience for all users. The report is organized as follows: Chapter 2 states the objectives, Chapter 3 details the system description and role permissions, Chapters 4 through 6 present the class diagram, collection structures, and ER diagram, Chapter 7 details the tech stack and architectural design, Chapter 8 comprehensively documents all project modules and role interfaces, Chapter 9 concludes the study, and Chapter 10 lists academic references."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 2: OBJECTIVES (PAGE 4)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 2\nOBJECTIVES")

    add_bullet_point(doc, "• Role-Based Security & OAuth Authentication: ",
                     "To provide secure role-based authentication and authorization using JSON Web Tokens (JWT) and bcrypt-hashed credentials, supplemented with Google OAuth 2.0 single sign-on across Student, Academic Mentor, Delivery Partner, and Administrator accounts.")
    
    add_bullet_point(doc, "• Centralized NoSQL Document Persistence: ",
                     "To maintain a normalized MongoDB database managing collections for users, examination catalogs, topic progression, mock test attempts, commerce products, orders, communication logs, discussions, and notifications.")

    add_bullet_point(doc, "• Weightage-Based Syllabus Roadmaps: ",
                     "To organize complex technical syllabi into hierarchical subjects, chapters, and topics ordered by weightage (High, Medium, Low) while preserving every topic to ensure structured preparation without content omission.")

    add_bullet_point(doc, "• Automated Mentor Progress Notifications: ",
                     "To automate academic mentor alerts via WhatsApp click-to-chat links, SMS messages, and emails whenever assigned students complete a mock test, log in for daily study, or finish an entire subject syllabus.")

    add_bullet_point(doc, "• Computer-Based Testing & Longitudinal Analytics: ",
                     "To provide timed computer-based mock evaluations, compute daily study streaks and calendar activity heatmaps, and maintain longitudinal performance trajectories over weekly, monthly, and yearly intervals.")

    add_bullet_point(doc, "• Dynamic Quiz Generation & Interactive Flashcards: ",
                     "To generate subject-specific dynamic quizzes with instant scoring and provide interactive revision flashcards with 3D flip animation for rapid formula and concept recall.")

    add_bullet_point(doc, "• Circular Textbook Marketplace & Donations: ",
                     "To facilitate peer-to-peer textbook resale, condition grading, price filtering, and 100% free textbook donations to support resource-deprived junior aspirants.")

    add_bullet_point(doc, "• Doorstep Fulfillment & OTP Verification: ",
                     "To streamline physical logistics fulfillment with real-time 10-second polling tracking, status transitions, and mandatory 4-digit OTP verification upon delivery.")

    add_bullet_point(doc, "• Peer Collaboration & Contextual AI Guidance: ",
                     "To integrate a student community discussion forum featuring upvoting and solution badges, complemented by a context-aware AI chatbot offering personalized study roadmaps.")

    add_bullet_point(doc, "• Universal UI Customization & Multi-Language Support: ",
                     "To provide universal appearance settings allowing users to adjust button colors, text colors, background colors, dark/light themes, font scaling, and multi-language translations (English, Tamil, Hindi).")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 3: DESCRIPTION (PAGE 5)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 3\nDESCRIPTION")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform is a web-based educational management and circular commerce system designed to consolidate competitive examination learning, academic supervision, and physical resource sharing within a unified architecture. The system supports four distinct operational user roles: Student, Academic Mentor, Delivery Partner, and System Administrator, each provided with dedicated access boundaries and functional toolsets."
    )

    add_styled_paragraph(
        doc,
        "1. Identity and Access Control: Public registration, unified credentials login, Google OAuth 2.0 authentication, and JWT-authenticated API endpoints ensure strict security isolation across all four platform roles without publicly disclosing internal role hierarchies."
    )

    add_styled_paragraph(
        doc,
        "2. Academic Preparation & Syllabus Exploration: Students access exhaustive catalogs for national exams (GATE CSE, UPSC, JEE, NEET, CAT), interact with weightage-categorized syllabi (High, Medium, Low), record topic progression, maintain daily study streaks, and evaluate readiness through timed mock tests and interactive revision flashcards."
    )

    add_styled_paragraph(
        doc,
        "3. Automated Mentorship Supervision: Mentors oversee assigned students through longitudinal performance dashboards and receive real-time automated progress alerts across WhatsApp, SMS, and email when tests are submitted, ensuring proactive guidance for lagging learners."
    )

    add_styled_paragraph(
        doc,
        "4. Circular Commerce & Book Circulation: Peer-to-peer textbook resale, condition grading (New, Like New, Good, Fair), free donation claiming, multi-tier checkout (COD, UPI, Card), and structured return workflows allow students to exchange materials affordably."
    )

    add_styled_paragraph(
        doc,
        "5. Logistics Fulfillment & Secure OTP Verification: Delivery personnel manage assigned consignments, advance order states, and confirm physical deliveries or donation pickups using mandatory 4-digit OTP verification, synchronized with 10-second client tracking polling."
    )

    add_styled_paragraph(
        doc,
        "6. System Governance & Multi-Channel Communication: Administrators monitor platform telemetry, allocate mentors, curate examination syllabi, and dispatch verified notifications via an integrated multi-channel communication engine."
    )

    add_heading_2(doc, "3.1 Access Permission of Roles")
    add_styled_paragraph(
        doc,
        "To ensure robust data isolation, integrity, and security, the application enforces strict Role-Based Access Control (RBAC). JSON Web Tokens carry authenticated user role claims that are validated on every API request via authentication middleware and client-side ProtectedRoute route guards. The diagram below details the comprehensive access permission matrix across all four platform roles:"
    )

    # High-res B&W Access Permission Matrix
    access_img = get_root("access_permission_roles_bw.png")
    if not os.path.exists(access_img):
        access_img = get_media("image2.png")
    add_screenshot(doc, access_img, "Fig 3.1 – Access Permission of Roles and Security Authorization Matrix.", width_inches=6.0)

    add_styled_paragraph(
        doc,
        "As illustrated in the authorization matrix, Students possess comprehensive permissions over learning roadmaps, mock tests, marketplace transactions, and community interactions. Academic Mentors are granted specialized supervisory privileges, enabling them to inspect assigned students' longitudinal study curves, receive automated WhatsApp alerts, and initiate direct guidance. Delivery Partners are restricted to logistics workflows, requiring client OTP input to verify handover. System Administrators retain full system governance with administrative access to user accounts, mentor assignments, catalog data, and multi-channel communication tools."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 4: CLASS DIAGRAM (PAGE 6)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 4\nCLASS DIAGRAM")

    add_styled_paragraph(
        doc,
        "The diagram illustrates the object-oriented database structure of the Multi-Exam Preparation and Resource Exchange Platform. The central User entity is connected to academic, logistics, and marketplace entities including Exam, Progress, MockAttempt, Product, Order, OrderItem, CommunicationLog, Discussion, and Notification. These entities store user credentials, study roadmaps, test scores, commerce listings, order states, and communication dispatch history. Primary keys (PK) uniquely identify records while foreign keys (FK) establish relationships between entities."
    )

    class_img = get_root("class_diagram_bw.png")
    if not os.path.exists(class_img):
        class_img = get_media("image3.png")
    add_screenshot(doc, class_img, "Fig 4.1 – Class Diagram – Entities of the platform with their attributes and relationships.", width_inches=6.1)

    add_styled_paragraph(
        doc,
        "The User class serves as the foundational identity entity, extended by discriminator properties for student, mentor, delivery, and admin roles. The Exam and Progress classes maintain strong associations: an Exam defines the static curriculum hierarchy of subjects, chapters, and topics, while Progress records dynamic completion mappings, timestamps, and streak counters per student. The Commerce domain encapsulates Product and Order entities with composition linkages to OrderItem, enforcing data integrity across transactions."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 5: TABLE STRUCTURES (PAGE 7-12)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 5\nTABLE STRUCTURES")

    add_styled_paragraph(
        doc,
        "The application stores each data type in its own MongoDB collection of the prepcycle database, and every item is a document. The structure of each collection is given below."
    )

    add_heading_2(doc, "5.1 MongoDB Collections")
    add_styled_paragraph(
        doc,
        "The persistent collections managed within the MongoDB prepcycle database are outlined below with their functional purpose, indexing strategy, and document schemas."
    )

    # 5.2 Users
    add_heading_2(doc, "5.2 Users:")
    add_styled_paragraph(
        doc,
        "Stores every account of the portal with its role, authentication method, verified flag, assigned mentor, and preferences."
    )
    format_schema_table(
        doc, "Table 5.2 – Structure of the users table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["name", "String", "NO", "None", "None", "Full user name"],
            ["email", "String", "NO", "UNI", "None", "Unique user email address"],
            ["password", "String", "YES", "None", "None", "Salted bcrypt password hash"],
            ["role", "Enum", "NO", "MUL", "student", "student | mentor | admin | delivery"],
            ["studentId", "String", "YES", "UNI / SPARSE", "None", "Unique student roll ID (e.g. PC-STU-100001)"],
            ["phone", "String", "YES", "None", "''", "Contact telephone number"],
            ["whatsappNumber", "String", "YES", "None", "''", "Phone number for WhatsApp alert dispatch"],
            ["mentor", "ObjectId", "YES", "FK / MUL", "null", "Reference to assigned mentor user"],
            ["assignedStudents", "Array[ObjectId]", "YES", "MUL", "[]", "List of student IDs assigned to mentor"],
            ["targetExam", "String", "YES", "None", "GATE CSE", "Primary goal competitive examination"],
            ["registeredExams", "Array[String]", "YES", "None", "[]", "Slugs of actively enrolled exams"],
            ["authProvider", "Enum", "NO", "None", "local", "local | google"],
            ["preferences", "SubDoc", "YES", "None", "{}", "Theme, palette, font size, language"],
            ["createdAt / updatedAt", "Date", "NO", "None", "Date.now", "System auditing timestamps"],
        ]
    )

    # 5.3 Exams
    add_heading_2(doc, "5.3 Exams:")
    add_styled_paragraph(
        doc,
        "Stores the examination catalog profiles, conducting authorities, syllabi, and weightage rankings."
    )
    format_schema_table(
        doc, "Table 5.3 – Structure of the exams table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["slug", "String", "NO", "UNI", "None", "URL-safe unique identifier (e.g. gate-cse)"],
            ["name", "String", "NO", "None", "None", "Full examination title"],
            ["category", "String", "NO", "None", "None", "Discipline category (e.g. engineering)"],
            ["authority", "String", "NO", "None", "None", "Conducting body or examination commission"],
            ["officialUrl", "String", "NO", "None", "None", "Official examination authority portal link"],
            ["subjects", "Array[SubDoc]", "NO", "None", "[]", "Embedded hierarchy of subjects & chapters"],
            ["createdAt / updatedAt", "Date", "NO", "None", "Date.now", "Auditing timestamps"],
        ]
    )

    # 5.4 Progress
    add_heading_2(doc, "5.4 Progress:")
    add_styled_paragraph(
        doc,
        "Stores individual student study progress, topic completion maps, and streak records."
    )
    format_schema_table(
        doc, "Table 5.4 – Structure of the progress table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Reference to User account"],
            ["examSlug", "String", "NO", "FK / MUL", "None", "Reference to Exam slug"],
            ["topicStatus", "Map[String, Enum]", "NO", "None", "{}", "Map of topicId -> pending | in_progress | completed"],
            ["studyDays", "Array[String]", "YES", "None", "[]", "ISO date strings (YYYY-MM-DD) for streak calculation"],
            ["currentStreak", "Number", "NO", "None", "0", "Consecutive days active streak counter"],
            ["dailyLogs", "Array[SubDoc]", "YES", "None", "[]", "Audit trail of topic updates and test scores"],
            ["createdAt / updatedAt", "Date", "NO", "None", "Date.now", "Record timestamps"],
        ]
    )

    # 5.5 Mock Attempts
    add_heading_2(doc, "5.5 Mock Attempts:")
    add_styled_paragraph(
        doc,
        "Stores computer-based mock test submissions, scores, question metrics, and timestamps."
    )
    format_schema_table(
        doc, "Table 5.5 – Structure of the mock_attempts table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Reference to Student user"],
            ["examSlug", "String", "NO", "MUL", "None", "Associated examination slug"],
            ["subjectName", "String", "NO", "None", "None", "Name of subject tested"],
            ["chapterName", "String", "NO", "None", "None", "Name of chapter tested"],
            ["mockName", "String", "NO", "None", "None", "Mock test title or CBT identifier"],
            ["questionsAttended", "Number", "NO", "None", "0", "Total questions attempted"],
            ["marks", "Number", "NO", "None", "0", "Marks obtained by student"],
            ["maxMarks", "Number", "NO", "None", "100", "Maximum attainable marks"],
            ["attemptedAt", "Date", "NO", "MUL", "Date.now", "Timestamp of test submission"],
        ]
    )

    # 5.6 Products
    add_heading_2(doc, "5.6 Products:")
    add_styled_paragraph(
        doc,
        "Stores the marketplace reference books, study notes, price tags, and donation flags."
    )
    format_schema_table(
        doc, "Table 5.6 – Structure of the products table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["title", "String", "NO", "None", "None", "Book title or material description"],
            ["author", "String", "YES", "None", "''", "Book author or publisher name"],
            ["category", "String", "NO", "MUL", "None", "Textbook | Notes | Solved Papers"],
            ["examSlug", "String", "YES", "MUL", "''", "Associated competitive exam"],
            ["price", "Number(10,2)", "NO", "None", "0.00", "Listing price in INR (0 for donations)"],
            ["condition", "Enum", "NO", "None", "Good", "New | Like New | Good | Fair"],
            ["isDonation", "Boolean", "NO", "MUL", "false", "Flags 100% free community donations"],
            ["stock", "Number", "NO", "None", "1", "Available inventory quantity"],
            ["seller", "ObjectId", "NO", "FK / MUL", "None", "Reference to listing student"],
            ["status", "Enum", "NO", "None", "available", "available | sold | claimed"],
        ]
    )

    # 5.7 Orders
    add_heading_2(doc, "5.7 Orders:")
    add_styled_paragraph(
        doc,
        "Stores buyer orders, payment details, assigned delivery partners, and 4-digit OTPs."
    )
    format_schema_table(
        doc, "Table 5.7 – Structure of the orders table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["trackingId", "String", "NO", "UNI", "None", "Human-readable order tracking ID (TRK-XXXXXX)"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Reference to purchasing Student"],
            ["items", "Array[SubDoc]", "NO", "None", "[]", "Array of purchased products, price & quantities"],
            ["totalAmount", "Number(10,2)", "NO", "None", "0.00", "Total payable order amount"],
            ["paymentMethod", "Enum", "NO", "None", "cod", "cod | upi | gpay | card | netbanking"],
            ["status", "Enum", "NO", "MUL", "Ordered", "Ordered | Dispatched | In Transit | Out for Delivery | Delivered"],
            ["verificationOtp", "String(4)", "NO", "None", "None", "4-digit security OTP required for delivery"],
            ["deliveryAddress", "SubDoc", "NO", "None", "None", "Recipient address, city, pincode & phone"],
            ["assignedPartner", "ObjectId", "YES", "FK / MUL", "null", "Reference to delivery partner account"],
        ]
    )

    # 5.8 Order Items
    add_heading_2(doc, "5.8 Order Items:")
    add_styled_paragraph(
        doc,
        "Stores normalized line items for order transactions, including quantity, unit price, and item status."
    )
    format_schema_table(
        doc, "Table 5.8 – Structure of the order_items table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique line item identifier"],
            ["orderId", "ObjectId", "NO", "FK / MUL", "None", "Foreign key to parent Order"],
            ["productId", "ObjectId", "NO", "FK / MUL", "None", "Foreign key to Product"],
            ["quantity", "Number", "NO", "None", "1", "Quantity purchased"],
            ["unitPrice", "Number(10,2)", "NO", "None", "0.00", "Price per unit in INR"],
            ["status", "Enum", "NO", "None", "active", "active | returned | cancelled"],
        ]
    )

    # 5.9 Communication Logs
    add_heading_2(doc, "5.9 Communication Logs:")
    add_styled_paragraph(
        doc,
        "Stores the notifications dispatched across WhatsApp, SMS, and email channels with delivery statuses."
    )
    format_schema_table(
        doc, "Table 5.9 – Structure of the communication_logs table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["user", "ObjectId", "YES", "FK / MUL", "null", "Recipient user reference"],
            ["channel", "Enum", "NO", "MUL", "None", "whatsapp | sms | email | notification"],
            ["messageType", "String", "NO", "MUL", "None", "mentor_mock_test_alert | mentor_subject_completed_alert"],
            ["recipient", "String", "NO", "None", "None", "Destination phone number or email"],
            ["subject", "String", "YES", "None", "''", "Subject header or brief title"],
            ["content", "String", "NO", "None", "None", "Full dispatched message body with WhatsApp link"],
            ["status", "Enum", "NO", "MUL", "pending", "delivered | pending | failed"],
            ["provider", "String", "YES", "None", "''", "Gateway used (WhatsApp Cloud API, Ethereal, SMS)"],
            ["timestamp", "Date", "NO", "MUL", "Date.now", "Message dispatch timestamp"],
        ]
    )

    # 5.10 Discussions
    add_heading_2(doc, "5.10 Discussions:")
    add_styled_paragraph(
        doc,
        "Stores community questions, answers, upvotes, and verified resolution flags."
    )
    format_schema_table(
        doc, "Table 5.10 – Structure of the discussions table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique discussion identifier"],
            ["author", "ObjectId", "NO", "FK / MUL", "None", "User reference of post author"],
            ["examSlug", "String", "NO", "MUL", "None", "Associated examination category"],
            ["title", "String", "NO", "None", "None", "Discussion question title"],
            ["body", "String", "NO", "None", "None", "Detailed question or query body"],
            ["upvotes", "Array[ObjectId]", "YES", "None", "[]", "User IDs who upvoted the question"],
            ["answers", "Array[SubDoc]", "YES", "None", "[]", "Replies with author, content, and upvotes"],
            ["resolved", "Boolean", "NO", "None", "false", "Flags whether question has accepted solution"],
            ["createdAt", "Date", "NO", "MUL", "Date.now", "Post creation timestamp"],
        ]
    )

    # 5.11 Notifications
    add_heading_2(doc, "5.11 Notifications:")
    add_styled_paragraph(
        doc,
        "Stores in-app alert notifications for user accounts with read/unread tracking."
    )
    format_schema_table(
        doc, "Table 5.11 – Structure of the notifications table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique notification identifier"],
            ["recipient", "ObjectId", "NO", "FK / MUL", "None", "Target user ID"],
            ["type", "Enum", "NO", "MUL", "system", "order | mentor | mock | system"],
            ["title", "String", "NO", "None", "None", "Short notification alert title"],
            ["message", "String", "NO", "None", "None", "Full notification text"],
            ["isRead", "Boolean", "NO", "MUL", "false", "Read/unread status flag"],
            ["actionUrl", "String", "YES", "None", "''", "Link to navigate user upon click"],
            ["createdAt", "Date", "NO", "MUL", "Date.now", "Creation timestamp"],
        ]
    )

    # 5.12 Return Requests
    add_heading_2(doc, "5.12 Return Requests:")
    add_styled_paragraph(
        doc,
        "Stores textbook return and buyback requests submitted by buyers within the eligible return window."
    )
    format_schema_table(
        doc, "Table 5.12 – Structure of the return_requests table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique return request identifier"],
            ["orderId", "ObjectId", "NO", "FK / MUL", "None", "Reference to original order"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Student requesting return"],
            ["reason", "Enum", "NO", "None", "None", "wrong_edition | damaged | exam_completed | other"],
            ["status", "Enum", "NO", "MUL", "requested", "requested | approved | rejected | refunded"],
            ["pickupAddress", "SubDoc", "NO", "None", "None", "Pickup address for delivery partner"],
            ["createdAt", "Date", "NO", "None", "Date.now", "Request submission timestamp"],
        ]
    )

    # 5.13 Flashcards
    add_heading_2(doc, "5.13 Flashcards:")
    add_styled_paragraph(
        doc,
        "Stores interactive revision flashcards categorized by examination, subject, and topic."
    )
    format_schema_table(
        doc, "Table 5.13 – Structure of the flashcards table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique flashcard identifier"],
            ["examSlug", "String", "NO", "MUL", "None", "Associated examination"],
            ["subject", "String", "NO", "None", "None", "Subject category"],
            ["question", "String", "NO", "None", "None", "Front-facing question or concept"],
            ["answer", "String", "NO", "None", "None", "Back-facing answer, theorem, or formula"],
            ["masteredBy", "Array[ObjectId]", "YES", "None", "[]", "Students who flagged card as mastered"],
        ]
    )

    # 5.14 Notes
    add_heading_2(doc, "5.14 Notes:")
    add_styled_paragraph(
        doc,
        "Stores user-generated rich study notes, summaries, and revision cheat sheets."
    )
    format_schema_table(
        doc, "Table 5.14 – Structure of the notes table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique note identifier"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Author student reference"],
            ["examSlug", "String", "NO", "MUL", "None", "Associated exam"],
            ["topicId", "String", "NO", "None", "None", "Topic identifier"],
            ["content", "String", "NO", "None", "None", "Markdown or text note body"],
            ["isPublic", "Boolean", "NO", "None", "false", "Visibility flag for peer sharing"],
            ["updatedAt", "Date", "NO", "None", "Date.now", "Last edit timestamp"],
        ]
    )

    # 5.15 Recently Accessed
    add_heading_2(doc, "5.15 Recently Accessed:")
    add_styled_paragraph(
        doc,
        "Stores the last visited examinations, subjects, and study materials of each user."
    )
    format_schema_table(
        doc, "Table 5.15 – Structure of the recently_accessed table",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique access record identifier"],
            ["user", "ObjectId", "NO", "FK / MUL", "None", "Reference to user account"],
            ["itemType", "Enum", "NO", "None", "exam", "exam | topic | product | mock"],
            ["itemId", "String", "NO", "None", "None", "Identifier of visited entity"],
            ["title", "String", "NO", "None", "None", "Display label of visited entity"],
            ["accessedAt", "Date", "NO", "MUL", "Date.now", "Last access timestamp"],
        ]
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 6: ER DIAGRAM (PAGE 13)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 6\nER DIAGRAM")

    add_styled_paragraph(
        doc,
        "The User entity is related to most other entities. A user registers for examinations, updates study progress, attends computer-based mock tests, lists marketplace products, places orders, and exchanges community discussion posts. The Academic Mentor is linked to multiple assigned students through an allocation relationship, while Delivery Partners are linked to assigned orders. Both mock tests and daily logins trigger communication log entries. The Entity-Relationship diagram below defines the cardinalities and relational associations governing the database schema:"
    )

    er_img = get_root("er_diagram_bw.png")
    if not os.path.exists(er_img):
        er_img = get_media("image4.png")
    add_screenshot(doc, er_img, "Fig 6.1 – ER Diagram – Entities and relationships of the Multi-Exam Preparation and Resource Exchange Platform.", width_inches=6.0)

    add_styled_paragraph(
        doc,
        "As depicted in the diagram, the relationship between User and Exam is many-to-many through registered enrollments, resolved by the Progress mapping entity. The User-to-MockAttempt relation is one-to-many, recording every attempt with timestamped metrics. In the commerce domain, a student user acts as either a buyer (User to Order: 1:N) or a seller (User to Product: 1:N). Orders maintain a 1:N composition with OrderItem, which in turn references the Product entity. The DeliveryPartner entity fulfills orders via a 1:N assignment relationship. The diagram demonstrates strict referential integrity across the academic and commerce subsystems."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 7: TECH STACK (PAGE 14)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 7\nTECH STACK")

    add_heading_2(doc, "7.1 TECH STACK")
    format_grid_table(
        doc,
        ["Layer", "Technology", "Purpose"],
        [
            ["Frontend", "React.js 18 + Vite", "Component-driven single page application with rapid HMR and optimized asset bundling."],
            ["Styling", "Vanilla CSS + CSS Variables", "Modular responsive styling supporting dynamic theme switching and accessibility scaling."],
            ["3D Visuals", "Three.js", "Interactive 3D geometric visualization rendered on the public authentication portal."],
            ["Routing", "React Router DOM v6", "Client-side declarative routing with role-based route guard boundaries."],
            ["Backend", "Node.js + Express.js", "RESTful micro-service API handling business logic, session validation, and data orchestration."],
            ["Database", "MongoDB Atlas + Mongoose", "Scalable document persistence, schema validation, and compound index querying."],
            ["Authentication", "JWT + bcryptjs", "Stateless bearer token authorization and 10-round salted password hashing."],
            ["OAuth SSO", "Google OAuth 2.0 API", "Real Google client sign-in integration validating verified email profiles."],
            ["Messaging", "WhatsApp + Twilio + Nodemailer", "Multi-channel automated alerts dispatched to mentors, students, and admins."],
            ["Logistics", "Custom OTP Engine", "Cryptographic 4-digit OTP generation and verification for safe doorstep handover."],
            ["Deployment", "Docker + Cloud Hosting", "Multi-stage containerization enabling automated builds and isolated cloud hosting."]
        ]
    )

    add_heading_2(doc, "7.2 ARCHITECTURE OVERVIEW")
    add_styled_paragraph(
        doc,
        "The system follows a classical Three-Tier Model-View-Controller (MVC) architectural pattern augmented with a decoupled event notification pipeline. The client-side View layer (React.js) communicates with the server-side Controller layer (Express.js) via asynchronous HTTP/JSON requests over TLS. The Controller validates input payloads and queries the Model layer (Mongoose ODM) which interfaces with the persistent MongoDB database. Background notification workers asynchronously dispatch WhatsApp, SMS, and email alerts without blocking client response threads."
    )

    arch_img = get_root("architecture_flow_bw.png")
    if os.path.exists(arch_img):
        add_screenshot(doc, arch_img, "Fig 7.1 – Architectural Data Flow Diagram of the Platform.", width_inches=5.8)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 8: MODULES (PAGE 15 ONWARDS)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 8\nMODULES")

    add_heading_2(doc, "8.0 Design Approach")
    add_styled_paragraph(
        doc,
        "The system-wide design baseline defines the common architectural principles followed by every module in the application. The web client provides a responsive interface with light and dark themes, full color palette customizability, font scaling, and support for multiple regional languages (English, Tamil, Hindi). The backend API manages authentication, collection-state operations, and offline seed-data fallback, while MongoDB serves as the single source of truth for persistent data. Robust error handling, rate limiting, and input sanitization ensure operational stability across all modules."
    )

    # 8.1 FOLDER STRUCTURE
    add_heading_2(doc, "8.1 FOLDER STRUCTURE")
    add_styled_paragraph(
        doc,
        "The PrepCycle project is organized into two main parts: a backend folder that contains the Node.js and Express.js server, and a frontend folder that contains the React application. Keeping the two parts separate allows them to be developed, tested, and run independently."
    )

    add_heading_3(doc, "BACKEND FOLDER")
    add_styled_paragraph(
        doc,
        "The image below illustrates the directory organization of the backend sub-system in Visual Studio Code. Inside the backend folder, modular directories contain controllers, models, routes, services, middleware, and configuration files along with database seeding scripts:"
    )
    add_screenshot(doc, get_media("image5.png"), "Fig 8.1 – Backend Folder Structure – Overall organization of backend files and directories.", width_inches=4.2)

    add_heading_3(doc, "FRONTEND FOLDER")
    add_styled_paragraph(
        doc,
        "The image below illustrates the directory organization of the React frontend sub-system in Visual Studio Code. The source directory contains dedicated folders for components, pages, context providers, API wrappers, and static assets:"
    )
    add_screenshot(doc, get_media("image6.png"), "Fig 8.2 – Frontend Folder Structure – Layout of the React-based frontend directories.", width_inches=4.2)

    # 8.2 USER AUTHENTICATION & ACCESS CONTROL
    add_heading_2(doc, "8.2 USER AUTHENTICATION & ACCESS CONTROL")
    add_screenshot(doc, get_media("image7.png"), "Fig 8.3 – User Authentication & Registration Interface – Sign-in with credentials or Google OAuth with 3D background.")
    add_screenshot(doc, get_media("image8.png"), "Fig 8.4 – Google OAuth 2.0 Real Authentication Interface – Single sign-on authentication.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides secure registration, sign-in, and role-based access for the four user types of the portal (Student, Academic Mentor, Delivery Partner, and Administrator). Every request that reads or writes portal data is accepted only when it carries a valid JSON Web Token (JWT). The module supports user session validation, handles invalid or expired tokens, and prevents unauthorized access to protected routes without publicly revealing role distinctions on the login page."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Unified Registration & Sign-In: ", "A visitor registers with a name, email, password, and role; passwords are encrypted with bcrypt salts. Registered users sign in and receive a signed JWT valid for 12 hours.")
    add_bullet_point(doc, "• Real Google OAuth Sign-In: ", "Users authenticate through official Google OAuth 2.0 authorization codes; Google ID tokens are verified on the backend to issue valid JWT sessions.")
    add_bullet_point(doc, "• Dynamic Role Redirection: ", "Upon sign-in, the client inspects role claims and immediately redirects Students to /exam-explorer, Mentors to /mentor, Delivery Partners to /delivery, and Administrators to /admin.")
    add_bullet_point(doc, "• Unique Student Roll ID: ", "The backend automatically generates non-colliding Student IDs (e.g. PC-STU-100001) upon student account creation.")
    add_bullet_point(doc, "• Secure Token Management: ", "The browser stores tokens in localStorage and attaches them as Authorization: Bearer headers on all subsequent API calls.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_styled_paragraph(doc, "How well the module must do it (the system-wide baseline in 8.0 also applies):", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Cryptographic Security: ", "Passwords are never stored in plaintext; 10-round bcrypt hashes ensure brute-force protection.")
    add_bullet_point(doc, "• Response Latency: ", "Authentication verification and JWT issuance complete in under 200 milliseconds.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["POST", "/api/auth/register", "Creates account with role, hashed password, and student ID."],
            ["POST", "/api/auth/login", "Authenticates credentials and returns JWT plus user role."],
            ["POST", "/api/auth/google/verify", "Validates Google OAuth tokens and issues platform session."],
            ["GET", "/api/auth/me", "Returns current authenticated user profile from token."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["users", "_id (ObjectId); unique email, sparse unique studentId", "name, email, password, role, studentId, mentor, authProvider"]
        ]
    )
    add_bullet_point(doc, "• Unique email index: ", "Enables rapid single-index authentication lookup and prevents duplicate registrations.")
    add_bullet_point(doc, "• Role claim field: ", "Controls access permissions across Student, Academic Mentor, Delivery Partner, and Administrator.")

    # 8.3 ROLE-BASED DASHBOARD ROUTING & PERMISSIONS
    add_heading_2(doc, "8.3 ROLE-BASED DASHBOARD ROUTING & PERMISSIONS")
    add_screenshot(doc, get_media("image9.png"), "Fig 8.5.1 – Student Dashboard Redirection – Access to study roadmaps and exams.")
    add_screenshot(doc, get_media("image10.png"), "Fig 8.5.2 – Admin Dashboard Redirection – Platform statistics and system governance.")
    add_screenshot(doc, get_media("image11.png"), "Fig 8.5.3 – Mentor Dashboard Redirection – Assigned students and progress curves.")
    add_screenshot(doc, get_media("image12.png"), "Fig 8.5.4 – Delivery Dashboard Redirection – Consignments and OTP verification.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Ensures strict data isolation and route protection by evaluating user roles and navigating authenticated users to their authorized operational dashboard while rejecting unauthorized access attempts."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Client-Side Route Protection: ", "ProtectedRoute wrappers intercept navigation, verifying token validity and role authorization before rendering target views.")
    add_bullet_point(doc, "• Automated Redirection: ", "Redirects unauthenticated visitors to /login and directs unauthorized role attempts to their designated home screen.")
    add_bullet_point(doc, "• Persistent State Restoration: ", "Re-authenticates active sessions on browser reload using stored localStorage tokens.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Zero-Flicker Routing: ", "Route authorization resolves synchronously to prevent UI layout shift or content leakage.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/auth/me", "Validates session token and returns authorized role claims."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["users", "role index (MUL)", "role, permissions, lastLogin"]
        ]
    )

    # 8.4 EXAM EXPLORER & OFFICIAL SYLLABUS ROADMAP
    add_heading_2(doc, "8.4 EXAM EXPLORER & OFFICIAL SYLLABUS ROADMAP")
    add_screenshot(doc, get_media("image13.png"), "Fig 8.6 – Student Exam Explorer Interface – Competitive examination catalog and selection.")
    add_screenshot(doc, get_media("image14.png"), "Fig 8.7 – Weightage-Based Syllabus Roadmap – High, Medium, and Low weightage topic prioritization.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Enables students to explore national competitive examination catalogs, register for target exams, and navigate structured, weightage-prioritized syllabus roadmaps (High, Medium, Low) without omitting any official topics."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Examination Catalog: ", "Lists competitive exams (GATE CSE, UPSC, JEE, NEET, CAT) with conducting body details and syllabus links.")
    add_bullet_point(doc, "• Weightage Sorting: ", "Categorizes subject chapters and topics into High, Medium, and Low weightage tiers while retaining complete topic coverage.")
    add_bullet_point(doc, "• Search & Filter: ", "Allows real-time searching across examination subjects, chapters, and topics.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Fast Catalog Rendering: ", "Syllabus trees load within 150ms from optimized embedded Mongoose document structures.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/exams", "Returns catalog of competitive examinations."],
            ["GET", "/api/exams/:slug", "Returns complete subject, chapter, and topic roadmap for an exam."],
            ["POST", "/api/exams/:slug/register", "Registers authenticated student for the target exam."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["exams", "unique slug index", "slug, name, category, authority, subjects[name, weightage, topics]"]
        ]
    )

    # 8.5 STUDY PROGRESS & HEATMAP ACTIVITY TRACKING
    add_heading_2(doc, "8.5 STUDY PROGRESS & HEATMAP ACTIVITY TRACKING")
    add_screenshot(doc, get_media("image15.png"), "Fig 8.8 – Syllabus Topic Progress Tracking – Interactive topic completion state management.")
    add_screenshot(doc, get_media("image16.png"), "Fig 8.9 – Daily Study Streaks & Activity Heatmap – Calendar visualization of student consistency.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Captures topic completion states, calculates syllabus completion percentages, tracks daily study streaks, and renders a GitHub-style calendar activity heatmap."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Topic State Toggle: ", "Allows students to toggle topics between Pending, In Progress, and Completed states.")
    add_bullet_point(doc, "• Progress Percentage Calculation: ", "Automatically recalculates overall and subject-level completion percentages upon state updates.")
    add_bullet_point(doc, "• Streak Counter: ", "Tracks consecutive active study days and increments streaks on daily activity.")
    add_bullet_point(doc, "• Calendar Activity Heatmap: ", "Visualizes past 365 days of study intensity using color-coded activity tiles.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Atomic Updates: ", "Topic state mutations execute atomically to prevent race conditions during rapid checklist clicking.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/progress/:examSlug", "Retrieves student's topic completion map and streak metrics."],
            ["PATCH", "/api/progress/:examSlug/topic", "Updates topic completion state and recalculates study streak."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["progress", "compound index (user, examSlug)", "user, examSlug, topicStatus, studyDays, currentStreak"]
        ]
    )

    # 8.6 COMPUTER-BASED MOCK TESTS & PERFORMANCE ANALYTICS
    add_heading_2(doc, "8.6 COMPUTER-BASED MOCK TESTS & PERFORMANCE ANALYTICS")
    add_screenshot(doc, get_media("image17.png"), "Fig 8.10 – Computer-Based Mock Test Interface – Timed examination simulator with question palette.")
    add_screenshot(doc, get_media("image18.png"), "Fig 8.11 – Mock Test Evaluation & Analytics – Score breakdowns and performance progression.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Simulates realistic computer-based competitive test environments with timer counters, question navigation palettes, instant score computation, and longitudinal performance analytics."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Timed CBT Simulator: ", "Presents multiple-choice questions with a synchronized countdown timer and status palette.")
    add_bullet_point(doc, "• Multi-Attempt Tracking: ", "Preserves scores and timestamps across multiple attempts, charting performance progression.")
    add_bullet_point(doc, "• Instant Evaluation: ", "Computes marks obtained, accuracy percentage, and negative marking adjustments.")
    add_bullet_point(doc, "• Mentor Alert Trigger: ", "Dispatches automated performance summaries to the student's assigned mentor upon submission.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Zero Test Data Loss: ", "Caches answers locally to survive accidental tab refreshes during examination sessions.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/mocks/:examSlug/chapter/:chapterId", "Fetches questions for a computer-based mock test."],
            ["POST", "/api/mock-attempts/:examSlug/chapter/:chapterId", "Submits test responses, logs scores, and alerts assigned mentor."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["mock_attempts", "compound index (user, attemptedAt)", "user, examSlug, mockName, marks, maxMarks, attemptedAt"]
        ]
    )

    # 8.7 DYNAMIC QUIZ GENERATOR & REVISION FLASHCARDS
    add_heading_2(doc, "8.7 DYNAMIC QUIZ GENERATOR & REVISION FLASHCARDS")
    add_screenshot(doc, get_media("image19.png"), "Fig 8.12 – Dynamic Quiz Generation & Assessment – Instant topic-specific quiz generation.")
    add_screenshot(doc, get_media("image20.png"), "Fig 8.13 – Interactive Revision Flashcards – 3D flipping flashcards for concept revision.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides quick formative assessments through dynamically generated topic quizzes and interactive 3D-flipping flashcards for rapid formula and theorem revision."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Dynamic Quiz Generation: ", "Generates 5-to-10 question topical mini-quizzes on demand with instant feedback.")
    add_bullet_point(doc, "• Interactive Flashcards: ", "Renders animated 3D flip cards displaying concepts on front and detailed explanations on back.")
    add_bullet_point(doc, "• Mastery Tracking: ", "Allows students to mark flashcards as mastered, filtering unmastered cards for focused review.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Fluid Animations: ", "60 FPS CSS 3D card flipping transitions.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/quizzes/generate", "Generates dynamic quiz questions for target topic."],
            ["GET", "/api/flashcards/:examSlug", "Retrieves revision flashcards categorized by subject."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["flashcards", "index on examSlug", "examSlug, subject, question, answer, masteredBy"]
        ]
    )

    # 8.8 PEER-TO-PEER RESOURCE MARKETPLACE & BOOK DONATION
    add_heading_2(doc, "8.8 PEER-TO-PEER RESOURCE MARKETPLACE & BOOK DONATION")
    add_screenshot(doc, get_media("image21.png"), "Fig 8.14 – Peer-to-Peer Educational Resource Marketplace – Pre-owned reference books and listings.")
    add_screenshot(doc, get_media("image22.png"), "Fig 8.15 – Educational Book Donation Interface – 100% free physical book sharing.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Fosters an affordable circular educational resource exchange where students purchase verified second-hand textbooks, list surplus study materials, or donate books to junior aspirants for free."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Resource Listings: ", "Students create listings specifying title, author, exam category, price, and condition (New, Like New, Good, Fair).")
    add_bullet_point(doc, "• Free Book Donations: ", "Supports 100% free donation listings (Price: ₹0) claimed on a first-come, first-served basis.")
    add_bullet_point(doc, "• Filtering & Search: ", "Filters catalog items by examination, condition, price range, and donation status.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Image Optimization: ", "Compresses uploaded book cover photos to under 300KB.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/marketplace/products", "Returns active marketplace products with filters."],
            ["POST", "/api/marketplace/products", "Creates a new book resale or donation listing."],
            ["GET", "/api/marketplace/donations", "Returns free community textbook donation listings."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["products", "indexes on examSlug, isDonation, status", "title, author, category, price, condition, isDonation, seller, status"]
        ]
    )

    # 8.9 SHOPPING CART, CHECKOUT & PAYMENT INTEGRATION
    add_heading_2(doc, "8.9 SHOPPING CART, CHECKOUT & PAYMENT INTEGRATION")
    add_screenshot(doc, get_media("image23.png"), "Fig 8.16 – Marketplace Shopping Cart – Item quantity adjustment and price subtotal.")
    add_screenshot(doc, get_media("image24.png"), "Fig 8.17 – Order Checkout & Payment Options – Shipping address and multi-tier payment methods.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Manages shopping cart persistence, address validation, multi-tier payment selection (Cash on Delivery, UPI, Cards, Net Banking), and secure order generation."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Cart Persistence: ", "Retains cart items across browser sessions using localStorage and synchronizes with inventory.")
    add_bullet_point(doc, "• Checkout Form Validation: ", "Validates recipient name, street address, postal code, and contact phone number.")
    add_bullet_point(doc, "• Multi-Tier Payments: ", "Supports Cash on Delivery (COD), UPI (Google Pay, PhonePe), Credit/Debit Cards, and Net Banking.")
    add_bullet_point(doc, "• Unique Tracking ID: ", "Generates human-readable tracking identifiers (e.g. TRK-482910) upon successful order creation.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Transaction Atomicity: ", "Decrements product inventory atomically upon order placement.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["POST", "/api/orders/checkout", "Processes checkout payload, decrements stock, and returns order tracking ID."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["orders", "unique trackingId index", "trackingId, user, items, totalAmount, paymentMethod, status, verificationOtp"]
        ]
    )

    # 8.10 ORDER TRACKING, RETURNS & BUYBACK WORKFLOWS
    add_heading_2(doc, "8.10 ORDER TRACKING, RETURNS & BUYBACK WORKFLOWS")
    add_screenshot(doc, get_media("image25.png"), "Fig 8.18 – Order Tracking Interface – Real-time progress bar with 10-second polling updates.")
    add_screenshot(doc, get_media("image26.png"), "Fig 8.19 – Return and Buyback Logistics Workflow – Return request interface.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides 10-second real-time tracking polling for physical book consignments and manages structured textbook return and buyback workflows."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• 10-Second Live Polling: ", "Client automatically polls order status every 10 seconds, reflecting dispatch updates in real time.")
    add_bullet_point(doc, "• Visual Stepper Progress: ", "Displays consignment progression through: Ordered → Dispatched → In Transit → Out for Delivery → Delivered.")
    add_bullet_point(doc, "• Return & Buyback Submission: ", "Allows buyers to initiate returns within eligible return windows with reason documentation.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Polling Efficiency: ", "Employs conditional HTTP headers and lightweight JSON payloads during status polling.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/orders/track/:trackingId", "Public endpoint returning live consignment stage and status."],
            ["POST", "/api/orders/:id/return", "Submits a textbook return or buyback request."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["return_requests", "index on orderId", "orderId, user, reason, status, pickupAddress"]
        ]
    )

    # 8.11 COMMUNITY DISCUSSION, AI STUDY ASSISTANT & MOTIVATION
    add_heading_2(doc, "8.11 COMMUNITY DISCUSSION, AI STUDY ASSISTANT & MOTIVATION")
    add_screenshot(doc, get_media("image27.png"), "Fig 8.20 – Student Community Discussion Interface – Question threads with upvotes and replies.")
    add_screenshot(doc, get_media("image28.png"), "Fig 8.21 – AI-Assisted Study Guidance Chatbot – Interactive AI academic advice.")
    add_screenshot(doc, get_media("image29.png"), "Fig 8.22 – Daily Motivation Interface – Daily inspirational quotes for exam focus.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Enhances peer learning through community discussion threads, offers contextual study roadmaps via an AI assistant chatbot, and sustains aspirant motivation through daily curated quotes."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Peer Q&A Forum: ", "Students post exam-specific queries, upvote insightful responses, and mark verified solutions.")
    add_bullet_point(doc, "• AI Study Chatbot: ", "Answers student queries regarding syllabus coverage, study schedules, and revision tactics.")
    add_bullet_point(doc, "• Daily Inspirational Quotes: ", "Serves refreshed inspirational academic quotations on daily login.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Sanitized User Content: ", "Sanitizes forum inputs to prevent stored Cross-Site Scripting (XSS).")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/community/discussions", "Returns discussion threads categorized by exam."],
            ["POST", "/api/community/discussions", "Publishes a new discussion question or query."],
            ["POST", "/api/chatbot/message", "Processes student query and returns AI roadmap advice."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["discussions", "indexes on examSlug, createdAt", "author, examSlug, title, body, upvotes, answers, resolved"]
        ]
    )

    # 8.12 UNIVERSAL THEME, PALETTE & ACCESSIBILITY CUSTOMIZATION
    add_heading_2(doc, "8.12 UNIVERSAL THEME, PALETTE & ACCESSIBILITY CUSTOMIZATION")
    add_screenshot(doc, get_media("image30.png"), "Fig 8.23 – Theme and Color Palette Customization – Custom button, text, and background colors.")
    add_screenshot(doc, get_media("image31.png"), "Fig 8.24 – Accessibility and Multi-Language Settings – Font scaling and language selector.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides a universal visual appearance customizer common to all user roles (Student, Mentor, Delivery Partner, Administrator) allowing granular adjustment of button colors, text colors, background colors, dark/light modes, font scaling, and multi-language translations."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Full Color Customizer: ", "Users independently customize button colors, text colors, and background theme colors via color pickers.")
    add_bullet_point(doc, "• Dark & Light Modes: ", "One-click toggle between optimized high-contrast light and dark visual themes.")
    add_bullet_point(doc, "• Font Size Scaling: ", "Scales application typography across Small, Medium, and Large sizing presets.")
    add_bullet_point(doc, "• Multi-Language Localization: ", "Translates interface labels across English, Tamil, and Hindi.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Universal Preference Persistence: ", "Preferences persist across sessions in the User document and apply immediately via CSS variables.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["PATCH", "/api/users/preferences", "Saves theme, palette, font size, and language settings to user profile."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["users", "embedded preferences sub-document", "preferences.theme, preferences.palette, preferences.fontSize, preferences.lang"]
        ]
    )

    # 8.13 ACADEMIC MENTOR PORTAL & AUTOMATED WHATSAPP ALERTS
    add_heading_2(doc, "8.13 ACADEMIC MENTOR PORTAL & AUTOMATED WHATSAPP ALERTS")
    add_screenshot(doc, get_media("image32.png"), "Fig 8.25 – Automated Academic Mentor Notifications – Real-time progress notifications.")
    add_screenshot(doc, get_media("image33.png"), "Fig 8.26 – Longitudinal Student Progress Analytics – Weekly, monthly, and yearly performance curves.")
    add_screenshot(doc, get_media("image34.png"), "Fig 8.27 – Identification of Students Requiring Academic Support – Lagging student detection.")
    add_screenshot(doc, get_media("image35.png"), "Fig 8.28 – Direct Academic Mentorship Communication – Mentorship messaging.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Equips academic mentors with tools to supervise assigned students, inspect longitudinal analytics curves, detect lagging performance, dispatch guidance, and receive automated WhatsApp, SMS, and email alerts on student activity."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Assigned Students View: ", "Mentors inspect all students assigned to them by the administrator, including active syllabus percentages.")
    add_bullet_point(doc, "• Automated WhatsApp Alerts: ", "Whenever a student attempts a mock test or logs in, an automated alert with performance metrics and a direct click-to-chat WhatsApp link is sent to the mentor.")
    add_bullet_point(doc, "• Longitudinal Analytics: ", "Mentors review weekly, monthly, and yearly syllabus completion and mock test trajectories per student.")
    add_bullet_point(doc, "• Lagging Student Detection: ", "The system flags students whose study velocity falls below recommended milestones.")
    add_bullet_point(doc, "• Direct Mentorship Messaging: ", "Mentors send direct motivation and guidance via WhatsApp and SMS.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Real-Time Dispatch: ", "Alerts dispatch within 3 seconds of student action without human administrative intervention.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/mentor/students", "Retrieves assigned students with syllabus completion rates and scores."],
            ["GET", "/api/mentor/students/:id/analytics", "Returns longitudinal weekly/monthly/yearly progress curves."],
            ["POST", "/api/mentor/message", "Dispatches direct motivational message to student via WhatsApp/SMS."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["users", "mentor index (MUL)", "mentor, assignedStudents, whatsappNumber, phone"]
        ]
    )

    # 8.14 DELIVERY PARTNER CONSOLE & 4-DIGIT OTP VERIFICATION
    add_heading_2(doc, "8.14 DELIVERY PARTNER CONSOLE & 4-DIGIT OTP VERIFICATION")
    add_screenshot(doc, get_media("image36.png"), "Fig 8.29 – Delivery Partner Consignment Dashboard – Assigned shipments and recipient details.")
    add_screenshot(doc, get_media("image37.png"), "Fig 8.30 – Order Lifecycle & Delivery Status Management – Order status progression.")
    add_screenshot(doc, get_media("image38.png"), "Fig 8.31 – Secure Delivery Confirmation Using OTP – 4-digit verification OTP prompt.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Enables delivery personnel to manage assigned consignments, advance fulfillment stages, and confirm physical deliveries or donation pickups using mandatory 4-digit OTP verification."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• Consignment Dashboard: ", "Displays shipments assigned to the authenticated delivery partner with recipient name, address, and phone number.")
    add_bullet_point(doc, "• Stage Transitions: ", "Advances consignments through: Ordered → Dispatched → In Transit → Out for Delivery → Delivered.")
    add_bullet_point(doc, "• Mandatory 4-Digit OTP Verification: ", "Delivery partners cannot complete a delivery without entering the recipient's 4-digit OTP, preventing fraudulent handovers.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• Cryptographic Validation: ", "OTPs are validated through constant-time string comparisons to prevent timing attacks.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/delivery/orders", "Returns consignments assigned to authenticated delivery partner."],
            ["PATCH", "/api/delivery/orders/:id/status", "Advances delivery stage; validates 4-digit OTP before marking Delivered."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["orders", "assignedPartner index (MUL)", "assignedPartner, status, verificationOtp, deliveryAddress"]
        ]
    )

    # 8.15 SYSTEM ADMINISTRATION & MULTI-CHANNEL COMMUNICATION ENGINE
    add_heading_2(doc, "8.15 SYSTEM ADMINISTRATION & MULTI-CHANNEL COMMUNICATION ENGINE")
    add_screenshot(doc, get_media("image39.png"), "Fig 8.32 – Administrative User Account Management – User governance and role assignment.")
    add_screenshot(doc, get_media("image40.png"), "Fig 8.33 – Academic Mentor Allocation Interface – Linking mentors with students.")
    add_screenshot(doc, get_media("image41.png"), "Fig 8.34 – Examination Catalog & Syllabus Administration – Syllabus curriculum editor.")
    add_screenshot(doc, get_media("image42.png"), "Fig 8.35 – Order & Fulfillment Monitoring – Order transactions and consignment monitoring.")
    add_screenshot(doc, get_media("image43.png"), "Fig 8.36 – Email Communication Module – Official emails dispatched from prepcycle@gmail.com.")
    add_screenshot(doc, get_media("image44.png"), "Fig 8.37 – WhatsApp Communication Module – Direct administrative messaging via WhatsApp.")

    add_heading_3(doc, "Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Equips administrators with full operational oversight of users, mentor allocations, exam catalogs, order fulfillment, return policies, and an active multi-channel communication engine operating via Email, WhatsApp, SMS, and in-app feeds."
    )

    add_heading_3(doc, "Functional Requirements")
    add_styled_paragraph(doc, "What the module must do:", first_line_indent=Inches(0.2))
    add_bullet_point(doc, "• User Governance: ", "Audit, activate, deactivate, and inspect all Student, Mentor, Delivery, and Admin accounts.")
    add_bullet_point(doc, "• Mentor Allocation: ", "Assign or reassign students to designated academic mentors, establishing supervisory linkages.")
    add_bullet_point(doc, "• Active Communication Engine: ", "Admins compose and send active Emails (dispatched from prepcycle@gmail.com), WhatsApp messages, and SMS notifications directly from the platform.")
    add_bullet_point(doc, "• Catalog & Order Oversight: ", "Create and edit competitive examinations, update syllabus roadmaps, and monitor consignment progress.")

    add_heading_3(doc, "Non-Functional Requirements")
    add_bullet_point(doc, "• High Throughput: ", "Processes multi-channel notification batches through asynchronous background queues without blocking admin UI.")

    add_heading_3(doc, "API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / contract"],
        [
            ["GET", "/api/admin/users", "Lists all registered accounts with role filters and account status."],
            ["POST", "/api/admin/assign-mentor", "Links a student account to a designated academic mentor."],
            ["POST", "/api/admin/communicate", "Dispatches an active Email, WhatsApp message, or SMS to target users."],
            ["GET", "/api/admin/analytics", "Aggregates total students, mock attempts, active orders, and mentor coverage."]
        ]
    )

    add_heading_3(doc, "DB Design")
    format_grid_table(
        doc, ["Collection", "Keys & indexes", "Key fields"],
        [
            ["communication_logs", "indexes on channel, timestamp", "user, channel, messageType, recipient, subject, content, status"]
        ]
    )

    # 8.16 ROLE-WISE USER INTERFACES
    add_heading_2(doc, "8.16 ROLE-WISE USER INTERFACES")
    add_styled_paragraph(
        doc,
        "This section presents the specialized role-based user interfaces designed for the four operational stakeholders of the platform: Student, Academic Mentor, Delivery Partner, and System Administrator. Each role interface provides a focused set of functional capabilities and telemetry displays tailored to the user's operational workflows."
    )

    add_heading_3(doc, "8.16.1 Student Role Interfaces")
    add_styled_paragraph(
        doc,
        "The Student workspace provides an integrated learning, assessment, and resource exchange environment. Students explore competitive examination roadmaps, track syllabus completion percentages, maintain daily study streaks, participate in timed computer-based mock tests, generate dynamic quizzes, revise with interactive flashcards, buy and sell second-hand textbooks, claim free book donations, track physical orders, and engage in peer discussions:"
    )
    add_screenshot(doc, get_media("image9.png"), "Fig 8.38 – Student Dashboard – Central learning overview with recently accessed exams and streak metrics.")
    add_screenshot(doc, get_media("image13.png"), "Fig 8.39 – Exam Explorer & Selection – Browsing national competitive exam catalogs.")
    add_screenshot(doc, get_media("image14.png"), "Fig 8.40 – Syllabus Roadmap View – Weightage-prioritized chapters and topics.")
    add_screenshot(doc, get_media("image17.png"), "Fig 8.41 – Computer-Based Mock Test Simulator – Realistic timed examination environment.")
    add_screenshot(doc, get_media("image21.png"), "Fig 8.42 – Peer-to-Peer Marketplace – Educational textbook resale and donation listings.")

    add_heading_3(doc, "8.16.2 Academic Mentor Role Interfaces")
    add_styled_paragraph(
        doc,
        "The Academic Mentor portal provides supervisory oversight of assigned students. Mentors review student preparation velocity, inspect longitudinal weekly, monthly, and yearly analytics curves, detect lagging indicators, initiate direct guidance via WhatsApp or SMS, and receive real-time automated progress alerts upon student mock test submissions or daily logins:"
    )
    add_screenshot(doc, get_media("image11.png"), "Fig 8.43 – Academic Mentor Dashboard – Overview of assigned students and preparation progress.")
    add_screenshot(doc, get_media("image33.png"), "Fig 8.44 – Longitudinal Student Progress Curves – Detailed study trajectories and score analysis.")
    add_screenshot(doc, get_media("image34.png"), "Fig 8.45 – Lagging Student Identification Panel – Proactive detection of students requiring academic intervention.")

    add_heading_3(doc, "8.16.3 Delivery Partner Role Interfaces")
    add_styled_paragraph(
        doc,
        "The Delivery Partner console coordinates physical doorstep textbook deliveries, return pickups, and donation transfers. Delivery personnel manage assigned consignments, advance delivery stages through structured lifecycle transitions, and confirm handovers using mandatory recipient 4-digit OTP verification:"
    )
    add_screenshot(doc, get_media("image12.png"), "Fig 8.46 – Delivery Partner Dashboard – Overview of active consignments and routes.")
    add_screenshot(doc, get_media("image36.png"), "Fig 8.47 – Consignment Shipment Manifest – Detailed recipient contact and address information.")
    add_screenshot(doc, get_media("image38.png"), "Fig 8.48 – 4-Digit OTP Verification Screen – Secure delivery handover confirmation.")

    add_heading_3(doc, "8.16.4 System Administrator Role Interfaces")
    add_styled_paragraph(
        doc,
        "The Administrator console equips platform managers with complete operational authority over user accounts, mentor allocations, examination catalogs, order tracking, and an active multi-channel communication engine operating via Email (prepcycle@gmail.com), WhatsApp, and SMS:"
    )
    add_screenshot(doc, get_media("image10.png"), "Fig 8.49 – System Administration Console – Platform-wide operational statistics and user telemetry.")
    add_screenshot(doc, get_media("image39.png"), "Fig 8.50 – User Account Management – Role-based user auditing and permission configuration.")
    add_screenshot(doc, get_media("image40.png"), "Fig 8.51 – Academic Mentor Allocation – Dynamic linking of mentors with enrolled students.")
    add_screenshot(doc, get_media("image43.png"), "Fig 8.52 – Multi-Channel Email Dispatcher – Official email communication from prepcycle@gmail.com.")
    add_screenshot(doc, get_media("image44.png"), "Fig 8.53 – Multi-Channel WhatsApp Dispatcher – Real-time administrative messaging via WhatsApp.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 9: CONCLUSION & FUTURE ENHANCEMENTS (PAGE 58)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 9\nCONCLUSION")

    add_styled_paragraph(
        doc,
        "In conclusion, the Multi-Exam Preparation and Resource Exchange Platform (PrepCycle) provides a robust, scalable, and user-centric solution addressing the key challenges of competitive examination preparation and educational resource scarcity. By uniting multi-tier syllabus exploration, weightage-based roadmaps, continuous mock test tracking, automated academic mentorship via real-time WhatsApp alerts, a circular textbook marketplace, and doorstep logistics with OTP verification, the system replaces fragmented, manual workflows with an integrated, data-driven web environment."
    )

    add_styled_paragraph(
        doc,
        "The application was architected following modern full-stack engineering standards utilizing React.js with Vite for the frontend presentation tier, Node.js with Express.js for the RESTful API service tier, and MongoDB with Mongoose for resilient, scalable NoSQL document persistence. JWT authentication, salted bcrypt password encryption, role-based access control across four distinct user roles, request rate limiting, and HTTP security headers ensure enterprise-grade security."
    )

    add_styled_paragraph(
        doc,
        "Students benefit from structured roadmaps, streak motivation, and affordable textbooks; Academic Mentors maintain continuous supervisory oversight with automated alerts; Delivery Partners manage consignments with cryptographic OTP verification; and Administrators govern the platform with an active multi-channel communication engine. The completed platform demonstrates how modern web technologies can optimize academic learning, reduce educational expenditure through circular textbook sharing, and improve examination performance outcomes."
    )

    add_heading_2(doc, "9.1 Future Enhancements")
    add_bullet_point(doc, "• Machine Learning Question Recommendations: ", "Integrating adaptive learning algorithms that dynamically generate practice questions based on a student's historical error patterns and weak syllabus domains.")
    add_bullet_point(doc, "• Native Mobile Application: ", "Developing cross-platform mobile clients using React Native to offer push notifications and offline study mode.")
    add_bullet_point(doc, "• Live Proctoring for Mock Tests: ", "Incorporating AI-assisted webcam proctoring to conduct authenticated national-level mock tests.")
    add_bullet_point(doc, "• Geolocation Route Optimization: ", "Implementing GPS routing algorithms for delivery partners to optimize multi-stop book delivery runs.")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 10: REFERENCES (PAGE 59)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 10\nREFERENCES")

    refs = [
        "1. V. Subramanian, \"Full Stack Web Development with React and Node.js: Architectural Patterns and Best Practices,\" IEEE Transactions on Learning Technologies, vol. 15, no. 3, pp. 312–326, 2022.",
        "2. K. Patel and R. Sharma, \"Role-Based Access Control and Tokenized Security in Modern Web Architectures,\" International Journal of Computer Applications, vol. 182, no. 45, pp. 28–35, 2021.",
        "3. M. Banka and D. Chitra, \"Design and Evaluation of Adaptive Computer-Based Examination Platforms for Competitive Testing,\" Journal of Educational Computing Research, vol. 59, no. 6, pp. 1140–1162, 2021.",
        "4. A. Kumar and S. Sengupta, \"Circular Economy in Academic Resources: Peer-to-Peer Educational Material Redistribution Networks,\" Sustainability in Higher Education, vol. 24, no. 2, pp. 88–104, 2023.",
        "5. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 4th ed. Cambridge, MA, USA: MIT Press, 2022.",
        "6. E. Gamma, R. Helm, R. Johnson, and J. Vlissides, Design Patterns: Elements of Reusable Object-Oriented Software. Reading, MA, USA: Addison-Wesley, 1994.",
        "7. World Wide Web Consortium, \"Web Content Accessibility Guidelines (WCAG) 2.1,\" W3C Recommendation, 2018. [Online]. Available: https://www.w3.org/TR/WCAG21/",
        "8. MongoDB Inc., \"MongoDB Architecture Guide: Scalable NoSQL Document Persistence and Sharding,\" MongoDB Technical Documentation, 2024. [Online]. Available: https://www.mongodb.com/docs/"
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)

    # Save output file
    target_path = os.path.join(ROOT_DIR, "final_mwt_el_report.docx")
    doc.save(target_path)
    print(f"Report generated successfully at: {target_path}")

if __name__ == "__main__":
    generate_full_report()
