from dagster import op, graph, ScheduleDefinition, Definitions, sensor, RunRequest
import subprocess
import os

@op
def scrape_telegram_op():
    """Run the Telegram scraping script/notebook."""
    # Replace with your actual scraping script path
    result = subprocess.run(["python", "src/scraping.py"], check=False)
    if result.returncode != 0:
        raise Exception("Telegram scraping failed")

@op
def load_raw_to_postgres_op():
    """Run the loader script to load raw JSON to Postgres."""
    result = subprocess.run(["python", "src/load_raw_to_postgres.py"], check=False)
    if result.returncode != 0:
        raise Exception("Loading raw data to Postgres failed")

@op
def run_dbt_op():
    """Run dbt transformations (dbt run)."""
    result = subprocess.run(["dbt", "run"], cwd="telegram_dbt", check=False)
    if result.returncode != 0:
        raise Exception("dbt run failed")

@op
def yolo_enrichment_op():
    """Run YOLO enrichment and load detections to Postgres."""
    # Run YOLO enrichment
    result1 = subprocess.run(["python", "src/yolo_enrichment.py"], check=False)
    if result1.returncode != 0:
        raise Exception("YOLO enrichment failed")
    # Load detections
    result2 = subprocess.run(["python", "src/load_yolo_detections_to_postgres.py"], check=False)
    if result2.returncode != 0:
        raise Exception("Loading YOLO detections to Postgres failed")

@graph
def telegram_data_pipeline():
    scrape_telegram_op()
    load_raw_to_postgres_op()
    run_dbt_op()
    yolo_enrichment_op()

# Create a job from the graph
telegram_data_job = telegram_data_pipeline.to_job()

daily_schedule = ScheduleDefinition(
    job=telegram_data_job,
    cron_schedule="0 2 * * *",  # Every day at 2 AM
)

@sensor(job=telegram_data_job)
def new_data_sensor(context):
    """Trigger the pipeline when new raw Telegram data is detected."""
    data_dir = os.path.join("data", "raw", "telegram_messages")
    if not os.path.exists(data_dir):
        return []
    # Look for any files in the directory tree
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            # You can add more logic here (e.g., only trigger on new files)
            context.log.info(f"Detected file: {file}")
            return [RunRequest(run_key=None, run_config={})]
    return []

defs = Definitions(
    jobs=[telegram_data_job],
    schedules=[daily_schedule],
    sensors=[new_data_sensor],
) 