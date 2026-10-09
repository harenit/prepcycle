import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from report_helpers_bw import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_styled_paragraph, add_heading_1, add_heading_2, add_heading_3,
    add_bullet_point, add_screenshot, format_schema_table, format_grid_table
)

def create_final_report():
    doc = Document()

    # Academic Project Report Margins (Anna University / NEC standard)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4 standard
        section.page_height = Inches(11.69)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(18)
    r = p_title.add_run("MULTI-EXAM PREPARATION AND RESOURCE EXCHANGE PLATFORM")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(40)
    r = p_course.add_run("23CS54C – MODERN WEB TECHNOLOGIES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    r = p_sub.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.italic = True
    r.font.bold = True

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(48)
    r = p_author.add_run("HARENI T 24104005")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_degree = doc.add_paragraph()
    p_degree.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_degree.paragraph_format.space_before = Pt(20)
    p_degree.paragraph_format.space_after = Pt(6)
    r = p_degree.add_run("In partial fulfillment for the award of the degree\nof\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True
    
    r_deg = p_degree.add_run("BACHELOR OF ENGINEERING\nin\nCOMPUTER SCIENCE AND ENGINEERING")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(13)
    r_deg.font.bold = True

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(64)
    p_inst.paragraph_format.space_after = Pt(36)
    
    r = p_inst.add_run("NATIONAL ENGINEERING COLLEGE\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    r2 = p_inst.add_run("(An Autonomous Institution affiliated to Anna University, Chennai)\nK.R.NAGAR, KOVILPATTI - 628503\n\nOCTOBER - 2026")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE
    # =========================================================================
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(24)
    p_c1.paragraph_format.space_after = Pt(6)
    r = p_c1.add_run("NATIONAL ENGINEERING COLLEGE\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    r = p_c1.add_run("(An Autonomous Institution affiliated to Anna University, Chennai)\nK.R.NAGAR, KOVILPATTI - 628503")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_bona = doc.add_paragraph()
    p_bona.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bona.paragraph_format.space_before = Pt(40)
    p_bona.paragraph_format.space_after = Pt(30)
    r = p_bona.add_run("BONAFIDE CERTIFICATE")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.6
    p_cert.paragraph_format.first_line_indent = Inches(0.5)
    p_cert.paragraph_format.space_after = Pt(72)
    r = p_cert.add_run("This is to certify that this project report, ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    
    r_bold = p_cert.add_run("“MULTI-EXAM PREPARATION AND RESOURCE EXCHANGE PLATFORM”")
    r_bold.font.name = 'Times New Roman'
    r_bold.font.size = Pt(12)
    r_bold.font.bold = True

    r_rem = p_cert.add_run(", is the bonafide work of ")
    r_rem.font.name = 'Times New Roman'
    r_rem.font.size = Pt(12)

    r_stu = p_cert.add_run("T HARENI (24104005)")
    r_stu.font.name = 'Times New Roman'
    r_stu.font.size = Pt(12)
    r_stu.font.bold = True

    r_end = p_cert.add_run(" who carried out the project work under my supervision.")
    r_end.font.name = 'Times New Roman'
    r_end.font.size = Pt(12)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_guide.paragraph_format.space_after = Pt(64)
    r = p_guide.add_run("Course Instructor/Guide")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_viva = doc.add_paragraph()
    p_viva.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_viva.paragraph_format.line_spacing = 1.3
    p_viva.paragraph_format.space_after = Pt(48)
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

    # =========================================================================
    # PAGE 3: TABLE OF CONTENTS
    # =========================================================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(18)
    p_toc.paragraph_format.space_after = Pt(24)
    r = p_toc.add_run("TABLE OF CONTENTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    toc_items = [
        ("1", "INTRODUCTION", "3"),
        ("2", "OBJECTIVES", "4"),
        ("3", "DESCRIPTION & ACCESS PERMISSION OF ROLES", "5"),
        ("4", "CLASS DIAGRAM", "7"),
        ("5", "TABLE STRUCTURES / SCHEMA SPECIFICATIONS", "8"),
        ("6", "ER DIAGRAM", "17"),
        ("7", "TECH STACK & ARCHITECTURE OVERVIEW", "19"),
        ("8", "MODULES", "20"),
        ("", "8.1 Project Structure (Backend & Frontend Organization)", "20"),
        ("", "8.2 User Authentication & Access Control (Login & Google OAuth)", "22"),
        ("", "8.3 Student Module & Learning Features", "24"),
        ("", "8.4 Academic Mentor Module & Monitoring Features", "30"),
        ("", "8.5 Delivery Partner Logistics Module", "33"),
        ("", "8.6 System Administration & Multi-Channel Communication Engine", "36"),
        ("9", "CONCLUSION", "39"),
    ]

    t_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_toc, "A0A0A0")
    
    h1, h2, h3 = t_toc.rows[0].cells
    h1.width = Inches(1.1)
    h2.width = Inches(4.5)
    h3.width = Inches(1.0)
    h1.text = "CH NO"
    h2.text = "TITLE"
    h3.text = "PAGE NO"
    for cell in [h1, h2, h3]:
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
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
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if ch in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    run.font.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0)
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c3.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 1\nINTRODUCTION")
    
    add_styled_paragraph(
        doc,
        "In the modern education ecosystem, the structured preparation for competitive examinations plays a vital role in determining student career progression and higher academic achievements. Millions of aspirants preparing for engineering, medical, civil services, management, and technical examinations in India—including GATE, UPSC, JEE, NEET, and CAT—face severe fragmentation of learning resources, prohibitive textbook expenses, lack of personalized progress tracking, and disconnected mentorship. Managing preparation across isolated syllabus PDFs, disparate practice portals, physical book purchases, and manual revision logs is time-consuming, disorganized, and lacks real-time academic accountability."
    )

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform is a comprehensive, full-stack web application designed to digitize and unify the complete lifecycle of competitive examination preparation. The platform establishes a cohesive ecosystem integrating official examination roadmaps, hierarchical subject and chapter syllabus tracking, multi-attempt mock test evaluation, automated academic mentor monitoring with real-time WhatsApp and SMS notifications, a circular peer-to-peer textbook marketplace, and doorstep delivery logistics."
    )

    add_styled_paragraph(
        doc,
        "The application is organized into three major functional domains: Academic & Examination Management, which covers foundational exam catalogs, official syllabus roadmaps with weightage prioritization (High, Medium, Low), interactive revision flashcards, and automated quiz generation; Student Progress & Mentorship Tracking, which provides continuous topic status tracking, daily study streaks, mock test analytics, and instant notification alerts dispatched to assigned academic mentors; and Circular Commerce & Logistics, which facilitates peer-to-peer textbook resale, free material donations, cart checkout with multiple payment modes, and doorstep delivery partner fulfillment protected by verification OTPs."
    )

    add_styled_paragraph(
        doc,
        "The system is developed using modern web engineering principles featuring React.js with Vite for a high-performance single-page application frontend, Node.js with Express.js for the RESTful API backend, and MongoDB with Mongoose for resilient NoSQL persistence. It is supported by automated containerization and deployment pipelines, making it production-ready, maintainable, and horizontally scalable. This report documents the architecture, database schema, component designs, API specifications, and operational workflows of the platform."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: OBJECTIVES
    # =========================================================================
    add_heading_1(doc, "CHAPTER 2\nOBJECTIVES")

    add_bullet_point(doc, "To Digitize Competitive Exam Preparation: ",
                     "Replace fragmented study logs and manual tracking with a unified, digital roadmap platform that provides complete syllabus transparency and structured guidance.")
    
    add_bullet_point(doc, "To Enforce Multi-Role Security & RBAC: ",
                     "Secure user accounts using JSON Web Tokens (JWT) and salted bcrypt password hashing, supporting distinct roles for Student, Academic Mentor, Administrator, and Delivery Partner with protected route boundaries.")
    
    add_bullet_point(doc, "To Provide Weightage-Based Syllabus Roadmaps: ",
                     "Organize complex technical syllabi into hierarchical subjects, chapters, and topics ordered by weightage (High, Medium, Low) while retaining every topic to ensure structured preparation without content omission.")
    
    add_bullet_point(doc, "To Automate Academic Mentor Notifications: ",
                     "Ensure continuous student supervision by automatically dispatching alerts to assigned mentors via WhatsApp, SMS, Email, and in-app feeds whenever a student completes a mock test, logs in for daily study, or finishes an entire subject.")
    
    add_bullet_point(doc, "To Track Multi-Attempt Mock Analytics & Streaks: ",
                     "Capture test scores, maximum marks, attendance dates, and percentage progressions across repeated attempts, computing daily study streaks and performance trends.")
    
    add_bullet_point(doc, "To Build a Circular Economy Resource Marketplace: ",
                     "Allow students to purchase pre-owned verified reference books, list surplus study materials for resale, or donate physical textbooks to junior aspirants.")
    
    add_bullet_point(doc, "To Streamline Doorstep Order Fulfillment: ",
                     "Provide a dedicated delivery partner interface to accept orders, manage route dispatch, and confirm physical deliveries and donation pickups using mandatory 4-digit OTP verification.")
    
    add_bullet_point(doc, "To Foster Peer Learning and AI Guidance: ",
                     "Incorporate a student community discussion board with question upvoting and best-reply badges, complemented by a context-aware AI chatbot assisting students with study roadmaps.")
    
    add_bullet_point(doc, "To Ensure Universal Accessibility & Customization: ",
                     "Enable complete visual customization for all user roles, allowing adjustments of button colors, text colors, background colors, dark/light themes, font scaling, and multi-language localization.")
    
    add_bullet_point(doc, "To Support Continuous Deployment & Cloud Hosting: ",
                     "Containerize frontend and backend services using Docker, providing automated build triggers and single-service production deployment on cloud hosting platforms.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: DESCRIPTION & ACCESS PERMISSION OF ROLES
    # =========================================================================
    add_heading_1(doc, "CHAPTER 3\nDESCRIPTION & ACCESS PERMISSION OF ROLES")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform is a full-stack web application developed to modernize examination preparation and academic resource circulation. The system provides role-based interfaces specifically tailored to Students, Academic Mentors, Delivery Partners, and System Administrators."
    )

    add_heading_2(doc, "3.1 Functional Domains Overview")
    add_styled_paragraph(
        doc,
        "1. Academic & Syllabus Exploration: Manages comprehensive profiles for national competitive examinations (GATE CSE, UPSC, JEE, NEET, CAT). Decomposes curricula into hierarchical subjects and weightage-prioritized chapters (High, Medium, Low) without content omissions.\n"
        "2. Assessment & Academic Mentorship: Records multi-attempt mock test evaluations, dynamic note-generated quizzes, and interactive flashcards. Dispatches real-time WhatsApp click-to-chat links, SMS messages, and emails directly to assigned mentors upon test completion or login.\n"
        "3. Circular Commerce & Book Circulation: Peer-to-peer textbook resale, condition grading (New, Like New, Good, Fair), price filters, 100% free donation claiming, multi-tier checkout, and resale return policies.\n"
        "4. Doorstep Logistics Fulfillment: Consignment assignment, live tracking polling (10s updates), and mandatory 4-digit verification OTP confirmation for physical deliveries and donation pickups.\n"
        "5. System Administration & Communication: Centralized administration of users, mentor allocation, syllabus management, and live multi-channel message dispatch from admin@examplatform.edu."
    )

    add_heading_2(doc, "3.2 Access Permission of Roles")
    add_styled_paragraph(
        doc,
        "To ensure robust data isolation, integrity, and security, the application enforces strict Role-Based Access Control (RBAC). JSON Web Tokens carry authenticated user role claims that are validated on every API request via authentication middleware and client-side ProtectedRoute route guards. The diagram below details the comprehensive access permission matrix across all four platform roles:"
    )

    # Insert Access Permission of Roles Diagram
    if os.path.exists("access_permission_roles_bw.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_before = Pt(8)
        doc.paragraphs[-1].paragraph_format.space_after = Pt(4)
        run = doc.paragraphs[-1].add_run()
        run.add_picture("access_permission_roles_bw.png", width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        r = p_cap.add_run("Fig 3.1: Access Permission of Roles and Security Authorization Matrix")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.italic = True
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)

    add_styled_paragraph(
        doc,
        "As illustrated in the authorization matrix, Students possess comprehensive permissions over learning roadmaps, mock tests, marketplace transactions, and community interactions. Academic Mentors are granted specialized supervisory privileges, enabling them to inspect assigned students' longitudinal study curves, receive automated WhatsApp alerts, and initiate direct guidance. Delivery Partners are restricted to logistics workflows, requiring client OTP input to verify handover. System Administrators retain full system governance with administrative access to user accounts, mentor assignments, catalog data, and multi-channel communication tools."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: CLASS DIAGRAM
    # =========================================================================
    add_heading_1(doc, "CHAPTER 4\nCLASS DIAGRAM")

    add_styled_paragraph(
        doc,
        "The UML class diagram models the object-oriented structure of the platform, specifying entity attributes, method signatures, inheritance structures, and inter-model associations across the academic and commerce domains. The User model acts as the foundational account entity, supporting specialized capabilities for Student, Mentor, Administrator, and Delivery Partner roles. Progress entities maintain dynamic mappings of topic completion states linked to hierarchical Exam definitions. Orders connect buyers, delivery partners, and marketplace products with strict encapsulation."
    )

    if os.path.exists("class_diagram_bw.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_before = Pt(12)
        doc.paragraphs[-1].paragraph_format.space_after = Pt(8)
        run = doc.paragraphs[-1].add_run()
        run.add_picture("class_diagram_bw.png", width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(18)
        r = p_cap.add_run("Fig 4.1 UML Class Diagram (Academic Models, Mentorship & Commerce)")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.italic = True
        r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: TABLE STRUCTURES
    # =========================================================================
    add_heading_1(doc, "CHAPTER 5\nTABLE STRUCTURES / SCHEMA SPECIFICATIONS")

    add_styled_paragraph(
        doc,
        "The platform persists structured entities in MongoDB collections governed by strictly validated Mongoose schemas. Primary keys are defined by unique ObjectIds and indexed alphanumeric identifiers. Below are the structural specifications of the operational collections:"
    )

    # 1. Users Schema
    format_schema_table(
        doc, "Table 5.1: Users Collection Schema (User Accounts & Roles)",
        ["Field", "Type", "Null", "Key / Index", "Default", "Description"],
        [
            ["_id", "ObjectId", "NO", "PRI", "UUID", "Unique document identifier"],
            ["name", "String(120)", "NO", "None", "None", "Full user display name"],
            ["email", "String", "NO", "UNI", "None", "Unique email address for login"],
            ["password", "String(255)", "YES", "None", "None", "Salted bcrypt hash (select: false)"],
            ["role", "Enum", "NO", "None", "student", "student | mentor | admin | delivery"],
            ["studentId", "String", "YES", "UNI (sparse)", "None", "Unique auto-generated student identifier"],
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

    # 2. Exams Schema
    format_schema_table(
        doc, "Table 5.2: Exams Collection Schema (Examination Metadata)",
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

    # 3. Progress Schema
    format_schema_table(
        doc, "Table 5.3: Progress Collection Schema (Syllabus & Streak Tracking)",
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

    # 4. Mock Attempts Schema
    format_schema_table(
        doc, "Table 5.4: Mock Attempts Collection Schema (Test Evaluations)",
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

    # 5. Products Schema
    format_schema_table(
        doc, "Table 5.5: Products Collection Schema (Marketplace Resources)",
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

    # 6. Orders Schema
    format_schema_table(
        doc, "Table 5.6: Orders Collection Schema (Commerce Transactions)",
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

    # 7. Communication Logs Schema
    format_schema_table(
        doc, "Table 5.7: Communication Logs Collection Schema (Notification Dispatch)",
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

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: ER DIAGRAM
    # =========================================================================
    add_heading_1(doc, "CHAPTER 6\nER DIAGRAM")

    add_styled_paragraph(
        doc,
        "The Entity-Relationship (ER) diagram models data semantics and relationship constraints between persistent collections. The central USER entity maintains role-based linkages: Students generate Progress documents across registered Exam entities, submit Mock Attempts, and place Orders for Marketplace Products. Academic Mentors are directly linked to Students through a 1:N mentoring association, receiving real-time Communication Logs. Orders maintain parent-child references with Order Items and assigned Delivery Partners, enforcing strict referential integrity."
    )

    if os.path.exists("er_diagram_bw.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_before = Pt(12)
        doc.paragraphs[-1].paragraph_format.space_after = Pt(8)
        run = doc.paragraphs[-1].add_run()
        run.add_picture("er_diagram_bw.png", width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(18)
        r = p_cap.add_run("Fig 6.1 Entity-Relationship Diagram (Academic, Mentorship & Logistics Schema)")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.italic = True
        r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: TECH STACK
    # =========================================================================
    add_heading_1(doc, "CHAPTER 7\nTECH STACK & ARCHITECTURE OVERVIEW")

    add_heading_2(doc, "7.1 Tech Stack")
    format_grid_table(
        doc,
        ["Layer", "Technology", "Purpose & Architectural Role"],
        [
            ["Frontend", "React.js 18 + Vite", "High-performance Single-Page Application (SPA) with fast modular hot-reload."],
            ["Routing & Guards", "React Router DOM v6", "Declarative client-side routing with role-based ProtectedRoute boundaries."],
            ["State & Client Store", "Context API + LocalStorage", "Authentication session, linguistic localization, and persistent shopping cart."],
            ["Styling & 3D Engine", "CSS3 Variables + Three.js", "Responsive layout system with hardware-accelerated 3D login background canvas."],
            ["Backend Runtime", "Node.js (ES Modules) + Express", "RESTful API server coordinating route handlers and asynchronous middleware."],
            ["Database & ODM", "MongoDB + Mongoose ODM", "Document persistence with indexing, schema validation, and lifecycle hooks."],
            ["Security & Token Auth", "JWT + bcryptjs + Google OAuth", "Stateless bearer token authentication, salted cryptographic password hashing, and Google OAuth 2.0."],
            ["Notification Gateway", "WhatsApp Click-to-Chat + Nodemailer", "Multi-channel notification dispatch for academic mentors and order updates."],
            ["Traffic Hardening", "CORS + Rate Limiter Middleware", "Request throttling (180 req/min) and HTTP header defense against scraping."],
            ["CI/CD Automation", "Docker + Cloud Web Service", "Containerized application packaging and production cloud web service deployment."]
        ]
    )

    add_heading_2(doc, "7.2 Architecture Overview")
    format_grid_table(
        doc,
        ["Layer", "Technology", "Purpose"],
        [
            ["Model", "Mongoose ODM + MongoDB", "Defines schema rules, handles index lookups, manages document relationships and data sanitization."],
            ["View", "React.js + Context API", "Renders the UI, manages component state, captures input events, and communicates via fetch/Axios."],
            ["Controller", "Node.js + Express Controllers", "Receives HTTP requests, validates payloads, enforces role authorization, and coordinates DB operations."]
        ]
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: MODULES
    # Heading: CHAPTER 8 \n MODULES
    # Subsections: 8.1 Project Structure (backend, frontend)
    # 8.2 User Authentication & Access Control (Login & Google Auth)
    # 8.3 Student Module & Learning Features (Dashboard, Explorer, Progress, Mock Tests, Quiz, Roadmap, Marketplace, Community, Settings)
    # 8.4 Academic Mentor Module & Monitoring Features
    # 8.5 Delivery Partner Logistics Module
    # 8.6 System Administration & Multi-Channel Communication Engine
    # =========================================================================
    add_heading_1(doc, "CHAPTER 8\nMODULES")

    # -------------------------------------------------------------------------
    # 8.1 PROJECT STRUCTURE (Backend & Frontend Organization)
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.1 Project Structure & Workspace Organization")
    add_styled_paragraph(
        doc,
        "The project follows a clean, decoupled full-stack architectural directory structure organized into root orchestration, backend service tier, and frontend single-page application sub-systems:"
    )

    add_heading_3(doc, "8.1.1 Backend Sub-System Organization (/backend)")
    add_styled_paragraph(
        doc,
        "The backend server is architected following the MVC design pattern with distinct separation between routing, controllers, models, and background services:"
    )
    add_bullet_point(doc, "server.js: ", "Main entry point initializing Express, CORS, security middleware, MongoDB connection, API route mounts, and production static file serving.")
    add_bullet_point(doc, "config/db.js: ", "Establishes resilient Mongoose connection to MongoDB Atlas with auto-reconnect logic and graceful connection teardown.")
    add_bullet_point(doc, "controllers/: ", "Contains 18 modular business controllers including authController.js, examController.js, progressController.js, mentorController.js, marketplaceController.js, orderController.js, and adminController.js.")
    add_bullet_point(doc, "models/: ", "Defines strictly validated Mongoose schemas (User.js, Exam.js, Progress.js, MockAttempt.js, Notification.js, CommunicationLog.js, catalogModels.js, commerceModels.js).")
    add_bullet_point(doc, "routes/: ", "Mounts modular REST endpoints with JWT authentication and RBAC middleware guards.")
    add_bullet_point(doc, "services/communicationService.js: ", "Handles automated multi-channel messaging across WhatsApp click-to-chat links, SMS gateways, and Nodemailer email dispatch.")
    add_bullet_point(doc, "data/seed.js & seedCatalog.js: ", "Automated seeders populating default examination syllabi, admin accounts, mentor profiles, and student testing accounts.")

    add_heading_3(doc, "8.1.2 Frontend Sub-System Organization (/frontend)")
    add_styled_paragraph(
        doc,
        "The frontend is built using React 18 with Vite for high-performance modular development and production bundling:"
    )
    add_bullet_point(doc, "src/main.jsx & App.jsx: ", "Application root configuring React Router DOM v6, AuthProvider, and LanguageProvider contexts.")
    add_bullet_point(doc, "src/components/: ", "Reusable interface widgets including AppLayout.jsx, Sidebar.jsx, ProtectedRoute.jsx, Auth3DVisual.jsx, GuidedTour.jsx, Chatbot.jsx, and FlipCard.jsx.")
    add_bullet_point(doc, "src/pages/: ", "Dedicated views for LoginPage.jsx, ExamExplorerPage.jsx, MyProgressPage.jsx, MentorDashboardPage.jsx, MarketplacePage.jsx, OrdersPage.jsx, DeliveryDashboardPage.jsx, AdminDashboardPage.jsx, CommunityPage.jsx, and SettingsPage.jsx.")
    add_bullet_point(doc, "src/context/: ", "AuthContext.jsx (JWT token management, login state, role-based routing) and LanguageContext.jsx (English, Tamil, Hindi translations).")
    add_bullet_point(doc, "src/api.js: ", "Centralized client fetch wrapper with automatic Bearer token injection, query formatting, and error handling.")

    # -------------------------------------------------------------------------
    # 8.2 USER AUTHENTICATION & ACCESS CONTROL (Login & Google Auth)
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.2 User Authentication & Access Control (Login & Google Authentication)")
    add_screenshot(doc, "screenshots/8_1_login.png", "Fig 8.2: User Authentication & Google OAuth Interface")

    add_heading_3(doc, "8.2.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides tokenized authentication, secure credential management, official Google OAuth 2.0 single sign-on, and Role-Based Access Control (RBAC) across Student, Mentor, Administrator, and Delivery Partner accounts without hardcoding role distinctions into the public interface."
    )
    
    add_heading_3(doc, "8.2.2 Functional Requirements")
    add_bullet_point(doc, "Unified Sign-In & Registration: ", "Users authenticate using email and password or Google OAuth on a single unified interface featuring an interactive Three.js 3D geometric background.")
    add_bullet_point(doc, "Official Google Authentication: ", "Integrates real Google OAuth credentials (client ID & secret), securely validating Google ID tokens on the backend to issue JWT sessions.")
    add_bullet_point(doc, "Dynamic Role-Based Redirection: ", "Upon authentication, the client evaluates role claims and routes Students to /exam-explorer, Mentors to /mentor, Admins to /admin, and Delivery Partners to /delivery.")
    add_bullet_point(doc, "Student ID Generation: ", "Auto-generates unique, non-colliding student identifiers (e.g. PC-STU-100001) upon account registration.")
    add_bullet_point(doc, "Route Protection: ", "Client-side ProtectedRoute wrappers prevent cross-role dashboard traversal, rejecting unauthorized access attempts.")

    add_heading_3(doc, "8.2.3 Non-Functional Requirements")
    add_bullet_point(doc, "Cryptographic Security: ", "Passwords are encrypted using bcryptjs with 10 salt rounds; password hashes are excluded from API payloads by default.")
    add_bullet_point(doc, "Stateless Session Scaling: ", "JSON Web Tokens are signed with a 12-hour expiry, enabling stateless horizontally scalable authorization verification.")

    add_heading_3(doc, "8.2.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["POST", "/api/auth/login", "Authenticates credentials, returns signed JWT and user role profile."],
            ["POST", "/api/auth/register", "Registers new user, assigns role, and generates unique Student ID."],
            ["POST", "/api/auth/google/verify", "Validates Google OAuth credential token, authenticating or registering user."],
            ["GET", "/api/auth/me", "Validates bearer token and returns current active user profile."]
        ]
    )

    add_heading_3(doc, "8.2.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Users", "_id, email, password, role, studentId, mentor, authProvider", "Unique index on email; sparse unique index on studentId; MUL index on mentor reference."]
        ]
    )

    # -------------------------------------------------------------------------
    # 8.3 STUDENT MODULE & LEARNING FEATURES
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.3 Student Module & Comprehensive Learning Features")
    add_styled_paragraph(
        doc,
        "The student module delivers a complete academic preparation suite covering exam catalog discovery, weightage-based syllabi, continuous progress tracking, study streak heatmaps, dynamic quizzes, active recall flashcards, peer book circulation, and community discussion."
    )

    # 8.3.1 Exam Explorer
    add_heading_3(doc, "8.3.1 Exam Explorer & Official Syllabus Roadmaps")
    add_screenshot(doc, "screenshots/8_2_exam_explorer.png", "Fig 8.3.1: Student Exam Explorer & Syllabus Roadmap Interface")
    add_styled_paragraph(
        doc,
        "Displays accredited national competitive examinations (GATE CSE, UPSC, JEE, NEET, CAT) categorized by discipline. Features registered vs. not registered exam sections, recently accessed exams, a step-by-step interactive tour guide, and direct enrollment. Syllabi decompose subjects into High, Medium, and Low weightage groups to optimize preparation sequence without omitting any syllabus topics."
    )

    # 8.3.2 Progress Tracking & Heatmap
    add_heading_3(doc, "8.3.2 Study Progress Tracking, Streaks & Activity Heatmap")
    add_screenshot(doc, "screenshots/8_3_progress_roadmap.png", "Fig 8.3.2: Study Progress Tracking & Activity Heatmap Interface")
    add_styled_paragraph(
        doc,
        "Monitors student completion state across every topic using interactive three-state selectors (Pending, In Progress, Completed). Automatically computes completion percentages at chapter, subject, and overall examination levels. Maintains consecutive daily study streaks using ISO date logs and renders an interactive annual activity heatmap. Completing a subject milestone automatically triggers a notification alert to the assigned mentor."
    )

    # 8.3.3 Mock Tests, Quizzes & Flashcards
    add_heading_3(doc, "8.3.3 Mock Test Evaluation, Dynamic Quizzes & Flashcards")
    add_styled_paragraph(
        doc,
        "Students participate in Computer-Based Test (CBT) mock simulations, capturing scores, questions attended, maximum marks, and percentage progressions across repeated attempts. The platform includes a Dynamic Quiz Generator that automatically parses student notes and chapter topics to generate multiple-choice assessments. Active recall flashcards feature 3D flip card animations, allowing students to test conceptual retention."
    )

    # 8.3.4 Resource Marketplace
    add_heading_3(doc, "8.3.4 Peer-to-Peer Resource Marketplace & Book Circulation")
    add_screenshot(doc, "screenshots/8_5_marketplace.png", "Fig 8.3.4: Resource Marketplace & Textbook Circulation Interface")
    add_styled_paragraph(
        doc,
        "Promotes educational affordability through peer-to-peer textbook resale, verified student listings, condition grading (New, Like New, Good, Fair), price filters, and a dedicated 100% free textbook donation feed. Includes a multi-tier checkout supporting Cash on Delivery (COD), UPI, Google Pay, Net Banking, and Cards, alongside return and buyback workflows."
    )

    # 8.3.5 Community & AI Assistant
    add_heading_3(doc, "8.3.5 Community Discussion Forums & AI Study Assistant")
    add_screenshot(doc, "screenshots/8_7_community.png", "Fig 8.3.5: Community Discussion & AI Assistant Interface")
    add_styled_paragraph(
        doc,
        "Fosters collaborative peer learning through exam-specific discussion threads with question upvoting and verified answers. Complemented by a context-aware AI study assistant that personalizes study advice based on the student's target examination and syllabus progress, alongside daily inspirational quotes dynamically served on login."
    )

    # 8.3.6 Universal Accessibility & Settings
    add_heading_3(doc, "8.3.6 Universal Accessibility & Custom Color Palette Settings")
    add_screenshot(doc, "screenshots/8_8_settings.png", "Fig 8.3.6: Universal Accessibility & Color Palette Settings Interface")
    add_styled_paragraph(
        doc,
        "Empowers students (and all platform roles) to customize their visual interface with live preview controls: button colors, text colors, background colors, dark/light theme switching, font scaling (Small, Medium, Large), and multi-language localization (English, Tamil, Hindi) with cross-session persistence."
    )

    # -------------------------------------------------------------------------
    # 8.4 ACADEMIC MENTOR MODULE & MONITORING FEATURES
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.4 Academic Mentor Module & Monitoring Features")
    add_screenshot(doc, "screenshots/8_4_mentor_dashboard.png", "Fig 8.4: Academic Mentor Monitoring & Evaluation Interface")

    add_heading_3(doc, "8.4.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides dedicated academic mentors real-time supervision over students assigned by administrators, featuring longitudinal progress analytics, automated WhatsApp notifications, and direct mentorship messaging."
    )

    add_heading_3(doc, "8.4.2 Functional Requirements")
    add_bullet_point(doc, "Assigned Students View: ", "Mentors access a personalized portal displaying all students assigned to them, showing active exam goals, overall syllabus percentage bars, and last active dates.")
    add_bullet_point(doc, "Automated WhatsApp Alerts: ", "Whenever a student attempts a mock test or logs in for the day, an automated alert containing student performance metrics and a direct click-to-chat WhatsApp link is dispatched to the mentor.")
    add_bullet_point(doc, "Longitudinal Progress Analytics: ", "Mentors can click any student's profile to inspect granular weekly, monthly, and yearly syllabus completion curves and mock test score trajectories.")
    add_bullet_point(doc, "Lagging Student Indicators: ", "The system automatically flags students lagging behind recommended study velocity, enabling mentors to proactively intervene.")
    add_bullet_point(doc, "Direct Mentorship Messaging: ", "Mentors can trigger motivational messages or academic advice directly to the student via WhatsApp or SMS.")

    add_heading_3(doc, "8.4.3 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/mentor/students", "Retrieves assigned students, syllabus completion percentages, and test history."],
            ["GET", "/api/mentor/students/:id/analytics", "Returns weekly, monthly, and yearly progress analytics for a student."],
            ["PATCH", "/api/mentor/profile", "Updates mentor contact details and WhatsApp phone number."],
            ["POST", "/api/mock-attempts/:examSlug/chapter/:chapterId", "Logs mock score and automatically triggers mentor notification."]
        ]
    )

    # -------------------------------------------------------------------------
    # 8.5 DELIVERY PARTNER LOGISTICS MODULE
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.5 Delivery Partner Logistics Module")
    add_screenshot(doc, "screenshots/8_6_delivery_fulfillment.png", "Fig 8.5: Delivery Partner Fulfillment & OTP Verification Interface")

    add_heading_3(doc, "8.5.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Coordinates physical doorstep book deliveries, return pickups, and donation transfers with assigned partner tracking and mandatory 4-digit OTP security."
    )

    add_heading_3(doc, "8.5.2 Functional Requirements")
    add_bullet_point(doc, "Consignment Dashboard (/delivery): ", "Delivery personnel view assigned shipments, recipient names, delivery addresses, telephone numbers, and dispatch instructions.")
    add_bullet_point(doc, "Real-Time Order Lifecycle: ", "Advances consignments through structured stages: Ordered → Dispatched → In Transit → Out for Delivery → Delivered.")
    add_bullet_point(doc, "Mandatory 4-Digit OTP Verification: ", "Delivery partners cannot mark an order completed without entering the recipient's 4-digit security OTP, preventing disputes and fraudulent status updates.")
    add_bullet_point(doc, "10-Second Live Polling: ", "Customer order tracking pages automatically poll updates every 10 seconds to maintain synchronized status visibility.")

    add_heading_3(doc, "8.5.3 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/delivery/orders", "Returns consignments assigned to the authenticated delivery partner."],
            ["PATCH", "/api/delivery/orders/:id/status", "Advances delivery stage; verifies 4-digit OTP before marking Delivered."],
            ["GET", "/api/orders/track/:trackingId", "Public endpoint providing real-time order tracking stage updates."]
        ]
    )

    # -------------------------------------------------------------------------
    # 8.6 SYSTEM ADMINISTRATION & COMMUNICATION ENGINE
    # -------------------------------------------------------------------------
    add_heading_2(doc, "8.6 System Administration & Multi-Channel Communication Engine")
    add_screenshot(doc, "screenshots/8_9_admin_dashboard.png", "Fig 8.6: System Administration & Communication Engine Interface")

    add_heading_3(doc, "8.6.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Equips administrators with full operational control over users, mentor allocations, exam catalogs, order fulfillment, return policies, and an active multi-channel communication engine."
    )

    add_heading_3(doc, "8.6.2 Functional Requirements")
    add_bullet_point(doc, "User Governance: ", "Audit, activate, deactivate, and inspect all Student, Mentor, and Delivery Partner accounts.")
    add_bullet_point(doc, "Academic Mentor Allocation: ", "Assign or reassign students to designated academic mentors, establishing supervisory linkages.")
    add_bullet_point(doc, "Active Multi-Channel Communication Engine: ", "Admins can compose and send live Emails (dispatched from admin@examplatform.edu), WhatsApp messages, and SMS notifications directly from the platform with real delivery confirmation.")
    add_bullet_point(doc, "Catalog & Order Management: ", "Create and edit competitive examinations, update syllabus roadmaps, and monitor physical consignment progress.")

    add_heading_3(doc, "8.6.3 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/admin/users", "Lists all registered accounts with role filters and account status."],
            ["POST", "/api/admin/assign-mentor", "Links a student account to a designated academic mentor."],
            ["POST", "/api/admin/communicate", "Dispatches an active Email, WhatsApp message, or SMS to target users."],
            ["GET", "/api/admin/analytics", "Aggregates total students, mock attempts, active orders, and mentor coverage."]
        ]
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: CONCLUSION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 9\nCONCLUSION")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform delivers an end-to-end, modern digital solution that resolves the major challenges of competitive exam preparation and academic resource scarcity. By uniting multi-tier syllabus exploration, weightage-based roadmaps, continuous mock test tracking, real-time academic mentorship via automated WhatsApp alerts, a circular peer-to-peer textbook marketplace, and doorstep logistics with OTP verification, the system replaces fragmented, manual workflows with an integrated, data-driven web environment."
    )

    add_styled_paragraph(
        doc,
        "The application was architected following robust full-stack engineering standards utilizing React.js with Vite for the frontend presentation tier, Node.js with Express.js for the RESTful API service tier, and MongoDB with Mongoose for resilient, scalable NoSQL document persistence. JWT authentication, salted bcrypt password encryption, role-based access control across four distinct user roles, request rate limiting, and HTTP security headers ensure enterprise-grade security."
    )

    add_styled_paragraph(
        doc,
        "The completed platform demonstrates how modern web technologies can optimize academic learning, reduce educational expenditure through textbook circulation, foster student-mentor connectivity, and improve examination performance outcomes. Its modular architecture supports high maintainability and lays the foundation for future enhancements such as automated machine-learning question recommendations and mobile application deployment. Overall, the project successfully fulfills all technical objectives, delivering a secure, performant, and reliable web platform."
    )

    # Save document as final_mwt_el_report.docx
    filename = "final_mwt_el_report.docx"
    doc.save(filename)
    print(f"Final report generated successfully as {filename}")

if __name__ == "__main__":
    create_final_report()
