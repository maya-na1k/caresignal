"""Tests for CareSignal's concern-score scoring logic.

These tests import directly from app.py. That works because app.py only
calls Streamlit functions (st.something) *inside* page functions and main(),
never at the top level of the file, so importing it does not try to launch
a Streamlit app or require a browser/session.

Run these tests from the project's root folder (the one that contains
app.py) with:

    pytest
"""

import sys
from pathlib import Path

# Make sure Python can find app.py, which lives one folder above tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import calculate_score, get_concern_level


def test_low_concern_example():
    # Good sleep, good mood, low stress, medication taken, no nighttime phone use.
    score = calculate_score(
        sleep_hours=8,
        mood=5,
        stress_level=1,
        medication_taken="Yes",
        nighttime_phone_use="No",
    )
    assert score == 0
    assert get_concern_level(score) == "Low concern"


def test_medium_concern_example():
    # A bit short on sleep, mood and stress right in the middle.
    score = calculate_score(
        sleep_hours=6,
        mood=3,
        stress_level=3,
        medication_taken="Yes",
        nighttime_phone_use="No",
    )
    assert score == 3
    assert get_concern_level(score) == "Medium concern"


def test_high_concern_example():
    # Low sleep, low mood, high stress, missed medication, nighttime phone use.
    score = calculate_score(
        sleep_hours=4,
        mood=1,
        stress_level=5,
        medication_taken="No",
        nighttime_phone_use="Yes",
    )
    assert score == 9
    assert get_concern_level(score) == "High concern"


def test_missed_medication_adds_two_points():
    took_medication = calculate_score(
        sleep_hours=8,
        mood=5,
        stress_level=1,
        medication_taken="Yes",
        nighttime_phone_use="No",
    )
    missed_medication = calculate_score(
        sleep_hours=8,
        mood=5,
        stress_level=1,
        medication_taken="No",
        nighttime_phone_use="No",
    )
    assert missed_medication == took_medication + 2


def test_nighttime_phone_use_adds_one_point():
    no_phone_use = calculate_score(
        sleep_hours=8,
        mood=5,
        stress_level=1,
        medication_taken="Yes",
        nighttime_phone_use="No",
    )
    with_phone_use = calculate_score(
        sleep_hours=8,
        mood=5,
        stress_level=1,
        medication_taken="Yes",
        nighttime_phone_use="Yes",
    )
    assert with_phone_use == no_phone_use + 1