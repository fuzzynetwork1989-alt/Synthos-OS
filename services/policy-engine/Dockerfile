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
COPY synthos_policy_engine/ ./synthos_policy_engine/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8008

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8008/health', timeout=5)"

# Run the application
CMD ["uvicorn", "synthos_policy_engine.main:app", "--host", "0.0.0.0", "--port", "8008"]