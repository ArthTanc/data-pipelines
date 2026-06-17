# Plan: Run Airflow DAG Tasks on Minikube via KubernetesPodOperator

## Overview

Airflow runs in Docker (existing setup), tasks execute as Kubernetes pods in Minikube.

---

## Steps

### 1. Start Minikube

```bash
minikube start --cpus=2 --memory=4096
```

### 2. Create task-runner script

**New file: `scripts/run_task.py`**

A standalone CLI entry point containing the logic from:
- `_generate_and_save_data` → command `generate-data`
- `_calculate_salary_metrics_duckdb` → command `calculate-metrics`

Accepts `--output` / `--input` file path arguments.

### 3. Create task-runner Docker image

**New file: `Dockerfile.task-runner`**

- Base: `python:3.12-slim`
- Install `faker` + `duckdb`
- Copy `scripts/` into the image

Build and load into Minikube:

```bash
docker build -t data-pipeline-task-runner -f Dockerfile.task-runner .
minikube image load data-pipeline-task-runner
```

### 4. Add kubernetes provider to Airflow

**File to modify: `pyproject.toml`**

Add to `dependencies`:
```
"apache-airflow-providers-cncf-kubernetes"
```

Rebuild Airflow image:
```bash
docker compose build
```

### 5. Give Airflow container access to Minikube API

**File to modify: `docker-compose.yaml`**

Add volume mount:
```yaml
- ~/.kube:/home/airflow/.kube:ro
```

Fix kubeconfig server address to use Minikube's IP (not `127.0.0.1`):
```bash
minikube ip
# Update ~/.kube/config server entry to the returned IP
```

### 6. Mount host directory for cross-task file sharing

Start background mount:
```bash
minikube mount ./task-outputs:/opt/airflow/task-outputs &
```

### 7. Rewrite the DAG

**File to modify: `dags/data-processing-dag.py`**

Replace `PythonOperator` with `KubernetesPodOperator`:

```python
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

generate_data_task = KubernetesPodOperator(
    task_id="generate_fake_employee_data",
    namespace="default",
    image="data-pipeline-task-runner:latest",
    cmds=["python", "/scripts/run_task.py"],
    arguments=["generate-data", "--output", "/opt/airflow/task-outputs/fake_employee_data.csv"],
    name="generate-fake-data",
    config_file="/home/airflow/.kube/config",
    in_cluster=False,
    is_delete_operator_pod=True,
    get_logs=True,
    volumes=[...],  # hostPath for task-outputs
    volume_mounts=[...],
)
```

Same pattern for `calculate_salary_metrics` task (reads input CSV, writes metrics CSV).

Both pods mount `/opt/airflow/task-outputs` as `hostPath` (bridged via `minikube mount`).

### 8. Rebuild and test

```bash
make build
```

Trigger the DAG from the Airflow UI, watch pods:
```bash
kubectl get pods -w
```
