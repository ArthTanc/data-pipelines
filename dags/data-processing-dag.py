from __future__ import annotations

import datetime
import os
import random

import polars as pl
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from faker import Faker

# Define file paths
BASE_DIR = "/opt/airflow/"  # Root for data and DAGs
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_FILE = os.path.join(DATA_DIR, "fake_employee_data.csv")
METRICS_FILE = os.path.join(DATA_DIR, "salary_metrics.csv")

# Ensure directories exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


# --- Task 1: Generate Fake Data ---
def _generate_and_save_data(**context):
    """Generates fake data and saves it to a CSV file."""
    fake = Faker()
    num_records = 1000
    data = []
    positions = ["Admin", "Manager", "Department Head", "Engineer", "Analyst"]

    print(f"Generating {num_records} fake employee records...")
    for _ in range(num_records):
        data.append(
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "position": random.choice(positions),
                "salary": round(random.uniform(40000, 180000), 2),
                "sex": random.choice(["Male", "Female"]),
            }
        )

    df = pl.DataFrame(data)
    output_filepath = context["params"]["output_filepath"]
    print(f"Saving data to {output_filepath}")
    df.write_csv(output_filepath)
    print("Data generation complete.")


# --- Task 2: Calculate Metrics ---
def _calculate_salary_metrics(**context):
    """Calculates salary metrics by position and sex."""
    input_filepath = context["params"]["input_filepath"]
    output_filepath = context["params"]["output_filepath"]

    print(f"Reading data from {input_filepath}")
    try:
        df = pl.scan_csv(input_filepath)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        raise  # Raise the exception to fail the task

    print(df.collect_schema())
    print("Calculating salary metrics by position and sex...")

    # Calculate average salary by position and sex
    avg_salary_by_position_sex = (
        df.group_by(["position", "sex"])
        .agg(pl.mean("salary").alias("average_salary"))
        .sort(["position", "sex"])
    )

    print(f"Saving metrics to {output_filepath}")
    avg_salary_by_position_sex.sink_csv(output_filepath)
    print("Metrics calculation complete.")


with DAG(
    dag_id="data_processing_pipeline",
    start_date=datetime.datetime(2023, 10, 26),
    schedule="@daily",
    catchup=False,
    tags=["data-processing", "fake-data", "metrics"],
    # Define default params that can be overridden by tasks
    params={
        "output_filepath": RAW_DATA_FILE,
        "input_filepath": RAW_DATA_FILE,
        "output_filepath_metrics": METRICS_FILE,
    },
) as dag:
    generate_data_task = PythonOperator(
        task_id="generate_fake_employee_data",
        python_callable=_generate_and_save_data,
        params={"output_filepath": RAW_DATA_FILE},
    )

    calculate_metrics_task = PythonOperator(
        task_id="calculate_salary_metrics",
        python_callable=_calculate_salary_metrics,
        params={
            "input_filepath": RAW_DATA_FILE,
            "output_filepath": METRICS_FILE,
        },
    )

    generate_data_task >> calculate_metrics_task
