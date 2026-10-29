"""Search and filtering utilities for scholarship schemes."""

from typing import List, Dict, Any, Optional


def filter_and_search_schemes(
    schemes: List[Dict[str, Any]],
    query: str = "",
    scheme_type: str = "All",
    state: str = "All",
    category: str = "All",
    gender: str = "All",
    education_level: str = "All",
    max_income: Optional[float] = None,
    sort_by: str = "Relevance / Name"
) -> List[Dict[str, Any]]:
    """Filter and search scholarship schemes based on student-selected criteria."""
    filtered = []
    
    q_clean = query.strip().lower()

    for scheme in schemes:
        rules = scheme.get("eligibility_rules", {})
        
        # 1. Text Search Query
        if q_clean:
            searchable_text = " ".join([
                scheme.get("name", ""),
                scheme.get("short_name", ""),
                scheme.get("ministry", ""),
                scheme.get("portal_name", ""),
                scheme.get("benefit_details", ""),
                " ".join(rules.get("other_conditions", [])),
                " ".join(scheme.get("required_documents", []))
            ]).lower()
            if q_clean not in searchable_text:
                continue

        # 2. Scheme Type Filter
        if scheme_type != "All":
            if scheme.get("scheme_type") != scheme_type:
                continue

        # 3. State / Domicile Filter
        if state != "All":
            domicile_states = rules.get("domicile_states", ["All India / Central"])
            if "All India / Central" not in domicile_states and state not in domicile_states:
                continue

        # 4. Social Category Filter
        if category != "All":
            target_cats = rules.get("target_categories", ["All"])
            if "All" not in target_cats and category not in target_cats:
                continue

        # 5. Gender Filter
        if gender != "All":
            target_genders = rules.get("target_genders", ["All"])
            if "All" not in target_genders and gender not in target_genders:
                continue

        # 6. Education Level Filter
        if education_level != "All":
            edu_levels = rules.get("education_levels", [])
            if edu_levels and education_level not in edu_levels:
                continue

        # 7. Max Income Filter
        if max_income is not None and max_income > 0:
            scheme_income_cap = rules.get("max_annual_income")
            if scheme_income_cap is not None and scheme_income_cap < max_income:
                # If scheme requires income below X, and user's income is higher than that cap, exclude
                continue

        filtered.append(scheme)

    # Sorting
    if sort_by == "Alphabetical (A-Z)":
        filtered.sort(key=lambda s: s.get("name", ""))
    elif sort_by == "Scheme Type":
        filtered.sort(key=lambda s: s.get("scheme_type", ""))
    elif sort_by == "Last Verified Date":
        filtered.sort(key=lambda s: s.get("last_verified_date", ""), reverse=True)
    elif sort_by == "Benefit Amount":
        # Sort by length or estimated ceiling if available
        filtered.sort(key=lambda s: s.get("benefit_amount_display", ""), reverse=True)

    return filtered
