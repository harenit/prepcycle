import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =============================================================================
# 1. NEW UPDATED CLASS DIAGRAM
# =============================================================================
def draw_uml_box(ax, x, y, w, title, attributes, methods, font_size=7.2):
    hdr_h = 2.4
    attr_h = (len(attributes) * 1.35) + 1.0
    method_h = (len(methods) * 1.35 + 1.0) if methods else 0
    total_h = hdr_h + attr_h + method_h

    # Outer Box
    rect = patches.Rectangle((x, y - total_h), w, total_h, facecolor='#ffffff', edgecolor='#000000', linewidth=1.6)
    ax.add_patch(rect)

    # Header Bar
    hdr_rect = patches.Rectangle((x, y - hdr_h), w, hdr_h, facecolor='#f3f4f6', edgecolor='#000000', linewidth=1.6)
    ax.add_patch(hdr_rect)
    ax.text(x + w / 2, y - hdr_h / 2, title, color='#000000', weight='bold', fontsize=font_size + 1.5, ha='center', va='center', fontfamily='serif')

    # Attributes
    attr_text = "\n".join(attributes)
    ax.text(x + 0.6, y - hdr_h - 0.7, attr_text, color='#000000', fontsize=font_size, ha='left', va='top', fontfamily='monospace')

    # Methods
    if methods:
        div_y = y - hdr_h - attr_h
        ax.plot([x, x + w], [div_y, div_y], color='#000000', linewidth=1.2)
        method_text = "\n".join(methods)
        ax.text(x + 0.6, div_y - 0.7, method_text, color='#000000', fontsize=font_size - 0.4, ha='left', va='top', fontfamily='monospace', fontstyle='italic')

    return total_h

def generate_updated_class_diagram():
    fig, ax = plt.subplots(figsize=(25, 18), dpi=300)
    ax.set_xlim(0, 125)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header
    ax.text(62.5, 98, "MULTI-EXAM PREPARATION & RESOURCE EXCHANGE PLATFORM — UML CLASS DIAGRAM", 
            fontsize=13, weight='bold', ha='center', va='center', fontfamily='serif')
    ax.plot([25, 100], [96.5, 96.5], color='#000000', lw=1.2)

    # 1. CORE USER CLASS (Center Top)
    draw_uml_box(ax, 48, 93, 30, "User (Account Entity)", [
        "+ _id: ObjectId [PK]",
        "+ studentId: String [UNI, sparse]",
        "+ name: String",
        "+ email: String [UNI]",
        "+ password: String (bcrypt hash)",
        "+ role: Enum {student, mentor, admin, delivery}",
        "+ phone: String",
        "+ whatsappNumber: String",
        "+ mentor: ObjectId [FK -> User]",
        "+ targetExam: String",
        "+ authProvider: Enum {local, google}",
        "+ registeredExams: List<String>",
        "+ preferences: UserPreferences"
    ], [
        "+ register(): User",
        "+ login(email, pwd): Token",
        "+ verifyGoogleToken(cred): Token",
        "+ updatePreferences(pref): void",
        "+ comparePassword(pwd): Boolean"
    ])

    # 2. STUDENT ROLE CLASS (Left Top)
    draw_uml_box(ax, 6, 93, 28, "Student (Role: student)", [
        "+ userRef: ObjectId [FK]",
        "+ targetExam: String",
        "+ dailyStreak: Number",
        "+ studyDays: List<String>",
        "+ cart: List<CartItem>",
        "+ notes: List<Note>",
        "+ flashcards: List<Flashcard>"
    ], [
        "+ enrollExam(slug): void",
        "+ markTopicStatus(id, st): void",
        "+ attemptMockTest(exam, score): void",
        "+ generateDynamicQuiz(): Quiz",
        "+ donateOrSellTextbook(): void"
    ])

    # 3. MENTOR ROLE CLASS (Right Top)
    draw_uml_box(ax, 90, 93, 29, "Mentor (Role: mentor)", [
        "+ userRef: ObjectId [FK]",
        "+ whatsappNumber: String",
        "+ phone: String",
        "+ bio: String",
        "+ assignedStudents: List<ObjectId>",
        "+ notificationActive: Boolean"
    ], [
        "+ viewAssignedStudents(): List",
        "+ sendWhatsAppGuidance(stuId): void",
        "+ getWeeklyStudentAnalytics(id): Stats",
        "+ receiveMockAlert(score): void",
        "+ receiveLoginAlert(stu): void"
    ])

    # 4. DELIVERY PARTNER CLASS (Right Mid)
    draw_uml_box(ax, 90, 58, 29, "DeliveryPartner (Role: delivery)", [
        "+ userRef: ObjectId [FK]",
        "+ activeZone: String",
        "+ vehicleDetails: String",
        "+ assignedOrders: List<ObjectId>",
        "+ pendingPickups: List<ObjectId>"
    ], [
        "+ getAssignedConsignments(): List",
        "+ updateDeliveryStage(orderId, st): void",
        "+ verifyOtpAndDeliver(id, otp): Boolean",
        "+ processDonationPickup(id, otp): void"
    ])

    # 5. ADMINISTRATOR CLASS (Far Right Bottom)
    draw_uml_box(ax, 90, 24, 29, "Administrator (Role: admin)", [
        "+ userRef: ObjectId [FK]",
        "+ adminDepartment: String",
        "+ permissions: List<String>"
    ], [
        "+ manageUsers(action, id): void",
        "+ assignMentorToStudent(m, s): void",
        "+ sendMultiChannelBroadcast(chn): void",
        "+ manageExamCatalog(exam): void",
        "+ inspectReturnPolicies(ret): void"
    ])

    # 6. EXAM CLASS (Left Mid)
    draw_uml_box(ax, 6, 62, 28, "Exam (Catalog Entity)", [
        "+ _id: ObjectId [PK]",
        "+ slug: String [UNI]",
        "+ name: String",
        "+ category: String",
        "+ authority: String",
        "+ officialUrl: String",
        "+ subjects: List<Subject>"
    ], [
        "+ getSyllabusTree(): Tree",
        "+ getChaptersByWeightage(): List",
        "+ addSubject(sub): void"
    ])

    # 7. SUBJECT & CHAPTER (Left Bottom)
    draw_uml_box(ax, 6, 26, 28, "Subject & Chapter (Components)", [
        "[Subject]",
        "+ id: String [PK]",
        "+ name: String",
        "+ chapters: List<Chapter>",
        "-----------------------------",
        "[Chapter]",
        "+ id: String [PK]",
        "+ name: String",
        "+ weightage: Enum {High, Med, Low}",
        "+ topics: List<Topic>"
    ], [
        "+ computeWeightageProgression(): Float",
        "+ getPendingTopics(): List<Topic>"
    ])

    # 8. PROGRESS (Center Mid)
    draw_uml_box(ax, 48, 59, 30, "Progress (Tracking Entity)", [
        "+ _id: ObjectId [PK]",
        "+ user: ObjectId [FK -> User]",
        "+ examSlug: String [FK -> Exam]",
        "+ topicStatus: Map<TopicId, Enum>",
        "+ studyDays: List<String>",
        "+ currentStreak: Number",
        "+ dailyLogs: List<DailyLog>"
    ], [
        "+ updateTopic(id, status): void",
        "+ calculateStreak(): Number",
        "+ checkSubjectCompletion(): Boolean",
        "+ getHeatmapMatrix(): List"
    ])

    # 9. MOCK ATTEMPT & QUIZ (Center Mid-Bottom)
    draw_uml_box(ax, 48, 29, 30, "MockAttempt & Quiz", [
        "[MockAttempt]",
        "+ _id: ObjectId [PK]",
        "+ user: ObjectId [FK -> User]",
        "+ examSlug: String [FK -> Exam]",
        "+ subjectName: String",
        "+ chapterName: String",
        "+ questionsAttended: Number",
        "+ marks: Number",
        "+ maxMarks: Number",
        "+ attemptedAt: DateTime"
    ], [
        "+ logMockScore(): void",
        "+ triggerMentorWhatsAppAlert(): void",
        "+ generateWeakTopicAnalysis(): List"
    ])

    # 10. PRODUCT (Marketplace - Center-Right Bottom)
    draw_uml_box(ax, 6, -5, 34, "Product (Marketplace Resource)", [
        "+ _id: ObjectId [PK]",
        "+ title: String",
        "+ author: String",
        "+ examSlug: String",
        "+ price: Decimal (0.00 for free)",
        "+ condition: Enum {New, LikeNew, Good, Fair}",
        "+ isDonation: Boolean",
        "+ seller: ObjectId [FK -> User]",
        "+ status: Enum {available, sold, claimed}"
    ], [
        "+ listProduct(): Product",
        "+ claimFreeDonation(): void",
        "+ decrementStock(): Boolean"
    ])

    # 11. ORDER & SHIPMENT
    draw_uml_box(ax, 46, -5, 34, "Order (Commerce Transaction)", [
        "+ _id: ObjectId [PK]",
        "+ trackingId: String [UNI]",
        "+ user: ObjectId [FK -> User]",
        "+ items: List<OrderItem>",
        "+ totalAmount: Decimal",
        "+ paymentMethod: Enum {cod, upi, gpay, card}",
        "+ status: Enum {Ordered, InTransit, Delivered}",
        "+ verificationOtp: String(4)",
        "+ assignedPartner: ObjectId [FK -> User]"
    ], [
        "+ placeOrder(): Order",
        "+ updateStatus(st): void",
        "+ verifyOtpAndDeliver(otp): Boolean"
    ])

    # 12. COMMUNICATION LOG (Bottom Right)
    draw_uml_box(ax, 86, -5, 33, "CommunicationLog (Notification Engine)", [
        "+ _id: ObjectId [PK]",
        "+ user: ObjectId [FK -> User]",
        "+ channel: Enum {whatsapp, sms, email, notif}",
        "+ messageType: String",
        "+ recipient: String",
        "+ content: String",
        "+ status: Enum {delivered, pending, failed}",
        "+ timestamp: DateTime"
    ], [
        "+ sendWhatsAppClickToChat(): String",
        "+ sendEmailViaNodemailer(): Result",
        "+ logDeliveryStatus(st): void"
    ])

    # Relational Lines & Annotations
    comp_spec = dict(arrowstyle="-|>", color="#000000", lw=1.4)
    arrow_spec = dict(arrowstyle="->", color="#000000", lw=1.3)
    dash_spec = dict(arrowstyle="->", color="#000000", lw=1.2, ls="--")

    # User -> Student
    ax.annotate("", xy=(34, 82), xytext=(48, 82), arrowprops=comp_spec)
    ax.text(39, 83, "role: student", fontsize=7.2, weight='bold', fontfamily='serif')

    # User -> Mentor
    ax.annotate("", xy=(90, 82), xytext=(78, 82), arrowprops=comp_spec)
    ax.text(80, 83, "role: mentor", fontsize=7.2, weight='bold', fontfamily='serif')

    # User -> Delivery
    ax.annotate("", xy=(90, 52), xytext=(78, 72), arrowprops=comp_spec)
    ax.text(80, 62, "role: delivery", fontsize=7.2, weight='bold', fontfamily='serif')

    # User -> Admin
    ax.annotate("", xy=(90, 20), xytext=(78, 72), arrowprops=comp_spec)
    ax.text(82, 38, "role: admin", fontsize=7.2, weight='bold', fontfamily='serif')

    # User -> Progress (1:N)
    ax.annotate("", xy=(63, 59), xytext=(63, 67), arrowprops=arrow_spec)
    ax.text(64, 63, "1 : N (tracks)", fontsize=7.2, weight='bold', fontfamily='serif')

    # Exam -> Progress (1:N)
    ax.annotate("", xy=(48, 48), xytext=(34, 48), arrowprops=arrow_spec)
    ax.text(37, 49, "1 : N (governs)", fontsize=7.2, weight='bold', fontfamily='serif')

    # Exam -> Subject (Composition)
    ax.annotate("", xy=(20, 26), xytext=(20, 36), arrowprops=arrow_spec)
    ax.text(21, 31, "composes (1 : N)", fontsize=7.2, weight='bold', fontfamily='serif')

    # Progress -> MockAttempt (1:N)
    ax.annotate("", xy=(63, 29), xytext=(63, 35), arrowprops=arrow_spec)
    ax.text(64, 32, "records (1 : N)", fontsize=7.2, weight='bold', fontfamily='serif')

    # MockAttempt -> CommunicationLog (Triggers WhatsApp)
    ax.annotate("", xy=(86, -1), xytext=(78, 12), arrowprops=dash_spec)
    ax.text(78, 5, "triggers WhatsApp alert", fontsize=7.2, weight='bold', fontfamily='serif')

    # Mentor -> Student (1 to N Mentoring)
    ax.plot([104, 104, 20, 20], [93, 96, 96, 93], color='#000000', lw=1.2, ls=':')
    ax.text(62, 96.5, "1 : N (monitors assigned students & sends WhatsApp alerts)", fontsize=7.5, weight='bold', ha='center', fontfamily='serif')

    plt.tight_layout()
    plt.savefig("class_diagram_bw.png", bbox_inches='tight')
    plt.close()
    print("[diagram] Class Diagram BW generated successfully.")

# =============================================================================
# 2. NEW UPDATED ER DIAGRAM
# =============================================================================
def draw_er_box(ax, x, y, w, title, columns, font_size=7.2):
    hdr_h = 2.2
    body_h = (len(columns) * 1.35) + 0.8
    total_h = hdr_h + body_h

    rect = patches.Rectangle((x, y - total_h), w, total_h, facecolor='#ffffff', edgecolor='#000000', linewidth=1.5)
    ax.add_patch(rect)

    hdr_rect = patches.Rectangle((x, y - hdr_h), w, hdr_h, facecolor='#e5e7eb', edgecolor='#000000', linewidth=1.5)
    ax.add_patch(hdr_rect)
    ax.text(x + w / 2, y - hdr_h / 2, title, color='#000000', weight='bold', fontsize=font_size + 1.2, ha='center', va='center', fontfamily='serif')

    for idx, (col_name, col_type, key_type) in enumerate(columns):
        row_y = y - hdr_h - (idx * 1.35) - 1.0
        if key_type:
            ax.text(x + 0.5, row_y, key_type, color='#000000', weight='bold', fontsize=font_size - 0.5, fontfamily='monospace')
        ax.text(x + 2.6, row_y, col_name, color='#000000', weight='bold' if 'PK' in key_type else 'normal', fontsize=font_size, fontfamily='monospace')
        ax.text(x + w - 0.5, row_y, col_type, color='#333333', fontsize=font_size - 0.5, ha='right', fontfamily='monospace')
        if idx < len(columns) - 1:
            ax.plot([x, x + w], [row_y - 0.35, row_y - 0.35], color='#e2e8f0', linewidth=0.6)

    return total_h

def generate_updated_er_diagram():
    fig, ax = plt.subplots(figsize=(25, 18), dpi=300)
    ax.set_xlim(0, 125)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(62.5, 98, "MULTI-EXAM PREPARATION & RESOURCE EXCHANGE PLATFORM — ENTITY RELATIONSHIP DIAGRAM", 
            fontsize=13, weight='bold', ha='center', va='center', fontfamily='serif')
    ax.plot([25, 100], [96.5, 96.5], color='#000000', lw=1.2)

    # 1. USERS (Center Top)
    draw_er_box(ax, 48, 93, 30, "users (Account Catalog)", [
        ("_id", "ObjectId", "PK"),
        ("studentId", "varchar(20)", "UQ"),
        ("name", "varchar(120)", ""),
        ("email", "varchar(150)", "UQ"),
        ("password", "varchar(255)", ""),
        ("role", "enum(student,mentor,admin,delivery)", ""),
        ("phone", "varchar(30)", ""),
        ("whatsappNumber", "varchar(30)", ""),
        ("mentor_id", "ObjectId", "FK"),
        ("targetExam", "varchar(50)", ""),
        ("authProvider", "varchar(20)", ""),
        ("registeredExams", "json/array", ""),
        ("createdAt", "datetime", "")
    ])

    # 2. EXAMS (Top Left)
    draw_er_box(ax, 6, 93, 28, "exams (Examination Master)", [
        ("_id", "ObjectId", "PK"),
        ("slug", "varchar(50)", "UQ"),
        ("name", "varchar(150)", ""),
        ("category", "varchar(50)", ""),
        ("authority", "varchar(100)", ""),
        ("officialUrl", "varchar(255)", ""),
        ("subjects", "json/subdocs", ""),
        ("createdAt", "datetime", "")
    ])

    # 3. SUBJECTS_CATALOG (Mid Left)
    draw_er_box(ax, 6, 64, 28, "subjects (Hierarchical Catalog)", [
        ("subjectId", "varchar(50)", "PK"),
        ("exam_slug", "varchar(50)", "FK"),
        ("name", "varchar(100)", ""),
        ("weightage", "enum(High,Med,Low)", ""),
        ("chapterCount", "int", ""),
        ("topicCount", "int", "")
    ])

    # 4. PROGRESS (Center Mid)
    draw_er_box(ax, 48, 62, 30, "progress (Syllabus Tracking)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("exam_slug", "varchar(50)", "FK"),
        ("topicStatus", "json/map", ""),
        ("studyDays", "json/array", ""),
        ("currentStreak", "int", ""),
        ("completionPct", "decimal(5,2)", ""),
        ("dailyLogs", "json/array", ""),
        ("updatedAt", "datetime", "")
    ])

    # 5. MOCK_ATTEMPTS (Center Bottom)
    draw_er_box(ax, 48, 33, 30, "mock_attempts (Evaluations)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("exam_slug", "varchar(50)", "FK"),
        ("subjectName", "varchar(100)", ""),
        ("chapterName", "varchar(100)", ""),
        ("mockName", "varchar(150)", ""),
        ("questionsAttended", "int", ""),
        ("marks", "decimal(6,2)", ""),
        ("maxMarks", "decimal(6,2)", ""),
        ("attemptedAt", "datetime", "")
    ])

    # 6. PRODUCTS (Right Top)
    draw_er_box(ax, 90, 93, 29, "products (Marketplace Resources)", [
        ("_id", "ObjectId", "PK"),
        ("title", "varchar(255)", ""),
        ("author", "varchar(100)", ""),
        ("examSlug", "varchar(50)", "FK"),
        ("price", "decimal(10,2)", ""),
        ("condition", "enum(New,LikeNew,Good,Fair)", ""),
        ("isDonation", "boolean", ""),
        ("stock", "int", ""),
        ("seller_id", "ObjectId", "FK"),
        ("status", "varchar(30)", "")
    ])

    # 7. ORDERS (Right Mid)
    draw_er_box(ax, 90, 60, 29, "orders (Transactions)", [
        ("_id", "ObjectId", "PK"),
        ("trackingId", "varchar(50)", "UQ"),
        ("user_id", "ObjectId", "FK"),
        ("totalAmount", "decimal(10,2)", ""),
        ("paymentMethod", "varchar(30)", ""),
        ("status", "enum(Ordered,InTransit,Delivered)", ""),
        ("verificationOtp", "varchar(4)", ""),
        ("assignedPartner_id", "ObjectId", "FK"),
        ("createdAt", "datetime", "")
    ])

    # 8. ORDER_ITEMS (Right Bottom)
    draw_er_box(ax, 90, 28, 29, "order_items (Line Items)", [
        ("itemId", "ObjectId", "PK"),
        ("order_id", "ObjectId", "FK"),
        ("product_id", "ObjectId", "FK"),
        ("quantity", "int", ""),
        ("priceAtOrder", "decimal(10,2)", ""),
        ("subtotal", "decimal(10,2)", "")
    ])

    # 9. COMMUNICATION_LOGS (Bottom Left)
    draw_er_box(ax, 6, 36, 28, "communication_logs (Alerts)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("channel", "enum(whatsapp,sms,email)", ""),
        ("messageType", "varchar(50)", ""),
        ("recipient", "varchar(100)", ""),
        ("subject", "varchar(150)", ""),
        ("content", "text", ""),
        ("status", "varchar(30)", ""),
        ("timestamp", "datetime", "")
    ])

    # 10. DISCUSSIONS & NOTIFICATIONS (Bottom Row)
    draw_er_box(ax, 6, 8, 28, "discussions (Peer Community)", [
        ("_id", "ObjectId", "PK"),
        ("author_id", "ObjectId", "FK"),
        ("examSlug", "varchar(50)", "FK"),
        ("title", "varchar(200)", ""),
        ("content", "text", ""),
        ("upvotes", "int", ""),
        ("isAnswered", "boolean", ""),
        ("createdAt", "datetime", "")
    ])

    draw_er_box(ax, 48, 6, 30, "notifications (Alert Hub)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("type", "varchar(30)", ""),
        ("title", "varchar(150)", ""),
        ("body", "text", ""),
        ("read", "boolean", ""),
        ("createdAt", "datetime", "")
    ])

    draw_er_box(ax, 90, -1, 29, "return_requests (Returns)", [
        ("_id", "ObjectId", "PK"),
        ("trackingId", "varchar(50)", "UQ"),
        ("user_id", "ObjectId", "FK"),
        ("order_id", "ObjectId", "FK"),
        ("status", "varchar(30)", ""),
        ("verificationOtp", "varchar(4)", ""),
        ("createdAt", "datetime", "")
    ])

    def draw_rel(p1, p2, label1="1", label2="N", text_mid=""):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#000000', lw=1.3)
        ax.text(p1[0] + (1.0 if p1[0] <= p2[0] else -2.0), p1[1], label1, fontsize=7.5, weight='bold', fontfamily='monospace')
        ax.text(p2[0] + (-2.0 if p1[0] <= p2[0] else 1.0), p2[1], label2, fontsize=7.5, weight='bold', fontfamily='monospace')
        if text_mid:
            ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.7, text_mid, fontsize=7.0, weight='bold', ha='center', fontfamily='serif')

    # users -> users (Mentor self link)
    ax.plot([48, 44, 44, 48], [88, 88, 91, 91], color='#000000', lw=1.2)
    ax.text(39.5, 89.5, "1:N (mentor)", fontsize=7.0, weight='bold', fontfamily='monospace')

    # users -> progress (1:N)
    draw_rel((63, 68), (63, 62), "1", "N")

    # exams -> progress (1:N)
    draw_rel((34, 76), (48, 55), "1", "N")

    # exams -> subjects (1:N)
    draw_rel((20, 71), (20, 64), "1", "N")

    # progress -> mock_attempts (1:N)
    draw_rel((63, 41), (63, 33), "1", "N")

    # mock_attempts -> communication_logs (Triggers WhatsApp)
    draw_rel((48, 22), (34, 22), "1", "N", "triggers WhatsApp")

    # users -> orders (1:N)
    draw_rel((78, 77), (90, 52), "1", "N")

    # orders -> order_items (1:N)
    draw_rel((104, 38), (104, 28), "1", "N")

    # products -> order_items (1:N)
    draw_rel((104, 69), (104, 60), "1", "N")

    # users -> products (1:N)
    draw_rel((78, 87), (90, 87), "1", "N")

    # users -> notifications (1:N)
    draw_rel((63, 14), (63, 6), "1", "N")

    plt.tight_layout()
    plt.savefig("er_diagram_bw.png", bbox_inches='tight')
    plt.close()
    print("[diagram] ER Diagram BW generated successfully.")

# =============================================================================
# 3. ACCESS PERMISSION OF ROLES DIAGRAM (Chapter 3)
# =============================================================================
def generate_access_permission_roles_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 80)
    ax.axis('off')

    # Title
    ax.text(60, 77, "ACCESS PERMISSION OF ROLES & AUTHORIZATION MATRIX", 
            fontsize=13, weight='bold', ha='center', va='center', fontfamily='serif')
    ax.plot([25, 95], [75.5, 75.5], color='#000000', lw=1.2)

    # 4 Roles across the top
    roles = [
        ("STUDENT", "Role: student\nAspirant Learner", 10),
        ("ACADEMIC MENTOR", "Role: mentor\nFaculty / Guide", 38),
        ("DELIVERY PARTNER", "Role: delivery\nLogistics Personnel", 66),
        ("ADMINISTRATOR", "Role: admin\nSystem Operator", 94)
    ]

    for title, sub, x in roles:
        box = patches.Rectangle((x, 62), 24, 10, facecolor='#f8fafc', edgecolor='#000000', linewidth=1.5)
        ax.add_patch(box)
        hdr = patches.Rectangle((x, 68), 24, 4, facecolor='#e2e8f0', edgecolor='#000000', linewidth=1.5)
        ax.add_patch(hdr)
        ax.text(x + 12, 70, title, weight='bold', fontsize=9.0, ha='center', va='center', fontfamily='serif')
        ax.text(x + 12, 65, sub, fontsize=7.5, ha='center', va='center', fontfamily='serif', style='italic')

    # Functional Capabilities / Permissions Table
    matrix_data = [
        ("Unified Authentication & 3D Canvas", "FULL", "FULL", "FULL", "FULL"),
        ("Exam Roadmaps & Weightage Syllabus", "FULL", "VIEW", "NONE", "FULL (CRUD)"),
        ("Topic Status & Study Heatmap Tracking", "FULL", "VIEW (Assigned)", "NONE", "VIEW ALL"),
        ("Mock Test Submission & Quiz Engine", "FULL", "VIEW SCORES", "NONE", "VIEW ALL"),
        ("Automated WhatsApp Alert Dispatch", "TRIGGER", "RECEIVE", "NONE", "AUDIT"),
        ("Assigned Student Longitudinal Analytics", "SELF ONLY", "FULL (Assigned)", "NONE", "FULL ALL"),
        ("Direct WhatsApp/SMS Mentorship Messaging", "RECEIVE", "DISPATCH", "NONE", "DISPATCH"),
        ("Resource Marketplace (Buy / Sell Books)", "FULL", "VIEW", "NONE", "MANAGE"),
        ("Free Material Donation Circulation", "FULL", "VIEW", "NONE", "MANAGE"),
        ("Doorstep Delivery & Route Dispatch", "TRACK (10s)", "NONE", "FULL", "MANAGE"),
        ("Mandatory 4-Digit Delivery Verification OTP", "RECEIVE", "NONE", "VERIFY (Input)", "AUDIT"),
        ("Peer Community Q&A & AI Assistant", "FULL", "MENTOR REPLY", "NONE", "MODERATE"),
        ("System Administration & User Management", "NONE", "NONE", "NONE", "FULL (CRUD)"),
        ("Mentor-Student Allocation Governance", "NONE", "NONE", "NONE", "FULL"),
        ("Universal Theme, Palette & Settings", "FULL", "FULL", "FULL", "FULL")
    ]

    y_start = 58
    row_h = 3.4
    table_w = 108

    # Table Header
    th_box = patches.Rectangle((6, y_start), table_w, row_h, facecolor='#000000', edgecolor='#000000')
    ax.add_patch(th_box)
    ax.text(8, y_start + row_h / 2, "FUNCTIONAL SYSTEM CAPABILITY / PERMISSION", color='#ffffff', weight='bold', fontsize=8.0, va='center', fontfamily='serif')
    ax.text(46, y_start + row_h / 2, "STUDENT", color='#ffffff', weight='bold', fontsize=8.0, ha='center', va='center', fontfamily='serif')
    ax.text(66, y_start + row_h / 2, "MENTOR", color='#ffffff', weight='bold', fontsize=8.0, ha='center', va='center', fontfamily='serif')
    ax.text(86, y_start + row_h / 2, "DELIVERY", color='#ffffff', weight='bold', fontsize=8.0, ha='center', va='center', fontfamily='serif')
    ax.text(106, y_start + row_h / 2, "ADMIN", color='#ffffff', weight='bold', fontsize=8.0, ha='center', va='center', fontfamily='serif')

    for i, (cap, s_perm, m_perm, d_perm, a_perm) in enumerate(matrix_data):
        curr_y = y_start - ((i + 1) * row_h)
        bg_col = '#f8fafc' if i % 2 == 1 else '#ffffff'
        r_box = patches.Rectangle((6, curr_y), table_w, row_h, facecolor=bg_col, edgecolor='#d1d5db', linewidth=0.8)
        ax.add_patch(r_box)

        # Border
        ax.plot([6, 6 + table_w], [curr_y, curr_y], color='#9ca3af', lw=0.6)

        # Capability Text
        ax.text(8, curr_y + row_h / 2, cap, fontsize=7.5, weight='bold', va='center', fontfamily='serif')

        # Values
        def draw_perm_badge(val, cx):
            weight = 'bold' if val in ['FULL', 'FULL (CRUD)', 'FULL ALL', 'FULL (Assigned)'] else 'normal'
            style = 'italic' if val in ['NONE', 'RECEIVE', 'TRIGGER'] else 'normal'
            color = '#000000' if val != 'NONE' else '#6b7280'
            ax.text(cx, curr_y + row_h / 2, val, color=color, weight=weight, fontsize=7.0, style=style, ha='center', va='center', fontfamily='monospace')

        draw_perm_badge(s_perm, 46)
        draw_perm_badge(m_perm, 66)
        draw_perm_badge(d_perm, 86)
        draw_perm_badge(a_perm, 106)

    # Outer table border
    tot_table_h = (len(matrix_data) + 1) * row_h
    tbl_outline = patches.Rectangle((6, y_start - (len(matrix_data) * row_h)), table_w, tot_table_h, facecolor='none', edgecolor='#000000', linewidth=1.6)
    ax.add_patch(tbl_outline)

    # Vertical Column Dividers
    for col_x in [36, 56, 76, 96]:
        ax.plot([col_x, col_x], [y_start + row_h, y_start - (len(matrix_data) * row_h)], color='#9ca3af', lw=0.8)

    plt.tight_layout()
    plt.savefig("access_permission_roles_bw.png", bbox_inches='tight')
    plt.close()
    print("[diagram] Access Permission of Roles Diagram BW generated successfully.")

if __name__ == "__main__":
    generate_updated_class_diagram()
    generate_updated_er_diagram()
    generate_access_permission_roles_diagram()
