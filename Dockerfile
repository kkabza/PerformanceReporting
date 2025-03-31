FROM python:3.9-slim

# Set build arguments and environment variables
ARG BUILD_VERSION=BUILD-20250331-dev
ENV BUILD_VERSION=$BUILD_VERSION
ENV FLASK_APP=app.py
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_RUN_PORT=8080

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p instance/logs build_reports

# Add build version comment to indicate the version
RUN echo "# Build version: $BUILD_VERSION" >> app.py

# Expose port
EXPOSE 8080

# Run pre-build tests and ensure reports are generated
RUN python run.py pre-build

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1 