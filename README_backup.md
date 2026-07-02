# CareSignal

CareSignal is a simple Streamlit caregiver support tool for logging daily patterns and preparing caregiver support. It does not diagnose anyone or predict a crisis.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Test with sample data

To test the app with prefilled data, copy the sample CSV into the app's expected data file:

```bash
cp sample_care_entries.csv care_entries.csv
streamlit run app.py
```

The app will show past entries, the latest concern level, a concern score trend chart, and a caregiver preparation checklist.
