FROM python:3.12-slim

WORKDIR /app

# Install uv (Rust-based package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --python 3.12 --path /app/.venv

# Copy application code
COPY . .

# Debug: Check where gunicorn is installed
RUN /app/.venv/bin/which gunicorn || echo "gunicorn not found in .venv/bin"
RUN ls -la /app/.venv/bin/ | grep -i gunicorn || echo "No gunicorn in bin"

# Create start script - use full paths
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo 'echo "Running migrations..."' >> /app/start.sh && \
    echo '/app/.venv/bin/python manage.py migrate' >> /app/start.sh && \
    echo 'echo "Starting gunicorn on port ${PORT:-8000}..."' >> /app/start.sh && \
    echo '/app/.venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile -' >> /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
