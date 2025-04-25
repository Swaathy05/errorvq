FROM python:3.10-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create data directory for SQLite
RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DATABASE_URL=sqlite:///data/queue_system.db

# Create and switch to a non-root user
RUN useradd -m myuser && \
    chown -R myuser:myuser /app
USER myuser

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:8080 wsgi:app 