"""Data models for student profile, scholarship schemes, and eligibility evaluations."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class StudentProfile:
    education_level: str = "Undergraduate (UG)"
    degree: str = "B.Tech / B.E. (Engineering)"
    year_of_study: str = "1st Year"
    state: str = "All India / Central"
    annual_income: float = 200000.0
    category: str = "General / Open"
    gender: str = "Female"
    is_pwd: bool = False
    is_minority: bool = False
    minority_community: str = "Not Applicable"
    is_single_girl_child: bool = False
    marks_percentage: Optional[float] = 75.0
    is_technical_course: bool = True
    is_hosteller: bool = False

    def validate(self) -> List[str]:
        """Validate student profile fields and return a list of error messages."""
        errors = []
        if self.annual_income < 0:
            errors.append("Annual family income cannot be negative.")
        if self.annual_income > 100000000:
            errors.append("Annual family income is unrealistically high. Please check the entered amount.")
        if self.marks_percentage is not None:
            if self.marks_percentage < 0 or self.marks_percentage > 100:
                errors.append("Academic score percentage must be between 0 and 100.")
        if not self.education_level:
            errors.append("Education level must be selected.")
        if not self.state:
            errors.append("Domicile state must be selected.")
        return errors

    def completeness_score(self) -> int:
        """Calculate profile completeness percentage."""
        fields = [
            bool(self.education_level),
            bool(self.degree),
            bool(self.year_of_study),
            bool(self.state and self.state != "Select State"),
            self.annual_income >= 0,
            bool(self.category),
            bool(self.gender),
            self.marks_percentage is not None and self.marks_percentage > 0,
        ]
        return int((sum(fields) / len(fields)) * 100)


@dataclass
class CriterionEvaluation:
    name: str
    status: str  # "MATCHED", "UNMET", "VERIFICATION_REQUIRED"
    detail: str
    required_value: Any = None
    provided_value: Any = None


@dataclass
class EligibilityResult:
    scheme_id: str
    scheme_name: str
    is_eligible: bool
    match_status: str  # "Eligible (High Match)", "Requires Verification", "Not Eligible"
    match_score_percentage: float
    matching_criteria: List[CriterionEvaluation] = field(default_factory=list)
    unmet_criteria: List[CriterionEvaluation] = field(default_factory=list)
    verification_required: List[CriterionEvaluation] = field(default_factory=list)
    summary_explanation: str = ""


@dataclass
class ScholarshipScheme:
    id: str
    name: str
    short_name: str
    ministry: str
    scheme_type: str
    portal_name: str
    official_portal_url: str
    guidelines_url: str
    last_verified_date: str
    verification_status: str
    application_cycle_note: str
    benefit_amount_display: str
    benefit_details: str
    eligibility_rules: Dict[str, Any]
    required_documents: List[str]
    verification_checklist: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScholarshipScheme":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            short_name=data.get("short_name", ""),
            ministry=data.get("ministry", ""),
            scheme_type=data.get("scheme_type", ""),
            portal_name=data.get("portal_name", ""),
            official_portal_url=data.get("official_portal_url", ""),
            guidelines_url=data.get("guidelines_url", ""),
            last_verified_date=data.get("last_verified_date", ""),
            verification_status=data.get("verification_status", "Unverified"),
            application_cycle_note=data.get("application_cycle_note", ""),
            benefit_amount_display=data.get("benefit_amount_display", ""),
            benefit_details=data.get("benefit_details", ""),
            eligibility_rules=data.get("eligibility_rules", {}),
            required_documents=data.get("required_documents", []),
            verification_checklist=data.get("verification_checklist", []),
        )
