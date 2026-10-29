"""Generate realistic, high-resolution application screenshots for ScholarNexus AI
matching the exact Streamlit user interface components for academic reports.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
from pathlib import Path

# Dimensions: 1600 x 1000 px, 150 DPI
WIDTH, HEIGHT = 16, 10
DPI = 150

BG_APP = '#090d16'
BG_SIDEBAR = '#0f172a'
BG_CARD = '#131e33'
BORDER_CARD = '#1e293b'
ACCENT_BLUE = '#38bdf8'
ACCENT_GREEN = '#10b981'
ACCENT_AMBER = '#f59e0b'
ACCENT_RED = '#f43f5e'
TEXT_WHITE = '#ffffff'
TEXT_MUTED = '#94a3b8'
TEXT_DARK = '#020617'

def setup_canvas():
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT), dpi=DPI)
    fig.patch.set_facecolor(BG_APP)
    ax.set_facecolor(BG_APP)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 1000)
    ax.axis('off')
    
    # 1. Window Browser Header (macOS/Chrome Style)
    win_bar = Rectangle((0, 960), 1600, 40, facecolor='#0b1120', edgecolor='#1e293b', zorder=1)
    ax.add_patch(win_bar)
    for i, c in enumerate(['#f43f5e', '#f59e0b', '#10b981']):
        dot = Circle((30 + i*22, 980), 5.5, facecolor=c, zorder=2)
        ax.add_patch(dot)
    
    # URL bar
    url_box = FancyBboxPatch((400, 968), 800, 24, boxstyle="round,pad=0,rounding_size=5",
                             facecolor='#172136', edgecolor='#2d3d59', zorder=2)
    ax.add_patch(url_box)
    ax.text(800, 980, "http://localhost:8501 — ScholarNexus AI", ha='center', va='center',
            color='#94a3b8', fontsize=8.5, family='sans-serif', zorder=3)
    
    # 2. Sidebar (Left 0 to 320)
    sidebar = Rectangle((0, 0), 320, 960, facecolor=BG_SIDEBAR, edgecolor='#1e293b', zorder=1)
    ax.add_patch(sidebar)
    
    ax.text(30, 920, "ScholarNexus AI", color=TEXT_WHITE, fontsize=14, fontweight='bold', zorder=2)
    ax.text(30, 900, "Govt Schemes & Scholarship Assistant", color=ACCENT_BLUE, fontsize=7.5, zorder=2)
    
    # Navigation items in sidebar
    navs = [
        ("🏠 Home Dashboard", True),
        ("👤 Student Profile & Match", False),
        ("🔍 Scheme Explorer & Filter", False),
        ("📋 Document Checklist", False),
        ("🤖 AI ScholarBot Chat", False),
        ("ℹ️ Official Portals Directory", False)
    ]
    return fig, ax

def draw_sidebar_nav(ax, active_idx=0):
    navs = [
        "[Home]  Home Dashboard",
        "[Profile]  Student Profile & Match",
        "[Search]  Scheme Explorer & Filter",
        "[Docs]  Document Checklist",
        "[AI]  AI ScholarBot Chat",
        "[Info]  Official Portals Directory"
    ]
    for i, name in enumerate(navs):
        ny = 830 - (i * 44)
        is_active = (i == active_idx)
        if is_active:
            pill = FancyBboxPatch((20, ny-6), 280, 32, boxstyle="round,pad=0,rounding_size=6",
                                  facecolor='#0284c7', edgecolor='none', zorder=3)
            ax.add_patch(pill)
            ax.text(35, ny + 10, name, color=TEXT_WHITE, fontsize=9.2, fontweight='bold', zorder=4)
        else:
            ax.text(35, ny + 10, name, color=TEXT_MUTED, fontsize=9, zorder=4)
            
    # Sidebar Profile Card
    card = FancyBboxPatch((20, 350), 280, 160, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#162238', edgecolor='#253552', zorder=3)
    ax.add_patch(card)
    ax.text(35, 485, "Active Student Profile", color=ACCENT_BLUE, fontsize=9.5, fontweight='bold', zorder=4)
    ax.text(35, 460, "Course: B.Tech (1st Year)", color='#cbd5e1', fontsize=8, zorder=4)
    ax.text(35, 440, "State: Maharashtra | Cat: General", color='#cbd5e1', fontsize=8, zorder=4)
    ax.text(35, 420, "Income: Rs 2,50,000 / year", color='#cbd5e1', fontsize=8, zorder=4)
    ax.text(35, 400, "Gender: Female | PwD: No", color='#cbd5e1', fontsize=8, zorder=4)
    
    # Progress
    pbar_bg = Rectangle((35, 375), 250, 6, facecolor='#0f172a', zorder=4)
    ax.add_patch(pbar_bg)
    pbar_fg = Rectangle((35, 375), 250 * 0.85, 6, facecolor=ACCENT_GREEN, zorder=5)
    ax.add_patch(pbar_fg)
    ax.text(35, 362, "Profile Completeness: 85%", color='#94a3b8', fontsize=7.2, zorder=4)

    # Sidebar Engine Mode
    status_card = FancyBboxPatch((20, 160), 280, 95, boxstyle="round,pad=0,rounding_size=8",
                                 facecolor='#111c30', edgecolor='#1e2c45', zorder=3)
    ax.add_patch(status_card)
    ax.text(35, 230, "System Engine Mode", color=TEXT_WHITE, fontsize=9, fontweight='bold', zorder=4)
    ax.text(35, 208, "● LLM API: Google Gemini Active", color=ACCENT_GREEN, fontsize=8, fontweight='bold', zorder=4)
    ax.text(35, 185, "● Grounded Offline Demo: Ready", color='#94a3b8', fontsize=7.6, zorder=4)
    ax.text(35, 170, "Data: 100% Verified Govt Sources", color=ACCENT_BLUE, fontsize=7.5, zorder=4)

def draw_main_header(ax, title="ScholarNexus AI", subtitle="AI-Powered Scholarship Intelligence & Eligibility Matching Platform"):
    # Header Banner
    banner = FancyBboxPatch((350, 830), 1220, 95, boxstyle="round,pad=0,rounding_size=10",
                            facecolor='#0d2847', edgecolor='#0369a1', linewidth=1.5, zorder=2)
    ax.add_patch(banner)
    ax.text(375, 890, title, color=TEXT_WHITE, fontsize=18, fontweight='bold', zorder=3)
    ax.text(375, 860, subtitle, color='#bae6fd', fontsize=9.5, zorder=3)
    
    # Official Disclaimer
    disc = FancyBboxPatch((350, 755), 1220, 60, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#261c02', edgecolor='#b45309', linewidth=1.2, zorder=2)
    ax.add_patch(disc)
    ax.text(370, 792, "⚠️ OFFICIAL DISCLAIMER:", color='#fbbf24', fontsize=8.8, fontweight='bold', zorder=3)
    ax.text(370, 772, "Preliminary matches generated by ScholarNexus AI are for informational & guidance purposes only. They do not constitute an official award guarantee.", color='#fde68a', fontsize=7.8, zorder=3)

# ---------------- SCREENSHOT 1: HOME DASHBOARD ----------------
def create_screenshot_1():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=0)
    draw_main_header(ax)
    
    # Metric cards
    metrics = [
        ("12", "Curated Govt Schemes", ACCENT_BLUE),
        ("Rs 93,600", "Max Annual Benefit", ACCENT_GREEN),
        ("100%", "Source-Verified", ACCENT_AMBER),
        ("0", "Hallucinated Data", '#38bdf8')
    ]
    for i, (val, lbl, col) in enumerate(metrics):
        cx = 350 + (i * 312)
        card = FancyBboxPatch((cx, 630), 290, 95, boxstyle="round,pad=0,rounding_size=10",
                              facecolor=BG_CARD, edgecolor=BORDER_CARD, linewidth=1.5, zorder=2)
        ax.add_patch(card)
        ax.text(cx + 145, 688, val, ha='center', va='center', color=col, fontsize=18, fontweight='bold', zorder=3)
        ax.text(cx + 145, 655, lbl, ha='center', va='center', color=TEXT_MUTED, fontsize=8.5, fontweight='bold', zorder=3)
        
    # Quick action containers
    actions = [
        ("[Match]  Check My Eligibility", "Fill your academic profile, income, and category to evaluate exact matches against central and state gazettes.", "Start Eligibility Check ->", ACCENT_BLUE),
        ("[Directory]  Browse & Filter Schemes", "Search all 12 verified schemes by state, ministry, gender, category, and maximum family income limits.", "Explore Directory ->", ACCENT_GREEN),
        ("[Chat]  Ask AI ScholarBot", "Consult the grounded AI assistant on dual scholarships, bank account NPCI mapping, and document guidelines.", "Open AI Chatbot ->", '#a855f7')
    ]
    for j, (atitle, adesc, abtn, acol) in enumerate(actions):
        ax_x = 350 + (j * 420)
        acard = FancyBboxPatch((ax_x, 380), 390, 215, boxstyle="round,pad=0,rounding_size=10",
                               facecolor='#101a2e', edgecolor='#1e2c45', linewidth=1.5, zorder=2)
        ax.add_patch(acard)
        ax.text(ax_x + 20, 560, atitle, color=TEXT_WHITE, fontsize=11, fontweight='bold', zorder=3)
        ax.text(ax_x + 20, 510, adesc, color=TEXT_MUTED, fontsize=8, wrap=True, zorder=3)
        
        # Action button
        btn = FancyBboxPatch((ax_x + 20, 405), 350, 38, boxstyle="round,pad=0,rounding_size=6",
                             facecolor=acol, edgecolor='none', zorder=3)
        ax.add_patch(btn)
        ax.text(ax_x + 195, 424, abtn, ha='center', va='center', color=TEXT_DARK if acol!= '#a855f7' else TEXT_WHITE,
                fontsize=8.8, fontweight='bold', zorder=4)

    # Lower Information Banner
    ann_card = FancyBboxPatch((350, 210), 1220, 135, boxstyle="round,pad=0,rounding_size=10",
                              facecolor='#0f192b', edgecolor='#1e2a40', linewidth=1.2, zorder=2)
    ax.add_patch(ann_card)
    ax.text(375, 315, "[Notice] Official Portal Academic Cycle Guidance", color=ACCENT_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(375, 280, "Government scholarship portals (NSP, AICTE, MahaDBT) operate on annual academic cycles. Application windows usually open between July and September,", color='#cbd5e1', fontsize=8, zorder=3)
    ax.text(375, 260, "and close between November and January. ScholarNexus AI strictly references official portals and does not fabricate artificial countdown timers.", color='#cbd5e1', fontsize=8, zorder=3)
    ax.text(375, 235, "Verified Portals Active: National Scholarship Portal (scholarships.gov.in) | AICTE Schemes Portal | UGC Ishan Uday | MahaDBT | UP Scholarship | Karnataka SSP", color='#94a3b8', fontsize=7.8, zorder=3)

    plt.tight_layout()
    plt.savefig("screenshot_3_1_home_dashboard.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 1 generated: screenshot_3_1_home_dashboard.png")

# ---------------- SCREENSHOT 2: STUDENT PROFILE ----------------
def create_screenshot_2():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=1)
    draw_main_header(ax, "Student Profile & Eligibility Matching Form", "Enter your academic, demographic, and financial details for deterministic rule evaluation")
    
    # Form Container
    form_box = FancyBboxPatch((350, 140), 1220, 600, boxstyle="round,pad=0,rounding_size=10",
                              facecolor='#111b2e', edgecolor='#1e2d47', linewidth=1.5, zorder=2)
    ax.add_patch(form_box)
    
    # Left Column: Academic
    ax.text(380, 705, "[Academic] Academic Background", color=ACCENT_BLUE, fontsize=12, fontweight='bold', zorder=3)
    
    fields_left = [
        ("Education Level *", "Undergraduate (UG)"),
        ("Degree / Stream *", "B.Tech / B.E. (Engineering)"),
        ("Year of Study *", "1st Year (Fresh Admission)"),
        ("Qualifying Score / Board Marks (%) *", "85.50 %")
    ]
    for i, (label, val) in enumerate(fields_left):
        fy = 640 - (i * 90)
        ax.text(380, fy + 24, label, color=TEXT_WHITE, fontsize=8.8, fontweight='bold', zorder=3)
        inp = FancyBboxPatch((380, fy - 18), 540, 36, boxstyle="round,pad=0,rounding_size=6",
                             facecolor='#090f1d', edgecolor='#253856', linewidth=1, zorder=3)
        ax.add_patch(inp)
        ax.text(395, fy, val, color='#e2e8f0', fontsize=8.5, zorder=4)

    # Checkboxes
    chk1 = FancyBboxPatch((380, 240), 20, 20, boxstyle="round,pad=0,rounding_size=4", facecolor=ACCENT_GREEN, zorder=3)
    ax.add_patch(chk1)
    ax.text(415, 250, "[x] Course is AICTE / Technical Approved", color='#e2e8f0', fontsize=8.5, zorder=3)
    
    chk2 = FancyBboxPatch((380, 200), 20, 20, boxstyle="round,pad=0,rounding_size=4", facecolor='#1e293b', edgecolor='#334155', zorder=3)
    ax.add_patch(chk2)
    ax.text(415, 210, "[ ] Currently staying in College Hostel (Hosteller)", color='#94a3b8', fontsize=8.5, zorder=3)

    # Right Column: Personal & Financial
    ax.text(980, 705, "[Personal] Personal & Financial Criteria", color=ACCENT_AMBER, fontsize=12, fontweight='bold', zorder=3)
    
    fields_right = [
        ("Permanent Domicile State / UT *", "Maharashtra"),
        ("Gross Annual Family Income (INR Rs) *", "Rs 2,50,000 / year (Under Rs 2.5 Lakh cap)"),
        ("Social Category / Caste *", "General / Open"),
        ("Gender *", "Female (Eligible for Girl Scholar Programs)")
    ]
    for j, (label, val) in enumerate(fields_right):
        fy = 640 - (j * 90)
        ax.text(980, fy + 24, label, color=TEXT_WHITE, fontsize=8.8, fontweight='bold', zorder=3)
        inp = FancyBboxPatch((980, fy - 18), 540, 36, boxstyle="round,pad=0,rounding_size=6",
                             facecolor='#090f1d', edgecolor='#253856', linewidth=1, zorder=3)
        ax.add_patch(inp)
        ax.text(995, fy, val, color='#e2e8f0', fontsize=8.5, zorder=4)

    # Submit Button
    sbtn = FancyBboxPatch((380, 160), 1160, 48, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#0284c7', edgecolor='none', zorder=3)
    ax.add_patch(sbtn)
    ax.text(960, 184, "🔍 Evaluate My Eligibility Across All 12 Government Schemes", ha='center', va='center',
            color=TEXT_WHITE, fontsize=10.5, fontweight='bold', zorder=4)

    plt.tight_layout()
    plt.savefig("screenshot_3_2_student_profile.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 2 generated: screenshot_3_2_student_profile.png")

# ---------------- SCREENSHOT 3: ELIGIBILITY RESULTS ----------------
def create_screenshot_3():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=1)
    draw_main_header(ax, "Scheme Eligibility Evaluation Results", "Deterministic match breakdown showing satisfied rules, unmet gates, and verification checkpoints")
    
    # Summary Bar
    sbar = FancyBboxPatch((350, 680), 1220, 50, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#0b2e1e', edgecolor='#059669', linewidth=1.2, zorder=2)
    ax.add_patch(sbar)
    ax.text(375, 705, "[Status] Preliminary Evaluation: 3 Schemes Matched (Eligible) | 9 Schemes Ineligible (Criteria Unmet)",
            color='#6ee7b7', fontsize=9.8, fontweight='bold', zorder=3)
    
    # Scheme 1: AICTE Pragati (Eligible)
    c1 = FancyBboxPatch((350, 440), 1220, 220, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#0d1b2e', edgecolor='#0284c7', linewidth=1.8, zorder=2)
    ax.add_patch(c1)
    ax.text(375, 625, "[Eligible] AICTE Pragati Scholarship Scheme for Girl Students (Technical Degree)", color=TEXT_WHITE, fontsize=12.5, fontweight='bold', zorder=3)
    ax.text(375, 602, "Ministry / Authority: All India Council for Technical Education (AICTE) | Type: UGC/AICTE Technical | Portal: National Scholarship Portal (NSP)", color=TEXT_MUTED, fontsize=8, zorder=3)
    
    # Benefit Badge
    bb1 = FancyBboxPatch((1370, 605), 180, 36, boxstyle="round,pad=0,rounding_size=6", facecolor='#022c22', edgecolor='#059669', zorder=3)
    ax.add_patch(bb1)
    ax.text(1460, 623, "Rs 50,000 / year", ha='center', va='center', color=ACCENT_GREEN, fontsize=10, fontweight='bold', zorder=4)

    # Detailed criteria breakdown boxes
    b_pass = FancyBboxPatch((375, 465), 570, 115, boxstyle="round,pad=0,rounding_size=6", facecolor='#042119', edgecolor='#065f46', zorder=3)
    ax.add_patch(b_pass)
    ax.text(390, 560, "✅ Matching Criteria Satisfied:", color='#6ee7b7', fontsize=8.8, fontweight='bold', zorder=4)
    ax.text(390, 540, "• Gender: Female student applicant satisfies girl-specific reservation", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 522, "• Course: B.Tech Engineering in AICTE approved technical institution", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 504, "• Income: Rs 2,50,000 is within the official ceiling of Rs 8,00,000/yr", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 486, "• Year of Study: 1st Year Fresh Degree student eligible", color='#cbd5e1', fontsize=7.8, zorder=4)

    b_verif = FancyBboxPatch((970, 465), 580, 115, boxstyle="round,pad=0,rounding_size=6", facecolor='#2b1a04', edgecolor='#92400e', zorder=3)
    ax.add_patch(b_verif)
    ax.text(985, 560, "⚠️ Institutional Verification Required:", color='#fde68a', fontsize=8.8, fontweight='bold', zorder=4)
    ax.text(985, 540, "• Tehsildar Income Certificate validity for current financial year", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 522, "• Bank Account NPCI Aadhaar mapper seeding verification", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 504, "• College Nodal Officer (CNO) bonafide admission authentication", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 486, "• Parental declaration of maximum 2 eligible girl applicants", color='#cbd5e1', fontsize=7.8, zorder=4)

    # Scheme 2: PM-USP CSSS (Eligible)
    c2 = FancyBboxPatch((350, 190), 1220, 225, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#0d1b2e', edgecolor='#0284c7', linewidth=1.8, zorder=2)
    ax.add_patch(c2)
    ax.text(375, 380, "[Eligible] Central Sector Scheme of Scholarship for College and University Students (PM-USP)", color=TEXT_WHITE, fontsize=12.5, fontweight='bold', zorder=3)
    ax.text(375, 357, "Department of Higher Education, Ministry of Education | Type: Central Sector | Portal: National Scholarship Portal (scholarships.gov.in)", color=TEXT_MUTED, fontsize=8, zorder=3)
    
    bb2 = FancyBboxPatch((1370, 360), 180, 36, boxstyle="round,pad=0,rounding_size=6", facecolor='#022c22', edgecolor='#059669', zorder=3)
    ax.add_patch(bb2)
    ax.text(1460, 378, "Rs 12,000 - 20,000 / yr", ha='center', va='center', color=ACCENT_GREEN, fontsize=9.5, fontweight='bold', zorder=4)

    b_pass2 = FancyBboxPatch((375, 215), 570, 120, boxstyle="round,pad=0,rounding_size=6", facecolor='#042119', edgecolor='#065f46', zorder=3)
    ax.add_patch(b_pass2)
    ax.text(390, 315, "✅ Matching Criteria Satisfied:", color='#6ee7b7', fontsize=8.8, fontweight='bold', zorder=4)
    ax.text(390, 295, "• Board Score: 85.5% meets the top 80th percentile benchmark", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 277, "• Income: Rs 2,50,000 is under the statutory limit of Rs 4,50,000/yr", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 259, "• Course: Full-time regular degree college course enrollment", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(390, 241, "• Domicile: Open to eligible residents of all Indian States & UTs", color='#cbd5e1', fontsize=7.8, zorder=4)

    b_verif2 = FancyBboxPatch((970, 215), 580, 120, boxstyle="round,pad=0,rounding_size=6", facecolor='#2b1a04', edgecolor='#92400e', zorder=3)
    ax.add_patch(b_verif2)
    ax.text(985, 315, "⚠️ Institutional Verification Required:", color='#fde68a', fontsize=8.8, fontweight='bold', zorder=4)
    ax.text(985, 295, "• State Board top-20th percentile list publication verification", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 277, "• AISHE institution code authentication by College Nodal Officer", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 259, "• Sole bank account NPCI mapping confirmation on UIDAI portal", color='#cbd5e1', fontsize=7.8, zorder=4)
    ax.text(985, 241, "• Undertaking of non-receipt of dual central scholarship assistance", color='#cbd5e1', fontsize=7.8, zorder=4)

    plt.tight_layout()
    plt.savefig("screenshot_3_3_eligibility_results.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 3 generated: screenshot_3_3_eligibility_results.png")

# ---------------- SCREENSHOT 4: SCHEME DIRECTORY ----------------
def create_screenshot_4():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=2)
    draw_main_header(ax, "Scholarship Scheme Directory & Search Filters", "Search and filter verified government schemes across Central Ministries and State Welfare Departments")
    
    # Filter Bar
    fbar = FancyBboxPatch((350, 680), 1220, 60, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#111c30', edgecolor='#233552', linewidth=1.2, zorder=2)
    ax.add_patch(fbar)
    
    filters = [
        ("Scheme Type:", "All Types [v]"),
        ("Domicile State:", "Maharashtra [v]"),
        ("Category:", "All Categories [v]"),
        ("Gender:", "Female [v]")
    ]
    for i, (flbl, fval) in enumerate(filters):
        fx = 370 + (i * 290)
        ax.text(fx, 718, flbl, color=TEXT_MUTED, fontsize=8, fontweight='bold', zorder=3)
        ax.text(fx, 696, fval, color=ACCENT_BLUE, fontsize=8.8, fontweight='bold', zorder=3)

    # Scheme Cards in Grid
    cards_data = [
        ("AICTE Pragati Scholarship for Girls (Degree)", "All India Council for Technical Education", "Rs 50,000 / year", "UGC/AICTE Technical", "Verified: 2025-01-15"),
        ("MahaDBT Rajarshi Shahu Maharaj EBC Scheme", "Higher & Technical Education Dept, Govt of Maharashtra", "50% Tuition Fee Concession", "State Government", "Verified: 2025-01-15"),
        ("Central Sector Scholarship Scheme (PM-USP)", "Department of Higher Education, Govt of India", "Rs 12,000 - 20,000 / yr", "Central Sector", "Verified: 2025-01-15"),
        ("Post-Matric Scholarship for Minorities", "Ministry of Minority Affairs, Govt of India", "Course Fee + Maint. Allowance", "Central Sector", "Verified: 2025-01-15")
    ]
    for k, (sname, sdept, sbenefit, stype, sverif) in enumerate(cards_data):
        cy = 500 - (k * 115)
        scard = FancyBboxPatch((350, cy), 1220, 98, boxstyle="round,pad=0,rounding_size=8",
                               facecolor='#101a2e', edgecolor='#1e2d45', linewidth=1.2, zorder=2)
        ax.add_patch(scard)
        ax.text(375, cy + 68, sname, color=TEXT_WHITE, fontsize=11, fontweight='bold', zorder=3)
        ax.text(375, cy + 44, sdept, color=TEXT_MUTED, fontsize=7.8, zorder=3)
        ax.text(375, cy + 20, f"[{stype}]  •  {sverif}  •  Portal: National Scholarship Portal (scholarships.gov.in)", color='#64748b', fontsize=7.2, zorder=3)
        
        # Benefit tag on right
        btag = FancyBboxPatch((1360, cy + 32), 190, 34, boxstyle="round,pad=0,rounding_size=6",
                              facecolor='#022619', edgecolor='#059669', zorder=3)
        ax.add_patch(btag)
        ax.text(1455, cy + 49, sbenefit, ha='center', va='center', color=ACCENT_GREEN, fontsize=8.8, fontweight='bold', zorder=4)

    plt.tight_layout()
    plt.savefig("screenshot_3_4_scheme_directory.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 4 generated: screenshot_3_4_scheme_directory.png")

# ---------------- SCREENSHOT 5: DOCUMENT CHECKLIST ----------------
def create_screenshot_5():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=3)
    draw_main_header(ax, "Official Document Checklist & Preparation Guide", "Interactive preparation dossier with pre-emptive rejection safeguards and Markdown export")
    
    # Selector Bar
    sbar = FancyBboxPatch((350, 680), 1220, 50, boxstyle="round,pad=0,rounding_size=8",
                          facecolor='#111b2e', edgecolor='#1e2d45', linewidth=1.2, zorder=2)
    ax.add_patch(sbar)
    ax.text(375, 705, "Selected Scheme: AICTE Pragati Scholarship for Girl Students (Technical Degree)  [Change Scheme v]",
            color=TEXT_WHITE, fontsize=9.5, fontweight='bold', zorder=3)

    # Left Container: Checkbox List
    left_c = FancyBboxPatch((350, 140), 740, 515, boxstyle="round,pad=0,rounding_size=10",
                            facecolor='#10192a', edgecolor='#1e2b42', linewidth=1.2, zorder=2)
    ax.add_patch(left_c)
    ax.text(375, 620, "[Checklist] Mandatory Document Checklist for Upload", color=ACCENT_BLUE, fontsize=11, fontweight='bold', zorder=3)
    
    checklist_items = [
        ("[x]  Aadhaar Card (Linked with sole student bank account)", True),
        ("[x]  Class 10th and 12th Board Marksheets & Passing Certificates", True),
        ("[x]  Centralized Admission Process (CAP) Technical Allotment Letter", True),
        ("[x]  Current Academic Year College Tuition Fee Receipt", True),
        ("[x]  Valid Annual Family Income Certificate (Issued by Tehsildar / SDM)", True),
        ("[ ]  Student Active Sole Bank Account Passbook (Aadhaar Seeded)", False),
        ("[ ]  Parental Declaration Affidavit (Confirming max 2 eligible girl applicants)", False)
    ]
    for i, (item, checked) in enumerate(checklist_items):
        iy = 560 - (i * 48)
        cbox = FancyBboxPatch((375, iy), 690, 36, boxstyle="round,pad=0,rounding_size=6",
                              facecolor='#022619' if checked else '#152033',
                              edgecolor='#059669' if checked else '#283852', linewidth=1, zorder=3)
        ax.add_patch(cbox)
        ax.text(395, iy + 18, item, va='center', color=TEXT_WHITE if checked else '#94a3b8', fontsize=8.2, zorder=4)

    # Progress & Download
    pbar_bg = Rectangle((375, 185), 690, 8, facecolor='#090d16', zorder=3)
    ax.add_patch(pbar_bg)
    pbar_fg = Rectangle((375, 185), 690 * (5/7), 8, facecolor=ACCENT_GREEN, zorder=4)
    ax.add_patch(pbar_fg)
    ax.text(375, 205, "Checklist Readiness: 5 of 7 items verified (71% Ready)", color=ACCENT_GREEN, fontsize=8.5, fontweight='bold', zorder=4)

    dn_btn = FancyBboxPatch((375, 148), 690, 32, boxstyle="round,pad=0,rounding_size=6", facecolor='#0284c7', zorder=3)
    ax.add_patch(dn_btn)
    ax.text(720, 164, "Download Checklist as Markdown Dossier (.md)", ha='center', va='center', color=TEXT_WHITE, fontsize=8.5, fontweight='bold', zorder=4)

    # Right Container: Avoid Rejection Pitfalls
    right_c = FancyBboxPatch((1115, 140), 455, 515, boxstyle="round,pad=0,rounding_size=10",
                             facecolor='#16111f', edgecolor='#4c1d95', linewidth=1.2, zorder=2)
    ax.add_patch(right_c)
    ax.text(1135, 620, "[Alert] Avoid Top Rejection Pitfalls", color='#c084fc', fontsize=11, fontweight='bold', zorder=3)
    
    pitfalls = [
        ("NPCI Aadhaar Mapping Missing", "Standard KYC alone causes over 90% of DBT payment failures. Ensure your sole bank account is explicitly seeded on the NPCI central mapper."),
        ("Name Mismatch on Certificates", "Minor spelling differences between Class 10 marksheet and Aadhaar card cause automated validation rejection."),
        ("Non-Revenue Income Certificates", "Notary affidavits or salary slips are rejected. Only revenue certificates signed by a Tehsildar/SDM are accepted.")
    ]
    for j, (p_title, p_desc) in enumerate(pitfalls):
        py = 500 - (j * 130)
        pbox = FancyBboxPatch((1135, py), 415, 105, boxstyle="round,pad=0,rounding_size=6",
                              facecolor='#231238', edgecolor='#6b21a8', zorder=3)
        ax.add_patch(pbox)
        ax.text(1150, py + 80, f"• {p_title}", color='#f3e8ff', fontsize=8.8, fontweight='bold', zorder=4)
        ax.text(1150, py + 45, p_desc, color='#cbd5e1', fontsize=7.4, wrap=True, zorder=4)

    plt.tight_layout()
    plt.savefig("screenshot_3_5_document_checklist.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 5 generated: screenshot_3_5_document_checklist.png")

# ---------------- SCREENSHOT 6: SCHOLARBOT CHAT ----------------
def create_screenshot_6():
    fig, ax = setup_canvas()
    draw_sidebar_nav(ax, active_idx=4)
    draw_main_header(ax, "AI ScholarBot — Grounded Conversational Advisor", "Natural-language question answering strictly grounded in retrieved official scheme guidelines")
    
    # Suggested Questions Pills
    ax.text(350, 718, "[Prompts] Suggested Student Questions:", color=TEXT_MUTED, fontsize=8.5, fontweight='bold', zorder=2)
    prompts = [
        "Scholarships for girls in B.Tech?",
        "PM-USP CSSS Income limit?",
        "Can I get 2 scholarships?",
        "What is NPCI bank mapping?"
    ]
    for i, ptxt in enumerate(prompts):
        px = 350 + (i * 310)
        p_pill = FancyBboxPatch((px, 675), 295, 30, boxstyle="round,pad=0,rounding_size=5",
                                facecolor='#132036', edgecolor='#253b5e', zorder=2)
        ax.add_patch(p_pill)
        ax.text(px + 147, 690, ptxt, ha='center', va='center', color=ACCENT_BLUE, fontsize=7.6, zorder=3)

    # Chat Messages Container
    # User message
    u_box = FancyBboxPatch((650, 580), 920, 60, boxstyle="round,pad=0,rounding_size=8",
                           facecolor='#0284c7', edgecolor='none', zorder=2)
    ax.add_patch(u_box)
    ax.text(670, 615, "Student:", color='#bae6fd', fontsize=8, fontweight='bold', zorder=3)
    ax.text(670, 595, "Can I apply for and receive multiple government scholarships at the same time?", color=TEXT_WHITE, fontsize=8.5, zorder=3)

    # Assistant Response (Grounded)
    a_box = FancyBboxPatch((350, 240), 1220, 310, boxstyle="round,pad=0,rounding_size=10",
                           facecolor='#0c182a', edgecolor='#1e3252', linewidth=1.2, zorder=2)
    ax.add_patch(a_box)
    ax.text(375, 515, "[ScholarBot] Grounded Official Response:", color=ACCENT_GREEN, fontsize=9.5, fontweight='bold', zorder=3)
    
    resp_text = (
        "According to official Government of India scholarship guidelines (including Ministry of Education and UGC regulations):\n\n"
        "1. Maintenance Allowance Prohibition: A student CANNOT draw two maintenance allowances or tuition fee reimbursements\n"
        "   from different government sources (Central and State) for the same academic course.\n\n"
        "2. Fee Waiver vs Pure Merit: If you receive a tuition fee waiver from your state government (e.g. MahaDBT EBC), you may be\n"
        "   permitted to accept a pure merit scholarship, provided the scheme guidelines of both programs explicitly allow it.\n\n"
        "3. Mandatory Declaration: On the National Scholarship Portal (NSP), you are required to submit an undertaking certifying\n"
        "   that you are not receiving benefits from any other government scheme."
    )
    ax.text(375, 420, resp_text, color='#e2e8f0', fontsize=8, zorder=3)
    
    # Citations box inside response
    cit_box = FancyBboxPatch((375, 255), 1170, 50, boxstyle="round,pad=0,rounding_size=6",
                             facecolor='#081424', edgecolor='#162c4a', zorder=3)
    ax.add_patch(cit_box)
    ax.text(390, 285, "Verified Sources: National Scholarship Portal (scholarships.gov.in)  |  PM-USP CSSS Guidelines  |  UGC Regulations", color=ACCENT_BLUE, fontsize=7.8, fontweight='bold', zorder=4)
    ax.text(390, 268, "Last Verified: 2025-01-15  •  Response Engine: Google Gemini 2.5 Flash with Grounded Context", color='#64748b', fontsize=7.2, zorder=4)

    # Chat Input Box at Bottom
    inp_box = FancyBboxPatch((350, 160), 1220, 50, boxstyle="round,pad=0,rounding_size=8",
                             facecolor='#0d1726', edgecolor='#233857', zorder=2)
    ax.add_patch(inp_box)
    ax.text(375, 185, "Ask a scholarship question (e.g. 'What is the income limit for PM-USP Central Sector?')...", color='#64748b', fontsize=8.5, zorder=3)
    send_btn = FancyBboxPatch((1470, 168), 85, 34, boxstyle="round,pad=0,rounding_size=5", facecolor='#0284c7', zorder=3)
    ax.add_patch(send_btn)
    ax.text(1512, 185, "Send ->", ha='center', va='center', color=TEXT_WHITE, fontsize=8, fontweight='bold', zorder=4)

    plt.tight_layout()
    plt.savefig("screenshot_3_6_scholarbot_chat.png", dpi=DPI, facecolor=BG_APP)
    plt.close()
    print("Screenshot 6 generated: screenshot_3_6_scholarbot_chat.png")

if __name__ == "__main__":
    create_screenshot_1()
    create_screenshot_2()
    create_screenshot_3()
    create_screenshot_4()
    create_screenshot_5()
    create_screenshot_6()
    print("All 6 publication-grade screenshots successfully generated!")
