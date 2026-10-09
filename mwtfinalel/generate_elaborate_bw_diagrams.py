import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_uml_box(ax, x, y, w, h, title, attributes, methods, font_size=7.5):
    # Header height is roughly 18% of total height or based on title
    hdr_h = 2.4
    attr_h = (len(attributes) * 1.5) + 1.2
    total_h = hdr_h + attr_h + (len(methods) * 1.4 + 1.2 if methods else 0)
    
    # Outer box
    rect = patches.Rectangle((x, y - total_h), w, total_h, facecolor='#ffffff', edgecolor='#000000', linewidth=1.6)
    ax.add_patch(rect)
    
    # Header bar
    hdr_rect = patches.Rectangle((x, y - hdr_h), w, hdr_h, facecolor='#f1f5f9', edgecolor='#000000', linewidth=1.6)
    ax.add_patch(hdr_rect)
    ax.text(x + w / 2, y - hdr_h / 2, title, color='#000000', weight='bold', fontsize=font_size + 1.5, ha='center', va='center', fontfamily='serif')
    
    # Attributes text
    attr_text = "\n".join(attributes)
    ax.text(x + 0.6, y - hdr_h - 0.8, attr_text, color='#000000', fontsize=font_size, ha='left', va='top', fontfamily='monospace')
    
    # Divider if methods exist
    if methods:
        div_y = y - hdr_h - attr_h
        ax.plot([x, x + w], [div_y, div_y], color='#000000', linewidth=1.2)
        method_text = "\n".join(methods)
        ax.text(x + 0.6, div_y - 0.8, method_text, color='#000000', fontsize=font_size - 0.5, ha='left', va='top', fontfamily='monospace', fontstyle='italic')
        
    return total_h

def generate_elaborate_class_diagram():
    fig, ax = plt.subplots(figsize=(24, 17), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 95)
    ax.axis('off')

    # Top Title
    ax.text(60, 93, "ACADEMIC PREPARATION & RESOURCE EXCHANGE PLATFORM — UML CLASS DIAGRAM", 
            fontsize=13, weight='bold', ha='center', va='center', fontfamily='serif')
    ax.plot([25, 95], [91.5, 91.5], color='#000000', lw=1.2)

    # 1. USER (Core Model - Center Top)
    h_user = draw_uml_box(ax, 46, 88, 28, 22, "User (Account Model)",
                 ["+ _id: ObjectId [PK]",
                  "+ studentId: String [UNI, sparse]",
                  "+ name: String",
                  "+ email: String [UNI]",
                  "+ password: String (bcrypt hash)",
                  "+ role: Enum {student, mentor, admin, delivery}",
                  "+ phone: String",
                  "+ whatsappNumber: String",
                  "+ mentor: ObjectId [FK -> User]",
                  "+ targetExam: String",
                  "+ authProvider: String",
                  "+ registeredExams: List<String>",
                  "+ createdAt: DateTime"],
                 ["+ register(): User",
                  "+ authenticate(pwd): Token",
                  "+ comparePassword(cand): Boolean",
                  "+ updateProfile(data): User",
                  "+ assignStudentId(): String"])

    # 2. STUDENT ROLE EXTENSION (Left Top)
    draw_uml_box(ax, 6, 88, 26, 17, "Student (Role: student)",
                 ["+ userRef: ObjectId [FK]",
                  "+ dailyGoalHours: Number",
                  "+ college: String",
                  "+ state: String",
                  "+ currentStreak: Number",
                  "+ bookmarkedResources: List<ObjectId>",
                  "+ cart: List<CartItem>"],
                 ["+ enrollExam(slug): void",
                  "+ updateTopicStatus(id, st): void",
                  "+ attemptMockTest(): void",
                  "+ donateTextbook(): void",
                  "+ raiseReturnRequest(): void"])

    # 3. MENTOR ROLE EXTENSION (Right Top)
    draw_uml_box(ax, 86, 88, 28, 17, "Mentor (Role: mentor)",
                 ["+ userRef: ObjectId [FK]",
                  "+ whatsappNumber: String",
                  "+ bio: String",
                  "+ assignedStudents: List<ObjectId>",
                  "+ notificationActive: Boolean"],
                 ["+ getAssignedStudents(): List<Student>",
                  "+ sendWhatsAppGuidance(stuId, msg): void",
                  "+ receiveMockAlert(stu, score): void",
                  "+ receiveSubjectMilestoneAlert(): void",
                  "+ updateWhatsAppContact(phone): void"])

    # 4. DELIVERY PARTNER (Far Right Top-Mid)
    draw_uml_box(ax, 86, 58, 28, 15, "DeliveryPartner (Role: delivery)",
                 ["+ userRef: ObjectId [FK]",
                  "+ activeZone: String",
                  "+ vehicleDetails: String",
                  "+ assignedOrders: List<ObjectId>",
                  "+ assignedPickups: List<ObjectId>"],
                 ["+ listAssignedConsignments(): List",
                  "+ updateTransitStatus(orderId, st): void",
                  "+ verifyOtpAndDeliver(orderId, otp): Boolean",
                  "+ inspectReturnedBookQuality(): void"])

    # 5. EXAM (Left Mid)
    draw_uml_box(ax, 6, 58, 26, 20, "Exam",
                 ["+ _id: ObjectId [PK]",
                  "+ slug: String [UNI]",
                  "+ name: String",
                  "+ category: String",
                  "+ authority: String",
                  "+ eligibility: String",
                  "+ officialUrl: String",
                  "+ subjects: List<Subject>"],
                 ["+ getSyllabusTree(): Tree",
                  "+ getChaptersByWeightage(): List",
                  "+ addSubject(sub): void",
                  "+ removeSubject(id): void"])

    # 6. SUBJECT & CHAPTER (Component Box - Left Mid-Bottom)
    draw_uml_box(ax, 6, 28, 26, 22, "Subject & Chapter (Components)",
                 ["[Subject]",
                  "+ id: String [PK]",
                  "+ name: String",
                  "+ chapters: List<Chapter>",
                  "-----------------------",
                  "[Chapter]",
                  "+ id: String [PK]",
                  "+ name: String",
                  "+ weightage: Enum {High, Med, Low}",
                  "+ roadmapOrder: Number",
                  "+ topics: List<Topic>"],
                 ["+ computeSubjectCompletion(): Float",
                  "+ getHighWeightageTopics(): List",
                  "+ getChapterMockLinks(): List"])

    # 7. PROGRESS (Center Mid)
    draw_uml_box(ax, 46, 56, 28, 20, "Progress",
                 ["+ _id: ObjectId [PK]",
                  "+ user: ObjectId [FK -> User]",
                  "+ examSlug: String [FK -> Exam]",
                  "+ topicStatus: Map<id, StatusEnum>",
                  "+ studyDays: List<String>",
                  "+ overallScore: Number",
                  "+ dailyLogs: List<DailyLog>"],
                 ["+ setTopicStatus(id, st): void",
                  "+ computeCompletionPercent(): Float",
                  "+ calculateConsecutiveStreak(): Number",
                  "+ checkSubjectMilestone(): Boolean"])

    # 8. MOCK ATTEMPT (Center Mid-Bottom)
    draw_uml_box(ax, 46, 28, 28, 22, "MockAttempt",
                 ["+ _id: ObjectId [PK]",
                  "+ user: ObjectId [FK -> User]",
                  "+ examSlug: String [FK -> Exam]",
                  "+ subjectName: String",
                  "+ chapterName: String",
                  "+ mockName: String",
                  "+ questionsAttended: Number",
                  "+ marks: Number",
                  "+ maxMarks: Number",
                  "+ attemptedAt: DateTime"],
                 ["+ recordAttempt(): MockAttempt",
                  "+ triggerMentorWhatsAppAlert(): void",
                  "+ triggerMentorEmailAlert(): void",
                  "+ getAttemptHistoryByUser(): List",
                  "+ calculateScorePercentage(): Float"])

    # 9. PRODUCT (Marketplace - Far Right Mid-Bottom)
    draw_uml_box(ax, 86, 34, 28, 20, "Product (Marketplace)",
                 ["+ _id: ObjectId [PK]",
                  "+ title: String",
                  "+ author: String",
                  "+ category: String",
                  "+ examSlug: String",
                  "+ price: Decimal",
                  "+ condition: Enum {New, LikeNew, Good, Fair}",
                  "+ isDonation: Boolean",
                  "+ stock: Number",
                  "+ seller: ObjectId [FK -> User]",
                  "+ status: String"],
                 ["+ listProduct(): Product",
                  "+ markAsDonated(): void",
                  "+ decrementStock(qty): Boolean",
                  "+ updateCondition(cond): void"])

    # 10. ORDER & SHIPMENT (Bottom Center-Left)
    draw_uml_box(ax, 6, 2, 34, 22, "Order (Commerce Transaction)",
                 ["+ _id: ObjectId [PK]",
                  "+ trackingId: String [UNI]",
                  "+ user: ObjectId [FK -> User]",
                  "+ items: List<OrderItem>",
                  "+ totalAmount: Decimal",
                  "+ paymentMethod: Enum {cod, upi, gpay, card}",
                  "+ status: Enum {Ordered, InTransit, Delivered}",
                  "+ verificationOtp: String(4)",
                  "+ deliveryAddress: Address",
                  "+ assignedPartner: ObjectId [FK -> User]"],
                 ["+ placeOrder(): Order",
                  "+ updateStatus(st): void",
                  "+ verifyDeliveryOtp(otp): Boolean",
                  "+ cancelOrder(): Boolean"])

    # 11. COMMUNICATION LOG (Bottom Center-Right)
    draw_uml_box(ax, 46, 2, 34, 20, "CommunicationLog (Audit Trail)",
                 ["+ _id: ObjectId [PK]",
                  "+ user: ObjectId [FK -> User]",
                  "+ channel: Enum {whatsapp, sms, email, notif}",
                  "+ messageType: String",
                  "+ recipient: String",
                  "+ subject: String",
                  "+ content: String",
                  "+ status: Enum {delivered, pending, failed}",
                  "+ provider: String",
                  "+ timestamp: DateTime"],
                 ["+ sendWhatsApp(num, msg): Result",
                  "+ sendSms(num, msg): Result",
                  "+ sendEmail(mail, subj, body): Result",
                  "+ generateClickToChatUrl(): String"])

    # Connectors & UML Associations
    arrow_spec = dict(arrowstyle="->", color="#000000", lw=1.3)
    comp_spec = dict(arrowstyle="-|>", color="#000000", lw=1.4)
    dash_spec = dict(arrowstyle="->", color="#000000", lw=1.2, ls="--")

    # User -> Student (Specialization)
    ax.annotate("", xy=(32, 78), xytext=(46, 78), arrowprops=comp_spec)
    ax.text(37, 79, "role: student", fontsize=7.5, weight='bold', fontfamily='serif')

    # User -> Mentor (Specialization)
    ax.annotate("", xy=(86, 78), xytext=(74, 78), arrowprops=comp_spec)
    ax.text(76, 79, "role: mentor", fontsize=7.5, weight='bold', fontfamily='serif')

    # User -> DeliveryPartner
    ax.annotate("", xy=(86, 52), xytext=(74, 66), arrowprops=comp_spec)
    ax.text(76, 58, "role: delivery", fontsize=7.5, weight='bold', fontfamily='serif')

    # User -> Progress (1 to N)
    ax.annotate("", xy=(60, 56), xytext=(60, 66), arrowprops=arrow_spec)
    ax.text(61, 61, "1 : N (tracks)", fontsize=7.5, weight='bold', fontfamily='serif')

    # Exam -> Progress (1 to N)
    ax.annotate("", xy=(46, 46), xytext=(32, 46), arrowprops=arrow_spec)
    ax.text(35, 47, "1 : N (governs)", fontsize=7.5, weight='bold', fontfamily='serif')

    # Exam -> Subject (Composition)
    ax.annotate("", xy=(19, 28), xytext=(19, 36), arrowprops=arrow_spec)
    ax.text(20, 32, "composes (1 : N)", fontsize=7.5, weight='bold', fontfamily='serif')

    # Progress -> MockAttempt (1 to N)
    ax.annotate("", xy=(60, 28), xytext=(60, 36), arrowprops=arrow_spec)
    ax.text(61, 32, "evaluates (1 : N)", fontsize=7.5, weight='bold', fontfamily='serif')

    # MockAttempt -> CommunicationLog (Triggers WhatsApp)
    ax.annotate("", xy=(60, 2), xytext=(60, 6), arrowprops=dash_spec)
    ax.text(61, 4, "triggers alert", fontsize=7.5, weight='bold', fontfamily='serif')

    # Mentor -> Student (1 to N Mentoring)
    ax.plot([100, 100, 30, 30], [88, 92, 92, 88], color='#000000', lw=1.2, ls=':')
    ax.text(60, 92.5, "1 : N (monitors assigned students via WhatsApp)", fontsize=7.5, weight='bold', ha='center', fontfamily='serif')

    # User -> Order (Places)
    ax.plot([46, 23, 23], [66, 66, 24], color='#000000', lw=1.2, ls='--')
    ax.text(25, 45, "places order (1 : N)", fontsize=7.5, weight='bold', fontfamily='serif')

    # Product -> Order (Contains)
    ax.plot([86, 40], [14, 14], color='#000000', lw=1.2)
    ax.text(62, 14.8, "purchases (N : M)", fontsize=7.5, weight='bold', fontfamily='serif')

    plt.tight_layout()
    plt.savefig("class_diagram_bw.png", bbox_inches='tight')
    plt.close()
    print("Elaborate B&W Class diagram generated successfully.")

def draw_er_table(ax, x, y, w, title, columns, font_size=7.2):
    # Header
    hdr_h = 2.2
    body_h = (len(columns) * 1.35) + 0.8
    total_h = hdr_h + body_h
    
    # Outer box
    rect = patches.Rectangle((x, y - total_h), w, total_h, facecolor='#ffffff', edgecolor='#000000', linewidth=1.5)
    ax.add_patch(rect)
    
    # Header bar
    hdr_rect = patches.Rectangle((x, y - hdr_h), w, hdr_h, facecolor='#e5e7eb', edgecolor='#000000', linewidth=1.5)
    ax.add_patch(hdr_rect)
    ax.text(x + w / 2, y - hdr_h / 2, title, color='#000000', weight='bold', fontsize=font_size + 1.2, ha='center', va='center', fontfamily='serif')
    
    # Rows
    for idx, (col_name, col_type, key_type) in enumerate(columns):
        row_y = y - hdr_h - (idx * 1.35) - 1.0
        
        # Key badge / indicator
        key_color = '#000000'
        if key_type == 'PK':
            ax.text(x + 0.5, row_y, "PK", color=key_color, weight='bold', fontsize=font_size - 0.5, fontfamily='monospace')
        elif key_type == 'FK':
            ax.text(x + 0.5, row_y, "FK", color=key_color, weight='bold', fontsize=font_size - 0.5, fontfamily='monospace')
        elif key_type == 'UNI':
            ax.text(x + 0.5, row_y, "UQ", color=key_color, weight='bold', fontsize=font_size - 0.5, fontfamily='monospace')
            
        # Column Name
        ax.text(x + 2.5, row_y, col_name, color='#000000', weight='bold' if key_type == 'PK' else 'normal', fontsize=font_size, fontfamily='monospace')
        
        # Column Type
        ax.text(x + w - 0.5, row_y, col_type, color='#333333', fontsize=font_size - 0.5, ha='right', fontfamily='monospace')
        
        # Sub divider line
        if idx < len(columns) - 1:
            ax.plot([x, x + w], [row_y - 0.35, row_y - 0.35], color='#e2e8f0', linewidth=0.6)
            
    return total_h

def generate_elaborate_er_diagram():
    fig, ax = plt.subplots(figsize=(24, 17), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 95)
    ax.axis('off')

    ax.text(60, 93, "ACADEMIC PREPARATION & RESOURCE EXCHANGE PLATFORM — ENTITY RELATIONSHIP DIAGRAM", 
            fontsize=13, weight='bold', ha='center', va='center', fontfamily='serif')
    ax.plot([20, 100], [91.5, 91.5], color='#000000', lw=1.2)

    # 1. USERS
    draw_er_table(ax, 46, 88, 28, "users (Account Catalog)", [
        ("_id", "ObjectId", "PK"),
        ("studentId", "varchar(20)", "UNI"),
        ("name", "varchar(120)", ""),
        ("email", "varchar(150)", "UNI"),
        ("password", "varchar(255)", ""),
        ("role", "enum(student,mentor,admin,delivery)", ""),
        ("phone", "varchar(30)", ""),
        ("whatsappNumber", "varchar(30)", ""),
        ("mentor_id", "ObjectId", "FK"),
        ("targetExam", "varchar(50)", ""),
        ("authProvider", "varchar(20)", ""),
        ("createdAt", "datetime", "")
    ])

    # 2. EXAMS (Top Left)
    draw_er_table(ax, 6, 88, 26, "exams (Examination Master)", [
        ("_id", "ObjectId", "PK"),
        ("slug", "varchar(50)", "UNI"),
        ("name", "varchar(150)", ""),
        ("category", "varchar(50)", ""),
        ("authority", "varchar(100)", ""),
        ("officialUrl", "varchar(255)", ""),
        ("subjectCount", "int", ""),
        ("createdAt", "datetime", "")
    ])

    # 3. SUBJECTS (Mid Left)
    draw_er_table(ax, 6, 65, 26, "subjects (Hierarchical Catalog)", [
        ("subjectId", "varchar(50)", "PK"),
        ("exam_slug", "varchar(50)", "FK"),
        ("name", "varchar(100)", ""),
        ("weightage", "enum(High,Med,Low)", ""),
        ("chapterCount", "int", ""),
        ("topicCount", "int", "")
    ])

    # 4. PROGRESS (Center Mid)
    draw_er_table(ax, 46, 62, 28, "progress (Syllabus Tracking)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("exam_slug", "varchar(50)", "FK"),
        ("topicStatus", "json / map", ""),
        ("studyDays", "json / array", ""),
        ("streakDays", "int", ""),
        ("completionPct", "decimal(5,2)", ""),
        ("updatedAt", "datetime", "")
    ])

    # 5. MOCK_ATTEMPTS (Center Bottom)
    draw_er_table(ax, 46, 38, 28, "mock_attempts (Test Evaluation)", [
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

    # 6. PRODUCTS (Right Top-Mid)
    draw_er_table(ax, 86, 88, 28, "products (Resource Marketplace)", [
        ("_id", "ObjectId", "PK"),
        ("title", "varchar(255)", ""),
        ("author", "varchar(100)", ""),
        ("exam_slug", "varchar(50)", "FK"),
        ("price", "decimal(10,2)", ""),
        ("condition", "enum(New,Good,Fair)", ""),
        ("isDonation", "boolean", ""),
        ("stock", "int", ""),
        ("seller_id", "ObjectId", "FK"),
        ("status", "varchar(30)", "")
    ])

    # 7. ORDERS (Right Mid)
    draw_er_table(ax, 86, 60, 28, "orders (Commerce Transactions)", [
        ("_id", "ObjectId", "PK"),
        ("trackingId", "varchar(50)", "UNI"),
        ("user_id", "ObjectId", "FK"),
        ("totalAmount", "decimal(10,2)", ""),
        ("paymentMethod", "varchar(30)", ""),
        ("status", "enum(Ordered,InTransit,Delivered)", ""),
        ("verificationOtp", "varchar(4)", ""),
        ("assignedPartner_id", "ObjectId", "FK"),
        ("createdAt", "datetime", "")
    ])

    # 8. ORDER_ITEMS (Right Bottom)
    draw_er_table(ax, 86, 32, 28, "order_items (Line Items)", [
        ("itemId", "ObjectId", "PK"),
        ("order_id", "ObjectId", "FK"),
        ("product_id", "ObjectId", "FK"),
        ("quantity", "int", ""),
        ("priceAtOrder", "decimal(10,2)", ""),
        ("subtotal", "decimal(10,2)", "")
    ])

    # 9. COMMUNICATION_LOGS (Bottom Left)
    draw_er_table(ax, 6, 38, 26, "communication_logs (Alerts)", [
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

    # 10. NOTIFICATIONS (Bottom Center)
    draw_er_table(ax, 46, 12, 28, "notifications (In-App Hub)", [
        ("_id", "ObjectId", "PK"),
        ("user_id", "ObjectId", "FK"),
        ("type", "varchar(30)", ""),
        ("title", "varchar(150)", ""),
        ("body", "text", ""),
        ("fromUser_id", "ObjectId", "FK"),
        ("read", "boolean", ""),
        ("createdAt", "datetime", "")
    ])

    # 11. RETURN_REQUESTS (Far Right Bottom)
    draw_er_table(ax, 86, 12, 28, "return_requests (Reverse Logistics)", [
        ("_id", "ObjectId", "PK"),
        ("trackingId", "varchar(50)", "UNI"),
        ("user_id", "ObjectId", "FK"),
        ("order_id", "ObjectId", "FK"),
        ("type", "enum(return,resale,donation)", ""),
        ("status", "enum(Pending,Inspected,Completed)", ""),
        ("verificationOtp", "varchar(4)", ""),
        ("createdAt", "datetime", "")
    ])

    # Connecting Relational Lines with Crow's Foot / Cardinality Notation
    def draw_rel_line(p1, p2, label1="1", label2="N", label_mid=""):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#000000', lw=1.2)
        ax.text(p1[0] + (0.8 if p1[0] <= p2[0] else -1.5), p1[1], label1, fontsize=7.5, weight='bold', fontfamily='monospace')
        ax.text(p2[0] + (-1.5 if p1[0] <= p2[0] else 0.8), p2[1], label2, fontsize=7.5, weight='bold', fontfamily='monospace')
        if label_mid:
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            ax.text(mid_x, mid_y + 0.6, label_mid, fontsize=6.8, weight='bold', ha='center', fontfamily='serif')

    # users -> users (Self-referencing Mentor 1:N)
    ax.plot([46, 42, 42, 46], [82, 82, 85, 85], color='#000000', lw=1.2)
    ax.text(37.5, 83.5, "1:N\n(mentor)", fontsize=6.8, weight='bold', fontfamily='monospace')

    # users -> progress (1:N)
    draw_rel_line((60, 68), (60, 62), "1", "N")

    # exams -> progress (1:N)
    draw_rel_line((32, 75), (46, 55), "1", "N")

    # exams -> subjects (1:N)
    draw_rel_line((19, 70), (19, 65), "1", "N")

    # progress -> mock_attempts (1:N)
    draw_rel_line((60, 44), (60, 38), "1", "N")

    # mock_attempts -> communication_logs (Triggers WhatsApp Alert)
    draw_rel_line((46, 26), (32, 26), "1", "N", "triggers WhatsApp")

    # users -> orders (1:N)
    draw_rel_line((74, 76), (86, 52), "1", "N")

    # orders -> order_items (1:N)
    draw_rel_line((100, 42), (100, 32), "1", "N")

    # products -> order_items (1:N)
    draw_rel_line((100, 66), (100, 60), "1", "N")

    # users -> products (1:N Seller)
    draw_rel_line((74, 82), (86, 82), "1", "N")

    # users -> notifications (1:N)
    draw_rel_line((60, 20), (60, 12), "1", "N")

    # orders -> return_requests (1:1)
    draw_rel_line((100, 16), (100, 12), "1", "1")

    plt.tight_layout()
    plt.savefig("er_diagram_bw.png", bbox_inches='tight')
    plt.close()
    print("Elaborate B&W ER diagram generated successfully.")

if __name__ == "__main__":
    generate_elaborate_class_diagram()
    generate_elaborate_er_diagram()
