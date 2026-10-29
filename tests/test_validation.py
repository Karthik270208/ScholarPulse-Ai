"""Unit tests for student profile input validation and completeness calculations."""

import pytest
from src.models import StudentProfile


def test_valid_student_profile():
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        year_of_study="1st Year",
        state="Maharashtra",
        annual_income=250000.0,
        category="General / Open",
        gender="Female",
        is_pwd=False,
        is_minority=False,
        marks_percentage=85.0
    )
    errors = profile.validate()
    assert len(errors) == 0
    assert profile.completeness_score() == 100


def test_negative_income_validation():
    profile = StudentProfile(annual_income=-50000.0)
    errors = profile.validate()
    assert any("negative" in err.lower() for err in errors)


def test_unrealistic_income_validation():
    profile = StudentProfile(annual_income=999999999.0)
    errors = profile.validate()
    assert any("unrealistically high" in err.lower() for err in errors)


def test_invalid_marks_percentage_validation():
    profile_low = StudentProfile(marks_percentage=-5.0)
    errors_low = profile_low.validate()
    assert any("between 0 and 100" in err for err in errors_low)

    profile_high = StudentProfile(marks_percentage=105.0)
    errors_high = profile_high.validate()
    assert any("between 0 and 100" in err for err in errors_high)


def test_missing_state_validation():
    profile = StudentProfile(state="")
    errors = profile.validate()
    assert any("state" in err.lower() for err in errors)
