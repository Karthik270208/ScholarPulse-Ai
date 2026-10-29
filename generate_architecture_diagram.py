"""Generate a publication-grade, ultra-sharp System Architecture diagram for ScholarNexus AI."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

# Setup 16:9 canvas at 300 DPI (4800 x 2700 px)
fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#070b14')
ax.set_facecolor('#070b14')
ax.set_xlim(0, 1600)
ax.set_ylim(0, 900)
ax.axis('off')

# Color Palette
BG_CARD = '#0f172a'
BORDER_BLUE = '#38bdf8'     # Frontend Client
BORDER_AMBER = '#f59e0b'    # Rules Engine
BORDER_PURPLE = '#c084fc'   # AI RAG
BORDER_GREEN = '#10b981'    # Data Tier
TEXT_WHITE = '#ffffff'
TEXT_MUTED = '#94a3b8'
TEXT_DARK = '#020617'

def draw_card(ax, x, y, w, h, border_color, title, subtitle=None, bg_color=BG_CARD, radius=14):
    # Shadow
    shadow = FancyBboxPatch((x+4, y-4), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                            facecolor='#020617', edgecolor='none', alpha=0.8, zorder=2)
    ax.add_patch(shadow)
    # Card Body
    card = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=3)
    ax.add_patch(card)
    # Header bar
    header_bar = FancyBboxPatch((x, y+h-42), w, 42, boxstyle=f"round,pad=0,rounding_size={radius}",
                                facecolor=border_color, edgecolor='none', zorder=4)
    ax.add_patch(header_bar)
    # Header text
    ax.text(x + w/2, y + h - 21, title, ha='center', va='center',
            color=TEXT_DARK, fontsize=11.5, fontweight='bold', zorder=5, family='sans-serif')
    if subtitle:
        ax.text(x + w/2, y + h - 56, subtitle, ha='center', va='center',
                color=TEXT_MUTED, fontsize=8.8, fontstyle='italic', zorder=5, family='sans-serif')

def draw_pill(ax, x, y, w, h, title_text, sub_text, bg_color='#1e293b', border_color='#334155', title_color='#f8fafc'):
    pill = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8",
                          facecolor=bg_color, edgecolor=border_color, linewidth=1.2, zorder=6)
    ax.add_patch(pill)
    ax.text(x + 14, y + h - 16, title_text, ha='left', va='center',
            color=title_color, fontsize=9.2, fontweight='bold', zorder=7, family='sans-serif')
    if sub_text:
        ax.text(x + 14, y + 14, sub_text, ha='left', va='center',
                color=TEXT_MUTED, fontsize=7.6, zorder=7, family='sans-serif')

def draw_arrow(ax, start, end, label='', color='#64748b', rad=0.0):
    arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=16,
                            color=color, linewidth=2.2, connectionstyle=f"arc3,rad={rad}", zorder=8)
    ax.add_patch(arrow)
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + 13
        ax.text(mid_x, mid_y, label, ha='center', va='center',
                color='#38bdf8', fontsize=8.2, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.22", fc='#0b1120', ec='#334155', lw=0.8), zorder=9)

# ----------------- 1. TITLE HEADER -----------------
ax.text(800, 860, "ScholarNexus AI — System Architecture", ha='center', va='center',
        color=TEXT_WHITE, fontsize=23, fontweight='bold', family='sans-serif')
ax.text(800, 830, "Client Layer  |  Deterministic Rules Engine  |  Grounded RAG Advisor  |  Verified Government Data Tier",
        ha='center', va='center', color='#38bdf8', fontsize=10.5, fontweight='medium', family='sans-serif')

# ----------------- 2. LAYER 1: FRONTEND CLIENT (LEFT) -----------------
draw_card(ax, 50, 120, 360, 680, BORDER_BLUE, "1. FRONTEND CLIENT LAYER", "Streamlit Reactive Single Page App (app.py)")
pills_ui = [
    ("Home Dashboard & Metrics", "12 Schemes - Rs 93,600 Max - 100% Verified"),
    ("Student Profile Form", "Income, Domicile, Category, Gender, PwD, Score"),
    ("Scheme Directory & Filters", "Type, State, Gender, Category, Income Ceiling"),
    ("Eligibility Results Breakdown", "Categorized: Matched, Unmet, Verification Alerts"),
    ("Interactive Document Checklist", "Status tracking, rejection prevention, MD export"),
    ("AI ScholarBot Chat Interface", "Contextual Q&A with statutory link citations")
]
for i, (p_title, p_sub) in enumerate(pills_ui):
    py = 645 - (i * 88)
    draw_pill(ax, 75, py, 310, 52, f"[UI-{i+1}] {p_title}", p_sub,
              bg_color='#021c38', border_color='#0284c7', title_color='#7dd3fc')

# ----------------- 3. LAYER 2: DETERMINISTIC RULES ENGINE (MIDDLE TOP) -----------------
draw_card(ax, 490, 475, 520, 325, BORDER_AMBER, "2. DETERMINISTIC RULES ENGINE", "Python Core (src/eligibility_engine.py)")
ax.text(515, 725, ">> ZERO-HALLUCINATION VERIFICATION PIPELINE", color=BORDER_AMBER, fontsize=9.2, fontweight='bold', zorder=6)
pills_engine = [
    ("Multi-Variable Constraint Evaluator", "Evaluates Education, Year, State Domicile, Gender, Category, Income, PwD"),
    ("Matching Criteria Sorter (Satisfied)", "Mathematically verifies criteria meeting or exceeding statutory rules"),
    ("Unmet Criteria Dissector (Deficits)", "Isolates specific disqualifications (e.g. family income ceiling exceeded)"),
    ("Institutional Safeguard Flags", "Flags Tehsildar certs, AISHE college registration, and NPCI bank mapping")
]
for i, (p_title, p_sub) in enumerate(pills_engine):
    py = 665 - (i * 54)
    draw_pill(ax, 515, py, 470, 42, f"[RULE-{i+1}] {p_title}", p_sub,
              bg_color='#291804', border_color='#d97706', title_color='#fde68a')

# ----------------- 4. LAYER 3: GROUNDED AI ADVISOR (MIDDLE BOTTOM) -----------------
draw_card(ax, 490, 120, 520, 325, BORDER_PURPLE, "3. GROUNDED AI ADVISOR (ScholarBot)", "Dual-Engine Architecture (src/ai_advisor.py)")
ax.text(515, 370, ">> HYBRID RETRIEVAL & FALLBACK PIPELINE", color=BORDER_PURPLE, fontsize=9.2, fontweight='bold', zorder=6)
pills_ai = [
    ("Tokenized Context Retrieval (RAG)", "Weighted keyword matching with category, state, & course intent boost"),
    ("Google Gemini 2.5 Flash / OpenAI REST", "Lightweight REST API client with zero third-party SDK dependencies"),
    ("Anti-Hallucination Guardrails", "Strict system prompt restricts synthesis strictly to supplied context"),
    ("Offline Grounded Demo Engine", "Deterministic fallback covering NPCI, multiple grants, & rules")
]
for i, (p_title, p_sub) in enumerate(pills_ai):
    py = 310 - (i * 54)
    draw_pill(ax, 515, py, 470, 42, f"[AI-{i+1}] {p_title}", p_sub,
              bg_color='#24123d', border_color='#9333ea', title_color='#f3e8ff')

# ----------------- 5. LAYER 4: DATA TIER & OFFICIAL SOURCES (RIGHT) -----------------
draw_card(ax, 1100, 120, 450, 680, BORDER_GREEN, "4. VERIFIED SCHEMES & DATA TIER", "Data Provenance & Gazette Archive (data/)")
pills_data = [
    ("National Apex Central Schemes", "PM-USP Central Sector (CSSS), Post-Matric SC/ST/OBC Schemes"),
    ("Technical & Specialized Bodies", "AICTE Pragati (Girls), Saksham (PwD), and Swanath Schemes"),
    ("Regional & Minority Grants", "UGC Ishan Uday (NER) and Post-Matric Minority Scholarships"),
    ("State Government Portals", "Maharashtra MahaDBT, UP Dashmottar, Karnataka SSP Portals"),
    ("Statutory Reference Metadata", "Official portal URLs, guidelines PDFs, and last-verified dates"),
    ("Data Provenance & Anti-Drift Store", "data/schemes_data.json and reference taxonomy in data/states.py")
]
for i, (p_title, p_sub) in enumerate(pills_data):
    py = 645 - (i * 88)
    draw_pill(ax, 1125, py, 400, 52, f"[DATA-{i+1}] {p_title}", p_sub,
              bg_color='#022619', border_color='#059669', title_color='#a7f3d0')

# ----------------- 6. DIRECTIONAL DATA FLOW ARROWS -----------------
# 1. Frontend -> Deterministic Engine
draw_arrow(ax, (410, 640), (490, 640), label="Profile Data", color='#38bdf8')
# 2. Deterministic Engine -> Frontend
draw_arrow(ax, (490, 580), (410, 580), label="Verdict & Score", color='#f59e0b')

# 3. Frontend -> AI Advisor
draw_arrow(ax, (410, 300), (490, 300), label="User Query", color='#38bdf8')
# 4. AI Advisor -> Frontend
draw_arrow(ax, (490, 240), (410, 240), label="Grounded Answer", color='#c084fc')

# 5. Data Tier -> Deterministic Engine
draw_arrow(ax, (1100, 640), (1010, 640), label="Gazette Rules", color='#10b981')

# 6. Data Tier -> AI Advisor (RAG Context)
draw_arrow(ax, (1100, 280), (1010, 280), label="Scheme Context", color='#10b981')

# ----------------- 7. FOOTER BAR / METRICS -----------------
footer = FancyBboxPatch((50, 25), 1500, 68, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#0f172a', edgecolor='#334155', linewidth=1.5, zorder=3)
ax.add_patch(footer)

metrics = [
    ("100% Mathematical Precision", "Zero AI hallucination in statutory decisions", BORDER_AMBER),
    ("< 200ms Decision Latency", "Instant in-memory deterministic rule execution", BORDER_BLUE),
    ("Dual-Mode Grounded RAG", "Google Gemini API with offline demo fallback", BORDER_PURPLE),
    ("Complete Data Provenance", "All schemes linked to official government gazettes", BORDER_GREEN)
]
for i, (m_title, m_desc, col) in enumerate(metrics):
    mx = 75 + (i * 380)
    ax.text(mx, 68, m_title, ha='left', va='center', color=col, fontsize=9.8, fontweight='bold', zorder=5)
    ax.text(mx, 44, m_desc, ha='left', va='center', color=TEXT_MUTED, fontsize=7.8, zorder=5)

output_path = Path("system_architecture.png")
plt.tight_layout()
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Flawless architecture diagram generated at: {output_path.resolve()}")
