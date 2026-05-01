FROM python:3.12-slim

WORKDIR /app

# Install uv (Rust-based package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency files and install
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Collect static files (if using whitenoise or similar)
# RUN uv run python manage.py collectstatic --noinput

EXPOSE 8000

# Run migrations and start gunicorn (production server)
CMD ["sh", "-c", "uv run python manage.py migrate && uv run gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
