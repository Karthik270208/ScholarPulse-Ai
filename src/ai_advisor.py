"""AI Advisor module for grounded Q&A over official scholarship guidelines.

Supports:
1. Google Gemini API (via GEMINI_API_KEY)
2. OpenAI-compatible API (via OPENAI_API_KEY)
3. Intelligent Deterministic Demo Mode (offline / no API key required)
"""

import os
import json
import requests
from typing import List, Dict, Any, Tuple
from src.utils import load_schemes_data, format_inr
from src.models import StudentProfile


SYSTEM_PROMPT = """You are ScholarGuide AI, an official Indian Government Schemes and Scholarship Assistant.
Your mission is to provide accurate, strictly grounded guidance to Indian college students.

Strict Rules:
1. Ground your answers ONLY in the official scholarship data provided in the context.
2. NEVER invent scholarship names, benefits, income caps, reservation percentages, deadlines, or URLs.
3. Every scholarship you mention MUST include its official portal name, verified application URL, and last-verified date.
4. If a user asks about a scholarship or rule that is not present in the provided context, clearly state: "This information is not documented in the current verified scheme database. Please check the National Scholarship Portal (https://scholarships.gov.in/) or the relevant state government department."
5. Clarify that application cycles typically follow annual academic calendars, and live dates must be verified on the official portal.
6. Always end with a brief reminder that preliminary eligibility matches are informational and not official award decisions.
"""


def retrieve_relevant_context(query: str, max_schemes: int = 4) -> List[Dict[str, Any]]:
    """Retrieve top relevant scheme documents based on keywords in student query."""
    schemes = load_schemes_data()
    # Normalize punctuation and split into words
    normalized_q = query.lower().replace("-", " ").replace("/", " ")
    q_words = [w.strip() for w in normalized_q.split() if len(w.strip()) >= 2]
    
    scored_schemes: List[Tuple[int, Dict[str, Any]]] = []
    
    for s in schemes:
        score = 0
        raw_corpus = (
            s.get("id", "") + " " +
            s.get("name", "") + " " +
            s.get("short_name", "") + " " +
            s.get("scheme_type", "") + " " +
            s.get("ministry", "") + " " +
            s.get("benefit_details", "") + " " +
            " ".join(s.get("eligibility_rules", {}).get("target_categories", [])) + " " +
            " ".join(s.get("eligibility_rules", {}).get("target_genders", [])) + " " +
            " ".join(s.get("eligibility_rules", {}).get("domicile_states", [])) + " " +
            " ".join(s.get("required_documents", []))
        ).lower()
        
        # Replace separators with spaces for flexible matching
        clean_corpus = raw_corpus.replace("-", " ").replace("/", " ").replace("(", " ").replace(")", " ")
        
        # Keyword matching
        for word in q_words:
            if word in clean_corpus:
                score += 3

        # Exact ID / acronym boost
        for word in q_words:
            if word in s.get("id", "").lower().split("-"):
                score += 5
            if word in s.get("short_name", "").lower().split():
                score += 5
        
        # Specific high-value intent boosts
        if "girl" in normalized_q or "female" in normalized_q or "women" in normalized_q:
            if "Female" in s.get("eligibility_rules", {}).get("target_genders", []):
                score += 12
        if "engineer" in normalized_q or "btech" in normalized_q or "technical" in normalized_q:
            if s.get("eligibility_rules", {}).get("technical_course_only"):
                score += 10
        if " sc " in f" {normalized_q} " or "scheduled caste" in normalized_q:
            if "Scheduled Caste (SC)" in s.get("eligibility_rules", {}).get("target_categories", []):
                score += 10
            if "sc" in s.get("id", "").lower():
                score += 12
        if " st " in f" {normalized_q} " or "scheduled tribe" in normalized_q:
            if "Scheduled Tribe (ST)" in s.get("eligibility_rules", {}).get("target_categories", []):
                score += 10
            if "st" in s.get("id", "").lower():
                score += 12
        if "minority" in normalized_q or "muslim" in normalized_q or "christian" in normalized_q or "sikh" in normalized_q:
            if s.get("eligibility_rules", {}).get("minority_only"):
                score += 12
        if "disabled" in normalized_q or "pwd" in normalized_q or "saksham" in normalized_q:
            if s.get("eligibility_rules", {}).get("pwd_required"):
                score += 12
        if "maharashtra" in normalized_q or "mahadbt" in normalized_q:
            if "Maharashtra" in s.get("eligibility_rules", {}).get("domicile_states", []):
                score += 12
        if "karnataka" in normalized_q or "ssp" in normalized_q:
            if "Karnataka" in s.get("eligibility_rules", {}).get("domicile_states", []):
                score += 12
        if "uttar pradesh" in normalized_q or "up" in normalized_q.split():
            if "Uttar Pradesh" in s.get("eligibility_rules", {}).get("domicile_states", []):
                score += 12
        if "north east" in normalized_q or "assam" in normalized_q or "ishan" in normalized_q:
            if "ishan" in s.get("id", ""):
                score += 12
        if "income" in normalized_q or "limit" in normalized_q:
            if s.get("eligibility_rules", {}).get("max_annual_income"):
                score += 3
        if "document" in normalized_q or "certificate" in normalized_q:
            score += 2

        scored_schemes.append((score, s))

    # Sort descending by score
    scored_schemes.sort(key=lambda x: x[0], reverse=True)
    
    # Return top N schemes
    top = [s for score, s in scored_schemes if score > 0][:max_schemes]
    if not top:
        top = [s for score, s in scored_schemes][:2]
    return top


def format_context_for_prompt(schemes: List[Dict[str, Any]], profile: StudentProfile = None) -> str:
    """Format retrieved schemes into clean text context for the model."""
    context_blocks = []
    
    if profile:
        context_blocks.append(
            f"STUDENT PROFILE:\n"
            f"- Education: {profile.education_level} ({profile.degree}, {profile.year_of_study})\n"
            f"- Domicile State: {profile.state}\n"
            f"- Annual Family Income: {format_inr(profile.annual_income)}\n"
            f"- Category: {profile.category} | Gender: {profile.gender}\n"
            f"- Differently Abled (PwD): {'Yes' if profile.is_pwd else 'No'} | Minority: {'Yes' if profile.is_minority else 'No'}\n"
            f"- Previous Score: {profile.marks_percentage}%\n"
        )
    
    context_blocks.append("OFFICIAL VERIFIED SCHEME DOCUMENTATION:")
    for i, s in enumerate(schemes, 1):
        rules = s.get("eligibility_rules", {})
        block = (
            f"\n[SCHEME {i}: {s.get('name')}]\n"
            f"- Ministry/Body: {s.get('ministry')}\n"
            f"- Scheme Type: {s.get('scheme_type')}\n"
            f"- Official Portal: {s.get('portal_name')} ({s.get('official_portal_url')})\n"
            f"- Official Guidelines Link: {s.get('guidelines_url')}\n"
            f"- Last Verified Date: {s.get('last_verified_date')}\n"
            f"- Application Cycle: {s.get('application_cycle_note')}\n"
            f"- Benefits: {s.get('benefit_amount_display')} ({s.get('benefit_details')})\n"
            f"- Eligibility Rules:\n"
            f"  * Education Levels: {', '.join(rules.get('education_levels', []))}\n"
            f"  * Target Genders: {', '.join(rules.get('target_genders', []))}\n"
            f"  * Target Categories: {', '.join(rules.get('target_categories', []))}\n"
            f"  * Max Family Income: {format_inr(rules.get('max_annual_income')) if rules.get('max_annual_income') else 'No strict income ceiling'}\n"
            f"  * Domicile States: {', '.join(rules.get('domicile_states', []))}\n"
            f"  * Minimum Marks: {rules.get('min_marks_percent')}% (if specified)\n"
            f"  * Additional Conditions: {'; '.join(rules.get('other_conditions', []))}\n"
            f"- Required Documents: {', '.join(s.get('required_documents', []))}\n"
        )
        context_blocks.append(block)

    return "\n".join(context_blocks)


def call_gemini_api(api_key: str, system_prompt: str, user_prompt: str) -> str:
    """Call Google Gemini REST API using requests."""
    # Using gemini-2.5-flash or gemini-1.5-flash
    models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_prompt}\n\nUser Question:\n{user_prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024
            }
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            # If 404 on model name, loop to fallback model
            if resp.status_code != 200:
                continue
        except Exception:
            continue
            
    raise RuntimeError("Gemini API call was unsuccessful. Falling back to Grounded Demo Engine.")


def call_openai_api(api_key: str, system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI-compatible REST API using requests."""
    url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=12)
    if resp.status_code == 200:
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    raise RuntimeError(f"OpenAI API error {resp.status_code}: {resp.text}")


def generate_grounded_demo_response(query: str, schemes: List[Dict[str, Any]], profile: StudentProfile = None) -> str:
    """Generate high-quality, grounded response deterministically when no API key is provided."""
    q_lower = query.lower()
    
    # 1. Multi-scholarship question
    if "multiple" in q_lower or "two scholarships" in q_lower or "both" in q_lower:
        return (
            "### ⚖️ Rules on Availing Multiple Government Scholarships\n\n"
            "According to official Government of India guidelines (including Ministry of Education and UGC rules):\n\n"
            "1. **Maintenance Allowance Prohibition:** A student cannot draw **two maintenance allowances** or tuition fee reimbursements from different government sources (Central and State) for the same course.\n"
            "2. **Fee Waiver vs Merit Stipend:** If you are awarded a fee waiver by your college or state government, you may be eligible to accept a pure merit scholarship, provided the scheme guidelines of both programs explicitly permit it.\n"
            "3. **Declaration Required:** On portals like the **National Scholarship Portal (NSP)**, you are required to submit an undertaking confirming that you are not receiving benefits from any other scholarship scheme for the current academic session.\n\n"
            "**Official Source:** [National Scholarship Portal Guidelines](https://scholarships.gov.in/)\n"
            "*Verification Date: 2025-01-15*\n\n"
            "> **Notice:** Preliminary matches are informational. Final rules depend on the respective scheme guidelines."
        )

    # 2. Income certificate or bank account / NPCI mapping questions
    if "npci" in q_lower or "aadhaar" in q_lower or "bank" in q_lower or "seeding" in q_lower:
        return (
            "### 💳 Aadhaar Seeding and NPCI Mapping Explained\n\n"
            "For all central and state scholarships disbursed through **Direct Benefit Transfer (DBT)**:\n\n"
            "- **Standard KYC vs NPCI Seeding:** Merely linking your Aadhaar number to your bank account for KYC is **NOT** sufficient. The bank account must be actively **seeded into the NPCI (National Payments Corporation of India) mapper**.\n"
            "- **Sole Account Only:** The account must be in the applicant's sole name (joint accounts frequently cause payment reversals).\n"
            "- **How to Verify:** You can check your Aadhaar-Bank mapping status on the official UIDAI resident portal or your bank's mobile app.\n\n"
            "**Official Portal:** [National Scholarship Portal DBT Helpdesk](https://scholarships.gov.in/)\n"
            "*Verification Date: 2025-01-15*"
        )

    # 3. Document checklist inquiry
    if "document" in q_lower or "certificate" in q_lower or "checklist" in q_lower:
        if schemes:
            target = schemes[0]
            docs = target.get("required_documents", [])
            doc_items = "\n".join([f"- **{d}**" for d in docs])
            return (
                f"### 📋 Document Checklist for {target.get('name')}\n\n"
                f"Based on official guidelines from **{target.get('ministry')}**:\n\n"
                f"{doc_items}\n\n"
                f"**Official Portal:** [{target.get('portal_name')}]({target.get('official_portal_url')})\n"
                f"**Scheme Guidelines:** [View Official Notification]({target.get('guidelines_url')})\n"
                f"**Last Verified:** {target.get('last_verified_date')}\n\n"
                f"> **Important Tip:** Ensure that names and dates of birth match exactly across your Aadhaar card and matriculation certificate to prevent automated verification rejection."
            )

    # 4. Standard scheme matching response based on retrieved context
    if schemes:
        response_lines = [
            f"### 🏛️ Verified Scholarship Findings for Your Query\n",
            f"Here is documented information from official government guidelines:\n"
        ]
        
        for i, s in enumerate(schemes[:3], 1):
            rules = s.get("eligibility_rules", {})
            income_str = format_inr(rules.get("max_annual_income")) if rules.get("max_annual_income") else "No rigid income limit"
            
            response_lines.append(f"#### {i}. {s.get('name')}")
            response_lines.append(f"- **Administrative Ministry / Authority:** {s.get('ministry')}")
            response_lines.append(f"- **Scholarship Benefit:** {s.get('benefit_amount_display')}")
            response_lines.append(f"- **Income Ceiling:** Up to {income_str} per annum")
            response_lines.append(f"- **Eligible Education Levels:** {', '.join(rules.get('education_levels', []))}")
            response_lines.append(f"- **Target Category & Gender:** {', '.join(rules.get('target_categories', []))} | {', '.join(rules.get('target_genders', []))}")
            response_lines.append(f"- **Application Cycle:** {s.get('application_cycle_note')}")
            response_lines.append(f"- **Official Portal:** [{s.get('portal_name')}]({s.get('official_portal_url')})")
            response_lines.append(f"- **Official Guidelines Link:** [Read Guidelines PDF]({s.get('guidelines_url')})")
            response_lines.append(f"- **Record Last Verified:** {s.get('last_verified_date')}\n")

        response_lines.append(
            "> ⚠️ **Official Disclaimer:** Preliminary matches are generated for guidance only and do NOT guarantee award selection. Always verify current academic year deadlines and eligibility on the official portal."
        )
        return "\n".join(response_lines)

    return (
        "I could not locate a verified government scholarship matching those exact terms in the current database. "
        "Please visit the official **[National Scholarship Portal (scholarships.gov.in)](https://scholarships.gov.in/)** "
        "or consult your State Directorate of Higher Education to verify documented schemes."
    )


def ask_scholar_bot(query: str, profile: StudentProfile = None) -> Dict[str, Any]:
    """Main entry point to ask questions to ScholarBot.

    Automatically uses GEMINI_API_KEY or OPENAI_API_KEY if configured in environment,
    otherwise gracefully executes in intelligent Grounded Demo Mode.
    """
    schemes = retrieve_relevant_context(query, max_schemes=3)
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    context_text = format_context_for_prompt(schemes, profile)
    full_user_prompt = f"CONTEXT:\n{context_text}\n\nSTUDENT QUESTION:\n{query}"

    mode_used = "Demo Mode (Grounded Official Data)"
    answer = ""

    if gemini_key and gemini_key.strip() and gemini_key != "your_gemini_api_key_here":
        try:
            answer = call_gemini_api(gemini_key.strip(), SYSTEM_PROMPT, full_user_prompt)
            mode_used = "Gemini LLM (Grounded Context)"
        except Exception as e:
            # Fallback to grounded demo mode
            answer = generate_grounded_demo_response(query, schemes, profile)
            mode_used = f"Demo Mode (API Fallback: {str(e)[:40]}...)"
    elif openai_key and openai_key.strip() and openai_key != "your_openai_api_key_here":
        try:
            answer = call_openai_api(openai_key.strip(), SYSTEM_PROMPT, full_user_prompt)
            mode_used = "OpenAI LLM (Grounded Context)"
        except Exception as e:
            answer = generate_grounded_demo_response(query, schemes, profile)
            mode_used = f"Demo Mode (API Fallback: {str(e)[:40]}...)"
    else:
        answer = generate_grounded_demo_response(query, schemes, profile)
        mode_used = "Demo Mode (Offline Grounded Engine)"

    return {
        "answer": answer,
        "mode": mode_used,
        "referenced_schemes": [s.get("name") for s in schemes],
        "sources": [
            {
                "name": s.get("name"),
                "portal": s.get("portal_name"),
                "portal_url": s.get("official_portal_url"),
                "guidelines_url": s.get("guidelines_url"),
                "last_verified": s.get("last_verified_date")
            }
            for s in schemes
        ]
    }
