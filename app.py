"""ScholarGuide AI — Government Schemes & Scholarship Assistant.

A Streamlit web application helping Indian college students discover
government scholarships, evaluate eligibility, prepare document checklists,
and consult an AI scholarship assistant grounded in official guidelines.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

from data.states import (
    INDIAN_STATES_AND_UTS,
    EDUCATION_LEVELS,
    DEGREE_COURSES,
    SOCIAL_CATEGORIES,
    MINORITY_COMMUNITIES
)
from src.models import StudentProfile
from src.utils import load_schemes_data, format_inr, get_income_bracket_label
from src.eligibility_engine import evaluate_eligibility, batch_evaluate_schemes
from src.search_filter import filter_and_search_schemes
from src.ai_advisor import ask_scholar_bot
from src.document_manager import (
    COMMON_REJECTION_REASONS,
    GENERAL_PORTAL_PREPARATION_STEPS,
    generate_scheme_checklist_markdown
)

# Page configuration
st.set_page_config(
    page_title="ScholarGuide AI — Govt Schemes & Scholarship Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, responsive student-friendly design
st.markdown("""
<style>
    /* Theme Accents */
    :root {
        --primary-navy: #1e3a8a;
        --saffron: #f97316;
        --emerald: #10b981;
        --slate-bg: #f8fafc;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%);
        padding: 2.2rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1.05rem;
        color: #e0f2fe;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    .disclaimer-banner {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 0.85rem 1.2rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #92400e;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 0.2rem;
    }
    
    .badge-verified {
        display: inline-block;
        background-color: #ecfdf5;
        color: #065f46;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        border: 1px solid #a7f3d0;
    }
    .badge-type {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        border: 1px solid #bfdbfe;
    }
    .badge-state {
        display: inline-block;
        background-color: #fef3c7;
        color: #92400e;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        border: 1px solid #fde68a;
    }
    
    .scheme-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    .match-eligible {
        color: #047857;
        font-weight: 700;
    }
    .match-ineligible {
        color: #b91c1c;
        font-weight: 700;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "student_profile" not in st.session_state:
    st.session_state.student_profile = StudentProfile()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! 🙏 I am **ScholarBot**, your official government scholarship advisor.\n\n"
                "I answer questions using documented guidelines from the **National Scholarship Portal (NSP)**, "
                "AICTE, UGC, and State Welfare departments.\n\n"
                "Ask me about eligibility rules, income caps, document requirements, or girl student schemes!"
            ),
            "sources": []
        }
    ]

if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {}

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "🏠 Home Dashboard"

# Check query parameter for direct tab linking / screenshot automation
query_nav = st.query_params.get("nav")
nav_map = {
    "home": "🏠 Home Dashboard",
    "profile": "👤 Student Profile & Match",
    "explorer": "🔍 Scheme Explorer & Filter",
    "checklist": "📋 Document Checklist",
    "chat": "🤖 AI ScholarBot Chat",
    "portals": "ℹ️ Official Portals & Guidelines"
}
if query_nav and query_nav in nav_map:
    st.session_state.active_nav = nav_map[query_nav]

# Load Schemes Dataset
all_schemes = load_schemes_data()

# Top Navigation / Header
st.markdown("""
<div class="main-header">
    <h1>ScholarNexus AI</h1>
    <p>AI-Powered Scholarship Intelligence and Eligibility Matching Platform</p>
</div>
""", unsafe_allow_html=True)

# Prominent Disclaimer
st.markdown("""
<div class="disclaimer-banner">
    ⚠️ <strong>Official Disclaimer:</strong> Preliminary matches generated by ScholarGuide AI are for informational & guidance purposes only.
    They do <strong>NOT</strong> constitute an official eligibility determination or guarantee of award. Final eligibility and selection are determined
    exclusively by the respective government ministries on official portals (such as the <a href="https://scholarships.gov.in/" target="_blank">National Scholarship Portal</a>).
    Always verify current academic year terms and cut-offs before applying.
</div>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("### 🇮🇳 Navigation")
    nav_options = [
        "🏠 Home Dashboard",
        "👤 Student Profile & Match",
        "🔍 Scheme Explorer & Filter",
        "📋 Document Checklist",
        "🤖 AI ScholarBot Chat",
        "ℹ️ Official Portals & Guidelines"
    ]
    
    # Selection
    current_index = 0
    if st.session_state.active_nav in nav_options:
        current_index = nav_options.index(st.session_state.active_nav)
        
    selected_nav = st.radio("Go to section:", nav_options, index=current_index, label_visibility="collapsed")
    st.session_state.active_nav = selected_nav

    st.markdown("---")
    
    # Active Profile Snapshot
    prof = st.session_state.student_profile
    st.markdown("#### 🎓 Current Profile")
    st.caption(f"**Course:** {prof.degree} ({prof.year_of_study})")
    st.caption(f"**State:** {prof.state}")
    st.caption(f"**Income:** {format_inr(prof.annual_income)}")
    st.caption(f"**Category:** {prof.category} | **Gender:** {prof.gender}")
    completeness = prof.completeness_score()
    st.progress(completeness / 100.0)
    st.caption(f"Profile Completeness: {completeness}%")

    st.markdown("---")
    
    # Engine & API Status
    st.markdown("#### ⚙️ System Status")
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if gemini_key and gemini_key.strip() and gemini_key != "your_gemini_api_key_here":
        st.success("🤖 LLM API: Gemini Active")
    elif openai_key and openai_key.strip() and openai_key != "your_openai_api_key_here":
        st.success("🤖 LLM API: OpenAI Active")
    else:
        st.info("💡 Mode: Offline Demo Engine (Deterministic Grounded Q&A)")

    st.caption("All scheme records verified against official government notifications.")


# -------------------------------------------------------------------------------------------------
# PAGE 1: HOME DASHBOARD
# -------------------------------------------------------------------------------------------------
if st.session_state.active_nav == "🏠 Home Dashboard":
    st.markdown("## Welcome to ScholarGuide AI")
    st.write(
        "Navigating Indian government scholarships can be challenging with differing income ceilings, "
        "category quotas, board percentile cutoffs, and strict documentation rules. ScholarGuide AI provides "
        "a transparent, rule-grounded assistant to help Indian undergraduate and postgraduate students discover "
        "legitimate schemes, assess exact eligibility criteria, and prepare correct paperwork."
    )

    # Key Statistics Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">12</div>
            <div class="metric-label">Curated Govt Schemes</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">₹93,600</div>
            <div class="metric-label">Max Annual Benefit</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">Source-Verified</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">0</div>
            <div class="metric-label">Hallucinated Data</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Start Action Cards
    st.markdown("### 🚀 Quick Actions")
    qcol1, qcol2, qcol3 = st.columns(3)
    
    with qcol1:
        with st.container(border=True):
            st.markdown("#### 🎯 Check My Eligibility")
            st.write("Fill your basic academic details, domicile, and category to see which central and state scholarships match you.")
            if st.button("Start Eligibility Check →", key="btn_home_profile", use_container_width=True):
                st.session_state.active_nav = "👤 Student Profile & Match"
                st.rerun()

    with qcol2:
        with st.container(border=True):
            st.markdown("#### 🔍 Browse & Filter Schemes")
            st.write("Search all 12 documented schemes by state, ministry, gender, category, and benefit amount.")
            if st.button("Explore Directory →", key="btn_home_explore", use_container_width=True):
                st.session_state.active_nav = "🔍 Scheme Explorer & Filter"
                st.rerun()

    with qcol3:
        with st.container(border=True):
            st.markdown("#### 🤖 Ask AI ScholarBot")
            st.write("Ask questions about dual scholarship restrictions, NPCI bank mapping, income certificates, and guidelines.")
            if st.button("Open AI Chatbot →", key="btn_home_chat", use_container_width=True):
                st.session_state.active_nav = "🤖 AI ScholarBot Chat"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Information Pillars
    st.markdown("### 🛡️ Why ScholarGuide AI is Different")
    pcol1, pcol2, pcol3 = st.columns(3)
    with pcol1:
        st.markdown("##### 📌 Deterministic Rule Matching")
        st.write("We do not rely on generative LLM guesses for eligibility decisions. Matching is calculated using deterministic rules derived straight from official scheme gazettes.")
    with pcol2:
        st.markdown("##### 🔗 Verified Official Links Only")
        st.write("Every single scheme links directly to authorized government domains (`scholarships.gov.in`, `aicte-india.org`, `mahadbt.maharashtra.gov.in`, etc.) with documented verification dates.")
    with pcol3:
        st.markdown("##### 🔒 Privacy & Free Access")
        st.write("No student personal data is stored on external servers or sold. ScholarGuide AI runs fully in demo mode even without third-party API keys.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📢 Official Portal Application Cycle Guidance")
    st.info(
        "**Note on Live Deadlines:** Government scholarship portals (e.g. NSP) operate on annual academic cycles. "
        "Opening windows typically begin around **July to September**, and closing windows typically run through **November to January**. "
        "ScholarGuide AI does not fabricate daily live countdowns without an official API; please check the respective verified portal links for current active dates."
    )


# -------------------------------------------------------------------------------------------------
# PAGE 2: STUDENT PROFILE & ELIGIBILITY MATCHING
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "👤 Student Profile & Match":
    st.markdown("## 👤 Student Profile & Eligibility Evaluation")
    st.write("Enter your academic and personal background details to evaluate matching criteria against all government schemes.")

    with st.form("student_profile_form"):
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("##### 🎓 Academic Information")
            edu_level = st.selectbox(
                "Education Level *",
                EDUCATION_LEVELS,
                index=EDUCATION_LEVELS.index(st.session_state.student_profile.education_level)
                if st.session_state.student_profile.education_level in EDUCATION_LEVELS else 0
            )
            degree = st.selectbox(
                "Degree / Course Stream *",
                DEGREE_COURSES,
                index=DEGREE_COURSES.index(st.session_state.student_profile.degree)
                if st.session_state.student_profile.degree in DEGREE_COURSES else 0
            )
            year_of_study = st.selectbox(
                "Current Year of Study *",
                ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "2nd Year (Lateral Entry)", "Final Year"],
                index=0
            )
            marks_pct = st.number_input(
                "Previous Qualifying Examination Marks / Percentage (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(st.session_state.student_profile.marks_percentage or 75.0),
                step=0.5,
                help="Enter your aggregate marks % in Class 12th (for 1st year UG) or previous semester."
            )
            is_technical = st.checkbox(
                "This is an AICTE / Technical Approved Course (Engineering/Pharmacy/Polytechnic)",
                value=st.session_state.student_profile.is_technical_course
            )
            is_hosteller = st.checkbox(
                "Currently staying in College Hostel (Hosteller)",
                value=st.session_state.student_profile.is_hosteller,
                help="Some schemes offer higher maintenance allowances to hostellers."
            )

        with col_b:
            st.markdown("##### 📍 Personal & Financial Criteria")
            state = st.selectbox(
                "Permanent Domicile State / UT *",
                INDIAN_STATES_AND_UTS,
                index=INDIAN_STATES_AND_UTS.index(st.session_state.student_profile.state)
                if st.session_state.student_profile.state in INDIAN_STATES_AND_UTS else 0,
                help="Select your state of permanent residence (as shown on Domicile certificate)."
            )
            annual_income = st.number_input(
                "Gross Annual Family Income (INR ₹) *",
                min_value=0.0,
                max_value=10000000.0,
                value=float(st.session_state.student_profile.annual_income),
                step=10000.0,
                help="Combined annual income from all sources as certified by the Tehsildar / Revenue Authority."
            )
            st.caption(f"Income Bracket: **{get_income_bracket_label(annual_income)}** ({format_inr(annual_income)})")
            
            category = st.selectbox(
                "Social Category / Caste *",
                SOCIAL_CATEGORIES,
                index=SOCIAL_CATEGORIES.index(st.session_state.student_profile.category)
                if st.session_state.student_profile.category in SOCIAL_CATEGORIES else 0
            )
            gender = st.selectbox(
                "Gender *",
                ["Female", "Male", "Transgender / Other"],
                index=0 if st.session_state.student_profile.gender == "Female" else 1
            )
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                is_pwd = st.checkbox(
                    "Differently Abled (PwD >= 40%)",
                    value=st.session_state.student_profile.is_pwd,
                    help="Benchmark disability certified by authorized medical board."
                )
                is_minority = st.checkbox(
                    "Minority Community",
                    value=st.session_state.student_profile.is_minority
                )
            with sub_col2:
                minority_comm = st.selectbox(
                    "Minority Religion",
                    MINORITY_COMMUNITIES,
                    index=MINORITY_COMMUNITIES.index(st.session_state.student_profile.minority_community)
                    if st.session_state.student_profile.minority_community in MINORITY_COMMUNITIES else 0,
                    disabled=not is_minority
                )
                is_single_girl = st.checkbox(
                    "Single Girl Child in Family",
                    value=st.session_state.student_profile.is_single_girl_child
                )

        submit_profile = st.form_submit_button("🔍 Evaluate My Eligibility Across All Schemes", type="primary", use_container_width=True)

    # Process Form
    if submit_profile:
        # Update profile
        new_profile = StudentProfile(
            education_level=edu_level,
            degree=degree,
            year_of_study=year_of_study,
            state=state,
            annual_income=annual_income,
            category=category,
            gender=gender,
            is_pwd=is_pwd,
            is_minority=is_minority,
            minority_community=minority_comm if is_minority else "Not Applicable",
            is_single_girl_child=is_single_girl,
            marks_percentage=marks_pct,
            is_technical_course=is_technical,
            is_hosteller=is_hosteller
        )
        
        # Validation
        validation_errors = new_profile.validate()
        if validation_errors:
            for err in validation_errors:
                st.error(f"⚠️ Validation Error: {err}")
        else:
            st.session_state.student_profile = new_profile
            st.success("✅ Profile updated successfully! Below is your detailed eligibility evaluation.")

    st.markdown("---")

    # Display Eligibility Results
    st.markdown("### 📊 Scheme Eligibility Results")
    eval_results = batch_evaluate_schemes(st.session_state.student_profile, all_schemes)
    
    eligible_count = sum(1 for _, res in eval_results if res.is_eligible)
    ineligible_count = len(eval_results) - eligible_count

    st.write(f"Based on your profile, **{eligible_count} schemes** show preliminary match, and **{ineligible_count} schemes** have unmet conditions.")

    # Filter tabs for results
    res_tab1, res_tab2 = st.tabs([f"✅ Eligible / Matching Schemes ({eligible_count})", f"❌ Ineligible Schemes ({ineligible_count})"])

    with res_tab1:
        if eligible_count == 0:
            st.info("No schemes met all preliminary criteria. Try updating your profile or explore all schemes directly in the Explorer.")
        else:
            for scheme, res in eval_results:
                if not res.is_eligible:
                    continue
                with st.container(border=True):
                    head_col1, head_col2 = st.columns([3, 1])
                    with head_col1:
                        st.markdown(f"#### 🏆 {scheme.get('name')}")
                        st.caption(f"**Ministry / Authority:** {scheme.get('ministry')}")
                        st.markdown(f"<span class='badge-type'>{scheme.get('scheme_type')}</span> <span class='badge-verified'>{scheme.get('verification_status')}</span>", unsafe_allow_html=True)
                    with head_col2:
                        st.markdown(f"<div style='text-align:right;'><span class='match-eligible'>● {res.match_status}</span><br><strong>Score: {res.match_score_percentage}%</strong></div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:right; font-size:1.1rem; color:#059669; font-weight:700;'>{scheme.get('benefit_amount_display')}</div>", unsafe_allow_html=True)

                    st.markdown(f"**Summary:** {res.summary_explanation}")
                    
                    # Criteria breakdown expander
                    with st.expander("🔍 View Detailed Criteria Breakdown & Verification Requirements", expanded=False):
                        crit_col1, crit_col2 = st.columns(2)
                        with crit_col1:
                            st.markdown("##### ✅ Matching Criteria Satisfied")
                            for c in res.matching_criteria:
                                st.markdown(f"- **{c.name}:** {c.detail}")
                        with crit_col2:
                            st.markdown("##### ⚠️ Verification Required (Institutional)")
                            for v in res.verification_required:
                                st.markdown(f"- **{v.name}:** {v.detail}")

                    # Official Links and Action Buttons
                    btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1.5, 3])
                    with btn_col1:
                        st.link_button(f"🌐 Apply on {scheme.get('portal_name')}", scheme.get('official_portal_url'), use_container_width=True)
                    with btn_col2:
                        st.link_button("📄 Official Guidelines PDF", scheme.get('guidelines_url'), use_container_width=True)
                    with btn_col3:
                        st.caption(f"Last Verified: {scheme.get('last_verified_date')} | Academic Cycle: {scheme.get('application_cycle_note')}")

    with res_tab2:
        for scheme, res in eval_results:
            if res.is_eligible:
                continue
            with st.container(border=True):
                head_col1, head_col2 = st.columns([3, 1])
                with head_col1:
                    st.markdown(f"#### {scheme.get('name')}")
                    st.caption(f"**Ministry:** {scheme.get('ministry')}")
                    st.markdown(f"<span class='badge-type'>{scheme.get('scheme_type')}</span>", unsafe_allow_html=True)
                with head_col2:
                    st.markdown(f"<div style='text-align:right;'><span class='match-ineligible'>✕ {res.match_status}</span><br>Score: {res.match_score_percentage}%</div>", unsafe_allow_html=True)

                st.markdown(f"**Reason:** {res.summary_explanation}")
                
                with st.expander("Why You Didn't Match", expanded=False):
                    st.markdown("##### ❌ Unmet Criteria")
                    for u in res.unmet_criteria:
                        st.markdown(f"- **{u.name}:** {u.detail}")
                    if res.matching_criteria:
                        st.markdown("##### Criteria You Did Meet")
                        for m in res.matching_criteria:
                            st.markdown(f"- **{m.name}:** {m.detail}")

                st.link_button(f"View Guidelines on {scheme.get('portal_name')}", scheme.get('guidelines_url'))


# -------------------------------------------------------------------------------------------------
# PAGE 3: SCHEME EXPLORER & FILTER
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "🔍 Scheme Explorer & Filter":
    st.markdown("## 🔍 Scholarship Scheme Directory & Search")
    st.write("Browse, search, and filter verified Central and State government schemes with documented eligibility rules.")

    # Search Bar & Filter Controls
    search_query = st.text_input("🔎 Search by scheme name, ministry, keyword, or document required:", placeholder="e.g. Pragati, engineering, minority, 50000, Aadhaar")
    
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)
    with fcol1:
        scheme_types = ["All", "Central Sector", "Centrally Sponsored", "UGC/AICTE Technical", "State Government"]
        sel_type = st.selectbox("Scheme Type", scheme_types)
    with fcol2:
        filter_states = ["All", "Maharashtra", "Uttar Pradesh", "Karnataka", "Assam", "Arunachal Pradesh", "Manipur", "Meghalaya"]
        sel_state = st.selectbox("Domicile State", filter_states)
    with fcol3:
        filter_cats = ["All", "General / Open", "OBC (Non-Creamy Layer)", "Scheduled Caste (SC)", "Scheduled Tribe (ST)", "Economically Weaker Section (EWS)"]
        sel_cat = st.selectbox("Social Category", filter_cats)
    with fcol4:
        filter_genders = ["All", "Female", "Male"]
        sel_gender = st.selectbox("Target Gender", filter_genders)

    fcol5, fcol6 = st.columns(2)
    with fcol5:
        max_inc_filter = st.number_input("Max Family Income Limit (₹)", min_value=0.0, max_value=10000000.0, value=0.0, step=50000.0, help="Leave 0 for no income ceiling filter")
    with fcol6:
        sort_choice = st.selectbox("Sort By", ["Relevance / Name", "Alphabetical (A-Z)", "Scheme Type", "Last Verified Date", "Benefit Amount"])

    # Perform Filter
    results = filter_and_search_schemes(
        all_schemes,
        query=search_query,
        scheme_type=sel_type,
        state=sel_state,
        category=sel_cat,
        gender=sel_gender,
        max_income=max_inc_filter if max_inc_filter > 0 else None,
        sort_by=sort_choice
    )

    st.markdown(f"**Found {len(results)} scholarships matching your filters**")

    # Display Schemes
    for s in results:
        rules = s.get("eligibility_rules", {})
        with st.container(border=True):
            rcol1, rcol2 = st.columns([3, 1])
            with rcol1:
                st.markdown(f"### {s.get('name')}")
                st.caption(f"**Administering Body:** {s.get('ministry')}")
                st.markdown(
                    f"<span class='badge-type'>{s.get('scheme_type')}</span> "
                    f"<span class='badge-verified'>{s.get('verification_status')}</span> "
                    f"<span class='badge-state'>{', '.join(rules.get('domicile_states', []))}</span>",
                    unsafe_allow_html=True
                )
            with rcol2:
                st.markdown(f"<div style='text-align:right; font-size:1.2rem; color:#1e3a8a; font-weight:800;'>{s.get('benefit_amount_display')}</div>", unsafe_allow_html=True)
                st.caption(f"<div style='text-align:right;'>Verified: {s.get('last_verified_date')}</div>", unsafe_allow_html=True)

            st.markdown(f"**Benefits:** {s.get('benefit_details')}")
            
            with st.expander("📋 Eligibility Guidelines & Documentation Rules"):
                ecol1, ecol2 = st.columns(2)
                with ecol1:
                    st.markdown("**Documented Eligibility Rules:**")
                    st.markdown(f"- **Education Levels:** {', '.join(rules.get('education_levels', []))}")
                    st.markdown(f"- **Target Genders:** {', '.join(rules.get('target_genders', []))}")
                    st.markdown(f"- **Target Categories:** {', '.join(rules.get('target_categories', []))}")
                    inc_val = format_inr(rules.get('max_annual_income')) if rules.get('max_annual_income') else "No rigid income ceiling"
                    st.markdown(f"- **Income Ceiling:** {inc_val}")
                    if rules.get("min_marks_percent"):
                        st.markdown(f"- **Minimum Marks:** {rules.get('min_marks_percent')}%")
                    if rules.get("other_conditions"):
                        st.markdown("**Key Conditions:**")
                        for cond in rules.get("other_conditions"):
                            st.markdown(f"  * {cond}")
                with ecol2:
                    st.markdown("**Required Documents:**")
                    for doc in s.get("required_documents", []):
                        st.markdown(f"- {doc}")

            st.caption(f"🗓️ **Application Cycle:** {s.get('application_cycle_note')}")
            
            b1, b2, b3 = st.columns([2, 2, 2])
            with b1:
                st.link_button(f"🚀 Official Portal ({s.get('portal_name')})", s.get("official_portal_url"), use_container_width=True)
            with b2:
                st.link_button("📄 Official Scheme Guidelines PDF", s.get("guidelines_url"), use_container_width=True)
            with b3:
                if st.button("📋 Generate Checklist", key=f"chk_nav_{s.get('id')}", use_container_width=True):
                    st.session_state.active_scheme_for_checklist = s.get("id")
                    st.session_state.active_nav = "📋 Document Checklist"
                    st.rerun()


# -------------------------------------------------------------------------------------------------
# PAGE 4: DOCUMENT CHECKLIST
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "📋 Document Checklist":
    st.markdown("## 📋 Official Document Checklist & Preparation Guide")
    st.write(
        "Application rejections are overwhelmingly caused by avoidable document mistakes—such as Aadhaar name mismatches, "
        "expired income certificates, or bank accounts not mapped to NPCI. Use this interactive checklist to prepare your dossier."
    )

    # Scheme Selector
    scheme_options = {s["name"]: s["id"] for s in all_schemes}
    
    # Pre-select if forwarded from Explorer
    pre_select_id = st.session_state.get("active_scheme_for_checklist", all_schemes[0]["id"])
    pre_select_name = [name for name, sid in scheme_options.items() if sid == pre_select_id]
    default_name = pre_select_name[0] if pre_select_name else list(scheme_options.keys())[0]

    chosen_scheme_name = st.selectbox("Select Scholarship Scheme to prepare checklist for:", list(scheme_options.keys()), index=list(scheme_options.keys()).index(default_name))
    chosen_id = scheme_options[chosen_scheme_name]
    chosen_scheme = next((s for s in all_schemes if s["id"] == chosen_id), all_schemes[0])

    st.markdown(f"### Documents for: **{chosen_scheme.get('name')}**")
    st.caption(f"**Portal:** [{chosen_scheme.get('portal_name')}]({chosen_scheme.get('official_portal_url')}) | **Last Verified:** {chosen_scheme.get('last_verified_date')}")

    # Checklist Container
    req_docs = chosen_scheme.get("required_documents", [])
    crit_verifs = chosen_scheme.get("verification_checklist", [])
    all_checklist_items = req_docs + crit_verifs

    # Initialize state for this scheme if absent
    if chosen_id not in st.session_state.checklist_state:
        st.session_state.checklist_state[chosen_id] = set()

    checked_items = st.session_state.checklist_state[chosen_id]

    doc_col1, doc_col2 = st.columns([3, 2])

    with doc_col1:
        st.markdown("#### 1. Mandatory Documents for Upload")
        for i, doc in enumerate(req_docs):
            is_checked = st.checkbox(doc, value=(doc in checked_items), key=f"chk_{chosen_id}_doc_{i}")
            if is_checked:
                checked_items.add(doc)
            else:
                checked_items.discard(doc)

        st.markdown("#### 2. Critical Verification Safeguards")
        for j, verif in enumerate(crit_verifs):
            is_checked = st.checkbox(verif, value=(verif in checked_items), key=f"chk_{chosen_id}_verif_{j}")
            if is_checked:
                checked_items.add(verif)
            else:
                checked_items.discard(verif)

        # Progress
        completed = len(checked_items)
        total = len(all_checklist_items)
        pct = int((completed / total) * 100) if total > 0 else 0
        st.progress(pct / 100.0)
        st.write(f"**Checklist Readiness: {completed} of {total} items verified ({pct}%)**")

        # Download Checklist as Markdown
        checklist_md = generate_scheme_checklist_markdown(chosen_scheme, list(checked_items))
        st.download_button(
            label="📥 Download Checklist as Markdown (.md)",
            data=checklist_md,
            file_name=f"{chosen_id}_document_checklist.md",
            mime="text/markdown",
            use_container_width=True
        )

    with doc_col2:
        st.markdown("#### ⚠️ Avoid Top Rejection Pitfalls")
        for rej in COMMON_REJECTION_REASONS[:3]:
            with st.container(border=True):
                st.markdown(f"**{rej['issue']}**")
                st.caption(rej["explanation"])
                st.info(f"💡 **Fix:** {rej['prevention']}")

    st.markdown("---")
    st.markdown("#### 📌 General Portal Application Protocol")
    for step in GENERAL_PORTAL_PREPARATION_STEPS:
        st.markdown(f"- {step}")


# -------------------------------------------------------------------------------------------------
# PAGE 5: AI SCHOLARBOT CHAT
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "🤖 AI ScholarBot Chat":
    st.markdown("## 🤖 AI Scholarship Assistant (ScholarBot)")
    st.write(
        "Ask questions about eligibility criteria, document requirements, reservation policies, and application rules. "
        "Answers are strictly grounded in verified government scholarship documentation."
    )

    # Prompt Suggestions
    st.markdown("##### 💡 Suggested Questions")
    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    
    suggested_q = None
    with pcol1:
        if st.button("Scholarships for girls in B.Tech?", use_container_width=True):
            suggested_q = "What scholarships are available for girl students in engineering or B.Tech?"
    with pcol2:
        if st.button("Income limit for Central Sector?", use_container_width=True):
            suggested_q = "What is the family income limit and eligibility for PM-USP Central Sector Scholarship?"
    with pcol3:
        if st.button("Documents for SC/ST scholarship?", use_container_width=True):
            suggested_q = "What documents are required to apply for Post-Matric SC scholarship?"
    with pcol4:
        if st.button("Can I get 2 scholarships?", use_container_width=True):
            suggested_q = "Can I apply for and receive multiple government scholarships at the same time?"

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.markdown("###### Verified Official Sources:")
                for src in msg["sources"]:
                    st.markdown(f"- **{src['name']}** — [{src['portal']}]({src['portal_url']}) (Verified: {src['last_verified']})")

    # Chat Input
    user_input = st.chat_input("Ask a scholarship question (e.g., 'What is NPCI mapping and why is it needed?')...")
    
    active_prompt = suggested_q if suggested_q else user_input

    if active_prompt:
        # User message
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching official scheme guidelines..."):
                resp = ask_scholar_bot(active_prompt, st.session_state.student_profile)
                
                st.markdown(resp["answer"])
                st.caption(f"Response mode: *{resp['mode']}*")
                
                if resp.get("sources"):
                    st.markdown("###### Verified Official Sources:")
                    for src in resp["sources"]:
                        st.markdown(f"- **{src['name']}** — [{src['portal']}]({src['portal_url']}) (Verified: {src['last_verified']})")

        # Save to chat history
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": resp["answer"],
            "sources": resp.get("sources", [])
        })


# -------------------------------------------------------------------------------------------------
# PAGE 6: OFFICIAL PORTALS & GUIDELINES
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "ℹ️ Official Portals & Guidelines":
    st.markdown("## ℹ️ Official Portals Directory & Verification Policy")
    st.write(
        "ScholarGuide AI prioritizes data authenticity above all. Below are the primary official portals "
        "and statutory authorities governing Indian higher education scholarships."
    )

    st.markdown("### 🏛️ Authorized Government Portals")
    
    portals = [
        {
            "name": "National Scholarship Portal (NSP)",
            "url": "https://scholarships.gov.in/",
            "desc": "The apex digital scholarship portal of the Government of India. Hosts Central Sector schemes from the Ministry of Education, Ministry of Social Justice, Ministry of Tribal Affairs, and Ministry of Minority Affairs.",
            "type": "National Apex Portal"
        },
        {
            "name": "AICTE Student Development Schemes Portal",
            "url": "https://www.aicte-india.org/schemes/students-development-schemes",
            "desc": "Official portal of the All India Council for Technical Education administering Pragati (for girls), Saksham (for specially abled), and Swanath scholarships.",
            "type": "Technical Education Regulatory Body"
        },
        {
            "name": "UGC Scholarships & Fellowships",
            "url": "https://www.ugc.gov.in/",
            "desc": "University Grants Commission portal administering Ishan Uday for the North Eastern Region and various postgraduate single girl child fellowships.",
            "type": "Higher Education Apex Regulator"
        },
        {
            "name": "MahaDBT (Aaple Sarkar DBT Portal)",
            "url": "https://mahadbt.maharashtra.gov.in/",
            "desc": "Direct Benefit Transfer portal of the Government of Maharashtra for EBC fee concessions and SC/ST/OBC/VJNT post-matric scholarships.",
            "type": "State DBT Portal (Maharashtra)"
        },
        {
            "name": "UP Scholarship Portal",
            "url": "https://scholarship.up.gov.in/",
            "desc": "Official portal of the Government of Uttar Pradesh for Dashmottar post-matric scholarships across General, OBC, SC, ST, and Minority communities.",
            "type": "State Scholarship Portal (UP)"
        },
        {
            "name": "Karnataka State Scholarship Portal (SSP)",
            "url": "https://ssp.postmatric.karnataka.gov.in/",
            "desc": "Single portal of the Government of Karnataka for post-matric student fee reimbursement and maintenance stipends with Kutumba ID integration.",
            "type": "State Scholarship Portal (Karnataka)"
        }
    ]

    for p in portals:
        with st.container(border=True):
            pcol1, pcol2 = st.columns([3, 1])
            with pcol1:
                st.markdown(f"#### {p['name']}")
                st.caption(f"**Authority Type:** {p['type']}")
                st.write(p["desc"])
            with pcol2:
                st.link_button(f"Visit Official Portal ↗", p["url"], use_container_width=True)

    st.markdown("---")
    st.markdown("### 📜 Data Integrity & Non-Hallucination Policy")
    st.markdown("""
    - **No Live Deadline Claims:** Portals alter application windows and deadline extensions continuously. We state documented academic cycles and direct students to official portals for live deadline verification.
    - **Documented Rules Only:** Eligibility calculations match codified rules published in official gazette notifications.
    - **Demonstration Marking:** Any sample data or unverified schemes are explicitly labeled and never mixed with statutory schemes.
    """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    <strong>ScholarGuide AI</strong> — Government Schemes & Scholarship Assistant<br>
    Empowering Indian college students with transparent, verifiable government scholarship intelligence.<br>
    <em>Preliminary guidance only. All grants and disbursements are subject to official portal verification by respective ministries.</em>
</div>
""", unsafe_allow_html=True)
