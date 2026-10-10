import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Users\haren\OneDrive\Desktop\mwtfinalel\compass_tables"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 15)
FONT_REG = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 14)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 13)

FONT_UI_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
FONT_UI_REG = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)

def render_compass_table(collection_name, columns, rows, out_path, width=1298):
    """
    Renders an authentic MongoDB Compass document table view image matching the sample PDF style.
    """
    row_height = 36
    header_y = 52
    header_height = 38
    total_height = header_y + header_height + len(rows) * row_height + 4
    
    img = Image.new('RGB', (width, total_height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 1. Subtle top background bar
    draw.rectangle([0, 0, width, header_y + header_height], fill='#F9FBFA')
    
    # 2. Collection pill tab
    tab_x = 24
    tab_w = max(115, len(collection_name) * 10 + 55)
    tab_h = 34
    draw.rounded_rectangle([tab_x, 14, tab_x + tab_w, 14 + tab_h], radius=4, fill='#FFFFFF', outline='#E1E8ED', width=1)
    
    # Home/database icon
    icon_x = tab_x + 14
    icon_y = 24
    draw.polygon([(icon_x + 6, icon_y), (icon_x, icon_y + 7), (icon_x + 12, icon_y + 7)], fill='#1C2D38')
    draw.rectangle([icon_x + 2, icon_y + 7, icon_x + 10, icon_y + 14], fill='#1C2D38')
    draw.rectangle([icon_x + 4, icon_y + 9, icon_x + 8, icon_y + 14], fill='#FFFFFF')
    
    # Collection name text
    draw.text((icon_x + 18, 22), collection_name, font=FONT_BOLD, fill='#1C2D38')
    
    # 3. Column widths
    col0_w = 52
    num_data_cols = len(columns)
    avail_w = width - col0_w - 2
    col_w = avail_w // num_data_cols
    
    col_x_positions = [col0_w + i * col_w for i in range(num_data_cols + 1)]
    col_x_positions[-1] = width - 1
    
    # 4. Header row background
    draw.rectangle([0, header_y, width, header_y + header_height], fill='#FFFFFF')
    draw.line([(0, header_y + header_height), (width, header_y + header_height)], fill='#E1E8ED', width=1)
    
    # Divider for col 0
    draw.line([(col0_w, header_y), (col0_w, total_height)], fill='#E1E8ED', width=1)
    
    # Header titles
    for idx, (col_name, col_type) in enumerate(columns):
        cx = col_x_positions[idx]
        cx_next = col_x_positions[idx + 1]
        
        draw.line([(cx_next, header_y), (cx_next, total_height)], fill='#E1E8ED', width=1)
        
        draw.text((cx + 14, header_y + 9), col_name, font=FONT_BOLD, fill='#1C2D38')
        name_w = int(draw.textlength(col_name, font=FONT_BOLD))
        draw.text((cx + 14 + name_w + 8, header_y + 9), col_type, font=FONT_REG, fill='#6B7C87')
        
    # 5. Data rows
    curr_y = header_y + header_height
    for r_idx, row_data in enumerate(rows):
        draw.line([(0, curr_y + row_height), (width, curr_y + row_height)], fill='#E1E8ED', width=1)
        
        # Row number
        r_num_str = str(r_idx + 1)
        num_w = int(draw.textlength(r_num_str, font=FONT_SMALL))
        draw.text((col0_w - num_w - 12, curr_y + 9), r_num_str, font=FONT_SMALL, fill='#8998A2')
        
        # Values
        for c_idx, val in enumerate(row_data):
            cx = col_x_positions[c_idx]
            val_str = str(val)
            max_chars = (col_w - 28) // 9
            if len(val_str) > max_chars:
                display_val = val_str[:max_chars - 3] + "..."
            else:
                display_val = val_str
                
            color = '#00684A' # Compass string green
            if display_val in ['true', 'false']:
                color = '#B45309'
            elif display_val.isdigit():
                color = '#0F766E'
            elif display_val == 'null':
                color = '#6B7C87'
                
            draw.text((cx + 14, curr_y + 9), display_val, font=FONT_REG, fill=color)
            
        curr_y += row_height
        
    img.save(out_path)
    print(f"Rendered: {os.path.basename(out_path)} ({width}x{total_height})")

def render_compass_collections_overview(out_path, width=1358):
    """
    Renders MongoDB Compass Collections overview (Fig 5.1) with crisp geometric sort arrows.
    """
    row_height = 40
    header_y = 12
    header_height = 42
    
    rows = [
        ("communication_logs", "-", "36.86 kB", "7.45 kB", "18", "414.00 B", "1", "36.86 kB"),
        ("discussions", "-", "20.48 kB", "2.10 kB", "6", "350.00 B", "1", "20.48 kB"),
        ("exams", "-", "40.96 kB", "15.20 kB", "5", "3.04 kB", "2", "40.96 kB"),
        ("flashcards", "-", "32.77 kB", "4.80 kB", "24", "200.00 B", "1", "32.77 kB"),
        ("mock_attempts", "-", "36.86 kB", "6.10 kB", "12", "508.33 B", "2", "36.86 kB"),
        ("notes", "-", "24.58 kB", "3.40 kB", "8", "425.00 B", "1", "24.58 kB"),
        ("notifications", "-", "20.48 kB", "1.80 kB", "14", "128.57 B", "1", "20.48 kB"),
        ("order_items", "-", "28.67 kB", "3.20 kB", "10", "320.00 B", "1", "28.67 kB"),
        ("orders", "-", "32.77 kB", "4.90 kB", "8", "612.50 B", "2", "32.77 kB"),
        ("products", "-", "40.96 kB", "12.40 kB", "15", "826.67 B", "2", "40.96 kB"),
        ("progress", "-", "32.77 kB", "5.60 kB", "10", "560.00 B", "2", "32.77 kB"),
        ("recently_accessed", "-", "20.48 kB", "850.00 B", "7", "121.43 B", "1", "20.48 kB"),
        ("return_requests", "-", "20.48 kB", "620.00 B", "3", "206.67 B", "1", "20.48 kB"),
        ("users", "-", "45.06 kB", "8.90 kB", "20", "445.00 B", "3", "45.06 kB"),
    ]
    
    total_height = header_y + header_height + len(rows) * row_height + 10
    img = Image.new('RGB', (width, total_height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    headers = [
        ("Collection name", 240),
        ("Properties", 120),
        ("Storage size", 150),
        ("Data size", 140),
        ("Documents", 140),
        ("Avg. document size", 180),
        ("Indexes", 120),
        ("Total index size", 160)
    ]
    
    draw.line([(0, header_y + header_height), (width, header_y + header_height)], fill='#E1E8ED', width=1)
    
    cur_x = 24
    x_offsets = []
    for h_title, w in headers:
        x_offsets.append(cur_x)
        draw.text((cur_x, header_y + 10), h_title, font=FONT_UI_BOLD, fill='#1C2D38')
        tw = int(draw.textlength(h_title, font=FONT_UI_BOLD))
        
        # Draw crisp sort arrows
        ax = cur_x + tw + 10
        ay = header_y + 20
        draw.polygon([(ax, ay - 6), (ax - 4, ay - 1), (ax + 4, ay - 1)], fill='#6B7C87')
        draw.polygon([(ax, ay + 6), (ax - 4, ay + 1), (ax + 4, ay + 1)], fill='#6B7C87')
        
        cur_x += w
        
    cur_y = header_y + header_height
    for row in rows:
        draw.line([(0, cur_y + row_height), (width, cur_y + row_height)], fill='#F0F4F6', width=1)
        
        draw.text((x_offsets[0], cur_y + 10), row[0], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[1], cur_y + 10), row[1], font=FONT_UI_REG, fill='#6B7C87')
        draw.text((x_offsets[2], cur_y + 10), row[2], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[3], cur_y + 10), row[3], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[4], cur_y + 10), row[4], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[5], cur_y + 10), row[5], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[6], cur_y + 10), row[6], font=FONT_UI_REG, fill='#1C2D38')
        draw.text((x_offsets[7], cur_y + 10), row[7], font=FONT_UI_REG, fill='#1C2D38')
        
        cur_y += row_height
        
    img.save(out_path)
    print(f"Rendered Overview: {out_path} ({width}x{total_height})")

def generate_all():
    render_compass_collections_overview(os.path.join(OUTPUT_DIR, "fig_5_1_collections.png"))
    
    # 5.2 Users (10 rows)
    render_compass_table(
        "users",
        [("id", "String"), ("name", "String"), ("email", "String"), ("role", "String"), ("studentId", "String")],
        [
            ['"u1"', '"Hareni T"', '"hareni@prepcycle.com"', '"student"', '"PC-STU-100001"'],
            ['"u2"', '"Dr. Ramanathan"', '"mentor@prepcycle.com"', '"mentor"', 'null'],
            ['"u3"', '"Murugan K"', '"delivery@prepcycle.com"', '"delivery"', 'null'],
            ['"u4"', '"System Administrator"', '"admin@prepcycle.com"', '"admin"', 'null'],
            ['"u5"', '"Ananya Sundaram"', '"ananya@prepcycle.com"', '"student"', '"PC-STU-100002"'],
            ['"u6"', '"Karthik Raja"', '"karthik@prepcycle.com"', '"student"', '"PC-STU-100003"'],
            ['"u7"', '"Prof. V. Sharma"', '"sharma@prepcycle.com"', '"mentor"', 'null'],
            ['"u8"', '"Selvam P"', '"selvam@prepcycle.com"', '"delivery"', 'null'],
            ['"u9"', '"Pooja Ramesh"', '"pooja@prepcycle.com"', '"student"', '"PC-STU-100004"'],
            ['"u10"', '"Venkatesh S"', '"venkat@prepcycle.com"', '"student"', '"PC-STU-100005"'],
        ],
        os.path.join(OUTPUT_DIR, "table_5_2_users.png")
    )
    
    # 5.3 Exams (5 rows)
    render_compass_table(
        "exams",
        [("slug", "String"), ("name", "String"), ("category", "String"), ("authority", "String"), ("officialUrl", "String")],
        [
            ['"gate-cse"', '"GATE Computer Science"', '"Engineering"', '"IIT Roorkee / GATE Comm."', '"https://gate2026.iitr.ac.in"'],
            ['"upsc-cse"', '"Civil Services Prelims"', '"Civil Services"', '"Union Public Service Comm."', '"https://upsc.gov.in"'],
            ['"jee-adv"', '"JEE Advanced (Paper 1)"', '"Engineering"', '"IIT Madras / JAB"', '"https://jeeadv.ac.in"'],
            ['"neet-ug"', '"National Eligibility Test"', '"Medical"', '"National Testing Agency"', '"https://exams.nta.ac.in/NEET"'],
            ['"cat-2026"', '"Common Admission Test"', '"Management"', '"IIM Kozhikode / CAT Comm."', '"https://iimcat.ac.in"']
        ],
        os.path.join(OUTPUT_DIR, "table_5_3_exams.png")
    )
    
    # 5.4 Progress (5 rows)
    render_compass_table(
        "progress",
        [("userId", "String"), ("examSlug", "String"), ("currentStreak", "Number"), ("activeDays", "Number"), ("overallPct", "Number")],
        [
            ['"u1"', '"gate-cse"', '14', '28', '64.5'],
            ['"u5"', '"gate-cse"', '7', '18', '42.0'],
            ['"u6"', '"upsc-cse"', '21', '35', '78.2'],
            ['"u9"', '"jee-adv"', '5', '12', '31.0'],
            ['"u10"', '"cat-2026"', '9', '20', '55.4']
        ],
        os.path.join(OUTPUT_DIR, "table_5_4_progress.png")
    )
    
    # 5.5 Mock Attempts (6 rows)
    render_compass_table(
        "mock_attempts",
        [("userId", "String"), ("examSlug", "String"), ("mockName", "String"), ("marks", "Number"), ("maxMarks", "Number")],
        [
            ['"u1"', '"gate-cse"', '"Algorithms CBT Mock 1"', '78.5', '100'],
            ['"u1"', '"gate-cse"', '"Operating Systems Mock 2"', '84.0', '100'],
            ['"u5"', '"gate-cse"', '"Discrete Math Quiz 1"', '62.0', '100'],
            ['"u6"', '"upsc-cse"', '"Indian Polity Prelims 1"', '71.0', '100'],
            ['"u9"', '"jee-adv"', '"Physics Mechanics CBT"', '54.5', '100'],
            ['"u10"', '"cat-2026"', '"Quantitative Ability Mock"', '88.0', '100']
        ],
        os.path.join(OUTPUT_DIR, "table_5_5_mock_attempts.png")
    )
    
    # 5.6 Products (6 rows)
    render_compass_table(
        "products",
        [("id", "String"), ("title", "String"), ("examSlug", "String"), ("price", "Number"), ("condition", "String"), ("isDonation", "Boolean")],
        [
            ['"p1"', '"CLRS Introduction to Algorithms"', '"gate-cse"', '450.00', '"Like New"', 'false'],
            ['"p2"', '"Galvin Operating System Concepts"', '"gate-cse"', '380.00', '"Good"', 'false'],
            ['"p3"', '"M. Laxmikanth Indian Polity 7th"', '"upsc-cse"', '0.00', '"Good"', 'true'],
            ['"p4"', '"Irodov Problems in Gen Physics"', '"jee-adv"', '180.00', '"Fair"', 'false'],
            ['"p5"', '"Arun Sharma Quantitative Aptitude"', '"cat-2026"', '290.00', '"Like New"', 'false'],
            ['"p6"', '"Tanenbaum Computer Networks 6th"', '"gate-cse"', '0.00', '"Good"', 'true']
        ],
        os.path.join(OUTPUT_DIR, "table_5_6_products.png")
    )
    
    # 5.7 Orders (5 rows)
    render_compass_table(
        "orders",
        [("trackingId", "String"), ("buyerId", "String"), ("totalAmount", "Number"), ("paymentMethod", "String"), ("status", "String"), ("otp", "String")],
        [
            ['"TRK-482910"', '"u1"', '450.00', '"upi"', '"Delivered"', '"4819"'],
            ['"TRK-591024"', '"u5"', '380.00', '"cod"', '"Out for Delivery"', '"7321"'],
            ['"TRK-602931"', '"u6"', '0.00', '"free_donation"', '"In Transit"', '"9182"'],
            ['"TRK-718294"', '"u9"', '180.00', '"card"', '"Dispatched"', '"5504"'],
            ['"TRK-829105"', '"u10"', '290.00', '"upi"', '"Ordered"', '"3198"']
        ],
        os.path.join(OUTPUT_DIR, "table_5_7_orders.png")
    )
    
    # 5.8 Order Items (5 rows)
    render_compass_table(
        "order_items",
        [("id", "String"), ("orderTrackingId", "String"), ("productId", "String"), ("quantity", "Number"), ("unitPrice", "Number")],
        [
            ['"oi1"', '"TRK-482910"', '"p1"', '1', '450.00'],
            ['"oi2"', '"TRK-591024"', '"p2"', '1', '380.00'],
            ['"oi3"', '"TRK-602931"', '"p3"', '1', '0.00'],
            ['"oi4"', '"TRK-718294"', '"p4"', '1', '180.00'],
            ['"oi5"', '"TRK-829105"', '"p5"', '1', '290.00']
        ],
        os.path.join(OUTPUT_DIR, "table_5_8_order_items.png")
    )
    
    # 5.9 Communication Logs (5 rows)
    render_compass_table(
        "communication_logs",
        [("id", "String"), ("channel", "String"), ("recipient", "String"), ("messageType", "String"), ("status", "String")],
        [
            ['"c1"', '"whatsapp"', '"+919443128490"', '"mock_completion_alert"', '"delivered"'],
            ['"c2"', '"sms"', '"+919842109845"', '"daily_login_notification"', '"delivered"'],
            ['"c3"', '"email"', '"mentor@prepcycle.com"', '"weekly_progress_summary"', '"delivered"'],
            ['"c4"', '"whatsapp"', '"+919443128490"', '"subject_finished_alert"', '"delivered"'],
            ['"c5"', '"email"', '"sharma@prepcycle.com"', '"lagging_student_flag"', '"delivered"']
        ],
        os.path.join(OUTPUT_DIR, "table_5_9_communication_logs.png")
    )
    
    # 5.10 Discussions (5 rows)
    render_compass_table(
        "discussions",
        [("id", "String"), ("authorId", "String"), ("examSlug", "String"), ("title", "String"), ("upvotes", "Number"), ("resolved", "Boolean")],
        [
            ['"d1"', '"u1"', '"gate-cse"', '"Time complexity of Master Theorem Case 2"', '14', 'true'],
            ['"d2"', '"u5"', '"gate-cse"', '"Difference between P and NP complete"', '8', 'true'],
            ['"d3"', '"u6"', '"upsc-cse"', '"Key constitutional amendments in Article 368"', '19', 'false'],
            ['"d4"', '"u9"', '"jee-adv"', '"Rotational dynamics conservation of L"', '11', 'true'],
            ['"d5"', '"u10"', '"cat-2026"', '"Shortcuts for circular arrangement DI sets"', '7', 'false']
        ],
        os.path.join(OUTPUT_DIR, "table_5_10_discussions.png")
    )
    
    # 5.11 Notifications (5 rows)
    render_compass_table(
        "notifications",
        [("id", "String"), ("userId", "String"), ("type", "String"), ("title", "String"), ("isRead", "Boolean")],
        [
            ['"n1"', '"u1"', '"mock"', '"Algorithms CBT Mock evaluated: 78.5/100"', 'true'],
            ['"n2"', '"u1"', '"order"', '"Your order TRK-482910 has been delivered!"', 'true'],
            ['"n3"', '"u2"', '"mentor"', '"Student Hareni T completed OS Chapter 3"', 'false'],
            ['"n4"', '"u5"', '"streak"', '"7-Day study streak achieved! Keep going!"', 'true'],
            ['"n5"', '"u6"', '"community"', '"Your answer was upvoted by 5 students"', 'false']
        ],
        os.path.join(OUTPUT_DIR, "table_5_11_notifications.png")
    )
    
    # 5.12 Return Requests (3 rows)
    render_compass_table(
        "return_requests",
        [("id", "String"), ("trackingId", "String"), ("userId", "String"), ("reason", "String"), ("status", "String")],
        [
            ['"ret1"', '"TRK-482910"', '"u1"', '"exam_completed_buyback"', '"approved"'],
            ['"ret2"', '"TRK-391824"', '"u5"', '"wrong_edition_delivered"', '"pickup_scheduled"'],
            ['"ret3"', '"TRK-294819"', '"u6"', '"pages_damaged_in_transit"', '"refunded"']
        ],
        os.path.join(OUTPUT_DIR, "table_5_12_return_requests.png")
    )
    
    # 5.13 Flashcards (5 rows)
    render_compass_table(
        "flashcards",
        [("id", "String"), ("examSlug", "String"), ("subject", "String"), ("question", "String"), ("masteredCount", "Number")],
        [
            ['"fc1"', '"gate-cse"', '"Algorithms"', '"What is the Master Theorem formula?"', '42'],
            ['"fc2"', '"gate-cse"', '"Operating Systems"', '"What are Coffman conditions for deadlock?"', '38'],
            ['"fc3"', '"gate-cse"', '"Databases"', '"Explain Boyce-Codd Normal Form (BCNF)"', '51'],
            ['"fc4"', '"upsc-cse"', '"Polity"', '"Which Article defines the Finance Commission?"', '29'],
            ['"fc5"', '"jee-adv"', '"Physics"', '"Write Biot-Savart law in vector form"', '33']
        ],
        os.path.join(OUTPUT_DIR, "table_5_13_flashcards.png")
    )
    
    # 5.14 Notes (5 rows)
    render_compass_table(
        "notes",
        [("id", "String"), ("userId", "String"), ("examSlug", "String"), ("topicName", "String"), ("isPublic", "Boolean")],
        [
            ['"nt1"', '"u1"', '"gate-cse"', '"Dynamic Programming Summary & Memoization"', 'true'],
            ['"nt2"', '"u1"', '"gate-cse"', '"Virtual Memory Paging and TLB Miss Flow"', 'true'],
            ['"nt3"', '"u5"', '"gate-cse"', '"SQL Joins and Index B-Tree Architecture"', 'false'],
            ['"nt4"', '"u6"', '"upsc-cse"', '"Preamble Key Doctrines and Case Laws"', 'true'],
            ['"nt5"', '"u10"', '"cat-2026"', '"Permutations & Combinations Cheat Sheet"', 'false']
        ],
        os.path.join(OUTPUT_DIR, "table_5_14_notes.png")
    )
    
    # 5.15 Recently Accessed (5 rows)
    render_compass_table(
        "recently_accessed",
        [("id", "String"), ("userId", "String"), ("itemType", "String"), ("itemId", "String"), ("title", "String")],
        [
            ['"ra1"', '"u1"', '"exam"', '"gate-cse"', '"GATE Computer Science Roadmap"'],
            ['"ra2"', '"u1"', '"topic"', '"algorithms-dp"', '"Dynamic Programming"'],
            ['"ra3"', '"u1"', '"mock"', '"mock-cbt-1"', '"Algorithms CBT Mock 1"'],
            ['"ra4"', '"u2"', '"student"', '"u1"', '"Student Profile: Hareni T"'],
            ['"ra5"', '"u5"', '"exam"', '"gate-cse"', '"GATE Computer Science Roadmap"']
        ],
        os.path.join(OUTPUT_DIR, "table_5_15_recently_accessed.png")
    )

if __name__ == "__main__":
    generate_all()
