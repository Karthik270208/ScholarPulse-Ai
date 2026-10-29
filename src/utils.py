"""Utility functions and formatting helpers for ScholarGuide AI."""

import json
import os
from typing import List, Dict, Any
from pathlib import Path


def format_inr(amount: float) -> str:
    """Format a number into Indian Rupee (INR) representation with lakhs/crores formatting."""
    try:
        val = int(round(amount))
        if val < 0:
            return f"-₹{abs(val):,}"
        
        # Standard Indian numbering system (xx,xx,xxx)
        s = str(val)
        if len(s) <= 3:
            return f"₹{s}"
        
        last_three = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
        return f"₹{formatted}"
    except (ValueError, TypeError):
        return f"₹{amount}"


def get_income_bracket_label(amount: float) -> str:
    """Return a human-readable income bracket label."""
    if amount <= 150000:
        return "Below ₹1.5 Lakh/year"
    elif amount <= 250000:
        return "₹1.5 Lakh - ₹2.5 Lakh/year"
    elif amount <= 450000:
        return "₹2.5 Lakh - ₹4.5 Lakh/year"
    elif amount <= 800000:
        return "₹4.5 Lakh - ₹8.0 Lakh/year"
    else:
        return "Above ₹8.0 Lakh/year"


def load_schemes_data() -> List[Dict[str, Any]]:
    """Load the curated schemes database from data/schemes_data.json."""
    current_dir = Path(__file__).resolve().parent.parent
    data_path = current_dir / "data" / "schemes_data.json"
    
    if not data_path.exists():
        # Fallback to local data folder
        data_path = Path("data") / "schemes_data.json"
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_scheme_by_id(scheme_id: str) -> Dict[str, Any] | None:
    """Find a specific scheme by its ID."""
    schemes = load_schemes_data()
    for s in schemes:
        if s.get("id") == scheme_id:
            return s
    return None
