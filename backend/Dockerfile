FROM python:3.12-slim

WORKDIR /app

# Install uv (Rust-based package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --python 3.12 && ln -s /app/.venv/bin /app/bin

# Copy application code
COPY . .

# Create start script for better error handling
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'echo "Running migrations..."' >> /app/start.sh && \
    echo 'python manage.py migrate' >> /app/start.sh && \
    echo 'echo "Starting gunicorn on port ${PORT:-8000}..."' >> /app/start.sh && \
    echo 'gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile -' >> /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8000

# Use start script with proper PATH to venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["/app/start.sh"]
