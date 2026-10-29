"""Document checklist generator, preparation guidelines, and export utilities."""

from typing import List, Dict, Any


COMMON_REJECTION_REASONS = [
    {
        "issue": "Bank Account Not Seeded with Aadhaar (NPCI Mapping)",
        "explanation": "Since government scholarships disburse funds via Direct Benefit Transfer (DBT), accounts with only standard KYC but no active NPCI Aadhaar mapper reject payment credits.",
        "prevention": "Visit your bank branch and submit an Aadhaar Seeding / NPCI Mapping consent form. Check status on UIDAI portal (resident.uidai.gov.in)."
    },
    {
        "issue": "Name or Date of Birth Mismatch in Aadhaar vs Marksheet",
        "explanation": "Minor spelling differences (e.g. initials vs expanded name) between Class 10/12 marksheet and Aadhaar cause automated portal verification rejections.",
        "prevention": "Update your Aadhaar card details beforehand at an Aadhaar Seva Kendra to match your official High School leaving marksheet."
    },
    {
        "issue": "Expired or Unauthorized Income Certificate",
        "explanation": "Submitting salary slips, affidavits, or notary certificates instead of a Digital Revenue Income Certificate signed by a Tehsildar/SDM.",
        "prevention": "Obtain an official revenue income certificate from your state's online portal (e-District / Nadakacheri / MahaOnline) issued within the current financial year."
    },
    {
        "issue": "Claiming Dual Central Scholarships",
        "explanation": "Applying for and receiving maintenance allowances from more than one government scheme for the same course year.",
        "prevention": "Select and apply for the single scheme offering the best benefit coverage for your situation."
    },
    {
        "issue": "Non-Submission of Institutional Bonafide Form",
        "explanation": "Uploading only the admission receipt without the official college Bonafide Certificate stamped by the Principal / Registrar.",
        "prevention": "Download the scheme-specific Bonafide format from the portal, get it physically stamped and signed by the college authorities, and re-upload before deadline."
    }
]


GENERAL_PORTAL_PREPARATION_STEPS = [
    "Step 1: Verify your Aadhaar details match your academic records (Exact Name, Father's Name, DOB).",
    "Step 2: Ensure your bank account is in your sole name (not joint) and linked to NPCI Aadhaar mapper.",
    "Step 3: Collect current financial year Income Certificate and Caste/Category Certificate from the Tehsildar.",
    "Step 4: Obtain Bonafide Student Certificate with AISHE institute code from your college office.",
    "Step 5: Keep scanned PDF copies under 200 KB each with clear, legible text (avoid blurry camera photos).",
    "Step 6: Submit application on the official portal and note down the permanent Application ID.",
    "Step 7: Submit physical copies along with original documents for college level verification before institute deadline."
]


def generate_scheme_checklist_markdown(scheme: Dict[str, Any], checked_items: List[str] = None) -> str:
    """Generate a clean Markdown checklist that the student can copy or save."""
    checked_set = set(checked_items or [])
    scheme_name = scheme.get("name", "Scholarship")
    portal = scheme.get("portal_name", "Official Portal")
    url = scheme.get("official_portal_url", "")
    docs = scheme.get("required_documents", [])
    verifs = scheme.get("verification_checklist", [])

    lines = [
        f"# Application Document Checklist — {scheme_name}",
        f"**Official Portal:** [{portal}]({url})",
        f"**Last Verified:** {scheme.get('last_verified_date', 'N/A')}",
        "",
        "## 1. Required Documents for Upload",
    ]

    for doc in docs:
        check = "x" if doc in checked_set else " "
        lines.append(f"- [{check}] {doc}")

    lines.append("")
    lines.append("## 2. Critical Verification Points")
    for v in verifs:
        check = "x" if v in checked_set else " "
        lines.append(f"- [{check}] {v}")

    lines.append("")
    lines.append("## 3. Official Source Links")
    lines.append(f"- Application Portal: {scheme.get('official_portal_url', 'N/A')}")
    lines.append(f"- Scheme Guidelines: {scheme.get('guidelines_url', 'N/A')}")
    lines.append("")
    lines.append("> **Notice:** This checklist is compiled from documented government scheme guidelines. Ensure all documents are original and current before submitting on the official portal.")

    return "\n".join(lines)
