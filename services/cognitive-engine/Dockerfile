FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY synthos_cognitive_engine/ ./synthos_cognitive_engine/

# Expose port
EXPOSE 8005

# Run the application
CMD ["uvicorn", "synthos_cognitive_engine.main:app", "--host", "0.0.0.0", "--port", "8005"]