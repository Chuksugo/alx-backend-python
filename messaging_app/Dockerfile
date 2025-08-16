# Use Python 3.10 as base image
FROM python:3.10

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies for MySQL client
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django default port (used for runtime mapping)
EXPOSE 8000

# Start Django server on all interfaces (0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
