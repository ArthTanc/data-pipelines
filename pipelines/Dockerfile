FROM apache/airflow:slim-3.2.2-python3.12

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Point uv at the system Python environment (installed by the base image)
ENV UV_PROJECT_ENVIRONMENT=/home/airflow/.local

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock ./

# Install only production deps; airflow itself is already in the image
RUN uv sync --frozen --no-dev --inexact --no-install-project

# Copy DAGs (task-outputs is mounted as a volume at runtime)
COPY dags/ dags/
