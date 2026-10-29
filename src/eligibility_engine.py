"""Deterministic eligibility evaluation engine for Indian government scholarships.

Evaluates a StudentProfile against official scheme rules.
Generates matched criteria, unmet criteria, and institutional verification requirements.
"""

from typing import List, Dict, Any, Tuple
from src.models import StudentProfile, CriterionEvaluation, EligibilityResult, ScholarshipScheme
from src.utils import format_inr


def evaluate_eligibility(profile: StudentProfile, scheme_dict: Dict[str, Any]) -> EligibilityResult:
    """Evaluate a student's profile against a single scholarship scheme."""
    rules = scheme_dict.get("eligibility_rules", {})
    scheme_id = scheme_dict.get("id", "")
    scheme_name = scheme_dict.get("name", "")
    
    matching_criteria: List[CriterionEvaluation] = []
    unmet_criteria: List[CriterionEvaluation] = []
    verification_required: List[CriterionEvaluation] = []

    # 1. Education Level
    allowed_edu = rules.get("education_levels", [])
    if allowed_edu:
        if profile.education_level in allowed_edu:
            matching_criteria.append(CriterionEvaluation(
                name="Education Level",
                status="MATCHED",
                detail=f"Enrolled in {profile.education_level}, which is accepted by this scheme.",
                required_value=", ".join(allowed_edu),
                provided_value=profile.education_level
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Education Level",
                status="UNMET",
                detail=f"Current education level ({profile.education_level}) is not supported. Scheme requires: {', '.join(allowed_edu)}.",
                required_value=", ".join(allowed_edu),
                provided_value=profile.education_level
            ))

    # 2. Year of Study / Fresh Application
    allowed_years = rules.get("allowed_years", [])
    fresh_year = rules.get("fresh_application_year")
    if fresh_year and profile.year_of_study != fresh_year:
        # Check if it's lateral entry for AICTE
        if "Lateral Entry" in profile.year_of_study and "2nd Year" in str(allowed_years):
            matching_criteria.append(CriterionEvaluation(
                name="Year of Study",
                status="MATCHED",
                detail=f"Eligible for 2nd Year Lateral Entry admission.",
                required_value=f"Fresh ({fresh_year}) or Lateral Entry",
                provided_value=profile.year_of_study
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Year of Study",
                status="UNMET",
                detail=f"Fresh award applications are restricted to {fresh_year} students. You indicated {profile.year_of_study}.",
                required_value=fresh_year,
                provided_value=profile.year_of_study
            ))
    elif allowed_years and profile.year_of_study not in allowed_years:
        unmet_criteria.append(CriterionEvaluation(
            name="Year of Study",
            status="UNMET",
            detail=f"Scheme applies to {', '.join(allowed_years)}, but student is in {profile.year_of_study}.",
            required_value=", ".join(allowed_years),
            provided_value=profile.year_of_study
        ))
    elif allowed_years:
        matching_criteria.append(CriterionEvaluation(
            name="Year of Study",
            status="MATCHED",
            detail=f"Year of study ({profile.year_of_study}) is eligible for application or renewal.",
            required_value=", ".join(allowed_years),
            provided_value=profile.year_of_study
        ))

    # 3. Gender
    target_genders = rules.get("target_genders", ["All"])
    if "All" in target_genders or profile.gender in target_genders:
        matching_criteria.append(CriterionEvaluation(
            name="Gender Eligibility",
            status="MATCHED",
            detail=f"Open to gender '{profile.gender}'.",
            required_value=", ".join(target_genders),
            provided_value=profile.gender
        ))
    else:
        unmet_criteria.append(CriterionEvaluation(
            name="Gender Eligibility",
            status="UNMET",
            detail=f"Scheme is designated exclusively for {', '.join(target_genders)} applicants.",
            required_value=", ".join(target_genders),
            provided_value=profile.gender
        ))

    # 4. Social Category / Caste
    target_categories = rules.get("target_categories", ["All"])
    if "All" in target_categories or profile.category in target_categories:
        matching_criteria.append(CriterionEvaluation(
            name="Social Category / Caste",
            status="MATCHED",
            detail=f"Your category '{profile.category}' meets the eligibility criteria.",
            required_value=", ".join(target_categories),
            provided_value=profile.category
        ))
    else:
        unmet_criteria.append(CriterionEvaluation(
            name="Social Category / Caste",
            status="UNMET",
            detail=f"Scheme is restricted to students in {', '.join(target_categories)}. Your profile specifies {profile.category}.",
            required_value=", ".join(target_categories),
            provided_value=profile.category
        ))

    # 5. Annual Family Income
    max_income = rules.get("max_annual_income")
    if max_income is not None:
        if profile.annual_income <= max_income:
            matching_criteria.append(CriterionEvaluation(
                name="Annual Family Income",
                status="MATCHED",
                detail=f"Family income ({format_inr(profile.annual_income)}) is within the official ceiling of {format_inr(max_income)}.",
                required_value=f"<= {format_inr(max_income)}",
                provided_value=format_inr(profile.annual_income)
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Annual Family Income",
                status="UNMET",
                detail=f"Family income ({format_inr(profile.annual_income)}) exceeds the maximum ceiling of {format_inr(max_income)}.",
                required_value=f"<= {format_inr(max_income)}",
                provided_value=format_inr(profile.annual_income)
            ))

    # 6. Domicile / State
    domicile_states = rules.get("domicile_states", ["All India / Central"])
    if "All India / Central" in domicile_states:
        matching_criteria.append(CriterionEvaluation(
            name="Domicile / State",
            status="MATCHED",
            detail="Central scheme open to eligible students across all Indian States & Union Territories.",
            required_value="All India",
            provided_value=profile.state
        ))
    elif profile.state in domicile_states:
        matching_criteria.append(CriterionEvaluation(
            name="Domicile / State",
            status="MATCHED",
            detail=f"Applicant domicile ({profile.state}) matches the designated state requirement.",
            required_value=", ".join(domicile_states),
            provided_value=profile.state
        ))
    else:
        unmet_criteria.append(CriterionEvaluation(
            name="Domicile / State",
            status="UNMET",
            detail=f"Scheme requires permanent domicile in {', '.join(domicile_states)}. Your profile indicates {profile.state}.",
            required_value=", ".join(domicile_states),
            provided_value=profile.state
        ))

    # 7. Differently Abled (PwD)
    pwd_required = rules.get("pwd_required", False)
    if pwd_required:
        if profile.is_pwd:
            matching_criteria.append(CriterionEvaluation(
                name="Differently Abled (PwD) Status",
                status="MATCHED",
                detail="Student has declared certified disability (40% or more), meeting requirement.",
                required_value="Disability >= 40%",
                provided_value="Yes (PwD)"
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Differently Abled (PwD) Status",
                status="UNMET",
                detail="This scholarship is reserved exclusively for students with benchmark disability (>=40%).",
                required_value="Disability >= 40%",
                provided_value="No"
            ))

    # 8. Minority Community
    minority_only = rules.get("minority_only", False)
    if minority_only:
        if profile.is_minority:
            community_str = profile.minority_community if profile.minority_community != "Not Applicable" else "Notified Community"
            matching_criteria.append(CriterionEvaluation(
                name="Minority Community",
                status="MATCHED",
                detail=f"Student belongs to notified minority community ({community_str}).",
                required_value="Muslim, Christian, Sikh, Buddhist, Jain, or Parsi",
                provided_value=community_str
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Minority Community",
                status="UNMET",
                detail="Scheme is exclusively for students belonging to notified religious minority communities.",
                required_value="Notified Minority Community",
                provided_value="Non-minority"
            ))

    # 9. Technical Course Requirement
    tech_only = rules.get("technical_course_only", False)
    if tech_only:
        if profile.is_technical_course:
            matching_criteria.append(CriterionEvaluation(
                name="Course Approval / Stream",
                status="MATCHED",
                detail="Enrolled in an AICTE-approved technical degree or diploma course.",
                required_value="AICTE Approved Technical Course",
                provided_value=profile.degree
            ))
        else:
            unmet_criteria.append(CriterionEvaluation(
                name="Course Approval / Stream",
                status="UNMET",
                detail="This scheme strictly funds AICTE-approved technical degree or diploma programs.",
                required_value="AICTE Approved Technical Course",
                provided_value=f"{profile.degree} (Non-technical)"
            ))

    # 10. Academic Marks / Percentile
    min_marks = rules.get("min_marks_percent")
    if min_marks is not None:
        if profile.marks_percentage is not None and profile.marks_percentage > 0:
            if profile.marks_percentage >= min_marks:
                matching_criteria.append(CriterionEvaluation(
                    name="Academic Score",
                    status="MATCHED",
                    detail=f"Score ({profile.marks_percentage}%) satisfies the minimum threshold of {min_marks}%.",
                    required_value=f">= {min_marks}%",
                    provided_value=f"{profile.marks_percentage}%"
                ))
            else:
                unmet_criteria.append(CriterionEvaluation(
                    name="Academic Score",
                    status="UNMET",
                    detail=f"Score ({profile.marks_percentage}%) is below the minimum required cutoff of {min_marks}%.",
                    required_value=f">= {min_marks}%",
                    provided_value=f"{profile.marks_percentage}%"
                ))
        else:
            verification_required.append(CriterionEvaluation(
                name="Academic Score Verification",
                status="VERIFICATION_REQUIRED",
                detail=f"Scheme requires qualifying score/percentile (>= {min_marks}% or state board top-20 percentile). Please verify official marksheet.",
                required_value=f">= {min_marks}%",
                provided_value="Not provided"
            ))

    # 11. Institutional Verification Criteria (Standard Government Conditions)
    verification_required.append(CriterionEvaluation(
        name="Income Certificate Verification",
        status="VERIFICATION_REQUIRED",
        detail="Income certificate must be issued by a competent Revenue Authority (Tehsildar/SDM) for the current financial year.",
        required_value="Valid official revenue certificate",
        provided_value="Self-reported"
    ))
    verification_required.append(CriterionEvaluation(
        name="Institute Registration & Bonafide",
        status="VERIFICATION_REQUIRED",
        detail="Your college/institution must be registered on the official portal with a valid AISHE / portal code and authenticate your admission.",
        required_value="Active AISHE registered institute",
        provided_value="Requires college verification"
    ))
    verification_required.append(CriterionEvaluation(
        name="Single Scholarship Undertaking",
        status="VERIFICATION_REQUIRED",
        detail="Government guidelines prohibit receiving dual scholarship maintenance allowances for the same course from other central/state programs.",
        required_value="No overlapping central/state scholarship",
        provided_value="Requires student undertaking"
    ))
    verification_required.append(CriterionEvaluation(
        name="Aadhaar-Seeded Bank Account (NPCI)",
        status="VERIFICATION_REQUIRED",
        detail="Bank account must be in applicant's sole name and mapped to Aadhaar via NPCI for Direct Benefit Transfer (DBT).",
        required_value="NPCI Aadhaar-seeded active account",
        provided_value="Requires bank verification"
    ))

    # Calculate overall eligibility verdict and match score
    total_evaluated = len(matching_criteria) + len(unmet_criteria)
    if total_evaluated == 0:
        match_score = 50.0
    else:
        match_score = round((len(matching_criteria) / total_evaluated) * 100, 1)

    if len(unmet_criteria) == 0:
        is_eligible = True
        match_status = "Eligible (High Match)"
        summary_explanation = (
            f"Great news! Your profile satisfies all primary documented eligibility requirements "
            f"for '{scheme_name}'. You now need to complete institutional verifications and compile required documents."
        )
    else:
        is_eligible = False
        match_status = "Not Eligible"
        unmet_names = [c.name for c in unmet_criteria]
        summary_explanation = (
            f"Your profile currently does not meet {len(unmet_criteria)} documented criteria: "
            f"{', '.join(unmet_names)}. Check scheme guidelines for full terms."
        )

    return EligibilityResult(
        scheme_id=scheme_id,
        scheme_name=scheme_name,
        is_eligible=is_eligible,
        match_status=match_status,
        match_score_percentage=match_score,
        matching_criteria=matching_criteria,
        unmet_criteria=unmet_criteria,
        verification_required=verification_required,
        summary_explanation=summary_explanation
    )


def batch_evaluate_schemes(profile: StudentProfile, schemes: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], EligibilityResult]]:
    """Evaluate student profile against a list of schemes and return results sorted by eligibility."""
    results = []
    for s in schemes:
        eval_res = evaluate_eligibility(profile, s)
        results.append((s, eval_res))
    
    # Sort: Eligible schemes first (sorted by match score desc), then Ineligible schemes
    results.sort(key=lambda item: (item[1].is_eligible, item[1].match_score_percentage), reverse=True)
    return results
