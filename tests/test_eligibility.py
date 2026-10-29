"""Unit tests for deterministic eligibility rules engine."""

import pytest
from src.models import StudentProfile
from src.eligibility_engine import evaluate_eligibility, batch_evaluate_schemes
from src.utils import get_scheme_by_id, load_schemes_data


def test_pm_usp_csss_eligible():
    csss = get_scheme_by_id("pm-usp-csss")
    assert csss is not None

    # Student with income <= 4.5L, marks >= 80%, UG 1st year
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Sc (Bachelor of Science)",
        year_of_study="1st Year",
        state="Maharashtra",
        annual_income=300000.0,
        category="General / Open",
        gender="Male",
        marks_percentage=85.0
    )
    result = evaluate_eligibility(profile, csss)
    assert result.is_eligible is True
    assert result.match_status == "Eligible (High Match)"
    assert len(result.unmet_criteria) == 0
    assert any(c.name == "Annual Family Income" and c.status == "MATCHED" for c in result.matching_criteria)


def test_pm_usp_csss_ineligible_high_income():
    csss = get_scheme_by_id("pm-usp-csss")
    assert csss is not None

    # Income exceeds 4.5L ceiling
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        year_of_study="1st Year",
        annual_income=500000.0,
        marks_percentage=85.0
    )
    result = evaluate_eligibility(profile, csss)
    assert result.is_eligible is False
    assert result.match_status == "Not Eligible"
    assert any(c.name == "Annual Family Income" and c.status == "UNMET" for c in result.unmet_criteria)


def test_aicte_pragati_female_engineering_eligible():
    pragati = get_scheme_by_id("aicte-pragati-degree")
    assert pragati is not None

    # Girl student in 1st year B.Tech, income <= 8L
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        gender="Female",
        annual_income=400000.0,
        is_technical_course=True
    )
    result = evaluate_eligibility(profile, pragati)
    assert result.is_eligible is True
    assert result.match_status == "Eligible (High Match)"
    assert len(result.unmet_criteria) == 0


def test_aicte_pragati_ineligible_for_male():
    pragati = get_scheme_by_id("aicte-pragati-degree")
    assert pragati is not None

    # Male student
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        gender="Male",
        annual_income=400000.0,
        is_technical_course=True
    )
    result = evaluate_eligibility(profile, pragati)
    assert result.is_eligible is False
    assert any(c.name == "Gender Eligibility" and c.status == "UNMET" for c in result.unmet_criteria)


def test_aicte_saksham_pwd_requirement():
    saksham = get_scheme_by_id("aicte-saksham-degree")
    assert saksham is not None

    # Student without disability
    non_pwd_profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        annual_income=300000.0,
        is_pwd=False,
        is_technical_course=True
    )
    result_non_pwd = evaluate_eligibility(non_pwd_profile, saksham)
    assert result_non_pwd.is_eligible is False
    assert any(c.name == "Differently Abled (PwD) Status" and c.status == "UNMET" for c in result_non_pwd.unmet_criteria)

    # Student with certified disability
    pwd_profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        annual_income=300000.0,
        is_pwd=True,
        is_technical_course=True
    )
    result_pwd = evaluate_eligibility(pwd_profile, saksham)
    assert result_pwd.is_eligible is True
    assert any(c.name == "Differently Abled (PwD) Status" and c.status == "MATCHED" for c in result_pwd.matching_criteria)


def test_ishan_uday_domicile():
    ishan = get_scheme_by_id("ishan-uday-ugc")
    assert ishan is not None

    # Assam domicile student
    assam_profile = StudentProfile(
        education_level="Undergraduate (UG)",
        year_of_study="1st Year",
        state="Assam",
        annual_income=350000.0
    )
    result_assam = evaluate_eligibility(assam_profile, ishan)
    assert result_assam.is_eligible is True

    # Non-NER domicile student (e.g. Gujarat)
    gujarat_profile = StudentProfile(
        education_level="Undergraduate (UG)",
        year_of_study="1st Year",
        state="Gujarat",
        annual_income=350000.0
    )
    result_gujarat = evaluate_eligibility(gujarat_profile, ishan)
    assert result_gujarat.is_eligible is False
    assert any(c.name == "Domicile / State" and c.status == "UNMET" for c in result_gujarat.unmet_criteria)


def test_batch_evaluate_sorting():
    schemes = load_schemes_data()
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        state="Maharashtra",
        annual_income=200000.0,
        category="General / Open",
        gender="Female",
        is_pwd=False,
        is_minority=False,
        marks_percentage=85.0,
        is_technical_course=True
    )
    results = batch_evaluate_schemes(profile, schemes)
    assert len(results) == len(schemes)
    # The first item should be eligible
    assert results[0][1].is_eligible is True
