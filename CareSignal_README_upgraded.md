# CareSignal

CareSignal is a simple caregiver support tool that helps families organize daily behavioral and wellness observations.

It is not a medical tool. It does not diagnose, predict, detect, or treat any condition. The goal is to help caregivers track observations, notice simple patterns, and prepare support information earlier.

## Problem Statement

Caregivers often notice small day-to-day changes, but those observations can be scattered across memory, texts, notebooks, or conversations. CareSignal provides one simple place to record daily observations and turn them into a basic concern level, trend view, checklist, and caregiver preparation report.

## Features

- Daily caregiver log
- Local CSV storage
- Simple concern score
- Low, medium, and high concern levels
- Dashboard with weekly summary metrics
- Trend charts over time
- Pattern flags
- “What changed?” insights
- Caregiver note tags
- Caregiver preparation plan
- Downloadable text report
- Privacy and safety disclaimer

## Tech Stack

- Python
- Streamlit
- Pandas
- Local CSV file storage
- Local JSON file storage for care plan

## How to Run Locally

1. Clone the repository.

```bash
git clone https://github.com/YOUR-USERNAME/caresignal.git
cd caresignal
```

2. Install requirements.

```bash
pip install -r requirements.txt
```

3. Run the app.

```bash
streamlit run app.py
```

## Requirements

```txt
streamlit
pandas
```

## Sample Data

You can test the app by manually entering daily logs or by adding a sample `care_entries.csv` file with these columns:

- Date
- Sleep Hours
- Mood
- Stress Level
- Medication Taken
- Nighttime Phone Use
- Note Tags
- Notes
- Concern Score
- Concern Level

## Scoring Logic

Sleep:
- Sleep below 5 hours: +2
- Sleep below 7 hours: +1

Mood:
- Mood of 1 or 2: +2
- Mood of 3: +1

Stress:
- Stress of 4 or 5: +2
- Stress of 3: +1

Medication:
- Medication not taken: +2

Nighttime phone use:
- Nighttime phone use reported: +1

Concern level:
- 0 to 2: Low concern
- 3 to 5: Medium concern
- 6 or higher: High concern

## Ethical Disclaimer

CareSignal stores information locally on your device. This tool is for caregiver organization and preparation only. It does not diagnose, predict, detect, or treat any condition. If there is immediate danger, contact emergency services or a trusted professional.

## Future Improvements

- Add PDF report export
- Add SQLite storage
- Add user authentication
- Add encrypted local storage
- Add reminders
- Add multi-caregiver sharing
- Add unit tests for scoring logic
- Add configurable scoring rules
- Deploy with Streamlit Community Cloud
