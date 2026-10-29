# ScholarGuide AI — Government Schemes & Scholarship Assistant 🎓🇮🇳

**ScholarGuide AI** is an intelligent, transparent web application designed to help Indian undergraduate, postgraduate, and technical college students discover legitimate government scholarships, evaluate their documented eligibility rules, prepare mistake-free document checklists, and navigate official application portals.

---

## 🌟 Key Features

1. **🏠 Home Dashboard:** Project introduction, statistics overview (12 curated government schemes, maximum benefit up to ₹93,600/yr), verified portal directory, and announcement guidelines.
2. **👤 Student Profile & Eligibility Match:** Dynamic profile form with education level, degree course, year of study, domicile state/UT, annual family income, social category, gender, PwD status, minority religion, and marks percentage.
3. **📊 Deterministic Rule-Matching Engine:** Evaluates student profiles against official gazette rules. Displays:
   - **Matching Criteria** (verified green checkmarks)
   - **Unmet Criteria** (exact reasons with red indicators)
   - **Verification Required** (institutional AISHE code, Tehsildar revenue certificate, single-scholarship undertaking)
4. **🔍 Scheme Explorer & Advanced Filters:** Search by keyword, scheme type (Central Sector, Centrally Sponsored, UGC/AICTE, State Govt), state domicile, category, gender, and income ceiling.
5. **🤖 AI ScholarBot Chat:** Grounded Q&A assistant using retrieved official guidelines rather than unsupported assumptions. Works in **Demo Mode (no API key required)** or connects to Gemini/OpenAI when keys are configured in `.env`.
6. **📋 Interactive Document Checklist:** Scheme-specific checklists with progress indicators, common rejection reasons (NPCI Aadhaar mapping, name mismatches), and downloadable Markdown checklists.
7. **🔗 100% Official Source Links:** Every scheme provides verified links to official portals ([scholarships.gov.in](https://scholarships.gov.in), AICTE, MahaDBT, UP Scholarship, SSP Karnataka) with documented verification dates.
8. **⚠️ Prominent Disclaimers:** Visible notices clarifying that preliminary evaluations are advisory and final award authority resides with the government ministries.

---

## 🏛️ Curated Government Schemes Included

1. **Central Sector Scheme of Scholarship for College and University Students (PM-USP CSSS)** — Ministry of Education
2. **AICTE Pragati Scholarship Scheme for Girl Students (Technical Degree)** — AICTE
3. **AICTE Saksham Scholarship Scheme for Specially-Abled Students** — AICTE
4. **AICTE Swanath Scholarship Scheme** (Orphan / COVID-19 / Wards of Martyrs) — AICTE
5. **Post-Matric Scholarships Scheme for Scheduled Caste Students (PMS-SC)** — Ministry of Social Justice
6. **Post-Matric Scholarship Scheme for Scheduled Tribe Students (PMS-ST)** — Ministry of Tribal Affairs
7. **Post-Matric Scholarship for Other Backward Classes (OBC)** — Ministry of Social Justice
8. **Ishan Uday Special Scholarship for North Eastern Region (NER)** — UGC / Ministry of Education
9. **Post-Matric Scholarship Scheme for Minorities** — Ministry of Minority Affairs
10. **Maharashtra MahaDBT Rajarshi Shahu Maharaj EBC Scheme** — Govt. of Maharashtra
11. **Uttar Pradesh Post-Matric Scholarship (Dashmottar)** — Govt. of Uttar Pradesh
12. **Karnataka State Scholarship Portal (SSP) Post-Matric Scheme** — Govt. of Karnataka

---

## 🛠️ Technology Stack

- **Frontend & App Framework:** Python 3.10+, [Streamlit](https://streamlit.io/)
- **Rules Engine:** Python deterministic evaluation algorithms (`src/eligibility_engine.py`)
- **LLM Integration:** Google Gemini REST API or OpenAI-compatible endpoint with automatic fallback to high-fidelity Offline Grounded Demo Engine
- **Testing:** Pytest (`tests/`)

---

## 🚀 Quickstart & Setup Instructions

### 1. Clone or Open the Repository
```bash
cd ScholarGuide-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note for Windows ARM64 / Python 3.14 environments:** If your environment flags a missing wheel for pyarrow, install Streamlit without binary build dependencies:
> ```bash
> pip install streamlit --no-deps
> pip install python-dotenv pytest requests altair click pydeck starlette uvicorn anyio python-multipart websockets itsdangerous watchdog
> ```

### 3. Configure Environment Variables (Optional)
The application works in **Demo Mode without any API keys**! If you wish to enable the live Google Gemini API:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Set your free Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```

### 4. Run the Test Suite
```bash
pytest
```
Expected output: **23 passed** unit tests covering eligibility rules, profile validation, search filters, and AI retrieval.

---

## 🖥️ Launch the Web Application

Run the following command in your terminal from the project folder:

```bash
streamlit run app.py
```

The application will start locally and open in your default web browser at:
```
http://localhost:8501
```

---

## 🧪 Testing Coverage

The project includes 23 unit tests across 4 test suites:
- `tests/test_validation.py`: Tests negative income handling, unrealistic bounds, percentage limits (0-100), and profile completeness.
- `tests/test_eligibility.py`: Tests CSSS board percentile and income caps, Pragati girl-student filtering, Saksham PwD verification, Ishan Uday North Eastern state domicile, and batch ranking.
- `tests/test_search.py`: Tests multi-criteria filtering, text search across scheme bodies, and alphabetical sorting.
- `tests/test_ai_advisor.py`: Tests grounded retrieval, Q&A synthesis, and demo mode fallback for NPCI and multiple scholarship rules.

---

## ⚖️ Official Disclaimer
ScholarGuide AI is an independent student guidance tool. All scheme criteria and guidelines are compiled from official public notifications published on the [National Scholarship Portal (scholarships.gov.in)](https://scholarships.gov.in/) and respective state portals. Final selection, grant disbursement, and institutional eligibility verification are governed exclusively by the competent government authorities.
