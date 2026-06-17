# Project: Airflow in Docker

## Concept

The goal is simple: **understand what Airflow actually is by running it yourself**, rather than just using a managed version someone else configured.

I'll spin up Airflow inside a Docker container, understand its components, and prove it works by writing and running a minimal DAG. No DBT, no Kubernetes, no orchestration complexity — just Docker and Airflow talking to each other.

This is a deliberately scoped-down first step. The point is not to build something impressive, but to build something that *works* and that I *understand entirely*.

---

## What I want to learn

- What Docker is doing when you "run" a service (volumes, ports, env vars)
- What Airflow's core components are (scheduler, webserver, metadata DB)
- How a DAG is just a Python file that Airflow picks up automatically
- The difference between *writing* a pipeline and *scheduling* one

---

## Definition of Done

The project is complete when I can check every box:

- [ ] Airflow is running locally via Docker (webserver accessible at `localhost:8080`)
- [ ] I understand what each service in `docker-compose.yml` does and *why* it's there
- [ ] A DAG with 2–3 tasks exists as a `.py` file in the `dags/` folder
- [ ] The DAG runs successfully from the Airflow UI (green tasks, no errors)
- [ ] I can trigger it manually and see logs per task
- [ ] I can break it on purpose (e.g. fail a task) and understand what the UI shows me