FROM python:3.12-slim
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install uv
WORKDIR /todo_rpg
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY config.toml .
RUN uv sync --locked --no-dev
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "todo_rpg.main:app", "--host", "0.0.0.0", "--port", "8000"]