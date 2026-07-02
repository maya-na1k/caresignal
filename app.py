import json
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_FILE = Path("care_entries.csv")
CARE_PLAN_FILE = Path("care_plan.json")
SAMPLE_DATA_FILE = Path("sample_care_entries.csv")

ENTRY_COLUMNS = [
    "Date",
    "Sleep Hours",
    "Mood",
    "Stress Level",
    "Medication Taken",
    "Nighttime Phone Use",
    "Note Tags",
    "Notes",
    "Concern Score",
    "Concern Level",
]

TAG_OPTIONS = [
    "Agitation",
    "Confusion",
    "Withdrawal",
    "Missed medication",
    "Sleep disruption",
    "Unusual behavior",
    "Appetite change",
    "Social isolation",
    "Other",
]


def apply_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f8fafc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .hero-card {
            background: linear-gradient(135deg, #eef6ff 0%, #f8fbff 55%, #ffffff 100%);
            padding: 2.2rem;
            border-radius: 24px;
            border: 1px solid #dbeafe;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1.5rem;
        }

        .hero-title {
            font-size: 2.7rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.5rem;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #475569;
            max-width: 850px;
            line-height: 1.6;
            margin-bottom: 1.2rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-top: 1rem;
        }

        .pill {
            background-color: #ffffff;
            color: #1e3a8a;
            border: 1px solid #bfdbfe;
            padding: 0.45rem 0.75rem;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .section-card {
            background-color: #ffffff;
            padding: 1.4rem;
            border-radius: 18px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
            margin-bottom: 1rem;
        }

        .small-card-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }

        .small-card-text {
            font-size: 0.95rem;
            color: #475569;
            line-height: 1.5;
        }

        .low-badge {
            background-color: #dcfce7;
            color: #166534;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-weight: 700;
            display: inline-block;
        }

        .medium-badge {
            background-color: #fef9c3;
            color: #854d0e;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-weight: 700;
            display: inline-block;
        }

        .high-badge {
            background-color: #fee2e2;
            color: #991b1b;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            font-weight: 700;
            display: inline-block;
        }

        .disclaimer-box {
            background-color: #f1f5f9;
            color: #334155;
            padding: 1rem 1.2rem;
            border-radius: 16px;
            border-left: 5px solid #3b82f6;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stSidebar"] {
            background-color: #0f172a;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        .sidebar-note {
            font-size: 0.85rem;
            color: #cbd5e1;
            line-height: 1.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">CareSignal</div>
            <div class="hero-subtitle">
                A simple caregiver support tool for tracking daily wellness and behavioral observations.
                CareSignal helps families organize notes, notice repeated patterns, and prepare support information earlier.
            </div>
            <div class="pill-row">
                <span class="pill">Daily logs</span>
                <span class="pill">Concern levels</span>
                <span class="pill">Trend tracking</span>
                <span class="pill">Caregiver preparation</span>
                <span class="pill">Local storage</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_purpose_section():
    st.markdown("### Purpose of CareSignal")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-card-title">Organize observations</div>
                <div class="small-card-text">
                    Caregivers can record sleep, mood, stress, medication, nighttime phone use, tags, and notes in one place.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-card-title">Notice simple patterns</div>
                <div class="small-card-text">
                    The dashboard highlights recent changes and repeated patterns without making medical claims.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-card-title">Prepare support earlier</div>
                <div class="small-card-text">
                    The care plan and report help families keep important support details ready when they need them.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def concern_badge(concern_level):
    if concern_level == "Low concern":
        css_class = "low-badge"
    elif concern_level == "Medium concern":
        css_class = "medium-badge"
    else:
        css_class = "high-badge"

    return f'<span class="{css_class}">{concern_level}</span>'


def calculate_score(sleep_hours, mood, stress_level, medication_taken, nighttime_phone_use):
    score = 0

    if sleep_hours < 5:
        score += 2
    elif sleep_hours < 7:
        score += 1

    if mood <= 2:
        score += 2
    elif mood == 3:
        score += 1

    if stress_level >= 4:
        score += 2
    elif stress_level == 3:
        score += 1

    if medication_taken == "No":
        score += 2

    if nighttime_phone_use == "Yes":
        score += 1

    return score


def get_concern_level(score):
    if score <= 2:
        return "Low concern"
    if score <= 5:
        return "Medium concern"
    return "High concern"


def get_checklist(concern_level):
    if concern_level == "Low concern":
        return [
            "Continue logging daily observations.",
            "Look for small changes in sleep, mood, stress, and routine.",
            "Keep notes short and consistent.",
        ]

    if concern_level == "Medium concern":
        return [
            "Review recent notes and look for repeated patterns.",
            "Check whether sleep, stress, or medication changes may need attention.",
            "Consider sharing observations with a trusted support person.",
            "Prepare contact information in case extra support is needed.",
        ]

    return [
        "Review the recent pattern and caregiver notes carefully.",
        "Consider reaching out to a trusted professional or support person if concerned.",
        "Make sure emergency and family contact information is easy to access.",
        "Use the care plan to prepare calming strategies and next steps.",
        "If there is immediate danger, contact emergency services.",
    ]


def get_concern_explanation(concern_level):
    if concern_level == "Low concern":
        return "Recent entries look relatively stable."

    if concern_level == "Medium concern":
        return "Some recent observations may need attention."

    return "Several recent observations may be worth reviewing with a trusted support person."


def load_entries():
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=ENTRY_COLUMNS)

    df = pd.read_csv(DATA_FILE)

    for col in ENTRY_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[ENTRY_COLUMNS]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date")

    numeric_columns = ["Sleep Hours", "Mood", "Stress Level", "Concern Score"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_columns)
    return df


def save_entry(entry):
    df = load_entries()
    new_row = pd.DataFrame([entry])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    updated_df.to_csv(DATA_FILE, index=False)


def load_sample_data():
    """Copy sample_care_entries.csv into care_entries.csv, if it's safe to do so."""
    if not SAMPLE_DATA_FILE.exists():
        st.warning(
            "No sample data file was found (expected sample_care_entries.csv in the "
            "project folder), so nothing was loaded."
        )
        return

    existing_df = load_entries()
    if not existing_df.empty:
        st.warning(
            "Sample data was not loaded because care_entries.csv already has entries. "
            "Delete or rename care_entries.csv first if you want to start over with sample data."
        )
        return

    sample_df = pd.read_csv(SAMPLE_DATA_FILE)
    sample_df.to_csv(DATA_FILE, index=False)
    st.success(f"Loaded {len(sample_df)} sample entries into care_entries.csv.")
    st.rerun()


def load_care_plan():
    default_plan = {
        "Emergency contact": "",
        "Primary doctor or therapist": "",
        "Preferred hospital or clinic": "",
        "Medication list": "",
        "Known triggers": "",
        "Calming strategies": "",
        "Family contact": "",
        "Caregiver notes": "",
    }

    if not CARE_PLAN_FILE.exists():
        return default_plan

    try:
        saved_plan = json.loads(CARE_PLAN_FILE.read_text())
        default_plan.update(saved_plan)
        return default_plan
    except json.JSONDecodeError:
        return default_plan


def save_care_plan(plan):
    CARE_PLAN_FILE.write_text(json.dumps(plan, indent=2))


def get_recent_entries(df, days=7):
    if df.empty:
        return df

    end_date = df["Date"].max()
    start_date = end_date - timedelta(days=days - 1)
    return df[df["Date"] >= start_date]


def get_weekly_summary(df):
    recent_df = get_recent_entries(df, days=7)

    if recent_df.empty:
        return {
            "Average sleep": 0,
            "Average mood": 0,
            "Average stress": 0,
            "Missed medication days": 0,
            "High concern days": 0,
            "Average concern score": 0,
        }

    return {
        "Average sleep": round(recent_df["Sleep Hours"].mean(), 1),
        "Average mood": round(recent_df["Mood"].mean(), 1),
        "Average stress": round(recent_df["Stress Level"].mean(), 1),
        "Missed medication days": int((recent_df["Medication Taken"] == "No").sum()),
        "High concern days": int((recent_df["Concern Level"] == "High concern").sum()),
        "Average concern score": round(recent_df["Concern Score"].mean(), 1),
    }


def has_consecutive_yes(values, needed_count):
    streak = 0
    for value in values:
        if value == "Yes":
            streak += 1
            if streak >= needed_count:
                return True
        else:
            streak = 0
    return False


def get_pattern_flags(df):
    if df.empty:
        return []

    recent_df = get_recent_entries(df, days=7)
    flags = []

    low_sleep_days = int((recent_df["Sleep Hours"] < 5).sum())
    high_stress_days = int((recent_df["Stress Level"] >= 4).sum())
    missed_med_days = int((recent_df["Medication Taken"] == "No").sum())

    if low_sleep_days >= 2:
        flags.append("Sleep was below 5 hours on 2 or more recent days.")

    if high_stress_days >= 3:
        flags.append("Stress was 4 or higher on 3 or more recent days.")

    if missed_med_days > 1:
        flags.append("Medication was missed more than once in the recent 7-day period.")

    if len(recent_df) >= 2:
        latest_score = float(recent_df.iloc[-1]["Concern Score"])
        previous_score = float(recent_df.iloc[-2]["Concern Score"])
        if latest_score > previous_score:
            flags.append("The latest concern score increased compared to the previous entry.")

    if has_consecutive_yes(recent_df["Nighttime Phone Use"].tolist(), 3):
        flags.append("Nighttime phone use happened several days in a row.")

    if not flags:
        flags.append("No major repeated patterns were flagged from the recent entries.")

    return flags


def get_what_changed(df):
    if len(df) < 2:
        return ["Add at least two entries to compare what changed."]

    latest = df.iloc[-1]
    previous = df.iloc[-2]
    changes = []

    sleep_change = float(latest["Sleep Hours"]) - float(previous["Sleep Hours"])
    if sleep_change <= -1:
        changes.append(f"Sleep decreased by {abs(round(sleep_change, 1))} hours compared to the previous entry.")
    elif sleep_change >= 1:
        changes.append(f"Sleep increased by {round(sleep_change, 1)} hours compared to the previous entry.")

    if int(latest["Stress Level"]) > int(previous["Stress Level"]):
        changes.append(f"Stress increased from {int(previous['Stress Level'])} to {int(latest['Stress Level'])}.")
    elif int(latest["Stress Level"]) < int(previous["Stress Level"]):
        changes.append(f"Stress decreased from {int(previous['Stress Level'])} to {int(latest['Stress Level'])}.")

    if int(latest["Mood"]) > int(previous["Mood"]):
        changes.append(f"Mood increased from {int(previous['Mood'])} to {int(latest['Mood'])}.")
    elif int(latest["Mood"]) < int(previous["Mood"]):
        changes.append(f"Mood decreased from {int(previous['Mood'])} to {int(latest['Mood'])}.")

    if latest["Medication Taken"] == "No" and previous["Medication Taken"] == "Yes":
        changes.append("Medication was missed in the latest entry.")

    if latest["Nighttime Phone Use"] == "Yes" and previous["Nighttime Phone Use"] == "No":
        changes.append("Nighttime phone use was reported in the latest entry.")

    latest_score = int(latest["Concern Score"])
    previous_score = int(previous["Concern Score"])
    if latest_score > previous_score:
        changes.append(f"Concern score increased from {previous_score} to {latest_score}.")
    elif latest_score < previous_score:
        changes.append(f"Concern score decreased from {previous_score} to {latest_score}.")

    if not changes:
        changes.append("No major changes were found compared to the previous entry.")

    return changes


def get_common_tags(df):
    all_tags = []

    for tag_string in df["Note Tags"].dropna():
        tags = [tag.strip() for tag in str(tag_string).split(",") if tag.strip()]
        all_tags.extend(tags)

    return Counter(all_tags).most_common(5)


def build_txt_report(df, care_plan):
    if df.empty:
        return "No CareSignal entries are available yet."

    latest = df.iloc[-1]
    recent_df = get_recent_entries(df, days=7)
    summary = get_weekly_summary(df)
    flags = get_pattern_flags(df)
    common_tags = get_common_tags(df)
    checklist = get_checklist(latest["Concern Level"])

    lines = []
    lines.append("CareSignal Caregiver Report")
    lines.append("=" * 32)
    lines.append("")
    lines.append("Purpose:")
    lines.append("This report is for caregiver organization and preparation only.")
    lines.append("It does not diagnose, predict, detect, or treat any condition.")
    lines.append("")
    lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    lines.append("")
    lines.append("Latest Entry:")
    lines.append(f"- Date: {latest['Date'].date()}")
    lines.append(f"- Concern score: {latest['Concern Score']}")
    lines.append(f"- Concern level: {latest['Concern Level']}")
    lines.append(f"- Sleep hours: {latest['Sleep Hours']}")
    lines.append(f"- Mood: {latest['Mood']}")
    lines.append(f"- Stress level: {latest['Stress Level']}")
    lines.append(f"- Medication taken: {latest['Medication Taken']}")
    lines.append(f"- Nighttime phone use: {latest['Nighttime Phone Use']}")
    lines.append("")
    lines.append("Recent 7-Day Summary:")
    for key, value in summary.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("Pattern Flags:")
    for flag in flags:
        lines.append(f"- {flag}")
    lines.append("")
    lines.append("Common Note Tags:")
    if common_tags:
        for tag, count in common_tags:
            lines.append(f"- {tag}: {count}")
    else:
        lines.append("- No tags recorded yet.")
    lines.append("")
    lines.append("Caregiver Preparation Checklist:")
    for item in checklist:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Care Plan:")
    for key, value in care_plan.items():
        clean_value = value if value else "Not provided"
        lines.append(f"- {key}: {clean_value}")
    lines.append("")
    lines.append("Recent Entries:")
    for _, row in recent_df.iterrows():
        lines.append(
            f"- {row['Date'].date()}: score {row['Concern Score']} "
            f"({row['Concern Level']}), sleep {row['Sleep Hours']}, "
            f"mood {row['Mood']}, stress {row['Stress Level']}"
        )
    lines.append("")
    lines.append("Safety note:")
    lines.append("If there is immediate danger, contact emergency services or a trusted professional.")

    return "\n".join(lines)


def show_disclaimer():
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>Privacy and safety note:</strong>
            CareSignal stores information locally on your device. This tool is for caregiver organization and preparation only.
            It does not diagnose, predict, detect, or treat any condition. If there is immediate danger, contact emergency
            services or a trusted professional.
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_daily_log():
    st.header("Daily Log")
    st.write("Record one daily observation. The goal is to keep notes simple, consistent, and useful for caregivers.")

    with st.form("daily_log_form"):
        col1, col2 = st.columns(2)

        with col1:
            entry_date = st.date_input("Date", value=date.today())
            sleep_hours = st.number_input("Sleep hours", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
            mood = st.slider("Mood, 1 = lowest and 5 = highest", min_value=1, max_value=5, value=3)
            stress_level = st.slider("Stress level, 1 = lowest and 5 = highest", min_value=1, max_value=5, value=3)

        with col2:
            medication_taken = st.radio("Medication taken?", ["Yes", "No"], horizontal=True)
            nighttime_phone_use = st.radio("Nighttime phone use?", ["No", "Yes"], horizontal=True)
            note_tags = st.multiselect("Caregiver note tags", TAG_OPTIONS)
            notes = st.text_area("Notes", placeholder="Example: Slept poorly, seemed withdrawn after dinner, refused walk.")

        submitted = st.form_submit_button("Save daily log")

    if submitted:
        score = calculate_score(
            sleep_hours=sleep_hours,
            mood=mood,
            stress_level=stress_level,
            medication_taken=medication_taken,
            nighttime_phone_use=nighttime_phone_use,
        )
        concern_level = get_concern_level(score)

        entry = {
            "Date": pd.to_datetime(entry_date),
            "Sleep Hours": sleep_hours,
            "Mood": mood,
            "Stress Level": stress_level,
            "Medication Taken": medication_taken,
            "Nighttime Phone Use": nighttime_phone_use,
            "Note Tags": ", ".join(note_tags),
            "Notes": notes,
            "Concern Score": score,
            "Concern Level": concern_level,
        }

        save_entry(entry)

        st.success("Daily log saved.")
        col1, col2 = st.columns(2)
        col1.metric("Concern score", score)
        with col2:
            st.write("Concern level")
            st.markdown(concern_badge(concern_level), unsafe_allow_html=True)
        st.caption(get_concern_explanation(concern_level))

        st.subheader("Caregiver checklist")
        for item in get_checklist(concern_level):
            st.write(f"- {item}")


def page_dashboard():
    st.header("Dashboard")
    df = load_entries()

    if df.empty:
        st.warning("No entries yet. Add a daily log first.")
        return

    latest = df.iloc[-1]
    summary = get_weekly_summary(df)

    st.subheader("Latest overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest concern score", int(latest["Concern Score"]))
    with col2:
        st.write("Latest concern level")
        st.markdown(concern_badge(latest["Concern Level"]), unsafe_allow_html=True)
        st.caption(get_concern_explanation(latest["Concern Level"]))
    col3.metric("Latest log date", latest["Date"].date().strftime("%Y-%m-%d"))

    st.subheader("Recent 7-day summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg sleep", summary["Average sleep"])
    c2.metric("Avg mood", summary["Average mood"])
    c3.metric("Avg stress", summary["Average stress"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Missed medication days", summary["Missed medication days"])
    c5.metric("High concern days", summary["High concern days"])
    c6.metric("Avg concern score", summary["Average concern score"])

    left, right = st.columns(2)

    with left:
        st.subheader("Pattern flags")
        for flag in get_pattern_flags(df):
            st.write(f"- {flag}")

    with right:
        st.subheader("What changed?")
        for change in get_what_changed(df):
            st.write(f"- {change}")

    st.subheader("Recent entries")
    display_df = df.sort_values("Date", ascending=False).head(10).copy()
    display_df["Date"] = display_df["Date"].dt.date
    st.dataframe(display_df, use_container_width=True)


def page_trends():
    st.header("Trends")
    df = load_entries()

    if df.empty:
        st.warning("No entries yet. Add a daily log first.")
        return

    trend_df = df.sort_values("Date").set_index("Date")

    st.subheader("Concern score over time")
    st.line_chart(trend_df["Concern Score"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sleep hours over time")
        st.line_chart(trend_df["Sleep Hours"])

        st.subheader("Mood over time")
        st.line_chart(trend_df["Mood"])

    with col2:
        st.subheader("Stress level over time")
        st.line_chart(trend_df["Stress Level"])

        st.subheader("How the score works")
        st.write(
            "The score uses simple rules based on sleep, mood, stress, medication, "
            "and nighttime phone use. It is not a medical score. It is only meant to "
            "help caregivers organize observations."
        )

        with st.expander("View scoring rules"):
            st.write("- Sleep below 5 hours: +2")
            st.write("- Sleep below 7 hours: +1")
            st.write("- Mood of 1 or 2: +2")
            st.write("- Mood of 3: +1")
            st.write("- Stress of 4 or 5: +2")
            st.write("- Stress of 3: +1")
            st.write("- Medication not taken: +2")
            st.write("- Nighttime phone use: +1")

    st.subheader("Most common note tags")
    common_tags = get_common_tags(df)
    if common_tags:
        tag_df = pd.DataFrame(common_tags, columns=["Tag", "Count"]).set_index("Tag")
        st.bar_chart(tag_df)
    else:
        st.write("No note tags have been recorded yet. Tags added on the Daily Log page will show up here.")


def page_care_plan():
    st.header("Caregiver Preparation Plan")
    st.write("Keep important support information in one place. This is stored locally on your device.")

    care_plan = load_care_plan()

    with st.form("care_plan_form"):
        col1, col2 = st.columns(2)

        updated_plan = {}

        with col1:
            updated_plan["Emergency contact"] = st.text_area("Emergency contact", value=care_plan["Emergency contact"])
            updated_plan["Primary doctor or therapist"] = st.text_area(
                "Primary doctor or therapist", value=care_plan["Primary doctor or therapist"]
            )
            updated_plan["Preferred hospital or clinic"] = st.text_area(
                "Preferred hospital or clinic", value=care_plan["Preferred hospital or clinic"]
            )
            updated_plan["Medication list"] = st.text_area("Medication list", value=care_plan["Medication list"])

        with col2:
            updated_plan["Known triggers"] = st.text_area("Known triggers", value=care_plan["Known triggers"])
            updated_plan["Calming strategies"] = st.text_area("Calming strategies", value=care_plan["Calming strategies"])
            updated_plan["Family contact"] = st.text_area("Family contact", value=care_plan["Family contact"])
            updated_plan["Caregiver notes"] = st.text_area("Caregiver notes", value=care_plan["Caregiver notes"])

        submitted = st.form_submit_button("Save care plan")

    if submitted:
        save_care_plan(updated_plan)
        st.success("Care plan saved locally.")

    st.subheader("Current checklist based on latest concern level")
    df = load_entries()

    if df.empty:
        st.write("Add a daily log to generate a checklist.")
    else:
        latest_level = df.iloc[-1]["Concern Level"]
        st.markdown(concern_badge(latest_level), unsafe_allow_html=True)
        for item in get_checklist(latest_level):
            st.write(f"- {item}")


def page_export_report():
    st.header("Export Report")
    df = load_entries()
    care_plan = load_care_plan()

    if df.empty:
        st.warning("No entries yet. Add a daily log first.")
        return

    report_text = build_txt_report(df, care_plan)

    st.write(
        "Download a simple text report that summarizes recent observations, pattern flags, "
        "and caregiver preparation details."
    )
    st.download_button(
        label="Download caregiver report",
        data=report_text,
        file_name="caresignal_caregiver_report.txt",
        mime="text/plain",
    )

    with st.expander("Preview report"):
        st.text(report_text)


def page_about():
    st.header("About CareSignal")

    st.write(
        "CareSignal is a simple caregiver support tool. It helps families organize daily "
        "behavioral and wellness observations before concerns become harder to communicate."
    )

    show_purpose_section()

    st.subheader("What CareSignal does")
    st.write("- Saves daily caregiver observations locally.")
    st.write("- Calculates a simple concern level using transparent rules.")
    st.write("- Shows trends and recent patterns.")
    st.write("- Creates a caregiver preparation checklist and report.")

    st.subheader("What CareSignal does not do")
    st.write("- It does not diagnose any condition.")
    st.write("- It does not predict a crisis.")
    st.write("- It does not replace professional support.")
    st.write("- It does not provide medical advice.")

    show_disclaimer()


def main():
    st.set_page_config(page_title="CareSignal", page_icon="💙", layout="wide")
    apply_custom_css()

    with st.sidebar:
        st.markdown("## CareSignal")
        st.markdown(
            """
            <div class="sidebar-note">
            A local caregiver observation tool for daily logs, trends, preparation, and reports.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Home",
                "Daily Log",
                "Dashboard",
                "Trends",
                "Care Plan",
                "Export Report",
                "About",
            ],
        )

        st.divider()
        st.markdown("### Local storage")
        st.markdown(
            f"""
            <div class="sidebar-note">
            Entries: <code>{DATA_FILE}</code><br>
            Care plan: <code>{CARE_PLAN_FILE}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if page == "Home":
        show_hero()
        show_purpose_section()

        st.subheader("Start here")
        st.write(
            "Use the Daily Log page to enter observations. Then use the Dashboard and Trends pages "
            "to review recent changes. The Care Plan page stores important support information, and "
            "the Export Report page creates a simple downloadable summary."
        )

        st.subheader("Try it with sample data")
        st.write(
            "New to CareSignal? Load a few sample daily logs to see how the dashboard, trends, "
            "and report look with real entries."
        )
        if st.button("Load sample data"):
            load_sample_data()

        show_disclaimer()

    elif page == "Daily Log":
        show_hero()
        page_daily_log()
    elif page == "Dashboard":
        show_hero()
        page_dashboard()
    elif page == "Trends":
        show_hero()
        page_trends()
    elif page == "Care Plan":
        show_hero()
        page_care_plan()
    elif page == "Export Report":
        show_hero()
        page_export_report()
    else:
        show_hero()
        page_about()


if __name__ == "__main__":
    main()