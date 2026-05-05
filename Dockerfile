# Use an official Python runtime as a parent image (Force Rebuild: 2026-03-14)
# Build Buster: 1533
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for pyswisseph and general builds
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 10000 available to the world outside this container
EXPOSE 10000

# Define environment variable for the port
ENV PORT=10000

# Run gunicorn to serve the app
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
