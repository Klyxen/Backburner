# Use a slim Python base image for a smaller footprint
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only the necessary files for dependency installation first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Install the Backburner package
RUN pip install .

# Set the entry point for the Backburner CLI
ENTRYPOINT ["python", "-m", "backburner"]

# Default command (interactive mode)
CMD []
