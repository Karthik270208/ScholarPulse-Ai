"""Unit tests for AI advisor, retrieval, and grounded demo mode."""

import pytest
from src.ai_advisor import retrieve_relevant_context, ask_scholar_bot, generate_grounded_demo_response
from src.models import StudentProfile


def test_retrieval_relevance_girls():
    matches = retrieve_relevant_context("scholarships for girls in engineering")
    assert len(matches) > 0
    top_ids = [m["id"] for m in matches]
    assert "aicte-pragati-degree" in top_ids


def test_retrieval_relevance_sc_st():
    matches = retrieve_relevant_context("post matric scholarship for SC students")
    assert len(matches) > 0
    top_ids = [m["id"] for m in matches]
    assert "pms-sc-central" in top_ids


def test_ask_scholar_bot_demo_mode():
    profile = StudentProfile(
        education_level="Undergraduate (UG)",
        degree="B.Tech / B.E. (Engineering)",
        gender="Female"
    )
    res = ask_scholar_bot("What scholarships are available for girl students?", profile)
    assert "answer" in res
    assert len(res["answer"]) > 50
    assert "sources" in res
    assert len(res["sources"]) > 0


def test_dual_scholarship_query_explanation():
    res = ask_scholar_bot("Can I apply for multiple scholarships at once?")
    assert "multiple" in res["answer"].lower() or "prohibition" in res["answer"].lower() or "national scholarship portal" in res["answer"].lower()


def test_bank_npci_query_explanation():
    res = ask_scholar_bot("What is NPCI mapping and Aadhaar seeding?")
    assert "npci" in res["answer"].lower() or "direct benefit transfer" in res["answer"].lower()
