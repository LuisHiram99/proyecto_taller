# Build stage
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client for health checks
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini .
COPY config/ config/
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set Python path to include src directory
ENV PYTHONPATH=/app/src

# Expose the port FastAPI runs on
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]