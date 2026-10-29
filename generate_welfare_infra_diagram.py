"""Generate an ultra-sharp, publication-grade diagram illustrating the
Public Digital Welfare Infrastructure and Direct Benefit Transfer (DBT) ecosystem in India.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

# Setup 16:9 canvas at 300 DPI (4800 x 2700 px)
fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#060913')
ax.set_facecolor('#060913')
ax.set_xlim(0, 1600)
ax.set_ylim(0, 900)
ax.axis('off')

# Color Palette
BORDER_GOLD = '#f59e0b'     # Level 1: Ministries & PFMS
BORDER_CYAN = '#06b6d4'     # Level 2: Portals
BORDER_PURPLE = '#a855f7'   # Level 3: Verification
BORDER_ROSE = '#f43f5e'     # Level 4: NPCI APBS (Critical link)
BORDER_GREEN = '#10b981'    # Level 5: Beneficiary
TEXT_WHITE = '#ffffff'
TEXT_MUTED = '#94a3b8'
TEXT_DARK = '#020617'

def draw_tier_container(ax, x, y, w, h, border_color, badge_text, title, subtitle):
    # Shadow
    shadow = FancyBboxPatch((x+4, y-4), w, h, boxstyle="round,pad=0,rounding_size=12",
                            facecolor='#010409', edgecolor='none', alpha=0.85, zorder=2)
    ax.add_patch(shadow)
    # Main Box
    card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12",
                           facecolor='#0c1322', edgecolor=border_color, linewidth=1.8, zorder=3)
    ax.add_patch(card)
    # Badge
    badge = FancyBboxPatch((x+16, y+h-26), 95, 20, boxstyle="round,pad=0,rounding_size=5",
                           facecolor=border_color, edgecolor='none', zorder=4)
    ax.add_patch(badge)
    ax.text(x+63, y+h-16, badge_text, ha='center', va='center',
            color=TEXT_DARK, fontsize=7.8, fontweight='bold', zorder=5, family='sans-serif')
    # Title & Subtitle
    ax.text(x+122, y+h-16, title, ha='left', va='center',
            color=TEXT_WHITE, fontsize=10.5, fontweight='bold', zorder=5, family='sans-serif')
    ax.text(x+w-20, y+h-16, subtitle, ha='right', va='center',
            color=TEXT_MUTED, fontsize=8, fontstyle='italic', zorder=5, family='sans-serif')

def draw_sub_box(ax, x, y, w, h, header_text, bullets, bg_color='#162032', border_color='#24334a', header_color='#f8fafc'):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8",
                         facecolor=bg_color, edgecolor=border_color, linewidth=1.2, zorder=6)
    ax.add_patch(box)
    # Header
    ax.text(x+14, y+h-18, header_text, ha='left', va='center',
            color=header_color, fontsize=9.2, fontweight='bold', zorder=7, family='sans-serif')
    # Bullets
    for i, bullet in enumerate(bullets):
        by = y + h - 38 - (i * 18)
        ax.text(x+16, by, f"• {bullet}", ha='left', va='center',
                color=TEXT_MUTED, fontsize=7.6, zorder=7, family='sans-serif')

def draw_arrow(ax, start, end, label='', color='#64748b'):
    arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=15,
                            color=color, linewidth=2.2, zorder=8)
    ax.add_patch(arrow)
    if label:
        ax.text((start[0]+end[0])/2, (start[1]+end[1])/2 + 10, label, ha='center', va='center',
                color='#38bdf8', fontsize=7.8, fontweight='bold', zorder=9)

def draw_down_arrow(ax, x, y_start, y_end, label='', color='#64748b'):
    arrow = FancyArrowPatch((x, y_start), (x, y_end), arrowstyle='->', mutation_scale=15,
                            color=color, linewidth=2.2, zorder=8)
    ax.add_patch(arrow)
    if label:
        ax.text(x+15, (y_start + y_end)/2, label, ha='left', va='center',
                color='#38bdf8', fontsize=7.8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc='#090d16', ec='#334155', lw=0.8), zorder=9)

# ----------------- 1. HEADER -----------------
ax.text(800, 866, "Public Digital Welfare & Direct Benefit Transfer (DBT) Ecosystem",
        ha='center', va='center', color=TEXT_WHITE, fontsize=21, fontweight='bold', family='sans-serif')
ax.text(800, 838, "End-to-End Higher Education Scholarship Architecture in India: From Budgetary Sanction to Student Bank Credit",
        ha='center', va='center', color='#38bdf8', fontsize=10.2, fontweight='medium', family='sans-serif')

# ----------------- 2. LEVEL 1: SOVEREIGN MINISTRIES & PFMS -----------------
draw_tier_container(ax, 120, 690, 1360, 125, BORDER_GOLD,
                    "STAGE 1", "CENTRAL MINISTRIES & PUBLIC FINANCIAL MANAGEMENT SYSTEM (PFMS)",
                    "Statutory Scheme Formulation & Budget Allocation")
draw_sub_box(ax, 140, 702, 420, 74, "Apex Sponsoring Ministries",
             ["Ministry of Education (Higher Education Department)",
              "Ministry of Social Justice, Tribal Affairs & Minority Affairs",
              "Technical Apex Regulators: AICTE & UGC"],
             bg_color='#241804', border_color='#b45309', header_color='#fde68a')
draw_sub_box(ax, 590, 702, 420, 74, "Consolidated Fund of India (DBT Quota)",
             ["Annual parliamentary budgetary allocation under GFR Rules",
              "Mandatory non-diversion of social category funds (SC/ST/EWS)",
              "Dual scholarship prohibition enforcement protocols"],
             bg_color='#241804', border_color='#b45309', header_color='#fde68a')
draw_sub_box(ax, 1040, 702, 420, 74, "PFMS Central Treasury Gateway",
             ["Central electronic payment sanctioning platform",
              "Digital signature validation (DSC) by sanctioning officers",
              "Generation of Direct Benefit Transfer (DBT) payment files"],
             bg_color='#241804', border_color='#b45309', header_color='#fde68a')

draw_down_arrow(ax, 800, 690, 645, "Scheme Guidelines & Funds", BORDER_GOLD)

# ----------------- 3. LEVEL 2: REGISTRATION & APPLICATION PORTALS -----------------
draw_tier_container(ax, 120, 520, 1360, 125, BORDER_CYAN,
                    "STAGE 2", "APEX APPLICATION PORTALS (CENTRAL & STATE APEX HUBS)",
                    "Student Onboarding, Authentication, and Application Processing")
draw_sub_box(ax, 140, 532, 640, 74, "National Scholarship Portal (NSP - scholarships.gov.in)",
             ["One-Time Registration (OTR) with biometric / facial Aadhaar e-KYC authentication",
              "DigiLocker API integration for instant electronic pulling of Board Class 10/12 Marksheets",
              "Central registry hosting Central Sector (CSSS), AICTE Pragati/Saksham, & PMS SC/ST"],
             bg_color='#042233', border_color='#0891b2', header_color='#67e8f9')
draw_sub_box(ax, 820, 532, 640, 74, "Designated State Welfare Portals (MahaDBT, UP Dashmottar, Karnataka SSP)",
             ["MahaDBT (Maharashtra): EBC 50% tuition reimbursement & CAP round merit verification",
              "UP Scholarship: e-District integration for automated online verification of Aay Praman Patra",
              "Karnataka SSP: Kutumba Family ID integration with automated e-Attestation workflows"],
             bg_color='#042233', border_color='#0891b2', header_color='#67e8f9')

draw_down_arrow(ax, 800, 520, 475, "Digital Applications", BORDER_CYAN)

# ----------------- 4. LEVEL 3: INSTITUTIONAL VERIFICATION -----------------
draw_tier_container(ax, 120, 350, 1360, 125, BORDER_PURPLE,
                    "STAGE 3", "MULTI-TIER INSTITUTIONAL & DISTRICT NODAL VERIFICATION LAYER",
                    "Mandatory Academic & Revenue Clearance")
draw_sub_box(ax, 140, 362, 420, 74, "AISHE Institute Code Validation",
             ["College must hold active All India Survey on Higher Education registry",
              "Institute Nodal Officer (INO) portal registration and profile approval",
              "Course recognition check by regulatory statutory councils (AICTE/UGC)"],
             bg_color='#1f0f33', border_color='#7e22ce', header_color='#e9d5ff')
draw_sub_box(ax, 590, 362, 420, 74, "College Nodal Officer (CNO) Audit",
             ["Verification of physical bonafide student status & original roll number",
              "Fee receipt audit: tuition fee breakdown vs non-refundable components",
              "Attendance check: minimum 75% attendance compliance in preceding term"],
             bg_color='#1f0f33', border_color='#7e22ce', header_color='#e9d5ff')
draw_sub_box(ax, 1040, 362, 420, 74, "District / State Welfare Sanction (DNO)",
             ["Tehsildar income certificate authenticity check against state revenue records",
              "Caste / Category verification on central / state social welfare databases",
              "Final recommendation and digital forwarding to Ministry PFMS queue"],
             bg_color='#1f0f33', border_color='#7e22ce', header_color='#e9d5ff')

draw_down_arrow(ax, 800, 350, 305, "Approved Beneficiary List", BORDER_PURPLE)

# ----------------- 5. LEVEL 4: NPCI APBS (CRITICAL LINK) & LEVEL 5: DISBURSEMENT -----------------
draw_tier_container(ax, 120, 155, 1360, 150, BORDER_ROSE,
                    "STAGE 4 & 5", "NPCI AADHAAR PAYMENT BRIDGE (APBS) & DIRECT BENEFIT DISBURSEMENT",
                    "Financial Transaction Routing & Beneficiary Credit")

# Sub-block 1: The Trap (Standard KYC)
draw_sub_box(ax, 140, 167, 360, 98, "[CRITICAL] Standard Bank KYC (FAIL)",
             ["Aadhaar photocopy submitted as ID proof only",
              "Account is NOT mapped in NPCI Central Database",
              "Aadhaar is 'linked' to account, but NOT 'seeded'",
              "RESULT: 90% of government DBT transactions REJECT"],
             bg_color='#330914', border_color='#be123c', header_color='#fda4af')

# Sub-block 2: The Mandatory Route (NPCI Seeding)
draw_sub_box(ax, 520, 167, 430, 98, "[MANDATORY] Active NPCI Aadhaar Mapper",
             ["Account explicitly seeded with NPCI APBS mapper",
              "Applicant's SOLE bank account (not joint account)",
              "Direct routing of DBT subsidy using 12-digit Aadhaar UID",
              "UIDAI Resident Portal enables live mapping verification"],
             bg_color='#022b1c', border_color='#059669', header_color='#6ee7b7')

# Sub-block 3: Final Credit to Student
draw_sub_box(ax, 970, 167, 490, 98, "[SUCCESS] Student Direct Account Disbursement",
             ["Instant Direct Benefit Transfer (DBT) credit into active bank account",
              "Tuition fee reimbursement + monthly maintenance allowance credited",
              "Zero middleman leakage; automated SMS alert sent via PFMS / Bank Gateway",
              "Annual renewal triggered upon passing marksheets and attendance upload"],
             bg_color='#022619', border_color='#10b981', header_color='#a7f3d0')

# Arrow from NPCI to Student
draw_arrow(ax, (950, 216), (970, 216), "", '#10b981')

# ----------------- 6. FOOTER: CRITICAL LESSONS & SCHOLARNEXUS SAFEGUARDS -----------------
footer = FancyBboxPatch((120, 22), 1360, 110, boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#090f1d', edgecolor='#1e293b', linewidth=1.5, zorder=3)
ax.add_patch(footer)

ax.text(145, 102, "KEY INSIGHT LEARNED: The 30% Application Rejection Bottleneck",
        ha='left', va='center', color='#f43f5e', fontsize=9.8, fontweight='bold', zorder=5)
ax.text(145, 78, "Government audits reveal that over 30% of eligible college applicants are rejected not because of merit, but due to avoidable clerical errors:\n"
                 "1. Bank account has basic KYC but lacks active NPCI mapper seeding.  2. Minor name/DOB spelling mismatch between Class 10 and Aadhaar.\n"
                 "3. Submitting notary affidavits instead of official Tehsildar revenue certificates.  4. College lacking active AISHE portal affiliation.",
        ha='left', va='center', color='#cbd5e1', fontsize=7.8, zorder=5)

ax.text(145, 42, "ScholarNexus AI Solution: Pre-application document checklists enforce NPCI verification, AISHE checks, and gazette compliance before portal submission.",
        ha='left', va='center', color='#38bdf8', fontsize=8.2, fontweight='bold', zorder=5)

output_path = Path("public_digital_welfare_infrastructure.png")
plt.tight_layout()
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Publication-grade diagram generated at: {output_path.resolve()}")
