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
COMPASS_DIR = r"c:\Users\haren\OneDrive\Desktop\mwtfinalel\compass_tables"

def get_media(fname):
    return os.path.join(MEDIA_DIR, fname)

def get_root(fname):
    return os.path.join(ROOT_DIR, fname)

def get_compass(fname):
    return os.path.join(COMPASS_DIR, fname)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=70, bottom=70, left=90, right=90):
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

def add_styled_paragraph(doc, text="", style='Normal', space_after=5, space_before=0, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.5)):
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
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(10)
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
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
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
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
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
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(1)
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
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run(caption)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.italic = True
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)

def format_grid_table(doc, headers, rows):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, "A0A0A0")

    for col_idx, h_text in enumerate(headers):
        cell = table.rows[0].cells[col_idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=55, bottom=55, left=75, right=75)
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
            set_cell_margins(cell, top=40, bottom=40, left=75, right=75)
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

def build_report_with_toc(toc_page_map=None):
    if toc_page_map is None:
        toc_page_map = {
            "1": "3", "2": "4", "3": "5", "4": "6", "5": "7",
            "6": "13", "7": "14", "8": "15", "9": "58", "10": "59"
        }

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
    # SECTION 2: BONAFIDE (PAGE 1) & NUMBERED BODY
    # -------------------------------------------------------------------------
    sec2 = doc.add_section()
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    setup_page_number_footer(sec2, start_number=1)

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
        ("1", "INTRODUCTION", toc_page_map.get("1", "3")),
        ("2", "OBJECTIVES", toc_page_map.get("2", "4")),
        ("3", "DESCRIPTION", toc_page_map.get("3", "5")),
        ("4", "CLASS DIAGRAM", toc_page_map.get("4", "6")),
        ("5", "TABLE STRUCTURES", toc_page_map.get("5", "7")),
        ("6", "ER DIAGRAM", toc_page_map.get("6", "13")),
        ("7", "TECH STACK", toc_page_map.get("7", "14")),
        ("8", "MODULES", toc_page_map.get("8", "15")),
        ("9", "CONCLUSION", toc_page_map.get("9", "58")),
        ("10", "REFERENCE", toc_page_map.get("10", "59")),
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
        "The Multi-Exam Preparation and Resource Exchange Platform (PrepCycle) is a web-based application developed to bring students, aspirants, academic mentors, delivery personnel and administrators together on a single digital platform. It is designed to replace the scattered, manual ways in which competitive exam preparation is conducted today, such as unverified study resources, isolated revision schedules, messaging channels and paper records. The system provides multiple types of users: Student, Academic Mentor, Delivery Partner and Administrator, each having specific roles and access privileges."
    )

    add_styled_paragraph(
        doc,
        "Students can explore structured exam catalogs, track syllabus topics with weightage-prioritized roadmaps (High, Medium, and Low), maintain daily study streaks, record activity heatmaps, take timed computer-based mock tests, generate dynamic quizzes and revise with interactive flashcards. In the marketplace, students can list surplus reference books for resale, purchase pre-owned textbooks, or donate books to junior aspirants for free. Academic Mentors receive automated alerts via WhatsApp, SMS, and email whenever an assigned student completes a mock test or logs in, while Delivery Partners coordinate physical book handovers using 4-digit OTP verification."
    )

    add_styled_paragraph(
        doc,
        "The system maintains accurate academic progress, mock score analytics and textbook order records, reduces study friction and saves time. It also enhances trust and transparency through JWT-based authentication, Google OAuth sign-in and automated mentor notifications. All information is stored in a MongoDB database, and the user interface supports light/dark themes, full color palette customizability, font scaling, and multiple languages. This system is useful for colleges, coaching institutions and aspirant communities that want to connect structured learning, mentorship and educational resources in a more organized and efficient manner."
    )

    add_styled_paragraph(
        doc,
        "The report is organized as follows. Chapters 2 and 3 state the objectives and describe the system. Chapters 4 to 6 present the class diagram, the collection structures and the ER diagram. Chapter 7 lists the technology stack, and Chapter 8 describes the folder structure, every functional module and the role-wise user interfaces. Chapter 9 concludes the report."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 2: OBJECTIVES (PAGE 4)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 2\nOBJECTIVES")

    add_bullet_point(doc, "• To provide role-based authentication and authorization using JWT and bcrypt-hashed ",
                     "passwords, with an additional Google OAuth 2.0 sign-in option.")
    
    add_bullet_point(doc, "• To maintain a centralized MongoDB database that stores all users, exams, progress, ",
                     "mock attempts, products, orders, order items and communication logs.")

    add_bullet_point(doc, "• To allow Students to explore national competitive examination catalogs and follow ",
                     "weightage-based syllabus roadmaps organized into High, Medium, and Low priorities.")

    add_bullet_point(doc, "• To track individual study progress, compute completion percentages, calculate daily streaks ",
                     "and display a 365-day calendar activity heatmap.")

    add_bullet_point(doc, "• To provide timed computer-based mock tests with instant score computation, performance ",
                     "analytics, dynamic quiz generation and interactive 3D revision flashcards.")

    add_bullet_point(doc, "• To facilitate a circular textbook marketplace allowing students to buy and sell pre-owned ",
                     "educational reference materials or donate books to junior aspirants for free.")

    add_bullet_point(doc, "• To streamline doorstep logistics fulfillment with real-time 10-second polling updates and ",
                     "mandatory 4-digit OTP verification upon physical delivery.")

    add_bullet_point(doc, "• To dispatch automated real-time progress notifications to assigned mentors via WhatsApp, ",
                     "SMS, and email upon student mock test submission or daily login.")

    add_bullet_point(doc, "• To equip administrators with comprehensive user governance, mentor allocation controls, ",
                     "and an active multi-channel communication engine.")

    add_bullet_point(doc, "• To provide a universally accessible interface with light and dark themes, full color palette ",
                     "customization, font scaling, and multi-language support (English, Tamil, Hindi).")

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 3: DESCRIPTION (PAGE 5)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 3\nDESCRIPTION")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform is a web-based application designed to connect students, academic mentors, delivery partners and administrators efficiently within a single academic and commerce network. The system includes multiple types of users: Student, Academic Mentor, Delivery Partner and Administrator. Students can enroll in competitive exams, follow weightage-ranked roadmaps, attempt timed mock tests, and exchange textbooks, while mentors monitor student progress curves and delivery partners coordinate physical book deliveries. All information is stored securely in a database for easy access and management."
    )

    add_styled_paragraph(
        doc,
        "1. Identity and Access: Registration, login, Google OAuth and the JWT-protected API give each of the four roles access only to the pages and actions meant for it."
    )

    add_styled_paragraph(
        doc,
        "2. Academic Preparation & Syllabus Exploration: Exams, progress, mock attempts, dynamic quizzes, and flashcards form the learning workflow. Each step is stored in its own collection so that it can be edited and traced independently."
    )

    add_styled_paragraph(
        doc,
        "3. Mentorship and Automated Tracking: Automated alerts notify mentors via WhatsApp, SMS, and email whenever students complete mock tests or log in, ensuring proactive academic supervision."
    )

    add_styled_paragraph(
        doc,
        "4. Circular Commerce & Book Circulation: Products, orders, and order items form the marketplace workflow. Students buy and sell pre-owned textbooks or donate them for free."
    )

    add_styled_paragraph(
        doc,
        "5. Doorstep Logistics & Security: Orders are tracked with 10-second real-time polling updates, and deliveries are validated via mandatory 4-digit OTP verification."
    )

    add_styled_paragraph(
        doc,
        "6. Administration & Governance: The Administrator monitors the whole platform through a dedicated dashboard, allocates mentors to students, and communicates via email, WhatsApp, and SMS."
    )

    add_heading_2(doc, "3.1 Access Permission of Roles")
    add_styled_paragraph(
        doc,
        "To ensure robust data isolation, integrity, and security, the application enforces strict Role-Based Access Control (RBAC). JSON Web Tokens carry authenticated user role claims that are validated on every API request via authentication middleware and client-side ProtectedRoute route guards. The diagram below details the comprehensive access permission matrix across all four platform roles:"
    )

    access_img = get_root("access_permission_roles_bw.png")
    if not os.path.exists(access_img):
        access_img = get_media("image2.png")
    add_screenshot(doc, access_img, "Fig 3.1 – Access Permission of Roles and Security Authorization Matrix.", width_inches=6.0)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 4: CLASS DIAGRAM (PAGE 6)
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 4\nCLASS DIAGRAM")

    add_styled_paragraph(
        doc,
        "The diagram illustrates the database structure of the Multi-Exam Preparation and Resource Exchange Platform. The central User entity is connected to Exam, Progress, MockAttempt, Product, Order, OrderItem, CommunicationLog, Discussion and Notification. These entities store user credentials, study roadmaps, test scores, commerce listings, order states and message logs. Primary keys (PK) uniquely identify records, while foreign keys (FK) establish relationships between entities."
    )

    class_img = get_root("class_diagram_bw.png")
    if not os.path.exists(class_img):
        class_img = get_media("image3.png")
    add_screenshot(doc, class_img, "Fig 4.1 – Class Diagram – Entities of the platform with their attributes and relationships.", width_inches=6.0)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 5: TABLE STRUCTURES (PAGE 7-12)
    # Exact wording, exact structure, exact Compass table screenshots matching sample PDF!
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 5\nTABLE STRUCTURES")

    # Exact 28 words matching sample PDF
    add_styled_paragraph(
        doc,
        "The application stores each data type in its own MongoDB collection of the prepcycle database, and every item is a document. The structure of each collection is given below."
    )

    # 5.1 MongoDB Collections (Exact 18 words)
    add_heading_2(doc, "5.1 MongoDB Collections")
    add_styled_paragraph(
        doc,
        "The collections available in MongoDB are displayed in the below image along with average data size, Documents etc…"
    )
    add_screenshot(doc, get_compass("fig_5_1_collections.png"), "Fig 5.1 – MongoDB Compass – Collections of the prepcycle database", width_inches=5.9)

    doc.add_page_break()

    # ---------------- PAGE 8 OF SAMPLE (PAGE 9 IN REPORT) ----------------
    # 5.2 Users (Exact 15 words)
    add_heading_2(doc, "5.2 Users:")
    add_styled_paragraph(
        doc,
        "Stores every account of the portal with its role, authentication method, verified flag and connections."
    )
    add_screenshot(doc, get_compass("table_5_2_users.png"), "Table 5.2 – Structure of the users table", width_inches=5.9)

    # 5.3 Exams (Exact 14 words)
    add_heading_2(doc, "5.3 Exams:")
    add_styled_paragraph(
        doc,
        "Stores the competitive exam profiles published by conducting authorities, with full syllabus details."
    )
    add_screenshot(doc, get_compass("table_5_3_exams.png"), "Table 5.3 – Structure of the exams table", width_inches=5.9)

    doc.add_page_break()

    # ---------------- PAGE 9 OF SAMPLE (PAGE 10 IN REPORT) ----------------
    # 5.4 Progress (Exact 10 words)
    add_heading_2(doc, "5.4 Progress:")
    add_styled_paragraph(
        doc,
        "Stores the study progress tracked by students, with streak records."
    )
    add_screenshot(doc, get_compass("table_5_4_progress.png"), "Table 5.4 – Structure of the progress table", width_inches=5.9)

    # 5.5 Mock Attempts (Exact 16 words)
    add_heading_2(doc, "5.5 Mock Attempts:")
    add_styled_paragraph(
        doc,
        "Stores each mock attempt with the student, the tested chapter, the marks, type, date and notes."
    )
    add_screenshot(doc, get_compass("table_5_5_mock_attempts.png"), "Table 5.5 – Structure of the mock_attempts table", width_inches=5.9)

    # 5.6 Products header (Exact 10 words)
    add_heading_2(doc, "5.6 Products:")
    add_styled_paragraph(
        doc,
        "Stores the textbooks listed for students together with the condition verdict."
    )

    doc.add_page_break()

    # ---------------- PAGE 10 OF SAMPLE (PAGE 11 IN REPORT) ----------------
    # 5.6 Products Table image + caption
    add_screenshot(doc, get_compass("table_5_6_products.png"), "Table 5.6 – Structure of the products table", width_inches=5.9)

    # 5.7 Orders (Exact 10 words)
    add_heading_2(doc, "5.7 Orders:")
    add_styled_paragraph(
        doc,
        "Stores the purchase orders (COD or UPI) sent between members."
    )
    add_screenshot(doc, get_compass("table_5_7_orders.png"), "Table 5.7 – Structure of the orders table", width_inches=5.9)

    # 5.8 Order Items (Exact 11 words)
    add_heading_2(doc, "5.8 Order Items:")
    add_styled_paragraph(
        doc,
        "Stores the order items generated from a purchase or an accepted order."
    )
    add_screenshot(doc, get_compass("table_5_8_order_items.png"), "Table 5.8 – Structure of the order_items table", width_inches=5.9)

    # 5.9 Communication Logs (Exact 6 words)
    add_heading_2(doc, "5.9 Communication Logs:")
    add_styled_paragraph(
        doc,
        "Stores the communication alerts between members."
    )

    doc.add_page_break()

    # ---------------- PAGE 11 OF SAMPLE (PAGE 12 IN REPORT) ----------------
    # 5.9 Communication Logs Table image + caption
    add_screenshot(doc, get_compass("table_5_9_communication_logs.png"), "Table 5.9 – Structure of the communication_logs table", width_inches=5.9)

    # 5.10 Discussions (Exact 7 words)
    add_heading_2(doc, "5.10 Discussions:")
    add_styled_paragraph(
        doc,
        "Stores the community questions exchanged between members."
    )
    add_screenshot(doc, get_compass("table_5_10_discussions.png"), "Table 5.10 – Structure of the discussions table", width_inches=5.9)

    # 5.11 Notifications (Exact 10 words)
    add_heading_2(doc, "5.11 Notifications:")
    add_styled_paragraph(
        doc,
        "Stores the notifications hosted in the portal and their deliveries."
    )
    add_screenshot(doc, get_compass("table_5_11_notifications.png"), "Table 5.11 – Structure of the notifications table", width_inches=5.9)

    # 5.12 Return Requests header (Exact 7 words)
    add_heading_2(doc, "5.12 Return Requests:")
    add_styled_paragraph(
        doc,
        "Stores the return requests posted by students."
    )

    doc.add_page_break()

    # ---------------- PAGE 12 OF SAMPLE (PAGE 13 IN REPORT) ----------------
    # 5.12 Return Requests Table image + caption
    add_screenshot(doc, get_compass("table_5_12_return_requests.png"), "Table 5.12 – Structure of the return_requests table", width_inches=5.9)

    # 5.13 Flashcards (Exact 9 words)
    add_heading_2(doc, "5.13 Flashcards:")
    add_styled_paragraph(
        doc,
        "Stores the revision flashcards created for registered competitive exams."
    )
    add_screenshot(doc, get_compass("table_5_13_flashcards.png"), "Table 5.13 – Structure of the flashcards table", width_inches=5.9)

    # 5.14 Notes (Exact 8 words)
    add_heading_2(doc, "5.14 Notes:")
    add_styled_paragraph(
        doc,
        "Stores the study notes and summaries uploaded by members."
    )
    add_screenshot(doc, get_compass("table_5_14_notes.png"), "Table 5.14 – Structure of the notes table", width_inches=5.9)

    # 5.15 Recently Accessed (Exact 8 words)
    add_heading_2(doc, "5.15 Recently Accessed:")
    add_styled_paragraph(
        doc,
        "Stores the last visited profiles of each user."
    )
    add_screenshot(doc, get_compass("table_5_15_recently_accessed.png"), "Table 5.15 – Structure of the recently_accessed table", width_inches=5.9)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 6: ER DIAGRAM (PAGE 13 IN SAMPLE)
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

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 7: TECH STACK (PAGE 14 IN SAMPLE)
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
    # CHAPTER 9: CONCLUSION & FUTURE ENHANCEMENTS
    # -------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 9\nCONCLUSION")

    add_styled_paragraph(
        doc,
        "In conclusion, the Multi-Exam Preparation and Resource Exchange Platform provides a simple and effective solution for connecting students, academic mentors, delivery partners and administrators in a digital learning environment. It reduces the need for manual coordination and streamlines exam syllabus tracking, timed mock testing, peer textbook sharing and doorstep order fulfillment. By offering role-based access with JWT authentication and Google OAuth, the system keeps every user's data protected."
    )

    add_styled_paragraph(
        doc,
        "Students can explore weightage-ranked roadmaps, attempt computer-based mock tests, trade pre-owned textbooks and ask community questions; Mentors can supervise assigned students, inspect longitudinal progress curves and receive automated WhatsApp alerts; Delivery Partners can fulfill orders securely using 4-digit OTP verification; and Administrators can govern users, allocate mentors and dispatch multi-channel communications. The multi-language interface and full color customizer make the platform accessible to a wider community. The system helps maintain accurate academic records, improves trust and saves time. Overall, it is a valuable tool for the competitive examination ecosystem to manage learning, supervision and educational resources in an organized and efficient manner."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 10: REFERENCES
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

    target_path = os.path.join(ROOT_DIR, "final_mwt_el_report.docx")
    doc.save(target_path)
    return target_path

def get_word_page_numbers(docx_path):
    import win32com.client
    word = None
    doc = None
    mapping = {}
    try:
        abs_path = os.path.abspath(docx_path)
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(abs_path)
        
        chapters = {
            'CHAPTER 1': '1', 'CHAPTER 2': '2', 'CHAPTER 3': '3',
            'CHAPTER 4': '4', 'CHAPTER 5': '5', 'CHAPTER 6': '6',
            'CHAPTER 7': '7', 'CHAPTER 8': '8', 'CHAPTER 9': '9',
            'CHAPTER 10': '10'
        }
        
        for p in doc.Paragraphs:
            t = p.Range.Text.strip()
            for ch_prefix, ch_num in chapters.items():
                if ch_num not in mapping and ch_prefix in t:
                    pg = p.Range.Information(3) # wdActiveEndPageNumber
                    displayed_pg = pg - 1 if pg > 1 else 1
                    mapping[ch_num] = str(displayed_pg)
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
    return mapping

if __name__ == '__main__':
    print("Step 1: Building initial report with authentic MongoDB Compass tables...")
    doc_path = build_report_with_toc()
    
    print("Step 2: Calibrating Table of Contents from Word COM statistics...")
    try:
        page_map = get_word_page_numbers(doc_path)
        print("Detected displayed page numbers:", page_map)
        
        print("Step 3: Rebuilding report with calibrated TOC...")
        build_report_with_toc(page_map)
        print("Report generation and calibration finished successfully!")
    except Exception as e:
        print("Could not automate Word for page lookup:", e)
