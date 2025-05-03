# Use a slim Python base image for a smaller footprint
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir colorama>=0.4.6

# Ensure the backburner package is installed
RUN pip install .

# Command to run the Backburner CLI
ENTRYPOINT ["python", "-m", "backburner"]

# Default command (interactive mode)
CMD []
