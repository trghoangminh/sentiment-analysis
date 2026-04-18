import pandas as pd
from sqlalchemy import create_engine
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TextOverviewPreset
from evidently.ui.workspace import Workspace
import os

# Connect to Database (Container connection)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://sentiment_user:sentiment_pass@localhost:5432/sentiment_db")
engine = create_engine(DATABASE_URL)

print("Fetching Current Data from Postgres...")
try:
    current_df = pd.read_sql("SELECT text, sentiment as prediction FROM predictions", con=engine)
except Exception as e:
    print("Failed to fetch data or no table found. Have you tested the API yet?", e)
    exit(1)

if current_df.empty:
    print("Not enough user traffic to generate drift reports. Go play with the API first!")
    exit(0)

print("Fetching Reference Data...")
ref_path = "../data/processed/sarcasm_dataset.csv"
if not os.path.exists(ref_path):
    # try full path backup
    ref_path = "/workspace/data/processed/sarcasm_dataset.csv"

ref_df = pd.read_csv(ref_path)

# Evidently requires the reference to have 'prediction' too if we evaluate Model Quality, 
# But for Data Drift of Text, we just need the 'text' columns. We map 'text' as a categorical/text feature.
ref_df = ref_df.rename(columns={"text": "text"})

print("Generating Data Drift Report...")
text_drift_report = Report(metrics=[
    DataDriftPreset(),
])

text_drift_report.run(reference_data=ref_df[['text']], current_data=current_df[['text']])

# Create or connect to the workspace mapped from docker-compose
ws = Workspace.create("/workspace/evidently_workspace")
project = ws.get_project("48c66e2c-29ea-4c54-94b2-4d2fb2df0823") # check if arbitrary ID exists

if project is None:
    project = ws.create_project("Sentiment Sarcasm Monitoring")
    project.description = "Text Data Drift tracking for Sentiment MLOps Pipeline"
    project.save()

ws.add_report(project.id, text_drift_report)
print("SUCCESS! Drift Report uploaded to Evidently UI Database (evidently_workspace). Check your localhost:8001!")
