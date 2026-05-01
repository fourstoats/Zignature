FROM python:3.12-slim

WORKDIR /app

# Install uv (Rust-based package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --python 3.12

# Copy application code
COPY . .

# Create start script using 'uv run' to automatically find the venv
RUN printf '#!/bin/sh\nset -e\necho "Running migrations..."\nuv run python manage.py migrate\necho "Starting gunicorn on port ${PORT:-8000}..."\nuv run gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile -\n' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
