"""Unit tests for scheme searching, filtering, and sorting."""

import pytest
from src.utils import load_schemes_data
from src.search_filter import filter_and_search_schemes


def test_search_by_keyword():
    schemes = load_schemes_data()
    
    # Search for Pragati
    results = filter_and_search_schemes(schemes, query="Pragati")
    assert len(results) >= 1
    assert any("pragati" in r["name"].lower() for r in results)

    # Search for non-existent term
    results_empty = filter_and_search_schemes(schemes, query="NonExistentSchemeXYZ")
    assert len(results_empty) == 0


def test_filter_by_scheme_type():
    schemes = load_schemes_data()
    
    state_schemes = filter_and_search_schemes(schemes, scheme_type="State Government")
    assert len(state_schemes) >= 1
    assert all(s["scheme_type"] == "State Government" for s in state_schemes)


def test_filter_by_gender():
    schemes = load_schemes_data()
    
    # Filter female-specific schemes
    female_schemes = filter_and_search_schemes(schemes, gender="Female")
    assert len(female_schemes) >= 1


def test_filter_by_category():
    schemes = load_schemes_data()
    
    sc_schemes = filter_and_search_schemes(schemes, category="Scheduled Caste (SC)")
    assert len(sc_schemes) >= 1


def test_filter_by_income():
    schemes = load_schemes_data()
    
    # User with 5 Lakh income should be excluded from schemes requiring <= 2 Lakh or 2.5 Lakh
    filtered = filter_and_search_schemes(schemes, max_income=500000.0)
    for s in filtered:
        income_cap = s.get("eligibility_rules", {}).get("max_annual_income")
        if income_cap is not None:
            assert income_cap >= 500000.0


def test_sort_alphabetical():
    schemes = load_schemes_data()
    sorted_schemes = filter_and_search_schemes(schemes, sort_by="Alphabetical (A-Z)")
    names = [s["name"] for s in sorted_schemes]
    assert names == sorted(names)
