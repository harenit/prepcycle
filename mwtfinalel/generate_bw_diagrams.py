import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_class_diagram_bw(filepath="class_diagram_bw.png"):
    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Strict Black & White Academic UML Styling
    header_color = '#ffffff'
    field_color = '#ffffff'
    border_color = '#000000'

    def draw_class(x, y, w, h, title, fields, methods):
        hdr_h = h * 0.22
        body_h = h - hdr_h
        # Draw outer box
        rect_total = patches.Rectangle((x, y), w, h, facecolor='#ffffff', edgecolor=border_color, linewidth=1.5)
        ax.add_patch(rect_total)
        
        # Header divider
        ax.plot([x, x + w], [y + body_h, y + body_h], color=border_color, linewidth=1.5)
        ax.text(x + w/2, y + body_h + hdr_h/2, title, color='#000000', weight='bold', fontsize=8.5, ha='center', va='center', fontfamily='serif')
        
        # Fields text
        field_text = "\n".join(fields)
        ax.text(x + 1, y + body_h - 1, field_text, color='#000000', fontsize=6.8, ha='left', va='top', fontfamily='monospace')
        
        # Divider line if methods exist
        if methods:
            div_y = y + (len(methods) * 2.2) + 1
            ax.plot([x, x + w], [div_y, div_y], color=border_color, linewidth=1.0)
            method_text = "\n".join(methods)
            ax.text(x + 1, div_y - 1, method_text, color='#000000', fontsize=6.8, ha='left', va='top', fontfamily='monospace', fontstyle='italic')

    # 1. User Class
    draw_class(38, 76, 24, 21, "User (Account Model)", 
               ["+ id: ObjectId [PK]", "+ studentId: String", "+ name: String", "+ email: String [UNIQUE]", "+ role: RoleEnum", "+ phone: String", "+ whatsappNumber: String", "+ mentor: ObjectId [FK]", "+ registeredExams: [String]"],
               ["+ register(): User", "+ authenticate(): Token", "+ updateProfile(): void"])

    # 2. Student (Role)
    draw_class(8, 78, 22, 18, "Student (Role: student)",
               ["+ userRef: ObjectId [FK]", "+ targetExam: String", "+ dailyGoalHours: Number", "+ currentStreak: Number", "+ bookmarkedResources: [Id]"],
               ["+ enrollExam(): void", "+ markTopicComplete(): void", "+ recordMockAttempt(): void"])

    # 3. Mentor (Role)
    draw_class(70, 78, 22, 18, "Mentor (Role: mentor)",
               ["+ userRef: ObjectId [FK]", "+ whatsappNumber: String", "+ bio: String", "+ assignedStudents: [ObjectId]", "+ notificationActive: Boolean"],
               ["+ viewStudentProgress(): List", "+ sendWhatsAppGuidance(): void", "+ receiveMockAlert(): void"])

    # 4. Exam Model (Left Mid)
    draw_class(6, 46, 26, 24, "Exam",
               ["+ id: ObjectId", "+ slug: String [PK]", "+ name: String", "+ category: String", "+ authority: String", "+ eligibility: String", "+ officialUrl: String", "+ subjects: [Subject]"],
               ["+ getSyllabus(): Tree", "+ addSubject(): void", "+ getRoadmapByWeightage(): List"])

    # 5. Progress Model (Center Mid)
    draw_class(38, 46, 24, 24, "Progress",
               ["+ id: ObjectId [PK]", "+ user: ObjectId [FK]", "+ examSlug: String [FK]", "+ topicStatus: Map<id, Status>", "+ studyDays: [Date]", "+ overallScore: Number", "+ dailyLogs: [LogEntry]"],
               ["+ updateTopicStatus(): void", "+ computeCompletion(): Float", "+ checkSubjectMilestone(): Boolean"])

    # 6. MockAttempt Model (Right Mid)
    draw_class(70, 46, 24, 24, "MockAttempt",
               ["+ id: ObjectId [PK]", "+ user: ObjectId [FK]", "+ examSlug: String [FK]", "+ subjectName: String", "+ chapterName: String", "+ mockName: String", "+ marks: Number", "+ maxMarks: Number", "+ attemptedAt: DateTime"],
               ["+ logAttempt(): MockAttempt", "+ notifyAssignedMentor(): void", "+ getPerformanceSummary(): Data"])

    # 7. Marketplace Product (Left Bottom)
    draw_class(6, 12, 26, 26, "Product (Marketplace)",
               ["+ id: ObjectId [PK]", "+ title: String", "+ examSlug: String", "+ subjectName: String", "+ price: Decimal", "+ condition: ConditionEnum", "+ stock: Number", "+ isDonation: Boolean", "+ seller: ObjectId [FK]"],
               ["+ listProduct(): Product", "+ markAsDonated(): void", "+ updateStock(): Boolean"])

    # 8. Order (Center Bottom)
    draw_class(38, 12, 24, 26, "Order",
               ["+ id: ObjectId [PK]", "+ trackingId: String [UNIQUE]", "+ user: ObjectId [FK]", "+ items: [OrderItem]", "+ totalAmount: Decimal", "+ status: OrderStatusEnum", "+ deliveryAddress: Address", "+ verificationOtp: String"],
               ["+ createOrder(): Order", "+ trackTimeline(): StatusInfo", "+ verifyOtpDelivery(): Boolean"])

    # 9. CommunicationLog (Right Bottom)
    draw_class(70, 12, 24, 26, "CommunicationLog",
               ["+ id: ObjectId [PK]", "+ user: ObjectId [FK]", "+ channel: ChannelEnum", "+ messageType: String", "+ recipient: String", "+ subject: String", "+ content: Text", "+ status: DeliveryStatus"],
               ["+ sendWhatsApp(): Result", "+ sendSms(): Result", "+ sendEmail(): Result"])

    # Associations
    arrow_props = dict(arrowstyle="->", color="#000000", lw=1.2)
    
    # User -> Student & Mentor
    ax.annotate("", xy=(30, 85), xytext=(38, 85), arrowprops=arrow_props)
    ax.annotate("", xy=(70, 85), xytext=(62, 85), arrowprops=arrow_props)
    
    # User -> Progress & MockAttempt
    ax.annotate("", xy=(50, 70), xytext=(50, 76), arrowprops=arrow_props)
    ax.annotate("", xy=(82, 70), xytext=(82, 78), arrowprops=arrow_props)

    # Exam -> Progress
    ax.annotate("", xy=(38, 58), xytext=(32, 58), arrowprops=arrow_props)

    # Progress -> MockAttempt
    ax.annotate("", xy=(70, 58), xytext=(62, 58), arrowprops=arrow_props)

    # User -> Order & CommunicationLog
    ax.annotate("", xy=(50, 38), xytext=(50, 46), arrowprops=arrow_props)
    ax.annotate("", xy=(82, 38), xytext=(82, 46), arrowprops=arrow_props)

    # Product -> Order
    ax.annotate("", xy=(38, 25), xytext=(32, 25), arrowprops=arrow_props)

    # Relationship labels
    ax.text(34, 86, "role", fontsize=7, color="#000000", fontfamily='serif')
    ax.text(64, 86, "role", fontsize=7, color="#000000", fontfamily='serif')
    ax.text(51, 73, "1 : N", fontsize=7.5, weight='bold', color="#000000", fontfamily='serif')
    ax.text(34, 59, "1 : N", fontsize=7.5, weight='bold', color="#000000", fontfamily='serif')
    ax.text(65, 59, "1 : N", fontsize=7.5, weight='bold', color="#000000", fontfamily='serif')
    ax.text(34, 26, "contains", fontsize=7, color="#000000", fontfamily='serif')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"B&W Class diagram saved to {filepath}")

def generate_er_diagram_bw(filepath="er_diagram_bw.png"):
    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_entity(x, y, w, h, name):
        rect = patches.Rectangle((x, y), w, h, facecolor='#ffffff', edgecolor='#000000', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, color='#000000', weight='bold', fontsize=8.5, ha='center', va='center', fontfamily='serif')

    def draw_relation(cx, cy, rx, ry, name):
        diamond = patches.Polygon([[cx, cy + ry], [cx + rx, cy], [cx, cy - ry], [cx - rx, cy]], facecolor='#ffffff', edgecolor='#000000', linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(cx, cy, name, color='#000000', weight='bold', fontsize=7.5, ha='center', va='center', fontfamily='serif')

    def draw_attribute(cx, cy, rx, ry, text, is_pk=False):
        ellipse = patches.Ellipse((cx, cy), rx*2, ry*2, facecolor='#ffffff', edgecolor='#000000', linewidth=1.0)
        ax.add_patch(ellipse)
        style = 'italic' if not is_pk else 'normal'
        weight = 'bold' if is_pk else 'normal'
        ax.text(cx, cy, text, color='#000000', fontsize=6.8, ha='center', va='center', fontfamily='monospace', fontstyle=style, weight=weight)

    # 1. USER Entity
    draw_entity(42, 78, 16, 8, "USER")
    draw_attribute(34, 91, 5, 2.2, "id (PK)", is_pk=True)
    draw_attribute(44, 93, 5, 2.2, "studentId")
    draw_attribute(54, 93, 5, 2.2, "email")
    draw_attribute(64, 91, 5, 2.2, "role")
    draw_attribute(66, 85, 5, 2.2, "whatsapp")
    
    # Connecting attributes to USER
    for pt in [(34, 88.8), (44, 90.8), (54, 90.8), (64, 88.8), (61, 85)]:
        ax.plot([50, pt[0]], [86, pt[1]], color='#000000', lw=0.9)

    # 2. EXAM Entity
    draw_entity(10, 48, 16, 8, "EXAM")
    draw_attribute(6, 62, 5, 2.2, "slug (PK)", is_pk=True)
    draw_attribute(16, 62, 5, 2.2, "name")
    draw_attribute(26, 62, 5, 2.2, "authority")
    for pt in [(6, 59.8), (16, 59.8), (24, 59.8)]:
        ax.plot([18, pt[0]], [56, pt[1]], color='#000000', lw=0.9)

    # 3. PROGRESS Entity
    draw_entity(42, 48, 16, 8, "PROGRESS")
    draw_attribute(42, 38, 5, 2.2, "id (PK)", is_pk=True)
    draw_attribute(50, 38, 5, 2.2, "topicStatus")
    draw_attribute(58, 38, 5, 2.2, "streak")
    for pt in [(42, 40.2), (50, 40.2), (58, 40.2)]:
        ax.plot([50, pt[0]], [48, pt[1]], color='#000000', lw=0.9)

    # 4. MOCK_ATTEMPT Entity
    draw_entity(74, 48, 16, 8, "MOCK_ATTEMPT")
    draw_attribute(74, 62, 5, 2.2, "id (PK)", is_pk=True)
    draw_attribute(84, 62, 5, 2.2, "marks")
    draw_attribute(94, 62, 5, 2.2, "mockName")
    for pt in [(74, 59.8), (84, 59.8), (91, 59.8)]:
        ax.plot([82, pt[0]], [56, pt[1]], color='#000000', lw=0.9)

    # 5. PRODUCT Entity
    draw_entity(10, 16, 16, 8, "PRODUCT")
    draw_attribute(6, 6, 5, 2.2, "id (PK)", is_pk=True)
    draw_attribute(16, 6, 5, 2.2, "price")
    draw_attribute(26, 6, 5, 2.2, "title")
    for pt in [(6, 8.2), (16, 8.2), (24, 8.2)]:
        ax.plot([18, pt[0]], [16, pt[1]], color='#000000', lw=0.9)

    # 6. ORDER Entity
    draw_entity(42, 16, 16, 8, "ORDER")
    draw_attribute(36, 6, 5, 2.2, "trackingId")
    draw_attribute(46, 6, 5, 2.2, "totalAmount")
    draw_attribute(56, 6, 5, 2.2, "status")
    for pt in [(38, 8.2), (48, 8.2), (56, 8.2)]:
        ax.plot([50, pt[0]], [16, pt[1]], color='#000000', lw=0.9)

    # 7. COMMUNICATION_LOG Entity
    draw_entity(74, 16, 16, 8, "COMMUNICATION")
    draw_attribute(74, 6, 5, 2.2, "channel")
    draw_attribute(84, 6, 5, 2.2, "recipient")
    draw_attribute(94, 6, 5, 2.2, "status")
    for pt in [(74, 8.2), (84, 8.2), (91, 8.2)]:
        ax.plot([82, pt[0]], [16, pt[1]], color='#000000', lw=0.9)

    # Relationships (Diamonds)
    draw_relation(50, 68, 4.5, 3.5, "TRACKS")
    draw_relation(30, 52, 4.5, 3.5, "ORGANIZES")
    draw_relation(70, 72, 4.5, 3.5, "MENTORS")
    draw_relation(82, 36, 4.5, 3.5, "NOTIFIES")
    draw_relation(30, 20, 4.5, 3.5, "CONTAINS")
    draw_relation(50, 32, 4.5, 3.5, "PLACES")

    # Connect Entities to Relations
    # User -> Tracks -> Progress
    ax.plot([50, 50], [78, 71.5], color='#000000', lw=1.2)
    ax.plot([50, 50], [64.5, 56], color='#000000', lw=1.2)

    # Exam -> Organizes -> Progress
    ax.plot([26, 25.5], [52, 52], color='#000000', lw=1.2)
    ax.plot([34.5, 42], [52, 52], color='#000000', lw=1.2)

    # User -> Mentors -> Student / MockAttempt
    ax.plot([58, 65.5], [82, 74], color='#000000', lw=1.2)
    ax.plot([74.5, 82], [70, 56], color='#000000', lw=1.2)

    # MockAttempt -> Notifies -> Communication
    ax.plot([82, 82], [48, 39.5], color='#000000', lw=1.2)
    ax.plot([82, 82], [32.5, 24], color='#000000', lw=1.2)

    # User -> Places -> Order
    ax.plot([42, 42], [78, 32], color='#000000', lw=1.2, ls=':')
    ax.plot([42, 44], [32, 24], color='#000000', lw=1.2)

    # Product -> Contains -> Order
    ax.plot([26, 25.5], [20, 20], color='#000000', lw=1.2)
    ax.plot([34.5, 42], [20, 20], color='#000000', lw=1.2)

    # Cardinalities
    ax.text(51, 75, "1", weight='bold', fontsize=7.5, color='#000000')
    ax.text(51, 60, "N", weight='bold', fontsize=7.5, color='#000000')
    ax.text(27, 53, "1", weight='bold', fontsize=7.5, color='#000000')
    ax.text(37, 53, "N", weight='bold', fontsize=7.5, color='#000000')
    ax.text(62, 79, "1", weight='bold', fontsize=7.5, color='#000000')
    ax.text(78, 64, "N", weight='bold', fontsize=7.5, color='#000000')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"B&W ER diagram saved to {filepath}")

def generate_architecture_flow_bw(filepath="architecture_flow_bw.png"):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    boxes = [
        ("Client (React 18 + Vite SPA)", "Pages (Exam Explorer, Progress, Marketplace, Orders, Mentor Portal) | Axios + JWT", 80),
        ("HTTP Network / API Boundary", "Authorization: Bearer <JWT> | CORS Headers | JSON Payload (25 MB limit)", 64),
        ("Express Middleware Layer", "rateLimit.js (180 req/min) | auth.js (JWT verify + role RBAC) | Cache-Control: no-store", 48),
        ("Controller & Business Services", "18 Controllers (auth, exams, progress, mock-attempts, mentor, commerce, delivery, chat)", 32),
        ("Database / Persistence Layer", "MongoDB + Mongoose ODM (Indexes, Schemas, Seed Automation)", 16)
    ]

    for title, desc, y in boxes:
        rect = patches.Rectangle((10, y), 80, 11, facecolor='#ffffff', edgecolor='#000000', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(12, y + 7.5, title, weight='bold', fontsize=9.5, color='#000000', fontfamily='serif')
        ax.text(12, y + 3.0, desc, fontsize=7.5, color='#000000', fontfamily='monospace')
        
        # Arrow down to next box
        if y > 16:
            ax.annotate("", xy=(50, y - 5), xytext=(50, y),
                        arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"B&W Architecture flow saved to {filepath}")

if __name__ == "__main__":
    generate_class_diagram_bw()
    generate_er_diagram_bw()
    generate_architecture_flow_bw()
