# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

#Install GIT
RUN apt-get update && apt-get install -y git

# Example Dockerfile snippet to update packages and dependencies
RUN apt-get update && apt-get install -y git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]

#Environment variable for GIT_PYTHON_GIT_EXECUTABLE
ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

