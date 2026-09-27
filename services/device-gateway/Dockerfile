FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY synthos_device_gateway/ ./synthos_device_gateway/

# Create logs directory
RUN mkdir -p /app/logs

# Expose ports
EXPOSE 8010 8011

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8010/health', timeout=5)"

# Run the application
CMD ["uvicorn", "synthos_device_gateway.main:app", "--host", "0.0.0.0", "--port", "8010"]