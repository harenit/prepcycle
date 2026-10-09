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

def create_report():
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
        ("3", "DESCRIPTION", "5"),
        ("4", "CLASS DIAGRAM", "6"),
        ("5", "TABLE STRUCTURES / SCHEMA SPECIFICATIONS", "7"),
        ("6", "ER DIAGRAM", "16"),
        ("7", "TECH STACK & ARCHITECTURE OVERVIEW", "18"),
        ("8.1", "USER AUTHENTICATION & ACCESS CONTROL", "19"),
        ("8.2", "EXAM EXPLORER & SYLLABUS ROADMAP MANAGEMENT", "22"),
        ("8.3", "STUDY PROGRESS TRACKING & REVISION ENGINE", "25"),
        ("8.4", "MOCK TEST EVALUATION & ACADEMIC MENTOR MONITORING", "28"),
        ("8.5", "PEER-TO-PEER RESOURCE MARKETPLACE & BOOK CIRCULATION", "31"),
        ("8.6", "ORDER FULFILLMENT & DELIVERY PARTNER LOGISTICS", "34"),
        ("8.7", "COMMUNITY DISCUSSION FORUMS & AI STUDY ASSISTANT", "37"),
        ("8.8", "UNIVERSAL ACCESSIBILITY & SETTINGS CUSTOMIZATION", "40"),
        ("8.9", "SYSTEM ADMINISTRATION & MULTI-CHANNEL COMMUNICATION", "43"),
        ("9", "CONCLUSION", "46"),
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
                if ch in ["1", "2", "3", "4", "5", "6", "7", "9"]:
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
        "The system is developed using modern web engineering principles featuring React.js with Vite for a high-performance single-page application frontend, Node.js with Express.js for the RESTful API backend, and MongoDB with Mongoose for resilient NoSQL persistence. It is supported by a Jenkins-based CI/CD pipeline for automated builds and testing, making it production-ready, maintainable, and horizontally scalable. This report documents the architecture, database schema, component designs, API specifications, and operational workflows of the platform."
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
    
    add_bullet_point(doc, "To Ensure System Security and High Performance: ",
                     "Implement HTTP hardening (CORS, Cache-Control: no-store), rate limiting (180 requests per minute), payload size limits (25 MB), and automated database seeders.")
    
    add_bullet_point(doc, "To Support Continuous Integration via CI/CD: ",
                     "Automate application testing, linting, and containerized deployment pipelines using Jenkins and Docker for consistent production deployments.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: DESCRIPTION
    # =========================================================================
    add_heading_1(doc, "CHAPTER 3\nDESCRIPTION")

    add_styled_paragraph(
        doc,
        "The Multi-Exam Preparation and Resource Exchange Platform is a full-stack web application developed to modernize examination preparation and academic resource circulation. The system consists of five major functional areas:"
    )

    add_heading_2(doc, "1. Academic & Syllabus Exploration Management")
    add_styled_paragraph(
        doc,
        "This module maintains verified profiles for national competitive examinations (such as GATE CSE, UPSC Civil Services, JEE Advanced, NEET, CAT, and State PSCs). Each examination maintains conduction authority information, eligibility criteria, and official portal links. Syllabi are decomposed into hierarchical subjects and chapters categorized by examination weightage (High, Medium, Low). Students track individual topic statuses (Pending, In Progress, Completed), while maintaining full visibility over remaining requirements."
    )

    add_heading_2(doc, "2. Continuous Assessment & Academic Mentorship")
    add_styled_paragraph(
        doc,
        "This module records multi-attempt mock test evaluations, automated quizzes generated dynamically from study notes, and active revision flashcards. When a student submits a mock test or completes the final topic of a subject, the backend immediately triggers automated communication dispatch across WhatsApp (via direct click-to-chat gateway links), SMS, and Email to the student's assigned academic mentor. Mentors access a dedicated portal to review student progress bars, test score histories, and initiate direct guidance."
    )

    add_heading_2(doc, "3. Circular Resource Marketplace & Cart Engine")
    add_styled_paragraph(
        doc,
        "This module manages peer-to-peer textbook exchange, addressing educational affordability. Students can list pre-owned reference books with condition grading (New, Like New, Good, Fair), price, and preview images, or mark materials as 100% free donations. The module provides a full shopping cart and multi-tier checkout supporting Cash on Delivery, UPI, Google Pay, Net Banking, and Credit/Debit Cards, alongside resale return and donation request workflows."
    )

    add_heading_2(doc, "4. Doorstep Logistics Fulfillment & Audit Control")
    add_styled_paragraph(
        doc,
        "The logistics module provides end-to-end shipment traceability. When orders or donation pickups are generated, unique tracking identifiers (e.g. TRK-XXXXXX) and 4-digit verification OTPs are created. Delivery personnel manage orders through stages (Dispatched, In Transit, Out for Delivery, Delivered) and cannot mark an order completed without entering the customer's verification OTP, preventing delivery disputes."
    )

    add_heading_2(doc, "5. Security, System Access, and Automated Deployment")
    add_styled_paragraph(
        doc,
        "The application secures user accounts using bcrypt password hashing and 12-hour signed JSON Web Tokens. Axios client interceptors handle session expiry and authorization headers. A centralized rate-limiting middleware defends against API abuse. The application uses React with Vite, Node.js with Express, and MongoDB with Mongoose, packaged and deployed using automated Jenkins pipelines."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: CLASS DIAGRAM
    # =========================================================================
    add_heading_1(doc, "CHAPTER 4\nCLASS DIAGRAM")

    add_styled_paragraph(
        doc,
        "The class diagram models the object-oriented structure of the platform, specifying entity attributes, method signatures, inheritance structures, and inter-model associations across the academic and commerce domains. The User model acts as the foundational account entity, supporting specialized capabilities for Student, Mentor, Administrator, and Delivery Partner roles. Progress entities maintain dynamic mappings of topic completion states linked to hierarchical Exam definitions. Orders connect buyers, delivery partners, and marketplace products with strict encapsulation."
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
            ["authProvider", "Enum", "NO", "None", "local", "local | google | apple"],
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
            ["Security & Token Auth", "JWT + bcryptjs", "Stateless bearer token authentication and salted cryptographic password hashing."],
            ["Notification Gateway", "WhatsApp Click-to-Chat + Nodemailer", "Multi-channel notification dispatch for academic mentors and order updates."],
            ["Traffic Hardening", "CORS + Rate Limiter Middleware", "Request throttling (180 req/min) and HTTP header defense against scraping."],
            ["CI/CD Automation", "Jenkins (Jenkinsfile) + Docker", "Automated syntax validation, frontend bundling, and containerized deployment."]
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
    # CHAPTER 8: MODULES (Starts directly with 8.1, NO Chapter 8 / 8.0 banner!)
    # Under each heading, output screenshot is placed IMMEDIATELY!
    # Tech stack, low-level architecture, back-of-the-envelope estimations REMOVED!
    # =========================================================================

    # MODULE 8.1: USER AUTHENTICATION & ACCESS CONTROL
    add_heading_2(doc, "8.1 USER AUTHENTICATION & ACCESS CONTROL")
    add_screenshot(doc, "screenshots/8_1_login.png", "Fig 8.1: User Authentication & Access Control Interface")

    add_heading_3(doc, "8.1.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides tokenized authentication, credential management, Google OAuth integration, and Role-Based Access Control (RBAC) across Student, Mentor, Administrator, and Delivery Partner accounts without hardcoding role distinctions into the public interface."
    )
    
    add_heading_3(doc, "8.1.2 Functional Requirements")
    add_bullet_point(doc, "Unified Sign-In & Registration: ", "Users authenticate using email and password or Google OAuth on a single unified interface featuring an interactive Three.js 3D geometric background.")
    add_bullet_point(doc, "Dynamic Role-Based Redirection: ", "Upon token generation, the client evaluates user role claims and routes Students to /exam-explorer, Mentors to /mentor, Admins to /admin, and Delivery Partners to /delivery.")
    add_bullet_point(doc, "Student ID Generation: ", "Auto-generates unique, non-colliding student identifiers (e.g. PC-STU-100001) upon account registration for academic tracking.")
    add_bullet_point(doc, "Route Protection: ", "Client-side ProtectedRoute wrappers prevent cross-role dashboard traversal, rejecting unauthorized access attempts.")

    add_heading_3(doc, "8.1.3 Non-Functional Requirements")
    add_bullet_point(doc, "Cryptographic Security: ", "Passwords are encrypted using bcryptjs with 10 salt rounds; password hashes are excluded from API payloads by default.")
    add_bullet_point(doc, "Stateless Session Scaling: ", "JSON Web Tokens are signed with a 12-hour expiry, enabling stateless horizontally scalable authorization verification.")
    add_bullet_point(doc, "Rate Limiting Defence: ", "Centralized rate-limiting protects authentication routes against brute-force credential stuffing.")

    add_heading_3(doc, "8.1.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["POST", "/api/auth/login", "Authenticates credentials, returns signed JWT and user role profile."],
            ["POST", "/api/auth/register", "Registers new user, assigns role, and generates unique Student ID."],
            ["GET", "/api/auth/me", "Validates bearer token and returns current active user profile."]
        ]
    )

    add_heading_3(doc, "8.1.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Users", "_id, email, password, role, studentId, mentor, authProvider", "Unique index on email; sparse unique index on studentId; MUL index on mentor reference."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.2: EXAM EXPLORER & SYLLABUS ROADMAP MANAGEMENT
    add_heading_2(doc, "8.2 EXAM EXPLORER & SYLLABUS ROADMAP MANAGEMENT")
    add_screenshot(doc, "screenshots/8_2_exam_explorer.png", "Fig 8.2: Exam Explorer & Syllabus Roadmap Management Interface")

    add_heading_3(doc, "8.2.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Centralizes comprehensive examination profiles, conducting authority information, registration eligibility, and hierarchical weightage-ordered syllabi to give students structured preparation roadmaps."
    )

    add_heading_3(doc, "8.2.2 Functional Requirements")
    add_bullet_point(doc, "Catalog Exploration: ", "Displays accredited national competitive examinations (GATE CSE, UPSC, JEE, NEET, CAT) categorized by discipline with search and filter controls.")
    add_bullet_point(doc, "Weightage Prioritization: ", "Organizes syllabus chapters into High, Medium, and Low weightage groups to optimize preparation sequence without omitting any topics.")
    add_bullet_point(doc, "Exam Registration: ", "Allows students to enroll in targeted examinations, initializing personalized progress records in the database.")
    add_bullet_point(doc, "Official Authority Portals: ", "Provides verified direct links to official examination conducting bodies and announcement portals.")

    add_heading_3(doc, "8.2.3 Non-Functional Requirements")
    add_bullet_point(doc, "Read Performance: ", "Optimized caching headers and indexed slugs ensure catalog responses deliver in under 80 ms.")
    add_bullet_point(doc, "Data Integrity: ", "Embedded subject and chapter sub-documents maintain immutable syllabus trees linked to exam slugs.")

    add_heading_3(doc, "8.2.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/exams", "Lists all available examinations with subject counts and category tags."],
            ["GET", "/api/exams/:slug", "Returns complete syllabus tree, subject chapters, and conducting authority info."],
            ["POST", "/api/exams/:slug/register", "Enrolls student in examination and initializes topic tracking record."]
        ]
    )

    add_heading_3(doc, "8.2.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Exams", "_id, slug, name, category, authority, officialUrl, subjects", "Unique index on slug; text index on name and category for search exploration."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.3: STUDY PROGRESS TRACKING & REVISION ENGINE
    add_heading_2(doc, "8.3 STUDY PROGRESS TRACKING & REVISION ENGINE")
    add_screenshot(doc, "screenshots/8_3_progress_roadmap.png", "Fig 8.3: Study Progress Tracking & Revision Engine Interface")

    add_heading_3(doc, "8.3.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Tracks granular topic-level completion states, computes daily study streaks, logs revision activity, and drives active recall through interactive flashcards and dynamic note quizzes."
    )

    add_heading_3(doc, "8.3.2 Functional Requirements")
    add_bullet_point(doc, "Interactive Topic Tracking: ", "Provides three-state status selectors (Pending, In Progress, Completed) for every syllabus topic.")
    add_bullet_point(doc, "Progress Analytics: ", "Computes dynamic completion percentages across chapters, subjects, and the aggregate examination curriculum.")
    add_bullet_point(doc, "Daily Study Streaks: ", "Maintains consecutive daily study streaks using ISO date logs and renders an interactive activity heatmap.")
    add_bullet_point(doc, "Flashcard Revision: ", "Enables students to create, flip, and review subject-specific active recall flashcards.")

    add_heading_3(doc, "8.3.3 Non-Functional Requirements")
    add_bullet_point(doc, "Atomic State Updates: ", "Mongoose document updates use atomic Map modifications to prevent race conditions during rapid checkbox toggles.")
    add_bullet_point(doc, "Responsiveness: ", "State mutations update client UI optimistically with background reconciliation to ensure zero perceived latency.")

    add_heading_3(doc, "8.3.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/progress/:examSlug", "Retrieves student topic statuses, completion stats, streak, and daily audit logs."],
            ["PATCH", "/api/progress/:examSlug/topic/:topicId", "Updates topic completion state and recalculates study streak."],
            ["GET / POST", "/api/flashcards", "Lists or persists subject revision flashcards with question and answer pairs."]
        ]
    )

    add_heading_3(doc, "8.3.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Progress", "_id, user, examSlug, topicStatus, studyDays, dailyLogs", "Compound index on (user, examSlug) ensuring single progress record per student-exam pair."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.4: MOCK TEST EVALUATION & ACADEMIC MENTOR MONITORING
    add_heading_2(doc, "8.4 MOCK TEST EVALUATION & ACADEMIC MENTOR MONITORING")
    add_screenshot(doc, "screenshots/8_4_mentor_dashboard.png", "Fig 8.4: Academic Mentor Monitoring & Evaluation Interface")

    add_heading_3(doc, "8.4.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Evaluates student mock test attempts, computes performance trends, and bridges students with dedicated academic mentors through automated WhatsApp alerts, SMS notifications, and a mentor portal."
    )

    add_heading_3(doc, "8.4.2 Functional Requirements")
    add_bullet_point(doc, "Mock Attempt Recording: ", "Captures scores, questions attended, maximum marks, and percentage progressions across repeated test attempts.")
    add_bullet_point(doc, "Automated WhatsApp & SMS Alerts: ", "Dispatches real-time notification alerts with click-to-chat links directly to assigned mentors when students complete tests or finish subjects.")
    add_bullet_point(doc, "Mentor Supervision Dashboard: ", "Provides mentors a dedicated view of assigned students, progress completion bars, mock score histories, and lagging student indicators.")
    add_bullet_point(doc, "Direct Mentor Guidance: ", "Enables mentors to initiate motivational messages or guidance conversations directly with students via WhatsApp or SMS.")

    add_heading_3(doc, "8.4.3 Non-Functional Requirements")
    add_bullet_point(doc, "Communication Resilience: ", "Multi-channel fallback dispatches alerts across WhatsApp, SMS, and in-app feeds, logging delivery status in the database.")
    add_bullet_point(doc, "Audit Logging: ", "All mock evaluations are recorded with immutable timestamps to maintain longitudinal academic progress records.")

    add_heading_3(doc, "8.4.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["POST", "/api/mock-attempts/:examSlug/chapter/:chapterId", "Records mock attempt score and triggers automated mentor notification."],
            ["GET", "/api/mentor/students", "Retrieves assigned students, syllabus completion percentages, and test history."],
            ["PATCH", "/api/mentor/profile", "Updates mentor phone and WhatsApp alert destination number."],
            ["POST", "/api/admin/assign-mentor", "Assigns or transfers a student to an academic mentor."]
        ]
    )

    add_heading_3(doc, "8.4.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["MockAttempts", "_id, user, examSlug, subjectName, marks, maxMarks, attemptedAt", "Compound index on (user, attemptedAt); index on examSlug."],
            ["CommunicationLogs", "_id, user, channel, messageType, recipient, status, timestamp", "Indexes on channel, status, and timestamp for auditing."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.5: PEER-TO-PEER RESOURCE MARKETPLACE & BOOK CIRCULATION
    add_heading_2(doc, "8.5 PEER-TO-PEER RESOURCE MARKETPLACE & BOOK CIRCULATION")
    add_screenshot(doc, "screenshots/8_5_marketplace.png", "Fig 8.5: Resource Marketplace & Textbook Circulation Interface")

    add_heading_3(doc, "8.5.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Promotes a circular student economy by facilitating peer-to-peer textbook resale, verified student listings, buyback returns, and 100% free study material donations to reduce education expenses."
    )

    add_heading_3(doc, "8.5.2 Functional Requirements")
    add_bullet_point(doc, "Textbook Listings: ", "Students create listings specifying title, author, competitive exam tag, condition grade (New, Like New, Good, Fair), and listing price.")
    add_bullet_point(doc, "Free Donation Feed: ", "Maintains a dedicated zero-rupee donation feed allowing junior aspirants to claim textbooks at ₹0.")
    add_bullet_point(doc, "Multi-Payment Cart: ", "Shopping cart with persistent local storage supporting Cash on Delivery (COD), UPI, Google Pay, Net Banking, and Cards.")
    add_bullet_point(doc, "Return Policies & Resale: ", "Provides structured buyback and resale return workflows for textbooks previously purchased through the platform.")

    add_heading_3(doc, "8.5.3 Non-Functional Requirements")
    add_bullet_point(doc, "Stock Concurrency: ", "Inventory decrement operations execute atomically during order creation to prevent overselling.")
    add_bullet_point(doc, "Search Indexing: ", "Text indexes on book title, author, and exam tag ensure responsive autocomplete filtering.")

    add_heading_3(doc, "8.5.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/marketplace/products", "Returns available products with condition, exam, and price filters."],
            ["POST", "/api/marketplace/products", "Publishes a new textbook resale or free donation listing."],
            ["POST", "/api/orders", "Processes shopping cart checkout, generating tracking ID and verification OTP."]
        ]
    )

    add_heading_3(doc, "8.5.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Products", "_id, title, author, category, examSlug, price, condition, isDonation, seller, status", "Text index on (title, author); index on examSlug; index on isDonation and status."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.6: ORDER FULFILLMENT & DELIVERY PARTNER LOGISTICS
    add_heading_2(doc, "8.6 ORDER FULFILLMENT & DELIVERY PARTNER LOGISTICS")
    add_screenshot(doc, "screenshots/8_6_delivery_fulfillment.png", "Fig 8.6: Delivery Partner Fulfillment & OTP Verification Interface")

    add_heading_3(doc, "8.6.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Orchestrates physical doorstep order deliveries, return evaluations, and donation pickups with delivery partner assignment, 10-second live status updates, and mandatory 4-digit OTP verification."
    )

    add_heading_3(doc, "8.6.2 Functional Requirements")
    add_bullet_point(doc, "Lifecycle Stage Tracking: ", "Monitors shipments through structured stages: Ordered → Dispatched → In Transit → Out for Delivery → Delivered.")
    add_bullet_point(doc, "Delivery Partner Dashboard: ", "Dedicated interface (/delivery) showing assigned consignments, customer addresses, contact numbers, and delivery instructions.")
    add_bullet_point(doc, "Mandatory OTP Handover: ", "Delivery personnel cannot mark an order completed without entering the customer's 4-digit verification OTP, eliminating false deliveries.")
    add_bullet_point(doc, "Real-Time Polling: ", "Client order tracking views poll updates every 10 seconds to maintain synchronized status visibility.")

    add_heading_3(doc, "8.6.3 Non-Functional Requirements")
    add_bullet_point(doc, "Delivery Verification: ", "Cryptographic validation ensures OTP checks are executed server-side with strict attempt limits.")
    add_bullet_point(doc, "Audit Trail: ", "Order stage changes record delivery partner ID, timestamp, and location coordinates.")

    add_heading_3(doc, "8.6.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/delivery/orders", "Returns shipments assigned to the authenticated delivery partner."],
            ["PATCH", "/api/delivery/orders/:id/status", "Advances delivery stage; verifies 4-digit OTP before marking Delivered."],
            ["GET", "/api/orders/track/:trackingId", "Public endpoint providing real-time order tracking stage updates."]
        ]
    )

    add_heading_3(doc, "8.6.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Orders", "_id, trackingId, user, items, totalAmount, paymentMethod, status, verificationOtp, assignedPartner", "Unique index on trackingId; compound index on (assignedPartner, status); index on user."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.7: COMMUNITY DISCUSSION FORUMS & AI STUDY ASSISTANT
    add_heading_2(doc, "8.7 COMMUNITY DISCUSSION FORUMS & AI STUDY ASSISTANT")
    add_screenshot(doc, "screenshots/8_7_community.png", "Fig 8.7: Community Discussion & AI Assistant Interface")

    add_heading_3(doc, "8.7.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Fosters collaborative peer learning through exam-specific discussion threads and provides an integrated AI study assistant offering context-aware roadmap advice and daily motivation."
    )

    add_heading_3(doc, "8.7.2 Functional Requirements")
    add_bullet_point(doc, "Categorized Q&A Forums: ", "Discussion threads organized by examination discipline (GATE, UPSC, JEE, NEET) with question upvoting and accepted answers.")
    add_bullet_point(doc, "Contextual AI Study Assistant: ", "Interactive chat assistant that personalizes study advice based on the student's target examination and syllabus progress.")
    add_bullet_point(doc, "Daily Motivational Greeting: ", "Greets students upon login with an inspirational academic quote dynamically served from the backend.")
    add_bullet_point(doc, "Community Moderation: ", "Admins and community moderators can flag inappropriate content or highlight verified solutions.")

    add_heading_3(doc, "8.7.3 Non-Functional Requirements")
    add_bullet_point(doc, "Low Latency Chat: ", "AI chatbot queries stream responses with graceful fallback to cached study strategy templates.")
    add_bullet_point(doc, "Thread Scalability: ", "Thread replies are paged in increments of 20 to maintain high rendering efficiency.")

    add_heading_3(doc, "8.7.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET / POST", "/api/community", "Retrieves peer discussion threads or posts a new question."],
            ["POST", "/api/community/:id/reply", "Appends a student answer to an existing discussion thread."],
            ["POST", "/api/chat", "Generates contextual AI study advice grounded in student exam syllabus context."]
        ]
    )

    add_heading_3(doc, "8.7.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Discussions", "_id, title, author, examSlug, content, upvotes, replies, isAnswered", "Index on examSlug; index on upvotes for popularity sorting; text index on title and content."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.8: UNIVERSAL ACCESSIBILITY & SETTINGS CUSTOMIZATION
    add_heading_2(doc, "8.8 UNIVERSAL ACCESSIBILITY & SETTINGS CUSTOMIZATION")
    add_screenshot(doc, "screenshots/8_8_settings.png", "Fig 8.8: Universal Accessibility & Color Palette Settings Interface")

    add_heading_3(doc, "8.8.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Empowers all user roles (Students, Mentors, Admins, Delivery Partners) to customize their visual interface through custom color palettes, font scaling, dark/light theme switching, and linguistic localization."
    )

    add_heading_3(doc, "8.8.2 Functional Requirements")
    add_bullet_point(doc, "Full Website Color Customization: ", "Allows users to independently customize button color, text color, and background color with live previews.")
    add_bullet_point(doc, "Universal Accessibility: ", "Settings page is identically accessible to all user roles (Student, Mentor, Admin, Delivery Partner).")
    add_bullet_point(doc, "Dark & Light Theme Switching: ", "Instant high-contrast dark mode and clean paper light mode toggles across all views.")
    add_bullet_point(doc, "Font Size & Multilingual Controls: ", "Dynamic font scaling (Small, Medium, Large) and language selection (English, Tamil, Hindi) with persistent client storage.")

    add_heading_3(doc, "8.8.3 Non-Functional Requirements")
    add_bullet_point(doc, "CSS Custom Properties: ", "All color selections map to dynamic CSS variables, enabling instantaneous re-theming without page refreshes.")
    add_bullet_point(doc, "Cross-Session Persistence: ", "Preferences persist across sessions using LocalStorage and synchronize with user database profiles upon login.")

    add_heading_3(doc, "8.8.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["PATCH", "/api/users/preferences", "Persists user color palette, theme, font size, and language settings."],
            ["GET", "/api/users/preferences", "Fetches saved user interface preferences upon session initialization."]
        ]
    )

    add_heading_3(doc, "8.8.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Users", "preferences.theme, preferences.palette, preferences.fontSize, preferences.language", "Embedded sub-document inside Users collection with zero additional join overhead."]
        ]
    )

    doc.add_page_break()

    # MODULE 8.9: SYSTEM ADMINISTRATION & MULTI-CHANNEL COMMUNICATION
    add_heading_2(doc, "8.9 SYSTEM ADMINISTRATION & MULTI-CHANNEL COMMUNICATION")
    add_screenshot(doc, "screenshots/8_9_admin_dashboard.png", "Fig 8.9: System Administration & Communication Engine Interface")

    add_heading_3(doc, "8.9.1 Purpose & Scope")
    add_styled_paragraph(
        doc,
        "Provides administrators full control over platform operations, including user auditing, exam catalog authoring, order dispatching, mentor-student matching, and an active multi-channel communication engine."
    )

    add_heading_3(doc, "8.9.2 Functional Requirements")
    add_bullet_point(doc, "User & Role Governance: ", "Inspect and manage student, mentor, and delivery partner accounts with activation and deactivation toggles.")
    add_bullet_point(doc, "Mentor-Student Assignment: ", "Allocate students to designated academic mentors to activate automated supervision and notifications.")
    add_bullet_point(doc, "Multi-Channel Communication Engine: ", "Send real emails, WhatsApp messages, and SMS notifications directly from the platform to users with live delivery status confirmation.")
    add_bullet_point(doc, "Catalog & Order Management: ", "Add new competitive examinations, update syllabus roadmaps, and monitor fulfillment of marketplace orders.")

    add_heading_3(doc, "8.9.3 Non-Functional Requirements")
    add_bullet_point(doc, "Operational Auditing: ", "All administrative modifications and dispatched communication logs are recorded with administrative user attribution.")
    add_bullet_point(doc, "Security Clearance: ", "Strict RBAC middleware blocks non-admin users from accessing /api/admin endpoints.")

    add_heading_3(doc, "8.9.4 API Design")
    format_grid_table(
        doc, ["Method", "Endpoint", "Purpose / Contract"],
        [
            ["GET", "/api/admin/users", "Lists all registered accounts with role filters and account status."],
            ["POST", "/api/admin/assign-mentor", "Links a student account to a designated academic mentor."],
            ["POST", "/api/admin/communicate", "Dispatches an active Email, WhatsApp message, or SMS to target users."],
            ["GET", "/api/admin/analytics", "Aggregates total students, mock attempts, active orders, and mentor coverage."]
        ]
    )

    add_heading_3(doc, "8.9.5 Database Design")
    format_grid_table(
        doc, ["Collection", "Key Attributes", "Indexing Strategy"],
        [
            ["Users, CommunicationLogs, Orders", "_id, role, channel, recipient, status, timestamp", "Compound indexes on (channel, status) and (role, createdAt)."]
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

    # Save document
    filename = "Multi_Exam_Preparation_and_Resource_Exchange_Platform_Report.docx"
    doc.save(filename)
    print(f"Final report generated successfully as {filename}")

if __name__ == "__main__":
    create_report()
