# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Update package lists and install Git
RUN apt-get update && apt-get install -y git

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]

