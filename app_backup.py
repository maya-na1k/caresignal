from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

DATA_FILE = Path("care_entries.csv")

COLUMNS = [
    "Date",
    "Sleep Hours",
    "Mood",
    "Stress Level",
    "Medication Taken",
    "Nighttime Phone Use",
    "Notes",
    "Concern Score",
    "Concern Level",
]


def calculate_concern_score(
    sleep_hours: float,
    mood: int,
    stress_level: int,
    medication_taken: bool,
    nighttime_phone_use: bool,
) -> int:
    """Return a simple concern score. Higher means more caregiver attention may be helpful."""
    score = 0

    # Sleep: very low sleep is a stronger concern.
    if sleep_hours < 5:
        score += 2
    elif sleep_hours < 7:
        score += 1

    # Mood: 1 is very low, 5 is very positive.
    if mood <= 2:
        score += 2
    elif mood == 3:
        score += 1

    # Stress: 1 is low, 5 is high.
    if stress_level >= 4:
        score += 2
    elif stress_level == 3:
        score += 1

    # Missed medication can be important for caregivers to notice.
    if not medication_taken:
        score += 2

    # Nighttime phone use may be a sign of poor sleep routine or restlessness.
    if nighttime_phone_use:
        score += 1

    return score


def get_concern_level(score: int) -> str:
    """Convert the numeric score into a simple level."""
    if score <= 2:
        return "Low"
    if score <= 5:
        return "Medium"
    return "High"


def get_checklist(level: str) -> list[str]:
    """Return caregiver preparation steps based on the concern level."""
    if level == "Low":
        return [
            "Keep logging daily patterns.",
            "Maintain normal routines for sleep, meals, and medication.",
            "Check in with the person in a calm, supportive way.",
        ]

    if level == "Medium":
        return [
            "Review the last few days of sleep, mood, stress, and medication patterns.",
            "Ask what support would feel helpful today.",
            "Reduce avoidable stressors where possible.",
            "Make sure emergency contacts and care team information are easy to find.",
        ]

    return [
        "Stay calm and avoid escalating the situation.",
        "Do not leave the person unsupported if you are worried about immediate safety.",
        "Contact a trusted caregiver, clinician, or crisis resource if needed.",
        "Prepare key information: medications, recent behavior changes, triggers, and emergency contacts.",
        "If there is immediate danger, call emergency services right away.",
    ]


def load_data() -> pd.DataFrame:
    """Load existing entries from the CSV file, or create an empty table."""
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_entry(entry: dict) -> None:
    """Append one entry to the CSV file."""
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    df["Date"] = df["Date"].dt.date.astype(str)
    df.to_csv(DATA_FILE, index=False)


st.set_page_config(page_title="CareSignal", page_icon="💙", layout="wide")

st.title("CareSignal")
st.write(
    "A simple caregiver support tool for tracking daily behavioral patterns. "
    "CareSignal does not diagnose or predict a crisis. It only helps caregivers notice patterns and prepare support."
)

st.warning(
    "This app is not medical advice. If there is immediate danger or concern for someone's safety, contact emergency services or a crisis resource."
)

st.header("Daily Check-In")

with st.form("daily_entry_form"):
    entry_date = st.date_input("Date", value=date.today())
    sleep_hours = st.number_input("Sleep hours", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    mood = st.slider("Mood", min_value=1, max_value=5, value=3, help="1 = very low, 5 = very positive")
    stress_level = st.slider("Stress level", min_value=1, max_value=5, value=3, help="1 = low, 5 = high")
    medication_taken = st.checkbox("Medication taken", value=True)
    nighttime_phone_use = st.checkbox("Nighttime phone use", value=False)
    notes = st.text_area("Notes", placeholder="Optional notes about behavior, triggers, routines, or caregiver observations")

    submitted = st.form_submit_button("Save Entry")

if submitted:
    score = calculate_concern_score(
        sleep_hours=sleep_hours,
        mood=mood,
        stress_level=stress_level,
        medication_taken=medication_taken,
        nighttime_phone_use=nighttime_phone_use,
    )
    level = get_concern_level(score)

    new_entry = {
        "Date": entry_date.isoformat(),
        "Sleep Hours": sleep_hours,
        "Mood": mood,
        "Stress Level": stress_level,
        "Medication Taken": medication_taken,
        "Nighttime Phone Use": nighttime_phone_use,
        "Notes": notes,
        "Concern Score": score,
        "Concern Level": level,
    }

    save_entry(new_entry)
    st.success(f"Entry saved. Concern level: {level} | Score: {score}")

entries = load_data()

st.header("Past Entries")

if entries.empty:
    st.info("No entries yet. Add your first daily check-in above.")
else:
    st.dataframe(entries, use_container_width=True)

    latest_entry = entries.iloc[0]
    latest_score = int(latest_entry["Concern Score"])
    latest_level = latest_entry["Concern Level"]

    st.header("Current Concern Level")
    col1, col2 = st.columns(2)
    col1.metric("Concern Score", latest_score)
    col2.metric("Concern Level", latest_level)

    st.header("Concern Score Trend")
    chart_data = entries.copy()
    chart_data["Date"] = pd.to_datetime(chart_data["Date"])
    chart_data = chart_data.sort_values("Date")
    chart_data = chart_data.set_index("Date")
    st.line_chart(chart_data["Concern Score"])

    st.header("Caregiver Preparation Checklist")
    for item in get_checklist(latest_level):
        st.checkbox(item, value=False)
